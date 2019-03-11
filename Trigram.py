import random


from NGram import NGram


class Trigram(NGram):

    mapping = {}

    def counter(self, separated_line):
        for i in range(len(separated_line)):
            if i + 2 < len(separated_line) and separated_line[i] != '' and separated_line != '\"':
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

    def generator(self, last_list, second_prev_word, prev_word, repeat_count):
        cumulative_probability = 0.0
        probability_distribution_list = []
        word_list = []
        temp_list = {}

        spec_map = self.mapping.get(second_prev_word).get(prev_word)
        if spec_map is None:
            spec_map = {}

        total_count = self.totalCountCalculator(spec_map)
        v_count = 0

        for values in self.mapping.items():
            if spec_map.get(values[0]):
                temp_list[values[0]] = spec_map.get(values[0]) + 1
            else:
                temp_list[values[0]] = 1
                v_count += 1

        total_count += v_count

        for values in temp_list.items():
            word_probability = values[1] / total_count
            cumulative_probability = cumulative_probability + word_probability
            probability_distribution_list.append(cumulative_probability)
            word_list.append(values[0])

        dice = random.uniform(0, 1)
        new_word = self.boundaries(dice, probability_distribution_list, word_list)
        last_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(last_list, prev_word, new_word, repeat_count + 1)