import psutil
import json
import time

def collect_stats():
    stats = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "network_sent": psutil.net_io_counters().bytes_sent,
        "network_recv": psutil.net_io_counters().bytes_recv
    }
    return stats

def save_stats(stats):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"system_stats_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(stats, f, indent=4)
    print(f"System stats saved to {filename}")

if __name__ == "__main__":
    stats = collect_stats()
    save_stats(stats)
