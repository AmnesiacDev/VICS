import customtkinter as ctk
from PIL import Image
import platform
from app import utils
from .SettingsMenu import SettingsMenu


class TitleBar(ctk.CTkFrame):
    def __init__(self, master, open_settings_callback):
        super().__init__(master)
        self.is_max = False
        self._x = self._y = None

        self.master = self.winfo_toplevel()
        self.pack(fill="x", side="top")

        self.title_bar = ctk.CTkFrame(self, height=30)
        self.title_bar.pack(fill="x", side="top")

        self.title_label = ctk.CTkLabel(self.title_bar, text="VICS", font=ctk.CTkFont(size=14))
        self.title_label.pack(side="left", padx=10)

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        self.close_image = Image.open(utils.close_icon)
        self.close_image = self.close_image.resize((10, 10))
        self.close_image = ctk.CTkImage(self.close_image, size=(10, 10))

        self.close_button = ctk.CTkButton(self.title_bar, text="", fg_color="transparent",
                                          image=self.close_image, width=30, command=self.winfo_toplevel().destroy)
        self.close_button.pack(side="right", padx=2)

        self.max_image = Image.open(utils.maximize_icon)
        self.max_image = self.max_image.resize((10, 10))
        self.min_image = Image.open(utils.minimize_icon)
        self.min_image = self.min_image.resize((10, 10))

        self.min_image = ctk.CTkImage(self.min_image, size=(10, 10))
        self.max_image = ctk.CTkImage(self.max_image, size=(10, 10))

        self.maxmin_button = ctk.CTkButton(self.title_bar, text="",
                                           image=self.max_image, width=30, fg_color="transparent", command=self.toggle_maximize)
        self.maxmin_button.pack(side="right", padx=2)

        self.settings_btn = ctk.CTkButton(self.title_bar, text="⚙", command=open_settings_callback, width=30, fg_color="transparent")
        self.settings_btn.pack(side="right", padx=2)



    def toggle_maximize(self):
        system = platform.system()

        def simulate_maximize():
            screen_width = self.winfo_toplevel().winfo_screenwidth()
            screen_height = self.winfo_toplevel().winfo_screenheight()
            self.winfo_toplevel().geometry(f"{screen_width}x{screen_height}+0+0")
            self.maxmin_button.configure(image=self.min_image)

        def simulate_minimize():
            self.winfo_toplevel().geometry(utils.DIMENSIONS)
            self.center_window(utils.WIDTH, utils.HEIGHT)
            self.maxmin_button.configure(image=self.max_image)


        if system == "Windows":
            if self.winfo_toplevel().state() == "zoomed":
                self.winfo_toplevel().state("normal")
            else:
                self.winfo_toplevel().state("zoomed")

        elif system == "Linux":
            if not self.is_max:
                simulate_maximize()
                self.is_max = True
            else:
                simulate_minimize()
                self.is_max = False

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.winfo_toplevel().geometry(f"{width}x{height}+{x}+{y}")



    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.master.winfo_pointerx() - self._x
        y = self.master.winfo_pointery() - self._y
        self.winfo_toplevel().geometry(f"+{x}+{y}")

