package buildinfo

import (
	"runtime"

	"golang.org/x/exp/slog"
)

// BuildInfo represents all available build information.
type BuildInfo struct {
	Version    string `json:"version"`
	CommitHash string `json:"commit_hash"`
	BuildDate  string `json:"build_date"`
	GoVersion  string `json:"go_version"`
	Os         string `json:"os"`
	Arch       string `json:"arch"`
	Compiler   string `json:"compiler"`
}

// New returns all available build information.
func New(version string, commitHash string, buildDate string) BuildInfo {
	return BuildInfo{
		Version:    version,
		CommitHash: commitHash,
		BuildDate:  buildDate,
		GoVersion:  runtime.Version(),
		Os:         runtime.GOOS,
		Arch:       runtime.GOARCH,
		Compiler:   runtime.Compiler,
	}
}

// Fields returns a map with the build information.
func (bi BuildInfo) Fields() map[string]interface{} {
	return map[string]interface{}{
		"version":     bi.Version,
		"commit_hash": bi.CommitHash,
		"build_date":  bi.BuildDate,
		"go_version":  bi.GoVersion,
		"os":          bi.Os,
		"arch":        bi.Arch,
		"compiler":    bi.Compiler,
	}
}

// LogValue implements slog.LogValuer.
// It returns a group containing the fields of BuildInfo.
func (bi BuildInfo) LogValue() slog.Value {
	return slog.GroupValue(
		slog.String("version", bi.Version),
		slog.String("commit_hash", bi.CommitHash),
		slog.String("build_date", bi.BuildDate),
		slog.String("go_version", bi.GoVersion),
		slog.String("os", bi.Os),
		slog.String("arch", bi.Arch),
		slog.String("compiler", bi.Compiler),
	)
}
