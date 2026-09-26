"""
Module Manager Interface and Base Implementation

This file defines how modules are managed by the core application,
including the interface and a base implementation.
"""

from typing import Dict, List, Optional, Any, Type
from abc import ABC, abstractmethod
import logging

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


class BaseModuleManager(ModuleManagerInterface):
    """
    Base implementation of ModuleManagerInterface.
    Provides core functionality for managing modules.
    """

    def __init__(self):
        self._modules: Dict[str, object] = {}
        self._module_classes: Dict[str, Type] = {}
        self._logger = logging.getLogger("module.manager")

    def register_module(self, module_id: str, module_class) -> None:
        self._module_classes[module_id] = module_class
        self._logger.info(f"Registered module: {module_id}")

    def load_module(self, module_id: str, config: Dict[str, Any]) -> bool:
        if module_id not in self._module_classes:
            return False

        try:
            module_class = self._module_classes[module_id]
            # Assuming module_class has an initialize method
            instance = module_class()
            instance.initialize(config)
            self._modules[module_id] = instance
            return True
        except Exception as e:
            self._logger.error(f"Failed to load module {module_id}: {e}")
            return False

    def unload_module(self, module_id: str) -> bool:
        if module_id in self._modules:
            del self._modules[module_id]
            return True
        return False

    def start_module(self, module_id: str) -> bool:
        module = self.get_module(module_id)
        if module and hasattr(module, 'start'):
            return module.start()
        return False

    def stop_module(self, module_id: str) -> bool:
        module = self.get_module(module_id)
        if module and hasattr(module, 'stop'):
            return module.stop()
        return False

    def get_module(self, module_id: str) -> Optional[object]:
        return self._modules.get(module_id)

    def list_modules(self) -> List[Dict[str, Any]]:
        return [{"id": mid, "status": "loaded" if mid in self._modules else "registered"}
                for mid in self._module_classes]

    def get_module_config(self, module_id: str) -> Dict[str, Any]:
        # Simplified config retrieval
        return {}

    def update_module_config(self, module_id: str, config: Dict[str, Any]) -> bool:
        # Simplified config update
        return True

    def get_module_endpoints(self, module_id: str) -> List[Dict[str, Any]]:
        module = self.get_module(module_id)
        if module and hasattr(module, 'get_endpoints'):
            return module.get_endpoints()
        return []

    def get_module_entities(self, module_id: str) -> List[str]:
        module = self.get_module(module_id)
        if module and hasattr(module, 'get_entities'):
            return module.get_entities()
        return []

    def get_module_status(self, module_id: str) -> Dict[str, Any]:
        return {"id": module_id, "status": "active" if module_id in self._modules else "inactive"}
