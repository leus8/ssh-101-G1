import logging
from security import Security
from alarm_controller import SensorMonitor
from io_manager import AlarmPanel, Speaker
from command_controller import CommandController

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

    speaker = Speaker()
    app = AlarmPanel(speaker=speaker)

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

    # Tkinter loop
    app.set_command_controller(commandController)
    app.mainloop()

if __name__ == "__main__":
    main()

