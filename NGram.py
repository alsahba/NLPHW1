import bisect, random


class NGram(object):

    def __init__(self):
        pass

    # This method takes three parameters, dice is the range number, breakpoints is the cumulative distribution list and
    # result is the words that matches with ranges.
    # Bisect used for matching ranges(breakpoints) to the words(result). With respect to some random dice number,
    # it looks to the breakpoints and get word with matched the range.
    def findWordWithRespectToRange(self, dice, breakpoints, result):
        i = bisect.bisect(breakpoints, dice)
        return result[i]

    # This method is used for calculation total number of the unigrams according to mapping that taken as parameter.
    # Then return the total number of mapping.
    def totalCountCalculator(self, mapping):
        summation = 0

        for values in mapping.items():
            summation += values[1]
        return summation

    # This method is counting frequency of the words in the unigram, bigram and trigram. Overridden in child classes.
    def counter(self, separated_line):
        pass

    # This method is for putting sentence definers(<s>, </s>) to the origin and end of the sentence.
    # Overridden in bigram and trigram.
    def prepareFirstAndLast(self, separated_line):
        pass

    # This method is used for generation takes unigram mapping and total size of the unigram mapping.
    # Calculates cumulative probability for all the words in the unigram mapping and
    # put them to the probability distribution list and put the specific word to the different word list.
    # Word list is the keys and distiribution list is range for that word list.
    # Two list sent to findWordWithRespectToRange method with random number and new word returned to the generator.
    # All unigram, bigram and trigram used this function without an overriding.
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

    # This method is used for getting total number of unique bigrams in the mapping that taken as parameter.
    def uniqueBigramCounter(self, mapping):
        unique_count = 0

        for second_mapping in mapping.items():
            unique_count += len(second_mapping)

        return unique_count

    # This method is used for getting total number of bigrams in the mapping that taken as parameter.
    def totalBigramCounter(self, mapping):
        summation = 0
        for first in mapping.items():
            for second in first[1].items():
                summation += second[1]
        return summation

    # This method is used for getting total number of unique trigrams in the mapping that taken as parameter.
    def uniqueTrigramCounter(self, mapping):
        unique_count = 0

        for first_layer_map in mapping.items():
            for second_layer_map in first_layer_map[1].items():
                unique_count += len(second_layer_map)

        return unique_count

    # This method is used for getting total number of trigrams in the mapping that taken as parameter.
    def totalTrigramCounter(self, mapping):
        summation = 0

        for first_layer_map in mapping.items():
            for second_layer_map in first_layer_map[1].items():
                for third_layer_map in second_layer_map[1].items():
                    summation += third_layer_map[1]

        return summation

    # This method is used for perplexity calculation of specific list that taken as parameter.
    # Method is overridden in unigram, bigram and trigram.
    def perplexityCalculator(self, separated_line):
        pass

