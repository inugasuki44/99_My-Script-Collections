#!/bin/bash

# Path provided by the user.
path="$1"

# Prints a usage message if no path is provided.
if [ -z "$path" ]; then
        echo "Usage: ./file_checker.sh <path>"
        exit 1
fi

# Check if the path is a regular file.
if [ -f "$path" ]; then
        echo "$path is a file."
# If not a file, check if it's a directory.
elif [ -d "$path" ]; then
        echo "$path is a directory."
# If it's neither a file nor a directory, check if it exists.
else
        if [ -e "$path" ]; then
            # This handles cases like symbolic links, sockets, etc.
            echo "$path exists, but it is not a regular file or directory."
        else
            # The path does not exist.
            echo "$path does not exist."
        fi
fi
