#!/bin/bash
dest_folder=`find ~/.mozilla/firefox -type d -maxdepth 1 -name *default*`
echo $dest_folder
echo $dest_folder/lock
if [ ${#dest_folder} -gt 0 ]; then
    rm $dest_folder/lock
    rm $dest_folder/.parentlock
fi
