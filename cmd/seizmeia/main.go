package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/dvcorreia/seizmeia/internal/platform/buildinfo"
	"github.com/dvcorreia/seizmeia/web"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"

	"github.com/pkg/errors"
	"github.com/spf13/pflag"
	"github.com/spf13/viper"
	"golang.org/x/exp/slog"
	"golang.org/x/sync/errgroup"
)

// Provisioned by ldflags
var (
	version    string
	commitHash string
	buildDate  string
)

const seizmeiaAscciFmt = ".~~~~.\ni====i_\n|cccc|_)\n|cccc|   %s\n`-==-'\n"

const (
	// It identifies the application itself, the actual instance needs to be identified via environment
	// and other details.
	appName = "seizmeia"

	// friendlyAppName is the visible name of the application.
	friendlyAppName = "Seizmeia: A credit management tool for a beer tap"
)

func main() { //nolint:funlen,gocyclo
	v, f := viper.New(), pflag.NewFlagSet(appName, pflag.ExitOnError)

	configure(v, f)

	f.String("config", "", "Configuration file")
	f.Bool("version", false, "Show version information")

	_ = f.Parse(os.Args[1:])

	if v, _ := f.GetBool("version"); v {
		fmt.Printf("%s version %s (%s) built on %s\n", friendlyAppName, version, commitHash, buildDate)

		os.Exit(0)
	}

	if c, _ := f.GetString("config"); c != "" {
		v.SetConfigFile(c)
	}

	// Attach command line flags to viper
	if err := v.BindPFlags(f); err != nil {
		panic(errors.Wrap(err, "setup: could not bind pflags"))
	}

	err := v.ReadInConfig()
	_, configFileNotFound := err.(viper.ConfigFileNotFoundError)

	if err != nil && !configFileNotFound {
		panic(errors.Wrap(err, "failed to read configuration"))
	}

	var config configuration
	if err := v.Unmarshal(&config); err != nil {
		panic(errors.Wrap(err, "failed to unmarshal config file"))
	}

	if err := config.Process(); err != nil {
		panic(errors.Wrap(err, "could not post-process config"))
	}

	fmt.Printf(seizmeiaAscciFmt, friendlyAppName)

	// Setup logger
	logger := config.Log.NewSlog().With(
		slog.String("app", appName),
	)

	slog.SetDefault(logger)

	if configFileNotFound {
		logger.Warn("configuration file not found")
	}

	if err := config.Validate(); err != nil {
		logger.Error("invalid service configuration", "err", err)

		os.Exit(3) //nolint:gomnd
	}

	buildInfo := buildinfo.New(version, commitHash, buildDate)

	logger.Info("hello, world!", "buildInfo", buildInfo)

	// Setup context cancellation for graceful shutdown
	ctx, _ := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)

	errg, ctx := errgroup.WithContext(ctx)

	// Set up http public API server
	{
		logger := logger.With(
			slog.String("module", "api"),
			slog.String("transport", "http"),
		)

		r := chi.NewRouter()

		r.Use(middleware.RequestID)
		r.Use(middleware.Recoverer)

		r.Mount("/api/buildinfo", buildinfo.HTTPHandler(buildInfo))

		r.NotFound(web.SPAHandler)

		httpServer := http.Server{
			Addr:    ":8000",
			Handler: r,
		}

		// Close server on context cancelation
		errg.Go(func() error {
			<-ctx.Done()

			ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()

			if err := httpServer.Shutdown(ctx); err != nil {
				logger.Error("could not close server", "err", err)
			}
			return nil
		})

		errg.Go(func() error {
			err := httpServer.ListenAndServe()
			if err != http.ErrServerClosed {
				return err
			}
			return nil
		})

		logger.Info("server listenning! 🎉", slog.String("addr", httpServer.Addr))
	}

	if err := errg.Wait(); err != nil {
		logger.Error("service closed with error", "err", err)
		return
	}

	logger.Info("shutting down gracefully 👋")
}
