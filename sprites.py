import pygame
from settings import *
import math
from pygame.math import Vector2 as vec


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = img
        self.speed = 3
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.x_velo = 0
        self.y_velo = 0
        self.handgun = True

    def rotate(self, img):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        img = pygame.transform.scale(img, (50, 50))
        self.image = pygame.transform.rotozoom(img, angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, img):
        keys = pygame.key.get_pressed()
        self.x_velo = 0
        self.y_velo = 0
        if keys[pygame.K_w]:
            self.y_velo = -1 * self.speed
        elif keys[pygame.K_s]:
            self.y_velo = self.speed
        if keys[pygame.K_d]:
            self.x_velo = self.speed
        elif keys[pygame.K_a]:
            self.x_velo = -1 * self.speed

        if pygame.MOUSEMOTION:
            self.rotate(img)
        self.rect.x += self.x_velo
        self.rect.y += self.y_velo

        if keys[pygame.K_SPACE]:
            pass


