import time
from configuration import globalConfig
from io_manager import LED_ID_ARMED, INDICATOR_ID_ERROR, INDICATOR_ID_MODE_0, INDICATOR_ID_MODE_1, INDICATOR_ID_ERROR


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
    def __init__(self, io_manager, security):
        self.io_manager = io_manager
        self.security = security
        self.awaiting_input = None  # Indica el proximo dato a recibir si se ingreso un comando especial
        self.password_errors = 0    # Numero de intentos fallidos para ingresar contraseña

    def process(self, command):
        if globalConfig.armed:
            if self.security.checkPassword(globalConfig.password, command):
                print("Password is correct. System unlocked")
                globalConfig.armed = False
                self.io_manager.set_led_state(LED_ID_ARMED, False)
                self.password_errors = 0
            return

        if self.awaiting_input:
            self.handle_special_input(command)
            return

        if command == "#1":
            print("Input new password:")
            self.awaiting_input = "password"
        elif command == "#2":
            print("Input the sensor number:")
            self.awaiting_input = "sensor"
        elif command == "#3":
            print("Input the central's phone number:")
            self.awaiting_input = "monitoring_number"
        elif command == "#4":
            print("Input user number:")
            self.awaiting_input = "user_number"
        elif command == "#5":
            print("Input operation mode")
            self.awaiting_input = "operation_mode"
        else:
            if self.security.checkPassword(globalConfig.password, command):
              globalConfig.armed = True
              print("Password is correct. System blocked")
              self.io_manager.set_led_state(LED_ID_ARMED, True)
            else:
              print(f"Unrecognized command: {command}")

    def handle_special_input(self, command):
        if self.awaiting_input == "password":
            if "*" in command or "#" in command:
                print("New password includes invalid characters")
                return

            if len(command) != PASSWORD_LENGTH:
                print(f"Password length {len(command)} invalid")
                return

            globalConfig.password = command
            print("Password changed succesfully")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "sensor":
            if command in ["0", "1", "2", "3", "4", "5", "6", "7", "8", \
                            "9", "10", "11", "12", "13", "14", "15"]:
              self.current_sensor = int(command)
              print("Input zone (0 o 1):")
              self.awaiting_input = "zone"
            else:
                print("Invalid sensor number, must be between 0 and 15")

        elif self.awaiting_input == "zone":
            if command in ["0", "1"]:
                globalConfig.sensors[self.current_sensor].zone = int(command)
                print(f"Sensor {self.current_sensor} assigned to zone {command}")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada
                self.current_sensor = None
            else:
                print("Invalid zone. Must be 0 or 1")

        elif self.awaiting_input == "monitoring_number":
            if len(command) != PHONE_LENGTH:
              print(f"Phone length {len(command)} invalid")
              # SW-11.6.8: display error for 5 seconds
              self.io_manager.set_indicator_state(INDICATOR_ID_ERROR, True)
              self.io_manager.after(5 * 1000, lambda: self.io_manager.set_indicator_state(INDICATOR_ID_ERROR, False))
              return

            globalConfig.central_phone = command
            print(f"Central phone number updated: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "user_number":
            if len(command) != USER_NUM_LENGTH:
              print(f"User number has an invalid length of {len(command)}")
              # SW-11.6.6: display error for 5 seconds
              self.io_manager.set_indicator_state(INDICATOR_ID_ERROR, True)
              self.io_manager.after(5 * 1000, lambda: self.io_manager.set_indicator_state(INDICATOR_ID_ERROR, False))
              return

            globalConfig.user_identifier = command
            print(f"User number updated: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "operation_mode":
            if command in ["0", "1"]:
                globalConfig.activeZone = int(command)
                print(f"Mode {command} activated")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada

                if command == "0":
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, True)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, False)
                else:
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, False)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, True)

            else:
                print("Invalid mode. Must be 0 or 1")

