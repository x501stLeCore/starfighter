import tkinter as tk


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Starfighter"
        # self.iconimage =

        self.frame_menu = tk.Frame(self, background="white")
        self.frame_jeu = tk.Frame(self, background="white")
        # self.menu =
        # self.jeu =
