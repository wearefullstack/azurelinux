// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package that assists with attach and detaching a loopback device cleanly.
package safeloopback

import (
	"errors"
	"fmt"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

type Loopback struct {
	devicePath              string
	diskFilePath            string
	diskIdMaj               string
	diskIdMin               string
	isAttached              bool
	createdPartitionDevices []string
}

func NewLoopback(diskFilePath string) (*Loopback, error) {
	loopback := &Loopback{
		diskFilePath: diskFilePath,
	}

	err := loopback.newLoopbackHelper()
	if err != nil {
		loopback.Close()
		return nil, err
	}

	return loopback, nil
}

func (l *Loopback) newLoopbackHelper() error {
	// Try to create the mount.
	devicePath, err := diskutils.SetupLoopbackDevice(l.diskFilePath)
	if err != nil {
		return err
	}

	l.devicePath = devicePath
	l.isAttached = true

	// Get the disk's IDs.
	maj, min, err := diskutils.GetDiskIds(l.devicePath)
	if err != nil {
		return err
	}

	l.diskIdMaj = maj
	l.diskIdMin = min

	// Ensure all the partitions have finished populating.
	err = diskutils.WaitForDevicesToSettle()
	if err != nil {
		return err
	}

	// Populate the partitions manually if needed (e.g. we are running in a container).
	err = l.ensurePartitionsPopulated()
	if err != nil {
		return err
	}

	return nil
}

func (l *Loopback) DevicePath() string {
	return l.devicePath
}

func (l *Loopback) DiskFilePath() string {
	return l.diskFilePath
}

func (l *Loopback) Close() {
	err := l.close(true /*async*/)
	if err != nil {
		logger.Log.Warnf("failed to close loopback: %s", err)
	}
}

func (l *Loopback) CleanClose() error {
	return l.close(false /*async*/)
}

func (l *Loopback) close(async bool) error {
	if l.isAttached {
		err := diskutils.DetachLoopbackDevice(l.devicePath)
		if err != nil {
			return err
		}

		l.isAttached = false
	}

	err := l.removePopulatedPartitions()
	if err != nil {
		return err
	}

	if !async {
		// The `losetup --detach` call happens asynchronously.
		// So, need to wait for it to complete.
		err := diskutils.WaitForLoopbackToDetach(l.devicePath, l.diskFilePath)
		if err != nil {
			return err
		}

		err = diskutils.BlockOnDiskIOByIds(l.devicePath, l.diskIdMaj, l.diskIdMin)
		if err != nil {
			return err
		}
	}

	return nil
}

// Checks if the partitions' block devices have been created and if they haven't, it creates then manually. This is
// useful inside containers that don't have the host's /dev mounted, since a container's namespaced /dev doesn't receive
// udev events.
func (l *Loopback) ensurePartitionsPopulated() error {
	partitions, err := diskutils.GetDiskPartitions(l.devicePath)
	if err != nil {
		return err
	}

	for _, partition := range partitions {
		exists, err := file.PathExists(partition.Path)
		if err != nil {
			return fmt.Errorf("failed to check if partition device (%s) exists:\n%w", partition.Path, err)
		}

		if !exists {
			err := createPartitionDevice(partition)
			if err != nil {
				return fmt.Errorf("failed to create partition device (%s):\n%w", partition.Path, err)
			}

			l.createdPartitionDevices = append(l.createdPartitionDevices, partition.Path)
		}
	}

	return nil
}

func createPartitionDevice(partition diskutils.PartitionInfo) error {
	maj, min, err := diskutils.ParseMajMin(partition.MajMin)
	if err != nil {
		return err
	}

	err = shell.ExecuteLive(true /*squashErrors*/, "mknod", partition.Path, "b", maj, min)
	if err != nil {
		return fmt.Errorf("mknod failed:\n%w", err)
	}

	return nil
}

func (l *Loopback) removePopulatedPartitions() error {
	errs := []error(nil)

	remainingPartitions := []string(nil)

	for _, partition := range l.createdPartitionDevices {
		logger.Log.Debugf("Removing manually created partition device (%s)", partition)
		err := os.Remove(partition)
		if err != nil {
			err = fmt.Errorf("failed to remove manually created partition device (%s):\n%w", partition, err)
			errs = append(errs, err)
			remainingPartitions = append(remainingPartitions, partition)
		}
	}

	l.createdPartitionDevices = remainingPartitions

	if len(errs) > 0 {
		err := errors.Join(errs...)
		return err
	}

	return nil
}
