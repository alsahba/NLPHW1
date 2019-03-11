from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram


class Author:

    unigram = Unigram()
    bigram = Bigram()
    trigram = Trigram()

    def counterCaller(self, separated_line):
        self.unigram.counter(separated_line)
        self.bigram.counter(separated_line)
        self.trigram.counter(separated_line)

    def generatorCaller(self, uni_list, bi_list, tri_list):
        self.unigram.generator(uni_list)
        self.bigram.generator(bi_list, '<s>')
        self.trigram.generator(tri_list, '<s>', '<s>')