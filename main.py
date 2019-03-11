import glob, os


from Author import Author


def openAllFiles(file_list):
    os.chdir("./dataset")
    for file in glob.glob("*.txt"):
        file_list.append(open(file, 'r'))


def frequencyCounter(text_file, author):
    for line in text_file.readlines():
        separated_line = line.split(' ')
        separated_line = list(map(lambda x: x.lower().strip(',.;:?()`\"\'\n[]'), separated_line))

        author.trigram.prepareFirstAndLast(separated_line)
        author.bigram.prepareFirstAndLast(separated_line)

        author.unigram.counter(separated_line)
        author.bigram.counter(separated_line)
        author.trigram.counter(separated_line)


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


uni_list = []
bi_list = []
tri_list = []

hamilton.unigram.generator(uni_list)
hamilton.bigram.generator(bi_list, '<s>')
hamilton.trigram.generator(tri_list, '<s>', '<s>')

print(*uni_list)
print(*bi_list)
print(*tri_list)
print(len(uni_list))
print(len(bi_list))
print(len(tri_list))

