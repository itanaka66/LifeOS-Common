"""
Plugin Interface for LifeOS Platform
Defines the standard interface that all plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging


class PluginInterface(ABC):
    """
    Base interface that all plugins must implement.

    This interface defines the standard contract that all plugins
    must follow to ensure compatibility with the platform.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the plugin."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the plugin."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the plugin."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        pass

    @abstractmethod
    def get_manifest(self) -> Dict[str, Any]:
        """Get plugin manifest information."""
        pass

    @abstractmethod
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints provided by this plugin."""
        pass

    @abstractmethod
    def get_entities(self) -> List[str]:
        """Get entity types provided by this plugin."""
        pass

    @abstractmethod
    def get_permissions(self) -> List[str]:
        """Get permissions required by this plugin."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start the plugin."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the plugin."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources when plugin is unloaded."""
        pass


class PluginBase(PluginInterface):
    """
    Base implementation of PluginInterface with common functionality.
    """

    def __init__(self, plugin_id: str, version: str, name: str):
        self._id = plugin_id
        self._version = version
        self._name = name
        self._config = None
        self._logger = logging.getLogger(f"plugin.{plugin_id}")
        self._is_initialized = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def version(self) -> str:
        return self._version

    @property
    def name(self) -> str:
        return self._name

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        self._config = config
        self._is_initialized = True
        self._logger.info(f"Plugin {self._id} initialized")

    def get_manifest(self) -> Dict[str, Any]:
        """Get plugin manifest information."""
        return {
            "id": self._id,
            "version": self._version,
            "name": self._name,
            "description": "Generic plugin",
            "min_version": "1.0.0"
        }

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints provided by this plugin."""
        return []

    def get_entities(self) -> List[str]:
        """Get entity types provided by this plugin."""
        return []

    def get_permissions(self) -> List[str]:
        """Get permissions required by this plugin."""
        return []

    def start(self) -> bool:
        """Start the plugin."""
        self._logger.info(f"Starting plugin {self._id}")
        return True

    def stop(self) -> bool:
        """Stop the plugin."""
        self._logger.info(f"Stopping plugin {self._id}")
        return True

    def cleanup(self) -> None:
        """Clean up resources when plugin is unloaded."""
        self._logger.info(f"Cleaning up plugin {self._id}")