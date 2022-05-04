import pygame
from settings import *
import math
from pygame.math import Vector2 as vec


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

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotozoom(self.image, 45, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

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


        # mousex, mousey = pygame.mouse.get_pos()
        # # build a vector between player position and mouse position
        # moveVector = (self.rect.x-mousex, self.rect.y-mousey)
        # angle = math.atan2(moveVector[0], moveVector[1])
        # angle_d = angle * 180 / math.pi
        # print(angle_d)
        #
        # self.image = pygame.transform.rotate(self.image, int(angle_d))
        # self.rect = self.image.get_rect(center=self.rect.center)
        if keys[pygame.K_f]:
            self.rotate()
        self.rect.x += self.x_velo
        self.rect.y += self.y_velo


