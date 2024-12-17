from random import random

import pygame
from pygame.locals import *
import random

# initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((800, 650))
clock = pygame.time.Clock()
listes_des_sprites = pygame.sprite.LayeredUpdates()
liste_batiments = pygame.sprite.LayeredUpdates()
# classes
class Fond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("fond.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.75)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Nuages(pygame.sprite.Sprite):
    def __init__(self, nom_image):
        super().__init__()
        self.image = pygame.image.load(nom_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, fenetre.get_rect().right - self.rect.width)
        self.rect.y = random.randint(0, fenetre.get_rect().bottom - self.rect.height)


class Avion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("avion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.centery = fenetre.get_rect().centery

class Batiment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("batiment.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = 300





# creation des sprites
fond = Fond()
nuages = Nuages("nuage1.png"), Nuages("nuage2.png"), Nuages("nuage3.png")
avion = Avion()
batiment = Batiment()


# ajout des sprites a la liste
listes_des_sprites.add(fond)
listes_des_sprites.add(nuages)
listes_des_sprites.add(avion)
liste_batiments.add(batiment)



# affichage fenetre
listes_des_sprites.draw(fenetre)
pygame.display.flip()
pygame.key.set_repeat(1,0)



#batiment.rect.x -= 5

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

    # affichage fenetre
    listes_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

