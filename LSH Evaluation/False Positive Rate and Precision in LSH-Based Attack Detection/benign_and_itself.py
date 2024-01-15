from fold_10 import *
import sys


def remove_evrth_after_metacharacter(list_of_lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in list_of_lines:
        if '%' in line:
            result.append(line.split('%')[0])
        else:
            result.append(line)
    return result


def remove_metacharacters(list_of_lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in list_of_lines:
        i = 0
        line = line
        while i < len(line):
            if line[i] == '%':
                line = line[:i] + line[i+3:]
            elif line[i] == "'":
                line = line[:i] + line[i+1:]
            i += 1
        result.append(line)
    return result


def remove_commands(list_of_lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in list_of_lines:
        line = line.replace('and', '')
        line = line.replace('AND', '')
        line = line.replace('or', '')
        line = line.replace('OR', '')
        line = line.replace('select', '')
        line = line.replace('SELECT', '')
        line = line.replace('union', '')
        line = line.replace('UNION', '')
        result.append(line)
    return result


def create_dict(file_path: str) -> dict[str, str]:
    '''
        Com o file path cria um dicionário com a
        key e o token correspondente

        Parameters:
        file_path (str): caminho para o ficheiro

        Returns:
        O dicionário relativo ao ficheiro
    '''
    infile = open(file_path, encoding='utf_8')
    lines = infile.readlines()
    infile.close()
    return_dict = {}
    for line in lines:
        key_and_token = line.split('<>')
        return_dict[key_and_token[0]] = key_and_token[1].strip()
    return return_dict


def from_dict_to_list(my_dict: dict[str, str]) -> list[str]:
    return list(my_dict.values()).copy()


def get_chunks(list_of_lines: list[str]) -> list[list[str]]:
    """
        Divides the list of lines into 10 diferent chunks
        
        Parameters:
            list_of_lines(list[str]): list of lines
        
        Returns:
            list[list[str]]: list of list of lines
    """
    random.shuffle(list_of_lines)  # shuffle the list
    ogLen = len(list_of_lines)  # original lenght
    fold_list_len = int(ogLen / 10)  # lenght of a single fold

    return [list_of_lines[x:x+fold_list_len]
            for x in range(0, len(list_of_lines), fold_list_len)]


def main():
    benign_test_name = sys.argv[1]
    threshold_value = sys.argv[2]

    file_name = "./../error_logs/23-01-23-parsed1.txt"

    file1 = open(file_name, 'r')
    lines = file1.readlines()
    chunks = get_chunks(get_list_of_lines(lines))
    if len(chunks) > 10:
        chunks = chunks[:-1]

    i = 0
    for chunk in chunks:
        print(f'chunk size in index {i}', len(chunk))
        i += 1
    benign_file_name = "./benign_to_transform.txt"
    benign_file_obj = open(benign_file_name, 'r')
    benign_lines = benign_file_obj.readlines()

    if benign_test_name == "after_metacaracter":
       benign_lines = remove_evrth_after_metacharacter(
           get_list_of_lines(benign_lines))

    elif benign_test_name == "meta_and_commands":
      benign_lines = remove_commands(
           remove_metacharacters(get_list_of_lines(benign_lines)))
    else:
      benign_lines = remove_metacharacters(get_list_of_lines(benign_lines))

    benign_chunks = get_chunks(benign_lines)
    metrics = []
    i = 0
    while i < len(chunks) - 1:
        test_chunk = chunks[i].copy()
        test_chunk += chunks[i+1].copy()
        benign_test_chunk = benign_chunks[i].copy() + benign_chunks[i+1].copy()

        if (len(benign_test_chunk) > len(test_dict)):
           benign_test_chunk = benign_test_chunk[:len(test_chunk)].copy()

        test_dict.update(from_list_to_dict(benign_test_chunk, False).copy())
        test_chunk += benign_test_chunk.copy()
        test_chunk = list(set(test_chunk))

        test_dict = from_list_to_dict(test_chunk, True).copy()
        test_indexes = (i, i + 1)
        print('test_chunk_indexes: ', test_indexes)
        print('test_chunk len ', len(test_chunk))
        j = 0
        train_chunk = []
        while j < len(chunks):
            if not (j in test_indexes):
                train_chunk += chunks[j].copy()
            j += 1
        (lsh, dict_tokens) = create_LSH(train_chunk, threshold_value=float(threshold_value),
                                        num_permut=256, shingle_size=3, is_wapiti=True)
        train_chunk = []
        (precision, recall, f1_score, accuracy) = classify_LSH(
            lsh, dict_tokens, test_chunk, test_dict, float(threshold_value))
        metrics.append((precision, recall, f1_score, accuracy))
        i += 1

    scores(
        f'./CSVs/ZAP_metrics_8020_{benign_test_name}_{threshold_value}_.csv', metrics)


main()