// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

const (
	tdnfInstallPrefix = "Installing/Updating: "
	tdnfRemovePrefix  = "Removing: "
)

var (
	tdnfTransactionError = regexp.MustCompile(`^Found \d+ problems$`)
)

func addRemoveAndUpdatePackages(buildDir string, baseConfigPath string, config *imagecustomizerapi.OS,
	imageChroot *safechroot.Chroot, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Note: The 'validatePackageLists' function read the PackageLists files and merged them into the inline package
	// lists.
	needRpmsSources := needsRpmSources(config)

	var mounts *rpmSourcesMounts
	if needRpmsSources {
		// Mount RPM sources.
		mounts, err = mountRpmSources(buildDir, imageChroot, rpmsSources, useBaseImageRpmRepos)
		if err != nil {
			return err
		}
		defer mounts.close()

		// Refresh metadata.
		err = refreshTdnfMetadata(imageChroot)
		if err != nil {
			return err
		}
	}

	for _, packageOperation := range config.PackageOperations {
		if len(packageOperation.Remove) > 0 {
			err = removePackages(packageOperation.Remove, imageChroot)
			if err != nil {
				return err
			}
		}

		if packageOperation.UpdateAll {
			err = updateAllPackages(imageChroot)
			if err != nil {
				return err
			}
		}

		if len(packageOperation.Install) > 0 {
			logger.Log.Infof("Installing packages: %v", packageOperation.Install)
			err = installOrUpdatePackages("install", packageOperation.Install, imageChroot)
			if err != nil {
				return err
			}
		}

		if len(packageOperation.Update) > 0 {
			logger.Log.Infof("Updating packages: %v", packageOperation.Update)
			err = installOrUpdatePackages("update", packageOperation.Update, imageChroot)
			if err != nil {
				return err
			}
		}
	}

	// Unmount RPM sources.
	if mounts != nil {
		err = mounts.close()
		if err != nil {
			return err
		}
	}

	return nil
}

func needsRpmSources(config *imagecustomizerapi.OS) bool {
	for _, packageOperation := range config.PackageOperations {
		if packageOperation.UpdateAll || len(packageOperation.Install) > 0 || len(packageOperation.Update) > 0 {
			return true
		}
	}

	return false
}

func refreshTdnfMetadata(imageChroot *safechroot.Chroot) error {
	tdnfArgs := []string{
		"-v", "check-update", "--refresh", "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := imageChroot.UnsafeRun(func() error {
		return shell.NewExecBuilder("tdnf", tdnfArgs...).
			LogLevel(logrus.DebugLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	})
	if err != nil {
		return fmt.Errorf("failed to refresh tdnf repo metadata:\n%w", err)
	}
	return nil
}

func collectPackagesList(baseConfigPath string, packageLists []string, packages []string) ([]string, error) {
	var err error

	// Read in the packages from the package list files.
	var allPackages []string
	for _, packageListRelativePath := range packageLists {
		packageListFilePath := file.GetAbsPathWithBase(baseConfigPath, packageListRelativePath)

		var packageList imagecustomizerapi.PackageList
		err = imagecustomizerapi.UnmarshalYamlFile(packageListFilePath, &packageList)
		if err != nil {
			return nil, fmt.Errorf("failed to read package list file (%s):\n%w", packageListFilePath, err)
		}

		allPackages = append(allPackages, packageList.Packages...)
	}

	allPackages = append(allPackages, packages...)
	return allPackages, nil
}

func removePackages(allPackagesToRemove []string, imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Removing packages: %v", allPackagesToRemove)

	tdnfRemoveArgs := []string{
		"-v", "remove", "--assumeyes", "--disablerepo", "*",
	}

	tdnfRemoveArgs = append(tdnfRemoveArgs, allPackagesToRemove...)

	err := callTdnf(tdnfRemoveArgs, tdnfRemovePrefix, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to remove packages (%v):\n%w", allPackagesToRemove, err)
	}

	return nil
}

func updateAllPackages(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Updating all packages")

	tdnfUpdateArgs := []string{
		"-v", "update", "--nogpgcheck", "--assumeyes", "--cacheonly",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := callTdnf(tdnfUpdateArgs, tdnfInstallPrefix, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to update all packages:\n%w", err)
	}

	return nil
}

func installOrUpdatePackages(action string, packages []string, imageChroot *safechroot.Chroot) error {
	// Create tdnf command args.
	// Note: When using `--repofromdir`, tdnf will not use any default repos and will only use the last
	// `--repofromdir` specified.
	tdnfArgs := []string{
		"-v", action, "--nogpgcheck", "--assumeyes", "--cacheonly",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	tdnfArgs = append(tdnfArgs, packages...)

	err := callTdnf(tdnfArgs, tdnfInstallPrefix, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to %s packages (%v):\n%w", action, packages, err)
	}

	return nil
}

func callTdnf(tdnfArgs []string, tdnfMessagePrefix string, imageChroot *safechroot.Chroot) error {
	seenTransactionErrorMessage := false
	stdoutCallback := func(line string) {
		if !seenTransactionErrorMessage {
			// Check if this line marks the start of a transaction error message.
			seenTransactionErrorMessage = tdnfTransactionError.MatchString(line)
		}

		if seenTransactionErrorMessage {
			// Report all of the transaction error message (i.e. the remainder of stdout) to WARN.
			logger.Log.Warn(line)
		} else if strings.HasPrefix(line, tdnfMessagePrefix) {
			logger.Log.Debug(line)
		} else {
			logger.Log.Trace(line)
		}
	}

	return imageChroot.UnsafeRun(func() error {
		return shell.NewExecBuilder("tdnf", tdnfArgs...).
			StdoutCallback(stdoutCallback).
			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	})
}

func isPackageInstalled(imageChroot *safechroot.Chroot, packageName string) bool {
	err := imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLive(true /*squashErrors*/, "rpm", "-qi", packageName)
	})
	if err != nil {
		return false
	}
	return true
}
