#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

PYTHON_SCRIPT="../src/hpo-get-nodes-and-edges.py"

python3 $PYTHON_SCRIPT