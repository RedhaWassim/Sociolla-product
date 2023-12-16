from pathlib import Path
import os
from typing import Any, Dict, Optional
from sociolla.utils.logger import logging


def retreive_base_path():
    current_path = Path(__file__).resolve()
    base_path = None

    while current_path:
        if (current_path / "README.md").exists():
            base_path = current_path
            break
        current_path = current_path.parent

    if base_path:
        return base_path
    else:
        logging.info("Base path not found")
        raise FileNotFoundError("Base path not found")


def get_from_dict_or_env(
    data: Dict[str, Any], key: str, env_key: str, default: Optional[str] = None
) -> Any:
    """Get a value from a dictionary or an environment variable."""
    if key in data and data[key]:
        return data[key]
    elif env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )
