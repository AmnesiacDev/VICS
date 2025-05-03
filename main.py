import customtkinter as ctk
import tkinter.filedialog as fd
import os

# Placeholder for your ML prediction function
def predict_from_audio(file_path):
    # TODO: Replace this with actual MFCC + model pipeline
    if "1" in file_path:
        return "One"
    return "Unknown"

# Main app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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

app.mainloop()
