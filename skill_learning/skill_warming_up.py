"""
Skill Warming Up V3 - Initial Skills Generation

Flow:
1. Generate common skills (cross-subfield patterns: visual evidence, constraints, format)
2. Generate subfield skills (domain-specific patterns by error type)
3. (Optional) Split skill files by semantic similarity - groups related patterns
4. Generate SKILL.md navigation file with File Index table

Split Strategy:
- Base split by file structure: common/{error_type}.md and {subfield}/{error_type}.md
- Optional semantic split: further divides files by pattern similarity
  e.g., portfolio_management/concept_confusion.md
      → portfolio_management/concept_confusion_risk_metrics.md
      → portfolio_management/concept_confusion_return_calc.md
- SKILL.md + load_skill_file enables progressive disclosure
- During learning phase, only content is refined (no re-splitting)

Configuration:
- ENABLE_SPLIT=true  → Enable semantic splitting (default: false)

Changes from V2:
- Added optional semantic split phase (ENABLE_SPLIT)
- Prompts separated to warming_up_prompts.py for easy modification
- Updated SKILL.md format with File Index table
- Full question/context/options passed (no truncation)

Reads failure_clusters.json and failure_signatures.json, generates:
1. Common skill files: {OUTPUT_DIR}/common/{error_type}.md
2. Subfield skill files: {OUTPUT_DIR}/{subfield}/{error_type}.md
3. (If split) Additional split files: {OUTPUT_DIR}/{subfield}/{error_type}_{group}.md
4. SKILL.md navigation: {OUTPUT_DIR}/SKILL.md
"""

import os
import json
import argparse
import yaml
import re
import time
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

# Import token tracker
try:
    from .token_tracker import tracker as token_tracker
except ImportError:
    from token_tracker import tracker as token_tracker

# Import prompts from separate file
try:
    from .warming_up_prompts import (
        ERROR_TYPE_NAMES,
        ERROR_TYPE_DESCRIPTIONS,
        COMMON_ERROR_TYPES,
        SKILL_GEN_PROMPT,
        REFINEMENT_PROMPT,
        REFINEMENT_PROMPT_PoT,
        SPLIT_PROMPT,
        SKILL_MD_PROMPT,
        SKILL_MD_PROMPT_PoT,
        format_file_inventory,
        get_skill_gen_prompt
    )
except ImportError:
    from warming_up_prompts import (
        ERROR_TYPE_NAMES,
        ERROR_TYPE_DESCRIPTIONS,
        COMMON_ERROR_TYPES,
        SKILL_GEN_PROMPT,
        REFINEMENT_PROMPT,
        REFINEMENT_PROMPT_PoT,
        SPLIT_PROMPT,
        SKILL_MD_PROMPT,
        SKILL_MD_PROMPT_PoT,
        format_file_inventory,
        get_skill_gen_prompt
    )

# Load environment variables (for API keys only)
load_dotenv()


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Skill Warming Up - Initial Skills Generation from Failure Clusters"
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to YAML configuration file'
    )
    return parser.parse_args()


# ============================================================
# Configuration defaults (for import compatibility)
# ============================================================
# When imported as a module, these defaults are used.
# When run as main, they are overwritten in init_config().

args = None
config = {}
CLUSTERS_FILE = None
SIGNATURES_FILE = None
OUTPUT_DIR = None
CHECKPOINT_FILE = None
BATCH_SIZE = 5
MAX_BATCHES = None
STABILITY_THRESHOLD = 0.75
MIN_CLUSTER_SIZE = 1
SKILL_MD_LINE_BUDGET = 200
COMMON_LINE_BUDGET = 300
SUBFIELD_LINE_BUDGET = 400
ENABLE_SPLIT = False
POT_MODE = False
MODEL = None
TEMPERATURE = 0.3
MAX_TOKENS = 20480
client = None
provider = None


def init_config():
    """Initialize configuration from command line. Called only when run as main."""
    global args, config, CLUSTERS_FILE, SIGNATURES_FILE, OUTPUT_DIR, CHECKPOINT_FILE
    global BATCH_SIZE, MAX_BATCHES, STABILITY_THRESHOLD, MIN_CLUSTER_SIZE
    global SKILL_MD_LINE_BUDGET, COMMON_LINE_BUDGET, SUBFIELD_LINE_BUDGET
    global ENABLE_SPLIT, POT_MODE, MODEL, TEMPERATURE, MAX_TOKENS, client, provider

    # Parse arguments and load config
    args = parse_args()
    config = load_config(args.config)

    # Extract configuration values
    CLUSTERS_FILE = config['input']['clusters_file']
    SIGNATURES_FILE = config['input']['signatures_file']
    OUTPUT_DIR = config['output']['dir']

    # Make checkpoint file unique per output directory
    checkpoint_dir = config['checkpoint']['dir']
    output_dir_name = os.path.basename(OUTPUT_DIR.rstrip('/'))
    CHECKPOINT_FILE = os.path.join(checkpoint_dir, f'warming_up_{output_dir_name}.json')

    # Batch processing settings
    BATCH_SIZE = config['batch']['size']
    MAX_BATCHES = config['batch']['max_batches']
    STABILITY_THRESHOLD = config['batch']['stability_threshold']
    MIN_CLUSTER_SIZE = config['batch']['min_cluster_size']

    # Line budgets (advisory)
    SKILL_MD_LINE_BUDGET = config['line_budget']['skill_md']
    COMMON_LINE_BUDGET = config['line_budget']['common']
    SUBFIELD_LINE_BUDGET = config['line_budget']['subfield']

    # Feature flags
    ENABLE_SPLIT = config['features']['enable_split']

    # PoT mode
    POT_MODE = config['input'].get('pot_mode', False)
    os.environ['POT_MODE'] = 'true' if POT_MODE else 'false'

    # Model configuration
    MODEL = config['model']['name']
    TEMPERATURE = config['model']['temperature']
    MAX_TOKENS = config['model']['max_tokens']

    # Setup API client based on provider field (or auto-detect from model name)
    config_provider = config['model'].get('provider', 'auto')

    if config_provider == 'openrouter':
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        provider = "OpenRouter"
    elif config_provider == 'anthropic' or (config_provider == 'auto' and MODEL.lower().startswith('claude')):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        client = OpenAI(api_key=api_key, base_url="https://api.anthropic.com/v1")
        provider = "Anthropic"
    elif config_provider == 'dashscope' or (config_provider == 'auto' and MODEL.lower().startswith('qwen')):
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY not found in environment variables")
        base_url = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        client = OpenAI(api_key=api_key, base_url=base_url)
        provider = "DashScope"
    else:
        raise ValueError(f"Unsupported provider '{config_provider}' or model '{MODEL}'")

    print(f"Using {provider} API with model: {MODEL}")


# ============================================================
# Utility Functions
# ============================================================

def count_lines(text: str) -> int:
    """Count lines in text."""
    if not text:
        return 0
    return len(text.strip().split('\n'))


def call_llm(prompt: str, max_tokens: int = None, track_component: str = "skill_generation") -> str:
    """Call LLM with retry logic."""
    if max_tokens is None:
        max_tokens = MAX_TOKENS

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=TEMPERATURE
            )
            # Track token usage
            token_tracker.add_from_response("phase2", track_component, response, MODEL)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  LLM call failed (attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
    return ""


def extract_pattern_names(content: str) -> list:
    """Extract pattern names from skill file content.

    Returns list of pattern names (not full summaries).

    Supports all header formats:
    - # Pattern: Name
    - # Pattern 1: Name
    - ## Pattern: Name
    - ## Pattern 1: Name
    - ### Pattern Name   (no colon)
    - ### Pattern 1: Name
    """
    if not content:
        return []

    # Single regex: 1–3 #, optional " N", then either ": Name" or " Name" (no colon)
    # (?m) = multiline so ^/$ match per line
    patterns = re.findall(
        r'(?m)^#+\s*Pattern(?:\s+\d+)?(?::\s*|\s+)(.+)$',
        content
    )
    pattern_names = [p.strip() for p in patterns]

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for name in pattern_names:
        if name and name not in seen:
            seen.add(name)
            unique.append(name)

    return unique


def extract_pattern_summaries(content: str) -> str:
    """Extract compact summaries of existing patterns from skill file content.

    Returns a compact list for refinement prompts.
    """
    summaries = []
    parts = re.split(r'(##\s+Pattern(?:\s+\d+)?:\s*.+)', content)

    i = 1
    while i < len(parts):
        header = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""

        name_match = re.search(r'##\s+Pattern(?:\s+\d+)?:\s*(.+)', header)
        name = name_match.group(1).strip() if name_match else "Unknown"

        description = ""
        when_to_use = ""
        for line in body.split('\n'):
            line_stripped = line.strip()
            if line_stripped.startswith('**Description:**'):
                description = line_stripped.replace('**Description:**', '').strip()
            elif line_stripped.startswith('**When to Use:**'):
                when_to_use = line_stripped.replace('**When to Use:**', '').strip()

        summary = f"- {name}"
        if description:
            summary += f" | Description: {description}"
        if when_to_use:
            summary += f" | Trigger: {when_to_use}"
        summaries.append(summary)
        i += 2

    return "\n".join(summaries) if summaries else "No patterns yet"


# ============================================================
# Data Loading
# ============================================================

def load_data() -> tuple:
    """Load failure clusters and full signatures."""
    with open(CLUSTERS_FILE, 'r') as f:
        clusters = json.load(f)

    with open(SIGNATURES_FILE, 'r') as f:
        signatures = json.load(f)

    # Build question_id -> full record lookup
    sig_lookup = {}
    for sig in signatures:
        sig_lookup[sig['question_id']] = sig

    print(f"Loaded {len(clusters)} clusters, {len(signatures)} signatures")
    return clusters, sig_lookup


def format_cases_for_prompt(question_ids: list, sig_lookup: dict) -> str:
    """Format failure cases for LLM prompt.

    Includes FULL question, context, and options (no truncation).
    """
    cases_text = []
    for i, qid in enumerate(question_ids, 1):
        sig = sig_lookup.get(qid)
        if not sig:
            continue

        # Build options section for MC questions (FULL options)
        options_str = ""
        if sig.get('question_type') == 'multiple-choice' and sig.get('options'):
            if isinstance(sig['options'], list):
                options_str = f"\n- Options: {', '.join(sig['options'])}"
            else:
                options_str = f"\n- Options: {sig['options']}"

        # FULL context and question (no truncation)
        context = sig.get('context', '') or 'N/A'
        question = sig.get('question', '') or 'N/A'
        explanation = sig.get('generated_explanation', '') or 'N/A'
        root_cause = sig.get('signature', {}).get('root_cause', 'N/A')

        case = f"""---
Case {i}:
- Question: {question}{options_str}
- Context: {context}
- Model's Wrong Answer: {sig.get('generated_answer', 'N/A')}
- Model's Explanation: {explanation}
- Ground Truth: {sig.get('ground_truth', 'N/A')}
- Root Cause: {root_cause}
---"""
        cases_text.append(case)

    return "\n".join(cases_text)


# ============================================================
# Cluster Routing
# ============================================================

def route_clusters(clusters: list) -> tuple:
    """Route clusters to common/ or {subfield}/ based on error type.

    Returns: (common_groups, subfield_groups)
    """
    common_groups = defaultdict(list)
    subfield_groups = defaultdict(list)

    # Default error_type=9 when missing; type 10 only exists in PoT mode (see signature_prompts).
    for cluster in clusters:
        error_type = cluster.get('error_type', 9)

        if error_type in COMMON_ERROR_TYPES:
            common_groups[error_type].append(cluster)
        else:
            if cluster['count'] >= MIN_CLUSTER_SIZE:
                subfield = cluster.get('subfield', 'unknown')
                subfield_groups[(subfield, error_type)].append(cluster)

    # Filter common groups by minimum size
    filtered_common = {}
    for error_type, group_clusters in common_groups.items():
        total = sum(c['count'] for c in group_clusters)
        if total >= MIN_CLUSTER_SIZE:
            filtered_common[error_type] = group_clusters

    skipped_subfield = sum(
        1 for c in clusters
        if c.get('error_type', 9) not in COMMON_ERROR_TYPES
        and c['count'] < MIN_CLUSTER_SIZE
    )

    print(f"\nRouting summary:")
    print(f"  Common groups: {len(filtered_common)}")
    print(f"  Subfield groups: {len(subfield_groups)}")
    print(f"  Skipped (count < {MIN_CLUSTER_SIZE}): {skipped_subfield} clusters")

    return filtered_common, subfield_groups


# ============================================================
# Skill File Generation
# ============================================================

def generate_skill_file(
    file_key: str,
    clusters: list,
    sig_lookup: dict,
    subfield: str,
    error_type: int,
    line_budget: int
) -> tuple:
    """Generate a skill file from clusters.

    Returns: (content, metadata)
    """
    error_name = ERROR_TYPE_NAMES.get(error_type, "unknown")
    error_desc = ERROR_TYPE_DESCRIPTIONS.get(error_type, "Unknown error type")

    # Collect all question IDs from clusters
    all_qids = []
    for cluster in clusters:
        for sample in cluster['samples']:
            all_qids.append(sample['question_id'])

    unique_qids = list(dict.fromkeys(all_qids))  # Preserve order, dedupe

    print(f"\n  Processing {file_key}: {len(unique_qids)} cases")

    # Process in batches
    content = ""
    batch_count = 0
    stability_count = 0

    for batch_start in range(0, len(unique_qids), BATCH_SIZE):
        if batch_count >= MAX_BATCHES:
            print(f"    Max batches ({MAX_BATCHES}) reached")
            break
        if stability_count >= STABILITY_THRESHOLD:
            print(f"    Stability threshold reached ({STABILITY_THRESHOLD} batches with no changes)")
            break

        batch_qids = unique_qids[batch_start:batch_start + BATCH_SIZE]
        batch_count += 1

        cases_text = format_cases_for_prompt(batch_qids, sig_lookup)

        if batch_count == 1:
            # First batch: generate initial content
            # Use PoT-specific prompt for error_type=10, standard prompt otherwise
            prompt = get_skill_gen_prompt(error_type).format(
                subfield=subfield,
                error_type=error_name,
                error_description=error_desc,
                cases_text=cases_text
            )
        else:
            # Subsequent batches: refine (use PoT refinement when error_type=10 or POT_MODE)
            pattern_summaries = extract_pattern_summaries(content)
            use_pot = (os.getenv("POT_MODE", "false").lower() == "true") or (error_type == 10)
            refinement_prompt = REFINEMENT_PROMPT_PoT if use_pot else REFINEMENT_PROMPT
            prompt = refinement_prompt.format(
                subfield=subfield,
                error_type=error_name,
                pattern_summaries=pattern_summaries,
                batch_num=batch_count,
                cases_text=cases_text
            )

        response = call_llm(prompt, max_tokens=8192)

        if batch_count == 1:
            content = response
            print(f"    Batch {batch_count}: Initial generation ({count_lines(content)} lines)")
        else:
            if has_changes(response):
                content, n_refined, n_new = apply_changes(content, response)
                print(f"    Batch {batch_count}: +{n_new} new, ~{n_refined} refined")
                stability_count = 0
            else:
                stability_count += 1
                print(f"    Batch {batch_count}: No changes (stability: {stability_count})")

    # Extract pattern names for File Index
    pattern_names = extract_pattern_names(content)

    # Build metadata
    metadata = {
        "file_key": file_key,
        "subfield": subfield,
        "error_type": error_type,
        "error_name": error_name,
        "error_description": error_desc,
        "case_count": len(unique_qids),
        "batch_count": batch_count,
        "line_count": count_lines(content),
        "pattern_names": pattern_names,  # List of pattern names for File Index
        "pattern_summaries": extract_pattern_summaries(content)
    }

    return content, metadata


def has_changes(response: str) -> bool:
    """Check if LLM response contains new or refined patterns."""
    if not response or not response.strip():
        return False
    if "NO_CHANGES" in response or "NO_NEW_PATTERNS" in response:
        return False
    if len(response.strip()) < 50:
        return False
    if ("## REFINED Pattern" in response
            or "## NEW Pattern" in response
            or "## Pattern" in response):
        return True
    return False


def apply_changes(content: str, response: str) -> tuple:
    """Apply REFINED and NEW patterns from response to content."""
    n_refined = 0
    n_new = 0

    sections = re.split(r'(## (?:REFINED|NEW) Pattern:\s*.+)', response)

    i = 1
    while i < len(sections):
        header = sections[i].strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        i += 2

        if not body:
            continue

        if header.startswith('## REFINED Pattern:'):
            pattern_name = header.replace('## REFINED Pattern:', '').strip()
            replacement = f"## Pattern: {pattern_name}\n\n{body}"

            # Find and replace matching pattern
            pattern_regex = re.compile(
                rf'## Pattern(?:\s+\d+)?:\s*{re.escape(pattern_name)}.*?(?=\n## |\Z)',
                re.DOTALL
            )
            if pattern_regex.search(content):
                # Use lambda to avoid interpreting backslashes in replacement text
                content = pattern_regex.sub(lambda m: replacement, content, count=1)
                n_refined += 1
            else:
                # Pattern not found, append as new
                content = content.rstrip() + "\n\n" + replacement
                n_new += 1

        elif header.startswith('## NEW Pattern:'):
            pattern_name = header.replace('## NEW Pattern:', '').strip()
            new_pattern = f"## Pattern: {pattern_name}\n\n{body}"
            content = content.rstrip() + "\n\n" + new_pattern
            n_new += 1

    return content, n_refined, n_new


# ============================================================
# Skill File Splitting (Optional)
# ============================================================

def split_skill_file(file_info: dict) -> list:
    """Split a skill file into multiple files by semantic similarity.

    Args:
        file_info: Dict with keys: rel_path, content, subfield, error_name, etc.

    Returns:
        List of new file_info dicts (or original if no split needed)
    """
    content = file_info.get('content', '')
    if not content:
        return [file_info]

    # Count patterns - if ≤3, likely no split needed
    pattern_names = extract_pattern_names(content)
    if len(pattern_names) <= 3:
        print(f"    {file_info['rel_path']}: {len(pattern_names)} patterns, skipping split")
        return [file_info]

    prompt = SPLIT_PROMPT.format(
        file_path=file_info['rel_path'],
        subfield=file_info.get('subfield', 'unknown'),
        error_type=file_info.get('error_name', 'unknown'),
        content=content
    )

    response = call_llm(prompt, max_tokens=8192)

    if not response or "NO_SPLIT" in response:
        print(f"    {file_info['rel_path']}: No split needed")
        return [file_info]

    # Parse split groups
    split_files = parse_split_response(response, file_info)

    if len(split_files) <= 1:
        print(f"    {file_info['rel_path']}: Split returned single group, keeping original")
        return [file_info]

    print(f"    {file_info['rel_path']}: Split into {len(split_files)} files")
    return split_files


def parse_split_response(response: str, original_info: dict) -> list:
    """Parse LLM split response into file info dicts."""
    split_files = []

    # Extract base path (remove .md extension)
    base_path = original_info['rel_path'].replace('.md', '')

    # Split by group headers
    groups = re.split(r'## SPLIT_GROUP:\s*', response)

    for group in groups[1:]:  # Skip first empty part
        lines = group.strip().split('\n')
        if not lines:
            continue

        # First line is group name
        group_name = lines[0].strip().lower().replace(' ', '_')

        # Find content after **Patterns:** or just take everything after topic
        content_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('**Patterns:**'):
                content_start = i + 1
                break
            elif line.strip().startswith('## Pattern'):
                content_start = i
                break

        group_content = '\n'.join(lines[content_start:]).strip()

        if not group_content:
            continue

        # Create new file info
        new_path = f"{base_path}_{group_name}.md"
        new_info = original_info.copy()
        new_info['rel_path'] = new_path
        new_info['content'] = group_content
        new_info['pattern_names'] = extract_pattern_names(group_content)
        new_info['line_count'] = count_lines(group_content)
        new_info['split_group'] = group_name

        split_files.append(new_info)

    return split_files


# ============================================================
# SKILL.md Navigation Generation (V3 - Updated Format)
# ============================================================

def generate_skill_md(generated_files: list) -> str:
    """Generate SKILL.md navigation file using LLM.

    V3: Uses File Index table format with pattern names.
    """
    # Build file inventory for the prompt
    file_info_list = []
    for f in generated_files:
        file_info_list.append({
            "file_path": f['rel_path'],
            "subfield": f['subfield'],
            "error_type": f['error_name'],
            "patterns": f.get('pattern_names', []),
            "case_count": f['case_count']
        })

    file_inventory = format_file_inventory(file_info_list)

    # Use PoT SKILL.md template when any file is error_type=10 (arithmetic/code) or POT_MODE
    use_pot = (os.getenv("POT_MODE", "false").lower() == "true") or any(
        f.get("error_type") == 10 for f in generated_files
    )
    skill_md_prompt = SKILL_MD_PROMPT_PoT if use_pot else SKILL_MD_PROMPT
    prompt = skill_md_prompt.format(file_inventory=file_inventory)
    response = call_llm(prompt, max_tokens=8192)

    if not response:
        print("  WARNING: SKILL.md generation returned empty response")
        return None

    return response


def validate_and_repair_skill_md(skill_md_content: str, generated_files: list, output_dir: str) -> str:
    """Validate SKILL.md lists all generated files; add missing rows if needed.

    Uses shared logic from skill_md_validator.py (same as scripts/repair_skill_md.py).

    Args:
        skill_md_content: Current SKILL.md content
        generated_files: List of dicts with 'rel_path', 'subfield', 'error_name' etc.
        output_dir: Directory where skill files are saved

    Returns:
        Updated SKILL.md content (also re-saved to disk if changes were made)
    """
    from skill_learning.skill_md_validator import validate_and_repair

    expected = {f['rel_path'] for f in generated_files}
    file_metadata_lookup = {f['rel_path']: f for f in generated_files}

    updated_content, missing = validate_and_repair(
        skill_md_content, expected, output_dir, file_metadata_lookup
    )

    if not missing:
        print(f"  SKILL.md validation: OK ({len(expected)} files listed)")
        return skill_md_content

    print(f"  SKILL.md validation: {len(missing)} files missing from table!")
    for rel_path in missing:
        print(f"    + {rel_path}")

    # Re-save
    save_skill_file("SKILL.md", updated_content)
    print(f"  SKILL.md repaired: added {len(missing)} missing entries")

    return updated_content


# ============================================================
# File Saving
# ============================================================

def save_skill_file(rel_path: str, content: str) -> None:
    """Save skill file to disk."""
    full_path = Path(OUTPUT_DIR) / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, 'w') as f:
        f.write(content)

    print(f"    Saved: {rel_path} ({count_lines(content)} lines)")


def save_checkpoint(data: dict) -> None:
    """Save checkpoint to disk."""
    Path(CHECKPOINT_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_checkpoint() -> dict:
    """Load checkpoint if exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {"processed_files": [], "generated_files": []}


# ============================================================
# Main
# ============================================================

def main():
    """Main execution flow."""
    print("=" * 70)
    print("Skill Warming Up — Initial Skills Generation")
    print("=" * 70)
    print(f"Name: {config['warming_up']['name']}")
    print(f"Description: {config['warming_up']['description']}")
    print(f"Model: {MODEL} ({provider})")
    print(f"Input: {CLUSTERS_FILE}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Batch size: {BATCH_SIZE}, Max batches: {MAX_BATCHES}")
    print(f"Min cluster size: {MIN_CLUSTER_SIZE}")
    print(f"Split by similarity: {'enabled' if ENABLE_SPLIT else 'disabled'}")
    print(f"PoT mode: {'enabled' if POT_MODE else 'disabled'}")
    print("=" * 70)

    # Load data
    clusters, sig_lookup = load_data()

    # Route clusters
    common_groups, subfield_groups = route_clusters(clusters)

    # Load checkpoint
    checkpoint = load_checkpoint()
    processed_files = set(checkpoint.get('processed_files', []))
    generated_files = checkpoint.get('generated_files', [])

    # Phase 1: Generate common/ skill files
    print("\n" + "=" * 70)
    print("Phase 1: Generating common/ skill files")
    print("=" * 70)

    for error_type, group_clusters in common_groups.items():
        error_name = ERROR_TYPE_NAMES.get(error_type, "unknown")
        file_key = f"common/{error_name}.md"

        if file_key in processed_files:
            print(f"  Skipping {file_key} (already processed)")
            continue

        content, metadata = generate_skill_file(
            file_key=file_key,
            clusters=group_clusters,
            sig_lookup=sig_lookup,
            subfield="Cross-subfield",
            error_type=error_type,
            line_budget=COMMON_LINE_BUDGET
        )

        if content:
            save_skill_file(file_key, content)
            metadata['rel_path'] = file_key
            metadata['content'] = content  # Store for potential split
            generated_files.append(metadata)
            processed_files.add(file_key)
            save_checkpoint({
                "processed_files": list(processed_files),
                "generated_files": [{k: v for k, v in f.items() if k != 'content'} for f in generated_files]
            })

    # Phase 2: Generate {subfield}/ skill files
    print("\n" + "=" * 70)
    print("Phase 2: Generating subfield/ skill files")
    print("=" * 70)

    for (subfield, error_type), group_clusters in subfield_groups.items():
        subfield_clean = subfield.replace(" ", "_").lower()
        error_name = ERROR_TYPE_NAMES.get(error_type, "unknown")
        file_key = f"{subfield_clean}/{error_name}.md"

        if file_key in processed_files:
            print(f"  Skipping {file_key} (already processed)")
            continue

        content, metadata = generate_skill_file(
            file_key=file_key,
            clusters=group_clusters,
            sig_lookup=sig_lookup,
            subfield=subfield,
            error_type=error_type,
            line_budget=SUBFIELD_LINE_BUDGET
        )

        if content:
            save_skill_file(file_key, content)
            metadata['rel_path'] = file_key
            metadata['content'] = content  # Store for potential split
            generated_files.append(metadata)
            processed_files.add(file_key)
            save_checkpoint({
                "processed_files": list(processed_files),
                "generated_files": [{k: v for k, v in f.items() if k != 'content'} for f in generated_files]
            })

    # Phase 3 (Optional): Split skill files by semantic similarity
    if ENABLE_SPLIT:
        print("\n" + "=" * 70)
        print("Phase 3: Splitting skill files by semantic similarity")
        print("=" * 70)

        final_files = []
        for file_info in generated_files:
            split_results = split_skill_file(file_info)

            for split_file in split_results:
                # Save split files (may be same as original if no split)
                if split_file.get('split_group'):
                    # This is a new split file, save it
                    save_skill_file(split_file['rel_path'], split_file['content'])

                final_files.append(split_file)

        generated_files = final_files
        print(f"\n  After split: {len(generated_files)} skill files")
    else:
        print("\n  Split disabled (set ENABLE_SPLIT=true to enable)")

    # Phase 4: Generate SKILL.md
    print("\n" + "=" * 70)
    print("Phase 4: Generating SKILL.md navigation file")
    print("=" * 70)

    skill_md_content = generate_skill_md(generated_files)
    if skill_md_content:
        save_skill_file("SKILL.md", skill_md_content)

        # Post-hoc validation: ensure all generated files appear in SKILL.md
        skill_md_content = validate_and_repair_skill_md(
            skill_md_content, generated_files, OUTPUT_DIR
        )

    # Print and save token usage
    token_tracker.summary(print_output=True)
    token_file = os.path.join(OUTPUT_DIR, "token_usage.json")
    token_tracker.save(token_file)

    print("\n" + "=" * 70)
    print("Skill Warming Up V3 Complete!")
    print(f"Generated {len(generated_files)} skill files")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    init_config()
    main()
