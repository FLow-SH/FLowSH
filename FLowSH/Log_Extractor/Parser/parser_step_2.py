#!/usr/bin/python3
import sys
import json
import io
'''
This scripts takes as input the apache log file processed in parse_log_1.py and saves the output into a txt file.

It is needed to update the log date in line 55. Example: line = line.replace("[Sat May 22 ", "2021/05/22T").
Have attention to the file enconding. Depending on the encoding line 46 may differ. Example: file1 = open(filename, 'r', encoding='utf16')


To run the script use the following command:
    python parser_step_2.py <log_path> >> <new_log_path>

<log_path>: the path of the log. Example: ./log/log_1_parsed.txt
<new_log_path> the path of the result. Example: ./log/log_1_final.txt

'''

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def out_flow(flow: list[list[str]]):
    if len(flow) > 0:
        if flow[0][6].startswith("GET"):
            print(",".join(flow[0]).rstrip("\n"))
        if flow[0][6].startswith("POST"):
            print(",".join(flow[0]).rstrip("\n"))
            print(",".join(flow[-1]).rstrip("\n"))
        if flow[0][5] == "dumpio_out":
            sip = flow[0][2]
            dip = flow[0][1]
            sport = flow[0][4]
            dport = flow[0][3]
            flow[0][1] = sip
            flow[0][2] = dip
            flow[0][3] = sport
            flow[0][4] = dport
            flow[0][6] = (flow[0][6].split(r"\r\n")[0])
            print(",".join(flow[0]).rstrip("\n"))
            

# Reads the log lines
filename = sys.argv[1]
file1 = open(filename, 'r', encoding='utf16')
Lines = file1.readlines()


# Parses the log
state = True
flow = []
for line in Lines:

    line = line.replace("[Sun May 28 ", "2023/05/28T")
    line = line.replace("] [client ", "##")
    line = line.replace("] [Local ", "##")
    line = line.replace("] dumpio_in ", "##dumpio_in##")
    line = line.replace("] dumpio_out ", "##dumpio_out##")

    arr = line.split("##")
    arr[0] = arr[0].replace(" 2023", "")

    arr.insert(3, arr[1].split(":")[1])
    arr.insert(4, arr[2].split(":")[1])
    arr[1] = arr[1].split(":")[0]
    arr[2] = arr[2].split(":")[0]

    if arr[6].startswith("GET"):
        out_flow(flow)
        flow = []
        flow.append(arr)
        state = False

    if arr[6].startswith("POST"):
        out_flow(flow)
        flow = []
        flow.append(arr)
        state = False

    if arr[5] == 'dumpio_out':
        if not state:
            out_flow(flow)
            flow = []
            flow.append(arr)
        state = True

    flow.append(arr)