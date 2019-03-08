def countWords (mappingList, key):
    if len(mappingList) == 0:
        newDict = {'key': key,
                   'count': 1}
        mappingList.append(newDict)

    else:
        foundFlag = False
        for mapping in mappingList:
            if str(mapping.get('key')) == key:
                var = int(mapping.get('count')) + 1
                mapping['count'] = var
                foundFlag = True
                break

        if foundFlag == False:
            newDict = {'key': key,
                       'count': 1}
            mappingList.append(newDict)


f = open("1.txt", "r")

unigram_word_mapping = []


for line in f.readlines():
    splitted_line = line.split(' ')
    for word in splitted_line:
        if word != '\n':
            countWords(unigram_word_mapping, word.lower())

print(unigram_word_mapping)




