import os
import logging
import sys
import importlib
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import time
import threading
from logging.handlers import RotatingFileHandler
import pyvo
from pyvo.core.pyvo_integration import PyvoIntegration
from pyvo.core.pyvo_monitor import pyvo_monitor
from pyvo.core.pyvo_error_handling import handle_error, get_error_summary
from pyvo.core.pyvo_performance import apply_performance_tracking, get_performance_summary, log_performance_summary, reset_performance_data

# Initialize Pyvo Integration with default settings
pyvo_integration = PyvoIntegration(enable_monitoring=True, enable_logging=True, enable_performance=True, enable_error_handling=True)

# Set up logging to a file with rotating file handler for large logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.StreamHandler(),
    logging.FileHandler('pyvo_dashboard.log', mode='a'),
    RotatingFileHandler('pyvo_dashboard.log', maxBytes=10**6, backupCount=5)
])

# Path to the scripts directory
SCRIPTS_DIR = "pyvo/scripts"

# Example function to integrate with Pyvo
@pyvo_integration.integrate
def sample_function(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed!")
    return x / y

class PyvoDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyvo Dashboard")
        self.root.geometry("800x500")

        # Create frames for organizing the layout
        self.frame_scripts = tk.Frame(self.root)
        self.frame_scripts.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.frame_settings = tk.Frame(self.root)
        self.frame_settings.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Load scripts dynamically from the scripts directory
        self.scripts = self.load_scripts()

        # Create dropdown menu
        self.script_var = tk.StringVar()
        self.script_var.set("Select a script")  # Default text in dropdown
        self.dropdown_menu = tk.OptionMenu(self.frame_scripts, self.script_var, *self.scripts)
        self.dropdown_menu.pack(pady=20)

        # Button to run the selected script
        self.run_button = tk.Button(self.frame_scripts, text="Run Script", command=self.run_script)
        self.run_button.pack(pady=20)

        # Logs text widget to display real-time logs
        self.logs_text = scrolledtext.ScrolledText(self.frame_scripts, height=10, wrap=tk.WORD)
        self.logs_text.pack(expand=True, fill=tk.BOTH)

        # Settings section for updating Pyvo configurations
        self.var_monitoring = tk.BooleanVar(value=pyvo_integration.enable_monitoring)
        self.var_logging = tk.BooleanVar(value=pyvo_integration.enable_logging)
        self.var_performance = tk.BooleanVar(value=pyvo_integration.enable_performance)
        self.var_error_handling = tk.BooleanVar(value=pyvo_integration.enable_error_handling)

        tk.Checkbutton(self.frame_settings, text="Enable Monitoring", variable=self.var_monitoring).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Logging", variable=self.var_logging).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Performance Tracking", variable=self.var_performance).pack(anchor=tk.W)
        tk.Checkbutton(self.frame_settings, text="Enable Error Handling", variable=self.var_error_handling).pack(anchor=tk.W)

        # Button to update settings
        self.btn_update_settings = tk.Button(self.frame_settings, text="Update Settings", command=self.update_settings)
        self.btn_update_settings.pack(pady=10)

        # Button to trigger the test function
        self.btn_test_function = tk.Button(self.frame_settings, text="Test Sample Function", command=self.test_function)
        self.btn_test_function.pack(pady=10)

        # Button to fetch and display the log summary
        self.log_button = tk.Button(self.root, text="Get Log Summary", command=self.show_log_summary)
        self.log_button.pack(pady=10)

        # Create a text area for displaying the log summary
        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.log_text.pack(pady=10)

        # Entry for dynamically adding modules
        self.module_entry_label = tk.Label(self.root, text="Enter Module Name to Decorate Functions:")
        self.module_entry_label.pack(pady=5)

        self.module_entry = tk.Entry(self.root, width=50)
        self.module_entry.pack(pady=5)

        self.decorate_button = tk.Button(self.root, text="Decorate Functions", command=self.decorate_module_functions)
        self.decorate_button.pack(pady=5)

        # Start the background thread for automatic log updates
        self.start_auto_update()

    def load_scripts(self):
        """Loads scripts from the pyvo/scripts directory."""
        if os.path.exists(SCRIPTS_DIR):
            scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith('.py')]
            scripts.sort()  # Sorting scripts alphabetically
            return scripts
        return []

    def run_script(self):
        """Runs the selected script from the dropdown."""
        selected_script = self.script_var.get()
        if selected_script == "Select a script":
            messagebox.showerror("Error", "Please select a script to run.")
            return

        script_path = os.path.join(SCRIPTS_DIR, selected_script)
        if not os.path.isfile(script_path):
            messagebox.showerror("Error", f"Script {selected_script} not found.")
            return

        try:
            # Run the selected script
            messagebox.showinfo("Running", f"Running {selected_script}...")
            result = subprocess.run(['python', script_path], capture_output=True, text=True)

            # Log the script execution result
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Script {selected_script} executed successfully.")
            else:
                logging.error(f"Error running script {selected_script}: {result.stderr}")
                messagebox.showerror("Error", f"Error running script:\n{result.stderr}")
        except Exception as e:
            logging.error(f"Error running script {selected_script}: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_settings(self):
        """Update Pyvo settings dynamically."""
        enable_monitoring = self.var_monitoring.get()
        enable_logging = self.var_logging.get()
        enable_performance = self.var_performance.get()
        enable_error_handling = self.var_error_handling.get()

        # Update Pyvo settings dynamically
        pyvo_integration.enable_monitoring = enable_monitoring
        pyvo_integration.enable_logging = enable_logging
        pyvo_integration.enable_performance = enable_performance
        pyvo_integration.enable_error_handling = enable_error_handling

        # Log the change
        logging.info(f"Updated settings: Monitoring={enable_monitoring}, Logging={enable_logging}, Performance={enable_performance}, Error Handling={enable_error_handling}")
        messagebox.showinfo("Settings Update", "Pyvo settings updated successfully!")

    def test_function(self):
        """Test the sample function with logging."""
        try:
            result = sample_function(10, 2)
            messagebox.showinfo("Test Function", f"Test Result: {result}")
        except Exception as e:
            logging.error(f"Error during sample function test: {str(e)}")
            messagebox.showerror("Test Function Error", f"Error: {str(e)}")

    def decorate_module_functions(self):
        """
        This function will dynamically import a module and decorate its functions using the PyvoMonitor.
        """
        module_name = self.module_entry.get().strip()
        if not module_name:
            messagebox.showerror("Error", "Please enter a module name.")
            return

        try:
            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Check if the module has functions to decorate
            if not any(callable(getattr(module, func)) for func in dir(module)):
                messagebox.showerror("Error", "Module has no callable functions to decorate.")
                return

            # Automatically decorate functions in the module
            pyvo_monitor.auto_decorate_functions(module)
            logging.info(f"Functions in module '{module_name}' have been decorated.")
            messagebox.showinfo("Success", f"Functions in module '{module_name}' decorated successfully.")
            self.show_log_summary()  # Refresh log summary after decorating
        except ModuleNotFoundError:
            logging.error(f"Module '{module_name}' not found.")
            messagebox.showerror("Error", f"Module '{module_name}' not found.")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_log_summary(self):
        """Display the log summary in the UI."""
        summary = pyvo_monitor.log_summary()
        self.log_text.delete(1.0, tk.END)  # Clear any existing text
        for line in summary:
            self.log_text.insert(tk.END, f"{line}\n")  # Insert summary line by line

    def start_auto_update(self):
        """Start background thread for automatic log updates every 2 seconds."""
        threading.Thread(target=self.auto_update_logs_thread, daemon=True).start()

    def auto_update_logs_thread(self):
        """Background thread to periodically update logs."""
        while True:
            self.update_logs()
            time.sleep(2)

    def update_logs(self):
        """Update the log display by reading the last 20 lines from the log file."""
        try:
            with open('pyvo_dashboard.log', 'r') as file:
                logs = file.readlines()[-20:]  # Display the last 20 logs
            self.root.after(0, lambda: self.logs_text.delete(1.0, tk.END))  # Update logs safely from the main thread
            self.root.after(0, lambda: self.logs_text.insert(tk.END, ''.join(logs)))  # Update logs safely
        except Exception as e:
            logging.error(f"Error reading logs: {str(e)}")
            self.logs_text.insert(tk.END, f"Error reading logs: {str(e)}\n")
