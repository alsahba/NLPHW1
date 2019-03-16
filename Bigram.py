import math

from NGram import NGram


class Bigram(NGram, object):

    mapping = {}

    def __init__(self):
        self.mapping = {}

    def counter(self, separated_line):
        for i in range(len(separated_line) - 1):

            current_word = separated_line[i]
            next_word = separated_line[i + 1]
            self.helper(current_word, next_word)

            renewed_current_word = current_word.replace(".", "")
            renewed_next_word = next_word.replace(".", "")

            if self.mapping.get(renewed_current_word):
                secondary_dictionary = self.mapping.get(renewed_current_word)
                if secondary_dictionary.get(renewed_next_word):
                    secondary_dictionary[renewed_next_word] += 1

                else:
                    secondary_dictionary[renewed_next_word] = 1
            else:
                self.mapping[renewed_current_word] = {renewed_next_word: 1}

    def generator(self, final_list, prev_word='<s>', repeat_count=1):
        temp_mapping = {}

        spec_map = self.mapping.get(prev_word)
        if spec_map is None:
            spec_map = {}

        total_count = self.totalCountCalculator(spec_map)
        v_count = 0

        for values in self.mapping.items():
            if spec_map.get(values[0]):
                temp_mapping[values[0]] = spec_map.get(values[0]) + 1
            else:
                temp_mapping[values[0]] = 1
                v_count += 1

        total_count += v_count

        new_word = self.generatorHelper(temp_mapping, total_count)
        final_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(final_list, new_word, repeat_count + 1)

    def prepareFirstAndLast(self, separated_line):
        self.mapping['<s>'] = {separated_line[0].replace(".", ""): 1}
        self.mapping[separated_line[-1].replace(".", "")] = {'</s>': 1}

    def uniqueBigramCounter(self):
        unique_count = 0

        for second_mapping in self.mapping.items():
            unique_count += len(second_mapping)

        return unique_count

    def calculateProbabilityOfNextWord(self, total_bigram_count, current_word, prev_word='<s>'):

        prev_map = self.mapping.get(prev_word)
        if prev_map is None:
            return math.log2(1 / (total_bigram_count + self.uniqueBigramCounter()))

        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map) + len(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word] + 1

        return math.log2(total_count_junction/total_count_prev_word)

    def helper(self, prev_word, current_word):
        if '.' in prev_word:
            prev_word = prev_word.replace(".", "")
            prev_spec_map = self.mapping.get(prev_word)
            current_word = current_word.replace(".", "")

            if prev_spec_map is None:
                self.mapping[prev_word] = {'</s>': 1}

            else:
                if prev_spec_map.get('</s>'):
                    prev_spec_map['</s>'] += 1

                else:
                    prev_spec_map['</s>'] = 1

            spec_map = self.mapping.get('<s>')

            if spec_map.get(current_word):
                spec_map[current_word] += 1

            else:
                spec_map[current_word] = 1

    def totalBigramCalculator(self):
        sum = 0
        for first in self.mapping.items():
            dictionary  = first[1]
            for second in dictionary.items():
                sum += second[1]
        return sum

    def perplexityCalculator(self, separated_line):
        total_bigram = self.totalBigramCalculator()
        total_probability = 0

        total_probability += self.calculateProbabilityOfNextWord(
            total_bigram, separated_line[0])

        for i in range(len(separated_line) - 1):
            prev_word = separated_line[i]
            next_word = separated_line[i + 1]

            if '.' in prev_word:
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = next_word.replace(".", "")

                total_probability += self.calculateProbabilityOfNextWord(
                    total_bigram, renewed_current_word)

                total_probability += self.calculateProbabilityOfNextWord(
                    total_bigram, '</s>', renewed_prev_word)


            else:
                renewed_current_word = next_word.replace(".", "")

                total_probability += self.calculateProbabilityOfNextWord(
                    total_bigram, renewed_current_word, prev_word)

        return total_probability
