import pygame, sys
from pygame.locals import *

import pygame

pygame.init()
# 设置帧率
FPS = 30
ftpClock = pygame.time.Clock()

DISPLAYSURFACE = pygame.display.set_mode((1400, 1300), 0, 32)
pygame.display.set_caption("cat")

WHITE = (255, 255, 255)
# 加载图片，返回一个surface对象
catImage = pygame.image.load("cat.png")
cat_x = 10
cat_y = 10
direction = "right"

while True:
    DISPLAYSURFACE.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if direction == "right":
        cat_x += 5
        if cat_x == 180:
            direction == "down"
    elif direction == "down":
        cat_y += 5
        if cat_y == 120:
            direction == "left"
    elif direction == "left":
        cat_x -= 5
        if cat_x == 10:
            direction == "up"
    elif direction == "up":
        cat_y -= 5
        if cat_y == 10:
            direction == "right"
    # 将catImage图像，复制到Surface对象上
    DISPLAYSURFACE.blit(catImage, (cat_x, cat_y))
    pygame.display.update()
    ftpClock.tick(FPS)
