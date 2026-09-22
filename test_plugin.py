from common.plugin_interface import PluginBase
from common.plugin_config import PluginManifest, PluginConfig

# Test basic plugin implementation
class TestPlugin(PluginBase):
    def __init__(self):
        super().__init__("test.plugin", "1.0.0", "Test Plugin")

    def get_manifest(self):
        manifest = super().get_manifest()
        manifest["description"] = "A test plugin for demonstration"
        return manifest

# Test instantiation
plugin = TestPlugin()
print(f"Plugin ID: {plugin.id}")
print(f"Plugin Name: {plugin.name}")
print(f"Plugin Version: {plugin.version}")

# Test manifest
manifest = plugin.get_manifest()
print(f"Manifest: {manifest}")

# Test configuration
config = {"test": "value"}
plugin.initialize(config)
print(f"Plugin initialized with config: {plugin._config}")