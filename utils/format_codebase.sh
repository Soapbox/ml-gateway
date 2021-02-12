#!/bin/bash

####
#### A convenient script to automatically format the codebase
####

echo "Formatting codebase..."

python -m black --config api/pyproject.toml "/api/"

echo ""
echo "Done!"
