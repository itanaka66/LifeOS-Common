"""
Test suite for the unified LifeOS Common Module

This file contains tests for both plugin and module functionality.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the common directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common'))

from common.plugin_interface import PluginInterface, PluginBase
from common.plugin_manager import PluginManagerInterface, BasePluginManager
from common.module_interface import ModuleInterface, ModuleBase
from common.module_manager import ModuleManagerInterface, BaseModuleManager
from common.data_models import BaseModel
from common.event_system import EventBus, Event
from common.utils import setup_logging, generate_plugin_id


class TestPluginInterface(unittest.TestCase):
    """Test plugin interface functionality"""

    def test_plugin_base_implements_interface(self):
        """Test that PluginBase implements PluginInterface"""

        class TestPlugin(PluginBase):
            def __init__(self):
                super().__init__("test.plugin", "1.0.0", "Test Plugin")

            def get_data(self):
                return {"message": "Hello from test plugin"}

        plugin = TestPlugin()

        # Test that it has all required properties
        self.assertEqual(plugin.id, "test.plugin")
        self.assertEqual(plugin.name, "Test Plugin")
        self.assertEqual(plugin.version, "1.0.0")

        # Test that it implements the interface methods
        self.assertTrue(plugin.initialize())
        self.assertTrue(plugin.start())
        self.assertTrue(plugin.stop())
        self.assertIsNotNone(plugin.get_manifest())
        self.assertTrue(plugin.is_running())


class TestPluginManager(unittest.TestCase):
    """Test plugin manager functionality"""

    def test_plugin_manager_interface(self):
        """Test that BasePluginManager implements PluginManagerInterface"""

        manager = BasePluginManager()

        # Test interface methods exist
        self.assertTrue(hasattr(manager, 'register_plugin'))
        self.assertTrue(hasattr(manager, 'unregister_plugin'))
        self.assertTrue(hasattr(manager, 'get_plugin'))
        self.assertTrue(hasattr(manager, 'list_plugins'))
        self.assertTrue(hasattr(manager, 'install_plugin'))
        self.assertTrue(hasattr(manager, 'uninstall_plugin'))
        self.assertTrue(hasattr(manager, 'enable_plugin'))
        self.assertTrue(hasattr(manager, 'disable_plugin'))
        self.assertTrue(hasattr(manager, 'start_plugin'))
        self.assertTrue(hasattr(manager, 'stop_plugin'))


class TestModuleInterface(unittest.TestCase):
    """Test module interface functionality"""

    def test_module_base_implements_interface(self):
        """Test that ModuleBase implements ModuleInterface"""

        class TestModule(ModuleBase):
            def __init__(self):
                super().__init__("test.module", "1.0.0", "Test Module")

            def get_data(self):
                return {"message": "Hello from test module"}

        module = TestModule()

        # Test that it has all required properties
        self.assertEqual(module.id, "test.module")
        self.assertEqual(module.name, "Test Module")
        self.assertEqual(module.version, "1.0.0")

        # Test that it implements the interface methods
        self.assertTrue(module.initialize())
        self.assertTrue(module.start())
        self.assertTrue(module.stop())
        self.assertIsNotNone(module.get_manifest())
        self.assertTrue(module.is_running())


class TestModuleManager(unittest.TestCase):
    """Test module manager functionality"""

    def test_module_manager_interface(self):
        """Test that BaseModuleManager implements ModuleManagerInterface"""

        manager = BaseModuleManager()

        # Test interface methods exist
        self.assertTrue(hasattr(manager, 'register_module'))
        self.assertTrue(hasattr(manager, 'unregister_module'))
        self.assertTrue(hasattr(manager, 'get_module'))
        self.assertTrue(hasattr(manager, 'list_modules'))
        self.assertTrue(hasattr(manager, 'install_module'))
        self.assertTrue(hasattr(manager, 'uninstall_module'))
        self.assertTrue(hasattr(manager, 'enable_module'))
        self.assertTrue(hasattr(manager, 'disable_module'))
        self.assertTrue(hasattr(manager, 'start_module'))
        self.assertTrue(hasattr(manager, 'stop_module'))


class TestEventSystem(unittest.TestCase):
    """Test event system functionality"""

    def test_event_bus(self):
        """Test EventBus functionality"""

        event_bus = EventBus()
        self.assertIsNotNone(event_bus)

        # Test that it has the required methods
        self.assertTrue(hasattr(event_bus, 'publish'))
        self.assertTrue(hasattr(event_bus, 'subscribe'))
        self.assertTrue(hasattr(event_bus, 'unsubscribe'))


class TestDataModels(unittest.TestCase):
    """Test data models functionality"""

    def test_base_model(self):
        """Test BaseModel functionality"""

        class TestModel(BaseModel):
            name: str
            value: int = 0

        model = TestModel(name="test", value=42)
        self.assertEqual(model.name, "test")
        self.assertEqual(model.value, 42)


class TestUtils(unittest.TestCase):
    """Test utility functions"""

    def test_setup_logging(self):
        """Test logging setup"""

        # Just make sure it doesn't crash
        setup_logging()

    def test_generate_plugin_id(self):
        """Test plugin ID generation"""

        # Test that it generates a string
        plugin_id = generate_plugin_id("test")
        self.assertIsInstance(plugin_id, str)
        self.assertTrue(len(plugin_id) > 0)


if __name__ == '__main__':
    unittest.main()