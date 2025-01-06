"""
This module is responsible for initializing the Pyvo plugins package.
It provides an interface for dynamic loading and management of various plugins 
that extend the functionality of Pyvo.
"""

# Import necessary plugins for use in the Pyvo framework
from .pyvo_integration_plugin import CustomIntegrationPlugin
from .performance_plugin import CustomPerformancePlugin
from .logging_plugin import CustomLoggingPlugin
from .external_monitor_plugin import ExternalMonitorPlugin
from .custom_plugin import CustomPlugin

# Define a list of all available plugins in this package for easy access
available_plugins = [
    CustomIntegrationPlugin,
    CustomPerformancePlugin,
    CustomLoggingPlugin,
    ExternalMonitorPlugin,
    CustomPlugin
]

def load_plugin(plugin_class, **kwargs):
    """
    Dynamically loads a specified plugin class and initializes it with optional configurations.
    This can be used to initialize and configure specific plugins based on the requirements.

    :param plugin_class: The plugin class to load.
    :param kwargs: Optional keyword arguments for configuring the plugin.
    :return: An instance of the specified plugin class.
    """
    if plugin_class not in available_plugins:
        raise ValueError(f"Plugin {plugin_class.__name__} not found in available plugins.")
    
    try:
        # Instantiate and return the plugin class, passing any extra configuration parameters
        return plugin_class(**kwargs)
    except Exception as e:
        raise RuntimeError(f"Failed to load plugin {plugin_class.__name__}: {str(e)}")

def load_all_plugins():
    """
    Loads all available plugins in the Pyvo plugins package.

    :return: A list of instantiated plugin objects.
    """
    plugins = []
    for plugin in available_plugins:
        try:
            plugins.append(load_plugin(plugin))
        except Exception as e:
            print(f"Error loading plugin {plugin.__name__}: {e}")
    return plugins

# Example initialization: Automatically load all plugins when the package is imported
loaded_plugins = load_all_plugins()

# Optionally, expose all the loaded plugins for direct access
__all__ = ['CustomIntegrationPlugin', 'CustomPerformancePlugin', 'CustomLoggingPlugin', 'ExternalMonitorPlugin', 'CustomPlugin', 'loaded_plugins']

# Example of how to load a single plugin with configuration:
if __name__ == "__main__":
    try:
        plugin_config = {'logging_enabled': True, 'dashboard_enabled': False}
        performance_plugin = load_plugin(CustomPerformancePlugin, **plugin_config)
        print(f"Loaded plugin: {performance_plugin.__class__.__name__}")
    except Exception as e:
        print(f"Error loading plugin: {e}")
