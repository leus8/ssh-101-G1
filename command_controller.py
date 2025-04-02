from configuration import globalConfig
from alert_controller import trigger_alarm
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
    def __init__(self, logger, io_manager, security):
        self.logger = logger
        self.io_manager = io_manager
        self.security = security
        self.awaiting_input = None  # Indica el proximo dato a recibir si se ingreso un comando especial
        self.password_errors = 0    # Numero de intentos fallidos para ingresar contraseña

    def process(self, command):
        if globalConfig.armed:
            if self.security.checkPassword(globalConfig.password, command):
                self.logger.info("Password is correct. System unlocked")
                globalConfig.armed = False
                self.io_manager.set_led_state(LED_ID_ARMED, False)
                self.password_errors = 0
            return

        if self.awaiting_input:
            self.handle_special_input(command)
            return

        if command == "#1":
            self.logger.info("Input new password:")
            self.awaiting_input = "password"
        elif command == "#2":
            self.logger.info("Input the sensor number:")
            self.awaiting_input = "sensor"
        elif command == "#3":
            self.logger.info("Input the central's phone number:")
            self.awaiting_input = "monitoring_number"
        elif command == "#4":
            self.logger.info("Input user number:")
            self.awaiting_input = "user_number"
        elif command == "#5":
            self.logger.info("Input operation mode")
            self.awaiting_input = "operation_mode"
        else:
            if self.security.checkPassword(globalConfig.password, command):
              globalConfig.armed = True
              self.logger.info("Password is correct. System blocked")
              self.io_manager.set_led_state(LED_ID_ARMED, True)
            else:
              self.logger.error(f"Unrecognized command: {command}")

    def handle_special_input(self, command):
        if self.awaiting_input == "password":
            if "*" in command or "#" in command:
                self.logger.error("New password includes invalid characters")
                return

            if len(command) != PASSWORD_LENGTH:
                self.logger.error(f"Password length {len(command)} invalid")
                return

            globalConfig.password = command
            self.logger.info("Password changed succesfully")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "sensor":
            if command in ["0", "1", "2", "3", "4", "5", "6", "7", "8", \
                            "9", "10", "11", "12", "13", "14", "15"]:
              self.current_sensor = int(command)
              self.logger.info("Input zone (0 o 1):")
              self.awaiting_input = "zone"
            else:
                self.logger.error("Invalid sensor number, must be between 0 and 15")

        elif self.awaiting_input == "zone":
            if command in ["0", "1"]:
                globalConfig.sensors[self.current_sensor].zone = int(command)
                self.logger.info(f"Sensor {self.current_sensor} assigned to zone {command}")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada
                self.current_sensor = None
            else:
                self.logger.error("Invalid zone. Must be 0 or 1")

        elif self.awaiting_input == "monitoring_number":
            if len(command) != PHONE_LENGTH:
              self.logger.info(f"Phone length {len(command)} invalid")
              return

            globalConfig.central_phone = command
            self.logger.info(f"Central phone number updated: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "user_number":
            if len(command) != USER_NUM_LENGTH:
              self.logger.info(f"User number has an invalid length of {len(command)}")
              return

            globalConfig.user_identifier = command
            self.logger.info(f"User number updated: {command}")
            self.awaiting_input = None  # Restablecer el estado de espera de entrada

        elif self.awaiting_input == "operation_mode":
            if command in ["0", "1"]:
                globalConfig.activeZone = int(command)
                self.logger.info(f"Mode {command} activated")
                self.awaiting_input = None  # Restablecer el estado de espera de entrada

                if command == "0":
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, True)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, False)
                else:
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_0, False)
                    self.io_manager.set_indicator_state(INDICATOR_ID_MODE_1, True)

            else:
                self.logger.error("Invalid mode. Must be 0 or 1")

