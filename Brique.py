from Data import RAYON_BALLE, pygame, screen, couleurs

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
            pygame.mixer.music.load("sounds/8-bit-shot.wav")
            pygame.mixer.music.play()   
            self.vie -= 1
            if self.vie == 0:
                pygame.mixer.music.load("sounds/8-bit-synth-chirp-notification.wav")
                pygame.mixer.music.play()   
        return touche
