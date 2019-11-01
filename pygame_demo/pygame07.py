import pygame, sys, random, logging, time
from pygame.locals import *

logging.basicConfig(level=logging.DEBUG)

# 常量
FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20 # 砖块尺寸
BOARDWIDTH = 10 # 砖块的宽
BOARDHEIGHT = 20 # 砖块的高
BLANK = '.' # 黑背景块,空白空格值

# 移动速度
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

# 间距
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE # 界面颜色
BGCOLOR = BLACK # 背景色
TEXTCOLOR = WHITE # 文本颜色
TEXTSHADOWCOLOR = GRAY # 文本阴影颜色
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW) # 高亮颜色
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

# 模板的宽、高
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]
# 砖块形状
PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def makeTextObjs(text, font, color):
    # 获取文本对象,和文本的尺寸
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def showTextScreen(text):

    # 显示文本阴影信息
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 显示文本信息
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 显示提示信息
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pygame.display.update()
    FPSCLOCK.tick()


def getBlankBoard():
    # 获取界面数据, 由.组成的队列
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def calculateLevelAndFallFreq(score):
    # 根据得分动态计算等级和掉落频率
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


def getNewPiece():
    # 生成砖块随机形状和颜色
    shape = random.choice(list(PIECES.keys()))
    newPiece = {"shape": shape, "rotation": random.randint(0, len(PIECES[shape]) - 1),
                "color": random.randint(0, len(COLORS) - 1),
                "x": int(BOARDWIDTH / 2), "y": -2}
    return newPiece


def convertToPixelCoords(boxx, boxy):
    # 位置坐标转换为屏幕坐标
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # 根据界面数据数据绘制图像
    # 绘制边界
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR,(XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    # 绘制背景
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # 绘制单独的格子
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # 绘制状态，显示score和level
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)
    pass


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # 如果没有指定位置，则使用本身自带的储存的位置信息
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # 绘制砖块
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # 显示文本Next
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # 绘制砖块
    drawPiece(piece, pixelx=WINDOWWIDTH - 120, pixely=100)


def isOnBoard(x, y):
    # 判断位置是否在界面上
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # 判断是否存在有效位置——是否结束砖块掉落
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0 # = 和 < 同时使用？
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                False
    return True


def terminate():
    # 退出程序
    pygame.quit()
    sys.exit()


def checkForQuit():
    # 检测是否响应退出事件
    for event in pygame.event.get(QUIT): # 窗口退出事件
        terminate()
    for event in pygame.event.get(KEYUP): # 响应KEYUP事件
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # 继续传递其他的KEYUP事件

def runGame():
    # 获取界面数据
    board = getBlankBoard()
    logging.debug(board)
    # 初始变量设置，时间，方向，分数
    lastMoveDownTime, lastMoveSidewaysTime, lastFallTime = time.time(), time.time(), time.time()
    movingDown, movingLeft, movingRight = False, False, False
    score = 0

    # 设置砖块下落速度和时间
    level, fallFred = calculateLevelAndFallFreq(score)

    # 获取即将下落的组块，显示下一个即将生成的组块
    fallingPiece, nextPiece = getNewPiece(), getNewPiece()

    # 主循环
    while True:
        # 判断上方是否存在需要掉落的砖块
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()
            # 是否存在一个有效位置
            if not isValidPosition(board, fallingPiece):
                return
        # 事件监听
        checkForQuit()
        # 按键响应
        for event in pygame.event.get():
            # 响应KeyUP：P键 pause, Left(a)，Right(d)，Down(s)
            if event.type == KEYUP:
                if event.key == K_p:
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime, lastMoveDownTime, lastMoveSidewaysTime = time.time(), time.time(), time.time()
                elif ((event.key == K_LEFT) or (event.key == K_a)):
                    logging.debug("K_LEFT")
                    movingLeft = False
                elif ((event.key == K_RIGHT) or (event.key == K_d)):
                    logging.debug("K_RIGHT")
                    movingRight = False
                elif ((event.key == K_DOWN) or (event.key == K_s)):
                    logging.debug("K_DOWN")
                    movingDown = False
            # 响应KeyDown：Left(a)，Right(d)，Down(s)
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pass
                pass

        # 画面更新
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board) # 绘制主界面
        drawStatus(score, level) # 绘制状态
        drawNextPiece(nextPiece) # 绘制下一个出现的砖块
        if fallingPiece != None: # 如果即将掉落的砖块存在，则绘制出来
            drawPiece(fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main():
    # 主函数
    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    # 初始化操作，窗口设置
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption("pygame07")
    FPSCLOCK = pygame.time.Clock()
    # 显示开始时文本信息
    showTextScreen("Tetromino")
    # 主循环
    while True:
        # 随机播放不同的音乐
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
            logging.debug('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
            logging.debug('tetrisc.mid')

        pygame.mixer.music.play(-1, 0.0)
        # 运行游戏
        runGame()
        # 停止音乐
        pygame.mixer.music.stop()
        # 显示结束时文本信息
        showTextScreen("Game Over")

if __name__ == "__main__":
    main()