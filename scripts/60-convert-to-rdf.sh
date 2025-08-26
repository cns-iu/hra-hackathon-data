#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

mkdir -p $OUTPUT_DIR/ttl

for CSV in $INPUT_DIR/*-nodes.csv; do
  TTL=$OUTPUT_DIR/ttl/$(basename -s .csv $CSV).ttl
  ./src/convert-csv-nodes.sh $CSV $TTL
done
