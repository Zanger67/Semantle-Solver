import pandas as pd
import requests



def getBaseUrl() : 
    return 'https://semantle.com/'

def getVectorUrl(wordGuess : str, actualWord : str) : # word guess
    return getBaseUrl() + 'model2/' + actualWord + '/' + wordGuess

def getActualUrl(actualWord : str) :
    return getVectorUrl(actualWord, actualWord)

urlRequest = semantleStarterRequest + 'plane'


initialJson = requests.get(urlRequest).json()

print(initialJson,'\n\n\n\n')

testRequest = pd.DataFrame(initialJson)

print(testRequest)

# print('sum\t', sum((testRequest.values)))
print()