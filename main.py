#!/usr/bin/ven python3

""" Main Framework """

import sys
import traceback

import pygame
from pygame.locals import *

import myplane
import bullet
import enemy
# import supply

pygame.init()
pygame.mixer.init()

BG_SIZE = width, height = 480, 700
screen = pygame.display.set_mode(BG_SIZE)
pygame.display.set_caption("Aircraft Battle -- Vincent")
background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load Musics
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, nums):
    for i in range(nums):
        es = enemy.SmallEnemy(BG_SIZE)
        group1.add(es)
        group2.add(es)

def add_mid_enemies(group1, group2, nums):
    for i in range(nums):
        em = enemy.MidEnemy(BG_SIZE)
        group1.add(em)
        group2.add(em)

def add_big_enemies(group1, group2, nums):
    for i in range(nums):
        eb = enemy.BigEnemy(BG_SIZE)
        group1.add(eb)
        group2.add(eb)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    mp = myplane.MyPlane(BG_SIZE)

    # 生成敌方飞机
    enemies = pygame.sprite.Group()

    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUMS = 4
    [bullet1.append(bullet.Bullet1(mp.rect.midtop)) for b in range(BULLET1_NUMS)]

    clock = pygame.time.Clock()

    # 用户得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 30)


    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_images = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1

    # 设置全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_nums = 3

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    mp_destroy_index = 0

    # 用于切换飞机形态(两张同样尺寸的图片)
    switch_image = True

    # 用于延迟
    delay = 100

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_images
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_nums:
                        bomb_nums -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.alive = False


        # 根据用户的得分增加游戏难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机，2架中型敌机和一架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        screen.blit(background, (0,0))

        if not paused:
            # 检测用户键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                mp.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                mp.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                mp.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                mp.moveRight()

            # 发射子弹
            if not (delay % 10):
                bullet1[bullet1_index].reset(mp.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUMS

            # 检测子弹是否击中敌机
            for b1 in bullet1:
                if b1.active:
                    b1.move()
                    screen.blit(b1.image, b1.rect)
                    hit_enemies = pygame.sprite.spritecollide(b1, enemies, False, pygame.sprite.collide_mask)

                    if hit_enemies:
                        b1.artive = False
                        for he in hit_enemies:
                            if he in mid_enemies or he in big_enemies:
                                he.hit = True
                                he.energy -= 1

                                if he.energy == 0:
                                    he.alive = False
                            else:
                                he.alive = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.alive:
                    each.move()

                    if each.hit:
                        # 绘制被击中的图片
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top -5), (each.rect.right, each.rect.top - 5), 2)

                    # 当生命值大于 20% 时显示为红色，否则显示为红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                    (each.rect.left, each.rect.top -5),
                                    (each.rect.left + each.rect.width * energy_remain, each.rect.top -5), 2)

                    # 距离屏幕50像素，播放大型敌机音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play()
                else:
                    # Destroy
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_down_sound.stop()
                            score += 10000
                            each.reset()


            # 绘制中型敌机
            for each in mid_enemies:
                if each.alive:
                    each.move()

                    if each.hit:
                        # 绘制被击中的图片
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top -5), (each.rect.right, each.rect.top - 5), 2)

                    # 当生命值大于 20% 时显示为红色，否则显示为红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                    (each.rect.left, each.rect.top -5),
                                    (each.rect.left + each.rect.width * energy_remain, each.rect.top -5), 2)
                else:
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            enemy2_down_sound.stop()
                            score += 6000
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.alive:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            enemy1_down_sound.stop()
                            score += 1000
                            each.reset()

            # 检测我文飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(mp, enemies, False, pygame.sprite.collide_mask)
            if enemies_down:
                mp.alive = False
                for e in enemies_down:
                    e.alive = False

            # 绘制我方飞机
            switch_image = not switch_image
            if mp.alive:
                if switch_image:
                    screen.blit(mp.image1, mp.rect)
                else:
                    screen.blit(mp.image2, mp.rect)
            else:
                if mp_destroy_index == 0:
                    me_down_sound.play()
                if not (delay % 3):
                    screen.blit(each.destroy_images[mp_destroy_index], mp.rect)
                    mp_destroy_index = (mp_destroy_index + 1) % 4
                    if mp_destroy_index == 0:
                        me_down_sound.stop()
                        # mp.reset()
                        mp.alive = True
                        print("Game Over...")
                        # running = False

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("x %d" % bomb_nums, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

        # 绘制得分
        score_text = score_font.render("Score : %s" % str(score), True, WHITE)
        screen.blit(score_text, (10, 2))

        # 绘制暂停按钮
        screen.blit(paused_image, pause_rect)

        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

