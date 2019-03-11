from NGram import NGram


class Bigram(NGram):

    mapping = {}

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

    def generator(self, last_list, prev_word, repeat_count=1):
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
        last_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(last_list, new_word, repeat_count + 1)

    def prepareFirstAndLast(self, separated_line):
        self.mapping['<s>'] = {separated_line[0]: 1}
        self.mapping[separated_line[-1]] = {'</s>': 1}