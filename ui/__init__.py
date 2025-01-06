# __init__.py for the pyvo/ui package

# Import relevant modules from the ui package to provide essential UI components
from .dashboard import PyvoDashboard  # For the main dashboard UI
from .settings import PyvoSettings    # For the settings-related UI elements
from .ui_helpers import (
    create_checkbutton,  # For creating Checkbutton UI elements
    create_button,       # For creating Button UI elements
    create_text_widget,  # For creating text widgets like Labels and Entry fields
    display_error_message,  # For displaying error messages in the UI
    display_info_message,   # For displaying informational messages
    update_log_display,     # For updating the log display in the UI
    reset_performance_data, # For resetting performance monitoring data
    display_performance_summary,  # For displaying a summary of performance metrics
    log_performance_summary   # For logging detailed performance metrics
)

# Ensuring all the UI components are readily accessible in the package namespace
__all__ = [
    'PyvoDashboard',  # The primary dashboard for the application
    'PyvoSettings',   # The settings configuration for the app
    'create_checkbutton',  # Helper function to create Checkbuttons
    'create_button',       # Helper function to create Buttons
    'create_text_widget',  # Helper function to create Text Widgets
    'display_error_message',  # Function for displaying error messages
    'display_info_message',   # Function for displaying info messages
    'update_log_display',     # Function for updating log display
    'reset_performance_data', # Function to reset performance data
    'display_performance_summary',  # Function to display performance summary
    'log_performance_summary'   # Function to log performance data
]
