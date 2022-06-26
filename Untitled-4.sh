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
  for filename in [0-9] in "$subdir"/*; do
     if [[ $filename =~ ^[0-9]+[[:blank:]]+(.+) ]] ; then
        # display original file name
        echo "< $filename"
        # grab the rest of the filename from
        # the regex capture group
        newname="${BASH_REMATCH[1]}"
        echo "> $newname"
        # uncomment to move
        echo file:///Y:/1mov/"$subdir"/"${filename##*/}"
        echo file:///Y:/1mov/"$subdir"/"${filename##*/}" >>  ./"$subdir"/"${filename##*/}.m3u"
    fi
  done

done

done