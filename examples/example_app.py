# examples/example_app.py

import time
import random
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.core.pyvo_monitor import pyvo_monitor
from pyvo.core.pyvo_performance import track_performance
from pyvo.core.pyvo_error_handling import pyvo_error_handling
from pyvo.plugins import CustomLoggingPlugin, CustomPerformancePlugin
from pyvo.ui.dashboard import PyvoDashboard
import tkinter as tk

# Initialize Pyvo integration with monitoring, logging, performance tracking, and error handling
pyvo_integration = PyvoIntegration(enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True)

# Initialize custom plugins
logging_plugin = CustomLoggingPlugin()
performance_plugin = CustomPerformancePlugin()

# Example function to demonstrate Pyvo functionality with monitoring, logging, performance tracking, and error handling
@pyvo_integration.integrate
@track_performance  # Track performance for this function
@pyvo_error_handling.handle_exceptions  # Handle exceptions (logging errors)
def process_data(data):
    """Simulate processing of data with potential errors."""
    if random.choice([True, False]):
        raise ValueError("Simulated error during data processing!")
    
    time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
    result = sum(data) / len(data)  # Calculate average of the list of numbers
    return result

def run_example_app():
    """Simulate running the example app."""
    try:
        # Simulate some example data
        data = [random.randint(1, 100) for _ in range(10)]
        result = process_data(data)
        print(f"Processed data result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Run the Pyvo dashboard for monitoring and visualization
    root = tk.Tk()
    dashboard = PyvoDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    # Run the example application
    run_example_app()

    # Fetch and display the performance and error logs
    pyvo_monitor.show_log_summary()
