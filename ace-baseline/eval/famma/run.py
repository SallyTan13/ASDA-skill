#!/usr/bin/env python3
"""
ACE system runner for FAMMA financial reasoning benchmark.

Usage:
    # Offline training (train on train split, validate on eval split)
    cd ace-baseline
    python -m eval.famma.run --task_name non_arithmetic --mode offline \
        --api_provider dashscope --generator_model qwen-flash \
        --save_path results/famma_non_arithmetic

    # Eval-only with pre-trained playbook
    python -m eval.famma.run --task_name non_arithmetic --mode eval_only \
        --initial_playbook_path results/famma_non_arithmetic/best_playbook.txt \
        --api_provider dashscope --generator_model qwen-flash \
        --save_path results/famma_non_arithmetic_eval

    # With Haiku 4.5 via OpenRouter
    python -m eval.famma.run --task_name non_arithmetic --mode offline \
        --api_provider openrouter \
        --generator_model anthropic/claude-3-5-haiku-20241022 \
        --save_path results/famma_haiku45_non_arithmetic
"""

import os
import json
import argparse
import openai
from datetime import datetime
from .data_processor import DataProcessor

# ACE imports (from ace-baseline root)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ace import ACE
from utils import initialize_clients


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="ACE System - FAMMA Benchmark")

    # Task configuration
    parser.add_argument(
        "--task_name",
        type=str,
        required=True,
        choices=["non_arithmetic", "arithmetic"],
        help="FAMMA task type",
    )
    parser.add_argument(
        "--initial_playbook_path",
        type=str,
        default=None,
        help="Path to initial playbook (optional)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="offline",
        choices=["offline", "online", "eval_only"],
        help="Run mode",
    )
    parser.add_argument(
        "--config_path",
        type=str,
        default=None,
        help="Path to task config JSON (default: auto-detect)",
    )

    # Model configuration
    parser.add_argument(
        "--api_provider",
        type=str,
        default="dashscope",
        choices=["sambanova", "together", "openai", "dashscope", "openrouter", "anthropic"],
        help="API provider for generator",
    )
    parser.add_argument(
        "--reflector_provider",
        type=str,
        default=None,
        choices=["sambanova", "together", "openai", "dashscope", "openrouter", "anthropic"],
        help="API provider for reflector (defaults to api_provider)",
    )
    parser.add_argument(
        "--curator_provider",
        type=str,
        default=None,
        choices=["sambanova", "together", "openai", "dashscope", "openrouter", "anthropic"],
        help="API provider for curator (defaults to api_provider)",
    )
    parser.add_argument(
        "--generator_model",
        type=str,
        default="qwen-flash",
        help="Model for generator",
    )
    parser.add_argument(
        "--reflector_model",
        type=str,
        default=None,
        help="Model for reflector (defaults to generator_model)",
    )
    parser.add_argument(
        "--curator_model",
        type=str,
        default=None,
        help="Model for curator (defaults to generator_model)",
    )

    # Training configuration
    parser.add_argument("--num_epochs", type=int, default=1)
    parser.add_argument("--max_num_rounds", type=int, default=3)
    parser.add_argument("--curator_frequency", type=int, default=1)
    parser.add_argument("--eval_steps", type=int, default=50)
    parser.add_argument("--online_eval_frequency", type=int, default=15)
    parser.add_argument("--save_steps", type=int, default=25)

    # System configuration
    parser.add_argument("--max_tokens", type=int, default=4096)
    parser.add_argument("--playbook_token_budget", type=int, default=80000)
    parser.add_argument("--test_workers", type=int, default=10)

    # Prompt configuration
    parser.add_argument("--json_mode", action="store_true")
    parser.add_argument("--no_ground_truth", action="store_true")

    # PoT (Program of Thought) mode
    parser.add_argument("--pot", action="store_true", help="Enable PoT mode: generator produces Python code")
    parser.add_argument("--selection_model", type=str, default="qwen-turbo",
                        help="Model for MC option selection in PoT mode")

    # Bulletpoint analyzer
    parser.add_argument("--use_bulletpoint_analyzer", action="store_true")
    parser.add_argument("--bulletpoint_analyzer_threshold", type=float, default=0.90)

    # Output
    parser.add_argument("--save_path", type=str, required=True)

    # Limit (for smoke testing)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of training samples (for testing)",
    )

    return parser.parse_args()


def load_data(data_path: str):
    """Load data from a JSONL file."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    data = []
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))

    print(f"Loaded {len(data)} samples from {data_path}")
    return data


def preprocess_data(task_name, config, mode, limit=None):
    """Load and preprocess FAMMA data."""
    processor = DataProcessor(task_name=task_name)

    if mode in ["online", "eval_only"]:
        train_samples = None
        val_samples = None

        if "test_data" in config:
            test_samples = load_data(config["test_data"])
            test_samples = processor.process_task_data(test_samples)
        else:
            raise ValueError(f"{mode} mode requires test_data in config")

        print(f"{mode} mode: Testing on {len(test_samples)} examples")

    else:  # offline
        train_samples = load_data(config["train_data"])
        train_samples = processor.process_task_data(train_samples)

        if limit:
            train_samples = train_samples[:limit]
            print(f"Limited training to {limit} samples")

        val_samples = load_data(config["val_data"])
        val_samples = processor.process_task_data(val_samples)

        if "test_data" in config:
            test_samples = load_data(config["test_data"])
            test_samples = processor.process_task_data(test_samples)
        else:
            test_samples = []

        print(
            f"Offline mode: Training on {len(train_samples)}, "
            f"validating on {len(val_samples)}, testing on {len(test_samples)}"
        )

    return train_samples, val_samples, test_samples, processor


def load_initial_playbook(path):
    """Load initial playbook if provided."""
    if path and os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return None


# PoT helpers — shared with ace.py via pot_utils.py
from pot_utils import extract_code_from_response, execute_pot_code, select_mc_option, pot_process_answer  # noqa: F401


def main():
    args = parse_args()

    # Default reflector/curator to generator model if not specified
    reflector_model = args.reflector_model or args.generator_model
    curator_model = args.curator_model or args.generator_model

    print(f"\n{'='*60}")
    print(f"ACE SYSTEM - FAMMA Benchmark")
    print(f"{'='*60}")
    print(f"Task: {args.task_name}")
    print(f"Mode: {args.mode.upper()}")
    print(f"Generator: {args.generator_model} [{args.api_provider}]")
    print(f"Reflector: {reflector_model} [{args.reflector_provider or args.api_provider}]")
    print(f"Curator:   {curator_model} [{args.curator_provider or args.api_provider}]")
    if args.pot:
        print(f"PoT mode:  ENABLED (selection: {args.selection_model})")
    if args.limit:
        print(f"Limit: {args.limit} training samples")
    print(f"{'='*60}\n")

    # Determine config path
    if args.config_path:
        config_path = args.config_path
    else:
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "task_config.json"
        )

    with open(config_path, "r") as f:
        task_config = json.load(f)

    if args.task_name not in task_config:
        raise ValueError(
            f"Task '{args.task_name}' not found in config. "
            f"Available: {list(task_config.keys())}"
        )

    # Preprocess data
    train_samples, val_samples, test_samples, data_processor = preprocess_data(
        args.task_name, task_config[args.task_name], args.mode, args.limit
    )

    # Load initial playbook
    initial_playbook = load_initial_playbook(args.initial_playbook_path)
    if initial_playbook:
        print(f"Loaded initial playbook from {args.initial_playbook_path}\n")
    else:
        print("Using empty playbook as initial playbook\n")

    # Create ACE system
    ace_system = ACE(
        api_provider=args.api_provider,
        generator_model=args.generator_model,
        reflector_model=reflector_model,
        curator_model=curator_model,
        max_tokens=args.max_tokens,
        initial_playbook=initial_playbook,
        use_bulletpoint_analyzer=args.use_bulletpoint_analyzer,
        bulletpoint_analyzer_threshold=args.bulletpoint_analyzer_threshold,
        reflector_provider=args.reflector_provider,
        curator_provider=args.curator_provider,
    )

    # Setup PoT selection client if needed
    selection_client = None
    if args.pot:
        sel_api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        sel_base_url = os.getenv('QWEN_API_BASE') or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        selection_client = openai.OpenAI(api_key=sel_api_key, base_url=sel_base_url)

    # Build config dict
    config = {
        "num_epochs": args.num_epochs,
        "max_num_rounds": args.max_num_rounds,
        "curator_frequency": args.curator_frequency,
        "eval_steps": args.eval_steps,
        "online_eval_frequency": args.online_eval_frequency,
        "save_steps": args.save_steps,
        "playbook_token_budget": args.playbook_token_budget,
        "task_name": args.task_name,
        "mode": args.mode,
        "json_mode": args.json_mode,
        "no_ground_truth": args.no_ground_truth,
        "save_dir": args.save_path,
        "test_workers": args.test_workers,
        "initial_playbook_path": args.initial_playbook_path,
        "use_bulletpoint_analyzer": args.use_bulletpoint_analyzer,
        "bulletpoint_analyzer_threshold": args.bulletpoint_analyzer_threshold,
        "api_provider": args.api_provider,
        "pot_mode": args.pot,
        "selection_model": args.selection_model,
        "selection_client": selection_client,
    }

    # Run ACE
    results = ace_system.run(
        mode=args.mode,
        train_samples=train_samples,
        val_samples=val_samples,
        test_samples=test_samples,
        data_processor=data_processor,
        config=config,
    )

    print(f"\n{'='*60}")
    print(f"ACE FAMMA run complete!")
    print(f"Results saved to: {args.save_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
