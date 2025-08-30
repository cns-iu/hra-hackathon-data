#!/bin/bash
source constants.sh
shopt -s extglob
set -ev

DIR=$OUTPUT_DIR
JNL=$DIR/blazegraph.jnl
rm -f $JNL

HRA_ATLAS=https://purl.humanatlas.io/graph/hra-kidney-disease-atlas

# Digital Objects to import into the Blazegraph Journal
CCF=https://purl.humanatlas.io/graph/ccf
HRA=https://purl.humanatlas.io/collection/hra
HRA_API=https://purl.humanatlas.io/collection/hra-api
UBERON=https://purl.humanatlas.io/vocab/uberon
CL=https://purl.humanatlas.io/vocab/cl
HPO=https://purl.humanatlas.io/vocab/hp

DOs_TO_IMPORT="$CCF $HRA $HRA_API $UBERON $CL $HPO"

for TTL in $OUTPUT_DIR/ttl/*.ttl; do
  blazegraph-runner load --journal=$JNL "--graph=${HRA_ATLAS}" $TTL
done

# Make modifications to the KG to improve its usefulness
blazegraph-runner update --journal=$JNL queries/construction/postprocessing/reify-edges.rq
# blazegraph-runner update --journal=$JNL queries/construction/postprocessing/remove-useless-edges.rq

# Dump HRA Atlas back out to turtle format for publishing
blazegraph-runner dump --journal=$JNL "--graph=${HRA_ATLAS}" $DIR/hra-kidney-disease-atlas.ttl

# Import digital objects from HRA KG to use for querying
for DO in $DOs_TO_IMPORT; do
  # Import the Digital Object
  curl -s $DO -H "Accept: application/rdf+xml" > $DIR/digital-object.owl
  blazegraph-runner load --journal=$JNL "--graph=${DO}" $DIR/digital-object.owl
  rm -f $DIR/digital-object.owl
done
