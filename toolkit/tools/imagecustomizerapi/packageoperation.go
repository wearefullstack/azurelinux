// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type PackageOperation struct {
	UpdateAll    bool     `yaml:"updateAll"`
	InstallLists []string `yaml:"installLists"`
	Install      []string `yaml:"install"`
	RemoveLists  []string `yaml:"removeLists"`
	Remove       []string `yaml:"remove"`
	UpdateLists  []string `yaml:"updateLists"`
	Update       []string `yaml:"update"`
}

func (o *PackageOperation) IsValid() error {
	hasInstall := len(o.Install) > 0 || len(o.InstallLists) > 0
	hasRemove := len(o.Remove) > 0 || len(o.RemoveLists) > 0
	hasUpdate := len(o.Update) > 0 || len(o.UpdateLists) > 0

	count := 0
	if o.UpdateAll {
		count += 1
	}
	if hasInstall {
		count += 1
	}
	if hasRemove {
		count += 1
	}
	if hasUpdate {
		count += 1
	}

	if count <= 0 {
		return fmt.Errorf("package operation is empty")
	}

	if count > 1 {
		return fmt.Errorf("package operation must only include one type of operation")
	}

	return nil
}
