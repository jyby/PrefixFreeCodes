import doctest,os
from collections import Counter

# adapted from http://stackoverflow.com/questions/14674266/word-frequency-calculation-for-1gb-text-file-in-python

def computeFrequenciesInUnionOfFiles(filenames):
    """Given a list of filenames, compute the frequencies of the words in each txt file in it.
   
>>> f = computeFrequenciesInUnionOfFiles(["test1.txt", "test2.txt"])
>>> print(sorted(f))
[('a', 2), ('b', 3), ('c', 5), ('d', 9), ('e', 17), ('f', 33), ('g', 1), ('h', 1), ('i', 1), ('j', 1), ('k', 1), ('l', 1), ('m', 1), ('n', 1), ('o', 1), ('p', 1), ('q', 1), ('r', 1), ('s', 1), ('t', 1), ('u', 1), ('v', 1), ('w', 1), ('x', 1), ('y', 1), ('z', 1)]
"""
    words = Counter()
    for filename in filenames:
        with open(filename) as f:
            for line in f:      
                words.update(line.split())
    return words.most_common()

        
if __name__ == '__main__':
    doctest.testmod()
