"""
Plugin Configuration for LifeOS Platform
Defines configuration structures and management for plugins.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import json


@dataclass
class PluginManifest:
    """
    Manifest describing a plugin's metadata and requirements.

    This class provides a standardized way to describe plugin capabilities,
    dependencies, and configuration requirements.
    """

    # Basic identification
    id: str
    version: str
    name: str
    description: str = ""

    # Platform compatibility
    min_version: str = "1.0.0"
    max_version: Optional[str] = None

    # Database configuration
    database: Dict[str, Any] = field(default_factory=dict)

    # Dependencies
    dependencies: Dict[str, Any] = field(default_factory=dict)

    # Permissions required
    permissions: List[str] = field(default_factory=list)

    # Entities provided
    entities: List[str] = field(default_factory=list)

    # UI configuration
    ui: Dict[str, Any] = field(default_factory=dict)

    # AI tools
    ai: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "id": self.id,
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "min_version": self.min_version,
            "max_version": self.max_version,
            "database": self.database,
            "dependencies": self.dependencies,
            "permissions": self.permissions,
            "entities": self.entities,
            "ui": self.ui,
            "ai": self.ai,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PluginManifest':
        """Create manifest from dictionary."""
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the manifest for required fields.

        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        if not self.id or not self.version or not self.name:
            return False
        return True


@dataclass
class PluginConfig:
    """
    Configuration for a plugin instance.

    This class holds the runtime configuration for a specific plugin.
    """

    # Basic settings
    enabled: bool = True
    version: str = ""
    config_data: Dict[str, Any] = field(default_factory=dict)

    # Database connection
    database_url: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    # Plugin-specific settings
    plugin_settings: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config_data[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "enabled": self.enabled,
            "version": self.version,
            "config_data": self.config_data,
            "database_url": self.database_url,
            "log_level": self.log_level,
            "plugin_settings": self.plugin_settings
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PluginConfig':
        """Create configuration from dictionary."""
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the configuration.

        Returns:
            True if valid, False otherwise
        """
        # Add validation logic as needed
        return True


class PluginConfigManager:
    """
    Manager for plugin configurations.

    Handles loading, saving, and managing plugin configurations.
    """

    def __init__(self, config_dir: str = "./config/plugins"):
        self.config_dir = config_dir
        self._configs: Dict[str, PluginConfig] = {}

    def load_config(self, plugin_id: str) -> Optional[PluginConfig]:
        """
        Load configuration for a specific plugin.

        Args:
            plugin_id: The ID of the plugin

        Returns:
            PluginConfig instance or None if not found
        """
        try:
            # In a real implementation, this would read from disk or database
            config_path = f"{self.config_dir}/{plugin_id}.json"

            # Check if file exists
            import os
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    self._configs[plugin_id] = PluginConfig.from_dict(data)
                    return self._configs[plugin_id]

            # Return default config if file doesn't exist
            self._configs[plugin_id] = PluginConfig()
            return self._configs[plugin_id]

        except Exception as e:
            print(f"Error loading config for {plugin_id}: {e}")
            return None

    def save_config(self, plugin_id: str, config: PluginConfig) -> bool:
        """
        Save configuration for a specific plugin.

        Args:
            plugin_id: The ID of the plugin
            config: The configuration to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            import os
            os.makedirs(self.config_dir, exist_ok=True)

            # Save to file
            config_path = f"{self.config_dir}/{plugin_id}.json"
            with open(config_path, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)

            self._configs[plugin_id] = config
            return True

        except Exception as e:
            print(f"Error saving config for {plugin_id}: {e}")
            return False

    def get_config(self, plugin_id: str) -> Optional[PluginConfig]:
        """
        Get configuration for a specific plugin.

        Args:
            plugin_id: The ID of the plugin

        Returns:
            PluginConfig instance or None if not found
        """
        return self._configs.get(plugin_id)