"""
Integration Example: Complete Training Workflow

Demonstrates how to integrate the skill learning system with existing baseline scripts.
Uses the SAME prompts as baseline - only adds skill content when skills are enabled.

Generation: Official FAMMA QuestionPrompt
Evaluation: Official FAMMA JudgePrompt
"""

import os
import sys
import json
import re
import time
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our training components
from skill_learning.run_logger import RunLogger
from skill_learning.evidence_collector import EvidenceCollector
from skill_learning.skill_trainer import SkillTrainer
from skill_learning.skills_router import SkillsRouter, determine_skill_method
from skill_learning.baseline_loader import BaselineLoader, load_baseline
from skill_learning.config import load_config, cfg, get_api_keys, is_config_loaded, setup_from_config
from skill_learning.token_tracker import tracker as token_tracker

# Import API clients
from openai import OpenAI
from anthropic import Anthropic

# Try to import json_repair (used in baseline scripts)
try:
    import json_repair
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False
    print("Warning: json_repair not installed. Using standard json parsing.")

# Try to import LangChain for batch evaluation
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain not installed. Batch evaluation disabled.")


def setup_environment():
    """Setup environment and API client.

    Uses YAML config if loaded, otherwise falls back to .env variables.

    Returns:
        Tuple of (client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider)
        - gen_provider: 'openrouter', 'anthropic', 'dashscope', or 'auto'
        - eval_provider: 'openrouter', 'anthropic', 'dashscope', or 'auto'
    """
    load_dotenv()

    # If config is loaded, use setup_from_config
    if is_config_loaded():
        result = setup_from_config()
        # Set global for get_gen_client helper
        global _openrouter_client, _gen_provider
        _openrouter_client = result[4]  # openrouter_client
        _gen_provider = result[5]  # gen_provider
        # Configure HF datasets cache
        os.environ['HF_DATASETS_CACHE'] = str(project_root / 'datasets')
        return result

    # Fallback to environment variables (backward compatibility)
    # Priority: DASHSCOPE_API_KEY > OPENAI_API_KEY > API_KEY (same as baseline)
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")

    # Priority: QWEN_API_BASE > OPENAI_BASE_URL > API_BASE_URL (same as baseline)
    base_url = os.getenv("QWEN_API_BASE") or os.getenv("OPENAI_BASE_URL") or os.getenv("API_BASE_URL")

    # Default to DashScope if DASHSCOPE_API_KEY is set
    if os.getenv("DASHSCOPE_API_KEY") and not base_url:
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # Separate models for generation and evaluation
    # Default model (fallback for legacy compatibility)
    if os.getenv("DASHSCOPE_API_KEY"):
        default_model = os.getenv("MODEL", "qwen-max")
    else:
        default_model = os.getenv("MODEL", "gpt-4o")

    # Get generation and evaluation models (fall back to default MODEL if not specified)
    gen_model = os.getenv("GEN_MODEL", default_model)
    eval_model = os.getenv("EVAL_MODEL", default_model)

    # Get providers from env (optional, default to 'auto')
    gen_provider = os.getenv("GEN_PROVIDER", "auto")
    eval_provider = os.getenv("EVAL_PROVIDER", "auto")

    if gen_model == eval_model:
        print(f"✓ Using model: {gen_model} (both generation and evaluation)")
    else:
        print(f"✓ Using generation model: {gen_model}")
        print(f"✓ Using evaluation model: {eval_model}")

    if not api_key:
        raise ValueError("No API key found. Set DASHSCOPE_API_KEY or OPENAI_API_KEY in .env")

    # OpenAI-compatible client for baseline/evaluation
    client = OpenAI(api_key=api_key, base_url=base_url)

    # Create clients based on gen_provider
    anthropic_client = None
    openrouter_client = None

    if gen_provider == 'openrouter':
        # Explicit OpenRouter provider
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if openrouter_api_key:
            openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
            print(f"✓ OpenRouter client created for {gen_model} (explicit provider)")
        else:
            print(f"⚠ OPENROUTER_API_KEY not set but gen_provider is 'openrouter'")
    elif gen_provider == 'anthropic':
        # Explicit Anthropic provider
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_api_key:
            anthropic_client = Anthropic(api_key=anthropic_api_key)
            print(f"✓ Anthropic client created for {gen_model} (explicit provider)")
        else:
            print(f"⚠ ANTHROPIC_API_KEY not set but gen_provider is 'anthropic'")
    elif gen_provider == 'dashscope':
        # Explicit DashScope provider - client already created above
        print(f"✓ DashScope client for {gen_model} (explicit provider)")
    else:
        # Auto-detect from model name
        if gen_model.startswith('anthropic/'):
            # OpenRouter model format
            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            if openrouter_api_key:
                openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"✓ OpenRouter client created for {gen_model} (auto-detected)")
        elif gen_model.lower().startswith('claude'):
            # Claude model - try Anthropic first
            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_api_key:
                anthropic_client = Anthropic(api_key=anthropic_api_key)
                print(f"✓ Anthropic client created for progressive loading (auto-detected)")
            else:
                # Fallback to OpenRouter
                openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                if openrouter_api_key:
                    openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                    print(f"✓ OpenRouter client created for {gen_model} (fallback)")
                else:
                    print(f"⚠ ANTHROPIC_API_KEY not set - will use router method for Claude")

    # Create eval_client based on eval_provider
    eval_client = client  # Default to DashScope client
    if eval_provider == 'openrouter':
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if openrouter_api_key:
            eval_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
            print(f"✓ Eval client: OpenRouter ({eval_model})")
    elif eval_provider == 'anthropic':
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_api_key:
            eval_client = Anthropic(api_key=anthropic_api_key)
            print(f"✓ Eval client: Anthropic ({eval_model})")
    elif eval_provider == 'dashscope':
        print(f"✓ Eval client: DashScope ({eval_model})")
    else:
        # Auto-detect from eval_model
        if eval_model.startswith('anthropic/'):
            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            if openrouter_api_key:
                eval_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"✓ Eval client: OpenRouter (auto-detected)")
        elif eval_model.lower().startswith('claude'):
            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_api_key:
                eval_client = Anthropic(api_key=anthropic_api_key)
                print(f"✓ Eval client: Anthropic (auto-detected)")

    # Set globals for get_gen_client helper
    _openrouter_client = openrouter_client
    _gen_provider = gen_provider

    # Configure HF datasets cache
    os.environ['HF_DATASETS_CACHE'] = str(project_root / 'datasets')

    return client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider


# Global openrouter_client and gen_provider (set by setup_environment)
_openrouter_client = None
_gen_provider = 'auto'


def get_gen_client(model: str, anthropic_client, fallback_client):
    """Get the appropriate client for generation based on provider and model name.

    Priority:
    1. Explicit provider (openrouter, anthropic) from config/env
    2. Auto-detect from model name (anthropic/*, claude* -> OpenRouter/Anthropic)
    3. Fallback client (DashScope/OpenAI)
    """
    global _openrouter_client, _gen_provider

    # Explicit provider takes precedence
    if _gen_provider == 'openrouter' and _openrouter_client:
        return _openrouter_client
    if _gen_provider == 'anthropic' and anthropic_client:
        return anthropic_client
    if _gen_provider == 'dashscope':
        return fallback_client

    # Auto-detect from model name
    if model.lower().startswith('claude') or model.startswith('anthropic/'):
        if _openrouter_client:
            return _openrouter_client
        if anthropic_client:
            return anthropic_client
    return fallback_client


def _is_valid_answer_structure(parsed: Any) -> bool:
    """Check if parsed result has valid answer structure.

    Valid structures:
    - Dict with 'answer' key: {"answer": ..., "explanation": ...}
    - Dict of dicts with 'answer' key: {"qid": {"answer": ..., "explanation": ...}}
    - List of dicts with 'answer' key: [{"answer": ..., "explanation": ...}]
    """
    if parsed is None:
        return False

    if isinstance(parsed, dict):
        # Direct answer dict
        if 'answer' in parsed:
            return True
        # Dict of answer dicts (keyed by question_id)
        for value in parsed.values():
            if isinstance(value, dict) and 'answer' in value:
                return True
        return False

    if isinstance(parsed, list) and len(parsed) > 0:
        # Check if first item is a valid answer dict
        first = parsed[0]
        if isinstance(first, dict) and 'answer' in first:
            return True
        # Check nested structure
        if isinstance(first, list) and len(first) > 0:
            # Nested list - likely garbage from json_repair
            return False
        return False

    return False


def parse_json_response(response_text: str) -> Tuple[Optional[Any], Optional[str]]:
    """
    Parse JSON response with json_repair for invalid escape sequences.
    Validates that result has expected answer structure to avoid garbage from json_repair.
    """
    if not response_text:
        return None, "Empty response"

    # First try to extract JSON object from text (more targeted)
    # This avoids json_repair creating garbage from mathematical expressions

    # Extract JSON from markdown code blocks first (most reliable)
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(1))
            if _is_valid_answer_structure(parsed):
                return parsed, None
        except json.JSONDecodeError:
            if HAS_JSON_REPAIR:
                try:
                    parsed = json_repair.loads(json_match.group(1))
                    if _is_valid_answer_structure(parsed):
                        return parsed, None
                except Exception:
                    pass

    # Extract any JSON object with greedy match
    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(0))
            if _is_valid_answer_structure(parsed):
                return parsed, None
        except json.JSONDecodeError:
            if HAS_JSON_REPAIR:
                try:
                    parsed = json_repair.loads(json_match.group(0))
                    if _is_valid_answer_structure(parsed):
                        return parsed, None
                except Exception:
                    pass

    # Try full text with standard json.loads (unlikely to work but safe)
    try:
        parsed = json.loads(response_text)
        if _is_valid_answer_structure(parsed):
            return parsed, None
    except json.JSONDecodeError:
        pass

    # Last resort: use json_repair on full text but validate result
    if HAS_JSON_REPAIR:
        try:
            parsed = json_repair.loads(response_text)
            if _is_valid_answer_structure(parsed):
                return parsed, None
        except Exception:
            pass

    return None, "Could not parse valid JSON answer from response"


def call_llm(
    client,
    model: str,
    prompt: str,
    max_tokens: int = None,
    max_retries: int = 3,
    track_phase: str = None,
    track_component: str = None
) -> str:
    """
    Call LLM with either OpenAI or Anthropic client.

    Includes retry logic for rate limit errors (429).

    Args:
        client: OpenAI or Anthropic client
        model: Model name
        prompt: Prompt text
        max_tokens: Maximum tokens in response
        max_retries: Maximum number of retries for rate limit errors
        track_phase: Phase name for token tracking (e.g., "phase3")
        track_component: Component name for token tracking (e.g., "generation_baseline")

    Returns:
        Response text
    """
    if max_tokens is None:
        max_tokens = cfg('model_params.gen_max_tokens') or int(os.getenv('GEN_MAX_TOKENS', '4096'))

    retry_delay = 10  # seconds to wait on rate limit

    for attempt in range(max_retries + 1):
        try:
            # Detect client type
            if isinstance(client, Anthropic):
                # Anthropic API
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                # Track tokens if requested
                if track_phase and track_component:
                    token_tracker.add_from_response(track_phase, track_component, response, model)
                return response.content[0].text
            else:
                # OpenAI-compatible API
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=max_tokens
                )
                # Track tokens if requested
                if track_phase and track_component:
                    token_tracker.add_from_response(track_phase, track_component, response, model)
                return response.choices[0].message.content

        except Exception as e:
            error_str = str(e)
            # Check for rate limit error (429)
            if '429' in error_str or 'rate_limit' in error_str.lower():
                if attempt < max_retries:
                    print(f"  ⚠️  Rate limit hit (attempt {attempt + 1}/{max_retries + 1}), sleeping {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # Exponential backoff
                    continue
                else:
                    print(f"  ❌ Rate limit exceeded after {max_retries + 1} attempts")
                    raise
            else:
                # Non-rate-limit error, re-raise immediately
                raise


def execute_pot_code(code_str: str, timeout: int = 10) -> tuple[str, bool]:
    """
    Execute Python code and return the result.
    Same logic as run_experiment.execute_code (single namespace, assignment vs expression).

    Supports three types of code endings:
    1. Expression: `x + y` - eval the last line
    2. Assignment: `result = x + y` - exec all, get variable
    3. Multi-line dict/list: `{ 'key': value }` - eval the entire block
    """
    if not code_str:
        return "", False

    try:
        lines = code_str.strip().split('\n')
        last_line = lines[-1].strip()

        # Strip inline comments for assignment detection (e.g., "x  # comment with = sign")
        last_line_no_comment = last_line.split('#')[0].strip() if '#' in last_line else last_line

        # Pre-import common libraries to avoid import errors in generated code
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
            # Also make scipy available as module
            import scipy
            namespace['scipy'] = scipy
        except ImportError:
            pass

        # Handle multi-line dict/list endings (e.g., last line is '}' or ']')
        if last_line_no_comment in ['}', ']']:
            bracket_map = {'}': '{', ']': '['}
            open_bracket = bracket_map[last_line_no_comment]
            close_bracket = last_line_no_comment

            # Search backwards for the matching opening bracket
            depth = 0
            start_idx = len(lines) - 1
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i]
                depth += line.count(close_bracket) - line.count(open_bracket)
                if depth == 0 and open_bracket in line:
                    start_idx = i
                    break

            # Execute lines before the dict/list
            if start_idx > 0:
                exec('\n'.join(lines[:start_idx]), namespace)

            # Eval the dict/list block and return as string
            dict_code = '\n'.join(lines[start_idx:])
            try:
                result = eval(dict_code, namespace)
                if result is not None:
                    return str(result), True
            except Exception:
                pass  # Fall through to original logic

        # Use comment-stripped version for assignment detection
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

    except Exception as e:
        return "", False


def extract_code_from_response(response_text: str) -> str:
    """
    Extract Python code from LLM response.
    Only returns content from explicit code blocks (```python or ```).
    If no code block is found, returns "" so we do not try to execute narrative as code.
    """
    # ```python ... ```
    pattern1 = r'```python\s*\n(.*?)\n```'
    match = re.search(pattern1, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # ``` ... ``` (no language specified)
    pattern2 = r'```\s*\n(.*?)\n```'
    match = re.search(pattern2, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # DEBUG: Print response when no code block found
    print("\n" + "="*80)
    print("[DEBUG] No code block found in response:")
    print("-"*80)
    print(response_text[:2000] if len(response_text) > 2000 else response_text)
    print("="*80 + "\n")

    return ""


def select_mc_option_from_numerical_result(
    numerical_result: str,
    question: str,
    options: str,
    context: str = "",
    client = None,
    model: str = "qwen-turbo",
    track_phase: str = None,
    track_component: str = None
) -> str:
    """
    Map numerical PoT result to multiple-choice letter (A, B, C, D, E).

    Args:
        numerical_result: The numerical answer from code execution
        question: The original question text
        options: Multiple choice options string
        context: Question context (optional)
        client: OpenAI-compatible client (DashScope for Qwen)
        model: Model to use for selection (default: qwen-turbo for speed)
        track_phase: Phase name for token tracking (e.g., "phase3")
        track_component: Component name for token tracking (e.g., "selection")

    Returns:
        Selected letter (A, B, C, D, E) or empty string if selection fails
    """
    # If no options provided, return the numerical result as-is
    if not options or not options.strip():
        return numerical_result

    # Build selection prompt
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
        if client is None:
            # No client provided, return numerical result as-is
            return numerical_result

        # Detect client type and call appropriate API
        client_class_name = type(client).__name__

        if client_class_name == 'Anthropic':
            # Anthropic API
            response = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": selection_prompt}],
                temperature=0.0,
                max_tokens=10
            )
            # Track tokens if requested
            if track_phase and track_component:
                token_tracker.add_from_response(track_phase, track_component, response, model)
            result = response.content[0].text.strip().upper()
        else:
            # OpenAI-compatible API (OpenAI, DashScope, etc.)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": selection_prompt}],
                temperature=0.0,
                max_tokens=10
            )
            # Track tokens if requested
            if track_phase and track_component:
                token_tracker.add_from_response(track_phase, track_component, response, model)
            result = response.choices[0].message.content.strip().upper()

        # Extract letter
        if result in ['A', 'B', 'C', 'D', 'E']:
            return result

        # Try to extract letter from response
        match = re.search(r'([A-E])', result)
        if match:
            return match.group(1)

        # Selection failed, return numerical result
        return numerical_result

    except Exception as e:
        # On error, return numerical result as-is
        print(f"  ⚠️  Selection error: {e}, returning numerical result")
        return numerical_result

def build_famma_question_block(
    question_id: str,
    question: str,
    question_type: str,
    context: str,
    options: Optional[str] = None
) -> str:
    """
    Build FAMMA-format question block for progressive loading.

    This is the question portion of the FAMMA prompt, used by progressive
    loading to ensure consistent JSON response format.

    Args:
        question_id: Unique question identifier
        question: The question text
        question_type: 'multiple-choice' or 'open-ended'
        context: Question context
        options: MC options (if applicable)

    Returns:
        FAMMA question block string
    """
    # Build sub_questions section
    sub_questions_text = "Sub_questions:\n"
    sub_questions_text += f"- id: {question_id}\n"
    sub_questions_text += f"  type: {question_type}\n"
    sub_questions_text += f"  question: {question}\n"
    if question_type == 'multiple-choice' and options and str(options).strip() not in ['nan', 'None', '']:
        sub_questions_text += f"  options: {options}\n"
    sub_questions_text += "\n"

    return f"""Question Format:
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


def build_generation_prompt(
    question_id: str,
    question: str,
    question_type: str,
    context: str,
    options: Optional[str] = None,
    skill_content: Optional[str] = None
) -> str:
    """
    Build generation prompt using OFFICIAL FAMMA QuestionPrompt.

    Supports both standard JSON response mode and PoT (Program of Thought) mode.
    Set POT_MODE=true environment variable to enable code generation.

    Args:
        question_id: Unique question identifier
        question: The question text
        question_type: 'multiple-choice' or 'open-ended'
        context: Question context
        options: MC options (if applicable)
        skill_content: Optional skill content to prepend (for skill-based generation)

    Returns:
        Complete prompt string
    """
    # Check if PoT mode is enabled
    pot_mode = cfg('skills.pot_mode') if cfg('skills.pot_mode') is not None else os.getenv("POT_MODE", "false").lower() == "true"

    if pot_mode:
        # PoT mode: Use code generation prompt
        pot_instructions = """You are a highly knowledgeable financial expert with strong coding skills.

For this question, you should:
1. Generate Python code to solve the problem
2. Use clear variable names and comments
3. End your code with an EXPRESSION (NOT print()) that evaluates to the final answer
4. Put your code in a ```python code block

Example format:
```python
# Patterns you used or referred in the [Domain Knowledge] (just Pattern Name)
# Calculate the answer
result = (some calculation)
result  # This should be the final answer
```

"""
        if skill_content:
            skill_prefix = f"""[Domain Knowledge for Reference]
The following domain knowledge may help you solve this problem:

{skill_content}

[End of Domain Knowledge]

"""
            prompt = pot_instructions + skill_prefix
        else:
            prompt = pot_instructions

        # Add the question
        if context:
            prompt += f"\nContext: {context}\n"
        prompt += f"\nQuestion: {question}\n"
        if options:
            prompt += f"\nOptions: {options}\n"

        prompt += "\nGenerate Python code to solve this problem:"
        return prompt

    else:
        # Standard mode: Use JSON response prompt
        # Build the question block
        question_block = build_famma_question_block(question_id, question, question_type, context, options)

        # Role prompt prefix
        role_prompt = f"""You are a highly knowledgeable financial expert. Please answer the questions in the finance domain. You are given context, images, questions and options.
The questions are multilingual (either in English, Chinese, or French) and multimodal (containing images as part of the question).

"""

        # If skill content is provided, prepend it as domain knowledge
        if skill_content:
            skill_prefix = f"""[Domain Knowledge for Reference]
The following domain knowledge may help you answer financial questions more accurately:

{skill_content}

[End of Domain Knowledge]

"""
            return role_prompt + skill_prefix + question_block
        else:
            return role_prompt + question_block


def generate_answer(
    client,  # OpenAI or Anthropic client for generation
    model: str,
    question_id: str,
    question: str,
    question_type: str,
    context: str,
    options: Optional[str] = None,
    skill_content: Optional[str] = None,
    selection_client = None,  # Optional separate client for MC selection (PoT mode)
    track_component: str = None  # Token tracking component ("generation_baseline" or "generation_skill")
) -> Dict[str, Any]:
    """
    Generate answer using the official FAMMA prompt.

    Args:
        client: OpenAI or Anthropic client for generation
        model: Model name
        question_id: Question ID
        question: Question text
        question_type: 'multiple-choice' or 'open-ended'
        context: Question context
        options: MC options (if applicable)
        skill_content: Optional skill content for skill-based generation
        selection_client: Optional separate client for MC selection (if model mismatch in PoT mode)
        track_component: Component name for token tracking ("generation_baseline" or "generation_skill")

    Returns:
        Dict with answer, explanation, and metadata
    """
    prompt = build_generation_prompt(
        question_id=question_id,
        question=question,
        question_type=question_type,
        context=context,
        options=options,
        skill_content=skill_content
    )

    start_time = time.time()
    gen_max_tokens = cfg('model_params.gen_max_tokens') or int(os.getenv('GEN_MAX_TOKENS', '4096'))

    try:
        response_text = call_llm(
            client, model, prompt, max_tokens=gen_max_tokens,
            track_phase="phase3" if track_component else None,
            track_component=track_component
        )
        elapsed = time.time() - start_time

        # Check if PoT mode is enabled
        pot_mode = cfg('skills.pot_mode') if cfg('skills.pot_mode') is not None else os.getenv("POT_MODE", "false").lower() == "true"

        if pot_mode:
            # PoT mode: Extract and execute Python code
            code = extract_code_from_response(response_text)
            if code:
                result, success = execute_pot_code(code)
                if success:
                    # For MC questions, map numerical result to letter
                    if question_type == 'multiple-choice' and options:
                        # Use selection function to map numerical to MC option
                        # Use selection_client if provided (for model mismatch cases)
                        sel_client = selection_client if selection_client is not None else client
                        selected_option = select_mc_option_from_numerical_result(
                            numerical_result=result,
                            question=question,
                            options=options,
                            context=context,
                            client=sel_client,
                            model=cfg('models.selection') or os.getenv("SELECTION_MODEL", "qwen-turbo"),
                            track_phase="phase3" if track_component else None,
                            track_component="selection" if track_component else None
                        )
                        return {
                            "answer": selected_option,
                            "explanation": f"Code execution result: {result}, selected option: {selected_option}",
                            "code_result": result,
                            "generated_code": code,  # Store code for refinement
                            "code_execution_success": True,
                            "elapsed": elapsed
                        }
                    else:
                        # Open-ended: return numerical result directly
                        return {
                            "answer": result,
                            "explanation": f"Code execution result: {result}",
                            "generated_code": code,  # Store code for refinement
                            "code_execution_success": True,
                            "elapsed": elapsed
                        }
                else:
                    return {
                        "answer": "",
                        "explanation": "Code execution failed",
                        "parse_error": "Code execution error",
                        "generated_code": code,  # Store failed code for debugging
                        "code_execution_success": False,
                        "elapsed": elapsed
                    }
            else:
                return {
                    "answer": "",
                    "explanation": "No code found in response",
                    "parse_error": "No code block found",
                    "generated_code": None,
                    "code_execution_success": False,
                    "elapsed": elapsed
                }

        # Standard mode: Parse JSON response
        parsed, error = parse_json_response(response_text)
        if error or not parsed:
            return {
                "answer": "",
                "explanation": response_text,
                "parse_error": error,
                "elapsed": elapsed
            }

        # Extract answer - handle both dict and list responses
        if isinstance(parsed, dict):
            # Dict response: {question_id: {answer, explanation}}
            if question_id in parsed:
                answer_data = parsed[question_id]
                if isinstance(answer_data, dict):
                    return {
                        "answer": answer_data.get("answer", ""),
                        "explanation": answer_data.get("explanation", ""),
                        "elapsed": elapsed
                    }
                elif isinstance(answer_data, str):
                    return {
                        "answer": answer_data,
                        "explanation": "",
                        "elapsed": elapsed
                    }
            else:
                # Try to get any answer from dict
                for qid, data in parsed.items():
                    if isinstance(data, dict):
                        return {
                            "answer": data.get("answer", ""),
                            "explanation": data.get("explanation", ""),
                            "elapsed": elapsed
                        }
                    elif isinstance(data, str):
                        return {
                            "answer": data,
                            "explanation": "",
                            "elapsed": elapsed
                        }
        elif isinstance(parsed, list) and len(parsed) > 0:
            # List response: [{answer, explanation}, ...]
            first_item = parsed[0]
            if isinstance(first_item, dict):
                return {
                    "answer": first_item.get("answer", ""),
                    "explanation": first_item.get("explanation", ""),
                    "elapsed": elapsed
                }
            elif isinstance(first_item, str):
                return {
                    "answer": first_item,
                    "explanation": "",
                    "elapsed": elapsed
                }

        return {
            "answer": "",
            "explanation": "",
            "parse_error": f"Question {question_id} not found in response",
            "elapsed": elapsed
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "answer": "",
            "explanation": str(e),
            "error": str(e),
            "elapsed": elapsed
        }


def evaluate_answer(
    client,  # OpenAI or Anthropic client
    model: str,
    question_id: str,
    question: str,
    question_type: str,
    context: str,
    generated_answer: str,
    generated_explanation: str,
    ground_truth: str,
    eval_strategy: str = "llm_only",  # "llm_only" or "hybrid"
    track_phase: str = None,
    track_component: str = None
) -> float:
    """
    Evaluate answer using the official FAMMA JudgePrompt.

    This is the SAME evaluation as scripts/evaluate_baseline_nonarithmetic.py.

    Args:
        eval_strategy: Evaluation strategy
            - "llm_only": Use LLM judge for all questions (default)
            - "hybrid": Rule-based for MC, LLM judge for open questions
        track_phase: Phase name for token tracking (e.g., "phase3")
        track_component: Component name for token tracking (e.g., "evaluation")

    Returns:
        Score (1.0 for correct, 0.0 for incorrect)
    """
    # Hybrid strategy: rule-based for multiple-choice
    if eval_strategy == "hybrid" and question_type == "multiple-choice":
        # Rule-based: exact match (case-insensitive)
        gen_clean = str(generated_answer).strip().upper()
        gt_clean = str(ground_truth).strip().upper()
        is_correct = (gen_clean == gt_clean)
        return 1.0 if is_correct else 0.0

    # LLM judge for all other cases
    # Build question dict (same format as baseline)
    question_dict = {
        "question_id": question_id,
        "context": context,
        "type": question_type,
        "question": question,
        "student_answer": generated_answer,
        "student_explanation": generated_explanation,
        "ground_truth": ground_truth
    }

    # Official FAMMA JudgePrompt (EXACT copy from baseline script)
    prompt = f"""You are a highly knowledgeable expert and teacher in the finance domain.
You are reviewing a student's answers to financial questions.
The questions are multilingual (either in English, Chinese, or French) and multimodal (containing images as part of the question). '<image_1>, <image_2> ...' mentioned in the text of the context or question are sequential placeholders for images, which are fed at the same time as the textual information.
You are given the context, the question, the student's answer and the student's explanation and the ground-truth answer.
Please use the given information and refer to the ground-truth answer to determine if the student's answer is correct.

Question Format:
{{
    "question_id": "{question_dict['question_id']}",
    "context": "{question_dict['context']}",
    "type": "{question_dict['type']}",
    "question": "{question_dict['question']}",
    "student_answer": "{question_dict['student_answer']}",
    "student_explanation": "{question_dict['student_explanation']}",
    "ground_truth": "{question_dict['ground_truth']}"
}}

Evaluation Guidelines:
For multiple-choice questions:
Correct if student's answer matches the ground truth content, regardless of format
Example: If correct answer is "A. Stock market", both "A" and "Stock market" are considered correct
Focus on whether the student selected the right concept/answer, not the format
For open-ended questions:
Compare key concepts and accuracy of student's response with ground truth
Respond directly as either 'correct' or 'incorrect'.

Your response must be in a standard JSON format and should follow this structure:
```json
{{
    "{question_id}": "correct" or "incorrect"
}}
```
Now please evaluate the following response:
{question_dict}"""

    try:
        result_text = call_llm(
            client, model, prompt, max_tokens=1024,
            track_phase=track_phase, track_component=track_component
        ).strip()

        # Parse JSON - looking for "correct" or "incorrect" string (same as baseline)
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            try:
                if HAS_JSON_REPAIR:
                    result = json_repair.loads(json_match.group(0))
                else:
                    result = json.loads(json_match.group(0))
                # Get the value for this question_id
                is_correct_str = result.get(question_id, "incorrect").lower()
                return 1.0 if is_correct_str == "correct" else 0.0
            except (json.JSONDecodeError, Exception):
                pass

        # Fallback: check for "correct" in response
        if "correct" in result_text.lower() and "incorrect" not in result_text.lower():
            return 1.0
        return 0.0

    except Exception as e:
        print(f"  ✗ Evaluation failed for {question_id}: {e}")
        return 0.0


def _build_eval_prompt(
    question_id: str,
    question: str,
    question_type: str,
    context: str,
    generated_answer: str,
    generated_explanation: str,
    ground_truth: str
) -> str:
    """Build evaluation prompt for a single question."""
    question_dict = {
        "question_id": question_id,
        "context": context,
        "type": question_type,
        "question": question,
        "student_answer": generated_answer,
        "student_explanation": generated_explanation,
        "ground_truth": ground_truth
    }

    return f"""You are a highly knowledgeable expert and teacher in the finance domain.
You are reviewing a student's answers to financial questions.
The questions are multilingual (either in English, Chinese, or French) and multimodal (containing images as part of the question). '<image_1>, <image_2> ...' mentioned in the text of the context or question are sequential placeholders for images, which are fed at the same time as the textual information.
You are given the context, the question, the student's answer and the student's explanation and the ground-truth answer.
Please use the given information and refer to the ground-truth answer to determine if the student's answer is correct.

Question Format:
{{
    "question_id": "{question_dict['question_id']}",
    "context": "{question_dict['context']}",
    "type": "{question_dict['type']}",
    "question": "{question_dict['question']}",
    "student_answer": "{question_dict['student_answer']}",
    "student_explanation": "{question_dict['student_explanation']}",
    "ground_truth": "{question_dict['ground_truth']}"
}}

Evaluation Guidelines:
For multiple-choice questions:
Correct if student's answer matches the ground truth content, regardless of format
Example: If correct answer is "A. Stock market", both "A" and "Stock market" are considered correct
Focus on whether the student selected the right concept/answer, not the format
For open-ended questions:
Compare key concepts and accuracy of student's response with ground truth
Respond directly as either 'correct' or 'incorrect'.

Your response must be in a standard JSON format and should follow this structure:
```json
{{
    "{question_id}": "correct" or "incorrect"
}}
```
Now please evaluate the following response:
{question_dict}"""


def _parse_eval_response(result_text: str, question_id: str) -> float:
    """Parse evaluation response to get score."""
    try:
        # Parse JSON - looking for "correct" or "incorrect" string
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            try:
                if HAS_JSON_REPAIR:
                    result = json_repair.loads(json_match.group(0))
                else:
                    result = json.loads(json_match.group(0))
                is_correct_str = result.get(question_id, "incorrect").lower()
                return 1.0 if is_correct_str == "correct" else 0.0
            except (json.JSONDecodeError, Exception):
                pass

        # Fallback: check for "correct" in response
        if "correct" in result_text.lower() and "incorrect" not in result_text.lower():
            return 1.0
        return 0.0
    except Exception:
        return 0.0


def evaluate_answers_batch(
    eval_items: List[Dict[str, Any]],
    eval_model: str,
    batch_size: int = 10
) -> List[float]:
    """
    Evaluate multiple answers in batch using LangChain.

    Args:
        eval_items: List of dicts with keys:
            - question_id, question, question_type, context
            - generated_answer, generated_explanation, ground_truth
        eval_model: Model name for evaluation
        batch_size: Number of concurrent requests (default: 10)

    Returns:
        List of scores (1.0 for correct, 0.0 for incorrect)
    """
    if not eval_items:
        return []

    # Check if LangChain is available
    if not LANGCHAIN_AVAILABLE:
        print("  LangChain not available, falling back to sequential evaluation")
        # Fallback to sequential - need client
        return None  # Signal to caller to use sequential

    # Get API credentials
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("QWEN_API_BASE") or os.getenv("OPENAI_BASE_URL")

    if not api_key:
        print("  No API key found for batch evaluation")
        return None

    # Build prompts for all items
    prompts = []
    for item in eval_items:
        prompt = _build_eval_prompt(
            question_id=item['question_id'],
            question=item['question'],
            question_type=item['question_type'],
            context=item['context'],
            generated_answer=item['generated_answer'],
            generated_explanation=item['generated_explanation'],
            ground_truth=item['ground_truth']
        )
        prompts.append([HumanMessage(content=prompt)])

    # Initialize LangChain client
    llm = ChatOpenAI(
        model=eval_model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.0,
        max_tokens=1024
    )

    # Batch call
    print(f"  Batch evaluating {len(prompts)} answers (batch_size={batch_size})...")
    try:
        responses = llm.batch(prompts, config={"max_concurrency": batch_size})
    except Exception as e:
        print(f"  Batch evaluation failed: {e}")
        return None

    # Parse responses
    scores = []
    for i, response in enumerate(responses):
        result_text = response.content if hasattr(response, 'content') else str(response)
        question_id = eval_items[i]['question_id']
        score = _parse_eval_response(result_text, question_id)
        scores.append(score)

    return scores


def load_dataset(csv_path: Path) -> pd.DataFrame:
    """Load dataset from CSV file."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} questions from {csv_path.name}")
    return df


def run_system_with_logging(
    data: pd.DataFrame,
    client: OpenAI,  # OpenAI-compatible client for baseline/evaluation
    gen_model: str,
    eval_model: str,
    router: SkillsRouter,
    logger: RunLogger,
    baseline_loader: Optional[BaselineLoader] = None,
    split: str = "train",
    use_skills: bool = True,
    max_questions: Optional[int] = None,
    skill_set_name: Optional[str] = None,
    skill_method: Optional[str] = None,  # "progressive", "router", or None (auto-detect)
    anthropic_client: Optional[Anthropic] = None,  # For Claude progressive loading
    batch_eval: Optional[bool] = None,  # Use batch evaluation (default from BATCH_EVAL_ENABLED env)
    eval_batch_size: Optional[int] = None,  # Batch size for evaluation (default from EVAL_BATCH_SIZE env)
    router_type: str = "llm"  # "llm" (requires subfield) or "auto" (no subfield needed)
) -> RunLogger:
    """
    Run the system on a dataset and collect run logs.

    Uses FIXED BASELINE from pre-computed results (if provided).
    Only generates skill answers, compares against fixed baseline.

    Args:
        data: DataFrame with questions
        client: OpenAI client
        gen_model: Model name for generation
        eval_model: Model name for evaluation
        router: Skills router (uses rule-based routing)
        logger: Run logger
        baseline_loader: Pre-loaded baseline results (recommended!)
        split: Dataset split name
        use_skills: Whether to use skills (False = baseline only)
        max_questions: Limit number of questions (for testing)
        skill_set_name: Logical name for the skill set (e.g., "famma-non-arithmetic-v1").
                        Used as chosen_skill in run log entries. Defaults to router.skill_dir.name.
        batch_eval: Use batch evaluation for speed (default from BATCH_EVAL_ENABLED env var)
        eval_batch_size: Batch size for evaluation (default from EVAL_BATCH_SIZE env var, or 10)
        router_type: Type of router - "llm" (requires subfield) or "auto" (LLM infers subfield)

    Returns:
        RunLogger with all comparisons logged
    """
    # Check if batch evaluation is enabled
    if batch_eval is None:
        batch_eval = cfg('evaluation.batch_enabled') if cfg('evaluation.batch_enabled') is not None else os.getenv('BATCH_EVAL_ENABLED', 'false').lower() == 'true'

    # Delegate to batch version if enabled
    if batch_eval:
        return run_system_with_logging_batch(
            data=data,
            client=client,
            gen_model=gen_model,
            eval_model=eval_model,
            router=router,
            logger=logger,
            baseline_loader=baseline_loader,
            split=split,
            use_skills=use_skills,
            max_questions=max_questions,
            skill_set_name=skill_set_name,
            skill_method=skill_method,
            anthropic_client=anthropic_client,
            eval_batch_size=eval_batch_size,
            router_type=router_type
        )

    from tqdm import tqdm

    print(f"\n[Running {split} set] {len(data)} questions")

    # Determine which client to use for generation/evaluation
    # Use anthropic_client for Claude models, otherwise use OpenAI client
    gen_client = get_gen_client(gen_model, anthropic_client, client)
    eval_client = anthropic_client if anthropic_client and eval_model.lower().startswith('claude') else client

    # Determine client for MC selection (PoT mode only)
    selection_model = cfg('models.selection') or os.getenv("SELECTION_MODEL", "qwen-turbo")
    selection_client = anthropic_client if anthropic_client and selection_model.lower().startswith('claude') else client

    # Evaluation strategy: "hybrid" (rule-based MC + LLM open) or "llm_only"
    eval_strategy = cfg('evaluation.strategy') or os.getenv("EVAL_STRATEGY", "llm_only")
    print(f"  Evaluation strategy: {eval_strategy}")

    if baseline_loader:
        print(f"  Using FIXED baseline from pre-computed results")
    else:
        print(f"  ⚠ No baseline loader - will regenerate baseline (slower)")

    if max_questions:
        data = data.head(max_questions)
        print(f"  (Limited to {max_questions} questions for testing)")

    for idx, row in tqdm(data.iterrows(), total=len(data), desc=f"Processing {split}"):
        qid = row.get('question_id', f"{split}_{idx}")
        question = row['question']
        question_type = row.get('question_type', 'open-ended')
        context = row.get('context', '') if pd.notna(row.get('context')) else ''
        options = row.get('options', None) if pd.notna(row.get('options')) else None
        ground_truth = str(row.get('answers', row.get('ground_truth', '')))

        # Extract signature for skill routing
        # Modality: use image_type if present, otherwise 'text-only'
        image_type = row.get('image_type', None)
        modality = image_type if pd.notna(image_type) else 'text-only'

        signature = {
            'subfield': row.get('subfield', 'unknown'),
            'modality': modality
            # Note: error_type is NOT used anymore - skill type is determined by keyword matching
        }

        # (a) Get BASELINE from pre-computed results (FIXED baseline)
        if baseline_loader and qid in baseline_loader:
            # Use pre-computed baseline (no API call needed!)
            baseline = baseline_loader.get_baseline(qid)
            baseline_answer = baseline.baseline_answer
            baseline_explanation = baseline.baseline_explanation
            baseline_score = baseline.baseline_score
            baseline_code = None  # Pre-computed baselines don't have code
            baseline_execution_success = None
        else:
            # Fallback: Generate baseline (only if no pre-computed results)
            baseline_result = generate_answer(
                client=gen_client,
                model=gen_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                options=options,
                skill_content=None,  # No skill = baseline
                selection_client=selection_client
            )
            baseline_answer = baseline_result['answer']
            baseline_explanation = baseline_result.get('explanation', '')
            baseline_code = baseline_result.get('generated_code', None)  # PoT mode
            baseline_execution_success = baseline_result.get('code_execution_success', None)  # PoT mode

            # Evaluate baseline
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
                eval_strategy=eval_strategy
            )

        # (b) Generate WITH SKILL (if enabled)
        skill_answer = None
        skill_explanation = None
        skill_score = None
        skill_version = None
        chosen_skill = None
        specific_skill_file = None
        all_skill_files = None
        skill_metadata = None
        skill_code = None  # PoT mode
        skill_execution_success = None  # PoT mode

        if use_skills:
            # Route to skill files using LLM-based routing (2-level structure)
            chosen_skill = skill_set_name or router.skill_dir.name  # logical skill set name
            skill_version = "v1"

            # Determine skill loading method
            actual_method = determine_skill_method(gen_model, skill_method)

            if actual_method == "progressive" and anthropic_client:
                # Progressive loading: Claude tool_use for on-demand skill loading
                # Build FAMMA question block for consistent JSON response format
                question_block = build_famma_question_block(
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options
                )

                response_text, metadata = router.generate_progressive(
                    client=anthropic_client,
                    model=gen_model,
                    question=question,
                    context=context,
                    question_block=question_block,  # Pass FAMMA-formatted block
                    max_turns=5
                )

                skill_metadata = metadata
                all_skill_files = metadata.get('loaded_files', [])
                # Filter out SKILL.md for evidence attribution (always loaded in progressive mode)
                non_skill_md_files = [f for f in all_skill_files if f != 'SKILL.md']
                specific_skill_file = non_skill_md_files[0] if non_skill_md_files else None
                # Also update all_skill_files to exclude SKILL.md for evidence collection
                all_skill_files = non_skill_md_files if non_skill_md_files else all_skill_files

                # Parse response
                if response_text:
                    parsed, _ = parse_json_response(response_text)
                    print("parsed: ", parsed)
                    if parsed:
                        # Handle both dict and list responses
                        if isinstance(parsed, dict):
                            for qid_key, data in parsed.items():
                                if isinstance(data, dict):
                                    skill_answer = data.get('answer', '')
                                    skill_explanation = data.get('explanation', '')
                                    break
                                elif isinstance(data, str):
                                    skill_answer = data
                                    break
                        elif isinstance(parsed, list) and len(parsed) > 0:
                            # List of answers - take the first one
                            first_item = parsed[0]
                            if isinstance(first_item, dict):
                                skill_answer = first_item.get('answer', '')
                                skill_explanation = first_item.get('explanation', '')
                            elif isinstance(first_item, str):
                                skill_answer = first_item
                    else:
                        skill_explanation = response_text

                # Sample display (1 per 20 questions)
                if idx % int(cfg('training.sample_display_frequency') or int(os.getenv('SAMPLE_DISPLAY_FREQUENCY', '20'))) == 0:
                    tqdm.write(f"  [{qid}] Progressive: {', '.join(all_skill_files)}")

            else:
                # Router method: LLM selects files upfront
                if router_type == "auto":
                    # Auto router: LLM infers subfield from question (no subfield param needed)
                    selected_files = router.get_auto_selected_files(
                        question=question,
                        context=context
                    )
                else:
                    # LLM router: requires subfield parameter
                    selected_files = router.get_llm_selected_files(
                        question=question,
                        context=context,
                        subfield=signature.get('subfield', '')
                    )

                if selected_files:
                    # Track ALL selected files for evidence attribution
                    all_skill_files = [str(f.relative_to(router.skill_dir)) for f in selected_files]
                    specific_skill_file = all_skill_files[0]  # Primary file (backward compat)
                    # Build concatenated content from all selected files
                    skill_content = router._build_content(selected_files)

                    # Sample skill selection display (1 per 20 questions for debugging)
                    if idx % int(cfg('training.sample_display_frequency') or int(os.getenv('SAMPLE_DISPLAY_FREQUENCY', '20'))) == 0:
                        tqdm.write(f"  [{qid}] Router: {', '.join(all_skill_files)}")
                else:
                    # LLM selected no files - generate without skill content
                    all_skill_files = []
                    specific_skill_file = None
                    skill_content = None
                    tqdm.write(f"  [{qid}] Router: no files selected")

                # Generate with skill (or without if no files selected)
                skill_result = generate_answer(
                    client=gen_client,
                    model=gen_model,
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options,
                    skill_content=skill_content,
                    selection_client=selection_client
                )
                skill_answer = skill_result['answer']
                skill_explanation = skill_result.get('explanation', '')
                skill_code = skill_result.get('generated_code', None)  # PoT mode
                skill_execution_success = skill_result.get('code_execution_success', None)  # PoT mode

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
                    generated_explanation=skill_explanation,
                    ground_truth=ground_truth,
                    eval_strategy=eval_strategy
                )
            else:
                # No answer generated (e.g., code execution failed) = wrong
                skill_score = 0.0

        # (c) Log the run
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
            skill_version=skill_version,
            specific_skill_file=specific_skill_file,
            all_skill_files=all_skill_files,
            skill_answer=skill_answer,
            skill_score=skill_score,
            skill_explanation=skill_explanation,
            skill_metadata=skill_metadata,  # Progressive loading metadata
            signature=signature,
            split=split,
            options=options,
            baseline_code=baseline_code,  # PoT mode
            skill_code=skill_code,  # PoT mode
            baseline_execution_success=baseline_execution_success,  # PoT mode
            skill_execution_success=skill_execution_success  # PoT mode
        )

        # Rate limiting (only needed for skill generation now)
        time.sleep(0.3)

    # Return the log entries list (not the logger object)
    # Return the appropriate log based on split (both "val" and "eval" use val_log)
    if split in ("val", "eval"):
        return logger.val_log
    else:
        return logger.train_log


def run_system_with_logging_batch(
    data: pd.DataFrame,
    client: OpenAI,  # OpenAI-compatible client for baseline/evaluation
    gen_model: str,
    eval_model: str,
    router: SkillsRouter,
    logger: RunLogger,
    baseline_loader: Optional[BaselineLoader] = None,
    split: str = "train",
    use_skills: bool = True,
    max_questions: Optional[int] = None,
    skill_set_name: Optional[str] = None,
    skill_method: Optional[str] = None,
    anthropic_client: Optional[Anthropic] = None,
    eval_batch_size: int = None,
    router_type: str = "llm"  # "llm" (requires subfield) or "auto" (no subfield needed)
) -> List:
    """
    Batch-optimized version of run_system_with_logging.

    Generates answers sequentially, then evaluates in batches for speed.

    Args:
        ... (same as run_system_with_logging)
        eval_batch_size: Batch size for evaluation (default from EVAL_BATCH_SIZE env var, or 10)
        router_type: Type of router - "llm" (requires subfield) or "auto" (LLM infers subfield)

    Returns:
        List of RunLogEntry
    """
    from tqdm import tqdm

    # Get batch size from config or env
    if eval_batch_size is None:
        eval_batch_size = cfg('evaluation.batch_size') or int(os.getenv('EVAL_BATCH_SIZE', '10'))

    print(f"\n[Running {split} set - BATCH MODE] {len(data)} questions")
    print(f"  Evaluation batch size: {eval_batch_size}")

    # Determine which client to use for generation
    gen_client = get_gen_client(gen_model, anthropic_client, client)
    eval_client = anthropic_client if anthropic_client and eval_model.lower().startswith('claude') else client

    # Determine client for MC selection (PoT mode only)
    selection_model = cfg('models.selection') or os.getenv("SELECTION_MODEL", "qwen-turbo")
    selection_client = anthropic_client if anthropic_client and selection_model.lower().startswith('claude') else client

    # Get evaluation strategy for fallback sequential evaluation
    eval_strategy = cfg('evaluation.strategy') or os.getenv("EVAL_STRATEGY", "llm_only")

    if baseline_loader:
        print(f"  Using FIXED baseline from pre-computed results")
    else:
        print(f"  ⚠ No baseline loader - will regenerate baseline (slower)")

    if max_questions:
        data = data.head(max_questions)
        print(f"  (Limited to {max_questions} questions for testing)")

    # ===== PHASE 1: Generate all answers sequentially =====
    print(f"\n  [Phase 1] Generating answers...")
    generated_items = []  # Store all generated data for later evaluation

    for idx, row in tqdm(data.iterrows(), total=len(data), desc=f"Generating {split}"):
        qid = row.get('question_id', f"{split}_{idx}")
        question = row['question']
        question_type = row.get('question_type', 'open-ended')
        context = row.get('context', '') if pd.notna(row.get('context')) else ''
        options = row.get('options', None) if pd.notna(row.get('options')) else None
        ground_truth = str(row.get('answers', row.get('ground_truth', '')))

        # Extract signature for skill routing
        image_type = row.get('image_type', None)
        modality = image_type if pd.notna(image_type) else 'text-only'
        signature = {
            'subfield': row.get('subfield', 'unknown'),
            'modality': modality
        }

        # Get BASELINE from pre-computed results (FIXED baseline)
        baseline_needs_eval = False
        if baseline_loader and qid in baseline_loader:
            baseline = baseline_loader.get_baseline(qid)
            baseline_answer = baseline.baseline_answer
            baseline_explanation = baseline.baseline_explanation
            baseline_score = baseline.baseline_score
            baseline_code = None  # Pre-computed baselines don't have code
            baseline_execution_success = None
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
                selection_client=selection_client
            )
            baseline_answer = baseline_result['answer']
            baseline_explanation = baseline_result.get('explanation', '')
            baseline_code = baseline_result.get('generated_code', None)  # PoT mode
            baseline_execution_success = baseline_result.get('code_execution_success', None)  # PoT mode
            baseline_score = None  # Will be evaluated in batch
            baseline_needs_eval = True

        # Generate WITH SKILL (if enabled)
        skill_answer = None
        skill_explanation = None
        skill_version = None
        chosen_skill = None
        specific_skill_file = None
        all_skill_files = None
        skill_metadata = None
        skill_code = None  # PoT mode
        skill_execution_success = None  # PoT mode

        if use_skills:
            chosen_skill = skill_set_name or router.skill_dir.name
            skill_version = "v1"
            actual_method = determine_skill_method(gen_model, skill_method)

            if actual_method == "progressive" and anthropic_client:
                question_block = build_famma_question_block(
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options
                )

                response_text, metadata = router.generate_progressive(
                    client=anthropic_client,
                    model=gen_model,
                    question=question,
                    context=context,
                    question_block=question_block,
                    max_turns=5
                )

                skill_metadata = metadata
                all_skill_files = metadata.get('loaded_files', [])
                non_skill_md_files = [f for f in all_skill_files if f != 'SKILL.md']
                specific_skill_file = non_skill_md_files[0] if non_skill_md_files else None
                all_skill_files = non_skill_md_files if non_skill_md_files else all_skill_files

                if response_text:
                    parsed, _ = parse_json_response(response_text)
                    if parsed:
                        if isinstance(parsed, dict):
                            for qid_key, data_item in parsed.items():
                                if isinstance(data_item, dict):
                                    skill_answer = data_item.get('answer', '')
                                    skill_explanation = data_item.get('explanation', '')
                                    break
                                elif isinstance(data_item, str):
                                    skill_answer = data_item
                                    break
                        elif isinstance(parsed, list) and len(parsed) > 0:
                            first_item = parsed[0]
                            if isinstance(first_item, dict):
                                skill_answer = first_item.get('answer', '')
                                skill_explanation = first_item.get('explanation', '')
                            elif isinstance(first_item, str):
                                skill_answer = first_item
                    else:
                        skill_explanation = response_text

                if idx % int(cfg('training.sample_display_frequency') or int(os.getenv('SAMPLE_DISPLAY_FREQUENCY', '20'))) == 0:
                    tqdm.write(f"  [{qid}] Progressive: {', '.join(all_skill_files) if all_skill_files else 'None'}")
            else:
                # Router method: LLM selects files upfront
                if router_type == "auto":
                    # Auto router: LLM infers subfield from question (no subfield param needed)
                    selected_files = router.get_auto_selected_files(
                        question=question,
                        context=context
                    )
                else:
                    # LLM router: requires subfield parameter
                    selected_files = router.get_llm_selected_files(
                        question=question,
                        context=context,
                        subfield=signature.get('subfield', '')
                    )

                if selected_files:
                    all_skill_files = [str(f.relative_to(router.skill_dir)) for f in selected_files]
                    specific_skill_file = all_skill_files[0]
                    skill_content = router._build_content(selected_files)

                    if idx % int(cfg('training.sample_display_frequency') or int(os.getenv('SAMPLE_DISPLAY_FREQUENCY', '20'))) == 0:
                        tqdm.write(f"  [{qid}] Router: {', '.join(all_skill_files)}")
                else:
                    # LLM selected no files - generate without skill content
                    all_skill_files = []
                    specific_skill_file = None
                    skill_content = None
                    tqdm.write(f"  [{qid}] Router: no files selected")

                # Generate with skill (or without if no files selected)
                skill_result = generate_answer(
                    client=gen_client,
                    model=gen_model,
                    question_id=qid,
                    question=question,
                    question_type=question_type,
                    context=context,
                    options=options,
                    skill_content=skill_content,
                    selection_client=selection_client
                )
                skill_answer = skill_result['answer']
                skill_explanation = skill_result.get('explanation', '')
                skill_code = skill_result.get('generated_code', None)  # PoT mode
                skill_execution_success = skill_result.get('code_execution_success', None)  # PoT mode

        # Store all data for batch evaluation
        generated_items.append({
            'qid': qid,
            'question': question,
            'question_type': question_type,
            'context': context,
            'options': options,
            'ground_truth': ground_truth,
            'signature': signature,
            'baseline_answer': baseline_answer,
            'baseline_explanation': baseline_explanation,
            'baseline_score': baseline_score,
            'baseline_needs_eval': baseline_needs_eval,
            'skill_answer': skill_answer,
            'skill_explanation': skill_explanation or '',
            'chosen_skill': chosen_skill,
            'skill_version': skill_version,
            'specific_skill_file': specific_skill_file,
            'all_skill_files': all_skill_files,
            'skill_metadata': skill_metadata,
            'baseline_code': baseline_code,  # PoT mode
            'skill_code': skill_code,  # PoT mode
            'baseline_execution_success': baseline_execution_success,  # PoT mode
            'skill_execution_success': skill_execution_success  # PoT mode
        })

        time.sleep(0.1)  # Reduced rate limiting for generation phase

    # ===== PHASE 2: Batch evaluate all answers =====
    print(f"\n  [Phase 2] Batch evaluating {len(generated_items)} answers...")

    # Prepare baseline evaluations (only for items that need it)
    baseline_eval_items = []
    baseline_eval_indices = []
    for i, item in enumerate(generated_items):
        if item['baseline_needs_eval']:
            baseline_eval_items.append({
                'question_id': item['qid'],
                'question': item['question'],
                'question_type': item['question_type'],
                'context': item['context'],
                'generated_answer': item['baseline_answer'],
                'generated_explanation': item['baseline_explanation'],
                'ground_truth': item['ground_truth']
            })
            baseline_eval_indices.append(i)

    # Prepare skill evaluations
    skill_eval_items = []
    skill_eval_indices = []
    for i, item in enumerate(generated_items):
        if item['skill_answer']:
            skill_eval_items.append({
                'question_id': item['qid'],
                'question': item['question'],
                'question_type': item['question_type'],
                'context': item['context'],
                'generated_answer': item['skill_answer'],
                'generated_explanation': item['skill_explanation'],
                'ground_truth': item['ground_truth']
            })
            skill_eval_indices.append(i)
        else:
            # No answer generated (e.g., code execution failed) = wrong
            item['skill_score'] = 0.0

    # Batch evaluate baselines
    if baseline_eval_items:
        print(f"    Evaluating {len(baseline_eval_items)} baselines...")
        baseline_scores = evaluate_answers_batch(baseline_eval_items, eval_model, eval_batch_size)
        if baseline_scores is None:
            # Fallback to sequential
            print(f"    Falling back to sequential evaluation...")
            baseline_scores = []
            for item in tqdm(baseline_eval_items, desc="Eval baselines"):
                score = evaluate_answer(
                    client=eval_client,
                    model=eval_model,
                    question_id=item['question_id'],
                    question=item['question'],
                    question_type=item['question_type'],
                    context=item['context'],
                    generated_answer=item['generated_answer'],
                    generated_explanation=item['generated_explanation'],
                    ground_truth=item['ground_truth'],
                    eval_strategy=eval_strategy
                )
                baseline_scores.append(score)

        # Update generated_items with baseline scores
        for idx, score in zip(baseline_eval_indices, baseline_scores):
            generated_items[idx]['baseline_score'] = score

    # Batch evaluate skills
    if skill_eval_items:
        print(f"    Evaluating {len(skill_eval_items)} skill answers...")
        skill_scores = evaluate_answers_batch(skill_eval_items, eval_model, eval_batch_size)
        if skill_scores is None:
            # Fallback to sequential
            print(f"    Falling back to sequential evaluation...")
            skill_scores = []
            for item in tqdm(skill_eval_items, desc="Eval skills"):
                score = evaluate_answer(
                    client=eval_client,
                    model=eval_model,
                    question_id=item['question_id'],
                    question=item['question'],
                    question_type=item['question_type'],
                    context=item['context'],
                    generated_answer=item['generated_answer'],
                    generated_explanation=item['generated_explanation'],
                    ground_truth=item['ground_truth'],
                    eval_strategy=eval_strategy
                )
                skill_scores.append(score)

        # Update generated_items with skill scores
        for idx, score in zip(skill_eval_indices, skill_scores):
            generated_items[idx]['skill_score'] = score

    # ===== PHASE 3: Log all results =====
    print(f"\n  [Phase 3] Logging {len(generated_items)} results...")

    for item in generated_items:
        logger.log_run(
            qid=item['qid'],
            question=item['question'],
            context=item['context'],
            ground_truth=item['ground_truth'],
            baseline_answer=item['baseline_answer'],
            baseline_score=item['baseline_score'],
            baseline_explanation=item['baseline_explanation'],
            candidates=[item['chosen_skill']] if item['chosen_skill'] else [],
            chosen_skill=item['chosen_skill'],
            skill_version=item['skill_version'],
            specific_skill_file=item['specific_skill_file'],
            all_skill_files=item['all_skill_files'],
            skill_answer=item['skill_answer'],
            skill_score=item.get('skill_score'),
            skill_explanation=item['skill_explanation'],
            skill_metadata=item['skill_metadata'],
            signature=item['signature'],
            split=split,
            options=item['options'],
            baseline_code=item.get('baseline_code'),  # PoT mode
            skill_code=item.get('skill_code'),  # PoT mode
            baseline_execution_success=item.get('baseline_execution_success'),  # PoT mode
            skill_execution_success=item.get('skill_execution_success')  # PoT mode
        )

    print(f"  ✓ Batch processing complete")
    # Return the appropriate log based on split (both "val" and "eval" use val_log)
    if split in ("val", "eval"):
        return logger.val_log
    else:
        return logger.train_log


def example_full_training_workflow(
    max_questions: int = None,
    max_val_questions: int = None,
    baseline_dir: str = None,
    train_baseline_dir: str = None,
    val_baseline_dir: str = None,
    splits: list = None,
    subfields: list = None
):
    """
    Complete example showing the full training workflow.

    Uses FIXED BASELINE from pre-computed results.
    Only generates skill answers, compares against fixed baseline.

    Args:
        max_questions: Max training questions (for testing)
        max_val_questions: Max validation questions (for testing/unit tests)
        baseline_dir: Default baseline directory (fallback if split-specific not set)
        train_baseline_dir: Separate baseline dir for train split (optional)
        val_baseline_dir: Separate baseline dir for val split (optional)
        splits: Which splits to run, e.g. ["train", "val"], ["train", "eval"], or ["train"]
        subfields: Filter by subfields, e.g. ["portfolio management", "derivatives"]
    """
    # Apply defaults from config or environment
    if max_questions is None:
        config_val = cfg('training.max_questions')
        if config_val is not None:
            max_questions = config_val
        else:
            env_val = os.getenv('TRAINING_MAX_QUESTIONS', '')
            if env_val and env_val.lower() != 'none':
                max_questions = int(env_val)
            else:
                max_questions = None

    if max_val_questions is None:
        config_val = cfg('training.max_val_questions')
        if config_val is not None:
            max_val_questions = config_val
        else:
            env_val = os.getenv('TRAINING_MAX_VAL_QUESTIONS', '')
            if env_val and env_val.lower() != 'none':
                max_val_questions = int(env_val)
            else:
                max_val_questions = None
    if baseline_dir is None:
        baseline_dir = cfg('paths.baseline_dir') or os.getenv('BASELINE_DIR', 'results/qwen_flash_non_arithmetic')
    if train_baseline_dir is None:
        train_baseline_dir = cfg('paths.train_baseline_dir')  # None means use baseline_dir
    if val_baseline_dir is None:
        val_baseline_dir = cfg('paths.val_baseline_dir')  # None means use baseline_dir
    if splits is None:
        splits = cfg('training.splits') or ["train", "val"]
    if subfields is None:
        subfields = cfg('training.subfields')  # Optional: filter by subfield list
    print("="*80)
    print(f"Full Training Workflow Example")
    print("="*80)
    print("\nUsing OFFICIAL FAMMA prompts:")
    print("  - Baseline: FIXED from pre-computed results (no regeneration)")
    print("  - Generation: QuestionPrompt from run_baseline_nonarithmetic.py")
    print("  - Evaluation: JudgePrompt from evaluate_baseline_nonarithmetic.py")
    print("  - Skills: Added as [Domain Knowledge] prefix when enabled")

    # Setup
    client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider = setup_environment()

    # Determine client for MC selection (PoT mode only)
    selection_model = cfg('models.selection') or os.getenv("SELECTION_MODEL", "qwen-turbo")
    selection_client = anthropic_client if anthropic_client and selection_model.lower().startswith('claude') else client

    # Evaluation strategy: "hybrid" (rule-based MC + LLM open) or "llm_only"
    eval_strategy = cfg('evaluation.strategy') or os.getenv("EVAL_STRATEGY", "llm_only")

    # Load FIXED baseline from pre-computed results
    print("\n[0] Loading FIXED baseline results...")
    baseline_loader = None

    # Determine baseline directories for each split
    train_dir = train_baseline_dir or baseline_dir
    val_dir = val_baseline_dir or baseline_dir

    # Check if we can use a single loader (same dir) or need to merge
    if train_dir == val_dir:
        # Same directory for all splits - load normally
        baseline_path = project_root / train_dir
        if baseline_path.exists():
            baseline_loader = load_baseline(str(baseline_path), splits=splits)
            stats = baseline_loader.get_statistics()
            print(f"  ✓ Baseline loaded from {baseline_path}")
            print(f"  ✓ Baseline accuracy: {stats['accuracy']:.2%} ({stats['correct']}/{stats['total']})")
            print(f"  ✓ Baseline failures (Q+ candidates): {len(baseline_loader.get_failures())}")
        else:
            print(f"  ⚠ Baseline not found at {baseline_path}")
            print(f"  Will regenerate baseline (slower, uses more API calls)")
    else:
        # Different directories for train/val - load each separately and merge
        baseline_loader = BaselineLoader(str(project_root / train_dir))  # Create empty loader
        baseline_loader.baselines = {}  # Clear any defaults

        if "train" in splits:
            train_path = project_root / train_dir
            if train_path.exists():
                temp_loader = load_baseline(str(train_path), splits=["train"])
                baseline_loader.baselines.update(temp_loader.baselines)
                print(f"  ✓ Train baseline loaded from {train_path}")
            else:
                print(f"  ⚠ Train baseline not found at {train_path}")

        # Support both "val" and "eval" as validation split names
        val_split_name = "eval" if "eval" in splits else "val" if "val" in splits else None
        if val_split_name:
            val_path = project_root / val_dir
            if val_path.exists():
                temp_loader = load_baseline(str(val_path), splits=[val_split_name])
                baseline_loader.baselines.update(temp_loader.baselines)
                print(f"  ✓ {val_split_name.capitalize()} baseline loaded from {val_path}")
            else:
                print(f"  ⚠ {val_split_name.capitalize()} baseline not found at {val_path}")

        if baseline_loader.baselines:
            stats = baseline_loader.get_statistics()
            print(f"  ✓ Combined baseline accuracy: {stats['accuracy']:.2%} ({stats['correct']}/{stats['total']})")
        else:
            baseline_loader = None
            print(f"  ⚠ No baselines loaded. Will regenerate baseline.")

    # Initialize components
    print("\n[1] Initializing components...")
    skills_dir = cfg('skills.dir') or os.getenv('SKILLS_DIR', str(project_root / ".claude/skills/generated-from-failures-v1"))
    router = SkillsRouter(skills_dir)

    print(f"  ✓ Loaded {len(router.all_files)} skill files from {router.skill_dir.name}")

    # Load datasets
    print("\n[1] Loading datasets...")
    train_csv = project_root / (cfg('paths.train_csv') or os.getenv('TRAIN_CSV', 'data/famma_non_arithmetic_train_split.csv'))
    val_csv = project_root / (cfg('paths.val_csv') or os.getenv('VAL_CSV', 'data/famma_non_arithmetic_val_split.csv'))

    if not train_csv.exists() or not val_csv.exists():
        print(f"  ⚠ CSV files not found. Please ensure:")
        print(f"    - {train_csv}")
        print(f"    - {val_csv}")
        print(f"\n  Creating sample data for demonstration...")
        # Create minimal sample data
        sample_data = pd.DataFrame([
            {
                'question_id': 'demo_1',
                'question': 'What is the P/E ratio if earnings per share is $5 and stock price is $100?',
                'question_type': 'open-ended',
                'context': 'Company XYZ financial data.',
                'answers': '20',
                'is_arithmetic': 0,
                'subfield': 'equity valuation',
                'error_type': 3
            },
            {
                'question_id': 'demo_2',
                'question': 'Which metric measures a company\'s ability to pay short-term obligations?',
                'question_type': 'multiple-choice',
                'options': 'A. P/E ratio B. Current ratio C. Debt ratio D. ROE',
                'context': 'Financial ratios analysis.',
                'answers': 'B',
                'is_arithmetic': 0,
                'subfield': 'corporate finance',
                'error_type': 3
            }
        ])
        train_data = sample_data.copy()
        val_data = sample_data.copy()
    else:
        train_data = load_dataset(train_csv)
        val_data = load_dataset(val_csv)

    # Optional: filter by subfields (for focused testing on specific domains)
    if subfields:
        train_before = len(train_data)
        val_before = len(val_data)
        # Filter by subfield column (case-insensitive matching)
        subfields_lower = [s.lower() for s in subfields]
        if 'subfield' in train_data.columns:
            train_data = train_data[train_data['subfield'].str.lower().isin(subfields_lower)]
            val_data = val_data[val_data['subfield'].str.lower().isin(subfields_lower)]
            print(f"  ✓ Filtered by subfields: {subfields}")
            print(f"    Train: {train_before} → {len(train_data)}, Val: {val_before} → {len(val_data)}")
        else:
            print(f"  ⚠ 'subfield' column not found in data, skipping subfield filter")

    # Optional: filter TRAIN and/or VALIDATION data by question IDs (for focused testing)
    # QIDs JSON is typically generated from eval comparisons or analysis scripts
    # Backwards compatible:
    #   - training.qids_file + training.qids_category  → filter VAL
    # New (optional):
    #   - training.train_qids_file + training.train_qids_category → filter TRAIN with its own file/category
    #   - training.val_qids_file   + training.qids_category       → override VAL file if needed
    base_qids_file = cfg('training.qids_file')
    val_qids_file = cfg('training.val_qids_file') or base_qids_file
    train_qids_file = cfg('training.train_qids_file') or base_qids_file
    qids_category = cfg('training.qids_category') or 'test_set'          # default category for VAL
    train_qids_category = cfg('training.train_qids_category')            # optional: separate category for TRAIN

    # Filter VAL
    if val_qids_file:
        val_qids_path = project_root / val_qids_file
        if val_qids_path.exists():
            with open(val_qids_path, 'r', encoding="utf-8") as f:
                val_qids_data = json.load(f)
            val_filter_qids = set(val_qids_data.get(qids_category, []))
            if val_filter_qids:
                val_before = len(val_data)
                val_data = val_data[val_data['question_id'].isin(val_filter_qids)]
                print(f"  ✓ Filtered VAL by QIDs from {val_qids_file} (category: {qids_category})")
                print(f"    Val: {val_before} → {len(val_data)} (Train size: {len(train_data)})")
            else:
                print(f"  ⚠ No QIDs found in category '{qids_category}' of {val_qids_file} for VAL")
        else:
            print(f"  ⚠ QIDs file not found for VAL: {val_qids_path}")

    # Filter TRAIN (only if category is provided)
    if train_qids_category and train_qids_file:
        train_qids_path = project_root / train_qids_file
        if train_qids_path.exists():
            with open(train_qids_path, 'r', encoding="utf-8") as f:
                train_qids_data = json.load(f)
            train_filter_qids = set(train_qids_data.get(train_qids_category, []))
            if train_filter_qids:
                train_before = len(train_data)
                train_data = train_data[train_data['question_id'].isin(train_filter_qids)]
                print(f"  ✓ Filtered TRAIN by QIDs from {train_qids_file} (category: {train_qids_category})")
                print(f"    Train: {train_before} → {len(train_data)} (Val size: {len(val_data)})")
            else:
                print(f"  ⚠ No QIDs found in category '{train_qids_category}' of {train_qids_file} for TRAIN")
        else:
            print(f"  ⚠ QIDs file not found for TRAIN: {train_qids_path}")

    # Define system runner (uses FIXED baseline)
    # Capture the logical skill set name for consistent run log entries
    _skill_set_name = Path(skills_dir).name  # e.g., "famma-non-arithmetic-v1"

    # Check batch evaluation settings
    _batch_eval = cfg('evaluation.batch_enabled') if cfg('evaluation.batch_enabled') is not None else os.getenv('BATCH_EVAL_ENABLED', 'false').lower() == 'true'
    _eval_batch_size = cfg('evaluation.batch_size') or int(os.getenv('EVAL_BATCH_SIZE', '10'))
    if _batch_eval:
        print(f"  ✓ Batch evaluation enabled (batch_size={_eval_batch_size})")

    def run_system_fn(data: pd.DataFrame, router: SkillsRouter, split: str = "train") -> RunLogger:
        """System runner for the training loop. Uses FIXED baseline."""
        logger = RunLogger()
        return run_system_with_logging(
            data=data,
            client=client,
            gen_model=gen_model,
            eval_model=eval_model,
            router=router,
            logger=logger,
            baseline_loader=baseline_loader,  # FIXED baseline - no regeneration!
            split=split,  # Use the provided split parameter
            use_skills=True,
            max_questions=None,  # Data already sliced before train(), don't limit again
            skill_set_name=_skill_set_name,  # Use logical name, not "working_skills"
            skill_method=skills_loading_mode,  # Use user-configured loading mode
            anthropic_client=anthropic_client,  # For Claude progressive loading
            batch_eval=_batch_eval,  # Use batch evaluation if enabled
            eval_batch_size=_eval_batch_size,  # Batch size for evaluation
            router_type=router_type  # "llm" or "auto" router type
        )

    # Initialize trainer
    checkpoint_dir = cfg('paths.checkpoint_dir') or os.getenv('CHECKPOINT_DIR', str(project_root / "skill_learning/checkpoints_api"))

    # Configuration from config or .env (with defaults)
    # M controls how many skills to update per epoch
    # M=1: Update only the worst-performing skill (recommended for careful refinement)
    # M=5: Update top-5 worst skills (faster iteration, but riskier)
    num_skills_to_update = cfg('training.M') or int(os.getenv('M', '5'))
    lambda_regress = cfg('training.lambda_regress') or float(os.getenv('LAMBDA_REGRESS', '2.0'))
    patience = cfg('training.patience') or int(os.getenv('PATIENCE', '2'))

    # Evidence collection parameters
    p_min = cfg('evidence.p_min') or int(os.getenv('P_MIN', '5'))
    r_min = cfg('evidence.r_min') or int(os.getenv('R_MIN', '2'))
    default_evidence_p = cfg('evidence.evidence_p') or int(os.getenv('EVIDENCE_P', '8'))
    default_evidence_n = cfg('evidence.evidence_n') or int(os.getenv('EVIDENCE_N', '8'))

    # Per-skill P/N configuration (optional)
    skill_p_n_config = {}

    # Residual evidence collection parameters
    enable_residual_analysis = cfg('residual.enable_analysis') if cfg('residual.enable_analysis') is not None else os.getenv('ENABLE_RESIDUAL_ANALYSIS', 'true').lower() == 'true'
    enable_probe_alternatives = cfg('residual.enable_probe_alternatives') if cfg('residual.enable_probe_alternatives') is not None else os.getenv('ENABLE_PROBE_ALTERNATIVES', 'true').lower() == 'true'
    max_residual_cases = cfg('residual.max_cases') or int(os.getenv('MAX_RESIDUAL_CASES', '20'))  # Max unsolved cases to probe
    max_probes_per_case = cfg('residual.max_probes_per_case') or int(os.getenv('MAX_PROBES_PER_CASE', '3'))  # Max alternative skills to try per case
    enable_residual_diagnosis = cfg('residual.enable_diagnosis') if cfg('residual.enable_diagnosis') is not None else os.getenv('ENABLE_RESIDUAL_DIAGNOSIS', 'true').lower() == 'true'

    # Determine skills loading mode based on model and client availability
    # Progressive mode: Claude + Anthropic client available
    # Router mode: Non-Claude model or no Anthropic client
    skills_loading_mode = cfg('skills.loading_mode') or os.getenv('SKILLS_LOADING_MODE', 'auto')
    if skills_loading_mode == 'auto':
        if anthropic_client and gen_model.lower().startswith('claude'):
            skills_loading_mode = 'progressive'
        else:
            skills_loading_mode = 'router'

    # Router type: "llm" (requires subfield) or "auto" (LLM infers subfield from question)
    router_type = cfg('skills.router_type') or os.getenv('ROUTER_TYPE', 'llm')

    trainer = SkillTrainer(
        skills_dir=skills_dir,
        checkpoint_dir=checkpoint_dir,
        lambda_regress=lambda_regress,
        M=num_skills_to_update,  # Number of files to refine per epoch
        patience=patience,
        p_min=p_min,
        r_min=r_min,
        default_P=default_evidence_p,
        default_N=default_evidence_n,
        skill_P_N_config=skill_p_n_config,
        # Residual evidence settings
        enable_residual_analysis=enable_residual_analysis,
        enable_probe_alternatives=enable_probe_alternatives,
        skills_loading_mode=skills_loading_mode,
        max_residual_cases=max_residual_cases,
        max_probes_per_case=max_probes_per_case,
        enable_residual_diagnosis=enable_residual_diagnosis,
        # Progressive mode support for sandbox verification
        anthropic_client=anthropic_client,
        gen_model=gen_model
    )

    print(f"  ✓ Trainer configured:")
    print(f"    - Refinement model: {cfg('models.refine') or os.getenv('REFINE_MODEL', 'claude-sonnet-4-5-20250929')}")
    print(f"    - Refinement temperature: {cfg('model_params.refine_temperature') or os.getenv('REFINE_TEMPERATURE', '0.3')}")
    print(f"    - Skills to update per epoch (M): {num_skills_to_update}")
    print(f"    - Regression penalty (λ): {trainer.lambda_regress}")
    print(f"    - Early stopping patience: {trainer.patience}")
    print(f"    - Evidence collection:")
    print(f"      - Min Q+ for refinement (p_min): {p_min}")
    print(f"      - Min Q- for refinement (r_min): {r_min}")
    print(f"      - Default max positives PER FILE (P): {default_evidence_p}")
    print(f"      - Default max negatives PER FILE (N): {default_evidence_n}")
    print(f"      - Note: P/N apply to each sub-skill file separately")
    if skill_p_n_config:
        print(f"      - Per-skill overrides:")
        for skill_name, config in skill_p_n_config.items():
            print(f"        - {skill_name}: P={config.get('P', default_evidence_p)}, N={config.get('N', default_evidence_n)}")
    print(f"    - Residual evidence:")
    print(f"      - Enabled: {enable_residual_analysis}")
    print(f"      - Probe alternatives: {enable_probe_alternatives}")
    print(f"      - Skills loading mode: {skills_loading_mode}")
    print(f"      - Router type: {router_type}")
    if enable_residual_analysis:
        if skills_loading_mode == 'router' and enable_probe_alternatives:
            print(f"      - Max unsolved cases to probe: {max_residual_cases}")
            print(f"      - Max alternatives per case: {max_probes_per_case}")
        elif not enable_probe_alternatives:
            print(f"      - Probing: disabled (enable_probe_alternatives=false)")
        else:
            print(f"      - Probing: skipped (progressive mode - model had agency to load any file)")
        print(f"      - LLM diagnosis: {enable_residual_diagnosis}")

    # Run training
    print(f"\n[3] Starting training loop...")

    # Max epochs from config or .env (default: 2)
    max_epochs = cfg('training.max_epochs') or int(os.getenv('MAX_EPOCHS', '2'))
    print(f"    - Max epochs: {max_epochs}")

    # Prepare train and val data
    train_subset = train_data.head(max_questions) if max_questions else train_data
    val_subset = val_data.head(max_val_questions) if max_val_questions else val_data

    # Print dataset info
    train_info = f"{len(train_subset)} train" + (f" (limited from {len(train_data)})" if max_questions else "")
    val_info = f"{len(val_subset)} val" + (f" (limited from {len(val_data)})" if max_val_questions else "")
    print(f"\n  Using datasets: {train_info}, {val_info} questions")

    # Create gen_func and eval_func for residual evidence probing
    def residual_gen_func(question: str, context: str, options: Optional[str], skill_content: str) -> Tuple[str, str]:
        """
        Generate answer with a skill for residual probing.

        Args:
            question: Question text
            context: Question context
            options: MC options (if applicable)
            skill_content: Skill content to use

        Returns:
            Tuple of (answer, explanation)
        """
        # Determine which client to use based on generation model
        gen_client = get_gen_client(gen_model, anthropic_client, client)

        # Use a placeholder question_id for probing
        result = generate_answer(
            client=gen_client,
            model=gen_model,
            question_id="probe_q",
            question=question,
            question_type="multiple-choice" if options else "open-ended",
            context=context,
            options=options,
            skill_content=skill_content,
            selection_client=selection_client
        )
        return result.get("answer", ""), result.get("explanation", "")

    def residual_eval_func(question: str, context: str, answer: str, explanation: str, ground_truth: str, question_type: str = "multiple-choice") -> float:
        """
        Evaluate answer for residual probing.

        Args:
            question: Question text
            context: Question context
            answer: Generated answer
            explanation: Generated explanation
            ground_truth: Ground truth answer
            question_type: Question type (default: multiple-choice)

        Returns:
            Score (1.0 for correct, 0.0 for incorrect)
        """
        return evaluate_answer(
            client=client,
            model=eval_model,
            question_id="probe_q",
            question=question,
            question_type=question_type,
            context=context,
            generated_answer=answer,
            generated_explanation=explanation,
            ground_truth=ground_truth,
            eval_strategy=eval_strategy
        )

    history = trainer.train(
        train_data=train_subset,
        val_data=val_subset,
        max_epochs=max_epochs,
        run_system_fn=run_system_fn,
        gen_func=residual_gen_func,  # For residual evidence probing
        eval_func=residual_eval_func  # For residual evidence evaluation
    )

    # Print results
    print("\n" + "="*80)
    print("Training Complete!")
    print("="*80)
    print(f"Best epoch: {history['best_epoch']}")
    print(f"Best val accuracy: {history['best_val_acc']:.2%}")
    print(f"\nCheckpoint saved to: {checkpoint_dir}/epoch_{history['best_epoch']}/")


def example_simple_comparison(
    max_questions: int = None,
    baseline_dir: str = None
):
    """
    Simple example: Compare baseline vs skill on a few questions.

    Uses FIXED baseline from pre-computed results.
    """
    # Apply defaults from config or environment
    if max_questions is None:
        max_questions = cfg('training.simple_example_max_questions') or int(os.getenv('SIMPLE_EXAMPLE_MAX_QUESTIONS', '5'))
    if baseline_dir is None:
        baseline_dir = cfg('paths.baseline_dir') or os.getenv('BASELINE_DIR', 'results/qwen_flash_non_arithmetic')

    print("="*80)
    print("Simple Baseline vs Skill Comparison")
    print("="*80)
    print("\nUsing FIXED baseline from pre-computed results.")

    # Setup
    client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider = setup_environment()

    # Determine client for MC selection (PoT mode only)
    selection_model = cfg('models.selection') or os.getenv("SELECTION_MODEL", "qwen-turbo")
    selection_client = anthropic_client if anthropic_client and selection_model.lower().startswith('claude') else client

    # Evaluation strategy: "hybrid" (rule-based MC + LLM open) or "llm_only"
    eval_strategy = cfg('evaluation.strategy') or os.getenv("EVAL_STRATEGY", "llm_only")

    skills_dir = cfg('skills.dir') or os.getenv('SKILLS_DIR', str(project_root / ".claude/skills/generated-from-failures-v1"))
    router = SkillsRouter(skills_dir)

    # Load FIXED baseline
    print("\n[0] Loading FIXED baseline results...")
    baseline_path = project_root / baseline_dir
    baseline_loader = None

    if baseline_path.exists():
        baseline_loader = load_baseline(str(baseline_path), splits=["val"])
        stats = baseline_loader.get_statistics()
        print(f"  ✓ Baseline accuracy: {stats['accuracy']:.2%}")
    else:
        print(f"  ⚠ Baseline not found at {baseline_path}")
        print(f"  Will regenerate baseline (slower)")

    # Load dataset
    val_csv = project_root / (cfg('paths.val_csv') or os.getenv('VAL_CSV', 'data/famma_non_arithmetic_val_split.csv'))

    if val_csv.exists():
        data = load_dataset(val_csv).head(max_questions)
    else:
        print(f"  ⚠ {val_csv} not found. Using sample data.")
        data = pd.DataFrame([
            {
                'question_id': 'demo_1',
                'question': 'What is the P/E ratio if earnings per share is $5 and stock price is $100?',
                'question_type': 'open-ended',
                'context': 'Company XYZ financial data.',
                'answers': '20',
                'subfield': 'equity valuation'
            }
        ])

    print(f"\n[1] Testing {len(data)} questions...\n")

    for idx, row in data.iterrows():
        qid = row.get('question_id', f'q_{idx}')
        question = row['question']
        question_type = row.get('question_type', 'open-ended')
        context = row.get('context', '') if pd.notna(row.get('context')) else ''
        options = row.get('options', None) if pd.notna(row.get('options')) else None
        ground_truth = str(row.get('answers', row.get('ground_truth', '')))

        print(f"Question: {question[:60]}...")

        # Get FIXED baseline (no API call if pre-computed!)
        if baseline_loader and qid in baseline_loader:
            baseline = baseline_loader.get_baseline(qid)
            baseline_answer = baseline.baseline_answer
            baseline_score = baseline.baseline_score
            print(f"  [Using pre-computed baseline]")
        else:
            # Fallback: Generate baseline
            gen_client = get_gen_client(gen_model, anthropic_client, client)
            baseline_result = generate_answer(
                client=gen_client,
                model=gen_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                options=options,
                skill_content=None,
                selection_client=selection_client
            )
            baseline_answer = baseline_result['answer']
            baseline_score = evaluate_answer(
                client=client,
                model=eval_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                generated_answer=baseline_answer,
                generated_explanation=baseline_result.get('explanation', ''),
                ground_truth=ground_truth,
                eval_strategy=eval_strategy
            )

        # With skill (LLM-based routing)
        subfield = row.get('subfield', 'unknown')

        # Route to relevant skill files
        skill_content = router.route_llm_based(
            question=question,
            context=context,
            subfield=subfield
        )
        skill_result = None

        if skill_content:
            gen_client = get_gen_client(gen_model, anthropic_client, client)
            skill_result = generate_answer(
                client=gen_client,
                model=gen_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                options=options,
                skill_content=skill_content,
                selection_client=selection_client
            )
            skill_score = evaluate_answer(
                client=client,
                model=eval_model,
                question_id=qid,
                question=question,
                question_type=question_type,
                context=context,
                generated_answer=skill_result['answer'],
                generated_explanation=skill_result.get('explanation', ''),
                ground_truth=ground_truth,
                eval_strategy=eval_strategy
            )
        else:
            skill_score = baseline_score

        # Print comparison
        delta = skill_score - baseline_score
        status = "✓ IMPROVED" if delta > 0 else "✗ REGRESSED" if delta < 0 else "= SAME"
        print(f"  {status:12s} | Baseline: {baseline_score:.0f} | Skill: {skill_score:.0f} | Δ: {delta:+.0f}")
        print(f"  Baseline answer: {baseline_answer}")
        if skill_result:
            print(f"  Skill answer:    {skill_result['answer']}")
        print(f"  Ground truth:    {ground_truth}\n")

        time.sleep(0.3)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Skill Learning Integration Examples")
    parser.add_argument(
        "mode",
        choices=["simple", "train-api"],
        help="Which mode to run: simple (quick comparison), train-api (automated)"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to YAML config file (e.g., configs/skill_learning/arithmetic.yaml)"
    )
    parser.add_argument(
        "--max-questions", "-n",
        type=int,
        default=None,
        help="Maximum questions to process for train set (val uses half). If not set, uses full datasets."
    )
    parser.add_argument(
        "--baseline-dir", "-b",
        type=str,
        default=None,
        help="Directory with pre-computed baseline results (default: from config or BASELINE_DIR env)"
    )
    parser.add_argument(
        "--train-baseline-dir",
        type=str,
        default=None,
        help="Separate baseline dir for train split (optional, overrides --baseline-dir for train)"
    )
    parser.add_argument(
        "--val-baseline-dir",
        type=str,
        default=None,
        help="Separate baseline dir for val split (optional, overrides --baseline-dir for val)"
    )
    parser.add_argument(
        "--splits",
        type=str,
        default=None,
        help="Which splits to run, comma-separated (e.g., 'train,val', 'train,eval', or 'train')"
    )
    parser.add_argument(
        "--subfields",
        type=str,
        default=None,
        help="Filter by subfields, comma-separated (e.g., 'portfolio management,derivatives')"
    )

    args = parser.parse_args()

    # Parse splits argument
    splits_list = None
    if args.splits:
        splits_list = [s.strip() for s in args.splits.split(",")]

    # Parse subfields argument
    subfields_list = None
    if args.subfields:
        subfields_list = [s.strip() for s in args.subfields.split(",")]

    # Load config if provided
    if args.config:
        load_config(args.config)

    if args.mode == "simple":
        example_simple_comparison(
            max_questions=args.max_questions,
            baseline_dir=args.baseline_dir
        )
    elif args.mode == "train-api":
        example_full_training_workflow(
            max_questions=args.max_questions,
            baseline_dir=args.baseline_dir,
            train_baseline_dir=args.train_baseline_dir,
            val_baseline_dir=args.val_baseline_dir,
            splits=splits_list,
            subfields=subfields_list
        )

    print("\n" + "="*80)
    print("Example complete!")
    print("="*80)
    