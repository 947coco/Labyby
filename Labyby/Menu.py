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
        self.clock = pygame.time.Clock()  

        # Charger l'image de fond
        self.background = pygame.image.load("menu_image1.png")
        self.background = pygame.transform.scale(self.background, (largeur, hauteur))

        # Créer les boutons pour niveaux
        self.boutons_niveaux = []
        espacement = 20  
        largeur_bouton = (largeur - (espacement * 11)) // 10  
        hauteur_bouton = 80
        y_position = hauteur // 2 - hauteur_bouton // 2  

        for i in range(10):  
            x_position = espacement + i * (largeur_bouton + espacement)
            bouton = Button(
                text=f"Niveau {i+1}",
                x=x_position,
                y=y_position,
                width=largeur_bouton,
                height=hauteur_bouton,
                color=blue,  
                hover_color=red,  
                font=self.small_font
            )
            self.boutons_niveaux.append(bouton)

        # Bouton Quitter
        self.bouton_quitter = Button(
            text="Quitter",
            x=largeur // 2 - 150,
            y=hauteur - 100,
            width=300,
            height=80,
            color=red,  
            hover_color=black,  
            font=self.small_font
        )

    def afficher_menu(self):
        # Dessiner l'image de fond
        self.fenetre.blit(self.background, (0, 0))

        # Afficher le titre
        titre = self.font.render("LABYBY", True, red)
        titre_rect = titre.get_rect(center=(self.largeur // 2, self.hauteur // 4))
        self.fenetre.blit(titre, titre_rect)

        # Afficher les boutons des niveaux
        for bouton in self.boutons_niveaux:
            bouton.draw(self.fenetre)

        # Afficher le bouton Quitter
        self.bouton_quitter.draw(self.fenetre)

        pygame.display.flip()

    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.running = False
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Vérifier si un bouton de niveau est cliqué
                for i, bouton in enumerate(self.boutons_niveaux):
                    if bouton.is_clicked(mouse_pos):
                        self.mode_jeu = i+1#f"niveau_{i+1}"  # Définir le mode de jeu
                        self.running = False
                # Vérifier si le bouton Quitter est cliqué
                if self.bouton_quitter.is_clicked(mouse_pos):
                    self.running = False

    def boucle_menu(self):
        self.running = True
        while self.running:
            self.gerer_evenements()  
            self.afficher_menu()  
            pygame.display.flip()  
            self.clock.tick(60)  # Limiter à 60 FPS