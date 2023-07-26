package main

import (
	"fmt"
	"strings"

	"github.com/dvcorreia/seizmeia/internal/platform/log"

	"github.com/spf13/pflag"
	"github.com/spf13/viper"
)

// configuration holds any kind of configuration that comes from the outside world and
// is necessary for running the application.
type configuration struct {
	// Log configuration
	Log log.Config
}

// configure configures some defaults in the Viper instance.
func configure(v *viper.Viper, _ *pflag.FlagSet) {
	// Configuration file settings
	v.SetConfigName("config")
	v.SetConfigType("yaml")

	v.AddConfigPath(fmt.Sprintf("/etc/%s/", appName))
	v.AddConfigPath(fmt.Sprintf("$HOME/.%s", appName))
	v.AddConfigPath(".")

	// Environment variable settings
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_", "-", "_"))
	v.SetEnvPrefix(appName)
	v.AllowEmptyEnv(true)
	v.AutomaticEnv()
}

// Process post-processes configuration after loading it.
func (c *configuration) Process() error {
	return nil
}

// Validate validates the configuration.
func (c configuration) Validate() error {
	return nil
}
