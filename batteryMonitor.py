'''
Requirements: SW-11.6.1

Input: Vin

This function runs the self-diagnosis test
and calls the IO Manager to display
battery information
'''
def batteryMonitor(panel, vin):

    # run the self_diagnosis
    self_diagnosis(panel, vin)
    # SW-11.6.1: wait 5 seconds
    panel.after(5000, lambda: batteryMonitor(panel, vin))


def self_diagnosis(panel, vin):
    # SW-11.6.1:
    # VIN < 105 VAC: disconnected
    # VIN  <= 105 VAC: connected
    if vin < 105:
        # turn on battery LED
        panel.set_led_state(0, True)
        panel.set_indicator_state(2, True)
    else:
        # turn off battery LED
        panel.set_led_state(0, False)
        panel.set_indicator_state(2, False)


