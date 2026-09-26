"""
Module Interface Definition

This file defines the base interface and base implementation that all LifeOS modules must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

class ModuleInterface(ABC):
    """Base interface that all LifeOS modules must implement."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the module."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the module."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the module."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module with configuration."""
        pass

    @abstractmethod
    def get_manifest(self) -> Dict[str, Any]:
        """Get module manifest information."""
        pass

    @abstractmethod
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints provided by this module."""
        pass

    @abstractmethod
    def get_entities(self) -> List[str]:
        """Get entity types provided by this module."""
        pass

    @abstractmethod
    def get_permissions(self) -> List[str]:
        """Get permissions required by this module."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start the module."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the module."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources when module is unloaded."""
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """Check if the module is currently running."""
        pass


class ModuleBase(ModuleInterface):
    """
    Base implementation of ModuleInterface with common functionality.
    """

    def __init__(self, module_id: str, version: str, name: str):
        self._id = module_id
        self._version = version
        self._name = name
        self._config = None
        self._logger = logging.getLogger(f"module.{module_id}")
        self._is_initialized = False
        self._is_running = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def version(self) -> str:
        return self._version

    @property
    def name(self) -> str:
        return self._name

    def initialize(self, config: Dict[str, Any] = None) -> None:
        """Initialize the module with configuration."""
        self._config = config or {}
        self._is_initialized = True
        self._logger.info(f"Module {self._id} initialized")

    def get_manifest(self) -> Dict[str, Any]:
        """Get module manifest information."""
        return {
            "id": self._id,
            "version": self._version,
            "name": self._name,
            "description": "Generic module",
            "min_version": "1.0.0"
        }

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints provided by this module."""
        return []

    def get_entities(self) -> List[str]:
        """Get entity types provided by this module."""
        return []

    def get_permissions(self) -> List[str]:
        """Get permissions required by this module."""
        return []

    def start(self) -> bool:
        """Start the module."""
        self._logger.info(f"Starting module {self._id}")
        self._is_running = True
        return True

    def stop(self) -> bool:
        """Stop the module."""
        self._logger.info(f"Stopping module {self._id}")
        self._is_running = False
        return True

    def is_running(self) -> bool:
        """Check if the module is currently running."""
        return self._is_running

    def cleanup(self) -> None:
        """Clean up resources when module is unloaded."""
        self._logger.info(f"Cleaning up module {self._id}")
