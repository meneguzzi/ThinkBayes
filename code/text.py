from os import path
import sys

from thinkbayes import Pmf

class TextStats(Pmf):

    def __init__(self, file):
        Pmf.__init__(self)
        word_list = []
        with open(file,"r") as f:
            lines = f.readlines()

            for line in lines:
                words = []
                for word in line.split():
                    word = word.lower()
                    word = word.strip('.\',!*&^%#$;:+()\"')
                    words.append(word)
                word_list = word_list + words

        for word in word_list:
            self.Incr(word,1)

        self.Normalize()

if __name__ == '__main__':
    tst = TextStats("./contract.cardinal.mfg.2004.02.13.txt")

    print(tst.Print())
