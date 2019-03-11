import glob, os


from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram
from Author import Author


def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


# def prepareFirstAndLastBigram(separated_line, bigram):
#     bigram.mapping['<s>'] = {separated_line[0]: 1}
#     bigram.mapping[separated_line[-1]] = {'</s>': 1}
#
#
# def preapareFirstAndLastTrigrams(separated_line, trigram):
#     lastIndex = len(separated_line) - 1
#     trigram.mapping['<s>'] = {'<s>': {separated_line[0]: 1}}
#     match = trigram.mapping.get('<s>')
#     match[separated_line[0]] = {separated_line[1]: 1}
#     trigram.mapping[separated_line[lastIndex]] = {'</s>': {'</s>': 1}}
#     trigram.mapping[separated_line[lastIndex - 1]] = {separated_line[lastIndex]: {'</s>': 1}}
#

# def unigramCounter(separated_line, mapping):
#     uniqWords = set(separated_line)
#     for word in uniqWords:
#         if mapping.get(word):
#             mapping[word] += separated_line.count(word)
#
#         else:
#             mapping[word] = separated_line.count(word)
#
#
# def bigramCounter(separated_line, mapping):
#     for i in range(len(separated_line)):
#         if i + 1 < len(separated_line):
#             if mapping.get(separated_line[i]):
#                 dict = mapping.get(separated_line[i])
#                 if dict.get(separated_line[i + 1]):
#                     dict[separated_line[i + 1]] += 1
#
#                 else:
#                     dict[separated_line[i + 1]] = 1
#             else:
#                 mapping[separated_line[i]] = {separated_line[i+1]:1}
#
#
# def trigramCounter(separated_line, mapping):
#     for i in range(len(separated_line)):
#         if i + 2 < len(separated_line) and separated_line[i] != '' and separated_line != '\"':
#             if mapping.get(separated_line[i]):
#                 dict_layer_1 = mapping.get(separated_line[i])
#                 if dict_layer_1.get(separated_line[i + 1]):
#                     dict_layer_2 = dict_layer_1.get(separated_line[i + 1])
#                     if dict_layer_2.get(separated_line[i + 2]):
#                         dict_layer_2[separated_line[i+2]] += 1
#
#                     else:
#                         dict_layer_2[separated_line[i + 2]] = 1
#
#                 else:
#                     dict_layer_1[separated_line[i + 1]] = {separated_line[i+2]: 1}
#
#             else:
#                 mapping[separated_line[i]] = {separated_line[i+1]: {separated_line[i+2]: 1}}
#

def frequencyCounter(text_file, author):
    for line in text_file.readlines():
        separated_line = line.split(' ')
        separated_line = list(map(lambda x: x.lower().strip(',.;:?()`\"\'\n[]'), separated_line))

        author.trigram.prepareFirstAndLast(separated_line)
        author.bigram.prepareFirstAndLast(separated_line)

        author.unigram.counter(separated_line)
        author.bigram.counter(separated_line)
        author.trigram.counter(separated_line)
# def boundaries(num, breakpoints, result):
#     i = bisect.bisect(breakpoints, num)
#     if i > len(result):
#         return '</s>'
#     return result[i]
#
#
# def generate(probability_distribution_list, word_list):
#     unmeaningful_list = []
#     for i in range(30):
#         dice = random.uniform(0, 1)
#         unmeaningful_list.append(boundaries(dice, probability_distribution_list, word_list))
#
#     return unmeaningful_list
#
#
# def totalCountCalculator(mapping):
#     sum = 0
#
#     for values in mapping.items():
#         sum += values[1]
#     return sum
#
#
# def unigramGenerator(mapping):
#     cumulative_probability = 0.0
#     probability_distribution_list = []
#     word_list = []
#
#     total_word_count = totalCountCalculator(mapping)
#     for values in mapping.items():
#         word_probability = values[1] / total_word_count
#         cumulative_probability = cumulative_probability + word_probability
#         probability_distribution_list.append(cumulative_probability)
#         word_list.append(values[0])
#
#     return generate(probability_distribution_list, word_list)
#
#
# def bigramGenerator(mapping, last_list, prev_word, repeat_count):
#     cumulative_probability = 0.0
#     probability_distribution_list = []
#     word_list = []
#     temp_list = {}
#
#     spec_map = mapping.get(prev_word)
#     if spec_map is None:
#         spec_map = {}
#
#     total_count = totalCountCalculator(spec_map)
#     v_count = 0
#
#     for values in mapping.items():
#         if spec_map.get(values[0]):
#             temp_list[values[0]] = spec_map.get(values[0]) + 1
#         else:
#             temp_list[values[0]] = 1
#             v_count += 1
#
#     total_count += v_count
#
#     for values in temp_list.items():
#         word_probability = values[1] / total_count
#         cumulative_probability = cumulative_probability + word_probability
#         probability_distribution_list.append(cumulative_probability)
#         word_list.append(values[0])
#
#     dice = random.uniform(0, 1)
#     new_word = boundaries(dice, probability_distribution_list, word_list)
#     last_list.append(new_word)
#
#     if repeat_count < 30 and new_word != '</s>':
#         bigramGenerator(mapping, last_list, new_word, repeat_count + 1)
#
#
# def trigramGenerator(mapping, last_list, second_prev_word, prev_word, repeat_count):
#     cumulative_probability = 0.0
#     probability_distribution_list = []
#     word_list = []
#     temp_list = {}
#
#     spec_map = mapping.get(second_prev_word).get(prev_word)
#     if spec_map is None:
#         spec_map = {}
#
#     total_count = totalCountCalculator(spec_map)
#     v_count = 0
#
#     for values in mapping.items():
#         if spec_map.get(values[0]):
#             temp_list[values[0]] = spec_map.get(values[0]) + 1
#         else:
#             temp_list[values[0]] = 1
#             v_count += 1
#
#     total_count += v_count
#
#     for values in temp_list.items():
#         word_probability = values[1] / total_count
#         cumulative_probability = cumulative_probability + word_probability
#         probability_distribution_list.append(cumulative_probability)
#         word_list.append(values[0])
#
#     dice = random.uniform(0, 1)
#     new_word = boundaries(dice, probability_distribution_list, word_list)
#     last_list.append(new_word)
#
#     if repeat_count < 30 and new_word != '</s>':
#         trigramGenerator(mapping, last_list, prev_word, new_word, repeat_count + 1)
file_list = []
openAllFiles(file_list)

hamilton = Author()
madison = Author()

for file in file_list:
    author = file.readline()

    if author.strip() == "HAMILTON":
        frequencyCounter(file, hamilton)

    else:
        frequencyCounter(file, madison)


liste = hamilton.unigram.generator()

bi_list = []
tri_list = []

hamilton.bigram.generator(bi_list, '<s>', 1)
hamilton.trigram.generator(tri_list, '<s>', '<s>', 1)
print(*liste)
print(*bi_list)
print(*tri_list)

