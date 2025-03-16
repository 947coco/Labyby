# Projet
Le groupe est composé de 3 lycéens en Terminal general dont moi-même.

## Sujet du projet 
création d’un jeu de labyrinthe codé sous Python 3 en Programmation Orientée Objet, projet conduit par des groupes de quatre élèves.
(on est bien 3)

## Lancer le jeu
Lancer le fichier Jeu.py dans le dossier fichiers_python

## Le cahier des charges (consignes)
Le programme doit être 100 % conçu orienté objet :
- [x] il doit contenir plusieurs classes : par exemple Labyrinthe, Jeu, Personnages, Niveaux... 
- [ ] Chaque élève du groupe ait codé au moins une des classes du programme (cela doit apparaître dans le padlet !)
- [x] Il doit utiliser l’interface graphique Pygame codée sous forme de classe :
    - [x] Par exemple, l’initialisation de Pygame peut se faire dans le constructeur de la classe Labyrinthe avec un nouvel attribut self.fenetre :
    pygame.init()
    pygame.display.set_caption('LABYRINTHE')
    self.fenetre = pygame.display.set_mode((644, 644))
    - [x] la gestion du clavier peut être codée dans une classe Jeu avec une boucle infinie (while True:)
    - [x] le programme principal ne contient alors que ces 3 lignes (c’est un exemple !) :
    if __name__=='__main__':
        jeu=Jeu() # instanciation d’un objet de la classe Jeu
        jeu.loop() # méthode de la classe Jeu qui comprend la boucle infinie qui lance le jeu

## A rendre pour le lundi 17 mars 2025

## Note obtenue : X/20