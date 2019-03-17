import bisect, random


class NGram(object):

    def __init__(self):
        pass

    def findWordWithRespectToRange(self, num, breakpoints, result):
        i = bisect.bisect(breakpoints, num)
        if i >= len(result):
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
            cumulative_probability += word_probability
            probability_distribution_list.append(cumulative_probability)
            word_list.append(values[0])

        dice = random.uniform(0, 1)
        return self.findWordWithRespectToRange(dice, probability_distribution_list, word_list)

    def uniqueBigramCounter(self, mapping):
        unique_count = 0

        for second_mapping in mapping.items():
            unique_count += len(second_mapping)

        return unique_count

    def totalBigramCounter(self, mapping):
        summation = 0
        for first in mapping.items():
            for second in first[1].items():
                summation += second[1]
        return summation

    def uniqueTrigramCounter(self, mapping):
        unique_count = 0

        for first_layer_map in mapping.items():
            for second_layer_map in first_layer_map[1].items():
                unique_count += len(second_layer_map)

        return unique_count

    def totalTrigramCounter(self, mapping):
        summation = 0

        for first_layer_map in mapping.items():
            for second_layer_map in first_layer_map[1].items():
                for third_layer_map in second_layer_map[1].items():
                    summation += third_layer_map[1]

        return summation

    def perplexityCalculator(self, separated_line):
        pass

