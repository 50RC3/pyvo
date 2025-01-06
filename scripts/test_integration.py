import logging
from pyvo.core.pyvo_integration import sample_function

# Set up logging configuration
logging.basicConfig(filename="sample_function_test.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def test_sample_function():
    try:
        # Sample function input
        x, y = 10, 2
        logging.info(f"Testing sample_function with x={x} and y={y}")
        
        # Call the sample function
        result = sample_function(x, y)
        
        # Log the result and print it
        print(f"Sample function result: {result}")
        logging.info(f"Sample function result: {result}")
    
    except Exception as e:
        # Log error with detailed information
        print(f"Error occurred: {e}")
        logging.error(f"Error occurred while testing sample_function with x={x} and y={y}")
        logging.exception(f"Exception details: {e}")

if __name__ == "__main__":
    test_sample_function()
