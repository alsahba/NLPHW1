import glob, os
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


def openAllTrainFiles(file_list):
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


def classifyAuthor(n_gram, author_name, madison_perplexity, hamilton_perplexity):

    if madison_perplexity < hamilton_perplexity:
        detected_author = "Madison"
    else:
        detected_author = "Hamilton"

    if author_name.lower().strip() == detected_author.lower():
        detection = "Successful detection!"
    else:
        detection = "Unsuccessful detection!"

    print("Author is: {} and detected author is: {}. {} with {}".format(
        author_name, detected_author, detection, n_gram))
    print("Perplexities: Hamilton language model: {}, Madison Language model: {}".format(
        hamilton_perplexity, madison_perplexity))
    print()


def test(hamilton, madison):
    test_file_list = []
    openAllTestFiles(test_file_list)

    for file in test_file_list:
        author_name = file.readline().strip()
        for line in file.readlines():
            separated_line = prepareLine(line)

            hamilton_bigram_perplexity = hamilton.getBigram().perplexityCalculator(separated_line)
            madison_bigram_perplexity = madison.getBigram().perplexityCalculator(separated_line)

            madison_trigram_perplexity = madison.getTrigram().perplexityCalculator(separated_line)
            hamilton_trigram_perplexity = hamilton.getTrigram().perplexityCalculator(separated_line)

            classifyAuthor("Bigram", author_name, madison_bigram_perplexity, hamilton_bigram_perplexity)
            classifyAuthor("Trigram", author_name, madison_trigram_perplexity, hamilton_trigram_perplexity)


def generateRandomTexts(author):
    unigram_generation, bigram_generation, trigram_generation = [], [], []
    author.generatorCaller(unigram_generation, bigram_generation, trigram_generation)

    print("{} language model's generations and perplexities: ".format(author.getName()))
    print(*unigram_generation)
    print(*bigram_generation)
    print(*trigram_generation)
    # print("Unigram generation: {}".format(*unigram_generation))
    # print("Bigram generation: {}".format(*bigram_generation))
    # print("Trigram generation: {}".format(*trigram_generation))
    print()
    print("Unigram perplexity: {}, Bigram perplexity: {}, Trigram perplexity: {}".format(
        author.getUnigram().perplexityCalculator(unigram_generation),
        author.getBigram().perplexityCalculator(bigram_generation),
        author.getTrigram().perplexityCalculator(trigram_generation)
    ))

    print()


file_list = []
openAllTrainFiles(file_list)

hamilton = Author("Hamilton")
madison = Author("Madison")

for file in file_list:
    author = file.readline()

    if author.strip() == "HAMILTON":
        frequencyCounter(file, hamilton)

    else:
        frequencyCounter(file, madison)

generateRandomTexts(hamilton)
generateRandomTexts(madison)
test(hamilton, madison)
