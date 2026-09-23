"""
Data Models for LifeOS Platform Plugins
Defines base data models and utilities for plugin data management.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class BaseModel(ABC):
    """
    Base class for all data models in the platform.

    Provides common functionality for data models including serialization,
    validation, and basic CRUD operations.
    """

    def __init__(self, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        Returns:
            Dictionary representation of the model
        """
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Initialize model from dictionary.

        Args:
            data: Dictionary with model data
        """
        pass

    def to_json(self) -> str:
        """
        Convert model instance to JSON string.

        Returns:
            JSON representation of the model
        """
        import json
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """
        Create model instance from JSON string.

        Args:
            json_str: JSON string representation

        Returns:
            Model instance
        """
        import json
        data = json.loads(json_str)
        instance = cls()
        instance.from_dict(data)
        return instance

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __eq__(self, other) -> bool:
        """Compare two models for equality."""
        if not isinstance(other, BaseModel):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash the model based on its ID."""
        return hash(self.id)


class DataModelMixin:
    """
    Mixin class providing common data model utilities.

    This mixin can be used to add additional functionality to data models.
    """

    @staticmethod
    def validate_field(field_name: str, value: Any, field_type: type, required: bool = True) -> bool:
        """
        Validate a field value against its expected type.

        Args:
            field_name: Name of the field
            value: Value to validate
            field_type: Expected type
            required: Whether the field is required

        Returns:
            True if valid, False otherwise
        """
        if required and value is None:
            return False
        if value is not None and not isinstance(value, field_type):
            return False
        return True

    @staticmethod
    def validate_dict(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
        """
        Validate a dictionary against a schema.

        Args:
            data: Dictionary to validate
            schema: Schema mapping field names to expected types

        Returns:
            True if valid, False otherwise
        """
        for field_name, expected_type in schema.items():
            if field_name not in data:
                continue  # Optional fields don't need to be present
            if not isinstance(data[field_name], expected_type):
                return False
        return True


class PluginEntity(BaseModel):
    """
    Base class for plugin entities.

    Represents a core entity that plugins can work with.
    """

    def __init__(self, id: Optional[str] = None, name: str = "", description: str = ""):
        super().__init__(id)
        self.name = name
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Initialize entity from dictionary."""
        self.id = data.get("id", self.id)
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else self.created_at
        self.updated_at = datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else self.updated_at


class PluginDataManager:
    """
    Data manager for plugin-related data operations.

    Provides utility methods for managing plugin entities and data.
    """

    def __init__(self):
        self._entities: Dict[str, PluginEntity] = {}

    def register_entity(self, entity: PluginEntity) -> None:
        """Register an entity."""
        self._entities[entity.id] = entity

    def get_entity(self, entity_id: str) -> Optional[PluginEntity]:
        """Get an entity by ID."""
        return self._entities.get(entity_id)

    def list_entities(self) -> Dict[str, PluginEntity]:
        """List all registered entities."""
        return self._entities.copy()

    def update_entity(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """Update an entity with new data."""
        if entity_id in self._entities:
            entity = self._entities[entity_id]
            entity.from_dict(data)
            entity.update_timestamp()
            return True
        return False

    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity."""
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False