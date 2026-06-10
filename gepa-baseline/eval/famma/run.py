#!/usr/bin/env python3
"""
GEPA system runner for FAMMA financial reasoning benchmark.

GEPA optimizes the system prompt itself using LLM-guided genetic/Pareto search.
It builds on the official FAMMA prompt as a seed and evolves it over training examples.

Usage:
    cd gepa-baseline
    python3.13 -m eval.famma.run \
        --task_name non_arithmetic \
        --api_provider dashscope \
        --generator_model qwen-flash \
        --reflection_model qwen-max \
        --max_metric_calls 150 \
        --save_path results/famma_non_arithmetic_qwen_flash

    # With Haiku 4.5 via OpenRouter
    python3.13 -m eval.famma.run \
        --task_name non_arithmetic \
        --api_provider openrouter \
        --generator_model anthropic/claude-3-5-haiku-20241022 \
        --reflection_model anthropic/claude-3-5-haiku-20241022 \
        --max_metric_calls 150 \
        --save_path results/famma_non_arithmetic_haiku45
"""

import os
import re
import sys
import json
import argparse
import pandas as pd
import openai
import gepa.optimize_anything as oa
from gepa.optimize_anything import optimize_anything, GEPAConfig, EngineConfig, ReflectionConfig
from dotenv import load_dotenv

load_dotenv()

# Try json_repair
try:
    import json_repair
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

DATA_FILES = {
    "non_arithmetic": {
        "train": os.path.join(DATA_DIR, "famma_non_arithmetic_gepa_train.csv"),
        "val":   os.path.join(DATA_DIR, "famma_non_arithmetic_gepa_val.csv"),
    },
    "arithmetic": {
        "train": os.path.join(DATA_DIR, "famma_arithmetic_gepa_train.csv"),
        "val":   os.path.join(DATA_DIR, "famma_arithmetic_gepa_val.csv"),
    },
}

# ── Seed prompts ──────────────────────────────────────────────────────────
# Non-PoT: Matches integration_example.py standard mode (lines 779-782)
SEED_PROMPT = """You are a highly knowledgeable financial expert. Please answer the questions in the finance domain. You are given context, images, questions and options.
The questions are multilingual (either in English, Chinese, or French) and multimodal (containing images as part of the question)."""

# PoT: Matches integration_example.py PoT mode (lines 734-747)
SEED_PROMPT_POT = """You are a highly knowledgeable financial expert with strong coding skills.

For this question, you should:
1. Generate Python code to solve the problem
2. Use clear variable names and comments
3. End your code with an EXPRESSION (NOT print()) that evaluates to the final answer
4. Put your code in a ```python code block

Example format:
```python
# Calculate the answer
result = (some calculation)
result  # This should be the final answer
```"""


# ── Data loading ───────────────────────────────────────────────────────────
def load_csv(path: str) -> list[dict]:
    df = pd.read_csv(path)
    records = []
    for _, row in df.iterrows():
        records.append({
            "question_id": str(row.get("question_id", "")),
            "question": str(row.get("question", "")),
            "context": str(row.get("context", "")) if pd.notna(row.get("context")) else "",
            "options": str(row.get("options", "")) if pd.notna(row.get("options")) else "",
            "answers": str(row.get("answers", "")),
            "question_type": str(row.get("question_type", "open-ended")),
        })
    return records


# ── LLM client factory ─────────────────────────────────────────────────────
def make_client(api_provider: str) -> openai.OpenAI:
    if api_provider == "dashscope":
        return openai.OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY", ""),
            base_url=os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
    elif api_provider == "openrouter":
        return openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            base_url="https://openrouter.ai/api/v1",
        )
    elif api_provider == "anthropic":
        return openai.OpenAI(
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            base_url="https://api.anthropic.com/v1",
        )
    else:
        return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


# ── Generation ─────────────────────────────────────────────────────────────
def build_prompt(system_prompt: str, example: dict) -> str:
    """Build full prompt matching integration_example.py build_famma_question_block exactly."""
    question_id = example["question_id"]
    question = example["question"]
    question_type = example["question_type"]
    context = example.get("context", "") or ""
    options = example.get("options", "") or ""

    # Sub_questions section (matches build_famma_question_block exactly)
    sub_questions_text = "Sub_questions:\n"
    sub_questions_text += f"- id: {question_id}\n"
    sub_questions_text += f"  type: {question_type}\n"
    sub_questions_text += f"  question: {question}\n"
    if question_type == "multiple-choice" and options and str(options).strip() not in ["nan", "None", ""]:
        sub_questions_text += f"  options: {options}\n"
    sub_questions_text += "\n"

    question_block = f"""Question Format:
- Context: The given financial context.
- Sub_questions: A list of sub-questions, where each contains:
id: unique identifier for the sub-question
type: question type ('multiple-choice' or 'open-ended')
question: the actual question text
- Images: Image placeholders like '<image_1>', '<image_2>' refer to accompanying images. If images are mentioned, they will be included alongside the textual context. If no images are provided, answer based solely on the textual context.

Answering Guidelines:
For each sub_question, provide:
- Answer:
    For multiple-choice questions, return the option index A, B, C, D, etc.
    For open-ended questions, provide a concise and precise answer.
- Explanation: Provide a clear and detailed explanation (maximum 200 words) for your answer in the same language as the question.
- Explanation Format: Write explanations in clear, natural language without using special characters or symbols that could interfere with JSON parsing (avoid \\n, \\t, etc.). Keep explanations concise and focused.

Your response must be in a standard JSON format and should follow this structure:
```json
{{
    "{question_id}": {{
        "answer": "<answer>",
        "explanation": "<explanation>"
    }}
}}
```
Ensure that the response strictly adheres to JSON syntax without any additional content.
Now please answer the following question:
context: {context}
{sub_questions_text}"""

    return system_prompt + "\n\n" + question_block


def generate(client: openai.OpenAI, model: str, prompt: str) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=4096,
    )
    return resp.choices[0].message.content.strip()


def extract_answer(response: str, question_id: str) -> tuple[str, str]:
    """Extract answer and explanation from JSON response."""
    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        try:
            if HAS_JSON_REPAIR:
                parsed = json_repair.loads(json_match.group(0))
            else:
                parsed = json.loads(json_match.group(0))

            if question_id in parsed:
                data = parsed[question_id]
                if isinstance(data, dict):
                    return str(data.get("answer", "")).strip(), str(data.get("explanation", "")).strip()
                return str(data).strip(), ""

            # Fallback: first value
            if parsed:
                first = next(iter(parsed.values()))
                if isinstance(first, dict):
                    return str(first.get("answer", "")).strip(), str(first.get("explanation", "")).strip()
                return str(first).strip(), ""
        except Exception:
            pass
    return response.strip(), ""


# ── PoT: Prompt, Code Execution, MC Selection ─────────────────────────────
# All logic below matches skill_learning/integration_example.py exactly.

def build_prompt_pot(system_prompt: str, example: dict) -> str:
    """Build PoT prompt matching integration_example.py PoT mode (lines 763-771)."""
    context = example.get("context", "") or ""
    question = example["question"]
    options = example.get("options", "") or ""

    prompt = system_prompt
    if context:
        prompt += f"\n\nContext: {context}"
    prompt += f"\n\nQuestion: {question}"
    if options and str(options).strip() not in ["nan", "None", ""]:
        prompt += f"\n\nOptions: {options}"
    prompt += "\n\nGenerate Python code to solve this problem:"
    return prompt


def extract_code_from_response(response_text: str) -> str:
    """Extract Python code from ```python or ``` blocks. Matches integration_example.py."""
    match = re.search(r'```python\s*\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r'```\s*\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def execute_pot_code(code_str: str, timeout: int = 10) -> tuple[str, bool]:
    """
    Execute Python code and return result.
    Matches integration_example.py execute_pot_code exactly:
    - Pre-imports numpy, math, scipy
    - Handles assignment vs expression last lines
    - eval() on last line for expressions
    """
    if not code_str:
        return "", False

    try:
        lines = code_str.strip().split('\n')
        last_line = lines[-1].strip()
        last_line_no_comment = last_line.split('#')[0].strip() if '#' in last_line else last_line

        # Pre-import common libraries
        namespace = {}
        try:
            import numpy as np
            import math
            namespace['np'] = np
            namespace['numpy'] = np
            namespace['math'] = math
        except ImportError:
            pass
        try:
            import numpy_financial as npf
            namespace['npf'] = npf
            namespace['numpy_financial'] = npf
        except ImportError:
            pass
        try:
            from scipy import stats as scipy_stats
            from scipy import optimize as scipy_optimize
            from scipy import interpolate as scipy_interpolate
            from scipy.stats import norm
            namespace['scipy_stats'] = scipy_stats
            namespace['scipy_optimize'] = scipy_optimize
            namespace['scipy_interpolate'] = scipy_interpolate
            namespace['norm'] = norm
            import scipy
            namespace['scipy'] = scipy
        except ImportError:
            pass

        # Handle multi-line dict/list endings
        if last_line_no_comment in ['}', ']']:
            bracket_map = {'}': '{', ']': '['}
            open_bracket = bracket_map[last_line_no_comment]
            close_bracket = last_line_no_comment
            depth = 0
            start_idx = len(lines) - 1
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i]
                depth += line.count(close_bracket) - line.count(open_bracket)
                if depth == 0 and open_bracket in line:
                    start_idx = i
                    break
            if start_idx > 0:
                exec('\n'.join(lines[:start_idx]), namespace)
            dict_code = '\n'.join(lines[start_idx:])
            try:
                result = eval(dict_code, namespace)
                if result is not None:
                    return str(result), True
            except Exception:
                pass

        # Assignment vs expression detection
        is_assignment = '=' in last_line_no_comment and not any(
            op in last_line_no_comment for op in ['==', '!=', '<=', '>=']
        )

        if is_assignment:
            exec('\n'.join(lines), namespace)
            var_name = last_line.split('=')[0].strip()
            for name in [var_name, 'result', 'answer', 'final_answer']:
                if name in namespace and namespace[name] is not None:
                    return str(namespace[name]), True
            return "", False
        else:
            if len(lines) > 1:
                exec('\n'.join(lines[:-1]), namespace)
            try:
                result = eval(last_line, namespace)
                if result is not None:
                    return str(result), True
            except Exception:
                if 'result' in namespace:
                    return str(namespace['result']), True
            return "", False

    except Exception:
        return "", False


def select_mc_option(
    sel_client: openai.OpenAI,
    sel_model: str,
    numerical_result: str,
    question: str,
    options: str,
    context: str = "",
) -> str:
    """Map numerical PoT result to MC letter. Matches integration_example.py selection prompt."""
    if not options or not options.strip():
        return numerical_result

    selection_prompt = f"""You are a helpful assistant that maps calculated numerical values to multiple-choice options.

Context: {context if context else "N/A"}

Question: {question}

Options:
{options}

Calculated Value: {numerical_result}

Your task:
1. Look at the calculated value: {numerical_result}
2. Compare it with each option
3. Select the option (A, B, C, D, or E) whose value most closely matches the calculated value

Important:
- Focus on numerical values, not text descriptions
- Consider that calculated values might have more decimal places than options
- If the calculated value is very close to an option (within 1%), select that option
- Return ONLY the letter (A, B, C, D, or E), nothing else

Your answer (just the letter):"""

    try:
        resp = sel_client.chat.completions.create(
            model=sel_model,
            messages=[{"role": "user", "content": selection_prompt}],
            temperature=0.0,
            max_tokens=10,
        )
        result = resp.choices[0].message.content.strip().upper()
        # Extract just the letter
        for ch in result:
            if ch in 'ABCDE':
                return ch
        return result
    except Exception as e:
        print(f"  [SEL ERROR] {e}", flush=True)
        return numerical_result


# ── Evaluation ─────────────────────────────────────────────────────────────
def mc_is_correct(predicted: str, ground_truth: str) -> bool:
    """Strict exact match."""
    return predicted.strip().upper() == ground_truth.strip().upper()


def open_is_correct(
    eval_client: openai.OpenAI,
    eval_model: str,
    example: dict,
    predicted: str,
    explanation: str = "",
) -> bool:
    """LLM judge using FAMMA official JudgePrompt."""
    question_id = example["question_id"]
    prompt = f"""You are a highly knowledgeable expert and teacher in the finance domain.
You are reviewing a student's answers to financial questions.
The questions are multilingual (either in English, Chinese, or French) and multimodal (containing images as part of the question).
You are given the context, the question, the student's answer and the ground-truth answer.
Please use the given information and refer to the ground-truth answer to determine if the student's answer is correct.

Question Format:
{{
    "question_id": "{question_id}",
    "context": "{example.get('context', '')}",
    "type": "{example['question_type']}",
    "question": "{example['question']}",
    "student_answer": "{predicted}",
    "student_explanation": "{explanation}",
    "ground_truth": "{example['answers']}"
}}

Evaluation Guidelines:
For multiple-choice questions:
Correct if student's answer matches the ground truth content, regardless of format
For open-ended questions:
Compare key concepts and accuracy of student's response with ground truth
Respond directly as either 'correct' or 'incorrect'.

Your response must be in a standard JSON format:
```json
{{
    "{question_id}": "correct" or "incorrect"
}}
```
Now please evaluate the following response:
{{"question_id": "{question_id}", "student_answer": "{predicted}", "ground_truth": "{example['answers']}"}}"""

    try:
        resp = eval_client.chat.completions.create(
            model=eval_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=256,
        )
        result_text = resp.choices[0].message.content.strip()
        json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
        if json_match:
            try:
                if HAS_JSON_REPAIR:
                    parsed = json_repair.loads(json_match.group(0))
                else:
                    parsed = json.loads(json_match.group(0))
                return parsed.get(question_id, "incorrect").lower() == "correct"
            except Exception:
                pass
        return "correct" in result_text.lower() and "incorrect" not in result_text.lower()
    except Exception as e:
        print(f"  Judge error for {question_id}: {e}")
        return False


# ── Main ───────────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="GEPA System - FAMMA Benchmark")
    parser.add_argument("--task_name", required=True, choices=["non_arithmetic", "arithmetic"])
    parser.add_argument("--api_provider", default="dashscope",
                        choices=["dashscope", "openrouter", "openai", "anthropic"])
    parser.add_argument("--generator_model", default="qwen-flash")
    parser.add_argument("--reflection_model", default=None,
                        help="Model for GEPA reflection LM (defaults to generator_model)")
    parser.add_argument("--reflection_provider", default=None,
                        choices=["dashscope", "openrouter", "openai", "anthropic"],
                        help="API provider for reflection LM (defaults to api_provider)")
    parser.add_argument("--eval_model", default=None,
                        help="Model for evaluation judge (defaults to qwen-max via dashscope)")
    parser.add_argument("--max_metric_calls", type=int, default=150,
                        help="GEPA optimization budget (number of evaluator calls)")
    parser.add_argument("--pot", action="store_true",
                        help="Enable Program of Thought mode (code generation + execution)")
    parser.add_argument("--selection_model", default="qwen-turbo",
                        help="Model for MC selection in PoT mode (default: qwen-turbo)")
    parser.add_argument("--minibatch_size", type=int, default=5,
                        help="Number of train examples per reflection proposal (default: 5)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit training samples (for smoke testing)")
    parser.add_argument("--val_limit", type=int, default=None,
                        help="Limit val samples for smoke testing (default: use full val set)")
    parser.add_argument("--save_path", required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    reflection_model = args.reflection_model or args.generator_model
    reflection_provider = args.reflection_provider or args.api_provider
    eval_model = args.eval_model or os.getenv("FAMMA_EVAL_MODEL", "qwen-max")

    pot_mode = args.pot

    print(f"\n{'='*60}")
    print(f"GEPA SYSTEM - FAMMA Benchmark")
    print(f"{'='*60}")
    print(f"Task:         {args.task_name}")
    print(f"PoT mode:     {pot_mode}")
    print(f"Generator:    {args.generator_model} [{args.api_provider}]")
    print(f"Reflection:   {reflection_model} [{reflection_provider}]")
    print(f"Eval model:   {eval_model}")
    if pot_mode:
        print(f"Selection:    {args.selection_model} [dashscope]")
    print(f"Budget:       {args.max_metric_calls} metric calls")
    print(f"Minibatch:    {args.minibatch_size} train examples per proposal")
    print(f"Parallel:     8 workers")
    if args.limit:
        print(f"Limit:        {args.limit} training samples")
    print(f"{'='*60}\n")

    # Load data
    train_path = DATA_FILES[args.task_name]["train"]
    val_path = DATA_FILES[args.task_name]["val"]
    train_data = load_csv(train_path)
    val_data = load_csv(val_path)

    if args.limit:
        train_data = train_data[:args.limit]
        print(f"Limited training to {args.limit} samples")
    if args.val_limit:
        val_data = val_data[:args.val_limit]
        print(f"Limited val to {args.val_limit} samples")

    print(f"Train: {len(train_data)}, Val: {len(val_data)}")

    # Clients
    gen_client = make_client(args.api_provider)

    # Eval client always uses dashscope qwen-max
    eval_client = openai.OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY", ""),
        base_url=os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    )

    # Selection client for PoT MC mapping (always DashScope)
    sel_client = eval_client  # reuse same dashscope client
    sel_model = args.selection_model

    # GEPA reflection LM string (uses litellm format)
    # Keyed on reflection_provider (teacher), independent of generator provider (student)
    if reflection_provider == "dashscope":
        import litellm
        litellm.api_base = os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        litellm.api_key = os.getenv("DASHSCOPE_API_KEY", "")
        reflection_lm = f"openai/{reflection_model}"
    elif reflection_provider == "openrouter":
        reflection_lm = f"openrouter/{reflection_model}"
    elif reflection_provider == "anthropic":
        reflection_lm = f"anthropic/{reflection_model}"
    else:
        reflection_lm = reflection_model

    # ── GEPA evaluator ─────────────────────────────────────────────────────
    def evaluator(candidate: str, example: dict) -> tuple[float, dict]:
        """
        GEPA evaluator: given a candidate system prompt + one FAMMA example,
        generate an answer and evaluate it.

        In PoT mode: generate code → execute → MC selection → evaluate.
        In standard mode: generate JSON answer → evaluate.
        """
        q_type = example["question_type"]
        explanation = ""
        side_info = {
            "question_id": example["question_id"],
            "question_type": q_type,
            "ground_truth": example["answers"],
        }

        if pot_mode:
            # PoT: generate code, execute, select
            prompt = build_prompt_pot(candidate, example)
            try:
                response = generate(gen_client, args.generator_model, prompt)
            except Exception as e:
                print(f"  [GEN ERROR] {example['question_id']}: {e}", flush=True)
                oa.log(f"Generation error: {e}")
                return 0.0, {**side_info, "error": str(e), "predicted": ""}

            code = extract_code_from_response(response)
            if not code:
                print(f"  [NO CODE] {example['question_id']}", flush=True)
                oa.log(f"No code extracted from response")
                return 0.0, {**side_info, "predicted": "", "code_error": "no_code_block"}

            code_result, success = execute_pot_code(code)
            if not success or not code_result:
                print(f"  [EXEC FAIL] {example['question_id']}: result={code_result!r}", flush=True)
                oa.log(f"Code execution failed")
                return 0.0, {**side_info, "predicted": "", "code_error": "execution_failed"}

            # For MC questions, map numerical result to letter
            predicted = code_result
            if q_type == "multiple-choice":
                options = example.get("options", "") or ""
                if options and predicted.strip().upper() not in ("A", "B", "C", "D", "E"):
                    predicted = select_mc_option(
                        sel_client, sel_model, code_result,
                        example["question"], options,
                        example.get("context", "") or "",
                    )
            side_info["code_result"] = code_result

        else:
            # Standard: JSON answer
            prompt = build_prompt(candidate, example)
            try:
                response = generate(gen_client, args.generator_model, prompt)
                predicted, explanation = extract_answer(response, example["question_id"])
            except Exception as e:
                print(f"  [GEN ERROR] {example['question_id']}: {e}", flush=True)
                oa.log(f"Generation error: {e}")
                return 0.0, {**side_info, "error": str(e), "predicted": ""}

        # Evaluate
        if q_type == "multiple-choice":
            correct = mc_is_correct(predicted, example["answers"])
        else:
            correct = open_is_correct(eval_client, eval_model, example, predicted, explanation)

        score = 1.0 if correct else 0.0

        # Diagnostic info
        status = "OK" if correct else "WRONG"
        extra = f" | code={side_info.get('code_result', '')!r}" if pot_mode else ""
        print(f"  [{status}] {example['question_id']} | {q_type} | pred={predicted!r} | truth={example['answers']!r}{extra}", flush=True)
        if not correct:
            oa.log(f"WRONG | type={q_type} | predicted={predicted!r} | truth={example['answers']!r}")
            oa.log(f"question={example['question'][:100]}")
        else:
            oa.log(f"CORRECT | type={q_type} | predicted={predicted!r}")

        side_info["predicted"] = predicted
        side_info["correct"] = correct
        return score, side_info

    # ── Run GEPA ───────────────────────────────────────────────────────────
    seed = SEED_PROMPT_POT if pot_mode else SEED_PROMPT
    objective_text = (
        "Optimize the system prompt to improve accuracy on FAMMA financial arithmetic questions. "
        "The model generates Python code to solve problems. The prompt should guide the model to "
        "write correct, executable code that produces accurate numerical answers. "
        "Questions are in English, Chinese, or French."
    ) if pot_mode else (
        "Optimize the system prompt to improve accuracy on FAMMA financial reasoning questions. "
        "Questions are in English, Chinese, or French and cover financial analysis, "
        "multiple-choice and open-ended formats."
    )
    result = optimize_anything(
        seed_candidate=seed,
        evaluator=evaluator,
        dataset=train_data,
        valset=val_data,
        objective=objective_text,
        config=GEPAConfig(
            engine=EngineConfig(
                max_metric_calls=args.max_metric_calls,
                parallel=True,
                max_workers=8,
            ),
            reflection=ReflectionConfig(
                reflection_lm=reflection_lm,
                reflection_minibatch_size=args.minibatch_size,
            ),
        ),
    )

    # ── Save results ───────────────────────────────────────────────────────
    os.makedirs(args.save_path, exist_ok=True)

    best_prompt_path = os.path.join(args.save_path, "best_prompt.txt")
    with open(best_prompt_path, "w") as f:
        f.write(result.best_candidate if isinstance(result.best_candidate, str)
                else json.dumps(result.best_candidate, indent=2))

    best_idx = result.best_idx
    best_score = result.val_aggregate_scores[best_idx] if result.val_aggregate_scores else None
    all_val_scores = result.val_aggregate_scores  # one per candidate (seed=0, then evolved)
    summary = {
        "task_name": args.task_name,
        "pot_mode": pot_mode,
        "api_provider": args.api_provider,
        "generator_model": args.generator_model,
        "reflection_model": reflection_model,
        "max_metric_calls": args.max_metric_calls,
        "best_idx": best_idx,
        "best_score": best_score,
        "seed_score": all_val_scores[0] if all_val_scores else None,
        "all_val_scores": all_val_scores,
        "total_metric_calls": result.total_metric_calls,
        "best_prompt_path": best_prompt_path,
    }
    with open(os.path.join(args.save_path, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"GEPA FAMMA run complete!")
    print(f"Seed score:  {all_val_scores[0] if all_val_scores else 'N/A':.4f}" if all_val_scores else "Seed score: N/A")
    print(f"Best score:  {best_score:.4f} (candidate #{best_idx})" if best_score is not None else "Best score: N/A")
    print(f"All val scores (per candidate): {[round(s,4) for s in all_val_scores]}" if all_val_scores else "")
    print(f"Best prompt saved to: {best_prompt_path}")
    print(f"Results saved to: {args.save_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
