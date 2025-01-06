import tkinter as tk
from tkinter import messagebox
import pyvo
from pyvo.core.pyvo_integration import PyvoIntegration

class PyvoSettings:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyvo Settings")
        self.root.geometry("400x300")  # Set window size
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())  # Center window
        self.create_widgets()

    def create_widgets(self):
        """Create the settings UI elements."""
        self.frame_settings = tk.Frame(self.root)
        self.frame_settings.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Settings section for updating Pyvo configurations
        self.var_monitoring = tk.BooleanVar(value=pyvo.PyvoIntegration.enable_monitoring)
        self.var_logging = tk.BooleanVar(value=pyvo.PyvoIntegration.enable_logging)
        self.var_performance = tk.BooleanVar(value=pyvo.PyvoIntegration.enable_performance)
        self.var_error_handling = tk.BooleanVar(value=pyvo.PyvoIntegration.enable_error_handling)

        # Checkbuttons for enabling/disabling features
        tk.Checkbutton(self.frame_settings, text="Enable Monitoring", variable=self.var_monitoring).grid(row=0, sticky=tk.W, padx=10)
        tk.Checkbutton(self.frame_settings, text="Enable Logging", variable=self.var_logging).grid(row=1, sticky=tk.W, padx=10)
        tk.Checkbutton(self.frame_settings, text="Enable Performance Tracking", variable=self.var_performance).grid(row=2, sticky=tk.W, padx=10)
        tk.Checkbutton(self.frame_settings, text="Enable Error Handling", variable=self.var_error_handling).grid(row=3, sticky=tk.W, padx=10)

        # Button to update settings
        self.btn_update_settings = tk.Button(self.frame_settings, text="Update Settings", command=self.update_settings)
        self.btn_update_settings.grid(row=4, pady=10)

        # Optional: Reset button
        self.btn_reset_settings = tk.Button(self.frame_settings, text="Reset to Default", command=self.reset_settings)
        self.btn_reset_settings.grid(row=5, pady=10)

    def update_settings(self):
        """Update Pyvo settings dynamically."""
        enable_monitoring = self.var_monitoring.get()
        enable_logging = self.var_logging.get()
        enable_performance = self.var_performance.get()
        enable_error_handling = self.var_error_handling.get()

        try:
            # Update Pyvo settings dynamically
            pyvo.PyvoIntegration.enable_monitoring = enable_monitoring
            pyvo.PyvoIntegration.enable_logging = enable_logging
            pyvo.PyvoIntegration.enable_performance = enable_performance
            pyvo.PyvoIntegration.enable_error_handling = enable_error_handling
            pyvo.PyvoIntegration.logger.info(f"Updated settings: Monitoring={enable_monitoring}, Logging={enable_logging}, Performance={enable_performance}, ErrorHandling={enable_error_handling}")
            messagebox.showinfo("Settings Update", "Pyvo settings updated successfully!")
        except Exception as e:
            pyvo.PyvoIntegration.logger.error(f"Error updating Pyvo settings: {e}")
            messagebox.showerror("Settings Update Error", f"An error occurred: {e}")

    def reset_settings(self):
        """Reset the settings to default values."""
        self.var_monitoring.set(False)
        self.var_logging.set(False)
        self.var_performance.set(False)
        self.var_error_handling.set(False)
        messagebox.showinfo("Settings Reset", "Settings have been reset to default values.")

# Main GUI loop for settings
if __name__ == "__main__":
    root = tk.Tk()
    settings_window = PyvoSettings(root)
    root.mainloop()
