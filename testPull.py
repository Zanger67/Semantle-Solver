import pandas as pd
import requests
import numpy as np

BASEURL = 'https://semantle.com/'

def getVectorUrl(wordGuess : str, actualWord : str) -> str: # word guess
    return BASEURL + 'model2/' + actualWord + '/' + wordGuess

def getActualUrl(actualWord : str) -> str: # actual word to comapare
    actualUrl = getVectorUrl(actualWord, actualWord)

    return actualUrl

def cosineSimilarityMath(vec1, vec2) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def getCosineSimilarity(wordGuess : str, actualWord : str) -> float:
    if wordGuess in previousCases :
        return previousCases[wordGuess]
    
    try :
        guessJson = requests.get(getVectorUrl(wordGuess, actualWord)).json()
        previousCases[wordGuess] = cosineSimilarityMath(guessJson['vec'], ACTUALJSON['vec'])
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

    global guessNo
    guessNo += 1

    cosinSim = getCosineSimilarity(guess, todaysWord)
    previousCases[guess] = (guessNo, decimalToPercentage(cosinSim), cosinSim)

    printPreviousGuesses()
    print(f'\n\n{guess}:\t', previousCases[guess][1])
    





# ==========================
# |||||| Main Program ||||||
# ==========================

todaysWord = str(input('Enter the actual word: '))

ACTUALURL = getActualUrl(todaysWord)
ACTUALJSON = requests.get(ACTUALURL).json()
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