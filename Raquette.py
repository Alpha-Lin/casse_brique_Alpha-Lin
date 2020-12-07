from Data import YMIN, YMAX, XMIN, XMAX, RAYON_BALLE, pygame, screen, couleurs

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