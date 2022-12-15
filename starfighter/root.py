from Controleur import MenuControleur, JeuControleur
import tkinter as tk
from tkinter import simpledialog
from functools import partial
from os.path import exists
import csv
import os
from Forme_temporaire import Bordure, Map
import vue

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Starfighter")
        
        [width,height] = self.resize_Frame(3)
        self.geometry(f"{width}x{height}")

        # pourrait être un affichage de HUD, à voir (14dec.2022)
        # self.frame_menu = tk.Frame(self, background="red")
        # self.frame_menu.pack(fill="both", expand=True)
        
        # canvas = tk.Canvas(Root) #est-ce que ça va fonctionner comme prévu?
        
        self.frame_jeu = tk.Frame(self, background="blue")
        self.jeu = JeuControleur(self.frame_jeu, width, height)
        self.menuControleur = MenuControleur(self.jeu) #Rajouter self.jeu (2e argument) à la fin du projet # self.destroy retiré
    
        menu_gui = tk.Menu(self)
        self.config(menu=menu_gui)
        self.Fichier = tk.Menu(menu_gui, tearoff = 0)   
        menu_gui.add_cascade(label="Nouveau", menu=self.Fichier)
        self.Fichier.add_command(label="Créer une session", command=self.menuControleur.create_Session)
        self.Fichier.add_command(label="Effacer une session", command=self.menuControleur.destroy_Session)
        self.Fichier.add_separator()
        self.Fichier.add_command(label="Quitter", command=self.destroy)
        
        # Menu difficulté
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
        
        #Menu Fenêtre
        self.Fenetre = tk.Menu(menu_gui, tearoff = 0)
        menu_gui.add_cascade(label="Fenêtre", menu=self.Fenetre)
        
        #Sous-Menu Fenêtre
        self.sub_Fenetre = tk.Menu(self.Fenetre, tearoff = 0)
        self.Fenetre.add_cascade(label="Ajuster la fenêtre de jeu", menu=self.sub_Fenetre) #command=self.menuControleur.resize_Frame)
        self.sub_Fenetre.add_command(label="Petite", command=partial(self.resize_Frame, 1))
        self.sub_Fenetre.add_command(label="Moyenne", command=partial(self.resize_Frame, 2))
        self.sub_Fenetre.add_command(label="Grande", command=partial(self.resize_Frame, 3))
        self.sub_Fenetre.add_command(label="Plein écran", command=partial(self.resize_Frame, 4))
        #self.menu.start()
               
        #self.frame_jeu.pack(fill="both", expand=True)
        self.frame_jeu.grid(row=0, column=0, sticky="nsew")
        #self.jeu =

    def resize_Frame(self, choixSize):
        match choixSize:
            case 1: newSize = [800,600, self.attributes("-fullscreen", False)]
            case 2: newSize = [1000,800, self.attributes("-fullscreen", False)]
            case 3: newSize = [1200,1000, self.attributes("-fullscreen", False)]
            case 4: newSize = [self.winfo_screenwidth(), self.winfo_screenheight(), self.attributes("-fullscreen", True)]
        self.geometry(f"{newSize[0]}x{newSize[1]}")
        
        # return necessaire pour créer la grosseur de la fenêtre au boot
        if choixSize == 3:
            return newSize[0], newSize[1]
        
        # self.jeu.resize_Bordure(newSize)
        # (width=newSize[0], height=newSize[1])
        # tester si le frame jeu va bien se redimensionner (pour le gameplay)
        #self.frame_jeu.pack(fill="both", expand=True)