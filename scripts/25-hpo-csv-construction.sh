#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

if [ "$1" == "--clean" ] || [ "$CLEAN" == "true" ]; then
  set -ev

  # cd HRA_HPO_integration
  # python ../src/hpo-get-nodes-and-edges.py
fi
