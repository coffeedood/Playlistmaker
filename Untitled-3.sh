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
  
  #echo "Processing $subdir"
  for filename in "$subdir"/*; do
     if [ "${filename: -4}" == ".aif" ] || [ "${filename: -5}" == ".aiff" ]
     then
     if [[ $filename =~ ^[0-9]+[[:blank:]]+(.+) ]] ; then
        # display original file name
        # grab the rest of the filename from
        # the regex capture group
        newname="${BASH_REMATCH[1]}"
        # uncomment to move
        # mv "$file" "$newname"
       name=$(basename "$newname" .aif)
       echo file:///Y:/1mov/"$subdir"/"${filename##*/}"
       echo file:///Y:/1mov/"$subdir"/"${filename##*/}" >>  ./"$subdir"/"$newname.m3u"
    fi
    fi
done
done