import tkinter as tk
from tkinter import Label, Button, Frame, Canvas

# Button widths
W5, W10 = 5, 10

# Button text
ESC = "Esc"
ENTER = "Enter"
PANIC = "Pánico"
FIREMAN = "Bomberos"

class AlarmPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH-101 Alarm Panel")
        self.geometry("630x230")
        self.configure(bg='lightgray')

        # Variable para almacenar el texto en la pantalla LCD
        self.screen_content = ""

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
        self.modes_frame = Frame(self.lcd_frame, bg="white")
        self.modes_frame.pack(side="right", padx=20, pady=5)

        # Modos de operación dentro de la pantalla LCD
        self.modes = ["Modo 0", "Modo 1", "Batería", "Error"]
        for mode in self.modes:
            lbl = Label(self.modes_frame,
                        text=mode,
                        font=("Arial", 8),
                        bg="white",
                        fg="gray")
            lbl.pack(anchor="e")

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
        self.create_led(self.led_frame, "Batería", "orange", 0)
        self.create_led(self.led_frame, "Armada", "orange", 1)

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
                   command=lambda t=text: self.on_button_press(t)).grid(row=row, column=col, padx=5, pady=5)

    def create_led(self, parent, text, color, col):
        """Crea un LED circular con texto debajo, con el doble de tamaño"""
        frame = Frame(parent, bg="lightgray")
        frame.grid(row=0, column=col, padx=10, pady=5)

        # Crear el canvas más grande
        canvas = Canvas(frame, width=60, height=60, bg="lightgray", highlightthickness=0)
        canvas.create_oval(10, 10, 50, 50, fill=color, outline="black")  # Óvalo más grande
        canvas.pack()

        # Agregar el texto debajo del LED
        label = Label(frame, text=text, font=("Arial", 10), bg="lightgray")
        label.pack()

    # Función para manejar la entrada del teclado
    def on_button_press(self, value):
        if value == ESC:
          # hacer algo
          self.clear_screen()
        elif value == PANIC:
            # hacer algo
            return
        elif value == FIREMAN:
            # hacer algo
            return
        elif len(self.screen_content) < 13:  # Limita el número de caracteres
            self.screen_content += value
            self.screen_text.config(text=self.screen_content)
    
    # Función para limpiar la pantalla LCD
    def clear_screen(self):
        self.screen_content = ""
        self.screen_text.config(text=self.screen_content)


if __name__ == "__main__":
    app = AlarmPanel()
    app.mainloop()
