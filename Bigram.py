import math
from NGram import NGram


class Bigram(NGram, object):

    # Bigram mapping, its form like this {previous_word: {current_word: repeat_count}}
    mapping = {}

    # Constructor
    def __init__(self):
        self.mapping = {}

    # This method takes splitted text file as list and scans all words and put them into a nested dictionary structure.
    # Words with dots mean that end of the sentence, all doubles in the splitted text sent to the dotHandler method
    # for finding right place in the nested dictionary(mapping).
    def counter(self, separated_line):
        for i in range(len(separated_line) - 1):

            current_word = separated_line[i]
            next_word = separated_line[i + 1]
            self.dotHandler(current_word, next_word)

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

    # This method takes a final_list and add generated words to it. Also new word's generation made
    # with previous word that method takes them as parameters also.
    # Since this is a recursive method we have to stop with respect to some event, repeat_count handled that mission.
    # After getting inner dictionary with respect to previous word, we sent them to a generator helper function.
    def generator(self, final_list, current_word='<s>', repeat_count=1):
        temp_mapping = {}

        spec_map = self.mapping.get(current_word)

        total_count = self.totalCountCalculator(spec_map)

        for values in spec_map.items():
            temp_mapping[values[0]] = values[1]

        new_word = self.generatorHelper(temp_mapping, total_count)
        final_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(final_list, new_word, repeat_count + 1)

        if new_word == '</s>':
            final_list.pop(len(final_list) - 1)

    # This method takes splitted text file and add origin and end points to the nested dictionary structure.
    def prepareFirstAndLast(self, separated_line):
        self.mapping['<s>'] = {separated_line[0].replace(".", ""): 1}
        self.mapping[separated_line[-1].replace(".", "")] = {'</s>': 1}

    # This method takes total bigram count and doubles as parameters. Look for the own nested dictionary structure and
    # calculates conditional probability with respect to double's order.
    def calculateProbability(self, total_bigram_count, current_word, prev_word='<s>'):

        prev_map = self.mapping.get(prev_word)
        if prev_map is None:
            return math.log2(1 / (total_bigram_count + self.uniqueBigramCounter(self.mapping)))

        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map) + len(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word] + 1

        return math.log2(total_count_junction/total_count_prev_word)

    # This method takes previous and current words as parameters. And put them into the nested dictionary with
    # respect to end of the sentence, beginning of the sentence difference.
    # In this method dot maybe be with the previous or current word, these words separated to the dots and
    # put into the right places in the nested dictionary.
    def dotHandler(self, prev_word, current_word):
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

    # This method took splitted text file as list and scans all words' probabilities in the list.
    # At the end calculates perplexity of the text file and return it.
    def perplexityCalculator(self, separated_line):
        total_bigram = self.totalBigramCounter(self.mapping)
        total_probability = 0

        total_probability += self.calculateProbability(
            total_bigram, separated_line[0])

        for i in range(len(separated_line) - 1):
            prev_word = separated_line[i]
            current_word = separated_line[i + 1]

            if '.' in prev_word:
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = current_word.replace(".", "")

                total_probability += self.calculateProbability(total_bigram, renewed_current_word)

                total_probability += self.calculateProbability(total_bigram, '</s>', renewed_prev_word)

            elif '.' in current_word:
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = current_word.replace(".", "")

                total_probability += self.calculateProbability(total_bigram, renewed_current_word, renewed_prev_word)
                total_probability += self.calculateProbability(total_bigram, '</s>', renewed_current_word)

            else:
                renewed_current_word = current_word.replace(".", "")

                total_probability += self.calculateProbability(total_bigram, renewed_current_word, prev_word)

        var = float(-1 / len(separated_line))
        perplexity = pow(2, var * total_probability)
        return perplexity
