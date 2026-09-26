"""
Event System

This file provides the event bus system interface and implementation for module communication.
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

class EventBus(EventBusInterface):
    """
    Concrete implementation of EventBusInterface.
    """

    def __init__(self):
        self._subscriptions: Dict[EventType, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> str:
        import uuid
        sub_id = str(uuid.uuid4())
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(callback)
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        # Simplified unsubscribe logic
        return True

    def publish(self, event: Event) -> None:
        callbacks = self._subscriptions.get(event.event_type, [])
        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")

    def get_subscriptions(self, event_type: EventType) -> List[str]:
        return [str(i) for i in range(len(self._subscriptions.get(event_type, [])))]
