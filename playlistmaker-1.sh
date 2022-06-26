#!/bin/bash
#
# bash script to create playlist files in music subdirectories
#
# Steve Carlson (stevengcarlson@gmail.com)
set -x
PWD=$(pwd)
find . -type d |
while read subdir
do
  rm -f "$subdir"/*.m3u
  
  echo "$(basename "$subdir")"
  if [ "$(basename "$subdir")" == "VIDEO_TS" ]
  then
  
  parentdir=$(builtin cd "$subdir"/..; pwd)
  parentname="$(basename "$parentdir")"
  echo $subdir $parentdir $parentname
  echo file:///Y:/1mov/"$subdir"/"${filename##*/}";
  echo file:///Y:/1mov/"$subdir"/"VIDEO_TS.IFO" >>  /mnt/c/playlists3/"$parentname.m3u"

  elif  [ -f "$subdir/VIDEO_TS.IFO" ]
  then
  maindir="$(basename "$subdir")"
  echo file:///Y:/1mov/"$subdir"/"VIDEO_TS.IFO" >>  /mnt/c/playlists3/"$maindir.m3u"
  fi
done