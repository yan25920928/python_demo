import pygame, sys, logging, random,time
from pygame.locals import *

logging.basicConfig(level=logging.DEBUG)

# 设置常量
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4  # seconds before game over if no button is pushed.
# 设置色值
#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

# 间距坐标
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# 绘制矩形对象，指定色彩和大小
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE,
                        BUTTONSIZE)
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')
    # 设置显示字体
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1,
                                DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # 加载音频软件
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # 定义game中需要使用的一些变量
    pattern = []  # 颜色图案
    currentStep = 0  # 下一轮颜色准备
    lastClickTime = 0  # 最后按键的时间戳
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False
    while True:

        clickedButton = None  # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)
        # 绘制按钮
        drawButtons()

        # 显示score，位于左上角
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        DISPLAYSURF.blit(infoSurf, infoRect)

        # 响应事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # 根据鼠标位置获取按钮所在的颜色块
                clickedButton = getButtonClicked(mousex, mousey)
                # logging.debug("鼠标响应%s"%clickedButton)
                logging.debug(clickedButton)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                logging.debug(clickedButton)
        # 等待状态时
        if not waitingForInput:
            logging.debug("等待状态时")
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN))) # 随机颜色
            logging.debug(pattern)
            # 闪烁色彩快
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # 等待用户输入
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0  # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (
                    currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# 结束时动画
def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time, roughly.
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                # checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# 改变背景色动画
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        # checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons() # redraw the buttons on top of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


# 绘制按钮
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

# 颜色块闪烁动画
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()

    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            # checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

# 获取数据点击所属的颜色块
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE

    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None


import matplotlib.pyplot as plt
import numpy


# 绘制折线图
def show_plt():
    x = numpy.arange(0, 7, 1)
    y = numpy.random.rand(len(x))
    # plt.plot(x[::4],y[::4],marker = "o")
    plt.plot(x, y, marker="o")
    plt.show()


if __name__ == "__main__":
    main()
    # show_plt()
