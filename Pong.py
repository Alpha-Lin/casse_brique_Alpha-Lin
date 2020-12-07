from Data import pygame
from Raquette import Raquette
from Jeu import Jeu

pygame.init() # initialisation de Pygame

pygame.display.set_caption("Ping")

# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

jeu = Jeu(3, 2)

while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()

    pygame.display.flip() # envoie de l'image à la carte graphique
    clock.tick(60) # on attend pour ne pas dépasser 60 images/seconde
