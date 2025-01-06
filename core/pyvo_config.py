import logging
import json
import os

# Define default configuration values
DEFAULT_CONFIG = {
    "enable_monitoring": True,
    "enable_logging": True,
    "enable_performance": True,
    "enable_error_handling": True,
    "log_level": "INFO",  # Logging level (INFO, DEBUG, ERROR, etc.)
    "performance_logging_interval": 60  # In seconds
}

# File path for storing persistent configurations
CONFIG_FILE_PATH = 'pyvo_config.json'

# Configuration class to handle Pyvo settings
class PyvoConfig:
    def __init__(self):
        """
        Initializes the configuration by loading existing settings or using default values.
        """
        self.config = DEFAULT_CONFIG.copy()  # Start with default values
        self.load_config()  # Load from file if it exists
        self.set_logging_level()  # Set logging level based on configuration

    def load_config(self):
        """
        Load configuration from a JSON file.
        """
        if os.path.exists(CONFIG_FILE_PATH):
            try:
                with open(CONFIG_FILE_PATH, 'r') as file:
                    config_data = json.load(file)
                    self.config.update(config_data)  # Update default settings with stored values
                    logging.info(f"Configuration loaded from {CONFIG_FILE_PATH}.")
            except json.JSONDecodeError as e:
                logging.warning(f"Failed to parse configuration file {CONFIG_FILE_PATH}: {e}")
            except Exception as e:
                logging.error(f"Failed to load configuration from file: {e}")
        else:
            logging.info("No configuration file found, using default settings.")

    def save_config(self):
        """
        Save current configuration to a JSON file.
        """
        try:
            with open(CONFIG_FILE_PATH, 'w') as file:
                json.dump(self.config, file, indent=4)
            logging.info(f"Configuration saved to {CONFIG_FILE_PATH}.")
        except Exception as e:
            logging.error(f"Failed to save configuration to file: {e}")

    def update_config(self, key, value):
        """
        Update a specific configuration setting and save it to file.
        
        :param key: The configuration key (e.g., "enable_monitoring")
        :param value: The new value to be assigned to the configuration key
        """
        if key in self.config:
            # Add type validation based on the key
            expected_type = type(DEFAULT_CONFIG[key])
            if isinstance(value, expected_type):
                self.config[key] = value
                self.save_config()
                logging.info(f"Configuration updated: {key} = {value}")
            else:
                logging.warning(f"Invalid type for {key}: Expected {expected_type.__name__}, got {type(value).__name__}")
        else:
            logging.warning(f"Attempted to update unknown configuration key: {key}")

    def get(self, key):
        """
        Get the value of a specific configuration setting.
        
        :param key: The configuration key (e.g., "enable_monitoring")
        :return: The value of the configuration setting
        """
        return self.config.get(key)

    def set_logging_level(self):
        """
        Set the logging level based on the configuration setting.
        """
        log_level = self.get("log_level").upper()
        level = logging.getLevelName(log_level)
        logging.basicConfig(level=level)
        logging.info(f"Logging level set to {log_level}.")

# Singleton instance of PyvoConfig
pyvo_config = PyvoConfig()

# Example usage of PyvoConfig class
if __name__ == "__main__":
    # Example of updating and retrieving configuration values
    print("Initial Configuration:", pyvo_config.config)
    
    # Update specific configuration setting
    pyvo_config.update_config("enable_logging", False)
    
    # Get individual configuration setting
    logging_enabled = pyvo_config.get("enable_logging")
    print(f"Logging Enabled: {logging_enabled}")
    
    # Print the updated configuration
    print("Updated Configuration:", pyvo_config.config)
