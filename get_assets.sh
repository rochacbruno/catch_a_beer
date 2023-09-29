#!/bin/bash

# GitHub URL for the assets.tar.gz file
github_url="https://github.com/rochacbruno/catch_a_beer/raw/main/src/catch_a_beer/assets.tar.gz"

# Destination directory for extraction
destination_dir="src/catch_a_beer"

# Check if the destination directory exists; if not, create it
if [ ! -d "$destination_dir" ]; then
    mkdir -p "$destination_dir"
fi

# Download the assets.tar.gz file using curl
curl -L -o assets.tar.gz "$github_url"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download successful."

    # Extract the downloaded tar.gz file to the destination directory
    tar -xzvf assets.tar.gz -C "$destination_dir"

    # Clean up: remove the downloaded tar.gz file
    rm assets.tar.gz

    echo "Extraction completed."
else
    echo "Download failed. Please check the URL or your internet connection."
fi

