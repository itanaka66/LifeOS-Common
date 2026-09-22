"""
LifeOS Common Components

This package provides shared interfaces and utilities for LifeOS extensions.
"""

__version__ = "1.0.0"
__author__ = "LifeOS Team"

# Import all public interfaces
from .module_interface import ModuleInterface
from .config_schema import ModuleConfig, ModuleManifest
from .event_system import EventBusInterface, Event, EventType
from .data_models import ModuleEntity, ModuleDataManager, BaseModel

__all__ = [
    'ModuleInterface',
    'ModuleConfig',
    'ModuleManifest',
    'EventBusInterface',
    'Event',
    'EventType',
    'ModuleEntity',
    'ModuleDataManager',
    'BaseModel'
]