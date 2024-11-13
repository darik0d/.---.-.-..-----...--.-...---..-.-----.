"""
This module is responsible for generating the graphics of the statistics.
"""

import matplotlib.pyplot as plt
import os
import re

# Define the maximum number of bigrams per figure to avoid excessively large images
max_bigrams_per_graph = 50  # Adjust this number based on preference
only_top = True

# TODO: add multiprocessing to improve performance
def generate_graphs():
    # Take the preprocessed files and generate statistics
    for folder in os.listdir("corpus/preprocessed"):
        if os.path.isdir(f"corpus/preprocessed/{folder}"):
            generate_graphs_folder(folder)

import os
import re
import matplotlib.pyplot as plt
import math

def generate_graphs_folder(folder):
    # Count the frequency of each bigram
    if folder in []: # Add languages to skip
        return
    bigram_frequency = dict()
    # Create output folder
    os.makedirs(f"stats/{folder}", exist_ok=True)
    for filename in os.listdir(f"corpus/preprocessed/{folder}"):
        if filename.endswith(".txt"):
            with open(os.path.join(f"corpus/preprocessed/{folder}", filename), "r", encoding="utf8") as f:
                text = f.read()
            bigrams = re.findall(r".{1,2}", text)
            for bigram in bigrams:
                if bigram in bigram_frequency:
                    bigram_frequency[bigram] += 1
                else:
                    bigram_frequency[bigram] = 1

    # Sort the bigrams by frequency
    bigram_frequency = dict(sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True))

    # Split the bigrams into chunks
    bigram_items = list(bigram_frequency.items())
    num_chunks = math.ceil(len(bigram_items) / max_bigrams_per_graph)
    if only_top:
        num_chunks = 1
    for i in range(num_chunks):
        chunk = bigram_items[i * max_bigrams_per_graph:(i + 1) * max_bigrams_per_graph]
        chunk_bigrams = dict(chunk)

        # Generate the graph for each chunk
        plt.figure(figsize=(10, len(chunk_bigrams) * 0.5))  # Adjust figure height for each chunk

        # Create the horizontal bar chart
        bars = plt.barh(list(chunk_bigrams.keys()), list(chunk_bigrams.values()), height=0.8)

        # Adjust label size and position
        plt.ylabel("Bigram", fontsize=12)
        plt.xlabel("Frequency", fontsize=12)
        plt.title(f"Bigram frequency of {folder} (Part {i + 1})", fontsize=14)

        # Make sure labels are not cut off (!)
        plt.tight_layout()

        # Save the graph for the current chunk
        plt.savefig(f"stats/{folder}/bigram_frequency_{folder}_part_{i + 1}.png", dpi=700)
        plt.close()


if __name__ == "__main__":
    generate_graphs()
    print("Graphs generated.")