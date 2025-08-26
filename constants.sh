shopt -s expand_aliases

# Set global configuration
export LANG=C.UTF-8
export PYTHONPATH=".:./src"
export GPG_TTY=$(tty)

# Load environment
if [ -e env.sh ]; then
  source env.sh
fi

export INPUT_DIR=${INPUT_DIR:-"./input-csvs"}
export OUTPUT_DIR=${OUTPUT_DIR:-"./output-data"}

mkdir -p $OUTPUT_DIR
