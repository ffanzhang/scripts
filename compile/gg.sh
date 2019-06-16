#!/bin/bash
DIR="${BASH_SOURCE%/*}"
source $DIR/create_test_file_if_missing.sh
gg() {
    test -f $1.cc && g++ -g -O2 -std=c++11 $1.cc -o $1 && create_test_file_if_missing $1 && time ./$1 < $1.in;
    test -f $1.cpp && g++ -g -O2 -std=c++11 $1.cpp -o $1 && create_test_file_if_missing $1 && time ./$1 < $1.in;
    test `uname -s` == Darwin && test -f $1.cc && g++-9 -g -O2 -std=c++11 $1.cc -o $1 && create_test_file_if_missing $1 && ./$1 < $1.in;
    test `uname -s` == Darwin && test -f $1.cpp && g++-9 -g -O2 -std=c++11 $1.cpp -o $1 && create_test_file_if_missing $1 && ./$1 < $1.in;
}

gg $1
