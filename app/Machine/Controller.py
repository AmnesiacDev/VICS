import os
import platform
import requests
import datetime
import app.Machine.Windows as Windows
import app.Machine.Linux as Linux
import webbrowser
import wikipedia
import random
from app import utils

class Command:
    def __init__(self, query):
        self.transcriber=query
        if platform.system() == "Windows":
            self.controller = Windows.Commands()

        self.command_list = {
            "open_google_maps": self.open_google_maps,
            "increase_volume": self.increase_volume,
            "decrease_volume": self.decrease_volume,
            "get_weather": self.get_weather,
            "get_time": self.get_time,
            "open_calculator": self.open_calculator,
            "open_calender": self.open_calender,
            "play_music": self.play_music,
            "tell_joke": self.tell_joke,
            "set_timer": self.set_timer,
            "unknown": self.unknown
        }

    def run(self, command, transcribed_text=None):
        func = self.command_list.get(command.lower())

        if func:
            result = func()
            if result:
                print(result)
        else:
            print(f"Unknown command: {command}")

            if transcribed_text:
                query = transcribed_text.strip()
                if query:
                    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    try:
                        webbrowser.open(url)  # Opens in default browser
                        print(f"Searching Google for: {query}")
                    except Exception as e:
                        print(f"Failed to open browser: {e}")
                else:
                    print("No transcribed text to search.")
            else:
                print("No transcribed text provided.")


    def increase_volume(self, step=20):
        percent = self.controller.get_volume() + step
        if percent > 100:
            percent = 100
        self.controller.change_volume(percent)
        return "boop"

    def unknown(self):
        if self.transcriber:
            query = self.transcriber
        else:
            query = input("Couldn't transcribe. Type what to search: ")

        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        try:
            webbrowser.open(url)  # This opens the URL in the default browser
        except Exception as e:
            print(f"Failed to open browser: {e}")

    def decrease_volume(self, step=20):
        percent = self.controller.get_volume() - step
        if percent < 0:
            percent = 0
        self.controller.change_volume(percent)

    def get_weather(self, city="cairo", api_key=None):
        try:
            os.system("start bingweather:")
            return "Opening Weather app..."
        except Exception as e:
            return f"Failed to open Weather app: {e}"

    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def open_calculator(self):
        print(" Opening Calculator...")
        os.system("start calc")

    def open_calender(self):
        print("Opening Calendar...")
        os.system("start outlookcal:")  # Opens the default calendar app (usually Windows Calendar or Outlook)

    def play_music(self):
        try:
            os.system("start spotify")
        except:
            webbrowser.open("https://www.spotify.com/")

    import webbrowser

    def open_google_maps(self):
        print(" Opening Maps app...")
        os.system("start bingmaps:")


    def tell_story(self):
        print("story")

    def tell_joke(self):
        jokeapi = ("https://v2.jokeapi.dev/joke/any", "setup", "delivery")
        official_joke = ("https://official-joke-api.appspot.com/random_joke", "setup", "punchline")
        choice = random.choice([jokeapi, official_joke])
        response = requests.get(choice[0])
        if response.status_code == 200:
            joke = response.json()
            print(f"{joke[choice[1]]} - {joke[choice[2]]}")

    def set_timer(self):
        print(" Opening Clock app... please set your timer manually.")
        try:
            os.system("start ms-clock:")
        except Exception as e:
            print(f"Failed to open Clock app: {e}")