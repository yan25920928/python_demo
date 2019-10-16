import pygame
from sys import exit
from random import randint

# 原理：视觉暂留(余晖效应)，静态画面快速连续播放，形成视觉上的连续活动画面

# 封装Bullt：初始化图片和位置，处理运动，状态激活重复利用等
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.PNG').convert_alpha()
        # 默认不激活
        self.active = False

    def move(self):
        # 激活状态下移动
        if self.active:
            self.y -= 3
        # 消失后，设置为冻结状态
        if self.y < 0:
            self.active = False

    # 重置位置与激活
    def restart(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        self.active = True

class Enemy:
    def __init__(self):
        self.restart()
        self.image = pygame.image.load("enemy.png")

    def restart(self):
        self.x = randint(50, 400)
        self.y = randint(-200, -50)

    def move(self):
        if self.y < 800:
            self.y += 0.1
        else:
            self.y = -50

# 检测是否命中：
def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width())\
            and((bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height())):
        enemy.restart()
        bullet.active = False
        return True
    return False

class Plane:
    def restart(self):
        self.x = 200
        self.y = 600
    def __init__(self):
        self.restart()
        self.image = pygame.image.load("plane.PNG").convert_alpha()
    def move(self):
        # 获取鼠标位置，显示图片
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2
        self.x = x
        self.y = y

# 检测是否撞机
def checkCrash(enemy, plane):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) \
            and (plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) \
            and (plane.y + 0.7 * plane.image.get_height() > enemy.y) \
            and (plane.y + 0.3 * plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((450,800), 0, 32)
pygame.display.set_caption("test_pygame")
background = pygame.image.load("pygame_test.jpg").convert()
score = 0
font = pygame.font.Font(None,32)

# 创建plane类
plane = Plane()
# Bullet类的调用与设置，通过list来管理
bullets = []
for i in range(5):
    bullets.append(Bullet())
count_b = len(bullets)
# 激活状态序号
index_b = 0
# 发射间隔
interval_b = 0

# list创建Enemy组
enemies = []
for i in range(5):
    enemies.append(Enemy())

gameover = False
# 主循环
while True:
    # 响应事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    # 绘制主背景
    screen.blit(background, (0, 0))
    # 没有撞机
    if not gameover:
        # 绘制plane
        plane.move()
        screen.blit(plane.image,(plane.x, plane.y))
        text = font.render("Score:%d" % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))
        # 绘制bullets 定时发射间隔，100
        interval_b -= 1
        if interval_b < 0:
            # 激活序列index_b的bullet
            bullets[index_b].restart()
            interval_b = 100
            # 更新index_b序列
            index_b = (index_b + 1) % count_b
        # 判断每个bullet状态，只绘制激活状态下的
        for bullet in bullets:
            if bullet.active:
                for e in enemies:
                    if checkHit(e,bullet):
                        score += 100
                bullet.move()
                screen.blit(bullet.image,(bullet.x,bullet.y))

        # 载入enemy组
        for enemy in enemies:
            if checkCrash(enemy, plane):
                gameover = True
            enemy.move()
            screen.blit(enemy.image,(enemy.x, enemy.y))
    else:
        text = font.render("Score:%d" % score, 1, (0, 0, 0))
        screen.blit(text, (50, 50))

    # 画面更新
    pygame.display.update()
