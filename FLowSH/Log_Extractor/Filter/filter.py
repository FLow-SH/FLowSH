from datetime import datetime

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def filter(log_file:str, date_time:datetime, threshold:float) -> list[str]:
    '''
        Given the log_file, the date_time and the threshold, returns the list
        of lines with the datetime requested with a certain threshold.

        Parameters:
        log_file(str): the path of the log file
        date_time(datetime): the datetime requested
        threshold(float): the threshold accepted 
    '''
    file = open(log_file, 'r', encoding='utf8')
    line_list = file.readlines()

    return_list = []

    for line in line_list:
        line = line.replace("[trace7]", "")
        line = line.replace("[dumpio]", "")
        line = line.replace(" mod_dumpio:", "")

        # Searchs for the line 103 in the mod_dumpio
        if "[mod_dumpio.c(103)]" in line:
            start_bracket = find(line, "[")
            end_bracket = find(line, "]")

            date = line[start_bracket[0]:end_bracket[0]+1]
            date = date[1:-1] 

            line_datetime = datetime.strptime(date, "%a %b %d %H%M%S.%f %Y")
            if abs((line_datetime - date_time).seconds) < threshold:
                return_list.append(line)
    return return_list


            