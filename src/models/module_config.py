"""
Module Configuration for LifeOS Platform

This file defines configuration schemas and manifests for modules.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import json


@dataclass
class ModuleManifest:
    """
    Manifest describing a module's metadata and requirements.

    This class provides information about what a module needs to run properly.
    """

    id: str
    version: str
    name: str
    description: str
    author: str
    license: str
    dependencies: Optional[List[str]] = None
    requirements: Optional[Dict[str, Any]] = None
    entry_point: Optional[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "id": self.id,
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "dependencies": self.dependencies or [],
            "requirements": self.requirements or {},
            "entry_point": self.entry_point,
            "config_schema": self.config_schema or {},
            "tags": self.tags or [],
            "categories": self.categories or []
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModuleManifest':
        """Create manifest from dictionary."""
        return cls(
            id=data.get("id"),
            version=data.get("version"),
            name=data.get("name"),
            description=data.get("description"),
            author=data.get("author"),
            license=data.get("license"),
            dependencies=data.get("dependencies"),
            requirements=data.get("requirements"),
            entry_point=data.get("entry_point"),
            config_schema=data.get("config_schema"),
            tags=data.get("tags"),
            categories=data.get("categories")
        )


class ModuleConfig:
    """
    Configuration class for module settings.

    This class handles loading, validating, and managing module configurations.
    """

    def __init__(self, manifest: ModuleManifest, config_data: Optional[Dict[str, Any]] = None):
        self.manifest = manifest
        self.config_data = config_data or {}
        self._validated = False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value

    def validate(self) -> bool:
        """
        Validate the configuration against the manifest schema.

        Returns:
            True if valid, False otherwise
        """
        # Basic validation - in a real implementation this would be more complex
        self._validated = True
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "manifest": self.manifest.to_dict(),
            "config_data": self.config_data,
            "validated": self._validated
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModuleConfig':
        """Create configuration from dictionary."""
        manifest = ModuleManifest.from_dict(data["manifest"])
        return cls(manifest, data.get("config_data"))

    def save(self, filepath: str) -> None:
        """
        Save configuration to file.

        Args:
            filepath: Path to save the configuration
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'ModuleConfig':
        """
        Load configuration from file.

        Args:
            filepath: Path to load the configuration from

        Returns:
            ModuleConfig instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
