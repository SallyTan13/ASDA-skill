#!/usr/bin/env python3
"""
Convert FAMMA CSV splits to JSONL format for ACE.

Usage:
    python eval/famma/convert_csv_to_jsonl.py

Reads from data/ CSVs, writes to eval/famma/data/ JSONL files.
"""

import os
import json
import pandas as pd
from pathlib import Path


def csv_to_jsonl(csv_path: str, jsonl_path: str):
    """Convert a FAMMA CSV to JSONL preserving all fields ACE needs."""
    df = pd.read_csv(csv_path)
    print(f"Reading {csv_path}: {len(df)} rows")

    records = []
    for _, row in df.iterrows():
        record = {
            "question_id": str(row.get("question_id", "")),
            "question": str(row.get("question", "")),
            "context": str(row.get("context", "")) if pd.notna(row.get("context")) else "",
            "options": str(row.get("options", "")) if pd.notna(row.get("options")) else "",
            "answers": str(row.get("answers", "")),
            "question_type": str(row.get("question_type", "")),
            "is_arithmetic": int(row.get("is_arithmetic", 0)),
            "topic_difficulty": str(row.get("topic_difficulty", "")) if pd.notna(row.get("topic_difficulty")) else "",
            "subfield": str(row.get("subfield", "")) if pd.notna(row.get("subfield")) else "",
            "language": str(row.get("language", "")) if pd.notna(row.get("language")) else "",
        }
        records.append(record)

    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"  -> Wrote {len(records)} records to {jsonl_path}")
    return len(records)


def main():
    # Paths
    project_root = Path(__file__).parent.parent.parent.parent  # project root
    data_dir = project_root / "data"
    output_dir = Path(__file__).parent / "data"

    # Mapping: CSV -> JSONL
    conversions = {
        # Non-arithmetic
        "famma_non_arithmetic_train_split.csv": "non_arithmetic_train.jsonl",
        "famma_non_arithmetic_eval_split.csv": "non_arithmetic_eval.jsonl",
        # Arithmetic
        "famma_arithmetic_train_split.csv": "arithmetic_train.jsonl",
        "famma_arithmetic_eval_split.csv": "arithmetic_eval.jsonl",
    }

    print("=" * 60)
    print("Converting FAMMA CSVs to JSONL for ACE")
    print("=" * 60)

    for csv_name, jsonl_name in conversions.items():
        csv_path = data_dir / csv_name
        jsonl_path = output_dir / jsonl_name

        if csv_path.exists():
            csv_to_jsonl(str(csv_path), str(jsonl_path))
        else:
            print(f"SKIPPED: {csv_path} not found")

    # Generate task_config.json
    config = {
        "non_arithmetic": {
            "train_data": str(output_dir / "non_arithmetic_train.jsonl"),
            "val_data": str(output_dir / "non_arithmetic_eval.jsonl"),
        },
        "arithmetic": {
            "train_data": str(output_dir / "arithmetic_train.jsonl"),
            "val_data": str(output_dir / "arithmetic_eval.jsonl"),
        },
    }

    config_path = output_dir / "task_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"\nTask config written to: {config_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()
