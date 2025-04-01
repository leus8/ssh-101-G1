from configuration import globalConfig
from alert_controller import trigger_alarm, contact_central
from io_manager import LED_ID_ARMED


class CommandController:
  def __init__(self, io_manager):
    self.io_manager = io_manager
    self.password_errors = 0


  def process(self, command):
    print(f"command: {command}")

    # Verificar estado de armado y desarmado del sistema
    if globalConfig.armed:
      self.checkForSystemDisarmed(command)

    elif not globalConfig.armed:
      self.disarmed_commands(command)
        

  def disarmed_commands(self, command):
    """
    Comandos habilitados cuando el sistema esta en modo desarmado
    """
    if command == globalConfig.password:
      globalConfig.armed = True
      self.io_manager.set_led_state(LED_ID_ARMED, True)


  def checkForSystemDisarmed(self, password):
    if password == globalConfig.password:
      globalConfig.armed = False
      self.io_manager.set_led_state(LED_ID_ARMED, False)
      self.password_errors = 0
    else:
      print(f"Password {password} is incorrect")
      self.password_errors += 1

    if self.password_errors >= 3:
      trigger_alarm()
      contact_central()
