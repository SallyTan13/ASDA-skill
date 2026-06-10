"""
Split arithmetic and non-arithmetic train.jsonl into train/val for ACE 3-way split.

- Stratified on topic_difficulty × question_type
- 60/40 split, seed 42
- Original eval.jsonl (300q arith, 252q non-arith) stays as clean test set
"""

import json
from sklearn.model_selection import train_test_split
from collections import Counter

TASKS = ["arithmetic", "non_arithmetic"]

for task in TASKS:
    input_path = f"{task}_train.jsonl"
    out_train = f"{task}_train_split.jsonl"
    out_val = f"{task}_val_split.jsonl"

    with open(input_path) as f:
        samples = [json.loads(line) for line in f]

    strat_keys = [s["topic_difficulty"] + "|" + s["question_type"] for s in samples]

    train, val = train_test_split(
        samples, test_size=0.4, random_state=42, stratify=strat_keys
    )

    print(f"\n{'='*50}")
    print(f"{task}: {len(samples)} → train={len(train)}, val={len(val)}")

    # Verify stratification
    orig = Counter(strat_keys)
    train_dist = Counter(s["topic_difficulty"] + "|" + s["question_type"] for s in train)
    val_dist = Counter(s["topic_difficulty"] + "|" + s["question_type"] for s in val)

    print(f"Stratification check:")
    for key in sorted(orig.keys()):
        print(f"  {key}: orig={orig[key]}, train={train_dist[key]}, val={val_dist[key]}")

    for out_path, data in [(out_train, train), (out_val, val)]:
        with open(out_path, "w") as f:
            for s in data:
                f.write(json.dumps(s) + "\n")
        print(f"Wrote {out_path} ({len(data)} samples)")
