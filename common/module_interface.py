"""
Module Interface for LifeOS Platform

This file defines the base interface that all modules must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import uuid


class ModuleInterface(ABC):
    """
    Base interface for all LifeOS modules.

    All modules must implement this interface to be compatible with the LifeOS platform.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Get the unique identifier of the module."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the module."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Get the version of the module."""
        pass

    @abstractmethod
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Initialize the module.

        Args:
            config: Configuration for the module

        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    def start(self) -> bool:
        """
        Start the module.

        Returns:
            True if start was successful, False otherwise
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the module.

        Returns:
            True if stop was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_manifest(self) -> Dict[str, Any]:
        """
        Get the module manifest information.

        Returns:
            Dictionary containing module metadata
        """
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """
        Check if the module is currently running.

        Returns:
            True if the module is running, False otherwise
        """
        pass


class ModuleBase(ModuleInterface):
    """
    Base implementation of a module with common functionality.

    This class provides default implementations for many methods that modules can override.
    """

    def __init__(self, id: str, version: str, name: str):
        self._id = id
        self._version = version
        self._name = name
        self._is_running = False
        self._config = None

    @property
    def id(self) -> str:
        """Get the unique identifier of the module."""
        return self._id

    @property
    def name(self) -> str:
        """Get the name of the module."""
        return self._name

    @property
    def version(self) -> str:
        """Get the version of the module."""
        return self._version

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Initialize the module.

        Args:
            config: Configuration for the module

        Returns:
            True if initialization was successful, False otherwise
        """
        self._config = config or {}
        return True

    def start(self) -> bool:
        """
        Start the module.

        Returns:
            True if start was successful, False otherwise
        """
        self._is_running = True
        return True

    def stop(self) -> bool:
        """
        Stop the module.

        Returns:
            True if stop was successful, False otherwise
        """
        self._is_running = False
        return True

    def get_manifest(self) -> Dict[str, Any]:
        """
        Get the module manifest information.

        Returns:
            Dictionary containing module metadata
        """
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "type": "module",
            "initialized": self._config is not None,
            "running": self._is_running
        }

    def is_running(self) -> bool:
        """
        Check if the module is currently running.

        Returns:
            True if the module is running, False otherwise
        """
        return self._is_running