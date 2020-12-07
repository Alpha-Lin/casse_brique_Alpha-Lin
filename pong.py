import random # Pour les tirages
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math
import time
import keyboard

pygame.init() # initialisation de Pygame

# Pour le texte.
pygame.freetype.init()
myfont=pygame.freetype.SysFont(None, 20) # texte de taille 20

# Taille de la fenetre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")

# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

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

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8 # vitesse initiale
        self.vitesse_par_angle(60) # vecteur vitesse
        self.sur_raquette = True

    def afficher(self):
        pygame.draw.rect(screen, couleurs[5], (int(self.x-RAYON_BALLE), int(self.y-RAYON_BALLE), 2*RAYON_BALLE, 2*RAYON_BALLE), 0)

    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur/2 + RAYON_BALLE
        angle = 90 + 80 * diff/longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette, instance_jeu):
        if self.sur_raquette:
            self.y = raquette.y - 2*RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_ballon(self) and self.vy > 0:
                self.rebond_raquette(raquette)
            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx
            if self.x - RAYON_BALLE < XMIN:
                self.vx = -self.vx
            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette = True
                instance_jeu.vie -= 1
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

class Jeu:
    def __init__(self, vie, vieBrique):
        self.vieConst = vie
        self.vieBrique = vieBrique
        self.initialisation()

    def initialisation(self):
        self.vie = self.vieConst
        self.balle = Balle()
        self.raquette = Raquette()
        self.lignesBriques = [[Brique(i * 58 * width // 800 + XMIN + RAYON_BALLE * 5, j * 45 * height // 600 + YMIN + RAYON_BALLE * 3, self.vieBrique) for j in range(5)] for i in range(11)]

    def gestion_evenements(self):
        # Gestion des evenements
        if keyboard.is_pressed('esc'):
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit() # Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Bouton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette, self)
        if self.vie == 0: # Quand la vie tombe à 0
            self.initialisation()
        else:
            for briques in self.lignesBriques:
                for brique in briques:
                    if brique.en_vie():
                        brique.collision_balle(self.balle)
            self.raquette.deplacer(x)

    def affichage(self):
        screen.fill(NOIR) # on efface l'écran
        self.balle.afficher()
        self.raquette.afficher()
        score = 0
        for briques in self.lignesBriques:
            for brique in briques:
                if brique.en_vie():
                    brique.afficher()
                else:
                    score += 1
        texte, rect = myfont.render("Score : " + str(score), (125, 125, 125), size=16)
        rect.topleft = (width//100, height//100)
        screen.blit(texte, rect)
        texte, rect = myfont.render("Vie : " + str(self.vie), (125, 125, 125), size=16)
        rect.topleft = (width//100, height//100 * 4)
        screen.blit(texte, rect)

        pygame.draw.rect(screen, couleurs[5], [width//100 * 7, height//100 * 7, width//100 * 84, height//100 * 84], (width + height) // 300) # Contour

class Raquette:
    def __init__(self):
        self.x = (YMIN+XMAX)/2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10*RAYON_BALLE

    def afficher(self):
        pygame.draw.rect(screen, couleurs[5], (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE), self.longueur, 2*RAYON_BALLE), 0)

    def deplacer(self, x):
        if x - self.longueur/2 < XMIN:
            self.x = XMIN + self.longueur/2
        elif x + self.longueur/2 > XMAX:
            self.x = XMAX - self.longueur/2
        else:
            self.x = x

    def collision_ballon(self, balle):
        vertical = abs(self.y - balle.y) < 2*RAYON_BALLE
        horizontal = abs(self.x - balle.x) < self.longueur/2 + RAYON_BALLE
        return vertical and horizontal

class Brique:
    def __init__(self, x, y, vie):
        self.x = x
        self.y = y
        self.vie = vie
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        couleur = self.vie if self.vie <= 5 else self.vie - self.vie // 5
        pygame.draw.rect(screen, couleurs[couleur], (int(self.x-self.longueur/2),
                                        int(self.y-self.largeur/2),
                                        self.longueur, self.largeur), 0)

    def collision_balle(self, balle):
        # on suppose que largeur<longueur
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x: # on regarde a droite
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge: # on touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a droite
                    balle.vx = -balle.vx
        else: # on regarde a gauche
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge: # on touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a gauche
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1   
        return touche

jeu = Jeu(3, 2)

while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()

    pygame.display.flip() # envoie de l'image à la carte graphique
    clock.tick(60) # on attend pour ne pas dépasser 60 images/seconde
