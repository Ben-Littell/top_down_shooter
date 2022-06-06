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
def read_hi_score():
    with open("score.txt", "r") as f:
        hi_score = f.readline()
    return hi_score


def write_hi_score(score):
    with open("score.txt", "w") as f:
        f.write(score)
##############################################################################


pygame.init()


def start_screen():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Zombie Survivor')
    clock = pygame.time.Clock()
    running = True
    level = Level(LEVEL_1_back, tile_size)
    while running:
        # get all mouse, keyboard, controller events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key is pygame.K_RETURN:
                    running = False

        screen.fill(BLACK)
        level.draw(screen)
        title = arial.render(f'Welcome to Zombie Survivor', True, WHITE)
        title_rect = title.get_rect()
        title_rect.center = 300, 20
        screen.blit(title, title_rect)
        start = arial.render(f'Press Enter to start', True, WHITE)
        start_rect = start.get_rect()
        start_rect.center = 300, 100
        screen.blit(start, start_rect)
        pygame.display.flip()

        clock.tick(FPS)

def game_over():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()
    running = True
    level = Level(LEVEL_1_back, tile_size)
    while running:
        # get all mouse, keyboard, controller events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key is pygame.K_RETURN:
                    running = False
                if event.key is pygame.K_q:
                    quit()

        screen.fill(BLACK)
        level.draw(screen)
        game_done = arial.render(f'Game Over', True, WHITE)
        game_rect = game_done.get_rect()
        game_rect.center = 300, 20
        screen.blit(game_done, game_rect)
        exit_game = arial.render(f'Press Q to Exit', True, WHITE)
        exit_rect = exit_game.get_rect()
        exit_rect.center = 300, 100
        screen.blit(exit_game, exit_rect)
        restart_game = arial.render(f'Press Enter to Restart', True, WHITE)
        restart_rect = restart_game.get_rect()
        restart_rect.center = 300, 180
        screen.blit(restart_game, restart_rect)
        with open('score.txt') as file:
            line = file.readline()
            score_game = arial.render(f'High Score: {line}', True, WHITE)
            score_rect = score_game.get_rect()
            score_rect.center = 300, 260
            screen.blit(score_game, score_rect)
        pygame.display.flip()

        clock.tick(FPS)


def main():
    game_over = False
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
        score_txt = arial.render(f'Score: {score}', True, WHITE)
        score_rect = score_txt.get_rect(x=20, y=30)
        screen.blit(score_txt, score_rect)

        enemy_bullet = pygame.sprite.groupcollide(enemy_group, player.bullet_g, True, True)
        if enemy_bullet:
            score += 1
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
                        game_over = True
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
        if len(enemy_group) >= 195:
            for enemy in enemy_group:
                if not enemy.attack:
                    enemy.speed = 4

        pygame.display.flip()

        clock.tick(FPS)
        if game_over:
            high_score = read_hi_score()
            if score > int(high_score):
                write_hi_score(str(score))
            running = False


# outside of game loop
start_screen()
while True:
    main()
    game_over()
pygame.quit()
