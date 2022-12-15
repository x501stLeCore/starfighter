import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import c31Geometry2 as c31

class Vue:
    def __init__(self, root):
        self.root = root
    
    def setListen(self, canvas, eventName, command):
        canvas.bind(eventName, command)
        
class VueJeu(Vue):
    def __init__(self, root, map, bordure, vaisseau,
                 rect_bleus: list, difficulte, nom):
        super().__init__(root)
        self.canvas = tk.Canvas(root, background=bordure.get_color(),
                                width=bordure.get_width(),
                                height=bordure.get_height())
        
        self.name_hud = tk.Label(text=nom, font=("Arial", 25),
                                 background="white")
        self.difficulty_hud = tk.Label(text=difficulte, font=("Arial", 25),
                                       background="white")
        self.update_difficulty(difficulte)
        self.timer_hud = tk.Label(text=str(0), font=("Arial", 25),
                                  background="white")

        self.map = self.canvas.create_rectangle(map.get_x(),
                                                map.get_x(),
                                                map.get_y(),
                                                map.get_y(),
                                                fill=map.get_color(),
                                                outline=map.get_color())
        self.vaisseau = c31.Carre(
                self.canvas,
                c31.Vecteur(
                    vaisseau.get_x(), vaisseau.get_y()),
                vaisseau.get_width(),
                remplissage=vaisseau.get_color(),
                bordure=vaisseau.get_color()
                )

        self.ovnis = [
            c31.Rectangle(self.canvas,
                          c31.Vecteur(rect.get_x(), rect.get_y()),
                          rect.get_width(), rect.get_height(),
                          remplissage=rect.get_color(),
                          bordure=rect.get_color())
            for rect in rect_bleus
            ]

        self.power_up = 0
        self.canvas.grid(column=0, columnspan=3)
        self.name_hud.grid(row=1, column=0, sticky="sw")
        self.difficulty_hud.grid(row=1, column=0, sticky="s")
        self.timer_hud.grid(row=1, column=0, sticky="se")

    def draw_ovnis(self):
        for rect in self.ovnis:
            rect.draw()

    def update_name(self, name):
        self.name_hud.config(text=name)
        
    # def update_canvas(self, bordure):
    #     self.canvas.config(width=bordure.get_width(),
    #                        height=bordure.get_height())

    def update_difficulty(self, diff_number):
        if diff_number == 1:
            diff = "Facile"
        elif diff_number == 2:
            diff = "Moyen"
        elif diff_number == 3:
            diff = "Difficile"
        self.difficulty_hud.config(text=diff)

    def update_timer(self, timer):
        self.timer_hud.config(text=str(round(timer, 3)))

    def draw_vaisseau(self):
        self.vaisseau.draw()

    def draw_power_up(self, power, x, y):
        self.power_up = c31.Cercle(
                        self.canvas,
                        c31.Vecteur(x, y),
                        power.get_width(),
                        remplissage=power.get_color(),
                        bordure=power.get_color()
                    )
        self.power_up.draw()

    def destroy_power_up(self):
        self.power_up.delete()
        self.power_up = None

    def trans_rects(self, rect, idx):
        self.ovnis[idx].translate(c31.Vecteur(rect.get_speedX(),
                                       rect.get_speedY()))
        self.ovnis[idx].draw()

    def trans_square(self, position: c31.Vecteur):
        self.vaisseau.translate(position)
        self.vaisseau.draw()

    def get_vaisseau(self):
        return self.vaisseau

    def get_ovnis(self):
        return self.ovnis
    
    # def get_boss(self):
    #     return self.boss

    def get_power_up(self):
        return self.power_up

    def get_canvas(self):
        return self.canvas

    def destroy(self):
        self.canvas.destroy()

    def reset_timer(self):
        self.update_timer(0)

    def message_box(self, title: str, text: str):
        messagebox.showinfo(title=title,
                            message=text)

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
