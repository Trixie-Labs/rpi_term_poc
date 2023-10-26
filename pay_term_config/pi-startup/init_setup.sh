#!/bin/bash

########
# Add hostapd dnsmasq for host network
########

# Update the package list and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y

# Install required software
sudo apt-get install hostapd dnsmasq -y

# Configure hostapd
sudo cat <<EOL > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=RP1
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=RP12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOL

# Configure dnsmasq
sudo cat <<EOL > /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOL

# Configure startup script
sudo cat <<EOL > /etc/sytemd/system/startup_script.sh
[Unit]
Description=Custom startup script
Requires=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash /home/vitor/pay_term_config/pi-startup/startup_script.sh

[Install]
WantedBy=multi-user.target
EOL

# Enable startup_script
sudo systemctl enable hostapd