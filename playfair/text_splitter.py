###########################
# Splits the string without spaces in to the words. Enjoy!
# The code is from the accepted answer here: https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
###########################
import math
import re
import os
import string
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
bigrams.extend(re.findall(r".{1,2}", text[1:]))
for bigram in bigrams:
    if bigram in bigrams_to_check:
        bigrams_to_check[bigram] += 1
    else:
        bigrams_to_check[bigram] = 1
for bigram in bigrams_to_check:
    bigrams_to_check[bigram] += 1
    bigrams_to_check[bigram] /= (len(bigrams) + 1) # Smoothing!
    bigrams_to_check[bigram] = math.log10(bigrams_to_check[bigram])
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
    bigrams.extend(re.findall(r".{1,2}", string[1:]))
    bigram_frequency = {}
    for bigram in bigrams:
        if bigram in bigram_frequency:
            bigram_frequency[bigram] += 1
        else:
            bigram_frequency[bigram] = 1
    bigram_frequency = dict(sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True))
    for bigram in bigram_frequency:
        if bigram in bigrams_to_check: # Normally should be ok
            # distance += (bigrams_to_check[bigram] - bigram_frequency[bigram]) ** 2
            distance += bigrams_to_check[bigram]*bigram_frequency[bigram]
    distance /= len(bigrams)
    return distance, "en" # Currently so

# # Quadrams (old version with own file)
#
# # Top english bigrams
# quadrams_to_check = dict()
# text = open("corpus/preprocessed/en/eng-uk_web_2002_1M-sentences.txt").read()
# quadrams = re.findall(r"[a-z]{4}", text)
# quadrams.extend(re.findall(r"[a-z]{4}", text[1:]))
# quadrams.extend(re.findall(r"[a-z]{4}", text[2:]))
# quadrams.extend(re.findall(r"[a-z]{4}", text[3:]))
# added = 0
# for quadram in quadrams:
#     if quadram in quadrams_to_check:
#         quadrams_to_check[quadram] += 1
#     else:
#         quadrams_to_check[quadram] = 1
# alph = list(string.ascii_lowercase)
# alph.remove("j")
# for l1 in alph.copy():
#     for l2 in alph.copy():
#         for l3 in alph.copy():
#             for l4 in alph.copy():
#                 if l1 + l2 + l3 + l4 not in quadrams_to_check:
#                     quadrams_to_check[l1 + l2 + l3 + l4] = 1
#                     added += 0.01
# #quadrams_length = len(quadrams) + added
# quadrams_length = len(quadrams)
# for quadram in quadrams_to_check:
#     quadrams_to_check[quadram] /= quadrams_length
#     quadrams_to_check[quadram] = math.log10(quadrams_to_check[quadram])
# # Sort
# quadrams_to_check = dict(sorted(quadrams_to_check.items(), key=lambda item: item[1], reverse=True))
#
# def twonorm_frequency_distance_with_quadrams(string: str):
#     """
#     Calculate the two norm distance between the quadram frequencies of the string and the quadrams_to_check.
#
#     :param string: The string to calculate the quadram frequencies.
#     :param quadrams_to_check: The quadram frequencies to compare with.
#     """
#     distance = 0
#     quadramss = re.findall(r"[a-z]{4}", string)
#     quadramss.extend(re.findall(r"[a-z]{4}", string[1:]))
#     quadramss.extend(re.findall(r"[a-z]{4}", string[2:]))
#     quadramss.extend(re.findall(r"[a-z]{4}", string[3:]))
#     # quadram_frequency = {}
#     # for quadram in quadramss:
#     #     if quadram in quadram_frequency:
#     #         quadram_frequency[quadram] += 1
#     #     else:
#     #         quadram_frequency[quadram] = 1
#     # quadram_frequency = dict(sorted(quadram_frequency.items(), key=lambda item: item[1], reverse=True))
#     # for quadram in quadram_frequency:
#     #     if quadram in quadrams_to_check:
#     #         distance += quadrams_to_check[quadram]*quadram_frequency[quadram]
#     #     else:
#     #         NOT_FOUND_FREQUENCY = math.log10((1.0 / quadrams_length))
#     #         distance += NOT_FOUND_FREQUENCY * quadram_frequency[quadram]
#     for quadram in quadramss:
#         distance += quadrams_to_check[quadram]
#
#     # distance /= len(quadramss)
#     return distance, "en" # Currently so

strange_quadgrams = {}
strange_list = []
q_file = open("./stats/en/quadrams.txt")
for line in q_file:
    line = line[:-1] # remove \n
    if line[0] != "-": continue
    if line[-1] == ",": line = line[:-1]
    strange_list.append(float(line))
alph = list(string.ascii_lowercase)
i = 0
for l1 in alph.copy():
    for l2 in alph.copy():
        for l3 in alph.copy():
            for l4 in alph.copy():
                strange_quadgrams[l1 + l2 + l3 + l4] = strange_list[i]
                i += 1

def twonorm_frequency_distance_with_quadrams(string: str):
    """
    Calculate the two norm distance between the quadram frequencies of the string and the quadrams_to_check.

    :param string: The string to calculate the quadram frequencies.
    :param quadrams_to_check: The quadram frequencies to compare with.
    """
    distance = 0
    for i in range(len(string)-4):
        q = string[i:i+4]
        score = strange_quadgrams[q]
        distance += score
    return distance, "en"

if __name__ == "__main__":
    s = "De naam en inspiratie komen van een Engelse termannealinguitgloeien binnen de metaalbewerking. Het betreft een techniek waarbij metaal verhit wordt en daarna gecontroleerd afgekoeld om de grootte van de kristallen binnen het materiaal te vergroten en daarmee het aantal defecten te verkleinen. "
    s = "The name of the algorithm comes from annealing in metallurgy, a technique involving heating and controlled cooling of a material to alter its physical properties. Both are attributes of the material that depend on their thermodynamic free energy."
    s = "La methode vient du constat que le refroidissement naturel de certains metaux ne permet pas aux atomes de se placer dans la configuration la plus solide. La configuration la plus stable est atteinte en maitrisant le refroidissement et en le ralentissant par un apport de chaleur externe, ou bien par une isolation. "
    #s = "aaarhdkssmsdmssdfsfgsfgsxsarfrwe"
    s = "ucncgtuetgawumnmabdfarpdtambzffyuwfqsgcetwhwnuvfhryunodmfqfygfymmpbgcmotwakotczfeacetwawhksiyeupkulhlueuawuqfksnmdqtfsnupumynutolndtrmmcvuzelutfbgnumpcmcvlupumyxknmoiftbgrnkbnwgtuetgawmrgtiavtupxdgdnupumynuvuzddmnrabysaqfupxcsugsodfufqtrcmtnuianwhdvnywuvtbtciosovwwupdbkftwurhcvnumpxpyuezrfuwiurnupkfumnmuqnurfwfvfmnuwtbnoiosovwwunuuoumtwvffssuptnukbcmrhfahtuqhbgtoknuuoawpdftqtvffkivrfuwvutqaifntwysxprnaikxqbabsixmairfxmzffybkeyvtbdfkdwvnxduvteuqutyhbnswpuzfnddmslnmnubagtokuqsgfkibmtbdfkivqafkzffyfqqtuvulqfntzfnrtomtbagtoknufkugwutbiqfkwohdvtkybtpxfanuianwhdvnywuvftcetwabuqcmdmcsiopuqtqyxknmnwnwtgupqucusuyqdsuqfklwmdmbpmylnmgthlqtintqnumpfkanfkwaorfkivossmysrffazfidlrbsyecmotwakomsmbfaabfkfslnfnzfnrthawgfvacmrquqshqdbzgsfakxsmalfabkdhzbsnfopumtpuymgfqtqyiarnundmilvnxsmtnukbuwosgtispuymfvfnqtqyiarndkdmtcdmilvniwsivanhwuabfkswfobavfiaadmcdmfthdrfclnmhsuovanubtvfiaadmcdmbkaxzdcmhdlulogfdmrhfalwmbyhtgtlnhbarozlsofaarpasmysrawvdmodmlpxuioskxuqpawufyfndmilvnawhcoretfky"
    s = "ALICEDELLAROCCAODIAVALASCUOLADISCIODIAVALASVEGLIAALLESETTEEMEZZODELMATTINOANCHENELLEVACANZEDINATALEESUOPADRECHEACOLAZIONELAFISSAVAESOTTOILTAVOLOFACEVABALLARELAGAMBANERVOSAMENTECOMEADIRESUSBRIGATIODIAVALACALZAMAGLIADILANACHELAPUNGEVASULLECOSCELEMOFFOLECHENONLELASCIAVANOMUOVERELEDITAILCASCOCHELESCHIACCIAVALEGUANCEEPUNTAVACONILFERROSULLAMANDIBOLAEPOIQUEGLISCARPONISEMPRETROPPOSTRETTICHELAFACEVANOCAMMINARECOMEUNGORILLA".lower()
    print(index_of_coincidence(s))

    s = s.lower()
    s = s.replace(" ", "")
    s = s.replace(",", "")
    s = s.replace(".", "")
    score, lang = score_text(s)
    print(infer_spaces(s, lang))
    print(score, lang)