import pygame, codecs, random, time, sys

# definition des couleurs primaires/principales
white, black          = (255, 255, 255), (0, 0, 0)
red, green, blue      = (255, 0, 0), (0, 255, 0), (0, 0, 255)
yellow, cyan, magenta = (255, 255, 0), (0, 255, 255), (255, 0, 255)
orange, purple, pink  = (255, 165, 0), (128, 0, 128), (233, 40, 99)

class Pile:
    def __init__(self):     self.contenu=[]
    def est_vide(self):     return self.contenu==[]
    def empiler(self,x):    self.contenu.append(x)
    def depiler(self):      return self.contenu.pop() if not self.est_vide() else print("Pile vide !")
    def taille(self):       return len(self.contenu)
    def sommet(self):       return self.contenu[-1] if not self.est_vide() else print("Pile vide !")

class Case: 
    def __init__(self): 
        self.murN, self.murS, self.murE, self.murW, self.vue = True, True, True, True, False

class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.hauteur, self.largeur = largeur, hauteur
        self.laby = [[Case() for i in range(self.largeur)] for x in range(self.hauteur)]

    def __directions_possibles(self,i,j):
        directions = []
        if 0 <= j < self.largeur-1 and not self.laby[i][j+1].vue: directions.append('S')
        if 1 <= j < self.largeur and not self.laby[i][j-1].vue: directions.append('N')
        if 1 <= i < self.hauteur and not self.laby[i-1][j].vue: directions.append('W')
        if 0 <= i < self.hauteur-1 and not self.laby[i+1][j].vue: directions.append('E')
        return directions

    def __abattre_mur(self,i,j,dir,pile):
        if dir == 'S': # on se dirige vers le sud
            self.laby[i][j].murS = False # on abat le mur sud de la case courante
            self.laby[i][j+1].murN = False # on abat le mur nord de la case situee en-dessous de la case courante
            self.laby[i][j+1].vue = True # cette case est alors marquee comme vue
            pile.empiler((i, j+1)) # on stocke les coordonnees de cette case dans la pile
        if dir == 'N':
            self.laby[i][j].murN = False  
            self.laby[i][j-1].murS = False  
            self.laby[i][j-1].vue = True 
            pile.empiler((i, j-1))  
        if dir == 'E':
            self.laby[i][j].murE = False  
            self.laby[i+1][j].murW = False 
            self.laby[i+1][j].vue = True 
            pile.empiler((i+1, j))  
        if dir == 'W':
            self.laby[i][j].murW = False  
            self.laby[i-1][j].murE = False  
            self.laby[i-1][j].vue = True 
            pile.empiler((i-1, j))   

    def generer(self):
        """
        J'ai ajouter la boucle for pour eviter que le labyrinthe soit parfait 
        """
        pile = Pile()
        i, j = random.randint(0, self.hauteur-1), random.randint(0, self.largeur-1)
        pile.empiler((i, j))
        self.laby[i][j].vue = True
        while not pile.est_vide():
            i, j = pile.sommet()
            directions = self.__directions_possibles(i, j)
            pile.depiler() if len(directions) == 0 else self.__abattre_mur(i, j, random.choice(directions), pile)
        for k in range(int(4*self.hauteur*self.largeur * 0.12)): # Supprime environ x% des murs du labyrinthe parfait
            x, y = random.randint(2, self.hauteur-2), random.randint(2, self.largeur-2)
            direction = random.choice(["W", "E", "N", "S"])
            self.__abattre_mur(x,y,direction,pile)         
        

""" 
Quand on aura fini, il faudra separer les classes dans des fichiers distincts pour que ce soit plus clean
mais pour l'instant, c'est plus pratique d'avoir la classe Labyrinthe a porter.
Et ducoup il faudra faire des importations : import Labyrinthe from Labyrinthe par exemple
"""

class Joueur():
    def __init__(self, vitesse, chemin_image, chemin_image_transparence, nb_flash, nb_leurre, cooldown_transparence):
        self.vitesse = vitesse
        self.image = pygame.image.load(chemin_image).convert()
        self.image_transparence = pygame.image.load(chemin_image_transparence).convert()
        self.cooldown_transparence = cooldown_transparence
        self.nb_flash, self.nb_leurre = nb_flash, nb_leurre

    def placer(self, coordonee_x, coordonee_y, direction_vue):
        self.coordonee_x, self.coordonee_y = coordonee_x, coordonee_y
        self.direction_vue = direction_vue

    def deplacer(self, touche_pressee):
        if touche_pressee == "z" : 
            self.coordonee_y -= 1
            time.sleep(1/self.vitesse)
        if touche_pressee == "q" : 
            self.coordonee_x -= 1
            time.sleep(1/self.vitesse)
        if touche_pressee == "s" : 
            self.coordonee_y += 1
            time.sleep(1/self.vitesse)
        if touche_pressee == "d" : 
            self.coordonee_x += 1
            time.sleep(1/self.vitesse)

    def devient_transparent(self, labyrinthe):
        pass
    def jete_flash(self):
        pass
    def jete_leurre(self):
        pass
    def controle_ennemie(self):
        pass
    def boost_vitesse(self):
        pass


class Ennemie():
    def __init__(self, labyrinthe, vitesse, chemin_image):
        self.vitesse = vitesse
        self.chemin_image = chemin_image


class Projectile(): # Flash, leurre... (tout ce qui est jetable)
    def __init__(self, vitesse, chemin_image, quantitee):
        self.vitesse = vitesse
        self.chemin_image = chemin_image
        self.quantitee = quantitee
        

    def lancement(self, direction_du_lance, position_joueur_x, position_joueur_y):

        pass

class Jeux():
    def __init__(self):
        self.joueur = None
        pass



    def creer_fenetre(self, couleur, titre, fenetre_principale, fenetre_existant_w=0, fenetre_existant_h=0):
        """
        creer une fenetre avec un titre, une couleur de fond et verifie si une fenetre principale
        a deja ete creer, dans ce cas, on creer une fenetre pop up plus petit au dessus de la principale 
        (exemple : fenetre de pause, d'acceuil...)
        """
        pygame.init()
        if fenetre_principale : # 1ère fenetre en plein ecran
            self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else : # Cas ou l'on veut creer une fenetre secondaire
            largeur, hauteur = self.unite_relatif(fenetre_existant_w, fenetre_existant_h)
            self.fenetre = pygame.display.set_mode((largeur, hauteur))
        self.fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
        self.clock = pygame.time.Clock()
        self.liste_labels = [] # dico pour enregistrer les labels (cle) et leurs coordonnees (valeur). forme : [x, y, w, h]
        self.liste_lignes = [] # dico pour enregistrer les lignes (cle) et leurs coordonnees (valeur). forme : [x1, y1, x2, y2]
        #self.icon = pygame.image.load('logo.png')
        #pygame.display.set_icon(self.icon)
        
        
    # FONCTIONS A FAIRE : Implementer les compteurs et afficher sur l'ecran ceux-ci    
    def afficher_score(self):
        pass # A FAIRE
    def afficher_compteur_munition(self):
        pass # A FAIRE
    def afficher_compteur_vie(self):
        pass # A FAIRE
    def afficher_compteur_transparence(self):
        pass # A FAIRE
    def afficher_compteur_flash(self):
        pass # A FAIRE
    def afficher_compteur_leurre(self):
        pass # A FAIRE
    def afficher_compteur_boost_vitesse(self):
        pass # A FAIRE

    # Sert a convertir des pourcentages X, Y en fonction de la taille de l'ecran afin de pouvoir jouer sur plusieurs resolutions possibles
    def unite_relatif(self, X, Y): return int(pygame.display.Info().current_w*X*0.01), int(pygame.display.Info().current_h *Y*0.018)
    # le petit 0.018 a la fin c'est pour ajuster le desequilibre entre la largeur et la hauteur de l'ecran car la hauteur est toujours plus petite  

    def creer_ligne(self, x1, y1, x2, y2, epaisseur, couleur):  # x1, y1 = coordonees du debut de la ligne, x2 et y2 sont la fin
        self.ligne = pygame.draw.line(self.fenetre, couleur, (x1, y1), (x2, y2), epaisseur)
        self.liste_lignes.append([x1, y1, x2, y2]) 

    def creer_label(self, coordonnee_x, coordonnee_y, largeur, hauteur, couleur):
        # creer un label de coordonees x, y et de taille largeur x hauteur
        x, y = self.unite_relatif(coordonnee_x, coordonnee_y)
        w, h = self.unite_relatif(largeur, hauteur) 
        label = pygame.surface.Surface(w , h)
        label.fill(couleur)
        self.liste_labels.append([x, y, w, h])
    

    def creer_labyrinthe(self, largeur, hauteur, marge_x, marge_y, longeur_mur, epaisseur_mur):
        self.long_mur_x, self.long_mur_y = self.unite_relatif(longeur_mur, longeur_mur)
        self.epaisseur_mur, pas_important  = self.unite_relatif(epaisseur_mur, 0) 
        self.marge_x, self.marge_y = self.unite_relatif(marge_x, marge_y)
        self.hauteur_laby, self.largeur_laby = largeur, hauteur
        self.labyrinthe = Labyrinthe(self.hauteur_laby, self.largeur_laby)
        self.labyrinthe.generer()
        self.afficher_labyrinthe()

    def afficher_labyrinthe(self):
        """
        Fonction pour afficher le labyrinthe. Explication de ce bordel :
        on a, pour chaque coordonnee de point (tout en unite relatif): 
        - la marge prise en compte (pour pouvoir deplacer tout notre labyrinthe)
        - la longeur du trait / mur
        - les coordonees de i et j pour les differentes cases
        """
        for i in range(len(self.labyrinthe.laby)):
            for j in range(len(self.labyrinthe.laby[i])):
                unite_i, unite_j = self.unite_relatif(i*2, j*2)
                unite_i += self.marge_x
                unite_j += self.marge_y
                if self.labyrinthe.laby[i][j].murS:
                    self.creer_ligne(unite_i, unite_j+self.long_mur_y, unite_i+self.long_mur_x, unite_j+self.long_mur_y, self.epaisseur_mur, green)
                if self.labyrinthe.laby[i][j].murW:
                    self.creer_ligne(unite_i, unite_j, unite_i, unite_j+self.long_mur_y, self.epaisseur_mur, green)
                if self.labyrinthe.laby[i][j].murN:
                    self.creer_ligne(unite_i, unite_j, unite_i+self.long_mur_x, unite_j, self.epaisseur_mur, green)
                if self.labyrinthe.laby[i][j].murE:
                    self.creer_ligne(unite_i+self.long_mur_x, unite_j, unite_i+self.long_mur_x, unite_j+self.long_mur_y, self.epaisseur_mur, green)

    def creer_joueur(self):
        self.joueur = Joueur(100, "./Logo_joueur.png", "./Logo_joueur.png", 0, 0, 0)
        coord_joueur_x, coord_joueur_y = self.unite_relatif(10, 10)
        self.joueur.placer(coord_joueur_x, coord_joueur_y, "S")

    def afficher_joueur(self):
        image =  pygame.transform.scale(self.joueur.image, (self.long_mur_x, self.long_mur_y))  
        self.fenetre.blit(image, (self.marge_x+self.joueur.coordonee_x, self.marge_y+self.joueur.coordonee_y))
        
    def verifier_collision(self):
        self.labyrinthe.laby[self.joueur.coordonee_x][self.joueur.coordonee_y].murN
    def boucle_jeu(self):
        joueur_present = False
        if self.joueur != None : joueur_present = True 
        while True :
            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    # Bouton exit
                    #if exit_xy[0] <= evenement.pos[0] <= exit_xy[0] + exit_wh[0] and exit_xy[1] <= evenement.pos[1] <= exit_xy[1] + exit_wh[1]:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            

            if keys[pygame.K_z]: self.joueur.deplacer("z")
            if keys[pygame.K_q]: self.joueur.deplacer("q")
            if keys[pygame.K_s]: self.joueur.deplacer("s")
            if keys[pygame.K_d]: self.joueur.deplacer("d")

            self.fenetre.fill(black)
            
            #self.update()
            self.afficher_labyrinthe()
            self.afficher_joueur()
            pygame.display.flip() # put your work on screen

            self.clock.tick(60)  # limites les FPS a 60


if __name__ == "__main__":
    jeu = Jeux()
    jeu.creer_fenetre(black, "titre1", True)
    jeu.creer_labyrinthe(30, 20, 6, 6, 2, 0.2)
    jeu.creer_joueur()
    #jeu.creer_label(500, 500, 200, 200, red)
    #jeu.creer_ligne(500, 500, 100, 100, 5, green)
    jeu.boucle_jeu()