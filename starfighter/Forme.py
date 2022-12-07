class Forme:
    def __init__(self, width, height, x, y, color):
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


class Missile(Forme):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y, "yellow")
        self.speed = 4

    def get_speed(self):
        return self.speed


class Vaisseau(Forme):
    def __init__(self, width, height, x, y, color, life):
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


class Ally(Vaisseau):
    def __init__(self):
        super().__init__(10, 10, 250, 250, "blue", 100)
        self.shield = 1

    def get_shield(self):
        return self.shield


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
