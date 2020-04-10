import pygame

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        # 底部状态栏 60 个像素
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.speed = 10

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        bottom = self.height - 60
        if self.rect.bottom < bottom:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = bottom

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
