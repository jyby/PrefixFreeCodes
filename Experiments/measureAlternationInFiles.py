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
(1, 26)
>>> print(measureAlternationInFile("test2.txt"))
(5, 6)
"""
    f = countFrequenciesInFile(filename)
    return (EIAlternation(f),len(f))

def measureAlternationInFiles(filenames):
    """Given a list of files, compute the alternation difficulty measure for each txt file in it, and returns it in a vector of pairs (filename,alternation).

>>> print(measureAlternationInFiles(["test1.txt","test2.txt"]))
[('test1.txt', 26, 1), ('test2.txt', 6, 5)]

"""
    stats = []
    for filename in filenames:
        alternation,size = measureAlternationInFile(filename)
        stats.append((filename,size,alternation))
    return stats

def outputAlternationsInFilesForLaTeX(filenames):
    """Given a list of files, print a latex formated string representing the alternation difficulty measure for each txt file in it.

>>> outputAlternationsInFilesForLaTeX(["test1.txt", "test2.txt", "test3.txt"])
\\begin{array}[c|c]
test1.txt & 26 & 1 \\\\ \\hline
test2.txt & 6 & 5 \\\\ \\hline
test3.txt & 6 & 5
\\end{array}
"""
    stats = measureAlternationInFiles(filenames)
    print("\\begin{array}[c|c|c]")
    print("Filename & alphabet size & alternation \\\\ \\hline")
    for (filename,size,alternation) in stats[0:-1]:
        print(filename+" & "+str(size)+" & "+str(alternation)+" \\\\ \\hline")
    (filename,size,alternation) = stats[-1]
    print(filename+" & "+str(size)+" & "+str(alternation))
    print("\\end{array}")
    
if __name__ == '__main__':
    doctest.testmod()

    filenames = ["../DataSets/14529-0.txt", "../DataSets/32575-0.txt", "../DataSets/pg12944.txt", "../DataSets/pg24742.txt", "../DataSets/pg25373.txt", "../DataSets/pg31471.txt", "../DataSets/pg4545.txt", "../DataSets/pg7925.txt", "../DataSets/shakespeare.txt"]
    outputAlternationsInFilesForLaTeX(filenames)
