import threading
import time

from io_manager import ALARM_TONE, SINGLE_TONE0, SINGLE_TONE1

VALID_PASSWORD = 0
WRONG_PASSWORD = 1
SENSOR_ACTIVATED = 2

class Security:
    def __init__(self, logger, doorTimeout, alertController, speaker):
        self.logger          = logger
        self.doorTimeout     = doorTimeout
        self.alertController = alertController
        self.speaker         = speaker

        self.password_errors = 0
        self.lock = threading.Lock()
        self.door_event_time = None  # Guarda el momento del evento de puerta
        self.alert_thread = threading.Thread(target=self.__monitor_door, daemon=True)
        self.alert_thread.start()

    def __monitor_door(self):
        while True:
            with self.lock:
                if self.door_event_time is not None:
                    if time.time() - self.door_event_time >= self.doorTimeout:
                        self.door_event_time = None  # Resetea despues de la alerta

                        # Generar alerta
                        self.alertController.alertDoorTimeout()
                        self.speaker.stop()
                        self.speaker.start(ALARM_TONE)

            time.sleep(1)


    def handleDoorEvent(self):
        with self.lock:
            if self.door_event_time is None:
                self.door_event_time = time.time()
                self.speaker.start(SINGLE_TONE0)


    def checkPassword(self, expected, received):
        if expected == received:
            self.logger.info("Valid password")
            self.speaker.stop()
            self.password_errors = 0
            return True

        else:
            self.logger.error("Wrong password")
            self.password_errors += 1

            if self.password_errors >= 3:
                self.password_errors = 0
                self.logger.info("3 failed tries, generating alert")
                self.speaker.start(ALARM_TONE)
                self.alertController.contact_central()

            return False

