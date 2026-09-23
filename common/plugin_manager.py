"""
Plugin Manager for LifeOS Platform
Manages the lifecycle of plugins including installation, loading, starting, and stopping.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type
import logging
import os
import json
from pathlib import Path

from .plugin_interface import PluginInterface


class PluginManagerInterface(ABC):
    """
    Interface for plugin management operations.

    Defines the standard methods that any plugin manager must implement.
    """

    @abstractmethod
    def register_plugin(self, plugin_class: Type[PluginInterface]) -> bool:
        """Register a plugin class with the system."""
        pass

    @abstractmethod
    def install_plugin(self, source_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Install a plugin from source."""
        pass

    @abstractmethod
    def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin."""
        pass

    @abstractmethod
    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin."""
        pass

    @abstractmethod
    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin."""
        pass

    @abstractmethod
    def start_plugin(self, plugin_id: str) -> bool:
        """Start a plugin."""
        pass

    @abstractmethod
    def stop_plugin(self, plugin_id: str) -> bool:
        """Stop a plugin."""
        pass

    @abstractmethod
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins."""
        pass

    @abstractmethod
    def get_plugin(self, plugin_id: str) -> Optional[PluginInterface]:
        """Get a specific plugin instance."""
        pass

    @abstractmethod
    def check_compatibility(self, plugin_manifest: Dict[str, Any]) -> bool:
        """Check if a plugin is compatible with the current system."""
        pass


class BasePluginManager(PluginManagerInterface):
    """
    Base implementation of PluginManagerInterface.

    Provides core functionality for managing plugins in a platform.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self._plugins: Dict[str, PluginInterface] = {}
        self._plugin_classes: Dict[str, Type[PluginInterface]] = {}
        self._logger = logging.getLogger("plugin.manager")
        self._config = config or {}
        self._loaded_plugins = set()

    def unregister_plugin(self, plugin_id: str) -> bool:
        """
        Unregister a plugin class from the system.

        Args:
            plugin_id: The ID of the plugin to unregister

        Returns:
            True if unregistration was successful
        """
        try:
            if plugin_id in self._plugin_classes:
                del self._plugin_classes[plugin_id]
                self._logger.info(f"Unregistered plugin: {plugin_id}")
                return True
            return False
        except Exception as e:
            self._logger.error(f"Failed to unregister plugin {plugin_id}: {e}")
            return False

    def register_plugin(self, plugin_class: Type[PluginInterface]) -> bool:
        """
        Register a plugin class with the system.

        Args:
            plugin_class: The plugin class to register

        Returns:
            True if registration was successful
        """
        try:
            # Create an instance to get the plugin ID
            instance = plugin_class()
            plugin_id = instance.id

            self._plugin_classes[plugin_id] = plugin_class
            self._logger.info(f"Registered plugin: {plugin_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to register plugin class: {e}")
            return False

    def install_plugin(self, source_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Install a plugin from source.

        Args:
            source_path: Path or URL to plugin source
            options: Installation options

        Returns:
            Installation result with status and metadata
        """
        try:
            # In a real implementation, this would:
            # 1. Download/extract plugin from source_path
            # 2. Validate plugin structure and manifest
            # 3. Install files to appropriate location
            # 4. Register in database

            self._logger.info(f"Installing plugin from {source_path}")
            return {"status": "success", "message": f"Plugin installed from {source_path}"}
        except Exception as e:
            self._logger.error(f"Failed to install plugin from {source_path}: {e}")
            return {"status": "error", "message": str(e)}

    def uninstall_plugin(self, plugin_id: str) -> bool:
        """
        Uninstall a plugin.

        Args:
            plugin_id: The ID of the plugin to uninstall

        Returns:
            True if uninstallation was successful
        """
        try:
            # In a real implementation, this would:
            # 1. Stop the plugin if running
            # 2. Remove plugin files from disk
            # 3. Remove from database
            # 4. Clean up any resources

            if plugin_id in self._plugins:
                plugin = self._plugins[plugin_id]
                plugin.cleanup()
                del self._plugins[plugin_id]

            if plugin_id in self._plugin_classes:
                del self._plugin_classes[plugin_id]

            self._logger.info(f"Uninstalled plugin: {plugin_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to uninstall plugin {plugin_id}: {e}")
            return False

    def enable_plugin(self, plugin_id: str) -> bool:
        """
        Enable a plugin.

        Args:
            plugin_id: The ID of the plugin to enable

        Returns:
            True if enabling was successful
        """
        try:
            # Check if plugin exists and is registered
            if plugin_id not in self._plugin_classes:
                self._logger.warning(f"Plugin {plugin_id} not found")
                return False

            # If already loaded, just enable it
            if plugin_id in self._plugins:
                self._logger.info(f"Plugin {plugin_id} already loaded")
                return True

            # Create and load the plugin
            plugin_class = self._plugin_classes[plugin_id]
            plugin_instance = plugin_class()

            # Initialize with default config
            plugin_instance.initialize({})

            # Start the plugin
            if plugin_instance.start():
                self._plugins[plugin_id] = plugin_instance
                self._loaded_plugins.add(plugin_id)
                self._logger.info(f"Enabled plugin: {plugin_id}")
                return True
            else:
                self._logger.error(f"Failed to start plugin {plugin_id}")
                return False

        except Exception as e:
            self._logger.error(f"Failed to enable plugin {plugin_id}: {e}")
            return False

    def disable_plugin(self, plugin_id: str) -> bool:
        """
        Disable a plugin.

        Args:
            plugin_id: The ID of the plugin to disable

        Returns:
            True if disabling was successful
        """
        try:
            # Check if plugin is loaded
            if plugin_id not in self._plugins:
                self._logger.warning(f"Plugin {plugin_id} not loaded")
                return False

            # Stop the plugin
            plugin = self._plugins[plugin_id]
            if plugin.stop():
                plugin.cleanup()
                del self._plugins[plugin_id]
                self._loaded_plugins.discard(plugin_id)
                self._logger.info(f"Disabled plugin: {plugin_id}")
                return True
            else:
                self._logger.error(f"Failed to stop plugin {plugin_id}")
                return False

        except Exception as e:
            self._logger.error(f"Failed to disable plugin {plugin_id}: {e}")
            return False

    def start_plugin(self, plugin_id: str) -> bool:
        """
        Start a plugin.

        Args:
            plugin_id: The ID of the plugin to start

        Returns:
            True if starting was successful
        """
        try:
            # If plugin is already loaded, just restart it
            if plugin_id in self._plugins:
                plugin = self._plugins[plugin_id]
                plugin.stop()
                plugin.start()
                self._logger.info(f"Restarted plugin: {plugin_id}")
                return True

            # Load and start the plugin
            if plugin_id in self._plugin_classes:
                plugin_class = self._plugin_classes[plugin_id]
                plugin_instance = plugin_class()

                # Initialize with default config
                plugin_instance.initialize({})

                if plugin_instance.start():
                    self._plugins[plugin_id] = plugin_instance
                    self._loaded_plugins.add(plugin_id)
                    self._logger.info(f"Started plugin: {plugin_id}")
                    return True
                else:
                    self._logger.error(f"Failed to start plugin {plugin_id}")
                    return False
            else:
                self._logger.warning(f"Plugin {plugin_id} not found")
                return False

        except Exception as e:
            self._logger.error(f"Failed to start plugin {plugin_id}: {e}")
            return False

    def stop_plugin(self, plugin_id: str) -> bool:
        """
        Stop a plugin.

        Args:
            plugin_id: The ID of the plugin to stop

        Returns:
            True if stopping was successful
        """
        try:
            # Check if plugin is loaded
            if plugin_id not in self._plugins:
                self._logger.warning(f"Plugin {plugin_id} not loaded")
                return False

            # Stop the plugin
            plugin = self._plugins[plugin_id]
            if plugin.stop():
                plugin.cleanup()
                del self._plugins[plugin_id]
                self._loaded_plugins.discard(plugin_id)
                self._logger.info(f"Stopped plugin: {plugin_id}")
                return True
            else:
                self._logger.error(f"Failed to stop plugin {plugin_id}")
                return False

        except Exception as e:
            self._logger.error(f"Failed to stop plugin {plugin_id}: {e}")
            return False

    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        List all installed plugins.

        Returns:
            List of plugin information dictionaries
        """
        plugins = []
        for plugin_id, plugin_class in self._plugin_classes.items():
            try:
                instance = plugin_class()
                manifest = instance.get_manifest()
                manifest["status"] = "installed" if plugin_id in self._plugins else "installed"
                plugins.append(manifest)
            except Exception as e:
                self._logger.error(f"Error getting manifest for {plugin_id}: {e}")
                plugins.append({
                    "id": plugin_id,
                    "name": "Unknown",
                    "version": "unknown",
                    "status": "error"
                })
        return plugins

    def get_plugin(self, plugin_id: str) -> Optional[PluginInterface]:
        """
        Get a specific plugin instance.

        Args:
            plugin_id: The ID of the plugin to retrieve

        Returns:
            Plugin instance or None if not found
        """
        return self._plugins.get(plugin_id)

    def check_compatibility(self, plugin_manifest: Dict[str, Any]) -> bool:
        """
        Check if a plugin is compatible with the current system.

        Args:
            plugin_manifest: The manifest of the plugin to check

        Returns:
            True if compatible, False otherwise
        """
        # In a real implementation, this would check:
        # - Minimum platform version
        # - Required dependencies
        # - Supported features

        try:
            min_version = plugin_manifest.get("min_version", "1.0.0")
            # Add compatibility checking logic here
            self._logger.info(f"Compatibility check for plugin {plugin_manifest.get('id', 'unknown')}")
            return True
        except Exception as e:
            self._logger.error(f"Error during compatibility check: {e}")
            return False

    def get_plugin_config(self, plugin_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific plugin.

        Args:
            plugin_id: The ID of the plugin

        Returns:
            Plugin configuration dictionary
        """
        # In a real implementation, this would retrieve from database or config files
        if plugin_id in self._plugins:
            return getattr(self._plugins[plugin_id], '_config', {})
        return {}