from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram


class Author(object):

    __name = ""
    __unigram = Unigram()
    __bigram = Bigram()
    __trigram = Trigram()

    # Constructor.
    def __init__(self, name):
        self.__name = name
        self.__unigram = Unigram()
        self.__bigram = Bigram()
        self.__trigram = Trigram()

    # Getters.
    def getUnigram(self):
        return self.__unigram

    def getBigram(self):
        return self.__bigram

    def getTrigram(self):
        return self.__trigram

    def getName(self):
        return self.__name

    # Caller method, it is used for counting frequency in the unigram, bigram and trigram.
    def counterCaller(self, separated_line):
        self.__unigram.counter(separated_line)
        self.__bigram.counter(separated_line)
        self.__trigram.counter(separated_line)

    # Caller method, it is used for generating new text with respect to unigram, bigram and trigram.
    def generatorCaller(self, uni_list, bi_list, tri_list):
        self.__unigram.generator(uni_list)
        self.__bigram.generator(bi_list)
        self.__trigram.generator(tri_list)
