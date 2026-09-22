# LifeOS Common Module

The common module provides shared interfaces, base classes, and utilities for building plugins for the LifeOS platform. This module contains all the core functionality that plugins can use to interact with the platform.

## Features

- **Plugin Interface**: Standard contract for all plugins
- **Plugin Manager**: Lifecycle management of plugins
- **Data Models**: Base classes for data entities
- **Event System**: Communication between plugins and system components
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

## Components

### Plugin Interface
- `PluginInterface`: Abstract base interface for all plugins
- `PluginBase`: Base implementation with common functionality

### Plugin Manager
- `PluginManagerInterface`: Interface for plugin management operations
- `BasePluginManager`: Core implementation of plugin manager

### Data Models
- `BaseModel`: Base class for data models
- `DataModelMixin`: Utility functions for data models

### Event System
- `EventBusInterface`: Interface for event bus operations
- `Event`: Event data structure
- `EventBus`: Implementation of the event bus system

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