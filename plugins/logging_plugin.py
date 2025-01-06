import logging
import time
import psutil
import os

class LoggingPlugin:
    def __init__(self):
        # Set up the logger
        self.logger = logging.getLogger('LoggingPlugin')
        self.logger.setLevel(logging.INFO)
        
        # Create a console handler and set the logging level
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def log_custom_message(self, level, message):
        """
        Logs a custom message at the specified level.
        :param level: Log level (e.g., 'INFO', 'ERROR', 'DEBUG')
        :param message: The message to be logged
        """
        if level == 'DEBUG':
            self.logger.debug(message)
        elif level == 'INFO':
            self.logger.info(message)
        elif level == 'ERROR':
            self.logger.error(message)
        elif level == 'WARNING':
            self.logger.warning(message)
        else:
            self.logger.info(f"Unknown level: {message}")

    def log_error(self, error_type, message):
        """
        Logs an error message at the ERROR level.
        :param error_type: The type of error (e.g., 'ValueError')
        :param message: The error message
        """
        self.logger.error(f"{error_type}: {message}")

    def log_exception(self, exception):
        """
        Logs an exception's details at the ERROR level.
        :param exception: The exception object
        """
        self.logger.exception(f"Exception occurred: {exception}")

    def enable_function_logging(self, func):
        """
        Decorates a function to log its calls and exceptions.
        :param func: The function to be decorated
        :return: The decorated function
        """
        def wrapper(*args, **kwargs):
            self.logger.info(f"Calling {func.__name__} with arguments: {args} and {kwargs}")
            start_time = time.time()  # Start time for performance tracking
            try:
                result = func(*args, **kwargs)
                end_time = time.time()  # End time for performance tracking
                execution_time = end_time - start_time
                self.logger.info(f"Function {func.__name__} returned: {result}")
                self.logger.info(f"Execution time: {execution_time:.4f} seconds")
                return result
            except Exception as e:
                self.log_exception(e)
                raise
        return wrapper

    def log_performance(self):
        """
        Logs performance data such as CPU and memory usage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        self.logger.info(f"CPU Usage: {cpu_usage}%")
        self.logger.info(f"Memory Usage: {memory_info.percent}%")
        self.logger.info(f"Available Memory: {memory_info.available / (1024 ** 2):.2f} MB")
        self.logger.info(f"Total Memory: {memory_info.total / (1024 ** 2):.2f} MB")

    def log_monitor_summary(self):
        """
        Logs system monitoring data like CPU and memory usage.
        """
        # CPU and memory usage information
        self.log_performance()
        
        # Disk space usage
        disk_usage = psutil.disk_usage('/')
        self.logger.info(f"Disk Usage: {disk_usage.percent}%")
        self.logger.info(f"Available Disk Space: {disk_usage.free / (1024 ** 3):.2f} GB")
        self.logger.info(f"Total Disk Space: {disk_usage.total / (1024 ** 3):.2f} GB")
        
        # Network statistics
        net_info = psutil.net_io_counters()
        self.logger.info(f"Sent bytes: {net_info.bytes_sent / (1024 ** 2):.2f} MB")
        self.logger.info(f"Received bytes: {net_info.bytes_recv / (1024 ** 2):.2f} MB")

    def set_log_level(self, level):
        """
        Dynamically set the logging level.
        :param level: The log level (e.g., 'INFO', 'DEBUG', 'WARNING', etc.)
        """
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        self.logger.info(f"Log level set to {level.upper()}")

# Example function to track with logging
def sample_function(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

# Initialize the plugin
logging_plugin = LoggingPlugin()

# Log custom message at INFO level
logging_plugin.log_custom_message('INFO', 'Custom log message for testing.')

# Log an error manually
logging_plugin.log_error('ValueError', 'A ValueError occurred.')

# Enable automatic function call logging
decorated_function = logging_plugin.enable_function_logging(sample_function)

# Test the decorated function with logging
try:
    result = decorated_function(10, 2)
    print(f"Function result: {result}")
    decorated_function(10, 0)  # This will raise an exception
except Exception as e:
    logging_plugin.log_exception(e)

# Log performance summary (logs CPU and memory usage)
logging_plugin.log_performance()

# Log function call summary (logs system information like CPU, memory, and disk)
logging_plugin.log_monitor_summary()

# Set the log level to DEBUG for more detailed logs
logging_plugin.set_log_level('DEBUG')
