# pyvo/core/__init__.py

# Initialize the pyvo package with essential imports.
from .pyvo_integration import PyvoIntegration
from .pyvo_monitor import pyvo_monitor  # Consider renaming to something more descriptive, e.g., `monitor_function`
from .pyvo_performance import (
    apply_performance_tracking,
    get_performance_summary,
    log_performance_summary,
    reset_performance_data
)
from .pyvo_error_handling import (
    handle_error,
    log_error,
    get_error_summary,
    reset_error_data
)

# Initialization for pyvo
__all__ = [
    "PyvoIntegration",  # Class for integration with Pyvo features
    "pyvo_monitor",  # Potentially renamed to something more descriptive
    "apply_performance_tracking",  # For enabling performance tracking
    "get_performance_summary",  # Retrieves performance summary data
    "log_performance_summary",  # Logs a performance summary
    "reset_performance_data",  # Resets performance data
    "handle_error",  # Handles errors in Pyvo functions
    "log_error",  # Logs errors
    "get_error_summary",  # Retrieves error summary
    "reset_error_data",  # Resets error data
]
