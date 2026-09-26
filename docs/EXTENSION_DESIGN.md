# Extension Design for LifeOS Platform

## Overview

This document defines the common design patterns and interfaces for developing extensions (modules) for the LifeOS platform. The design ensures that extensions can be developed in separate repositories while maintaining compatibility with the main application. Extensions are implemented as independent modules that can run as Linux services, Docker containers, or any other execution environment, integrating with the core platform through well-defined communication mechanisms.

## Architecture Principles

### 1. Separation of Concerns
- Main application provides core functionality and runtime environment
- Extensions provide domain-specific features as independent modules
- Clear boundaries between core and extension components

### 2. Modular Architecture
- Extensions are implemented as independent modules
- Modules can run as Linux services, Docker containers, or other execution environments
- Services communicate through well-defined APIs and message queues
- Each module runs in its own process with isolated resources

### 3. Version Compatibility
- Stable API contracts for extensions
- Semantic versioning for both core and extensions
- Migration paths for breaking changes

## Common Design Structure

### 1. Module Interface Definition

```python
# module_interface.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from uuid import UUID

class ModuleInterface(ABC):
    """Base interface that all LifeOS modules must implement."""
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the module."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the module."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the module."""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module with configuration."""
        pass
    
    @abstractmethod
    def get_manifest(self) -> Dict[str, Any]:
        """Get module manifest information."""
        pass
    
    @abstractmethod
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints provided by this module."""
        pass
    
    @abstractmethod
    def get_entities(self) -> List[str]:
        """Get entity types provided by this module."""
        pass
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        """Get permissions required by this module."""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Start the module."""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop the module."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources when module is unloaded."""
        pass
```

### 2. Module Configuration Schema

```python
# config_schema.py
from typing import Dict, List, Optional
from pydantic import BaseModel

class ModuleConfig(BaseModel):
    """Configuration schema for modules."""
    
    # Core module information
    id: str
    version: str
    enabled: bool = True
    
    # Module type and execution details
    module_type: str  # e.g., "api", "worker", "daemon", "docker"
    execution_mode: str  # "local", "docker", "kubernetes"
    startup_mode: str  # "auto", "manual", "on-demand"
    
    # Resource configuration
    memory_limit: Optional[str] = None
    cpu_limit: Optional[str] = None
    restart_policy: str = "always"
    
    # Database configuration
    database: Optional[Dict[str, Any]] = None
    
    # API endpoints
    api_endpoints: List[Dict[str, Any]] = []
    
    # UI components
    ui_components: List[Dict[str, Any]] = []
    
    # Event subscriptions
    events: List[Dict[str, Any]] = []
    
    # Custom configuration
    custom_config: Dict[str, Any] = {}

class ModuleManifest(BaseModel):
    """Manifest file structure for modules."""
    
    # Basic metadata
    id: str
    version: str
    name: str
    description: str
    
    # Compatibility
    min_core_version: str
    max_core_version: Optional[str] = None
    
    # Dependencies
    dependencies: Dict[str, str] = {}
    
    # Requirements
    permissions: List[str] = []
    entities: List[str] = []
    
    # Module configuration
    module_type: str  # e.g., "api", "worker", "daemon", "docker"
    execution_mode: str = "local"
    startup_mode: str = "auto"
    
    # UI configuration
    ui: Optional[Dict[str, Any]] = None
    
    # AI tools
    ai_tools: List[str] = []
```

### 3. Module Manager Interface

```python
# module_manager.py
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from uuid import UUID

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
```

### 4. Common Event System

```python
# event_system.py
from typing import Dict, Any, Callable, List
from abc import ABC, abstractmethod
from enum import Enum
import time

class EventType(Enum):
    """Supported event types."""
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    DOCUMENT_CREATED = "document.created"
    MODULE_INSTALLED = "module.installed"
    MODULE_UNINSTALLED = "module.uninstalled"

class Event:
    """Event data structure."""
    
    def __init__(self, event_type: EventType, data: Dict[str, Any], 
                 source: str = "unknown", timestamp: float = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.timestamp = timestamp or time.time()

class EventBusInterface(ABC):
    """Interface for event bus system."""
    
    @abstractmethod
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> str:
        """Subscribe to an event type."""
        pass
    
    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from an event."""
        pass
    
    @abstractmethod
    def publish(self, event: Event) -> None:
        """Publish an event."""
        pass
    
    @abstractmethod
    def get_subscriptions(self, event_type: EventType) -> List[str]:
        """Get all subscriptions for an event type."""
        pass
```

### 5. Data Model Interface

```python
# data_models.py
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from uuid import UUID

class BaseModel(ABC):
    """Base model class for module data models."""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Initialize model from dictionary."""
        pass

class ModuleEntity(BaseModel):
    """Base class for module entities."""
    
    def __init__(self, id: Optional[UUID] = None, created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
    
    @abstractmethod
    def get_entity_type(self) -> str:
        """Get the type of entity."""
        pass

class ModuleDataManager(ABC):
    """Interface for data management in modules."""
    
    @abstractmethod
    def create_entity(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get_entity(self, entity_type: str, entity_id: UUID) -> Optional[Dict[str, Any]]:
        """Get an entity by ID."""
        pass
    
    @abstractmethod
    def update_entity(self, entity_type: str, entity_id: UUID, data: Dict[str, Any]) -> bool:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete_entity(self, entity_type: str, entity_id: UUID) -> bool:
        """Delete an entity."""
        pass
    
    @abstractmethod
    def list_entities(self, entity_type: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """List entities with optional filtering."""
        pass
```

## Extension Development Guidelines

### 1. Repository Structure

```
extension-repo/
├── extension_name/
━E  ├── __init__.py
━E  ├── manifest.py          # Extension manifest
━E  ├── extension.py         # Main extension class
━E  ├── api/                 # API endpoints
━E  ━E  ├── __init__.py
━E  ━E  └── endpoints.py
━E  ├── models/              # Data models
━E  ━E  ├── __init__.py
━E  ━E  └── entities.py
━E  ├── services/            # Business logic
━E  ━E  ├── __init__.py
━E  ━E  └── service.py
━E  ├── migrations/          # Database migrations
━E  ━E  └── versions/
━E  ━E      └── 0001_initial.py
━E  └── static/              # Static assets (UI, etc.)
━E      └── ui/
├── tests/
━E  └── test_extension.py
├── requirements.txt
├── setup.py
└── README.md
```

### 2. Module Implementation Example

```python
# example_module.py
from module_interface import ModuleInterface
from config_schema import ModuleManifest, ModuleConfig
import logging

class ExampleModule(ModuleInterface):
    """Example module implementation."""
    
    def __init__(self):
        self._id = "lifeos.example"
        self._version = "1.0.0"
        self._name = "Example Module"
        self._config = None
        self._logger = logging.getLogger(__name__)
        
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def name(self) -> str:
        return self._name
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module."""
        self._config = ModuleConfig(**config)
        self._logger.info(f"Example module initialized with config: {config}")
    
    def get_manifest(self) -> Dict[str, Any]:
        """Get module manifest."""
        return {
            "id": self._id,
            "version": self._version,
            "name": self._name,
            "description": "An example module for LifeOS",
            "min_core_version": "1.0.0"
        }
    
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get API endpoints."""
        return [
            {
                "path": "/example/health",
                "method": "GET",
                "handler": self.health_check
            },
            {
                "path": "/example/data",
                "method": "POST",
                "handler": self.process_data
            }
        ]
    
    def get_entities(self) -> List[str]:
        """Get entities provided."""
        return ["ExampleEntity"]
    
    def get_permissions(self) -> List[str]:
        """Get required permissions."""
        return ["example.read", "example.write"]
    
    def start(self) -> bool:
        """Start the module."""
        self._logger.info("Starting Example module")
        return True
    
    def stop(self) -> bool:
        """Stop the module."""
        self._logger.info("Stopping Example module")
        return True
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self._logger.info("Cleaning up Example module")
    
    # API endpoint handlers
    def health_check(self, request):
        return {"status": "healthy", "module": self._name}
    
    def process_data(self, request):
        data = request.json()
        # Process the data
        return {"result": "processed", "data": data}
```

### 3. Extension Installation Process

```python
# module_installer.py
import os
import json
from typing import Dict, Any
from pathlib import Path

class ModuleInstaller:
    """Handles module installation and management."""
    
    def __init__(self, module_dir: str = "./modules"):
        self.module_dir = Path(module_dir)
        self.module_dir.mkdir(exist_ok=True)
    
    def install_from_directory(self, module_path: str) -> Dict[str, Any]:
        """Install module from local directory."""
        # Copy files to module directory
        # Read manifest file
        # Register with module manager
        pass
    
    def install_from_package(self, package_name: str) -> Dict[str, Any]:
        """Install module from package repository."""
        # Download and extract package
        # Validate manifest
        # Install dependencies
        # Register with module manager
        pass
    
    def uninstall(self, module_id: str) -> bool:
        """Uninstall module."""
        # Remove files
        # Unregister from module manager
        # Clean up database entries
        pass
    
    def validate_manifest(self, manifest_path: str) -> bool:
        """Validate module manifest file."""
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Validate required fields
            required_fields = ['id', 'version', 'name']
            for field in required_fields:
                if field not in manifest:
                    return False
            
            return True
        except Exception:
            return False
```

## Integration with Main Application

### 1. Import Structure

Main application imports:
```python
# main_app.py
from src.api.module_interface import ModuleInterface
from src.service.module_manager import ModuleManagerInterface
from src.models.config_schema import ModuleManifest, ModuleConfig
from src.api.event_system import EventBusInterface, Event

# Module modules import from common design:
# In module code:
from src.api.module_interface import ModuleInterface
from src.models.data_models import ModuleEntity, ModuleDataManager
from src.models.config_schema import ModuleConfig
```

### 2. Runtime Integration

```python
# main_application.py
from module_manager import ModuleManager
from event_bus import EventBus

class LifeOSApplication:
    def __init__(self):
        self.module_manager = ModuleManager()
        self.event_bus = EventBus()
        self._load_modules()
    
    def _load_modules(self):
        """Load all registered modules."""
        # Scan module directories
        # Load manifest files
        # Initialize each module
        pass
    
    def register_module(self, module_class):
        """Register a module with the system."""
        self.module_manager.register_module(module_class)
    
    def get_module_api_endpoints(self):
        """Get all API endpoints from modules."""
        endpoints = []
        for mod in self.module_manager.list_modules():
            endpoints.extend(mod.get_endpoints())
        return endpoints
```

## Version Compatibility

### 1. Semantic Versioning

Extensions should follow semantic versioning:
- MAJOR: Breaking changes to API or functionality
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### 2. Compatibility Check

```python
def check_compatibility(module_manifest: ModuleManifest, 
                       core_version: str) -> bool:
    """Check if module is compatible with core version."""
    
    # Check minimum core version
    if compare_versions(core_version, module_manifest.min_core_version) < 0:
        return False
    
    # Check maximum core version
    if (module_manifest.max_core_version and 
        compare_versions(core_version, module_manifest.max_core_version) > 0):
        return False
    
    return True
```

## Best Practices

### 1. Testing
- Write comprehensive unit tests for modules
- Include integration tests with main application
- Test edge cases and error conditions
- Provide test fixtures for common scenarios

### 2. Documentation
- Include README.md with installation instructions
- Document API endpoints clearly
- Provide usage examples
- Include configuration options

### 3. Security
- Validate all inputs from modules
- Implement proper access controls
- Use secure communication patterns
- Regular security audits

This common design ensures that modules can be developed in separate repositories while maintaining compatibility with the main LifeOS application through well-defined interfaces and standardized data structures.
