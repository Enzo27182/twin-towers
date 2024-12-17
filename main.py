import pygame
from pygame.key import get_mods
from pygame.locals import *

# initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((800, 600),FULLSCREEN)
clock = pygame.time.Clock()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_batiments = pygame.sprite.LayeredUpdates()

# classes
class Fond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("fond.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.5)
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
        self.vitesse = 0

    def voler(self):
        self.rect.y += self.vitesse
        self.vitesse += 0.1

    def monter(self):
        self.vitesse = -5

class Batiment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("batiment.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 600

# creation des sprites
fond = Fond()
avion = Avion()
batiment = Batiment()

# ajout des sprites a la liste
liste_des_sprites.add(fond)
liste_des_sprites.add(avion)
liste_des_sprites.add(batiment)

# affichage fenetre
liste_des_sprites.draw(fenetre)
pygame.display.flip()
pygame.key.set_repeat(1,0)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
            if event.key == K_SPACE:
                avion.monter()

    avion.voler()

    # affichage fenetre
    liste_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)
    if avion.rect.bottom >= fenetre.get_rect().bottom:
        continuer = False
quitter = False
while not quitter:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            quitter = True
pygame.quit()

