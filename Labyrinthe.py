import pygame, codecs, random

class Pile:
    def __init__(self):     self.contenu=[]
    def est_vide(self):     return self.contenu==[]
    def empiler(self,x):    self.contenu.append(x)
    def depiler(self):      return self.contenu.pop() if not self.est_vide() else print("Pile vide !")
    def taille(self):       return len(self.contenu)
    def sommet(self):       return self.contenu[-1] if not self.est_vide() else print("Pile vide !")

class Case:
    def __init__(self):
        self.murN, self.murS, self.murE, self.murW = True, True, True, True
        self.vue = False

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


class Fenetre():
    def __init__(self):
        pass

    def creer_fenetre(self, couleur, titre):
        pygame.init()
        fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
    
    def xy_pourcent(X, Y): return int(pygame.display.Info().current_w*X*0.01), int(pygame.display.Info().current_h *Y*0.01)






if __name__ == "__main__":
    # Lancer le programme
    pass