import os
import re
import HammingDistance

def count_worlds(text, pattern):
    count = 0

    for i in range(len(text) - len(pattern) + 1):
        if(text[i:i+len(pattern)] == pattern):
            count = count + 1

    #print(count)
    return count

def all_substrings(text, pattern):

    regexp = "(?=" + pattern + ")" 
    return [m.start() for m in re.finditer(regexp, text)]

def approx_pattern_count(text, pattern, dist):
    pos = []
        
    for i in range(len(text) - len(pattern) + 1):
        chunk = text[i:i+len(pattern)]
        if (chunk == pattern) | (HammingDistance.hamming_distance(chunk, pattern) <= dist):
            pos.append(i)

    return len(pos)

print(approx_pattern_count("TACGCATTACAAAGCACA", "AA", 1))