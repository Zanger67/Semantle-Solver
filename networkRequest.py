from datetime import date, datetime
import requests



class networkRequest :
    SECRET_WORD_URL = 'https://semantle.com/assets/js/secretWords.js'
    BASEURL = 'https://semantle.com/'

    def __init__(self, dayModifier: int) -> None:
        self.dayModifier = dayModifier

    # word guess
    def getVectorUrl(self, wordGuess : str) -> str:
        return self.BASEURL + 'model2/' + self.TODAYS_WORD + '/' + wordGuess

    # actual word to compare
    def getActualUrl(self, actualWord : str) -> str:
        self.TODAYS_URL = self.getVectorUrl(actualWord)

        return self.TODAYS_URL

    def getJson(self, word: str) -> dict:
        if (self.TODAYS_WORD == None) :
            self.TODAYS_WORD = self.getCurrentAnswerWord()

        return requests.get(self.getVectorUrl(word)).json()

    def getTodaysJson(self) -> dict :
        return self.getJson(self.TODAYS_WORD)
    
    def getCurrentAnswerWord(self) -> str:
        currDay = self.getCurrentDay() + self.dayModifier
        secretWords = self.getSecretWords()

        self.TODAYS_WORD = secretWords[currDay % len(secretWords)]

        return self.TODAYS_WORD

    def getSecretWords(self) -> list:
        self.secretWords = requests.get(self.SECRET_WORD_URL)
        self.secretWords = self.secretWords.text
        self.secretWords = self.secretWords[self.secretWords.find('[') + 1 : self.secretWords.find(']')]

        removeChars = ['\"', ' ', '\n']
        for i in removeChars :
            self.secretWords = self.secretWords.replace(i, '')

        self.secretWords = self.secretWords.split(',')
        self.secretWords = self.secretWords[:-1] # remove blank string case
        
        return self.secretWords

    def getCurrentDay(self) -> int:
        currDay = (date.today() - date(2022,1,29)).days
        
        if (int(datetime.now().strftime('%H')) >= 19) : # puzzle changes at 19h00
            currDay += 1

        return currDay

