import csv

"""
Iterates over every order of columns and prints the orders that are most likely to be correct
according to the highest digram frequency and the number of zero frequencies.
"""

file = open("frequencies.csv", "r")
reader = csv.reader(file)

# The minimal threshold for the maximum frequency of a digram to be considered
# experimentally determined
max_frequency_threshold = 360

for row in reader:
    frequencies = eval(row[1]) # row consists of order and frequencies
    current_max_freq = max(frequencies.values())
    if current_max_freq > max_frequency_threshold:
        zerocount = 0
        for key in frequencies:
            if frequencies[key] == 0:
                zerocount += 1
        print(f"For order {row[0]}, found {zerocount} zero frequencies with highest relative frequency {current_max_freq/sum(frequencies.values())}.")
        
file.close()