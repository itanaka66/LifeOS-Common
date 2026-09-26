# LifeOS Common Files for Extension Development

## Overview

This document outlines the essential common files that should be shared in the LifeOS-Common repository to enable consistent extension development across separate repositories while maintaining compatibility with the main LifeOS platform.

## Essential Common Files

### 1. Module Interface Definition
```
module_interface.py
```
This defines the base interface that all LifeOS modules must implement.

### 2. Configuration Schema
```
config_schema.py
```
This contains the configuration schemas for modules including ModuleConfig and ModuleManifest.

### 3. Event System
```
event_system.py
```
This provides the event bus system interface for module communication.

### 4. Data Models
```
data_models.py
```
This defines the base data model classes and interfaces for module entities.

## Additional Supporting Files

### 5. Module Manager Interface
```
module_manager.py
```
This defines how modules are managed by the core application.

### 6. Installation Utilities
```
module_installer.py
```
This handles module installation and management processes.

## Repository Structure for LifeOS-Common

```
lifeos-common/
├── module_interface.py
├── config_schema.py
├── event_system.py
├── data_models.py
├── module_manager.py
├── module_installer.py
├── __init__.py
└── README.md
```

## Key Features of Common Files

1. **Interface Definitions**: All abstract base classes that ensure consistency across modules
2. **Configuration Management**: Standardized configuration schemas for different execution modes (local, docker, kubernetes)
3. **Event System**: Unified event bus pattern for module communication
4. **Data Models**: Consistent data handling patterns across modules
5. **Module Management**: Interfaces for module lifecycle management

## Usage Guidelines

These common files should be imported by extension developers when creating new modules:

```python
# Example usage in an extension
from src.api.module_interface import ModuleInterface
from src.models.config_schema import ModuleManifest, ModuleConfig
from src.api.event_system import EventBusInterface, Event
from src.models.data_models import ModuleEntity, ModuleDataManager
```

The common files provide the foundation that ensures all extensions can be properly integrated with the main LifeOS platform while allowing developers to create extensions in separate repositories.
