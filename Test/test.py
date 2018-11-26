
import random


HIRAGANA_LIST = list(u"あいうえおかきくけこさしすせそたちつてと"\
                  u"なにぬねのはひふへほまみむめもやゆよ"\
                  u"らりるれろわをん")


def generateWW(length):
    watchword = ""
    for i in range(length):
        n = len(HIRAGANA_LIST)
        watchword = watchword + HIRAGANA_LIST[random.randint(0, n-1)]

    return watchword

if __name__ == "__main__":
    #l = list(NAMES_CHARS)

    s = generateWW(10)
    print(s)