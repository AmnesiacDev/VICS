import os
import pickle
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import webbrowser
import datetime
import speech_recognition as sr
import os
from app.Machine.Model import VoiceCommandModel
audio_file = "temp.wav"
volume = 50

model = VoiceCommandModel(data_path=None)
model.load_model(r"C:\Users\habib\PycharmProjects\PATTERNNNN\model.pkl")
def get_volume():
    return volume

def change_volume(new_percent):
    global volume
    volume = max(0, min(100, new_percent))
    print(f"Volume set to {volume}%")


def classify_text_command(text):
    text = text.lower()
    command, confidence = model.predict_command(audio_file)
    print(f"Predicted command: {command} (Confidence: {confidence:.2f})")

    if any(kw in text for kw in ["louder", "increase volume", "volume up"]):
        return "increase_volume"
    elif any(kw in text for kw in ["quieter", "decrease volume", "volume down", "lower volume"]):
        return "decrease_volume"
    elif any(kw in text for kw in ["what's the time", "time now", "tell me the time", "current time"]):
        return "get_time"
    elif any(kw in text for kw in ["open spotify", "play music", "start music"]):
        return "play_music"
    elif any(kw in text for kw in ["open calendar", "my schedule"]):
        return "open_calender"
    elif any(kw in text for kw in ["weather", "forecast"]):
        return "get_weather"
    elif any(kw in text for kw in ["map", "directions", "location"]):
        return "open_google_maps"
    elif any(kw in text for kw in ["calculator", "calc"]):
        return "open_calculator"
    elif any(kw in text for kw in ["joke", "make me laugh"]):
        return "tell_joke"
    elif any(kw in text for kw in ["reminder", "note"]):
        return "set_reminder"
    elif any(kw in text for kw in ["timer", "countdown"]):
        return "set_timer"
    else:
        return "unknown"