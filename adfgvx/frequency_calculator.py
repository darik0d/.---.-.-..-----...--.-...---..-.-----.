from math import ceil
import itertools
from copy import deepcopy
import csv
import threading
import time


"""
Calculates the frequency of ADFGVX digrams for every possible column transposition with keys of length 1-10.
Stores the frequency information in a CSV file.
"""

# read the ciphertext
file = open("opgave.txt", "r")
text = file.read()
file.close()

empty_frequencies = {"ADFGVX"[i//6]+"ADFGVX"[i%6]: 0  for i in range(36)}

def handle_orders(orders, unordered_columns, keylen, colheight, output):
    """
    Given a list of column orders, performs every order on the columns and computes the digram frequencies.
    The new frequencies are added to the output list.
    
    """
    for order in orders:
        columns = []
        for i in order:
            columns.append(unordered_columns[i])
        decoded = ""
        for i in range(colheight):
            for j in range(keylen):
                try:
                    newchar = columns[j][i]
                except IndexError:
                    newchar = ""
                decoded += newchar
            
        frequencies = deepcopy(empty_frequencies)
        for i in range(0, len(decoded), 2):
            digram = decoded[i:i+2]
            frequencies[digram] += 1
            
        output.append([order, frequencies])
            

output = []
threads = []

# start a timer
start = time.time()

# for every keylength
for keylen in range(2,11):
    print(f"key length: {keylen}")
    
    # generate all possible column orders
    arranged = range(keylen)
    orders = list(itertools.permutations(arranged))
    column_height = ceil(len(text)/keylen)
    
    threadcount = 8
    # divide the text up into columns
    unordered_columns = [text[i*column_height:(i+1)*column_height] for i in range(keylen)]    
    
    # divide the orders list up into intervals and start a thread for each interval
    for i in range(0, len(orders), ceil(len(orders)/threadcount)):
        interval_size = int(len(orders)/threadcount)
        if i+interval_size > len(orders):
            interval_size = len(orders)-i
        t = threading.Thread(target=handle_orders, args=(orders[i:i+interval_size], unordered_columns, keylen, column_height, output))
        threads.append(t)
        t.start()
        
# wait for all threads to finish
for t in threads:
    t.join()

# write all computed frequencies to a CSV file
file = open("frequencies.csv", "w", newline='')
writer = csv.writer(file)
for row in output:
    writer.writerow(row)
file.close()

# how long did it take?
print("seconds:", time.time()-start)