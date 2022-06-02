import pygame
import math
import random
from settings import *
from sprites import Player, Level, Enemies

# colors in RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
COLORS = [RED, GREEN, BLUE, BLACK]
PURPLE = (91, 10, 145)

# Math Constants
PI = math.pi

# Game Constants


##############################################################################
##############################################################################

pygame.init()


def main():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Animation Intro')

    clock = pygame.time.Clock()

    running = True
    ########################################################################################################################
    player_img = pygame.image.load('assets/Top_Down_Survivor/rifle/shoot/survivor-shoot_rifle_1.png')
    skeleton_a_imgs = [pygame.image.load(f'assets/top down zombies/skeleton-attack_{val}.png') for val in range(9)]
    skeleton_move_imgs = [pygame.image.load(f'assets/top down zombies/skeleton-move_{val}.png') for val in range(17)]
    player = Player(500, 400, player_img)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    tile_test = pygame.image.load('assets/tiles/grass.png')
    level1 = Level(LEVEL_1_back, tile_size)
    enemy_group = pygame.sprite.Group()
    # for numb in range(200):
    #     enem = Enemies(100 + 20 * numb, 100 + 10 * numb, skeleton_move_imgs, skeleton_a_imgs, 2)
    #     enemy_group.add(enem)
    health_bar_img = pygame.image.load('assets/healthbar.png')
    spawn_time = pygame.time.get_ticks()
    spawn_delay = 500

    ########################################################################################################################
    def spawn_enemies(enemy_g):
        now = pygame.time.get_ticks()
        side = random.randint(0, 4)
        if len(enemy_group) < 150:
            for numb in range(5):
                if side == 0:
                    enem = Enemies(20 * numb, -20, skeleton_move_imgs, skeleton_a_imgs, 2)
                    enemy_group.add(enem)
                elif side == 1:
                    enem = Enemies(WIDTH + 50, 20 * numb, skeleton_move_imgs, skeleton_a_imgs, 2)
                    enemy_group.add(enem)
                elif side == 2:
                    enem = Enemies(WIDTH + -20 * numb, HEIGHT + 20, skeleton_move_imgs, skeleton_a_imgs, 2)
                    enemy_group.add(enem)

    ########################################################################################################################
    # game loop
    prev_time = pygame.time.get_ticks()
    regen_delay = 1000
    score = 0
    while running:
        # get all mouse, keyboard, controller events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        now = pygame.time.get_ticks()
        if now - spawn_time >= spawn_delay:
            spawn_enemies(enemy_group)
            spawn_time = now
        level1.draw(screen)
        pygame.draw.rect(screen, PURPLE, (774, 10, (player.health * 0.756), 50))
        screen.blit(health_bar_img, (750, 10))
        player_group.draw(screen)
        player_group.update(player_img)
        player.bullet_g.draw(screen)
        player.bullet_g.update()
        enemy_group.draw(screen)
        enemy_group.update(skeleton_move_imgs, skeleton_a_imgs, player.rect.x, player.rect.y)

        enemy_bullet = pygame.sprite.groupcollide(enemy_group, player.bullet_g, True, True)
        if enemy_bullet:
            score += 5
        for enemy in enemy_group:
            enemy_player = pygame.sprite.spritecollideany(enemy, player_group,
                                                          collided=pygame.sprite.collide_rect_ratio(.75))
            now = pygame.time.get_ticks()
            if enemy_player:
                prev_time = now
                enemy.attack = True
                enemy.move = False
                damage_y = True
                if enemy.image_index_a == 6 and damage_y:
                    player.health -= 5
                    damage_y = False
                    if player.health <= 0:
                        player.kill()
                        print(score)
                elif enemy.image_index_a != 0:
                    damage_y = True
            else:
                enemy.attack = False
                enemy.move = True
                if player.health < 200 and player_group:
                    if now - prev_time >= regen_delay:
                        prev_time = now
                        player.health += 4
                        if player.health > 200:
                            player.health = 200

        pygame.display.flip()

        clock.tick(FPS)


# outside of game loop
main()
pygame.quit()
