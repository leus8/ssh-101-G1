from dataclasses import dataclass
from schema import Sensor

@dataclass
class Configuration:
  activeZone: int
  armed: bool
  password: str
  sensors: list

  def __init__(self):
    self.activeZone = 0
    self.armed = True
    self.password = "12345678"
    self.central_phone = "88888888"
    self.user_identifier = "00000000"
    self.sensors = [Sensor(0),  Sensor(1),  Sensor(2),  Sensor(3),
                    Sensor(4),  Sensor(5),  Sensor(6),  Sensor(7),
                    Sensor(8),  Sensor(9),  Sensor(10), Sensor(11),
                    Sensor(12), Sensor(13), Sensor(14), Sensor(15)]


# Structure that stores the global configuration of the app
globalConfig = Configuration()
