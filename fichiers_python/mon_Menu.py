from couleurs import *
from Button import Button
import pygame


class Menu:
    def __init__(self, fenetre, largeur, hauteur):
        self.fenetre = fenetre
        self.largeur = largeur
        self.hauteur = hauteur
        self.font = pygame.font.Font(None, 85)
        self.small_font = pygame.font.Font(None, 50)
        self.mode_jeu = None
        self.running = True
        self.clock = pygame.time.Clock()  # Ajouter une horloge pour limiter les FPS

        # Charger l'image de fond
        self.background = pygame.image.load("menu2_image.jpg")  # Remplacez par le chemin de votre image
        self.background = pygame.transform.scale(self.background, (largeur, hauteur))  # Redimensionner l'image

        # Créer les boutons
        self.bouton_solo = Button("Solo", largeur // 2 - 150, hauteur // 2 - 100, 300, 80, blue, black, self.small_font)
        self.bouton_1vs1 = Button("1 vs 1", largeur // 2 - 150, hauteur // 2, 300, 80, blue, black, self.small_font)
        self.bouton_quitter = Button("Quitter", largeur // 2 - 150, hauteur // 2 + 100, 300, 80, red, black, self.small_font)

    def afficher_menu(self):
        # Dessiner l'image de fond
        self.fenetre.blit(self.background, (0, 0))

        # Afficher le titre
        titre = self.font.render("CHOISISSEZ UN MODE DE JEU", True, red)
        titre_rect = titre.get_rect(center=(self.largeur // 2, self.hauteur // 4))
        self.fenetre.blit(titre, titre_rect)

        # Afficher les boutons
        self.bouton_solo.draw(self.fenetre)
        self.bouton_1vs1.draw(self.fenetre)
        self.bouton_quitter.draw(self.fenetre)

        pygame.display.flip()

    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.running = False
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.bouton_solo.is_clicked(mouse_pos):
                    self.mode_jeu = "solo"
                    self.running = False
                elif self.bouton_1vs1.is_clicked(mouse_pos):
                    self.mode_jeu = "1vs1"
                    self.running = False
                elif self.bouton_quitter.is_clicked(mouse_pos):
                    self.running = False

    def boucle_menu(self):
        self.running = True  # Réinitialiser l'état du menu
        while self.running:
            self.gerer_evenements()  # Gérer les événements
            self.afficher_menu()     # Afficher le menu
            pygame.display.flip()    # Rafraîchir l'affichage
            self.clock.tick(60)      # Limiter à 60 FPS
        # Ne pas quitter Pygame ici, laisser le jeu se lancer
