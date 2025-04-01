from dataclasses import dataclass
from schema import Sensor

@dataclass
class Configuration:
  activeZone: int
  armed: bool
  password: str
  sensors: list

  def __init__(self):
    self.activeZone = 1
    self.armed = True
    self.password = "1234"
    self.sensors = [Sensor(0,  0), Sensor(1,  0), Sensor(2,  0), Sensor(3,  0),
                    Sensor(4,  0), Sensor(5,  0), Sensor(6,  0), Sensor(7,  0),
                    Sensor(8,  0), Sensor(9,  0), Sensor(10, 0), Sensor(11, 0),
                    Sensor(12, 0), Sensor(13, 0), Sensor(14, 0), Sensor(15, 0)]


# Structure that stores the global configuration of the app
globalConfig = Configuration()
