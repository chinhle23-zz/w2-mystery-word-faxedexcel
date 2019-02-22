import string 
    # import the 'string' built-in module
    # https://docs.python.org/3.7/library/string.html

import random
    # https://docs.python.org/3.7/library/random.html

def create_word_length_list(a_list, min_char, max_char):
    """
    Given a list of lists made of [word, word length], create a new list with a minimum and maximum number of characters
    """
    new_list = []
    i = 0
    while i < len(a_list):
        if min_char <= a_list[i][1] <= max_char:
            new_list.append(a_list[i])
        i += 1
    return new_list

def demand_valid_letter(a_str):
    """
    Given a string, keep asking for input until a letter or hyphen is inputted and return it
    """
    valid_letters = string.ascii_letters + "-"
        # 'string.ascii_letters' variable is imported from 'string' module
        # valid letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' + '-'
    invalid_guess = True
    while invalid_guess:
        if a_str not in valid_letters:
            a_str = input("Invalid letter! Please type a letter: ")
        else:
            invalid_guess = False
    return a_str.upper()

def display_correct_letter(letter, guesses):
    """
    Conditionally display a letter. If the letter is already in
    the list `guesses`, then return it. Otherwise, return "_".
    """
    if letter in guesses:
        return letter
    else:
        return "_"

def print_word(word, guesses):
    """
    Prints 'word' to the screen displaying only letters in the list 'guesses' and underscores as placeholders for letters not in the list
    """
    correct_guess_list = [display_correct_letter(letter, guesses) for letter in word]
        # new list called 'correct_guess_list' created using list comprehension
        # 'display_correct_letter(letter, guesses)' is the collection
        # 'for letter in word' is the iteration
        # loop through each 'letter' in 'word', if the 'letter' is in 'guesses', then add it to the list, otherwise add an underscore to the list
    print(" ".join(correct_guess_list))
        # 'str.join(iterable)' method returns a string which is the concatenation of the strings in 'iterable' and the separator between elements is the 'str' providing this method
        # https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join

def is_word_done(word, guesses):
    """
    Returns whether all the letters in 'word' is in the list 'guesses' 
    """
    correct_word = ""
    for letter in word:
        if letter in guesses:
            correct_word += letter
    if correct_word == word:
        return True
    return False
    
# read in text file
with open('words.txt') as file:
    # 'with' statement is used to wrap the execution of a block with methods defined by a context manager https://docs.python.org/3.7/reference/compound_stmts.html#the-with-statement
    # a 'context manager' is an object that defines the runtime context to be established when executing a 'with' statement. the 'context manager' handles the entry into, and the exit from, the desired runtime context for the execution of the block of code https://docs.python.org/3.7/reference/datamodel.html#context-managers
    # 'context manager types' https://docs.python.org/3.7/library/stdtypes.html#typecontextmanager
    # 'open(file, mode='r', bufferring=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)' function opens 'file' named 'filename' https://docs.python.org/3.7/library/functions.html#open
    # simpler explanation: https://www.pythonforbeginners.com/files/with-statement-in-python
    text = file.read()

# store list of words for which user can guess from
words = []
for word in text.split("\n"):
    # '<sample_string>.split(sep=None, maxsplit=-1)' method will split 'text' using 'newline' as the delimiter and returns a list of words
    if word != '':
        words.append(word.upper())
            # '<sample_list>.append(x)' method appends a new item with value 'x' (in this case 'word.upper()') to the end of the list named 'words' https://docs.python.org/3.7/library/array.html?highlight=append#array.array.append

# create list of all words that holds [word, word_length]
all_words = []
i = 0
while i < len(words):
    word_with_length = []
    word_with_length.append(words[i])
    word_with_length.append(len(words[i]))
    all_words.append(word_with_length)
    i += 1
    
# create (easy, normal, and hard) difficulty level list of words
easy_words = create_word_length_list(all_words, 4, 6)
normal_words = create_word_length_list(all_words, 6, 8)
hard_words = create_word_length_list(all_words, 8, 100)

# ask user for difficulty level
difficulty_level = input("Choose your level [Easy, Normal, or Hard]: ").casefold()
invalid_difficulty = True
while invalid_difficulty:
    if difficulty_level == 'easy' or difficulty_level == 'normal' or difficulty_level == 'hard':
        invalid_difficulty = False
    else:
        difficulty_level = input("Invalid input! Please type [Easy, Normal, or Hard]: ").casefold()

# choose random word based on user input of easy, normal, or hard
random_word = ''
if difficulty_level == 'easy':
    random_word = random.choice(easy_words)[0]
        # 'random.choice(seq)' function is imported from the 'random' module' and returns a random element from the non-empty sequence 'seq'
elif difficulty_level == 'normal':
    random_word = random.choice(normal_words)[0]
else:
    random_word = random.choice(hard_words)[0]

# start of the game: let the user know how many letters the computer's word contains
print(f"""The mystery word contains {len(random_word)} characters.""")
print(f"show mystery_word: {random_word}")
letter_guess = demand_valid_letter(input("Guess any letter: "))

already_guessed_list = []
incorrect_guess_count = 0
max_guess = 8
continue_game = True
while continue_game:

    # if the letter has already been guessed, tell user to guess again  
    if letter_guess in already_guessed_list:
        letter_guess = demand_valid_letter(input(f"[{letter_guess}] already guessed. Try again: ")).upper()

    # if the guessed letter is incorrect, let user know how many incorrect guesses they have left and tell user to guess again
    elif letter_guess not in already_guessed_list and letter_guess not in random_word:
        incorrect_guess_count += 1
        already_guessed_list.append(letter_guess)
        # if user has ran out of incorrect guesses, reveal the word and end the game
        if incorrect_guess_count == max_guess:
            print(f"Game Over. You lose! The word was: {random_word}")
            continue_game = False
        else:    
            print(f"Sorry, [{letter_guess}] is not in the mystery word.")
            letter_guess = demand_valid_letter(input(f"You get {max_guess - incorrect_guess_count} more incorrect guess(es). Try again: "))
        
    # if the guessed letter is correct, print the mystery word only displaying the correct guesses    
    else:
        already_guessed_list.append(letter_guess)
        print(f"Correct guess! [{letter_guess}] is in the mystery word")
        print_word(random_word, already_guessed_list)
        # if all the letters in the mystery word have been guessed, let the user know and end the game
        if is_word_done(random_word, already_guessed_list):
            print(f"Congratulations! You guessed the mystery word: {random_word}")
            break
        else:
            letter_guess = demand_valid_letter(input("Guess another letter: "))  

print("Done")



