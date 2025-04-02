import logging
from security import Security
from alarm_controller import SensorMonitor
from io_manager import AlarmPanel, Speaker
from command_controller import CommandController
from batteryMonitor import BatteryMonitor
from emergency_monitor import EmergencyMonitor

logger = logging.getLogger(__name__)


class Print:
    def info(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

class MockingAlertController:
    def alertDoorTimeout(self):
        print("Contacting central...")

    def trigger_alarm(self):
        print("Alarma generada!")

    def contact_central(self):
        print("Contactando central!")


def main():
    logging.basicConfig(filename='ssh101.log', level=logging.INFO)

    # EmergencyMonitor Logger thread
    emergency_monitor = EmergencyMonitor()

    speaker = Speaker()
    app = AlarmPanel(speaker=speaker, emergency_monitor=emergency_monitor)

    alertController = MockingAlertController()

    security = Security(logger=Print(),
                        doorTimeout=5,
                        alertController=alertController,
                        speaker=speaker)

    monitor = SensorMonitor(logger=Print(),
                            security=security,
                            alertController=alertController)

    commandController = CommandController(logger=logger,
                                          io_manager=app,
                                          security = security)

    # BatteryMonitor Daemon
    batteryMonitor = BatteryMonitor(io_manager=app)

    # Tkinter loop
    app.set_command_controller(commandController)
    app.mainloop()

if __name__ == "__main__":
    main()

