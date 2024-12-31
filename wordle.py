from colorama import Fore, Style    # terminal output formatting
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
sheet = wb.sheets["qwerty"]         # gaining data for displaying letters in an alphabetical list to the player about what is left

def main():
    global sheet
    global wb

    counter = 0                     # keeps track of the number of guesses
    guesses = []
    won = False             # keep track of if the user won
    start_time = datetime.now()  # Start time of the game

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
        guesses.append(guess)               # add the guess to the guess list for data
        # print_alphabetical_list(guesses)
        print_qwerty(guesses)
        print()
        counter+=1
        

        if guess == correct:            # this while loop in main will only terminate once the user gets the word correct, or uses up their 6 guesses
            print("CONGRATULATIONS, you got the word in " + str(counter) + " guesses!")
            won = True         
            break
        if counter >= 6:
            print("Better luck next time, the word was: " + correct)
            break

    end_time = datetime.now()  # End time of the game
    time_taken = end_time - start_time  # Calculate time taken
    # Log the game data to Excel
    log_data(counter, guesses, won, time_taken)
    


# Compare the user guess to the correct word, return the info on the guessed word about          #
# incorrect letters, correct letters in the wrong place, and correct letters in the right place. #
def check(guess):
    return_word = ""
    correct_counts = {}  # counts occurrences of each letter in the correct word
    guess_status = [None] * 5  # tracks the status of each letter in the guess (None, 'green', 'yellow', 'red')

    # count occurrences of each letter in the correct word
    for letter in correct:
        correct_counts[letter] = correct_counts.get(letter, 0) + 1

    # first pass: Mark correct placements (green)
    for i in range(5):
        if guess[i] == correct[i]:  # correct placement
            guess_status[i] = 'green'
            correct_counts[guess[i]] -= 1  # reduce available count for that letter

    # second pass: Mark misplaced letters (yellow)
    for i in range(5):
        if guess_status[i] is None and guess[i] in correct and correct_counts[guess[i]] > 0:
            guess_status[i] = 'yellow'
            correct_counts[guess[i]] -= 1  # reduce available count for that letter

    # third pass: Mark incorrect letters (red)
    for i in range(5):
        if guess_status[i] is None:
            guess_status[i] = 'red'

    # construct the return word with colors
    for i in range(5):
        if guess_status[i] == 'green':
            return_word += f"{Fore.GREEN}{guess[i]}{Style.RESET_ALL} "
        elif guess_status[i] == 'yellow':
            return_word += f"{Fore.YELLOW}{guess[i]}{Style.RESET_ALL} "
        else:  # 'red'
            return_word += f"{Fore.RED}{guess[i]}{Style.RESET_ALL} "

    return return_word.strip()

def print_alphabetical_list(guesses):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    guessed_letters = set()
    
    for guess in guesses:
        guessed_letters.update(set(guess))
    
    confirmed_letters = set(correct) & guessed_letters
    remaining_letters = [letter for letter in alphabet if letter not in guessed_letters or letter in confirmed_letters]    # remove any incorrect guessed letters from display
    print(' '.join(remaining_letters))

def print_qwerty(guesses):
    qwerty_rows = [
        list(""),
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM")
    ]

    guessed_status = {}  # store letter status: 'correct', 'misplaced', 'incorrect'

    for guess in guesses:
        for i, letter in enumerate(guess):
            if letter == correct[i]:  # correct placement
                guessed_status[letter] = 'correct'
            elif letter in correct:  # misplaced but in the word
                if guessed_status.get(letter) != 'correct':  # only override if not already correct
                    guessed_status[letter] = 'misplaced'
            else:  # Incorrect
                guessed_status.setdefault(letter, 'incorrect')

    for row in qwerty_rows:     # update qwerty layout colors
        row_display = []
        for letter in row:
            if guessed_status.get(letter) == 'correct':
                row_display.append(f"{Fore.GREEN}{letter}{Style.RESET_ALL}")
            elif guessed_status.get(letter) == 'misplaced':
                row_display.append(f"{Fore.YELLOW}{letter}{Style.RESET_ALL}")
            elif guessed_status.get(letter) == 'incorrect':
                row_display.append(f"{Fore.RED}{letter}{Style.RESET_ALL}")
            else:
                row_display.append(letter)

        # indenation attempts to look more like keyboard, not working yet
        if i == 1:
            print(" " * 2 + ' '.join(row_display))  # indent second row
        elif i == 2:
            print(" " * 4 + ' '.join(row_display))  # indent third row
        else:
            print(' '.join(row_display))  # no indentation for the first row

def log_data(counter, guesses, won, time_taken):                # add data about the game played into the excel file
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
    sheet.range(f"J{row}").value = datetime.now().strftime("%H:%M:%S")      # time of day
    sheet.range(f"K{row}").value = datetime.now().strftime("%D")            # date
    sheet.range(f"L{row}").value = str(time_taken)                          # time taken

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
        