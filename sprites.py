import pygame
from settings import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_0.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.x_velo = 0
        self.y_velo = 0
        self.handgun = True

    def update(self):
        keys = pygame.key.get_pressed()
        self.x_velo = 0
        self.y_velo = 0
        if keys[pygame.K_w]:
            self.y_velo = -4
        elif keys[pygame.K_s]:
            self.y_velo = 4
        if keys[pygame.K_d]:
            self.x_velo = 4
        elif keys[pygame.K_a]:
            self.x_velo = -4

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                # build a vector between player position and mouse position
                moveVector = (mousex-self.rect.x, mousey-self.rect.y)
                angle = math.atan2(moveVector[0], moveVector[1])

                self.image = pygame.transform.rotate(self.image, angle)
        self.rect.x += self.x_velo
        self.rect.y += self.y_velo


