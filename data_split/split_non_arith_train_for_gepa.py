#!/usr/bin/env python3
"""
Split the non-arithmetic train set 50/50 into train/val for GEPA,
using stratified sampling on strata_final (topic_difficulty × question_type).

Produces:
  data/famma_non_arithmetic_gepa_train.csv
  data/famma_non_arithmetic_gepa_val.csv

Seed: 42 (same as original 3-way split)
"""

import pandas as pd
import random

INPUT = "data/famma_non_arithmetic_train_split.csv"
SEED = 42

df = pd.read_csv(INPUT)
print(f"Input: {len(df)} rows")
print(f"Strata distribution:\n{df.strata_final.value_counts()}\n")

# Stratified 50/50 split
random.seed(SEED)
train_idx = []
val_idx = []

for stratum, group in df.groupby("strata_final"):
    indices = group.index.tolist()
    random.shuffle(indices)
    mid = len(indices) // 2
    train_idx.extend(indices[:mid])
    val_idx.extend(indices[mid:])

train = df.loc[sorted(train_idx)].reset_index(drop=True)
val = df.loc[sorted(val_idx)].reset_index(drop=True)

print(f"GEPA train: {len(train)} rows")
print(f"GEPA val:   {len(val)} rows")
print(f"\nTrain strata:\n{train.strata_final.value_counts()}")
print(f"\nVal strata:\n{val.strata_final.value_counts()}")

train.to_csv("data/famma_non_arithmetic_gepa_train.csv", index=False)
val.to_csv("data/famma_non_arithmetic_gepa_val.csv", index=False)

print("\nSaved:")
print("  data/famma_non_arithmetic_gepa_train.csv")
print("  data/famma_non_arithmetic_gepa_val.csv")
