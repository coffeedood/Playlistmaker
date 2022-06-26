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
  for file in "$subdir"/*; do
     filename=$(basename "$file"| sed "s/.aiff\?//")
     if [[ "$filename" =~ ^[0-9]+[[:blank:]]+(.+) ]] ; then
        # display original file name
        # grab the rest of the file from
        # the regex capture group
        newname="${BASH_REMATCH[1]}"
        # uncomment to move
        echo file:///Y:/1music/"$subdir"/"${file##*/}" ./"$subdir"/"${newname}.m3u"
        echo file:///Y:/1music/"$subdir"/"${file##*/}" >>  ./"$subdir"/"${newname}.m3u"
    fi
  done

done