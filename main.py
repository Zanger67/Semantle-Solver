import pandas as pd
import requests
import numpy as np
from datetime import date, datetime



# ===============================
# ||||||   SET CONSTANTS   ||||||
# ===============================

SECRET_WORD_URL = 'https://semantle.com/assets/js/secretWords.js'
BASEURL = 'https://semantle.com/'
ORDER_BY_SIMILARITY = True # true if print prev guesses by sim otherwise print by guess no.




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
        return previousCases[wordGuess][2]
        # return previousCases[wordGuess]
    
    try :
        guessJson = requests.get(getVectorUrl(wordGuess, actualWord)).json()
        # previousCases[wordGuess] = cosineSimilarityMath(guessJson['vec'], ACTUAL_JSON['vec'])
        return cosineSimilarityMath(guessJson['vec'], ACTUAL_JSON['vec'])
    except :
        return -2.0
        # previousCases[wordGuess] = -2.0

    # return previousCases[wordGuess]

def decimalToPercentage(decimal : float) -> str : 
    if (decimal == -2.0) :
        return 'Unknown Word'
    
    return str(round(decimal * 100, 2)) + '%'


def printPreviousGuesses() :
    # establishes which dict to use dep if we want to order by similarity or guess no.
    global ORDER_BY_SIMILARITY
    global previousCasesUnknown
    global maxLenGuess

    prevCaseToUse = previousCasesRanked if ORDER_BY_SIMILARITY else previousCases
    
    guessLen = maxLenGuess + 1
    guessLen += guessLen % 2 # make even to balance 'Previous Guesses' left and right balance
    similarityLen = len('similarity') if len(previousCasesUnknown) == 0 else len('Unknown Word')

    # len of all 3 columns together
    allColsWidth = (10                    # guessNo
                    + guessLen            # maxGuess size
                    + similarityLen       # similarity size will be this since 
                    + 1) # offset space   # max of percent is 100.00% aka len=7

    print('\n\n',
          ('{0:=<' + str(allColsWidth) + '}').format(''), '\n',
          '|||||', ('{0:^' + str(allColsWidth - 2 * len('|||||') - 2) + '}').format('Previous Guesses'), '|||||', '\n',
          ('{0:=<' + str(allColsWidth) + '}').format(''))
    
    
    # print('\n\n',
    #       '================================', '\n',
    #       '|||||   Previous Guesses   |||||', '\n',
    #       '================================')

    stringFormats = {'guessNo' : '{0:>10}',
                     'guess' : ('{0:<' + str(guessLen) + '}'),
                     'similarity' : '{}'}

    print(stringFormats['guessNo'].format('Guess No.'),
          stringFormats['guess'].format('Guess'),
          'Similarity')
    
    keys = reversed(sorted(prevCaseToUse.keys())) if ORDER_BY_SIMILARITY else prevCaseToUse.keys()
    
    for key in keys :
        print(stringFormats['guessNo'].format((str(prevCaseToUse[key][0]) + '.')),
              stringFormats['guess'].format(prevCaseToUse[key][3]),
              prevCaseToUse[key][1])
    
    for key in previousCasesUnknown.keys() :
        print(stringFormats['guessNo'].format((str(previousCasesUnknown[key][0]) + '.')),
            stringFormats['guess'].format(previousCasesUnknown[key][3]),
            previousCasesUnknown[key][1])

def makeGuess(guess : str) :
    global perviousCases
    global previousCasesRanked
    global previousCasesUnknown
    guess = guess.lower()

    if (guess in previousCases 
        or guess in previousCasesUnknown) :

        print('Already guessed this guess.')
        print('Cosine Similarity:\t', previousCases[guess][1],'\n\n\n')
        return
    
    global maxLenGuess
    maxLenGuess = max(len(guess), maxLenGuess)

    cosinSim = getCosineSimilarity(guess, TODAYS_WORD)

    thisResult = None

    if not cosinSim == -2.0 :
        global guessNo
        guessNo += 1
        thisResult = (guessNo, decimalToPercentage(cosinSim), cosinSim, guess)
        previousCases[guess] = thisResult
        previousCasesRanked[cosinSim] = thisResult
    else :
        thisResult = ('-', decimalToPercentage(cosinSim), cosinSim, guess)
        previousCasesUnknown[guess] = thisResult

    printPreviousGuesses()
    allColsWidth = 10 + 4 + (maxLenGuess + (maxLenGuess + 1) % 2)
    print(('{0:<' + str(allColsWidth) + '}').format(f'\n\n{guessNo}. {guess}:'), thisResult[1])

    if thisResult[2] == 1.0 :
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
previousCasesRanked = {}
previousCasesUnknown = {}
dayModifier = 0
guessNo = 0
maxLenGuess = len('Guess ')



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

