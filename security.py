import threading
import time
import traceback

from io_manager import ALARM_TONE, SINGLE_TONE1
from emergency_monitor import EVENT_SENSOR, EVENT_PASSWORD

DOOR_SENSOR_ID = 0


class Security:
    def __init__(self, doorTimeout, alertController, speaker):
        self.doorTimeout     = doorTimeout
        self.alertController = alertController
        self.speaker         = speaker

        self.password_errors = 0
        self.lock = threading.Lock()
        self.door_event_time = None  # Guarda el momento del evento de puerta
        self.alert_thread = threading.Thread(target=self.__monitor_door, daemon=True)
        self.alert_thread.start()

    def __monitor_door(self):
        # comentar si no se quiere usar
        # print("Profundidad de pila:", len(traceback.extract_stack()))
        while True:
            with self.lock:
                if self.door_event_time is not None:
                    if time.time() - self.door_event_time >= self.doorTimeout:
                        self.door_event_time = None  # Resetea despues de la alerta

                        # Generar alerta
                        self.alertController.dump_event(EVENT_SENSOR, DOOR_SENSOR_ID)
                        self.speaker.stop()
                        self.speaker.start(ALARM_TONE)

            time.sleep(1)


    def handleDoorEvent(self):
        # comentar si no se quiere usar
        # print("Profundidad de pila:", len(traceback.extract_stack()))
        with self.lock:
            if self.door_event_time is None:
                self.door_event_time = time.time()
                self.speaker.start(SINGLE_TONE1)


    def checkPassword(self, expected, received):
        # comentar si no se quiere usar
        # print("Profundidad de pila:", len(traceback.extract_stack()))
        if expected == received:
            print("Valid password")
            self.speaker.stop()
            self.door_event_time = None
            self.password_errors = 0
            return True

        else:
            print("Wrong password")
            self.password_errors += 1

            if self.password_errors >= 3:
                self.password_errors = 0
                print("3 failed tries, generating alert")
                self.speaker.start(ALARM_TONE)
                self.alertController.dump_event(EVENT_PASSWORD)

            return False

