import threading
import queue
from configuration import globalConfig
from emergency_monitor import EVENT_SENSOR
from io_manager import ALARM_TONE


def contact_central_temp():
  print("Contactando central!")

DOOR_SENSOR = 0

class SensorMonitor:
  def __init__(self, speaker, security, alertController):
    self.speaker = speaker
    self.security = security
    self.alertController = alertController

    self.event_queue = queue.Queue()
    self.thread = threading.Thread(target=self.__process_event, daemon=True)
    self.thread.start()


  def __process_event(self):
    while True:
      sensor_id = self.event_queue.get() # Bloquea hasta que haya un evento
      sensor = globalConfig.sensors[sensor_id]

      print(f"Procesando evento en sensor {sensor_id}")

      if sensor_id == DOOR_SENSOR:
        self.security.handleDoorEvent()

      elif globalConfig.armed and sensor.is_monitored(globalConfig.activeZone):
          self.speaker.start(ALARM_TONE)
          self.alertController.dump_event(globalConfig.user_identifier,
                                          EVENT_SENSOR,
                                          sensor_id)


  def simulate_event(self, sensor_id):
    self.event_queue.put(sensor_id) # Simular la interrupcion de un sensor
