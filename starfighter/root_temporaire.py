from Controleur import MenuControleur
import tkinter as tk
from tkinter import simpledialog
from functools import partial
from os.path import exists
import csv
import os

import vue

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Starfighter")
        #[a,b] = simpledialog.askstring(title="Votre grosseur de fenetre", prompt="Saisissez la largeur et la hauteur de la fenetre \n(Veuillez séparer les 2 valeurs par une virgule)").split(sep=",")
        #f"{a}x{b}"
        self.geometry("800x600")
        #self.frame_menu = tk.Frame(self, background="white")
        self.frame_jeu = tk.Frame(self, background="white")
        
        # canvas = tk.Canvas(Root) #est-ce que ça va fonctionner comme prévu?
        
        self.menuControleur = MenuControleur() #Rajouter self.jeu (2e argument) à la fin du projet # self.destroy retiré
        #self.frame_menu.pack()
        menu_gui = tk.Menu(self)
        # self.config(menu=MenuControleur.creationMenu)
        self.config(menu=menu_gui)
        self.Fichier = tk.Menu(menu_gui, tearoff = 0)   
        menu_gui.add_cascade(label="Nouveau", menu=self.Fichier)
        self.Fichier.add_command(label="Créer une session", command=self.menuControleur.create_Session)
        self.Fichier.add_command(label="Effacer une session", command=self.menuControleur.destroy_Session)
        self.Fichier.add_separator()
        self.Fichier.add_command(label="Quitter", command=self.destroy)
        
        # Menu diffiulté
        self.Difficulte = tk.Menu(menu_gui, tearoff = 0)
        menu_gui.add_cascade(label="Difficulté", menu=self.Difficulte)
        
        # Sous-menu "Difficulté"
        self.sub_difficulty = tk.Menu(self.Difficulte, tearoff = 0)
        self.Difficulte.add_cascade(label="Choisir la difficulté", menu=self.sub_difficulty)
        self.sub_difficulty.add_command(label="Facile", command=partial(self.menuControleur.set_Difficulte, 1))
        self.sub_difficulty.add_command(label="Moyen", command=partial(self.menuControleur.set_Difficulte, 2))
        self.sub_difficulty.add_command(label="Difficile", command=partial(self.menuControleur.set_Difficulte, 3))
     
        self.Score = tk.Menu(menu_gui, tearoff = 0)
        menu_gui.add_cascade(label="Scores", menu=self.Score)
        self.Score.add_command(label="Afficher les scores de la session", command=self.menuControleur.set_Leaderboard)
        
        #menu Fenetre
        self.Fenetre = tk.Menu(menu_gui, tearoff = 0)
        menu_gui.add_cascade(label="Fenêtre", menu=self.Fenetre)
        
        
        #Sous-Menu fenetre
        self.sub_Fenetre = tk.Menu(self.Fenetre, tearoff = 0)
        self.Fenetre.add_cascade(label="Ajuster la fenêtre de jeu", menu=self.sub_Fenetre) #command=self.menuControleur.resize_Frame)
        self.sub_Fenetre.add_command(label="Petite", command=partial(self.resize_Frame, 1))
        self.sub_Fenetre.add_command(label="Moyenne", command=partial(self.resize_Frame, 2))
        self.sub_Fenetre.add_command(label="Grande", command=partial(self.resize_Frame, 3))
        self.sub_Fenetre.add_command(label="Plein écran", command=partial(self.resize_Frame, 4))
        #self.menu.start()
        
        #self.frame_jeu.pack()        
        #self.frame_jeu.pack(fill="both", expand=True)
        #self.jeu =
        

    def resize_Frame(self, choixSize):
        match choixSize:
            case 1: newSize = [800,600, self.attributes("-fullscreen", False)]
            case 2: newSize = [1000,800, self.attributes("-fullscreen", False)]
            case 3: newSize = [1200,1000, self.attributes("-fullscreen", False)]
            case 4: newSize = [self.winfo_screenwidth(), self.winfo_screenheight(), self.attributes("-fullscreen", True)]
        self.geometry(f"{newSize[0]}x{newSize[1]}")