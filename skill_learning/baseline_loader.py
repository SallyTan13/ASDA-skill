"""
Baseline Loader

Loads pre-computed baseline results from existing evaluation files.
This avoids regenerating baseline answers for each training epoch.

The baseline is FIXED - computed once and used as reference for all epochs.
This is critical for proper Q+/Q- evidence collection:
- Q+ (fixes) = baseline failed, skill succeeded
- Q- (regressions) = baseline succeeded, skill failed
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class BaselineResult:
    """Single baseline result entry."""
    question_id: str
    question: str
    question_type: str
    context: str
    ground_truth: str
    baseline_answer: str
    baseline_explanation: str
    baseline_correct: bool  # True if baseline got it right
    baseline_score: float   # 1.0 if correct, 0.0 if incorrect


class BaselineLoader:
    """
    Loads and manages pre-computed baseline results.

    Usage:
        loader = BaselineLoader("results/qwen_flash_non_arithmetic")
        loader.load_split("train")  # or "val", "test"

        # Get baseline for a specific question
        baseline = loader.get_baseline("english_1_1_r3")
        print(baseline.baseline_correct)  # True/False
    """

    def __init__(self, results_dir: str):
        """
        Initialize baseline loader.

        Args:
            results_dir: Directory containing evaluation results
                        (e.g., "results/qwen_flash_non_arithmetic")
        """
        self.results_dir = Path(results_dir)
        self.baselines: Dict[str, BaselineResult] = {}
        self.splits_loaded: List[str] = []

    def load_split(self, split: str) -> int:
        """
        Load baseline results for a specific split.

        Args:
            split: "train", "val", or "test"

        Returns:
            Number of entries loaded
        """
        # Try different filename patterns
        possible_files = [
            f"evaluation_results_{split}_final.json",
            f"evaluation_results_{split}.json",
            f"eval_results_{split}.json",
        ]

        eval_file = None
        for filename in possible_files:
            candidate = self.results_dir / filename
            if candidate.exists():
                eval_file = candidate
                break

        if not eval_file:
            raise FileNotFoundError(
                f"No evaluation results found for split '{split}' in {self.results_dir}. "
                f"Tried: {possible_files}"
            )

        with open(eval_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for entry in data:
            qid = entry['question_id']

            # Handle different field names
            is_correct = entry.get('is_correct', False)
            if isinstance(is_correct, str):
                is_correct = is_correct.lower() == 'correct'

            self.baselines[qid] = BaselineResult(
                question_id=qid,
                question=entry.get('question', ''),
                question_type=entry.get('question_type', 'open-ended'),
                context=entry.get('context', ''),
                ground_truth=str(entry.get('ground_truth', '')),
                baseline_answer=str(entry.get('generated_answer', '')),
                baseline_explanation=entry.get('generated_explanation', ''),
                baseline_correct=is_correct,
                baseline_score=1.0 if is_correct else 0.0
            )
            count += 1

        self.splits_loaded.append(split)
        print(f"✓ Loaded {count} baseline results from {eval_file.name}")

        return count

    def load_all_splits(self) -> int:
        """
        Load all available splits (train, val, test).

        Returns:
            Total number of entries loaded
        """
        total = 0
        for split in ["train", "val", "test"]:
            try:
                total += self.load_split(split)
            except FileNotFoundError:
                print(f"  ℹ No {split} split found (skipping)")
        return total

    def get_baseline(self, question_id: str) -> Optional[BaselineResult]:
        """
        Get baseline result for a specific question.

        Args:
            question_id: The question ID

        Returns:
            BaselineResult or None if not found
        """
        return self.baselines.get(question_id)

    def get_baseline_score(self, question_id: str) -> float:
        """
        Get baseline score for a specific question.

        Args:
            question_id: The question ID

        Returns:
            1.0 if correct, 0.0 if incorrect, -1.0 if not found
        """
        baseline = self.get_baseline(question_id)
        if baseline is None:
            return -1.0
        return baseline.baseline_score

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about loaded baselines.

        Returns:
            Dict with accuracy, counts, etc.
        """
        if not self.baselines:
            return {"error": "No baselines loaded"}

        total = len(self.baselines)
        correct = sum(1 for b in self.baselines.values() if b.baseline_correct)

        # By question type
        mc_total = sum(1 for b in self.baselines.values() if b.question_type == 'multiple-choice')
        mc_correct = sum(1 for b in self.baselines.values()
                        if b.question_type == 'multiple-choice' and b.baseline_correct)

        open_total = total - mc_total
        open_correct = correct - mc_correct

        return {
            "total": total,
            "correct": correct,
            "accuracy": correct / total if total > 0 else 0,
            "splits_loaded": self.splits_loaded,
            "by_type": {
                "multiple-choice": {
                    "total": mc_total,
                    "correct": mc_correct,
                    "accuracy": mc_correct / mc_total if mc_total > 0 else 0
                },
                "open-ended": {
                    "total": open_total,
                    "correct": open_correct,
                    "accuracy": open_correct / open_total if open_total > 0 else 0
                }
            }
        }

    def get_failures(self) -> List[BaselineResult]:
        """
        Get all baseline failures (questions baseline got wrong).

        These are candidates for Q+ evidence (skill can fix them).
        """
        return [b for b in self.baselines.values() if not b.baseline_correct]

    def get_successes(self) -> List[BaselineResult]:
        """
        Get all baseline successes (questions baseline got right).

        These need protection - skill should not break them (avoid Q-).
        """
        return [b for b in self.baselines.values() if b.baseline_correct]

    def __len__(self) -> int:
        return len(self.baselines)

    def __contains__(self, question_id: str) -> bool:
        return question_id in self.baselines


def load_baseline(results_dir: str, splits: Optional[List[str]] = None) -> BaselineLoader:
    """
    Convenience function to load baseline results.

    Args:
        results_dir: Directory with evaluation results
        splits: List of splits to load (default: ["train", "val"])

    Returns:
        Loaded BaselineLoader
    """
    loader = BaselineLoader(results_dir)

    if splits is None:
        splits = ["train", "val"]

    for split in splits:
        try:
            loader.load_split(split)
        except FileNotFoundError as e:
            print(f"  ⚠ {e}")

    return loader


if __name__ == "__main__":
    # Test with existing baseline
    import sys

    results_dir = sys.argv[1] if len(sys.argv) > 1 else "results/qwen_flash_non_arithmetic"

    print("="*70)
    print("Baseline Loader Test")
    print("="*70)

    loader = load_baseline(results_dir)

    print(f"\nLoaded {len(loader)} baseline entries")

    stats = loader.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Correct: {stats['correct']}")
    print(f"  Accuracy: {stats['accuracy']:.2%}")
    print(f"  Splits: {stats['splits_loaded']}")

    print(f"\nBy Question Type:")
    for qtype, data in stats['by_type'].items():
        print(f"  {qtype}: {data['correct']}/{data['total']} ({data['accuracy']:.2%})")

    print(f"\nBaseline Failures (Q+ candidates): {len(loader.get_failures())}")
    print(f"Baseline Successes (protect from Q-): {len(loader.get_successes())}")

    # Sample lookup
    print("\nSample lookup:")
    for qid in list(loader.baselines.keys())[:3]:
        b = loader.get_baseline(qid)
        status = "✓" if b.baseline_correct else "✗"
        print(f"  {status} {qid}: {b.baseline_answer[:30]}...")
