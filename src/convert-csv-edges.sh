#!/bin/bash

csvformat -T $1 | linkml-convert -t ttl -o $2 -s schemas/kg.yaml -C Graph --index-slot edges -f tsv /dev/stdin
