import glob, os, math

from Author import Author


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
        separated_line = line.split(' ')
        separated_line = list(map(lambda x: x.lower().strip(',;:?()`\t\"\'\n[]\r'), separated_line))

        author.getBigram().prepareFirstAndLast(separated_line)
        author.getTrigram().prepareFirstAndLast(separated_line)

        author.counterCaller(separated_line)


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


# uni_list = []
# bi_list = []
# tri_list = []
# hamilton.generatorCaller(uni_list, bi_list, tri_list)

fire_list = []
openAllTestFiles(fire_list)
fire = fire_list[3]
print(fire.readline())
hamiltonPro = 0
madisonPro = 0

totalBigramMadi = madison.getBigram().totalBigramCalculator()
totalBigramHami = hamilton.getBigram().totalBigramCalculator()

# for line in fire.readlines():
#     separated_line = line.split(' ')
#     separated_line = list(map(lambda x: x.lower().replace(".,?;:",""), separated_line))
#     for i in range(len(separated_line) - 1):
#         if i == 0:
#             perplexityM = madison.getBigram().calculateProbabilityOfNextWord(totalBigramMadi,
#                                                                              separated_line[i])
#             perplexityH = hamilton.getBigram().calculateProbabilityOfNextWord(totalBigramHami,
#                                                                               separated_line[i])
#         else:
#             perplexityM = madison.getBigram().calculateProbabilityOfNextWord(totalBigramMadi,
#                                                                              separated_line[i+1], separated_line[i])
#             perplexityH = hamilton.getBigram().calculateProbabilityOfNextWord(totalBigramHami,
#                                                                                separated_line[i+1], separated_line[i])



print("hamiltonPro: {}, madisonPro: {}".format(hamiltonPro, madisonPro))

# print(*uni_list)
# print(*bi_list)
# print(*tri_list)
# print(len(uni_list))
# print(len(bi_list))
# print(len(tri_list))

