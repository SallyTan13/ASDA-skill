"""
Skills Router - Route questions to relevant skill files.

Three routing methods:
1. Rule-based: Parse SKILL.md file reference table, match by subfield + keywords
2. LLM-based: LLM reads SKILL.md navigation and selects specific files
3. Progressive: Build tool definition for Claude tool_use (on-demand loading)

Default: Progressive loading (requires Claude model, auto-fallback to LLM-based for others)

Both rule/LLM methods select from ALL files (common + subfield-specific).
Common files are NOT auto-included — they must be selected like any other file.

Environment Variables:
    SKILL_METHOD    "progressive" (default) or "router"
    GEN_MODEL       If not Claude, auto-fallback to router method

Usage:
    router = SkillsRouter(".claude/skills/famma-non-arithmetic-v1")

    # Rule-based (no API call, keyword matching from SKILL.md)
    content = router.route_rule_based(
        question="Which portfolio dominates under mean-variance?",
        subfield="portfolio management"
    )

    # LLM-based (LLM reads SKILL.md, selects files)
    content = router.route_llm_based(
        question="Which portfolio dominates under mean-variance?",
        context="Portfolio A: 10% return, 5% risk...",
        subfield="portfolio management"
    )

    # Progressive loading (build tool for Claude tool_use)
    tool_def = router.build_skill_files_tool()
    prompt = router.build_progressive_prompt(question, context)
    content = router.load_skill_file_content("common/visual_evidence.md")

    # Auto-detect method based on model
    from skills_router import determine_skill_method
    method = determine_skill_method(gen_model="qwen-max")  # Returns "router"
    method = determine_skill_method(gen_model="claude-3-5-haiku")  # Returns "progressive"

Standalone functions (without SkillsRouter):
    from skills_router import (
        discover_skill_files,
        build_skill_files_tool,
        build_progressive_prompt,
        load_skill_file_content,
        determine_skill_method
    )

    skill_files = discover_skill_files(".claude/skills/my-skills")
    tool_def = build_skill_files_tool(skill_files)
    method = determine_skill_method("claude-3-5-haiku", requested_method="progressive")
"""

import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple, Tuple
from dotenv import load_dotenv
from openai import OpenAI

from skill_learning.token_tracker import tracker as token_tracker

load_dotenv()

# ============================================================
# API Setup (lazy initialization to read from config)
# ============================================================

# Import config functions
try:
    from skill_learning.config import cfg, is_config_loaded
except ImportError:
    from config import cfg, is_config_loaded

# Lazy-loaded router model, provider, and client
_router_model_cache = None
_router_provider_cache = None
_router_client_cache = None

def get_router_model():
    """Get router model (lazy initialization from config)."""
    global _router_model_cache
    if _router_model_cache is None:
        if is_config_loaded():
            config_val = cfg('models.router')
            if config_val is not None:
                _router_model_cache = config_val
                print(f"  [SkillsRouter] Using router model from config: {_router_model_cache}")
            else:
                _router_model_cache = os.getenv('ROUTER_MODEL', 'qwen-max')
                print(f"  [SkillsRouter] ⚠️  Using router model from env/fallback: {_router_model_cache}")
        else:
            _router_model_cache = os.getenv('ROUTER_MODEL', 'qwen-max')
            print(f"  [SkillsRouter] ⚠️  Config not loaded, using fallback router model: {_router_model_cache}")
    return _router_model_cache

def get_router_provider():
    """Get router provider (lazy initialization from config).

    Returns: 'openrouter', 'anthropic', 'dashscope', or 'auto' (default).
    When 'auto', provider is detected from model name.
    """
    global _router_provider_cache
    if _router_provider_cache is None:
        if is_config_loaded():
            config_val = cfg('models.router_provider')
            if config_val is not None:
                _router_provider_cache = config_val
                print(f"  [SkillsRouter] Using router provider from config: {_router_provider_cache}")
            else:
                _router_provider_cache = os.getenv('ROUTER_PROVIDER', 'auto')
        else:
            _router_provider_cache = os.getenv('ROUTER_PROVIDER', 'auto')
    return _router_provider_cache

def get_router_client():
    """Get router client (lazy initialization based on router model and provider).

    Provider selection:
    1. Explicit provider from config (openrouter, anthropic, dashscope)
    2. Auto-detect from model name when provider is 'auto':
       - anthropic/* -> OpenRouter
       - claude* -> Anthropic
       - qwen* -> DashScope
       - others -> OpenAI
    """
    global _router_client_cache
    if _router_client_cache is None:
        router_model = get_router_model()
        router_provider = get_router_provider()

        # Explicit provider takes precedence
        if router_provider == 'openrouter':
            _api_key = os.getenv('OPENROUTER_API_KEY')
            if not _api_key:
                raise ValueError("OPENROUTER_API_KEY required when router_provider is 'openrouter'")
            _router_client_cache = OpenAI(api_key=_api_key, base_url="https://openrouter.ai/api/v1")
            print(f"  [SkillsRouter] Router client: OpenRouter ({router_model})")
        elif router_provider == 'anthropic':
            _api_key = os.getenv('ANTHROPIC_API_KEY')
            if not _api_key:
                raise ValueError("ANTHROPIC_API_KEY required when router_provider is 'anthropic'")
            _router_client_cache = OpenAI(api_key=_api_key, base_url="https://api.anthropic.com/v1")
            print(f"  [SkillsRouter] Router client: Anthropic ({router_model})")
        elif router_provider == 'dashscope':
            _api_key = os.getenv('DASHSCOPE_API_KEY')
            if not _api_key:
                raise ValueError("DASHSCOPE_API_KEY required when router_provider is 'dashscope'")
            _base_url = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
            _router_client_cache = OpenAI(api_key=_api_key, base_url=_base_url)
            print(f"  [SkillsRouter] Router client: DashScope ({router_model})")
        else:
            # Auto-detect from model name
            if router_model.startswith('anthropic/'):
                # OpenRouter model format (e.g., anthropic/claude-3.5-haiku)
                _api_key = os.getenv('OPENROUTER_API_KEY')
                if not _api_key:
                    raise ValueError(f"OPENROUTER_API_KEY required for model: {router_model}")
                _router_client_cache = OpenAI(api_key=_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"  [SkillsRouter] Router client: OpenRouter (auto-detected)")
            elif router_model.lower().startswith('claude'):
                _api_key = os.getenv('ANTHROPIC_API_KEY')
                if not _api_key:
                    raise ValueError("ANTHROPIC_API_KEY required for Claude models")
                _router_client_cache = OpenAI(api_key=_api_key, base_url="https://api.anthropic.com/v1")
                print(f"  [SkillsRouter] Router client: Anthropic (auto-detected)")
            elif router_model.lower().startswith('qwen'):
                _api_key = os.getenv('DASHSCOPE_API_KEY')
                if not _api_key:
                    raise ValueError("DASHSCOPE_API_KEY required for Qwen models")
                _base_url = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
                _router_client_cache = OpenAI(api_key=_api_key, base_url=_base_url)
                print(f"  [SkillsRouter] Router client: DashScope (auto-detected)")
            else:
                _api_key = os.getenv('OPENAI_API_KEY') or os.getenv('API_KEY')
                if not _api_key:
                    raise ValueError(f"No API key found for model: {router_model}")
                _base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
                _router_client_cache = OpenAI(api_key=_api_key, base_url=_base_url)
                print(f"  [SkillsRouter] Router client: OpenAI (fallback)")
    return _router_client_cache

def reset_router_cache():
    """Reset router caches. Call this when config changes."""
    global _router_model_cache, _router_provider_cache, _router_client_cache
    _router_model_cache = None
    _router_provider_cache = None
    _router_client_cache = None

# For backwards compatibility (deprecated - use functions instead)
ROUTER_MODEL = None  # Use get_router_model() instead
_client = None  # Use get_router_client() instead

# ============================================================
# Progressive Loading Prompt Template
# ============================================================

PROGRESSIVE_PROMPT_TEMPLATE = """You are a highly knowledgeable financial expert with access to specialized domain knowledge files.

# Quick Reference (SKILL.md)

{skill_md_content}

# Available Tools

You have access to a tool `load_skill_file` that can load detailed reference files:
{file_listing}

**IMPORTANT — Before answering, you MUST:**
1. Read the question carefully and identify the financial domain and potential reasoning pitfalls.
2. Use the `load_skill_file` tool to load the most relevant domain file(s) (1-3 files).
3. Also load common/ files if the question involves visual evidence, explicit constraints, or output formatting.
4. Only AFTER receiving the skill file content, provide your final answer.

# Your Task

{task_instructions}

{question_block}"""


# ============================================================
# LLM Routing Prompt
# ============================================================

LLM_ROUTE_PROMPT = """You are a skill file router. Given a financial question, its context, \
and the subfield, select the most relevant skill files from the navigation below.

## SKILL.md Navigation

{skill_md_content}

## Question Info

- Subfield: {subfield}
- Question: {question}
- Context: {context}

## Rules

1. Select from ALL available files — both common/ and subfield-specific files.
2. Common files (common/*.md) address cross-subfield issues (visual evidence, constraints, output format). Select them when relevant to the question.
3. Subfield files ({subfield}/*.md) address domain-specific issues. Match by subfield first, then by error type / pattern relevance.
4. Select 1-5 files maximum. Prefer fewer, more targeted files.
5. If no file is relevant, respond with: NONE

## Output Format

Return ONLY the file paths, one per line. Example:
common/visual_evidence.md
portfolio_management/concept_confusion.md
portfolio_management/wrong_targets.md

Or if none are relevant:
NONE"""


LLM_ROUTE_PROMPT_REMOVE_SUBFIELD = """You are a skill file router. Given a financial question and its context, select the most relevant skill files from the navigation below.

## Subfield Quick Guide

Pick the subfield based on the PRIMARY computation object:

- corporate finance: company/project decisions (NPV/IRR, WACC, capital structure, merger, post-merger share price, dividend growth/DCF).
- equity: stock-level valuation/return (dividends+price return, firm vs equity value, single-stock required return).
- fixed income: bonds & yield curve (bond price/YTM, spot/forward/discount factors, bootstrapping, duration/convexity, HPR).
- derivatives: derivative contracts & payoff/hedge (options/futures/forwards/swaps/CDS, contract multiplier, #contracts, Greeks, parity, BSM/binomial).
- portfolio management: portfolio-level risk/return & performance (beta/alpha at portfolio level, covariance/correlation, Sharpe/IR, attribution, rebalancing, tax efficiency methods).
- financial statement analysis: accounting statements & ratios (IS/BS/CF extraction, ROE/DuPont, margins/turnover, leverage ratios, working capital/CCC).
- economics: macro/FX mechanisms (PPP, exchange rate regimes, inflation/interest-rate macro relations, overshooting-style logic).
- alternative investments: real assets / non-traditional (real estate cash flows & sale proceeds, private assets, tax-adjusted property calculations; often "after-tax proceeds" on property).

Tie-breakers (when multiple seem plausible):
1) option/futures/swap/CDS pricing, payoff, or #contracts → derivatives.
2) bond pricing/YTM/curve/duration/bootstrapping → fixed income.
3) portfolio beta/variance/performance/attribution/tax-lot → portfolio management.
4) property lease income + sale after-tax proceeds → alternative investments.
5) reading financial statements / ratio definitions → financial statement analysis.

## SKILL.md Navigation

{skill_md_content}

## Question Info

- Question: {question}
- Context: {context}

## Rules

1. Use the Subfield Quick Guide above to identify the primary subfield from the question and context.
2. From the SKILL.md Navigation, select subfield-specific files whose **"Key Patterns"** column matches the question's core concept.
3. Then consider common files (common/*.md) — only add if genuinely relevant to the question characteristics (visual evidence, missed constraints, output format issues).
4. Select 1-4 files total. Prefer fewer, more targeted files.
5. If no file is relevant, respond with: NONE

## Output Format

Return ONLY the file paths, one per line. Example:
common/visual_evidence.md
portfolio_management/concept_confusion.md
portfolio_management/wrong_targets.md

Or if none are relevant:
NONE"""

# ============================================================
# SkillsRouter
# ============================================================


class FileIndex(NamedTuple):
    """Index entry for a skill file parsed from SKILL.md."""
    path: str           # e.g., "common/visual_evidence.md"
    subfield: str       # e.g., "Cross-subfield" or "Portfolio management"
    error_type: str     # e.g., "Concept confusion"
    keywords: List[str] # e.g., ["Mean-Variance Dominance", "CAPM Regression"]


class SkillsRouter:
    """Routes questions to relevant skill files within a 2-level skill set.

    Both routing methods select from ALL files (common + subfield).
    Common files are NOT auto-included — they are selected like any other.

    Structure expected:
        skill_dir/
          SKILL.md              # Navigation file with file reference table
          common/               # Cross-subfield skills
            visual_evidence.md
            missed_constraints.md
            wrong_output_format.md
          {subfield}/           # Subfield-specific skills
            concept_confusion.md
            wrong_targets.md
            ...
    """

    def __init__(self, skill_dir: str):
        self.skill_dir = Path(skill_dir)
        self.skill_md_content = ""
        self.all_files: Dict[str, Path] = {}  # relative_path → absolute Path
        self.file_index: List[FileIndex] = []  # parsed from SKILL.md

        self._load_skill_md()
        self._discover_files()
        self._parse_skill_md_index()

    def _load_skill_md(self):
        """Load SKILL.md content for LLM routing."""
        skill_md = self.skill_dir / "SKILL.md"
        if skill_md.exists():
            self.skill_md_content = skill_md.read_text(encoding='utf-8')
        else:
            print(f"Warning: SKILL.md not found at {skill_md}")

    def _discover_files(self):
        """Discover all skill files into a flat dict.

        Handles two layouts:
        1. 2-level: common/*.md, subfield/*.md (subdirectories)
        2. Flat: *.md files directly in skill_dir root
        """
        if not self.skill_dir.exists():
            print(f"Warning: Skill directory {self.skill_dir} does not exist")
            return

        folder_counts: Dict[str, int] = {}

        skip_names = {'SKILL.md', 'README.md', 'INDEX.md'}

        # 1. Discover files in subdirectories (2-level structure)
        for entry in sorted(self.skill_dir.iterdir()):
            if not entry.is_dir():
                continue

            md_files = sorted(entry.glob("*.md"))
            # Filter out navigation/meta files
            md_files = [f for f in md_files if f.name not in skip_names]
            if not md_files:
                continue

            folder_counts[entry.name] = len(md_files)
            for f in md_files:
                rel_path = str(f.relative_to(self.skill_dir))
                self.all_files[rel_path] = f

        # 2. If no subdirectory files found, discover flat files in root
        if not self.all_files:
            root_md = sorted(self.skill_dir.glob("*.md"))
            root_skill_files = [f for f in root_md if f.name not in skip_names]

            if root_skill_files:
                folder_counts["(root)"] = len(root_skill_files)
                for f in root_skill_files:
                    rel_path = f.name  # Just the filename for flat layout
                    self.all_files[rel_path] = f

        print(f"Skills discovered in {self.skill_dir.name}/:")
        for folder, count in sorted(folder_counts.items()):
            print(f"  {folder}/: {count} files")
        print(f"  Total: {len(self.all_files)} files")

    def _parse_skill_md_index(self):
        """Parse the Skill File Reference from SKILL.md to build a keyword index.

        Supports two formats:

        Format 1 — Pipe-delimited table (v1):
            | File Path | Subfield | Error Type | Key Patterns |
            |-----------|----------|------------|--------------|
            | `common/visual_evidence.md` | Cross-subfield | ... | Pattern1, Pattern2 |

        Format 2 — Markdown links (v2, generated-from-failures-v1, etc.):
            ### common/ (cross-subfield)
            - **[visual_evidence.md](common/visual_evidence.md)** — 10 patterns
              Key patterns: Pattern1, Pattern2
        """
        if not self.skill_md_content:
            print("Warning: No SKILL.md content to parse for index")
            return

        # Try Format 1 first (pipe-delimited table)
        self._parse_pipe_table_index()

        # If no entries found, try Format 2 (markdown links)
        if not self.file_index:
            self._parse_markdown_link_index()

        print(f"SKILL.md index: {len(self.file_index)} file entries parsed")

    def _parse_pipe_table_index(self):
        """Parse pipe-delimited table format from SKILL.md.

        Expected:
            | `common/visual_evidence.md` | Cross-subfield | Error type | Pattern1, Pattern2 |
        """
        for line in self.skill_md_content.split('\n'):
            line = line.strip()
            if not line.startswith('|'):
                continue

            cols = [c.strip() for c in line.split('|')]
            cols = [c for c in cols if c]

            if len(cols) < 4:
                continue

            file_path = cols[0].strip('`').strip()

            # Skip header / separator rows
            if file_path in ('File Path', '---', '---------') \
                    or file_path.startswith('---'):
                continue

            if file_path not in self.all_files:
                continue

            subfield = cols[1].strip()
            error_type = cols[2].strip()
            keywords_raw = cols[3].strip() if len(cols) > 3 else ""
            keywords = [k.strip() for k in keywords_raw.split(',') if k.strip()]

            self.file_index.append(FileIndex(
                path=file_path,
                subfield=subfield,
                error_type=error_type,
                keywords=keywords
            ))

    def _parse_markdown_link_index(self):
        """Parse markdown-link format from SKILL.md.

        Handles several variants:
          - **[name.md](subfield/name.md)** — N patterns
            Key patterns: Pattern1, Pattern2
          - [Readable Name](subfield/name.md) - description
          **Details**: [NAME.md](NAME.md)
        """
        lines = self.skill_md_content.split('\n')
        # Track current section heading for subfield inference
        current_section = ""
        seen_paths: set = set()  # Deduplicate entries
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Track section headings (### subfield/ or ### Priority N: Subfield)
            if line.startswith('###'):
                current_section = line.lstrip('#').strip()

            # Look for markdown links to .md files: [text](path.md)
            link_matches = re.findall(r'\[([^\]]*)\]\(([^)]*\.md)\)', line)

            for link_text, link_path in link_matches:
                # Skip navigation/meta files by filename
                filename = link_path.rsplit('/', 1)[-1]
                if filename.upper() in ('INDEX.MD', 'README.MD', 'SKILL.MD'):
                    continue
                # Skip if path doesn't point to a known file
                if link_path not in self.all_files:
                    continue
                # Skip duplicates
                if link_path in seen_paths:
                    continue
                seen_paths.add(link_path)

                # Infer subfield from folder name or section heading
                if '/' in link_path:
                    folder = link_path.split('/')[0]
                    subfield = folder.replace('_', ' ').title()
                elif current_section:
                    subfield = current_section
                else:
                    subfield = "Unknown"

                # Infer error type from filename
                filename = link_path.rsplit('/', 1)[-1].replace('.md', '')
                error_type = filename.replace('_', ' ').title()

                # Extract keywords from the same line and the next line
                keywords = []
                # Check for "Key patterns:" on current or next line
                for check_line in [line, lines[i + 1].strip() if i + 1 < len(lines) else ""]:
                    kp_match = re.search(r'[Kk]ey\s+[Pp]atterns?:\s*(.+)', check_line)
                    if kp_match:
                        keywords = [k.strip() for k in kp_match.group(1).split(',') if k.strip()]
                        break
                # Also extract keywords from "Common errors:" lines
                if not keywords:
                    for check_line in [line, lines[i + 1].strip() if i + 1 < len(lines) else ""]:
                        ce_match = re.search(r'[Cc]ommon\s+[Ee]rrors?:\s*(.+)', check_line)
                        if ce_match:
                            keywords = [k.strip() for k in ce_match.group(1).split(',') if k.strip()]
                            break

                self.file_index.append(FileIndex(
                    path=link_path,
                    subfield=subfield,
                    error_type=error_type,
                    keywords=keywords
                ))

            i += 1

    @staticmethod
    def _sanitize_subfield(subfield: str) -> str:
        """Convert subfield name to folder name format."""
        name = subfield.lower().strip()
        name = re.sub(r'[^a-z0-9_\s]', '', name)
        name = re.sub(r'\s+', '_', name)
        return name

    def _load_file_content(self, file_path: Path) -> str:
        """Load content from a single skill file."""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return ""

    def _build_content(self, file_paths: List[Path]) -> str:
        """Concatenate content from multiple skill files."""
        sections = []
        for fp in file_paths:
            content = self._load_file_content(fp)
            if content:
                sections.append(content)
        return "\n\n---\n\n".join(sections)

    # ----------------------------------------------------------
    # Rule-based routing
    # ----------------------------------------------------------

    def _match_subfield(self, index_subfield: str, query_subfield: str) -> bool:
        """Check if a file's subfield (from SKILL.md) matches the query subfield.

        Handles:
        - Exact match (case-insensitive)
        - "Cross-subfield" matches everything
        - Substring match (e.g., "portfolio" in "portfolio management")
        """
        idx_lower = index_subfield.lower().strip()
        query_lower = query_subfield.lower().strip()

        # Cross-subfield (common/) files can match any subfield
        if idx_lower == "cross-subfield":
            return True

        # Exact match
        if idx_lower == query_lower:
            return True

        # Sanitized match (e.g., "portfolio_management" vs "portfolio management")
        idx_sanitized = self._sanitize_subfield(index_subfield)
        query_sanitized = self._sanitize_subfield(query_subfield)
        if idx_sanitized == query_sanitized:
            return True

        # Substring match
        if idx_sanitized in query_sanitized or query_sanitized in idx_sanitized:
            return True

        return False

    def _match_keywords(self, keywords: List[str], question: str) -> int:
        """Count how many keywords from a file's index match the question text.

        Returns the number of keyword hits (case-insensitive).
        """
        question_lower = question.lower()
        hits = 0
        for kw in keywords:
            # Match individual words from the keyword phrase
            kw_words = kw.lower().split()
            if any(word in question_lower for word in kw_words if len(word) > 3):
                hits += 1
        return hits

    def route_rule_based(self, question: str, subfield: str) -> str:
        """Route by parsing SKILL.md index: match subfield + keywords.

        Selects files whose subfield matches (including cross-subfield/common)
        and optionally ranks by keyword overlap with the question.

        Args:
            question: The question text (used for keyword matching)
            subfield: The question's subfield (e.g., "portfolio management")

        Returns:
            Concatenated skill file content
        """
        selected = self._select_rule_based(question, subfield)
        selected_names = [str(f.relative_to(self.skill_dir)) for f in selected]
        print(f"[Rule] Selected {len(selected)} files: {selected_names}")
        return self._build_content(selected)

    def _select_rule_based(self, question: str, subfield: str) -> List[Path]:
        """Core rule-based selection logic. Returns list of file paths.

        Strategy:
        1. Filter files by subfield match (including cross-subfield)
        2. Rank by keyword overlap with question
        3. Return all subfield-matched files (keyword score used for ordering)
        """
        if not self.file_index:
            # Fallback: if no index, return all files for the subfield folder
            print("[Rule] Warning: No SKILL.md index, using folder-name fallback")
            return self._fallback_folder_match(subfield)

        scored: List[tuple] = []  # (score, FileIndex)

        for entry in self.file_index:
            if not self._match_subfield(entry.subfield, subfield):
                continue

            keyword_hits = self._match_keywords(entry.keywords, question)
            # Subfield-specific files get a base score of 1
            # Cross-subfield (common) files only selected if keywords match
            is_cross = entry.subfield.lower().strip() == "cross-subfield"
            if is_cross and keyword_hits == 0:
                continue

            score = keyword_hits + (0 if is_cross else 1)
            scored.append((score, entry))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        selected: List[Path] = []
        for _, entry in scored:
            if entry.path in self.all_files:
                selected.append(self.all_files[entry.path])

        return selected

    def _fallback_folder_match(self, subfield: str) -> List[Path]:
        """Fallback when no SKILL.md index: match by folder name."""
        subfield_key = self._sanitize_subfield(subfield)
        selected: List[Path] = []

        for rel_path, abs_path in sorted(self.all_files.items()):
            folder = rel_path.split('/')[0] if '/' in rel_path else ''
            if folder == subfield_key:
                selected.append(abs_path)
            elif folder == "common":
                selected.append(abs_path)
            else:
                # Fuzzy folder match
                if subfield_key in folder or folder in subfield_key:
                    selected.append(abs_path)

        return selected

    def get_rule_based_files(self, question: str, subfield: str) -> List[Path]:
        """Return the list of selected file paths (without loading content).

        Useful when the caller wants to inspect which files were selected.
        """
        return self._select_rule_based(question, subfield)

    # ----------------------------------------------------------
    # LLM-based routing
    # ----------------------------------------------------------

    def route_llm_based(self, question: str, context: str,
                        subfield: str) -> str:
        """Route using LLM to select files from SKILL.md navigation.

        LLM selects from ALL files (common + subfield). No auto-inclusion.

        Args:
            question: The question text
            context: The question context
            subfield: The question's subfield

        Returns:
            Concatenated skill file content (LLM-selected only)
        """
        selected = self._select_llm_based(question, context, subfield)
        selected_names = [str(f.relative_to(self.skill_dir)) for f in selected]
        print(f"[LLM] Selected {len(selected)} files: {selected_names}")
        return self._build_content(selected)

    def _select_llm_based(self, question: str, context: str,
                          subfield: str, max_retries: int = 3,
                          model: Optional[str] = None,
                          client: Optional[OpenAI] = None) -> List[Path]:
        """Core LLM-based selection logic. Returns list of file paths.

        When model and/or client are provided, they override the lazy-loaded
        router model and client (e.g. when called from evaluate_checkpoint with config).
        """
        prompt = LLM_ROUTE_PROMPT.format(
            skill_md_content=self.skill_md_content,
            subfield=subfield or "unknown",
            question=question,
            context=context or "N/A"
        )

        use_model = model if model is not None else get_router_model()
        use_client = client if client is not None else get_router_client()

        retry_delay = 10  # seconds
        result = None

        for retry in range(max_retries + 1):
            try:
                response = use_client.chat.completions.create(
                    model=use_model,
                    messages=[
                        {"role": "system",
                         "content": "You are a precise skill file router. "
                                    "Output only file paths or NONE."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=256
                )
                # Track router token usage
                token_tracker.add_from_response("phase3", "router", response, use_model)
                time.sleep(0.5)
                result = response.choices[0].message.content.strip()
                break  # Success

            except Exception as e:
                error_str = str(e)
                # Check for rate limit error (429)
                if '429' in error_str or 'rate_limit' in error_str.lower():
                    if retry < max_retries:
                        print(f"[LLM] ⚠️  Rate limit hit (retry {retry + 1}/{max_retries}), sleeping {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5  # Exponential backoff
                        continue
                    else:
                        print(f"[LLM] ❌ Rate limit exceeded after {max_retries} retries")
                        return []
                else:
                    print(f"[LLM] API error: {e}, returning empty selection")
                    return []

        if result is None:
            return []

        # Parse LLM response
        if result.upper().strip() == "NONE":
            print("[LLM] LLM selected no files")
            return []

        # Parse file paths from response (robust parsing)
        selected: List[Path] = []
        for line in result.strip().split('\n'):
            # Strip common formatting: backticks, dashes, numbers, whitespace
            cleaned = line.strip()
            # Remove numbered list prefix: "1. ", "2) "
            cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned)
            # Remove bullet prefix: "- ", "* "
            cleaned = re.sub(r'^[-*]\s*', '', cleaned)
            # Remove backticks (both surrounding and inline)
            cleaned = cleaned.strip('`').strip()
            # Remove any remaining leading/trailing whitespace
            cleaned = cleaned.strip()

            if not cleaned or cleaned.upper() == "NONE":
                continue

            # Skip lines that are not file paths (all valid paths end with .md)
            if not cleaned.endswith('.md'):
                continue

            # Try to extract a markdown link path if present: [text](path)
            link_match = re.search(r'\(([^)]*\.md)\)', cleaned)
            if link_match:
                cleaned = link_match.group(1)

            # Handle "pattern_name in file_path.md" format
            # e.g., "Dornbusch_Overshooting in economics/concept_confusion.md"
            if ' in ' in cleaned:
                parts = cleaned.split(' in ')
                # Take the last part which should be the file path
                cleaned = parts[-1].strip()

            # Resolve path relative to skill_dir
            candidate = self.skill_dir / cleaned
            if candidate.exists() and candidate.is_file():
                selected.append(candidate)
            else:
                # Try fuzzy matching: find closest file name
                fuzzy_match = self._fuzzy_find_file(cleaned)
                if fuzzy_match:
                    print(f"[LLM] Fuzzy match: '{cleaned}' → '{fuzzy_match}'")
                    selected.append(self.skill_dir / fuzzy_match)
                else:
                    print(f"[LLM] Warning: file not found — {cleaned}")

        if not selected:
            print("[LLM] No valid files from LLM response")

        return selected

    def get_llm_selected_files(self, question: str, context: str,
                               subfield: str,
                               model: Optional[str] = None,
                               client: Optional[OpenAI] = None) -> List[Path]:
        """Return the list of LLM-selected file paths (without loading content).

        Useful when the caller wants to inspect or log which files were chosen.
        When model/client are provided (e.g. from config), they override the
        lazy-loaded router model and client.
        """
        return self._select_llm_based(question, context, subfield,
                                     model=model, client=client)

    # ----------------------------------------------------------
    # Auto-routing (LLM without subfield)
    # ----------------------------------------------------------

    def route_auto(self, question: str, context: str) -> str:
        """Route using LLM to select files without requiring subfield.

        Uses LLM_ROUTE_PROMPT_REMOVE_SUBFIELD which lets the LLM identify
        the subfield from the question itself.

        Args:
            question: The question text
            context: The question context

        Returns:
            Concatenated skill file content (LLM-selected only)
        """
        selected = self._select_auto(question, context)
        selected_names = [str(f.relative_to(self.skill_dir)) for f in selected]
        print(f"[Auto] Selected {len(selected)} files: {selected_names}")
        return self._build_content(selected)

    def _select_auto(self, question: str, context: str,
                     max_retries: int = 3,
                     model: Optional[str] = None,
                     client: Optional[OpenAI] = None) -> List[Path]:
        """Core auto-routing logic (LLM without subfield). Returns list of file paths.

        When model and/or client are provided, they override the lazy-loaded
        router model and client.
        """
        prompt = LLM_ROUTE_PROMPT_REMOVE_SUBFIELD.format(
            skill_md_content=self.skill_md_content,
            question=question,
            context=context or "N/A"
        )

        use_model = model if model is not None else get_router_model()
        use_client = client if client is not None else get_router_client()

        retry_delay = 10  # seconds
        result = None

        for retry in range(max_retries + 1):
            try:
                response = use_client.chat.completions.create(
                    model=use_model,
                    messages=[
                        {"role": "system",
                         "content": "You are a precise skill file router. "
                                    "Output only file paths or NONE."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=256
                )
                # Track router token usage
                token_tracker.add_from_response("phase3", "auto_router", response, use_model)
                time.sleep(0.5)
                result = response.choices[0].message.content.strip()
                break  # Success

            except Exception as e:
                error_str = str(e)
                # Check for rate limit error (429)
                if '429' in error_str or 'rate_limit' in error_str.lower():
                    if retry < max_retries:
                        print(f"[Auto] ⚠️  Rate limit hit (retry {retry + 1}/{max_retries}), sleeping {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5  # Exponential backoff
                        continue
                    else:
                        print(f"[Auto] ❌ Rate limit exceeded after {max_retries} retries")
                        return []
                else:
                    print(f"[Auto] API error: {e}, returning empty selection")
                    return []

        if result is None:
            return []

        # Parse LLM response
        if result.upper().strip() == "NONE":
            print("[Auto] LLM selected no files")
            return []

        # Debug: print raw LLM response for troubleshooting
        # print(f"[Auto] Raw LLM response:\n{result}")

        # Parse file paths from response (robust parsing)
        selected: List[Path] = []
        for line in result.strip().split('\n'):
            # Strip common formatting: backticks, dashes, numbers, whitespace
            cleaned = line.strip()
            # Remove numbered list prefix: "1. ", "2) "
            cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned)
            # Remove bullet prefix: "- ", "* "
            cleaned = re.sub(r'^[-*]\s*', '', cleaned)
            # Remove backticks (both surrounding and inline)
            cleaned = cleaned.strip('`').strip()
            # Remove any remaining leading/trailing whitespace
            cleaned = cleaned.strip()

            if not cleaned or cleaned.upper() == "NONE":
                continue

            # Skip lines that are not file paths (all valid paths end with .md)
            if not cleaned.endswith('.md'):
                continue

            # Try to extract a markdown link path if present: [text](path)
            link_match = re.search(r'\(([^)]*\.md)\)', cleaned)
            if link_match:
                cleaned = link_match.group(1)

            # Handle "pattern_name in file_path.md" format
            # e.g., "Dornbusch_Overshooting in economics/concept_confusion.md"
            if ' in ' in cleaned:
                parts = cleaned.split(' in ')
                # Take the last part which should be the file path
                cleaned = parts[-1].strip()

            # Resolve path relative to skill_dir
            candidate = self.skill_dir / cleaned
            if candidate.exists() and candidate.is_file():
                selected.append(candidate)
            else:
                # Try fuzzy matching: find closest file name
                fuzzy_match = self._fuzzy_find_file(cleaned)
                if fuzzy_match:
                    print(f"[Auto] Fuzzy match: '{cleaned}' → '{fuzzy_match}'")
                    selected.append(self.skill_dir / fuzzy_match)
                else:
                    print(f"[Auto] Warning: file not found — {cleaned}")

        if not selected:
            print("[Auto] No valid files from LLM response")

        return selected

    def _fuzzy_find_file(self, bad_path: str) -> Optional[str]:
        """Try to find a matching file using fuzzy logic.

        Handles common LLM errors:
        - Truncated names: unit_currency_.md → unit_currency_percent.md
        - Extra underscores: _code_execution_error.md → code_execution_error.md
        - Extra prefix: md common/file.md → common/file.md
        """
        if not self.all_files:
            return None

        # Extract directory and filename
        if '/' in bad_path:
            dir_part, file_part = bad_path.rsplit('/', 1)
        else:
            dir_part, file_part = '', bad_path

        # Clean up common issues
        # Remove leading underscores from filename
        file_part_clean = file_part.lstrip('_')
        # Remove "md " prefix from path
        if dir_part.startswith('md '):
            dir_part = dir_part[3:]

        best_match = None
        best_score = 0

        for rel_path in self.all_files.keys():
            # Check directory match
            if '/' in rel_path:
                rel_dir, rel_file = rel_path.rsplit('/', 1)
            else:
                rel_dir, rel_file = '', rel_path

            # Directory must match (if specified)
            if dir_part and rel_dir != dir_part:
                continue

            # Score based on substring matching
            score = 0

            # Exact match (after cleanup)
            if rel_file == file_part_clean:
                return rel_path

            # Check if cleaned file_part is a prefix of actual filename
            if rel_file.startswith(file_part_clean.replace('.md', '')):
                score = len(file_part_clean)

            # Check if actual filename contains the key part
            key_part = file_part_clean.replace('.md', '').replace('_', '')
            rel_key = rel_file.replace('.md', '').replace('_', '')
            if key_part in rel_key or rel_key in key_part:
                score = max(score, min(len(key_part), len(rel_key)))

            if score > best_score:
                best_score = score
                best_match = rel_path

        # Only return if we have a reasonable match
        return best_match if best_score >= 5 else None

    def get_auto_selected_files(self, question: str, context: str,
                                model: Optional[str] = None,
                                client: Optional[OpenAI] = None) -> List[Path]:
        """Return the list of auto-selected file paths (without loading content).

        Useful when the caller wants to inspect or log which files were chosen.
        Uses LLM routing without requiring subfield.
        """
        return self._select_auto(question, context,
                                model=model, client=client)

    # ----------------------------------------------------------
    # Progressive Loading Support
    # ----------------------------------------------------------

    def get_discovered_files(self) -> Dict[str, Path]:
        """Return all discovered skill files.

        Returns:
            dict of {relative_path: absolute_path}
        """
        return self.all_files.copy()

    def load_skill_file_content(self, file_name: str) -> str:
        """Load content of a specific skill file by relative path.

        Args:
            file_name: Relative path (e.g., "common/visual_evidence.md")

        Returns:
            File content or error message
        """
        if file_name in self.all_files:
            return self._load_file_content(self.all_files[file_name])
        return f"Error: {file_name} not found in {self.skill_dir}"

    def build_skill_files_tool(self) -> dict:
        """Build Anthropic tool definition dynamically from discovered skill files.

        Returns tool schema for Claude's tool_use with enum populated from
        actual skill files.

        Returns:
            dict: Anthropic tool definition for load_skill_file
        """
        if not self.all_files:
            return {}

        # Group by directory for description text
        dirs: Dict[str, List[str]] = {}
        for rel_path in sorted(self.all_files.keys()):
            folder = rel_path.split('/')[0] if '/' in rel_path else "(root)"
            if folder not in dirs:
                dirs[folder] = []
            dirs[folder].append(rel_path)

        desc_lines = [
            "Load a detailed skill reference file with domain-specific "
            "financial reasoning guidance.",
            "",
            "Available files by domain:"
        ]
        for folder, paths in sorted(dirs.items()):
            label = folder.replace('_', ' ').title()
            desc_lines.append(f"  {label}:")
            for p in paths:
                desc_lines.append(f"    - {p}")

        return {
            "name": "load_skill_file",
            "description": "\n".join(desc_lines),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "enum": sorted(self.all_files.keys()),
                        "description": "Skill reference file to load"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Brief reason why this file is needed"
                    }
                },
                "required": ["file"]
            }
        }

    def get_skill_md_content(self) -> str:
        """Return SKILL.md content for progressive loading prompts."""
        return self.skill_md_content

    def get_file_listing(self) -> str:
        """Build a formatted file listing for progressive loading prompt.

        Returns:
            Formatted string with files grouped by domain
        """
        dirs: Dict[str, List[str]] = {}
        for rel_path in sorted(self.all_files.keys()):
            folder = rel_path.split('/')[0] if '/' in rel_path else "(root)"
            label = folder.replace('_', ' ').title()
            if label not in dirs:
                dirs[label] = []
            dirs[label].append(rel_path)

        file_listing = ""
        for label, paths in sorted(dirs.items()):
            file_listing += f"\n**{label}:**\n"
            for p in paths:
                file_listing += f"  - {p}\n"

        return file_listing

    def build_progressive_prompt(
        self,
        question: str,
        context: str = "",
        task_instructions: str = "Please answer the following financial question accurately.",
        question_block: str = ""
    ) -> str:
        """Build prompt for progressive disclosure method.

        Includes SKILL.md as quick reference and instructs the model to use
        the load_skill_file tool before answering.

        Args:
            question: The question text
            context: Question context
            task_instructions: Custom task instructions
            question_block: Pre-formatted question block (if provided, ignores question/context)

        Returns:
            Formatted progressive prompt
        """
        if not question_block:
            question_block = f"**Context:** {context}\n\n**Question:** {question}"

        return PROGRESSIVE_PROMPT_TEMPLATE.format(
            skill_md_content=self.skill_md_content,
            file_listing=self.get_file_listing(),
            task_instructions=task_instructions,
            question_block=question_block
        )

    def generate_progressive(
        self,
        client,  # Anthropic client
        model: str,
        question: str,
        context: str = "",
        task_instructions: str = "Please answer the following financial question accurately.",
        question_block: str = "",
        max_turns: int = 5,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> Tuple[str, dict]:
        """Multi-turn generation with progressive skill loading.

        Convenience method that builds prompt, tool definition, and handles
        the multi-turn conversation.

        Args:
            client: Anthropic client instance
            model: Model name (must be Claude)
            question: Question text
            context: Question context
            task_instructions: Custom task instructions
            question_block: Pre-formatted question block
            max_turns: Maximum conversation turns
            max_tokens: Max tokens per response
            temperature: Sampling temperature

        Returns:
            Tuple of (response_text, metadata_dict)
        """
        prompt = self.build_progressive_prompt(
            question=question,
            context=context,
            task_instructions=task_instructions,
            question_block=question_block
        )
        tool_def = self.build_skill_files_tool()

        return generate_with_progressive_loading(
            client=client,
            model=model,
            prompt=prompt,
            skill_files_tool=tool_def,
            skill_dir=str(self.skill_dir),
            max_turns=max_turns,
            max_tokens=max_tokens,
            temperature=temperature
        )


# ============================================================
# Standalone Functions (for use without SkillsRouter instance)
# ============================================================

def discover_skill_files(skill_dir: str) -> Dict[str, Path]:
    """Discover all skill .md files (excluding SKILL.md, README.md).

    Args:
        skill_dir: Path to skill directory

    Returns:
        dict of {relative_path: absolute_path}
    """
    skill_path = Path(skill_dir)
    skip = {'SKILL.md', 'README.md', 'INDEX.md'}
    files: Dict[str, Path] = {}

    if not skill_path.exists():
        return files

    # Check subdirectories first
    for entry in sorted(skill_path.iterdir()):
        if not entry.is_dir():
            continue
        for f in sorted(entry.glob("*.md")):
            if f.name not in skip:
                rel = str(f.relative_to(skill_path))
                files[rel] = f

    # If no subdirectory files, check root
    if not files:
        for f in sorted(skill_path.glob("*.md")):
            if f.name not in skip:
                files[f.name] = f

    return files


def build_skill_files_tool(skill_files: Dict[str, Path]) -> dict:
    """Build Anthropic tool definition from discovered skill files.

    Args:
        skill_files: dict of {relative_path: absolute_path}

    Returns:
        dict: Anthropic tool definition for load_skill_file
    """
    if not skill_files:
        return {}

    # Group by directory
    dirs: Dict[str, List[str]] = {}
    for rel_path in sorted(skill_files.keys()):
        folder = rel_path.split('/')[0] if '/' in rel_path else "(root)"
        if folder not in dirs:
            dirs[folder] = []
        dirs[folder].append(rel_path)

    desc_lines = [
        "Load a detailed skill reference file with domain-specific "
        "financial reasoning guidance.",
        "",
        "Available files by domain:"
    ]
    for folder, paths in sorted(dirs.items()):
        label = folder.replace('_', ' ').title()
        desc_lines.append(f"  {label}:")
        for p in paths:
            desc_lines.append(f"    - {p}")

    return {
        "name": "load_skill_file",
        "description": "\n".join(desc_lines),
        "input_schema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "enum": sorted(skill_files.keys()),
                    "description": "Skill reference file to load"
                },
                "reason": {
                    "type": "string",
                    "description": "Brief reason why this file is needed"
                }
            },
            "required": ["file"]
        }
    }


def load_skill_file_content(skill_dir: str, file_name: str) -> str:
    """Load content of a specific skill file by relative path.

    Args:
        skill_dir: Path to skill directory
        file_name: Relative path (e.g., "common/visual_evidence.md")

    Returns:
        File content or error message
    """
    file_path = Path(skill_dir) / file_name
    if file_path.exists():
        return file_path.read_text(encoding='utf-8')
    return f"Error: {file_name} not found in {skill_dir}"


def load_skill_md(skill_dir: str) -> str:
    """Load SKILL.md content.

    Args:
        skill_dir: Path to skill directory

    Returns:
        SKILL.md content or empty string
    """
    skill_md = Path(skill_dir) / "SKILL.md"
    if skill_md.exists():
        return skill_md.read_text(encoding='utf-8')
    return ""


def get_file_listing(skill_files: Dict[str, Path]) -> str:
    """Build a formatted file listing for progressive loading prompt.

    Args:
        skill_files: dict of {relative_path: absolute_path}

    Returns:
        Formatted string with files grouped by domain
    """
    dirs: Dict[str, List[str]] = {}
    for rel_path in sorted(skill_files.keys()):
        folder = rel_path.split('/')[0] if '/' in rel_path else "(root)"
        label = folder.replace('_', ' ').title()
        if label not in dirs:
            dirs[label] = []
        dirs[label].append(rel_path)

    file_listing = ""
    for label, paths in sorted(dirs.items()):
        file_listing += f"\n**{label}:**\n"
        for p in paths:
            file_listing += f"  - {p}\n"

    return file_listing


def build_progressive_prompt(
    skill_md_content: str,
    skill_files: Dict[str, Path],
    question: str,
    context: str = "",
    task_instructions: str = "Please answer the following financial question accurately.",
    question_block: str = ""
) -> str:
    """Build prompt for progressive disclosure method (standalone version).

    Args:
        skill_md_content: SKILL.md content
        skill_files: dict of discovered skill files
        question: The question text
        context: Question context
        task_instructions: Custom task instructions
        question_block: Pre-formatted question block (if provided, ignores question/context)

    Returns:
        Formatted progressive prompt
    """
    if not question_block:
        question_block = f"**Context:** {context}\n\n**Question:** {question}"

    file_listing = get_file_listing(skill_files)

    return PROGRESSIVE_PROMPT_TEMPLATE.format(
        skill_md_content=skill_md_content,
        file_listing=file_listing,
        task_instructions=task_instructions,
        question_block=question_block
    )


def generate_with_progressive_loading(
    client,  # Anthropic client
    model: str,
    prompt: str,
    skill_files_tool: dict,
    skill_dir: str,
    max_turns: int = 5,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    max_retries: int = 3
) -> Tuple[str, dict]:
    """Multi-turn generation with progressive skill loading via tool_use.

    Handles the multi-turn conversation where Claude can request skill files
    using the load_skill_file tool. Includes retry logic for rate limit errors.

    Args:
        client: Anthropic client instance
        model: Model name (must be Claude)
        prompt: Initial prompt (from build_progressive_prompt)
        skill_files_tool: Tool definition from build_skill_files_tool
        skill_dir: Path to skill directory for loading files
        max_turns: Maximum conversation turns
        max_tokens: Max tokens per response
        temperature: Sampling temperature
        max_retries: Maximum retries for rate limit errors

    Returns:
        Tuple of (response_text, metadata_dict)
        metadata_dict contains:
            - loaded_files: deduplicated list of unique files loaded
            - loaded_files_raw: raw list with duplicates (for debugging)
            - turns: number of conversation turns
            - tool_calls: total number of tool calls (may include duplicates)
            - tool_call_sequence: full sequence with reasons (for refinement)
            - skill_method: "progressive"
    """
    messages = [{"role": "user", "content": prompt}]
    loaded_files_raw = ['SKILL.md']  # Raw list with potential duplicates
    tool_call_sequence = []  # Full sequence with reasons for refinement
    response = None
    retry_delay = 10  # Initial delay for rate limit retries

    for turn in range(max_turns):
        # Retry loop for rate limit errors
        for retry in range(max_retries + 1):
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    tools=[skill_files_tool],
                    messages=messages
                )
                break  # Success, exit retry loop

            except Exception as e:
                error_str = str(e)
                # Check for rate limit error (429)
                if '429' in error_str or 'rate_limit' in error_str.lower():
                    if retry < max_retries:
                        print(f"  ⚠️  Rate limit hit (turn {turn + 1}, retry {retry + 1}/{max_retries}), sleeping {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5  # Exponential backoff
                        continue
                    else:
                        print(f"  ❌ Rate limit exceeded after {max_retries} retries (turn {turn + 1})")
                        loaded_files_unique = _deduplicate_preserve_order(loaded_files_raw)
                        return None, {
                            'loaded_files': loaded_files_unique,
                            'loaded_files_raw': loaded_files_raw,
                            'turns': turn + 1,
                            'tool_calls': len(loaded_files_raw) - 1,
                            'unique_files': len(loaded_files_unique) - 1,
                            'tool_call_sequence': tool_call_sequence,
                            'skill_method': 'progressive',
                            'error': str(e)
                        }
                else:
                    # Non-rate-limit error
                    print(f"  API Error (turn {turn + 1}): {str(e)}")
                    loaded_files_unique = _deduplicate_preserve_order(loaded_files_raw)
                    return None, {
                        'loaded_files': loaded_files_unique,
                        'loaded_files_raw': loaded_files_raw,
                        'turns': turn + 1,
                        'tool_calls': len(loaded_files_raw) - 1,
                        'unique_files': len(loaded_files_unique) - 1,
                        'tool_call_sequence': tool_call_sequence,
                        'skill_method': 'progressive',
                        'error': str(e)
                    }

        if response is None:
            # This shouldn't happen, but just in case
            continue

        # Model wants to call tool(s)
        if response.stop_reason == "tool_use":
            tool_use_blocks = [
                b for b in response.content
                if hasattr(b, 'type') and b.type == "tool_use"
            ]

            if tool_use_blocks:
                tool_results = []
                for block in tool_use_blocks:
                    file_name = block.input.get("file", "")
                    reason = block.input.get("reason", "")

                    # Always record in sequence (for refinement analysis)
                    tool_call_sequence.append({
                        'turn': turn + 1,
                        'file': file_name,
                        'reason': reason,
                        'is_duplicate': file_name in loaded_files_raw
                    })

                    # Load content (even for duplicates - model might need it again)
                    content = load_skill_file_content(skill_dir, file_name)
                    loaded_files_raw.append(file_name)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": content
                    })

                # Feed tool results back
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                continue

        # Final answer - extract text
        response_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text

        # Deduplicate loaded_files for evidence attribution
        loaded_files_unique = _deduplicate_preserve_order(loaded_files_raw)

        return response_text, {
            'loaded_files': loaded_files_unique,  # Deduplicated
            'loaded_files_raw': loaded_files_raw,  # With duplicates
            'turns': turn + 1,
            'tool_calls': len(loaded_files_raw) - 1,  # Total calls
            'unique_files': len(loaded_files_unique) - 1,  # Unique files (excl SKILL.md)
            'tool_call_sequence': tool_call_sequence,  # Full sequence with reasons
            'skill_method': 'progressive'
        }

    # Max turns reached - extract whatever text we have
    response_text = ""
    if response and response.content:
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text

    loaded_files_unique = _deduplicate_preserve_order(loaded_files_raw)
    return response_text, {
        'loaded_files': loaded_files_unique,
        'loaded_files_raw': loaded_files_raw,
        'turns': max_turns,
        'tool_calls': len(loaded_files_raw) - 1,
        'unique_files': len(loaded_files_unique) - 1,
        'tool_call_sequence': tool_call_sequence,
        'skill_method': 'progressive'
    }


def _deduplicate_preserve_order(items: List[str]) -> List[str]:
    """Deduplicate a list while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def determine_skill_method(gen_model: str, requested_method: str = None) -> str:
    """Determine the skill loading method based on model and user preference.

    Progressive loading requires Claude (tool_use support).
    Falls back to LLM-based routing for non-Claude models.

    Args:
        gen_model: Generation model name (e.g., "claude-3-5-haiku-20241022", "qwen-max")
        requested_method: User-requested method ("progressive", "router", or None for auto)

    Returns:
        "progressive" or "router"
    """
    is_claude = gen_model.lower().startswith("claude")

    # If user explicitly requests a method
    if requested_method:
        method = requested_method.lower()
        if method == "progressive":
            if not is_claude:
                print(f"Warning: progressive method requires Claude model, "
                      f"but got {gen_model}. Falling back to router.")
                return "router"
            return "progressive"
        elif method == "router":
            return "router"
        else:
            print(f"Warning: Unknown SKILL_METHOD={method}. Using auto-detection.")

    # Auto-detect: progressive for Claude, router for others
    if is_claude:
        return "progressive"
    else:
        return "router"


# ============================================================
# Main (test)
# ============================================================


def main():
    """Test the skills router."""
    import sys

    skill_dir = sys.argv[1] if len(sys.argv) > 1 \
        else ".claude/skills/famma-non-arithmetic-v1"

    print("=" * 70)
    print("Skills Router Test")
    print(f"Skill dir: {skill_dir}")
    print(f"Router model: {get_router_model()}")
    print("=" * 70)

    router = SkillsRouter(skill_dir)

    # Show parsed index
    print(f"\nParsed index ({len(router.file_index)} entries):")
    for entry in router.file_index:
        print(f"  {entry.path} | {entry.subfield} | {entry.error_type} "
              f"| {len(entry.keywords)} keywords")

    # Test 1: Rule-based — portfolio management
    print("\n" + "-" * 70)
    print("Test 1: Rule-based — portfolio management")
    print("-" * 70)
    content = router.route_rule_based(
        question="Which portfolio dominates under mean-variance framework?",
        subfield="portfolio management"
    )
    print(f"Content length: {len(content)} chars")

    # Test 2: Rule-based — unknown subfield
    print("\n" + "-" * 70)
    print("Test 2: Rule-based — unknown subfield")
    print("-" * 70)
    content = router.route_rule_based(
        question="What is the quantum tunneling effect?",
        subfield="quantum physics"
    )
    print(f"Content length: {len(content)} chars")

    # Test 3: Rule-based — question with visual evidence keywords
    print("\n" + "-" * 70)
    print("Test 3: Rule-based — equity with tabular data")
    print("-" * 70)
    content = router.route_rule_based(
        question="Based on the scatter plot, which fund has the highest R-squared?",
        subfield="equity"
    )
    print(f"Content length: {len(content)} chars")

    # Test 4: LLM-based
    print("\n" + "-" * 70)
    print("Test 4: LLM-based — derivatives question")
    print("-" * 70)
    content = router.route_llm_based(
        question="What is the correct way to adjust portfolio beta using futures?",
        context="Current beta: 1.2, Target beta: 0.8, Futures beta: 1.0",
        subfield="derivatives"
    )
    print(f"Content length: {len(content)} chars")

    print("\n" + "=" * 70)
    print("Tests complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
