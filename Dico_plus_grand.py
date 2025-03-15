class Dico_plus_grand():
    def __init__(self, largeur, hauteur):
        self.largeur, self.hauteur = largeur, hauteur
        self.liste_de_dico = [{} for x in range(hauteur)]

    def ajouter(self, cle, valeur):
        for dico in self.liste_de_dico:
            if len(dico) < self.largeur:
                if cle in dico : dico[cle].append(valeur)
                else : dico[cle] = [valeur]
                return True
        return False
    
    def voisin_de(self, cle):
        for dico in self.liste_de_dico:
            if cle in dico: return dico[cle]
        return []
    
    def retirer(self, cle, voisin):
        for dico in self.liste_de_dico:
            if cle in dico and voisin in dico[cle]:
                dico[cle].remove(voisin)
                return True
        return False               


    