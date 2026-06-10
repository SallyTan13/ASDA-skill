"""
Checkpoint Manager - Save and Load Skill Training Checkpoints

Manages saving and loading of training checkpoints including:
- Skill library snapshots
- Run logs (train/val)
- Metrics
- Diff reports
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd


class SkillCheckpoint:
    """Manages skill library checkpoints."""

    def __init__(self, checkpoint_dir: str = None):
        if checkpoint_dir is None:
            checkpoint_dir = os.getenv('CHECKPOINT_DIR', 'skill_learning/checkpoints')
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        epoch: int,
        skills_dir: Path,
        run_log_train: List,
        run_log_val: List,
        train_metrics: Dict,
        val_metrics: Dict,
        diff_report: str,
        accepted: bool
    ):
        """
        Save a checkpoint with all components.

        Args:
            epoch: Epoch number
            skills_dir: Path to skill library directory
            run_log_train: Training run log
            run_log_val: Validation run log
            train_metrics: Training metrics
            val_metrics: Validation metrics
            diff_report: Diff report (what changed)
            accepted: Whether this checkpoint was accepted
        """
        ckpt_dir = self.checkpoint_dir / f"epoch_{epoch}"
        ckpt_dir.mkdir(exist_ok=True)

        # 1. Copy skill library
        skills_ckpt = ckpt_dir / "skills"
        if skills_ckpt.exists():
            shutil.rmtree(skills_ckpt)
        shutil.copytree(skills_dir, skills_ckpt)

        # 2. Save run logs (parquet)
        if run_log_train:
            df_train = pd.DataFrame(self._prepare_for_parquet(run_log_train))
            df_train.to_parquet(ckpt_dir / "runlog_train.parquet", index=False)

        if run_log_val:
            df_val = pd.DataFrame(self._prepare_for_parquet(run_log_val))
            df_val.to_parquet(ckpt_dir / "runlog_val.parquet", index=False)

        # 3. Save metrics
        with open(ckpt_dir / "train_metrics.json", 'w') as f:
            json.dump(train_metrics, f, indent=2)

        with open(ckpt_dir / "val_metrics.json", 'w') as f:
            json.dump(val_metrics, f, indent=2)

        # 4. Save diff report
        with open(ckpt_dir / "diff_report.md", 'w') as f:
            f.write(diff_report)

        # 5. Save checkpoint metadata
        metadata = {
            "epoch": epoch,
            "timestamp": datetime.now().isoformat(),
            "accepted": accepted,
            "train_metrics": train_metrics,
            "val_metrics": val_metrics
        }

        with open(ckpt_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        status = "✅ Accepted" if accepted else "❌ Rejected"
        print(f"\n{status} Checkpoint saved: {ckpt_dir}")

    def load_checkpoint(self, epoch: int) -> Dict:
        """
        Load a checkpoint.

        Args:
            epoch: Epoch number to load

        Returns:
            Dictionary with checkpoint data
        """
        ckpt_dir = self.checkpoint_dir / f"epoch_{epoch}"

        if not ckpt_dir.exists():
            raise FileNotFoundError(f"Checkpoint not found: {ckpt_dir}")

        # Load metadata
        with open(ckpt_dir / "metadata.json", 'r') as f:
            metadata = json.load(f)

        return {
            "epoch": epoch,
            "skills_dir": ckpt_dir / "skills",
            "metadata": metadata
        }

    def list_checkpoints(self) -> List[int]:
        """List all available checkpoint epochs."""
        epochs = []
        for path in self.checkpoint_dir.iterdir():
            if path.is_dir() and path.name.startswith("epoch_"):
                try:
                    epoch = int(path.name.split("_")[1])
                    epochs.append(epoch)
                except ValueError:
                    pass
        return sorted(epochs)

    def get_best_checkpoint(self) -> Dict:
        """Get the best checkpoint based on validation accuracy."""
        best_epoch = None
        best_val_acc = -1.0

        for epoch in self.list_checkpoints():
            ckpt = self.load_checkpoint(epoch)
            val_acc = ckpt["metadata"].get("val_metrics", {}).get("accuracy", 0)
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_epoch = epoch

        if best_epoch is None:
            raise FileNotFoundError("No checkpoints found")

        return self.load_checkpoint(best_epoch)

    def _prepare_for_parquet(self, entries: List) -> List[Dict]:
        """Convert run log entries to parquet-compatible format."""
        records = []
        for entry in entries:
            record = entry.__dict__.copy()
            # Convert complex types to JSON strings
            for key in ['signature', 'candidates', 'all_skill_files', 'skill_metadata']:
                if key in record and record[key] is not None:
                    record[key] = json.dumps(record[key])
            # Handle fields that might be dict/list instead of string
            for key in ['skill_answer', 'baseline_answer', 'ground_truth']:
                if key in record and record[key] is not None:
                    if isinstance(record[key], (dict, list)):
                        record[key] = json.dumps(record[key])
                    else:
                        record[key] = str(record[key])
            records.append(record)
        return records
        