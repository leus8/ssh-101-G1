import tkinter as tk
from tkinter import Label, Button, Frame

class AlarmPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH-101 Alarm Panel")
        self.geometry("500x300")
        self.configure(bg='lightgray')

        # Screen (LCD)
        self.screen = Label(self, text="", font=("Arial", 18), width=15, height=3, relief="sunken", bg="white")
        self.screen.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        # Modes
        self.modes = ["Modo 0", "Modo 1", "Batería", "Error"]
        self.mode_frame = Frame(self, bg='lightgray')
        self.mode_frame.grid(row=0, column=4, padx=10, pady=10, sticky='n')

        for mode in self.modes:
            lbl = Label(self.mode_frame, text=mode, font=("Arial", 10), bg="lightgray")
            lbl.pack(anchor='w')

        # LED Indicators
        self.led_frame = Frame(self, bg='lightgray')
        self.led_frame.grid(row=1, column=0, columnspan=4, pady=5)

        self.led_battery = Label(self.led_frame, text="Batería", font=("Arial", 10), bg="orange", width=10)
        self.led_battery.pack(side='left', padx=5)

        self.led_armed = Label(self.led_frame, text="Armada", font=("Arial", 10), bg="orange", width=10)
        self.led_armed.pack(side='left', padx=5)

        # Keypad Buttons
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('*', 3, 0), ('0', 3, 1), ('#', 3, 2)
        ]

        for (text, row, col) in buttons:
            Button(self.buttons_frame,
                   text=text,
                   width=5,
                   height=2,
                   command=lambda t=text: self.on_button_press(t)).grid(row=row, column=col, padx=5, pady=5)

        # Special Buttons
        self.special_frame = Frame(self)
        self.special_frame.grid(row=2, column=4, padx=10, pady=10, sticky='n')

        Button(self.special_frame, text="Esc", width=10, height=2).pack(pady=5)
        Button(self.special_frame, text="Enter", width=10, height=2).pack(pady=5)
        Button(self.special_frame, text="Pánico", width=10, height=2, bg="blue", fg="white").pack(pady=5)
        Button(self.special_frame, text="Bomberos", width=10, height=2, bg="blue", fg="white").pack(pady=5)

    # Función para manejar la entrada del teclado
    def on_button_press(self, value):
        current_text = self.screen["text"]
        self.screen["text"] = current_text + value


if __name__ == "__main__":
    app = AlarmPanel()
    app.mainloop()
