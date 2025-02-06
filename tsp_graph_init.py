import numpy as np

class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def distance(self, lieu):
        return np.sqrt((self.x - lieu.x)**2+(self.y - lieu.y)**2)