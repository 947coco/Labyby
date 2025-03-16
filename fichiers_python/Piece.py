import pygame

class Piece():
    def __init__(self, chemin_image, largeur_image, hauteur_image, x, y):
        self.image = pygame.image.load(chemin_image).convert_alpha()
        self.largeur, self.hauteur = largeur_image, hauteur_image
        self.x1, self.y1, self.x2, self.y2 = x, y, x+largeur_image, y+hauteur_image
