#!/bin/bash

csvformat -T $1 | linkml-convert -t ttl -o $2 -s schemas/kg.yaml -C Graph --index-slot nodes -f tsv /dev/stdin
