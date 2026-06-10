"""
Evaluate a Checkpoint on Validation Set

Loads skills from a specific checkpoint and evaluates on the full validation set.
Supports both router-based and progressive skill loading modes.

For arithmetic questions with PoT (Program of Thought):
  - Set POT_MODE=true for code generation + execution.
  - MC questions: numerical result is mapped to option letter (A–E) via selection model
    before LLM evaluation. Override selection model with SELECTION_MODEL (default: qwen-turbo).
  - Use arithmetic val CSV and optional baseline, e.g.:
    VAL_CSV=data/famma_arithmetic_val_split.csv POT_MODE=true python skill_learning/evaluate_checkpoint.py --checkpoint epoch_4

Usage:
    python skill_learning/evaluate_checkpoint.py --checkpoint epoch_4
    python skill_learning/evaluate_checkpoint.py --checkpoint epoch_4 --baseline-only
    python skill_learning/evaluate_checkpoint.py --checkpoint epoch_4 --skills-mode progressive
    VAL_CSV=data/famma_arithmetic_val_split.csv POT_MODE=true python skill_learning/evaluate_checkpoint.py --checkpoint epoch_4
"""

import os
import sys
import json
import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import from integration_example
from skill_learning.integration_example import (
    load_dataset,
    BaselineLoader,
    generate_answer,
    evaluate_answer,
    build_generation_prompt,
    build_famma_question_block,
    parse_json_response,
    select_mc_option_from_numerical_result,
    extract_code_from_response,
    execute_pot_code,
)
from skill_learning.skills_router import SkillsRouter, determine_skill_method
from skill_learning.run_logger import RunLogger
from skill_learning.token_tracker import tracker as token_tracker
from skill_learning.config import set_config

# Load environment variables
load_dotenv()

# Try to import Anthropic client for progressive loading
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
    track_phase: str = None,
    track_component: str = None,
) -> Optional[str]:
    """If PoT mode and multiple-choice, map numerical result to MC letter (A–E)."""
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
        track_phase=track_phase,
        track_component=track_component,
    )
    return selected if selected else answer


def run_validation_with_checkpoint(
    checkpoint_dir: Path,
    val_data: pd.DataFrame,
    client: OpenAI,
    gen_model: str,
    eval_model: str,
    baseline_loader: Optional[BaselineLoader] = None,
    use_skills: bool = True,
    skills_loading_mode: str = "auto",
    anthropic_client: Optional['Anthropic'] = None,
    openrouter_client: Optional[OpenAI] = None,
    eval_client: Optional[OpenAI] = None,
    skills_dir_override: Optional[Path] = None,
    debug: bool = False,
    eval_strategy: str = "llm_only",
    router_model: Optional[str] = None,
    router_client: Optional[OpenAI] = None,
    router_type: str = "llm",  # "llm" (requires subfield) or "auto" (no subfield)
    gen_provider: str = "auto",
) -> Dict:
    """
    Run validation set with skills from a checkpoint.

    Args:
        checkpoint_dir: Path to checkpoint directory (e.g., checkpoints_api/epoch_4), or output base when skills_dir_override is set
        val_data: Validation dataset
        client: OpenAI client (for router mode and selection)
        gen_model: Model for generation
        eval_model: Model for evaluation
        baseline_loader: Pre-loaded baseline results
        use_skills: Whether to use skills (False = baseline only)
        skills_loading_mode: "auto", "router", or "progressive"
        anthropic_client: Anthropic client (required for progressive mode)
        openrouter_client: OpenRouter client for Claude models (alternative to anthropic_client)
        eval_client: Client for evaluation (if None, uses client)
        skills_dir_override: If set, use this as the skill set root (e.g. .claude/skills/famma-arithmetic-sonnet-20260214) instead of checkpoint_dir/skills
        debug: If True, print per-question ground_truth, baseline_answer, skill_answer, and skills used
        eval_strategy: Evaluation strategy ("llm_only" or "hybrid")
        router_model: Model for LLM-based skill file routing (when skills_loading_mode is "router"). If None, skills_router uses ROUTER_MODEL env.
        router_client: OpenAI-compatible client for the router (must match router_model provider). If None, skills_router uses its default _client.
        router_type: Type of router to use when skills_loading_mode is "router":
            - "llm" (default): Uses LLM routing with subfield (LLM_ROUTE_PROMPT)
            - "auto": Uses LLM routing without subfield (LLM_ROUTE_PROMPT_REMOVE_SUBFIELD)

    Returns:
        Dictionary with metrics and results
    """
    # Skill set root: either direct path or checkpoint_dir/skills
    if skills_dir_override is not None:
        skills_dir = Path(skills_dir_override).resolve()
        if not skills_dir.exists():
            raise FileNotFoundError(f"Skills directory not found: {skills_dir}")
    else:
        skills_dir = checkpoint_dir / "skills"
        if not skills_dir.exists():
            raise FileNotFoundError(f"Skills directory not found in checkpoint: {checkpoint_dir}")

    # If the checkpoint has an old nested layout (skills/skill_set_name/), detect and adjust
    skill_md = skills_dir / "SKILL.md"
    if not skill_md.exists():
        # Try to find a nested skill set directory
        subdirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        if subdirs:
            skills_dir = subdirs[0]
        else:
            raise FileNotFoundError(f"No SKILL.md found in {skills_dir} or its subdirectories")

    print(f"\n[Loading Skills from Checkpoint]")
    print(f"  Checkpoint: {checkpoint_dir.name}")
    print(f"  Skills dir: {skills_dir}")

    # Initialize router with checkpoint skills (2-level structure)
    router = SkillsRouter(str(skills_dir))

    print(f"  ✓ Loaded {len(router.all_files)} skill file(s)")
    for rel_path in list(router.all_files.keys())[:5]:
        print(f"    - {rel_path}")

    # Determine actual skill loading method
    actual_method = determine_skill_method(gen_model, skills_loading_mode)

    # Validate progressive requirements
    if actual_method == "progressive" and not anthropic_client:
        print(f"  ⚠️  Progressive mode requires Anthropic client, falling back to router")
        actual_method = "router"

    # Choose generation client based on gen_provider from YAML config
    is_claude_gen = gen_model.lower().startswith("claude") or gen_model.startswith("anthropic/")
    if gen_provider == 'anthropic' and anthropic_client:
        gen_client = anthropic_client
    elif gen_provider == 'openrouter' and openrouter_client:
        gen_client = openrouter_client
    elif gen_provider == 'auto' and is_claude_gen and openrouter_client:
        gen_client = openrouter_client
    elif gen_provider == 'auto' and is_claude_gen and anthropic_client:
        gen_client = anthropic_client
    else:
        gen_client = client

    # Use provided eval_client or fall back to default client
    if eval_client is None:
        eval_client = client

    # Initialize logger
    logger = RunLogger()

    print(f"\n[Running Validation Set]")
    print(f"  Total questions: {len(val_data)}")
    print(f"  Use skills: {use_skills}")
    print(f"  Skills loading mode: {actual_method}")
    if baseline_loader:
        print(f"  Using FIXED baseline from pre-computed results")

    results = []

    for idx, row in tqdm(val_data.iterrows(), total=len(val_data), desc="Processing validation"):
        qid = row.get('question_id', f"val_{idx}")
        question = row['question']
        question_type = row.get('question_type', 'open-ended')
        context = row.get('context', '') if pd.notna(row.get('context')) else ''
        options = row.get('options', None) if pd.notna(row.get('options')) else None
        ground_truth = str(row.get('answers', row.get('ground_truth', '')))

        # Extract signature
        image_type = row.get('image_type', None)
        modality = image_type if pd.notna(image_type) else 'text-only'

        signature = {
            'subfield': row.get('subfield', 'unknown'),
            'modality': modality
        }

        # Get baseline
        baseline_code_status = None
        baseline_code = None
        if baseline_loader and qid in baseline_loader:
            baseline = baseline_loader.get_baseline(qid)
            baseline_answer = baseline.baseline_answer
            baseline_explanation = baseline.baseline_explanation
            baseline_score = baseline.baseline_score
            # Try to get code execution status and code from baseline if available
            if hasattr(baseline, 'code_execution_success'):
                baseline_code_status = baseline.code_execution_success
            if hasattr(baseline, 'generated_code'):
                baseline_code = baseline.generated_code
        else:
            # Generate baseline
            baseline_result = generate_answer(
                client=gen_client,
                model=gen_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                options=options,
                skill_content=None,
                selection_client=client,  # Use OpenAI client for qwen-turbo selection
                track_component="generation_baseline"
            )
            baseline_answer = baseline_result['answer']
            baseline_explanation = baseline_result.get('explanation', '')
            baseline_code_status = baseline_result.get('code_execution_success', None)
            baseline_code = baseline_result.get('generated_code', None)
            # PoT + MC: map numerical result to option letter before LLM evaluation
            baseline_answer = _maybe_map_pot_to_mc(
                baseline_answer, question, question_type, options, context, client,
                track_phase="phase3", track_component="selection"
            ) or baseline_answer

            baseline_score = evaluate_answer(
                client=eval_client,
                model=eval_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                generated_answer=baseline_answer,
                generated_explanation=baseline_explanation,
                ground_truth=ground_truth,
                eval_strategy=eval_strategy,
                track_phase="phase3",
                track_component="evaluation"
            )

        # Generate with skill (if enabled)
        skill_answer = None
        skill_explanation = None
        skill_score = None
        skill_code_status = None
        skill_code = None
        chosen_skill = None
        specific_skill_file = None
        all_skill_files = None

        if use_skills:
            # Route to skill files using LLM-based routing
            chosen_skill = router.skill_dir.name  # skill set name

            if actual_method == "progressive" and anthropic_client:
                # Progressive loading: Claude dynamically requests skill files
                question_block = build_famma_question_block(
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options
                )

                # Check if PoT mode is enabled and set appropriate task instructions
                pot_mode = os.getenv("POT_MODE", "false").lower() == "true"
                if pot_mode:
                    task_instructions = """For this question, you should:
1. Generate Python code to solve the problem
2. Use clear variable names and comments
3. End your code with an EXPRESSION (NOT print()) that evaluates to the final answer
4. Put your code in a ```python code block

Example format:
```python
# Calculate the answer
result = (some calculation)
result  # This should be the final answer
```

Generate Python code to solve this problem:"""
                else:
                    task_instructions = "Please answer the following financial question accurately."

                response_text, metadata = router.generate_progressive(
                    client=anthropic_client,
                    model=gen_model,
                    question=question,
                    context=context,
                    question_block=question_block,
                    task_instructions=task_instructions,
                    max_turns=5
                )

                # Track loaded files from progressive loading
                if metadata:
                    loaded_files = metadata.get('loaded_files', [])
                    # Filter out SKILL.md (always loaded)
                    all_skill_files = [f for f in loaded_files if f != 'SKILL.md']
                    specific_skill_file = all_skill_files[0] if all_skill_files else None

                # Parse response (pot_mode already checked above)
                if response_text:
                    if pot_mode:
                        # PoT mode: Extract and execute Python code from response
                        code = extract_code_from_response(response_text)
                        skill_code = code  # Store the generated code
                        if code:
                            result, success = execute_pot_code(code)
                            skill_code_status = success
                            if success:
                                # For MC questions, map numerical result to letter
                                if question_type == 'multiple-choice' and options:
                                    selected_option = select_mc_option_from_numerical_result(
                                        numerical_result=result,
                                        question=question,
                                        options=str(options) if options else "",
                                        context=context or "",
                                        client=client,  # Use OpenAI client for qwen-turbo
                                        model=os.getenv("SELECTION_MODEL", "qwen-turbo")
                                    )
                                    skill_answer = selected_option
                                    skill_explanation = f"Code execution result: {result}, selected option: {selected_option}"
                                else:
                                    # Open-ended: return numerical result directly
                                    skill_answer = result
                                    skill_explanation = f"Code execution result: {result}"
                            else:
                                skill_answer = ""
                                skill_explanation = "Code execution failed"
                        else:
                            skill_answer = ""
                            skill_explanation = "No code found in response"
                            skill_code_status = False
                    else:
                        # Standard mode: Parse JSON response
                        parsed, _ = parse_json_response(response_text)
                        if parsed:
                            if isinstance(parsed, dict):
                                for qid_key, data in parsed.items():
                                    if isinstance(data, dict):
                                        skill_answer = data.get('answer', '')
                                        skill_explanation = data.get('explanation', '')
                                        skill_code_status = data.get('code_execution_success', None)
                                        break
                                    elif isinstance(data, str):
                                        skill_answer = data
                                        break
                            elif isinstance(parsed, list) and len(parsed) > 0:
                                first_item = parsed[0]
                                if isinstance(first_item, dict):
                                    skill_answer = first_item.get('answer', '')
                                    skill_explanation = first_item.get('explanation', '')
                                    skill_code_status = first_item.get('code_execution_success', None)
                                elif isinstance(first_item, str):
                                    skill_answer = first_item

                # Evaluate with skill (if we got an answer)
                if skill_answer:
                    skill_score = evaluate_answer(
                        client=eval_client,
                        model=eval_model,
                        question_id=qid,
                        question=question,
                        question_type=question_type,
                        context=context,
                        generated_answer=skill_answer,
                        generated_explanation=skill_explanation or '',
                        ground_truth=ground_truth,
                        eval_strategy=eval_strategy,
                        track_phase="phase3",
                        track_component="evaluation"
                    )

            else:
                # Router mode: LLM pre-selects skill files (use config router_model/client when provided)
                if router_type == "auto":
                    # Auto router: LLM identifies subfield from question (no subfield param needed)
                    print(f"  [Using auto router for {qid}]")
                    selected_files = router.get_auto_selected_files(
                        question=question,
                        context=context,
                        model=router_model,
                        client=router_client,
                    )
                else:
                    # LLM router: requires subfield parameter
                    selected_files = router.get_llm_selected_files(
                        question=question,
                        context=context,
                        subfield=signature.get('subfield', ''),
                        model=router_model,
                        client=router_client,
                    )

                if selected_files:
                    # Track ALL selected files for evidence attribution
                    all_skill_files = [str(f.relative_to(router.skill_dir)) for f in selected_files]
                    specific_skill_file = all_skill_files[0]  # Primary file (backward compat)
                    # Build concatenated skill content from all selected files
                    skill_content = router._build_content(selected_files)
                else:
                    # LLM selected no files - generate without skill content
                    all_skill_files = []
                    specific_skill_file = None
                    skill_content = None
                    print(f"  [LLM selected no files for {qid}]")

                # Generate answer (with or without skill content)
                skill_result = generate_answer(
                    client=gen_client,
                    model=gen_model,
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options,
                    skill_content=skill_content,
                    selection_client=client,  # Use OpenAI client for qwen-turbo selection
                    track_component="generation_skill"
                )
                print("skill_result: ", skill_result)
                skill_answer = skill_result['answer']
                skill_explanation = skill_result.get('explanation', '')
                skill_code_status = skill_result.get('code_execution_success', None)
                skill_code = skill_result.get('generated_code', None)
                # PoT + MC: map numerical result to option letter before LLM evaluation
                skill_answer = _maybe_map_pot_to_mc(
                    skill_answer, question, question_type, options, context, client,
                    track_phase="phase3", track_component="selection"
                ) or skill_answer

                # Evaluate with skill
                skill_score = evaluate_answer(
                    client=eval_client,
                    model=eval_model,
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    generated_answer=skill_answer,
                    generated_explanation=skill_explanation,
                    ground_truth=ground_truth,
                    eval_strategy=eval_strategy,
                    track_phase="phase3",
                    track_component="evaluation"
                )

        # Debug: print per-question answers and skills used
        if debug:
            skills_used = all_skill_files if all_skill_files else (([specific_skill_file] if specific_skill_file else []) or ([] if not chosen_skill else [chosen_skill]))
            if isinstance(skills_used, str):
                skills_used = [skills_used]
            print(f"\n--- [{qid}] ---")
            print(f"  ground_truth:      {repr(ground_truth)}")
            print(f"  baseline_answer:   {repr(baseline_answer)}  (score: {baseline_score})")
            print(f"  skill_answer:      {repr(skill_answer)}  (score: {skill_score})")
            print(f"  skills_used:       {skills_used}")

        # Log the run
        logger.log_run(
            qid=qid,
            question=question,
            context=context,
            ground_truth=ground_truth,
            baseline_answer=baseline_answer,
            baseline_score=baseline_score,
            baseline_explanation=baseline_explanation,
            candidates=[chosen_skill] if chosen_skill else [],
            chosen_skill=chosen_skill,
            skill_version="checkpoint",
            specific_skill_file=specific_skill_file,
            all_skill_files=all_skill_files,
            skill_answer=skill_answer,
            skill_score=skill_score,
            skill_explanation=skill_explanation,
            signature=signature,
            split="val",
            options=options,
            # PoT mode parameters
            baseline_code=baseline_code,
            skill_code=skill_code,
            baseline_execution_success=baseline_code_status,
            skill_execution_success=skill_code_status
        )

        # Collect detailed result
        result_dict = {
            'question_id': qid,
            'question': question,
            'question_type': question_type,
            'context': context,
            'options': options,
            'ground_truth': ground_truth,
            'subfield': signature['subfield'],
            'modality': signature['modality'],
            # Baseline results
            'baseline_answer': baseline_answer,
            'baseline_explanation': baseline_explanation,
            'baseline_score': baseline_score,
            # Skill results
            'skill_answer': skill_answer,
            'skill_explanation': skill_explanation,
            'skill_score': skill_score if skill_score is not None else baseline_score,
            # Skills used
            'skills_used': all_skill_files if all_skill_files else [],
            'chosen_skill': chosen_skill,
            'specific_file': specific_skill_file,
            # Analysis
            'is_fix': baseline_score == 0 and skill_score == 1 if skill_score is not None else False,
            'is_regress': baseline_score == 1 and skill_score == 0 if skill_score is not None else False,
        }

        # Add code execution status and generated code if in PoT mode
        pot_mode = os.getenv('POT_MODE', 'false').lower() == 'true'
        if pot_mode:
            result_dict['baseline_code_execution_status'] = baseline_code_status
            result_dict['skill_code_execution_status'] = skill_code_status
            result_dict['baseline_code'] = baseline_code
            result_dict['skill_code'] = skill_code

        results.append(result_dict)

    # Compute metrics
    df_results = pd.DataFrame(results)

    total = len(df_results)
    baseline_correct = (df_results['baseline_score'] == 1).sum()
    skill_correct = (df_results['skill_score'] == 1).sum()
    fixes = (df_results['is_fix'] == True).sum()
    regressions = (df_results['is_regress'] == True).sum()

    # By question type (FAMMA uses "open question", we also accept "open-ended")
    mc_results = df_results[df_results['question_type'] == 'multiple-choice']
    open_results = df_results[df_results['question_type'].isin(['open-ended', 'open question'])]

    metrics = {
        'total': total,
        'baseline_accuracy': baseline_correct / total if total > 0 else 0,
        'skill_accuracy': skill_correct / total if total > 0 else 0,
        'improvement': (skill_correct - baseline_correct) / total if total > 0 else 0,
        'fixes': int(fixes),
        'regressions': int(regressions),
        'net_improvement': int(fixes - regressions),
        'mc': {
            'total': len(mc_results),
            'baseline_accuracy': (mc_results['baseline_score'] == 1).sum() / len(mc_results) if len(mc_results) > 0 else 0,
            'skill_accuracy': (mc_results['skill_score'] == 1).sum() / len(mc_results) if len(mc_results) > 0 else 0,
        },
        'open': {
            'total': len(open_results),
            'baseline_accuracy': (open_results['baseline_score'] == 1).sum() / len(open_results) if len(open_results) > 0 else 0,
            'skill_accuracy': (open_results['skill_score'] == 1).sum() / len(open_results) if len(open_results) > 0 else 0,
        }
    }

    return {
        'metrics': metrics,
        'logger': logger,
        'results': df_results,
        'detailed_results': results  # Raw list for JSON output
    }


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    parser = argparse.ArgumentParser(description="Evaluate skills or checkpoint on validation set")
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to YAML configuration file (recommended method)'
    )
    # Legacy/alternative arguments (for backward compatibility with checkpoint mode)
    parser.add_argument(
        '--checkpoint',
        type=str,
        default=os.getenv('DEFAULT_CHECKPOINT_NAME', None),
        help='Checkpoint name (e.g., epoch_4) - for checkpoint-based evaluation'
    )
    parser.add_argument(
        '--checkpoint-mode',
        type=str,
        default=os.getenv('DEFAULT_CHECKPOINT_MODE', 'api'),
        help='Checkpoint mode (api, interactive, etc.) - used with --checkpoint'
    )
    parser.add_argument(
        '--skills-dir',
        type=str,
        default=None,
        help='Direct path to skill set root (e.g. .claude/skills/famma-arithmetic-haiku45-v1)'
    )
    parser.add_argument(
        '--skills-mode',
        type=str,
        default=os.getenv('SKILLS_LOADING_MODE', 'auto'),
        choices=['auto', 'router', 'progressive'],
        help='Skills loading mode (used in legacy mode)'
    )
    parser.add_argument(
        '--baseline-only',
        action='store_true',
        help='Run baseline only (no skills) - legacy mode'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Only run on first N validation samples (for quick tests)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print per-question details'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file for results (JSON) - legacy mode'
    )

    args = parser.parse_args()

    # Load configuration
    if args.config:
        # YAML config mode (recommended)
        print(f"✓ Loading configuration from: {args.config}")
        config = load_config(args.config)
        set_config(config)  # Make config available via cfg() for other modules

        # Extract configuration
        skills_dir_str = config['skills']['dir']
        use_skills = config['skills']['use_skills']
        skills_loading_mode = config['skills']['loading_mode']
        router_model_config = config['skills'].get('router_model', None)
        router_provider_config = config['skills'].get('router_provider', 'auto')
        router_type_config = config['skills'].get('router_type', 'llm')  # "llm" or "auto"

        gen_model = config['generation']['model']
        gen_provider = config['generation'].get('provider', 'auto')  # Read provider from config
        pot_mode_config = config['generation']['pot_mode']

        eval_model = config['eval_model']['name']
        eval_provider = config['eval_model'].get('provider', 'auto')
        selection_model = config['eval_model'].get('selection_model', 'qwen-turbo')
        eval_strategy = config['eval_model'].get('strategy', 'llm_only')

        val_csv_path = config['input']['val_csv']
        baseline_dir_str = config['input'].get('baseline_dir', None)
        limit = args.limit if args.limit is not None else config['input'].get('limit', None)

        output_dir_str = config['output']['dir']
        include_baseline = config['output'].get('include_baseline', True)
        include_code_status = config['output'].get('include_code_status', pot_mode_config)

        debug = config['debug'].get('enabled', args.debug)
        checkpoint_name = None  # Not used in YAML mode

        # Set PoT mode environment variable
        os.environ['POT_MODE'] = 'true' if pot_mode_config else 'false'
        os.environ['SELECTION_MODEL'] = selection_model

        print(f"✓ Configuration loaded: {config['evaluation']['name']}")

    else:
        # Legacy mode (backward compatibility with existing scripts)
        print(f"✓ Using legacy parameter mode")

        if not args.checkpoint and not args.skills_dir:
            print("❌ Error: Either --config or --checkpoint/--skills-dir must be provided")
            sys.exit(1)

        skills_dir_str = args.skills_dir
        checkpoint_name = args.checkpoint
        checkpoint_mode = args.checkpoint_mode
        use_skills = not args.baseline_only
        skills_loading_mode = args.skills_mode

        gen_model = os.getenv('GEN_MODEL', 'qwen-flash')
        pot_mode_config = os.getenv('POT_MODE', 'false').lower() == 'true'

        eval_model = os.getenv('EVAL_MODEL', 'qwen-max')
        eval_provider = os.getenv('EVAL_PROVIDER', 'dashscope')
        selection_model = os.getenv('SELECTION_MODEL', 'qwen-turbo')
        eval_strategy = os.getenv('EVAL_STRATEGY', 'llm_only')

        val_csv_path = os.getenv('VAL_CSV', 'data/famma_non_arithmetic_eval_split.csv')
        baseline_dir_str = os.getenv('BASELINE_DIR', 'results/qwen_flash_non_arithmetic')
        limit = args.limit

        output_dir_str = None  # Will use checkpoint dir
        include_baseline = True
        include_code_status = pot_mode_config

        debug = args.debug

    # Resolve skills dir and checkpoint dir
    skills_dir_override = None

    if skills_dir_str:
        # Direct skills directory provided (YAML mode or --skills-dir)
        p = Path(skills_dir_str)
        skills_dir_override = (project_root / p).resolve() if not p.is_absolute() else p.resolve()
        if not skills_dir_override.exists():
            print(f"❌ Skills directory not found: {skills_dir_override}")
            sys.exit(1)
        checkpoint_dir = skills_dir_override  # Default output location
        print(f"✓ Using skills dir: {skills_dir_override}")
    elif checkpoint_name:
        # Checkpoint mode (legacy: --checkpoint epoch_4)
        checkpoint_dir = project_root / "skill_learning" / f"checkpoints_{checkpoint_mode}" / checkpoint_name
        if not checkpoint_dir.exists():
            print(f"❌ Checkpoint not found: {checkpoint_dir}")
            sys.exit(1)
        print(f"✓ Using checkpoint: {checkpoint_name} (mode: {checkpoint_mode})")
    else:
        print(f"❌ Error: Either skills directory or checkpoint must be specified")
        sys.exit(1)

    # Set output directory
    if output_dir_str:
        output_dir = (project_root / output_dir_str).resolve() if not Path(output_dir_str).is_absolute() else Path(output_dir_str).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory: {output_dir}")
    else:
        output_dir = checkpoint_dir

    # Load dataset
    val_csv = project_root / val_csv_path
    if not val_csv.exists():
        print(f"❌ Validation dataset not found: {val_csv}")
        sys.exit(1)

    val_data = load_dataset(val_csv)
    print(f"✓ Loaded validation dataset: {len(val_data)} questions")

    if limit is not None:
        val_data = val_data.head(limit)
        print(f"✓ Limited to first {limit} validation samples")

    # Load baseline (if available)
    baseline_loader = None
    if baseline_dir_str:
        baseline_dir = project_root / baseline_dir_str
        baseline_val_file = baseline_dir / "evaluation_results_eval_final.json"

        if baseline_val_file.exists():
            print(f"\n[Loading Baseline]")
            baseline_loader = BaselineLoader(str(baseline_dir))
            baseline_loader.load_split("eval")
            print(f"  ✓ Loaded {len(baseline_loader.baselines)} validation baselines")
        else:
            print(f"  ⚠️  Baseline file not found: {baseline_val_file}")
            print(f"  Will generate baseline on-the-fly")

    # Setup API clients based on provider specified in YAML config
    # DashScope client (default for selection and router)
    dashscope_api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY') or os.getenv('API_KEY')
    dashscope_base_url = os.getenv('QWEN_API_BASE') or os.getenv('OPENAI_BASE_URL') or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_client = OpenAI(api_key=dashscope_api_key, base_url=dashscope_base_url)

    # Anthropic client (for Claude models when provider=anthropic)
    anthropic_client = None
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if ANTHROPIC_AVAILABLE and anthropic_api_key:
        anthropic_client = Anthropic(api_key=anthropic_api_key)

    # OpenRouter client (for models when provider=openrouter, e.g. Haiku 3.5)
    openrouter_client = None
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    if openrouter_api_key:
        openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")

    # OpenAI-compatible Anthropic client (for router when provider=anthropic, e.g. Haiku 4.5)
    anthropic_oai_client = None
    if anthropic_api_key:
        anthropic_oai_client = OpenAI(api_key=anthropic_api_key, base_url="https://api.anthropic.com/v1")

    # Choose generation client based on gen_provider from YAML
    if gen_provider == 'openrouter' and openrouter_client:
        print(f"✓ Generation client: OpenRouter ({gen_model})")
    elif gen_provider == 'anthropic' and anthropic_client:
        print(f"✓ Generation client: Anthropic ({gen_model})")
    else:
        print(f"✓ Generation client: DashScope ({gen_model})")

    # Choose eval client based on eval_provider from YAML
    if eval_provider == 'openrouter' and openrouter_client:
        eval_client = openrouter_client
        print(f"✓ Evaluation client: OpenRouter ({eval_model})")
    elif eval_provider == 'anthropic' and anthropic_client:
        eval_client = anthropic_client
        print(f"✓ Evaluation client: Anthropic ({eval_model})")
    else:
        eval_client = dashscope_client
        print(f"✓ Evaluation client: DashScope ({eval_model})")

    # Default client for selection (always DashScope for cost)
    client = dashscope_client

    # Choose router client based on router_provider from YAML config
    router_model = None
    router_client = None
    router_type = "llm"  # default: LLM router with subfield
    if args.config:
        # Read router config (already loaded above)
        router_model = router_model_config
        if router_provider_config == 'openrouter' and openrouter_client:
            router_client = openrouter_client
            print(f"✓ Router client: OpenRouter ({router_model})")
        elif router_provider_config == 'anthropic' and anthropic_oai_client:
            router_client = anthropic_oai_client
            print(f"✓ Router client: Anthropic ({router_model})")
        elif router_provider_config == 'dashscope':
            router_client = dashscope_client
            print(f"✓ Router client: DashScope ({router_model})")
        else:
            # Auto-detect based on model name
            if router_model and router_model.startswith('anthropic/'):
                # OpenRouter format (e.g. anthropic/claude-3.5-haiku)
                if openrouter_client:
                    router_client = openrouter_client
                    print(f"✓ Router client: OpenRouter (auto-detected, {router_model})")
                else:
                    router_client = dashscope_client
                    print(f"✓ Router client: DashScope (fallback, no OpenRouter key)")
            elif router_model and router_model.lower().startswith('claude'):
                # Anthropic direct format (e.g. claude-haiku-4-5-20251001)
                if anthropic_oai_client:
                    router_client = anthropic_oai_client
                    print(f"✓ Router client: Anthropic (auto-detected, {router_model})")
                else:
                    router_client = dashscope_client
                    print(f"✓ Router client: DashScope (fallback, no Anthropic key)")
            else:
                router_client = dashscope_client
                print(f"✓ Router client: DashScope (default)")
        # Set router_type from config
        router_type = router_type_config
        if router_type == "auto":
            print(f"✓ Router type: auto (no subfield required)")

    print(f"✓ Using generation model: {gen_model}")
    print(f"✓ Using evaluation model: {eval_model}")
    print(f"✓ Evaluation strategy: {eval_strategy}")
    print(f"✓ Skills loading mode: {skills_loading_mode}")
    if pot_mode_config:
        print(f"✓ PoT mode: ON (code gen + execution; MC numerical→letter mapping before eval)")
        print(f"✓ Selection model: {selection_model}")

    # Run evaluation
    print("\n" + "="*80)
    eval_label = checkpoint_dir.name if skills_dir_override else args.checkpoint
    print(f"Evaluating: {eval_label}")
    print("="*80)

    result = run_validation_with_checkpoint(
        checkpoint_dir=checkpoint_dir,
        val_data=val_data,
        client=client,
        gen_model=gen_model,
        eval_model=eval_model,
        baseline_loader=baseline_loader,
        use_skills=use_skills,
        skills_loading_mode=skills_loading_mode,
        anthropic_client=anthropic_client,
        openrouter_client=openrouter_client,
        eval_client=eval_client,
        skills_dir_override=skills_dir_override,
        debug=debug,
        eval_strategy=eval_strategy,
        router_model=router_model,
        router_client=router_client,
        router_type=router_type,
        gen_provider=gen_provider,
    )

    # Print metrics
    print("\n" + "="*80)
    print("Validation Results")
    print("="*80)

    metrics = result['metrics']

    print(f"\n{'Overall:':<30} {metrics['total']} questions")
    print(f"{'  Baseline Accuracy:':<30} {metrics['baseline_accuracy']:.2%} ({int(metrics['baseline_accuracy'] * metrics['total'])}/{metrics['total']})")
    print(f"{'  Skill Accuracy:':<30} {metrics['skill_accuracy']:.2%} ({int(metrics['skill_accuracy'] * metrics['total'])}/{metrics['total']})")
    print(f"{'  Improvement:':<30} {metrics['improvement']:+.2%} ({metrics['improvement'] * metrics['total']:+.1f})")
    print(f"{'  Fixes:':<30} {metrics['fixes']}")
    print(f"{'  Regressions:':<30} {metrics['regressions']}")
    print(f"{'  Net Improvement:':<30} {metrics['net_improvement']:+d}")

    print(f"\n{'Multiple-Choice:':<30} {metrics['mc']['total']} questions")
    print(f"{'  Baseline Accuracy:':<30} {metrics['mc']['baseline_accuracy']:.2%}")
    print(f"{'  Skill Accuracy:':<30} {metrics['mc']['skill_accuracy']:.2%}")
    print(f"{'  Improvement:':<30} {(metrics['mc']['skill_accuracy'] - metrics['mc']['baseline_accuracy']):+.2%}")

    print(f"\n{'Open-Ended:':<30} {metrics['open']['total']} questions")
    print(f"{'  Baseline Accuracy:':<30} {metrics['open']['baseline_accuracy']:.2%}")
    print(f"{'  Skill Accuracy:':<30} {metrics['open']['skill_accuracy']:.2%}")
    print(f"{'  Improvement:':<30} {(metrics['open']['skill_accuracy'] - metrics['open']['baseline_accuracy']):+.2%}")

    # Save results if requested
    if args.output:
        output_path = Path(args.output)
        output_data = {
            'checkpoint': args.checkpoint,
            'checkpoint_dir': str(checkpoint_dir),
            'metrics': metrics,
            'timestamp': pd.Timestamp.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✓ Results saved to: {output_path}")

    # Save detailed results to JSON
    detailed_results = result['detailed_results']
    output_json = output_dir / "validation_evaluation_results.json"

    # Get evaluation name and description from config if available
    if args.config:
        eval_name = config.get('evaluation', {}).get('name', 'checkpoint_evaluation')
        eval_desc = config.get('evaluation', {}).get('description', '')
    else:
        eval_name = f"checkpoint_evaluation_{checkpoint_name}" if checkpoint_name else 'checkpoint_evaluation'
        eval_desc = f"Evaluation of {checkpoint_name}" if checkpoint_name else 'Checkpoint evaluation'

    output_data = {
        'evaluation': {
            'name': eval_name,
            'description': eval_desc,
            'timestamp': pd.Timestamp.now().isoformat()
        },
        'configuration': {
            'skills_dir': str(skills_dir_override) if skills_dir_override else str(checkpoint_dir / 'skills'),
            'generation_model': gen_model,
            'evaluation_model': eval_model,
            'pot_mode': pot_mode_config,
            'skills_loading_mode': skills_loading_mode,
            'use_skills': use_skills
        },
        'metrics': metrics,
        'results': detailed_results
    }

    with open(output_json, 'w') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Detailed results saved to: {output_json}")

    # Print and save token usage summary
    token_tracker.summary(print_output=True)
    token_usage_file = output_dir / "token_usage.json"
    token_tracker.save(str(token_usage_file))

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
