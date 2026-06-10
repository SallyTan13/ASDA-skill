# How to Replicate ACE and GEPA Baselines on FAMMA

## GEPA (GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning)


### 1. Clone and install GEPA

```bash
git clone https://github.com/gepa-ai/gepa.git gepa-baseline
cd gepa-baseline
pip install -e .
```

### 2. Add our FAMMA evaluation module

Copy the following files from our repo into the GEPA repo:

```
gepa-baseline/
└── eval/
    └── famma/
        ├── __init__.py
        └── run.py          # Runner with seed prompt, PoT code execution, LLM judge evaluation
```

`run.py` is self-contained — it includes the seed prompt, PoT code execution (using `exec()`/`eval()`), LLM judge evaluation, and the GEPA `optimize_anything()` call.

### 3. Prepare data

GEPA uses a 50/50 split of the training pool for its internal optimization loop (train/val). The test set is never seen during optimization.

```bash
# Generate the splits (from our repo root)
python data_split/split_train_for_gepa.py            # arithmetic
python data_split/split_non_arith_train_for_gepa.py   # non-arithmetic
```

This produces:
- `data/famma_arithmetic_gepa_train.csv` + `data/famma_arithmetic_gepa_val.csv`
- `data/famma_non_arithmetic_gepa_train.csv` + `data/famma_non_arithmetic_gepa_val.csv`

Pre-split CSVs are included in our repo under `data/`.

### 4. Run

```bash
cd gepa-baseline

# Arithmetic (with PoT)
python -m eval.famma.run \
  --task_name arithmetic \
  --pot \
  --api_provider openrouter \
  --generator_model anthropic/claude-3.5-haiku \
  --reflection_model claude-sonnet-4-5-20250929 \
  --max_metric_calls 1500 \
  --save_path results/famma_arithmetic

# Non-arithmetic (no PoT)
python -m eval.famma.run \
  --task_name non_arithmetic \
  --api_provider openrouter \
  --generator_model anthropic/claude-3.5-haiku \
  --reflection_model claude-sonnet-4-5-20250929 \
  --max_metric_calls 1500 \
  --save_path results/famma_non_arithmetic
```

### 5. What we changed vs original GEPA

Nothing in the GEPA framework code. We only added `eval/famma/` as a new evaluation task.

### Paper results

| Task | Seed Score | Best Val Score | Metric Calls |
|------|-----------|---------------|--------------|
| Arithmetic (PoT) | 46.90% | 49.56% | 1,506 |
| Non-arithmetic | 47.37% | 52.63% | 1,690 |

---

## ACE (Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models)

### 1. Clone and install ACE

```bash
git clone https://github.com/ace-agent/ace.git ace-baseline
cd ace-baseline
pip install -e .  # or: uv sync
```

### 2. Add our FAMMA evaluation module

Copy the following files from our repo into the ACE repo:

```
ace-baseline/
├── pot_utils.py                    # PoT code execution helper
└── eval/
    └── famma/
        ├── __init__.py
        ├── run.py                  # Runner with seed prompt
        ├── data_processor.py       # Data loading, evaluation, PoT execution
        ├── convert_csv_to_jsonl.py # CSV to JSONL converter
        └── data/
            ├── task_config.json          # Points to data files (update paths)
            ├── arithmetic_train.jsonl
            ├── arithmetic_eval.jsonl
            ├── non_arithmetic_train.jsonl
            └── non_arithmetic_eval.jsonl
```

### 3. Prepare data

ACE uses JSONL format. Convert from our CSVs:

```bash
cd eval/famma/data
python ../convert_csv_to_jsonl.py
```

Pre-converted JSONL files are included in our repo. The paper runs used the full training set for ACE's training data and the full test set (300 arithmetic / 252 non-arithmetic) for ACE's validation data.

**Important**: Update the paths in `task_config.json` to match your local setup (they currently contain absolute paths).

### 4. Run

```bash
cd ace-baseline

# Arithmetic (with PoT)
python -m eval.famma.run \
  --task_name arithmetic \
  --mode offline \
  --pot \
  --api_provider openrouter \
  --generator_model anthropic/claude-3.5-haiku \
  --reflector_model claude-sonnet-4-5-20250929 \
  --curator_model claude-sonnet-4-5-20250929 \
  --max_num_rounds 1 \
  --curator_frequency 5 \
  --eval_steps 100 \
  --save_steps 25 \
  --save_path results/famma_arithmetic

# Non-arithmetic (no PoT)
python -m eval.famma.run \
  --task_name non_arithmetic \
  --mode offline \
  --api_provider openrouter \
  --generator_model anthropic/claude-3.5-haiku \
  --reflector_model claude-sonnet-4-5-20250929 \
  --curator_model claude-sonnet-4-5-20250929 \
  --max_num_rounds 1 \
  --curator_frequency 5 \
  --eval_steps 100 \
  --save_steps 25 \
  --save_path results/famma_non_arithmetic
```

### 5. What we changed vs original ACE

Nothing in the ACE framework code. We added:
- `eval/famma/` — a new evaluation task (runner + data processor)
- `pot_utils.py` — shared PoT code execution helper (uses `exec()`/`eval()`, same as our ASDA pipeline)

### Paper results

We report the best validation checkpoint from each run:

| Task | Best Val Acc | Best Checkpoint |
|------|-------------|-----------------|
| Arithmetic (PoT) | 45.56% | Step 400 |
| Non-arithmetic | 49.60% | Step 100 |

---

## Notes

- Both baselines use OpenRouter as the API provider with `anthropic/claude-3.5-haiku` as the generator and `claude-sonnet-4-5-20250929` as the optimizer/reflector.
- PoT code execution uses `exec()`/`eval()` (expression-based, not `print()`-based) — consistent across ASDA, ACE, and GEPA.
- Neither ACE nor GEPA framework code was modified. All FAMMA-specific logic lives in the `eval/famma/` modules we added.
