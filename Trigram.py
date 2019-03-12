from NGram import NGram


class Trigram(NGram):

    mapping = {}

    def __init__(self, tri_map={}):
        self.mapping = tri_map

    def counter(self, separated_line):
        for i in range(len(separated_line) - 2):
            if self.mapping.get(separated_line[i]):
                dict_layer_1 = self.mapping.get(separated_line[i])
                if dict_layer_1.get(separated_line[i + 1]):
                    dict_layer_2 = dict_layer_1.get(separated_line[i + 1])
                    if dict_layer_2.get(separated_line[i + 2]):
                        dict_layer_2[separated_line[i + 2]] += 1

                    else:
                        dict_layer_2[separated_line[i + 2]] = 1

                else:
                    dict_layer_1[separated_line[i + 1]] = {separated_line[i + 2]: 1}

            else:
                self.mapping[separated_line[i]] = {separated_line[i + 1]: {separated_line[i + 2]: 1}}

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