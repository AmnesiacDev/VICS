import customtkinter as ctk
from app import utils
from matplotlib import font_manager

class TextBlock(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        FONT = ctk.CTkFont(family=utils.font_name, size=16)
        self.text_box = ctk.CTkButton(self.master, width=300, height=200, text=utils.PLACEHOLDER, fg_color=utils.dark_hover, font=FONT, anchor="nw", text_color=utils.dark_theme,
                                     hover=False, corner_radius=20, compound="left", border_spacing=5)
        self.text_box.place(x=50, y=230)


    def new_text(self, new_text):
        row_size = 35
        formatted = self.chunk_words(new_text, row_size)
        print(type(formatted))
        if ctk.get_appearance_mode() == "light":
            self.text_box.configure(text=formatted, text_color="#000000")
        else:
            self.text_box.configure(text=formatted, text_color="#FFFFFF")

    def light_theme(self):
        self.text_box.configure(fg_color=utils.light_hover, text_color="#000000")

    def dark_theme(self):
        self.text_box.configure(fg_color=utils.dark_hover, text_color="#FFFFFF")

    def get_text(self):
        return self.text_box.cget("text")

    def chunk_words(self, text, max_len=18):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + (1 if current else 0) <= max_len:
                current += (" " if current else "") + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return "\n".join(lines)




