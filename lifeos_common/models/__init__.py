"""
LifeOS Common Module

This package provides shared interfaces, base classes, and utilities for building
plugins and modules for the LifeOS platform.
"""

__version__ = "1.0.0"
__author__ = "LifeOS Team"

# Import core components - Plugin interfaces
from .plugin_interface import PluginInterface
from .plugin_manager import PluginManagerInterface, BasePluginManager
from .plugin_config import PluginManifest, PluginConfig
from .data_models import BaseModel, DataModelMixin

# Import module interfaces (merged)
from .module_interface import ModuleInterface
from .module_manager import ModuleManagerInterface, BaseModuleManager
from .module_config import ModuleManifest, ModuleConfig

# Import event system components - Both plugin and module versions
from .event_system import EventBusInterface, Event, EventBus, EventType

# Import utility functions
from .utils import setup_logging, generate_plugin_id, sanitize_input, validate_json

__all__ = [
    # Plugin interfaces
    "PluginInterface",
    "PluginManagerInterface",
    "BasePluginManager",
    "PluginManifest",
    "PluginConfig",

    # Module interfaces
    "ModuleInterface",
    "ModuleManagerInterface",
    "BaseModuleManager",
    "ModuleManifest",
    "ModuleConfig",

    # Data models
    "BaseModel",
    "DataModelMixin",

    # Event system
    "EventBusInterface",
    "Event",
    "EventBus",
    "EventType",

    # Utilities
    "setup_logging",
    "generate_plugin_id",
    "sanitize_input",
    "validate_json"
]