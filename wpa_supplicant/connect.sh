#!/bin/bash

ifaces=`iw dev | grep -oP "Interface \K\w+"`
# ifaces=`cat test1 | grep -oP "Interface \K\w+"`;
ifaces_len=`echo $ifaces | wc -w`;
interface="";
if [ $ifaces_len -eq 1 ] ; then
    interface=$ifaces;
    echo Using $interface;
else
    iface_arr=($ifaces);
    iface_arrlen=${#iface_arr[@]};
    echo Interface Options:;
    for i in `seq 1 $iface_arrlen`
    do
        echo $i")" ${iface_arr[(($i - 1))]};
    done
    option=1;
    read option;
    while [[ $((option)) -lt 1 ]] || [[ $((option)) -gt $iface_arrlen ]];
    do
        echo Invalid Option, try again;
        read option;
    done
    interface=${iface_arr[$((option - 1))]};
    echo Chose $option")" $interface;
fi

sudo ip link set $interface down
sudo ip link set $interface up
echo SSID Options:
ssids=`sudo iw $interface scan | grep -oP "SSID: \K.+" | head -n10`;
ssid_arr=($ssids);
ssid_len=${#ssid_arr[@]};
for i in `seq 1 $ssid_len`
do
    echo $i")" ${ssid_arr[((i - 1))]};
done

option=1;
read option;
while [[ $((option)) -lt 1 ]] || [[ $((option)) -gt $ssid_len ]];
do
    echo Invalid Option, try again;
    read option;
done

ssid=${ssid_arr[$((option - 1))]};
echo Chose $option")" $ssid;

has_info=`cat /etc/wpa_supplicant.conf | grep $ssid | wc -m`
if [[ $((has_info)) -eq 0 ]]; then
    sudo wpa_passphrase $ssid >> /etc/wpa_supplicant/wpa_supplicant.conf;
fi

sudo wpa_supplicant -B -D nl80211,wext -i $interface -c /etc/wpa_supplicant/wpa_supplicant.conf;
sudo dhclient $interface;
ping 8.8.8.8;
