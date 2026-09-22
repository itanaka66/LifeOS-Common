"""
Configuration Schema

This file contains the configuration schemas for modules.
"""

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