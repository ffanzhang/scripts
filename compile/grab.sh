#!/bin/bash
DIR="${BASH_SOURCE%/*}"
source $DIR/create_test_file_if_missing.sh
while getopts "ho" arg; do
  case $arg in
    h)
      echo "usage: grab ([-o] || filename)";
      exit 0;
      ;;
    o)
      ls ~/.local/bin/src;
      exit 0;
      ;;
  esac
done

for item in `ls ~/.local/bin/src | grep -i $1`
do
    cp ~/.local/bin/src/$item .
done
