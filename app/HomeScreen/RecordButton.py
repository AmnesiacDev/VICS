import threading
import customtkinter as ctk
import sounddevice as sd
from PIL import Image
from app import utils

class RecordButton(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        print("in record")
        self.recording = None

        record_btn_x = 140
        record_btn_y = 80


        self.record_btn = ctk.CTkButton(
            self.master,
            text="",
            hover=False,
            corner_radius=60,
            fg_color=utils.idle_color,
            #font=ctk.CTkFont(size=18),
            width=120,
            height=120,
        )
        self.record_btn.place(x=record_btn_x, y=record_btn_y)



        self.white_circle_image = Image.open(utils.white_circle)
        self.white_circle_image = self.white_circle_image.resize((100, 100))

        self.ctk_image = ctk.CTkImage(self.white_circle_image,size=(80, 80))

        self.white_circle_label = ctk.CTkLabel(self.master, fg_color=utils.idle_color, bg_color="transparent", image=self.ctk_image, text="")
        self.white_circle_label.place(x=record_btn_x+20, y=record_btn_y+20)



        def on_hover(event):
            if self.recording:
                self.white_circle_label.configure(fg_color=utils.blood_red)
                self.record_btn.configure(fg_color=utils.blood_red)
            else:
                self.white_circle_label.configure(fg_color=utils.hover_color)
                self.record_btn.configure(fg_color=utils.hover_color)

        def on_exit(event):
            if self.recording:
                self.white_circle_label.configure(fg_color=utils.active_color)
                self.record_btn.configure(fg_color=utils.active_color)
            else:
                self.white_circle_label.configure(fg_color=utils.idle_color)
                self.record_btn.configure(fg_color=utils.idle_color)


        self.white_circle_label.bind("<Enter>", on_hover)
        self.white_circle_label.bind("<Leave>", on_exit)
        self.white_circle_label.bind("<Button-1>", self.start_recording)


        self.record_btn.bind("<Enter>", on_hover)
        self.record_btn.bind("<Leave>", on_exit)
        self.record_btn.bind("<Button-1>", self.start_recording)

    def stop_recording(self):
        def stop_recording():
            self.recording = False
            print("ended")
        if self.recording:
            self.smooth_color_transition(self.record_btn, utils.active_color, utils.idle_color)
            self.smooth_color_transition(self.white_circle_label, utils.active_color, utils.idle_color)
            self.after(100, stop_recording)

    def start_recording(self, event):
        if self.recording:
            self.stop_recording()
        else:
            self.recording = True

            self.record_btn.configure(fg_color=utils.active_color)
            self.white_circle_label.configure(fg_color=utils.active_color)

            self.smooth_color_transition(self.record_btn, utils.hover_color, utils.active_color)
            self.smooth_color_transition(self.white_circle_label, utils.hover_color, utils.active_color)

            threading.Thread(target=self.record_audio).start()



    def record_audio(self):

        while self.recording:
            print("starting new stream")
            audio = sd.rec(
                int(utils.DURATION * utils.FREQUENCY),
                samplerate=utils.FREQUENCY,
                channels=2,
                dtype='int16'
            )
            sd.wait()
            self.temp_callback(audio)


    def temp_callback(self, audio):
        print("inside")
        # MAIN CALLBACK FOR TEXT: this function here
        # will call and give the recorded audio sample to the machine learning model for translation
        # look at utils.DURATION for the duration of each interval





    def smooth_color_transition(self, widget, start_color, end_color, steps=20, delay=20):
        """Smoothly transition the color of the widget from start_color to end_color."""
        # Extract RGB components of the colors
        def hex_to_rgb(hex_color):
            """Convert a hex color to RGB."""
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        def rgb_to_hex(r, g, b):
            """Convert RGB values to hex color."""
            return f"#{r:02x}{g:02x}{b:02x}"


        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)

        # Calculate the step sizes for each color component (R, G, B)
        r_step = (end_rgb[0] - start_rgb[0]) / steps
        g_step = (end_rgb[1] - start_rgb[1]) / steps
        b_step = (end_rgb[2] - start_rgb[2]) / steps

        # Define a method to update the color step by step
        def update_color(step):
            r = int(start_rgb[0] + r_step * step)
            g = int(start_rgb[1] + g_step * step)
            b = int(start_rgb[2] + b_step * step)
            new_color = rgb_to_hex(r, g, b)
            widget.configure(fg_color=new_color)

            # Continue updating until we reach the final color
            if step < steps:
                self.after(delay, update_color, step + 1)

        # Start the color transition
        update_color(0)



