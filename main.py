import pygame
from pygame.locals import *
import random
import time

# initialisation de pygame
pygame.init()

fenetre = pygame.display.set_mode((800, 600)) #FULLSCREEN
clock = pygame.time.Clock()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_batiments = pygame.sprite.LayeredUpdates()
liste_des_nuages = pygame.sprite.LayeredUpdates()
liste_des_sprites_de_resume = pygame.sprite.LayeredUpdates()
temps_initial = time.time()

# classes
class Instructions:
    def __init__(self):
        self.height = fenetre.get_rect().height
        


class Ecriture:
    def __init__(self):
        self.police = pygame.font.Font(None, 14)



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
        self.vitesse += 0.2

    def monter(self):
        self.vitesse = -5


class Batiment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("batiment.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = fenetre.get_rect().right
        self.rect.y = random.randint(300,fenetre.get_rect().bottom)
        self.vitesse = 5

    def deplacer(self):
        self.rect.x -= self.vitesse


class BatimentsRenverses(Batiment):
    def __init__(self, batiment_du_dessous):
        super().__init__()
        self.image = pygame.image.load("batiment_renversé.png").convert_alpha()
        self.rect.y = batiment_du_dessous.rect.y - self.rect.height - 200


class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.police = pygame.font.Font("LATINWD.TTF", 60)
        self.image = self.police.render("Game Over !", True, "royalblue4", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.centery = fenetre.get_rect().centery


class Score(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.score = int(time.time() - temps_initial) 
        self.police = pygame.font.Font("LATINWD.TTF", 40)
        self.image = self.police.render(f"Score : {self.score}", True, "royalblue4", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.y = y


# creation des sprites
fond = Fond()
nom_nuages = ["nuage1.png", "nuage2.png", "nuage3.png"]
nuages = []
for nuage in nom_nuages:
    nuages.append(Nuages(nuage, 100))
batiment = Batiment()
batiment_renverse = BatimentsRenverses(batiment)
avion = Avion()

# ajout des sprites a la liste
liste_des_sprites.add(fond)

for nuage in nuages:
    liste_des_sprites.add(nuage)
    liste_des_nuages.add(nuage)

liste_des_batiments.add(batiment)
liste_des_sprites.add(batiment)
liste_des_batiments.add(batiment_renverse)
liste_des_sprites.add(batiment_renverse)

liste_des_sprites.add(avion)

# parametrage du clavier
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
            liste_des_sprites.remove(nuage)
            liste_des_nuages.remove(nuage)
            nuage.kill()
            nouveau_nuage = Nuages(nom_nuages[random.randint(0,2)], 100)
            liste_des_sprites.add(nouveau_nuage)
            liste_des_nuages.add(nouveau_nuage)

    # gestion des batiment
    for bat in liste_des_batiments:
        batiment.deplacer()
        batiment_renverse.deplacer()
        if avion.rect.colliderect(bat.rect):
            continuer = False
        """
        if bat.rect.x == fenetre.get_rect().centerx:
            nouveau_batiment = Batiment()
            nouveau_batiment_renverse = BatimentsRenverses(nouveau_batiment)
            liste_des_batiments.add(nouveau_batiment)
            liste_des_sprites.add(nouveau_batiment)
            liste_des_batiments.add(nouveau_batiment_renverse)
            liste_des_sprites.add(nouveau_batiment_renverse)"""
        if bat.rect.right < 0:
            bat.kill()

    avion.voler()

    # affichage fenetre
    liste_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)

# creation des sprites de resume de jeu
gameover = Gameover()
score = Score(gameover.rect.bottom)

# ajout des sprites a la liste des sprites de resume
liste_des_sprites_de_resume.add(gameover)
liste_des_sprites_de_resume.add(score)

quitter = False
while not quitter:
    for event in pygame.event.get():
        if event.type == QUIT:
            quitter = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quitter = True
    # affichage du resume
    liste_des_sprites_de_resume.draw(fenetre)
    pygame.display.flip()

pygame.quit()
