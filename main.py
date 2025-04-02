import logging
from io_manager import AlarmPanel
from command_controller import CommandController

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(filename='ssh101.log', level=logging.INFO)

    app = AlarmPanel()
    commandController = CommandController(io_manager=app,
                                          logger=logger)
    app.set_command_controller(commandController)

    app.mainloop()

if __name__ == "__main__":
    main()

