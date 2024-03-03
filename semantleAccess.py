import pandas as pd
import requests
import numpy as np
from datetime import date, datetime


class semantleAccess :
    # ===============================
    # |||||| Helpers Variables ||||||
    # ===============================

    SECRET_WORD_URL = 'https://semantle.com/assets/js/secretWords.js'
    BASEURL = 'https://semantle.com/'
    ORDER_BY_SIMILARITY = True # true if print prev guesses by sim otherwise print by guess no.

    previousCases = {}
    previousCasesRanked = {}
    previousCasesUnknown = {}
    dayModifier = 0
    guessNo = 0
    maxLenGuess = len('Guess ')


    # ================================
    # ||||||   Initialization   ||||||
    # ================================

    def __init__(self, dayModifier: int) -> None:
        self.TODAYS_WORD = self.getCurrentAnswerWord(dayModifier)
        self.ACTUAL_URL = self.getActualUrl(self.TODAYS_WORD)
        self.ACTUAL_JSON = requests.get(self.ACTUAL_URL).json()


    # ===============================
    # ||||||  Program Helpers  ||||||
    # ===============================

    def getVectorUrl(self, wordGuess : str, actualWord : str) -> str: # word guess
        return self.BASEURL + 'model2/' + actualWord + '/' + wordGuess

    def getActualUrl(self, actualWord : str) -> str: # actual word to comapare
        ACTUAL_URL = self.getVectorUrl(actualWord, actualWord)

        return ACTUAL_URL

    def cosineSimilarityMath(self, vec1, vec2) -> float:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def getCosineSimilarity(self, wordGuess : str, actualWord : str) -> float:
        if wordGuess in self.previousCases :
            return self.previousCases[wordGuess][2]
        
        try :
            guessJson = requests.get(self.getVectorUrl(wordGuess, actualWord)).json()
            return self.cosineSimilarityMath(guessJson['vec'], self.ACTUAL_JSON['vec'])
        except :
            return -2.0

    def decimalToPercentage(self, decimal : float) -> str : 
        if (decimal == -2.0) :
            return 'Unknown Word'
        
        return str(round(decimal * 100, 2)) + '%'


    def printPreviousGuesses(self) :
        # establishes which dict to use dep if we want to order by similarity or guess no.
        self.prevCaseToUse = self.previousCasesRanked if self.ORDER_BY_SIMILARITY else self.previousCases
        
        guessLen = self.maxLenGuess + 1
        guessLen += guessLen % 2 # make even to balance 'Previous Guesses' left and right balance
        similarityLen = len('similarity') if len(self.previousCasesUnknown) == 0 else len('Unknown Word')

        # len of all 3 columns together
        allColsWidth = (10                    # guessNo
                        + guessLen            # maxGuess size
                        + similarityLen       # similarity size will be this since 
                        + 1) # offset space   # max of percent is 100.00% aka len=7

        print('\n\n',
            ('{0:=<' + str(allColsWidth) + '}').format(''), '\n',
            '|||||', ('{0:^' + str(allColsWidth - 2 * len('|||||') - 2) + '}').format('Previous Guesses'), '|||||', '\n',
            ('{0:=<' + str(allColsWidth) + '}').format(''))
        

        stringFormats = {'guessNo' : '{0:>10}',
                        'guess' : ('{0:<' + str(guessLen) + '}'),
                        'similarity' : '{}'}

        print(stringFormats['guessNo'].format('Guess No.'),
            stringFormats['guess'].format('Guess'),
            'Similarity')
        
        keys = reversed(sorted(self.prevCaseToUse.keys())) if self.ORDER_BY_SIMILARITY else self.prevCaseToUse.keys()
        
        for key in keys :
            print(stringFormats['guessNo'].format((str(self.prevCaseToUse[key][0]) + '.')),
                stringFormats['guess'].format(self.prevCaseToUse[key][3]),
                self.prevCaseToUse[key][1])
        
        for key in self.previousCasesUnknown.keys() :
            print(stringFormats['guessNo'].format((str(self.previousCasesUnknown[key][0]) + '.')),
                stringFormats['guess'].format(self.previousCasesUnknown[key][3]),
                self.previousCasesUnknown[key][1])

    def makeGuess(self, guess : str) -> bool :
        guess = guess.lower()

        if (guess in self.previousCases 
            or guess in self.previousCasesUnknown) :

            print('Already guessed this guess.')
            print('Cosine Similarity:\t', self.previousCases[guess][1],'\n\n\n')
            return
        
        self.maxLenGuess = max(len(guess), self.maxLenGuess)

        cosinSim = round(self.getCosineSimilarity(guess, self.TODAYS_WORD),4)

        thisResult = None

        if not cosinSim == -2.0 :
            self.guessNo += 1
            thisResult = (self.guessNo, self.decimalToPercentage(cosinSim), cosinSim, guess)
            self.previousCases[guess] = thisResult
            self.previousCasesRanked[cosinSim] = thisResult
        else :
            thisResult = ('-', self.decimalToPercentage(cosinSim), cosinSim, guess)
            self.previousCasesUnknown[guess] = thisResult

        self.printPreviousGuesses()
        allColsWidth = 10 + 4 + (self.maxLenGuess + (self.maxLenGuess + 1) % 2)
        print(('{0:<' + str(allColsWidth) + '}').format(f'\n\n{self.guessNo}. {guess}:'), thisResult[1])

        if thisResult[2] == 1.0 :
            print('\n\nYou Win!')
            return True
            # quit()
        return False
        
    def getCurrentDay(self) -> int:
        currDay = (date.today() - date(2022,1,29)).days
        
        if (int(datetime.now().strftime('%H')) >= 19) : # puzzle changes at 19h00
            currDay += 1

        return currDay

    def getCurrentAnswerWord(self, dayModifier: int) -> str:
        self.secretWords = requests.get(self.SECRET_WORD_URL)
        self.secretWords = self.secretWords.text
        self.secretWords = self.secretWords[self.secretWords.find('[') + 1 : self.secretWords.find(']')]

        removeChars = ['\"', ' ', '\n']
        for i in removeChars :
            self.secretWords = self.secretWords.replace(i, '')

        self.secretWords = self.secretWords.split(',')
        self.secretWords = self.secretWords[:-1] # remove blank string case

        currDay = self.getCurrentDay() + dayModifier

        return self.secretWords[currDay % len(self.secretWords)]

