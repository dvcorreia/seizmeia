package sql

import (
	"context"
	"database/sql"
	"embed"
	"fmt"

	migrate "github.com/golang-migrate/migrate/v4"
	"github.com/golang-migrate/migrate/v4/database"
	"github.com/golang-migrate/migrate/v4/database/postgres"
	"github.com/golang-migrate/migrate/v4/database/sqlite"
	"github.com/golang-migrate/migrate/v4/source/iofs"
	"golang.org/x/exp/slog"
)

//go:embed migrations/*.sql
var fs embed.FS

// version defines the current migration version. This ensures the app
// is always compatible with the version of the database.
const version = 1

// migrateSchema migrates the Postgres schema to the current version.
func migrateSchema(db *sql.DB, scheme string) error {
	sourceInstance, err := iofs.New(fs, "migrations")
	if err != nil {
		return err
	}

	var driverInstance database.Driver
	switch scheme {
	case "sqlite":
		driverInstance, err = sqlite.WithInstance(db, new(sqlite.Config))
	case "postgres", "postgresql":
		driverInstance, err = postgres.WithInstance(db, new(postgres.Config))
	default:
		return fmt.Errorf("unsuported scheme: %q", scheme)
	}

	if err != nil {
		return err
	}

	m, err := migrate.NewWithInstance("iofs", sourceInstance, scheme, driverInstance)
	if err != nil {
		return err
	}

	m.Log = migrateSlogger{
		SetVerbose: true,
	}

	err = m.Migrate(version) // current version
	if err != nil && err != migrate.ErrNoChange {
		return err
	}
	return sourceInstance.Close()
}

type migrateSlogger struct {
	SetVerbose bool
}

func (ml migrateSlogger) Printf(format string, v ...interface{}) {
	slog.LogAttrs(
		context.Background(),
		slog.LevelDebug,
		fmt.Sprintf(format, v...),
		slog.String("module", "golang-migrate"),
	)
}

// Verbose should return true when verbose logging output is wanted
func (ml migrateSlogger) Verbose() bool {
	return ml.SetVerbose
}
