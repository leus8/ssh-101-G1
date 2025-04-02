import threading
import queue
import time

VALID_PASSWORD = 0
WRONG_PASSWORD = 1

class Security:
    def __init__(self, logger, passwordTimeout, alertController, speaker):
        self.logger = logger
        self.passwordTimeout = passwordTimeout
        self.alertController = alertController
        self.speaker         = speaker

        self.password_errors = 0
        self.event_queue = queue.Queue()
        self.lock = threading.Lock()
        self.last_wrong_time = None  # Guarda el momento del primer password_wrong
        self.alert_thread = threading.Thread(target=self.__monitor_events, daemon=True)
        self.alert_thread.start()

    def __monitor_events(self):
        while True:
            try:
                event = self.event_queue.get(timeout=1)  # Espera hasta 1 segundo por un evento
                if event == WRONG_PASSWORD:
                    with self.lock:
                        if self.last_wrong_time is None:  # Solo guarda el primer intento fallido
                            self.last_wrong_time = time.time()
                            self.speaker.startBip()
                elif event == VALID_PASSWORD:
                    with self.lock:
                        self.last_wrong_time = None  # Resetea el contador solo si la contraseña es correcta
                        self.speaker.stopBip()

            except queue.Empty:
                # Si la cola está vacía, verificamos si han pasado 30 segundos desde el primer "password_wrong"
                with self.lock:
                    if self.last_wrong_time and time.time() - self.last_wrong_time >= self.passwordTimeout:
                        self.last_wrong_time = None  # Resetea después de la alerta
                        
                        # Generar alerta
                        self.alertController.alertPasswordTimeout()

    def __generate_event(self, event):
        if event in [VALID_PASSWORD, WRONG_PASSWORD]:
            self.event_queue.put(event)
            self.logger.info(f"Event received: {event}")
        else:
            self.logger.error("Invalid event")

    def checkPassword(self, expected, received):
        if expected == received:
            self.logger.error("Valid password")
            self.__generate_event(VALID_PASSWORD)
            self.password_errors = 0
            return True
        else:
            self.logger.error("Wrong password")
            self.password_errors += 1
            self.__generate_event(WRONG_PASSWORD)

            if self.password_errors >= 3:
              self.logger.info("3 failed tries, generating alert")
              self.alertController.trigger_alarm()
              self.alertController.contact_central()

            return False

