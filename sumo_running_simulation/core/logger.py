import datetime
from termcolor import colored

class Logger:
    """ Handles logging to both the console and a log file with timestamps and colors. """
    def __init__(self, log_file_path="main/simulation_log.log"):
        self.log_file = open(log_file_path, "w", encoding="utf-8")

    def log(self, message, level="INFO", color=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        if color:
            print(colored(log_entry, color))
        else:
            print(log_entry)

        self.log_file.write(log_entry + "\n")

    def close(self):
        """ Closes the log file. """
        self.log_file.close()
