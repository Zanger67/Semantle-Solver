import pandas as pd
import requests
import numpy as np


class vectorAndUrlHelpers :
    def init(self, actualString : str) :
        global todaysWord
        global actualUrl
        global actualJson
        global previousCases
        global guessNo

        todaysWord = actualString
        actualUrl = self.getActualUrl(todaysWord)
        actualJson = requests.get(actualUrl).json()
        previousCases = {}
        guessNo = 0




    def getBaseUrl(self) : 
        return 'https://semantle.com/'

    def getVectorUrl(self, wordGuess : str) : # word guess
        return self.getBaseUrl() + 'model2/' + todaysWord + '/' + wordGuess

    def getActualUrl(self, actualWord : str) : # actual word to comapare
        actualUrl = self.getVectorUrl(actualWord)

        return actualUrl

    def cosineSimilairtyMath(self, v1, v2) :
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def getCosineSimilarity(self, wordGuess : str) :
        if wordGuess in previousCases :
            return previousCases[wordGuess]
        
        try : #
            guessJson = requests.get(self.getVectorUrl(wordGuess, todaysWord)).json()
            previousCases[wordGuess] = self.cosineSimilairtyMath(guessJson['vec'], actualJson['vec'])
        except : # cosine similairty is [-1.0, 1.0] in theory 
                # but stated to be more like [-0.4, 0.4] so we'll
                # default -2 to identify
            previousCases[wordGuess] = -2.0
        

        return previousCases[wordGuess]

    def decimalToPercentage(self, decimal : float) :
        if decimal == -2.0 :
            return '???'
        return str(round(decimal * 100,2)) + '%'


    def printPreviousCases(self) :
        print('\n\n\n\n',
            '===========================\n',
            '||||  Previous Guesses ||||\n',
            '===========================')

        for key in previousCases :
            print(key, '\t', previousCases[key][2])



    def enterGuess(self, guess : str) :
        cosinSimVal = self.getCosineSimilarity(guess)
        cosinSimStr = self.decimalToPercentage(cosinSimVal)
        guessNo += 1
        
        previousCases[guess] = (guessNo, 
                                cosinSimVal, 
                                self.decimalToPercentage(cosinSimVal))
        
        return cosinSimVal
        
