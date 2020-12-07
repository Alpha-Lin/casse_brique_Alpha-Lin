import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte

# Pour le texte.
pygame.freetype.init()
myfont=pygame.freetype.SysFont(None, 20) # texte de taille 20

# Taille de la fenetre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

couleurs = [(255, 0, 0), # Rouge
            (0, 255, 255), # Cyan
            (0, 0, 255), # Bleu
            (165, 42, 42), # Marron
            (255, 255, 0), # Jaune
            (255, 255, 255),] # Blanc

NOIR = (0, 0, 0)

RAYON_BALLE = (width + height) // 170
XMIN, YMIN = width//100 * 7 , height//100 * 7
XMAX, YMAX = width//100 * 91, height//100 * 91