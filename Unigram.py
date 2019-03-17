import math
from NGram import NGram


class Unigram(NGram, object):

    mapping = {}

    def __init__(self):
        self.mapping = {}

    def counter(self, separated_line):
        unique_words = set(separated_line)
        for word in unique_words:
            if "." in word:
                word = word.replace(".", "")

            if self.mapping.get(word):
                self.mapping[word] += separated_line.count(word)

            else:
                self.mapping[word] = separated_line.count(word)

    def generator(self, final_list, repeat_count = 1):

        total_count = self.totalCountCalculator(self.mapping)
        final_list.append(self.generatorHelper(self.mapping, total_count))

        if repeat_count < 30:
            self.generator(final_list, repeat_count + 1)

    def perplexityCalculator(self, separated_line):
        perplexity = 0
        total_probability = 0

        for word in separated_line:
            total_probability += math.log2(self.mapping.get(word) / self.totalCountCalculator(self.mapping))

        var = float(-1 / len(separated_line))
        perplexity = pow(2, var * total_probability)
        return perplexity