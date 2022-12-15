class Forme:
    def __init__(self, width, height, color, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color
    
    # tiré de redsqaure
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

# necessaire pour la zone de jeu de starfighter
class Map(Forme):
    def __init__(self, color="white", x=1, y=1199):
        super().__init__(0, 0,color, x, y)

class Misc(Forme):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y, "white")
        self.speed = 4

    def get_speed(self):
        return self.speed

class Asteroide(Misc):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y, "white", 4)

class Missile(Misc):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y, "yellow", 4)

class Vaisseau(Forme):
    def __init__(self, width=20, height=20, x=250, y=250, color="blue", life="true"):
        super().__init__(width, height, x, y, color)
        self.life = life
        self.alive = True
        self.missiles = []

    def get_life(self):
        return self.life

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def set_missile(self, missile: type[Missile]):
        self.missiles.append(missile)

    def get_missiles(self) -> list:
        return self.missiles
    
    def get_color(self):
        return self.color
    
    def reset(self):
        self.x = 250
        self.y = 250

class Ally(Vaisseau):
    def __init__(self):
        super().__init__(50, 50, 600, 920, "blue", 100)
        self.shield = 1

    def get_shield(self):
        return self.shield
    
class CarreRouge(Forme):
    def __init__(self, width=40, color="red", x=600, y=920):
        super().__init__(width, width, color, x, y)

    def reset(self):
        self.x = 600
        self.y = 920

class Enemy(Vaisseau):
    def __init__(self, width, height, x, y, color, life, speed):
        super().__init__(width, height, x, y, color, life)
        self.speed = speed

    def get_speed(self):
        return self.speed

class Ovni(Enemy):
    def __init__(self, x, y, life, speed):
        super().__init__(10, 10, x, y, "red", life, speed)

class Boss(Enemy):
    def __init__(self, x, y, life, speed):
        super().__init__(100, 100, x, y, "pink", life, speed)
        
class RectBleu(Forme):
    def __init__(self, width, height, speedX, speedY, x, y, color="blue"):
        super().__init__(width, height, color, x, y)
        self.speedX = speedX
        self.speedY = speedY

    def set_speed(self, speedX, speedY):
        self.speedX = speedX
        self.speedY = speedY

    def get_speedX(self):
        return self.speedX

    def get_speedY(self):
        return self.speedY

    def invert_speedX(self):
        self.speedX *= -1

    def invert_speedY(self):
        self.speedY *= -1

    def upgrade_speed(self):
        self.speedX += 5 if self.speedX > -1 else -5
        self.speedY += 5 if self.speedY > -1 else -5

# class Bordure est necessaire pour star fighter
class Bordure(Forme):
    def __init__(self, width, height, color="black"):
        super().__init__(width, height, color, 0, 0)
        
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height    

class Stop(Forme):
    def __init__(self, x=0, y=0, width=10, color="yellow"):
        super().__init__(width, width, color, x, y)


class Immortality(Forme):
    def __init__(self, x=0, y=0, width=10, color="orange"):
        super().__init__(width, width, color, x, y)


class NoLimit(Forme):
    def __init__(self, x=0, y=0, width=10, color="green"):
        super().__init__(width, width, color, x, y)

    @staticmethod
    def get_no_limit(color, active, posX, posY):
        x = 0
        y = 0
        if color == "green" and active:
            x = posX - 50
            y = posY + 50
        else:
            x = posX
            y = posY

        return x, y