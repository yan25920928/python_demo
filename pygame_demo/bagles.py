import random
import logging

logging.basicConfig(level=logging.DEBUG)

# 位数
NUM_DIGITS = 3
# 次数
MAX_GUESS = 10


# 生成随机数
def getSecretNum():
    numbers = list(range(10))
    # 随机乱序
    random.shuffle(numbers)
    secretNum = ''
    for i in range(NUM_DIGITS):
        # 组成指定位数的数字串
        secretNum += str(numbers[i])
    return secretNum


# 获取提示: guess拆解成单个str，遍历secretNum，是否包含，是否位置正确
def getClues(guess, secretNum):
    if guess == secretNum:
        return "You get it!"
    clues = []
    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            clues.append('Fermi')
        elif guess[i] in secretNum:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'
    # 对提示进行排序，取消位置与线索关系，增加难度
    clues.sort()
    # 通过" "将clues元素连接起来，形成单个str
    return ' '.join(clues)


# 是否输入为数字
def isOnlyDigits(num):
    if num == "":
        return False
    for i in num:
        if i not in "0 1 2 3 4 5 6 7 8 9".split():
            return False
    return True


def playAgain():
    print("Do you want to play again? (yes or no)")
    return input().lower().startswith("y")


if __name__ == "__main__":
    print("I am thinking of a %s-digit number. Try to guess what is it" % NUM_DIGITS)
    print("Hera are some clues:")
    print("When I say:      That means:")
    print(" Pico            One digit correct but in the wrong position")
    print(" Fermi           One digit correct and in the right position")
    print(" Bagels          No digit is correct")

    while True:
        secretNum = getSecretNum()
        # secretNum = "123"
        print("I have thought up a number. You have %s guess to get it." % MAX_GUESS)
        numGuess = 1
        while numGuess <= MAX_GUESS:
            guess = ""
            while len(guess) != NUM_DIGITS or not isOnlyDigits(guess):
                print("Guess %s:" % numGuess)
                guess = input()
            print(getClues(guess, secretNum))
            numGuess += 1
            if guess == secretNum:
                break
        if numGuess > MAX_GUESS:
            print("you ran out of guess. The answer was %s." % secretNum)
        if not playAgain():
            break
