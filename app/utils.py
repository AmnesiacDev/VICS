from matplotlib import font_manager
from pynput import keyboard
import ctypes
import os
import shutil
import subprocess

DIMENSIONS = "400x300"
WIDTH = 400
HEIGHT = 500
TITLE = "VICS"
FILENAME = "assets/recorded.wav"
DURATION = 5
SAMPLE_RATE = 44100
FREQUENCY = 44100
PLACEHOLDER = "I am a placeholder..."

melon_font_path = "assets/font/melon_camp/Melon Camp.otf"
font_name = "Melon Camp"

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

WEATHER = "92617575565c4fb6b2434710252005"






def center_window(self, width, height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    self.geometry(f"{width}x{height}+{x}+{y}")


def windows_install_font(font_path):
    if not is_font_installed():
        FR_PRIVATE = 0x10
        if os.path.exists(font_path):
            result = ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)  # Broadcast font change
            return result > 0
        return False
    else:
        print("font already exists")


def linux_user_install_font(font_path):
    if not is_font_installed():
        font_dir = os.path.expanduser("~/.local/share/fonts/")
        os.makedirs(font_dir, exist_ok=True)
        dest_path = os.path.join(font_dir, font_name)
        shutil.copy(font_path, dest_path)
        subprocess.run(["fc-cache", "-f", "-v"], check=True)
        return dest_path
    else:
        print("font already exists")


def is_font_installed():
    try:
        for font in font_manager.findSystemFonts(fontpaths=None, fontext="otf"):
            prop = font_manager.FontProperties(fname=font)
            if prop.get_name().lower() == font_name.lower():
                return True
    except RuntimeError:
        pass

    return False