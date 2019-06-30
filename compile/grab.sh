#!/bin/bash
DIR="${BASH_SOURCE%/*}"
source $DIR/create_test_file_if_missing.sh


while getopts "hou" arg; do
  case $arg in
    h)
      echo "Usage: grab [-hou | filename]";
      ;;
    o)
      ls ~/.local/bin/src;
      ;;
    u)
      pushd ~/.local/bin/src; \
      git stash branch master; \
      git pull origin master; \
      pushd ~/.local/bin/kattis-cli; \
      git stash branch master; \
      git pull origin master; \
      popd;
      popd;
      ;;
  esac
done

shift $(($OPTIND - 1))

for item in `ls ~/.local/bin/src | grep -i $@`
do
    cp ~/.local/bin/src/$item .
done
