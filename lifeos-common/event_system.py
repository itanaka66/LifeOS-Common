"""
Event System

This file provides the event bus system interface for module communication.
"""

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