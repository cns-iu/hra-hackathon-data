#!/bin/bash

gen-project -d schemas/generated/ schemas/kg.yaml
linkml generate erdiagram schemas/kg.yaml -f markdown > schemas/generated/mermaid.md
linkml generate erdiagram schemas/kg.yaml -f mermaid > schemas/generated/mermaid.mmd
