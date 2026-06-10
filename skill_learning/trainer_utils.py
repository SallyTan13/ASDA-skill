"""
Trainer Utilities - Metrics, Statistics, and Helper Functions

Provides utility functions for skill training:
- Metrics computation
- Evidence grouping
- Skill statistics
- Validation gate logic
- Evidence stability analysis
- Diff report generation

Implemented as a mixin class to be inherited by SkillTrainer.
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


class TrainerUtilsMixin:
    """
    Mixin class providing utility methods for SkillTrainer.

    Expects the following attributes on self:
    - lambda_regress: float
    - M: int
    - working_skills_dir: Path
    - textual_optimizer: TextualOptimizer
    - prev_epoch_evidence: Dict
    """

    def compute_metrics(self, run_log: List) -> Dict:
        """
        Compute metrics from run log.

        accuracy = skill-only accuracy (how the current skill set performed)
        baseline_accuracy = baseline-only accuracy (without any skill)

        Args:
            run_log: List of RunLogEntry

        Returns:
            Dictionary of metrics
        """
        if not run_log:
            return {}

        total = len(run_log)
        skill_correct = sum(1 for e in run_log if e.skill_score == 1)
        baseline_correct = sum(1 for e in run_log if e.baseline_score == 1)
        fixes = sum(1 for e in run_log if e.is_fix)
        regressions = sum(1 for e in run_log if e.is_regress)

        acc = skill_correct / total if total > 0 else 0
        baseline_acc = baseline_correct / total if total > 0 else 0
        fix_rate = fixes / total if total > 0 else 0
        regress_rate = regressions / total if total > 0 else 0

        # Training loss: -acc + λ*regress_rate
        loss = -acc + self.lambda_regress * regress_rate

        return {
            "total": total,
            "accuracy": acc,
            "baseline_accuracy": baseline_acc,
            "fix_count": fixes,
            "fix_rate": fix_rate,
            "regress_count": regressions,
            "regress_rate": regress_rate,
            "loss": loss
        }

    def _group_evidence_by_file(self, Q_plus: List, Q_minus: List) -> Dict[str, Tuple[List, List]]:
        """
        Group evidence by specific_skill_file.

        Args:
            Q_plus: List of positive evidence cards
            Q_minus: List of negative evidence cards

        Returns:
            Dict mapping specific_skill_file -> (Q_plus_for_file, Q_minus_for_file)
        """
        grouped = defaultdict(lambda: ([], []))

        # Group Q+ by specific_skill_file (skip SKILL.md - it's always loaded)
        for card in Q_plus:
            file_key = card.specific_skill_file
            if file_key and file_key != "SKILL.md":
                grouped[file_key][0].append(card)

        # Group Q- by specific_skill_file (skip SKILL.md - it's always loaded)
        for card in Q_minus:
            file_key = card.specific_skill_file
            if file_key and file_key != "SKILL.md":
                grouped[file_key][1].append(card)

        # Convert defaultdict to regular dict with tuples
        result = {}
        for file_key, (plus_list, minus_list) in grouped.items():
            result[file_key] = (plus_list, minus_list)

        return result

    def compute_skill_stats(self, run_log: List) -> Dict[str, Dict]:
        """
        Compute per-file statistics for selecting update set.

        Groups by specific_skill_file (e.g., "portfolio_management/concept_confusion.md")
        since we have a single skill set with multiple files.

        Args:
            run_log: List of RunLogEntry

        Returns:
            Dictionary mapping specific_skill_file -> stats
        """
        stats = {}

        for entry in run_log:
            # Attribute to ALL files used (not just primary), skip SKILL.md
            files = getattr(entry, 'all_skill_files', None)
            if not files:
                specific = entry.specific_skill_file
                files = [specific] if specific and specific != "SKILL.md" else []

            for file_key in files:
                # Skip SKILL.md - it's always loaded, not a specific skill file
                if file_key == "SKILL.md":
                    continue
                if file_key not in stats:
                    stats[file_key] = {
                        "used": 0,
                        "fixes": 0,
                        "regressions": 0,
                        "net": 0,
                        "local_loss": 0
                    }

                stats[file_key]["used"] += 1
                if entry.is_fix:
                    stats[file_key]["fixes"] += 1
                if entry.is_regress:
                    stats[file_key]["regressions"] += 1

        # Calculate net and local loss
        for file_key, s in stats.items():
            s["net"] = s["fixes"] - self.lambda_regress * s["regressions"]
            if s["used"] > 0:
                s["local_loss"] = -s["net"] / s["used"]
            else:
                s["local_loss"] = 0

        return stats

    def select_update_set(self, stats: Dict[str, Dict]) -> List[str]:
        """
        Select top-M skill files to refine based on worst local loss.

        Args:
            stats: Per-file statistics (keyed by specific_skill_file)

        Returns:
            List of specific_skill_file paths to update
        """
        # Sort by local_loss (descending) - worst files first
        sorted_files = sorted(
            stats.items(),
            key=lambda x: x[1]["local_loss"],
            reverse=True
        )

        # Take top M
        update_set = [file_key for file_key, _ in sorted_files[:self.M]]

        print(f"\nSelected {len(update_set)} files for refinement:")
        for file_key in update_set:
            s = stats[file_key]
            print(f"  {file_key}: net={s['net']:.2f}, loss={s['local_loss']:.3f}")

        return update_set

    def _file_exists(self, skill_file: str) -> bool:
        """Check if a skill file exists in the working skills directory."""
        return (self.working_skills_dir / skill_file).exists()

    def _get_subfield_folder(self, subfield: str) -> str:
        """Convert subfield name to folder name."""
        import re as _re
        name = subfield.lower().strip()
        name = _re.sub(r'[^a-z0-9_\s]', '', name)
        name = _re.sub(r'\s+', '_', name)
        return name

    def _format_gap_cards_for_new_skill(self, cards: list) -> str:
        """
        Format gap cards for new skill creation.

        Creates abstracted evidence without full question text to avoid memorization.

        Args:
            cards: List of UnsolvedCard objects

        Returns:
            Formatted evidence string
        """
        formatted = ["## Capability Gap Evidence\n"]
        formatted.append(f"These {len(cards)} cases reveal a gap in existing skills:\n")

        for i, card in enumerate(cards[:5], 1):  # Limit to 5 cases
            # Abstract the question - only show key concepts, not full text
            question_abstract = card.question[:150] + "..." if len(card.question) > 150 else card.question

            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Topic**: {card.signature.get('subfield', 'unknown')}
**Question Pattern**: {question_abstract}
**Ground Truth**: {card.ground_truth}

**What Was Tried**: {card.skill_used.get('specific_file', 'N/A')}
**Result**: Incorrect

**Root Cause**: {card.diagnosis_explanation or 'Capability gap - no skill covers this scenario'}

---
""")

        formatted.append("""
**Action Required**: Create a new sub-skill to handle this pattern.
- Focus on the CONCEPT/PATTERN, not specific question text
- Create generalizable procedures
- Avoid copying exact questions (prevents memorization)
""")

        return "\n".join(formatted)

    def _determine_new_skill_path(self, skill_content: str, subfield: str) -> str:
        """
        Determine the relative file path for a newly created skill file.

        Tries to extract from SKILL_MD_ENTRY line in generated content.
        Falls back to {subfield_folder}/new_patterns.md.

        Args:
            skill_content: Generated skill content
            subfield: Subfield name

        Returns:
            Relative path like "portfolio_management/new_patterns.md"
        """
        import re
        import time

        subfield_folder = self._get_subfield_folder(subfield)

        # Try to extract path from SKILL_MD_ENTRY line
        entry_line = self.textual_optimizer.extract_skill_md_entry_from_content(skill_content)
        if entry_line:
            # Parse: | `path/file.md` | ... |
            match = re.search(r'`([^`]+\.md)`', entry_line)
            if match:
                return match.group(1)

        # Fallback: {subfield_folder}/new_patterns_{timestamp}.md
        timestamp = int(time.time()) % 10000
        return f"{subfield_folder}/new_patterns_{timestamp}.md"

    def passes_validation_gate(
        self,
        val_metrics: Dict,
        prev_val_metrics: Optional[Dict]
    ) -> bool:
        """
        Check if new skills pass validation gate.

        Criteria:
        - Δval_regress_rate <= 0 (hard constraint)
        - Δval_acc >= -ε (ε ≈ 0.003)

        Args:
            val_metrics: New validation metrics
            prev_val_metrics: Previous validation metrics

        Returns:
            True if passed, False otherwise
        """
        if prev_val_metrics is None:
            return True  # First epoch always passes

        delta_regress = val_metrics["regress_rate"] - prev_val_metrics["regress_rate"]
        delta_acc = val_metrics["accuracy"] - prev_val_metrics["accuracy"]

        epsilon = 0.003

        # Hard constraints
        passes_regress = delta_regress <= 0
        passes_acc = delta_acc >= -epsilon

        print(f"\nValidation Gate:")
        print(f"  Δregress_rate: {delta_regress:.4f} {'✅' if passes_regress else '❌'} (must be ≤ 0)")
        print(f"  Δaccuracy: {delta_acc:.4f} {'✅' if passes_acc else '❌'} (must be ≥ {-epsilon})")

        return passes_regress and passes_acc

    def _collect_raw_evidence_qids(self, run_log: List) -> Tuple[Dict[str, set], Dict[str, set]]:
        """
        Collect ALL Q+/Q- QIDs from run log (unsampled), grouped by specific_skill_file.

        Used for stability analysis where sampling noise would cause false signals.

        Args:
            run_log: List of RunLogEntry

        Returns:
            Tuple of (raw_Q_plus, raw_Q_minus) where each is
            Dict[specific_skill_file -> set of qids]
        """
        raw_Q_plus = defaultdict(set)
        raw_Q_minus = defaultdict(set)

        for entry in run_log:
            # Attribute to ALL files used (skip SKILL.md - it's always loaded)
            files = getattr(entry, 'all_skill_files', None)
            if not files:
                specific = entry.specific_skill_file
                files = [specific] if specific and specific != "SKILL.md" else []

            for file_key in files:
                # Skip SKILL.md - it's always loaded, not a specific skill file
                if file_key == "SKILL.md":
                    continue
                if entry.is_fix or entry.delta > 0:
                    raw_Q_plus[file_key].add(entry.qid)

                if entry.is_regress or entry.delta < 0:
                    raw_Q_minus[file_key].add(entry.qid)

        return dict(raw_Q_plus), dict(raw_Q_minus)

    def analyze_evidence_stability(
        self,
        raw_Q_plus: Dict[str, set],
        raw_Q_minus: Dict[str, set],
        epoch: int
    ):
        """
        Analyze evidence stability across epochs.

        Tracks which Q+/Q- cases remain stable, which are new, and which were converted.

        IMPORTANT: Uses full unsampled QID sets (not sampled evidence cards) to avoid
        false "lost"/"new" signals caused by sampling randomness.

        Args:
            raw_Q_plus: Full Q+ QIDs by specific_skill_file (from _collect_raw_evidence_qids)
            raw_Q_minus: Full Q- QIDs by specific_skill_file (from _collect_raw_evidence_qids)
            epoch: Current epoch number
        """
        print(f"\n[Evidence Stability Analysis - Epoch {epoch}]")

        if epoch == 1 or not self.prev_epoch_evidence:
            print("  First epoch - no previous evidence to compare")
            # Store current evidence for next epoch
            self.prev_epoch_evidence = {
                'Q_plus': raw_Q_plus,
                'Q_minus': raw_Q_minus
            }
            return

        # Current epoch evidence (already sets of qids)
        current_Q_plus = raw_Q_plus
        current_Q_minus = raw_Q_minus

        # Previous epoch evidence
        prev_Q_plus = self.prev_epoch_evidence.get('Q_plus', {})
        prev_Q_minus = self.prev_epoch_evidence.get('Q_minus', {})

        # Analyze for each skill
        all_skills = set(current_Q_plus.keys()) | set(current_Q_minus.keys()) | set(prev_Q_plus.keys()) | set(prev_Q_minus.keys())

        for skill in all_skills:
            curr_plus = current_Q_plus.get(skill, set())
            curr_minus = current_Q_minus.get(skill, set())
            prev_plus = prev_Q_plus.get(skill, set())
            prev_minus = prev_Q_minus.get(skill, set())

            # Calculate stability metrics
            stable_Q_plus = curr_plus & prev_plus  # Still Q+ in both epochs
            new_Q_plus = curr_plus - prev_plus     # Newly Q+ in this epoch
            lost_Q_plus = prev_plus - curr_plus    # Was Q+ but not anymore

            stable_Q_minus = curr_minus & prev_minus  # Still Q- in both epochs
            new_Q_minus = curr_minus - prev_minus     # Newly Q- in this epoch
            lost_Q_minus = prev_minus - curr_minus    # Was Q- but not anymore

            # Special cases: conversions
            Q_minus_to_Q_plus = prev_minus & curr_plus  # Was regression, now fixed!
            Q_plus_to_Q_minus = prev_plus & curr_minus  # Was fixed, now regression!

            # Print report for this skill
            if len(curr_plus) + len(curr_minus) + len(prev_plus) + len(prev_minus) > 0:
                print(f"\n  {skill}:")
                print(f"    Q+ (Fixes):")
                print(f"      Stable (still fixing):  {len(stable_Q_plus)}")
                print(f"      New (newly fixed):      {len(new_Q_plus)}")
                print(f"      Lost (no longer fixed): {len(lost_Q_plus)}")
                if Q_minus_to_Q_plus:
                    print(f"      🎉 Converted from Q-:   {len(Q_minus_to_Q_plus)} (regressions fixed!)")

                print(f"    Q- (Regressions):")
                print(f"      Stable (still breaking): {len(stable_Q_minus)}")
                print(f"      New (new regressions):   {len(new_Q_minus)}")
                print(f"      Lost (no longer break):  {len(lost_Q_minus)}")
                if Q_plus_to_Q_minus:
                    print(f"      ⚠️  Converted from Q+:    {len(Q_plus_to_Q_minus)} (fixes became regressions!)")

        # Store current evidence for next epoch
        self.prev_epoch_evidence = {
            'Q_plus': current_Q_plus,
            'Q_minus': current_Q_minus
        }

    def generate_diff_report(
        self,
        update_set: List[str],
        Q_plus_all: Dict,
        Q_minus_all: Dict,
        Q_plus_discover: Optional[List] = None,
        Q_zero_gap: Optional[List] = None
    ) -> str:
        """
        Generate diff report for checkpoint.

        Args:
            update_set: List of updated skill IDs
            Q_plus_all: All positive evidence
            Q_minus_all: All negative evidence
            Q_plus_discover: Discover evidence (optional)
            Q_zero_gap: Gap evidence (optional)

        Returns:
            Markdown diff report
        """
        report = f"# Skill Updates Report\n\n"
        report += f"**Timestamp**: {datetime.now().isoformat()}\n"
        report += f"**Updated Skills**: {len(update_set)}\n\n"

        # Standard Q+/Q- evidence
        report += "## Q+/Q- Evidence\n\n"
        for skill_id in update_set:
            report += f"### {skill_id}\n\n"
            report += f"- Positive evidence (Q+): {len(Q_plus_all.get(skill_id, []))}\n"
            report += f"- Negative evidence (Q-): {len(Q_minus_all.get(skill_id, []))}\n\n"

        # Residual evidence summary
        if Q_plus_discover or Q_zero_gap:
            report += "## Residual Evidence (Unsolved Cases)\n\n"

            if Q_plus_discover:
                report += f"### Q+_discover (Router/Trigger Issues): {len(Q_plus_discover)} cases\n\n"
                report += "These cases were solved by a different skill - need trigger updates.\n\n"

                # Group by solving skill
                by_solving = {}
                for card in Q_plus_discover:
                    solving = card.solving_skill or "unknown"
                    if solving not in by_solving:
                        by_solving[solving] = 0
                    by_solving[solving] += 1

                for skill, count in by_solving.items():
                    report += f"- `{skill}`: {count} cases\n"
                report += "\n"

            if Q_zero_gap:
                report += f"### Q0_gap (Capability Gaps): {len(Q_zero_gap)} cases\n\n"
                report += "These cases could not be solved by any skill - need new procedures or sub-skills.\n\n"

                # Group by diagnosis
                by_diagnosis = {}
                for card in Q_zero_gap:
                    diag = card.diagnosis or "unknown"
                    if diag not in by_diagnosis:
                        by_diagnosis[diag] = 0
                    by_diagnosis[diag] += 1

                for diag, count in by_diagnosis.items():
                    report += f"- `{diag}`: {count} cases\n"
                report += "\n"

        return report

    def _check_early_stopping(self, current_epoch: int) -> bool:
        """Check if early stopping criteria is met."""
        if self.history["best_epoch"] is None:
            return False

        epochs_since_best = current_epoch - self.history["best_epoch"]
        return epochs_since_best >= self.patience
        