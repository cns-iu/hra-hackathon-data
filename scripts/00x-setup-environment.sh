#!/bin/bash
source constants.sh
shopt -s extglob
set -e

# Base paths
DIR="${0%/*}"
ROOT_DIR="$DIR/.."

# Parse arguments
ENV=${1:-.venv}
if [[ ! "$ENV" = /* ]]; then ENV="$ROOT_DIR/$ENV"; fi

if [ ! -e "$ENV/bin/activate" ]; then
  python3 -m venv $ENV
fi

# Install dependencies
if [ -e "$ENV/bin/activate" ]; then
  set +u # Disable in case we are running old venv versions that can't handle strict mode
  source "$ENV/bin/activate"
  set -u

  # Install python deps
  python -m pip install --upgrade pip
  python -m pip install -r "$ROOT_DIR/requirements.txt"
  python -m pip cache purge

  # Install node (latest LTS version)
  if [ ! -e "$ENV/bin/node" ]; then
    nodeenv --python-virtualenv --node lts
  fi
fi

# Install node deps
if [ ! -e "node_modules" ]; then
  npm ci
fi

# Install Blazegraph Runner
if [ ! -e "$ENV/opt/blazegraph-runner" ]; then
  mkdir -p $ENV/opt
  BR=1.7
  curl -L -o blazegraph-runner-$BR.tgz https://github.com/balhoff/blazegraph-runner/releases/download/v$BR/blazegraph-runner-$BR.tgz &&
    tar -zxf blazegraph-runner-$BR.tgz &&
    mv blazegraph-runner-$BR $ENV/opt/blazegraph-runner
  ln -s $ENV/opt/blazegraph-runner/bin/blazegraph-runner $ENV/bin/blazegraph-runner
  rm -f blazegraph-runner-$BR.tgz
fi

if [ ! -e "$ENV/bin/duckdb" ]; then
  curl -L -o duckdb_cli-linux-amd64.zip https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip &&
    unzip -qq duckdb_cli-linux-amd64.zip duckdb &&
    mv duckdb $ENV/bin/duckdb &&
    rm -f duckdb_cli-linux-amd64.zip
fi

if [ -e "$ENV/bin/activate" ]; then
  set +u # Just to be on the safe side
  deactivate
  set -u
fi
