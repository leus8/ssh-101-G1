import threading
import queue
import time
 
from io_manager import LED_ID_BATTERY, INDICATOR_ID_BATTERY

'''
Requirements: SW-11.6.1

This class runs the self-diagnosis test
and calls the IO Manager to read and display
battery information
'''

class BatteryMonitor:
    def __init__(self, io_manager):       
        self.io_manager = io_manager
        self.thread = threading.Thread(target=self.process_event, daemon=True)
        self.thread.start()

    def process_event(self):
        while True:
            vin = self.io_manager.vin.get()
            if vin < 105:
                # turn on battery LED
                self.io_manager.set_led_state(LED_ID_BATTERY, True)
                self.io_manager.set_indicator_state(INDICATOR_ID_BATTERY, True)
            else:
                # turn off battery LED
                self.io_manager.set_led_state(LED_ID_BATTERY, False)
                self.io_manager.set_indicator_state(INDICATOR_ID_BATTERY, False)
            
            # wait for 5 seconds
            time.sleep(5)



