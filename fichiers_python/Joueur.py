import pygame, random, sys
from couleurs import *


class Joueur():
    def __init__(self, vitesse, coord_x, coord_y, case_i, case_j, direction, largeur, hauteur, chemin_image, nb_grenade, nb_tire, pieces_a_recup, nb_destruction, nb_construction, est_joueur=True, labyrinthe=None, joueur=None):
        # Différentes images pour diriger le modèle en fonction de la direction du regard
        self.image_droite = pygame.image.load(chemin_image).convert_alpha()
        self.image_gauche = pygame.transform.flip(self.image_droite, True, False)
        self.image_haut = pygame.transform.rotate(self.image_droite, 90)
        self.image_bas = pygame.transform.flip(self.image_haut, False, True)
        self.image = self.image_droite

        # Coordonnées relatives
        self.coord_x, self.coord_y = coord_x, coord_y  # Coordonnées du milieu de la hitbox
        self.case_i, self.case_j = case_i, case_j  # Sur quelle case se trouve le personnage
        self.largeur, self.hauteur = largeur, hauteur  # Dimensions de l'image représentant le personnage
        self.mettre_a_jour_hitbox()

        # Autres attributs
        self.vitesse = vitesse
        self.vitesse_ini = vitesse
        self.direction = direction # direction du regard 
        self.pieces_possedee = 0
        self.pieces_a_recup = pieces_a_recup
        self.nb_grenade, self.nb_leurre = nb_grenade, nb_leurre 
        self.nb_destruction, self.nb_construction = nb_destruction, nb_construction 
        self.nb_tire = nb_tire
        self.dernier_tire = time.time()
        self.veut_detruire = False
        if est_joueur : 
            self.endurance = 120
            self.cours_mtn = False
        if not est_joueur:
            self.case = self.case_random( labyrinthe)
        self.vie = 100  # Le joueur a 100 PV
        self.dernier_degat = 0  # Timestamp du dernier dégât reçu

    def peut_tirer(): return self.nb_tire > 0

    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox

    def deplacer(self, touche_pressee, longeur_saut):
        # deplacer le joueur en fonction de sa vitesse et de la touche appuiee
        if touche_pressee == "z" : self.coord_y -= self.vitesse/longeur_saut 
        if touche_pressee == "q" : self.coord_x -= self.vitesse/longeur_saut
        if touche_pressee == "d" : self.coord_x += self.vitesse/longeur_saut
        if touche_pressee == "s" : self.coord_y += self.vitesse/longeur_saut
        self.mettre_a_jour_hitbox()
    
    def deplacer_ennemie(self, long_mur, arrivee, labyrinthe):
        if self.case.milieu_y < self.coord_y: self.deplacer("z", long_mur)
        if self.case.milieu_x < self.coord_x: self.deplacer("q", long_mur)
        if self.case.milieu_y > self.coord_y: self.deplacer("s", long_mur)
        if self.case.milieu_x > self.coord_x: self.deplacer("d", long_mur)
        if self.x1 < self.case.milieu_x < self.x2 and self.y1 < self.case.milieu_y < self.y2 :
            self.case = self.case_random(labyrinthe)


    def chemin_entier(self, arrivee, labyrinthe):
        i1, j1 = self.case_i, self.case_j
        i2, j2 = arrivee
        chemin = []
        while i2 != i1 and j2 != j1:
            case = self.case_random(labyrinthe)
            case.vue = True
            chemin.append(case)
            # a reprendre

    def case_random(self, labyrinthe):
        try : i, j = random.choice(labyrinthe.graphe.voisin_de((self.case_i, self.case_j)))
        except: i, j = self.case_i, self.case_j
        return labyrinthe.laby[i][j]
    
    def meilleur_case(self, debut, arrivee, labyrinthe, chemin=[]):
        G = labyrinthe.graphe
        distance_min = 999
        meilleur_case = random.choice(G.voisin_de(debut))
        for (i, j) in G.voisin_de(debut):
            distance = self.distance((i, j), arrivee)
            case = labyrinthe.laby[i][j]
            if distance < distance_min and len(G.voisin_de((i, j))) > 1 and case not in chemin: # si la case se rapproche et qu'elle a plus de 1 voisin
                distance_min = distance
                meilleur_case = case
        return meilleur_case

    def distance(self, depart, arrivee):
        i1, j1 = depart
        i2, j2 = arrivee
        return abs(j2-j1) + abs(i2-i1)
    
    def jete_flash(self):
        pass
    def jete_leurre(self):
        pass
    def boost_vitesse(self):
        pass
    
    def joueur_meurt(self):
        font = pygame.font.Font(None, 74)
        texte = font.render("Vous êtes mort !", True, red)
        texte_rect = texte.get_rect(center=(self.fenetre.get_width() // 2, self.fenetre.get_height() // 2))
        self.fenetre.blit(texte, texte_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Attendre 2 secondes avant de quitter
        pygame.quit()
        sys.exit()
