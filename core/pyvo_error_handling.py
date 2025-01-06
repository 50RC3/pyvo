import logging
import traceback
import requests
from pyvo.ui.dashboard import update_error_summary  # Assuming this function is used to update the dashboard error display

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# A dictionary to store error information that can be accessed from the dashboard
class ErrorStore:
    def __init__(self):
        self.general_errors = []
        self.specific_errors = {}

    def add_error(self, error_message, stack_trace, error_type):
        # Add to general errors
        self.general_errors.append({'message': error_message, 'stack_trace': stack_trace})

        # Add to specific errors
        if error_type not in self.specific_errors:
            self.specific_errors[error_type] = []

        self.specific_errors[error_type].append({'message': error_message, 'stack_trace': stack_trace})

# Instantiate the error store globally
error_store = ErrorStore()

def handle_error(error):
    """
    This function handles errors that occur within decorated functions.
    It logs the error details and stack trace for debugging purposes.
    It also stores the error information in a global store for later access.

    Args:
        error (Exception): The exception that was raised during function execution.
    """
    # Log the error with a detailed traceback
    error_message = str(error)
    stack_trace = traceback.format_exc()
    
    logger.error(f"An error occurred at {time.time()}: {error_message}")
    logger.error("Stack Trace:")
    logger.error(stack_trace)  # Log the full stack trace of the error

    # Store the error in the general errors list
    error_store.add_error(error_message, stack_trace, "GeneralError")

    # Dynamically categorize the error based on its type
    error_type = type(error).__name__  # Get the type of the error dynamically

    # Store the specific error type
    error_store.add_error(error_message, stack_trace, error_type)

    # Optionally, send the error details to an external service for further analysis
    send_error_to_service(error)

    # Update the dashboard error summary with the new error information
    update_error_summary()

def send_error_to_service(error):
    """
    Optionally send the error details to an external error reporting service.
    This could be a service like Sentry, Rollbar, or your custom solution.

    Args:
        error (Exception): The error to send to the external service.
    """
    try:
        # Example of sending error to an external service (this is a placeholder for actual implementation)
        external_service_url = "https://example.com/error-reporting"
        payload = {
            "error_message": str(error),
            "stack_trace": traceback.format_exc(),
            "module": "pyvo"
        }

        # Example of sending a POST request (you'd use actual request code in a real-world scenario)
        response = requests.post(external_service_url, json=payload)
        if response.status_code == 200:
            logger.info("Error sent successfully to the external service.")
        else:
            logger.warning("Failed to send error to the external service.")
    except Exception as e:
        # Log any errors that happen while trying to send the error to the external service
        logger.error(f"Error while sending error to external service: {str(e)}")

def get_error_summary():
    """
    Get the summary of all errors, both general and type-specific.
    This information will be used in the dashboard to display error information.

    Returns:
        dict: A dictionary containing both general and specific error summaries.
    """
    return {
        'general_errors': error_store.general_errors,
        'specific_errors': error_store.specific_errors
    }

def update_error_summary():
    """
    This function is responsible for updating the error summary in the dashboard.
    It will trigger the update in the UI, allowing the user to view the most recent errors.
    This could be implemented with a UI callback or a direct update to the dashboard's display logic.
    """
    # Assuming there's a function in the dashboard that takes error data and updates the UI
    # For example, we might send the error summary to a web UI or a dedicated error monitoring service
    error_summary = get_error_summary()

    # Placeholder: Update the UI or dashboard with the error summary
    # You would replace this with your actual UI update code
    print(f"Error Summary: {error_summary}")
    
# Example usage:
if __name__ == "__main__":
    # Sample function to test error handling
    def sample_function(x, y):
        if y == 0:
            raise ValueError("Division by zero is not allowed!")
        return x / y

    # Case 1: Full integration with all features enabled
    try:
        result = sample_function(10, 2)
        print(f"Result of function call: {result}")
    except Exception as e:
        handle_error(e)

    # Case 2: Triggering a ZeroDivisionError to test error handling
    try:
        result = sample_function(10, 0)  # This will raise a ValueError
        print(f"Result of function call: {result}")
    except Exception as e:
        handle_error(e)
