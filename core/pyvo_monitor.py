import logging
import time
import functools
import sys
from pyvo.core.pyvo_error_handling import handle_error

# Initialize logger
logger = logging.getLogger(__name__)

class PyvoMonitor:
    def __init__(self):
        self.function_logs = {}

    def _log_function_call(self, func_name, execution_time, error=None):
        """Logs the details of a function call including execution time and errors."""
        if func_name not in self.function_logs:
            self.function_logs[func_name] = {
                'call_count': 0,
                'total_execution_time': 0,
                'error_count': 0,
                'error_details': []
            }
        
        self.function_logs[func_name]['call_count'] += 1
        self.function_logs[func_name]['total_execution_time'] += execution_time
        
        if error:
            self.function_logs[func_name]['error_count'] += 1
            self.function_logs[func_name]['error_details'].append(str(error))

    def log_summary(self):
        """Generates a summary of function logs."""
        summary = []
        for func_name, logs in self.function_logs.items():
            avg_execution_time = logs['total_execution_time'] / logs['call_count'] if logs['call_count'] > 0 else 0
            summary.append(f"Function: {func_name}")
            summary.append(f"  Total Calls: {logs['call_count']}")
            summary.append(f"  Total Errors: {logs['error_count']}")
            summary.append(f"  Average Execution Time: {avg_execution_time:.4f} seconds")
            if logs['error_count'] > 0:
                summary.append(f"  Errors: {', '.join(logs['error_details'])}")
            summary.append("-" * 50)
        return summary

    def auto_decorate_functions(self, module):
        """Auto-decorates all functions in a given module to track their execution."""
        for name, obj in module.__dict__.items():
            if callable(obj):
                # Only decorate functions
                decorated_func = self._decorate_function(obj)
                setattr(module, name, decorated_func)
                
    def _decorate_function(self, func):
        """Decorator function to measure the execution time and log errors."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                self._log_function_call(func.__name__, execution_time)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                self._log_function_call(func.__name__, execution_time, error=e)
                handle_error(e)  # Call external error handler if defined
                raise e  # Re-raise exception after logging
        return wrapper


# Initialize PyvoMonitor instance
pyvo_monitor = PyvoMonitor()
