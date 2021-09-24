from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    list1 = []
    list2 = []
    sims = []

    list1 = a.split("\n")
    list2 = b.split("\n")

    for line in list2:
        if line in list1 and line not in sims:
            sims.append(line)

    return sims


def sentences(a, b):
    """Return sentences in both a and b"""


    list1 = []
    list2 = []
    sims = []

    list1 = sent_tokenize(a)
    list2 = sent_tokenize(b)

    for line in list2:
        if line in list1 and line not in sims:
            sims.append(line)

    return sims



def substrings(a, b, n):

    list1 = []
    list2 = []
    sims = []

    for i in range(len(a) - (n - 1)):
        list1.append(a[i:(i+n)])

    for i in range(len(b) - (n - 1)):
        list2.append(b[i:(i+n)])

    for line in list2:
        if line in list1 and line not in sims:
            sims.append(line)

    return sims