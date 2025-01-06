import psutil
import logging

# Set up logging
logging.basicConfig(filename="system_health.log", level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_cpu(threshold=85):
    """Check CPU usage and log if it exceeds the threshold."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > threshold:
            print(f"Warning: CPU usage is high ({cpu_usage}%)")
            logging.warning(f"CPU usage is high ({cpu_usage}%)")
        else:
            print(f"CPU usage: {cpu_usage}%")
            logging.info(f"CPU usage: {cpu_usage}%")
    except Exception as e:
        print(f"Error checking CPU usage: {e}")
        logging.error(f"Error checking CPU usage: {e}")

def check_memory(threshold=85):
    """Check memory usage and log if it exceeds the threshold."""
    try:
        memory = psutil.virtual_memory()
        if memory.percent > threshold:
            print(f"Warning: Memory usage is high ({memory.percent}%)")
            logging.warning(f"Memory usage is high ({memory.percent}%)")
        else:
            print(f"Memory usage: {memory.percent}%")
            logging.info(f"Memory usage: {memory.percent}%")
    except Exception as e:
        print(f"Error checking memory usage: {e}")
        logging.error(f"Error checking memory usage: {e}")

def check_disk(threshold=85):
    """Check disk usage and log if it exceeds the threshold."""
    try:
        disk = psutil.disk_usage('/')
        if disk.percent > threshold:
            print(f"Warning: Disk usage is high ({disk.percent}%)")
            logging.warning(f"Disk usage is high ({disk.percent}%)")
        else:
            print(f"Disk usage: {disk.percent}%")
            logging.info(f"Disk usage: {disk.percent}%")
    except Exception as e:
        print(f"Error accessing disk usage: {e}")
        logging.error(f"Error accessing disk usage: {e}")

def check_network():
    """Log the network traffic (sent and received)."""
    try:
        net = psutil.net_io_counters()
        print(f"Sent: {net.bytes_sent} bytes")
        print(f"Received: {net.bytes_recv} bytes")
        logging.info(f"Sent: {net.bytes_sent} bytes")
        logging.info(f"Received: {net.bytes_recv} bytes")
    except Exception as e:
        print(f"Error checking network usage: {e}")
        logging.error(f"Error checking network usage: {e}")

def check_resources(cpu_threshold=85, memory_threshold=85, disk_threshold=85):
    """Perform all system health checks."""
    check_cpu(cpu_threshold)
    check_memory(memory_threshold)
    check_disk(disk_threshold)
    check_network()

if __name__ == "__main__":
    print("Running system health check and resource test...")
    check_resources(cpu_threshold=85, memory_threshold=85, disk_threshold=85)
