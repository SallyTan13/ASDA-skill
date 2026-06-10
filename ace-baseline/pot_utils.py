"""
Program of Thought (PoT) utilities for ACE system.

Shared helpers for code extraction, execution, and MC option selection.
"""

import re
import openai


def extract_code_from_response(response_text: str) -> str:
    """Extract Python code from ```python or ``` blocks."""
    match = re.search(r'```python\s*\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r'```\s*\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def execute_pot_code(code_str: str, timeout: int = 10) -> tuple:
    """
    Execute Python code and return (result_str, success_bool).
    Uses eval() on last line to get the result.
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
    """Map numerical PoT result to MC letter."""
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
        for ch in result:
            if ch in 'ABCDE':
                return ch
        return result
    except Exception as e:
        print(f"  [SEL ERROR] {e}", flush=True)
        return numerical_result


def pot_process_answer(
    gen_response: str,
    question: str,
    target: str,
    others: dict,
    selection_client,
    selection_model: str,
) -> tuple:
    """
    Full PoT pipeline: extract code → execute → MC select if needed.

    Args:
        gen_response: Raw generator response (may contain code block)
        question: The question text
        target: Ground truth answer
        others: Dict with question_type, options, original_question, context
        selection_client: OpenAI client for MC selection
        selection_model: Model name for MC selection

    Returns:
        Tuple of (final_answer, code_str, exec_output, exec_success, execution_trace_text)
        execution_trace_text is appended to gen_response for Reflector input.
    """
    # Try extracting code from the raw response first
    code_str = extract_code_from_response(gen_response)

    # If not found, the code might be inside a JSON "final_answer" field
    # with escaped newlines. Try to parse JSON and extract from final_answer.
    if not code_str:
        try:
            import json
            json_match = re.search(r'\{.*\}', gen_response, re.DOTALL)
            if json_match:
                try:
                    import json_repair
                    parsed = json_repair.loads(json_match.group(0))
                except (ImportError, Exception):
                    parsed = json.loads(json_match.group(0))
                final_answer_field = parsed.get("final_answer", "")
                if isinstance(final_answer_field, str):
                    code_str = extract_code_from_response(final_answer_field)
        except Exception:
            pass

    exec_output, exec_success = execute_pot_code(code_str)

    if not exec_success or not exec_output:
        # Code execution failed — fall back to raw answer
        trace = f"\n\n--- Code Execution Trace ---\nCode:\n```python\n{code_str}\n```\nExecution: FAILED (no output)\n"
        return exec_output or "", code_str, exec_output, exec_success, trace

    final_answer = exec_output
    question_type = others.get("question_type", "")
    options = others.get("options", "")
    context = others.get("context", "")

    # MC selection: map numerical result → letter
    if question_type == "multiple-choice" and options and selection_client:
        selected = select_mc_option(
            selection_client, selection_model,
            exec_output, question, str(options), context,
        )
        if selected:
            final_answer = selected

    trace = (
        f"\n\n--- Code Execution Trace ---\n"
        f"Code:\n```python\n{code_str}\n```\n"
        f"Execution Output: {exec_output}\n"
        f"Execution Success: {exec_success}\n"
        f"Final Answer (after selection): {final_answer}\n"
    )

    return final_answer, code_str, exec_output, exec_success, trace
