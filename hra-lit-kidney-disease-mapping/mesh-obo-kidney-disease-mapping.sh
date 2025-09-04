#!/bin/bash

# Clean up the raw data
# grep -v ",,,,," mesh-obo-kidney-disease-mapping.sssom.csv | csvcut -C accuracy > mesh-obo-kidney-disease-mapping.fixed.sssom.csv

# Combine metadata and data into a final sssom.tsv file
sssom parse -m mesh-obo-kidney-disease-mapping.yml -I tsv -o mesh-obo-kidney-disease-mapping.sssom.tsv mesh-obo-kidney-disease-mapping.csv

# Validate the sssom.tsv file
sssom validate mesh-obo-kidney-disease-mapping.sssom.tsv

# Convert to RDF/turtle
sssom convert mesh-obo-kidney-disease-mapping.sssom.tsv -O owl -o mesh-obo-kidney-disease-mapping.sssom.ttl
