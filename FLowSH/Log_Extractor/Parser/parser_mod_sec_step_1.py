import sys
'''
This scripts takes as input the apache log file and saves the output into a txt file.

To run the script use the following command:
    python parser_mod_sec_step_1.py <log_path> >> <new_log_path>

<log_path>: the path of the log. Example: ./log/log_1.txt
<new_log_path> the path of the result. Example: ./log/log_1_parsed.txt

Some files may be saved on utf-16 encoding.
'''


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def filter_lines_by_ids(ids, lines):
    """
        Filter the lines by the ids

        Parameters:
            ids(list[str]): the ids of the lines
            lines(list[str]): the lines
        
        Returns:
            list[str]: the filtered lines
    """
    filtered_lines = [line for line in lines if any(id in line for id in ids)]
    return filtered_lines


# Reads the log lines
filename = sys.argv[1]
file1 = open(filename, 'r', encoding='utf8')
Lines = file1.readlines()
line_103 = {"date": "", "request": "", "dumpio_line": "", "client": "",
            "server": "", "direction": "", "msg": ""}

line_list = []

modsecurity: list[str] = []
modsecurity_request_id = ""
for line in Lines:
    line = line.replace("[trace7]", "")
    line = line.replace("[dumpio]", "")
    line = line.replace(" mod_dumpio:", "")
    line = line.replace("[error]", "")

    # Searchs for the line 103 in the mod_dumpio
    if "[mod_dumpio.c(103)]" in line:

        start_bracket = find(line, "[")
        end_bracket = find(line, "]")
        date = line[start_bracket[0]:end_bracket[0]+1]
        request_id = line[start_bracket[1]:end_bracket[1]+1]
        dumpio_line = line[start_bracket[3]:end_bracket[2]+1]
        client = line[start_bracket[4]:end_bracket[3]+1]
        server = line[start_bracket[5]:end_bracket[4]+1]
        msg = line[end_bracket[4]+2:]
        direction = msg.lstrip().split(" ")[0]

        # Remove the dumpio_out or dumpio_in
        msg = msg[len(direction)+2:]
        # Remove the text between parenthesis
        msg = msg[find(msg, ")")[0]+3:]
        # Remove the end space and then remove the \r\n when it exists
        msg = msg[:-1]
        msg = msg.rstrip("\\r\\n ")

        # If date, cumpio, client and direction are the same, get msg together
        if line_103['date'] == date and \
                line_103['dumpio_line'] == dumpio_line and \
                line_103['client'] == client and \
                line_103['server'] == server and \
                line_103['direction'] == direction:
            line_103['msg'] = line_103['msg']+" "+msg
        # Else it is a new log. Print what exists and start again.
        else:
            # Prepares the msg and prints in the it existe content
            if line_103['msg'].startswith("G ET"):
                line_103["msg"] = line_103["msg"].replace(" ", "", 1)
            if line_103['msg'].startswith("P OST"):
                line_103["msg"] = line_103["msg"].replace(" ", "", 1)

            if line_103['date'] != "" and \
                    line_103['dumpio_line'] != "" and \
                    line_103['client'] != "" and \
                    line_103['server'] != "" and \
                    line_103['direction'] != "":
                line_list.append(line_103['date'] + " " + line_103['request'] + " " + line_103['client'] + " " +
                                 line_103['server'] + " " + line_103['direction'] + " " + line_103['msg'])
            
            line_103 = {"date": "", "dumpio_line": "", "client": "",
                        "server": "", "direction": "", "msg": ""}
            line_103['date'] = date
            line_103['dumpio_line'] = dumpio_line
            line_103['client'] = client
            line_103['direction'] = direction
            line_103['msg'] = msg
            line_103['server'] = server
            line_103['request'] = request_id

    # if apache2_util.c(273) in line then mod security detected attack
    if "[apache2_util.c(273)]" in line:
        modsecurity_start_bracket = find(line, "[")
        modsecurity_end_bracket = find(line, "]")
        modsecurity_request_id = line[modsecurity_start_bracket[1]:modsecurity_end_bracket[1]+1]
        if "[id \"920350\"]" not in line:
            modsecurity.append(modsecurity_request_id)

# remove duplicates
modsecurity = list(set(modsecurity))

# filter the lines
filtered_lines: list[str] = filter_lines_by_ids(modsecurity, line_list)


for line in filtered_lines:
    modsecurity_start_bracket = find(line, "[")
    modsecurity_end_bracket = find(line, "]")
    modsecurity_request_id = line[modsecurity_start_bracket[1]
        :modsecurity_end_bracket[1]+1]
    line = line.replace(modsecurity_request_id, "")
    print(line)