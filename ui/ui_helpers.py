import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyvo
from pyvo.core.pyvo_monitor import pyvo_monitor

def create_checkbutton(frame, text, variable, anchor=tk.W):
    """
    Creates a Checkbutton widget for the UI.

    Parameters:
    - frame: The parent frame to place the Checkbutton in.
    - text: The text displayed next to the checkbox.
    - variable: The Tkinter variable to bind to the checkbox.
    - anchor: The alignment of the widget in the parent frame (default is left).
    
    Returns:
    - The Checkbutton widget.
    """
    checkbutton = tk.Checkbutton(frame, text=text, variable=variable, anchor=anchor)
    checkbutton.pack(anchor=anchor)
    return checkbutton

def create_button(frame, text, command, width=None):
    """
    Creates a Button widget for the UI.

    Parameters:
    - frame: The parent frame to place the button in.
    - text: The text displayed on the button.
    - command: The function to be called when the button is clicked.
    - width: The width of the button (optional).

    Returns:
    - The Button widget.
    """
    button = tk.Button(frame, text=text, command=command, width=width)
    button.pack(pady=10)
    return button

def create_text_widget(frame, height, wrap=tk.WORD):
    """
    Creates a ScrolledText widget for displaying logs or results.

    Parameters:
    - frame: The parent frame to place the text widget in.
    - height: The height of the text widget.
    - wrap: The text wrapping style (default is WORD).

    Returns:
    - The ScrolledText widget.
    """
    text_widget = scrolledtext.ScrolledText(frame, height=height, wrap=wrap)
    text_widget.pack(expand=True, fill=tk.BOTH)
    return text_widget

def display_error_message(message):
    """
    Displays an error message in a messagebox.

    Parameters:
    - message: The message to be displayed.
    """
    messagebox.showerror("Error", message)

def display_info_message(message):
    """
    Displays an informational message in a messagebox.

    Parameters:
    - message: The message to be displayed.
    """
    messagebox.showinfo("Info", message)

def update_log_display(log_widget, log_file, line_count=20):
    """
    Updates the log display with the last `line_count` lines from the log file.

    Parameters:
    - log_widget: The ScrolledText widget to update.
    - log_file: The log file to read from.
    - line_count: The number of lines to display (default is 20).
    """
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()[-line_count:]  # Display the last `line_count` logs
        log_widget.delete(1.0, tk.END)  # Clear the existing logs in the UI
        log_widget.insert(tk.END, ''.join(logs))  # Display the new logs
    except Exception as e:
        log_widget.delete(1.0, tk.END)
        log_widget.insert(tk.END, f"Error reading log file: {str(e)}")
        pyvo.PyvoIntegration.logger.error(f"Error reading log file: {str(e)}")

def reset_performance_data():
    """
    Resets the stored performance data, clearing any recorded execution times.
    """
    try:
        pyvo_monitor.reset_performance_data()
        display_info_message("Performance data has been reset.")
        pyvo.PyvoIntegration.logger.info("Performance data reset successfully.")
    except Exception as e:
        display_error_message(f"Error resetting performance data: {str(e)}")
        pyvo.PyvoIntegration.logger.error(f"Error resetting performance data: {str(e)}")

def display_performance_summary(summary_widget):
    """
    Displays a summary of function performance, including average, max, and min times.

    Parameters:
    - summary_widget: The widget to display the performance summary in.
    """
    summary = pyvo_monitor.get_performance_summary()
    summary_widget.delete(1.0, tk.END)  # Clear any existing text
    if summary:
        for line in summary:
            summary_widget.insert(tk.END, f"{line}\n")  # Insert summary line by line
    else:
        summary_widget.insert(tk.END, "No performance data available.")

def log_performance_summary():
    """
    Logs the current performance summary to the log file.
    """
    summary = pyvo_monitor.get_performance_summary()
    if summary:
        for line in summary:
            pyvo.PyvoIntegration.logger.info(line)
    else:
        pyvo.PyvoIntegration.logger.info("No performance data available.")
