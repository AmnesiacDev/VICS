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
        if platform.system() == "Linux":
            self.controller = Linux.Commands()
        elif platform.system() == "Windows":
            self.controller = Windows.Commands()

        self.command_list = {
            "increase_volume": self.increase_volume(),
            "decrease_volume": self.decrease_volume(),
            "get_weather": self.get_weather(),
            "get_time": self.get_time(),
            "open_calculator": self.open_calculator(),
            "open_calender": self.open_calender(),
            "play_music": self.play_music(),
            "open_chrome": self.open_chrome(),
            "set_reminder": lambda: self.search(query),
            "tell_joke": self.tell_joke()
        }

    def run(self, command):
        print(self.command_list.get(command.lower()))


    def increase_volume(self, step=20):
        percent = self.controller.get_volume() + step
        if percent > 100:
            percent = 100
        self.controller.change_volume(percent)
        return "boop"


    def decrease_volume(self, step=20):
        percent = self.controller.get_volume() - step
        if percent < 0:
            percent = 0
        self.controller.change_volume(percent)


    def get_weather(self, city="cairo", api_key=utils.WEATHER):
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "error" in data:
            return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"

        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        feelslike = data["current"]["feelslike_c"]
        return {
            "temperature": temp,
            "condition": condition,
            "feels_like": feelslike,
            "humidity": humidity,
            "wind_speed_kph": wind_kph
        }


    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def open_calculator(self):
        self.controller.open_calculator()

    def open_calender(self):
        self.controller.open_calender()

    def play_music(self):
        webbrowser.open("https://www.spotify.com/")

    def open_chrome(self):
        webbrowser.open("https://www.google.com/")

    def open_maps(self):
        print("map")

    def set_alarm(self):
        print("alarm")

    def search(self, query, sentences=2):
        try:
            summary = wikipedia.summary(query, sentences=sentences)
            return summary
        except wikipedia.DisambiguationError as e:
            return f"Too many results. Suggestions: {e.options[:5]}"
        except wikipedia.PageError:
            return "Page not found."
        except Exception as e:
            return f"Error: {e}"

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
