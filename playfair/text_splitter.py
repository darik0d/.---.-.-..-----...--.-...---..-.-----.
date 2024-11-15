###########################
# Splits the string without spaces in to the words. Enjoy!
# The code is from the accepted answer here: https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
###########################
import math
import re
import os
from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).

def infer_spaces(s, lang):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""
    # Find the path starting with lang prefix
    path = [filename for filename in os.listdir("word_lists/without_frequency/") if filename.startswith(lang)]

    if len(path) > 1:
        print("There are multiple files with the same prefix. Please specify the language.")
        return
    path = path[0]
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    words = open("word_lists/without_frequency/" + path).read().split()
    wordcost = dict((k, log((i+1)*log(len(words)))) for i, k in enumerate(words))
    maxword = max(len(x) for x in words)
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))

def score_text(to_evaluate: str, langs=None):
    if langs is None:
        langs = ["en", "nl", "de", "fr", "es", "it"]
    best_score = math.inf
    best_lang = None
    current_score = 0
    for lang in langs:
        path = [filename for filename in os.listdir("word_lists/without_frequency/") if filename.startswith(lang)]
        if len(path) > 1:
            print("There are multiple files with the same prefix. Please specify the language.")
            return
        path = path[0]
        words = open("word_lists/without_frequency/" + path).read().split()
        # wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
        str_words = infer_spaces(to_evaluate, lang).split()
        not_found = 0
        for word_index in range(min(len(str_words), 100)): # Speedup the process by limiting
            try:
                word = str_words[word_index]
                # Get the rank of the word
                word_rank = words.index(word)
                # word_cost = log((word_rank + 1) * log(len(words)))
                word_cost = word_rank
                current_score += word_cost
            except:
                #print("Word not found in the list: ", word)
                not_found += 1
        # Penalize if a lot of words with 1 letter
        one_letter_words = len([word for word in str_words if len(word) == 1])
        current_score += one_letter_words * len(words) / 10
        current_score /= (len(str_words) - not_found)
        if best_score > current_score:
            best_score = current_score
            best_lang = lang
        current_score = 0

    return best_score, best_lang

def index_of_coincidence(string: str):
    n = len(string)
    freq = {}
    for char in string:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    ic = 0
    for key in freq:
        ic += freq[key] * (freq[key] - 1)
    ic /= n * (n - 1)
    return ic, "en" # Currently so
# Top english bigrams
bigrams_to_check = dict()
text = open("corpus/preprocessed/en/eng_news_2005_100K-sentences.txt").read()
bigrams = re.findall(r".{1,2}", text)
for bigram in bigrams:
    if bigram in bigrams_to_check:
        bigrams_to_check[bigram] += 1
    else:
        bigrams_to_check[bigram] = 1
for bigram in bigrams_to_check:
    bigrams_to_check[bigram] /= len(bigrams)
# Sort
bigrams_to_check = dict(sorted(bigrams_to_check.items(), key=lambda item: item[1], reverse=True))

def twonorm_frequency_distance(string: str):
    """
    Calculate the two norm distance between the bigram frequencies of the string and the bigrams_to_check.

    :param string: The string to calculate the bigram frequencies.
    :param bigrams_to_check: The bigram frequencies to compare with.
    """
    distance = 0
    bigrams = re.findall(r".{1,2}", string)
    bigram_frequency = {}
    for bigram in bigrams:
        if bigram in bigram_frequency:
            bigram_frequency[bigram] += 1
        else:
            bigram_frequency[bigram] = 1
    bigram_frequency = dict(sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True))
    for bigram in bigram_frequency:
        bigram_frequency[bigram] /= len(bigrams)
    for bigram in bigrams_to_check:
        if bigram in bigram_frequency:
            distance += (bigrams_to_check[bigram] - bigram_frequency[bigram]) ** 2
    distance = math.sqrt(distance)
    return distance, "en" # Currently so

if __name__ == "__main__":
    s = "De naam en inspiratie komen van een Engelse termannealinguitgloeien binnen de metaalbewerking. Het betreft een techniek waarbij metaal verhit wordt en daarna gecontroleerd afgekoeld om de grootte van de kristallen binnen het materiaal te vergroten en daarmee het aantal defecten te verkleinen. "
    s = "The name of the algorithm comes from annealing in metallurgy, a technique involving heating and controlled cooling of a material to alter its physical properties. Both are attributes of the material that depend on their thermodynamic free energy."
    s = "La methode vient du constat que le refroidissement naturel de certains metaux ne permet pas aux atomes de se placer dans la configuration la plus solide. La configuration la plus stable est atteinte en maitrisant le refroidissement et en le ralentissant par un apport de chaleur externe, ou bien par une isolation. "
    #s = "aaarhdkssmsdmssdfsfgsfgsxsarfrwe"
    s = "ucncgtuetgawumnmabdfarpdtambzffyuwfqsgcetwhwnuvfhryunodmfqfygfymmpbgcmotwakotczfeacetwawhksiyeupkulhlueuawuqfksnmdqtfsnupumynutolndtrmmcvuzelutfbgnumpcmcvlupumyxknmoiftbgrnkbnwgtuetgawmrgtiavtupxdgdnupumynuvuzddmnrabysaqfupxcsugsodfufqtrcmtnuianwhdvnywuvtbtciosovwwupdbkftwurhcvnumpxpyuezrfuwiurnupkfumnmuqnurfwfvfmnuwtbnoiosovwwunuuoumtwvffssuptnukbcmrhfahtuqhbgtoknuuoawpdftqtvffkivrfuwvutqaifntwysxprnaikxqbabsixmairfxmzffybkeyvtbdfkdwvnxduvteuqutyhbnswpuzfnddmslnmnubagtokuqsgfkibmtbdfkivqafkzffyfqqtuvulqfntzfnrtomtbagtoknufkugwutbiqfkwohdvtkybtpxfanuianwhdvnywuvftcetwabuqcmdmcsiopuqtqyxknmnwnwtgupqucusuyqdsuqfklwmdmbpmylnmgthlqtintqnumpfkanfkwaorfkivossmysrffazfidlrbsyecmotwakomsmbfaabfkfslnfnzfnrthawgfvacmrquqshqdbzgsfakxsmalfabkdhzbsnfopumtpuymgfqtqyiarnundmilvnxsmtnukbuwosgtispuymfvfnqtqyiarndkdmtcdmilvniwsivanhwuabfkswfobavfiaadmcdmfthdrfclnmhsuovanubtvfiaadmcdmbkaxzdcmhdlulogfdmrhfalwmbyhtgtlnhbarozlsofaarpasmysrawvdmodmlpxuioskxuqpawufyfndmilvnawhcoretfky"

    print(index_of_coincidence(s))

    s = s.lower()
    s = s.replace(" ", "")
    s = s.replace(",", "")
    s = s.replace(".", "")
    score, lang = score_text(s)
    print(infer_spaces(s, lang))
    print(score, lang)