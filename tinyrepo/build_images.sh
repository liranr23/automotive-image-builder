#!/bin/bash

d=`date "+%Y%m%d"`
AUTOSIGREPO=$1
HTMLROOT=$2

pushd $AUTOSIGREPO/osbuild-manifests

# Let's update the git repo
git pull --rebase

# Clean all all cached data
make clean
rm *.log || true
rm *.img || true
rm *.qcow2 || true
rm *.img.xz || true
rm *.qcow2.xz || true
dnf clean all
sudo dnf clean all

# Build all images
sudo make cs9-qemu-developer-regular.aarch64.qcow2 > cs9-qemu-developer-regular.aarch64.log
sudo make cs9-qemu-developer-regular.aarch64.oci.tar > cs9-qemu-developer-regular.aarch64.oci.tar.log
sudo make osbuildvm-images > osbuildvm-images.log

# Compact them
xz cs9-qemu-developer-regular.aarch64.qcow2 &
tar cfz osbuildvm-images.tar.gz _build/osbuildvm-aarch64.* &

wait

popd

# Move the images to apache
mkdir -p $HTMLROOT/images/$d
cp $AUTOSIGREPO/osbuild-manifests/*.xz  $HTMLROOT/images/$d/
cp $AUTOSIGREPO/osbuild-manifests/*.tar  $HTMLROOT/images/$d/
cp $AUTOSIGREPO/osbuild-manifests/*.tar.gz  $HTMLROOT/images/$d/

# Update the `latest` symlink
ln -nsf $d $HTMLROOT/images/latest
