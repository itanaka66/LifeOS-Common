"""
Common module for LifeOS platform plugin system.
This module provides shared interfaces, base classes, and utilities
for building and managing plugins.
"""

__version__ = "1.0.0"
__author__ = "LifeOS Team"

# Import core components
from .plugin_interface import PluginInterface
from .plugin_manager import PluginManagerInterface, BasePluginManager
from .plugin_config import PluginManifest, PluginConfig
from .data_models import BaseModel, DataModelMixin
from .event_system import EventBusInterface, Event, EventBus

__all__ = [
    "PluginInterface",
    "PluginManagerInterface",
    "BasePluginManager",
    "PluginManifest",
    "PluginConfig",
    "BaseModel",
    "DataModelMixin",
    "EventBusInterface",
    "Event",
    "EventBus"
]