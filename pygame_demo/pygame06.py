import logging, pygame, sys, random
from pygame.locals import *

logging.basicConfig(level=logging.DEBUG)

# 设置常量
FPS = 3
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20 # 网格尺寸

# assert与logging都比print要好
assert WINDOWHEIGHT % CELLSIZE == 0
assert WINDOWWIDTH % CELLSIZE == 0

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
DARKGREEN   = (0, 155, 0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head


def drawPressKeyMsg():
    logging.debug("绘制Msg信息")
    pressKeySurf = BASICFONT.render("Press a key to play", True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect() # TODO: ???
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showStartScreen():
    logging.debug("初始化屏幕")

    # 创建Font对象，设置显示内容
    titleFont = pygame.font.Font('freesansbold.ttf',100)
    titleSurf1 = titleFont.render("Welcome 06", True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render("Welcome 06", True, GREEN)

    # 设置角度
    degrees1 = 0
    degrees2 = 0

    # 开启循环
    while True:

        DISPLAYSURF.fill(BGCOLOR) # 填充背景色

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)  # 生成翻转对象
        rotatedRect1 = rotatedSurf1.get_rect()  # 绘制矩形背景
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2) # 设置角度
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1) # 绘制到Surface对象上

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect1)

        # 绘制文本信息
        drawPressKeyMsg()

        # 检测按键
        if(checkForKeyPress()):
            pygame.event.get()
            return
        # 界面更新
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def getRandomLocation():
    return {'x': random.randint(0, CELLSIZE - 1), 'y': random.randint(0, CELLSIZE - 1)}

# 绘制界面表格
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

# 绘制条状物
def drawWorm(wormCoords):
    logging.debug("绘制条状物")
    logging.debug(wormCoords)
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


# 绘制Apple
def drawApple(apple_coord):
    logging.debug("绘制apple")
    x = apple_coord['x'] * CELLSIZE
    y = apple_coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


# 显示分数
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def runGame():
    logging.debug("开始运行")

    # 随机一个初始位置
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    # 设置方向
    direction = RIGHT

    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    apple = getRandomLocation()
    # 主循环
    while True:
        # 事件监听
        for event in pygame.event.get(): # 退出监听
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN: # 按键监听，确保虫子不会自己碰到自己
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif (event.key == K_ESCAPE):
                    terminate()

        # 控制方向移动，状态更新，通过insert方法组成新的头部
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead) # 插入

        # 结束逻辑：碰撞检测——头部移动到格栅以外，或者头部移动到身体所在的位置
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # 虫子头部与苹果坐标重合，则随机生成新的一个苹果；如果没有就删除虫子身体的最后一个的位置坐标
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # 界面绘制
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pass

# 显示结束：Surf-Rect-Rect.topleft-DISPLAYSURF.blit(Surf, Rect)
def showGameOverScreen():
    logging.debug("显示结束")
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)

    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render("Over", True, WHITE)

    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

# 检测按键,检测事件队列中是否有QUIT事件，按键抬起检测是否为ESCAPE
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# 终止程序
def terminate():
    pygame.quit()
    sys.exit()

# 主函数
def main():
    # 全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    # 初始化操作
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("pygame06")

    # 程序开始，初始化屏幕
    # showStartScreen()

    # 主循环
    while True:
        # runGame()
        # 程序结束，显示图片
        showGameOverScreen()

if __name__ == "__main__":
    main()
