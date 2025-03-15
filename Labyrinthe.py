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

    def regenerer(self):
        for i in range(self.largeur-1):
            for j in range(self.hauteur-1):
                case = self.laby[j][i] 
                case.vue, case.murN, case.murS, case.murE, case.murW = False, True, True, True, True
        self.generer()

    def creer_un_graphe(self):
        dico_adjacence = {(x, y): [] for x in range(self.largeur) for y in range(self.hauteur)} # initialiser toutes les cases (i, j) sans voisins []
        for i in range(self.largeur-1):           # ajouter les cases voisines grace a la presence ou non des murs
            for j in range(self.hauteur-1):
                case = self.laby[j][i]
                if not case.murN and j > 0: dico_adjacence[(i, j)].append((i, j-1))
                if not case.murS : dico_adjacence[(i, j)].append((i, j+1))
                if not case.murE : dico_adjacence[(i, j)].append((i+1, j))
                if not case.murW and i > 0: dico_adjacence[(i, j)].append((i-1, j))
        return dico_adjacence
    


class Joueur():
    def __init__(self, vitesse, coord_x, coord_y, case_i, case_j, direction, largeur, hauteur, chemin_image, nb_grenade, nb_leurre, pieces_a_recup, nb_destruction, nb_construction):
        # differentes images pour diriger le modele en fonction de la direction du regard
        self.image_droite = pygame.image.load(chemin_image).convert_alpha()
        self.image_gauche = pygame.transform.flip(self.image_droite, True, False)
        self.image_haut = pygame.transform.rotate(self.image_droite, 90)
        self.image_bas = pygame.transform.flip(self.image_haut, False, True)
        self.image = self.image_droite
        # coordonnes relative 
        self.coord_x, self.coord_y = coord_x, coord_y # coordonnes du milieu de la hitbox
        self.case_i, self.case_j = case_i, case_j # Sur quelle case se trouve le personnage
        self.largeur, self.hauteur = largeur, hauteur # dimensions de l'image representant le personnage
        self.mettre_a_jour_hitbox()
        # Autres
        self.vitesse = vitesse
        self.direction = direction # direction du regard 
        self.pieces_possedee = 0
        self.pieces_a_recup = pieces_a_recup
        self.nb_grenade, self.nb_leurre = nb_grenade, nb_leurre 
        self.nb_destruction, self.nb_construction = nb_destruction, nb_construction 
        self.veut_detruire = False
            
    def mettre_a_jour_hitbox(self):
        self.x1, self.y1 = self.coord_x-self.largeur/2, self.coord_y-self.hauteur/2 # bords gauche et haut de la hitox
        self.x2, self.y2 = self.coord_x+self.largeur/2, self.coord_y+self.hauteur/2 # bords droite et bas de la hitbox

    def deplacer(self, touche_pressee, longeur_saut):
        # deplacer le joueur en fonction de sa vitesse et de la touche appuiee
        if touche_pressee == "z" : self.coord_y -= self.vitesse/longeur_saut 
        if touche_pressee == "q" : self.coord_x -= self.vitesse/longeur_saut
        if touche_pressee == "d" : self.coord_x += self.vitesse/longeur_saut
        if touche_pressee == "s" : self.coord_y += self.vitesse/longeur_saut
        self.mettre_a_jour_hitbox()
    
    def deplacer_ennemie(self, long_mur):
        i, j = 10, 10 #self.chemin[0]
        if i > self.case_i: self.deplacer("q", long_mur)
        if i < self.case_i: self.deplacer("d", long_mur)
        if j > self.case_j: self.deplacer("z", long_mur)
        if j < self.case_j: self.deplacer("s", long_mur)
        self.mettre_a_jour_hitbox()

    def C39_bfs_iteratif2(self, graphe, debut, fin):
        parents = {debut: None}
        f = File()
        f.enfiler(debut)
        while not f.est_vide():
            sommet = f.defiler()

            if sommet == fin: # reconstruire le chemin
                chemin = [fin]
                while sommet != None:
                    chemin.append(sommet)
                    sommet = parents[sommet]
                self.chemin = chemin[::-1]
                print(self.chemin)

            for voisin in graphe[sommet]:
                if voisin not in parents:
                    f.enfiler(voisin)
                    parents[voisin] = sommet  

    def jete_flash(self):
        pass
    def jete_leurre(self):
        pass
    def boost_vitesse(self):
        pass




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

    def lancer(self, long_mur, labyrinthe):
        self.mettre_a_jour_hitbox()
        if self.etat_post_explosion: self.explose(labyrinthe); return None
        distance_lancer = long_mur*self.distance_nb_case
        if  ((abs(self.coord_x - self.x_init) > distance_lancer or abs(self.coord_y - self.y_init) > distance_lancer)): 
            self.debut = time.time() # pour calculer le temps avant la suppression du projectile a l'ecran
            self.etat_post_explosion = True
        elif self.arret_mur(labyrinthe):
            self.debut = time.time() # pour
            self.etat_post_explosion = True
            self.mur_doit_etre_detruit = True
        else : 
            self.avance(long_mur) 

    def arret_mur(self, labyrinthe):
        case = labyrinthe.laby[self.case_i][self.case_j]
        if (case.y1>self.y1 and case.murN) or (case.x1>self.x1 and case.murW) or (case.y2<self.y2 and case.murS) or (case.x2<self.x2 and case.murE) :
            return True  

    def avance(self, longueur_mur):
        if self.direction == "N": self.coord_y -= self.vitesse/longueur_mur
        elif self.direction == "S": self.coord_y += self.vitesse/longueur_mur
        elif self.direction == "E": self.coord_x += self.vitesse/longueur_mur
        elif self.direction == "W": self.coord_x -= self.vitesse/longueur_mur

    def explose(self, labyrinthe):
        self.largeur *= 1.005
        self.hauteur *= 1.005
        if time.time() - self.debut > 1.5:  # si l'explosion a duree plus de 1 secondes
            pygame.mixer.Sound(self.fichier_son).play()
            self.produit_effet(labyrinthe)
            self.doit_etre_detruit = True

    def produit_effet(self, labyrinthe):
        if self.type == "grenade" and self.mur_doit_etre_detruit: labyrinthe.abattre_mur(self.case_i, self.case_j, self.direction)
        elif self.type == "leurre": pass # attirer ennemies
        
class Piece():
    def __init__(self, chemin_image, largeur_image, hauteur_image, x, y):
        self.image = pygame.image.load(chemin_image).convert_alpha()
        self.largeur, self.hauteur = largeur_image, hauteur_image
        self.x1, self.y1, self.x2, self.y2 = x, y, x+largeur_image, y+hauteur_image

class Jeux():
    def __init__(self, couleur, titre):
        self.labels, self.pieces, self.personnages= [], [], []
        self.projectile = []
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
    def afficher_compteur_flash(self):
        pass # A FAIRE
    def afficher_compteur_leurre(self):
        pass # A FAIRE
    def afficher_compteur_boost_vitesse(self):
        pass # A FAIRE

    # Sert a convertir des pourcentages X, Y en fonction de la taille de l'ecran afin de pouvoir jouer sur plusieurs resolutions possibles
    def unite_relatif(self, X, Y): return int(pygame.display.Info().current_w*X*0.01), int(pygame.display.Info().current_h *Y*0.0177777777) 

    def afficher_ligne(self, x1, y1, x2, y2, epaisseur, couleur):  pygame.draw.line(self.fenetre, couleur, (x1, y1), (x2, y2), epaisseur)
        
    def creer_label(self, coordonnee_x, coordonnee_y, largeur, hauteur, couleur, nom):
        # creer un label de coordonees x, y et de taille largeur x hauteur
        w, h = self.unite_relatif(largeur, hauteur)
        x, y = self.unite_relatif(coordonnee_x, coordonnee_y)
        label = pygame.surface.Surface((w, h))
        label.fill(couleur)
        self.labels.append([label, x, y, w, h, nom])

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

    def creer_entite(self, vitesse, chemin_image, i, j, largeur, hauteur, nb_flash, nb_leurre, est_joueur, pieces_a_recup,nb_destruction, nb_construction):
        case = self.labyrinthe.laby[i][j]
        vitesse_relative, peut_importe = self.unite_relatif(vitesse, 0)
        largeur_relative, hauteur_relative = self.unite_relatif(largeur, hauteur)
        self.personnages.append(Joueur(vitesse_relative, case.milieu_x, case.milieu_y, i, j, "N", largeur_relative, hauteur_relative, 
                            chemin_image, nb_flash, nb_leurre, pieces_a_recup,nb_destruction, nb_construction))
        if est_joueur: self.joueur = self.personnages[-1] # si le nb de pieces a recup est > 0 = c le joueur (ennemies n'en recup pas)

    def creer_projectile(self, vitesse, chemin_image, fichier_son, type, largeur, hauteur, distance_max):
        self.projectile.append(Projectile(vitesse, chemin_image, fichier_son, type, largeur, hauteur, self.joueur, distance_max))

    def creer_pieces(self, nb_pieces, chemin_image, labyrinthe, joueur, longeur_mur):
        joueur.pieces_a_recup = nb_pieces
        for piece in range(nb_pieces):
            i, j = joueur.case_i, joueur.case_j
            while i == joueur.case_i and j == joueur.case_j:
                i, j = random.randint(1, labyrinthe.largeur-1), random.randint(1, labyrinthe.hauteur-1)
            case = labyrinthe.laby[j][i]
            self.pieces.append(Piece(chemin_image, longeur_mur*0.5, longeur_mur*0.5, case.x1+longeur_mur*0.2, case.y1+longeur_mur*0.2))

    def afficher_entitee(self, liste_entites):
        if liste_entites == self.labels: [self.fenetre.blit(label, (x, y)) for label, x, y, w, h, nom in self.labels]; return None
        for entite in liste_entites: 
            self.fenetre.blit(pygame.transform.scale(entite.image, (entite.largeur, entite.hauteur)), (entite.x1, entite.y1))

    def mettre_a_jour_ennemies(self):
        for ennemie in self.personnages:
            if ennemie != self.joueur:
                ennemie.deplacer_ennemie(self.long_mur)
                self.tourner_modele(ennemie)

    def mettre_a_jour_projectile(self):
        for projectile in self.projectile:
            self.changement_de_case(projectile)
            projectile.lancer(self.long_mur, self.labyrinthe)
            if projectile.doit_etre_detruit:
                self.projectile.remove(projectile)

    def tourner_modele(self, personnage): 
        regard_relie_image = {"W": personnage.image_gauche, "E": personnage.image_droite, "N": personnage.image_haut, "S": personnage.image_bas }
        personnage.image = regard_relie_image[personnage.direction]

    def tourner_regard(self, touche_pressee, personnage):
        direction_relie_regard = {"z":"N", "s":"S", "d":"E", "q":"W"}
        personnage.direction = direction_relie_regard[touche_pressee]

    def changement_de_case(self, personnage):
        case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
        if personnage.coord_x < case.x1 : personnage.case_i -= 1
        if personnage.coord_x > case.x2: personnage.case_i += 1
        if personnage.coord_y < case.y1 : personnage.case_j -= 1
        if personnage.coord_y > case.y2: personnage.case_j += 1

    def collision_mur(self, personnage):
        case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
        for personnage in self.personnages:
            if case.y1>personnage.y1 and case.murN : personnage.coord_y = case.y1+personnage.hauteur/2; 
            if case.x1>personnage.x1 and case.murW : personnage.coord_x = case.x1+personnage.largeur/2; 
            if case.y2<personnage.y2 and case.murS : personnage.coord_y = case.y2-personnage.hauteur/2; 
            if case.x2<personnage.x2 and case.murE : personnage.coord_x = case.x2-personnage.largeur/2; 

    def collision_ennemie(self):
        for i in range(1, len(self.personnages)):
            ennemie = self.personnages[i]
            coins_joueur = [[self.joueur.x1, self.joueur.x2], [self.joueur.y1, self.joueur.y2]]
            for i in range(2):
                for j in range(2):
                    point_x, point_y = coins_joueur[0][i], coins_joueur[1][j]
                    if ennemie.x1 < point_x < ennemie.x2 and ennemie.y1 < point_y < ennemie.y2 :
                        self.joueur_meurt()

    def joueur_meurt(self):
        print("joueur mort")

    def collision_piece(self):
        for piece in self.pieces:
            coins_piece = [[piece.x1, piece.x2], [piece.y1, piece.y2]]
            for i in range(2):
                for j in range(2):
                    point_x, point_y = coins_piece[0][i], coins_piece[1][j]
                    if self.joueur.x1 < point_x < self.joueur.x2 and self.joueur.y1 < point_y < self.joueur.y2:
                        self.joueur.pieces_possedee += 1
                        try : self.pieces.remove(piece)
                        except : pass # parfois ca recupere 2 fois la piece (enfin je pense) et fait tout crasher donc je passe l'erreur

    def joueur_va_se_coincer(self, case):
        compteur = 0
        for mur in [case.murN , case.murS , case.murE , case.murW]: 
            if mur: compteur += 1
        return (self.joueur.nb_destruction == 0 or self.joueur.nb_grenade == 0) and compteur == 3
    
    def si_joueur_veut_detruire(self, a_clique = "", couleur_destruction = red, couleur_construction = green):
        if self.joueur.veut_detruire : 
            case = self.labyrinthe.laby[self.joueur.case_i][self.joueur.case_j]
            if self.joueur.direction == "S" and self.joueur.case_j < self.labyrinthe.largeur-1:
                if case.murS:
                    
                    if a_clique == "clique_gauche" and self.joueur.nb_destruction > 0:         
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "S")       
                        self.joueur.nb_destruction -= 1
                    elif self.joueur.nb_destruction > 0 :
                            self.afficher_ligne(case.x1, case.y2, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur_destruction)
                else :
                    if a_clique == "clique_droit" and self.joueur.nb_construction > 0 and not self.joueur_va_se_coincer(case):          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "S", veut_construire=True)
                        self.joueur.nb_construction -= 1
                    elif self.joueur.nb_construction > 0 :
                            self.afficher_ligne(case.x1, case.y2, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur_construction) # sinon on affiche le mur de couleur "couleur"
                
            if self.joueur.direction == "N" and self.joueur.case_j > 0 :
                if case.murN:
                    if a_clique == "clique_gauche" and self.joueur.nb_destruction > 0:         
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "N")      
                        self.joueur.nb_destruction -= 1
                    elif self.joueur.nb_destruction > 0 :
                            self.afficher_ligne(case.x1, case.y1, case.x2, case.y1, int(self.epaisseur_mur*1.33), couleur_destruction)
                else :
                    if a_clique == "clique_droit" and self.joueur.nb_construction > 0 and not self.joueur_va_se_coincer(case):          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "N", veut_construire=True)
                        self.joueur.nb_construction -= 1
                    elif self.joueur.nb_construction > 0 :
                            self.afficher_ligne(case.x1, case.y1, case.x2, case.y1, int(self.epaisseur_mur*1.33), couleur_construction)
                

            if self.joueur.direction == "E" and self.joueur.case_i < self.labyrinthe.hauteur-1:
                if case.murE:
                    if a_clique == "clique_gauche" and self.joueur.nb_destruction > 0:          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "E")      
                        self.joueur.nb_destruction -= 1
                    elif self.joueur.nb_destruction > 0:
                        self.afficher_ligne(case.x2, case.y1, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur_destruction)
                        
                else :
                    if a_clique == "clique_droit" and self.joueur.nb_construction > 0 and not self.joueur_va_se_coincer(case):          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "E", veut_construire=True)
                        self.joueur.nb_construction -= 1
                    elif self.joueur.nb_construction > 0:
                        self.afficher_ligne(case.x2, case.y1, case.x2, case.y2, int(self.epaisseur_mur*1.33), couleur_construction)
                        

            if self.joueur.direction == "W" and self.joueur.case_i > 0:
                if case.murW:
                    if a_clique == "clique_gauche" and self.joueur.nb_destruction > 0:          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "W")      
                        self.joueur.nb_destruction -= 1
                    elif self.joueur.nb_destruction > 0:
                        self.afficher_ligne(case.x1, case.y1, case.x1, case.y2, int(self.epaisseur_mur*1.33), couleur_destruction)
                        
                else :
                    if a_clique == "clique_droit" and self.joueur.nb_construction > 0 and not self.joueur_va_se_coincer(case):          
                        self.labyrinthe.abattre_mur(self.joueur.case_i, self.joueur.case_j, "W", veut_construire=True)
                        self.joueur.nb_construction -= 1
                    elif self.joueur.nb_construction > 0:
                        self.afficher_ligne(case.x1, case.y1, case.x1, case.y2, int(self.epaisseur_mur*1.33), couleur_construction)
                        
    def lancer_projectile(self, type, distance_max, maintient):
        temps_maintient = time.time()-maintient
        if temps_maintient> distance_max: distance_lance = distance_max
        else :  distance_lance = round(temps_maintient)
        self.creer_projectile(60, "yt.png", "boom.mp3", type, self.long_mur/2, self.long_mur/2, distance_lance*1.7)
        
    def verifier_deplacement(self, touche_pressee): 
        """Tourner le regard du joueur, verifier si il y a une collision (mur ou ennemie), verifier si il a changer de case, le deplacer"""
        self.collision_piece()        
        self.collision_mur(self.joueur)
        self.collision_ennemie()
        self.tourner_regard(touche_pressee, self.joueur)
        self.changement_de_case(self.joueur)
        self.joueur.deplacer(touche_pressee, self.long_mur)
        
    def verifications_touches_calvier_appuiees(self):
        touche_clavier = pygame.key.get_pressed()
        # On aurait pu les detecter dans un KEYDOWN mais ca marche nickel donc on change rien
        if touche_clavier[pygame.K_z]: self.verifier_deplacement("z")
        if touche_clavier[pygame.K_q]: self.verifier_deplacement("q")
        if touche_clavier[pygame.K_s]: self.verifier_deplacement("s")
        if touche_clavier[pygame.K_d]: self.verifier_deplacement("d")
        self.tourner_modele(self.joueur)
 

    def verifications_autres_touches(self):
        for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    if evenement.button == 1:
                        self.si_joueur_veut_detruire("clique_gauche") 
                        for label, x, y, w, h, nom in self.labels:
                            if nom == "quitter" and x < evenement.pos[0] < x+w and y < evenement.pos[1] < y+h:
                                pygame.quit(); sys.exit() # on detruit la fenetre pygame puis on termine le processus correctement
                
                    if evenement.button == 3: # clique_droit
                            self.si_joueur_veut_detruire("clique_droit") 
               
                if evenement.type == pygame.KEYDOWN:    # Verifier si une touche est enfoncee 
                    if evenement.key == pygame.K_LSHIFT: self.joueur.vitesse *= 1.4 # courir
                    if evenement.key == pygame.K_SPACE:  self.joueur.veut_detruire = not self.joueur.veut_detruire
                    if evenement.key == pygame.K_e: self.maintient_flash = time.time()# maintient de la flash
                    if evenement.key == pygame.K_f: self.labyrinthe.regenerer() # maintient du leurre mais pr l'instant test du regenerer
                    if evenement.key == pygame.K_a: self.maintient_grenade = time.time() # maintient de la grenade


                if evenement.type == pygame.KEYUP:   # Verifier si une touche est relachee
                    if evenement.key == pygame.K_LSHIFT: self.joueur.vitesse /= 1.4 # ne plus courir
                    if evenement.key == pygame.K_a: 
                        if self.joueur.nb_grenade > 0:
                            self.lancer_projectile("grenade", 5, self.maintient_grenade)
                    if evenement.key == pygame.K_e: 
                        if self.joueur.nb_leurre > 0:
                            self.lancer_projectile("leurre", 6, self.maintient_flash) 
                    if evenement.key == pygame.K_f: pass
 
                    
    def boucle_jeu(self):
        while True :
            self.verifications_touches_calvier_appuiees()
            self.verifications_autres_touches()
            self.fenetre.fill(black) # Tout effacer
            # Tout charger
            self.afficher_labyrinthe()
            self.si_joueur_veut_detruire()
            self.afficher_entitee(self.pieces)
            self.afficher_entitee(self.personnages)
            self.afficher_entitee(self.labels)
            self.afficher_entitee(self.projectile)
            self.mettre_a_jour_projectile()
            self.mettre_a_jour_ennemies()
            pygame.display.flip() # tout reafficher

            self.clock.tick(60)  # limites les FPS a 60 (ATTENTION ! Si on change le nombre de FPS, la vitesse est impactee !)


if __name__ == "__main__":
    jeu = Jeux(black, "titre1")
    jeu.creer_labyrinthe(40, 20, 6, 6, 2, 0.2, blue) 
    jeu.afficher_labyrinthe()
    jeu.creer_label(96, 0, 6, 4, red, "quitter")
    jeu.creer_entite(2, "Logo_joueur.png", 0, 1, 1.5, 1.5, 10, 10, True, 0, 2, 2)
    jeu.creer_pieces(20,"piece.png", jeu.labyrinthe, jeu.personnages[0], jeu.long_mur)
    jeu.creer_entite(20, "yt.png", 10, 10, 1.5, 1.5, 0, 0 , False, 0, 0, 0)
    jeu.boucle_jeu()