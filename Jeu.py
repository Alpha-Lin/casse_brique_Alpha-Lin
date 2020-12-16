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
        self.all_dead = False
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
            tmp_all_dead = True
            for briques in self.lignesBriques:
                for brique in briques:
                    if brique.en_vie():
                        tmp_all_dead = False
                        brique.collision_balle(self.balle)
            if tmp_all_dead:
                self.all_dead = True
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

        pygame.draw.rect(screen, couleurs[5], [width//100 * 7, height//100 * 7, 84 * (width//100), 84 * (height//100)], (width + height) // 300) # Contour

    def ecran_fin(self, texte):
        screen.fill(NOIR)

        texte, rect = myfont.render(texte, couleurs[5], size = 12 * (width + height) // 175)
        rect.topleft = (width//24 , height//10 * 3)
        screen.blit(texte, rect)

        texte, rect = myfont.render("Appuyez sur la souris pour recommencer", couleurs[5], size = 4 * (width + height) // 175)
        rect.topleft = (25 * width//192,  height//2)
        screen.blit(texte, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.initialisation()