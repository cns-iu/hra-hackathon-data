#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

NAME=hra-kidney-disease-atlas
ATLAS=$OUTPUT_DIR/$NAME

FILES=$(ls input-csvs/hpo-*-{nodes,edges}.csv input-csvs/hra-pop-kidney-{nodes,edges}.csv input-csvs/hra-asctb-kidney-{nodes,edges}.csv)
for f in $FILES; do
  echo validating $(basename $f)...
  kgx validate -i csv $f
done

kgx transform -i csv -f json -o ${ATLAS}.json $FILES
kgx transform -i json -f nt -o ${ATLAS}.nt ${ATLAS}.json
kgx transform -i json -f tsv -o ${ATLAS} ${ATLAS}.json
kgx graph-summary -i json -f json -o ${ATLAS}.report.json ${ATLAS}.json

rm -f ${ATLAS}.kgx_tsv.tar.gz
tar -czf ${ATLAS}.kgx_tsv.tar.gz -C $OUTPUT_DIR ${NAME}_nodes.tsv ${NAME}_edges.tsv
