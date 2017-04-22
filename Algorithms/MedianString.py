import sys
import PatternConverters
import HammingDistance

def median_string(dna, k):
    distance = sys.maxsize
    median = []
    for i in range(4**k -1):
        pattern = PatternConverters.number_to_pattern(i, k)
        interm_distance = __distance_between_pattern_and_strings(pattern, dna)
        if distance >= interm_distance:
            distance = interm_distance
            median.append((pattern, distance))

    return median
        

def __distance_between_pattern_and_strings(pattern, dna):
    
    distance = 0
    for str in dna:
        hamming_distance = sys.maxsize
        for i in range(len(str) - len(pattern) + 1):
            interm_distance = HammingDistance.hamming_distance(pattern, str[i:i+len(pattern)])
            if hamming_distance > interm_distance:
                hamming_distance = interm_distance

        distance += hamming_distance
    
    return distance            
 
#print(median_string(["CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC","GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC","GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG"], 7))
