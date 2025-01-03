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

    def deplacer(self):
        self.rect.x -= self.vitesse


class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.police = pygame.font.Font("BRADHITC.TTF", 108)
        self.image = self.police.render("Game Over !", True, "darkred", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.centery = fenetre.get_rect().centery


class Score(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.score = 0
        self.police = pygame.font.Font("BRADHITC.TTF", int(108 / 2))
        self.image = self.police.render(f"Score : {self.score}", True, "darkred", None)
        self.rect = self.image.get_rect()
        self.rect.centerx = fenetre.get_rect().centerx
        self.rect.y = y


class RectangleDeFond(pygame.sprite.Sprite):
    def __init__(self, x, y, longueur, hauteur):
        super().__init__()
        self.longueur = longueur
        self.hauteur = hauteur
        self.image = pygame.Surface((self.longueur, self.hauteur))
        self.image.fill("black")
        self.image.set_colorkey("black")
        self.rectangle = pygame.Rect(0, 0, self.longueur, self.hauteur)
        pygame.draw.rect(self.image, "antiquewhite", self.rectangle, 0)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
            liste_des_sprites.remove(nuage)
            liste_des_nuages.remove(nuage)
            nuage.kill()
            nouveau_nuage = Nuages(nom_nuages[random.randint(0,2)], 100)
            liste_des_sprites.add(nouveau_nuage)
            liste_des_nuages.add(nouveau_nuage)
    for batiment in liste_des_batiments:
        batiment.deplacer()
        if avion.rect.colliderect(batiment):
            continuer = False
        if batiment.rect.right <= fenetre.get_rect().centerx: ### a modifier
            nouveau_batiment = Batiment()
            liste_des_sprites.add(nouveau_batiment)
            liste_des_batiments.add(nouveau_batiment)
        if batiment.rect.right < 0:
            liste_des_sprites.remove(batiment)
            liste_des_batiments.remove(batiment)
            batiment.kill()
    avion.voler()
    # affichage fenetre
    liste_des_sprites.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)

# creation des sprites de resume de jeu
gameover = Gameover()
score = Score(gameover.rect.bottom)
rectangle_de_fond = RectangleDeFond(gameover.rect.x, gameover.rect.y, gameover.rect.width, gameover.rect.height + score.rect.height)

# ajout des sprites a la liste des sprites de resume
liste_des_sprites_de_resume.add(rectangle_de_fond)
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
