"""
Module Manager for LifeOS Platform

This file provides interfaces and implementations for managing modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from .module_interface import ModuleInterface
from .module_config import ModuleManifest


class ModuleManagerInterface(ABC):
    """
    Interface for module management operations.

    Defines the standard methods that any module manager must implement.
    """

    @abstractmethod
    def register_module(self, module: ModuleInterface) -> bool:
        """
        Register a module with the manager.

        Args:
            module: Module to register

        Returns:
            True if registration was successful, False otherwise
        """
        pass

    @abstractmethod
    def unregister_module(self, module_id: str) -> bool:
        """
        Unregister a module from the manager.

        Args:
            module_id: ID of the module to unregister

        Returns:
            True if unregistration was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_module(self, module_id: str) -> Optional[ModuleInterface]:
        """
        Get a registered module by its ID.

        Args:
            module_id: ID of the module to retrieve

        Returns:
            Module instance or None if not found
        """
        pass

    @abstractmethod
    def list_modules(self) -> List[Dict[str, Any]]:
        """
        List all registered modules.

        Returns:
            List of module information dictionaries
        """
        pass

    @abstractmethod
    def install_module(self, manifest: ModuleManifest, source: str) -> bool:
        """
        Install a module from source.

        Args:
            manifest: Manifest describing the module to install
            source: Source location (path, URL, etc.)

        Returns:
            True if installation was successful, False otherwise
        """
        pass

    @abstractmethod
    def uninstall_module(self, module_id: str) -> bool:
        """
        Uninstall a module.

        Args:
            module_id: ID of the module to uninstall

        Returns:
            True if uninstallation was successful, False otherwise
        """
        pass

    @abstractmethod
    def enable_module(self, module_id: str) -> bool:
        """
        Enable a module.

        Args:
            module_id: ID of the module to enable

        Returns:
            True if enabling was successful, False otherwise
        """
        pass

    @abstractmethod
    def disable_module(self, module_id: str) -> bool:
        """
        Disable a module.

        Args:
            module_id: ID of the module to disable

        Returns:
            True if disabling was successful, False otherwise
        """
        pass

    @abstractmethod
    def start_module(self, module_id: str) -> bool:
        """
        Start a module.

        Args:
            module_id: ID of the module to start

        Returns:
            True if starting was successful, False otherwise
        """
        pass

    @abstractmethod
    def stop_module(self, module_id: str) -> bool:
        """
        Stop a module.

        Args:
            module_id: ID of the module to stop

        Returns:
            True if stopping was successful, False otherwise
        """
        pass


class BaseModuleManager(ModuleManagerInterface):
    """
    Core implementation of module manager.

    Provides basic functionality for managing modules.
    """

    def __init__(self):
        self._modules: Dict[str, ModuleInterface] = {}
        self._enabled_modules: Dict[str, bool] = {}

    def register_module(self, module: ModuleInterface) -> bool:
        """
        Register a module with the manager.

        Args:
            module: Module to register

        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._modules[module.id] = module
            self._enabled_modules[module.id] = False
            return True
        except Exception:
            return False

    def unregister_module(self, module_id: str) -> bool:
        """
        Unregister a module from the manager.

        Args:
            module_id: ID of the module to unregister

        Returns:
            True if unregistration was successful, False otherwise
        """
        try:
            if module_id in self._modules:
                del self._modules[module_id]
                del self._enabled_modules[module_id]
                return True
            return False
        except Exception:
            return False

    def get_module(self, module_id: str) -> Optional[ModuleInterface]:
        """
        Get a registered module by its ID.

        Args:
            module_id: ID of the module to retrieve

        Returns:
            Module instance or None if not found
        """
        return self._modules.get(module_id)

    def list_modules(self) -> List[Dict[str, Any]]:
        """
        List all registered modules.

        Returns:
            List of module information dictionaries
        """
        modules_info = []
        for module_id, module in self._modules.items():
            info = {
                "id": module_id,
                "name": module.name,
                "version": module.version,
                "running": module.is_running(),
                "enabled": self._enabled_modules.get(module_id, False)
            }
            modules_info.append(info)
        return modules_info

    def install_module(self, manifest: ModuleManifest, source: str) -> bool:
        """
        Install a module from source.

        Args:
            manifest: Manifest describing the module to install
            source: Source location (path, URL, etc.)

        Returns:
            True if installation was successful, False otherwise
        """
        # In a real implementation this would handle actual installation logic
        # For now we just return True as an example
        return True

    def uninstall_module(self, module_id: str) -> bool:
        """
        Uninstall a module.

        Args:
            module_id: ID of the module to uninstall

        Returns:
            True if uninstallation was successful, False otherwise
        """
        # In a real implementation this would handle actual uninstallation logic
        return self.unregister_module(module_id)

    def enable_module(self, module_id: str) -> bool:
        """
        Enable a module.

        Args:
            module_id: ID of the module to enable

        Returns:
            True if enabling was successful, False otherwise
        """
        try:
            if module_id in self._enabled_modules:
                self._enabled_modules[module_id] = True
                return True
            return False
        except Exception:
            return False

    def disable_module(self, module_id: str) -> bool:
        """
        Disable a module.

        Args:
            module_id: ID of the module to disable

        Returns:
            True if disabling was successful, False otherwise
        """
        try:
            if module_id in self._enabled_modules:
                self._enabled_modules[module_id] = False
                return True
            return False
        except Exception:
            return False

    def start_module(self, module_id: str) -> bool:
        """
        Start a module.

        Args:
            module_id: ID of the module to start

        Returns:
            True if starting was successful, False otherwise
        """
        try:
            module = self.get_module(module_id)
            if module and self._enabled_modules.get(module_id, False):
                return module.start()
            return False
        except Exception:
            return False

    def stop_module(self, module_id: str) -> bool:
        """
        Stop a module.

        Args:
            module_id: ID of the module to stop

        Returns:
            True if stopping was successful, False otherwise
        """
        try:
            module = self.get_module(module_id)
            if module:
                return module.stop()
            return False
        except Exception:
            return False