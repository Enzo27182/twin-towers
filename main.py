import pygame
from pygame.locals import *

# initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
listes_des_srpites = pygame.sprite.LayeredUpdates()

# classes
class Fond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("fond.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Avion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("avion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.centery = fenetre.get_rect().centery

# creation des sprites
fond = Fond()
avion = Avion()

# ajout des sprites a la liste
listes_des_srpites.add(fond)
listes_des_srpites.add(avion)

# affichage fenetre
listes_des_srpites.draw(fenetre)
pygame.display.flip()
pygame.key.set_repeat(1,0)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

    # affichage fenetre
    listes_des_srpites.draw(fenetre)
    pygame.display.flip()
pygame.quit()

