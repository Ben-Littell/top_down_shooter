import pygame
import math
import random
from settings import *
from sprites import Player, Level

# colors in RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
COLORS = [RED, GREEN, BLUE, BLACK]

# Math Constants
PI = math.pi

# Game Constants


##############################################################################
##############################################################################

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Animation Intro')

clock = pygame.time.Clock()

running = True
########################################################################################################################
player_img = pygame.image.load('assets/Top_Down_Survivor/rifle/shoot/survivor-shoot_rifle_1.png')
player = Player(500, 400, player_img)
player_group = pygame.sprite.Group()
player_group.add(player)
tile_test = pygame.image.load('assets/tiles/grass.png')
level1 = Level(LEVEL_1_back, tile_size)
########################################################################################################################
# game loop
while running:
    # get all mouse, keyboard, controller events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    level1.draw(screen)
    player_group.draw(screen)
    player_group.update(player_img)
    player.bullet_g.draw(screen)
    player.bullet_g.update()
    pygame.display.flip()

    clock.tick(FPS)

# outside of game loop
pygame.quit()






