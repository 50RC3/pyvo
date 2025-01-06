import logging
import time
import os
from pyvo.core.pyvo_performance import track_performance
from pyvo.core.pyvo_error_handling import log_error
from pyvo.core.pyvo_dashboard import update_dashboard

class PerformancePlugin:
    """
    Performance Plugin for Pyvo to track the performance of functions.
    This includes measuring execution time, handling errors, logging, and updating a custom dashboard.
    """

    def __init__(self, logging_enabled=True, dashboard_enabled=True, log_file_path=None):
        """
        Initializes the performance plugin with optional logging and dashboard integration.
        
        :param logging_enabled: Boolean flag to enable/disable logging of errors and performance data.
        :param dashboard_enabled: Boolean flag to enable/disable updating the dashboard with metrics.
        :param log_file_path: Path to the log file. If None, default path will be used.
        """
        self.logging_enabled = logging_enabled
        self.dashboard_enabled = dashboard_enabled
        self.logger = logging.getLogger('PerformancePlugin')
        self.logger.setLevel(logging.DEBUG)

        # Set the log file path or use the default path
        log_file_path = log_file_path or os.getenv('LOG_FILE_PATH', 'performance_plugin.log')

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
        # Here we integrate it with Pyvo's performance tracking system
        track_performance(func_name, execution_time, success, error_message)

    def update_custom_dashboard(self, func_name, execution_time, success, error_message=None):
        """
        Updates a custom dashboard with real-time performance metrics.
        
        :param func_name: The name of the function being tracked.
        :param execution_time: Time taken by the function to execute.
        :param success: Boolean indicating whether the function was successful.
        :param error_message: Error message if the function fails (optional).
        """
        if self.dashboard_enabled:
            # Using Pyvo's dashboard update function for real-time tracking
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
                # Call the actual function
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                # Send data to custom system and update the custom dashboard
                self.send_to_custom_system(func.__name__, execution_time, success=True)
                self.update_custom_dashboard(func.__name__, execution_time, success=True)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                # Log the error and send data to the custom system and update the dashboard
                self.send_to_custom_system(func.__name__, execution_time, success=False, error_message=str(e))
                self.update_custom_dashboard(func.__name__, execution_time, success=False, error_message=str(e))
                log_error(e)  # Pyvo error handler integration
                raise e  # Re-raise the exception

        return wrapper

    def reset_custom_metrics(self):
        """
        Resets the performance metrics stored in the custom dashboard or external system.
        This could be triggered by the user through the UI.
        """
        if self.dashboard_enabled:
            update_dashboard(reset=True)  # Reset the custom dashboard metrics
        # Optionally, reset metrics in an external system if required
        self.logger.info("Custom performance metrics have been reset.")

    def enable_logging(self, level=logging.DEBUG):
        """
        Enable or disable logging of function calls, performance, and errors for the performance plugin.
        
        :param level: The logging level to set (default is DEBUG).
        """
        self.logger.setLevel(level)
        self.logger.info(f"Logging level set to {logging.getLevelName(level)}.")

# Example Usage:
# Initialize the performance plugin
performance_plugin = PerformancePlugin(logging_enabled=True, dashboard_enabled=True)

# Use the decorator to track function performance
@performance_plugin.track_function_performance
def example_function(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed.")
    return x / y

# Call the function
try:
    result = example_function(10, 2)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error occurred: {str(e)}")

# Reset custom metrics
performance_plugin.reset_custom_metrics()

# Disable logging for the performance plugin
performance_plugin.enable_logging(logging.CRITICAL)

# This plugin can be customized to fit specific needs, allowing users to extend or modify the core functionality of Pyvo according to their requirements.
