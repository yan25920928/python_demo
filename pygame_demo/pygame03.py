import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 2
BOARDHEIGHT = 2
# 断言测试
assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0, "断言调试：确保 宽高可以形成偶数个方块"
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# R G B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
# 背景色常量
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHT = BLUE
# 图标类型常量
DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"
# 定义颜色和图标元组
ALLCOLOR = (GRAY, NAVYBLUE, WHITE, RED, GREEN, BLUE, YELLOW)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
# 断言 图标有足够多的颜色和形状
assert len(ALLCOLOR) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT


# 获取版面状态信息：：一个由元组组成元素的列表，其中，每个元组都有两个值，一个用于图标的形状，另一个用于图标的颜色
# 确保每种类型的图标有且只有两个
def getRandomizedBoard():
    # 获取所有图片的可能
    icons = []
    for color in ALLCOLOR:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    # 打乱并截取图标列表
    random.shuffle(icons)
    numIconUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # 获取可用图标个数
    icons = icons[:numIconUsed] * 2  # 确保图标总数是成对出现的
    random.shuffle(icons)  # 打乱图标

    # ******************************#
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


# 获取那块被遮住了——Boolean值的列表的一个列表
def generateRevealBoxesData(param):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([param] * BOARDHEIGHT)  # for 循环创造列
    return revealedBoxes


def drawBorad(mainBoard, revealedBoxes):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR,
                                 (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(mainBoard, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


# 面板中方块左上角在上笛卡尔坐标的位置
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


# 像素坐标转换为方块坐标
def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


# 绘制图标
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # 左上角坐标

    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, (
        (left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


# 绘制关闭的方块
def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR,
                             (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHT, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


# 获取形状和颜色
def getShapeAndColor(mainBoard, boxx, boxy):
    return mainBoard[boxx][boxy][0], mainBoard[boxx][boxy][1]


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def revealedBoxesAnimation(mainBoard, boxesToReveal):
    for coverage in range(BOXSIZE, -1, - REVEALSPEED):
        drawBoxCovers(mainBoard, boxesToReveal, coverage)


def coverBoxesAnimation(mainBoard, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(mainBoard, boxesToCover, coverage)


def startGameAnimation(board):
    coveredBoxes = generateRevealBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    # 揭开和盖住方块
    drawBorad(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealedBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(mainBoard):
    coveredBoxes = generateRevealBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        DISPLAYSURF.fill(color1)
        drawBorad(mainBoard, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


# 主函数，自顶而下的编程思维
def main():
    global FPSCLOCK, DISPLAYSURF  # 全局变量
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    pygame.display.set_caption("03")
    mainBoard = getRandomizedBoard()  # 获取版面状态信息
    revealedBoxes = generateRevealBoxesData(False)  # 获取那块被遮住了
    firstSelection = None  # 点击图标是记录，当标记为None时，表明用户是第一次点击；将图标的XY坐标当成一个元组存入到变量firstSelection中
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)  # 提示动画——闪现预览色彩和形状

    while True:  # 主循环
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBorad(mainBoard, revealedBoxes)  # 绘制版本
        pass

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:  # 光标移动事件
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == MOUSEMOTION:  # 光标点击后释放事件
                mousex, mousey = event.pos

        boxx, boxy = getBoxAtPixel(mousex, mousey)  # 获取鼠标位于其上方的方块的坐标
        if boxx != None and boxy != None:  # 如果鼠标光标方块之上（例如，如果它超出了游戏板的边界，或者它位于两个方块之间的间隙上），那么该函数返回元组(None,None)
            if not revealedBoxes[boxx][boxy]:  # 方块处于盖住，未点击状态。(通过读取revealedBoxes[boxx][boxy]中存储的值，检查这个方块是否被盖住了，如果为False——盖住状态)
                drawHighlightBox(boxx, boxy)  # 鼠标位于一个盖住的方块之上，绘制高亮边框，提示可以点击。如果已经打开，不会绘制这个高亮边框
            if not revealedBoxes[boxx][boxy] and mouseClicked:  # 方块处于盖住，且点击状态
                revealedBoxesAnimation(mainBoard, [(boxx, boxy)])  # 展示翻开动画
                revealedBoxes[boxx][boxy] = True  # 更新板面数据

                if firstSelection == None:  # 表明是第一块
                    firstSelection = (boxx, boxy)

                else:  # 点击的为第二块，检测图标的颜色，形状是否相同
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon2color != icon1color:  # 处理不一致的图标
                        pygame.time.wait(1000)  # 暂停1000毫秒
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])  # 播放关闭动画
                        # 标记两个方块，为关闭状态
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False

                    elif hasWon(revealedBoxes):  # 处理获胜
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        # 重新设置板面方块状态
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealBoxesData(False)
                        drawBorad(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                    firstSelection = None

        pygame.display.update()  # 绘制更新
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
