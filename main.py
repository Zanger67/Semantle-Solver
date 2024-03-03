import semantleAccess as semantle
from datetime import date

# ==============================
# ||||||   Main Program   ||||||
# ==============================

print('This program will proceed with the OFFICIAL word of the day unless otherwise specified', '\n',
      '- Enter \'-EXIT\' to exit the program at any time', '\n',
      '- Enter \'-ADJUSTDAY\' to be prompted to change the day', '\n',
      '- Enter \'-VIEWANSWER\' to see the today\'s word', '\n\n',
      'Otherwise, begin entering guesses...')

sem = semantle.semantleAccess(0)

guess = str(input())
if guess.upper() == '-EXIT' :
    quit()
elif guess.upper() == '-ADJUSTDAY' : # pos values for future, neg values for past
    dayModifier = int(input('Enter how many days to adjust by (+future, -past): '))

    print(f'\n\nAdjustment has been made by {dayModifier} days.',
          'Proceed with guessing or enter \'-VIEWANSWER\'\n\n')
    
    sem = semantle.semantleAccess(dayModifier)
    
    guess = str(input())



# TODAYS_WORD = str(input('Enter the actual word: '))




if guess.upper() == '-VIEWANSWER' :
    print('\n\n', 'Answer for ', date.today(), ':\t', sem.TODAYS_WORD)
    quit()
   


# Program loop to play
while True :
    sem.makeGuess(guess)
    guess = str(input('\nEnter your guess: '))
    if guess.lower() == '-exit' :
        break

