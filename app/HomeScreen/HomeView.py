import customtkinter as ctk
from app import utils
from app.HomeScreen import ThemeSwitchButton, RecordButton

class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.theme_switch = ThemeSwitchButton.ThemeSwitch(master)
        self.rec_screen = RecordButton(master)
