#!/bin/bash
set -e
source constants.sh

CLEAN=$1

echo Run started on $(date)...
echo
for f in scripts/??-*.sh
do
  echo ">>" Running $f...
  time bash $f $CLEAN
  echo
done

echo
echo Run finished on $(date)
