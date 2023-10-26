
#!/bin/bash

# Disable the hotspot
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

# Remove config for static IP for wlan0
sudo sed '/interface wlan0/,/nohook wpa_supplicant/d' /etc/dhcpcd.conf > dhcpcd.txt
sudo mv dhcpcd.txt /etc/dhcpcd.conf

# Add network settings
sudo sed  '/^network={/,/^}$/d' /etc/wpa_supplicant/wpa_supplicant.conf > wifi_temp.txt
sudo cat wifi_temp.txt > /etc/wpa_supplicant/wpa_supplicant.conf
sudo cat /home/vitor/pay_term_config/settings.txt >> /etc/wpa_supplicant/wpa_supplicant.conf

# Restore the original network configuration
sudo systemctl enable dhcpcd
sudo systemctl restart dhcpcd
