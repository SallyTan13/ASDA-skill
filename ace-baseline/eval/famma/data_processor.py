"""
FAMMA DataProcessor for ACE system.

Handles FAMMA financial reasoning benchmark data:
- Multiple-choice questions: rule-based exact match evaluation
- Open-ended questions: LLM judge evaluation (FAMMA official JudgePrompt)

Matches the evaluation logic in skill_learning/integration_example.py
to ensure accuracy numbers are directly comparable.
"""

import os
import re
import json
import openai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Try to import json_repair for robust JSON parsing
try:
    import json_repair
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False


class DataProcessor:
    """
    Processor for FAMMA financial reasoning benchmark.

    Implements the three methods required by ACE:
    - process_task_data: Convert FAMMA JSONL to ACE format
    - answer_is_correct: Hybrid evaluation (rule-based MC + LLM judge open)
    - evaluate_accuracy: Overall accuracy calculation
    """

    def __init__(self, task_name: str):
        self.task_name = task_name  # "non_arithmetic" or "arithmetic"

        # Initialize LLM judge client for open-ended evaluation
        eval_provider = os.getenv("FAMMA_EVAL_PROVIDER", "dashscope")
        self.eval_model = os.getenv("FAMMA_EVAL_MODEL", "qwen-max")

        if eval_provider == "dashscope":
            api_key = os.getenv("DASHSCOPE_API_KEY", "")
            base_url = os.getenv(
                "QWEN_API_BASE",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        elif eval_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            base_url = "https://api.openai.com/v1"
        else:
            api_key = os.getenv("OPENAI_API_KEY", "")
            base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        self.eval_client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def process_task_data(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Convert FAMMA JSONL data to ACE standard format.

        Each FAMMA record has: question_id, question, context, options,
        answers, question_type, etc.

        ACE expects: context, question, target, others
        """
        processed_data = []

        for item in raw_data:
            question = item.get("question", "")
            context = item.get("context", "")
            options = item.get("options", "")
            question_type = item.get("question_type", "open-ended")
            target = item.get("answers", "")

            # Build the question text with options for MC questions
            full_question = question
            if question_type == "multiple-choice" and options:
                full_question = f"{question}\nOptions: {options}"

            processed_item = {
                "context": context if context else "",
                "question": full_question,
                "target": str(target),
                "others": {
                    "question_id": item.get("question_id", ""),
                    "question_type": question_type,
                    "options": options,
                    "original_question": question,
                    "task": self.task_name,
                },
            }
            processed_data.append(processed_item)

        return processed_data

    def answer_is_correct(self, predicted: str, ground_truth: str, **kwargs) -> bool:
        """
        FAMMA hybrid evaluation.

        - Multiple-choice: rule-based exact match (case-insensitive)
        - Open-ended: LLM judge using FAMMA official JudgePrompt

        The 'others' dict is passed via kwargs when available from ACE internals.
        We detect MC vs open from the predicted answer format as a fallback.
        """
        predicted = str(predicted).strip()
        ground_truth = str(ground_truth).strip()

        # Determine question type from kwargs or infer
        others = kwargs.get("others", {})
        question_type = others.get("question_type", "")

        if not question_type:
            # Infer: if ground truth is a single letter A-E, treat as MC
            if re.match(r"^[A-E]\.?$", ground_truth, re.IGNORECASE):
                question_type = "multiple-choice"
            else:
                question_type = "open-ended"

        if question_type == "multiple-choice":
            return self._mc_is_correct(predicted, ground_truth)
        else:
            return self._open_is_correct(
                predicted,
                ground_truth,
                question=others.get("original_question", ""),
                context=kwargs.get("context", ""),
                question_id=others.get("question_id", "unknown"),
            )

    def _mc_is_correct(self, predicted: str, ground_truth: str) -> bool:
        """Strict exact match for multiple-choice."""
        pred_clean = predicted.strip().upper()
        gt_clean = ground_truth.strip().upper()
        return pred_clean == gt_clean

    def _open_is_correct(
        self,
        predicted: str,
        ground_truth: str,
        question: str = "",
        context: str = "",
        question_id: str = "unknown",
    ) -> bool:
        """
        LLM judge for open-ended questions.
        Uses the FAMMA official JudgePrompt.
        """
        question_dict = {
            "question_id": question_id,
            "context": context,
            "type": "open-ended",
            "question": question,
            "student_answer": predicted,
            "student_explanation": "",
            "ground_truth": ground_truth,
        }

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
            response = self.eval_client.chat.completions.create(
                model=self.eval_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=1024,
            )
            result_text = response.choices[0].message.content.strip()

            # Parse JSON response
            json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
            if json_match:
                try:
                    if HAS_JSON_REPAIR:
                        result = json_repair.loads(json_match.group(0))
                    else:
                        result = json.loads(json_match.group(0))
                    is_correct_str = result.get(question_id, "incorrect").lower()
                    return is_correct_str == "correct"
                except (json.JSONDecodeError, Exception):
                    pass

            # Fallback
            if "correct" in result_text.lower() and "incorrect" not in result_text.lower():
                return True
            return False

        except Exception as e:
            print(f"  LLM judge error for {question_id}: {e}")
            return False

    def evaluate_accuracy(self, out: List[str], target: List[str]) -> float:
        """
        Calculate overall accuracy.
        Simple correct/total ratio.
        """
        if len(out) != len(target):
            raise ValueError("Prediction and target lists must have same length")

        if len(out) == 0:
            return 0.0

        correct = sum(
            1 for pred, gt in zip(out, target) if self.answer_is_correct(pred, gt)
        )
        return correct / len(out)
