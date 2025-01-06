import json
import os
import logging

# Setup logging
logging.basicConfig(filename="performance_report.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

PERFORMANCE_FILE = 'performance_data.json'

def generate_report(file_path=PERFORMANCE_FILE):
    """Generates a performance report from the given file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validate the execution_times field
            if "execution_times" not in data or not isinstance(data["execution_times"], list):
                raise ValueError("Invalid data structure: 'execution_times' should be a list.")
            
            execution_times = data["execution_times"]

            if not execution_times:
                raise ValueError("No execution times found in the data.")

            # Calculate metrics
            avg_time = sum(execution_times) / len(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)
            stddev_time = (sum((x - avg_time) ** 2 for x in execution_times) / len(execution_times)) ** 0.5
            
            report = {
                "average_execution_time": avg_time,
                "max_execution_time": max_time,
                "min_execution_time": min_time,
                "standard_deviation_execution_time": stddev_time
            }

            print("Performance Report:")
            print(json.dumps(report, indent=4))
            logging.info("Performance report generated successfully.")
        
        except ValueError as e:
            print(f"Error: {e}")
            logging.error(f"Error while processing performance data: {e}")
        
        except json.JSONDecodeError:
            print("Error: Invalid JSON in performance data file.")
            logging.error("Error: Invalid JSON in performance data file.")
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            logging.error(f"Unexpected error: {e}")
    
    else:
        print("No performance data found.")
        logging.warning("No performance data found.")

if __name__ == "__main__":
    generate_report()
