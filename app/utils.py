from pynput import keyboard

DIMENSIONS = "400x300"
WIDTH = 400
HEIGHT = 300
TITLE = "VICS"
FILENAME = "assets/recorded.wav"
DURATION = 300
SAMPLE_RATE = 16000
FREQUENCY = 44100

keyboard_shortcut = [{keyboard.Key.shift, keyboard.Key.f1}]

close_icon = "assets/title_bar/close.png"
maximize_icon = "assets/title_bar/stop.png"
minimize_icon = "assets/title_bar/diamond.png"
white_circle = "assets/home_screen/circle_white.png"

light_sun = "assets/settings_screen/light.png"
dark_sun = "assets/settings_screen/dark.png"

idle_color = "#8a8584"
active_color = "#de2c1f"
hover_color = "#2c198c"
dark_theme = "#2B2B2B"
light_theme = "#f0f0f0"
blood_red = "#880808"

dark_hover = "#1c1c1c"
light_hover = "#aba7a7"


def center_window(self, width, height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    self.geometry(f"{width}x{height}+{x}+{y}")

