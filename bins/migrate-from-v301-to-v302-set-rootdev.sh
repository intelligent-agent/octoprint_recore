#!/bin/bash

if [ ! -b /dev/sda2 ]; then
  echo "Could not find the root partition in the USB drive"
  echo "Make sure you have a USB drive inserted with Refactor v3.0.2-RC4 or newer"
  exit 1
fi
mkdir -p /tmp/usb
mount /dev/sda2 /tmp/usb

if [ ! -f /tmp/usb/etc/refactor.version ] ; then
  echo "could not find a valid image installed on USB drive"
  exit 1
fi

NEW_VERSION=`cat /tmp/usb/etc/refactor.version`
echo "Found USB drive with Refactor version: ${NEW_VERSION}"
echo

sync
umount /dev/sda2

echo "Running fsck"
fsck /dev/sda1
if [ ! $? ]; then
  echo "fsck /dev/sda1 did not pass check. Please make sure you have a valid image in the USB drive"
  exit 1
fi
fsck /dev/sda2
if [ ! $? ]; then
  echo "fsck /dev/sda2 did not pass check. Please make sure you have a valid image in the USB drive"
  exit 1
fi

echo
if [ ! -f /boot/armbianEnv.txt ] ; then
  echo "Could not find /boot/armbianEnv.txt"
  exit 1
fi
# Remove extraargs
KEY="^rootdev=.*$"
REPLACE="rootdev=/dev/sda2"
sed -i "s:${KEY}:${REPLACE}:g" /boot/armbianEnv.txt

# Remove extraargs
sed -i "s:extraargs=.*::g" /boot/armbianEnv.txt

echo "The file /boot/armbianEnv.txt now looks like this: "
cat /boot/armbianEnv.txt

sync
sleep 2

echo
echo "Done. Please run the command: reboot"
