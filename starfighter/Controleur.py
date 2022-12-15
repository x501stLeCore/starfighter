import csv
import os
from os.path import exists
from functools import partial
from tkinter import simpledialog
from random import choice, randint
from tkinter import messagebox, ttk

import c31Geometry2 as c31
from vue import VueMenu, VueJeu
from Forme_temporaire import Misc, Asteroide, Missile, Vaisseau, Ally, Enemy, Ovni, Boss, Map, CarreRouge, Bordure, RectBleu,  Immortality, NoLimit, Stop

class JeuControleur:
    def __init__(self, root, width, height):
        self.root = root
        self.nom_joueur = "Veuillez créer une session"
        self.started = False
        self.difficulte = 1
        self.speed = 10
        self.timer = 0.000
        
        self.vaisseau = CarreRouge()
        # -48 pour laisser de la place au hud en bas de l'écran
        self.bordure = Bordure(width, height-48)
        self.map = Map()
        
        self.vec_power = None
        self.ovnis = []
        self.missiles = []
        self.color = None
      
        self.is_power_active = False
        self.power_up = None
        self.power_timer = 0
        self.power_ups = [
            Immortality(),
            NoLimit(),
            Stop()
        ]

        self.timeout = 100
        self.init_game()


    def define_event(self):
        nom_vide = "Veuillez créer une session"
        if self.nom_joueur != nom_vide and self.difficulte > 0:
            self.vue.setListen(self.vue.canvas,
                               '<Button-1>', self.loop_start) # ne fonctione strictement qu'avec '<Button-1>'
            
        self.vue.setListen(self.vue.canvas, '<Motion>', self.move)
        self.vue.setListen(self.vue.canvas, '<Leave>', self.chasePointer)
        self.vue.setListen(self.vue.canvas, '<Button-3>', self.shoot)
    
    def shoot(self, event):
        vec_carre = c31.Vecteur(self.vue.get_vaisseau().get_barycentre().x,
                                self.vue.get_vaisseau().get_barycentre().y)
        self.missiles.append(Missile(10, 10, vec_carre.x, vec_carre.y, "yellow", 4))
        self.vue.draw_missile(self.missiles[-1], vec_carre.x, vec_carre.y)
        print("shoot")

    def spawn_power_up(self):
        if (round(self.timer, 1) % 10 == 0 and round(self.timer, 1) != 0 and
                self.power_up is None):

            self.power_up = choice(self.power_ups)
            posX = randint(
                self.map.get_x() + self.power_up.get_width(),
                self.map.get_y() - self.power_up.get_width()
                )
            posY = randint(
                self.map.get_x() + self.power_up.get_width(),
                self.map.get_y() - self.power_up.get_width()
                )

            self.power_up.set_x(posX)
            self.power_up.set_x(posY)
            self.vue.draw_power_up(self.power_up, posX, posY)

    def loop_start(self, e):
        if not self.started:
            self.game_loop = c31.LoopEvent(self.vue.canvas, self.start,
                                           self.timeout)
            self.started = True
            self.game_loop.start()

    def has_game_started(self):
        return self.started

    def update_score(self):
        data = [round(self.timer, 3), self.difficulte]

        with open("sessions\\"
                  + MenuControleur.sessions + self.nom_joueur + ".csv",
                  "a", encoding="UTF8", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(data)

    def start(self):
        if self.started:
            if self.difficulte == 4:
                self.upgrade_speed()

            if not self.is_power_active:
                self.spawn_power_up()

            if not self.is_power_active or self.color != "yellow":
                self.change_direction()

            self.update_timer()
            
            # à retravailler pour ne pas entre en conflit avec l'initialisation de la partie
            # if self.timer % 10 == 0:
            #     self.spawn_asteroides()
            #     self.spawn_ovnis()

            if self.is_power_active:
                self.power_timer += 0.1
                if (round(self.power_timer, 1) % 10 == 0 and
                        self.timer != 0):
                    self.cancel_power_up()

            if (self.has_square_collided()):
                self.started = False
                self.timeout *= 3
                self.update_score()
                self.vue.destroy()
                self.vue.message_box("Partie terminée!", "Nombre de secondes: "
                                     + str(round(self.timer, 3)))
                self.vue.reset_timer()
                self.timer = 0
                self.ovnis = []
                self.reset_power_up()
                self.vaisseau.reset()
                self.spawn_ovnis()
                self.define_event()
                self.vue.draw_vaisseau()

    def has_game_started(self):
        return self.started

    def reset_power_up(self):
        self.power_up = None
        self.color = ""

    def move(self, e):
        curseur = c31.Vecteur(e.x, e.y)
        carre_bary = self.vue.get_vaisseau().get_barycentre()
        newPos = curseur - carre_bary

        if curseur.distance(carre_bary) <= self.vaisseau.get_width() / 2:
            self.vue.trans_square(newPos)

    def chasePointer(self, event):
        curseur = c31.Vecteur(event.x, event.y)
        print(curseur)
        translateTo = curseur - self.vue.get_vaisseau().get_barycentre()
        print(translateTo)

    def init_game(self) -> None:
        rect1 = RectBleu(60, 60, self.speed, self.speed, 125, 125)
        rect2 = RectBleu(60, 50, -self.speed, self.speed, 325, 110)
        rect3 = RectBleu(30, 60, self.speed, -self.speed, 110, 375)
        rect4 = RectBleu(100, 20, -self.speed, -self.speed, 380, 365)

        self.ovnis.append(rect1)
        self.ovnis.append(rect2)
        self.ovnis.append(rect3)
        self.ovnis.append(rect4)
        
        self.vue = VueJeu(self.root, self.map, self.bordure,
                           self.vaisseau, self.ovnis,
                           self.difficulte, self.nom_joueur)

        self.vue.draw_ovnis()
        self.vue.draw_vaisseau()
        
    def update_timer(self):
        self.timer += 0.1
        self.vue.update_timer(self.timer)

    def set_nom_joueur(self, name):
        self.nom_joueur = name
        self.vue.update_name(name)
        if self.difficulte > 0:
            self.define_event()

    def set_difficulte(self, difficulte):
        self.difficulte = difficulte
        self.vue.update_difficulty(difficulte)
        self.set_speed()

        if self.nom_joueur != "":
            self.define_event()

    def upgrade_speed(self):
        if round(self.timer, 1) % 5 == 0 and round(self.timer, 1) != 0:
            for rect in self.ovnis:
                rect.upgrade_speed()

    def set_speed(self):
        if self.difficulte == 1 or self.difficulte == 4:
            self.speed = 10
        if self.difficulte == 2:
            self.speed = 15
        if self.difficulte == 3:
            self.speed = 20

        for rect in self.ovnis:
            speedX = self.speed
            speedY = self.speed
            if rect.get_speedX() < -1:
                speedX *= -1
            if rect.get_speedY() < -1:
                speedY *= -1

            rect.set_speed(speedX, speedY)

    def change_direction(self):
        i = 0
        for rect in self.vue.get_ovnis():
            if (rect.get_coordonnees()[1][0] > self.bordure.get_width() or
                    rect.get_coordonnees()[2][0] > self.bordure.get_width()):
                self.ovnis[i].invert_speedX()

            if (rect.get_coordonnees()[0][0] < 0 or
                    rect.get_coordonnees()[3][0] < 0):
                self.ovnis[i].invert_speedX()

            if (rect.get_coordonnees()[0][1] < 0 or
                    rect.get_coordonnees()[1][1] < 0):
                self.ovnis[i].invert_speedY()

            if (rect.get_coordonnees()[2][1] > self.bordure.get_height() or
                    rect.get_coordonnees()[3][1] > self.bordure.get_height()):
                self.ovnis[i].invert_speedY()

            self.vue.trans_rects(self.ovnis[i], i)
            i += 1

    def activate_power_up(self):
        self.is_power_active = True

    def cancel_power_up(self):
        self.is_power_active = False
        self.power_timer = 0

    def has_square_collided(self):
        coord_square = self.vue.get_vaisseau().get_coordonnees()

        vec_carre = c31.Vecteur(self.vue.get_vaisseau().get_barycentre().x,
                                self.vue.get_vaisseau().get_barycentre().y)

        dist_carre = self.vaisseau.get_width()

        if self.power_up:
            self.vec_power = c31.Vecteur(
                self.vue.get_power_up().get_barycentre().x,
                self.vue.get_power_up().get_barycentre().y
            )

            if self.vec_power.distance(vec_carre) < 20:
                self.vue.destroy_power_up()
                self.activate_power_up()
                self.color = self.power_up.get_color()
                self.power_up = None
        # Si le carre rouge dépasse les limites de la map
        out_min = self.map.get_x()
        out_max = self.map.get_y()

        if self.is_power_active:
            # Si le power up est No Limit
            out_min, out_max = NoLimit.get_no_limit(
                self.color,
                self.is_power_active,
                out_min,
                out_max
            )

        if not (coord_square[0][0] > out_min
                and coord_square[1][0] < out_max
                and coord_square[1][1] > out_min
                and coord_square[2][1] < out_max):
            return True

        # Si le carré rouge touche un des rectangles bleus
        if not self.is_power_active or self.color != "orange":
            if self.ovnis:
                i = 0
                for rect in self.vue.get_ovnis():
                    vec_rect = c31.Vecteur(
                                    rect.get_barycentre().x,
                                    rect.get_barycentre().y
                                )

                    if vec_rect.distance(vec_carre) <= dist_carre:
                        return True

                    i += 1

        return False

class MenuControleur:
    """ Variables de classe pour créer, détruire une session et consulter le csv (high scores).
        Utilisées dans 3 méthodes du contrôleur.
    """
    sessions = "sessions"  # Répertoire
    ext = ".csv"

    def __init__(self, JeuControleur):
        """ Fait passer les méthodes du MenuControleur en entier en paramètres à la vue
            pour avoir accès au méthodes du controleur à partir des boutons graphiques.
        """  
        self.jeuControleur = JeuControleur
        self.vue = VueMenu()       

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
            prompt="Saisissez votre nom de la session à creer").capitalize()
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

                self.jeuControleur.set_nom_joueur(name)
            else:  # Si la string est vide.
                errorCode = 5
                VueMenu.message_Box(self, errorCode, name)
        except ValueError:
            pass

    def set_Difficulte(self, choixDifficulte):
        """ Match case Python, équivalent d'un switch.

        Arguments:
            choixDifficulte (int): reçoit en paramètre la difficulté choisie dans le menu supérieur
            
        Envoie ensuite en paramètre la difficulté au jeuControleur et initialise la diffculté du jeu.
        """
        match choixDifficulte:
            case 1 : stringdifficulte = "Facile"
            case 2 : stringdifficulte = "Moyen"
            case 3 : stringdifficulte = "Difficile"
            
        messagebox.showinfo("Choix de difficulté", "La difficulté choisie est : \n\n" +  stringdifficulte)
        self.jeuControleur.set_difficulte(choixDifficulte)

    def destroy_Session(self) -> None:
        """ Destruction d'un fichier csv, on entre le nom de l'utilisateur et s'il existe le fichier sera effacé. """
        name = simpledialog.askstring(title="effacer une session",
                                      prompt="Saisissez le nom à effacer").capitalize()
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
                        ).capitalize()

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
