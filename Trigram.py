import math

from NGram import NGram


class Trigram(NGram, object):

    mapping = {}

    def __init__(self):
        self.mapping = {}

    def counter(self, separated_line):
        for i in range(len(separated_line) - 2):

            prev_word = separated_line[i]
            current_word = separated_line[i + 1]
            next_word = separated_line[i + 2]

            if i + 3 < len(separated_line):
                second_next_word = separated_line[i + 3]
            else:
                second_next_word = "</s>"

            self.helper(prev_word, current_word, next_word, second_next_word)
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = current_word.replace(".", "")
            renewed_next_word = next_word.replace(".", "")

            if self.mapping.get(renewed_prev_word):
                dict_layer_1 = self.mapping.get(renewed_prev_word)
                if dict_layer_1.get(renewed_current_word):
                    dict_layer_2 = dict_layer_1.get(renewed_current_word)
                    if dict_layer_2.get(renewed_next_word):
                        dict_layer_2[renewed_next_word] += 1

                    else:
                        dict_layer_2[renewed_next_word] = 1

                else:
                    dict_layer_1[renewed_current_word] = {renewed_next_word: 1}

            else:
                self.mapping[renewed_prev_word] = {renewed_current_word: {renewed_next_word: 1}}

    def generator(self, final_list, second_prev_word='<s>', prev_word='<s>', repeat_count=1):
        temp_mapping = {}

        spec_map = self.mapping.get(second_prev_word).get(prev_word)
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
            self.generator(final_list, prev_word, new_word, repeat_count + 1)

    def prepareFirstAndLast(self, separated_line):
        lastIndex = len(separated_line) - 1
        self.mapping['<s>'] = {'<s>': {separated_line[0]: 1}}
        match = self.mapping.get('<s>')
        match[separated_line[0]] = {separated_line[1]: 1}
        self.mapping[separated_line[lastIndex]] = {'</s>': {'</s>': 1}}
        self.mapping[separated_line[lastIndex - 1]] = {separated_line[lastIndex]: {'</s>': 1}}

    def calculateProbabilityOfNextWord(self, total_trigram_count, current_word, prev_word='<s>', second_prev_word='<s>'):
        second_prev_map = self.mapping.get(second_prev_word)
        if second_prev_map is None:
            return 1 / total_trigram_count

        prev_map = second_prev_map.get(prev_word)
        if prev_map is None: #todo var burada
            return 1 / (total_trigram_count / 3)

        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word]

        else:
            total_count_prev_word += len(prev_map)

        return math.log2(float(total_count_junction/total_count_prev_word))

    def helper(self, prev_word, current_word, next_word, second_next_word):
        if '.' in current_word:
            cur_spec_map = self.mapping.get(current_word)
            prev_spec_map = self.mapping.get(prev_word)
            start_spec_map = self.mapping.get('<s>')

            if prev_spec_map is None:
                self.mapping[prev_word] = {current_word: {'</s>': 1}}

            else:
                temp_spec_map = prev_spec_map.get(current_word)
                if temp_spec_map is None:
                    prev_spec_map[current_word] = {'</s>': 1}

                elif temp_spec_map is not None and not temp_spec_map.get('</s>'):
                    temp_spec_map['</s>'] = 1

                else:
                    temp_spec_map['</s>'] += 1

            if cur_spec_map is None:
                self.mapping[current_word] = {next_word: {'</s>': 1}}

            else:
                temp_spec_map = cur_spec_map.get(next_word)

                if temp_spec_map is None:
                    cur_spec_map[next_word] = {'</s>': 1}

                elif temp_spec_map is not None and not temp_spec_map.get('</s>'):
                    temp_spec_map['</s>'] = 1

                else:
                    temp_spec_map['</s>'] += 1

            next_spec_map = start_spec_map.get(next_word)

            if next_spec_map is None:
                start_spec_map[next_word] = {second_next_word: 1}

            else:
                if next_spec_map.get(second_next_word):
                    next_spec_map[second_next_word] += 1
                else:
                    next_spec_map[second_next_word] = 1


