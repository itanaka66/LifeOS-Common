"""
Module Manager Interface

This file defines how modules are managed by the core application.
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from uuid import UUID

class ModuleManagerInterface(ABC):
    """Interface for managing modules."""

    @abstractmethod
    def register_module(self, module_id: str, module_class) -> None:
        """Register a module class."""
        pass

    @abstractmethod
    def load_module(self, module_id: str, config: Dict[str, Any]) -> bool:
        """Load and initialize a module."""
        pass

    @abstractmethod
    def unload_module(self, module_id: str) -> bool:
        """Unload a module."""
        pass

    @abstractmethod
    def start_module(self, module_id: str) -> bool:
        """Start a module."""
        pass

    @abstractmethod
    def stop_module(self, module_id: str) -> bool:
        """Stop a module."""
        pass

    @abstractmethod
    def get_module(self, module_id: str) -> Optional[object]:
        """Get loaded module instance."""
        pass

    @abstractmethod
    def list_modules(self) -> List[Dict[str, Any]]:
        """List all registered modules."""
        pass

    @abstractmethod
    def get_module_config(self, module_id: str) -> Dict[str, Any]:
        """Get configuration for a module."""
        pass

    @abstractmethod
    def update_module_config(self, module_id: str, config: Dict[str, Any]) -> bool:
        """Update module configuration."""
        pass

    @abstractmethod
    def get_module_endpoints(self, module_id: str) -> List[Dict[str, Any]]:
        """Get API endpoints for a module."""
        pass

    @abstractmethod
    def get_module_entities(self, module_id: str) -> List[str]:
        """Get entities provided by a module."""
        pass

    @abstractmethod
    def get_module_status(self, module_id: str) -> Dict[str, Any]:
        """Get status of a module."""
        pass