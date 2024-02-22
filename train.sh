#!/bin/bash

# shellcheck disable=SC1073
cwd=$(pwd)
poems=$cwd'/data/poems/'
#amount=$(ls $poems | wc -l)


# shellcheck disable=SC2045

path_to_poems=$cwd'/data/all_poems.csv'
# shellcheck disable=SC2154
$(cd lyrics-generator_copy && python3 -m lyrics.train --songdata-file $path_to_poems --artists "*")

#echo $cwd