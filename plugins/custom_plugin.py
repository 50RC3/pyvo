import logging
import time
from pyvo.core.pyvo_performance import track_performance
from pyvo.core.pyvo_error_handling import log_error
from pyvo.core.pyvo_dashboard import update_dashboard

class CustomPlugin:
    """
    Custom Plugin for Pyvo to extend its functionality.
    This can include tracking performance, handling errors, or integrating with other systems.
    """

    def __init__(self, logging_enabled=True, dashboard_enabled=True, log_file_path='custom_plugin.log'):
        """
        Initializes the custom plugin with optional logging and dashboard integration.
        
        :param logging_enabled: Boolean flag to enable/disable logging of errors and performance data.
        :param dashboard_enabled: Boolean flag to enable/disable updating the dashboard with metrics.
        :param log_file_path: Path to the log file.
        """
        self.logging_enabled = logging_enabled
        self.dashboard_enabled = dashboard_enabled
        self.logger = logging.getLogger('CustomPlugin')
        self.logger.setLevel(logging.DEBUG)

        # Add a file handler for logging errors and performance data
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def send_to_custom_system(self, func_name, execution_time, success, error_message=None):
        """
        Sends function performance data and errors to a custom external system.
        
        :param func_name: The name of the function being monitored.
        :param execution_time: Time taken by the function to execute.
        :param success: Boolean indicating whether the function was successful.
        :param error_message: Error message if the function fails (optional).
        """
        if self.logging_enabled:
            self.logger.info(f"Function: {func_name}, Execution Time: {execution_time}s, Success: {success}")
            if error_message:
                self.logger.error(f"Error: {error_message}")

        # Example: Send data to a custom system (like a database, API, etc.)
        # You can extend this to integrate with external services like Datadog, Prometheus, etc.

    def update_custom_dashboard(self, func_name, execution_time, success, error_message=None):
        """
        Updates a custom dashboard with real-time performance metrics.
        
        :param func_name: The name of the function being tracked.
        :param execution_time: Time taken by the function to execute.
        :param success: Boolean indicating whether the function was successful.
        :param error_message: Error message if the function fails (optional).
        """
        if self.dashboard_enabled:
            update_dashboard(func_name, execution_time, success, error_message)

    def track_function_performance(self, func):
        """
        Decorator for tracking function performance and handling errors.
        
        :param func: The function to be decorated for performance tracking.
        :return: Wrapped function.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                self.send_to_custom_system(func.__name__, execution_time, success=True)
                self.update_custom_dashboard(func.__name__, execution_time, success=True)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                self.send_to_custom_system(func.__name__, execution_time, success=False, error_message=str(e))
                self.update_custom_dashboard(func.__name__, execution_time, success=False, error_message=str(e))
                log_error(e)
                raise e  # Re-raise the exception

        return wrapper

    def reset_custom_metrics(self):
        """
        Resets the performance metrics stored in the custom dashboard or external system.
        """
        if self.dashboard_enabled:
            update_dashboard(reset=True)
        self.logger.info("Custom performance metrics have been reset.")

    def enable_logging(self, level=logging.DEBUG):
        """
        Enable or disable logging of function calls, performance, and errors for the custom plugin.
        
        :param level: The logging level to set (default is DEBUG).
        """
        self.logger.setLevel(level)
        self.logger.info(f"Logging level set to {logging.getLevelName(level)}.")

# Example Usage
custom_plugin = CustomPlugin(logging_enabled=True, dashboard_enabled=True)

@custom_plugin.track_function_performance
def example_function(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed.")
    return x / y

try:
    result = example_function(10, 2)
except Exception as e:
    print(f"Error occurred: {str(e)}")

# Reset custom metrics
custom_plugin.reset_custom_metrics()

# Disable logging
custom_plugin.enable_logging(logging.CRITICAL)
