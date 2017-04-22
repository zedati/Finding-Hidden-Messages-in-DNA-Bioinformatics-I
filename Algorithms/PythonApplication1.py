import os
import json
import PatternCount
import FrequentWords
import PatternConverters
import Formatter
import Skew
from itertools import groupby
from collections import Counter
import operator
import HammingDistance
import MedianString
import Motifs

file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_197_3.txt"), "r")

pattern = file.readline().rstrip('\n');
text = file.readline().rstrip('\n');
#k = file.readline().rstrip('\n');

#PatternCount.count_worlds(text)
#array = PatternConverters.reverse_compliment(text)


output = open("output.txt", "w")
#for item in array:
#    print(item, file=output, end="")

#output.close()
#res = FrequentWords.clump_finding(text, 9, 500, 3)

#print(MedianString.median_string(text, int(pattern)))

#k = int(file.readline())
#matrix = {}
#for c in ["A", "C", "G", "T"]:
#    matrix[c] = list(map((lambda x: float(x)), file.readline().split()))

#text = [x.rstrip('\n') for x in text]

res = "\n".join(x for x in PatternConverters.composition(text, 100))
print(res, file=output)
file.close()
list = []

for i in range(1000):
    motifs = Motifs.gibbs_sampler_search(text, 15, 100)
    list.append(motifs)

for x in sorted(list, key=operator.itemgetter(1))[0][0]:
    print(x)

print(x)