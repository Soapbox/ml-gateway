#!/bin/bash

#####
##### A script which runs the unit test.
#####

export IS_UNIT_TEST="True"

unittest() {
    echo "###################################################"
    echo "Unit test results:"
    echo "###################################################"

    for FILENAME in $(find test -iname "*.py")
    do
        python -m unittest --failfast $FILENAME

        if [ $? -ne 0 ]; then
            echo "Unit test failed!"
            echo ""
            exit 1
        fi
    done
}

unittest

echo ""
echo "Done!"
