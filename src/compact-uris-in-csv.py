#!/usr/bin/env python3
"""
csv_compact_curie_kgx.py
Compact IRIs in one or more CSV columns into CURIEs using kgx.PrefixManager.

Usage:
  python csv_compact_curie_kgx.py -i data.csv -o data.curie.csv
  python csv_compact_curie_kgx.py -i data.csv.gz -o out.csv.gz -c subject -c object
  python csv_compact_curie_kgx.py -i data.csv -o dummy --inplace

If no -c/--column option is given, *all* columns will be compacted.
"""

import argparse
import sys
import os
import gzip
import io
import pandas as pd
from kgx.prefix_manager import PrefixManager


def open_csv(path, mode="r"):
    """Support reading/writing gzipped CSVs seamlessly."""
    if path.endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path, "rb")) if "r" in mode else gzip.open(path, "wt")
    return open(path, mode, newline="")


def compact_value(pm: PrefixManager, val: str, fallback="keep"):
    """Try to compact a URI into a CURIE using the PrefixManager."""
    if pd.isna(val) or not str(val).strip():
        return val
    try:
        curie = pm.contract(val)
        if curie and curie != val:
            return curie
        else:
            raise ValueError("unmappable")
    except Exception:
        return val if fallback == "keep" else ""


def main():
    p = argparse.ArgumentParser(
        description="Compact IRIs in CSV columns to CURIEs using KGX PrefixManager."
    )
    p.add_argument("-i", "--input", required=True, help="Input CSV (can be .gz)")
    p.add_argument("-o", "--output", required=True, help="Output CSV (can be .gz)")
    p.add_argument(
        "-c",
        "--column",
        dest="columns",
        action="append",
        help="Column name(s) to compact; if omitted, all columns will be compacted.",
    )
    p.add_argument(
        "-C",
        "--exclude",
        dest="exclude_columns",
        action="append",
        help="Column name(s) to exclude from compaction",
    )
    p.add_argument(
        "--fallback",
        choices=("keep", "blank"),
        default="keep",
        help="What to do if URI cannot be compacted (default: keep)",
    )
    p.add_argument("--chunksize", type=int, default=0, help="Read CSV in chunks")
    p.add_argument("--inplace", action="store_true", help="Overwrite input file after processing")
    args = p.parse_args()

    if args.inplace:
        tmp_out = args.input + ".tmp"
        out_path = tmp_out
    else:
        out_path = args.output

    # Initialize PrefixManager with Biolink/KGX defaults
    pm = PrefixManager()
    pm.prefix_map['NCIT'] = 'https://purl.org/ccf/ASCTB-TEMP_'
    pm.prefix_map['ENSEMBL'] = 'https://identifiers.org/ensembl:'

    columns_to_exclude = set(args.exclude_columns or [])

    if args.chunksize > 0:
        reader = pd.read_csv(args.input, chunksize=args.chunksize, dtype=str)
        first = True
        for chunk in reader:
            columns_to_compact = args.columns or list(chunk.columns)
            columns_to_compact = [ col for col in columns_to_compact if col not in columns_to_exclude ]
            for col in columns_to_compact:
                if col in chunk.columns:
                    chunk[col] = chunk[col].apply(lambda v: compact_value(pm, v, args.fallback))
                else:
                    print(f"Warning: column '{col}' not found.", file=sys.stderr)
            chunk.to_csv(out_path, index=False, mode="w" if first else "a", header=first)
            first = False
    else:
        df = pd.read_csv(args.input, dtype=str)
        columns_to_compact = args.columns or list(df.columns)
        columns_to_compact = [ col for col in columns_to_compact if col not in columns_to_exclude ]
        print(f"Compacting columns: {columns_to_compact}")
        for col in columns_to_compact:
            if col in df.columns:
                df[col] = df[col].apply(lambda v: compact_value(pm, v, args.fallback))
            else:
                print(f"Warning: column '{col}' not found.", file=sys.stderr)
        df.to_csv(out_path, index=False)

    if args.inplace:
        os.replace(tmp_out, args.input)
        print("Replaced input file with compacted version.")


if __name__ == "__main__":
    main()
