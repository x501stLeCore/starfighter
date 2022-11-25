import csv
import os
from os.path import exists
from functools import partial
from tkinter import simpledialog
from random import choice, randint
from tkinter import messagebox, ttk

import c31Geometry2 as c31
from vue import VueMenu

class MenuControleur:
    """ Variables de classe pour créer, détruire une session et consulter le csv (high scores).
        Utilisées dans 3 méthodes du contrôleur.
    """
    sessions = "sessions"  # Répertoire
    ext = ".csv"

    def __init__(self, root,  closeApp): # JeuControleur, argument à ajouter à la fin du projet
        """ Fait passer les méthodes du MenuControleur en entier en paramètres à la vue
            pour avoir accès au méthodes du controleur à partir des boutons graphiques.
        """  
        #self.jeuControler = JeuControleur  # variable à ajouter à la fin du projet
        self.vue = VueMenu(
            root, self.create_Session,
            self.destroy_Session, self.set_Difficulte,
            self.set_Leaderboard, closeApp
        )

    def start(self):
        """Créer graphiquement le menu."""
        self.vue.draw()

    def create_Session(self):
        """ Création de session, l'utilisateur est invité à entrer son nom dans
            la fenêtre interactive, un fichier csv portant son nom est alors créé, ainsi qu'un rpertoir si nécessaire
            Le paramètre nom est ensuite envoyé au jeuControlleur.
        """
        name = simpledialog.askstring(
            title="inscription session",
            prompt="Saisissez votre nom de la session à creer")
        name.capitalize()
        errorCode = 0
        try:
            if not exists(MenuControleur.sessions + "/"):
                os.mkdir(MenuControleur.sessions + "/")
            if name:
                # Vérifie si la string n'est pas vide on crée le fichier CSV
                if not exists(MenuControleur.sessions + "/" + name + MenuControleur.ext):

                    header = ["Temps", "Difficulte"]
                    with open(MenuControleur.sessions + "/" + name + MenuControleur.ext, "w",
                              encoding="UTF8", newline='') as f:
                        writer = csv.writer(f, delimiter=',')
                        writer.writerow(header)
                    errorCode = 1
                    VueMenu.message_Box(self, errorCode, name)
                else:  # Si l'utilisateur existe déjà
                    errorCode = 2
                    VueMenu.message_Box(self, errorCode, name)

                #self.jeuControler.set_nom_joueur(name)
            else:  # Si la string est vide.
                errorCode = 5
                VueMenu.message_Box(self, errorCode, name)
        except ValueError:
            pass

    def set_Difficulte(self):
        """ Match case Python, équivalent d'un switch, peut prendre une string comme choix de 'case'.

        Arguments:
            choixDifficulte (string): reçoit en paramètre la difficulté choisie dans le menu à choix déroulant.
            
        Envoie ensuite en paramètre la difficulté au jeuControleur et initialise la vitesse de jeu.
        """
        
        choixDifficulte = simpledialog.askinteger(title="Choix de difficulté", prompt="inscrivez un nombre entre 1 et 3")
        msgdiff = str(choixDifficulte)
        messagebox.showinfo("Choix de difficulté", "La difficulté choisie est : " +  msgdiff)
        # match choixDifficulte:
        #     case "1-Facile": difficulte = 1
        #     case "2-Normal": difficulte = 2
        #     case "3-Difficile": difficulte = 3
        #     case "4-Progressif": difficulte = 4

        #self.jeuControleur.set_difficulte(difficulte)

    def destroy_Session(self) -> None:
        """ Destruction d'un fichier csv, on entre le nom de l'utilisateur et s'il existe le fichier sera effacé. """
        name = simpledialog.askstring(title="effacer une session",
                                      prompt="Saisissez le nom à effacer")
        name.capitalize()
        errorCode = 0

        try:
            if name:  # Vérifier si la string n'est pas vide
                if exists(MenuControleur.sessions + "/" + name + MenuControleur.ext):

                    os.remove(MenuControleur.sessions + "/" + name + MenuControleur.ext)
                    errorCode = 3
                    VueMenu.message_Box(self, errorCode, name)
                else:
                    errorCode = 4
                    VueMenu.message_Box(self, errorCode, name)
            else:
                errorCode = 5 # Si la string est vide.
                VueMenu.message_Box(self, errorCode, name)
        except Exception:
            pass

    def set_Leaderboard(self):
        """ Affichage des scores pour une session, l'utlisateur écrit le nom de fichier d'une personne et ses meilleurs temps apparaissent. """
   
        name = simpledialog.askstring(
                            title="Afficher les temps d'un utilisateur",
                            prompt="Saisissez le nom de l'utilisateur "
                                   + "pour voir les scores"
                        )
        name.capitalize()

        if exists(MenuControleur.sessions + "/" + name + MenuControleur.ext):
            with open(MenuControleur.sessions + "/" + name + MenuControleur.ext, "r") as f:
                next(f)
                self.reader = csv.reader(f)
                self.leaderboard = list(self.reader)
                self.leaderboard.sort(key=lambda score: float(score[0]),
                                      reverse=True)
                self.vue.draw_leaderboard(name, self.leaderboard)
        else:
            pass
