from io_manager import AlarmPanel
from command_controller import CommandController

if __name__ == "__main__":
    app = AlarmPanel()
    commandController = CommandController(io_manager=app)
    app.set_command_controller(commandController)

    app.mainloop()

