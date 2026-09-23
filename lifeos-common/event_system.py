"""
Event System for LifeOS Platform Plugins
Defines the event bus and event handling mechanisms for plugin communication.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
import logging


# Define event types enum
from enum import Enum

class EventType(Enum):
    """
    Enum defining supported event types in the LifeOS platform.

    These are standard event types that plugins and modules can use to
    communicate within the system.
    """
    PLUGIN_STARTED = "plugin.started"
    PLUGIN_STOPPED = "plugin.stopped"
    MODULE_STARTED = "module.started"
    MODULE_STOPPED = "module.stopped"
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    DATA_CHANGED = "data.changed"
    CONFIGURATION_CHANGED = "config.changed"
    ERROR_OCCURRED = "error.occurred"


@dataclass
class Event:
    """
    Represents an event in the system.

    Events are used to communicate between plugins and the core system.
    """

    id: str
    name: str
    source: str
    timestamp: datetime
    data: Dict[str, Any]
    priority: int = 0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize event fields."""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "priority": self.priority,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create event from dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            source=data.get("source"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            data=data.get("data", {}),
            priority=data.get("priority", 0),
            metadata=data.get("metadata", {})
        )


class EventBusInterface(ABC):
    """
    Interface for event bus operations.

    Defines the standard methods that any event bus must implement.
    """

    @abstractmethod
    def publish(self, event: Event) -> bool:
        """Publish an event to the bus."""
        pass

    @abstractmethod
    def subscribe(self, event_name: str, handler: Callable[[Event], None], priority: int = 0) -> bool:
        """Subscribe to events of a specific type."""
        pass

    @abstractmethod
    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> bool:
        """Unsubscribe from events of a specific type."""
        pass

    @abstractmethod
    def get_subscribers(self, event_name: str) -> List[Callable[[Event], None]]:
        """Get list of subscribers for an event type."""
        pass

    @abstractmethod
    def get_event_history(self, limit: int = 100) -> List[Event]:
        """Get recent events from history."""
        pass


class EventBus(EventBusInterface):
    """
    Implementation of the event bus system.

    Provides a mechanism for plugins to communicate through events.
    """

    def __init__(self, max_history: int = 1000):
        self._subscribers: Dict[str, List[tuple]] = {}  # event_name -> [(priority, handler)]
        self._event_history: List[Event] = []
        self._max_history = max_history
        self._logger = logging.getLogger("event.bus")
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the event bus."""
        self._initialized = True
        self._logger.info("Event bus initialized")

    def publish(self, event: Event) -> bool:
        """
        Publish an event to the bus.

        Args:
            event: The event to publish

        Returns:
            True if successful, False otherwise
        """
        if not self._initialized:
            self.initialize()

        try:
            # Add to history
            self._event_history.append(event)
            if len(self._event_history) > self._max_history:
                self._event_history.pop(0)

            # Notify subscribers
            subscribers = self._subscribers.get(event.name, [])
            # Sort by priority (higher first)
            subscribers.sort(key=lambda x: x[0], reverse=True)

            for priority, handler in subscribers:
                try:
                    handler(event)
                except Exception as e:
                    self._logger.error(f"Error in event handler for {event.name}: {e}")

            self._logger.debug(f"Published event: {event.name}")
            return True

        except Exception as e:
            self._logger.error(f"Failed to publish event {event.name}: {e}")
            return False

    def subscribe(self, event_name: str, handler: Callable[[Event], None], priority: int = 0) -> bool:
        """
        Subscribe to events of a specific type.

        Args:
            event_name: Name of the event to subscribe to
            handler: Function to call when event occurs
            priority: Priority of this handler (higher numbers execute first)

        Returns:
            True if successful, False otherwise
        """
        try:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []

            # Check if handler is already subscribed
            for existing_priority, existing_handler in self._subscribers[event_name]:
                if existing_handler == handler:
                    return True  # Already subscribed

            self._subscribers[event_name].append((priority, handler))
            self._logger.debug(f"Subscribed to event: {event_name}")
            return True

        except Exception as e:
            self._logger.error(f"Failed to subscribe to event {event_name}: {e}")
            return False

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> bool:
        """
        Unsubscribe from events of a specific type.

        Args:
            event_name: Name of the event to unsubscribe from
            handler: Function that was subscribed

        Returns:
            True if successful, False otherwise
        """
        try:
            if event_name in self._subscribers:
                self._subscribers[event_name] = [
                    (priority, h) for priority, h in self._subscribers[event_name]
                    if h != handler
                ]
                self._logger.debug(f"Unsubscribed from event: {event_name}")
                return True
            return False

        except Exception as e:
            self._logger.error(f"Failed to unsubscribe from event {event_name}: {e}")
            return False

    def get_subscribers(self, event_name: str) -> List[Callable[[Event], None]]:
        """
        Get list of subscribers for an event type.

        Args:
            event_name: Name of the event

        Returns:
            List of subscriber handlers
        """
        subscribers = self._subscribers.get(event_name, [])
        return [handler for priority, handler in subscribers]

    def get_event_history(self, limit: int = 100) -> List[Event]:
        """
        Get recent events from history.

        Args:
            limit: Maximum number of events to return

        Returns:
            List of recent events
        """
        return self._event_history[-limit:]

    def clear_history(self) -> None:
        """Clear the event history."""
        self._event_history.clear()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the event bus.

        Returns:
            Dictionary with event bus statistics
        """
        return {
            "total_subscribers": sum(len(subs) for subs in self._subscribers.values()),
            "total_events": len(self._event_history),
            "event_types": list(self._subscribers.keys())
        }