// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Logic to enable/disable certain error cases

package pedantic

import "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"

var (
	// EnablePedanticMode is a flag to enable/disable pedantic mode
	enablePedanticMode bool
)

// EnablePedanticMode sets the flag to enable/disable pedantic mode
func EnablePedanticMode(enable bool) {
	enablePedanticMode = enable
}

// IsPedanticModeEnabled returns the flag to enable/disable pedantic mode
func IsPedanticModeEnabled() bool {
	return enablePedanticMode
}

// PedanticError is a function to return an error if pedantic mode is enabled,
// otherwise it returns nil
func PedanticError(potentialError error) error {
	if enablePedanticMode {
		return potentialError
	}
	return nil
}

// PedanticErrorWithWarning is a function to return an error if pedantic mode is enabled,
// otherwise it returns a warning message and nil.
func PedanticErrorWithWarning(potentialError error) error {
	if enablePedanticMode {
		return potentialError
	} else if logger.Log != nil {
		logger.Log.Warnf("Pedantic mode is disabled, but a potential error was encountered: %v", potentialError)
	}
	return nil
}
