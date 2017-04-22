def hamming_distance(str1, str2):

    if len(str1) != len(str2):
        raise Exception("Strings of different length")

    distance = 0    

    for i, v in enumerate(str1):
        if str1[i] != str2[i]:
            distance += 1

    return distance


def hamming_neighbors(pattern, d):
    if d == 0:
        return pattern
    
    if len(pattern) == 1:
        return ['A', 'C', 'G', 'T']

    neighborhood = []
    suffixNeighbors = hamming_neighbors(pattern[1:], d)
    
    for str in suffixNeighbors:
        if hamming_distance(pattern[1:], str) < d:
            for n in ['A', 'C', 'G', 'T']:
                neighborhood.append(n + str)
        else:
            neighborhood.append(pattern[0] + str)
    
    return set(neighborhood)

print(hamming_neighbors("CCAGTCAATG", 1))