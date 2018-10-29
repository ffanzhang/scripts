#!/bin/bash
SSH_KEYPATH=""
CUR_HOSTNAME=`hostname`
for i in `seq 1 25` 
do
    REMOTE_HOSTNAME=`printf "lin%02d" $i` 
    if [ $CUR_HOSTNAME != $REMOTE_HOSTNAME ]; then
        yes | ssh -i $SSH_KEYPATH $REMOTE_HOSTNAME 'pkill firefox'
    fi
done
