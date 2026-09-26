"""
Data Models

This file defines the base data model classes and interfaces for module entities.
"""

from typing import Dict, List, Any, Optional
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

class PluginEntity(ModuleEntity):
    """Entity representing a plugin."""

    def get_entity_type(self) -> str:
        return "plugin"

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
