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

    def uniqueTrigramCounter(self):
        summation = 0

        for first_layer_map in self.mapping.items():
            for second_layer_map in first_layer_map[1].items():
                summation += len(second_layer_map)

        return summation

    def calculateProbabilityOfNextWord(self, total_trigram_count, current_word, prev_word='<s>', second_prev_word='<s>'):
        second_prev_map = self.mapping.get(second_prev_word)
        if second_prev_map is None:
            return 1 / (total_trigram_count + len(self.mapping))

        prev_map = second_prev_map.get(prev_word)
        if prev_map is None:
            return 1 / len(second_prev_map)

        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word]

        else:
            total_count_prev_word += len(prev_map)

        return math.log2(float(total_count_junction/total_count_prev_word))

    def helper(self, prev_word, current_word, next_word, second_next_word):
        if '.' in current_word:
            prev_word = prev_word.replace(".", "")
            current_word = current_word.replace(".", "")
            next_word = next_word.replace(".", "")
            second_next_word = second_next_word.replace(".", "")

            cur_spec_map = self.mapping.get(current_word)
            prev_spec_map = self.mapping.get(prev_word)
            start_spec_map = self.mapping.get('<s>')

            # s s next word
            if start_spec_map.get('<s>') is None:
                start_spec_map['<s>'] = {next_word: 1}

            else:
                if start_spec_map.get('<s>').get(next_word) is None:
                    start_spec_map.get('<s>')[next_word] = 1

                else:
                    start_spec_map.get('<s>')[next_word] += 1

            # s next_word second_next_word
            if start_spec_map.get(next_word) is None:
                start_spec_map[next_word] = {second_next_word: 1}

            else:
                if start_spec_map.get(next_word).get(second_next_word) is None:
                    start_spec_map.get(next_word)[second_next_word] = 1

                else:
                    start_spec_map.get('<s>')[next_word] += 1


            # prev cur /s
            if prev_spec_map is None:
                self.mapping[prev_word] = {current_word: {'</s>': 1}}

            else:
                if prev_spec_map.get(current_word) is None:
                    prev_spec_map[current_word] = {'</s>': 1}

                else:
                    if prev_spec_map.get(current_word).get('</s>') is None:
                        prev_spec_map.get(current_word)['</s>'] = 1

                    else:
                        prev_spec_map.get(current_word)['</s>'] += 1


            # cur /s /s
            if cur_spec_map is None:
                self.mapping[current_word] = {'</s>': {'</s>': 1}}

            else:
                if cur_spec_map.get('</s>') is None:
                    cur_spec_map['</s>'] = {'</s>': 1}

                else:
                    if cur_spec_map.get('</s>').get('</s>') is None:
                        cur_spec_map.get('</s>')['</s>'] = 1

                    else:
                        cur_spec_map.get('</s>')['</s>'] += 1

    def totalTrigramCalculator(self):
        summation = 0

        for first_layer_map in self.mapping.items():
            for second_layer_map in first_layer_map[1].items():
                summation += second_layer_map[1]

        return summation

    def perplexityCalculator(self, separated_line):
        total_trigram = self.totalTrigramCalculator()
        total_probability = 0

        total_probability += self.calculateProbabilityOfNextWord(
            total_trigram, separated_line[0])

        for i in range(len(separated_line) - 1):
            prev_word = separated_line[i]
            next_word = separated_line[i + 1]

            if '.' in prev_word:
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = next_word.replace(".", "")

                total_probability += self.calculateProbabilityOfNextWord(
                    total_trigram, renewed_current_word)

                total_probability += self.calculateProbabilityOfNextWord(
                    total_trigram, '</s>', renewed_prev_word)


            else:
                renewed_current_word = next_word.replace(".", "")

                total_probability += self.calculateProbabilityOfNextWord(
                    total_trigram, renewed_current_word, prev_word)

        return total_probability