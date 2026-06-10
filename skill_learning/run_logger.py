"""
Run Logger - Training Signals Collection

Logs all system runs (baseline + skill) for training and validation.

Each log entry contains:
- Query metadata (qid, question, context, ground_truth)
- Baseline performance (answer, score)
- Skill selection (candidates, chosen_skill, version)
- Skill performance (answer, score)
- Delta metrics (is_fix, is_regress)
- Failure signature (subfield, modality, error_type, etc.)
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FailureSignature:
    """Failure signature for a question."""
    subfield: str
    modality: str
    error_type: int
    required_ops: List[str]
    missed_constraints: bool


@dataclass
class RunLogEntry:
    """Single run log entry."""
    # Query metadata (required fields)
    qid: str
    question: str
    context: str
    ground_truth: str
    baseline_answer: str
    baseline_score: float  # 0 or 1
    signature: Dict[str, Any]

    # All optional fields with defaults
    options: Optional[str] = None  # MC options text (e.g., "A. ... B. ... C. ...")
    baseline_explanation: Optional[str] = None  # Model's reasoning without skill
    candidates: List[str] = None  # Candidate skill IDs
    chosen_skill: Optional[str] = None  # Chosen skill ID or None
    skill_version: Optional[str] = None  # e.g., "v1", "v2"
    specific_skill_file: Optional[str] = None  # Primary sub-skill file (first selected)
    all_skill_files: Optional[List[str]] = None  # ALL sub-skill files used for this question
    skill_answer: Optional[str] = None
    skill_score: Optional[float] = None  # 0 or 1
    skill_explanation: Optional[str] = None  # Model's reasoning with skill
    skill_metadata: Optional[Dict[str, Any]] = None  # Progressive loading metadata (loaded_files, tool_call_sequence)
    
    # PoT mode specific fields (for code-based skills)
    baseline_code: Optional[str] = None  # Code generated in baseline run (PoT mode)
    skill_code: Optional[str] = None  # Code generated in skill run (PoT mode)
    baseline_execution_success: Optional[bool] = None  # Baseline code execution status (PoT mode)
    skill_execution_success: Optional[bool] = None  # Skill code execution status (PoT mode)
    
    delta: float = 0.0  # skill_score - baseline_score
    is_fix: bool = False  # baseline_fail && skill_correct
    is_regress: bool = False  # baseline_correct && skill_wrong
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            from datetime import datetime
            self.timestamp = datetime.now().isoformat()
        if self.candidates is None:
            self.candidates = []
        if self.all_skill_files is None and self.specific_skill_file:
            self.all_skill_files = [self.specific_skill_file]


class RunLogger:
    """Collects and manages run logs for training/validation."""

    def __init__(self, output_dir: str = None):
        import os
        if output_dir is None:
            output_dir = 'skill_learning/logs'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.train_log: List[RunLogEntry] = []
        self.val_log: List[RunLogEntry] = []

    def log_run(
        self,
        qid: str,
        question: str,
        context: str,
        ground_truth: str,
        baseline_answer: str,
        baseline_score: float,
        candidates: List[str],
        chosen_skill: Optional[str],
        skill_version: Optional[str],
        skill_answer: Optional[str],
        skill_score: Optional[float],
        signature: Dict[str, Any],
        split: str = "train",
        baseline_explanation: Optional[str] = None,
        skill_explanation: Optional[str] = None,
        specific_skill_file: Optional[str] = None,
        all_skill_files: Optional[List[str]] = None,
        options: Optional[str] = None,  # MC options text
        skill_metadata: Optional[Dict[str, Any]] = None,  # Progressive loading metadata
        baseline_code: Optional[str] = None,  # PoT mode: code generated in baseline run
        skill_code: Optional[str] = None,  # PoT mode: code generated in skill run
        baseline_execution_success: Optional[bool] = None,  # PoT mode: baseline code execution status
        skill_execution_success: Optional[bool] = None  # PoT mode: skill code execution status
    ):
        """
        Log a single run.

        Args:
            qid: Question ID
            question: Question text
            context: Context text
            ground_truth: Ground truth answer
            baseline_answer: Baseline answer (no skill)
            baseline_score: Baseline score (0 or 1)
            candidates: List of candidate skill IDs
            chosen_skill: Chosen skill ID or None
            skill_version: Skill version (e.g., "v1")
            skill_answer: Answer with skill applied
            skill_score: Score with skill (0 or 1)
            signature: Failure signature dict
            split: "train" or "val"
            baseline_explanation: Model's reasoning without skill
            skill_explanation: Model's reasoning with skill
            specific_skill_file: Primary sub-skill file (first selected)
            all_skill_files: ALL sub-skill files used for this question
            skill_metadata: Progressive loading metadata (loaded_files, tool_call_sequence)
            baseline_code: PoT mode - Code generated in baseline run
            skill_code: PoT mode - Code generated in skill run
            baseline_execution_success: PoT mode - Baseline code execution status
            skill_execution_success: PoT mode - Skill code execution status
        """
        # Calculate delta and flags
        if skill_score is not None:
            delta = skill_score - baseline_score
            is_fix = (baseline_score == 0) and (skill_score == 1)
            is_regress = (baseline_score == 1) and (skill_score == 0)
        else:
            delta = 0.0
            is_fix = False
            is_regress = False

        # Create log entry
        entry = RunLogEntry(
            qid=qid,
            question=question,
            context=context,
            ground_truth=ground_truth,
            baseline_answer=baseline_answer,
            baseline_score=baseline_score,
            baseline_explanation=baseline_explanation,
            options=options,
            candidates=candidates,
            chosen_skill=chosen_skill,
            skill_version=skill_version,
            specific_skill_file=specific_skill_file,
            all_skill_files=all_skill_files,
            skill_answer=skill_answer,
            skill_score=skill_score,
            skill_explanation=skill_explanation,
            skill_metadata=skill_metadata,
            baseline_code=baseline_code,  # PoT mode
            skill_code=skill_code,  # PoT mode
            baseline_execution_success=baseline_execution_success,  # PoT mode
            skill_execution_success=skill_execution_success,  # PoT mode
            delta=delta,
            is_fix=is_fix,
            is_regress=is_regress,
            signature=signature
        )

        # Add to appropriate log
        if split == "train":
            self.train_log.append(entry)
        elif split == "val":
            self.val_log.append(entry)
        else:
            raise ValueError(f"Invalid split: {split}. Must be 'train' or 'val'")

    def save_logs(self, epoch: int):
        """
        Save logs to disk (JSON and CSV formats for easy reading).

        Args:
            epoch: Current epoch number
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save train log
        if self.train_log:
            # JSON format (for easy inspection and programmatic access)
            train_json_path = self.output_dir / f"runlog_train_epoch{epoch}_{timestamp}.json"
            with open(train_json_path, 'w') as f:
                json.dump([asdict(entry) for entry in self.train_log], f, indent=2)

            # CSV format (for easy viewing in spreadsheet software)
            train_csv_path = self.output_dir / f"runlog_train_epoch{epoch}.csv"
            df_train = pd.DataFrame([asdict(entry) for entry in self.train_log])
            df_train.to_csv(train_csv_path, index=False)

            print(f"✓ Saved train log: {train_json_path}")
            print(f"✓ Saved train log (CSV): {train_csv_path}")

        # Save val log
        if self.val_log:
            # JSON format
            val_json_path = self.output_dir / f"runlog_val_epoch{epoch}_{timestamp}.json"
            with open(val_json_path, 'w') as f:
                json.dump([asdict(entry) for entry in self.val_log], f, indent=2)

            # CSV format
            val_csv_path = self.output_dir / f"runlog_val_epoch{epoch}.csv"
            df_val = pd.DataFrame([asdict(entry) for entry in self.val_log])
            df_val.to_csv(val_csv_path, index=False)

            print(f"✓ Saved val log: {val_json_path}")
            print(f"✓ Saved val log (CSV): {val_csv_path}")

    def load_logs(self, epoch: int):
        """
        Load logs from disk (CSV format).

        Args:
            epoch: Epoch number to load
        """
        # Load train log from CSV
        train_csv_path = self.output_dir / f"runlog_train_epoch{epoch}.csv"
        if train_csv_path.exists():
            df_train = pd.read_csv(train_csv_path)
            self.train_log = [RunLogEntry(**row) for _, row in df_train.iterrows()]
            print(f"✓ Loaded train log: {train_csv_path}")

        # Load val log from CSV
        val_csv_path = self.output_dir / f"runlog_val_epoch{epoch}.csv"
        if val_csv_path.exists():
            df_val = pd.read_csv(val_csv_path)
            self.val_log = [RunLogEntry(**row) for _, row in df_val.iterrows()]
            print(f"✓ Loaded val log: {val_csv_path}")

    def get_stats(self, split: str = "train") -> Dict[str, Any]:
        """
        Get statistics from logs.

        Args:
            split: "train" or "val"

        Returns:
            Dictionary of statistics
        """
        log = self.train_log if split == "train" else self.val_log

        if not log:
            return {}

        total = len(log)
        baseline_correct = sum(1 for e in log if e.baseline_score == 1)
        skill_applied = sum(1 for e in log if e.chosen_skill is not None)
        skill_correct = sum(1 for e in log if e.skill_score == 1)
        fixes = sum(1 for e in log if e.is_fix)
        regressions = sum(1 for e in log if e.is_regress)

        return {
            "total_queries": total,
            "baseline_accuracy": baseline_correct / total if total > 0 else 0,
            "skill_applied_rate": skill_applied / total if total > 0 else 0,
            "skill_accuracy": skill_correct / total if total > 0 else 0,
            "fix_count": fixes,
            "fix_rate": fixes / total if total > 0 else 0,
            "regress_count": regressions,
            "regress_rate": regressions / total if total > 0 else 0,
            "net_improvement": fixes - regressions
        }

    def get_skill_stats(self, split: str = "train") -> Dict[str, Dict[str, Any]]:
        """
        Get per-skill statistics.

        Args:
            split: "train" or "val"

        Returns:
            Dictionary mapping skill_id -> stats
        """
        log = self.train_log if split == "train" else self.val_log

        skill_stats = {}

        for entry in log:
            if entry.chosen_skill is None:
                continue

            skill_id = entry.chosen_skill

            if skill_id not in skill_stats:
                skill_stats[skill_id] = {
                    "used": 0,
                    "fixes": 0,
                    "regressions": 0,
                    "net": 0,
                    "delta_sum": 0.0
                }

            skill_stats[skill_id]["used"] += 1
            if entry.is_fix:
                skill_stats[skill_id]["fixes"] += 1
            if entry.is_regress:
                skill_stats[skill_id]["regressions"] += 1
            skill_stats[skill_id]["delta_sum"] += entry.delta

        # Calculate net improvement
        for skill_id, stats in skill_stats.items():
            stats["net"] = stats["fixes"] - stats["regressions"]

        return skill_stats

    def clear_logs(self):
        """Clear in-memory logs."""
        self.train_log = []
        self.val_log = []


# Example usage
if __name__ == "__main__":
    logger = RunLogger()

    # Example log entry
    logger.log_run(
        qid="english_20_1_r3",
        question="According to mean-variance criterion, which is correct?",
        context="Portfolio A: E(R)=10%, σ=15%. Portfolio B: E(R)=10%, σ=12%.",
        ground_truth="B",
        baseline_answer="A",
        baseline_score=0.0,
        candidates=["portfolio-mgmt-v1", "risk-mgmt-v1"],
        chosen_skill="portfolio-mgmt-v1",
        skill_version="v1",
        skill_answer="B",
        skill_score=1.0,
        signature={
            "subfield": "portfolio management",
            "modality": "text-only",
            "error_type": 3,
            "required_ops": ["comparison", "risk-return tradeoff"],
            "missed_constraints": True
        },
        split="train",
        options="A. Portfolio A\nB. Portfolio B\nC. Both are equally good\nD. Cannot determine"
    )

    # Save logs
    logger.save_logs(epoch=1)

    # Get stats
    stats = logger.get_stats("train")
    print(f"\nTrain Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    skill_stats = logger.get_skill_stats("train")
    print(f"\nSkill Stats:")
    for skill_id, stats in skill_stats.items():
        print(f"  {skill_id}: {stats}")
