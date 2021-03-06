#!/bin/bash
PWD=$(pwd)
find . -type d |
    while read subdir; do
        rm -f "$subdir"/*.m3u

        echo "Processing $subdir"
        for filename in "$subdir"/*; do
            if [ ${filename: -4} == ".aif" ] || [ ${filename: -5} == ".aiff" ]; then
                echo file:///Z:/1music/"$subdir"/"${filename##*/}"
                echo file:///Z:/1music/"$subdir"/"${filename##*/}" >>./"$subdir"/"${subdir##*/}.m3u"
            fi
        done

    done
