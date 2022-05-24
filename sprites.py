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
        self.bullet_prev = pygame.time.get_ticks()
        self.bullet_delay = 200

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

        mouse_press = pygame.mouse.get_pressed(3)
        current_time = pygame.time.get_ticks()
        if mouse_press[0] and current_time - self.bullet_delay >= self.bullet_prev:
            bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_img, self.angle)
            self.bullet_g.add(bullet)
            self.bullet_prev = current_time

        if self.rect.left + self.x_velo <= 0:
            self.x_velo = 0
        elif self.rect.right + self.x_velo >= WIDTH:
            self.x_velo = 0
        if self.rect.top + self.y_velo <= 0:
            self.y_velo = 0
        elif self.rect.bottom + self.y_velo >= HEIGHT:
            self.y_velo = 0

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


class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, img_m, img_a, speed):
        pygame.sprite.Sprite.__init__(self)
        self.move_imgs = [pygame.transform.scale(img, (50, 50)) for img in img_m]
        self.attack_imgs = [pygame.transform.scale(img, (50, 50)) for img in img_a]
        self.image = self.move_imgs[0]
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


class Level:
    def __init__(self, level_layout, tile_size):
        self.level_layout = level_layout
        self.tile_size = tile_size
        self.tile_list_back = []
        grass = pygame.image.load('assets/tiles/grass.png')
        grass = pygame.transform.scale(grass, (tile_size, tile_size))
        g_b_s_180 = pygame.image.load('assets/tiles/grass-beach0/straight/180/0.png')
        g_b_s_180 = pygame.transform.scale(g_b_s_180, (tile_size, tile_size))
        g_b_s_270 = pygame.image.load('assets/tiles/grass-beach0/straight/270/0.png')
        g_b_s_270 = pygame.transform.scale(g_b_s_270, (tile_size, tile_size))
        g_b_s_0 = pygame.image.load('assets/tiles/grass-beach0/straight/0/0.png')
        g_b_s_0 = pygame.transform.scale(g_b_s_0, (tile_size, tile_size))
        g_b_s_90 = pygame.image.load('assets/tiles/grass-beach0/straight/90/0.png')
        g_b_s_90 = pygame.transform.scale(g_b_s_90, (tile_size, tile_size))
        g_b_ci_90 = pygame.image.load('assets/tiles/grass-beach0/curve_in/90/0.png')
        g_b_ci_90 = pygame.transform.scale(g_b_ci_90, (tile_size, tile_size))
        g_b_ci_0 = pygame.image.load('assets/tiles/grass-beach0/curve_in/0/0.png')
        g_b_ci_0 = pygame.transform.scale(g_b_ci_0, (tile_size, tile_size))
        g_b_ci_180 = pygame.image.load('assets/tiles/grass-beach0/curve_in/180/0.png')
        g_b_ci_180 = pygame.transform.scale(g_b_ci_180, (tile_size, tile_size))
        g_b_ci_270 = pygame.image.load('assets/tiles/grass-beach0/curve_in/270/0.png')
        g_b_ci_270 = pygame.transform.scale(g_b_ci_270, (tile_size, tile_size))
        water = pygame.image.load('assets/tiles/water.png')
        water = pygame.transform.scale(water, (tile_size, tile_size))

        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * tile_size
                y_val = i * tile_size
                if col == '0':
                    img_rect = water.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (water, img_rect)
                    self.tile_list_back.append(tile)
                elif col == "1":
                    img_rect = grass.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (grass, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '2':
                    img_rect = g_b_s_180.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_s_180, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '3':
                    img_rect = g_b_s_270.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_s_270, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '4':
                    img_rect = g_b_s_0.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_s_0, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '5':
                    img_rect = g_b_s_90.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_s_90, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '6':
                    img_rect = g_b_ci_90.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_ci_90, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '7':
                    img_rect = g_b_ci_0.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_ci_0, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '8':
                    img_rect = g_b_ci_180.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_ci_180, img_rect)
                    self.tile_list_back.append(tile)
                elif col == '9':
                    img_rect = g_b_ci_270.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (g_b_ci_270, img_rect)
                    self.tile_list_back.append(tile)

    def draw(self, screen):
        for tile in self.tile_list_back:
            screen.blit(tile[0], tile[1])

