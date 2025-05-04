import customtkinter as ctk
from app import utils

class SettingsMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.overlay = ctk.CTkFrame(self.winfo_toplevel(), fg_color="#000000", corner_radius=0)
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lower()  # Keep it under other widgets when hidden

        self.settings_frame = ctk.CTkFrame(self, width=300, height=self.winfo_toplevel().winfo_height(), fg_color=utils.light_theme)
        self.settings_frame.place(x=utils.WIDTH, y=50)


    def slide_in_settings(self):
        print("Sliding in settings...")
        #self.overlay.lift()
        self.overlay.bind("<Button-1>", lambda e: self.slide_out_settings())

        self.settings_frame.lift()

        start_x = self.winfo_toplevel().winfo_width()
        target_x = start_x - 300

        def animate(x):
            if x > target_x:
                self.settings_frame.place(x=x, y=0)
                self.after(5, lambda: animate(x - 20))
            else:
                self.settings_frame.place(x=target_x, y=0)

        animate(start_x)

    def slide_out_settings(self):
        print("Sliding out settings...")
        def animate(x):
            if x < self.winfo_toplevel().winfo_width():
                self.settings_frame.place(x=x, y=0)
                self.after(5, lambda: animate(x + 20))
            else:
                self.overlay.lower()

        animate(self.settings_frame.winfo_x())