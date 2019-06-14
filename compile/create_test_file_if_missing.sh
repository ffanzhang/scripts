#!/bin/bash
create_test_file_if_missing() {
    if ! [ -f $1.in ]; then
        touch $1.in;
    fi
}

