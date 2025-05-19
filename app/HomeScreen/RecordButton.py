import threading
import customtkinter as ctk
import numpy as np
import sounddevice as sd
from PIL import Image
from app import utils
import app.Machine.Transcribe as tr
import queue

class RecordButton(ctk.CTkFrame):
    def __init__(self, master, text_box, **kwargs):
        super().__init__(master, **kwargs)
        self.recorded_frames = None
        self.started_recording = None
        self.stop_flag = None
        print("in record")
        self.recording = None
        self.text_box = text_box

        record_btn_x = 140
        record_btn_y = 80


        self.record_btn = ctk.CTkButton(self.master, text="", hover=False, corner_radius=60,
                                        fg_color=utils.idle_color, width=120, height=120)
        self.record_btn.place(x=record_btn_x, y=record_btn_y)


        self.white_circle_image = Image.open(utils.white_circle)
        self.white_circle_image = self.white_circle_image.resize((100, 100))

        self.ctk_image = ctk.CTkImage(self.white_circle_image,size=(80, 80))

        self.white_circle_label = ctk.CTkLabel(self.master, fg_color=utils.idle_color, bg_color="transparent",
                                               image=self.ctk_image, text="")
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

            audio_data = np.concatenate(self.recorded_frames, axis=0)
            self.temp_callback(audio_data)

        if self.recording:
            self.text_box.new_text("Transcribing....")
            self.stop_flag.set()
            self.started_recording.join()

            self.smooth_color_transition(self.record_btn, utils.active_color, utils.idle_color)
            self.smooth_color_transition(self.white_circle_label, utils.active_color, utils.idle_color)
            self.after(450, stop_recording)


    def start_recording(self, event):
        if self.recording:
            self.stop_recording()
        else:
            self.recording = True

            self.text_box.new_text("recording...")
            self.record_btn.configure(fg_color=utils.active_color)
            self.white_circle_label.configure(fg_color=utils.active_color)

            self.smooth_color_transition(self.record_btn, utils.hover_color, utils.active_color)
            self.smooth_color_transition(self.white_circle_label, utils.hover_color, utils.active_color)

            self.stop_flag = threading.Event()
            self.started_recording = threading.Thread(target=self.record_audio)
            self.started_recording.start()


    def record_audio(self):

        print("starting new stream")
        self.recorded_frames = []
        audio_queue = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_queue.put(indata.copy())

        with sd.InputStream(samplerate=utils.FREQUENCY, channels=2,dtype='int16',callback=callback):

            while not self.stop_flag.is_set():
                try:
                    data = audio_queue.get(timeout=0.1)
                    self.recorded_frames.append(data)
                except queue.Empty:
                    continue



    def temp_callback(self, audio):
        self.text_box.new_text(tr.transcribe_audio(audio, utils.FREQUENCY))



    def process_command(self, command):
        # Just print the recognized text as a string
        print(f"Recognized command: '{command}'")

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



