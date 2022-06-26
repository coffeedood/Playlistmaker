#!/bin/bash
#
# bash script to create playlist files in music subdirectories
#
# Steve Carlson (stevengcarlson@gmail.com)
PWD=$(pwd)
find . -type d |
while read subdir
do
  rm -f "$subdir"/*.m3u
  
  echo "Processing $subdir"
  for filename in "$subdir"/*; do
    if [ "${filename: -4}" == ".aif" ]
    then
     for filename in [0-9]* ; do
    # only process start start with a number
    # followed by one or more space characters
    if [[ $file =~ ^[0-9]+[[:blank:]]+(.+) ]] ; then
        # display original file name
        echo "< $file"
        # grab the rest of the filename from
        # the regex capture group
        newname="${BASH_REMATCH[1]}"
        echo "> $newname"
        # uncomment to move
        # mv "$file" "$newname"
    fi
    fi
  done

done