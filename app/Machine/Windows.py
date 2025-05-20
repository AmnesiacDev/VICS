import datetime
import os



class Commands:

    def get_volume(self):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        return round(volume.GetMasterVolumeLevelScalar() * 100)


    def change_volume(self, percent):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(percent / 100, None)


    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def open_calculator(self):
        return os.system("start calc")

    def open_calender(self):
        os.system("start outlookcal:")



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