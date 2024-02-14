import random
import nltk   # checks to make sure guesses are valid words, make sure to download nltk on computer
import xlwings as xw
from datetime import datetime

nltk.download('words')
english_words = set(nltk.corpus.words.words())

with open('C:/Users/jazdo/Desktop/wordle/words.txt', 'r') as f:     # read in the possible words file and
    words = f.read()                                                # format them correctly
words = words.split(',')
words = [word.strip(" '") for word in words]

wb = xw.Book("C:\\Users\\jazdo\\Desktop\\wordle\\wordle.xlsx")
sheet = wb.sheets["no_letters"]         # gaining data for displaying no letters to the player about what is left

def main():
    global sheet
    global wb

    counter = 0                     # keeps track of the number of guesses
    guesses = []
    won = False             # keep track of if the user won

    while True:
        guess = input("Enter guess: ")
        guess = guess.lower()           # format the guess in all lowercase so that nltk can check it. The nltk library is lowercase and it is case-sensitive

        while (len(guess) != 5) or guess not in english_words:                  # keep the player in this loop in case they input multiple invalid guesses (not 5 letters or not a valid word) in a row
            if (len(guess) != 5 and guess not in english_words):
                guess = input("Your guess must be 5 letters long and a valid word: ")
            elif (len(guess) != 5):
                guess = input("Your guess must be 5 letters long: ")
            else:
                guess = input("Your guess must be a valid word: ")
            guess = guess.lower()                   

        guess = guess.upper()           # now format the guess to uppercase for a better display to the user
        print(check(guess))
        print()
        counter+=1
        guesses.append(guess)               # add the guess to the guess list for data

        if guess == correct:            # this while loop in main will only terminate once the user gets the word correct, or uses up their 6 guesses
            print("CONGRATULATIONS, you got the word in " + str(counter) + " guesses!")
            won = True         
            break
        if counter >= 6:
            print("Better luck next time, the word was: " + correct)
            break

    # Log the game data to Excel
    log_data(counter, guesses, won)
    


# Compare the user guess to the correct word, return the info on the guessed word about          #
# incorrect letters, correct letters in the wrong place, and correct letters in the right place. #
def check(guess):
    return_word = ''                # the guess string to be returned and printed out showing the user their progress
    doneLetters = []                # doneLetters and rightIndex help keep track of letters that appear multiple times in the correct word in order to output the information correctly
    rightIndex = []

    for i in range(0, 5):           # iterate through the guess and correct word to fill out rightIndex and doneLetters 
        if guess[i] == correct[i]:      # appends index of every correct letter in the guess to rightIndex 
            rightIndex.append(i)
        for j in range(0, 5):
            if j != i and guess[i] == correct[j] and j not in rightIndex:       # does not append a letter to doneLetters if there are multiple in the word and not all of them are correct
                break
            if j == 4:
                doneLetters.append(guess[i])

    for j in range(0, 5):           # using rightIndex and doneLetters, assign each letter it's corresponding place identifier
        if j in rightIndex:         # if a letter is in the right spot, put plus signs around it
            return_word += (' +' + guess[j] + '+ ')
        elif guess[j] in correct and guess[j] not in doneLetters and return_word.count(guess[j]) < correct.count(guess[j]):     # if a letter is in the guess but not in the correct spot, put minus signs around it
            return_word += (' -' + guess[j] + '- ')
        else:                       # otherwise, put nothing around the letter
            return_word += (' ' + guess[j] + ' ')
    return return_word.upper()


def log_data(counter, guesses, won):                # add data about the game played into the excel file
    global sheet

    row = sheet.cells(sheet.cells.last_cell.row, 1).end("up").row + 1           # find the first open row

    # Write data to Excel
    sheet.range(f"A{row}").value = "Yes" if won else "No"               # if they won or not
    if won:
        sheet.range(f"B{row}").value = counter                  # if won, add the number of guesses taken
    sheet.range(f"C{row}").value = correct                  
    for i in range(6):                      # add the guesses to their respective columns and leave unguessed columns blank
        if i < len(guesses):
            sheet.range(row, i + 4).value = guesses[i]
        else:
            sheet.range(row, i + 4).value = ""
    sheet.range(f"J{row}").value = datetime.now().strftime("%H:%M:%S")          # time of day
    sheet.range(f"K{row}").value = datetime.now().strftime("%D")            # date

if __name__ == '__main__':
    correct = (random.choice(words)).upper()                # choose a random word from the words list as the first correct word when running the program

    main()
    while True:
        choice = input("\nKeep playing? (y/n): ")
        choice = choice.lower()
        while choice != 'y' and choice != 'n':          # yes or no input validation
            choice = input("You must enter y or n: ")
            choice = choice.lower()
        if choice == 'y':
            correct = (random.choice(words)).upper()

            main()
        else:
            wb.save("C:\\Users\\jazdo\\Desktop\\wordle\\wordle.xlsx")           # save and close the xlsx file
            wb.close()
            break
        