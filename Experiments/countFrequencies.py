# from http://stackoverflow.com/questions/14674266/word-frequency-calculation-for-1gb-text-file-in-python

def computeFrequenciesInFiles(directory):
    """Given a directory, compute the frequencies of the words in each txt file in it.

"""
    from collections import Counter
    words = Counter()
    filenames = [f for f in os.listdir(directory) if r'[0-9]+.*\.txt', f)]
    for filename in filenames:
        with open(filename) as f:
            for line in f:      
                words.update(line.split())
    words.most_common()
