import math

from NGram import NGram


class Bigram(NGram, object):

    mapping = {}

    def __init__(self):
        self.mapping = {}

    def counter(self, separated_line):
        for i in range(len(separated_line) - 1):
            current_word = separated_line[i]

            if current_word.strip('.,:?;') == "publius":
                break

            next_word = separated_line[i + 1]
            self.helper(current_word, next_word)
            renewed_current_word =  current_word.replace(".","")

            if self.mapping.get(renewed_current_word):
                secondary_dictionary = self.mapping.get(renewed_current_word)
                if secondary_dictionary.get(next_word):
                    secondary_dictionary[next_word] += 1

                else:
                    secondary_dictionary[next_word] = 1
            else:
                self.mapping[renewed_current_word] = {next_word: 1}

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
        self.mapping['<s>'] = {separated_line[0].strip("."): 1}
        self.mapping[separated_line[-1].strip(".")] = {'</s>': 1}

    def calculateProbabilityOfNextWord(self, perplexity, totalBigramCount, current_word, prev_word='<s>'):
        total_count_junction = 1
        total_count_prev_word = 0

        prev_map = self.mapping.get(prev_word)
        if prev_map is None:
            return 1 / totalBigramCount

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word]
            total_count_prev_word = self.totalCountCalculator(prev_map)

        else:
            total_count_prev_word += len(prev_map)

        return math.log2(float(total_count_junction/total_count_prev_word))

    def helper(self, word, next_word):
        if '.' in word:
            prev_spec_map = self.mapping.get(word)
            if prev_spec_map is not None and prev_spec_map.get('</s>'):
                prev_spec_map['</s>'] += 1
            else:
                if prev_spec_map is None:
                    prev_spec_map = {}
                prev_spec_map['</s>'] = 1

            spec_map = self.mapping.get('<s>')

            if spec_map is not None and spec_map.get(next_word):
                spec_map[next_word] += 1
            else:
                if spec_map is None:
                    spec_map = {}
                spec_map[next_word] = 1

    def totalBigramCalculator(self):
        sum = 0
        for first in self.mapping.items():
            dictionary  = first[1]
            for second in dictionary.items():
                sum += second[1]
        return sum
