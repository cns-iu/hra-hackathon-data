#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

for f in hra-lit-kidney-as-nodes.csv hra-lit-kidney-disease-nodes.csv hra-lit-kidney-diseases-cooccur-edges.csv; do
  rm -f input-csvs/$f
  curl -s -o input-csvs/$f https://raw.githubusercontent.com/x-atlas-consortia/hra-lit/refs/heads/main/output-data/hra-lit/v0.7.1/reports/hra-lit-kidney/$f
done
