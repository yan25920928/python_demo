import pygame, sys, logging
from pygame.locals import *

logging.basicConfig(level=logging.DEBUG)

my_list = [1,2,3,4,5,6,7,8,9]

def main():
    for i in my_list:
        for j in my_list:
            if(i >= j):
                print("%d*%d=%d     " % (j, i, i * j),end="")
        print()

if __name__ == "__main__":
    main()