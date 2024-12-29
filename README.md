# wordle
Python Wordle clone to be used for data collection on my game tendencies and stats.

'wordle.py' is the Python Wordle file
'words.txt' is the file containing all of the possible Wordle words. Each word is in this format: 'word here', 'word here', etc

I am using the xlwings library to track and store the data from each game played in order to determine the best way of outputting the letters available to the player. 
Data collected contain the following columns: Won, Number of Guesses, Correct Word, Guess 1, Guess 2, Guess 3, Guess 4, Guess 5, Guess 6, Time of Day, and Date. 
The different options (sheet names) I am using to display the available letters to the player are:
- no_letters: the only thing the players see are their previous guesses and the corresponding correctness indicators for those letters
- alphabetical_list: above each of the past guesses, the user gets a list of all letters in the alphabet that either haven't been guessed or have been guessed and are confirmed in the word
- qwerty: this is exactly as it sounds, it appears above each guess and looks like a keyboard with the indicators around each letter (like what NYT Wordle uses)

