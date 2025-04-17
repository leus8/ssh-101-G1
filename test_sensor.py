import random
import time
from schema import Sensor
from sensor_monitor import SensorMonitor, globalConfig
from emergency_monitor import EVENT_SENSOR 

ZONE0 = 0
ZONE1 = 1

# [SW-11.6.4] Cuando la alarma es operada en Modo 0, el software
#             debe supervisar todos los sensores conectados.
# 
# Condiciones iniciales: funcionamiento normal del sistema
# Entradas: modo del sistema
# Salidas:  bandera que indica si el sensor es monitoreado.
# Casos:    1. Sensores con zonas random.
#           2. Todos los sensores pertenecientes a la zona 0.
#           3. Todos los sensores pertenecientes a la zona 1.
def test_sensor_monotired_on_mode0():
  sensors = []
  num_sensors = random.randint(1, 16)

  for i in range(num_sensors):
    new_sensor = Sensor(i)
    new_sensor.zone = random.randint(0, 1)

    sensors.append(new_sensor)

  # Caso 1: Sensores con zonas random
  for i in range(num_sensors):
    assert sensors[i].is_monitored(ZONE0)

  # Caso 2: Todos los sensores pertenecientes a la zona 0.
  for i in range(num_sensors):
    sensors[i].zone = ZONE0

  for i in range(num_sensors):
    assert sensors[i].is_monitored(ZONE0)

  # Caso 3: Todos los sensores pertenecientes a la zona 1.
  for i in range(num_sensors):
    sensors[i].zone = ZONE1

  for i in range(num_sensors):
    assert sensors[i].is_monitored(ZONE0)


# [SW-11.6.13] Cuando la alarma es operada en Modo 1, se supervisan
#              únicamente los sensores pertenecientes a la zona 1.
#
# Condiciones iniciales: funcionamiento normal del sistema
# Entradas: modo del sistema
# Salidas:  bandera que indica si el sensor es monitoreado.
# Casos:    1. Sensores con zonas random.
#           2. Todos los sensores pertenecientes a la zona 0.
#           3. Todos los sensores pertenecientes a la zona 1.
def test_sensor_monitored_on_mode1():
  sensors = []
  num_sensors = random.randint(1, 16)

  for i in range(num_sensors):
    new_sensor = Sensor(i)
    new_sensor.zone = random.randint(0, 1)

    sensors.append(new_sensor)

  # Caso 1: Sensores con zonas random
  for i in range(num_sensors):
    expected = sensors[i].zone == ZONE1
    assert expected == sensors[i].is_monitored(ZONE1)

  # Caso 2: Todos los sensores pertenecientes a la zona 0.
  for i in range(num_sensors):
    sensors[i].zone = ZONE0

  for i in range(num_sensors):
    assert sensors[i].is_monitored(ZONE1) is False

  # Caso 3: Todos los sensores pertenecientes a la zona 1.
  for i in range(num_sensors):
    sensors[i].zone = ZONE1

  for i in range(num_sensors):
    assert sensors[i].is_monitored(ZONE1)


class MockEvent:
  activated: bool
  timestamp: float

  def __init__(self):
    self.activated = False
    self.timestamp = 0

  def reset(self):
    self.activated = False
    self.timestamp = 0

  def setTimestamp(self):
    self.activated = True
    self.timestamp = time.time()

  def getTimestamp(self):
    return self.timestamp

  def getActivated(self):
    return self.activated

class MockSpeaker(MockEvent):
  def start(self, tone):
    self.setTimestamp()

class MockAlertController(MockEvent):
  user_identifier: int
  event: int
  sensor_id: int

  def dump_event(self, user_identifier, event, sensor_id):
    self.setTimestamp()
    self.user_identifier = user_identifier
    self.event = event
    self.sensor_id = sensor_id

class MockSecutiry():
  def handleDoorEvent(self):
    pass

# [SW-11.3.1] El software debe reaccionar a la activación de un sensor en un
#             tiempo menor a 500 ms un 95% de las veces.
#
# Condiciones iniciales: sistema armado y monitoreando la zona 0
# Entradas: activacion de un sensor diferente al de la puerta
# Salidas:  tiempo de respuesta en procesar el evento
# Casos:    1. Enviar señal de alerta en uno de los sensores, y medir
#              el tiempo que se tardo en activar la alarma y conectar la central
def test_sensor_response_time():
  mockSpeaker = MockSpeaker()
  mockAlertController = MockAlertController()
  sensorMonitor = SensorMonitor(speaker=mockSpeaker,
                                alertController=mockAlertController,
                                security=MockSecutiry())
  globalConfig.armed = True
  globalConfig.activeZone = ZONE0

  start = time.time()

  sensor_id = random.randint(1, 15)
  sensorMonitor.simulate_event(sensor_id)

  time.sleep(1)

  # Tiempo de activacion de la alarma sonora
  speakerTime = mockSpeaker.getTimestamp() - start
  assert speakerTime < 0.501

  # Tiempo de activacion alerta central
  alertTime = mockAlertController.getTimestamp() - start
  assert alertTime < 0.501

# [SW-11.6.17] Cuando se activa un sensor correspondiente a la zona activa y el
#              sistema está armado, el software debe activar la bocina y realizar
#              una llamada al centro de supervisión de la agencia de seguridad
#              indicando el número de usuario y el número de sensor activado.
#
# Condiciones iniciales: funcionamiento normal del sistema
# Entradas: estado de armado del sistema, zona activa, zona del sensor activado
# Salidas:  generacion de alerta
# Casos:    Sistema | Zona   | Zona sensor | Alerta
#           armado  | activa |   activado  | generada
#       1.     0    |    0   |      0      |    0
#       2.     0    |    0   |      1      |    0
#       3.     0    |    1   |      0      |    0
#       4.     0    |    1   |      1      |    0
#       5.     1    |    0   |      0      |    1
#       6.     1    |    0   |      1      |    1
#       7.     1    |    1   |      0      |    0
#       8.     1    |    1   |      1      |    1
def test_sensor_central_alert_1():
  mockSpeaker = MockSpeaker()
  mockAlertController = MockAlertController()
  sensorMonitor = SensorMonitor(speaker=mockSpeaker,
                                alertController=mockAlertController,
                                security=MockSecutiry())
  globalConfig.user_identifier = random.randint(10000000, 99999999)

  test_cases = [ (0, ZONE0, ZONE0, False),
                 (0, ZONE0, ZONE1, False),
                 (0, ZONE1, ZONE0, False),
                 (0, ZONE1, ZONE1, False),
                 (1, ZONE0, ZONE0, True ),
                 (1, ZONE0, ZONE1, True ),
                 (1, ZONE1, ZONE0, False),
                 (1, ZONE1, ZONE1, True )]

  for armed, activeZone, sensorZone, alertGenerated in test_cases:
    mockSpeaker.reset()
    mockAlertController.reset()

    sensor_id = random.randint(1, 15)

    globalConfig.armed = armed
    globalConfig.activeZone = activeZone
    globalConfig.sensors[sensor_id].zone = sensorZone

    sensorMonitor.simulate_event(sensor_id)

    time.sleep(0.501)

    alert = mockSpeaker.getActivated() and mockAlertController.getActivated()
    assert alert is alertGenerated, f"Failed on testcase armed: {armed}, activeZone: {activeZone}, " \
                                    f"sensorZone: {sensorZone}, alertGenerated: {alertGenerated}"

# [SW-11.6.17] Cuando se activa un sensor correspondiente a la zona activa y el
#              sistema está armado, el software debe activar la bocina y realizar
#              una llamada al centro de supervisión de la agencia de seguridad
#              indicando el número de usuario y el número de sensor activado.
#
# Condiciones iniciales: sistema armado y monitoreando una zona
# Entradas: activacion de un sensor
# Salidas:  activacion de la bocina, llamado a central, numero de usuario y sensor activado
# Casos:    1. Activar un sensor monitoreado y verificar que se active la bocina
#              y se contacta a la central indicando el numero de usuario y el
#              sensor activado.
def test_sensor_central_alert_2():
  mockSpeaker = MockSpeaker()
  mockAlertController = MockAlertController()
  sensorMonitor = SensorMonitor(speaker=mockSpeaker,
                                alertController=mockAlertController,
                                security=MockSecutiry())
  globalConfig.user_identifier = random.randint(10000000, 99999999)
  sensor_id = random.randint(1, 15)
  globalConfig.activeZone = random.randint(0, 1)
  globalConfig.sensors[sensor_id].zone = globalConfig.activeZone

  # Caso 1: Activar un sensor monitoreado y verificar que se active la bocina
  #         y se contacta a la central indicando el numero de usuario y el
  #         sensor activado.

  sensorMonitor.simulate_event(sensor_id)

  time.sleep(0.5)

  # Checks de la bocina
  assert mockSpeaker.getActivated()

  # Checks de la central
  assert mockAlertController.getActivated()
  assert EVENT_SENSOR == mockAlertController.event
  assert sensor_id == mockAlertController.sensor_id
  assert globalConfig.user_identifier == mockAlertController.user_identifier
