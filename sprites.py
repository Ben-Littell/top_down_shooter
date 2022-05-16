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
        self.bullet_g = pygame.sprite.Group()
        self.angle = 0

    def rotate(self, img):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * -self.angle
        img = pygame.transform.scale(img, (50, 50))
        self.image = pygame.transform.rotozoom(img, angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, img):
        bullet_img = pygame.image.load('assets/bullet.png')
        bullet_img = pygame.transform.scale(bullet_img, (5, 5))
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

        if keys[pygame.K_SPACE]:
            bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_img, self.angle)
            self.bullet_g.add(bullet)

        self.rect.x += self.x_velo
        self.rect.y += self.y_velo


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect(x=x, y=y)
        self.angle = angle
        self.speed = 6

    def update(self):
        velo_x = self.speed * math.cos(self.angle)
        velo_y = self.speed * math.sin(self.angle)

        self.rect.x += velo_x
        self.rect.y += velo_y

        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()
        elif self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()


class Level:
    def __init__(self, level_layout, tile_size):
        self.level_layout = level_layout
        self.tile_size = tile_size
