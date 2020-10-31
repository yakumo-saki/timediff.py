import sys
import time
from datetime import datetime
from dateutil.parser import parse

from calc import calc_answer
from consts import * 

def read_file():
    state = STATE_NAME
    list = []
    dict = {}
    for line in open('timediff.txt', 'r'):
        line = line.replace("\n", "")
        if (line == "\n" or line == ""): 
            continue  # skip empty line
        elif (line.startswith(":")):
            continue  # skip reactions
        elif (line == "1"):
            continue  # skip Add reaction

        if (line.startswith(ANSWER_PREFIX)):
            list.append({"name": ANSWER_KEY, "time": parse_answer(line)})
        elif (state == STATE_NAME):
            name = line.split(" ")[0]

            dict["name"] = name
            state = STATE_TIME
        elif (state == STATE_TIME):
            time = line.replace("（編集済み）", "")
            time = time.strip()

            dict["time"] = time
            state = STATE_NAME
            list.append(dict)
            dict = {}

    return list


def parse_data(list):
    result = []
    for d in list:
        name = parse_name(d["name"])
        time = parse_time(d["time"])
        result.append({"name": name, "time": time, "time_string": d["time"]})

    return result

def parse_name(name):
    # なまえ:icon2:  14時間前 の 時間部分を切る
    return name.split(" ")[0]

def parse_time(time):
    time_str = time.replace("（編集済み）", "")
    time_str = time.strip()

    time_str = time_str.replace("時間", ":").replace("分", ":").replace("秒", "")
    time_str = time_str.replace(" ", "")

    if (time_str.count(":") == 1):
        time_str = "00:" + time_str

    #dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    time = parse(time_str)

    return time


# 45分 50秒  ,  1時間 20分 50秒
def parse_answer(line):
    ans_str = line[len(ANSWER_PREFIX):]
    if (not "時間" in ans_str):
        ans_str = "0時間 " + ans_str

    if (not "秒" in ans_str):
        ans_str = ans_str + " 0秒"

    return ans_str


def main():
    dirty_list = read_file()
    list = parse_data(dirty_list)
    # print(list)

    ans_list = calc_answer(list)

    for ans in ans_list:
        if (ans["name"] == ANSWER_KEY):
            continue

        ans["answer"].total_seconds()
        print(f'{ans["name"]} {int(ans["answer"].total_seconds())}sec')

if __name__ == "__main__":
    main()