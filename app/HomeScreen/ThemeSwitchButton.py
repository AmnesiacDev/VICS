import customtkinter as ctk
from PIL import Image
from app import utils


class ThemeSwitch(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.theme = False

        self.light_sun_image = Image.open(utils.light_sun)
        self.light_sun_image = self.light_sun_image.resize((30, 30))
        self.light_sun_image = ctk.CTkImage(self.light_sun_image, size=(30, 30))

        self.dark_sun_image = Image.open(utils.dark_sun)
        self.dark_sun_image = self.dark_sun_image.resize((30, 30))
        self.dark_sun_image = ctk.CTkImage(self.dark_sun_image, size=(30, 30))

        def on_hover(event):
            if self._get_appearance_mode() == "dark":
                self.theme_switch.configure(fg_color=utils.dark_hover)
            else:
                self.theme_switch.configure(fg_color=utils.light_hover)

        def on_exit(event):
            self.theme_switch.configure(fg_color="transparent")

        self.theme_switch = ctk.CTkButton(self.master, text="", command=self.toggle_theme, anchor="ne",
                                          image=self.light_sun_image, fg_color="transparent", hover=False, width=20)
        self.theme_switch.place(x=300, y=30)

        self.theme_switch.bind("<Enter>", on_hover)
        self.theme_switch.bind("<Leave>", on_exit)



    def toggle_theme(self):
        if self.theme:
            self.theme = False
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(image=self.light_sun_image, fg_color=utils.dark_hover)
        else:
            self.theme = True
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(image=self.dark_sun_image, fg_color=utils.light_hover)
