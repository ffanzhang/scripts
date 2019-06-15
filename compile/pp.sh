#!/bin/bash
DIR="${BASH_SOURCE%/*}"
source $DIR/create_test_file_if_missing.sh
pp() {
    test -f $1.py && create_test_file_if_missing $1 && time python $1.py < $1.in;
}

pp $1
