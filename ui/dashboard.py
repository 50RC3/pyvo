import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
import importlib
import pyvo
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.core.pyvo_monitor import pyvo_monitor
from pyvo.core.pyvo_error_handling import pyvo_error_handling
from pyvo.core.pyvo_performance import pyvo_performance

# Initialize the Pyvo integration with default settings
pyvo_integration = PyvoIntegration(enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True)

# Set up logging to a file for the dashboard to read
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.StreamHandler(),
    logging.FileHandler('pyvo_dashboard.log', mode='a')
])

# Example function to integrate with Pyvo
@pyvo_integration.integrate
def sample_function(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed!")
    return x / y

class PyvoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyvo Dashboard")
        self.create_widgets()

    def create_widgets(self):
        """Create the dashboard UI elements."""
        self.frame_logs = tk.Frame(self.root)
        self.frame_logs.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.frame_settings = tk.Frame(self.root)
        self.frame_settings.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.logs_text = scrolledtext.ScrolledText(self.frame_logs, height=10, wrap=tk.WORD)
        self.logs_text.pack(expand=True, fill=tk.BOTH)

        self.var_monitoring = tk.BooleanVar(value=pyvo_integration.enable_monitoring)
        self.var_logging = tk.BooleanVar(value=pyvo_integration.enable_logging)
        self.var_performance = tk.BooleanVar(value=pyvo_integration.enable_performance)
        self.var_error_handling = tk.BooleanVar(value=pyvo_integration.enable_error_handling)

        tk.Checkbutton(self.frame_settings, text="Enable Monitoring", variable=self.var_monitoring).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Logging", variable=self.var_logging).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Performance Tracking", variable=self.var_performance).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Error Handling", variable=self.var_error_handling).pack(anchor=tk.W)

        self.btn_update_settings = tk.Button(self.frame_settings, text="Update Settings", command=self.update_settings)
        self.btn_update_settings.pack(pady=10)

        self.btn_test_function = tk.Button(self.frame_settings, text="Test Sample Function", command=self.test_function)
        self.btn_test_function.pack(pady=10)

        self.log_button = tk.Button(self.root, text="Get Log Summary", command=self.show_log_summary)
        self.log_button.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.log_text.pack(pady=10)

        self.module_entry_label = tk.Label(self.root, text="Enter Module Name to Decorate Functions:")
        self.module_entry_label.pack(pady=5)

        self.module_entry = tk.Entry(self.root, width=50)
        self.module_entry.pack(pady=5)

        self.decorate_button = tk.Button(self.root, text="Decorate Functions", command=self.decorate_module_functions)
        self.decorate_button.pack(pady=5)

        self.auto_update_logs()

    def update_logs(self):
        """Update the log display by reading the last 20 lines from the log file."""
        try:
            with open('pyvo_dashboard.log', 'r') as file:
                logs = file.readlines()[-20:]
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(tk.END, ''.join(logs))
        except Exception as e:
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(tk.END, f"Error reading log file: {str(e)}")

    def show_log_summary(self):
        """Fetch and display the log summary."""
        summary = pyvo_monitor.log_summary()
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Log Summary:\n")
        self.log_text.insert(tk.END, f"Total Errors: {pyvo_monitor.total_errors()}\n")
        self.log_text.insert(tk.END, f"Total Warnings: {pyvo_monitor.total_warnings()}\n")
        for line in summary:
            self.log_text.insert(tk.END, f"{line}\n")

    def update_settings(self):
        """Update Pyvo settings dynamically."""
        enable_monitoring = self.var_monitoring.get()
        enable_logging = self.var_logging.get()
        enable_performance = self.var_performance.get()
        enable_error_handling = self.var_error_handling.get()

        pyvo_integration.enable_monitoring = enable_monitoring
        pyvo_integration.enable_logging = enable_logging
        pyvo_integration.enable_performance = enable_performance
        pyvo_integration.enable_error_handling = enable_error_handling

        logging.info(f"Updated settings: Monitoring={enable_monitoring}, Logging={enable_logging}, Performance={enable_performance}, Error Handling={enable_error_handling}")
        messagebox.showinfo("Settings Update", "Pyvo settings updated successfully!")

    def test_function(self):
        """Test the sample function with logging."""
        try:
            result = sample_function(10, 2)
            messagebox.showinfo("Test Function", f"Test Result: {result}")
        except Exception as e:
            messagebox.showerror("Test Function Error", f"Error: {str(e)}")

    def decorate_module_functions(self):
        """Dynamically import a module and decorate its functions."""
        module_name = self.module_entry.get().strip()
        if not module_name:
            messagebox.showerror("Input Error", "Please enter a module name.")
            return
        try:
            module = importlib.import_module(module_name)
            pyvo_monitor.auto_decorate_functions(module)
            self.show_log_summary()
            messagebox.showinfo("Module Decorated", f"Functions in module '{module_name}' have been decorated.")
        except ModuleNotFoundError:
            messagebox.showerror("Module Not Found", f"Module '{module_name}' not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def auto_update_logs(self):
        """Automatically update logs every 2 seconds."""
        self.update_logs()
        self.root.after(2000, self.auto_update_logs)
        

# Main GUI loop
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = PyvoDashboard(root)
    root.mainloop()
