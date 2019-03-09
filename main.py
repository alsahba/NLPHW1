import glob, os
import bisect
import random

def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


def preCountWords(separated_line, mapping_list):
    for word in separated_line:
        if word != '\n':
            countWords(mapping_list, word.lower().strip("?,.;:"))


def preCountWordsBigram(separated_line, mapping_list):
    for i in range(len(separated_line)):
        if i == 0:
            new_dict = {'count': 1,
                        'key': separated_line[i].lower().strip("?,.;:"),
                        'prev_key': '<s>'}
            mapping_list.append(new_dict)

        elif separated_line[i] != '\n':
            countWordsBigram(mapping_list, separated_line[i - 1].lower().strip("?,.;:"),
                             separated_line[i].lower().strip("?,.;:"))

    new_dict = {'count': 1,
                'key': '</s>',
                'prev_key': separated_line[len(separated_line) - 1].lower().strip("?,.;:")}
    mapping_list.append(new_dict)


def preCountWordsTrigram(separated_line, mapping_list):
    for i in range(len(separated_line)):
        if i == 0:
            new_dict = {'count': 1,
                        'key': separated_line[i].lower().strip("?,.;:"),
                        'prev_key': '<s>',
                        'second_prev_key': '<s>'}
            mapping_list.append(new_dict)

        elif i == 1:
            new_dict = {'count': 1,
                        'key': separated_line[i].lower().strip("?,.:;"),
                        'prev_key': separated_line[i - 1].lower().strip("?,.:;"),
                        'second_prev_key': '<s>'}
            mapping_list.append(new_dict)

        elif separated_line[i] != '\n':
            countWordsTrigram(mapping_list, separated_line[i-2].lower().strip("?,.;:"),
                              separated_line[i - 1].lower().strip("?,.;:"), separated_line[i].lower().strip("?,.;:"))

    new_dict = {'count': 1,
                'key': '</s>',
                'prev_key': separated_line[len(separated_line) - 1].lower().strip("?,.;:"),
                'second_prev_key': separated_line[len(separated_line) - 2].lower().strip("?,.;:")}
    mapping_list.append(new_dict)

    new_dict = {'count': 1,
                'key': '</s>',
                'prev_key': '</s>',
                'second_prev_key': separated_line[len(separated_line) - 1].lower().strip("?,.;:")}
    mapping_list.append(new_dict)


def mappingDistributor(text_file, unigram_mapping_list, bigram_mapping_list, trigram_mapping_list):
    for line in text_file.readlines():
        split_line = line.split(' ')
        # preCountWords(split_line, unigram_mapping_list)
        preCountWordsBigram(split_line, bigram_mapping_list)
        #preCountWordsTrigram(split_line, trigram_mapping_list)


def countWords(mapping_list, key):
    if len(mapping_list) == 0:
        new_dict = {'count': 1,
                    'key': key}
        mapping_list.append(new_dict)
    else:
        not_found_flag = True
        for mapping in mapping_list:
            if str(mapping.get('key')) == key:
                var = int(mapping.get('count')) + 1
                mapping['count'] = var
                not_found_flag = False
                break

        if not_found_flag:
            new_dict = {'count': 1,
                        'key': key}
            mapping_list.append(new_dict)


def countWordsBigram(mapping_list, prev_key, key):
    not_found_flag = True
    for mapping in mapping_list:
        if mapping.get('prev_key') == prev_key and mapping.get('key') == key:
            var = int(mapping.get('count')) + 1
            mapping['count'] = var
            not_found_flag = False
            break

    if not_found_flag:
        new_dict = {'count': 1,
                    'key': key,
                    'prev_key': prev_key}
        mapping_list.append(new_dict)


def countWordsTrigram(mapping_list, second_prev_key, prev_key, key):
    not_found_flag = True
    for mapping in mapping_list:
        if str(mapping.get('second_prev_key')) == second_prev_key and str(mapping.get('prev_key')) == prev_key and str(mapping.get('key')) == key:
            var = int(mapping.get('count')) + 1
            mapping['count'] = var
            not_found_flag = False
            break

    if not_found_flag:
        new_dict = {'count': 1,
                    'key': key,
                    'prev_key': prev_key,
                    'second_prev_key': second_prev_key}
        mapping_list.append(new_dict)


def boundaries(num, breakpoints, result):
    i = bisect.bisect(breakpoints, num)

    if i >= len(result):
        i = len(result) - 1
    return result[i]


def generate(probability_distribution_list, word_list):
    unmeaningful_list = []
    for i in range(30):
        dice = random.uniform(0, 1)
        unmeaningful_list.append(boundaries(dice, probability_distribution_list, word_list))

    print(*unmeaningful_list)

def probabilityCalculator(word_dict, total_word_count):
    return word_dict.get('count') / total_word_count

def totalWordCountCalculator(mapping_list):
    sum = 0
    for dicts in mapping_list:
        sum = sum + int(dicts.get('count'))
    return sum

def unigramGenerator(mapping_list):
    cumulative_probability = 0.0
    probability_distribution_list = []
    word_list = []

    totalCount = totalWordCountCalculator(mapping_list)

    for dict in mapping_list:
        word_probability = probabilityCalculator(dict, totalCount)
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
        if dict.get('prev_key') == prev_word:
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
    print(repeat_count)
    if repeat_count <= 30 and new_word != '</s>':
        bigramGenerator(mapping_list, last_list, new_word, repeat_count + 1)

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
    print(file.name + " " + author)

    if author.strip() == "HAMILTON":
        mappingDistributor(file, hamilton_unigram_word_mapping,
                           hamilton_bigram_word_mapping, hamilton_trigram_word_mapping)

    else:
        mappingDistributor(file, madison_unigram_word_mapping,
                           madison_bigram_word_mapping, madison_trigram_word_mapping)

    count -= 1
    print(count)

#unigramGenerator(hamilton_unigram_word_mapping)
random_list = []
bigramGenerator(hamilton_bigram_word_mapping, random_list, 'to', 1)


print(*random_list)

