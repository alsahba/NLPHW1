import glob, os


from Author import Author
from Unigram import Unigram
from Bigram import Bigram
from Trigram import Trigram

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
        separated_line = list(map(lambda x: x.lower().strip(',.;:?()`\"\'\n[]'), separated_line))

        author.getBigram().prepareFirstAndLast(separated_line)
        author.getTrigram().prepareFirstAndLast(separated_line)

        author.counterCaller(separated_line)


file_list = []
openAllFiles(file_list)

u1 = Unigram({})
u2 = Unigram({})
b1 = Bigram({})
b2 = Bigram({})
t1 = Trigram({})
t2 = Trigram({})

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

# hamilton.generatorCaller(uni_list, bi_list, tri_list)

fire_list = []
openAllTestFiles(fire_list)
fire = fire_list[2]
print(fire.readline())
m = 0
n=0
for line in fire.readlines():
    separated_line = line.split(' ')
    separated_line = list(map(lambda x: x.lower().strip(',.;:?()`\"\'\n[]'), separated_line))
    for i in range(len(separated_line) - 1):
        m += madison.getBigram().calculateProbabilityOfNextWord(separated_line[i+1],separated_line[i])
        n += hamilton.getBigram().calculateProbabilityOfNextWord(separated_line[i+1],separated_line[i])


print("m: {}, n: {}".format(m,n))


# print(*uni_list)
# print(*bi_list)
# print(*tri_list)
# print(len(uni_list))
print(len(bi_list))
# print(len(tri_list))

