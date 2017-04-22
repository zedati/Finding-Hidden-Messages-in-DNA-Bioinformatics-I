def skew(genome):
    skew = [0]*(len(genome) + 1)
    skew[0] = 0
    for i in range(len(genome)):
        if(genome[i] == "G"):
            skew[i+1] = skew[i] + 1
            continue
        if(genome[i] == "C"):
            skew[i+1] = skew[i] - 1
            continue
        skew[i+1] = skew[i]
    
    min_val = min(skew)

    return (i for i, v in enumerate(skew) if v == min_val)

print(skew("CATTCCAGTACTTCGATGATGGCGTGAAGA"))