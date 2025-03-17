import pygame, time

class Projectile(): # Flash, leurre... (tout ce qui est jetable)
    def __init__(self, vitesse, chemin_image, fichier_son, type, largeur, hauteur, joueur, distance_nb_case):
        self.vitesse = vitesse
        self.distance_nb_case = distance_nb_case
        self.doit_etre_detruit = False
        self.etat_post_explosion = False
        self.image = pygame.image.load(chemin_image).convert_alpha()
        self.fichier_son = fichier_son
        self.type = type 
        self.largeur, self.hauteur = largeur, hauteur
        self.case_i, self.case_j = joueur.case_i, joueur.case_j
        self.direction = joueur.direction
        self.coord_x, self.coord_y= joueur.coord_x, joueur.coord_y
        self.x_init, self.y_init = joueur.coord_x, joueur.coord_y
        self.mur_doit_etre_detruit = False
        self.mettre_a_jour_hitbox()

    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox

    def lancer(self, long_mur, labyrinthe, liste_ennemies, joueur):
        self.mettre_a_jour_hitbox()
        if self.etat_post_explosion: self.explose(labyrinthe,  liste_ennemies, joueur); return None
        distance_lancer = long_mur*self.distance_nb_case
        if  ((abs(self.coord_x - self.x_init) > distance_lancer or abs(self.coord_y - self.y_init) > distance_lancer)): 
            self.debut = time.time() # pour calculer le temps avant la suppression du projectile a l'ecran
            self.etat_post_explosion = True
        elif self.arret_mur(labyrinthe):
            self.debut = time.time() # pour
            self.etat_post_explosion = True
            self.mur_doit_etre_detruit = True
        else : 
            self.avance(long_mur, liste_ennemies) 

    def arret_mur(self, labyrinthe):
        case = labyrinthe.laby[self.case_i][self.case_j]
        if (case.y1>self.y1 and case.murN) or (case.x1>self.x1 and case.murW) or (case.y2<self.y2 and case.murS) or (case.x2<self.x2 and case.murE) :
            return True  

    def avance(self, longueur_mur, liste_ennemies):
        if self.direction == "N": self.coord_y -= self.vitesse/longueur_mur
        elif self.direction == "S": self.coord_y += self.vitesse/longueur_mur
        elif self.direction == "E": self.coord_x += self.vitesse/longueur_mur
        elif self.direction == "W": self.coord_x -= self.vitesse/longueur_mur
        if self.type == "tire":
            for ennemie in liste_ennemies:
                if self.x1<ennemie.coord_x<self.x2 and self.x1<ennemie.coord_x<self.x2:
                    liste_ennemies.remove(ennemie)

    def explose(self, labyrinthe,  liste_ennemies, joueur):
        self.largeur *= 1.005
        self.hauteur *= 1.005
        if time.time() - self.debut > 1.5:  # si l'explosion a duree plus de 1 secondes
            pygame.mixer.Sound(self.fichier_son).play()
            self.produit_effet(labyrinthe, liste_ennemies, joueur)
            self.doit_etre_detruit = True

    def produit_effet(self, labyrinthe, liste_ennemies, joueur):
        if self.type == "grenade" and self.mur_doit_etre_detruit and 0<self.case_i<labyrinthe.largeur and 0<self.case_j<labyrinthe.hauteur : 
            labyrinthe.abattre_mur(self.case_i, self.case_j, self.direction)
            if self.x1<joueur.coord_x<self.x2 and self.y1<joueur.coord_y<self.y2:
                joueur.vie -= 10
            for ennemie in liste_ennemies:
                    if self.x1<ennemie.coord_x<self.x2 and self.x1<ennemie.coord_x<self.x2:
                        liste_ennemies.remove(ennemie)
        


        
        