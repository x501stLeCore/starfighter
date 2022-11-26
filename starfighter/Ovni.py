# Sous-classe de Enemy

class Ovni(Enemy):
    def __init__(self):
        super().__init__()
        
        self.image = PhotoImage(file="images/ovni.png")
        