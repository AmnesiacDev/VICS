import speech_recognition as sr


def transcribe_audio(audio, sample_rate):
    recognizer = sr.Recognizer()

    if audio.ndim > 1:
        audio = audio.mean(axis=1).astype(audio.dtype)
    try:
        audio_data = sr.AudioData(audio.tobytes(), sample_rate, 2)
        text = recognizer.recognize_google(audio_data)
        print(" Transcribed Text:", text)
        return text
    except sr.UnknownValueError:
        print(" Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(" Recognition error:", e)
        return None
