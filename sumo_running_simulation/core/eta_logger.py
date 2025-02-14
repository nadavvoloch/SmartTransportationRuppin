import datetime
from termcolor import colored

class ETAFileLogger:
    """ Handles logging specific to ETA tracking in a separate log file. """
    
    def __init__(self, log_file_path="custom_ETA_vehicle_log.log"):
        self.log_file = open(log_file_path, "w", encoding="utf-8")
        self.log("ETA tracking log file initialized.", "INFO", "cyan", class_name="ETAFileLogger", function_name="__init__")
        

    def log(self, message, level="INFO", color=None, class_name="", function_name=""):
        """ Logs a message with timestamp, level, and source class/function. """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [{class_name}::{function_name}] {message}"

        if color:
            print(colored(log_entry, color))
        else:
            print(log_entry)

        self.log_file.write(log_entry + "\n")

    def close(self):
        """ Closes the log file. """
        self.log_file.close()