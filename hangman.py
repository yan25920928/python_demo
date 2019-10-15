import random
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
    =====
  ''', '''
  +---+
  0   |
      |
      |
    =====
  ''', '''
  +---+
  0   |
  |   |
      |
    =====
  ''', '''
  +---+
  0   |
 /|   |
      |
    =====
  ''', '''
  +---+
  0   |
 /|\  |
      |
    =====
  ''', '''
  +---+
  0   |
 /|\  |
 /    |
    =====
  ''', '''
  +---+
  0   |
 /|\  |
 / \  |
    =====
  ''']
words = 'ant baboon badger bat beaver camel crow deer dog fox goose monkey mouse panda shark sheep snake tiger'.split()

def getRandomWord(wordList):
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()
    print('Missed letters:',end=" ")
    for letter in missedLetters:
        print(letter, end=" ")
    print()
    blanks = '_' * len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    for letter in blanks:
        print(letter, end=" ")
    print()