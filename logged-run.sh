#!/bin/bash
source constants.sh

LOG=$OUTPUT_DIR/log.txt
rm -r $OUTPUT_DIR/*

time bash -c "time ./run.sh 2>&1" | tee $LOG
