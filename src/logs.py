import glob
import os
import time

class Logging:
    def __init__(self):
        self.logFileOpened = False

    def log(self, log_string: str):
        logs_directory = os.getcwd() + "/logs"

        if not os.path.exists(logs_directory):
            os.mkdir(logs_directory)
        
        log_files = glob.glob(r"logs/log-*.txt")

        log_file_numbers = [int(file[9:-4]) for file in log_files]
        
        if not log_file_numbers:
            log_file_numbers.append(0)
        
        log_file_name = f"logs/log-{max(log_file_numbers) + 1 if not self.logFileOpened else max(log_file_numbers)}.txt"

        
        with open(log_file_name, "a" if self.logFileOpened else "w") as log_file:
            self.logFileOpened = True

            current_time = time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(time.time()))
            log_file.write(f"[{current_time}] {log_string.encode('ascii', 'replace').decode()}\n")
