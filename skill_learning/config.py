"""
Configuration Loader for Skill Learning

Loads configuration from YAML files. API keys always from .env.

Usage:
    from skill_learning.config import load_config, cfg

    # Load from YAML file
    config = load_config("configs/skill_learning/arithmetic.yaml")

    # Access parameters using helper function
    gen_model = cfg("models.gen")
    p_min = cfg("evidence.p_min")

    # Or direct dict access
    gen_model = config["models"]["gen"]
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv

# Load .env for API keys
load_dotenv()

# Global config instance
_config: Optional[Dict[str, Any]] = None


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to YAML config file.

    Returns:
        Configuration dictionary.
    """
    global _config

    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}

    print(f"[OK] Loaded config from {config_path}")
    print(f"  Config keys: {list(config.keys()) if config else 'empty'}")
    if 'models' in config:
        print(f"  models.gen: {config.get('models', {}).get('gen', 'NOT SET')}")
    if 'skills' in config:
        print(f"  skills.method: {config.get('skills', {}).get('method', 'NOT SET')}")
    _config = config
    return config


def get_config() -> Dict[str, Any]:
    """Get the current configuration singleton."""
    global _config
    if _config is None:
        raise RuntimeError("Config not loaded. Call load_config() first.")
    return _config


def set_config(config: Dict[str, Any]) -> None:
    """Set the global configuration directly.

    Use this when loading config from external sources (e.g., evaluate_checkpoint.py
    has its own YAML loader but needs to make values available via cfg()).

    Args:
        config: Configuration dictionary to set as global config.
    """
    global _config
    _config = config


def is_config_loaded() -> bool:
    """Check if config has been loaded."""
    return _config is not None


def cfg(path: str, default: Any = None, debug: bool = False) -> Any:
    """Get config value by dot-separated path.

    Args:
        path: Dot-separated path like "models.gen" or "evidence.p_min"
        default: Default value if path not found
        debug: Print debug info if True

    Returns:
        Config value or default.

    Example:
        gen_model = cfg("models.gen")
        p_min = cfg("evidence.p_min", 5)
    """
    global _config
    if _config is None:
        if debug:
            print(f"  [cfg] _config is None, returning default for '{path}'")
        return default

    keys = path.split(".")
    value = _config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            if debug:
                print(f"  [cfg] Key '{key}' not found in path '{path}', returning default")
            return default
    if debug:
        print(f"  [cfg] Found '{path}' = {value}")
    return value


def get_api_keys() -> Dict[str, str]:
    """Get API keys from .env (never from YAML for security)."""
    return {
        "dashscope_api_key": os.getenv("DASHSCOPE_API_KEY", ""),
        "qwen_api_base": os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
        "anthropic_api_base": os.getenv("ANTHROPIC_API_BASE", "https://api.anthropic.com"),
    }


def setup_from_config(config: Dict[str, Any] = None):
    """Setup API clients from config.

    Args:
        config: Config dict. If None, uses global config.

    Returns:
        Tuple of (client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider)

    Provider selection:
    1. Explicit provider from config (openrouter, anthropic, dashscope)
    2. Auto-detect from model name when provider is 'auto' or not set:
       - anthropic/* -> OpenRouter
       - claude* -> Anthropic
       - qwen* -> DashScope
    """
    from openai import OpenAI
    from anthropic import Anthropic

    if config is None:
        config = get_config()

    api_keys = get_api_keys()

    # Get models from config
    gen_model = config["models"]["gen"]
    eval_model = config["models"]["eval"]

    # Get providers from config (optional, default to 'auto')
    gen_provider = config.get("models", {}).get("gen_provider", "auto")
    eval_provider = config.get("models", {}).get("eval_provider", "auto")

    # DashScope client (default for eval and fallback)
    dashscope_api_key = api_keys["dashscope_api_key"] or os.getenv("OPENAI_API_KEY", "")
    dashscope_base_url = api_keys["qwen_api_base"] if api_keys["dashscope_api_key"] else os.getenv("OPENAI_BASE_URL", "")

    if not dashscope_api_key:
        raise ValueError("No API key found. Set DASHSCOPE_API_KEY or OPENAI_API_KEY in .env")

    # Create default OpenAI-compatible client (DashScope)
    client = OpenAI(api_key=dashscope_api_key, base_url=dashscope_base_url)

    # Create clients based on gen_provider
    anthropic_client = None
    openrouter_client = None

    if gen_provider == 'openrouter':
        # Explicit OpenRouter provider
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY required when gen_provider is 'openrouter'")
        openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
        print(f"[OK] OpenRouter client created for {gen_model} (explicit provider)")
    elif gen_provider == 'anthropic':
        # Explicit Anthropic provider
        anthropic_api_key = api_keys["anthropic_api_key"]
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY required when gen_provider is 'anthropic'")
        anthropic_base_url = api_keys["anthropic_api_base"]
        if anthropic_base_url and anthropic_base_url != "https://api.anthropic.com":
            anthropic_client = Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
        else:
            anthropic_client = Anthropic(api_key=anthropic_api_key)
        print(f"[OK] Anthropic client created for {gen_model} (explicit provider)")
    elif gen_provider == 'dashscope':
        # Explicit DashScope provider - client already created above
        print(f"[OK] DashScope client for {gen_model} (explicit provider)")
    else:
        # Auto-detect from model name
        if gen_model.startswith('anthropic/'):
            # OpenRouter model format (e.g., anthropic/claude-3.5-haiku)
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
            if openrouter_api_key:
                openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"[OK] OpenRouter client created for {gen_model} (auto-detected)")
            else:
                print(f"[WARN] OPENROUTER_API_KEY not set for model {gen_model}")
        elif gen_model.lower().startswith('claude'):
            # Claude model - try Anthropic first, then OpenRouter
            anthropic_api_key = api_keys["anthropic_api_key"]
            if anthropic_api_key:
                anthropic_base_url = api_keys["anthropic_api_base"]
                if anthropic_base_url and anthropic_base_url != "https://api.anthropic.com":
                    anthropic_client = Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
                else:
                    anthropic_client = Anthropic(api_key=anthropic_api_key)
                print(f"[OK] Anthropic client created for {gen_model} (auto-detected)")
            else:
                # Fallback to OpenRouter if available
                openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
                if openrouter_api_key:
                    openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                    print(f"[OK] OpenRouter client created for {gen_model} (fallback, ANTHROPIC_API_KEY not set)")
                else:
                    print(f"[WARN] Neither ANTHROPIC_API_KEY nor OPENROUTER_API_KEY set - will use router method for Claude")

    # Create eval_client based on eval_provider
    eval_client = None
    if eval_provider == 'openrouter':
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_api_key:
            eval_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
            print(f"[OK] Eval client: OpenRouter ({eval_model})")
    elif eval_provider == 'anthropic':
        anthropic_api_key = api_keys["anthropic_api_key"]
        if anthropic_api_key:
            eval_client = Anthropic(api_key=anthropic_api_key)
            print(f"[OK] Eval client: Anthropic ({eval_model})")
    elif eval_provider == 'dashscope':
        eval_client = client  # Use default DashScope client
        print(f"[OK] Eval client: DashScope ({eval_model})")
    else:
        # Auto-detect from eval_model name
        if eval_model.startswith('anthropic/'):
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
            if openrouter_api_key:
                eval_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"[OK] Eval client: OpenRouter (auto-detected)")
        elif eval_model.lower().startswith('claude'):
            anthropic_api_key = api_keys["anthropic_api_key"]
            if anthropic_api_key:
                eval_client = Anthropic(api_key=anthropic_api_key)
                print(f"[OK] Eval client: Anthropic (auto-detected)")
        elif eval_model.lower().startswith('qwen'):
            eval_client = client  # Use default DashScope client
            print(f"[OK] Eval client: DashScope (auto-detected)")
        else:
            eval_client = client  # Fallback to default client
            print(f"[OK] Eval client: Default (fallback)")

    # Print model info
    if gen_model == eval_model:
        print(f"[OK] Using model: {gen_model} (both generation and evaluation)")
    else:
        print(f"[OK] Using generation model: {gen_model}")
        print(f"[OK] Using evaluation model: {eval_model}")

    return client, gen_model, eval_model, anthropic_client, openrouter_client, gen_provider, eval_client, eval_provider
