from __future__ import print_function

import wikipedia
import sys
import random
import re
import nltk.data
from datetime import datetime


def process_file(f):
    names = {}
    with open(f) as file:
        for line in file:
            l = line.strip().split('\t')
            if len(l) != 3:
                continue
            (k, v, y) = l
            names[k] = (v, y)
    return names


REGEX_IN_DATE = r".*in\s*(?:[^ ,]*?)?\s*(\d\d\d\d).*"


def process_page(id, birth_year):
    page = wikipedia.page(pageid=id)
    in_date_regex = re.compile(REGEX_IN_DATE, re.IGNORECASE)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    text_to_date = lambda x, y: datetime.strptime(x, y).date()

    birth_date = text_to_date(birth_year, '%Y-%m-%d+%H:%M')

    out = set()
    for line in tokenizer.tokenize(page.content, realign_boundaries=True):
        if '\n' in line:
            line = line.split('\n')
        else:
            line = [line]

        for l in line:
            match = in_date_regex.match(l)
            if match is not None:
                date = text_to_date(match.group(1), '%Y')
                age = (date - birth_date).days // 365
                out.add((age, l))
    return sorted(out, key=lambda achievement: achievement[0])

if __name__ == '__main__':
    for file in sys.argv[1:]:
        names = process_file(file)
        if len(names) > 10:
            sample = random.sample(names, 10)
        else:
            sample = names

        for name in sample:
            data = names[name]
            print ("Results of processing {} ({}, {})".format(name, *data))
            for achievement in process_page(*data):
                print ("\t", achievement[0],
                       "\t", achievement[1].encode('utf-8'))
