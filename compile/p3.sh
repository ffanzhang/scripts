#!/bin/bash
DIR="${BASH_SOURCE%/*}"
source $DIR/create_test_file_if_missing.sh
p3() {
    create_test_file_if_missing $1
    test -f $1.py && time python3 $1.py < $1.in;
}

p3 $1
