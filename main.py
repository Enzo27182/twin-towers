import pygame
from pygame.locals import *
import random

# initialisation de pygame
pygame.init()

fenetre = pygame.display.set_mode((800, 600)) #FULLSCREEN
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

# creation des variables de stockage
dernier_batiment = batiment

# ajout des sprites a la liste
liste_des_sprites.add(fond)
for nuage in nuages:
    liste_des_sprites.add(nuage)
    liste_des_nuages.add(nuage)
liste_des_sprites.add(batiment)
liste_des_batiments.add(batiment)
liste_des_sprites.add(avion)

# parametrage du calvier
pygame.key.set_repeat(1,0)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
            if event.key == K_SPACE:
                avion.monter()
    if avion.rect.bottom >= fenetre.get_rect().bottom or avion.rect.top <= 0:
        continuer = False
    for nuage in liste_des_nuages:
        nuage.deplacer()
        if nuage.rect.right < 0:
            nuage.remove(liste_des_sprites)
            nuage.remove(liste_des_nuages)
            nuage.kill()
        while len(liste_des_nuages) < 3:
            cloud = Nuages(nom_nuages[random.randint(0,2)], 100)
            cloud.add(liste_des_sprites)
            cloud.add(liste_des_nuages)
    for batiment in liste_des_batiments:
        if avion.rect.colliderect(batiment):
            continuer = False
        if batiment.rect.right < 0:
            batiment.remove(liste_des_sprites)
            batiment.remove(liste_des_batiments)
            batiment.kill()
    if dernier_batiment.rect.right == fenetre.get_rect().centerx:
        batiment = Batiment()
        dernier_batiment = batiment
        liste_des_sprites.add(batiment)
        liste_des_batiments.add(batiment)
    avion.voler()
    batiment.deplacement()

    # affichage fenetre
    liste_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)

quitter = False
while not quitter:
    for event in pygame.event.get():
        if event.type == QUIT:
            quitter = True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            quitter = True
pygame.quit()
