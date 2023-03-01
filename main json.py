import json
import tkinter as tk
import pynput
import pygame

class KeyboardApp:

    def __init__(self, master=None, button_layout='button_layout.json', button_width=None, ratio=None):
        self.master = master
        self.button_layout_path = button_layout
        self.button_width = button_width
        self.ratio = ratio
        self.pressed_keys = set()

        master.title("Keyboard App")
        master.geometry("480x145")

        self.load_button_layout()
        self.create_buttons(self.master, self.button_width, self.ratio)

        master.bind("<Key>", self.key_pressed)
        master.bind("<KeyRelease>", self.key_released)

        self.listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        master.protocol("WM_DELETE_WINDOW", self.save_window_size)

    def load_button_layout(self):
        with open('button_layout.json') as f:
            layout_data = json.load(f)

        button_layout = {}
        button_positions = {}
        for k, v in layout_data.items():
            if isinstance(v, dict):
                button_positions[k] = v.values()
            else:
                button_layout[k] = v

        self.button_layout = button_layout
        self.button_positions = button_positions
        self.window_size = layout_data.get('window_size', (480, 145))

    def create_buttons(screen, button_width, ratio, button_layout_path='button_layout.json'):
        with open(button_layout_path) as f:
            button_layout = json.load(f)

        buttons = []
        for button in button_layout:
            pos = button['position']
            x, y, w, h = pos['x'], pos['y'], pos['length'], pos['height']
            x, y, w, h = int(x * button_width), int(y * button_width / ratio), int(w * button_width), int(h * button_width / ratio)
            color = button['color']
            label = button['label']
            font_size = button['font_size']
            font = pygame.font.Font(None, font_size)
            buttons.append(Button(screen, (x, y, w, h), color, label, font))

        return buttons

    def trigger_effect(self, key, state):
        if state:
            print(f'{key} pressed')
            # trigger effect for key press
        else:
            print(f'{key} released')
            # trigger effect for key release

    def key_pressed(self, event):
        key = event.char
        if key in self.button_layout:
            self.pressed_keys.add(key)
            if len(self.pressed_keys) == 1:
                self.master.after(10, self.trigger_effect, key, True)

        if key == '<':
            self.listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()

    def key_released(self, event):
        key = event.char
        if key in self.button_layout:
            self.pressed_keys.discard(key)
            if not self.pressed_keys:
                self.trigger_effect(key, False)

    def on_press(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        if key_char in self.button_layout:
            self.pressed_keys.add(key_char)
            if len(self.pressed_keys) == 1:
                self.trigger_effect(key_char, True)

    def on_release(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        if key_char in self.button_layout:
            self.pressed_keys.discard(key_char)
            if not self.pressed_keys:
                self.trigger_effect(key_char, False)

    def save_window_size(self):
        size = (self.master.winfo_width(), self.master.winfo_height())
        with open('button_layout.json', 'w') as f:
            json.dump({'buttons': self.button_layout, 'positions': self.button_positions, 'window_size': size}, f)

if __name__ == '__main__':
    root = tk.Tk()
    app = KeyboardApp(root)
    app.master.geometry(f"{app.window_size[0]}x{app.window_size[1]}")
    root.mainloop()