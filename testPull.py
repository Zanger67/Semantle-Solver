import pandas as pd
import requests
import numpy as np
from datetime import date, datetime

BASEURL = 'https://semantle.com/'

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
        return '???'
    
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
    
def getCurrentDay() -> int:
    currDay = (date.today() - date(2022,1,29)).days

    # print(datetime.now().strftime('%H'))
    # print('hour: ', datetime.now().strftime('%H'), type(datetime.now().strftime('%H')))
    
    if (int(datetime.now().strftime('%H')) >= 19) : # puzzle changes at 19h00
        currDay += 1

    return currDay

def getCurrentAnswerWord() -> str:
    secretWords = requests.get('https://semantle.com/assets/js/secretWords.js')
    secretWords = secretWords.text
    secretWords = secretWords[secretWords.find('[') + 1 : secretWords.find(']')]

    removeChars = ['\"', ' ', '\n']
    for i in removeChars :
        secretWords = secretWords.replace(i, '')

    secretWords = secretWords.split(',')
    secretWords = secretWords[:-1] # remove blank string case

    # print(secretWords)

    currDay = getCurrentDay()

    return secretWords[currDay % len(secretWords)]



# ===========================
# ||||||   Constants   ||||||
# ===========================


# print('days:', (date.today() - date(2022,1,30)).days)
# print(getCurrentDay())

# print(getCurrentAnswerWord())





# ==========================
# |||||| Main Program ||||||
# ==========================

# TODAYS_WORD = str(input('Enter the actual word: '))
TODAYS_WORD = getCurrentAnswerWord()

ACTUAL_URL = getActualUrl(TODAYS_WORD)
ACTUAL_JSON = requests.get(ACTUAL_URL).json()
previousCases = {}
guessNo = 0
maxLenGuess = 0


while True :
    guess = str(input('Enter your guess: '))
    if guess == 'exit' :
        break

    makeGuess(guess)





# initialJson = requests.get(urlRequest).json()

# print(initialJson,'\n\n\n\n')

# testRequest = pd.DataFrame(initialJson)

# print(testRequest)

# # print('sum\t', sum((testRequest.values)))
# print()