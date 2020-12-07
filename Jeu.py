from Balle import Balle
from Raquette import Raquette
from Brique import Brique
from Data import *
import sys

class Jeu:
    def __init__(self, vie, vieBrique):
        self.vieConst = vie
        self.vieBrique = vieBrique
        self.initialisation()

    def initialisation(self):
        self.vie = self.vieConst
        self.balle = Balle()
        self.raquette = Raquette()
        self.perdu = False
        self.lignesBriques = [[Brique(i * 29 * width // 400 + XMIN + RAYON_BALLE * 5, j * 3 * height // 40 + YMIN + RAYON_BALLE * 3, self.vieBrique) for j in range(5)] for i in range(11)]

    def gestion_evenements(self):
        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Pour quitter
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Bouton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette, self)
        if self.vie == 0: # Quand la vie tombe à 0
            self.perdu = True
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
        texte, rect = myfont.render("Score : " + str(score), couleurs[5], size = 2 * (width + height) // 175)
        rect.topleft = (width//100, height//100)
        screen.blit(texte, rect)
        texte, rect = myfont.render("Vie : " + str(self.vie), couleurs[5], size = 2 * (width + height) // 175)
        rect.topleft = (width//100, height//25)
        screen.blit(texte, rect)

        pygame.draw.rect(screen, couleurs[5], [width//100 * 7, height//100 * 7, width//25 * 21, height//25 * 21], (width + height) // 300) # Contour

