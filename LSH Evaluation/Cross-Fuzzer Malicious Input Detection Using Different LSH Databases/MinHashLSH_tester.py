import sys
from csv import reader
import re
from datasketch import MinHash, MinHashLSH, MinHashLSHForest
import pickle
import random
import math

"""
Performs a 10 fold cross validation
Can perform with a ratio of 70/30, 80/20 or 90/10 train-test set

To run the script use the following command:
    python fold_10.py <threshold> 
"""


def get_list_of_lines(lines: list[str]) -> list[str]:
    """
        Returns the list of lines pretended

        Parameters:
            lines(list[str]): the list of lines raw
        
        Returns:
            list[str]: the list of lines pretended
    """
    list_of_lines = set()
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
            list_of_lines.add(s)
    print(len(list_of_lines))
    return list(list_of_lines)


def from_list_to_dict(list_of_lines: list[str], is_malign: bool) -> dict[str, bool]:
    """
        From the list and the boolean, return the dictionary with the values from 
        the list as keys and bool as values

        Parameters:
            list_of_lines(list[str]): the list of lines 
            is_malign(bool): the boolean
        
        Returns:
            dict[str, bool]: the dictionary with the values as keys and bool as value
    """
    result_dict = {}
    for line in list_of_lines:
        result_dict[line] = is_malign
    return result_dict


def scores(file_name: str, metrics_list: list[tuple[float, float, float, float]]) -> None:
    """
        Saves the scores of the LSH into a file

        Parameters:
            file_name(str): the name of the file where the scores are saved
            metrics_list(list[tuple[float, float, float, float]]): the tuple list with the scores
    """
    precision_sum = 0
    recall_sum = 0
    f1_score_sum = 0
    accuracy_sum = 0
    for metrics in metrics_list:
        (precision, recall, f1_score, accuracy) = metrics
        precision_sum += precision
        recall_sum += recall
        f1_score_sum += f1_score
        accuracy_sum += accuracy

    precision_mean = precision_sum / len(metrics_list)
    recall_mean = recall_sum / len(metrics_list)
    f1_score_mean = f1_score_sum / len(metrics_list)
    accuracy_mean = accuracy_sum / len(metrics_list)

    precision_deviation = 0
    recall_deviation = 0
    f1_score_deviation = 0
    accuracy_deviation = 0
    for metrics in metrics_list:
        (precision, recall, f1_score, accuracy) = metrics
        precision_deviation += (precision - precision_mean)**2
        recall_deviation += (recall - recall_mean)**2
        f1_score_deviation += (f1_score - f1_score_mean)**2
        accuracy_deviation += (accuracy - accuracy_mean)**2
    precision_deviation = math.sqrt(precision_deviation / len(metrics_list))
    recall_deviation = math.sqrt(recall_deviation / len(metrics_list))
    f1_score_deviation = math.sqrt(f1_score_deviation / len(metrics_list))
    accuracy_deviation = math.sqrt(accuracy_deviation / len(metrics_list))

    handle = open(file_name, 'w')
    handle.write('metric, mean, deviation\n')
    handle.write('precision, '+str(precision_mean) +
                 ", " + str(precision_deviation) + '\n')
    handle.write('recall, '+str(recall_mean) + ", " +
                 str(recall_deviation) + '\n')
    handle.write('f1_score, '+str(f1_score_mean) +
                 ", " + str(f1_score_deviation) + '\n')
    handle.write('accuracy, '+str(accuracy_mean) +
                 ", " + str(accuracy_deviation) + '\n')

def divide_chunks(l:list[str], n:int) -> list[list[str]]:
    """
        Divides the list of lines into chunks

        Parameters:
            l(list[str]): the list of lines
            n(int): the number of chunks
        
        Returns:
            list[list[str]]: the n lists of list of lines
    """
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


def create_LSH(train_chunk: list[str], threshold_value: int, num_permut: float, shingle_size: int) -> tuple[MinHashLSH, dict[str]]:
    """
        Creates the LSH

        Parameters:
            train_chunk(list[str]): the train set to build the LSH
            threshold_value(int): the threshold value requested
            num_permut(float): the number of permutation done
            shingle_size(int): the size of the shingle
        
        Returns:
            tuple[MinHashLSH, list[str]]: the LSH object and the dict of tokens
    """
    token_idx = 1
    lsh = MinHashLSH(threshold=threshold_value, num_perm=num_permut)

    dict_tokens = {}
    for line in train_chunk:
        if len(line) < shingle_size + 1:
            continue

        list_of_shingles = set()
        for n in range(0, len(line)-shingle_size-1, 1):
            new_s = (line[n:n+shingle_size])
            list_of_shingles.add(new_s)

        exec("m%s = MinHash(num_perm=%d)" % (token_idx, num_permut))
        dict_tokens["m%s" % token_idx] = ("%s" % line)
        

        for d in list_of_shingles:
            exec("m%s.update(d.encode('utf8'))" % (token_idx))

        exec('lsh.insert("m%s",m%s)' % (token_idx, token_idx))

        token_idx = token_idx+1
    return (lsh, dict_tokens)


def create_MinHash(line: str, shingle_size: int, num_permut: int) -> MinHash:
    """
        Creates the MinHash of the line received.

        Parameters:
            line (str): The line to be minhashed
            shingle_size (int): the shingle size
            _num_perm (int): the number of permutations

        Returns:
            MinHash: the MinHash object
    """
    if len(line) < shingle_size + 1:
        n = MinHash(num_perm=num_permut)
        n.update(line.encode('utf8'))
        return n

    list_of_shingles = set()  # Fazer um set logo

    for n in range(0, len(line)-shingle_size-1, 1):
        new_s = (line[n:n+shingle_size])
        list_of_shingles.add(new_s)

    n = MinHash(num_perm=num_permut)

    for d in list_of_shingles:
        n.update(d.encode('utf8'))
    return n


def print_results(result: list[str], tokens_dict: dict[str, str]) -> list[str]:
    '''
        Print the results of que query and returns the list of the tokens corresponding to the result keys

        Parameters:
            result(list[str]): the result
            tokens_dict(dict[str,str]): the token dictionay

        Returns:
            list[str]: the inputs similar to the input queried
    '''
    if result == []:
        return []
    if result != []:
        list_tokens = {}
        for key in result:
            dict_token = tokens_dict[key]  
            list_tokens[key] = dict_token
        return list_tokens


def print_best_token(list_tokens: dict[str, str], n1: MinHash, threshold: float = 0.6) -> tuple[bool, bool]:
    """
        Knowing the tokens similar to the one queried, get the best one and determines if the best one has
        worst jaccard similarity than the threshold requested

        Parameters:
            list_tokens(dict[str,str]): the list of tokens similar to the token queried
            n1(MinHash): the minhash object of the token queried
            threshold(float): the threshold requested

    """
    jaccard_list = {}
    for key in list_tokens:
        token = list_tokens[key]
        token = token.strip()
        m = create_MinHash(token, 3, 256)
        jaccard_list[key] = n1.jaccard(m)

    key_max_value = max(jaccard_list, key=jaccard_list.get)
    return (jaccard_list[key_max_value] == 1, threshold > jaccard_list[key_max_value])


def classify_LSH(lsh: MinHashLSH, dict_tokens: dict[str], test_chunk: list[str], test_dict: dict[str, bool], threshold_value: float) -> tuple[float, float, float, float]:
    """
        Calculates the precision, recall, f1_score and accuracy of the LSH

        Parameters:
            lsh(MinHashLSH): the trained LSH object
            dict_tokens(dict[str]): the dictionary with all tokens in the LSH
            test_chunk(list[str, bool]): the dictionary with the tokens as keys and the malign or benign bool as value
            threshold_value(float): the threshold value requested

        Returns:
            tuple[float, float, float, float]: a tuple with the result for that test chunk set
    
    """
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for test_line in test_chunk:
        test_line = test_line.strip()
        minhash = create_MinHash(test_line, shingle_size=3, num_permut=256)
        result = lsh.query(minhash)
        list_tokens = print_results(result, dict_tokens)

        if result != [] and test_dict[test_line]:
            # TP += 1
            (is_one, is_worst) = print_best_token(list_tokens, minhash, threshold=threshold_value)
            if (not is_one) and (not is_worst):
                TP += 1
            else:
                FN += 1
        elif result != [] and (not test_dict[test_line]):
            FP += 1
        elif result == [] and test_dict[test_line]:
            FN += 1
        elif result == [] and (not test_dict[test_line]):
            TN += 1

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = (2 * precision * recall) / (precision + recall)
    accuracy = (TP + TN) / (TP + FN + TN + FP)
    return (precision, recall, f1_score, accuracy)


def main():
    """
        Main function:
            1: Gets the log with the tokens and divides it 10 chunks
            2: For each chunk:
                2.1: Creates a train set with 9 chunks and a test set with 1 chunk (if 90/10)
                2.2: Creates the LSH with the train set
                2.3: Calculates the metrics for the test set and saves in a list
            3. Saves the list into a file of choice
    """
    threshold_value = (sys.argv[1])
    print('threshold', threshold_value)
    file_name = "./../error_logs/w4af_parsed1.txt"

    file1 = open(file_name, 'r', encoding='utf16')
    lines = file1.readlines()
    (lsh, dict_tokens) = create_LSH(get_list_of_lines(lines), threshold_value=float(threshold_value),
                                        num_permut=256, shingle_size=3)
    
    file_name_test = "./../error_logs/error8_2_parsed1.txt"
    file2 = open(file_name_test, 'r', encoding='utf16')
    lines = file2.readlines()
    test_dict = from_list_to_dict(get_list_of_lines(lines), True).copy()
    (_, recall, _, _) = classify_LSH(lsh, dict_tokens, get_list_of_lines(lines), test_dict, float(threshold_value))

    scores(
        f'./CSVs/ZA_vs_WA_{threshold_value}.csv', recall)

main()