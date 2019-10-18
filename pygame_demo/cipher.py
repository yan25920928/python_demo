import logging
# logging.basicConfig(level=logging.DEBUG)
# 凯撒密码，ASCII，ord() chr()

MAX_KEY_SIZE = 26

def getMode():
    while True:
        print("Do you wish to encrypt or decrypt or brute a message?")
        mode = input().lower()
        if mode in "encrypt decrypt brute e d b".split():
            logging.debug(mode)
            return mode
        else:
            print("Enter either %s or %s, %s or %s, %s or %s"%("encrypt","e","decrypt","d","brute","b"))

def getMessage():
    print("Enter your message")
    return input()

def getKey():
    key = 0
    while True:
        print("Enter the key number(1-%s)"%(MAX_KEY_SIZE))
        key = int(input())
        if (key >= 1 and key <= MAX_KEY_SIZE):
            logging.debug(key)
            return key

def getTranslateMessage(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = ''

    for symbol in message:
        # 判断是否是字母
        if symbol.isalpha():
            num = ord(symbol)
            num += key
            if symbol.isupper():
                # 加解密后符号超过字母表取值范围，A或Z，周期
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            translated += chr(num)
        else:
            translated += symbol
    logging.debug(translated)
    return translated


if __name__ == "__main__":
    mode = getMode()
    message = getMessage()
    key = getKey()
    print("Your translated text is:")
    if mode[0] != "b":
        print(getTranslateMessage(mode, message, key))
    else:
        # 遍历秘钥，暴力破解
        for key in range(1,MAX_KEY_SIZE+1):
            print(key, getTranslateMessage("d", message, key))