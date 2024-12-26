import pygame
from pygame.locals import *
import random

# initialisation de pygame
pygame.init()

fenetre = pygame.display.set_mode((800, 600),FULLSCREEN)
clock = pygame.time.Clock()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_batiments = pygame.sprite.LayeredUpdates()
liste_des_nuages = pygame.sprite.LayeredUpdates()

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
    def __init__(self, nom_image, y):
        super().__init__()
        self.image = pygame.image.load(nom_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = fenetre.get_rect().right
        self.rect.y = y
        self.vitesse = - random.randint(1,4)

    def deplacer(self):
        self.rect.x += self.vitesse


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
        self.rect.x = fenetre.get_rect().right
        self.rect.y = 300
        self.vitesse = 5
        #self.rect.y = fenetre.get_rect().bottom - self.rect.height

    def deplacement(self):
        self.rect.x -= self.vitesse


# creation des sprites
fond = Fond()
nom_nuages = ["nuage1.png", "nuage2.png", "nuage3.png"]
nuages = []
for nuage in nom_nuages:
    nuages.append(Nuages(nuage, 100))
avion = Avion()
batiment = Batiment()


# ajout des sprites a la liste

liste_des_sprites.add(fond)

for nuage in nuages:
    liste_des_sprites.add(nuage)
    liste_des_nuages.add(nuage)
liste_des_sprites.add(batiment)
liste_des_batiments.add(batiment)
liste_des_sprites.add(avion)

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
    for nuage in nuages:
        nuage.deplacer()
        if nuage.rect.right < 0:
            nuage.kill()
            nuage.remove(liste_des_sprites)
            nuage.remove(liste_des_nuages)
        while len(liste_des_nuages) < 3:
            cloud = Nuages(nom_nuages[random.randint(0,2)], 100)
            cloud.add(liste_des_sprites)
            cloud.add(liste_des_nuages)
    avion.voler()
    batiment.deplacement()

    # affichage fenetre
    liste_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)
    if avion.rect.bottom > fenetre.get_rect().bottom:
        continuer = False
quitter = False
while not quitter:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            quitter = True
pygame.quit()

