import sys
from csv import reader
import re
from datasketch import MinHash, MinHashLSH, MinHashLSHForest
import pickle

'''
This script takes the preprocessed log file, creates the LSH object and saves the tokens into a txt file. This object is then
saved in the directory ./db/*

To run the script use the following command:
    python create_minhashLSH.py <threshold> <log_path> <shingle_size> <num_perm>

<threshold> can be any value, in a percentage way. Example: {60, 70, 80, 90, 95}
<file_path> the path of the log. Example: ./log/log_1.txt
<shingle_size> the size of the shingle: {1,2,3,4,5}
<num_per> number of permutations done by the LSH: {128, 256}
'''


# gets the parameters from the terminal
file_name = sys.argv[2]
shingle_size = int(sys.argv[3])
_num_perm = int(sys.argv[4])
pickle_file = sys.argv[1]
threshold_value = int(pickle_file)/100

# reads the log lines
file1 = open(file_name, 'r')
lines = file1.readlines()
listOfLines = set()

for line in lines:
    line = line.rstrip()

    # Gets the payload from the dumpio_in
    if "dumpio_out," in line:
        continue
    if "dumpio_in," in line:
        line = (line.split("dumpio_in,")[1])
    line_s = line.split(" ")
    for s in line_s:
        if "/" in s:
            continue
        if s == "POST" or s == "GET" or s == "":
            continue

        # Adds the payload into the set
        listOfLines.add(s)

# Initialisation the LSH with the threshold and number of permutations requested
token_idx = 1
lsh = MinHashLSH(threshold=threshold_value, num_perm=_num_perm)

list_to_write = []

# Creation and insertion of the MinHash object into the LSH
for line in listOfLines:
    # If the size of the line is smaller than the shingle size requested -> continue
    if len(line) < shingle_size + 1:
        continue

    # Creates the shingles and saves them in a MinHash object
    list_of_shingles = set()
    for n in range(0, len(line)-shingle_size-1, 1):
        new_s = (line[n:n+shingle_size])
        list_of_shingles.add(new_s)

    exec("m%s = MinHash(num_perm=%d)" % (token_idx, _num_perm))

    list_to_write.append("m%s<>%s" % (token_idx, line))

    for d in list_of_shingles:
        exec("m%s.update(d.encode('utf8'))" % (token_idx))

    # Inserts the MinHash object into the LSH object with the key equal to its index
    exec('lsh.insert("m%s",m%s)' % (token_idx, token_idx))

    token_idx = token_idx+1

# Saves the LSH object into a pickle
file1 = r".\MinHashLSH_"+pickle_file
data = pickle.dumps(lsh)
with open(file1, 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

file2 = r".\tokens.txt"
handle = open(file2, 'w', encoding='utf8')
for item in list_to_write:
    handle.write(item+"\n")