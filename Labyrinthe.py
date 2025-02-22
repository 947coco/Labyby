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
        self.largeur, self.hauteur = largeur, hauteur
        self.laby = [[Case() for i in range(self.hauteur)] for x in range(self.largeur)]

    def __directions_possibles(self,i,j):
        directions = []
        if 0 <= j < self.hauteur-1 and not self.laby[i][j+1].vue: directions.append('S')
        if 1 <= j < self.hauteur and not self.laby[i][j-1].vue: directions.append('N')
        if 1 <= i < self.largeur and not self.laby[i-1][j].vue: directions.append('W')
        if 0 <= i < self.largeur-1 and not self.laby[i+1][j].vue: directions.append('E')
        return directions


    def __abattre_mur(self,i,j,dir,pile):
        if dir == 'S': # on se dirige vers le sud
            self.laby[i][j].murS = False # on abat le mur sud de la case courante
            self.laby[i][j+1].murN = False # on abat le mur nord de la case située en-dessous de la case courante
            self.laby[i][j+1].vue = True # cette case est alors marquée comme vue
            pile.empiler((i, j+1)) # on stocke les coordonnées de cette case dans la pile
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
        pass


    def generer(self):
        pile = Pile()
        i, j = random.randint(0, self.largeur-1), random.randint(0, self.hauteur-1)
        pile.empiler((i, j))
        self.laby[i][j].vue = True
        while not pile.est_vide():
            i, j = pile.sommet()
            directions = self.__directions_possibles(i, j)
            pile.depiler() if len(directions) == 0 else self.__abattre_mur(i, j, random.choice(directions), pile)

    

class Jeux():
    def __init__(self, couleur, titre, largeur_laby, hauteur_laby):
        pygame.init()
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
        self.icon = pygame.image.load('logo.png')
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.liste_labels = [] # liste de tuple pour enregistrer les labels
        self.liste_lignes = [] # liste de tuple pour enregistrer les lignes
        self.largeur_laby, self.hauteur_laby = largeur_laby, hauteur_laby
        self.labyrinthe = Labyrinthe(largeur_laby, hauteur_laby)

    # Sert à convertir des pourcentages X, Y en fonction de la taille de l'écran (donc 100 > X,Y > 0)
    def unite_relatif(self, X, Y): return int(pygame.display.Info().current_w*X*0.01), int(pygame.display.Info().current_h *Y*0.01)

    def creer_ligne(self, x1, y1, x2, y2, epaisseur, couleur): 
        self.ligne = pygame.draw.line(self.fenetre, couleur, (x1, y1), (x2, y2), epaisseur)
        self.liste_labels.append(self.ligne)

    def update(self): 
        #[self.fenetre.blit(element, position) for element, position, taille in self.liste_labels]
        [self.fenetre.blit(element) for element in self.liste_lignes]
    """
    def creer_label(self, x, y, w, h, couleur):
        self.label_xy = self.unite_relatif(x, y)
        self.label_wh = self.unite_relatif(w, h)
        self.label = pygame.surface.Surface(self.label_wh)
        self.label.fill(couleur)
        self.liste_labels.append((self.label, self.label_xy))
    """
    def afficher(self, marge, longeur, epaisseur):
        """
        Fonction pour afficher le labyrinthe. Explication de ce bordel :
        on a, pour chaque coordonner de point (tout en unite relatif): 
        - la marge prise en compte (pour pouvoir deplacer tout notre labyrinthe)
        - la longeur du trait
        - les coordonees de i et j pour les differentes cases
        """
        marge_x, marge_y = self.unite_relatif(marge, marge)
        long_mur_x, long_mur_y = self.unite_relatif(longeur, longeur)
        epaisseur_relatif, pas_imortant  = self.unite_relatif(epaisseur, epaisseur) 
        for i in range(self.largeur_laby):
            for j in range(self.hauteur_laby):
                unite_i, unite_j = self.unite_relatif(i*2, j*2)
                if self.labyrinthe.laby[i][j].murS:
                    self.creer_ligne(marge_x+unite_i, marge_y+unite_j+long_mur_y, marge_x+unite_i+long_mur_x, marge_y+unite_j+long_mur_y, epaisseur_relatif, green)
                if self.labyrinthe.laby[i][j].murW:
                    self.creer_ligne(marge_x+unite_i, marge_y+unite_j, marge_x+unite_i, marge_y+unite_j+long_mur_y, epaisseur_relatif, green)
                if self.labyrinthe.laby[i][j].murN:
                    self.creer_ligne(marge_x+unite_i, marge_y+unite_j, marge_x+unite_i+long_mur_x, marge_y+unite_j, epaisseur_relatif, green)
                if self.labyrinthe.laby[i][j].murE:
                    self.creer_ligne(marge_x+unite_i+long_mur_x, marge_y+unite_j, marge_x+unite_i+long_mur_x, marge_y+unite_j+long_mur_y, epaisseur_relatif, green)
        

    def boucle_jeu(self):
        while True :
            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    # Bouton exit
                    #if exit_xy[0] <= evenement.pos[0] <= exit_xy[0] + exit_wh[0] and exit_xy[1] <= evenement.pos[1] <= exit_xy[1] + exit_wh[1]:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                print("touche z clique")
            if keys[pygame.K_s]:
                print("touche s clique")

            
            self.afficher(20, 2, 0.1)
            self.update()

            pygame.display.flip() # put your work on screen

            self.clock.tick(60)  # limites les FPS a 60

jeu = Jeux(black, "titre1", 10, 20)
#jeu.creer_label(500, 500, 200, 200, red)
#jeu.creer_ligne(500, 500, 100, 100, 5, green)
jeu.boucle_jeu()
if __name__ == "__main__":
    # Lancer le programme
    pass