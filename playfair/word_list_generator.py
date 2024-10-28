#######################
# The purpose of this file is to provide a function to generate a word list from the corpus.
#######################

import os
import re
from collections import Counter

def generate_word_list(corpus_path: str, output_path: str, with_frequency = True) -> None:
    """
    Generate a word list from the corpus.

    :param corpus_path: The path to the corpus.
    :param output_path: The path to the output file.
    """

    # Read the corpus
    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = f.read()
    # Remove special characters
    corpus = re.sub(r"[^a-zA-Z0-9\s]", "", corpus)
    # Convert to lowercase
    corpus = corpus.lower()
    # Tokenize the corpus
    words = re.findall(r"\b\w+\b", corpus)

    # Count the frequency of each word
    word_frequency = Counter(words)

    # Sort the words by frequency
    word_frequency = dict(sorted(word_frequency.items(), key=lambda item: item[1], reverse=True))

    # Write the word list to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        if with_frequency:
            for word, frequency in word_frequency.items():
                f.write(f"{word} {frequency}\n")
        else:
            for word in word_frequency.keys():
                f.write(f"{word}\n")

# Generate the word list
if __name__ == "__main__":

    if not os.path.exists("word_lists"):
        os.makedirs("word_lists")

    if not os.path.exists("word_lists/with_frequency"):
        os.makedirs("word_lists/with_frequency")

    if not os.path.exists("word_lists/without_frequency"):
        os.makedirs("word_lists/without_frequency")

    for folder in os.listdir("corpus/original"):
        if os.path.isdir(f"corpus/original/{folder}"):
            for filename in os.listdir(f"corpus/original/{folder}"):
                if filename.endswith(".txt"):
                    generate_word_list(f"corpus/original/{folder}/{filename}",
                                       f"word_lists/with_frequency/{folder}_{filename}")
                    generate_word_list(f"corpus/original/{folder}/{filename}",
                                       f"word_lists/without_frequency/{folder}_{filename}", False)