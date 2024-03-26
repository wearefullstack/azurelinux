#!/bin/bash 
echo "localpkg_gpgcheck=1" | sudo tee -a /etc/tdnf/tdnf.conf
echo "blacklist squashfs" | sudo tee -a /etc/modprobe.d/usb.conf

