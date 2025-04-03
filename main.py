from security import Security
from alarm_controller import SensorMonitor
from io_manager import AlarmPanel, Speaker
from command_controller import CommandController
from batteryMonitor import BatteryMonitor
from emergency_monitor import EmergencyMonitor


class MockingAlertController:
    def alertDoorTimeout(self):
        print("Contacting central...")

    def trigger_alarm(self):
        print("Alarma generada!")

    def contact_central(self):
        print("Contactando central!")


def main():
    speaker = Speaker()

    # EmergencyMonitor Logger thread
    emergency_monitor = EmergencyMonitor()

    alertController = MockingAlertController()

    security = Security(doorTimeout=5,
                        alertController=alertController,
                        speaker=speaker)

    monitor = SensorMonitor(security=security,
                            alertController=alertController)

    app = AlarmPanel(speaker=speaker,
                     emergency_monitor=emergency_monitor,
                     sensorTrigger=monitor)

    commandController = CommandController(io_manager=app,
                                          security=security)

    # BatteryMonitor Daemon
    batteryMonitor = BatteryMonitor(io_manager=app)

    # Tkinter loop
    app.set_command_controller(commandController)
    app.mainloop()

if __name__ == "__main__":
    main()

