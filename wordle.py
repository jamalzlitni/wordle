import random
import nltk   # checks to make sure guesses are valid words, make sure to download nltk on computer

nltk.download('words')
english_words = set(nltk.corpus.words.words())

with open('C:/Users/jazdo/Desktop/wordle/words.txt', 'r') as f:
    words = f.read()
words = words.split(',')
words = [word.strip(" '") for word in words]


def main():
    counter = 0
    while True:
        guess = input("Enter guess: ")
        guess = guess.lower()
        while (len(guess) != 5) or guess not in english_words:
            if (len(guess) != 5 and guess not in english_words):
                guess = input("Your guess must be 5 letters long and a valid word: ")
            elif (len(guess) != 5):
                guess = input("Your guess must be 5 letters long: ")
            else:
                guess = input("Your guess must be a valid word: ")
            guess = guess.lower()
        guess = guess.upper()
        print(check(guess))
        counter+=1
        if guess == correct:
            print("CONGRATULATIONS, you got the word in " + str(counter) + " guesses!")
            break
        if counter >= 6:
            print("Better luck next time, the word was: " + correct)
            break
    

def check(guess):
    return_word = ''
    doneLetters = []
    rightIndex = []
    for i in range(0, 5):
        if guess[i] == correct[i]:
            rightIndex.append(i)
        for j in range(0, 5):
            if j != i and guess[i] == correct[j] and j not in rightIndex:
                break
            if j == 4:
                doneLetters.append(guess[i])
    for j in range(0, 5):
        if j in rightIndex:
            return_word += (' +' + guess[j] + '+ ')
        elif guess[j] in correct and guess[j] not in doneLetters and return_word.count(guess[j]) < correct.count(guess[j]):
            return_word += (' -' + guess[j] + '- ')
        else:
            return_word += (' ' + guess[j] + ' ')
    return return_word.upper()

if __name__ == '__main__':
    correct = (random.choice(words)).upper()

    main()
    while True:
        choice = input("\nKeep playing? (y/n): ")
        choice = choice.lower()
        while choice != 'y' and choice != 'n':
            choice = input("You must enter y or n: ")
            choice = choice.lower()
        if choice == 'y':
            correct = (random.choice(words)).upper()

            main()
        else: exit()
        