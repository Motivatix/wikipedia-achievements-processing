import wikipedia
import sys
import random
import re
import nltk.data


def process_file(f):
    names = {}
    with open(f) as file:
        for line in file:
            l = line.strip().split('\t')
            if len(l) != 2:
                continue
            (k, v) = l
            names[k] = v
    return names


REGEX_IN_DATE = r".*in\s*(?:[^ ,]*?)?\s*\d\d\d\d.*"


def process_page(id):
    page = wikipedia.page(pageid=id)
    in_date_regex = re.compile(REGEX_IN_DATE, re.IGNORECASE)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    out = set()
    for line in tokenizer.tokenize(page.content, realign_boundaries=True):
        if '\n' in line:
            line = line.split('\n')
        else:
            line = [line]

        for l in line:
            if in_date_regex.match(l):
                out.add(l)
    return out

if __name__ == '__main__':
    for file in sys.argv[1:]:
        names = process_file(file)
        if len(names) > 10:
            sample = random.sample(names, 10)
        else:
            sample = names

        for name in sample:
            pageid = names[name]
            print "Results of processing {} ({})".format(name, pageid)
            for achievement in process_page(pageid):
                print ("\t", achievement.encode('utf-8'))
