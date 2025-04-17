import json
from datetime import datetime
import threading


# Types of emergency alerts
EVENT_SENSOR = 0
EVENT_FIREMAN = 1
EVENT_PANIC = 2
EVENT_PASSWORD = 3


'''
Requirements: SW-11.6.19 (main), SW-11.6.9, SW-11.6.11
Logs and emergency event and dumps the file contents in JSON style format
'''
class EmergencyMonitor:
    def __init__(self):
        self.log_file = "events.log"
        self.lock = threading.Lock()

    def __contact_central(self, user_identifier, event):
        # generate the JSON entry
        log_entry = {
            "Evento": event,
            "Usuario": user_identifier,
            "Registro": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        # dumps json to event_log file
        with self.lock:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

    def dump_event(self, user_identifier, event_type, sensor_id=-1):
        event_text = ""
        
        if event_type == EVENT_SENSOR:
            event_text = f"sensor_{sensor_id}"
        elif event_type == EVENT_FIREMAN:
            event_text = "bomberos"
        elif event_type == EVENT_PANIC:
            event_text = "panico"
        elif event_type == EVENT_PASSWORD:
            event_text = "Password tries"

        print(f"EventMonitor received a {event_text} event")

        self.__contact_central(user_identifier, event_text)
