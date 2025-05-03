import customtkinter as ctk
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import os
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DIMENSIONS = "400x300"
WIDTH = 400
HEIGHT = 300
TITLE = "VICS"
FILENAME = "recorded.wav"
DURATION = 4  # seconds
SAMPLE_RATE = 16000


class VICS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self._y = None
        self._x = None
        self.geometry(DIMENSIONS)
        self.center_window(WIDTH, HEIGHT)

        self.custom_title_bar = TitleBar(self)
        self.custom_title_bar.pack(fill="x", side="top")

        self.resizable(True, True)  # Allow resizing in both dimensions

        self.switch = ctk.CTkSwitch(
            self, text="Dark Mode", command=self.toggle_theme
        )
        self.switch.select()
        self.switch.pack()

        self.content_frame = ctk.CTkFrame(self)  # New frame just for screen content
        self.content_frame.pack(fill="both", expand=True)


        self.rec_screen = RecordScreen(self.content_frame)
        self.show_instance(self.rec_screen)

    def toggle_theme(self):
        if self.switch.get():
            ctk.set_appearance_mode("dark")
            self.switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("light")
            self.switch.configure(text="Light Mode")

    def show_instance(self, frame_to_show):
        # Hide all instances
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.pack_forget()
        frame_to_show.pack(fill="both", expand=True)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")



class TitleBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._y = None
        self._x = None
        self.master = self.winfo_toplevel()
        self.pack(fill="x", side="top")

        self.title_bar = ctk.CTkFrame(self, height=30, fg_color="#222222")
        self.title_bar.pack(fill="x", side="top")

        self.title_label = ctk.CTkLabel(self.title_bar, text="VICS", font=ctk.CTkFont(size=14))
        self.title_label.pack(side="left", padx=10)

        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=30, command=self.winfo_toplevel().destroy)
        self.close_button.pack(side="right", padx=5)

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.master.winfo_pointerx() - self._x
        y = self.master.winfo_pointery() - self._y
        self.winfo_toplevel().geometry(f"+{x}+{y}")




class RecordScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.recording = None

        record_btn_x = 130
        record_btn_y = 50
        self.idle_color = "#8a8584"
        self.active_color = "#de2c1f"
        self.hover_color = "#2c198c"
        self.record_btn = ctk.CTkButton(
            self,
            text="",
            hover=False,
            corner_radius=60,
            fg_color=self.idle_color,
            #font=ctk.CTkFont(size=18),
            width=120,
            height=120,
        )
        self.record_btn.place(x=record_btn_x, y=record_btn_y)


        self.white_circle_image = Image.open("content/circle_white.png")
        self.white_circle_image = self.white_circle_image.resize((100, 100))

        self.ctk_image = ctk.CTkImage(self.white_circle_image,size=(80, 80))

        self.white_circle_label = ctk.CTkLabel(self,fg_color=self.idle_color, bg_color="transparent", image=self.ctk_image, text="")
        self.white_circle_label.place(x=record_btn_x+20, y=record_btn_y+20)

        def on_hover(event):
            if self.recording:
                return
            self.white_circle_label.configure(fg_color=self.hover_color)
            self.record_btn.configure(fg_color=self.hover_color)

        def on_exit(event):
            if self.recording:
                return
            self.white_circle_label.configure(fg_color=self.idle_color)
            self.record_btn.configure(fg_color=self.idle_color)


        self.white_circle_label.bind("<Enter>", on_hover)
        self.white_circle_label.bind("<Leave>", on_exit)
        self.white_circle_label.bind("<Button-1>", self.start_recording)


        self.record_btn.bind("<Enter>", on_hover)
        self.record_btn.bind("<Leave>", on_exit)
        self.record_btn.bind("<Button-1>", self.start_recording)








    def start_recording(self, event):
        if self.recording:
            return

        self.recording = True

        self.record_btn.configure(fg_color=self.active_color)
        self.white_circle_label.configure(fg_color=self.active_color)

        self.smooth_color_transition(self.record_btn, self.idle_color, self.active_color)
        self.smooth_color_transition(self.white_circle_label, self.idle_color, self.active_color)


        thread = threading.Thread(target=self.record_audio)
        thread.start()

    def record_audio(self):
        # Record and save audio
        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        write(FILENAME, SAMPLE_RATE, audio)

        # Reset button UI
        self.record_btn.configure(fg_color=self.idle_color)
        self.white_circle_label.configure(fg_color=self.idle_color)
        self.recording = False

    def smooth_color_transition(self, widget, start_color, end_color, steps=20, delay=50):
        """Smoothly transition the color of the widget from start_color to end_color."""
        # Extract RGB components of the colors
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        # Calculate the step sizes for each color component (R, G, B)
        r_step = (end_rgb[0] - start_rgb[0]) / steps
        g_step = (end_rgb[1] - start_rgb[1]) / steps
        b_step = (end_rgb[2] - start_rgb[2]) / steps

        # Define a method to update the color step by step
        def update_color(step):
            r = int(start_rgb[0] + r_step * step)
            g = int(start_rgb[1] + g_step * step)
            b = int(start_rgb[2] + b_step * step)
            new_color = self.rgb_to_hex(r, g, b)
            widget.configure(fg_color=new_color)

            # Continue updating until we reach the final color
            if step < steps:
                self.after(delay, update_color, step + 1)

        # Start the color transition
        update_color(0)

    def hex_to_rgb(self, hex_color):
        """Convert a hex color to RGB."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex color."""
        return f"#{r:02x}{g:02x}{b:02x}"








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
