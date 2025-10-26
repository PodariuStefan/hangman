import string
import sys

def censor_word(input_word):
    input_len = len(input_word)
    new_word = ''
    for i in range(input_len):
        if i == 0 or i == input_len - 1:
            new_word += input_word[i]
        elif input_word[i] == input_word[0].lower() or input_word[i].lower() == input_word[input_len - 1]:
            new_word += input_word[i].lower()
        else:
            new_word += '*'

    return new_word

letters = ['e', 'a', 'i', 'u', 'o', 'ă', 'î', 'â','r', 'n', 't', 'c', 'l', 's', 'd', 'p', 'm', 'ș', 'v', 'f', 'b', 'g', 'ț', 'z', 'h', 'j', 'k', 'x', 'y', 'q']

game_id = 1

input_path = ""
output_path = ""
dict_path = ""
buffer = ""


def censored_word_indexer(word, target):
    return [i for i in range(len(target)) if word[i].upper() == target[i]]

def validation(guess, target):
    i, guesses = 0, 0
    global game_id, buffer
    status = "Fail"
    used_letters = []
    for letter in letters:
        if guess == target:
            status = "OK"
            break
        used_letters.append(letter)
        indices = [i for i in range(len(target)) if (letter.upper() == target[i] and letter.upper() not in guess)]
        if len(indices) == 0:
            guesses += 1
            continue
        for i in indices:
            guess = guess[0:i] + target[i] + guess[i + 1:] # removed upper method
        indices = indices.clear()
        guesses += 1
    buffer += f"{game_id}, {guesses}, {guess}, {status}, "
    print(f"Game id: {game_id}, cuvantul \"{guess}\" a fost gasit in {guesses} incercari.\
 Status: {status}.")
    print("Litere incercate: ", end="")
    for i in range(len(used_letters)):
        if i == len(used_letters) - 1:
            print(used_letters[i].upper())
            buffer += used_letters[i].upper() + '\n'
        else:
            print(used_letters[i].upper(), end=', ')
            buffer += used_letters[i].upper() + ', '
    return guesses

def collection(dictionary, guess, target): # dont forget to remove the potential list for less letter search
    priority = []
    for word in dictionary:
        if len(word.upper()) == len(guess):
            indicesAll = [i for i in range(len(target)) if (word[i].upper() == guess[i])]
            used_letters = []
            if indicesAll == censored_word_indexer(guess, target):
                priority.append(word)   
    return priority

def selector(container, guess, target):
    global game_id, buffer
    status = "Fail"
    guesses = 0
    used_letters = []
    for i in range(len(container)):
        for j in range(len(container[i])):
            if container[i][j] not in used_letters:
                used_letters.append(container[i][j])
                guesses += 1
            indices = [k for k in range(len(container[i])) if container[i][j] == target[j]]
            if any(indices):
                for q in indices:
                    guess = guess[:q] + target[q] + guess[q + 1:]
    if guess == target:
        status = "OK"
        buffer += f"{game_id}, {guesses}, {guess}, {status}, "
        print(f"Game id:{game_id}, cuvantul \"{guess}\" a fost gasit in {guesses} incercari.\
 Status: {status}.")
        print("Litere incercate: ", end="")
    for i in range(len(used_letters)):
        if i == len(used_letters) - 1:
            print(used_letters[i].upper())
            buffer += used_letters[i].upper() + '\n'
        else:
            print(used_letters[i].upper(), end=', ')
            buffer += used_letters[i].upper() + ', '
    game_id += 1
    return guess, guesses
    
def reshape(list):
    word_dict = {}
    id = 0
    for line in list:
        if id == 0:
            line = line.replace('\ufeff', '')
        line = line.strip()
        word_dict.update({id:line.split(";")})
        id += 1
            
    return word_dict

def main():
    global game_id, input_path, output_path, dict_path, buffer
    options = ["-i", "--input", "-o", "--output", "-d", "--dict", "-h", "--help"]
    args = sys.argv[1:]
    total_guesses = 0

    if len(args) != 6:
        print("Please make sure all fields are complete!")
        exit(1)
    for a in range(len(args)):
        if a % 2 == 0 and args[a] in options:
            match args[a] in options:
                case True:
                    pass
                case False:
                    print("Invalid arguments for main function, please use -h or --help for all options and their descriptions!")
                    exit(1)
        else:
            try:
                with open(args[a]) as test:
                    test.close()
            except FileNotFoundError:
                print(f"Please make sure the absolute paths are correct! Maybe check element number: {a} for mistakes.")
    
    input_path = args[1]
    output_path = args[3]
    dict_path = args[5]
                
    with open(input_path, 'r', encoding="UTF-8") as f, open(dict_path, 'r', encoding="UTF-8") as d:
        words = f.readlines()
        words = reshape(words)
        for keys in words:
            word_lst = []
        for line in d:
            word_lst.append(line.strip())
    for key in words:
        container = collection(word_lst, words[key][1], words[key][2])
        placeholder = selector(container, words[key][1], words[key][2])
        if placeholder[0] != words[key][2]:
            total_guesses += validation(placeholder[0], words[key][2]) + placeholder[1]
        else:
            total_guesses += placeholder[1]

    print(f"Numar total de incercari pentru {len(words)} de cuvinte este: {total_guesses}")

    with open(output_path, 'w', encoding="UTF-8") as o:
        o.write(buffer)

if __name__ == "__main__":
    main()
    

        

    
