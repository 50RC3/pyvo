# examples/example_ui_usage.py

import tkinter as tk
from tkinter import messagebox
import random
import time
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.plugins.performance_plugin import CustomPerformancePlugin
from pyvo.plugins.logging_plugin import CustomLoggingPlugin
from pyvo.plugins.pyvo_integration_plugin import PyvoIntegrationPlugin

# Initialize Pyvo integration
pyvo_integration = PyvoIntegration(enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True)

# Initialize custom plugins
performance_plugin = CustomPerformancePlugin()
logging_plugin = CustomLoggingPlugin()

# Apply custom plugins to Pyvo
pyvo_integration.add_plugin(performance_plugin)
pyvo_integration.add_plugin(logging_plugin)

# Example function to demonstrate error handling, monitoring, and performance tracking
@pyvo_integration.integrate
def example_function(x, y):
    """Simulate an operation that could either succeed or fail."""
    if y == 0:
        raise ZeroDivisionError("Attempted division by zero.")
    time.sleep(random.uniform(1, 3))  # Simulate some delay
    return x / y

class PyvoAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyvo Dashboard UI Example")

        # Create the UI components
        self.create_widgets()

    def create_widgets(self):
        """Create the UI components for interacting with the Pyvo system."""
        # Example function call button
        self.test_function_button = tk.Button(self.root, text="Run Example Function", command=self.run_example_function)
        self.test_function_button.pack(pady=10)

        # Log summary display area
        self.log_button = tk.Button(self.root, text="Get Log Summary", command=self.show_log_summary)
        self.log_button.pack(pady=10)

        self.log_display_area = tk.Text(self.root, height=10, width=60)
        self.log_display_area.pack(pady=10)

        # Performance summary display area
        self.performance_button = tk.Button(self.root, text="Get Performance Summary", command=self.show_performance_summary)
        self.performance_button.pack(pady=10)

        self.performance_display_area = tk.Text(self.root, height=10, width=60)
        self.performance_display_area.pack(pady=10)

        # Error handling summary display area
        self.error_button = tk.Button(self.root, text="Get Error Summary", command=self.show_error_summary)
        self.error_button.pack(pady=10)

        self.error_display_area = tk.Text(self.root, height=10, width=60)
        self.error_display_area.pack(pady=10)

    def run_example_function(self):
        """Run the example function and display the result."""
        try:
            # Example data for testing
            x = random.randint(1, 10)
            y = random.randint(0, 10)  # Will sometimes be zero to trigger error

            # Call the decorated function
            result = example_function(x, y)
            messagebox.showinfo("Function Result", f"Function result: {result}")
        except Exception as e:
            messagebox.showerror("Function Error", f"Error occurred: {str(e)}")

    def show_log_summary(self):
        """Display the log summary in the UI."""
        log_summary = logging_plugin.get_log_summary()
        self.log_display_area.delete(1.0, tk.END)  # Clear the display area
        self.log_display_area.insert(tk.END, log_summary)

    def show_performance_summary(self):
        """Display the performance summary in the UI."""
        performance_summary = performance_plugin.get_performance_summary()
        self.performance_display_area.delete(1.0, tk.END)  # Clear the display area
        self.performance_display_area.insert(tk.END, performance_summary)

    def show_error_summary(self):
        """Display the error summary in the UI."""
        error_summary = logging_plugin.get_error_summary()
        self.error_display_area.delete(1.0, tk.END)  # Clear the display area
        self.error_display_area.insert(tk.END, error_summary)

# Main execution of the Tkinter UI
if __name__ == "__main__":
    root = tk.Tk()
    app_ui = PyvoAppUI(root)
    root.mainloop()
