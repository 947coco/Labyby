import random

class Changer_Niveau():
    def __init__(self, numero, labyrinthe, joueur, liste_ennemies, liste_pieces, long_mur):
        self.niveau = 0
        self.numero, self.labyrinthe, self.joueur = numero, labyrinthe, joueur
        self.liste_ennemies, self.liste_pieces, self.long_mur = liste_ennemies, liste_pieces, long_mur   
        self.charger_niveau(0)


    def caracteristiques_niveau(self, largeur_laby, hauteur_laby, vitesse_ennemies, largeur_ennemies, hauteur_ennemies, 
                                nb_grenade, nb_tire, nb_construction, nb_destruciton, nb_pieces, nb_ennemies, 
                                case_joueur=(0, 0)):

        self.labyrinthe.regenerer(largeur_laby, hauteur_laby)
        largeur_ennemie, hauteur_ennemie = self.long_mur*largeur_ennemies, self.long_mur*hauteur_ennemies
        chemin_image = "yt.png"
        self.liste_ennemies, self.liste_pieces = [], []
        vitesse_relative, peut_importe = self.unite_relatif(vitesse_ennemies, 0)
        self.joueur.nb_grenade, self.joueur.nb_tire = nb_grenade, nb_tire
        self.joueur.nb_construction, self.joueur.nb_destruction = nb_construction, nb_destruciton
        self.joueur.nb_pieces_a_recup = nb_pieces
        self.joueur.case_i, self.joueur.case_j = case_joueur[0], case_joueur[1]
        case_joueur = self.labyrinthe.laby[self.joueur.case_i][self.joueur.case_j]
        for x in range(nb_ennemies):
            i, j = random.randint(0, self.labyrinthe.largeur-1), random.randint(0, self.labyrinthe.hauteur-1)
            case = self.labyrinthe.laby[i][j]
            #self.liste_ennemies.append(Joueur(vitesse_relative, case.milieu_x, case.milieu_y, i, j, "N",
                                     #  largeur_ennemie, hauteur_ennemie, chemin_image, 0, 0, 0, 0, 0, 
                                      # False, self.labyrinthe, self.joueur))



    def charger_niveau(self, numero):
        if numero == 0: self.caracteristiques_niveau(15, 15, 0.5, 0.4, 0.4, 10, 100, 10, 10, 3, 1,  (0, 0)) # tuto sympa
        if numero == 1: self.caracteristiques_niveau(20, 20, 1, 0.5, 0.5, 7, 40, 4, 2, 8, 12,(10, 10))
        if numero == 2: self.caracteristiques_niveau(30, 20, 3, 0.7, 0.7, 5, 70, 4, 7, 12, 15,   (30, 20))
        if numero == 3: self.caracteristiques_niveau(40, 20, 2, 0.8, 0.8, 15, 30, 5, 5, 20, 40,   (40, 19))
        if numero == 4: self.caracteristiques_niveau(10, 10, 5, 1, 1, 4, 15, 0, 0, 3, 20,   (0, 0))
