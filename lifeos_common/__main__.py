"""
Main entry point for the common module.
This file provides initialization and setup for the common module.
"""

import sys
import os

# Add the parent directory to the Python path so we can import from it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from . import *

def main():
    """Main entry point for the common module."""
    print("LifeOS Common Module")
    print("====================")
    print("Version: 1.0.0")
    print("Author: LifeOS Team")
    print("\nAvailable components:")
    print("- PluginInterface")
    print("- PluginManagerInterface")
    print("- BasePluginManager")
    print("- PluginManifest")
    print("- PluginConfig")
    print("- BaseModel")
    print("- DataModelMixin")
    print("- EventBusInterface")
    print("- Event")
    print("- EventBus")
    print("- Decorators")
    print("- Utilities")

if __name__ == "__main__":
    main()