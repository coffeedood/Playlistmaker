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
     if [ ${filename: -5} == ".aif" ] || [ ${filename: -5} == ".aiff" ]
     then
        echo file:///Y:/1mov/"$subdir"/"${filename##*/}"
        echo file:///Y:/1mov/"$subdir"/"${filename##*/}" >>  ./"$subdir"/"${filename##*/}.m3u"
    fi
  done

done

done