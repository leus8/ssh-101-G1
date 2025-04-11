from security import Security
from sensor_monitor import SensorMonitor
from io_manager import AlarmPanel, Speaker
from command_controller import CommandController
from batteryMonitor import BatteryMonitor
from emergency_monitor import EmergencyMonitor
import threading

def main():
    speaker = Speaker()

    # EmergencyMonitor Logger thread
    emergency_monitor = EmergencyMonitor()

    security = Security(doorTimeout=15,
                        alertController=emergency_monitor,
                        speaker=speaker)

    monitor = SensorMonitor(speaker=speaker,
                            security=security,
                            alertController=emergency_monitor)

    app = AlarmPanel(speaker=speaker,
                     emergency_monitor=emergency_monitor,
                     sensorTrigger=monitor)

    commandController = CommandController(io_manager=app,
                                          security=security,
                                          speaker=speaker)

    # BatteryMonitor Daemon
    batteryMonitor = BatteryMonitor(io_manager=app)

    # Tkinter loop
    app.set_command_controller(commandController)
    app.mainloop()

    # descomentar si se desea ver hilos activos al cerrar el progrma
    # print("Hilos activos:", threading.active_count())
    # for t in threading.enumerate():
    #     print("-", t.name)

if __name__ == "__main__":
    main()

