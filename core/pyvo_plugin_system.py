import importlib
import logging
import sys
import os
import functools
import types

# Set up logging for plugin-related activities with flexibility
def setup_logging():
    logger = logging.getLogger("pyvo_plugin_system")
    logger.setLevel(logging.INFO)
    
    # Stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # File handler for logging to file
    file_handler = logging.FileHandler('pyvo_plugin_system.log', mode='a')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

class PyvoPluginSystem:
    def __init__(self):
        self.plugins = {}  # A dictionary to store active plugins
        self.plugin_modules = []  # List to store plugin modules
        self.plugin_handlers = {}  # Dictionary to store plugin-specific handlers
        
    def load_plugin(self, plugin_name):
        try:
            if plugin_name not in self.plugins:
                plugin_module = importlib.import_module(f"pyvo.plugins.{plugin_name}")
                self.plugin_modules.append(plugin_module)
                self.plugins[plugin_name] = plugin_module
                logger.info(f"Plugin '{plugin_name}' loaded successfully.")
            else:
                logger.info(f"Plugin '{plugin_name}' is already loaded.")
        except ImportError as e:
            logger.error(f"Error loading plugin '{plugin_name}': {str(e)}")
    
    def integrate_plugin(self, plugin_name, function=None, class_method=False):
        try:
            plugin = self.plugins.get(plugin_name)
            if not plugin:
                raise ValueError(f"Plugin '{plugin_name}' is not loaded.")
            
            if hasattr(plugin, 'integrate'):
                integrate_function = plugin.integrate
                if class_method:
                    return functools.partial(integrate_function, target=class_method)
                else:
                    return integrate_function(function)
            else:
                raise AttributeError(f"Plugin '{plugin_name}' does not have an 'integrate' function.")
        except Exception as e:
            logger.error(f"Error integrating plugin '{plugin_name}': {str(e)}")

    def get_plugin(self, plugin_name):
        return self.plugins.get(plugin_name)

    def list_plugins(self):
        return list(self.plugins.keys())

    def unload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logger.info(f"Plugin '{plugin_name}' unloaded successfully.")
        else:
            logger.warning(f"Plugin '{plugin_name}' is not loaded.")
    
    def add_plugin_handler(self, plugin_name, handler_function):
        self.plugin_handlers[plugin_name] = handler_function
        logger.info(f"Custom handler added for plugin '{plugin_name}'.")

    def call_plugin_handler(self, plugin_name, *args, **kwargs):
        handler = self.plugin_handlers.get(plugin_name)
        if handler:
            try:
                handler(*args, **kwargs)
                logger.info(f"Custom handler for plugin '{plugin_name}' executed.")
            except Exception as e:
                logger.error(f"Error executing handler for plugin '{plugin_name}': {str(e)}")
        else:
            logger.warning(f"No handler found for plugin '{plugin_name}'.")

    def auto_load_plugins(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), '../../plugins')
        if os.path.isdir(plugin_dir):
            for plugin_filename in os.listdir(plugin_dir):
                if plugin_filename.endswith('.py') and plugin_filename != '__init__.py':
                    plugin_name = plugin_filename[:-3]  # Strip '.py' extension
                    self.load_plugin(plugin_name)
        else:
            logger.warning("No plugins directory found.")
    
    def apply_to_function(self, function_name, plugin_name):
        try:
            target_function = globals().get(function_name)
            if target_function and isinstance(target_function, types.FunctionType):
                self.integrate_plugin(plugin_name, target_function)
                logger.info(f"Plugin '{plugin_name}' applied to function '{function_name}'.")
            else:
                logger.warning(f"Function '{function_name}' not found or invalid.")
        except Exception as e:
            logger.error(f"Error applying plugin '{plugin_name}' to function '{function_name}': {str(e)}")
