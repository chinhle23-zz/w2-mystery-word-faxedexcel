import string

def convert_to_list(a_file):
    """
    Given a text file, return a list of words
    """
    with open(a_file) as file:
        text = file.readlines()
        # '.read()' reads whole file (character by character)
        # '.readlines()' reads whole file (line by line and places each line into list)
        # '.readline()' reads one line (line by line each time method is called)
    all_words = []    
    for line in text:
        all_words.append(line.replace("\n","").upper())
    return all_words

def word_length(a_list):
    """
    Prompt user for a word length and return it
    if valid input, then continue...otherwise keep prompting for valid input
    """
    possible_lengths = []
    for word in a_list:
        if len(word) not in possible_lengths:
            possible_lengths.append(len(word))
    print(sorted(possible_lengths))

    length = input("Choose your word length: ")
    invalid_length = True
    while invalid_length:
        if not length.isdigit():
            length = input(f"{length} is not a valid input. Try again: ")
        elif int(length) in possible_lengths:
            invalid_length = False
        else:
            length = input(f"Words {length} characters long do not exist. Try again: ")
    return int(length)

def num_of_guesses():
    """
    Prompt user for a number of guesses and return it
    if valid input, then continue...otherwise keep prompting for valid input
    """
    guesses = input("How many guesses do you want? ")
    invalid_input = True
    while invalid_input:
        if not guesses.isdigit() or int(guesses) < 1:
            guesses = input(f"{guesses} is not a valid input. Try again: ")
        else:
            invalid_input = False   
    return int(guesses)  

def want_words_remain():
    """
    Prompt user if they want to have a running total of the number of words remaining
    if 'y', then return true, otherwise return false
    """
    if input("Do you want a running total of the number of words remaining (Y/N)? ").casefold() == 'y':
        return True
    else:
        return False

def print_word(guessed_list, remain_list):
    """
    Prints first item of 'remain_list' to the screen displaying only correct letters in 'guessed_list' 
    and underscores as placeholders for letters not in 'guessed_list'
    """
    possible_word = []
    for letter in remain_list[0]:
        if letter in guessed_list:
            possible_word.append(letter)
        else:
            possible_word.append("_")
    return " ".join(possible_word)

def verify_valid_letter(a_str):
    """
    Given a string, keep asking for input until a letter is inputted and return it
    """
    valid_letters = string.ascii_letters
        # valid letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    invalid_letter = True
    while invalid_letter:
        if a_str not in valid_letters or a_str == "":
            a_str = input("Invalid letter! Please type a letter: ")
        else:
            invalid_letter = False
    return a_str.upper()

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

def demon_list(guess_list, remain_list):
    possible_words = []
    i = 0 
    while i < len(remain_list):
        word = []
        for letter in remain_list[i]:
            if letter in guess_list:
                word.append(letter)
            else:
                word.append("_") 
        possible_words.append(" ".join(word))
        i += 1
    zipped_list = list(zip(possible_words, remain_list))

    distinct_list = []
    i = 0
    while i < len(zipped_list):
        for word in zipped_list[i]:
            if zipped_list[i][0] not in distinct_list:
                distinct_list.append(zipped_list[i][0])
        i += 1

    occurence_list = []
    for word in (distinct_list):
        counter = 0
        i = 0
        while i < len(zipped_list):
            if word == zipped_list[i][0]:
                counter += 1
            i += 1
        occurence_list.append([word, counter])
        
    i = 0 
    max_occurence = occurence_list[0][1]
    while i < len(occurence_list):
        if occurence_list[i][1] > max_occurence:
            max_occurence = occurence_list[i][1]
        i += 1

    demon_word = ""
    i = 0
    while i < len(occurence_list):
        if occurence_list[i][1] == max_occurence:  
            demon_word = occurence_list[i][0]
        i += 1

    cheat_list = []
    i = 0
    while i < len(zipped_list):
        if zipped_list[i][0] == demon_word:
            cheat_list.append(zipped_list[i][1])
        i += 1 


    return cheat_list

continue_game = True
while continue_game:
    # create list of all possible words
    all_words = convert_to_list("dictionary.txt")

    # call 'word_length()' function to ask user for a word length and store in the variable 'length'
    length = word_length(all_words)

    # cut down the 'all_words' list so that it only contains words with the user specified length
    remaining_list = [word for word in all_words if len(word) == length]

    # call 'num_of_guess()' function to ask user for max number of incorrect guesses and store it
    max_guesses = num_of_guesses()

    incorrect_guesses = 0
    already_guessed = []
    continue_round = True
    while continue_round:
        if max_guesses - incorrect_guesses == 0:
            print(f"Sorry, you lose. The word was {remaining_list[0]}")
            continue_round = False
            answer = input(f"The game has ended. Do you want to play again (Y/N)? ")
            if answer == 'y' or answer =='Y':
                continue_game = True
                incorrect_guesses = 0
                already_guessed = []
            else:
                continue_game = False

        else:
            print(f"You have {max_guesses - incorrect_guesses} remaining incorrect guess(es).")
            print(f"Letters already guessed: {already_guessed}")

            # ask user if they want to have a running total of the number of words remaining
            if want_words_remain():
                print(f"There are {len(remaining_list)} word(s) remaining")

            # ask user to guess a letter    
            letter_guess = verify_valid_letter(input("Guess any letter: "))

            while letter_guess in already_guessed:
                letter_guess = verify_valid_letter(input(f"[{letter_guess}] already guessed. Try again: ")).upper()
            
            already_guessed.append(letter_guess)

            # pare down remaining list based on user's letter guess
            remaining_list = demon_list(already_guessed, remaining_list)
            demon_word = print_word(already_guessed, remaining_list)

            if letter_guess in demon_word:
                print(f"Good guess. [{letter_guess}] is in the word")
                if is_word_done(remaining_list[0], already_guessed):
                    print(f"Congratulations, you win! Answer: {remaining_list[0]}")
                    continue_round = False
                    answer = input(f"The game has ended. Do you want to play again (Y/N)? ")
                    if answer == 'y' or answer =='Y':
                        continue_game = True
                        incorrect_guesses = 0
                        already_guessed = []
                    else:
                        continue_game = False
            else:
                print(f"Sorry, [{letter_guess}] is not in the word.")
                incorrect_guesses += 1

        if continue_round:
            print(demon_word)
            print(remaining_list)

print("Done")
