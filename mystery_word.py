import string, random

def convert_to_list(a_file):
    """
    Given a text file, return a list of words
    """
    with open(a_file) as file:
        text = file.read()
        # '.read()' reads whole file (character by character)
        # '.readlines()' reads whole file (line by line)
        # '.readline()' reads one line (line by line each time method is called)
    all_words = []
    for word in text.split("\n"):
        if word != '':
            all_words.append(word.upper())
    return all_words

def difficulty_level():
    """
    Ask user for difficulty level ("easy", "normal", or "hard") and return it
    if valid input, then continue...otherwise keep asking for valid input
    """
    difficulty_level = input("Choose your level [Easy, Normal, or Hard]: ").casefold()
    invalid_difficulty = True
    while invalid_difficulty:
        if difficulty_level in ["easy", "normal", "hard"]:
            invalid_difficulty = False
        else:
            difficulty_level = input("Invalid input! Please type [Easy, Normal, or Hard]: ").casefold()
    return difficulty_level

def create_difficulty_list(a_str, a_list):
    """
    Given a string ("easy", "normal", or "hard") and a list of all words,
    return a list of words with specific lengths
    """
    min_length = 0
    max_length = 0
    if a_str == "easy":
        min_length = 4
        max_length = 6
    elif a_str == "normal":
        min_length = 6
        max_length = 8
    else:
        min_length = 8
        max_length = 100
    # return a list using list comprehension
    return [word # collection: do something to each item in a list
            for word in a_list # iteration: iterate through each item 'word' in a list 'a_list'
            if min_length <= len(word) <= max_length] # selection: set a condition

def verify_valid_letter(a_str):
    """
    Given a string, keep asking for input until a letter or hyphen is inputted and return it
    """
    valid_letters = string.ascii_letters + "-"
        # valid letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' + '-'
    invalid_guess = True
    while invalid_guess:
        if a_str not in valid_letters or a_str == "":
            a_str = input("Invalid letter! Please type a letter: ")
        else:
            invalid_guess = False
    return a_str.upper()

def display_correct_letter(letter, guesses):
    """
    Conditionally display a letter. If the letter is already in the list `guesses`, 
    then return it...otherwise, return "_".
    """
    if letter in guesses:
        return letter
    else:
        return "_"

def print_word(word, guesses):
    """
    Prints 'word' to the screen displaying only letters in the list 'guesses' 
    and underscores as placeholders for letters not in the list
    """
    correct_guess_list = [display_correct_letter(letter, guesses) # collection: 'guesses' here represents list 
                                                                  # of characters already guessed
                          for letter in word] # iteration: 'word' here represents random word
    print(" ".join(correct_guess_list))

def is_word_done(word, guesses):
    """
    Given a random word 'word' and list of characters already guessed 'guesses',
    return True if all the characters in the random word have been guessed
    """
    correct_word = ""
    for letter in word:
        if letter in guesses:
            correct_word += letter
    if correct_word == word:
        return True
    return False

def mystery_word_game(a_file):
    """
    Given a text file, run the mystery word game
    """
    all_words = convert_to_list(a_file)
    continue_mystery_word = True
    while continue_mystery_word:
        # ask user for difficulty level and create a list of words based on level
        difficulty_list = create_difficulty_list(difficulty_level(), all_words)

        # choose random word from created list
        random_word = random.choice(difficulty_list)

        # start of the game: let the user know how many letters the computer's word contains
        print(f"""The mystery word contains {len(random_word)} characters.""")
        print(f"show mystery_word: {random_word}")
        letter_guess = verify_valid_letter(input("Guess any letter: "))
        
        already_guessed_list = []
        incorrect_guess_count = 0
        max_guess = 8
        go_again_answer = ""

        continue_round = True
        while continue_round:

            # if the letter has already been guessed, tell user to guess again  
            if letter_guess in already_guessed_list:
                letter_guess = verify_valid_letter(input(f"[{letter_guess}] already guessed. Try again: ")).upper()

            # if the guessed letter is incorrect, let user know how many incorrect guesses they have left 
            # and tell user to guess again
            elif letter_guess not in already_guessed_list and letter_guess not in random_word:
                incorrect_guess_count += 1
                already_guessed_list.append(letter_guess)
                # if user has ran out of incorrect guesses, reveal the word and end the game
                if incorrect_guess_count == max_guess:
                    print(f"Game Over. You lose! The word was: {random_word}")
                    
                    # ask user if they want to again: if yes then exit inner while loop,
                    # otherwise exit both inner and outer while loops
                    go_again_answer = input(f"Do you want to go again (Y/N)? ").upper()
                    if go_again_answer == 'Y':
                        continue_round = False
                    else:
                        continue_round = False
                        continue_mystery_word = False
                else:    
                    print(f"Sorry, [{letter_guess}] is not in the mystery word.")
                    letter_guess = verify_valid_letter(input(f"You get {max_guess - incorrect_guess_count} more incorrect guess(es). Try again: "))
                
            # if the guessed letter is correct, print the mystery word only displaying the correct guesses    
            else:
                already_guessed_list.append(letter_guess)
                print(f"Correct guess! [{letter_guess}] is in the mystery word")
                print_word(random_word, already_guessed_list)

                # if all the letters in the mystery word have been guessed, let the user know and end the game
                if is_word_done(random_word, already_guessed_list):
                    print(f"Congratulations! You guessed the mystery word: {random_word}")

                    # ask user if they want to go again: 
                    # if yes then exit inner while loop, otherwise exit both inner and outer while loops
                    go_again_answer = input(f"Do you want to go again (Y/N)? ").upper()
                    if go_again_answer == 'Y':
                        continue_round = False
                    else:
                        continue_round = False
                        continue_mystery_word = False
                else:
                    letter_guess = verify_valid_letter(input("Guess another letter: "))

mystery_word_game("words.txt")