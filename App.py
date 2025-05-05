import threading
import customtkinter as ctk
from PIL import Image
from pynput import mouse, keyboard


from app import TitleBar, RecordButton, SettingsMenu, utils

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VICS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self._y = None
        self._x = None
        self.withdrawn = False
        self.theme = False
        self.geometry(utils.DIMENSIONS)
        self.center_window(utils.WIDTH, utils.HEIGHT)

        self.settings = SettingsMenu(self)
        self.settings.place(x=self.winfo_width(), y=0, relheight=1)

        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(fill="x", side="top")
        self.custom_title_bar = TitleBar(self.temp_frame, open_settings_callback=self.settings.slide_in_settings)
        self.custom_title_bar.pack(fill="x", side="top")

        self.content_frame = ctk.CTkFrame(self, fg_color=utils.dark_theme)  # New frame just for screen assets
        self.content_frame.pack(fill="both", expand=True, side="left")

        self.resizable(True, True)  # Allow resizing in both dimensions

        self.light_sun_image = Image.open(utils.light_sun)
        self.light_sun_image = self.light_sun_image.resize((30, 30))
        self.light_sun_image = ctk.CTkImage(self.light_sun_image, size=(30,30))


        self.dark_sun_image = Image.open(utils.dark_sun)
        self.dark_sun_image = self.dark_sun_image.resize((30, 30))

        self.dark_sun_image = ctk.CTkImage(self.dark_sun_image, size=(30,30))

        def on_hover(event):
            if self._get_appearance_mode() == "dark":
                self.theme_switch.configure(fg_color=utils.dark_hover)
            else:
                self.theme_switch.configure(fg_color=utils.light_hover)

        def on_exit(event):
            self.theme_switch.configure(fg_color="transparent")

        self.theme_switch = ctk.CTkButton(self.content_frame, text="", command=self.toggle_theme, anchor="ne",
                                          image=self.light_sun_image, fg_color="transparent", hover=False, width=20)
        self.theme_switch.pack(side="top")

        self.theme_switch.bind("<Enter>", on_hover)
        self.theme_switch.bind("<Leave>", on_exit)

        self.rec_screen = RecordButton(self.content_frame)
        self.active_frame = self.show_instance(self.rec_screen)
        self.focus_in = True
        def on_click(x, y, button, pressed):

            x_coord_start = self.winfo_rootx()
            y_coord_start = self.winfo_rooty()
            x_coord_end = x_coord_start +utils.WIDTH
            y_coord_end = y_coord_start + utils.HEIGHT
            print(button)
            if pressed:
                if (x_coord_start < x < x_coord_end) and (y_coord_start < y < y_coord_end):
                    print("between")
                elif self.focus_in:
                    self.withdraw()
                    self.focus_in = False


        self.cmb = utils.keyboard_shortcut
        self.current = set()

        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        listener = mouse.Listener(on_click=on_click)
        listener.start()

    def get_settings(self):
        return self.settings
    def toggle_theme(self):
        if self.theme:
            self.theme = False
            ctk.set_appearance_mode("dark")
            self.content_frame.configure(fg_color=utils.dark_theme)
            self.theme_switch.configure(image=self.light_sun_image, fg_color=utils.dark_hover)
            self.custom_title_bar.configure(fg_color=utils.dark_theme)
        else:
            self.theme = True
            ctk.set_appearance_mode("light")
            self.content_frame.configure(fg_color=utils.light_theme)
            self.theme_switch.configure(image=self.dark_sun_image, fg_color=utils.light_hover)
            self.custom_title_bar.configure(fg_color=utils.light_theme)

    def show_instance(self, frame_to_show):
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.pack_forget()
        frame_to_show.pack(fill="both", expand=True)
        return frame_to_show

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_press(self, key):
        if any([key in z for z in self.cmb]):
            self.current.add(key)
            if any(all(k in self.current for k in z) for z in self.cmb):
                self.show_app()

    def on_release(self, key):
        if any([key in z for z in self.cmb]):
            self.current.remove(key)

    def keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def show_app(self):
        if not self.focus_in:
            self.deiconify()







# Placeholder for your ML prediction function
def predict_from_audio(file_path):
    if "1" in file_path:
        return "One"
    return "Unknown"

# Main app

"""""
app = ctk.CTk()
app.title("Voice Recognition")
app.geometry("400x250")

selected_file_path = ctk.StringVar()
prediction_result = ctk.StringVar(value="Prediction: None")

def load_audio():
    file_path = fd.askopenfilename(
        title="Select Audio File",
        filetypes=[("WAV files", "*.wav")]
    )
    if file_path:
        selected_file_path.set(file_path)
        prediction_result.set("Prediction: Ready to run")

def run_prediction():
    path = selected_file_path.get()
    if not os.path.exists(path):
        prediction_result.set("Error: No file selected")
        return
    result = predict_from_audio(path)
    prediction_result.set(f"Prediction: {result}")

# Widgets
title = ctk.CTkLabel(app, text="Voice Recognition App", font=ctk.CTkFont(size=18, weight="bold"))
title.pack(pady=10)

load_btn = ctk.CTkButton(app, text="Load Audio File", command=load_audio)
load_btn.pack(pady=10)

predict_btn = ctk.CTkButton(app, text="Run Prediction", command=run_prediction)
predict_btn.pack(pady=10)

result_label = ctk.CTkLabel(app, textvariable=prediction_result, font=ctk.CTkFont(size=14))
result_label.pack(pady=20)
"""""

if __name__ == "__main__":
    app = VICS()
    app.mainloop()
