import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, ttk

import threading
import numpy as np
import sounddevice as sd

from configuration import globalConfig
from emergency_monitor import EVENT_FIREMAN, EVENT_PANIC

# Types of tones
ALARM_TONE = 0
SINGLE_TONE0 = 1
SINGLE_TONE1 = 2

# Button widths
W5, W10 = 5, 10

# Button text
ESC = "Esc"
ENTER = "Enter"
PANIC = "Pánico"
FIREMAN = "Bomberos"

LED_ID_BATTERY = 0 
LED_ID_ARMED = 1

INDICATOR_ID_MODE_0 = 0
INDICATOR_ID_MODE_1 = 1
INDICATOR_ID_BATTERY = 2
INDICATOR_ID_ERROR = 3


class AlarmPanel(tk.Tk):
    def __init__(self, speaker, emergency_monitor, sensorTrigger):
        super().__init__()
        self.title("SSH-101 Alarm Panel")
        self.geometry("630x300")
        self.configure(bg='lightgray')

        self.leds = {}  # Diccionario para almacenar los LEDs (referencias a los Canvas)
        self.indicators = {}  # Diccionario para almacenar los indicadores (referencias a los Labels)
        self.screen_content = "" # Variable para almacenar el texto en la pantalla LCD
        self.command_controller = None
        self.speaker = speaker
        self.emergency_monitor = emergency_monitor
        self.sensorTrigger = sensorTrigger
        self.vin = tk.IntVar(value=105) # Vin variable, default to 105 VAC.

        # Contenedor que agrupa la pantalla LCD y los LEDs
        self.lcd_led_frame = Frame(self, bg="lightgray")
        self.lcd_led_frame.grid(row=0,
                                column=0,
                                columnspan=4,
                                padx=20,
                                pady=10,
                                sticky='ew')

        # Contenedor de la pantalla LCD
        self.lcd_frame = Frame(self.lcd_led_frame,
                               bg="white",
                               relief="sunken",
                               bd=3,
                               width=300,
                               height=100)
        self.lcd_frame.grid(row=0,
                            column=0,
                            columnspan=4,
                            sticky="ew")
        self.lcd_frame.pack_propagate(False)

        # Texto principal en la pantalla LCD
        self.screen_text = Label(self.lcd_frame,
                                 text=self.screen_content,
                                 font=("Arial", 18, "bold"),
                                 bg="white",
                                 fg="black")
        self.screen_text.pack(side="left",
                              padx=10,
                              pady=10)

        # Frame para los modos de operación dentro de la pantalla LCD
        self.indicators_frame = Frame(self.lcd_frame, bg="white")
        self.indicators_frame.pack(side="right", padx=20, pady=5)

        # Modos de operación dentro de la pantalla LCD
        self.indicators = ["Modo 0", "Modo 1", "Batería", "Error"]
        for i, mode in enumerate(self.indicators):
            lbl = Label(self.indicators_frame,
                        text=mode,
                        font=("Arial", 8),
                        bg="white",
                        fg="gray")
            lbl.pack(anchor="e")
            self.indicators[i] = lbl # Guardar la referencia del Label

        # LED Indicators dentro del mismo contenedor que la pantalla
        self.led_frame = Frame(self.lcd_led_frame, bg='lightgray')
        self.led_frame.grid(row=1,
                            column=0,
                            columnspan=4,
                            pady=5,
                            sticky='ew')

        # Configurar columnas para centrar los LEDs
        self.led_frame.columnconfigure(0, weight=1)
        self.led_frame.columnconfigure(1, weight=1)

        # Crear los LEDs con texto abajo
        self.__create_led(self.led_frame, "Batería", "orange", 0)
        self.__create_led(self.led_frame, "Armada", "orange", 1)

        # Keypad Buttons
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row=0,
                                column=4,
                                columnspan=4,
                                padx=10,
                                pady=10,
                                sticky='w')

        buttons = [
            ('1', 0, 0, W5), ('2', 0, 1, W5), ('3', 0, 2, W5), (ESC,     0, 3, W10),
            ('4', 1, 0, W5), ('5', 1, 1, W5), ('6', 1, 2, W5), (ENTER,   1, 3, W10),
            ('7', 2, 0, W5), ('8', 2, 1, W5), ('9', 2, 2, W5), (PANIC,   2, 3, W10),
            ('*', 3, 0, W5), ('0', 3, 1, W5), ('#', 3, 2, W5), (FIREMAN, 3, 3, W10),
        ]

        for (text, row, col, width) in buttons:
            bg = "white smoke"
            fg = "black"

            if text in ['Pánico', 'Bomberos']:
                bg = "blue"
                fg = "white"

            Button(self.buttons_frame,
                   text=text,
                   width=width,
                   height=2,
                   bg=bg,
                   fg=fg,
                   command=lambda t=text: self.__on_button_press(t)).grid(row=row, column=col, padx=5, pady=5)

        # set values for LEDs and indicators
        if globalConfig.activeZone == 0:
            self.set_indicator_state(INDICATOR_ID_MODE_0, True)
        else:
            self.set_indicator_state(INDICATOR_ID_MODE_1, True)

        self.set_led_state(LED_ID_ARMED, globalConfig.armed)

        # Debugging tools
        self.__create_debugging_tools()


    def __create_debugging_tools(self):
        # Vin slider frame
        self.slider_frame = Frame(self, bg="lightgray")
        # self.slider_frame.grid(row=1, column=0, columnspan=8, pady=10)
        self.slider_frame.grid(row=1, column=0, pady=10)

        Label(self.slider_frame, text="Vin", bg="lightgray", font=("Arial", 10)).pack(side="left", padx=5)

        self.vin_slider = tk.Scale(self.slider_frame,
                                from_=100,
                                to=110,
                                orient=tk.HORIZONTAL,
                                variable=self.vin,
                                length=200,
                                resolution=1,
                                bg="lightgray")
        self.vin_slider.pack(side="left")

        # Combobox for sensor triggering
        self.combobox_frame = tk.Frame(self, bg="lightgray")
        self.combobox_frame.grid(row=1, column=4, pady=10)

        self.combobox = ttk.Combobox(self.combobox_frame,
                                     values=[str(i) for i in range(16)],
                                     state="readonly")
        self.combobox.pack(side=tk.LEFT, padx=(0, 5))
        self.combobox.current(0)  # Select default value

        boton = tk.Button(self.combobox_frame,
                          text="Trigger",
                          command=self.__trigger_sensor)
        boton.pack(side=tk.LEFT)


    def __create_led(self, parent, text, color, col):
        """Crea un LED circular con texto debajo, con el doble de tamaño"""
        frame = Frame(parent, bg="lightgray")
        frame.grid(row=0, column=col, padx=10, pady=5)

        # Crear canvas
        canvas = Canvas(frame, width=60, height=60, bg="lightgray", highlightthickness=0)
        canvas.create_oval(10, 10, 50, 50, fill=color, outline="black")
        canvas.pack()

        # Agregar el texto debajo del LED
        label = Label(frame, text=text, font=("Arial", 10), bg="lightgray")
        label.pack()

        # Agregar el LED al diccionario
        self.leds[col] = canvas


    # Función para manejar la entrada del teclado
    def __on_button_press(self, value):
        if value == ESC:
            self.__clear_screen()
        elif value == ENTER:
            self.command_controller.process(self.screen_content)
            self.__clear_screen()
        elif value == PANIC:
            # plays alarm and contacts security central
            self.speaker.start(ALARM_TONE)
            self.emergency_monitor.dump_event(globalConfig.user_identifier,
                                              EVENT_PANIC)
            return
        elif value == FIREMAN:
            # plays alarm and contacts security central
            self.speaker.start(ALARM_TONE)
            self.emergency_monitor.dump_event(globalConfig.user_identifier,
                                              EVENT_FIREMAN)
            return
        elif len(self.screen_content) < 13:  # Limita el número de caracteres
            self.screen_content += value
            self.screen_text.config(text=self.screen_content)


    # Función para limpiar la pantalla LCD
    def __clear_screen(self):
        self.screen_content = ""
        self.screen_text.config(text=self.screen_content)


    def __trigger_sensor(self):
        sensor_id = int(self.combobox.get())
        print(f"Generating event on sensor {sensor_id}")
        self.sensorTrigger.simulate_event(sensor_id)


    def set_command_controller(self, command_controller):
        self.command_controller = command_controller


    def set_led_state(self, led_id, enable):
        if led_id not in self.leds:
            print(f"Error, led_id {led_id} desconocido")
            return

        canvas = self.leds[led_id]
        if enable:
            canvas.itemconfig(canvas.find_all(), fill="green")  # Cambiar a color verde cuando se activa
        else:
            canvas.itemconfig(canvas.find_all(), fill="orange")  # Cambiar a color rojo cuando se desactiva


    def set_indicator_state(self, indicator_id, enable):
        if indicator_id < 0 or indicator_id >= len(self.indicators):
            print(f"Error, indicator_id {indicator_id} desconocido")
            return
        
        enable_color = "green"
        if indicator_id in [2, 3]:
            enable_color = "red"

        label = self.indicators[indicator_id]
        if enable:
            label.config(fg=enable_color)  # Cambiar a color cuando se activa
        else:
            label.config(fg="gray")  # Cambiar a color gris cuando se desactiva

        return

# Two tone alarm
# tone 0 -> 500 Hz
# tone 1 -> 1200 Hz

class Speaker:
    def __init__(self):
        """Inicializa la clase con los parámetros del tono."""
        self.playing = False
        self.thread = None
        self.lock = threading.Lock()
        self.play_tone0 = True
        self.play_tone1 = True

    def _generate_tone(self, frequency, duration, samplerate):
        t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
        return 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitud reducida para evitar distorsión

    def _play_tone_loop(self):
        samplerate = 44100
        tone0 = self._generate_tone(500, 0.5, samplerate)
        tone1 = self._generate_tone(1200, 0.5, samplerate)
        while self.playing:
            if self.play_tone0:
                sd.play(tone0, samplerate=samplerate)
                sd.wait()  # Espera a que termine de reproducirse
            
            if self.play_tone1:
                sd.play(tone1, samplerate=samplerate)
                sd.wait()

    def start(self, tone):
        with self.lock:
            if tone == ALARM_TONE:
                self.play_tone0 = True
                self.play_tone1 = True
            elif tone == SINGLE_TONE0:
                self.play_tone0 = True
                self.play_tone1 = False
            elif tone == SINGLE_TONE1:
                self.play_tone0 = False
                self.play_tone1 = True

            if not self.playing:
                self.playing = True
                self.thread = threading.Thread(target=self._play_tone_loop, daemon=True)
                self.thread.start()

    def stop(self):
        with self.lock:
            if not self.playing:
                return

            self.playing = False
            if self.thread:
                self.thread.join()
                self.thread = None
