#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

OUT=$OUTPUT_DIR

node src/gen-report-markdown.js $OUT/REPORTS.md queries/reports $OUT/reports

# for file in `find $OUT -name "*.*" -size +95M`; do
#   zip -j ${file}.zip $file
#   rm $file
# done

CREATION_DATE=$(date)
echo "$CREATION_DATE" > $OUT/CREATION_DATE

node src/gen-readme.js $VERSION "$CREATION_DATE" $OUT/README.md
