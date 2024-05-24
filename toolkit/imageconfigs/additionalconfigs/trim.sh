# Setup the data partition
mkdir /data/overlays
mkdir -p /data/overlays/etc/upper
mkdir -p /data/overlays/etc/work

# Ensure data partition is mounted in initrd along with overlay
sed -i "s/data ext4 defaults/data ext4 defaults,x-initrd.mount/" /etc/fstab
echo "overlay /etc overlay x-initrd.mount,x-systemd.requires-mounts-for=/sysroot/data,lowerdir=/sysroot/etc,upperdir=/sysroot/data/overlays/etc/upper,workdir=/sysroot/data/overlays/etc/work 0 0" >> /etc/fstab

# Enable initrd to break into a shell
sed -i "s/rd.shell=0 rd.emergency=reboot/rd.shell=1 rd.break=pre-pivot/" /boot/grub2/grub.cfg

# Ensure overlay driver is available in initrd
echo "add_drivers+=\" overlay \"" >> /etc/dracut.conf.d/01-overlay.conf

# Regenerate initrd
dracut --force --regenerate-all --include /usr/lib/locale /usr/lib/locale

# Clean initramfs dependencies
#rpm -e --noscripts initramfs
#rpm -e dracut procps-ng grubby findutils cpio gzip azurelinux-rpm-macros libxkbcommon xkeyboard-config
