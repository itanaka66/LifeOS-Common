"""
Utility functions for LifeOS Platform Plugins
Provides common utility functions for plugin development.
"""

import logging
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib
import base64


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration for plugins.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("plugin")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid adding multiple handlers if this is called multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger


def generate_plugin_id(name: str, version: str) -> str:
    """
    Generate a unique plugin ID based on name and version.

    Args:
        name: Plugin name
        version: Plugin version

    Returns:
        Generated plugin ID
    """
    # Create a hash of the name and version
    input_string = f"{name}-{version}"
    hash_object = hashlib.sha256(input_string.encode())
    hex_dig = hash_object.hexdigest()

    # Use first 16 characters as plugin ID
    return f"plugin.{hex_dig[:16]}"


def sanitize_input(data: Any) -> Any:
    """
    Sanitize input data to prevent injection attacks.

    Args:
        data: Input data to sanitize

    Returns:
        Sanitized data
    """
    if isinstance(data, str):
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '&', '"', "'", '`', ';', '--', '/*', '*/']
        sanitized = data
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    else:
        return data


def validate_json(data: Any) -> bool:
    """
    Validate that data can be serialized to JSON.

    Args:
        data: Data to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        Current timestamp as string
    """
    return datetime.utcnow().isoformat()


def encode_base64(data: str) -> str:
    """
    Encode string data to base64.

    Args:
        data: String to encode

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(data.encode()).decode()


def decode_base64(encoded_data: str) -> str:
    """
    Decode base64 encoded string.

    Args:
        encoded_data: Base64 encoded string

    Returns:
        Decoded string
    """
    return base64.b64decode(encoded_data.encode()).decode()


class PluginUtils:
    """
    Utility class for plugin development.

    Provides static methods that are commonly used across plugins.
    """

    @staticmethod
    def load_config_from_file(config_path: str) -> Optional[Dict[str, Any]]:
        """
        Load configuration from JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary or None if failed
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.getLogger("utils").error(f"Failed to load config from {config_path}: {e}")
            return None

    @staticmethod
    def save_config_to_file(config: Dict[str, Any], config_path: str) -> bool:
        """
        Save configuration to JSON file.

        Args:
            config: Configuration dictionary
            config_path: Path to save configuration

        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            logging.getLogger("utils").error(f"Failed to save config to {config_path}: {e}")
            return False

    @staticmethod
    def merge_configs(default_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.

        Args:
            default_config: Default configuration
            override_config: Override configuration

        Returns:
            Merged configuration
        """
        merged = default_config.copy()
        merged.update(override_config)
        return merged

    @staticmethod
    def flatten_dict(data: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten a nested dictionary.

        Args:
            data: Dictionary to flatten
            parent_key: Parent key for recursion
            sep: Separator for keys

        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(PluginUtils.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
