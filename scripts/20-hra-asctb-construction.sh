#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

ENDPOINT="https://lod.humanatlas.io/sparql"

for RQ in queries/construction/hra-asctb/*.rq; do
  OUT=$INPUT_DIR/$(basename -s .rq $RQ).csv
  ./src/sparql-select.sh $ENDPOINT $RQ | csvformat > $OUT
done
