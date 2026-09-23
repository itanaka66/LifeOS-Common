# LifeOS Common Module

The common module provides shared interfaces, base classes, and utilities for building plugins and modules for the LifeOS platform. This module contains all the core functionality that plugins and modules can use to interact with the platform.

## Features

- **Plugin Interface**: Standard contract for all plugins
- **Plugin Manager**: Lifecycle management of plugins
- **Module Interface**: Standard contract for all modules  
- **Module Manager**: Lifecycle management of modules
- **Data Models**: Base classes for data entities
- **Event System**: Communication between plugins, modules and system components
- **Decorators**: Common decorators for plugin development
- **Utilities**: Helper functions and tools

## Installation

```bash
pip install .
```

Or if you're working in the source directory:

```bash
pip install -e .
```

## Usage

### Basic Plugin Implementation

```python
from common.plugin_interface import PluginBase
from common.decorators import require_permission

class MyPlugin(PluginBase):
    def __init__(self):
        super().__init__("my.plugin", "1.0.0", "My Sample Plugin")
    
    @require_permission("sample.read")
    def get_data(self):
        return {"message": "Hello from my plugin!"}
```

### Basic Module Implementation

```python
from common.module_interface import ModuleBase
from common.decorators import require_permission

class MyModule(ModuleBase):
    def __init__(self):
        super().__init__("my.module", "1.0.0", "My Sample Module")
    
    @require_permission("sample.read")
    def get_data(self):
        return {"message": "Hello from my module!"}
```

### Plugin Manager Usage

```python
from common.plugin_manager import BasePluginManager

# Create a plugin manager
manager = BasePluginManager()

# Register your plugin class
manager.register_plugin(MyPlugin)

# Install and enable plugins
manager.install_plugin("/path/to/plugin")
manager.enable_plugin("my.plugin")
```

### Module Manager Usage

```python
from common.module_manager import BaseModuleManager

# Create a module manager
manager = BaseModuleManager()

# Register your module
manager.register_module(MyModule())

# Enable and start modules
manager.enable_module("my.module")
manager.start_module("my.module")
```

## Components

### Plugin Interface
- `PluginInterface`: Abstract base interface for all plugins
- `PluginBase`: Base implementation with common functionality

### Plugin Manager
- `PluginManagerInterface`: Interface for plugin management operations
- `BasePluginManager`: Core implementation of plugin manager

### Module Interface
- `ModuleInterface`: Abstract base interface for all modules
- `ModuleBase`: Base implementation with common functionality

### Module Manager
- `ModuleManagerInterface`: Interface for module management operations
- `BaseModuleManager`: Core implementation of module manager

### Data Models
- `BaseModel`: Base class for data models
- `DataModelMixin`: Utility functions for data models

### Event System
- `EventBusInterface`: Interface for event bus operations
- `Event`: Event data structure
- `EventBus`: Implementation of the event bus system
- `EventType`: Enum defining supported event types

### Decorators
- `require_permission`: Permission checking decorator
- `validate_input`: Input validation decorator
- `rate_limit`: Rate limiting decorator
- `log_execution`: Execution logging decorator
- `retry`: Retry mechanism decorator

### Utilities
- Logging setup utilities
- Configuration management
- Data sanitization
- Plugin ID generation

## License

MIT License