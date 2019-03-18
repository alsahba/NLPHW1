import math
from NGram import NGram


class Trigram(NGram, object):

    # Trigram mapping, its form like this {second_previous_word: {previous_word: {current_word: repeat_count}}}
    mapping = {}

    # Constructor.
    def __init__(self):
        self.mapping = {}

    # This method takes splitted text file as list and scans all words and put them into a nested dictionary structure.
    # Words with dots mean that end of the sentence, all triplets in the splitted text sent to the dotHandler method
    # for finding right place in the nested dictionary(mapping).
    def counter(self, separated_line):
        for i in range(len(separated_line) - 2):
            prev_word = separated_line[i]
            current_word = separated_line[i + 1]
            next_word = separated_line[i + 2]

            self.dotHandler(prev_word, current_word, next_word)

    # This method takes a final_list and add generated words to it. Also new word's generation made
    # with previous words that method takes them as parameters also.
    # Since this is a recursive method we have to stop with respect to some event, repeat_count handled that mission.
    # After getting inner dictionary with respect to previous words, we sent them to a generator helper function.
    def generator(self, final_list, prev_word='<s>', second_prev_word='<s>', repeat_count=1):
        temp_mapping = {}
        #todo burada hata atti bir kere tam incelemek lazim
        spec_map = self.mapping.get(second_prev_word).get(prev_word)

        if spec_map is None:
            spec_map = {}

        # Total repeat count of the known words. This helps for deciding denominator while calculating probability.
        total_count = self.totalCountCalculator(spec_map)

        for values in spec_map.items():
            temp_mapping[values[0]] = values[1]

        new_word = self.generatorHelper(temp_mapping, total_count)
        final_list.append(new_word)

        if repeat_count < 30 and new_word != '</s>':
            self.generator(final_list, new_word, prev_word, repeat_count + 1)

        if new_word == '</s>':
            final_list.pop(len(final_list) - 1)

    # This method takes splitted text file and add origin and end points to the nested dictionary structure.
    def prepareFirstAndLast(self, separated_line):
        lastIndex = len(separated_line) - 1
        self.mapping['<s>'] = {'<s>': {separated_line[0]: 1}}
        match = self.mapping.get('<s>')
        match[separated_line[0]] = {separated_line[1]: 1}
        self.mapping[separated_line[lastIndex]] = {'</s>': {'</s>': 1}}
        self.mapping[separated_line[lastIndex - 1]] = {separated_line[lastIndex]: {'</s>': 1}}

    # This method takes total trigram count and triplet as parameters. Look for the own nested dictionary structure and
    # calculates conditional probability with respect to triplet's order.
    def calculateProbability(self, total_trigram_count, current_word, prev_word='<s>', second_prev_word='<s>'):
        second_prev_map = self.mapping.get(second_prev_word)

        # Second previous word has not seen in the first layer of the nested dictionary which means that
        # never encountered before in the train part.
        # We have to add one to seen counter and add one to all of the unique trigrams.
        if second_prev_map is None:
            return math.log2(float(1 / (total_trigram_count + self.uniqueTrigramCounter(self.mapping))))

        prev_map = second_prev_map.get(prev_word)

        # Previous word has not seen yet after the second previous word.
        # We have to add one to seen counter and add one to all unique bigrams.
        if prev_map is None:
            return math.log2(float(1 / (self.totalBigramCounter(second_prev_map) + self.uniqueBigramCounter(second_prev_map))))

        # All good, the double has seen before but we have to add one to all unique unigrams. Because maybe
        # the current word has not seen yet after the previous words.
        total_count_junction = 1
        total_count_prev_word = self.totalCountCalculator(prev_map) + len(prev_map)

        if prev_map.get(current_word):
            total_count_junction = prev_map[current_word] + 1

        return math.log2(float(total_count_junction/total_count_prev_word))

    # This method takes previous, current and next word as parameters. And put them into the nested dictionary with
    # respect to end of the sentence, beginning of the sentence difference.
    # In this method dot maybe be with the previous, current or next word, these words separated to the dots and
    # put into the right places in the nested dictionary.
    def dotHandler(self, prev_word, current_word, next_word):
        renewed_prev_word = prev_word.replace(".", "")
        renewed_current_word = current_word.replace(".", "")
        renewed_next_word = next_word.replace(".", "")

        if '.' in prev_word:
            # previous_word -> </s> -> </s>
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

            # <s> -> current_word -> next_word
            if self.mapping.get('<s>').get(renewed_current_word):
                if self.mapping.get('<s>').get(renewed_current_word).get(renewed_next_word):
                    self.mapping.get('<s>').get(renewed_current_word)[renewed_next_word] += 1
                else:
                    self.mapping.get('<s>').get(renewed_current_word)[renewed_next_word] = 1
            else:
                self.mapping.get('<s>')[renewed_current_word] = {renewed_next_word: 1}

        elif '.' in current_word:
            # previous_word -> current_word -> </s>
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

            # <s> -> <s> -> next_word
            if self.mapping.get('<s>').get('<s>'):
                if self.mapping.get('<s>').get('<s>').get(renewed_next_word):
                    self.mapping.get('<s>').get('<s>')[renewed_next_word] += 1
                else:
                    self.mapping.get('<s>').get('<s>')[renewed_next_word] = 1
            else:
                self.mapping.get('<s>')['<s>'] = {renewed_next_word: 1}

        else:
            # previous_word -> current_word -> next_word
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

    # This method took splitted text file as list and scans all words' probabilities in the list.
    # At the end calculates perplexity of the text file and return it.
    def perplexityCalculator(self, separated_line):
        total_trigram = self.totalTrigramCounter(self.mapping)
        total_probability = 0

        # first_word <- <s> <- <s>
        total_probability += self.calculateProbability(
            total_trigram, separated_line[0])

        # second_word <- first_word <- <s>
        total_probability += self.calculateProbability(
            total_trigram, separated_line[1], separated_line[0])

        # calculation of probabilities of words in text file.
        for i in range(2, len(separated_line)):
            second_prev_word = separated_line[i - 2]
            prev_word = separated_line[i - 1]
            current_word = separated_line[i]

            renewed_second_prev_word = second_prev_word.replace(".", "")
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = current_word.replace(".", "")

            if '.' in current_word:

                # current_word <- prev_word <- second_prev_word
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word, renewed_prev_word, renewed_second_prev_word)

                # </s> <- current_word <- prev_word
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', renewed_current_word, renewed_prev_word)

                # </s> <- </s> <- current_word
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_current_word)

            elif '.' in prev_word:

                # </s> <- prev_word <- second_prev_word
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', renewed_prev_word, renewed_second_prev_word)

                # current_word <- <s> <- <s>
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word)

                # </s> <- </s> <- prev_word
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_prev_word)

            elif '.' in second_prev_word:

                # </s> <- </s> <- second_prev_word
                total_probability += self.calculateProbability(
                    total_trigram, '</s>', '</s>', renewed_second_prev_word)

                # prev_word <- <s> <- <s>
                total_probability += self.calculateProbability(
                    total_trigram, renewed_prev_word)

                # current_word <- prev_word <- <s>
                total_probability += self.calculateProbability(
                    total_trigram, renewed_current_word, renewed_prev_word)

            else:
                # current_word <- prev_word <- second_prev_word
                total_probability += self.calculateProbability(
                    total_trigram, current_word, prev_word, second_prev_word)

        # perplexity calculation part
        var = float(-1 / len(separated_line))
        perplexity = pow(2, var * total_probability)
        return perplexity
