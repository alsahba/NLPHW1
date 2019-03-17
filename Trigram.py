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

            self.dotHandler(prev_word, current_word, next_word)

    def generator(self, final_list, prev_word='<s>', second_prev_word='<s>', repeat_count=1):
        temp_mapping = {}
        #todo burada hata atti bir kere tam incelemek lazim
        spec_map = self.mapping.get(second_prev_word).get(prev_word)

        if spec_map is None:
            spec_map = {}

        total_count = self.totalCountCalculator(spec_map)

        for values in spec_map.items():
            temp_mapping[values[0]] = values[1]

        new_word = self.generatorHelper(temp_mapping, total_count)
        final_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(final_list, new_word, prev_word, repeat_count + 1)

        if new_word == '</s>':
            final_list.pop(len(final_list) - 1)

    def prepareFirstAndLast(self, separated_line):
        lastIndex = len(separated_line) - 1
        self.mapping['<s>'] = {'<s>': {separated_line[0]: 1}}
        match = self.mapping.get('<s>')
        match[separated_line[0]] = {separated_line[1]: 1}
        self.mapping[separated_line[lastIndex]] = {'</s>': {'</s>': 1}}
        self.mapping[separated_line[lastIndex - 1]] = {separated_line[lastIndex]: {'</s>': 1}}

    def calculateProbability(self, total_trigram_count, current_word, prev_word='<s>', second_prev_word='<s>'):
        second_prev_map = self.mapping.get(second_prev_word)
        if second_prev_map is None:
            return math.log2(float(1 / (total_trigram_count + self.uniqueTrigramCounter(self.mapping))))

        prev_map = second_prev_map.get(prev_word)
        if prev_map is None:
            return math.log2(float(1 / (self.totalBigramCounter(second_prev_map) + self.uniqueBigramCounter(second_prev_map))))

        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map) + len(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word] + 1

        return math.log2(float(total_count_junction/total_count_prev_word))

    def dotHandler(self, prev_word, current_word, next_word):
        if '.' in prev_word:
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = current_word.replace(".", "")
            renewed_next_word = next_word.replace(".", "")

            #prev /s /s
            if self.mapping.get(renewed_prev_word):
                if self.mapping.get(renewed_prev_word).get('</s>'):
                    if self.mapping.get(renewed_prev_word).get('</s>').get('</s>'):
                        self.mapping.get(renewed_prev_word).get('</s>')['</s>'] += 1
                    else:
                        self.mapping.get(renewed_prev_word).get('</s>')['</s>'] = 1
                else:
                    self.mapping.get(renewed_prev_word)['</s>'] = {'</s>': 1}
            else:
                self.mapping[renewed_prev_word] = {'</s>': {'</s>': 1}}

            #s cur next
            if self.mapping.get('<s>').get(renewed_current_word):
                if self.mapping.get('<s>').get(renewed_current_word).get(renewed_next_word):
                    self.mapping.get('<s>').get(renewed_current_word)[renewed_next_word] += 1
                else:
                    self.mapping.get('<s>').get(renewed_current_word)[renewed_next_word] = 1
            else:
                self.mapping.get('<s>')[renewed_current_word] = {renewed_next_word: 1}

        elif '.' in current_word:
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = current_word.replace(".", "")
            renewed_next_word = next_word.replace(".", "")

            # prev cur /s
            if self.mapping.get(renewed_prev_word):
                if self.mapping.get(renewed_prev_word).get(renewed_current_word):
                    if self.mapping.get(renewed_prev_word).get(renewed_current_word).get('</s>'):
                        self.mapping.get(renewed_prev_word).get(renewed_current_word)['</s>'] += 1
                    else:
                        self.mapping.get(renewed_prev_word).get(renewed_current_word)['</s>'] = 1
                else:
                    self.mapping.get(renewed_prev_word)[renewed_current_word] = {'</s>': 1}
            else:
                self.mapping[renewed_prev_word] = {renewed_current_word: {'</s>': 1}}

            # s s next
            if self.mapping.get('<s>').get('<s>'):
                if self.mapping.get('<s>').get('<s>').get(renewed_next_word):
                    self.mapping.get('<s>').get('<s>')[renewed_next_word] += 1
                else:
                    self.mapping.get('<s>').get('<s>')[renewed_next_word] = 1
            else:
                self.mapping.get('<s>')['<s>'] = {renewed_next_word: 1}

        else:
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = current_word.replace(".", "")
            renewed_next_word = next_word.replace(".", "")

            #prev cur next
            if self.mapping.get(renewed_prev_word):
                if self.mapping.get(renewed_prev_word).get(renewed_current_word):
                    if self.mapping.get(renewed_prev_word).get(renewed_current_word).get(renewed_next_word):
                        self.mapping.get(renewed_prev_word).get(renewed_current_word)[renewed_next_word] += 1
                    else:
                        self.mapping.get(renewed_prev_word).get(renewed_current_word)[renewed_next_word] = 1
                else:
                    self.mapping.get(renewed_prev_word)[renewed_current_word] = {renewed_next_word: 1}
            else:
                self.mapping[renewed_prev_word] = {renewed_current_word: {renewed_next_word: 1}}

    def perplexityCalculator(self, separated_line):
        total_trigram = self.totalTrigramCounter(self.mapping)
        total_probability = 0

        total_probability += self.calculateProbability(
            total_trigram, separated_line[0])

        total_probability += self.calculateProbability(
            total_trigram, separated_line[1], separated_line[0])

        for i in range(2, len(separated_line)):
            second_prev_word = separated_line[i - 2]
            prev_word = separated_line[i - 1]
            current_word = separated_line[i]

            if '.' in current_word:
                renewed_second_prev_word = second_prev_word.replace(".", "")
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = current_word.replace(".", "")

                #cur prev sec_prev
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word, renewed_prev_word, renewed_second_prev_word)

                #/s cur prev
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', renewed_current_word, renewed_prev_word)

                #/s /s cur
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_current_word)

            elif '.' in prev_word:
                renewed_second_prev_word = second_prev_word.replace(".", "")
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = current_word.replace(".", "")

                #/s prev sec_prev
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', renewed_prev_word, renewed_second_prev_word)

                #cur s s
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word)

                #/s /s prev
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_prev_word)

            elif '.' in second_prev_word:
                renewed_second_prev_word = second_prev_word.replace(".", "")
                renewed_prev_word = prev_word.replace(".", "")
                renewed_current_word = current_word.replace(".", "")

                # /s /s sec_prev
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_second_prev_word)

                #prev s s
                total_probability += self.calculateProbability(
                    total_trigram, renewed_prev_word)

                #cur prev s
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word, renewed_prev_word)

            else:
                # cur prev sec_prev
                total_probability += self.calculateProbability(
                    total_trigram, current_word, prev_word, second_prev_word)

        var = float(-1 / len(separated_line))
        perplexity = pow(2, var * total_probability)
        return perplexity
