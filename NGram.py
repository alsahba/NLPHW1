import bisect
import random

class NGram():

    def boundaries(self, num, breakpoints, result):
        i = bisect.bisect(breakpoints, num)
        if i > len(result):
            return '</s>'
        return result[i]

    def totalCountCalculator(self, mapping):
        summation = 0

        for values in mapping.items():
            summation += values[1]
        return summation

    def counter(self, separated_line):
        pass

    def prepareFirstAndLast(self, separated_line):
        pass

    def generatorHelper(self, mapping, total_count):
        cumulative_probability = 0.0
        probability_distribution_list = []
        word_list = []

        for values in mapping.items():
            word_probability = values[1] / total_count
            cumulative_probability = cumulative_probability + word_probability
            probability_distribution_list.append(cumulative_probability)
            word_list.append(values[0])

        dice = random.uniform(0, 1)
        return self.boundaries(dice, probability_distribution_list, word_list)
