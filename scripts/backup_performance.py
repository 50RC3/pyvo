import json
import shutil
import time

PERFORMANCE_FILE = 'performance_data.json'
BACKUP_DIR = 'performance_backups'

def backup_performance_data():
    if os.path.exists(PERFORMANCE_FILE):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = os.path.join(BACKUP_DIR, f"performance_backup_{timestamp}.json")
        
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        shutil.copy(PERFORMANCE_FILE, backup_file)
        print(f"Performance data backed up to {backup_file}")
    else:
        print(f"No performance data file found.")

if __name__ == "__main__":
    backup_performance_data()
