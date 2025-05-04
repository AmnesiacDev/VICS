import platform
import threading
import sys
import os

# DOES NOT WORK YET



class TaskbarTrayIcon:
    def __init__(self, app_title, icon_path, show_callback=None, quit_callback=None):
        self.app_title = app_title
        self.icon_path = icon_path
        self.show_callback = show_callback
        self.quit_callback = quit_callback or sys.exit

        system = platform.system()
        if system == "Windows":
            self.setup_windows_icon()
        elif system == "Linux":
            threading.Thread(target=self.setup_linux_icon, daemon=True).start()

    # Windows setup using pywin32
    def setup_windows_icon(self):
        try:
            import win32gui
            import win32con

            hwnd = win32gui.FindWindow(None, self.app_title)
            if hwnd == 0:
                print("Window not found")
                return

            icon_handle = win32gui.LoadImage(
                0, self.icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE
            )

            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon_handle)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon_handle)
        except Exception as e:
            print(f"Windows icon setup failed: {e}")

    # Linux setup using AppIndicator3
    def setup_linux_icon(self):
        try:
            import gi
            gi.require_version("Gtk", "3.0")
            gi.require_version("AppIndicator3", "0.1")
            from gi.repository import Gtk, AppIndicator3

            self.indicator = AppIndicator3.Indicator.new(
                self.app_title,
                self.icon_path,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

            menu = Gtk.Menu()

            show_item = Gtk.MenuItem(label="Show")
            show_item.connect("activate", lambda _: self.show_callback())
            menu.append(show_item)

            quit_item = Gtk.MenuItem(label="Quit")
            quit_item.connect("activate", lambda _: self.quit_callback())
            menu.append(quit_item)

            menu.show_all()
            self.indicator.set_menu(menu)

            Gtk.main()
        except Exception as e:
            print(f"Linux tray setup failed: {e}")