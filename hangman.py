import os
import string

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

def validation(guess, target):
    i, guesses = 0, 0
    for letter in letters:
        if guess == target:
            break
        indices = [i for i in range(len(target)) if (letter.upper() == target[i] and letter.upper() not in guess)]
        #if letter.upper() in guess:
        #    pass
        if len(indices) == 0:
            guesses += 1
            continue
        for i in indices:
            guess = guess[0:i] + target[i].upper() + guess[i + 1:]
        indices = indices.clear()
        guesses += 1
        
    print(f"Cuvantul \"{guess}\" a fost gasit in {guesses} incercari.")
    return guesses

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

if __name__ == "__main__":
    with open("data/cuvinte_de_verificat.txt", 'r') as f:
        total_guesses = 0
        words = f.readlines()
        words = reshape(words)
        for key in words:
            total_guesses += validation(words[key][1], words[key][2])
        print(f"Numar total de incercari pentru {len(words)} de cuvinte este: {total_guesses}")
        
                
    

        

    
