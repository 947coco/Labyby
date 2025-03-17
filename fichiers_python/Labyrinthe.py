from Case import Case
from Pile import Pile
from Dico_plus_grand import Dico_plus_grand
import random

class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.hauteur, self.largeur = largeur, hauteur
        self.laby = [[Case() for i in range(self.largeur)] for x in range(self.hauteur)]

    def directions_possibles(self,i,j):
        directions = []
        if 0 <= j < self.largeur-1 and not self.laby[i][j+1].vue: directions.append('S')
        if 1 <= j < self.largeur and not self.laby[i][j-1].vue: directions.append('N')
        if 1 <= i < self.hauteur and not self.laby[i-1][j].vue: directions.append('W')
        if 0 <= i < self.hauteur-1 and not self.laby[i+1][j].vue: directions.append('E')
        return directions

    def abattre_mur(self,i,j,dir,pile=False, veut_construire = False): # le False est pour quand on veut detruire un mur manuellement et pas pendant la generation du labyrinthe
        if dir == 'S': # on se dirige vers le sud
            self.laby[i][j].murS = veut_construire # on abat le mur sud de la case courante
            self.laby[i][j+1].murN = veut_construire # on abat le mur nord de la case situee en-dessous de la case courante
            self.laby[i][j+1].vue = True # cette case est alors marquee comme vue
            if pile: pile.empiler((i, j+1)) # on stocke les coordonnees de cette case dans la pile
        if dir == 'N':
            self.laby[i][j].murN = veut_construire  
            self.laby[i][j-1].murS = veut_construire  
            self.laby[i][j-1].vue = True 
            if pile: pile.empiler((i, j-1))  
        if dir == 'E':
            self.laby[i][j].murE = veut_construire  
            self.laby[i+1][j].murW = veut_construire 
            self.laby[i+1][j].vue = True 
            if pile: pile.empiler((i+1, j))  
        if dir == 'W':
            self.laby[i][j].murW = veut_construire  
            self.laby[i-1][j].murE = veut_construire  
            self.laby[i-1][j].vue = True 
            if pile: pile.empiler((i-1, j))  

    def generer(self):
        pile = Pile()
        i, j = random.randint(0, self.hauteur-1), random.randint(0, self.largeur-1)
        pile.empiler((i, j))
        self.laby[i][j].vue = True
        while not pile.est_vide():
            i, j = pile.sommet()
            directions = self.directions_possibles(i, j)
            pile.depiler() if len(directions) == 0 else self.abattre_mur(i, j, random.choice(directions), pile) 
        # destruction de x% de murs pour un labyrinthe plus ouvert
        for k in range(int(4*self.hauteur*self.largeur * 0.05)): 
            x, y = random.randint(2, self.hauteur-2), random.randint(2, self.largeur-2)
            direction = random.choice(["W", "E", "N", "S"])
            self.abattre_mur(x,y,direction,pile) 

        self.graphe = self.creer_un_graphe()    # enregistrer un dictionnaire d'adjacence avec la methode juste en-dessous

    def regenerer(self, largeur, hauteur):
        self.laby = [[Case() for i in range(largeur)] for x in range(hauteur)]
        self.generer()

    def creer_un_graphe(self):
        dico_adjacence = Dico_plus_grand(self.largeur, self.hauteur) # initialiser toutes les cases (i, j) sans voisins []
        for j in range(self.largeur):           # ajouter les cases voisines grace a la presence ou non des murs
            for i in range(self.hauteur):
                case = self.laby[i][j]
                if not case.murN and j > 0: dico_adjacence.ajouter((i, j), (i, j-1))
                if not case.murS and j < self.hauteur: dico_adjacence.ajouter((i, j), (i, j+1))
                if not case.murE and i < self.largeur: dico_adjacence.ajouter((i, j), (i+1, j))
                if not case.murW and i > 0: dico_adjacence.ajouter((i, j), (i-1, j))
        return dico_adjacence
    