"""
This file contains code for preprocessing the corpus.
Goal: remove unwanted characters and replace some characters with their corresponding characters.
Run this file to preprocess the corpus. The preprocessed files will be saved in the preprocessed folder.
Working directory should be playfair/corpus.
"""

import re
import multiprocessing
import os

permittable_characters = "abcdefghiklmnopqrstuvwxyz"
# TODO: is "ß": "ss" correct?
replace_characters = {"j": "i", "ü": "u", "ö": "o", "ä": "a", "ß": "ss",
                      "é": "e", "è": "e", "ê": "e", "à": "a", "â": "a", "ç": "c",
                      "ô": "o", "û": "u", "î": "i", "ï": "i", "ë": "e", "ù": "u", "œ": "oe", "æ": "ae"}
possible_characters = permittable_characters + "".join(replace_characters.keys())

# Calculate the number of folders in the original folder
number_of_threads = len([f for f in os.listdir("original") if os.path.isdir(f"original/{f}")])

# Preprocess each folder separately
def preprocess_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            preprocess_file(os.path.join(folder, filename))


def preprocess_file(file):

    with open(file, "r", encoding="utf8") as f:
        text = f.read()
    text = preprocess_text(text)
    # Write the preprocessed text to a new file in preprocessed folder/language_name
    preprocessed_folder = os.path.join("preprocessed", os.path.basename(os.path.dirname(file)))
    os.makedirs(preprocessed_folder, exist_ok=True)
    with open(os.path.join(preprocessed_folder, os.path.basename(file)), "w") as f:
        f.write(text)


def preprocess_text(text):
    text = text.lower()
    # Remove all characters that are not in possible_characters
    text = re.sub(f"[^{possible_characters}]", "", text)
    for char in replace_characters:
        text = text.replace(char, replace_characters[char])
    return text


if __name__ == "__main__":
    # Preprocess each folder in parallel
    with multiprocessing.Pool(number_of_threads) as pool:
        pool.map(preprocess_folder, [f"original/{i}" for i in os.listdir("original") if os.path.isdir(f"original/{i}")])

    print("Preprocessing done.")
