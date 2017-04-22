def pattern_to_number(pattern):
    
    if(len(pattern) == 1):
        return __symbol_to_number(pattern)

    return 4*pattern_to_number(pattern[:-1]) + __symbol_to_number(pattern[-1:])


def number_to_pattern(index, k):
    if(k == 1):
        return __number_to_symbol(index)
    
    reminder = index % 4
    index = index // 4

    return number_to_pattern(index, k-1) + __number_to_symbol(reminder)


def reverse_compliment(text):

    reverse = text[::-1]
    compliment = []

    for i in range(len(reverse)):
        compliment.append(__compliment(reverse[i]))

    return compliment
        
def composition(text, k):
    arr = [text[i:i+k] for i in range(0, len(text) - k + 1)]
    return sorted(arr)


def __symbol_to_number(symbol):
    return switcher.get(symbol, -1)

def __number_to_symbol(val):
    for symbol, value in switcher.items():
        if(value == val):
            return symbol

def __compliment(symbol):
    return complimentor.get(symbol)

switcher = {
    "A": 0,
    "C": 1,
    "G": 2,
    "T": 3
}

complimentor = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G"
}

#print(pattern_to_number("ATGCAA"))
#print(pattern_to_number("ACG"))
#print(number_to_pattern(5437, 7))
#print(number_to_pattern(5437, 8))
#print(reverse_compliment("CCAGATC"))