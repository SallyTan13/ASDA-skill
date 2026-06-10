"""
Failure Signature Analysis for Non-Arithmetic Questions

This script analyzes failures from baseline evaluation results and generates:
1. Failure signatures for each failed sample using LLM (Sonnet 4.5)
2. Clusters of similar failures for skill development

Based on docs/cases_analysis.md specifications.
"""

import os
import json
import argparse
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm
import pandas as pd
import pyarrow.parquet as pq

# Import prompts and taxonomy from separate file for easy modification
from signature_prompts import get_error_taxonomy, get_signature_prompt

# Import token tracker
from token_tracker import tracker as token_tracker

# Load environment variables (for API keys only)
load_dotenv()


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Failure Signature Analysis for FAMMA Questions"
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to YAML configuration file'
    )
    return parser.parse_args()


# Parse arguments and load config
args = parse_args()
config = load_config(args.config)

# Extract configuration values
INPUT_DIR = config['input']['results_dir']
OUTPUT_DIR = config['output']['dir']
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "signature_checkpoint.json")
CLUSTERING_METHOD = config['clustering']['method']
FAMMA_DATASET_PATH = config['input']['famma_dataset']
SPLITS_TO_ANALYZE = config['input']['splits']

# PoT mode (determines if error type 10 "code execution error" is included)
POT_MODE = config['input'].get('pot_mode', False)

# Checkpoint settings
CHECKPOINT_ENABLED = config['checkpoint']['enabled']
CHECKPOINT_INTERVAL = config['checkpoint']['interval']

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get error taxonomy and signature prompt based on PoT mode
ERROR_TAXONOMY = get_error_taxonomy(pot_mode=POT_MODE)
SIGNATURE_PROMPT = get_signature_prompt(pot_mode=POT_MODE)

print(f"PoT Mode: {'enabled' if POT_MODE else 'disabled'}")
print(f"Error taxonomy: Types 1-{len(ERROR_TAXONOMY)} ({'includes' if POT_MODE else 'excludes'} code execution error)")

# Load subfield and options mapping from FAMMA dataset
SUBFIELD_MAPPING = {}
OPTIONS_MAPPING = {}
try:
    if os.path.exists(FAMMA_DATASET_PATH):
        df = pd.read_parquet(FAMMA_DATASET_PATH)
        # Create mappings: question_id -> subfield, question_id -> options
        for _, row in df.iterrows():
            question_id = row['question_id']
            subfield = row.get('subfield', 'unknown')
            SUBFIELD_MAPPING[question_id] = subfield
            # Store options for multiple-choice questions
            options = row.get('options', None)
            if options is not None and len(options) > 0:
                OPTIONS_MAPPING[question_id] = list(options)
        print(f"Loaded {len(SUBFIELD_MAPPING)} subfield mappings from FAMMA dataset")
        print(f"Loaded {len(OPTIONS_MAPPING)} options mappings for MC questions")
    else:
        print(f"Warning: FAMMA dataset not found at {FAMMA_DATASET_PATH}")
except Exception as e:
    print(f"Warning: Could not load subfield/options mapping: {e}")

# Setup API client based on config
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


def load_checkpoint() -> Dict[str, Any]:
    """Load checkpoint if exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {"processed_ids": [], "signatures": []}


def save_checkpoint(checkpoint: Dict[str, Any]):
    """Save checkpoint."""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)


def generate_failure_signature(sample: Dict[str, Any]) -> Dict[str, Any]:
    """Generate failure signature using LLM."""
    # Build options section for multiple-choice questions
    options_section = ""
    if sample.get('question_type') == 'multiple-choice':
        options = OPTIONS_MAPPING.get(sample['question_id'], [])
        if options:
            options_str = "\n".join(options)
            options_section = f"\n**Options:**\n{options_str}\n"

    # Build code execution status section for PoT mode
    code_status_section = ""
    if POT_MODE:
        code_success = sample.get('code_execution_success', False)
        code_status_section = f"\n**Code Execution Status:** {code_success}\n"

    prompt = SIGNATURE_PROMPT.format(
        context=sample.get('context', 'N/A'),
        question=sample['question'],
        options_section=options_section,
        ground_truth=sample['ground_truth'],
        generated_answer=sample['generated_answer'],
        generated_explanation=sample.get('generated_explanation', 'N/A'),
        code_status_section=code_status_section
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing financial reasoning failures. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        # Track token usage
        token_tracker.add_from_response("phase1", "signature_analysis", response, MODEL)

        response_text = response.choices[0].message.content.strip()

        # Extract JSON from code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # Try to parse JSON, handling extra text after JSON object
        try:
            signature = json.loads(response_text)
        except json.JSONDecodeError as e:
            # If "Extra data" error, extract just the first JSON object
            if "Extra data" in str(e):
                # Find the end of the JSON object by matching braces
                brace_count = 0
                in_string = False
                escape_next = False
                for i, char in enumerate(response_text):
                    if escape_next:
                        escape_next = False
                        continue
                    if char == '\\' and in_string:
                        escape_next = True
                        continue
                    if char == '"' and not escape_next:
                        in_string = not in_string
                        continue
                    if not in_string:
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                signature = json.loads(response_text[:i+1])
                                break
                else:
                    raise
            else:
                raise

        return signature

    except Exception as e:
        print(f"\nError generating signature for {sample['question_id']}: {e}")
        # Return a default signature
        return {
            "modality": "unknown",
            "error_type": 10,
            "error_detail": f"Error during analysis: {str(e)}",
            "required_ops": [],
            "root_cause": "Analysis failed"
        }


def analyze_failures(split: str = "val") -> List[Dict[str, Any]]:
    """Analyze failures for a given split."""

    # Load evaluation results (prefer merged file with generated_code and context)
    merged_file = os.path.join(INPUT_DIR, f"evaluation_results_{split}_merged.json")
    eval_file = os.path.join(INPUT_DIR, f"evaluation_results_{split}_final.json")
    
    # Try merged file first, fallback to original file
    if os.path.exists(merged_file):
        eval_file = merged_file
        print(f"Using merged file: {merged_file}")
    elif os.path.exists(eval_file):
        print(f"Using original file: {eval_file}")
    else:
        print(f"Evaluation file not found: {eval_file} or {merged_file}")
        return []

    with open(eval_file, 'r') as f:
        results = json.load(f)

    # Filter failures
    failures = [r for r in results if not r['is_correct']]
    print(f"\nFound {len(failures)} failures out of {len(results)} total questions in {split} split")

    # Load checkpoint
    checkpoint = load_checkpoint()
    processed_ids = set(checkpoint['processed_ids'])
    signatures = checkpoint['signatures']

    # Process failures
    for sample in tqdm(failures, desc=f"Generating signatures for {split}"):
        if sample['question_id'] in processed_ids:
            continue

        # Generate signature
        signature = generate_failure_signature(sample)

        # Get subfield and options from mapping (or from sample if available)
        subfield = sample.get('subfield', SUBFIELD_MAPPING.get(sample['question_id'], 'unknown'))
        options = sample.get('options', OPTIONS_MAPPING.get(sample['question_id'], []))

        # Combine with sample data (base fields)
        result = {
            "question_id": sample['question_id'],
            "question_type": sample['question_type'],
            "question": sample['question'],
            "options": options if sample['question_type'] == 'multiple-choice' else [],
            "context": sample.get('context', ''),
            "ground_truth": sample['ground_truth'],
            "generated_answer": sample['generated_answer'],
            "generated_explanation": sample.get('generated_explanation', ''),
            "subfield": subfield,
            "signature": signature,
            "split": split
        }

        # Include code-related fields only for PoT mode (arithmetic questions)
        if POT_MODE:
            result["generated_code"] = sample.get('generated_code', '')
            result["code_execution_success"] = sample.get('code_execution_success', False)

        signatures.append(result)
        processed_ids.add(sample['question_id'])

        # Save checkpoint based on config
        if CHECKPOINT_ENABLED and len(signatures) % CHECKPOINT_INTERVAL == 0:
            checkpoint['processed_ids'] = list(processed_ids)
            checkpoint['signatures'] = signatures
            save_checkpoint(checkpoint)

    # Final checkpoint save
    checkpoint['processed_ids'] = list(processed_ids)
    checkpoint['signatures'] = signatures
    save_checkpoint(checkpoint)

    return signatures


def cluster_by_signature(signatures: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Cluster failures by full signature (modality + error_type + ops)."""
    clusters = defaultdict(list)

    for sig in signatures:
        s = sig['signature']
        error_type = s.get('error_type', 10)
        # Include error_detail in key when error_type is 9 (others)
        error_detail = s.get('error_detail', '') if error_type == 9 else ''
        cluster_key = (
            s.get('modality', 'unknown'),
            error_type,
            error_detail,
            tuple(sorted(s.get('required_ops', [])))
        )
        clusters[cluster_key].append(sig)

    return dict(clusters)


def cluster_by_error_type(signatures: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Cluster failures by error type only."""
    clusters = defaultdict(list)

    for sig in signatures:
        s = sig['signature']
        error_type = s.get('error_type', 10)
        # Include error_detail in key when error_type is 9 (others)
        error_detail = s.get('error_detail', '') if error_type == 9 else ''
        cluster_key = (error_type, error_detail)
        clusters[cluster_key].append(sig)

    return dict(clusters)


def cluster_by_modality(signatures: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Cluster failures by modality only."""
    clusters = defaultdict(list)

    for sig in signatures:
        modality = sig['signature'].get('modality', 'unknown')
        cluster_key = (modality,)
        clusters[cluster_key].append(sig)

    return dict(clusters)


def cluster_by_statistics(signatures: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Cluster by subfield + error type (statistical grouping by domain and error)."""
    clusters = defaultdict(list)

    for sig in signatures:
        s = sig['signature']
        subfield = sig.get('subfield', 'unknown')
        error_type = s.get('error_type', 10)
        # Include error_detail in key when error_type is 9 (others)
        error_detail = s.get('error_detail', '') if error_type == 9 else ''
        cluster_key = (
            subfield,
            error_type,
            error_detail
        )
        clusters[cluster_key].append(sig)

    return dict(clusters)


def cluster_by_embedding(signatures: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Cluster using embeddings (requires sentence-transformers)."""
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.cluster import KMeans
        import numpy as np
    except ImportError:
        print("Warning: sentence-transformers not installed. Falling back to signature clustering.")
        print("Install with: pip install sentence-transformers scikit-learn")
        return cluster_by_signature(signatures)

    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Create text representations for clustering
    texts = []
    for sig in signatures:
        s = sig['signature']
        text = f"{sig['question']} {s.get('root_cause', '')} {s.get('error_detail', '')}"
        texts.append(text)

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Determine number of clusters (using square root heuristic)
    n_clusters = max(5, min(20, int(np.sqrt(len(signatures)))))
    print(f"Clustering into {n_clusters} groups...")

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)

    # Group by cluster label
    clusters = defaultdict(list)
    for sig, label in zip(signatures, cluster_labels):
        clusters[(f"cluster_{label}",)].append(sig)

    return dict(clusters)


def cluster_failures(signatures: List[Dict[str, Any]], method: str = "signature") -> Dict[str, List[Dict[str, Any]]]:
    """
    Cluster failures using the specified method.

    Available methods:
    - "signature": Full signature (modality + error_type + ops + constraints)
    - "error_type": Error type only
    - "modality": Modality only
    - "statistical": Subfield + error type (domain-specific error clustering)
    - "embedding": Embedding-based clustering using semantic similarity
    """
    clustering_functions = {
        "signature": cluster_by_signature,
        "error_type": cluster_by_error_type,
        "modality": cluster_by_modality,
        "statistical": cluster_by_statistics,
        "embedding": cluster_by_embedding
    }

    if method not in clustering_functions:
        print(f"Warning: Unknown clustering method '{method}'. Using 'signature' instead.")
        method = "signature"

    print(f"\nUsing clustering method: {method}")
    return clustering_functions[method](signatures)


def format_cluster_key(key: Tuple, method: str = "signature") -> str:
    """Format cluster key for display based on clustering method."""

    def get_error_display(error_type: int, error_detail: str = '') -> str:
        """Get error display string, using error_detail for type 9."""
        if error_type == 9 and error_detail:
            return f"{error_type}:{error_detail}"
        else:
            error_desc = ERROR_TAXONOMY.get(str(error_type), "Unknown")
            return f"{error_type}:{error_desc}"

    if method == "signature":
        # Full signature: (modality, error_type, error_detail, required_ops)
        modality, error_type, error_detail, required_ops = key
        error_display = get_error_display(error_type, error_detail)
        ops_str = ", ".join(required_ops) if required_ops else "none"
        return f"Modality={modality} | Error={error_display} | Ops=[{ops_str}]"

    elif method == "error_type":
        # Error type only: (error_type, error_detail)
        error_type, error_detail = key
        error_display = get_error_display(error_type, error_detail)
        return f"Error={error_display}"

    elif method == "modality":
        # Modality only: (modality,)
        modality = key[0]
        return f"Modality={modality}"

    elif method == "statistical":
        # Subfield + error type: (subfield, error_type, error_detail)
        subfield, error_type, error_detail = key
        error_display = get_error_display(error_type, error_detail)
        return f"Subfield={subfield} | Error={error_display}"

    elif method == "embedding":
        # Cluster label: (cluster_N,)
        return f"{key[0]}"

    else:
        return str(key)


def save_analysis_results(signatures: List[Dict[str, Any]], clusters: Dict, method: str = "statistical"):
    """Save analysis results to files."""

    # Save all signatures
    output_file = os.path.join(OUTPUT_DIR, "failure_signatures.json")
    with open(output_file, 'w') as f:
        json.dump(signatures, f, indent=2)
    print(f"\nSaved {len(signatures)} signatures to {output_file}")

    # Save clusters
    clusters_output = []
    for key, items in clusters.items():
        # Build sample list with conditional code-related fields
        samples = []
        for item in items:
            sample = {
                "question_id": item['question_id'],
                "question_type": item['question_type'],
                "question": item['question'],
                "context": item.get('context', ''),
                "options": item.get('options', []),
                "subfield": item.get('subfield', 'unknown'),
                "ground_truth": item['ground_truth'],
                "model_answer": item['generated_answer'],
                "model_explanation": item.get('generated_explanation', ''),
                "root_cause": item['signature'].get('root_cause', ''),
                "split": item['split']
            }
            # Include code execution status only for PoT mode
            if POT_MODE:
                sample["code_execution_success"] = item.get('code_execution_success', False)
            samples.append(sample)

        cluster_info = {
            "cluster_key": format_cluster_key(key, method),
            "count": len(items),
            "clustering_method": method,
            "samples": samples
        }

        # Add method-specific metadata
        if method == "signature":
            # Key: (modality, error_type, error_detail, required_ops)
            cluster_info["modality"] = key[0]
            cluster_info["error_type"] = key[1]
            cluster_info["error_detail"] = key[2]
            error_type = key[1]
            if error_type == 9 and key[2]:
                cluster_info["error_description"] = key[2]
            else:
                cluster_info["error_description"] = ERROR_TAXONOMY.get(str(error_type), "Unknown")
            cluster_info["required_ops"] = list(key[3])
        elif method == "statistical":
            # Key: (subfield, error_type, error_detail)
            cluster_info["subfield"] = key[0]
            cluster_info["error_type"] = key[1]
            cluster_info["error_detail"] = key[2]
            error_type = key[1]
            if error_type == 9 and key[2]:
                cluster_info["error_description"] = key[2]
            else:
                cluster_info["error_description"] = ERROR_TAXONOMY.get(str(error_type), "Unknown")
        elif method == "error_type":
            # Key: (error_type, error_detail)
            cluster_info["error_type"] = key[0]
            cluster_info["error_detail"] = key[1]
            error_type = key[0]
            if error_type == 9 and key[1]:
                cluster_info["error_description"] = key[1]
            else:
                cluster_info["error_description"] = ERROR_TAXONOMY.get(str(error_type), "Unknown")
        elif method == "modality":
            cluster_info["modality"] = key[0]
        elif method == "embedding":
            cluster_info["cluster_id"] = key[0]

        clusters_output.append(cluster_info)

    # Sort by cluster size
    clusters_output.sort(key=lambda x: x['count'], reverse=True)

    clusters_file = os.path.join(OUTPUT_DIR, "failure_clusters.json")
    with open(clusters_file, 'w') as f:
        json.dump(clusters_output, f, indent=2)
    print(f"Saved {len(clusters_output)} clusters to {clusters_file}")

    # Generate summary report
    generate_summary_report(signatures, clusters_output)


def generate_summary_report(signatures: List[Dict[str, Any]], clusters: List[Dict]):
    """Generate a human-readable summary report."""

    report = []
    report.append("# Failure Signature Analysis Report")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\nTotal Failures Analyzed: {len(signatures)}")
    report.append(f"Total Clusters: {len(clusters)}")

    # Statistics by error type
    report.append("\n## Error Type Distribution")
    error_counts = defaultdict(int)
    for sig in signatures:
        error_type = sig['signature'].get('error_type', 10)
        error_counts[error_type] += 1

    for error_type in sorted(error_counts.keys()):
        count = error_counts[error_type]
        desc = ERROR_TAXONOMY.get(str(error_type), "Unknown")
        pct = (count / len(signatures)) * 100
        report.append(f"- {error_type}. {desc}: {count} ({pct:.1f}%)")

    # Statistics by modality
    report.append("\n## Modality Distribution")
    modality_counts = defaultdict(int)
    for sig in signatures:
        modality = sig['signature'].get('modality', 'unknown')
        modality_counts[modality] += 1

    for modality, count in sorted(modality_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(signatures)) * 100
        report.append(f"- {modality}: {count} ({pct:.1f}%)")

    # Top clusters
    report.append("\n## Top 10 Failure Clusters")
    for i, cluster in enumerate(clusters[:10], 1):
        report.append(f"\n### {i}. {cluster['cluster_key']}")
        report.append(f"Count: {cluster['count']}")
        report.append("\nRepresentative samples:")
        for j, sample in enumerate(cluster['samples'][:3], 1):
            report.append(f"{j}. [{sample['question_id']}] {sample['question']}")
            report.append(f"   Root cause: {sample['root_cause']}")

    # Save report
    report_file = os.path.join(OUTPUT_DIR, "ANALYSIS_REPORT.md")
    with open(report_file, 'w') as f:
        f.write('\n'.join(report))
    print(f"\nSaved summary report to {report_file}")


def main():
    """Main execution function."""

    print("=" * 80)
    print("Failure Signature Analysis")
    print("=" * 80)
    print(f"Analysis: {config['analysis']['name']}")
    print(f"Model: {MODEL} ({provider})")
    print(f"Clustering Method: {CLUSTERING_METHOD}")
    print(f"Input Directory: {INPUT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Splits to analyze: {', '.join(SPLITS_TO_ANALYZE)}")
    print("=" * 80)

    # Analyze specified splits
    all_signatures = []
    for split in SPLITS_TO_ANALYZE:
        signatures = analyze_failures(split)
        all_signatures.extend(signatures)

    if not all_signatures:
        print("\nNo failures to analyze!")
        return

    # Cluster failures
    print("\nClustering failures...")
    clusters = cluster_failures(all_signatures, method=CLUSTERING_METHOD)
    print(f"Found {len(clusters)} distinct clusters")

    # Save results
    save_analysis_results(all_signatures, clusters, method=CLUSTERING_METHOD)

    # Print and save token usage
    token_tracker.summary(print_output=True)
    token_file = os.path.join(OUTPUT_DIR, "token_usage.json")
    token_tracker.save(token_file)

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
