import doctest,os
from collections import Counter
from statisticsMeasure import statistics

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

def measureStatisticsInFile(filename):
    """Given a file name, compute the statistics on it.

>>> print(measureStatisticsInFile("test1.txt"))
(26, 26, 'EEEEEEEEEEEEEEEEEEEEEEEEEEIIIIIIIIIIIIIIIIIIIIIIIII', 1, 5, 2)
>>> print(measureStatisticsInFile("test2.txt"))
(63, 6, 'EEIEIEIEIEI', 5, 5, 5)
"""
    f = countFrequenciesInFile(filename)
    (signature,alternation,maxCodelength,nbDistinctCodeLengths) = statistics(f)
    return (sum(f),len(f),signature,alternation,maxCodelength,nbDistinctCodeLengths)

def measureStatisticsInFiles(filenames):
    """Given a list of files, compute the statistics for each txt file in it, and returns it in a vector of tuples (filename,statistics).

>>> print(measureStatisticsInFiles(["test1.txt","test2.txt"]))
[('test1.txt', 26, 26, 'EEEEEEEEEEEEEEEEEEEEEEEEEEIIIIIIIIIIIIIIIIIIIIIIIII', 1, 5, 2), ('test2.txt', 63, 6, 'EEIEIEIEIEI', 5, 5, 5)]


"""
    stats = []
    for filename in filenames:
        (documentSize,alphabetSize,signature,alternation,maxCodelength,nbDistinctCodeLengths) = measureStatisticsInFile(filename)
        stats.append((filename,documentSize,alphabetSize,signature,alternation,maxCodelength,nbDistinctCodeLengths))
    return stats

def outputStatisticsInFilesForLaTeX(filenames):
    """Given a list of files, print a latex formated string representing the statistics for each txt file in it.
"""
    stats = measureStatisticsInFiles(filenames)
    print("\\begin{tabular}{c|c|c|c|c|c}")
    print("Filename & document size & alphabet size & alternation & maxCodeLength & nbDistinctCodeLengths \\\\ \\hline")
    for (filename,documentSize,alphabetSize,signature,alternation,maxCodelength,nbDistinctCodeLengths) in stats[0:-1]:
        print(filename+" & "+str(documentSize)+" & "+str(alphabetSize)+" & "+str(alternation)+" & "+str(maxCodelength)+" & "+str(nbDistinctCodeLengths)+" \\\\ \\hline")
    (filename,documentSize,alphabetSize,signature,alternation,maxCodelength,nbDistinctCodeLengths) = stats[-1]
    print(filename+" & "+str(documentSize)+" & "+str(alphabetSize)+" & "+str(alternation)+" & "+str(maxCodelength)+" & "+str(nbDistinctCodeLengths))
    print("\\end{tabular}")
    
if __name__ == '__main__':
    doctest.testmod()

    filenames = ["../DataSets/14529-0.txt", "../DataSets/32575-0.txt", "../DataSets/pg12944.txt", "../DataSets/pg24742.txt", "../DataSets/pg25373.txt", "../DataSets/pg31471.txt", "../DataSets/pg4545.txt", "../DataSets/pg7925.txt", "../DataSets/shakespeare.txt"]
    print("Computing the statistics on "+str(filenames)+":")
    outputStatisticsInFilesForLaTeX(filenames)
