package log

import (
	"os"
	"strings"

	"golang.org/x/exp/slog"
)

const (
	LogFormatText = "text"
	LogFormatJSON = "json"
)

// Config holds details necessary for logging.
type Config struct {
	// Level is the minimum log level that should appear on the output.
	Level string

	// Format specifies the output log format.
	// Accepted values are: json, text
	Format string
}

func (c Config) NewSlog() *slog.Logger {
	opts := slog.HandlerOptions{
		Level: SlogLevel(c.Level),
	}

	var h slog.Handler

	switch c.Format {
	case LogFormatText:
		h = slog.NewTextHandler(os.Stdout, &opts)
	case LogFormatJSON:
		h = slog.NewJSONHandler(os.Stdout, &opts)
	default:
		h = slog.NewJSONHandler(os.Stdout, &opts)
	}

	return slog.New(h)
}

// SlogLevel converts a string level to the slog level.
func SlogLevel(level string) slog.Level {
	switch strings.ToLower(level) {
	case "debug":
		return slog.LevelDebug
	case "info":
		return slog.LevelInfo
	case "warn":
		return slog.LevelWarn
	case "error":
		return slog.LevelError
	default:
		return slog.LevelInfo
	}
}
