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

    def generate(self, probability_distribution_list, word_list):
        unmeaningful_list = []
        for i in range(30):
            dice = random.uniform(0, 1)
            unmeaningful_list.append(self.boundaries(dice, probability_distribution_list, word_list))

        return unmeaningful_list

    def generator(self):
        cumulative_probability = 0.0
        probability_distribution_list = []
        word_list = []

        total_word_count = self.totalCountCalculator(self.mapping)
        for values in self.mapping.items():
            word_probability = values[1] / total_word_count
            cumulative_probability = cumulative_probability + word_probability
            probability_distribution_list.append(cumulative_probability)
            word_list.append(values[0])

        return self.generate(probability_distribution_list, word_list)
