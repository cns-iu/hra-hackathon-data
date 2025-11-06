#!/bin/bash
source constants.sh
shopt -s extglob

if [ "$1" == "--clean" ] || [ "$CLEAN" == "true" ]; then
  set -ev

  ENDPOINT="https://lod.humanatlas.io/sparql"
  for RQ in queries/construction/hra-asctb/*.rq; do
    OUT=$INPUT_DIR/$(basename -s .rq $RQ).csv
    ./src/sparql-select.sh $ENDPOINT $RQ | csvformat > $OUT
    ./src/compact-uris-in-csv.py -i $OUT -o dummy --inplace
  done
fi
