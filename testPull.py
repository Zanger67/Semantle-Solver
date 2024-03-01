from vectorAndUrlHelpers import vectorAndUrlHelpers as helper




helper.init(actualString=str(input('Enter the answer to guess: ')))

while True :
    guess = str(input('Enter your guess: '))
    
    if guess == 'exit' :
        break

    cosinSimVal = helper.enterGuess(guess)


    helper.printPreviousCases()
    print('\n\n', 'Recent Guess:\t', guess, '\t', helper.decimalToPercentage(cosinSimVal), '\n\n')
    






# initialJson = requests.get(urlRequest).json()

# print(initialJson,'\n\n\n\n')

# testRequest = pd.DataFrame(initialJson)

# print(testRequest)

# # print('sum\t', sum((testRequest.values)))
# print()