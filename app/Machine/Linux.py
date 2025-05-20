import os
import subprocess
import re
import datetime
import shutil



class Commands:
    def get_volume(self):
            output = subprocess.check_output(["amixer", "get", "Master"]).decode()
            # Extract the first volume percentage
            match = re.search(r"\[(\d{1,3})%\]", output)
            if match:
                return int(match.group(1))

    def change_volume(self, percent):
            os.system(f"amixer sset 'Master' {percent}%")

    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def open_calculator(self):
        for cmd in ["gnome-calculator", "kcalc", "xcalc"]:
            if os.system(f"which {cmd}") == 0:
                os.system(cmd)
                break
        print("No calculator found")

    def open_calender(self):
        for app in ["gnome-calendar", "korganizer", "orage"]:
            if shutil.which(app):
                os.system(app)
                return
        print("No known calendar app found.")

    def open_maps(self):
        print("map")

    def set_alarm(self):
        print("alarm")

    def set_reminder(self):
        print("reminder")

    def tell_story(self):
        print("story")

    def tell_joke(self):
        print("joke")

    def search(self):
        print("search")
