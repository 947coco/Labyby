import pygame, codecs, random, time, sys

""" Ne mettez aucun accent sinon ça affiche de mauvais caractères. 
Quand on aura fini, il faudra separer les classes dans des fichiers distincts pour que ce soit plus clean
mais pour l'instant, c'est plus pratique d'avoir la classe Labyrinthe a porter.
Et ducoup il faudra faire des importations : import Labyrinthe from Labyrinthe par exemple
"""

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
    def __init__(self):  
        self.murN, self.murS, self.murE, self.murW, self.vue = True, True, True, True, False
    def assigner_coordonnees(self, x1, y1, x2, y2): 
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.milieu_x, self.milieu_y = x1+(x2-x1)/2, y1+(y2-y1)/2

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

    def abattre_mur(self,i,j,dir,pile=False): # le False est pour quand on veut detruire un mur manuellement et pas pendant la generation du labyrinthe
        if dir == 'S': # on se dirige vers le sud
            self.laby[i][j].murS = False # on abat le mur sud de la case courante
            self.laby[i][j+1].murN = False # on abat le mur nord de la case situee en-dessous de la case courante
            self.laby[i][j+1].vue = True # cette case est alors marquee comme vue
            if pile: pile.empiler((i, j+1)) # on stocke les coordonnees de cette case dans la pile
        if dir == 'N':
            self.laby[i][j].murN = False  
            self.laby[i][j-1].murS = False  
            self.laby[i][j-1].vue = True 
            if pile: pile.empiler((i, j-1))  
        if dir == 'E':
            self.laby[i][j].murE = False  
            self.laby[i+1][j].murW = False 
            self.laby[i+1][j].vue = True 
            if pile: pile.empiler((i+1, j))  
        if dir == 'W':
            self.laby[i][j].murW = False  
            self.laby[i-1][j].murE = False  
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
        for k in range(int(4*self.hauteur*self.largeur * 0.12)): 
            x, y = random.randint(2, self.hauteur-2), random.randint(2, self.largeur-2)
            direction = random.choice(["W", "E", "N", "S"])
            self.abattre_mur(x,y,direction,pile) 

        self.graphe = self.creer_un_graphe()    # enregistrer un dictionnaire d'adjacence avec la methode juste en-dessous

    def creer_un_graphe(self):
        dico_adjacence = {(x, y): [] for x in range(self.largeur) for y in range(self.hauteur)} # initialiser toutes les cases (i, j) sans voisins []
        for i in range(self.largeur):           # ajouter les cases voisines grace a la presence ou non des murs
            for j in range(self.hauteur):
                case = self.laby[j][i]
                if case.murN : dico_adjacence[i, j].append((i, j-1))
                if case.murS : dico_adjacence[i, j].append((i, j+1))
                if case.murE : dico_adjacence[i, j].append((i+1, j))
                if case.murW : dico_adjacence[i, j].append((i-1, j))
        return dico_adjacence
    


class Joueur():
    def __init__(self, vitesse, coord_x, coord_y, case_i, case_j, direction, largeur, hauteur, chemin_image, nb_flash, nb_leurre):
        # differentes images pour diriger le modele du joueur en fonction de la direction du regard
        self.image_droite = pygame.image.load(chemin_image).convert_alpha()
        self.image_gauche = pygame.transform.flip(self.image_droite, True, False)
        self.image_haut = pygame.transform.rotate(self.image_droite, 90)
        self.image_bas = pygame.transform.flip(self.image_haut, False, True)
        self.image_afficher = self.image_droite
        # coordonnes relative du joueur
        self.coord_x, self.coord_y = coord_x, coord_y # coordonnes du milieu de la hitbox
        self.case_i, self.case_j = case_i, case_j# Sur quelle case se trouve le joueur
        self.largeur, self.hauteur = largeur, hauteur # dimensions de l'image representant le joueur
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        # Autres
        self.vitesse = vitesse
        self.veut_detruire = False
        self.nb_flash, self.nb_leurre = nb_flash, nb_leurre 
        self.direction = direction # direction du regard du joueur
        self.pieces_possedee = 0
        self.pieces_a_recup = 9999
        self.mettre_a_jour_hitbox()

    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox

    def deplacer(self, touche_pressee, longeur_saut_x, longeur_saut_y):
        # deplacer le joueur en fonction de sa vitesse et de la touche appuiee
        if touche_pressee == "z" : self.coord_y -= self.vitesse/longeur_saut_y 
        if touche_pressee == "q" : self.coord_x -= self.vitesse/longeur_saut_x
        if touche_pressee == "d" : self.coord_x += self.vitesse/longeur_saut_x
        if touche_pressee == "s" : self.coord_y += self.vitesse/longeur_saut_y
        self.mettre_a_jour_hitbox()
        
    def jete_flash(self):
        pass
    def jete_leurre(self):
        pass
    def controle_ennemie(self):
        pass
    def boost_vitesse(self):
        pass


class Ennemie():
    def __init__(self, vitesse, chemin_image, x, y, case_i, case_j, largeur, hauteur, labyrinthe, long_mur):
        self.vitesse = vitesse
        self.chemin_image = pygame.image.load(chemin_image).convert_alpha()
        self.x1, self.y1, self.x2, self.y2 = x, y, x+largeur, y+hauteur
        case = labyrinthe.laby[case_i][case_j]
        self.coord_x, self.coord_y = case.x1+long_mur*0.5, case.y1+long_mur*0.5
        self.case_i, self.case_j = case_i, case_j
        self.largeur, self.hauteur = largeur, hauteur
        self.suite_i, self.suite_j = (0, 0)

    def deplacer(self, longeur_saut, labyrinthe, joueur):
        self.suite_i, self.suite_j = self.prochaine_case_a_prendre(labyrinthe.graphe, joueur.case_i, joueur.case_j)
        case_prochaine = labyrinthe.laby[self.suite_i][self.suite_j]
        if case_prochaine.x1 < self.coord_x < case_prochaine.x2 and case_prochaine.y1 < self.coord_y < case_prochaine.y2 :
                self.suite_i, self.suite_j = self.prochaine_case_a_prendre(labyrinthe.graphe, joueur.case_i, joueur.case_j)
        self.coord_x += (case_prochaine.milieu_x-self.coord_x)# *(self.vitesse/longeur_saut) 
        self.coord_y += (case_prochaine.milieu_y-self.coord_y)#*(self.vitesse/longeur_saut) 
        self.mettre_a_jour_hitbox()

    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox


    def mettre_a_jour_case(self, case):
        if self.coord_x < case.x1 : self.case_i -= 1
        if self.coord_x > case.x2: self.case_i += 1
        if self.coord_y < case.y1 : self.case_j -= 1
        if self.coord_y > case.y2: self.case_j += 1

    def distance(self, depart, arrivee):
        # Sert a savoir si la case depart se rapproche de la case arriver (voir methode en-dessous)
        i1, j1 = depart
        i2, j2 = arrivee
        return (i2-i1) + (j2-j1)
    
    def prochaine_case_a_prendre(self, graphe, joueur_i, joueur_j):
        voisins = graphe[(self.case_i, self.case_j)]
        distance_min = 99999
        meilleur_case = voisins[0]
        for index, case in enumerate(voisins):
            distance_case = self.distance((self.case_i, self.case_j), (joueur_i, joueur_j))
            if distance_case < distance_min and len(graphe[case]) > 1 : 
                distance_min = distance_case
                meilleur_case = case
        return meilleur_case
        
    # Basee sur la seance C39 bfs_iteratif mais tres modifiee
    def chemin_depart_a_arrivee(self, graphe, depart, arrivee):
        # graphe = dictionnaire d'adjacence, depart et arrivee = tuples de coordonnees de cases
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
                distance_minimum = min(case_plus_rapprochee) # on identifie la distance minimum parmis les voisins -> on choisi la case correspondante
                meilleur_case = graphe[tmp][distance_minimum.index()]
                if meilleur_case in chemin_plus_court or f.present(meilleur_case):
                    case_plus_rapprochee.remove(distance_minimum)  # si la case est deja dans la file ou le chemin, on la supprime (et le while recommence)
                else :
                    chemin_plus_court.append(meilleur_case) # si cette case n'est pas deja dans la file et pas dans le chemin, on l'ajoute au chemin
                    case_plus_rapprochee = [] # on efface la liste temporaire pour une nouvelle utilisation
            else : print("erreur dans la comparaison des cases voisines")


class Projectile(): # Flash, leurre... (tout ce qui est jetable)
    def __init__(self, vitesse, chemin_image, fichier_son, type, largeur, hauteur, joueur, labyrinthe, distance_nb_case):
        self.vitesse = vitesse
        self.chemin_image = chemin_image
        self.fichier_son = fichier_son
        self.type = type 
        self.largeur, self.hauteur = largeur, hauteur
        self.case_i, self.case_j = joueur.case_i, joueur.case_j
        self.direction = joueur.direction_vue
        self.coord_x, self.coord_y= joueur.coord_x, joueur.coord_y
        self.x_init, self.y_init = joueur.coord_x, joueur.coord_y
        if self.direction == "N": self.case_arret = labyrinthe.laby[joueur.case_j-distance_nb_case][joueur.case_i]
        if self.direction == "S": self.case_arret = labyrinthe.laby[joueur.case_j+distance_nb_case][joueur.case_i]
        if self.direction == "E": self.case_arret = labyrinthe.laby[joueur.case_j][joueur.case_i+distance_nb_case]
        if self.direction == "W": self.case_arret = labyrinthe.laby[joueur.case_j][joueur.case_i-distance_nb_case]
        self.mettre_a_jour_hitbox()
        self.doit_etre_supprimer = False

    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox

    def mettre_a_jour_case(self, case):
        if self.coord_x < case.x1 : self.case_i -= 1
        if self.coord_x > case.x2: self.case_i += 1
        if self.coord_y < case.y1 : self.case_j -= 1
        if self.coord_y > case.y2: self.case_j += 1

    def lancer(self, labyrinthe):
        case = labyrinthe.laby[self.case_i][self.case_j]
        collision_mur = {"N": self.coord_y<case.y1, "S": self.coord_y>case.y2, "E": self.coord_x>case.x2, "W": self.coord_x<case.x1}
        self.mettre_a_jour_hitbox()
        self.mettre_a_jour_case(case)
        if (self.case_arret.x1 < self.coord_x < self.case_arret.x2 and self.case_arret.y1 < self.coord_y < self.case_arret.y2) or collision_mur[self.direction]:
            self.explose() # si le projectile arrive a la case maximale ou se heurte a un mur, il explose
            self.debut = time.time() # pour calculer le temps avant la suppression du projectile a l'ecran
        else : 
            self.avance(labyrinthe.long_mur) 

    def avance(self, longueur_mur):
        if self.direction == "N": self.coord_y -= self.vitesse/longueur_mur
        if self.direction == "S": self.coord_y += self.vitesse/longueur_mur
        if self.direction == "E": self.coord_x += self.vitesse/longueur_mur
        if self.direction == "W": self.coord_x -= self.vitesse/longueur_mur

    def explose(self):
        self.largeur *= 1.1
        self.hauteur *= 1.1
        if time.time() - self.debut > 2:  # si l'explosion a duree plus de 2 secondes
            pygame.mixer.Sound(self.fichier_son).play()
            self.produit_effet()
            self.doit_etre_supprimer = True


    def produit_effet(self):
        # produire l'effet voulu selon le type de projectile (grenade, flash, leurre...)
        pass
class Piece():
    def __init__(self, chemin_image, largeur_image, hauteur_image, x, y):
        chargement_image = pygame.image.load(chemin_image).convert_alpha()
        self.image = pygame.transform.scale(chargement_image, (largeur_image, hauteur_image))  
        self.x1, self.y1, self.x2, self.y2 = x, y, x+largeur_image, y+hauteur_image

class Jeux():
    def __init__(self, couleur, titre):
        #creer une fenetre avec un titre et une couleur de fond 
        self.joueur = None
        self.labels = [] # bdd afin d'afficher tout les labels
        self.pieces = [] # bdd afin d'afficher toutes les pieces
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.mixer.init()
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
        #self.icon = pygame.image.load('logo.png')
        #pygame.display.set_icon(self.icon)
        
        
    def creer_pieces(self, nb_pieces, chemin_image, labyrinthe, joueur, longeur_mur):
        joueur.pieces_a_recup = nb_pieces
        for piece in range(nb_pieces):
            i, j = joueur.case_i, joueur.case_j
            while i == joueur.case_i and j == joueur.case_j:
                i, j = random.randint(0, labyrinthe.largeur-1), random.randint(0, labyrinthe.hauteur-1)
            case = labyrinthe.laby[j][i]
            piece = Piece(chemin_image, longeur_mur*0.5, longeur_mur*0.5, case.x1+longeur_mur*0.2, case.y1+longeur_mur*0.2)
            self.pieces.append(piece)

    
    def afficher_pieces(self):
        if self.pieces != []: 
            [self.fenetre.blit(piece.image, (piece.x1, piece.y1)) for piece in self.pieces]

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
    def unite_relatif(self, X, Y): return int(pygame.display.Info().current_w*X*0.01), int(pygame.display.Info().current_h *Y*0.0177777777) 

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
        self.long_mur, self.epaisseur_mur = self.unite_relatif(longeur_mur, epaisseur_mur)
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
                x2, y2 = x1+self.long_mur, y1+self.long_mur 
                case = self.labyrinthe.laby[i][j]
                case.assigner_coordonnees(x1, y1, x2, y2)
                if case.murS: self.afficher_ligne(x1, y2, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murW: self.afficher_ligne(x1, y1, x1, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murN: self.afficher_ligne(x1, y1, x2, y1, self.epaisseur_mur, self.couleur_labyrinthe)
                if case.murE: self.afficher_ligne(x2, y1, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)

    def creer_joueur(self, case_i, case_j, direction, vitesse, nb_flash, nb_leurre):
        case = self.labyrinthe.laby[case_i][case_j]
        vitesse_relative, peut_importe = self.unite_relatif(vitesse, 0)
        espacement = self.long_mur*0.3
        self.joueur = Joueur(vitesse_relative, case.x1+espacement, case.y1+espacement, case_i, case_j, direction, self.long_mur*0.6, self.long_mur*0.7, 
                             "./Logo_joueur.png", nb_flash, nb_leurre)

    def afficher_joueur(self):
        direction = self.tourner_modele(self.joueur)
        image =  pygame.transform.scale(self.joueur.image_afficher, (self.joueur.largeur, self.joueur.hauteur))  
        self.fenetre.blit(image, (self.joueur.x1, self.joueur.y1))

    def creer_ennemie(self, vitesse, chemin_image, i, j):
        case = self.labyrinthe.laby[i][j]
        vitesse_relative, peut_importe = self.unite_relatif(vitesse, 0)
        self.ennemie = Ennemie(vitesse, chemin_image, case.x1+self.long_mur*0.3, case.y1+self.long_mur*0.3, i, j, self.long_mur*0.6, self.long_mur*0.6, self.labyrinthe, self.long_mur)

    
    def afficher_ennemie(self,ennemie):
        image =  pygame.transform.scale(ennemie.chemin_image, (ennemie.largeur, ennemie.hauteur)) 
        self.fenetre.blit(image, (ennemie.x1, ennemie.y1))

    def tourner_modele(self, personnage): 
        if personnage.direction == "W": personnage.image_afficher = personnage.image_gauche
        if personnage.direction == "E": personnage.image_afficher = personnage.image_droite
        if personnage.direction == "N": personnage.image_afficher = personnage.image_haut
        if personnage.direction == "S": personnage.image_afficher = personnage.image_bas 
        
    def tourner_regard(self, touche_pressee, personnage):
        if touche_pressee == "z" : personnage.direction = "N"
        if touche_pressee == "s" : personnage.direction = "S"
        if touche_pressee == "d" : personnage.direction = "E"
        if touche_pressee == "q" : personnage.direction = "W"

    def changement_de_case(self, personnage):
        case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
        if personnage.coord_x < case.x1 : personnage.case_i -= 1
        if personnage.coord_x > case.x2: personnage.case_i += 1
        if personnage.coord_y < case.y1 : personnage.case_j -= 1
        if personnage.coord_y > case.y2: personnage.case_j += 1

    def collision_mur(self, personnage):
        case = case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
        if case.y1>personnage.y1 and case.murN : personnage.coord_y = case.y1+personnage.hauteur/2
        if case.x1>personnage.x1 and case.murW : personnage.coord_x = case.x1+personnage.largeur/2
        if case.y2<personnage.y2 and case.murS : personnage.coord_y = case.y2-personnage.hauteur/2
        if case.x2<personnage.x2 and case.murE : personnage.coord_x = case.x2-personnage.largeur/2

    def collision_ennemie(self):
        if self.ennemie.y2 > self.joueur.y1 or self.ennemie.y1 < self.joueur.y2: # si il y 
            if self.ennemie.x1<self.joueur.x2 or self.ennemie.x2>self.joueur.x1:
                self.personnage_meurt(self.joueur)

    def collision_piece(self):
        for piece in self.pieces:
            if piece.x1 < self.joueur.coord_x < piece.x2 and piece.y1 < self.joueur.coord_y < piece.y2:
                piece.recoltee = True
                self.joueur.pieces_possedee += 1
                self.pieces.remove(piece)

    def personnage_meurt(self, personnage): 
        print("le joueur est mort")

    def verifier_deplacement(self, touche_pressee): 
        """Tourner le regard du joueur, verifier si il y a une collision (mur ou ennemie), verifier si il a changer de case, le deplacer"""
        self.collision_ennemie()
        self.collision_piece()        
        self.collision_mur(self.joueur)
        self.tourner_regard(touche_pressee, self.joueur)
        self.changement_de_case(self.joueur)
        self.joueur.deplacer(touche_pressee, self.long_mur, self.long_mur)
        
    def si_joueur_veut_detruire(self, a_clique = False, couleur = white):
        if self.joueur.veut_detruire : 
            case = self.labyrinthe.laby[self.joueur.case_i][self.joueur.case_j]
            if self.joueur.direction == "S" and case.murS and self.joueur.case_j < self.labyrinthe.largeur-1:
                if a_clique : self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "S") # si il a cliquer, on detruit le mur
                else :        self.afficher_ligne(case.x1, case.y2, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur) # sinon on affiche le mur de couleur "couleur"
                
            if self.joueur.direction == "N" and case.murN and self.joueur.case_j > 0 :
                if a_clique : self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "N")
                else :        self.afficher_ligne(case.x1, case.y1, case.x2, case.y1, int(self.epaisseur_mur*1.33), couleur)

            if self.joueur.direction == "E" and case.murE and self.joueur.case_i < self.labyrinthe.hauteur-1:
                if a_clique : self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "E") 
                else :        self.afficher_ligne(case.x2, case.y1, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur)

            if self.joueur.direction == "W" and case.murW and self.joueur.case_i > 0:
                if a_clique : self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "W")
                else :        self.afficher_ligne(case.x1, case.y1, case.x1, case.y2, int(self.epaisseur_mur*1.33), couleur)

    def verifications_touches_calvier_appuiees(self):
        touche_clavier = pygame.key.get_pressed()
        # On aurait pu les detecter dans un KEYDOWN mais ca marche nickel donc on change rien
        if touche_clavier[pygame.K_z]: self.verifier_deplacement("z")
        if touche_clavier[pygame.K_q]: self.verifier_deplacement("q")
        if touche_clavier[pygame.K_s]: self.verifier_deplacement("s")
        if touche_clavier[pygame.K_d]: self.verifier_deplacement("d")
 
    def verifications_autres_touches(self):
        for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    # Bouton exit
                    for label in self.labels:
                        # si le bouton est quitter et coordonnee_x < x_souris < coordonnee_x+largeur  et coordonnee_y < y_souris < coordonnee_y+hauteur
                        if label[3] == "quitter" and label[1] < evenement.pos[0] < label[1]+label[4] and label[2] < evenement.pos[1] < label[2]+label[5]:
                            pygame.quit() # on detruit la fenetre pygame
                            sys.exit() # on termine le processus correctement
                    if self.joueur.veut_detruire : self.si_joueur_veut_detruire(True) 
                

                
               
                if evenement.type == pygame.KEYDOWN:    # Verifier si une touche est enfoncee 
                    if evenement.key == pygame.K_LSHIFT: self.joueur.vitesse *= 1.4 # courir
                    if evenement.key == pygame.K_SPACE:  self.joueur.veut_detruire = not self.joueur.veut_detruire
                    if evenement.key == pygame.K_a: pass # maintient de la grenade
                    if evenement.key == pygame.K_e: pass # maintient de la flash
                    if evenement.key == pygame.K_f: pass # maintient du leurre


                if evenement.type == pygame.KEYUP:   # Verifier si une touche est relachee
                    if evenement.key == pygame.K_LSHIFT: self.joueur.vitesse /= 1.4 # ne plus courir
                    if evenement.key == pygame.K_a: pass # relachement de la grenade
                    if evenement.key == pygame.K_e: pass # relachement de la flash
                    if evenement.key == pygame.K_f: pass # relachement du leurre
                        
    def boucle_jeu(self):
        while True :
            self.verifications_touches_calvier_appuiees()
            self.verifications_autres_touches()
            self.ennemie.deplacer(self.long_mur*0.1, self.labyrinthe, self.joueur)
            self.fenetre.fill(black) # Tout effacer
            # Tout charger
            self.afficher_labyrinthe()
            self.si_joueur_veut_detruire()
            self.afficher_pieces()
            self.afficher_joueur()
            self.afficher_ennemie(self.ennemie)
            self.afficher_label()
            pygame.display.flip() # tout réafficher

            self.clock.tick(60)  # limites les FPS a 60 (ATTENTION ! Si on change le nombre de FPS, la vitesse est impactee !)


if __name__ == "__main__":
    jeu = Jeux(black, "titre1")
    jeu.creer_labyrinthe(40, 20, 6, 6, 2, 0.2, red) 
    jeu.afficher_labyrinthe()
    jeu.creer_label(96, 0, 6, 4, red, "quitter")
    jeu.creer_joueur(9, 0, "S", 1.3, 0, 0)
    jeu.creer_pieces(4,"piece.png", jeu.labyrinthe, jeu.joueur, jeu.long_mur)
    jeu.creer_ennemie(0.1, "./yt.png", 15, 10)
    jeu.boucle_jeu()