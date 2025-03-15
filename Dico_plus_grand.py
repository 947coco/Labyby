class Dico_plus_grand():
    def __init__(self, largeur, hauteur):
        self.liste_de_dico = []


    def creer_dico(self):
        dico_adjacence = {(x, y): [] for x in range(self.largeur) for y in range(self.hauteur)} # initialiser toutes les cases (i, j) sans voisins []
        for i in range(self.largeur-1):           # ajouter les cases voisines grace a la presence ou non des murs
            for j in range(self.hauteur-1):
                case = self.laby[j][i]
                if not case.murN and j > 0: dico_adjacence[(i, j)].append((i, j-1))
                if not case.murS : dico_adjacence[(i, j)].append((i, j+1))
                if not case.murE : dico_adjacence[(i, j)].append((i+1, j))
                if not case.murW and i > 0: dico_adjacence[(i, j)].append((i-1, j))
        return dico_adjacence