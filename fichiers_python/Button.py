import pygame
from couleurs import *
# Classe pour les boutons du menu
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, fenetre):
        # Change la couleur si la souris est sur le bouton
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(fenetre, self.hover_color, self.rect)
        else:
            pygame.draw.rect(fenetre, self.color, self.rect)

        # Ajoute le texte au centre du bouton
        text_surface = self.font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        fenetre.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
