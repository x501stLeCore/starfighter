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
        [a,b] = simpledialog.askstring(title="Votre grosseur de fenetre", prompt="Saisissez la largeur et la hauteur de la fenetre \n(Veuillez séparer les 2 valeurs par une virgule)").split(sep=",")
        self.geometry(f"{a}x{b}")
        self.frame_menu = tk.Frame(self, background="white")
        self.frame_jeu = tk.Frame(self, background="white")
        
        self.menu = MenuControleur(self.frame_menu, self.destroy) #Rajouter self.jeu (2e argument) à la fin du projet
        self.frame_menu.pack()
        
        menu_gui = tk.Menu(self)
        # self.config(menu=MenuControleur.creationMenu)
        self.config(menu=menu_gui)
    
        self.Fichier = tk.Menu(menu_gui)    
        menu_gui.add_cascade(label="Nouveau", menu=self.Fichier)
        self.Fichier.add_command(label="Créer une session", command=self.menu.create_Session)
        self.Fichier.add_command(label="Effacer une session", command=self.menu.destroy_Session)
        self.Fichier.add_separator()
        self.Fichier.add_command(label="Quitter", command=self.destroy)
        
        self.Difficulte = tk.Menu(menu_gui)
        menu_gui.add_cascade(label="Difficulté", menu=self.Difficulte)
        self.Difficulte.add_command(label="Choisir le niveau de difficulté", command=self.menu.set_Difficulte)

        self.Score = tk.Menu(menu_gui)
        menu_gui.add_cascade(label="Scores", menu=self.Score)
        self.Score.add_command(label="Afficher les scores de la session", command=self.menu.set_Leaderboard)
        
        self.Fenetre = tk.Menu(menu_gui)
        menu_gui.add_cascade(label="Fenêtre", menu=self.Fenetre)
        #self.Fenetre.add_command(label="Définir la taille du jeu", command=self.menu.set_frame_jeu_size)
        
        # self.frame_jeu.pack(fill="both", expand=True)
        # self.jeu =
        
        self.menu.start()