import pytest
from unittest.mock import patch, MagicMock

import io_manager
from io_manager import AlarmPanel, FIREMAN, ALARM_TONE
from configuration import globalConfig

# dummy speaker
class DummySpeaker: pass

# dummy EmergencyMonitor
class DummyEmergencyMonitor: pass

# TST-6.0
# prueba el requerimiento [SW-11.2.8]
def test_set_indicator_mode_0():

    # clases Dummy
    speaker = DummySpeaker()
    emergency_monitor = DummyEmergencyMonitor()

    # setea modo 0
    globalConfig.activeZone = 0

    with patch.object(io_manager.AlarmPanel, 'set_indicator_state') as mock_set_indicator:
        
        # llama a AlarmPanel
        panel = AlarmPanel(speaker, emergency_monitor)
        
        # SW-11.2.8: prueba que se llama el set_indicator que despliega el indicador de modo 0
        mock_set_indicator.assert_any_call(io_manager.INDICATOR_ID_MODE_0, True)

# copiar test_set_indicator_mode_0 para el modo 1

# TST-4.0
# prueba el requerimiento SW-11.6.9
def test_bombero_alarma_speaker():
    
    # clases Dummy
    speaker = DummySpeaker()
    emergency_monitor = DummyEmergencyMonitor()

    speaker = MagicMock()
    emergency_monitor = MagicMock()

    # llama a AlarmPanel
    panel = AlarmPanel(speaker, emergency_monitor)

    # ejecuta el __on_button_press
    panel._AlarmPanel__on_button_press(FIREMAN)

    # SW-11.6.9: aserta si se inicia el speaker
    speaker.start.assert_called_once_with(ALARM_TONE)

# TST-5.0
# prueba el requerimiento SW-11.6.22
def test_bombero_alarma_contacto():
    
    # clases Dummy
    speaker = DummySpeaker()
    emergency_monitor = DummyEmergencyMonitor()
    speaker = MagicMock()
    emergency_monitor = MagicMock()

    # llama a AlarmPanel
    panel = AlarmPanel(speaker, emergency_monitor)

    # ejecuta el __on_button_press
    panel._AlarmPanel__on_button_press(FIREMAN)

    # SW-11.6.22: aserta si se contacta la central de emergencia
    emergency_monitor.dump_event.assert_called_once_with("BOMBEROS")



