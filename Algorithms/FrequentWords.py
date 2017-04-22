import os
import PatternCount
import PatternConverters
import HammingDistance

# Straitforward algorithm in O(n^2) time #
def frequent_words(text, k):
        
    frequentWords = []    
    count = []

    for i in range(len(text) - k + 1):
        substr = text[i:i+k]
        count.append(PatternCount.count_worlds(text, substr))

    max_num = 0
    max_num = max(count)
    for i in range(len(count)):
        if(count[i] == max_num):
            frequentWords.append(text[i:i+k])

    print(set(frequentWords))

def frequent_words_optimized(text, k):
    
    frequency_array = [0]*4**k
    for i in range (len(text) - k + 1):
        pattern = text[i:i+k]
        index = PatternConverters.pattern_to_number(pattern)
        frequency_array[index] = frequency_array[index] + 1
    
    #result = " ".join(map(str,frequency_array))
    #print(result)

    return frequency_array
    
def clump_finding(genome, k, L, t):
    frequent_patterns = []
    clumps = []
    frequency_array = [0]*4**k

    frequency_array = frequent_words_optimized(genome[0:L], k)

    for i in range(len(frequency_array)):
        if (frequency_array[i] >= t):
            clumps.append(PatternConverters.number_to_pattern(i, k))
    
    for i in range(1, len(genome) - L):
        first_index = PatternConverters.pattern_to_number(genome[i-1:i+k-1])
        frequency_array[first_index] = frequency_array[first_index] - 1
        last_index = PatternConverters.pattern_to_number(genome[i+L-k:i+L])
        frequency_array[last_index] = frequency_array[last_index] + 1
        if(frequency_array[last_index] >= t):
            clumps.append(PatternConverters.number_to_pattern(last_index, k))

    return set(clumps)   

def frequent_words_with_mismatches(text, k, d):
    frequent_patterns = [0]*4**k    
    frequency_array = [0]*4**k    
    close_patterns = [0]*4**k

    for i in range(len(text) - k):
        neighborhood = HammingDistance.hamming_neighbors(text[i:i+k], d)
        for pattern in neighborhood:
            index = PatternConverters.pattern_to_number(pattern)
            close_patterns[index] = 1

    for i, v in enumerate(close_patterns):
        if close_patterns[i] == 1:
            pattern = PatternConverters.number_to_pattern(i, k)
            frequency_array[i] = PatternCount.approx_pattern_count(text, pattern, d) + PatternCount.approx_pattern_count(PatternConverters.reverse_compliment(text), pattern, d)

    maxCount = max(frequency_array)

    return [PatternConverters.number_to_pattern(i, k) for i, x in enumerate(frequency_array) if x == maxCount]
