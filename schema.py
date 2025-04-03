from dataclasses import dataclass


@dataclass
class Sensor:
  id: int
  zone: int

  def __init__(self, id):
    self.zone = 0

  def is_monitored(self, activeZone):
    # print(f"sensor id: {self.id} zone: {self.zone} activeZone: {activeZone}")
    if activeZone == 0:
      return True
    elif self.zone == activeZone:
      return True
    else:
      return False
