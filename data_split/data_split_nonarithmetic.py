#!/usr/bin/env python3
"""
Create two-way split for FAMMA non-arithmetic questions
Train (60%), Test (40%)
Stratified by: topic_difficulty, question_type, and subfield
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import os
import json
from collections import Counter

project_root = Path(__file__).parent.parent

print("="*80)
print("CREATING TWO-WAY SPLIT: Train/Test (60/40)")
print("="*80)

# Load dataset: try local parquet first, fallback to Hugging Face
famma_data_dir = project_root / "famma_data"
parquet_file = famma_data_dir / "release_basic_txt-00000-of-00001.parquet"

if parquet_file.exists():
    print("\nLoading FAMMA dataset from local parquet file...")
    df = pd.read_parquet(parquet_file)
else:
    print("\nLocal parquet not found. Downloading from Hugging Face...")
    from datasets import load_dataset

    # Configure dataset cache
    cache_dir = project_root / "datasets"
    os.environ['HF_DATASETS_CACHE'] = str(cache_dir)

    dataset = load_dataset("weaverbirdllm/famma", split="release_basic_txt")
    df = pd.DataFrame(dataset)

print(f"Total dataset size: {len(df)}")

# ✅ FIX: Propagate context BEFORE filtering (not after)
print("\n✅ Propagating context BEFORE filtering (fixed Jan 4, 2026)...")
df['group_id'] = df['language'] + '_' + df['main_question_id'].astype(str)

for group_id, group in df.groupby('group_id'):
    first_context = group.iloc[0]['context']

    # Handle both actual NaN and string "nan"
    if pd.isna(first_context) or str(first_context).strip() == 'nan':
        # Try to find ANY question in group with real context
        for idx, row in group.iterrows():
            ctx = row['context']
            if pd.notna(ctx) and str(ctx).strip() != 'nan' and len(str(ctx)) > 10:
                first_context = ctx
                break

    # Propagate the real context (or NaN if none found)
    df.loc[group.index, 'context'] = first_context

print(f"Context propagation complete across all {len(df)} questions")

# NOW filter for arithmetic questions in English
print("\nFiltering for non-arithmetic questions (English only)...")
arithmetic_df = df[
    (df['is_arithmetic'] == 0) &
    (df['language'] == 'english')
].copy()

print(f"Arithmetic questions (English): {len(arithmetic_df)}")

# Check how many questions have real context
real_context = arithmetic_df['context'].apply(
    lambda x: pd.notna(x) and str(x).strip() != 'nan' and len(str(x)) > 10
).sum()
print(f"Questions with real context: {real_context}/{len(arithmetic_df)} ({real_context/len(arithmetic_df)*100:.1f}%)")

# Check stratification variables
print("\n" + "="*80)
print("STRATIFICATION VARIABLES")
print("="*80)

print("\n1. Topic Difficulty:")
diff_counts = arithmetic_df['topic_difficulty'].value_counts().sort_index()
for diff, count in diff_counts.items():
    print(f"   {diff}: {count} ({count/len(arithmetic_df)*100:.1f}%)")

print("\n2. Question Type:")
type_counts = arithmetic_df['question_type'].value_counts()
for qtype, count in type_counts.items():
    print(f"   {qtype}: {count} ({count/len(arithmetic_df)*100:.1f}%)")

print("\n3. Subfield:")
subfield_counts = arithmetic_df['subfield'].value_counts()
for subfield, count in subfield_counts.items():
    print(f"   {subfield}: {count} ({count/len(arithmetic_df)*100:.1f}%)")

# Create stratification strategy
# Start with most granular, simplify for small groups
print("\n" + "="*80)
print("CREATING STRATIFICATION STRATEGY")
print("="*80)

# Try full stratification first
arithmetic_df['strata_full'] = (
    arithmetic_df['topic_difficulty'].astype(str) + '_' + 
    arithmetic_df['question_type'] + '_' + 
    arithmetic_df['subfield'].astype(str)
)

strata_counts_full = arithmetic_df['strata_full'].value_counts()
print(f"\nFull stratification (diff + type + subfield):")
print(f"  Unique strata: {len(strata_counts_full)}")
print(f"  Min samples: {strata_counts_full.min()}")

# Keep at 5 to match original stratification logic (ensures identical train set)
min_samples_needed = 5
small_strata = strata_counts_full[strata_counts_full < min_samples_needed]

if len(small_strata) > 0:
    print(f"  ⚠️  {len(small_strata)} strata have < {min_samples_needed} samples")
    print(f"\n  Using simplified stratification (diff + type only)")
    
    # Use simplified: difficulty + question_type only
    arithmetic_df['strata_final'] = (
        arithmetic_df['topic_difficulty'].astype(str) + '_' + 
        arithmetic_df['question_type']
    )
    
    strata_counts_simple = arithmetic_df['strata_final'].value_counts()
    print(f"  Simplified stratification:")
    print(f"    Unique strata: {len(strata_counts_simple)}")
    print(f"    Min samples: {strata_counts_simple.min()}")
    
    # Check if this works
    if strata_counts_simple.min() < min_samples_needed:
        print(f"  ⚠️  Still too small, using difficulty only")
        arithmetic_df['strata_final'] = arithmetic_df['topic_difficulty'].astype(str)
else:
    print(f"  ✅ All strata have sufficient samples")
    arithmetic_df['strata_final'] = arithmetic_df['strata_full']

print(f"\nFinal stratification variable: strata_final")
print(f"Distribution:")
for strata, count in arithmetic_df['strata_final'].value_counts().sort_index().items():
    print(f"  {strata}: {count}")

print("\n" + "="*80)
print("CREATING SPLIT")
print("="*80)

# Split: 60% train, 40% test
print("\nSplit: Train (60%) vs Test (40%)...")
train_df, test_df = train_test_split(
    arithmetic_df,
    test_size=0.4,
    random_state=42,
    stratify=arithmetic_df['strata_final']
)

print(f"Train: {len(train_df)} questions")
print(f"Test: {len(test_df)} questions")

# Verify split ratios
total = len(arithmetic_df)
print("\n" + "="*80)
print("SPLIT VERIFICATION")
print("="*80)
print(f"\nTrain: {len(train_df)}/{total} = {len(train_df)/total*100:.1f}%")
print(f"Test: {len(test_df)}/{total} = {len(test_df)/total*100:.1f}%")

# Verify stratification worked
print("\n" + "="*80)
print("STRATIFICATION VERIFICATION")
print("="*80)

for split_name, split_df in [('Train', train_df), ('Test', test_df)]:
    print(f"\n{split_name}:")
    
    # Difficulty
    print("  Difficulty:")
    for diff in sorted(arithmetic_df['topic_difficulty'].unique()):
        count = len(split_df[split_df['topic_difficulty'] == diff])
        pct = count / len(split_df) * 100
        print(f"    {diff}: {count} ({pct:.1f}%)")
    
    # Question type
    print("  Question Type:")
    for qtype in arithmetic_df['question_type'].unique():
        count = len(split_df[split_df['question_type'] == qtype])
        pct = count / len(split_df) * 100
        print(f"    {qtype}: {count} ({pct:.1f}%)")
    
    # Subfield (top 5 only for brevity)
    print("  Subfield (top 5):")
    top_subfields = split_df['subfield'].value_counts().head(5)
    for subfield, count in top_subfields.items():
        pct = count / len(split_df) * 100
        print(f"    {subfield}: {count} ({pct:.1f}%)")

# Save splits
print("\n" + "="*80)
print("SAVING SPLITS")
print("="*80)

# Save to CSV for easy inspection
data_dir = project_root / 'data'
data_dir.mkdir(exist_ok=True)

train_df.to_csv(data_dir / 'famma_non_arithmetic_train_split.csv', index=False)
test_df.to_csv(data_dir / 'famma_non_arithmetic_test_split.csv', index=False)

print(f"\n✅ Saved CSV files to {data_dir}/")
print(f"   - famma_non_arithmetic_train_split.csv ({len(train_df)} questions)")
print(f"   - famma_non_arithmetic_test_split.csv ({len(test_df)} questions)")

# Save split metadata
split_info = {
    'total_questions': total,
    'split_ratios': {
        'train': 0.6,
        'test': 0.4
    },
    'actual_counts': {
        'train': len(train_df),
        'test': len(test_df)
    },
    'stratification_variables': ['topic_difficulty', 'question_type', 'subfield'],
    'random_seed': 42,
    'question_ids': {
        'train': train_df['question_id'].tolist(),
        'test': test_df['question_id'].tolist()
    },
    'distribution': {
        'train': {
            'difficulty': train_df['topic_difficulty'].value_counts().to_dict(),
            'question_type': train_df['question_type'].value_counts().to_dict(),
            'subfield': train_df['subfield'].value_counts().to_dict()
        },
        'test': {
            'difficulty': test_df['topic_difficulty'].value_counts().to_dict(),
            'question_type': test_df['question_type'].value_counts().to_dict(),
            'subfield': test_df['subfield'].value_counts().to_dict()
        }
    }
}

with open(data_dir / 'non_arithmetic_split_metadata.json', 'w') as f:
    json.dump(split_info, f, indent=2)

print(f"\n✅ Saved split metadata to {data_dir / 'non_arithmetic_split_metadata.json'}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\n✅ Two-way split created successfully!")
print(f"\nUsage:")
print(f"  - Train ({len(train_df)}q): Build skills from failures")
print(f"  - Test ({len(test_df)}q): Held-out evaluation")

