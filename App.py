import threading
import customtkinter as ctk
from pynput import mouse, keyboard
from app import TitleBar, HomeView, utils
import platform

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VICS(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.resizable(True, True)
        self.geometry(utils.DIMENSIONS)

        if "Windows" in platform.system():
            utils.windows_install_font(utils.melon_font_path)
        elif "Linux" in platform.system():
            utils.linux_user_install_font(utils.melon_font_path)

        self._y = self._x =None
        self.withdrawn = self.theme = False
        self.focus_in = True

        utils.center_window(self, utils.WIDTH, utils.HEIGHT)

        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(fill="x", side="top")

        self.custom_title_bar = TitleBar(self.temp_frame)
        self.custom_title_bar.pack(fill="x", side="top")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, side="left")

        self.home_screen = HomeView(self.content_frame)
        self.home_screen.pack(fill="x", side="top")

        self.active_frame = self.show_instance(self.content_frame)

        self.cmb = utils.keyboard_shortcut
        self.current = set()



        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        mouse.Listener(on_click=self.mouse_listener).start()


    def show_instance(self, frame_to_show):
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.pack_forget()
        frame_to_show.pack(fill="both", expand=True)
        return frame_to_show

    def keyboard_listener(self):

        def show_app():
            if not self.focus_in:
                self.deiconify()
                self.focus_in = True
        def on_press(key):


            if any([key in z for z in self.cmb]):
                self.current.add(key)
                if any(all(k in self.current for k in z) for z in self.cmb):
                    show_app()

        def on_release(key):
            if any([key in z for z in self.cmb]):
                self.current.remove(key)


        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def mouse_listener(self, x, y, button, pressed):
        x_coord_start = self.winfo_rootx()
        y_coord_start = self.winfo_rooty()
        x_coord_end = x_coord_start + utils.WIDTH
        y_coord_end = y_coord_start + utils.HEIGHT
        if pressed:
            if (x_coord_start < x < x_coord_end) and (y_coord_start < y < y_coord_end):
                pass
            elif self.focus_in:
                self.withdraw()
                self.focus_in = False


if __name__ == "__main__":
    app = VICS()
    app.mainloop()
