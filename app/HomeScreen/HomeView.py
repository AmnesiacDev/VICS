import customtkinter as ctk
from app.HomeScreen import ThemeSwitchButton, RecordButton
from .TextBlock import TextBlock

class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.recorded_data = None
        self.text_box = TextBlock(master)
        self.theme_switch = ThemeSwitchButton.ThemeSwitch(master, self.text_box)
        self.rec_screen = RecordButton(master, self.text_box)
