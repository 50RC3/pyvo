import logging
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.core.pyvo_monitor import pyvo_monitoring
from pyvo.core.pyvo_error_handling import pyvo_error_handling
from pyvo.core.pyvo_performance import pyvo_performance_tracking

class PyvoIntegrationPlugin:
    """
    This plugin integrates Pyvo functionality into an external system, providing hooks
    for monitoring, logging, performance tracking, and error handling.
    """
    
    def __init__(self, enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True):
        self.enable_monitoring = enable_monitoring
        self.enable_logging = enable_logging
        self.enable_performance = enable_performance
        self.enable_error_handling = enable_error_handling
        
        # Initialize PyvoIntegration
        self.pyvo_integration = PyvoIntegration(
            enable_monitoring=self.enable_monitoring,
            enable_logging=self.enable_logging,
            enable_performance=self.enable_performance,
            enable_error_handling=self.enable_error_handling
        )

    def integrate_function(self, func):
        """
        Integrates the provided function with Pyvo functionality, enabling monitoring,
        logging, performance tracking, and error handling based on the plugin settings.
        """
        if self.enable_monitoring:
            func = self._apply_monitoring(func)  # Apply Pyvo monitoring functionality
        if self.enable_logging:
            func = self._add_logging(func)  # Add logging functionality
        if self.enable_performance:
            func = pyvo_performance_tracking(func)  # Track performance of the function
        if self.enable_error_handling:
            func = pyvo_error_handling(func)  # Add error handling functionality
        return func
    
    def _apply_monitoring(self, func):
        """
        Apply monitoring functionality to a function.
        """
        return pyvo_monitoring(func)

    def _add_logging(self, func):
        """
        Adds logging functionality to a function by creating a wrapper that logs its calls.
        """
        def wrapper(*args, **kwargs):
            logging.info(f"Calling function {func.__name__} with arguments: {args}, {kwargs}")
            try:
                result = func(*args, **kwargs)
                logging.info(f"Function {func.__name__} returned: {result}")
                return result
            except Exception as e:
                logging.error(f"Error occurred in function {func.__name__} with arguments {args} and {kwargs}: {e}")
                raise
        return wrapper

    def log_summary(self):
        """
        Summarizes the logs collected from the integration. Displays logs and errors based on current configurations.
        """
        log_summary = []
        if self.enable_logging:
            log_summary.append("Logging is enabled.")
        if self.enable_monitoring:
            log_summary.append("Monitoring is enabled.")
        if self.enable_performance:
            log_summary.append("Performance tracking is enabled.")
        if self.enable_error_handling:
            log_summary.append("Error handling is enabled.")
        return log_summary

    def reset_integration(self):
        """
        Resets all integration settings to their default state (all features are enabled by default).
        """
        self.enable_monitoring = True
        self.enable_logging = True
        self.enable_performance = True
        self.enable_error_handling = True
        self.pyvo_integration = PyvoIntegration(
            enable_monitoring=self.enable_monitoring,
            enable_logging=self.enable_logging,
            enable_performance=self.enable_performance,
            enable_error_handling=self.enable_error_handling
        )
        logging.info("Pyvo integration settings have been reset to default.")

    def update_settings(self, enable_monitoring=None, enable_logging=None, enable_performance=None, enable_error_handling=None):
        """
        Dynamically update the integration settings based on user input or configuration changes.
        """
        if enable_monitoring is not None:
            self.enable_monitoring = enable_monitoring
        if enable_logging is not None:
            self.enable_logging = enable_logging
        if enable_performance is not None:
            self.enable_performance = enable_performance
        if enable_error_handling is not None:
            self.enable_error_handling = enable_error_handling
        
        # Only re-initialize PyvoIntegration if settings have been changed
        self.pyvo_integration = PyvoIntegration(
            enable_monitoring=self.enable_monitoring,
            enable_logging=self.enable_logging,
            enable_performance=self.enable_performance,
            enable_error_handling=self.enable_error_handling
        )
        logging.info("Pyvo integration settings have been updated.")

    def get_integration_status(self):
        """
        Returns the current status of the Pyvo integration settings.
        """
        status = {
            "Monitoring": self.enable_monitoring,
            "Logging": self.enable_logging,
            "Performance": self.enable_performance,
            "Error Handling": self.enable_error_handling
        }
        return status


# Example of how to use the plugin

def sample_function(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

# Initialize the plugin with desired settings
plugin = PyvoIntegrationPlugin(enable_logging=True, enable_monitoring=True, enable_performance=True, enable_error_handling=True)

# Integrate the sample function with Pyvo
integrated_function = plugin.integrate_function(sample_function)

# Test the integrated function
try:
    result = integrated_function(10, 2)
    print(f"Function result: {result}")
except Exception as e:
    print(f"Error: {e}")

# Display the current integration status
print(plugin.get_integration_status())

# Update the settings dynamically
plugin.update_settings(enable_logging=False)
print(plugin.get_integration_status())

# Log the summary of the integration
print(plugin.log_summary())

# Reset the integration settings to their defaults
plugin.reset_integration()
print(plugin.get_integration_status())

# This plugin can be used to wrap any function with the desired Pyvo functionality.
# The integrated_function can then be used just like the original function, but with the additional benefits of logging, performance tracking, and error handling.
# By using the plugin, developers can integrate Pyvo's capabilities into their applications without modifying their existing functions directly.
