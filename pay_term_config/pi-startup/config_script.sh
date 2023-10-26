#!/bin/bash

# Configure static IP for wlan0
echo "Configure static IP for wlan0"
sudo cat <<EOL >> /etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
EOL

# Enable and start hostapd and dnsmasq
echo "Enable and start hostapd and dnsmasq"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq



