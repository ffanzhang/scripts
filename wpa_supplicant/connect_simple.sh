#!/bin/bash

# sudo iw dev
interface="";
# sudo iw $interface scan 
ssid="";
sudo ip link set $interface down
sudo ip link set $interface up
sudo wpa_passphrase $ssid >> /etc/wpa_supplicant/wpa_supplicant.conf;
sudo wpa_supplicant -B -D nl80211,wext -i $interface -c /etc/wpa_supplicant/wpa_supplicant.conf;
sudo dhclient $interface;
ping 8.8.8.8;
