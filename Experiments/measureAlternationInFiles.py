import doctest,os
from collections import Counter
from alternationMeasure import EISignature,EIAlternation,EISignatureAndAlternation

def countFrequenciesInFile(filename):
    """Given a file name, compute the frequencies of the words in the corresponding file.

>>> f = countFrequenciesInFile("test1.txt")
>>> print(sorted(f))
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

>>> f = countFrequenciesInFile("test2.txt")
>>> print(sorted(f))
[1, 2, 4, 8, 16, 32]
"""
    words = Counter()
    with open(filename) as myfile:
        for line in myfile:      
            words.update(line.split())
    f = []
    for (word,frequency) in words.most_common():
        f.append(frequency)
    return f

def measureAlternationInFile(filename):
    """Given a file name, compute the alternation difficulty measure on it.

>>> print(measureAlternationInFile("test1.txt"))
1
>>> print(measureAlternationInFile("test2.txt"))
5
"""
    f = countFrequenciesInFile(filename)
    return EIAlternation(f)

def measureAlternationInFiles(filenames):
    """Given a list of files, compute the alternation difficulty measure for each txt file in it, and returns it in a vector of pairs (filename,alternation).

>>> print(measureAlternationInFiles(["test1.txt","test2.txt"]))
[('test1.txt', 1), ('test2.txt', 5)]

"""
    stats = []
    for filename in filenames:
        alternation = measureAlternationInFile(filename)
        stats.append((filename,alternation))
    return stats

def outputAlternationsInFilesForLaTeX(filenames):
    """Given a list of files, print a latex formated string representing the alternation difficulty measure for each txt file in it.

>>> outputAlternationsInFilesForLaTeX(["test1.txt", "test2.txt", "test3.txt"])
\\begin{array}[c|c]
test1.txt & 1 \\\\ \\hline
test2.txt & 5 \\\\ \\hline
test3.txt & 5
\\end{array}
"""
    stats = measureAlternationInFiles(filenames)
    print("\\begin{array}[c|c]")
    for (filename,alternation) in stats[0:-1]:
        print(filename+" & "+str(alternation)+" \\\\ \\hline")
    (filename,alternation) = stats[-1]
    print(filename+" & "+str(alternation))
    print("\\end{array}")
    
if __name__ == '__main__':
    doctest.testmod()
