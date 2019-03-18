import math
from NGram import NGram


class Unigram(NGram, object):

    # Unigram mapping, its form like this {word1: repeat_count1, word2: repeat_count2...}
    mapping = {}

    # Constructor.
    def __init__(self):
        self.mapping = {}

    # This method is used for counting frequency in words that taken as word list parameter.
    # This method differenced other counters because it does not need a dotHandler.
    # Just put the words in dictionary with their repeated counts.
    def counter(self, separated_line):
        unique_words = set(separated_line)
        for word in unique_words:
            if "." in word:
                word = word.replace(".", "")

            if self.mapping.get(word):
                self.mapping[word] += separated_line.count(word)

            else:
                self.mapping[word] = separated_line.count(word)

    # This method takes a final_list and add generated words to it.
    # Since this is a recursive method we have to stop with respect to some event, repeat_count handled that mission.
    # Unigram dictionary and total word count in the dictionary sent to the generation helper
    # for getting new generated word with respect to mapping and total count.
    def generator(self, final_list, repeat_count=1):

        total_count = self.totalCountCalculator(self.mapping)
        final_list.append(self.generatorHelper(self.mapping, total_count))

        if repeat_count < 30:
            self.generator(final_list, repeat_count + 1)

    # This method took splitted text file as list and scans all words' probabilities in the list.
    # At the end calculates perplexity of the text file and return it.
    def perplexityCalculator(self, separated_line):
        total_probability = 0

        for word in separated_line:
            total_probability += math.log2(self.mapping.get(word) / self.totalCountCalculator(self.mapping))

        var = float(-1 / len(separated_line))
        perplexity = pow(2, var * total_probability)
        return perplexity