import glob, os
from Author import Author

# This method is used for get rid of unnecessary punctuation. Only dots are not handled.
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


# This method is used for opening all text files and put them to a file list in train file directory.
def openAllTrainFiles(file_list):
    os.chdir("./dataset")
    for f in glob.glob("*.txt"):
        file_list.append(open(f, 'r'))


# This method is used for opening all text files and put them to a file list in train file directory.
def openAllTestFiles(file_list):
    os.chdir("../datatest")
    for f in glob.glob("*.txt"):
        file_list.append(open(f, 'r'))


# This method is used for calling frequency counter functions of author for a file.
def frequencyCounter(text_file, author):
    for line in text_file.readlines():
        separated_line = prepareLine(line)

        author.getBigram().prepareFirstAndLast(separated_line)
        author.getTrigram().prepareFirstAndLast(separated_line)

        author.counterCaller(separated_line)


# This method is used for detection author of a file.
# It takes perplexities calculated with respect to hamilton and madison language model.
# If detected author matches test text file's author's name then detection is succeed.
def classifyAuthor(n_gram, author_name, hamilton_perplexity, madison_perplexity):

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
    print("Perplexities -> Hamilton language model: {}, Madison Language model: {}".format(
        hamilton_perplexity, madison_perplexity))
    print()

# This method is used for test our language models for test text files.
# All of the txt files in the test directory opened and
# perplexities calculated with respect to two authors' language models.
# After all that classifyAuthor method is called and result is tested
# whether is a successful detection or unsuccessful detection.
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

            classifyAuthor("Bigram", author_name, hamilton_bigram_perplexity, madison_bigram_perplexity)
            classifyAuthor("Trigram", author_name, hamilton_trigram_perplexity, madison_trigram_perplexity)


# This method is used for generation of random text and
# calculate generated text's perplexity for unigram, bigram and trigram with respect to author's language model.
def generateRandomTexts(author):
    unigram_generation, bigram_generation, trigram_generation = [], [], []
    author.generatorCaller(unigram_generation, bigram_generation, trigram_generation)

    print("{} language model's generations and perplexities: ".format(author.getName()))
    print("Unigram generation: {}".format(" ".join(str(x) for x in unigram_generation)))
    print("Bigram generation: {}".format(" ".join(str(x) for x in bigram_generation)))
    print("Trigram generation: {}".format(" ".join(str(x) for x in trigram_generation)))
    print()
    print("Unigram perplexity: {}, Bigram perplexity: {}, Trigram perplexity: {}".format(
        author.getUnigram().perplexityCalculator(unigram_generation),
        author.getBigram().perplexityCalculator(bigram_generation),
        author.getTrigram().perplexityCalculator(trigram_generation)
    ))

    print('\n\n')


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

