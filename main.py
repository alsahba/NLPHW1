import glob, os
import bisect
import random


def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


def preCountWords(separated_line, mapping_list):
    uniqWords = set(separated_line)
    for word in uniqWords:
        countWords(mapping_list, word, separated_line.count(word))


def newBigramCounter(separated_line, mapping):
    for i in range(len(separated_line)):
        if i + 1 < len(separated_line):
            if mapping.get(separated_line[i]):
                dict = mapping.get(separated_line[i])
                if dict.get(separated_line[i + 1]):
                    dict[separated_line[i + 1]] += 1

                else:
                    dict[separated_line[i + 1]] = 1
            else:
                mapping[separated_line[i]] = {separated_line[i+1]:1}


def newTrigramCounter(separated_line, mapping):
    for i in range(len(separated_line)):
        if i + 2 < len(separated_line):
            if mapping.get(separated_line[i]):
                dict_layer_1 = mapping.get(separated_line[i])
                if dict_layer_1.get(separated_line[i + 1]):
                    dict_layer_2 = dict_layer_1.get(separated_line[i + 1])
                    if dict_layer_2.get(separated_line[i + 2]):
                        dict_layer_2[separated_line[i+2]] += 1

                    else:
                        dict_layer_2[separated_line[i + 2]] = 1

                else:
                    dict_layer_1[separated_line[i + 1]] = {separated_line[i+2]: 1}

            else:
                mapping[separated_line[i]] = {separated_line[i+1]: {separated_line[i+2]: 1}}


def mappingDistributor(text_file, unigram_mapping_list, bigram_mapping_list, trigram_mapping_list):
    for line in text_file.readlines():
        split_line = line.split(' ')
        split_line = list(map(lambda x: x.lower().strip(',.;:?()`'), split_line))
        preCountWords(split_line, unigram_mapping_list)
        newBigramCounter(split_line, bigram_mapping_list)
        newTrigramCounter(split_line, trigram_mapping_list)


def countWords(mapping_list, key, count):
    if mapping_list.get(key):
        mapping_list[key] += count

    else:
        mapping_list[key] = count


def boundaries(num, breakpoints, result):
    i = bisect.bisect(breakpoints, num)
    if i > len(result):
        return '</s>'
    return result[i]


def generate(probability_distribution_list, word_list):
    unmeaningful_list = []
    for i in range(30):
        dice = random.uniform(0, 1)
        unmeaningful_list.append(boundaries(dice, probability_distribution_list, word_list))

    return unmeaningful_list


def probabilityCalculator(word_dict, total_word_count):
    return word_dict.get('count') / total_word_count


def totalCountCalculator(mapping):
    sum = 0
    for values in mapping.items():
        sum += values[1]
    return sum


def unigramGenerator(mapping):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []

    total_word_count = totalCountCalculator(mapping)
    for values in mapping.items():
        word_probability = values[1] / total_word_count
        cumulative_probability = cumulative_probability + word_probability
        probability_distribution_list.append(cumulative_probability)
        word_list.append(values[0])

    return generate(probability_distribution_list, word_list)


def bigramGenerator(mapping, last_list, prev_word, repeat_count):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []
    temp_list = {}

    spec_map = mapping.get(prev_word)
    total_count = totalCountCalculator(spec_map)
    v_count = 0

    for values in mapping.items():
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
    new_word = boundaries(dice, probability_distribution_list, word_list)
    last_list.append(new_word)

    if repeat_count < 30 and new_word != '</s>':
        bigramGenerator(mapping, last_list, new_word, repeat_count + 1)

def trigramGenerator(mapping_list, last_list, second_prev_word, prev_word, repeat_count):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []
    found_ones = []
    temp_list = []

    for dict in mapping_list:
        if dict.get('second_prev_key') == second_prev_word and dict.get('prev_key') == prev_word:
            found_ones.append(dict)
        elif not dict.get('key') in temp_list:
            temp_list.append(str(dict.get('key')))

    total_count = len(found_ones) + len(temp_list)
    temp_list.clear()

    for dict in mapping_list:
        dict_count = 0
        if dict in found_ones:
            dict_count += int(dict.get('count')) + 1

        else:
            dict_count += 1

        word_probability = dict_count / total_count
        if not dict.get('key') in word_list:
            cumulative_probability = cumulative_probability + word_probability
            probability_distribution_list.append(cumulative_probability)
            word_list.append(dict.get('key'))

    dice = random.uniform(0, 1)
    new_word = boundaries(dice, probability_distribution_list, word_list)
    last_list.append(new_word)

    probability_distribution_list.clear()
    word_list.clear()
    found_ones.clear()
    temp_list.clear()

    # print(repeat_count)
    if repeat_count <= 30 and new_word != '</s>':
        trigramGenerator(mapping_list, last_list, prev_word, new_word, repeat_count + 1)


file_list = []
openAllFiles(file_list)

hamilton_unigram_word_mapping = {}
madison_unigram_word_mapping = {}
hamilton_bigram_word_mapping = {}
madison_bigram_word_mapping = {}
hamilton_trigram_word_mapping = {}
madison_trigram_word_mapping = {}

count = len(file_list)
for file in file_list:
    author = file.readline()

    if author.strip() == "HAMILTON":
        mappingDistributor(file, hamilton_unigram_word_mapping,
                           hamilton_bigram_word_mapping, hamilton_trigram_word_mapping)

    else:
        mappingDistributor(file, madison_unigram_word_mapping,
                           madison_bigram_word_mapping, madison_trigram_word_mapping)

    count -= 1
    print(count)

sorted(hamilton_unigram_word_mapping)

liste = unigramGenerator(hamilton_unigram_word_mapping)
print(*liste)

bi_list = []
tri_list = []

# i = totalWordCountCalculator(hamilton_unigram_word_mapping)

# dicts = {'jack': 4098, 'sape': 4139}
#
# for dicts in dicts.items():
#     print(dicts[1])

#unigramGenerator(hamilton_unigram_word_mapping, i)
bigramGenerator(hamilton_bigram_word_mapping, bi_list, 'to', 1)
print(*bi_list)
print(len(bi_list))
# trigramGenerator(hamilton_trigram_word_mapping, tri_list, '<s>', '<s>', 1)

# print(hamilton_unigram_word_mapping)

