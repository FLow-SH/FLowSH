import fold_10
import random

'''
This script is to get 25% of each fuzzer tokens to get samples to create bening inputs

To run the script use the following command:
    python get_samples_to_benign.py
'''

def main():
    file_names = ["./../error_logs/w4af_parsed1.txt",
                  "./../error_logs/23-01-23-parsed1.txt", "./../error_logs/error8_2_parsed1.txt", "./../error_logs/error_burp_bwapp_without_modsecurity_parsed1.log"]
    final_list = []
    for file_name in file_names:
        if file_name == ('./../error_logs/w4af_parsed1.txt' or "./../error_logs/error_burp_bwapp_sem_modsecurity_parsed1.log"):
            file = open(file_name, 'r', encoding='utf16')
        else:
            file = open(file_name, 'r')

        lines = file.readlines()
        list_of_lines = fold_10.get_list_of_lines(lines)
        list_to_insert = list(random.sample(list_of_lines, int(
            len(list_of_lines) * 0.25)))
        final_list += list_to_insert

        random.shuffle(final_list)
    file = "./benign_to_transform.txt"
    print(len(final_list))
    handle = open(file, 'w', encoding='utf8')
    for item in final_list:
        handle.write(item+"\n")


main()