import glob, os
import bisect
import random


def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


# def pre(separated_line, unigram_mapping_list, bigram_mapping_list, trigram_mapping_list):
#
#     for i in range(2, len(separated_line)):
#         if separated_line[i] != '\n':
#             countWords(unigram_mapping_list, separated_line[i].lower().strip("?;:.,()"))
#             countWordsBigram(bigram_mapping_list, separated_line[i - 1].lower().strip("?;:.,()"),
#                              separated_line[i].lower().strip("?;:.,()"))
#             countWordsTrigram(trigram_mapping_list, separated_line[i - 2].lower().strip("?;:.,()"),
#                               separated_line[i - 1].lower().strip("?;:.,()"), separated_line[i].lower().strip("?;:.,()"))


def preCountWords(separated_line, mapping_list):
    uniqWords = set(separated_line)
    for word in uniqWords:
        countWords(mapping_list, word, separated_line.count(word))


# def preCountWordsBigram(separated_line, mapping_list):
#     for i in range(len(separated_line)):
#         if i == 0:
#             new_dict = {'count': 1,
#                         'key': separated_line[i],
#                         'prev_key': '<s>'}
#             mapping_list.append(new_dict)
#
#         elif separated_line[i] != '\n':
#             countWordsBigram(mapping_list, separated_line[i - 1],
#                              separated_line[i])
#
#     new_dict = {'count': 1,
#                 'key': '</s>',
#                 'prev_key': separated_line[len(separated_line) - 1]}
#     mapping_list.append(new_dict)


def newBigramCounter(separated_line, unigram_mapping_list):
    for i in range(len(separated_line)):
        if i + 1 < len(separated_line):
            k = []
            for dicti in [x for x in unigram_mapping_list if x["key"] == separated_line[i]]:
                for dicti2 in [y for y in dicti['next_key'] if y["key"] == separated_line[i + 1]]:
                    k.append(dicti2)

                if len(k) != 0:
                    var = k[0]['count'] + 1
                    k[0]['count'] = var

                else:
                    new_dict = {'count': 1,
                                'key': separated_line[i + 1],
                                'next_key': []}
                    dicti['next_key'].append(new_dict)

def newTrigramCounter(separated_line, mapping_list):
    for i in range(len(separated_line)):
        if i + 2 < len(separated_line):
            k = []
            for dicti in [x for x in mapping_list if x["key"] == separated_line[i]]:
                for dicti2 in [y for y in dicti['next_key'] if y["key"] == separated_line[i + 1]]:
                    for dicti3 in [z for z in dicti2['next_key'] if z["key"] == separated_line[i + 2]]:
                        k.append(dicti3)

                if len(k) != 0:
                    var = k[0]['count'] + 1
                    k[0]['count'] = var

                else:
                    new_dict = {'count': 1,
                                'key': separated_line[i + 2],
                                'next_key': []}
                    dicti2['next_key'].append(new_dict)


# def preCountWordsTrigram(separated_line, mapping_list):
#     for i in range(len(separated_line)):
#         if i == 0:
#             new_dict = {'count': 1,
#                         'key': separated_line[i],
#                         'prev_key': '<s>',
#                         'second_prev_key': '<s>'}
#             mapping_list.append(new_dict)
#
#         elif i == 1:
#             new_dict = {'count': 1,
#                         'key': separated_line[i],
#                         'prev_key': separated_line[i - 1],
#                         'second_prev_key': '<s>'}
#             mapping_list.append(new_dict)
#
#         elif separated_line[i] != '\n':
#             countWordsTrigram(mapping_list, separated_line[i-2],
#                               separated_line[i - 1], separated_line[i])
#
#     new_dict = {'count': 1,
#                 'key': '</s>',
#                 'prev_key': separated_line[len(separated_line) - 1],
#                 'second_prev_key': separated_line[len(separated_line) - 2]}
#     mapping_list.append(new_dict)
#
#     new_dict = {'count': 1,
#                 'key': '</s>',
#                 'prev_key': '</s>',
#                 'second_prev_key': separated_line[len(separated_line) - 1]}
#     mapping_list.append(new_dict)


def mappingDistributor(text_file, unigram_mapping_list, bigram_mapping_list, trigram_mapping_list):
    for line in text_file.readlines():
        split_line = line.split(' ')
        split_line = list(map(lambda x: x.lower().strip(',.;:?()'), split_line))
        preCountWords(split_line, unigram_mapping_list)
        newBigramCounter(split_line, unigram_mapping_list)
        newTrigramCounter(split_line, unigram_mapping_list)

def countWords(mapping_list, key, count):
    k = []
    for dicti in [x for x in mapping_list if x["key"] == key]:
        k.append(dicti)

    if len(k) != 0:
        var = k[0].get('count') + count
        k[0]['count'] = var

    else:
        new_dict = {'count': count,
                    'key': key,
                    'next_key': []}
        mapping_list.append(new_dict)


# def countWordsBigram(mapping_list, prev_key, key):
#     k = []
#     for dicti in [x for x in mapping_list if x["prev_key"] == prev_key and x["key"] == key]:
#         k.append(dicti)
#
#     if len(k) != 0:
#         var = k[0].get('count') + 1
#         k[0]['count'] = var
#
#     else:
#         new_dict = {'count': 1,
#                     'key': key,
#                     'prev_key': prev_key}
#         mapping_list.append(new_dict)
#
#
# def countWordsTrigram(mapping_list, second_prev_key, prev_key, key):
#     k  = []
#     for dicti in [x for x in mapping_list if x["second_prev_key"] == second_prev_key
#                                             and x["prev_key"] == prev_key and x["key"] == key]:
#         k.append(dicti)
#
#     if len(k) != 0:
#         var = k[0].get('count') + 1
#         k[0]['count'] = var
#
#     else:
#         new_dict = {'count': 1,
#                     'key': key,
#                     'prev_key': prev_key,
#                     'second_prev_key': second_prev_key}
#         mapping_list.append(new_dict)
#
#
# def newerCountWordsTrigram(mapping_list, second_prev_key, prev_key, key):
#
#     for dicti in [x for x in mapping_list if x["second_prev_key"] == second_prev_key
#                                             and x["prev_key"] == prev_key and x["key"] == key]:
#         k.append(dicti)
#
#     if len(k) != 0:
#         var = k[0].get('count') + 1
#         k[0]['count'] = var
#
#     else:
#         new_dict = {'count': 1,
#                     'key': key,
#                     'prev_key': prev_key,
#                     'second_prev_key': second_prev_key}
#         mapping_list.append(new_dict)
#

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


def totalWordCountCalculator(mapping_list):
    sum = 0
    for dicts in mapping_list:
        sum = sum + int(dicts.get('count'))
    return sum


def unigramGenerator(mapping_list, total_word_count):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []

    for dict in mapping_list:
        word_probability = probabilityCalculator(dict, total_word_count)
        cumulative_probability = cumulative_probability + word_probability
        probability_distribution_list.append(cumulative_probability)
        word_list.append(dict.get('key'))

    generate(probability_distribution_list, word_list)

#Big time defects ayrilmasi gerekiyor unigraminda bigraminda su anki hal cok kotu
#Baslangicta random bi word secmesi gerekiyor onun icinde unigrama ihtiyaci var
def bigramGenerator(mapping_list, last_list, prev_word, repeat_count):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []
    found_ones = []
    temp_list = []

    for dict in mapping_list:
        if dict.get('key') == prev_word:
            found_ones.append(dict)
        elif not dict.get('key') in temp_list:
            temp_list.append(dict.get('key'))

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

    print(repeat_count)
    if repeat_count <= 30 and new_word != '</s>':
        bigramGenerator(mapping_list, last_list, new_word, repeat_count + 1)


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

hamilton_unigram_word_mapping = []
madison_unigram_word_mapping = []
hamilton_bigram_word_mapping = []
madison_bigram_word_mapping = []
hamilton_trigram_word_mapping = []
madison_trigram_word_mapping = []

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

#unigramGenerator(hamilton_unigram_word_mapping)
bi_list = []
tri_list = []

i = totalWordCountCalculator(hamilton_unigram_word_mapping)


unigramGenerator(hamilton_unigram_word_mapping, i)
# bigramGenerator(hamilton_bigram_word_mapping, bi_list, '<s>', 1)
# trigramGenerator(hamilton_trigram_word_mapping, tri_list, '<s>', '<s>', 1)

# print(hamilton_unigram_word_mapping)

