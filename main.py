import logging
from security import Security
from io_manager import AlarmPanel, Speaker
from command_controller import CommandController

logger = logging.getLogger(__name__)


class Print:
    def info(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

class MockingAlertController():
    def alertPasswordTimeout(self):
        print("Contacting central...")

    def trigger_alarm():
        print("Alarma generada!")

    def contact_central():
        print("Contactando central!")


def main():
    logging.basicConfig(filename='ssh101.log', level=logging.INFO)

    app = AlarmPanel()

    security = Security(logger=Print(),
                        passwordTimeout=5,
                        alertController=MockingAlertController(),
                        speaker=Speaker())

    commandController = CommandController(logger=logger,
                                          io_manager=app,
                                          security = security)

    # Tkinter loop
    app.set_command_controller(commandController)
    app.mainloop()

if __name__ == "__main__":
    main()

