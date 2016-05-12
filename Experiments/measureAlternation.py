import doctest,os
from collections import Counter
from alternationMeasure import EISignature,EIAlternation

def countFrequenciesInFile(filename):
    """Given a file name, compute the frequencies of the words in the corresponding file.

>>> f = countFrequenciesInFile("test1.txt")
>>> print(sorted(f))
[('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1), ('f', 1), ('g', 1), ('h', 1), ('i', 1), ('j', 1), ('k', 1), ('l', 1), ('m', 1), ('n', 1), ('o', 1), ('p', 1), ('q', 1), ('r', 1), ('s', 1), ('t', 1), ('u', 1), ('v', 1), ('w', 1), ('x', 1), ('y', 1), ('z', 1)]

>>> f = countFrequenciesInFile("test2.txt")
>>> print(f[0])
('f', 32)
"""
    words = Counter()
    with open(filename) as f:
        for line in f:      
            words.update(line.split())
    return words.most_common()

def measureAlternationsInFile(filename):
    """Given a file name, compute the alternation difficulty measure on it.

>>> print(measureAlternationsInFile("test1.txt"))
1
>>> print(measureAlternationsInFile("test2.txt"))
4
"""
    f = countFrequenciesInFile(filename)
    return EIAlternation(f)

    
if __name__ == '__main__':
    doctest.testmod()
