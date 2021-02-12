#!/bin/bash

####
#### A convenient script to automatically format the codebase
####

codeformatter() {
    echo "###################################################"
    echo "Code formatter results:"
    echo "###################################################"

    python -m black --config api/pyproject.toml --check "/api/"

    if [ $? -ne 0 ]; then
        echo "Code formatter check failed!"
        echo ""
        exit 1
    fi

    echo "Code formatter check passed!"
    echo ""
}

codeformatter
