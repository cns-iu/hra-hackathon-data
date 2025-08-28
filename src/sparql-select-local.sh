#!/bin/bash

JNL=$1
query=$2
output=$3

blazegraph-runner --journal=$JNL --outformat=json select $query $output.json
node ./src/sparql-json2csv.js $output.json $output
rm $output.json
