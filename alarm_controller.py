import threading
import queue
from configuration import globalConfig
from alert_controller import trigger_alarm


def contact_central_temp():
  print("Contactando central!")


class SensorMonitor:
  def __init__(self):
    self.event_queue = queue.Queue()
    self.thread = threading.Thread(target=self.process_event, daemon=True)
    self.thread.start()

  def process_event(self):
    while True:
      sensor_id = self.event_queue.get() # Bloquea hasta que haya un evento
      print(f"Procesando evento en sensor {sensor_id}")

      sensor = globalConfig.sensors[sensor_id]

      if globalConfig.armed and sensor.is_monitored(globalConfig.activeZone):
        trigger_alarm()
        contact_central_temp()

  def simulate_event(self, sensor_id):
    self.event_queue.put(sensor_id) # Simular la interrupcion de un sensor


monitor = SensorMonitor()
monitor.simulate_event(3)
monitor.simulate_event(5)
monitor.simulate_event(7)

from time import sleep
sleep(2)

