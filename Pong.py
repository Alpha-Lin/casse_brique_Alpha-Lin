from Data import pygame, couleurs, width, height, myfont, screen, NOIR
from Raquette import Raquette
from Jeu import Jeu

pygame.display.set_caption("Ping")

# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

jeu = Jeu(1, 2)

while True:
    if not jeu.perdu:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()
    else:
        screen.fill(NOIR)

        texte, rect = myfont.render("Vous avez perdu", couleurs[5], size = 12 * (width + height) // 175)
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
                jeu.initialisation()

    pygame.display.flip() # envoie de l'image à la carte graphique
    clock.tick(60) # on attend pour ne pas dépasser 60 images/seconde
