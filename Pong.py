from Data import pygame, couleurs, width, height, myfont, screen, NOIR
from Raquette import Raquette
from Jeu import Jeu

pygame.display.set_caption("Ping")

# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

jeu = Jeu(1, 2)
jeu.mise_a_jour()

while True:
    if jeu.perdu:
        jeu.ecran_fin("Vous avez perdu")
    elif jeu.all_dead:
        jeu.ecran_fin("Vous avez gagné")
    else:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()

    pygame.display.flip() # envoie de l'image à la carte graphique
    clock.tick(60) # on attend pour ne pas dépasser 60 images/seconde
