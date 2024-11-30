"""
This file contains code for encoding text to playfair format.
Run this file to convert preprocessed files to playfair format.
The preprocessed files will be saved in the preprocessed folder.
Working directory should be playfair/corpus
"""

import os
import re
import multiprocessing

# Calculate the number of folders in the preprocessed folder
number_of_threads = len([f for f in os.listdir("preprocessed") if os.path.isdir(f"preprocessed/{f}")])

# Encode each folder separately
def to_playfair_format_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            to_playfair_format_file(os.path.join(folder, filename))


def to_playfair_format_file(file):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
    text = to_playfair_format_text(text)
    # Write the encoded text to a new file in encoded folder/language_name
    encoded_folder = os.path.join("encoded", os.path.basename(os.path.dirname(file)))
    os.makedirs(encoded_folder, exist_ok=True)
    with open(os.path.join(encoded_folder, os.path.basename(file)), "w") as f:
        f.write(text)


def to_playfair_format_text(text):
    # Split the text into bigrams
    bigrams = re.findall(r".{1,2}", text)
    # Look you need to add x if the bigram has the same character twice
    # TODO: work further on this
    #bigrams = [bigram if bigram[0] != bigram[1] else bigram[0] + "x" for bigram in bigrams]



# # Does not work yet
# to_playfair_format_folder("preprocessed/de")
# to_playfair_format_folder("preprocessed/nl")
# to_playfair_format_folder("preprocessed/fr")
# to_playfair_format_folder("preprocessed/es")
# to_playfair_format_folder("preprocessed/it")
to_playfair_format_folder("preprocessed/en")