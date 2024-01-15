import sys
from fold_10 import *

'''
Use this script to evaluate Burp and test the Burp LSH with the 109FN
that mod security could not detect

To run the script use the following command:
    python evaluate_burp.py
'''


threshold_value = sys.argv[1]

malign_file_name = "./../error_logs/error_burp_without_modsecurity_parsed1.log"
remove_file_name = "./../remove_lines.txt"

malign_file_obj = open(malign_file_name, 'r', encoding='utf16')
remove_file_obj = open(remove_file_name, 'r', encoding='utf16')

malign_lines = malign_file_obj.readlines()
remove_lines = remove_file_obj.readlines()

malign_lines = get_list_of_lines(malign_lines)
remove_lines = get_list_of_lines(remove_lines)
malign_lines = list(set(malign_lines) - set(remove_lines))

test_dict = from_list_to_dict(remove_lines, True)
(lsh, dict_tokens) = create_LSH(malign_lines, threshold_value=float(
    threshold_value)/100, num_permut=256, shingle_size=3, is_wapiti=True)

metrics = classify_LSH(lsh, dict_tokens, remove_lines,
                       test_dict, float(threshold_value)/100)

scores(
    f'./CSVs/BURP_against_109FN_metrics_8020_{threshold_value}_.csv', [metrics])