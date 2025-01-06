import os
import time
import shutil

LOG_DIR = 'pyvo_dashboard.log'
ARCHIVE_DIR = 'pyvo_log_archive'

def cleanup_logs():
    if os.path.exists(LOG_DIR):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        archived_file = os.path.join(ARCHIVE_DIR, f"pyvo_dashboard_{timestamp}.log")
        
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)
        
        shutil.move(LOG_DIR, archived_file)
        print(f"Log file moved to {archived_file}")
    else:
        print(f"No log file found to clean up.")

if __name__ == "__main__":
    cleanup_logs()
