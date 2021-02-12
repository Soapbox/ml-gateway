#!/bin/bash

#####
##### A script which runs a single unit test.
#####

export IS_UNIT_TEST="True"

echo "###################################################"
echo "Unit test results:"
echo "###################################################"

python -m unittest --failfast $1

if [ $? -ne 0 ]; then
    echo "Unit test failed!"
    echo ""
    exit 1
fi

echo ""
echo "Done!"
