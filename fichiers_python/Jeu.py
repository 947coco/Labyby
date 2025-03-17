import pygame, codecs, random, time, sys, math # importation de modules
# importation de nos classes
from Labyrinthe import Labyrinthe 
from Projectile import Projectile  
from Menu import Menu   
from Piece import Piece  
from couleurs import *


class Joueur():
    def __init__(self, vitesse, coord_x, coord_y, case_i, case_j, direction, largeur, hauteur, chemin_image, nb_grenade, nb_tire, pieces_a_recup, nb_destruction, nb_construction, est_joueur=True, labyrinthe=None, joueur=None):
        # Différentes images pour diriger le modèle en fonction de la direction du regard
        self.image_droite = pygame.image.load(chemin_image).convert_alpha()
        self.image_gauche = pygame.transform.flip(self.image_droite, True, False)
        self.image_haut = pygame.transform.rotate(self.image_droite, 90)
        self.image_bas = pygame.transform.flip(self.image_haut, False, True)
        self.image = self.image_droite

        # Coordonnées relatives
        self.coord_x, self.coord_y = coord_x, coord_y  # Coordonnées du milieu de la hitbox
        self.case_i, self.case_j = case_i, case_j  # Sur quelle case se trouve le personnage
        self.largeur, self.hauteur = largeur, hauteur  # Dimensions de l'image représentant le personnage
        self.mettre_a_jour_hitbox()

        # Autres attributs
        self.vitesse = vitesse
        self.vitesse_ini = vitesse
        self.direction = direction # direction du regard 
        self.pieces_possedee = 0
        self.pieces_a_recup = pieces_a_recup
        self.nb_grenade, self.nb_tire = nb_grenade, nb_tire
        self.nb_destruction, self.nb_construction = nb_destruction, nb_construction 
        self.veut_detruire = False
        self.endurance = 120
        self.cours_mtn = False
        self.vie = 100  # Le joueur a 100 PV
        self.dernier_degat = 0  # Timestamp du dernier dégât reçu
        self.dernier_tire = time.time()
        if not est_joueur:
            self.case = self.case_random(labyrinthe)
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
    
    def deplacer_ennemie(self, long_mur, arrivee, labyrinthe):
        if self.case.milieu_y < self.coord_y: self.deplacer("z", long_mur)
        if self.case.milieu_x < self.coord_x: self.deplacer("q", long_mur)
        if self.case.milieu_y > self.coord_y: self.deplacer("s", long_mur)
        if self.case.milieu_x > self.coord_x: self.deplacer("d", long_mur)
        if self.x1 < self.case.milieu_x < self.x2 and self.y1 < self.case.milieu_y < self.y2 :
            self.case = self.case_random(labyrinthe)


    def chemin_entier(self, arrivee, labyrinthe):
        i1, j1 = self.case_i, self.case_j
        i2, j2 = arrivee
        chemin = []
        while i2 != i1 and j2 != j1:
            case = self.case_random(labyrinthe)
            case.vue = True
            chemin.append(case)
            # a reprendre

    def case_random(self, labyrinthe):
        try : i, j = random.choice(labyrinthe.graphe.voisin_de((self.case_i, self.case_j)))
        except: i, j = self.case_i, self.case_j
        return labyrinthe.laby[i][j]
    
    def meilleur_case(self, debut, arrivee, labyrinthe, chemin=[]):
        G = labyrinthe.graphe
        distance_min = 999
        meilleur_case = random.choice(G.voisin_de(debut))
        for (i, j) in G.voisin_de(debut):
            distance = self.distance((i, j), arrivee)
            case = labyrinthe.laby[i][j]
            if distance < distance_min and len(G.voisin_de((i, j))) > 1 and case not in chemin: # si la case se rapproche et qu'elle a plus de 1 voisin
                distance_min = distance
                meilleur_case = case
        return meilleur_case

    def distance(self, depart, arrivee):
        i1, j1 = depart
        i2, j2 = arrivee
        return abs(j2-j1) + abs(i2-i1)
    
    def jete_flash(self):
        pass
    def jete_leurre(self):
        pass
    def boost_vitesse(self):
        pass
    
    def joueur_meurt(self):
        font = pygame.font.Font(None, 74)
        texte = font.render("Vous êtes mort !", True, red)
        texte_rect = texte.get_rect(center=(self.fenetre.get_width() // 2, self.fenetre.get_height() // 2))
        self.fenetre.blit(texte, texte_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Attendre 2 secondes avant de quitter
        """
        Mettre bouton recommencer
        """


# Fonction pour afficher une page de chargement
def afficher_chargement(fenetre, largeur, hauteur):
    font = pygame.font.Font(None, 74)
    clock = pygame.time.Clock()
    temps_debut = time.time()
    while time.time() - temps_debut < 2:  # Simuler un chargement de 2 secondes
        fenetre.fill(black)
        texte = font.render("Chargement...", True, white)
        texte_rect = texte.get_rect(center=(largeur // 2, hauteur // 2))
        fenetre.blit(texte, texte_rect)
        pygame.display.flip()
        clock.tick(60)  # Limiter à 60 FPS

# Initialisation de Pygame
pygame.init()
fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
largeur, hauteur = pygame.display.get_surface().get_size()

# Afficher le menu
menu = Menu(fenetre, largeur, hauteur)
menu.gerer_evenements()

# Lancer le jeu avec le mode sélectionné
if menu.mode_jeu:
    print(f"Mode de jeu sélectionné : {menu.mode_jeu}")
    # Vous pouvez maintenant initialiser votre jeu avec le mode sélectionné
    # Par exemple :
    # jeu = Jeux(black, "titre1")
    # jeu.creer_labyrinthe(40, 20, 6, 6, 2, 0.2, blue)
    # jeu.boucle_jeu()
else:
    pygame.quit()




class Jeux():
    def __init__(self, couleur, titre):
        self.labels, self.pieces, self.personnages= [], [], []
        self.projectile = []
        self.nb_niveau = 0
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fenetre.fill(couleur) 
        pygame.display.set_caption(titre)
        #self.icon = pygame.image.load('logo.png')
        #pygame.display.set_icon(self.icon)

    def reinitialiser(self,largeur_laby, hauteur_laby, vitesse_ennemies, largeur_ennemies, hauteur_ennemies, 
                                nb_grenade, nb_tire, nb_construction, nb_destruction, nb_pieces, nb_ennemies, 
                                case_joueur=(0, 0)):
        self.labels, self.pieces, self.personnages= [], [], []
        self.projectile = []
        self.labyrinthe, self.joueur, self.nb_pieces_ini, self.maintient_grenade = None, None, nb_pieces, False
        self.creer_labyrinthe(largeur_laby, hauteur_laby, 6, 6, 2, 0.2, blue)
        self.afficher_labyrinthe()
        print(self.labyrinthe.largeur, self.labyrinthe.hauteur)
        self.creer_label(96, 0, 6, 4, red, "quitter")
        self.creer_label(94, 20, 0.5, 1, green, "endurance")
        self.creer_entite(1.4, "Logo_joueur.png", case_joueur[0], case_joueur[1], 1.5, 1.5, nb_grenade, nb_tire, True, nb_pieces, nb_destruction, nb_construction)
        self.creer_pieces(nb_pieces,"piece.png", self.labyrinthe, self.joueur, self.long_mur)
        for ennemie in range(nb_ennemies):
            j, i = self.labyrinthe.case_random()
            self.creer_entite(vitesse_ennemies, "yt.png", i, j, largeur_ennemies, hauteur_ennemies, 0, 0, False, 0, 0, 0)
        self.joueur.pieces_a_recup = nb_pieces

    def choisir_niveau(self, numero):
        if numero == 0: self.reinitialiser(15, 15, 0.5, 0.4, 0.4, 10, 100, 10, 10, 3, 3,  (0, 0)) # tuto sympa
        if numero == 1: self.reinitialiser(20, 20, 1, 0.5, 0.5, 7, 40, 4, 2, 8, 20,(10, 10))
        if numero == 2: self.reinitialiser(30, 20, 3, 0.7, 0.7, 5, 70, 4, 7, 12, 30,   (25, 17))
        if numero == 3: self.reinitialiser(40, 20, 2, 0.8, 0.8, 15, 30, 5, 5, 20, 50,   (37, 16))
        if numero == 4: self.reinitialiser(10, 10, 5, 1, 1, 4, 15, 0, 0, 20, 25,   (0, 0))
        if numero == 5: self.reinitialiser(40, 20, 7, 1.1, 1.1, 10, 50, 10, 10, 50, 25,   (15, 18))
        if numero == 6: self.reinitialiser(40, 20, 7, 1.1, 1.1, 10, 50, 10, 10, 50, 25,   (15, 18))
        if numero == 7: self.reinitialiser(40, 20, 7, 1.1, 1.1, 10, 50, 10, 10, 50, 25,   (15, 18))
        if numero == 8: self.reinitialiser(40, 20, 7, 1.1, 1.1, 10, 50, 10, 10, 50, 25,   (15, 18))
        


    # FONCTIONS A FAIRE : Implementer les compteurs et afficher sur l'ecran ceux-ci  


    def afficher_compteur_munition(self):
        pass # A FAIRE
    def afficher_compteur_flash(self):
        pass # A FAIRE
    def afficher_compteur_leurre(self):
        pass # A FAIRE
    def afficher_compteur_boost_vitesse(self):
        pass # A FAIR

    def afficher_barre_de_vie(self):
        vie_max = 100  # Vie maximale du joueur
        vie_actuelle = self.joueur.vie  # Vie actuelle du joueur
        barre_largeur = 200  # Largeur de la barre de vie
        barre_hauteur = 20  # Hauteur de la barre de vie
        barre_x = 250  # Position X de la barre de vie 
        barre_y = 20  # Position Y de la barre de vie 

        # Calculer largeur barre vie fonction vie actuelle
        largeur_vie = (vie_actuelle / vie_max) * barre_largeur

         
        pygame.draw.rect(self.fenetre, red, (barre_x, barre_y, barre_largeur, barre_hauteur))
        pygame.draw.rect(self.fenetre, green, (barre_x, barre_y, largeur_vie, barre_hauteur)) 
        pygame.draw.rect(self.fenetre, white, (barre_x, barre_y, barre_largeur, barre_hauteur), 2)

        # Afficher le texte de la vie actuelle
        font = pygame.font.Font(None, 36)
        texte_vie = font.render(f"Vie: {vie_actuelle}/{vie_max}", True, white)
        texte_rect = texte_vie.get_rect(topleft=(barre_x + barre_largeur + 10, barre_y))
        self.fenetre.blit(texte_vie, texte_rect)

    def afficher_compteur_pieces(self):
        font = pygame.font.Font(None, 50)  
        texte = font.render(f"Pièces: {self.joueur.pieces_possedee}", True, white)  
        # Dimensions du rectangle
        rect_width = texte.get_width() + 40
        rect_height = texte.get_height() + 20
        # Créer un rectangle avec fond et bordure
        fond = pygame.Surface((rect_width, rect_height))
        fond.fill((30, 30, 30))  
        pygame.draw.rect(fond, red, (0, 0, rect_width, rect_height), 3)  
        # Position du rectangle et du texte
        rect_x, rect_y = 20, 20  
        self.fenetre.blit(fond, (rect_x, rect_y))
        self.fenetre.blit(texte, (rect_x + 20, rect_y + 10))  
        
    def afficher_touches(self):
        font = pygame.font.Font(None, 36)
        touches = [
            ("Z", "Haut"),
            ("Q", "Gauche"),
            ("S", "Bas"),
            ("D", "Droite"),
            ("E", "Flash"),
            ("A", "Grenade"),
            ("F", "Régénérer"),
            ("Shift", "Courir"),
            ("Espace", "Détruire/Construire"),
            ("Clic G", "Détruire"),
            ("Clic D", "Construire ")
        ]
        # Calculer la largeur maximale du texte pour les touches et les actions
        max_touche_width = max(font.render(touche, True, white).get_width() for touche, _ in touches)
        max_action_width = max(font.render(action, True, white).get_width() for _, action in touches)
        
        # La largeur du rectangle est la plus grande des deux largeurs + une marge
        rect_width = max(max_touche_width, max_action_width) + 40  # marge 40 pixels
        
        # Hauteur du rectangle (deux lignes de texte + marge)
        rect_height = font.get_height() * 2 + 30  
        espacement = 10  
        
        # Diviser les touches en deux groupes
        moitie = len(touches) // 2
        touches_ligne1 = touches[:moitie]  
        touches_ligne2 = touches[moitie:]  
        
        # Position de départ pour la première ligne (en bas de l'écran)
        start_x_ligne1 = (self.fenetre.get_width() - (len(touches_ligne1) * (rect_width + espacement))) // 2
        start_y_ligne1 = self.fenetre.get_height() - rect_height - 20
        
        # Position de départ pour la deuxième ligne 
        start_x_ligne2 = (self.fenetre.get_width() - (len(touches_ligne2) * (rect_width + espacement))) // 2
        start_y_ligne2 = start_y_ligne1 - rect_height - espacement
        
        # Afficher les touches de la première ligne
        for i, (touche, action) in enumerate(touches_ligne1):
            rect_x = start_x_ligne1 + i * (rect_width + espacement)
            rect_y = start_y_ligne1
            fond = pygame.Surface((rect_width, rect_height))
            fond.fill((30, 30, 30))  
            pygame.draw.rect(fond, blue, (0, 0, rect_width, rect_height), 3)  
            # Afficher le rectangle
            self.fenetre.blit(fond, (rect_x, rect_y))
            # Afficher la touche
            texte_touche = font.render(touche, True, white)
            texte_touche_rect = texte_touche.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 3))
            self.fenetre.blit(texte_touche, texte_touche_rect)
            # Afficher l'action
            texte_action = font.render(action, True, white)
            texte_action_rect = texte_action.get_rect(center=(rect_x + rect_width // 2, rect_y + 2 * rect_height // 3))
            self.fenetre.blit(texte_action, texte_action_rect)
        
        # Afficher les touches de la deuxième ligne
        for i, (touche, action) in enumerate(touches_ligne2):
            rect_x = start_x_ligne2 + i * (rect_width + espacement)
            rect_y = start_y_ligne2
            fond = pygame.Surface((rect_width, rect_height))
            fond.fill((30, 30, 30))  
            pygame.draw.rect(fond, blue, (0, 0, rect_width, rect_height), 3)  
            # Afficher le rectangle
            self.fenetre.blit(fond, (rect_x, rect_y))
            # Afficher la touche
            texte_touche = font.render(touche, True, white)
            texte_touche_rect = texte_touche.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 3))
            self.fenetre.blit(texte_touche, texte_touche_rect)
            # Afficher l'action
            texte_action = font.render(action, True, white)
            texte_action_rect = texte_action.get_rect(center=(rect_x + rect_width // 2, rect_y + 2 * rect_height // 3))
            self.fenetre.blit(texte_action, texte_action_rect)

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
        # esthetique du labyrinthe en rapport �� l'affichage du labyrinthe avec pygame 
        self.long_mur, self.epaisseur_mur = self.unite_relatif(longeur_mur, epaisseur_mur)
        self.marge_x, self.marge_y = self.unite_relatif(marge_x, marge_y)
        self.couleur_labyrinthe = couleur
        # utilisation de la classe labyrinthe
        self.labyrinthe = Labyrinthe(largeur, hauteur)
        self.labyrinthe.generer()


    def afficher_labyrinthe(self, que_assigner_coord=False):
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
                if not que_assigner_coord:
                    if case.murS: self.afficher_ligne(x1, y2, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                    if case.murW: self.afficher_ligne(x1, y1, x1, y2, self.epaisseur_mur, self.couleur_labyrinthe)
                    if case.murN: self.afficher_ligne(x1, y1, x2, y1, self.epaisseur_mur, self.couleur_labyrinthe)
                    if case.murE: self.afficher_ligne(x2, y1, x2, y2, self.epaisseur_mur, self.couleur_labyrinthe)
        self.labyrinthe.graphe = self.labyrinthe.creer_un_graphe()

    def creer_entite(self, vitesse, chemin_image, i, j, largeur, hauteur, nb_grenade, nb_tire, est_joueur, pieces_a_recup, nb_destruction, nb_construction):
        case = self.labyrinthe.laby[i][j]
        vitesse_relative, peut_importe = self.unite_relatif(vitesse, 0)
        largeur_relative, hauteur_relative = self.unite_relatif(largeur, hauteur)
        if est_joueur: 
            self.joueur = Joueur(vitesse_relative, case.milieu_x, case.milieu_y, i, j, "N", largeur_relative, hauteur_relative, chemin_image, nb_grenade, nb_tire, pieces_a_recup,nb_destruction, nb_construction, est_joueur)
        else :
            entite = Joueur(vitesse_relative, case.milieu_x, case.milieu_y, i, j, "N", largeur_relative, hauteur_relative, chemin_image, nb_grenade, 
                             nb_tire, pieces_a_recup,nb_destruction, nb_construction, est_joueur, self.labyrinthe, self.joueur)
            self.personnages.append(entite)
        
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
        self.nb_pieces_ini = len(self.pieces)
    def afficher_entitee(self, liste_entites):
        if liste_entites == self.labels: [self.fenetre.blit(label, (x, y)) for label, x, y, w, h, nom in self.labels]; return None
        for entite in liste_entites: 
            self.fenetre.blit(pygame.transform.scale(entite.image, (entite.largeur, entite.hauteur)), (entite.x1, entite.y1))

    def mettre_a_jour_barre_endurance(self):
        for index, (label, x, y, w, h, nom) in enumerate(self.labels):
            if nom == "endurance":
                peut_importe, new_h = self.unite_relatif(0, self.joueur.endurance/130)
                self.labels[index][1] = self.joueur.x2+2
                self.labels[index][2] = self.joueur.y1
                self.labels[index][0] = pygame.transform.scale(label, (w, new_h))

    def mettre_a_jour_ennemies(self):
        [ennemie.deplacer_ennemie(self.long_mur, (self.joueur.case_i, self.joueur.case_j), self.labyrinthe) for ennemie in self.personnages]
        self.collision_mur(self.personnages)
        self.changement_de_case([self.joueur])
        self.changement_de_case(self.personnages)
        self.tourner_modele(self.personnages)

    def mettre_a_jour_projectile(self):
        self.changement_de_case(self.projectile)
        for projectile in self.projectile:
            projectile.lancer(self.long_mur, self.labyrinthe, self.personnages, self.joueur)
            if projectile.doit_etre_detruit:
                self.projectile.remove(projectile)

    def tourner_modele(self, liste_personnage): 
        for personnage in liste_personnage:
            regard_relie_image = {"W": personnage.image_gauche, "E": personnage.image_droite, "N": personnage.image_haut, "S": personnage.image_bas }
            personnage.image = regard_relie_image[personnage.direction]

    def tourner_regard(self, touche_pressee, liste_personnage):
        direction_relie_regard = {"z":"N", "s":"S", "d":"E", "q":"W"}
        for personnage in liste_personnage:
            personnage.direction = direction_relie_regard[touche_pressee]

    def changement_de_case(self, liste_personnage):
        for personnage in liste_personnage:
            case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
            if personnage.coord_x < case.x1 : personnage.case_i -= 1
            if personnage.coord_x > case.x2: personnage.case_i += 1
            if personnage.coord_y < case.y1 : personnage.case_j -= 1
            if personnage.coord_y > case.y2: personnage.case_j += 1

    def collision_mur(self, liste_personnage):
        for personnage in liste_personnage:
            case = self.labyrinthe.laby[personnage.case_i][personnage.case_j]
            if case.y1>personnage.y1 and case.murN : personnage.coord_y = case.y1+personnage.hauteur/2; 
            if case.x1>personnage.x1 and case.murW : personnage.coord_x = case.x1+personnage.largeur/2; 
            if case.y2<personnage.y2 and case.murS : personnage.coord_y = case.y2-personnage.hauteur/2; 
            if case.x2<personnage.x2 and case.murE : personnage.coord_x = case.x2-personnage.largeur/2; 

    def collision_ennemie(self):
        temps_actuel = time.time()  # Temps actuel en secondes
        for i in range(1, len(self.personnages)):
            ennemie = self.personnages[i]
            coins_joueur = [[self.joueur.x1, self.joueur.x2], [self.joueur.y1, self.joueur.y2]]
            coin_ennemie = [[ennemie.x1, ennemie.x2], [ennemie.y1, ennemie.y2]]
            for i in range(2):
                for j in range(2):
                    point_x, point_y = coins_joueur[0][i], coins_joueur[1][j]
                    for ennemie in self.personnages:
                        point_ennemie_x, point_ennemie_y = coin_ennemie[0][i], coin_ennemie[1][j]
                        if ennemie.x1 < point_x < ennemie.x2 and ennemie.y1 < point_y < ennemie.y2 or self.joueur.x1 < point_ennemie_x < self.joueur.x2 and self.joueur.y1 < point_ennemie_y < self.joueur.y2:
                            if temps_actuel - self.joueur.dernier_degat >= 1:  # Vérifier si 3 secondes se sont écoulées
                                self.joueur.vie -= 10  # Le joueur perd 10 PV
                                self.joueur.dernier_degat = temps_actuel  # Mettre à jour le dernier dégât
                                if self.joueur.vie <= 0:
                                    self.joueur_meurt()

    def joueur_meurt(self):
        font = pygame.font.Font(None, 74)
        texte = font.render("Vous êtes mort !", True, red)
        texte_rect = texte.get_rect(center=(self.fenetre.get_width() // 2, self.fenetre.get_height() // 2))
        self.fenetre.blit(texte, texte_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Attendre 2 secondes avant de quitter

    def afficher_victoire(self):
        font = pygame.font.Font(None, 50)  
        texte = font.render(f"Bravo tu as récolté les {self.nb_pieces_ini} pièces sans mourir !!!", True, green)  
        # Dimensions du rectangle 
        rect_width = texte.get_width() + 40
        rect_height = texte.get_height() + 20
        # rectangle avec fond et bordure
        fond = pygame.Surface((rect_width, rect_height))
        fond.fill((30, 30, 30))  
        pygame.draw.rect(fond, white, (0, 0, rect_width, rect_height), 3)  
        # Position du rectangle et du texte
        rect_x = (self.fenetre.get_width() - rect_width) // 2
        rect_y = (self.fenetre.get_height() - rect_height) // 2
        self.fenetre.blit(fond, (rect_x, rect_y))
        self.fenetre.blit(texte, (rect_x + 20, rect_y + 10))
        pygame.display.flip()  # Rafraîchir l'affichage

        # Attendre 2 secondes avant de passer au prochain niveau 
        time.sleep(2)
        self.nb_niveau += 1
        self.choisir_niveau(self.nb_niveau)

    def collision_piece(self):
        for piece in self.pieces:
            coins_piece = [[piece.x1, piece.x2], [piece.y1, piece.y2]]
            for i in range(2):
                for j in range(2):
                    point_x, point_y = coins_piece[0][i], coins_piece[1][j]
                    if self.joueur.x1 < point_x < self.joueur.x2 and self.joueur.y1 < point_y < self.joueur.y2: 
                        try: self.pieces.remove(piece)  # Supprimer pièce collectée
                        except: pass  # Gérer erreurs potentielles
                        self.joueur.pieces_possedee = self.nb_pieces_ini-len(self.pieces)

                        # Mettre à jour l'affichage du compteur de pièces
                        self.afficher_compteur_pieces()
                        pygame.display.flip()  

                        # Vérifier si le joueur a exactement 20 pièces
                        if self.joueur.pieces_possedee == self.joueur.pieces_a_recup:
                            self.afficher_victoire()
                            return  # Arrêter méthode si joueur a gagné

    def joueur_va_se_coincer(self, case):
        compteur = 0
        for mur in [case.murN , case.murS , case.murE , case.murW]: 
            if mur: compteur += 1
        return self.joueur.nb_destruction == 0 and self.joueur.nb_grenade == 0 and compteur == 3
    
        
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
        else :  distance_lance = math.ceil(temps_maintient)
        self.creer_projectile(60, "yt.png", "boom.mp3", type, self.long_mur/2, self.long_mur/2, distance_lance*1.5)
        

    def verifier_deplacement(self, touche_pressee): 
        """Tourner le regard du joueur, verifier si il y a une collision (mur ou ennemie), verifier si il a changer de case, le deplacer"""
        self.collision_piece()        
        self.collision_mur([self.joueur])
        self.collision_ennemie()
        self.tourner_regard(touche_pressee, [self.joueur])
        self.changement_de_case([self.joueur])
        self.joueur.deplacer(touche_pressee, self.long_mur)
        
    def verifications_touches_calvier_appuiees(self):
        touche_clavier = pygame.key.get_pressed()
        # On aurait pu les detecter dans un KEYDOWN mais ca marche nickel donc on change rien
        if touche_clavier[pygame.K_z]: self.verifier_deplacement("z")
        if touche_clavier[pygame.K_q]: self.verifier_deplacement("q")
        if touche_clavier[pygame.K_s]: self.verifier_deplacement("s")
        if touche_clavier[pygame.K_d]: self.verifier_deplacement("d")
        if touche_clavier[pygame.K_e]: 
            if self.joueur.nb_tire > 0 and time.time()-self.joueur.dernier_tire>0.4 :
                self.joueur.dernier_tire = time.time() 
                self.creer_projectile(70, "yt.png", "boom.mp3", "tire", self.long_mur/6, self.long_mur/6, 999)
        self.tourner_modele([self.joueur])

 
    def course_joueur(self):
        if self.joueur.cours_mtn :
            if self.joueur.endurance>10: 
                self.joueur.endurance -= 1
                self.joueur.vitesse = self.joueur.vitesse_ini*2.5
            else :
                self.joueur.vitesse = self.joueur.vitesse_ini
                self.joueur.cours_mtn = False
        else : 
            if self.joueur.endurance < 180: self.joueur.endurance += 0.4
            self.joueur.vitesse = self.joueur.vitesse_ini

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
                    if evenement.key == pygame.K_LSHIFT: self.joueur.cours_mtn = True
                    if evenement.key == pygame.K_SPACE:  self.joueur.veut_detruire = not self.joueur.veut_detruire
                    if evenement.key == pygame.K_f: self.labyrinthe.regenerer(self.labyrinthe.largeur, self.labyrinthe.hauteur) # maintient du leurre mais pr l'instant test du regenerer
                    if evenement.key == pygame.K_a: self.maintient_grenade = time.time() # maintient de la grenade


                if evenement.type == pygame.KEYUP:   # Verifier si une touche est relachee
                    if evenement.key == pygame.K_LSHIFT: self.joueur.cours_mtn = False
                    if evenement.key == pygame.K_a: 
                        if self.joueur.nb_grenade > 0:
                            self.lancer_projectile("grenade", 5, self.maintient_grenade)


 
                    
    def boucle_jeu(self):
        while True:
            self.verifications_touches_calvier_appuiees()
            self.verifications_autres_touches()
            self.fenetre.fill(black) # Tout effacer
            # Tout charger
            self.afficher_labyrinthe()
            self.si_joueur_veut_detruire()
            self.afficher_entitee(self.pieces)
            self.afficher_entitee(self.personnages)
            self.afficher_entitee([self.joueur])
            self.afficher_entitee(self.labels)
            self.afficher_entitee(self.projectile)
            self.mettre_a_jour_projectile()
            self.mettre_a_jour_ennemies()
            self.mettre_a_jour_barre_endurance()
            self.course_joueur()
            self.afficher_compteur_pieces()  
            self.afficher_barre_de_vie()  
            self.afficher_touches()  
            if self.joueur.vie <= 0: self.joueur_meurt()
            pygame.display.flip()  

            self.clock.tick(60)  # Limiter les FPS à 60

if __name__ == "__main__":
    pygame.init()
    fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    largeur, hauteur = pygame.display.get_surface().get_size()

    # Afficher la page de chargement 
    afficher_chargement(fenetre, largeur, hauteur)

    # Afficher le menu
    menu = Menu(fenetre, largeur, hauteur)
    menu.boucle_menu()  # Afficher et gérer le menu
    

    # Si un mode de jeu a été sélectionné, lancer le jeu
    if menu.mode_jeu:
        jeu = Jeux(black, "Labyrinthe Game")
        jeu.choisir_niveau(menu.mode_jeu)
        """
        jeu.creer_labyrinthe(40, 20, 6, 6, 2, 0.2, blue)
        jeu.afficher_labyrinthe()
        jeu.creer_label(96, 0, 6, 4, red, "quitter")
        jeu.creer_label(94, 20, 0.5, 1, green, "endurance")
        jeu.creer_entite(1.4, "Logo_joueur.png", 0, 1, 1.5, 1.5, 10, 10, True, 0, 2, 2)
        jeu.creer_pieces(2,"piece.png", jeu.labyrinthe, jeu.joueur, jeu.long_mur)
        jeu.creer_entite(4, "yt.png", 10, 10, 1, 1, 0, 0 , False, 0, 0, 0)
        jeu.creer_entite(4, "yt.png", 30, 5, 1, 1, 0, 0 , False, 0, 0, 0)
        jeu.creer_entite(4, "yt.png", 10, 10, 1, 1, 0, 0 , False, 0, 0, 0)
        jeu.creer_entite(4, "yt.png", 0, 18, 1, 1, 0, 0 , False, 0, 0, 0)
        jeu.creer_entite(4, "yt.png", 10, 19, 1, 1, 0, 0 , False, 0, 0, 0) "
        """
        jeu.boucle_jeu()
