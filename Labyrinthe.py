import pygame, codecs, random, time, sys

""" Ne mettez aucun accent sinon ça affihce de mauvais caractères"""

# definition des couleurs primaires/principales
white, black          = (255, 255, 255), (0, 0, 0)
red, green, blue      = (255, 0, 0), (0, 255, 0), (0, 0, 255)
yellow, cyan, magenta = (255, 255, 0), (0, 255, 255), (255, 0, 255)
orange, purple, pink  = (255, 165, 0), (128, 0, 128), (233, 40, 99)

class File:
    def __init__(self): self.contenu=[]
    def est_vide(self): return self.contenu==[]
    def enfiler(self,x): self.contenu.append(x)
    def taille(self): return len(self.contenu)
    def present(self,x): return x in self.contenu
    def defiler(self):
        assert not self.est_vide(),"File vide !"
        return self.contenu.pop(0)   #ou del self.file[-1]
    def sommet(self):
        assert not self.est_vide(),"File vide !"
        return self.contenu[0]
    
class Pile:
    def __init__(self):     self.contenu=[]
    def est_vide(self):     return self.contenu==[]
    def empiler(self,x):    self.contenu.append(x)
    def depiler(self):      return self.contenu.pop() if not self.est_vide() else print("Pile vide !")
    def taille(self):       return len(self.contenu)
    def sommet(self):       return self.contenu[-1] if not self.est_vide() else print("Pile vide !")

class Case: 
    def __init__(self):  self.murN, self.murS, self.murE, self.murW, self.vue = True, True, True, True, False
    def assigner_coordonnees(self, x1, y1, x2, y2): self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

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
            directions = self.directions_possibles(i, j)
            pile.depiler() if len(directions) == 0 else self.__abattre_mur(i, j, random.choice(directions), pile)
        # destruction de quelques murs pour un labyrinthe plus ouvert
        for k in range(int(4*self.hauteur*self.largeur * 0.12)): # Supprime environ x% des murs du labyrinthe parfait
            x, y = random.randint(2, self.hauteur-2), random.randint(2, self.largeur-2)
            direction = random.choice(["W", "E", "N", "S"])
            self.__abattre_mur(x,y,direction,pile) 

        self.graphe = self.creer_un_graphe()    

    def creer_un_graphe(self):
        # initialiser toutes les cases (i, j) sans voisins [] pour l'instant
        dico_adjacence = {(i, j): [] for i in range(self.largeur) for j in range(self.hauteur)}
        # ajouter les cases voisines grace a la methode directions possibles
        for i in range(self.largeur):
            for j in range(self.hauteur):
                case = self.laby[j][i]
                if case.murN : dico_adjacence[i, j].append((i, j-1))
                if case.murS : dico_adjacence[i, j].append((i, j+1))
                if case.murE : dico_adjacence[i, j].append((i+1, j))
                if case.murW : dico_adjacence[i, j].append((i-1, j))
        return dico_adjacence

""" 
Quand on aura fini, il faudra separer les classes dans des fichiers distincts pour que ce soit plus clean
mais pour l'instant, c'est plus pratique d'avoir la classe Labyrinthe a porter.
Et ducoup il faudra faire des importations : import Labyrinthe from Labyrinthe par exemple
"""

class Joueur():
    def __init__(self, vitesse, coordonee_x, coordonee_y, direction_vue, largeur, hauteur, chemin_image, 
                 chemin_image_transparence, nb_flash, nb_leurre, cooldown_transparence):
        self.vitesse = vitesse
        self.image = pygame.image.load(chemin_image).convert()
        self.image_transparence = pygame.image.load(chemin_image).convert_alpha()
        for y in range(self.image_transparence.get_height()):
            for x in range(self.image_transparence.get_width()):
                r, g, b, a = self.image_transparence.get_at((x, y))
                self.image_transparence.set_at((x, y), (r, g, b, 160)) # 0 = invisible, 255 = visible
        self.cooldown_transparence = cooldown_transparence
        self.nb_flash, self.nb_leurre = nb_flash, nb_leurre 
        self.coordonee_x, self.coordonee_y = coordonee_x, coordonee_y # coordonnes sur l'ecran
        self.case_i, self.case_j = 0,0 # Sur quelle case se trouve le joueur
        self.largeur, self.hauteur = largeur, hauteur # dimensions de l'image representant le joueur
        self.direction_vue = direction_vue # direction du regard du joueur
        

    def deplacer(self, touche_pressee, longeur_saut_x, longeur_saut_y):
        if touche_pressee == "z" : 
            self.direction_vue = "N" # diriger le regard du joueur
            self.coordonee_y -= self.vitesse/longeur_saut_y # deplacer le joueur
        if touche_pressee == "q" : 
            self.direction_vue = "W"
            self.coordonee_x -= self.vitesse/longeur_saut_x
        if touche_pressee == "s" : 
            self.direction_vue = "S"
            self.coordonee_y += self.vitesse/longeur_saut_y
        if touche_pressee == "d" : 
            self.direction_vue = "E"
            self.coordonee_x += self.vitesse/longeur_saut_x

    def devient_transparent(self):
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

    def distance_entre_2_cases(self, depart, arrivee):
        # renvoie un seul nombre representant une distance au point d'arrivee
        i1, j1 = depart
        i2, j2 = arrivee
        return (i2-i1) + (j2-j1)
    
    # Basee sur la seance C39 bfs_iteratif mais tres modifiee
    def chemin_depart_a_arrivee(self, graphe, depart, arrivee):
        """graphe = dictionnaire d'adjacence, depart et arrivee = tuples de coordonnees de cases"""
        chemin_plus_court = [] # chemin final le plus court possible
        case_plus_rapprochee = [] # liste temporaire afin de comparer laquelle des cases voisines se rapproche plus du joueur (10 lignes plus bas)
        f = File()
        f.enfiler(depart)
        while not f.est_vide():
            tmp = f.defiler()
            if tmp not in chemin_plus_court:
                chemin_plus_court.append(tmp)
            if tmp == arrivee : return chemin_plus_court # ajout de la condition de rencontre avec la case d'arrivee
            for voisin in graphe[tmp]:
                # on enregistre les distances moyennes des differents voisins de la case dans la liste case_plus_rapprochee
                case_plus_rapprochee.append(self.distance_entre_2_cases(voisin, arrivee)) 
            while case_plus_rapprochee != []:
                # on identifie la distance minimum parmis les voisins -> on choisi la case correspondante
                distance_minimum = min(case_plus_rapprochee)
                meilleur_case = graphe[tmp][distance_minimum.index()]
                if meilleur_case in chemin_plus_court or f.present(meilleur_case):
                    # si la case est deja dans la file ou le chemin, on la supprime (et le while recommence)
                    case_plus_rapprochee.remove(distance_minimum) 
                else :
                    # si cette case n'est pas deja dans la file et pas dans le chemin, on l'ajoute au chemin
                    chemin_plus_court.append(meilleur_case)
                    # on efface la liste temporaire pour une nouvelle utilisation
                    case_plus_rapprochee = []


class Projectile(): # Flash, leurre... (tout ce qui est jetable)
    def __init__(self, vitesse, chemin_image, quantitee):
        self.vitesse = vitesse
        self.chemin_image = chemin_image
        self.quantitee = quantitee
        

    def lancement(self, direction_du_lance, position_joueur_x, position_joueur_y):

        pass

class Jeux():
    def __init__(self, couleur, titre, fenetre_principale, fenetre_existant_w=0, fenetre_existant_h=0):
        """
        creer une fenetre avec un titre, une couleur de fond et verifie si une fenetre principale
        a deja ete creer, dans ce cas, on creer une fenetre pop up plus petit au dessus de la principale 
        (exemple : fenetre de pause, d'acceuil...)
        """
        self.joueur = None
        self.labels = [] # bdd afin d'afficher tout les labels
        self.clock = pygame.time.Clock()
        pygame.init()
        if fenetre_principale : # 1ère fenetre en plein ecran
            self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else : # Cas ou l'on veut creer une fenetre secondaire
            largeur, hauteur = self.unite_relatif(fenetre_existant_w, fenetre_existant_h)
            self.fenetre = pygame.display.set_mode((largeur, hauteur))
        self.fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
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

    def afficher_ligne(self, x1, y1, x2, y2, epaisseur, couleur):  pygame.draw.line(self.fenetre, couleur, (x1, y1), (x2, y2), epaisseur)
        

    def creer_label(self, coordonnee_x, coordonnee_y, largeur, hauteur, couleur, description):
        # creer un label de coordonees x, y et de taille largeur x hauteur
        w, h = self.unite_relatif(largeur, hauteur) 
        x, y = self.unite_relatif(coordonnee_x, coordonnee_y) 
        label = pygame.surface.Surface((w, h))
        label.fill(couleur)
        self.labels.append([label, x, y, description, w, h])
        
    def afficher_label(self): [self.fenetre.blit(sous_liste[0], (sous_liste[1], sous_liste[2])) for sous_liste in self.labels]

    def creer_labyrinthe(self, largeur, hauteur, marge_x, marge_y, longeur_mur, epaisseur_mur, couleur):
        # esthetique du labyrinthe en rapport à l'affichage du labyrinthe avec pygame 
        self.long_mur_x, self.long_mur_y = self.unite_relatif(longeur_mur, longeur_mur)
        self.epaisseur_mur, pas_important  = self.unite_relatif(epaisseur_mur, 0) 
        self.marge_x, self.marge_y = self.unite_relatif(marge_x, marge_y)
        self.couleur_labyrinthe = couleur
        # utilisation de la classe labyrinthe
        self.labyrinthe = Labyrinthe(largeur, hauteur)
        self.labyrinthe.generer()

    def afficher_labyrinthe(self):
        """
        Fonction pour afficher le labyrinthe. Explication :
        les coordonnees sont un melange de: 
        - la marge prise en compte (pour pouvoir espacer notre labyrinthe des bords)
        - la longeur du trait / mur
        - les coordonees de i et j pour les differentes cases
        """
        for i in range(len(self.labyrinthe.laby)):
            for j in range(len(self.labyrinthe.laby[i])):
                x1, y1 = self.unite_relatif(i*2, j*2) # coordonnees i et j
                x1 += self.marge_x # ajout des marges
                y1 += self.marge_y
                x2, y2 = x1+self.long_mur_x, y1+self.long_mur_y 
                case = self.labyrinthe.laby[i][j]
                case.assigner_coordonnees(x1, y1, x2, y2)
                if case.murS: self.afficher_ligne(x1, y2, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murW: self.afficher_ligne(x1, y1, x1, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murN: self.afficher_ligne(x1, y1, x2, y1, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murE: self.afficher_ligne(x2, y1, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)

    def creer_joueur(self, coord_case_x, coord_case_y, direction, vitesse, nb_flash, nb_leurre, cooldown_transparence):
        case = self.labyrinthe.laby[coord_case_x][coord_case_y]
        self.joueur = Joueur(vitesse, case.x1, case.y1, direction, self.long_mur_x*0.6, self.long_mur_y*0.6, 
                             "./Logo_joueur.png", "./Logo_joueur.png", nb_flash, nb_leurre, cooldown_transparence)

    def afficher_joueur(self):
        image =  pygame.transform.scale(self.joueur.image, (self.joueur.largeur, self.joueur.hauteur))  
        self.fenetre.blit(image, (self.joueur.coordonee_x-self.joueur.largeur*0.4, self.joueur.coordonee_y-self.joueur.hauteur*0.4))

    def verifier_deplacement(self, touche_pressee):
        case = self.labyrinthe.laby[self.joueur.case_i][self.joueur.case_j]
        i, j = self.joueur.case_i, self.joueur.case_j

        if touche_pressee == "z" and case.y1>self.joueur.coordonee_y-self.joueur.hauteur/2: 
            if case.murN: self.joueur.coordonee_y = case.y1+self.joueur.hauteur/1.9 # Si il y a un mur, on repousse le joueur
            elif case.y1>self.joueur.coordonee_y: self.joueur.case_j -= 1 # si le centre du modele du joueur a depasser la ligne, on le change de case

        if touche_pressee == "q" and case.x1>self.joueur.coordonee_x-self.joueur.largeur/2: 
            if case.murW : self.joueur.coordonee_x = case.x1+self.joueur.hauteur/1.9
            elif case.x1>self.joueur.coordonee_x: self.joueur.case_i -= 1

        if touche_pressee == "s" and case.y2<self.joueur.coordonee_y+self.joueur.hauteur/2: 
            if case.murS : self.joueur.coordonee_y = case.y2-self.joueur.hauteur/1.9
            elif case.y2<self.joueur.coordonee_y : self.joueur.case_j += 1

        if touche_pressee == "d" and case.x2<self.joueur.coordonee_x+self.joueur.largeur/2: 
            if case.murE : self.joueur.coordonee_x = case.x2-self.joueur.hauteur/1.9
            elif case.x2<self.joueur.coordonee_x : self.joueur.case_i += 1

        self.joueur.deplacer(touche_pressee, self.long_mur_x, self.long_mur_y)
        
    def boucle_jeu(self):
        while True :
            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    # Bouton exit
                    for label in self.labels:
                        # si le bouton est quitter et coordonnee_x < x_souris < coordonnee_x+largeur  et coordonnee_y < y_souris < coordonnee_y+hauteur
                        if label[3] == "quitter" and label[1] < evenement.pos[0] < label[1]+label[4] and label[2] < evenement.pos[1] < label[2]+label[5]:
                            pygame.quit() # on detruit la fenetre pygame
                            sys.exit() # on termine le processus correctement
                
                # Verifier si une touche est enfoncee
                if evenement.type == pygame.KEYDOWN:  
                    if evenement.key == pygame.K_LSHIFT: # rester appuyer sur maj/shift
                        self.joueur.vitesse *= 2 # courir

                 # Verifier si une touche est relachee
                if evenement.type == pygame.KEYUP:
                    if evenement.key == pygame.K_LSHIFT: # relacher maj/shift
                        self.joueur.vitesse /= 2 # ne plus courir
            keys = pygame.key.get_pressed()

            # On aurait pu les detecter dans un KEYDOWN mais ca marche nickel sans donc on change rien
            if keys[pygame.K_z]: self.verifier_deplacement("z")
            if keys[pygame.K_q]: self.verifier_deplacement("q")
            if keys[pygame.K_s]: self.verifier_deplacement("s")
            if keys[pygame.K_d]: self.verifier_deplacement("d")
            

            # simuler des appuie de touches constament afin de bien repousser le joueur au contact du "coin bugge"
            self.verifier_deplacement("z")
            self.verifier_deplacement("q")
            self.verifier_deplacement("s")
            self.verifier_deplacement("d")

            self.fenetre.fill(black) # Tout effacer

            # Tout charger
            self.afficher_labyrinthe()
            self.afficher_joueur()
            self.afficher_label()
            pygame.display.flip() # tout réafficher

            self.clock.tick(60)  # limites les FPS a 60


if __name__ == "__main__":
    jeu = Jeux(black, "titre1", True)
    jeu.creer_labyrinthe(30, 20, 6, 6, 2, 0.2, cyan)
    jeu.creer_labyrinthe(10, 5, 6, 6, 2, 0.2, red) 
    jeu.afficher_labyrinthe()
    jeu.creer_label(96, 0, 6, 4, red, "quitter")
    jeu.creer_joueur(0,0, "S", 30, 1, 1, 1)
    jeu.boucle_jeu()