import glob, os


def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


def preCountWords(splited_line, mapping_list):
    for word in splited_line:
        if word != '\n':
            countWords(mapping_list, word.lower())


def preCountWordsBigram(splited_line, mapping_list):
    for i in range(len(splited_line)):
        if i == 0:
            new_dict = {'count': 1,
                        'key': splited_line[i],
                        'prev_key': '<s>'}
            mapping_list.append(new_dict)

        elif splited_line[i] != '\n':
            countWordsBigram(mapping_list, splited_line[i - 1].lower(), splited_line[i].lower())


def authorDecicive(text_file, mapping_list):
    for line in text_file.readlines():
        split_line = line.split(' ')
        preCountWords(split_line, mapping_list)


def authorDeciciveBigram(text_file, mapping_list):
    for line in text_file.readlines():
        split_line = line.split(' ')
        preCountWordsBigram(split_line, mapping_list)


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
            new_dict = {'key': key,
                        'count': 1}
            mapping_list.append(new_dict)


def countWordsBigram(mapping_list, prev_key, key):
    not_found_flag = True
    for mapping in mapping_list:
        if str(mapping.get('prev_key')) == prev_key and str(mapping.get('key')) == key:
            var = int(mapping.get('count')) + 1
            mapping['count'] = var
            not_found_flag = False
            break

    if not_found_flag:
        new_dict = {'count': 1,
                    'key': key,
                    'prev_key': prev_key}
        mapping_list.append(new_dict)


file_list = []
openAllFiles(file_list)

hamilton_unigram_word_mapping = []
madison_unigram_word_mapping = []
hamilton_bigram_word_mapping = []
madison_bigram_word_mapping = []

for file in file_list:
    author = file.readline()
    print(file.name + " " + author)
    if author.strip() == "HAMILTON":
        #authorDecicive(file, hamilton_unigram_word_mapping)
        authorDeciciveBigram(file, hamilton_bigram_word_mapping)
    else:
        #authorDecicive(file, madison_unigram_word_mapping)
        authorDeciciveBigram(file, madison_bigram_word_mapping)

print("{} {}".format(madison_bigram_word_mapping, len(hamilton_bigram_word_mapping)))
