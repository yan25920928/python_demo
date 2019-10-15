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

def getGuess(alreadyGuess):
    while True:
        print("Guess a letter.")
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print("Please enter a single letter.")
        elif guess in alreadyGuess:
            print('You have already guessed that letter, Choose again')
        elif guess not in 'abcdefghigklmnopqrstuvwxyz':
            print("Please enter a LETTER.")
        else:
            return guess

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

print("H A N G M A N")
missedLetters = ""
correctLetters = ""
secretWord = getRandomWord(words)
gameIsDone = False

while True:
    displayBoard(missedLetters, correctLetters, secretWord)
    guess = getGuess(missedLetters + correctLetters)
    if guess in secretWord:
        correctLetters = correctLetters + guess
        foundAllLetter = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetter = False
                break
        if foundAllLetter:
            print("you win")
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters,correctLetters,secretWord)
            print("You have run out of guess ! \n after" + str(len(missedLetters))+"missed guesses and"
                  + str(len(correctLetters))+"correct guesses, the word was"+ secretWord+"\"")
            gameIsDone = True

    if gameIsDone:
        if playAgain():
            missedLetters = ""
            correctLetters = ""
            gameIsDone = False
            secretWord = getRandomWord(words)
        else:
            break
