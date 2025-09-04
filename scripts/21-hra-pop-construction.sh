#!/bin/bash
source constants.sh
shopt -s extglob

if [ "$CLEAN" == "true" ]; then
  set -ev

  if [ ! -e raw-data/hra-pop-blazegraph.jnl ]; then
    mkdir -p raw-data
    curl -o raw-data/hra-pop-blazegraph.jnl http://cdn.humanatlas.io/dvc/hra-pop/raw-data/v1.0/blazegraph.jnl
  fi

  time src/sparql-select-local.sh \
    raw-data/hra-pop-blazegraph.jnl \
    queries/construction/hra-pop/hra-pop-kidney-data.rq \
    input-csvs/hra-pop-kidney-data.csv

  ./src/sql-select.sh queries/construction/hra-pop/hra-pop-kidney-nodes.sql \
    input-csvs/hra-pop-kidney-data.csv \
    input-csvs/hra-pop-kidney-nodes.csv

  ./src/sql-select.sh queries/construction/hra-pop/hra-pop-kidney-edges.sql \
    input-csvs/hra-pop-kidney-data.csv \
    input-csvs/hra-pop-kidney-edges.csv
fi
