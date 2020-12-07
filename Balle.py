import math
from Data import pygame, screen, couleurs, RAYON_BALLE, XMIN, XMAX, YMIN, YMAX

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
