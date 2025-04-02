import json
from datetime import datetime
import threading
from configuration import globalConfig

'''
Requirements: SW-11.6.19 (main), SW-11.6.9, SW-11.6.11
Logs and emergency event and dumps the file contents in JSON style format
'''
class EmergencyMonitor:
    def __init__(self):
        self.log_file = "event_log.json"
        self.lock = threading.Lock()

    def dump_event(self, button_type):
        
        # generate the JSON entry
        log_entry = {
            "Evento": button_type,
            "Usuario": globalConfig.user_identifier,
            "Registro": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        # dumps json to event_log file
        with self.lock:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
