# Clean initramfs dependencies
rpm -e --noscripts initramfs
rpm -e dracut procps-ng grubby findutils cpio gzip azurelinux-rpm-macros libxkbcommon xkeyboard-config