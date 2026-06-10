<div align="center">

# ASDA: Automated Skill Distillation and Adaptation for Financial Reasoning

[![arXiv](https://img.shields.io/badge/arXiv-2603.16112-b31b1b.svg)](https://arxiv.org/abs/2603.16112)

_Official implementation of "ASDA: Automated Skill Distillation and Adaptation for Financial Reasoning"_

</div>

<p align="center">
  <img src="docs/ASDA-updated-diagram.png" alt="ASDA Framework Overview" width="90%">
</p>

## 📰 Latest News

- **Jun 2026** &nbsp;🎉 Our paper is accepted to the **ECML-PKDD 2026 Applied Data Science Track**!
- **Mar 2026** &nbsp;📄 The paper is now available on [arXiv](https://arxiv.org/abs/2603.16112).

## Environment Setup

### Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Installation

1. **Create a new conda environment:**

```bash
conda create -n asda python=3.12 -y
conda activate asda
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Required: At least one of these for generation/evaluation
DASHSCOPE_API_KEY=your_dashscope_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# For OpenRouter models
OPENROUTER_API_KEY=your_openrouter_key_here

# API endpoints
QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
ANTHROPIC_API_BASE=https://api.anthropic.com
```

## Project Structure

```
.
├── configs/                              # YAML configuration files
│   ├── analysis/                         # Failure analysis configs
│   ├── baseline/                         # Baseline evaluation configs
│   ├── evaluation/                       # Checkpoint evaluation configs
│   ├── skill_learning/                   # Training loop configs
│   └── warm_up/                          # Skill warm-up configs
├── data/                                 # Pre-split datasets
│   ├── famma_arithmetic_train_split.csv
│   ├── famma_arithmetic_eval_split.csv
│   ├── famma_non_arithmetic_train_split.csv
│   └── famma_non_arithmetic_eval_split.csv
├── data_split/                           # Data splitting scripts
│   ├── data_split_arithmetic.py
│   └── data_split_nonarithmetic.py
├── famma_data/                           # Raw FAMMA dataset (download required)
├── skill_learning/                       # Core training modules
│   ├── run_baseline.py                   # Baseline generation & evaluation
│   ├── analyze_failure_signatures.py     # Failure pattern analysis
│   ├── skill_warming_up.py               # Initial skill generation
│   ├── skill_trainer.py                  # Iterative refinement loop
│   ├── integration_example.py            # Main training entry point
│   ├── evaluate_checkpoint.py            # Checkpoint evaluation
│   ├── evidence_collector.py             # Q+/Q- evidence collection
│   ├── residual_evidence_collector.py    # Gap/discover evidence
│   ├── textual_optimizer.py              # LLM-based skill refinement
│   ├── skills_router.py                  # Skill routing & loading
│   ├── config.py                         # Configuration loader
│   ├── baseline_loader.py                # Baseline results loader
│   ├── checkpoint_manager.py             # Checkpoint management
│   ├── sandbox_verifier.py               # Sandbox verification
│   ├── token_tracker.py                  # Token usage tracking
│   ├── run_logger.py                     # Run logging
│   ├── iteration_logger.py               # Iteration logging
│   ├── trainer_utils.py                  # Training utilities
│   ├── optimizer_prompts.py              # Optimizer prompts
│   ├── optimizer_prompts_pot.py          # Optimizer prompts (PoT)
│   ├── residual_prompts.py               # Residual analysis prompts
│   ├── residual_prompts_pot.py           # Residual analysis prompts (PoT)
│   ├── signature_prompts.py              # Failure signature prompts
│   ├── warming_up_prompts.py             # Skill warm-up prompts
│   └── regression_analysis_prompts.py    # Regression analysis prompts
└── docs/                                 # Documentation
```

## Quick Start

### 1. Download FAMMA Dataset 

```bash
# Download FAMMA dataset from Hugging Face
mkdir -p famma_data
huggingface-cli download weaverbirdllm/famma --repo-type dataset --local-dir famma_data
```

### 2. Data Splitting

The split datasets are already provided in the `data/` folder. If you need to regenerate them: 

```bash
# Arithmetic questions
python data_split/data_split_arithmetic.py

# Non-arithmetic questions
python data_split/data_split_nonarithmetic.py
```

This creates train/test splits (60/40) with stratification by difficulty, question type, and subfield.

### 3. Run Baseline Evaluation

Generate baseline results (without skills) for comparison. Example:

```bash
python skill_learning/run_baseline.py --config configs/baseline/haiku35_arithmetic_train.yaml
```

Available baseline configs in `configs/baseline/`:

| Config | Dataset | Split |
|--------|---------|-------|
| `haiku35_arithmetic_train.yaml` | Arithmetic | Train |
| `haiku35_arithmetic_eval.yaml` | Arithmetic | Test |
| `haiku35_non_arithmetic_train.yaml` | Non-arithmetic | Train |
| `haiku35_non_arithmetic_eval.yaml` | Non-arithmetic | Test |

Options:
- `--limit N`: Run on first N questions only (for testing)
- `--debug`: Print per-question details

### 4. Warm-Up

Generate initial skills from baseline failures. This consists of two steps:

#### 4.1 Failure Analysis

Analyze baseline failures to identify error patterns and cluster similar failures:

```bash
python skill_learning/analyze_failure_signatures.py --config configs/analysis/haiku35_arithmetic_failures.yaml
```

```bash
python skill_learning/analyze_failure_signatures.py --config configs/analysis/haiku35_non_arithmetic_failures.yaml
```

This generates:
- `failure_signatures.json`: Error type classification for each failed question
- `failure_clusters.json`: Grouped failures by error type and subfield

#### 4.2 Skills Generation

Generate initial skill files from failure clusters:

```bash
python skill_learning/skill_warming_up.py --config configs/warm_up/haiku35_arithmetic_warming_up.yaml
```

```bash
python skill_learning/skill_warming_up.py --config configs/warm_up/haiku35_non_arithmetic_warming_up.yaml
```

This generates:
- `common/*.md`: Cross-subfield skills (visual evidence, constraints, format)
- `{subfield}/*.md`: Domain-specific skills by error type
- `SKILL.md`: Navigation file with skill index

### 5. Iterative Refinement

Run the automated training loop to iteratively refine skills:

```bash
python skill_learning/integration_example.py train-api --config configs/skill_learning/haiku35_arithmetic.yaml
```

```bash
python skill_learning/integration_example.py train-api --config configs/skill_learning/haiku35_non_arithmetic.yaml
```

### 6. Evaluation

Evaluate warm-up skills on the test set:

```bash
# Using config file (recommended)
python skill_learning/evaluate_checkpoint.py --config configs/evaluation/haiku35_arithmetic_eval_warm_up_skills.yaml
```

```bash
# Using config file (recommended)
python skill_learning/evaluate_checkpoint.py --config configs/evaluation/haiku35_non_arithmetic_eval_warm_up_skills.yaml
```

## Generated Skills

Generated skill libraries are provided in the `skills/` folder. These skills are distilled from **Haiku 3.5** and **Haiku 4.5** baseline failures on the FAMMA dataset. Each skill set is named `famma-{question-type}-{base-model}-{stage}`.

### Warm-Up Skills

Initial skills generated from failure analysis:

| Skill Set | Base Model | Path | Skill Files |
|-----------|------------|------|-------------|
| Arithmetic | Haiku 3.5 | `skills/famma-arithmetic-haiku35-warm-up/` | 29 |
| Arithmetic | Haiku 4.5 | `skills/famma-arithmetic-haiku45-warm-up/` | 25 |
| Arithmetic (self-teacher) | Haiku 3.5 | `skills/famma-arithmetic-haiku35-self-teacher-warm-up/` | 15 |
| Non-Arithmetic | Haiku 3.5 | `skills/famma-non-arithmetic-haiku35-warm-up/` | 14 |
| Non-Arithmetic | Haiku 4.5 | `skills/famma-non-arithmetic-haiku45-warm-up/` | 20 |
| Non-Arithmetic (self-teacher) | Haiku 3.5 | `skills/famma-non-arithmetic-haiku35-self-teacher-warm-up/` | 16 |

> The **self-teacher** variant generates the initial non-arithmetic warm-up skills using the model's own reasoning traces rather than the standard failure-analysis pipeline.

### Iteratively Refined Skills

Skills after dual-phase iterative refinement:

| Skill Set | Base Model | Path | Skill Files |
|-----------|------------|------|-------------|
| Arithmetic | Haiku 3.5 | `skills/famma-arithmetic-haiku35-refined/` | 37 |
| Arithmetic | Haiku 4.5 | `skills/famma-arithmetic-haiku45-refined/` | 29 |
| Non-Arithmetic | Haiku 3.5 | `skills/famma-non-arithmetic-haiku35-refined/` | 23 |
| Non-Arithmetic | Haiku 4.5 | `skills/famma-non-arithmetic-haiku45-refined/` | 27 |

### Skill Directory Structure

Each skill set follows this structure:

```
skills/{skill-set-name}/
├── SKILL.md                      # Navigation file with skill index
├── common/                       # Cross-subfield skills
│   ├── visual_evidence.md
│   ├── constraint_handling.md
│   └── ...
├── portfolio_management/         # Subfield-specific skills
├── derivatives/
├── fixed_income/
├── equity/
├── corporate_finance/
├── financial_statement_analysis/
├── economics/
└── alternative_investments/
```

## Replicating ACE & GEPA

Please see [REPLICATE_ACE_GEPA.md](REPLICATE_ACE_GEPA.md).

## 📝 Citation

If you find ASDA useful in your research, please consider citing our paper:

```bibtex
@article{yim2026asda,
  title={ASDA: Automated Skill Distillation and Adaptation for Financial Reasoning},
  author={Yim, Tik Yu and Tan, Wenting and Chan, Sum Yee and Lam, Tak-Wah and Yiu, Siu Ming},
  journal={arXiv preprint arXiv:2603.16112},
  year={2026}
}
```

<div style="text-align: center; font-weight: bold;">

⭐ If you find ASDA useful, please give us a star!

</div>
