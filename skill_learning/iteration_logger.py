"""
Iteration Logger - Track and Analyze Sandbox Iteration Attempts

Provides functionality to:
- Save iteration logs for each sandbox attempt
- Analyze patterns across failed attempts
- Support recovery from intermediate states
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class IterationLogger:
    """Manages iteration logging for sandbox verification attempts."""

    def __init__(self, checkpoint_dir: Path):
        """
        Initialize iteration logger.

        Args:
            checkpoint_dir: Base checkpoint directory
        """
        self.checkpoint_dir = Path(checkpoint_dir)

    def save_iteration_log(
        self,
        file_key: str,
        epoch: int,
        attempt: int,
        content: Optional[str],
        metrics: Dict,
        passed: bool
    ) -> None:
        """
        Save iteration log for analysis and recovery.

        Stores both metrics (JSON) and skill content (MD) for each attempt.

        Args:
            file_key: Skill file being refined (e.g., "portfolio_management/concept_confusion.md")
            epoch: Current epoch number
            attempt: Attempt number within the epoch
            content: Skill content (None if no content generated)
            metrics: Sandbox metrics and analysis
            passed: Whether this attempt passed sandbox
        """
        log_dir = self.checkpoint_dir / f"epoch_{epoch}" / "iterations"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize file_key for filename
        safe_file_key = file_key.replace('/', '_').replace('\\', '_')

        # Save metrics
        log_file = log_dir / f"{safe_file_key}_attempt_{attempt}.json"
        log_data = {
            'file_key': file_key,
            'epoch': epoch,
            'attempt': attempt,
            'passed': passed,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        # Save content if available
        if content:
            content_file = log_dir / f"{safe_file_key}_attempt_{attempt}.md"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(content)

    def load_iteration_history(
        self,
        file_key: str,
        epoch: int
    ) -> List[Dict]:
        """
        Load iteration history for a specific file and epoch.

        Args:
            file_key: Skill file path
            epoch: Epoch number

        Returns:
            List of iteration records sorted by attempt number
        """
        log_dir = self.checkpoint_dir / f"epoch_{epoch}" / "iterations"
        if not log_dir.exists():
            return []

        safe_file_key = file_key.replace('/', '_').replace('\\', '_')
        history = []

        for log_file in log_dir.glob(f"{safe_file_key}_attempt_*.json"):
            with open(log_file, 'r', encoding='utf-8') as f:
                history.append(json.load(f))

        return sorted(history, key=lambda x: x.get('attempt', 0))

    def load_iteration_content(
        self,
        file_key: str,
        epoch: int,
        attempt: int
    ) -> Optional[str]:
        """
        Load skill content from a specific iteration.

        Args:
            file_key: Skill file path
            epoch: Epoch number
            attempt: Attempt number

        Returns:
            Skill content or None if not found
        """
        safe_file_key = file_key.replace('/', '_').replace('\\', '_')
        content_file = (
            self.checkpoint_dir / f"epoch_{epoch}" / "iterations" /
            f"{safe_file_key}_attempt_{attempt}.md"
        )

        if content_file.exists():
            with open(content_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def analyze_failed_attempts(
        self,
        file_key: str,
        iteration_history: List[Dict]
    ) -> Dict:
        """
        Analyze patterns across failed sandbox attempts.

        Detects:
        - Oscillation (same errors repeating)
        - Regression (Q+ getting worse)
        - Plateau (no improvement)
        - Stubborn cases (always fail)

        Args:
            file_key: Skill file being refined
            iteration_history: List of attempt records from _refine_with_retry

        Returns:
            Analysis dict with patterns and recommendations
        """
        analysis = {
            'file_key': file_key,
            'num_attempts': len(iteration_history),
            'patterns': [],
            'recommendations': []
        }

        if len(iteration_history) < 2:
            return analysis

        # Extract scores
        scores = [h.get('score', h.get('q_minus_rate', 0)) for h in iteration_history]

        # 1. Check for oscillation
        if len(scores) >= 3:
            diffs = [scores[i+1] - scores[i] for i in range(len(scores)-1)]
            sign_changes = sum(1 for i in range(len(diffs)-1) if diffs[i] * diffs[i+1] < 0)
            if sign_changes >= len(diffs) - 1:
                analysis['patterns'].append('oscillation')
                analysis['recommendations'].append(
                    'Skill changes are oscillating. Consider: '
                    '(1) More specific constraints, (2) Different approach'
                )

        # 2. Check for Q+ regression trend
        q_plus_rates = [h.get('q_plus_rate', 1.0) for h in iteration_history]
        if len(q_plus_rates) >= 2:
            if all(q_plus_rates[i] >= q_plus_rates[i+1] for i in range(len(q_plus_rates)-1)):
                if q_plus_rates[0] - q_plus_rates[-1] > 0.1:  # >10% decline
                    analysis['patterns'].append('q_plus_declining')
                    analysis['recommendations'].append(
                        'Q+ retention is declining. Updates may be too aggressive. '
                        'Consider preserving more of the original skill.'
                    )

        # 3. Check for plateau
        if len(scores) >= 3:
            recent = scores[-3:]
            if max(recent) - min(recent) < 0.05:  # <5% variance
                analysis['patterns'].append('plateau')
                analysis['recommendations'].append(
                    'Score has plateaued. The skill may have reached its limit. '
                    'Consider: (1) More diverse evidence, (2) New approach, (3) Accept current best'
                )

        # 4. Best attempt analysis
        if iteration_history:
            best_idx = max(range(len(scores)), key=lambda i: scores[i])
            analysis['best_attempt'] = iteration_history[best_idx].get('attempt', best_idx + 1)
            analysis['best_score'] = scores[best_idx]

        return analysis

    def get_best_attempt(
        self,
        file_key: str,
        epoch: int
    ) -> Optional[Dict]:
        """
        Get the best attempt for a file in an epoch.

        Args:
            file_key: Skill file path
            epoch: Epoch number

        Returns:
            Best iteration record or None
        """
        history = self.load_iteration_history(file_key, epoch)
        if not history:
            return None

        # Find best by combined score or q_minus_rate
        return max(
            history,
            key=lambda h: h.get('metrics', {}).get('combined_score',
                          h.get('metrics', {}).get('solve_rate', 0))
        )
        