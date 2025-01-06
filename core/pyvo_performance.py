import time
import logging
import functools
import statistics

# A dictionary to store performance data for functions
performance_data = {}

def track_performance(func):
    """
    A decorator function to track the execution time of functions.
    Logs and stores performance metrics like execution time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error executing function {func.__name__}: {e}")
            raise
        finally:
            end_time = time.time()  # Record the end time
            execution_time = end_time - start_time
            function_name = func.__name__
            
            # Store the execution time in the performance data dictionary
            if function_name not in performance_data:
                performance_data[function_name] = []
            performance_data[function_name].append(execution_time)
            
            # Log the performance metric
            logging.info(f"Performance: {function_name} executed in {execution_time:.4f} seconds.")
            
        return result

    return wrapper

def apply_performance_tracking(module):
    """
    Automatically applies the @track_performance decorator to all functions in the given module.
    """
    for name, obj in module.__dict__.items():
        if callable(obj) and isinstance(obj, type(functools.partial)):  # Ensure obj is a function
            try:
                decorated_func = track_performance(obj)
                setattr(module, name, decorated_func)
            except Exception as e:
                logging.error(f"Error decorating function {name}: {e}")

def get_performance_summary():
    """
    Retrieves a performance summary for all tracked functions.
    Displays the average, maximum, and minimum execution times.
    Accessible via the dashboard.
    """
    summary = []
    if performance_data:
        for function_name, times in performance_data.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            stddev_time = round(statistics.stdev(times), 4) if len(times) > 1 else 0
            summary.append({
                "Function": function_name,
                "Average Execution Time (s)": round(avg_time, 4),
                "Max Execution Time (s)": round(max_time, 4),
                "Min Execution Time (s)": round(min_time, 4),
                "Standard Deviation (s)": stddev_time,
                "Execution Count": len(times)
            })
    else:
        summary.append({"Error": "No performance data available yet."})
    
    return summary

def log_performance_summary():
    """
    Logs the performance summary to the log system for tracking and visualization.
    This data can be shown in the dashboard.
    """
    summary = get_performance_summary()
    if summary:
        for item in summary:
            if "Error" in item:
                logging.error(item["Error"])
            else:
                logging.info(f"Function: {item['Function']}")
                logging.info(f"    Average Execution Time: {item['Average Execution Time (s)']} seconds")
                logging.info(f"    Max Execution Time: {item['Max Execution Time (s)']} seconds")
                logging.info(f"    Min Execution Time: {item['Min Execution Time (s)']} seconds")
                logging.info(f"    Standard Deviation: {item['Standard Deviation (s)']} seconds")
                logging.info(f"    Execution Count: {item['Execution Count']}")

def reset_performance_data():
    """
    Resets the stored performance data.
    This can be triggered from the dashboard to start fresh measurements.
    Clears the performance_data dictionary.
    """
    global performance_data
    performance_data = {}
    logging.info("Performance data has been reset.")
    
    return "Performance data has been reset."

def get_performance_data_for_graph():
    """
    Returns the performance data in a format suitable for graph plotting.
    This is for use in visualizing the performance metrics as a line graph.
    """
    graph_data = {}
    for function_name, times in performance_data.items():
        graph_data[function_name] = {
            "timestamps": list(range(len(times))),  # Each execution has a unique timestamp
            "values": times
        }
    return graph_data
