import logging
import time
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class ExternalMonitorPlugin:
    """
    An external monitoring plugin to send Pyvo's function call data, errors, 
    and performance metrics to an external monitoring system such as Prometheus,
    Datadog, or any HTTP-based monitoring platform.
    """

    def __init__(self, monitor_url=None, api_key=None):
        """
        Initializes the external monitor plugin with the monitoring URL and optional API key.
        
        :param monitor_url: URL of the external monitoring service.
        :param api_key: Optional API key for authentication with the external service.
        """
        # Use environment variables if arguments are not provided
        self.monitor_url = monitor_url or os.getenv("MONITOR_URL")
        self.api_key = api_key or os.getenv("API_KEY")

        if not self.monitor_url:
            raise ValueError("Monitor URL must be provided via parameter or environment variable.")
        if not self.api_key:
            raise ValueError("API Key must be provided via parameter or environment variable.")

        self.logger = logging.getLogger('ExternalMonitorPlugin')
        self.logger.setLevel(logging.DEBUG)

        # Optional: File handler for logging local debug information
        file_handler = logging.FileHandler('external_monitor_plugin.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Set up retry logic for HTTP requests
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def send_function_metrics(self, func_name, execution_time, success, error_message=None):
        """
        Sends function execution metrics to the external monitoring system.
        
        :param func_name: Name of the function being monitored.
        :param execution_time: Time taken by the function to execute in seconds.
        :param success: Boolean indicating whether the function was successful.
        :param error_message: Error message (if any) for failed function calls.
        """
        metrics_data = {
            "func_name": func_name,
            "execution_time": execution_time,
            "success": success,
            "error_message": error_message,
            "timestamp": int(time.time())
        }

        if self.api_key:
            metrics_data["api_key"] = self.api_key

        try:
            response = self.session.post(self.monitor_url, json=metrics_data)
            if response.status_code == 200:
                self.logger.info(f"Successfully sent metrics for function: {func_name}")
            else:
                self.logger.error(f"Failed to send metrics for function: {func_name}, Status Code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error sending metrics to the external monitoring service: {str(e)}")

    def send_error_metrics(self, error_type, error_message):
        """
        Sends error data to the external monitoring system.
        
        :param error_type: Type of the error (e.g., ValueError, ZeroDivisionError).
        :param error_message: Error message to send.
        """
        error_data = {
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": int(time.time())
        }

        if self.api_key:
            error_data["api_key"] = self.api_key

        try:
            response = self.session.post(self.monitor_url + "/errors", json=error_data)
            if response.status_code == 200:
                self.logger.info(f"Successfully sent error metrics: {error_type}")
            else:
                self.logger.error(f"Failed to send error metrics: {error_type}, Status Code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error sending error metrics to the external monitoring service: {str(e)}")

    def send_performance_summary(self, performance_summary):
        """
        Sends performance summary (average, max, min execution time) to the external monitoring system.
        
        :param performance_summary: Dictionary containing the performance summary of tracked functions.
        """
        summary_data = {
            "performance_summary": performance_summary,
            "timestamp": int(time.time())
        }

        if self.api_key:
            summary_data["api_key"] = self.api_key

        try:
            response = self.session.post(self.monitor_url + "/performance_summary", json=summary_data)
            if response.status_code == 200:
                self.logger.info("Successfully sent performance summary.")
            else:
                self.logger.error(f"Failed to send performance summary, Status Code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error sending performance summary to the external monitoring service: {str(e)}")

    def send_function_call_summary(self, function_call_summary):
        """
        Sends a summary of function calls (e.g., call count, error count, avg execution time) to the external monitoring system.
        
        :param function_call_summary: Dictionary containing function call metrics.
        """
        summary_data = {
            "function_call_summary": function_call_summary,
            "timestamp": int(time.time())
        }

        if self.api_key:
            summary_data["api_key"] = self.api_key

        try:
            response = self.session.post(self.monitor_url + "/function_calls", json=summary_data)
            if response.status_code == 200:
                self.logger.info("Successfully sent function call summary.")
            else:
                self.logger.error(f"Failed to send function call summary, Status Code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error sending function call summary to the external monitoring service: {str(e)}")

    def monitor_function(self, func, *args, **kwargs):
        """
        Decorator to monitor function execution time and send the metrics to the external monitoring system.
        
        :param func: The function to monitor.
        :param args: Function arguments.
        :param kwargs: Function keyword arguments.
        :return: The result of the function call.
        """
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            self.send_function_metrics(func.__name__, execution_time, success=True)
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            self.send_function_metrics(func.__name__, execution_time, success=False, error_message=str(e))
            self.send_error_metrics(type(e).__name__, str(e))
            raise e

    def get_function_call_summary(self, function_calls):
        """
        Aggregates function call data into a summary.
        
        :param function_calls: List of function call data, where each entry is a dict containing 
                               'func_name', 'execution_time', and 'success' information.
        :return: Dictionary with function call summary (e.g., count, average execution time, etc.).
        """
        function_summary = {}
        for call in function_calls:
            func_name = call['func_name']
            if func_name not in function_summary:
                function_summary[func_name] = {'count': 0, 'success_count': 0, 'error_count': 0, 'total_time': 0}
            function_summary[func_name]['count'] += 1
            if call['success']:
                function_summary[func_name]['success_count'] += 1
            else:
                function_summary[func_name]['error_count'] += 1
            function_summary[func_name]['total_time'] += call['execution_time']

        # Compute averages and other metrics
        for func_name, summary in function_summary.items():
            summary['avg_time'] = summary['total_time'] / summary['count']
            summary['max_time'] = max(call['execution_time'] for call in function_calls if call['func_name'] == func_name)
            summary['min_time'] = min(call['execution_time'] for call in function_calls if call['func_name'] == func_name)

        return function_summary

    def get_performance_summary(self, performance_data):
        """
        Aggregates performance data and computes statistics.
        
        :param performance_data: List of performance data, including execution times.
        :return: Dictionary containing the performance summary (average, max, min execution time).
        """
        if not performance_data:
            return {"message": "No performance data available."}

        avg_time = sum(performance_data) / len(performance_data)
        max_time = max(performance_data)
        min_time = min(performance_data)

        return {
            "average_execution_time": avg_time,
            "max_execution_time": max_time,
            "min_execution_time": min_time
        }


# Example Usage:
# Initialize the external monitor plugin with environment variables
monitor_plugin = ExternalMonitorPlugin()

# Example function to monitor
@monitor_plugin.monitor_function
def sample_function(x, y):
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return x / y

# Call the function to trigger monitoring
try:
    result = sample_function(10, 2)
except Exception as e:
    print(f"Error occurred: {str(e)}")

# Example of sending performance summary
performance_data = [0.5, 1.2, 0.3, 0.8]
performance_summary = monitor_plugin.get_performance_summary(performance_data)
monitor_plugin.send_performance_summary(performance_summary)

# Example of sending function call summary
function_calls = [
    {"func_name": "sample_function", "execution_time": 0.5, "success": True},
    {"func_name": "sample_function", "execution_time": 0.8, "success": False},
]
function_call_summary = monitor_plugin.get_function_call_summary(function_calls)
monitor_plugin.send_function_call_summary(function_call_summary)
