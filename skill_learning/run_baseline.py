"""
Run Baseline Evaluation

Generates baseline results (no skills) for training or evaluation datasets.
Uses the same prompts as evaluate_checkpoint.py for consistency.

Usage:
    python skill_learning/run_baseline.py --config configs/baseline/haiku35_arithmetic_train.yaml
    python skill_learning/run_baseline.py --config configs/baseline/haiku35_arithmetic_eval.yaml --limit 10
"""

import os
import sys
import json
import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import from integration_example (same as evaluate_checkpoint)
from skill_learning.integration_example import (
    load_dataset,
    generate_answer,
    evaluate_answer,
    select_mc_option_from_numerical_result,
)
from skill_learning.token_tracker import tracker as token_tracker

# Load environment variables
load_dotenv()

# Try to import Anthropic client
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


def _maybe_map_pot_to_mc(
    answer: Optional[str],
    question: str,
    question_type: str,
    options: Optional[str],
    context: str,
    client,
) -> Optional[str]:
    """If PoT mode and multiple-choice, map numerical result to MC letter (A-E)."""
    if not answer or question_type != "multiple-choice":
        return answer
    pot_mode = os.getenv("POT_MODE", "false").lower() == "true"
    if not pot_mode or answer.strip().upper() in ("A", "B", "C", "D", "E"):
        return answer
    opts = str(options) if options is not None else ""
    selected = select_mc_option_from_numerical_result(
        numerical_result=answer,
        question=question,
        options=opts,
        context=context or "",
        client=client,
        model=os.getenv("SELECTION_MODEL", "qwen-turbo"),
        track_phase="baseline",
        track_component="selection",
    )
    return selected if selected else answer


def run_baseline(
    data: pd.DataFrame,
    gen_client,
    eval_client,
    gen_model: str,
    eval_model: str,
    selection_client,
    eval_strategy: str = "hybrid",
    debug: bool = False,
    output_dir: Path = None,
    checkpoint_interval: int = 25,
) -> Dict:
    """
    Run baseline evaluation on dataset.

    Args:
        data: Dataset DataFrame
        gen_client: Client for generation (Anthropic or OpenAI)
        eval_client: Client for evaluation
        gen_model: Model for generation
        eval_model: Model for evaluation
        selection_client: OpenAI-compatible client for MC selection
        eval_strategy: "hybrid" (rule-based MC + LLM open) or "llm_only"
        debug: Print per-question details
        output_dir: Directory for checkpoint files
        checkpoint_interval: Save checkpoint every N questions

    Returns:
        Dictionary with metrics and results
    """
    results = []
    processed_ids = set()

    # Load existing checkpoint if available
    checkpoint_file = output_dir / "checkpoint.json" if output_dir else None
    if checkpoint_file and checkpoint_file.exists():
        print(f"Loading checkpoint from {checkpoint_file}")
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
            results = checkpoint_data.get('results', [])
            processed_ids = set(checkpoint_data.get('processed_ids', []))
            print(f"Resuming from checkpoint: {len(processed_ids)} questions already processed")

    for idx, row in tqdm(data.iterrows(), total=len(data), desc="Generating baseline"):
        qid = row.get('question_id', f"q_{idx}")

        # Skip if already processed (resume from checkpoint)
        if qid in processed_ids:
            continue

        question = row['question']
        question_type = row.get('question_type', 'open-ended')
        context = row.get('context', '') if pd.notna(row.get('context')) else ''
        options = row.get('options', None) if pd.notna(row.get('options')) else None
        ground_truth = str(row.get('answers', row.get('ground_truth', '')))

        # Generate answer
        gen_result = generate_answer(
            client=gen_client,
            model=gen_model,
            question_id=qid,
            question=question,
            question_type=question_type,
            context=context,
            options=options,
            skill_content=None,
            selection_client=selection_client,
            track_component="generation_baseline"
        )

        generated_answer = gen_result.get('answer', '')
        generated_explanation = gen_result.get('explanation', '')
        generated_code = gen_result.get('generated_code', '')
        code_execution_success = gen_result.get('code_execution_success', None)

        # PoT + MC: map numerical result to option letter
        generated_answer = _maybe_map_pot_to_mc(
            generated_answer, question, question_type, options, context, selection_client
        ) or generated_answer

        # Evaluate answer
        score = evaluate_answer(
            client=eval_client,
            model=eval_model,
            question_id=qid,
            question=question,
            question_type=question_type,
            context=context,
            generated_answer=generated_answer,
            generated_explanation=generated_explanation,
            ground_truth=ground_truth,
            eval_strategy=eval_strategy,
            track_phase="baseline",
            track_component="evaluation"
        )

        is_correct = (score == 1.0)

        if debug:
            print(f"\n--- [{qid}] ---")
            print(f"  ground_truth:     {repr(ground_truth)}")
            print(f"  generated_answer: {repr(generated_answer)}")
            print(f"  is_correct:       {is_correct}")

        # Build result dict (BaselineLoader-compatible format)
        result = {
            'question_id': qid,
            'question_type': question_type,
            'question': question,
            'context': context,
            'options': options,
            'generated_answer': generated_answer,
            'generated_explanation': generated_explanation,
            'ground_truth': ground_truth,
            'is_correct': is_correct,
            'evaluation_method': 'rule_based' if (eval_strategy == 'hybrid' and question_type == 'multiple-choice') else 'llm_judge',
            'timestamp': pd.Timestamp.now().isoformat(),
        }

        # Add PoT-specific fields
        if generated_code:
            result['generated_code'] = generated_code
            result['code_execution_success'] = code_execution_success

        results.append(result)
        processed_ids.add(qid)

        # Save checkpoint periodically
        if checkpoint_file and len(results) % checkpoint_interval == 0:
            checkpoint_data = {
                'processed_ids': list(processed_ids),
                'results': results,
                'last_updated': pd.Timestamp.now().isoformat(),
            }
            with open(checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Checkpoint saved: {len(results)} questions processed")

    # Compute metrics
    df_results = pd.DataFrame(results)
    total = len(df_results)
    correct = df_results['is_correct'].sum()

    mc_results = df_results[df_results['question_type'] == 'multiple-choice']
    open_results = df_results[df_results['question_type'].isin(['open-ended', 'open question'])]

    metrics = {
        'total_questions': total,
        'total_correct': int(correct),
        'overall_accuracy': correct / total if total > 0 else 0,
        'mc_questions': len(mc_results),
        'mc_correct': int(mc_results['is_correct'].sum()) if len(mc_results) > 0 else 0,
        'mc_accuracy': mc_results['is_correct'].mean() if len(mc_results) > 0 else 0,
        'open_questions': len(open_results),
        'open_correct': int(open_results['is_correct'].sum()) if len(open_results) > 0 else 0,
        'open_accuracy': open_results['is_correct'].mean() if len(open_results) > 0 else 0,
        'timestamp': pd.Timestamp.now().isoformat(),
    }

    return {
        'metrics': metrics,
        'results': results,
    }


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    parser = argparse.ArgumentParser(description="Run baseline evaluation (no skills)")
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit to first N questions (for testing)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print per-question details'
    )

    args = parser.parse_args()

    # Load configuration
    print(f"Loading configuration from: {args.config}")
    config = load_config(args.config)

    # Extract config values
    baseline_name = config['baseline']['name']
    baseline_desc = config['baseline'].get('description', '')

    gen_model = config['generation']['model']
    gen_provider = config['generation'].get('provider', 'auto')  # auto, anthropic, openrouter, dashscope
    pot_mode = config['generation'].get('pot_mode', False)

    eval_model = config['evaluation']['model']
    eval_provider = config['evaluation'].get('provider', 'dashscope')
    selection_model = config['evaluation'].get('selection_model', 'qwen-turbo')
    eval_strategy = config['evaluation'].get('strategy', 'hybrid')

    dataset_path = config['dataset']['path']
    dataset_split = config['dataset'].get('split', 'train')

    output_dir_str = config['output']['dir']

    debug = config.get('debug', {}).get('enabled', args.debug)
    limit = args.limit or config.get('dataset', {}).get('limit', None)

    # Set environment variables for PoT mode
    os.environ['POT_MODE'] = 'true' if pot_mode else 'false'
    os.environ['SELECTION_MODEL'] = selection_model

    print(f"\n{'='*60}")
    print(f"Baseline Evaluation: {baseline_name}")
    print(f"{'='*60}")
    print(f"Description: {baseline_desc}")
    print(f"Generation model: {gen_model}")
    print(f"Evaluation model: {eval_model}")
    print(f"PoT mode: {pot_mode}")
    print(f"Eval strategy: {eval_strategy}")
    print(f"Dataset: {dataset_path}")
    print(f"Split: {dataset_split}")

    # Setup output directory
    output_dir = project_root / output_dir_str
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Load dataset
    dataset_file = project_root / dataset_path
    if not dataset_file.exists():
        print(f"Dataset not found: {dataset_file}")
        sys.exit(1)

    data = load_dataset(dataset_file)
    print(f"Loaded {len(data)} questions")

    if limit:
        data = data.head(limit)
        print(f"Limited to first {limit} questions")

    # Setup API clients
    def create_client(model: str, provider: str):
        """Create API client based on provider specified in YAML config."""
        if provider == 'openrouter':
            api_key = os.getenv('OPENROUTER_API_KEY')
            if not api_key:
                print("OPENROUTER_API_KEY required for OpenRouter")
                sys.exit(1)
            return OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        elif provider == 'anthropic' or (provider == 'auto' and model.lower().startswith('claude')):
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            if not anthropic_key:
                print("ANTHROPIC_API_KEY required for Anthropic")
                sys.exit(1)
            return Anthropic(api_key=anthropic_key)
        elif provider == 'dashscope' or (provider == 'auto' and model.lower().startswith('qwen')):
            api_key = os.getenv('DASHSCOPE_API_KEY')
            base_url = os.getenv('QWEN_API_BASE') or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            return OpenAI(api_key=api_key, base_url=base_url)
        else:
            # Default to OpenAI-compatible
            api_key = os.getenv('OPENAI_API_KEY') or os.getenv('DASHSCOPE_API_KEY')
            base_url = os.getenv('OPENAI_BASE_URL') or os.getenv('QWEN_API_BASE') or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            return OpenAI(api_key=api_key, base_url=base_url)

    # Generation client
    gen_client = create_client(gen_model, gen_provider)
    print(f"Using {gen_provider} client for generation")

    # Evaluation client
    eval_client = create_client(eval_model, eval_provider)
    print(f"Using {eval_provider} client for evaluation")

    # Selection client (always DashScope for qwen-turbo)
    api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('QWEN_API_BASE') or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    selection_client = OpenAI(api_key=api_key, base_url=base_url)

    # Set token tracker metadata
    token_tracker.set_metadata(
        baseline_name=baseline_name,
        gen_model=gen_model,
        eval_model=eval_model,
        pot_mode=pot_mode,
    )

    print(f"\n{'='*60}")
    print(f"Running baseline evaluation...")
    print(f"{'='*60}\n")

    # Run baseline
    result = run_baseline(
        data=data,
        gen_client=gen_client,
        eval_client=eval_client,
        gen_model=gen_model,
        eval_model=eval_model,
        selection_client=selection_client,
        eval_strategy=eval_strategy,
        debug=debug,
        output_dir=output_dir,
        checkpoint_interval=25,
    )

    metrics = result['metrics']
    results = result['results']

    # Print metrics
    print(f"\n{'='*60}")
    print(f"Baseline Results: {baseline_name}")
    print(f"{'='*60}")
    print(f"Total: {metrics['total_questions']} questions")
    print(f"Overall Accuracy: {metrics['overall_accuracy']:.2%} ({metrics['total_correct']}/{metrics['total_questions']})")
    print(f"MC Accuracy: {metrics['mc_accuracy']:.2%} ({metrics['mc_correct']}/{metrics['mc_questions']})")
    print(f"Open Accuracy: {metrics['open_accuracy']:.2%} ({metrics['open_correct']}/{metrics['open_questions']})")

    # Save results in BaselineLoader-compatible format
    # evaluation_results_{split}_final.json
    results_file = output_dir / f"evaluation_results_{dataset_split}_final.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {results_file}")

    # Save metrics
    metrics['experiment_name'] = baseline_name
    metrics_file = output_dir / "metrics.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {metrics_file}")

    # Print and save token usage
    token_tracker.summary(print_output=True)
    token_file = output_dir / "token_usage.json"
    token_tracker.save(str(token_file))

    print(f"\n{'='*60}")
    print(f"Baseline evaluation complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
