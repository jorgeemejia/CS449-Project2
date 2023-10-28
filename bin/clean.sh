#!/bin/bash

# Unmount the primary FUSE filesystem
fusermount -u var/primary/fuse

# Wait for unmounting to complete (you can adjust the time as needed)
sleep 2

# Remove the contents of the primary FUSE and data directories
rm -r var/primary/fuse/*
rm -r var/primary/data/*

# Unmount the secondary FUSE filesystem
fusermount -u var/secondary/fuse

# Wait for unmounting to complete (you can adjust the time as needed)
sleep 2

# Remove the contents of the secondary FUSE and data directories
rm -r var/secondary/fuse/*
rm -r var/secondary/data/*

# Unmount secondary_2 FUSE filesystem
fusermount -u var/secondary_2/fuse

# Wait for unmounting to complete (you can adjust the time as needed)
sleep 2

# Remove the contents of the secondary_2 FUSE and data directories
rm -r var/secondary_2/fuse/*
rm -r var/secondary_2/data/*

echo "Contents of primary and secondary directories have been deleted."
