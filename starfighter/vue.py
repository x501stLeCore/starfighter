import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import c31Geometry2 as c31

class Vue:
    def __init__(self, root):
        self.root = root

    def setListen(self, canvas, eventName, command):
        canvas.bind(eventName, command)

class VueMenu():
    def __init__(self): # root, fct_creer_session, destroy_Session, fct_Choix_diff, set_Leaderboard, closeApp
        """ Création graphique du menu du logiciel,
            reçoit en paramètre les méthodes à appeler au controlleur
            lorsqu'on appuie sur un bouton du GUI.

        Arguments:
            root (tk): _description_
            fct_creer_session (méthode):    Bouton pour appeler la méthode create_Session
            destroy_Session (méthode):      Bouton pour appeler la méthode destroy_Session
            fct_Choix_diff (méthode):       Bouton pour appeler la méthode set_Difficulte
            set_Leaderboard (méthode):      Bouton pour appeler la méthode set_Leaderboard
            closeApp (méthode):             Bouton pour appeler root.destroy()
        """
        #self.root = root
        
    #     self.root.grid()
    #     # self.btn_create = tk.PhotoImage(
    #     #                         file="images/buttons/btn_create_session.png"
    #     #                     )
    #     self.boutonCreateSession = ttk.Button(
    #                                 root, text="Créer session",
    #                                 command=fct_creer_session
    #                             )

    #     # self.btn_delete = tk.PhotoImage(
    #     #                         file="images/buttons/btn_delete_session.png"
    #     #                     )

    #     self.boutonDestroySession = ttk.Button(root, text="Effacer session",
    #                                            command=destroy_Session)
        
    #     """ Menu déroulant pour sélectionner la difficulté du jeu.
    #         Lorsque l'utilisateur effectue son choix, le 4e argument du ttk.OptionMenu (*self.choix)
    #         envoie la string choisie en paramètre au moment de l'appel de la commande
    #     """
    #     self.selection = StringVar()
    #     self.selection.set("Difficulte")
    #     self.choix = [
    #         "1-Facile",
    #         "2-Normal",
    #         "3-Difficile",
    #         "4-Progressif"
    #     ]
    #     # self.diff_choice = tk.PhotoImage(
    #     #                     file="images/buttons/btn_choix_diff.png"
    #     #                     )
    #     self.boutonSetDifficulte = ttk.OptionMenu(root, self.selection,
    #                                               "Difficulte", *self.choix,
    #                                               command=fct_Choix_diff)

    #     # self.show_score = tk.PhotoImage(
    #     #                             file="images/buttons/btn_show_scores.png"
    #     #                             )

    #     self.boutonSetLeaderboard = ttk.Button(root, text="Afficher scores",
    #                                            command=set_Leaderboard)

    #     self.boutonQuitterJeu = ttk.Button(root, text="Quitter le jeu",
    #                                        command=closeApp)

    # def draw(self):
    #     """ Positionnement des boutons dans l'environnement GUI. """
    #     i = 1
    #     self.boutonCreateSession.grid   (row=i, column=1)
    #     self.boutonDestroySession.grid  (row=i, column=2)
    #     self.boutonSetDifficulte.grid   (row=i, column=3)
    #     self.boutonSetLeaderboard.grid  (row=i, column=4)
    #     self.boutonQuitterJeu.grid      (row=i, column=5)

    def message_Box(self, codeErreur, name):
        """ Boîtes de messages contextuelle pour les boutons Créer session, effacer session et afficher les scores.

        Arguments:
            codeErreur (int): numéro du code d'erreur envoyé pour faire afficher selon le contexte.
            name (string): Nom de la personne saisie au clavier
        """
        
        match codeErreur:
            case 1: messagebox.showinfo(
                'Confirmation creation',
                "l'utilisateur " + name + " a ete cree"
            )

            case 2: messagebox.showerror(
                'Erreur de creation',
                "l'utilisateur " + name + " existe dejà"
            )

            case 3: messagebox.showinfo(
                'Confirmation suppression',
                "l'utilisateur " + name + " a bien ete supprime"
            )

            case 4: messagebox.showerror(
                'Erreur de suppression',
                "l'utilisateur " + name + " n'existe pas"
            )

            case 5: messagebox.showerror('Erreur',
                                         "vous n'avez rien saisi au clavier")

    def draw_leaderboard(self, name,  list):
        """ Affiche les temps de la personne

        Arguments:
            name (String): Nom de la personne saisie au clavier
            list (string[]): Les temps de la personne
        """
        texte = ""
        i = 1
        for score in list:
            sec = score[0] + "s "
            diff = ""
            print(score[1])
            if score[1] == "1":
                diff = "Facile"
            elif score[1] == "2":
                diff = "Normal"
            elif score[1] == "3":
                diff = "Difficile"
            else:
                diff = "Progressif"

            texte += str(i) + ". " + sec + diff + "\n"
            i += 1

        messagebox.showinfo("Meilleurs temps pour " + name, texte)
