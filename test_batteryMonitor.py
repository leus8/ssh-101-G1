import pytest
from unittest.mock import MagicMock, patch
from batteryMonitor import BatteryMonitor
from io_manager import LED_ID_BATTERY, INDICATOR_ID_BATTERY


class BatteryMonitorTestable(BatteryMonitor):
    def __init__(self, io_manager):
        self.io_manager = io_manager

# TST-1.0
# SW-11.6.21: preuba si se enciede led de bateria cuando Vin < 105 VAC
# valores a testear
@pytest.mark.parametrize("vin_value", [110, 105, 104, 100])
def test_vin_turn_on_battery_led(vin_value):
    
    # crea un mock
    mock_io_manager = MagicMock()
    # barrido de los valores a testear
    mock_io_manager.vin.get = MagicMock(return_value=vin_value)

    # ejecuta el loop una vez
    monitor = BatteryMonitorTestable(mock_io_manager)
    # termina el loop infinito cuando se ejecuta time.sleep()
    with patch("time.sleep", side_effect=Exception("Stop")):
        try:
            monitor.process_event()
        except Exception as e:
            assert str(e) == "Stop"

    # SW-11.6.21: aserta si se enciende led de bateria
    if vin_value < 105:
        mock_io_manager.set_led_state.assert_called_with(LED_ID_BATTERY, True)
    else:
        mock_io_manager.set_led_state.assert_called_with(LED_ID_BATTERY, False)

# TST-2.0
# SW-11.6.20: preuba si se enciede indicador de bateria cuando Vin < 105 VAC
# valores a testear
@pytest.mark.parametrize("vin_value", [110, 105, 104, 100])
def test_vin_turn_on_battery_indicator(vin_value):
    
    # crea un mock
    mock_io_manager = MagicMock()
    # barrido de los valores a testear
    mock_io_manager.vin.get = MagicMock(return_value=vin_value)

    # ejecuta el loop una vez
    monitor = BatteryMonitorTestable(mock_io_manager)
    # termina el loop infinito cuando se ejecuta time.sleep()
    with patch("time.sleep", side_effect=Exception("Stop")):
        try:
            monitor.process_event()
        except Exception as e:
            assert str(e) == "Stop"

    # SW-11.6.20: aserta si se enciende indicador de bateria
    if vin_value < 105:
        mock_io_manager.set_indicator_state.assert_called_with(INDICATOR_ID_BATTERY, True)
    else:
        mock_io_manager.set_indicator_state.assert_called_with(INDICATOR_ID_BATTERY, False)


# valores a testear
@pytest.mark.parametrize("vin_value", [105, 110])
def test_vin_turn_off_battery(vin_value):
    
    # crea un mock
    mock_io_manager = MagicMock()
    # barrido de los valores a testear
    mock_io_manager.vin.get = MagicMock(return_value=vin_value)  # Simula voltaje >= 105

    # ejecuta el loop una vez
    monitor = BatteryMonitorTestable(mock_io_manager)
    # termina el loop infinito cuando se ejecuta time.sleep()
    with patch("time.sleep", side_effect=Exception("Stop")):
        try:
            monitor.process_event()
        except Exception as e:
            assert str(e) == "Stop"

    # aserciones
    mock_io_manager.set_led_state.assert_called_with(LED_ID_BATTERY, False)
    mock_io_manager.set_indicator_state.assert_called_with(INDICATOR_ID_BATTERY, False)

# TST-3.0
# SW-11.6.1: prueba de tiempo
def test_tiempo_autodiagnostico():

    # crea un mock
    mock_io_manager = MagicMock()
    # valor cualquiera a testear
    mock_io_manager.vin.get = MagicMock(return_value=100)


    monitor = BatteryMonitorTestable(mock_io_manager)

    # guarda las veces que se llama sleep
    sleep_calls = []


    def mock_sleep(seconds):
        sleep_calls.append(seconds)
        # corre bucle dos veces
        if len(sleep_calls) >= 2:
            raise Exception("stop")

    # termina el loop infinito cuando se ejecuta time.sleep()
    with patch("time.sleep", side_effect=mock_sleep):
        try:
            monitor.process_event()
        except Exception as e:
            assert str(e) == "stop"

    # SW-11.6.1: aserta si el autodiagnostico se realizó nuevamente a los 5 segundos
    for duration in sleep_calls:
        assert 4 <= duration <= 6  # 5 ± 1