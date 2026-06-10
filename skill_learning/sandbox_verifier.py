"""
Sandbox Verifier - Verify Skill Updates with Sandbox Testing

Provides sandbox verification functionality:
- Test Q+ retention (should remain correct)
- Test Q- fixes (should be fixed)
- Test gap case solutions
- Test routing correctness

Implemented as a mixin class to be inherited by SkillTrainer.
"""

import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional, Callable


class SandboxVerifierMixin:
    """
    Mixin class providing sandbox verification methods.

    Expects the following attributes on self:
    - logger.train_log: List of RunLogEntry
    - sandbox_solve_threshold: float
    - sandbox_route_threshold: float
    - sandbox_max_cases: int
    - skills_loading_mode: str ("progressive" or "router")
    - anthropic_client: Optional Anthropic client
    - gen_model: Optional str
    - working_skills_dir: Path
    - router: SkillsRouter
    """

    def _sandbox_pass(self, solved: int, total: int, threshold: float) -> bool:
        """
        Determine if a sandbox check passes.

        For small samples (≤2 cases), solving at least 1 is enough — percentage
        thresholds are meaningless when N is tiny. For larger samples, the
        configured threshold applies normally.

        Args:
            solved: Number of cases solved
            total: Total number of test cases
            threshold: Configured threshold (e.g. 0.3)

        Returns:
            True if the sandbox check passes
        """
        if total == 0:
            return True
        if total <= 2:
            # Small sample: just need ≥1 solved
            return solved >= 1
        return (solved / total) >= threshold

    def _calculate_combined_score(self, q_plus_rate: float, q_minus_rate: float,
                                   q_plus_total: int, q_minus_total: int) -> float:
        """
        Calculate combined score, only including non-empty test sets.

        This prevents empty Q+ (default 100%) from artificially inflating the score
        when only Q- exists.
        """
        if q_plus_total == 0 and q_minus_total == 0:
            return 0.0
        elif q_plus_total == 0:
            # Only Q- exists, use Q- rate directly
            return q_minus_rate
        elif q_minus_total == 0:
            # Only Q+ exists, use Q+ rate directly
            return q_plus_rate
        else:
            # Both exist, average them
            return (q_plus_rate * 0.5 + q_minus_rate * 0.5)

    def _get_q_minus_entries_for_file(self, file_key: str) -> List:
        """Get Q- (regression/negative) RunLogEntries attributed to a specific file."""
        entries = []
        for entry in self.logger.train_log:
            files = getattr(entry, 'all_skill_files', None) or \
                    ([entry.specific_skill_file] if entry.specific_skill_file else [])
            if file_key in files:
                if entry.is_regress or entry.delta < 0:
                    entries.append(entry)
        return entries

    def _get_q_plus_entries_for_file(self, file_key: str) -> List:
        """Get Q+ (fix/positive) RunLogEntries attributed to a specific file."""
        entries = []
        for entry in self.logger.train_log:
            files = getattr(entry, 'all_skill_files', None) or \
                    ([entry.specific_skill_file] if entry.specific_skill_file else [])
            if file_key in files:
                if entry.is_fix or entry.delta > 0:
                    entries.append(entry)
        return entries

    def _cards_to_entries(self, cards: List) -> List:
        """
        Convert EvidenceCards to entry-like objects for sandbox testing.

        Creates SimpleNamespace objects with the fields needed by sandbox testing.
        This ensures sandbox uses the SAME evidence as refinement.

        Args:
            cards: List of EvidenceCard objects

        Returns:
            List of entry-like objects with required fields
        """
        from types import SimpleNamespace

        entries = []
        for card in cards:
            # Create entry-like object with fields needed by sandbox
            entry = SimpleNamespace(
                qid=card.qid,
                question=card.question,
                context=card.context,
                ground_truth=card.ground_truth,
                options=getattr(card, 'options', None),
                # Baseline info
                baseline_answer=card.baseline.get('answer', ''),
                baseline_score=card.baseline.get('score', 0),
                baseline_explanation=card.baseline.get('explanation', ''),
                # Skill info
                skill_answer=card.skill_k.get('answer', ''),
                skill_score=card.skill_k.get('score', 0),
                skill_explanation=card.skill_k.get('explanation', ''),
                # File attribution
                specific_skill_file=card.specific_skill_file,
                loaded_files=card.loaded_files or [],
                all_skill_files=card.loaded_files or ([card.specific_skill_file] if card.specific_skill_file else []),
                # Delta and flags
                delta=card.delta,
                is_fix=card.is_fix,
                is_regress=card.is_regress,
                # Signature
                signature=card.signature
            )
            entries.append(entry)

        return entries

    def _sandbox_verify_full(
        self,
        file_key: str,
        updated_content: str,
        gen_func: Callable,
        eval_func: Callable,
        use_combined_content: bool = False,
        q_plus_cards: List = None,
        q_minus_cards: List = None
    ) -> Tuple[bool, Dict, str]:
        """
        Full sandbox verification: test both Q+ retention and Q- fixes.

        Thresholds:
        - Q+ retention: ≥80% (must keep most fixes working)
        - Q- fix: ≥30% (should fix some failures)

        For small samples (≤2), uses relaxed rules (≥1 correct is enough).

        When use_combined_content=True (for common files):
        - Combines updated content with original loaded files for each entry
        - More accurate testing for common files that work with specific files

        Args:
            file_key: Specific skill file being verified
            updated_content: The proposed updated skill content
            gen_func: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: fn(question, context, answer, explanation, ground_truth) -> score
            use_combined_content: If True, combine updated file with original loaded files
            q_plus_cards: Optional list of Q+ evidence cards (use same data as refinement)
            q_minus_cards: Optional list of Q- evidence cards (use same data as refinement)

        Returns:
            (passed, metrics_dict, detail_message)
            metrics_dict includes 'fixed_qids' set for tracking which Q- entries were fixed
        """
        Q_PLUS_THRESHOLD = float(os.getenv('SANDBOX_Q_PLUS_THRESHOLD', '0.80'))
        Q_MINUS_THRESHOLD = self.sandbox_solve_threshold

        # Use provided evidence cards if available, otherwise query from train_log
        # This ensures sandbox uses the SAME data as evidence collection/refinement
        if q_plus_cards is not None or q_minus_cards is not None:
            # Convert evidence cards to entry-like objects for sandbox testing
            q_plus_entries = self._cards_to_entries(q_plus_cards or [])
            q_minus_entries = self._cards_to_entries(q_minus_cards or [])
        else:
            # Fallback: query from train_log (may have different data!)
            q_plus_entries = self._get_q_plus_entries_for_file(file_key)
            q_minus_entries = self._get_q_minus_entries_for_file(file_key)

        # Sample up to sandbox_max_cases each
        q_plus_test = q_plus_entries[:self.sandbox_max_cases]
        q_minus_test = q_minus_entries[:self.sandbox_max_cases]

        # Check if we should use progressive mode for sandbox
        use_progressive = (
            self.skills_loading_mode == 'progressive' and
            self.anthropic_client is not None and
            self.gen_model and self.gen_model.lower().startswith('claude')
        )

        q_plus_correct = 0
        q_minus_fixed = 0
        q_plus_details = []
        q_minus_details = []
        fixed_qids = set()

        # For common files, use combined content testing
        if use_combined_content or self._is_common_file(file_key):
            q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details, fixed_qids = \
                self._test_entries_with_combined_content(
                    file_key, updated_content, q_plus_test, q_minus_test, gen_func, eval_func
                )
            mode_str = "[combined]"
        elif use_progressive:
            q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details = \
                self._test_entries_progressive(
                    file_key, updated_content, q_plus_test, q_minus_test, eval_func
                )
            # Extract fixed_qids from details
            fixed_qids = {d['qid'] for d in q_minus_details if d.get('fixed', False)}
            mode_str = "[progressive]"
        else:
            q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details = \
                self._test_entries_router(
                    updated_content, q_plus_test, q_minus_test, gen_func, eval_func
                )
            # Extract fixed_qids from details
            fixed_qids = {d['qid'] for d in q_minus_details if d.get('fixed', False)}
            mode_str = "[router]"

        # Calculate rates
        q_plus_rate = q_plus_correct / len(q_plus_test) if q_plus_test else 1.0
        q_minus_rate = q_minus_fixed / len(q_minus_test) if q_minus_test else 0.0

        # Use small-sample rules
        q_plus_passed = self._sandbox_pass(q_plus_correct, len(q_plus_test), Q_PLUS_THRESHOLD)
        q_minus_passed = self._sandbox_pass(q_minus_fixed, len(q_minus_test), Q_MINUS_THRESHOLD)

        # Overall pass logic
        if not q_plus_test and not q_minus_test:
            passed = True
        elif not q_plus_test:
            passed = q_minus_passed
        elif not q_minus_test:
            passed = q_plus_passed
        else:
            passed = q_plus_passed and q_minus_passed

        # Build metrics dict
        metrics = {
            'q_plus_correct': q_plus_correct,
            'q_plus_total': len(q_plus_test),
            'q_plus_rate': q_plus_rate,
            'q_plus_passed': q_plus_passed,
            'q_plus_details': q_plus_details,
            'q_minus_fixed': q_minus_fixed,
            'q_minus_total': len(q_minus_test),
            'q_minus_rate': q_minus_rate,
            'q_minus_passed': q_minus_passed,
            'q_minus_details': q_minus_details,
            'fixed_qids': list(fixed_qids),  # Track which Q- entries were fixed (as list for JSON serialization)
            # Only include rates for non-empty test sets in combined score
            # This prevents empty Q+ (default 100%) from artificially inflating the score
            'combined_score': self._calculate_combined_score(q_plus_rate, q_minus_rate, len(q_plus_test), len(q_minus_test))
        }

        detail = (
            f"{mode_str} Q+ {q_plus_correct}/{len(q_plus_test)} ({q_plus_rate:.0%}), "
            f"Q- {q_minus_fixed}/{len(q_minus_test)} ({q_minus_rate:.0%})"
        )

        return passed, metrics, detail

    def _test_entries_progressive(
        self,
        file_key: str,
        updated_content: str,
        q_plus_test: List,
        q_minus_test: List,
        eval_func: Callable
    ) -> Tuple[int, int, List, List]:
        """Test entries in progressive mode (Claude tool_use)."""
        from skills_router import generate_with_progressive_loading

        q_plus_correct = 0
        q_minus_fixed = 0
        q_plus_details = []
        q_minus_details = []

        skill_file_path = self.working_skills_dir / file_key
        original_content = skill_file_path.read_text() if skill_file_path.exists() else ""

        try:
            # Write updated content to file
            skill_file_path.parent.mkdir(parents=True, exist_ok=True)
            skill_file_path.write_text(updated_content)

            # Reload router to pick up the updated file
            self._reload_router()
            skill_files_tool = self.router.build_skill_files_tool()

            from integration_example import build_famma_question_block, parse_json_response

            def test_entry(entry):
                """Test a single entry in progressive mode. Returns (success, qid, answer, explanation)."""
                try:
                    question_block = build_famma_question_block(
                        question_id=entry.qid,
                        question=entry.question,
                        question_type=getattr(entry, 'question_type', 'multiple-choice'),
                        context=entry.context,
                        options=getattr(entry, 'options', None)
                    )
                    prompt = self.router.build_progressive_prompt(
                        question=entry.question,
                        context=entry.context,
                        question_block=question_block
                    )
                    response_text, metadata = generate_with_progressive_loading(
                        client=self.anthropic_client,
                        model=self.gen_model,
                        prompt=prompt,
                        skill_files_tool=skill_files_tool,
                        skill_dir=str(self.working_skills_dir),
                        max_turns=5,
                        max_tokens=8196
                    )
                    answer = ""
                    explanation = ""
                    if response_text:
                        parsed, _ = parse_json_response(response_text)
                        if parsed and isinstance(parsed, dict):
                            for qid_key, data in parsed.items():
                                if isinstance(data, dict):
                                    answer = data.get('answer', '')
                                    explanation = data.get('explanation', '')
                                    break
                                elif isinstance(data, str):
                                    answer = data
                                    break
                    # Infer question_type from options field
                    question_type = "multiple-choice" if getattr(entry, 'options', None) else "open"
                    score = eval_func(
                        entry.question, entry.context, answer, explanation, entry.ground_truth,
                        question_type
                    )
                    return score == 1, entry.qid, answer, explanation
                except Exception as e:
                    return False, entry.qid, None, str(e)

            # Test Q+ entries
            for entry in q_plus_test:
                correct, qid, answer, explanation = test_entry(entry)
                if correct:
                    q_plus_correct += 1
                q_plus_details.append({
                    'qid': qid,
                    'correct': correct,
                    'answer': answer,
                    'explanation': explanation,
                    'ground_truth': entry.ground_truth
                })

            # Test Q- entries
            for entry in q_minus_test:
                fixed, qid, answer, explanation = test_entry(entry)
                if fixed:
                    q_minus_fixed += 1
                q_minus_details.append({
                    'qid': qid,
                    'fixed': fixed,
                    'answer': answer,
                    'explanation': explanation,
                    'ground_truth': entry.ground_truth
                })

        finally:
            # Restore original content
            if original_content:
                skill_file_path.write_text(original_content)
            elif skill_file_path.exists():
                skill_file_path.unlink()

        return q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details

    def _test_entries_router(
        self,
        updated_content: str,
        q_plus_test: List,
        q_minus_test: List,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[int, int, List, List]:
        """Test entries in router mode (direct gen_func)."""
        q_plus_correct = 0
        q_minus_fixed = 0
        q_plus_details = []
        q_minus_details = []

        def test_entry(entry):
            """Test a single entry in router mode. Returns (success, qid, answer, explanation)."""
            try:
                answer, explanation = gen_func(
                    entry.question,
                    entry.context,
                    getattr(entry, 'options', None),
                    updated_content
                )
                # Infer question_type from options field
                question_type = "multiple-choice" if getattr(entry, 'options', None) else "open"
                score = eval_func(
                    entry.question, entry.context, answer, explanation, entry.ground_truth,
                    question_type
                )
                return score == 1, entry.qid, answer, explanation
            except Exception as e:
                return False, entry.qid, None, str(e)

        # Test Q+ entries
        for entry in q_plus_test:
            correct, qid, answer, explanation = test_entry(entry)
            if correct:
                q_plus_correct += 1
            q_plus_details.append({
                'qid': qid,
                'correct': correct,
                'answer': answer,
                'explanation': explanation,  # For PoT mode, this contains code
                'ground_truth': entry.ground_truth
            })

        # Test Q- entries
        for entry in q_minus_test:
            fixed, qid, answer, explanation = test_entry(entry)
            if fixed:
                q_minus_fixed += 1
            q_minus_details.append({
                'qid': qid,
                'fixed': fixed,
                'answer': answer,
                'explanation': explanation,  # For PoT mode, this contains code
                'ground_truth': entry.ground_truth
            })

        return q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details

    def _test_entries_with_combined_content(
        self,
        updated_file_key: str,
        updated_content: str,
        q_plus_test: List,
        q_minus_test: List,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[int, int, List, List, set]:
        """
        Test entries using updated file combined with original loaded files.

        For common file updates, this combines:
        - The updated common file content
        - The original specific skill files that were loaded with each entry

        Args:
            updated_file_key: The file being updated (e.g., "common/visual_evidence.md")
            updated_content: The proposed updated content for this file
            q_plus_test: List of positive evidence entries to test
            q_minus_test: List of negative evidence entries to test
            gen_func: Generation function
            eval_func: Evaluation function

        Returns:
            Tuple of (q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details, fixed_qids)
        """
        q_plus_correct = 0
        q_minus_fixed = 0
        q_plus_details = []
        q_minus_details = []
        fixed_qids = set()

        def build_combined_content(entry) -> str:
            """Build combined content from entry's loaded_files."""
            loaded_files = getattr(entry, 'loaded_files', None) or []
            if not loaded_files:
                # Fallback to just the updated content
                return updated_content

            combined_parts = []
            for file_path in loaded_files:
                if file_path == updated_file_key:
                    # Use updated content for the file being tested
                    combined_parts.append(f"## {file_path}\n{updated_content}")
                elif file_path != "SKILL.md":
                    # Load original content for other files
                    original_content = self._load_skill_file_content(file_path)
                    if original_content:
                        combined_parts.append(f"## {file_path}\n{original_content}")

            return "\n\n".join(combined_parts) if combined_parts else updated_content

        def test_entry(entry):
            """Test a single entry with combined content. Returns (success, qid, answer, explanation)."""
            try:
                combined_content = build_combined_content(entry)
                answer, explanation = gen_func(
                    entry.question,
                    entry.context,
                    getattr(entry, 'options', None),
                    combined_content
                )
                # Infer question_type from options field
                question_type = "multiple-choice" if getattr(entry, 'options', None) else "open"
                score = eval_func(
                    entry.question, entry.context, answer, explanation, entry.ground_truth,
                    question_type
                )
                return score == 1, entry.qid, answer, explanation
            except Exception as e:
                return False, entry.qid, None, str(e)

        # Test Q+ entries
        for entry in q_plus_test:
            correct, qid, answer, explanation = test_entry(entry)
            if correct:
                q_plus_correct += 1
            q_plus_details.append({
                'qid': qid,
                'correct': correct,
                'answer': answer,
                'explanation': explanation,  # For PoT mode, this contains code
                'ground_truth': entry.ground_truth
            })

        # Test Q- entries
        for entry in q_minus_test:
            fixed, qid, answer, explanation = test_entry(entry)
            if fixed:
                q_minus_fixed += 1
                fixed_qids.add(qid)
            q_minus_details.append({
                'qid': qid,
                'fixed': fixed,
                'answer': answer,
                'explanation': explanation,  # For PoT mode, this contains code
                'ground_truth': entry.ground_truth
            })

        return q_plus_correct, q_minus_fixed, q_plus_details, q_minus_details, fixed_qids

    def _load_skill_file_content(self, file_path: str) -> Optional[str]:
        """Load skill file content from working_skills_dir.

        Args:
            file_path: Relative path to skill file (e.g., "equity/concept_confusion.md")

        Returns:
            File content or None if not found
        """
        if not hasattr(self, 'working_skills_dir') or not self.working_skills_dir:
            return None

        full_path = Path(self.working_skills_dir) / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding="utf-8") as f:
                    return f.read()
            except Exception:
                return None
        return None

    def _is_common_file(self, file_path: str) -> bool:
        """Check if a file path is a common skill file."""
        return file_path.startswith('common/') or '/common/' in file_path

    def _sandbox_verify_skill_update(
        self,
        file_key: str,
        updated_content: str,
        gen_func: Callable,
        eval_func: Callable,
        use_combined_content: bool = False
    ) -> Tuple[bool, float, str, set]:
        """
        Sandbox: verify that updated skill solves Q- cases.

        For ROUTER mode: Re-runs gen_func with updated_content prepended to prompt.
        For PROGRESSIVE mode: Temporarily writes updated content to file, then runs
        progressive generation with tool_use so Claude can load the updated file.

        When use_combined_content=True (for common files):
        - Combines updated content with original loaded files for each entry
        - More accurate testing for common files that work with specific files

        Args:
            file_key: Specific skill file being verified
            updated_content: The proposed updated skill content
            gen_func: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: fn(question, context, answer, explanation, ground_truth) -> score
            use_combined_content: If True, combine updated file with original loaded files

        Returns:
            (passed, solve_rate, detail_message, fixed_qids)
        """
        q_minus_entries = self._get_q_minus_entries_for_file(file_key)

        if not q_minus_entries:
            return True, 1.0, "No Q- cases to verify", set()

        test_entries = q_minus_entries[:self.sandbox_max_cases]
        solved = 0
        fixed_qids = set()

        use_progressive = (
            self.skills_loading_mode == 'progressive' and
            self.anthropic_client is not None and
            self.gen_model and self.gen_model.lower().startswith('claude')
        )

        # For common files, use combined content testing
        if use_combined_content or self._is_common_file(file_key):
            _, solved, _, q_minus_details, fixed_qids = self._test_entries_with_combined_content(
                file_key, updated_content, [], test_entries, gen_func, eval_func
            )
            mode_str = "[combined]"
        elif use_progressive:
            _, solved, _, q_minus_details = self._test_entries_progressive(
                file_key, updated_content, [], test_entries, eval_func
            )
            # Extract fixed_qids from details
            fixed_qids = {d['qid'] for d in q_minus_details if d.get('fixed', False)}
            mode_str = "[progressive]"
        else:
            _, solved, _, q_minus_details = self._test_entries_router(
                updated_content, [], test_entries, gen_func, eval_func
            )
            # Extract fixed_qids from details
            fixed_qids = {d['qid'] for d in q_minus_details if d.get('fixed', False)}
            mode_str = "[router]"

        solve_rate = solved / len(test_entries) if test_entries else 0
        passed = self._sandbox_pass(solved, len(test_entries), self.sandbox_solve_threshold)

        detail = (f"{mode_str} Solved {solved}/{len(test_entries)} Q- cases ({solve_rate:.0%}), "
                  f"threshold={self.sandbox_solve_threshold:.0%}"
                  f"{' [small-sample: ≥1 required]' if len(test_entries) <= 2 else ''}")
        return passed, solve_rate, detail, fixed_qids

    def _sandbox_verify_gap_update(
        self,
        file_key: str,
        updated_content: str,
        gap_cards: list,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[bool, float, str, List[Dict]]:
        """
        Sandbox: verify that updated skill solves Q0_gap cases.

        Args:
            file_key: Specific skill file being verified
            updated_content: The proposed updated skill content
            gap_cards: List of UnsolvedCard (Q0_gap cases for this file)
            gen_func: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: fn(question, context, answer, explanation, ground_truth) -> score

        Returns:
            (passed, solve_rate, detail_message, gap_details)
            gap_details is a list of per-question results with keys:
            - qid, solved, answer, explanation, ground_truth, error
        """
        if not gap_cards:
            return True, 1.0, "No gap cases to verify", []

        test_cards = gap_cards[:self.sandbox_max_cases]
        solved = 0
        gap_details = []

        use_progressive = (
            self.skills_loading_mode == 'progressive' and
            self.anthropic_client is not None and
            self.gen_model and self.gen_model.lower().startswith('claude')
        )

        if use_progressive:
            solved, gap_details = self._test_gap_cards_progressive(
                file_key, updated_content, test_cards, eval_func
            )
        else:
            solved, gap_details = self._test_gap_cards_router(
                updated_content, test_cards, gen_func, eval_func
            )

        solve_rate = solved / len(test_cards) if test_cards else 0
        passed = self._sandbox_pass(solved, len(test_cards), self.sandbox_solve_threshold)

        mode_str = "[progressive]" if use_progressive else "[router]"
        detail = (f"{mode_str} Solved {solved}/{len(test_cards)} gap cases ({solve_rate:.0%}), "
                  f"threshold={self.sandbox_solve_threshold:.0%}"
                  f"{' [small-sample: ≥1 required]' if len(test_cards) <= 2 else ''}")
        return passed, solve_rate, detail, gap_details

    def _test_gap_cards_progressive(
        self,
        file_key: str,
        updated_content: str,
        test_cards: List,
        eval_func: Callable
    ) -> Tuple[int, List[Dict]]:
        """Test gap cards in progressive mode.

        Returns:
            (solved_count, details_list) where details_list contains per-question results
        """
        from skills_router import generate_with_progressive_loading

        skill_file_path = self.working_skills_dir / file_key
        original_content = skill_file_path.read_text() if skill_file_path.exists() else ""
        solved = 0
        details = []

        try:
            skill_file_path.parent.mkdir(parents=True, exist_ok=True)
            skill_file_path.write_text(updated_content)

            self._reload_router()
            skill_files_tool = self.router.build_skill_files_tool()

            from integration_example import build_famma_question_block, parse_json_response

            for card in test_cards:
                detail = {
                    'qid': card.qid,
                    'solved': False,
                    'answer': '',
                    'explanation': '',
                    'ground_truth': card.ground_truth,
                    'error': None
                }
                try:
                    question_block = build_famma_question_block(
                        question_id=card.qid,
                        question=card.question,
                        question_type=getattr(card, 'question_type', 'multiple-choice'),
                        context=card.context,
                        options=getattr(card, 'options', None)
                    )
                    prompt = self.router.build_progressive_prompt(
                        question=card.question,
                        context=card.context,
                        question_block=question_block
                    )
                    response_text, metadata = generate_with_progressive_loading(
                        client=self.anthropic_client,
                        model=self.gen_model,
                        prompt=prompt,
                        skill_files_tool=skill_files_tool,
                        skill_dir=str(self.working_skills_dir),
                        max_turns=5,
                        max_tokens=8196
                    )
                    answer = ""
                    explanation = ""
                    if response_text:
                        parsed, _ = parse_json_response(response_text)
                        if parsed and isinstance(parsed, dict):
                            for qid_key, data in parsed.items():
                                if isinstance(data, dict):
                                    answer = data.get('answer', '')
                                    explanation = data.get('explanation', '')
                                    break
                                elif isinstance(data, str):
                                    answer = data
                                    break

                    detail['answer'] = str(answer) if answer else ''
                    detail['explanation'] = str(explanation)[:2048] if explanation else ''

                    # Infer question_type from options field
                    question_type = "multiple-choice" if getattr(card, 'options', None) else "open"
                    score = eval_func(
                        card.question, card.context, answer, explanation, card.ground_truth,
                        question_type
                    )
                    if score == 1:
                        solved += 1
                        detail['solved'] = True
                except Exception as e:
                    detail['error'] = str(e)[:200]
                    print(f"      [Progressive sandbox] Error for {card.qid}: {e}")

                details.append(detail)

        finally:
            if original_content:
                skill_file_path.write_text(original_content)
            elif skill_file_path.exists():
                skill_file_path.unlink()

        return solved, details

    def _test_gap_cards_router(
        self,
        updated_content: str,
        test_cards: List,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[int, List[Dict]]:
        """Test gap cards in router mode.

        Returns:
            (solved_count, details_list) where details_list contains per-question results
        """
        solved = 0
        details = []

        for card in test_cards:
            detail = {
                'qid': card.qid,
                'solved': False,
                'answer': '',
                'explanation': '',
                'ground_truth': card.ground_truth,
                'error': None
            }
            try:
                answer, explanation = gen_func(
                    card.question,
                    card.context,
                    getattr(card, 'options', None),
                    updated_content
                )
                detail['answer'] = str(answer) if answer else ''
                detail['explanation'] = str(explanation)[:2048] if explanation else ''

                # Infer question_type from options field
                question_type = "multiple-choice" if getattr(card, 'options', None) else "open"
                score = eval_func(
                    card.question, card.context, answer, explanation, card.ground_truth,
                    question_type
                )
                if score == 1:
                    solved += 1
                    detail['solved'] = True
            except Exception as e:
                detail['error'] = str(e)[:200]

            details.append(detail)

        return solved, details

    def _sandbox_verify_routing(
        self,
        discover_cards: list
    ) -> Tuple[bool, float, str]:
        """
        Sandbox: verify that updated SKILL.md routes Q+_discover correctly.

        Re-routes discover cases and checks if the solving_skill is now selected.

        Args:
            discover_cards: List of UnsolvedCard (Q+_discover cases)

        Returns:
            (passed, route_rate, detail_message)
        """
        if not discover_cards:
            return True, 1.0, "No discover cases to verify"

        test_cards = discover_cards[:self.sandbox_max_cases]
        correct = 0

        for card in test_cards:
            try:
                selected = self.router.get_llm_selected_files(
                    question=card.question,
                    context=card.context,
                    subfield=card.signature.get('subfield', '')
                )
                selected_rel = [str(f.relative_to(self.router.skill_dir)) for f in selected]

                if card.solving_skill in selected_rel:
                    correct += 1
            except Exception:
                pass

        route_rate = correct / len(test_cards) if test_cards else 0
        passed = self._sandbox_pass(correct, len(test_cards), self.sandbox_route_threshold)

        detail = (f"Routed {correct}/{len(test_cards)} correctly ({route_rate:.0%}), "
                  f"threshold={self.sandbox_route_threshold:.0%}"
                  f"{' [small-sample: ≥1 required]' if len(test_cards) <= 2 else ''}")
        return passed, route_rate, detail

    def _verify_post_coverage_q0_gap(
        self,
        q0_gap_cards: List,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[List, List]:
        """
        Verify which Q0_gap cases are now fixed after Coverage phase updates.

        Uses the CURRENT skill files (already updated by Coverage phase) to test
        each Q0_gap case and determine which ones are now correctly answered.

        Args:
            q0_gap_cards: List of UnsolvedCard (Q0_gap cases)
            gen_func: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: fn(question, context, answer, explanation, ground_truth, question_type) -> score

        Returns:
            Tuple of (fixed_cards, unfixed_cards) where:
            - fixed_cards: UnsolvedCards that are now correctly answered (add to Q+)
            - unfixed_cards: UnsolvedCards that are still wrong (can go to Q-)
        """
        if not q0_gap_cards:
            return [], []

        fixed_cards = []
        unfixed_cards = []

        # Build combined skill content from each card's attributed files
        for card in q0_gap_cards:
            try:
                # Get files that were used for this card
                files_to_load = []
                if hasattr(card, 'skill_used') and card.skill_used:
                    files_to_load = card.skill_used.get('all_files', [])
                if not files_to_load and hasattr(card, 'loaded_files'):
                    files_to_load = card.loaded_files or []
                if not files_to_load:
                    specific_file = card.skill_used.get('specific_file') if hasattr(card, 'skill_used') else None
                    if specific_file:
                        files_to_load = [specific_file]

                # Build combined content from current (updated) skill files
                combined_content = self._build_combined_content_for_card(files_to_load)

                # Generate and evaluate
                answer, explanation = gen_func(
                    card.question,
                    card.context,
                    getattr(card, 'options', None),
                    combined_content
                )

                # Determine question type
                question_type = "multiple-choice" if getattr(card, 'options', None) else "open"
                score = eval_func(
                    card.question, card.context, answer, explanation, card.ground_truth,
                    question_type
                )

                if score == 1:
                    # Fixed! Mark and add to fixed_cards
                    card.mark_as_fixed()
                    fixed_cards.append(card)
                else:
                    # Still unfixed
                    card.mark_as_unfixed()
                    unfixed_cards.append(card)

            except Exception as e:
                # On error, treat as unfixed
                card.mark_as_unfixed()
                unfixed_cards.append(card)

        return fixed_cards, unfixed_cards

    def _build_combined_content_for_card(self, files_to_load: List[str]) -> str:
        """
        Build combined skill content from a list of skill files.

        Reads current (updated) content from working_skills_dir.

        Args:
            files_to_load: List of relative file paths

        Returns:
            Combined content string
        """
        if not files_to_load:
            return ""

        combined_parts = []
        for file_path in files_to_load:
            if file_path == "SKILL.md":
                continue
            content = self._load_skill_file_content(file_path)
            if content:
                combined_parts.append(f"## {file_path}\n{content}")

        return "\n\n".join(combined_parts)

    def _verify_post_coverage_q_plus(
        self,
        q_plus_cards: List,
        gen_func: Callable,
        eval_func: Callable
    ) -> Tuple[List, List]:
        """
        Verify which original Q+ cases are still correct after Coverage phase updates.

        For broken Q+ cards (now incorrect), swaps evidence:
        - new baseline = old skill_k (was correct)
        - new skill_k = post-verification result (now incorrect)

        Args:
            q_plus_cards: List of EvidenceCard (original Q+ cases to verify)
            gen_func: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: fn(question, context, answer, explanation, ground_truth, question_type) -> score

        Returns:
            Tuple of (retained_cards, broken_cards) where:
            - retained_cards: Q+ cards that are still correct
            - broken_cards: Q+ cards that are now incorrect (with swapped evidence)
        """
        if not q_plus_cards:
            return [], []

        retained_cards = []
        broken_cards = []

        for card in q_plus_cards:
            try:
                # Get files to load for this card
                files_to_load = []
                if hasattr(card, 'loaded_files') and card.loaded_files:
                    files_to_load = card.loaded_files
                elif hasattr(card, 'specific_skill_file') and card.specific_skill_file:
                    files_to_load = [card.specific_skill_file]

                # Build combined content from current (updated) skill files
                combined_content = self._build_combined_content_for_card(files_to_load)

                # Generate and evaluate
                answer, explanation = gen_func(
                    card.question,
                    card.context,
                    getattr(card, 'options', None),
                    combined_content
                )

                # Determine question type
                question_type = "multiple-choice" if getattr(card, 'options', None) else "open"
                score = eval_func(
                    card.question, card.context, answer, explanation, card.ground_truth,
                    question_type
                )

                if score == 1:
                    # Still correct, retain in Q+
                    retained_cards.append(card)
                else:
                    # Broken! Swap evidence and move to Q-
                    # Save old skill_k before overwriting
                    old_skill_k = dict(card.skill_k) if hasattr(card, 'skill_k') and card.skill_k else {}

                    # New skill_k = post-verification result (now wrong)
                    new_skill_k = {
                        'answer': str(answer) if answer else '',
                        'score': score,
                        'explanation': str(explanation)[:2048] if explanation else ''
                    }

                    # Swap evidence:
                    # - old skill_k (was correct) becomes new baseline
                    # - new result (now wrong) becomes new skill_k
                    card.baseline = old_skill_k
                    card.skill_k = new_skill_k

                    # Update delta and flags
                    card.delta = new_skill_k.get('score', 0) - old_skill_k.get('score', 0)
                    card.is_fix = False  # No longer a fix
                    card.is_regress = True  # Now a regression

                    broken_cards.append(card)

            except Exception as e:
                # On error, keep in Q+ (don't falsely move to Q-)
                retained_cards.append(card)

        return retained_cards, broken_cards