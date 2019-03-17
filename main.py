import glob, os, re

from Author import Author


def prepareLine(line):
    line = line.replace(",", " ")
    line = line.replace(";", " ")
    line = line.replace(":", " ")
    line = line.replace("?", " ")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.replace("`", " ")
    line = line.replace("[", " ")
    line = line.replace("]", " ")
    line = line.replace("\n", "")
    line = line.replace("\t", "")
    line = line.replace("\r", "")
    line = line.replace("\'", " ")
    line = line.replace("\"", " ")
    line = line.replace("  ", " ")
    line = line.replace("   ", " ")
    line = line.replace(" .", ".")
    line = line.lower()
    return line.split()


def openAllFiles(file_list):
    os.chdir("./dataset")
    for f in glob.glob("*.txt"):
        file_list.append(open(f, 'r'))


def openAllTestFiles(file_list):
    os.chdir("../datatest")
    for f in glob.glob("*.txt"):
        file_list.append(open(f, 'r'))


def frequencyCounter(text_file, author):
    for line in text_file.readlines():
        separated_line = prepareLine(line)

        author.getBigram().prepareFirstAndLast(separated_line)
        author.getTrigram().prepareFirstAndLast(separated_line)

        author.counterCaller(separated_line)


def uniqueBigramCounter(bigram):
    unique_count = 0

    for second_mapping in bigram.mapping.items():
        unique_count += len(second_mapping)

    return unique_count


def bigramTotalProbability(separated_line, hamilton_total_probability=0, madison_total_probability=0):
    totalBigramMadi = madison.getBigram().totalBigramCalculator()
    totalBigramHami = hamilton.getBigram().totalBigramCalculator()

    madison_total_probability += madison.getBigram().calculateProbabilityOfNextWord(
        totalBigramMadi, separated_line[0])
    hamilton_total_probability += hamilton.getBigram().calculateProbabilityOfNextWord(
        totalBigramHami, separated_line[0])

    for i in range(len(separated_line) - 1):
        prev_word = separated_line[i]
        next_word = separated_line[i + 1]

        if '.' in prev_word:
            renewed_prev_word = prev_word.replace(".", "")
            renewed_current_word = next_word.replace(".", "")

            madison_total_probability += madison.getBigram().calculateProbabilityOfNextWord(
                totalBigramMadi, renewed_current_word)
            hamilton_total_probability += hamilton.getBigram().calculateProbabilityOfNextWord(
                totalBigramHami, renewed_current_word)

            madison_total_probability += madison.getBigram().calculateProbabilityOfNextWord(
                totalBigramMadi, '</s>', renewed_prev_word)
            hamilton_total_probability += hamilton.getBigram().calculateProbabilityOfNextWord(
                totalBigramHami, '</s>', renewed_prev_word)

        else:
            renewed_current_word = next_word.replace(".", "")

            madison_total_probability += madison.getBigram().calculateProbabilityOfNextWord(
                totalBigramMadi, renewed_current_word, prev_word)
            hamilton_total_probability += hamilton.getBigram().calculateProbabilityOfNextWord(
                totalBigramHami, renewed_current_word, prev_word)

    return {'madison': madison_total_probability, 'hamilton': hamilton_total_probability}

def trigramTotalProbability(separated_line, hamilton_total_probability=0, madison_total_probability=0):
    for i in range(len(separated_line) - 2):
        prev_word = separated_line[i]
        next_word = separated_line[i + 1]


        # if '.' in prev_word:
        #     prev_word = prev_word.replace(".", "")
        #     next_word = next_word.replace(".", "")
        #
        #     hamilton_trigram_total_probability += hamilton.getTrigram().calculateProbabilityOfNextWord(60000,
        #                                                                                                separated_line[
        #                                                                                                    i + 2],
        #                                                                                                separated_line[
        #                                                                                                    i + 1])
        #     madison_trigram_total_probability += madison.getTrigram().calculateProbabilityOfNextWord(60000,
        #                                                                                              separated_line[
        #                                                                                                  i + 2],
        #                                                                                              separated_line[
        #                                                                                                  i + 1])
        # else:
        #     hamilton_trigram_total_probability += hamilton.getTrigram().calculateProbabilityOfNextWord(60000,
        #         separated_line[i + 2], separated_line[i + 1], separated_line[i])
        #     madison_trigram_total_probability += madison.getTrigram().calculateProbabilityOfNextWord(60000,
        #         separated_line[i + 2], separated_line[i + 1], separated_line[i])


file_list = []
openAllFiles(file_list)

hamilton = Author("hamilton")
madison = Author("madison")

for file in file_list:
    author = file.readline()

    if author.strip() == "HAMILTON":
        frequencyCounter(file, hamilton)

    else:
        frequencyCounter(file, madison)


uni_list = []
bi_list = []
tri_list = []
hamilton.generatorCaller(uni_list, bi_list, tri_list)

fire_list = []
openAllTestFiles(fire_list)
fire = fire_list[5]
print(fire.readline())

hamilton_trigram_total_probability = 0
madison_trigram_total_probability = 0

hamilton_total_probability = 0
madison_total_probability = 0

mapo = madison.getTrigram().mapping.get('<s>')

for line in fire.readlines():
    separated_line = prepareLine(line)

    hamilton_total_probability = hamilton.getBigram().perplexityCalculator(separated_line)
    madison_total_probability = madison.getBigram().perplexityCalculator(separated_line)

    madison_trigram_total_probability = madison.getTrigram().perplexityCalculator(separated_line)
    hamilton_trigram_total_probability = hamilton.getTrigram().perplexityCalculator(separated_line)

var = float(-1/len(separated_line))
hamilton_total_probability = var * hamilton_total_probability
madison_total_probability = var * madison_total_probability

hamilton_total_probability = pow(2, hamilton_total_probability)
madison_total_probability = pow(2, madison_total_probability)

hamilton_trigram_total_probability = var * hamilton_trigram_total_probability
madison_trigram_total_probability = var * madison_trigram_total_probability

hamilton_trigram_total_probability = pow(2, hamilton_trigram_total_probability)
madison_trigram_total_probability = pow(2, madison_trigram_total_probability)


print("hamilton_total_probability: {}, madison_total_probability: {}".format(hamilton_total_probability, madison_total_probability))

print("hamilton_trigram_probability: {}, madison_trigram_probability: {}".format(hamilton_trigram_total_probability,
                                                                                 madison_trigram_total_probability))
print(*uni_list)
print(*bi_list)
print(*tri_list)
# print(len(uni_list))
# print(len(bi_list))
# print(len(tri_list))


