###########################
# Splits the string without spaces in to the words. Enjoy!
# The code is from the accepted answer here: https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
###########################

import re
import os
from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("word_lists/without_frequency/en_eng_news_2005_100K-sentences.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)
words_with_freq = open("word_lists/with_frequency/en_eng_news_2005_100K-sentences.txt").read().split("\n")
# TODO

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

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