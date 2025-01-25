from time import sleep

import pygame
from pygame.locals import *
import random
import time

# initialisation de pygame
pygame.init()

fenetre = pygame.display.set_mode((800, 600)) #FULLSCREEN
clock = pygame.time.Clock()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_instructions = pygame.sprite.LayeredUpdates()
liste_des_batiments = pygame.sprite.LayeredUpdates()
liste_des_batiments_renverses = pygame.sprite.LayeredUpdates()
liste_des_nuages = pygame.sprite.LayeredUpdates()
liste_des_sprites_de_resume = pygame.sprite.LayeredUpdates()
temps_initial = time.time()

# classes
class Instructions(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fenetre.fill("white")
        self.police = pygame.font.Font("LATINWD.TTF", 20)
        self.texte = "Appuyez sur espace pour commencer à jouer !"
        self.image = self.police.render(self.texte, True, "royalblue4", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.centery = fenetre.get_rect().centery


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
        self.rect.x = fenetre.get_rect().right
        self.rect.y = random.randint(50, 200)
        self.vitesse = random.randint(1,3)

    def deplacer(self):
        self.rect.x -= self.vitesse


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
    def __init__(self, vitesse):
        super().__init__()
        self.image = pygame.image.load("batiment.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = fenetre.get_rect().right
        self.rect.y = random.randint(200,fenetre.get_rect().bottom)
        self.vitesse = vitesse

    def deplacer(self):
        self.rect.x -= self.vitesse


class BatimentsRenverses(Batiment):
    def __init__(self, vitesse, batiment_du_dessous):
        super().__init__(vitesse)
        self.image = pygame.image.load("batiment_renversé.png").convert_alpha()
        self.rect.bottom = batiment_du_dessous.rect.y - 250


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
        self.score = int((time.time() - temps_initial)/5)
        self.police = pygame.font.Font("LATINWD.TTF", 40)
        self.image = self.police.render(f"Score : {self.score}", True, "royalblue4", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.y = y

# vitesse initiale de tous les batiments
v = 5

# creation des sprites
regles = Instructions()
fond = Fond()
nom_nuages = ["nuage1.png", "nuage2.png", "nuage3.png"]
nuages = []
for nuage in nom_nuages:
    nuages.append(Nuages(nuage))
batiment = Batiment(v)
batiment_renverse = BatimentsRenverses(v, batiment)
avion = Avion()

# ajout des sprites a la liste
liste_des_instructions.add(regles)
liste_des_sprites.add(fond)

liste_des_batiments.add(batiment)
liste_des_sprites.add(batiment)
liste_des_batiments_renverses.add(batiment_renverse)
liste_des_sprites.add(batiment_renverse)

liste_des_sprites.add(avion)

for nuage in nuages:
    liste_des_sprites.add(nuage)
    liste_des_nuages.add(nuage)

# parametrage du clavier
pygame.key.set_repeat(1,0)

# variables pour la continuation du jeu
instruction = True
continuer = True
quitter = False

# affichage des regles
while instruction:
    for event in pygame.event.get():
        if event.type == QUIT:
            instruction = False
            continuer = False
            quitter = True
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                instruction = False
    liste_des_instructions.draw(fenetre)
    pygame.display.flip()

# boucle de jeu
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
            quitter = True
        if event.type == KEYDOWN:
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
            nouveau_nuage = Nuages(nom_nuages[random.randint(0,2)])
            liste_des_sprites.add(nouveau_nuage)
            liste_des_nuages.add(nouveau_nuage)

    # augmentattion de la vitesse de tous les batiments
    v += 0.001

    # gestion des batiments
    for bat in liste_des_batiments:
        bat.deplacer()
        if avion.rect.colliderect(bat.rect):
            continuer = False
        if bat.rect.right < 0:
            liste_des_batiments.remove(bat)
            liste_des_sprites.remove(bat)
            bat.kill()
            nouveau_batiment = Batiment(v)
            liste_des_batiments.add(nouveau_batiment)
            liste_des_sprites.add(nouveau_batiment)
    for bat_renv in liste_des_batiments_renverses:
        bat_renv.deplacer()
        if avion.rect.colliderect(bat_renv.rect):
            continuer = False
        if bat_renv.rect.right < 0:
            liste_des_batiments_renverses.remove(bat_renv)
            liste_des_sprites.remove(bat_renv)
            bat_renv.kill()
            nouveau_batiment_renverse = BatimentsRenverses(v, nouveau_batiment)
            liste_des_batiments_renverses.add(nouveau_batiment_renverse)
            liste_des_sprites.add(nouveau_batiment_renverse)

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

# figeage de la fenetre
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
