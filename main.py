import pygame
from pygame.locals import *
from random import randint

pygame.init()
LARGEUR = 600
HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()
continuer = True


while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False


    pygame.display.flip()
    fenetre.fill((0, 0, 0))
    clock.tick(60)

pygame.quit()

print("Hello world !")