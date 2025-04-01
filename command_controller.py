from configuration import globalConfig
from alert_controller import trigger_alarm, contact_central
from io_manager import LED_ID_ARMED, INDICATOR_ID_ERROR, INDICATOR_ID_MODE_0, INDICATOR_ID_MODE_1


"""
Lista de comandos aceptados por el sistema

#1: cambiar la contraseña del sistema
#2: asignar un sensor a una zona
#3: ingresar número telefónico de la central de monitoreo
#4: ingresar número de usuario

Cuando el usuario ingresa '#1', el siguiente input que recibe el software es la nueva contraseña.
Cuando el usuario ingresa '#2', el siguiente input que recibe el software es el número de sensor, el siguiente después de ese es la zona 0 o 1 a la cual asignar el sensor.
Cuando el usuario ingresa '#3', el siguiente input que recibe el software es el número telefónico de la central de monitoreo.
Cuando el usuario ingresa '#4', el siguiente input que recibe el software es el número de usuario.
Cuando el usuario ingresa '#5', el siguiente input que recibe el software es el modo de operacion.

"""
PASSWORD_LENGTH = 8
PHONE_LENGTH = 8
USER_NUM_LENGTH = 8


class CommandController:
    def __init__(self, io_manager):
        self.io_manager = io_manager
        self.awaiting_input = None  # Indica el proximo dato a recibir si se ingreso un comando especial
        self.password_errors = 0    # Numero de intentos fallidos para ingresar contraseña

    def process(self, command):
        if globalConfig.armed:
            if command == globalConfig.password:
                print("Contraseña correcta. Sistema desbloqueado")
                globalConfig.armed = False
                self.io_manager.set_led_state(LED_ID_ARMED, False)
                self.password_errors = 0
            else:
                print("Contraseña incorrecta. Sistema bloqueado")
                self.password_errors += 1

                if self.password_errors >= 3:
                  trigger_alarm()
                  contact_central()

            return

        if self.awaiting_input:
            self.handle_special_input(command)
            return

        if command == "#1":
            print("Ingrese la nueva contraseña:")
            self.awaiting_input = "password"
        elif command == "#2":
            print("Ingrese el número de sensor:")
            self.awaiting_input = "sensor"
        elif command == "#3":
            print("Ingrese el número telefónico de la central de monitoreo:")
            self.awaiting_input = "monitoring_number"
        elif command == "#4":
            print("Ingrese el número de usuario:")
            self.awaiting_input = "user_number"
        elif command == "#5":
            print("Ingrese el modo de operacion")
            self.awaiting_input = "operation_mode"
        else:
            if command == globalConfig.password:
              globalConfig.armed = True
              print("Contraseña correcta. Sistema bloqueado")
              self.io_manager.set_led_state(LED_ID_ARMED, True)
            else:
              print("Comando no reconocido")

    def handle_special_input(self, command):
        if self.awaiting_input == "password":
            if "*" in command or "#" in command:
                print("Caracteres invalidos en la nueva contraseña")
                return

            if len(command) != PASSWORD_LENGTH:
                print(f"Largo de contraseña {len(command)} invalido")
                return

            globalConfig.password = command
            print("Contraseña cambiada exitosamente")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "sensor":
            if command in ["0", "1", "2", "3", "4", "5", "6", "7", "8", \
                            "9", "10", "11", "12", "13", "14", "15"]:
              self.current_sensor = int(command)
              print("Ingrese la zona (0 o 1):")
              self.awaiting_input = "zone"
            else:
                print("Número de sensor inválido, debe ser del 0 al 15")

        elif self.awaiting_input == "zone":
            if command in ["0", "1"]:
                globalConfig.sensors[self.current_sensor].zone = int(command)
                print(f"Sensor {self.current_sensor} asignado a la zona {command}")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada
                self.current_sensor = None
            else:
                print("Zona inválida. Debe ser 0 o 1")

        elif self.awaiting_input == "monitoring_number":
            if len(command) != PHONE_LENGTH:
              print(f"Largo de telefono de {len(command)} invalido")
              return

            globalConfig.central_phone = command
            print(f"Número de la central de monitoreo actualizado: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "user_number":
            if len(command) != USER_NUM_LENGTH:
              print(f"Largo de numero de usuario de {len(command)} invalido")
              return

            globalConfig.user_identifier = command
            print(f"Número de usuario actualizado: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "operation_mode":
            if command in ["0", "1"]:
                globalConfig.activeZone = int(command)
                print(f"Modo {command} activado")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada

                if command == "0":
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, True)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, False)
                else:
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, False)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, True)

            else:
                print("Modo invalido. Debe ser 0 o 1")

"""
class MockingIOManager:
  def set_led_state(self, led_id, enable):
    pass

cntrl = CommandController(io_manager=MockingIOManager())

while True:
    command = input(">")
    cntrl.process(command)
"""
