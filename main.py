import pygame
from pygame.locals import *

# initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((800, 600), FULLSCREEN)
clock = pygame.time.Clock()
listes_des_srpites = pygame.sprite.LayeredUpdates()

# classes
class Avion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("avion.png").convert_alpha()
        self.rect = self.image.get_rect()
