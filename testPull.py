import pandas as pd
import requests
import numpy as np



def getBaseUrl() : 
    return 'https://semantle.com/'

def getVectorUrl(wordGuess : str, actualWord : str) : # word guess
    return getBaseUrl() + 'model2/' + actualWord + '/' + wordGuess

def getActualUrl(actualWord : str) : # actual word to comapare
    # if actualUrl == '' :
    actualUrl = getVectorUrl(actualWord, actualWord)

    return actualUrl

def getCosineSimilarity(wordGuess : str, actualWord : str) :
    if wordGuess in previousCases :
        return previousCases[wordGuess]
    
    try :
        guessJson = requests.get(getVectorUrl(wordGuess, actualWord)).json()
    except :
        return -1.0

    # print(guessJson)
    # if not guessJson['vec'] :
    #     return 0
    
    temp = np.dot(guessJson['vec'], actualJson['vec']) / (np.linalg.norm(guessJson['vec']) * np.linalg.norm(actualJson['vec']))

    previousCases[wordGuess] = temp

    return temp



todaysWord = str(input('Enter the actual word: '))
actualUrl = getActualUrl(todaysWord)
actualJson = requests.get(actualUrl).json()
previousCases = {}

while True :
    guess = str(input('Enter your guess: '))
    if guess == 'exit' :
        break
    print(getCosineSimilarity(guess, todaysWord))





# initialJson = requests.get(urlRequest).json()

# print(initialJson,'\n\n\n\n')

# testRequest = pd.DataFrame(initialJson)

# print(testRequest)

# # print('sum\t', sum((testRequest.values)))
# print()