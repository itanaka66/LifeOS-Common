"""
Module Interface Definition

This file defines the base interface that all LifeOS modules must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from uuid import UUID

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