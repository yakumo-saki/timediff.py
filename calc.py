from consts import * 
from datetime import datetime

def calc_answer(list):
    answer = get_answer(list)

    for d in list:
        if (d["name"] == ANSWER_KEY):
            continue

        if (d["time"] > answer):
            d["answer"] = d["time"] - answer
        else:
            d["answer"] = answer - d["time"]

    return list


def get_answer(list):
    for d in list:
        if (d["name"] == ANSWER_KEY):
            return d["time"]

    raise AssertionError("answer not found in list")
