import pygame, sys
from pygame.locals import *

# 初始化
pygame.init()

# 创建Surface对象
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)

# 设置标题
pygame.display.set_caption("Drawing")

# 设置颜色对象
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# 填充Surface对象
DISPLAYSURF.fill(WHITE)
# 五边形
pygame.draw.polygon(DISPLAYSURF,GREEN,((146,0),(291,106),(236,277),(56,277),(0,106)))
# 线段
pygame.draw.line(DISPLAYSURF,BLUE,(60,60),(120,60),4)
pygame.draw.line(DISPLAYSURF,BLUE,(120,60),(60,120),4)
pygame.draw.line(DISPLAYSURF,BLUE,(60,120),(120,120),4)
# 圆形
pygame.draw.circle(DISPLAYSURF,BLUE,(300,50),20,0)
# 椭圆
pygame.draw.ellipse(DISPLAYSURF,RED,(300,250,40,80),1)
# 矩形
pygame.draw.rect(DISPLAYSURF,RED,(200,150,100,50))

# 锁定像素
pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK

pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK

# 删除PixelArray对象
del pixObj

# 主函数：响应事件，绘制画面
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
