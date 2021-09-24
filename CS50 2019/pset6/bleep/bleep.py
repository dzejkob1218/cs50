from cs50 import get_string
from sys import argv


def main():

    blacklist = {}
    blackfile = open("banned.txt","r")
    for line in blackfile:
        pair = line.strip('\n').split()
        blacklist[pair[0]] = pair[1]
    blackfile.close()

    print("Welcome to the censor machine. Enter your query")
    words = get_string("").split()

    for word in words:
        if word in blacklist:
            print(blacklist[word], end = " ")
        else:
            print(word, end = " ")
    print()

if __name__ == "__main__":
    main()
