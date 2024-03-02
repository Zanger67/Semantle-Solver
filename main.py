import pandas as pd
import requests
import numpy as np
from datetime import date, datetime



# ===============================
# ||||||   SET CONSTANTS   ||||||
# ===============================

SECRET_WORD_URL = 'https://semantle.com/assets/js/secretWords.js'
BASEURL = 'https://semantle.com/'





# ===============================
# ||||||  Program Helpers  ||||||
# ===============================

def getVectorUrl(wordGuess : str, actualWord : str) -> str: # word guess
    return BASEURL + 'model2/' + actualWord + '/' + wordGuess

def getActualUrl(actualWord : str) -> str: # actual word to comapare
    ACTUAL_URL = getVectorUrl(actualWord, actualWord)

    return ACTUAL_URL

def cosineSimilarityMath(vec1, vec2) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def getCosineSimilarity(wordGuess : str, actualWord : str) -> float:
    if wordGuess in previousCases :
        return previousCases[wordGuess]
    
    try :
        guessJson = requests.get(getVectorUrl(wordGuess, actualWord)).json()
        previousCases[wordGuess] = cosineSimilarityMath(guessJson['vec'], ACTUAL_JSON['vec'])
    except :
        previousCases[wordGuess] = -2.0

    return previousCases[wordGuess]

def decimalToPercentage(decimal : float) -> str : 
    if (decimal == -2.0) :
        return 'Unknown Word'
    
    return str(round(decimal * 100, 2)) + '%'


def printPreviousGuesses() :
    print('\n\n',
          '================================\n',
          '|||||   Previous Guesses   |||||\n',
          '================================')
    
    print('{0:>10}'.format('Guess No.'),
          '{0:<15}'.format('Guess'),
          '{}'.format('Similarity'))
    for guess in previousCases :
        # print(previousCases[guess])
        print('{0:>9}'.format(previousCases[guess][0]) + '.',
              '{0:<15}'.format(guess),
              previousCases[guess][1])
        # print(f'{previousCases[guess][0]:>3}. {guess:>15} {previousCases[guess][1]}')
        # print(guess, ' : ', previousCases[guess])


def makeGuess(guess : str) :
    global perviousCases
    guess = guess.lower()

    if (guess in previousCases) :
        print('Already guessed this guess.')
        print('Cosine Similarity:\t', previousCases[guess][1],'\n\n\n')
        return
    
    global maxLenGuess
    maxLenGuess = max(len(guess), maxLenGuess)

    cosinSim = getCosineSimilarity(guess, TODAYS_WORD)

    if not cosinSim == -2.0 :
        global guessNo
        guessNo += 1
        previousCases[guess] = (guessNo, decimalToPercentage(cosinSim), cosinSim)
    else :
        previousCases[guess] = ('-', decimalToPercentage(cosinSim), cosinSim)

    printPreviousGuesses()
    print(f'\n\n{guess}:\t', previousCases[guess][1])

    if previousCases[guess][2] == 1.0 :
        print('\n\nYou Win!')
        quit()
    
def getCurrentDay() -> int:
    currDay = (date.today() - date(2022,1,29)).days

    # print(datetime.now().strftime('%H'))
    # print('hour: ', datetime.now().strftime('%H'), type(datetime.now().strftime('%H')))
    
    if (int(datetime.now().strftime('%H')) >= 19) : # puzzle changes at 19h00
        currDay += 1

    return currDay

def getCurrentAnswerWord(dayModifier: int) -> str:
    secretWords = requests.get(SECRET_WORD_URL)
    secretWords = secretWords.text
    secretWords = secretWords[secretWords.find('[') + 1 : secretWords.find(']')]

    removeChars = ['\"', ' ', '\n']
    for i in removeChars :
        secretWords = secretWords.replace(i, '')

    secretWords = secretWords.split(',')
    secretWords = secretWords[:-1] # remove blank string case

    # print(secretWords)

    currDay = getCurrentDay() + dayModifier

    return secretWords[currDay % len(secretWords)]



# ==============================
# ||||||   Main Program   ||||||
# ==============================

previousCases = {}
dayModifier = 0
guessNo = 0
maxLenGuess = 0


print('This program will proceed with the OFFICIAL word of the day unless otherwise specified', '\n',
      '- Enter \'-EXIT\' to exit the program at any time', '\n',
      '- Enter \'-ADJUSTDAY\' to be prompted to change the day', '\n',
      '- Enter \'-VIEWANSWER\' to see the today\'s word', '\n\n',
      'Otherwise, begin entering guesses...')


guess = str(input())
if guess.upper() == '-EXIT' :
    quit()
elif guess.upper() == '-ADJUSTDAY' : # pos values for future, neg values for past
    dayModifier = int(input('Enter how many days to adjust by (+future, -past): '))

    print(f'\n\nAdjustment has been made by {dayModifier} days.',
          'Proceed with guessing or enter \'-VIEWANSWER\'\n\n')
    
    guess = str(input())



# TODAYS_WORD = str(input('Enter the actual word: '))
TODAYS_WORD = getCurrentAnswerWord(dayModifier)
ACTUAL_URL = getActualUrl(TODAYS_WORD)
ACTUAL_JSON = requests.get(ACTUAL_URL).json()



if guess.upper() == '-VIEWANSWER' :
    print('\n\n', 'Answer for ', date.today(), ':\t', TODAYS_WORD)
    quit()
    



# Program loop to play
while True :
    makeGuess(guess)
    guess = str(input('\nEnter your guess: '))
    if guess.lower() == '-exit' :
        break
