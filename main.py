#!/usr/bin/ven python3

import sys
import traceback

import pygame

import myplane
# import bullet
import enemy
# import supply

from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Battle -- Vincent")
background = pygame.image.load("images/background.png").convert()

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
        es = enemy.SmallEnemy(bg_size)
        group1.add(es)
        group2.add(es)

def add_mid_enemies(group1, group2, nums):
    for i in range(nums):
        em = enemy.MidEnemy(bg_size)
        group1.add(em)
        group2.add(em)

def add_big_enemies(group1, group2, nums):
    for i in range(nums):
        eb = enemy.BigEnemy(bg_size)
        group1.add(eb)
        group2.add(eb)


def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    mp = myplane.MyPlane(bg_size)

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

    clock = pygame.time.Clock()

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

        screen.blit(background, (0,0))

        # 绘制大型敌机
        for each in big_enemies:
            each.move()
            if switch_image:
                screen.blit(each.image1, each.rect)
            else:
                screen.blit(each.image2, each.rect)

            # 距离屏幕50像素，播放大型敌机音效
            if each.rect.bottom > -50:
                enemy3_fly_sound.play()

        # 绘制中型敌机
        for each in mid_enemies:
            each.move()
            screen.blit(each.image, each.rect)

        # 绘制小型敌机
        for each in small_enemies:
            each.move()
            screen.blit(each.image, each.rect)

        # 绘制我方飞机
        switch_image = not switch_image
        if switch_image:
            screen.blit(mp.image1, mp.rect)
        else:
            screen.blit(mp.image2, mp.rect)

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

