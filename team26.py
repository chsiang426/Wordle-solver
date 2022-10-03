import sys

def play(ans, answers_file):
    guess_results = ""
    ignore_chars = "" 
    res = ""
    answer_words = load_words(answers_file)
    number_of_guesses = 0 
    time = 1
    
    res += f"{ans}\n"
    while len(answer_words) > 0:
        current_guess = pick_word(answer_words, ignore_chars)
        number_of_guesses += 1

        guess_results = evaluate_guess_results(ans, current_guess) 

        copy_guess_result = change_format(guess_results)
        res += f"{time}; {current_guess}; \"{copy_guess_result}\"\n"

        if guess_results == "11111":
            break

        answer_words, ignore_chars = filter_words(answer_words, current_guess, guess_results, ignore_chars)

        time+=1

    if guess_results == "11111":
        pass
    else:
        print("Could not guess word")
        sys.exit()

    return number_of_guesses, res

def change_format(s):
    result = ""
    for i in range(len(s)):
        if i != (len(s)-1):
            result += s[i]+','
        else:
            result += s[i]
    return result

def load_words(answers_file):
    answer_words = []

    # load all answer words
    with open(answers_file, "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                answer_words.append(word)

    return answer_words

def filter_words(words, guess_word, guess_result, ignore_chars):

    new_ignore_chars = ignore_chars
    for i in range(len(guess_result)):
        if guess_result[i] == "0":
            if guess_word[i] not in ignore_chars:
                new_ignore_chars += guess_word[i]

    return [word for word in words if match_guess_result(word, guess_word, guess_result)], new_ignore_chars

def pick_word(answer_words, ignore_chars):
    letter_frequency = {}
    placement_frequency = [{}]*6

    if len(answer_words) <= 2:
        return answer_words[0]

    #count letter frequency, ignore letters that have already been guessed
    for word in answer_words:
        ignore_chars_copy = ignore_chars
        placement_index = 0
        for letter in word:
            if letter in ignore_chars_copy:
                ignore_chars_copy = ignore_chars_copy.replace(letter,"",1)
            else:
                if letter not in letter_frequency:
                    letter_frequency[letter] = 0

                letter_frequency[letter] += 1

            if letter not in placement_frequency[placement_index]:
                placement_frequency[placement_index][letter] = 0
            placement_frequency[placement_index][letter] += 1

            placement_index += 1
    best_word = answer_words[0]
    max_frequency = 0
    max_placement_score = 0

    # find best word based on letter frequency, ignore letters that have already been guessed
    for word in answer_words:
        current_frequency = 0
        picked = set()
        ignore_chars_copy = ignore_chars
        for letter in word:
            if letter in ignore_chars_copy:
                ignore_chars_copy = ignore_chars_copy.replace(letter,"",1)
            else:
                if letter in picked:
                    continue
                picked.add(letter)
                if letter in letter_frequency:
                    current_frequency += letter_frequency[letter]

        if current_frequency > max_frequency:
            max_frequency = current_frequency
            best_word = word

            placement_score = 0
            for i in range(len(word)):
                if word[i] in placement_frequency[i]:
                    placement_score += placement_frequency[i][word[i]]
            max_placement_score = max_placement_score

        elif current_frequency == max_frequency:
            placement_score = 0
            for i in range(len(word)):
                if word[i] in placement_frequency[i]:
                    placement_score += placement_frequency[i][word[i]]

            if placement_score > max_placement_score:
                max_placement_score = placement_score
                best_word = word

    return best_word

def match_guess_result(word, guess_word, guess_result):
    for i in range(len(guess_result)):
        if guess_result[i] == "1" and word[i] != guess_word[i]:
            return False
        elif guess_result[i] == "2":
            if guess_word[i] == word[i]:
                return False
            elif guess_word[i] not in word:
                return False
        elif guess_result[i] == "0":
            if word[i] == guess_word[i]:
                return False

            wrong_letter_instances_guess = find_letter_indexes_in_word(guess_word, guess_word[i])
            okCount = 0
            for j in wrong_letter_instances_guess:
                if guess_result[j] != "0":
                    okCount += 1
            wrong_letter_instances_word = find_letter_indexes_in_word(word, guess_word[i])
            if len(wrong_letter_instances_word) > okCount:
                return False

    return True

def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

# return guess results for a given word
def evaluate_guess_results(correct, guess):
    result = '0'* len(correct)

    for index in range(len(correct)):
        if guess[index] == correct[index]:
            result = result[:index] + '1' + result[(index+1):]
            correct = correct.replace(guess[index], '@', 1)

    for index in range(len(correct)):
        if guess[index] in correct and result[index] == '0':
            result = result[:index] + '2' + result[(index+1):]
            correct = correct.replace(guess[index], '@', 1)

    return result


if __name__ == "__main__":
    sum = 0
    answers = []
    if len(sys.argv)!=4:
        print("Error")
        sys.exit(0)
    answers_file = sys.argv[1]
    test_words_file = sys.argv[2]
    response_file = sys.argv[3]

    with open(test_words_file, "r", newline="") as f:
        for word in f:
            word = word.lower().strip() 
            if len(word) == 5 and word.isalpha():          
                answers.append(word)
                
    with open(response_file, "w", newline="") as f:
        for ans in answers:
            total_guesses = 0
            total_guesses, result = play(ans, answers_file)
            f.write(f"{result}{total_guesses}\n")
  




