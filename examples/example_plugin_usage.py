# examples/example_plugin_usage.py

import time
import random
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.plugins.performance_plugin import CustomPerformancePlugin
from pyvo.plugins.logging_plugin import CustomLoggingPlugin
from pyvo.plugins.pyvo_integration_plugin import PyvoIntegrationPlugin

# Initialize Pyvo integration
pyvo_integration = PyvoIntegration(enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True)

# Initialize custom plugins
performance_plugin = CustomPerformancePlugin()
logging_plugin = CustomLoggingPlugin()

# Apply custom plugins
pyvo_integration.add_plugin(performance_plugin)
pyvo_integration.add_plugin(logging_plugin)

# Example function to demonstrate plugin functionality
@pyvo_integration.integrate
def process_data(data):
    """Simulate processing of data."""
    if random.choice([True, False]):
        raise ValueError("Simulated error during data processing!")
    
    time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
    result = sum(data) / len(data)  # Calculate average of the list of numbers
    return result

def run_plugin_example():
    """Run the plugin example to demonstrate Pyvo plugin usage."""
    try:
        # Simulate some example data
        data = [random.randint(1, 100) for _ in range(10)]
        result = process_data(data)
        print(f"Processed data result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # You can call any plugin's specific functionality after running your application
    # For example, to view the logs or performance metrics tracked by the plugins
    performance_plugin.get_performance_summary()
    logging_plugin.get_log_summary()

if __name__ == "__main__":
    # Run the plugin example application
    run_plugin_example()

    # You can fetch the performance summary or logs manually after the application runs
    # Example of fetching log summary after running the app
    print("Performance Summary:")
    performance_plugin.get_performance_summary()

    print("\nLog Summary:")
    logging_plugin.get_log_summary()
