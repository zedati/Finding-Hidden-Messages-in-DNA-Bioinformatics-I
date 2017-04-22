import HammingDistance
from collections import Counter
import random
import operator

def motif_enumeration(dna, k, d):
    patterns = []
    pr = []

    for strand in dna:
        for i in range(len(strand) - k):
            neighborhood = HammingDistance.hamming_neighbors(strand[i:i+k], d)
            for pattern_prime in neighborhood:
                c = 0
                for x in dna:
                    for i in range(len(x) - len(pattern_prime) + 1):
                        chunk = x[i:i+len(pattern_prime)]
                        if (chunk == pattern_prime) | (HammingDistance.hamming_distance(chunk, pattern_prime) <= d):
                            c += 1
                            break

                #c += sum(1 for x in dna if pattern_prime in x)
                if c == len(dna):
                    patterns.append(pattern_prime)

    return set(patterns)


def most_probable_motif(text, k, profile_matrix):
    max_prob = 0
    most_prop_kmer = ""
    for i in range(len(text) - k + 1):
        cur_prop = 1
        kmer = text[i:i+k]
        for i, c in enumerate(kmer):
            cur_prop *= profile_matrix[c][i]
        if max_prob < cur_prop:
            max_prob = cur_prop
            most_prop_kmer = kmer
    
    if most_prop_kmer == "":
        most_prop_kmer = text[:k]

    return most_prop_kmer
  

def greedy_motif_search(sequences, k):
    best_motifs = [seq[:k] for seq in sequences]
    motifs = []

    for i in range(len(sequences[0]) - k + 1):
        kmer = sequences[0][i:i+k]
        motifs.append(kmer)
        profile_matrix = generate_profile_matrix(motifs, len(motifs))
        
        for j in range(1, len(sequences)):
            most_prop_kmer_in_seq = most_probable_motif(sequences[j], k, profile_matrix)
            motifs.append(most_prop_kmer_in_seq)
            profile_matrix = generate_profile_matrix(motifs, len(motifs))
        
        if __score_motifs(motifs, k) < __score_motifs(best_motifs, k):
            best_motifs = motifs  
        motifs = []
    return best_motifs


def randomized_motif_search(sequences, k):
    motifs = []
    for sequence in sequences:
        r = random.randrange(0, len(sequences[0]) - k)
        motifs.append(sequence[r:r+k])

    best_motifs = motifs   
    best_score = __score_motifs(best_motifs, k) 
    
    while True:
        profile_matrix = generate_profile_matrix(motifs, len(motifs))
        motifs = __get_most_probable_kmers(profile_matrix, sequences, k)
        cur_score = __score_motifs(motifs, k)
        if cur_score < best_score:
            best_motifs = motifs
            best_score = cur_score
        else:
            return [best_motifs, best_score]
     
def gibbs_sampler_search(sequences, k, n):
    motifs = []
    for sequence in sequences:
        r = random.randrange(0, len(sequences[0]) - k)
        motifs.append(sequence[r:r+k])

    best_motifs = motifs   
    best_score = __score_motifs(best_motifs, k) 
    
    for j in range(n):
        r = random.randrange(0, len(sequences))
        del motifs[r]
        profile_matrix = generate_profile_matrix(motifs, len(motifs))

        kmers_probability = {}
        for i in range(len(sequence) - k + 1):
            kmer = sequences[r][i:i+k]
            kmers_probability[kmer] = __get_kmer_probability(kmer, profile_matrix)
        total_prob = sum(kmers_probability.values())
        motif = max(kmers_probability.items(), key=operator.itemgetter(1))[0]
        #norm_prob = {k: v/float(total_prob) for k, v in kmers_probability.items()}
        #br = biased_random([v for v in norm_prob.values()])
        #motif = [v for i, v in enumerate(norm_prob.keys()) if i == br][0]
        motifs.insert(r, motif)
        cur_score = __score_motifs(motifs, k)
        if cur_score < best_score:
            best_motifs = motifs
            best_score = cur_score

    return [best_motifs, best_score]

def generate_profile_matrix(kmers, count):
    profile_matrix = {}
    matrix = {
      "A": [],
      "C": [],
      "G": [],
      "T": []
    } 
    for i, c in enumerate(kmers[0]):
        for letter in ["A", "C", "G", "T"]:
            matrix[letter].append((letter == c) if float(1) else float(0))
    
    for i in range(1, len(kmers)):
        for i, c in enumerate(kmers[i]):
            matrix[c][i] += 1

    #isZeroPresent = False
    #for key, value in matrix.items():
    #    for i, v in enumerate(value):
    #        if matrix[key][i] == 0:
    #            isZeroPresent = True

    #if isZeroPresent:
    #    count += 4
    #    for key, value in matrix.items():
    #        for i, v in enumerate(value):
    #            matrix[key][i] += 1

    for key, value in matrix.items():
        for i, v in enumerate(value):
            matrix[key][i] = round(v/count, 4)

    for i in range(len(kmers[0])):
        c = 0
        for key, value in matrix.items():
            c += matrix[key][i]
        assert abs(c - 1) < 1e-3

    return matrix
         
def __score_motifs(motifs, k):
    score = 0    
    for i in range(k):
        col = []
        for motif in motifs: 
            col.append(motif[i]);
        most_common_letter = Counter(col).most_common(1)       
        score += sum(1 for v in col if v != most_common_letter[0][0])  
    
    return score

 
def __get_most_probable_kmers(profile_matrix, sequences, k):
    most_probable_kmers = []
    for sequence in sequences:
        kmers_probability = {}
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]
            kmers_probability[kmer] = __get_kmer_probability(kmer, profile_matrix)
        kmers_probability = max(kmers_probability.items(), key=operator.itemgetter(1))
        most_probable_kmers.append(kmers_probability[0]) 

    return most_probable_kmers

def __get_kmer_probability(kmer, profile_matrix):
    probability = 1
    for i,c in enumerate(kmer):
        probability *= profile_matrix[c][i]
        if probability == 0:
            return 0
    return probability

def func():
    dict = {}
    list1 = []
    for i in range(5000):
        motifs = randomized_motif_search([
"AAGCCAAA",
"AATCCTGG",
"GCTACTTG",
"ATGTTTTG"], 3)
         
        list1.append(motifs)
    return sorted(list1, key=operator.itemgetter(1))


def biased_random(intervals):
    for i, v in enumerate(intervals):
        if i == len(intervals) - 1:
            break
        intervals[i+1] = intervals[i] + intervals[i+1]
    x = random.random()
    for i, v in enumerate(intervals):
        if (x < v):
            return i

#greedy_motif_search(["GGCGTTCAGGCA",
#     "AAGAATCAGTCA",
#     "CAAGGAGTTCGC",
#     "CACGTCAATCAC",
#     "CAATAATATTCG"], 3)  

__score_motifs([
"TTAACC",
"ATAACT",
"TTAACC",
"TGAAGT",
"TTAACC",
"TTAAGC",
"TTAACC",
"TGAACA"
],6)
