"""
Token Usage Tracker for ASDA Pipeline

Tracks token usage across all phases and components:
- Phase 1: Failure Analysis (clustering LLM calls)
- Phase 2: Skill Generation (teacher model)
- Phase 3: Evaluation (router, generation, selection, evaluation)

Usage:
    from skill_learning.token_tracker import tracker, track_usage

    # Option 1: Manual tracking
    tracker.add("phase3", "generation", input_tokens=500, output_tokens=200, model="haiku-4.5")

    # Option 2: Decorator for functions that return API responses
    @track_usage("phase3", "router")
    def call_router(...):
        return client.chat.completions.create(...)

    # Get summary
    tracker.summary()
    tracker.save("token_usage.json")
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from functools import wraps


@dataclass
class TokenUsage:
    """Token usage for a single API call."""
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    timestamp: str = ""

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class ComponentUsage:
    """Aggregated token usage for a component (e.g., router, generation)."""
    input_tokens: int = 0
    output_tokens: int = 0
    call_count: int = 0
    models: Dict[str, int] = field(default_factory=dict)  # model -> call count

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

    def add(self, input_tokens: int, output_tokens: int, model: str = ""):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.call_count += 1
        if model:
            self.models[model] = self.models.get(model, 0) + 1

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total,
            "call_count": self.call_count,
            "models": self.models
        }


class TokenTracker:
    """
    Global token usage tracker for the ASDA pipeline.

    Phases:
        - phase1: Failure Analysis
        - phase2: Skill Generation
        - phase3: Evaluation

    Components (phase3):
        - router: Skill file selection
        - generation_baseline: Baseline answer generation
        - generation_skill: Skill-augmented answer generation
        - selection: MC numerical → letter mapping
        - evaluation: LLM judge for open questions
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all usage counters."""
        self._usage: Dict[str, Dict[str, ComponentUsage]] = {
            "phase1": {
                "clustering": ComponentUsage(),
                "signature_extraction": ComponentUsage(),
            },
            "phase2": {
                "skill_generation": ComponentUsage(),
                "skill_refinement": ComponentUsage(),
            },
            "phase3": {
                "router": ComponentUsage(),
                "generation_baseline": ComponentUsage(),
                "generation_skill": ComponentUsage(),
                "selection": ComponentUsage(),
                "evaluation": ComponentUsage(),
            },
        }
        self._start_time = datetime.now()
        self._metadata: Dict[str, Any] = {}

    def set_metadata(self, **kwargs):
        """Set metadata for the current run (e.g., config name, model names)."""
        self._metadata.update(kwargs)

    def add(
        self,
        phase: str,
        component: str,
        input_tokens: int,
        output_tokens: int,
        model: str = ""
    ):
        """
        Add token usage for a component.

        Args:
            phase: Phase name (phase1, phase2, phase3)
            component: Component name (e.g., router, generation_baseline)
            input_tokens: Number of input/prompt tokens
            output_tokens: Number of output/completion tokens
            model: Model name (optional, for tracking)
        """
        if phase not in self._usage:
            self._usage[phase] = {}
        if component not in self._usage[phase]:
            self._usage[phase][component] = ComponentUsage()

        self._usage[phase][component].add(input_tokens, output_tokens, model)

    def add_from_response(
        self,
        phase: str,
        component: str,
        response: Any,
        model: str = ""
    ):
        """
        Extract and add token usage from an API response.

        Supports:
            - OpenAI/DashScope: response.usage.prompt_tokens, completion_tokens
            - Anthropic: response.usage.input_tokens, output_tokens
        """
        input_tokens = 0
        output_tokens = 0

        if hasattr(response, 'usage'):
            usage = response.usage
            # OpenAI-style
            if hasattr(usage, 'prompt_tokens'):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            # Anthropic-style
            elif hasattr(usage, 'input_tokens'):
                input_tokens = usage.input_tokens or 0
                output_tokens = usage.output_tokens or 0

        if input_tokens > 0 or output_tokens > 0:
            self.add(phase, component, input_tokens, output_tokens, model)

    def get_phase_total(self, phase: str) -> Dict[str, int]:
        """Get total tokens for a phase."""
        if phase not in self._usage:
            return {"input": 0, "output": 0, "total": 0}

        total_input = sum(c.input_tokens for c in self._usage[phase].values())
        total_output = sum(c.output_tokens for c in self._usage[phase].values())
        return {
            "input": total_input,
            "output": total_output,
            "total": total_input + total_output
        }

    def get_grand_total(self) -> Dict[str, int]:
        """Get total tokens across all phases."""
        total_input = 0
        total_output = 0
        for phase in self._usage.values():
            for component in phase.values():
                total_input += component.input_tokens
                total_output += component.output_tokens
        return {
            "input": total_input,
            "output": total_output,
            "total": total_input + total_output
        }

    def summary(self, print_output: bool = True) -> Dict[str, Any]:
        """
        Generate a summary of token usage.

        Args:
            print_output: If True, print the summary to console

        Returns:
            Dictionary with usage breakdown
        """
        result = {
            "metadata": self._metadata,
            "start_time": self._start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "phases": {},
            "grand_total": self.get_grand_total()
        }

        for phase_name, components in self._usage.items():
            phase_data = {
                "components": {},
                "total": self.get_phase_total(phase_name)
            }
            for comp_name, comp_usage in components.items():
                if comp_usage.call_count > 0:
                    phase_data["components"][comp_name] = comp_usage.to_dict()

            if phase_data["components"]:  # Only include phases with usage
                result["phases"][phase_name] = phase_data

        if print_output:
            self._print_summary(result)

        return result

    def _print_summary(self, result: Dict[str, Any]):
        """Print formatted summary to console."""
        print("\n" + "=" * 60)
        print("TOKEN USAGE SUMMARY")
        print("=" * 60)

        if result["metadata"]:
            print(f"\nMetadata: {result['metadata']}")

        for phase_name, phase_data in result["phases"].items():
            print(f"\n{phase_name.upper()}")
            print("-" * 40)

            for comp_name, comp_data in phase_data["components"].items():
                print(f"  {comp_name}:")
                print(f"    Calls: {comp_data['call_count']}")
                print(f"    Input:  {comp_data['input_tokens']:,}")
                print(f"    Output: {comp_data['output_tokens']:,}")
                print(f"    Total:  {comp_data['total_tokens']:,}")
                if comp_data['models']:
                    print(f"    Models: {comp_data['models']}")

            total = phase_data["total"]
            print(f"  --- Phase Total: {total['total']:,} tokens ---")

        grand = result["grand_total"]
        print(f"\n{'=' * 40}")
        print(f"GRAND TOTAL: {grand['total']:,} tokens")
        print(f"  Input:  {grand['input']:,}")
        print(f"  Output: {grand['output']:,}")
        print("=" * 60)

    def save(self, filepath: str):
        """Save usage summary to JSON file."""
        result = self.summary(print_output=False)
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Token usage saved to {filepath}")

    def load(self, filepath: str):
        """Load previous usage (for aggregation across runs)."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        # This could be extended to merge usage data
        return data


# Global tracker instance
tracker = TokenTracker()


def track_usage(phase: str, component: str, model: str = ""):
    """
    Decorator to automatically track token usage from API responses.

    The decorated function must return an API response object with .usage attribute.

    Usage:
        @track_usage("phase3", "router", model="qwen-flash")
        def call_router(client, prompt):
            return client.chat.completions.create(...)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            tracker.add_from_response(phase, component, response, model)
            return response
        return wrapper
    return decorator


def extract_usage_from_response(response: Any) -> Dict[str, int]:
    """
    Extract token usage from an API response.

    Returns:
        Dict with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    if hasattr(response, 'usage'):
        usage = response.usage
        if hasattr(usage, 'prompt_tokens'):
            input_tokens = usage.prompt_tokens or 0
            output_tokens = usage.completion_tokens or 0
        elif hasattr(usage, 'input_tokens'):
            input_tokens = usage.input_tokens or 0
            output_tokens = usage.output_tokens or 0

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }
