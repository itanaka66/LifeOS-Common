# LifeOS Common Components

This repository contains shared interfaces and utilities for LifeOS extensions.

## Package Structure

```
lifeos-common/
├── __init__.py
├── module_interface.py
├── config_schema.py
├── event_system.py
├── data_models.py
├── module_manager.py
└── module_installer.py
```

## Usage

Extensions can import from this package:

```python
from lifeos_common.module_interface import ModuleInterface
from lifeos_common.config_schema import ModuleManifest, ModuleConfig
from lifeos_common.event_system import EventBusInterface, Event
from lifeos_common.data_models import ModuleEntity, ModuleDataManager
```

## Files Overview

- **module_interface.py**: Base interface that all LifeOS modules must implement
- **config_schema.py**: Configuration schemas for modules including ModuleConfig and ModuleManifest  
- **event_system.py**: Event bus system interface for module communication
- **data_models.py**: Base data model classes and interfaces for module entities
- **module_manager.py**: Interface for managing modules by the core application
- **module_installer.py**: Utilities for installing and managing modules

## Features

- Supports multiple execution environments (local services, Docker containers, Kubernetes)
- Standardized configuration schemas
- Event-driven architecture for module communication
- Consistent data model interfaces
- Module lifecycle management