import pygame,sys
from pygame.locals import *

# 初始化
pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("font text")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

# 创建Font对象 字体，字号
fontObj = pygame.font.Font("freesansbold.ttf",32)
# 创建Surface对象用来 绘制 文字内容，抗锯齿，字体颜色，底色
textSurfaceObj = fontObj.render("Font text!", True, GREEN, BLUE)
# 显示对象
textRectObj = textSurfaceObj.get_rect()
# 指定位置
textRectObj.center = (200, 150)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURFACE.fill(WHITE)
    DISPLAYSURFACE.blit(textSurfaceObj, textRectObj)
    pygame.display.update()