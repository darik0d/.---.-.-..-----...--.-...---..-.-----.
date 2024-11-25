import itertools
from math import ceil
from random import randint

# read the ciphertext
file = open("opgave.txt", "r")
raw_text = file.read()
file.close()

# reconstruct the column-swapped text
keylen = 9
colheight = ceil(len(raw_text)/keylen)
unordered_columns = [raw_text[i*colheight:(i+1)*colheight] for i in range(keylen)]
order = (3, 1, 6, 8, 4, 2, 5, 0, 7)
columns = []
for i in order:
    columns.append(unordered_columns[i])
after_column_swap = ""
for i in range(colheight):
    for j in range(keylen):
        try:
            newchar = columns[j][i]
        except IndexError:
            newchar = ""
        after_column_swap += newchar
        
# from https://en.wikipedia.org/wiki/Letter_frequency
french_letter_frequencies = {'E': 0.162, 'A': 0.076, 'S': 0.079, 'I': 0.075, 'T': 0.072, 'N': 0.070, 'R': 0.066, 'U': 0.063, 'L': 0.054, 'O': 0.057, 'D': 0.036, 'C': 0.032, 'P': 0.025, 'M': 0.029, 'V': 0.018, 'G': 0.008, 'B': 0.009, 'F': 0.010, 'Q': 0.013, 'H': 0.009, 'J': 0.008, 'X': 0.003, 'Z': 0.003, 'Y': 0.002, 'K': 0.001, 'W': 0.001}
french_letter_frequencies = sorted(french_letter_frequencies.items(), key=lambda x: x[1], reverse=True)
# frequencies of our column-swapped text
freqs = {'AA': 1, 'AD': 17, 'DA': 77, 'AF': 13, 'FA': 26, 'AG': 35, 'GA': 0, 'AV': 156, 'VA': 0, 'AX': 87, 'XA': 184, 'DD': 0, 'DF': 0, 'FD': 10, 'DG': 82, 'GD': 153, 'DV': 49, 'VD': 439, 'DX': 0, 'XD': 20, 'FF': 149, 'FG': 177, 'GF': 0, 'FV': 0, 'VF': 0, 'FX': 0, 'XF': 230, 'GG': 25, 'GV': 0, 'VG': 166, 'GX': 0, 'XG': 80, 'VV': 0, 'VX': 134, 'XV': 184, 'XX': 8}
freqs_sum = sum(freqs.values())
freqs = {key: value/freqs_sum for key, value in freqs.items() if value > 0}
sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)


def decode_text(text, assignment):
    """
    Performs a substitution on the text using the assignment dictionary.
    """
    decoded = ""
    for j in range(0, len(text), 2):
        digram = text[j:j+2]
        if digram in assignment:
            decoded += assignment[digram]
        else:
            decoded += " "
    return decoded

def fitness(text):
    """
    Fitness function for hill climbing.
    """
    n = 4
    # from http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/french-letter-frequencies/
    ngram_frequencies = {
        "TION" :  0.43,        "EDES" :  0.14,        "EDEL" :  0.11,
        "MENT" :  0.34,        "ONDE" :  0.14,        "QUES" :  0.11,
        "EMEN" :  0.25,        "IOND" :  0.13,        "COMM" :  0.11,
        "DELA" :  0.24,        "IONS" :  0.13,        "ENTD" :  0.11,
        "ATIO" :  0.24,        "ANSL" :  0.12,        "EURS" :  0.11,
        "IQUE" :  0.23,        "AIRE" :  0.12,        "NTDE" :  0.11,
        "ELLE" :  0.20,        "PLUS" :  0.12,        "PART" :  0.10,
        "DANS" :  0.19,        "ILLE" :  0.12,        "NTRE" :  0.10,
        "POUR" :  0.17,        "QUEL" :  0.12,        "OUVE" :  0.10,
        "ESDE" :  0.15,        "SONT" :  0.11,        "ENTE" :  0.10
    }
    score = 0
    for i in range(0, len(text)-n, 1):
        ngram = text[i:i+n]
        if ngram in ngram_frequencies:
            score += n*ngram_frequencies[ngram]
        
    return score

def get_random_bigram():
    """
    Gets a random bigram from the bigrams available in the text.
    """
    global sorted_freqs
    i = randint(0, len(sorted_freqs)-1)
    return sorted_freqs[i][0]
    

def hill_climbing():    
    global after_column_swap
    global sorted_freqs
    global french_letter_frequencies
    
    # initialize the assignment dictionary with the expected frequencies
    assignment = {}
    for i in range(len(sorted_freqs)):
        assignment[sorted_freqs[i][0]] = french_letter_frequencies[i][0]
    
    # maximum number of swaps to try per assignment
    max_swaps_per_assignment = (len(sorted_freqs)-1)**2
    
    # compute the initial score
    decoded = decode_text(after_column_swap, assignment)
    score = fitness(decoded)
    # keep track of the swaps that have been tried so far - to avoid trying the same swap twice
    tried_swaps = set()
    while True:
        # *Stochastic* hill climbing
        first = get_random_bigram()
        second = first
        while second == first and (first, second) not in tried_swaps:
            second = get_random_bigram()
            
        # do the swap
        tried_swaps.add((first, second))
        new_assignment = {key: value for key, value in assignment.items()}
        new_assignment[first], new_assignment[second] = new_assignment[second], new_assignment[first]
        # compute the new score
        new_decoded = decode_text(after_column_swap, new_assignment)
        new_score = fitness(new_decoded)
        if new_score > score:
            # if the new score is better, update the assignment and the score
            score = new_score
            tried_swaps = set()
            assignment = new_assignment
            print(f"new best score {score} with assignment {assignment}")
            print(f"decoded text: {new_decoded}")
        elif len(tried_swaps) > max_swaps_per_assignment:
            # if all possible swaps have been tried, stop
            # this is a local maximum
            break

if __name__ == "__main__":
    hill_climbing()
