import tkinter as tk
from tkinter import Label, Button, Frame

class AlarmPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH-101 Alarm Panel")
        self.geometry("500x300")
        self.configure(bg='lightgray')

        # Variable para almacenar el texto en la pantalla LCD
        self.screen_content = ""

        # Contenedor de la pantalla LCD
        self.lcd_frame = Frame(self, bg="white", relief="sunken", bd=3, width=300, height=100)
        self.lcd_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky='w')
        self.lcd_frame.pack_propagate(False)  # Evita que el frame se reduzca al tamaño de su contenido

        # Texto principal en la pantalla LCD
        self.screen_text = Label(self.lcd_frame, text="0123", font=("Arial", 18, "bold"), bg="white", fg="black")
        self.screen_text.pack(side="left", padx=10, pady=10)

        # Frame para los modos de operación dentro de la pantalla LCD
        self.modes_frame = Frame(self.lcd_frame, bg="white")
        self.modes_frame.pack(side="right", padx=20, pady=5)  # Más espacio horizontal

        # Modos de operación (alineados a la derecha dentro del LCD)
        self.modes = ["Modo 0", "Modo 1", "Batería", "Error"]
        for mode in self.modes:
            lbl = Label(self.modes_frame, text=mode, font=("Arial", 8), bg="white", fg="gray")
            lbl.pack(anchor="e")


        # LED Indicators
        self.led_frame = Frame(self, bg='lightgray')
        self.led_frame.grid(row=1, column=0, columnspan=4, pady=5)

        self.led_battery = Label(self.led_frame, text="Batería", font=("Arial", 10), bg="orange", width=10)
        self.led_battery.pack(side='left', padx=5)

        self.led_armed = Label(self.led_frame, text="Armada", font=("Arial", 10), bg="orange", width=10)
        self.led_armed.pack(side='left', padx=5)

        # Keypad Buttons
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row=0, column=4, columnspan=4, padx=10, pady=10, sticky='w')

        # Button widths
        W5, W10 = 5, 10

        buttons = [
            ('1', 0, 0, W5), ('2', 0, 1, W5), ('3', 0, 2, W5), ('Esc',      0, 3, W10),
            ('4', 1, 0, W5), ('5', 1, 1, W5), ('6', 1, 2, W5), ('Enter',    1, 3, W10),
            ('7', 2, 0, W5), ('8', 2, 1, W5), ('9', 2, 2, W5), ('Pánico',   2, 3, W10),
            ('*', 3, 0, W5), ('0', 3, 1, W5), ('#', 3, 2, W5), ('Bomberos', 3, 3, W10),
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

    # Función para manejar la entrada del teclado
    def on_button_press(self, value):
        if len(self.screen_content) < 10:  # Limita el número de caracteres
            self.screen_content += value
            self.screen_text.config(text=self.screen_content)
    
    # Función para limpiar la pantalla LCD
    def clear_screen(self):
        self.screen_content = ""
        self.screen_text.config(text=self.screen_content)


if __name__ == "__main__":
    app = AlarmPanel()
    app.mainloop()
