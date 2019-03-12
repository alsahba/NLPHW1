import math

from NGram import NGram


class Bigram(NGram):

    mapping = {}

    def __init__(self, bi_map = {}):
        self.mapping = bi_map

    def counter(self, separated_line):
        for i in range(len(separated_line) - 1):
            if self.mapping.get(separated_line[i]):
                secondary_dictionary = self.mapping.get(separated_line[i])
                if secondary_dictionary.get(separated_line[i + 1]):
                    secondary_dictionary[separated_line[i + 1]] += 1

                else:
                    secondary_dictionary[separated_line[i + 1]] = 1
            else:
                self.mapping[separated_line[i]] = {separated_line[i + 1]: 1}

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
        self.mapping['<s>'] = {separated_line[0]: 1}
        self.mapping[separated_line[-1]] = {'</s>': 1}

    def calculateProbabilityOfNextWord(self, current_word, prev_word='<s>'):
        total_count_junction = 1
        total_count_prev_word = 0

        prev_map = self.mapping.get(prev_word)
        if prev_map is None:
            return 0.0000001
            prev_map = {}

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word]
            total_count_prev_word = self.totalCountCalculator(prev_map)

        else:
            total_count_prev_word += len(prev_map)

        return math.log(total_count_junction/total_count_prev_word)

