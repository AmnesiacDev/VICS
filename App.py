import threading
import customtkinter as ctk
from PIL import Image
from pynput import mouse, keyboard
from app import TitleBar, HomeView, SettingsMenu, utils

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
        utils.center_window(self, utils.WIDTH, utils.HEIGHT)
        self.resizable(True, True)

        #self.settings = SettingsMenu(self)
        #self.settings.place(x=self.winfo_width(), y=0, relheight=1)

        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(fill="x", side="top")

        self.custom_title_bar = TitleBar(self.temp_frame)
        self.custom_title_bar.pack(fill="x", side="top")


        self.content_frame = ctk.CTkFrame(self)  # New frame just for screen assets
        self.content_frame.pack(fill="both", expand=True, side="left")

        self.home_screen = HomeView(self.content_frame)
        self.home_screen.pack(fill="x", side="top")


        self.active_frame = self.show_instance(self.content_frame)
        self.focus_in = True

        self.cmb = utils.keyboard_shortcut
        self.current = set()

        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        mouse.Listener(on_click=self.mouse_listener).start()


    def show_instance(self, frame_to_show):
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.pack_forget()
        frame_to_show.pack(fill="both", expand=True)
        return frame_to_show

    def keyboard_listener(self):

        def show_app():
            if not self.focus_in:
                self.deiconify()
                self.focus_in = True
        def on_press(key):


            if any([key in z for z in self.cmb]):
                self.current.add(key)
                if any(all(k in self.current for k in z) for z in self.cmb):
                    show_app()

        def on_release(key):
            if any([key in z for z in self.cmb]):
                self.current.remove(key)


        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def mouse_listener(self, x, y, button, pressed):
        x_coord_start = self.winfo_rootx()
        y_coord_start = self.winfo_rooty()
        x_coord_end = x_coord_start + utils.WIDTH
        y_coord_end = y_coord_start + utils.HEIGHT
        if pressed:
            if (x_coord_start < x < x_coord_end) and (y_coord_start < y < y_coord_end):
                pass
            elif self.focus_in:
                self.withdraw()
                self.focus_in = False








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
