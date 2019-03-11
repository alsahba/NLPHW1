from NGram import NGram
import random


class Unigram(NGram):

    mapping = {}

    def counter(self, separated_line):
        unique_words = set(separated_line)
        for word in unique_words:
            if self.mapping.get(word):
                self.mapping[word] += separated_line.count(word)

            else:
                self.mapping[word] = separated_line.count(word)

    def generator(self, final_list, repeat_count = 1):

        total_count = self.totalCountCalculator(self.mapping)
        final_list.append(self.generatorHelper(self.mapping, total_count))

        if repeat_count < 30:
            self.generator(final_list, repeat_count + 1)


