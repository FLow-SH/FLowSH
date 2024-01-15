
'''
Script that compares the 2 logs, used in the mod security evaluation to collect 
the 109 attacks not detected by the ModSecurity

To run the script use the following command:
    python compare_logs.py >> <file_path>
'''


def list_to_dict(list: list[str]) -> dict[str, str]:
    dict_result: dict[str, str] = {}
    for line in list:
        key = line.split('<>')[0]
        value = line.split('<>')[1]
        dict_result[key] = value
    return dict_result


filename_1 = "./tokens_burp_without_mod_security.txt"
filename_2 = "./tokens_burp_mod_security.txt"

file_1 = open(filename_1, 'r')
file_2 = open(filename_2, 'r')

line_list_1 = file_1.readlines()
line_list_2 = file_2.readlines()

line_dict_1 = list_to_dict(line_list_1)
line_dict_2 = list_to_dict(line_list_2)

different_values_dict = line_dict_1.copy()
for key_1 in line_dict_1:
    for key_2 in line_dict_2:
        if line_dict_1[key_1] == line_dict_2[key_2]:
            different_values_dict.pop(key_1)

for key in different_values_dict:
    print(different_values_dict[key].strip())