import threading
import queue
from configuration import globalConfig
from alert_controller import trigger_alarm


def contact_central_temp():
  print("Contactando central!")

DOOR_SENSOR = 0

class SensorMonitor:
  def __init__(self, security, alertController):
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
          self.alertController.sensorAlert(sensor_id)


  def simulate_event(self, sensor_id):
    self.event_queue.put(sensor_id) # Simular la interrupcion de un sensor
