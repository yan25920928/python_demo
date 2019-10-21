import pygame,sys
from pygame.locals import *

# 初始化操作
pygame.init()

# 获取一个surface对象，set_mode传入一个元组数据，而不是两个整数
DISPLAYSURF = pygame.display.set_mode((300, 400))

# 显示顶部标题
pygame.display.set_caption("pygame_01")

# 开启主循环——处理事件（鼠标，键盘），更新状态（各种player相关的变量数值），绘制画面
while True:
    # 迭代响应事件列表
    for event in pygame.event.get():
        if event.type == QUIT:
            # 停止pygame
            pygame.quit()
            # 退出
            sys.exit()
    # 更新绘制
    pygame.display.update()
