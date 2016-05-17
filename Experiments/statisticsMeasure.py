import unittest,doctest
from depths import depths
from collections import Counter

def codeLengthDistribution(codelengths):
    """Given a vector of codelengths, return the number of distinct codelengths.

>>> codeLengthDistribution([1,1,2,2,3,3])
[(1, 2), (2, 2), (3, 2)]
"""
    cnt = Counter()
    for c in codelengths:
        cnt[c] += 1 
    return cnt.most_common()

class codeLengthDistributionTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(codeLengthDistribution([]),[])
    def test_simpleVector(self):
        """Simple Vector."""
        self.assertEquals(codeLengthDistribution([1,1,2,2,3,3]),[(1,2),(2,2),(3,2)])


def statistics(W):
    """Given a list of weights, return 
- the EI signature, 
- the Alternation,
- the maximal codelength, and 
- the number of distinct codelenghts.
 
>>> statistics([1,1,4])
('EEIEI', 2, 2, 2)
"""

    if W==[]:
        return ("",0,0,0)
    elif len(W)==1:
        return ("E",1,0,1)
    W = sorted(W)
    i = 0
    trees = []
    signature = ""
    previous = 'E'
    alternation = 0
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            signature = signature + "E"
            previous = 'E'
        else:
            left = trees[0]
            trees = trees[1:]
            signature = signature + "I"
            if previous == 'E':
                alternation += 1
            previous = 'I'
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            signature = signature + "E"
            previous = 'E'
        else:
            right = trees[0]
            trees = trees[1:]
            signature = signature + "I"
            if previous == 'E':
                alternation += 1
            previous = 'I'
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    signature = signature + "I"
    if previous == 'E':
        alternation += 1
    codeLengths = depths(trees[0])
    maximalCodeLength = max(codeLengths)
    numberOfDistinctCodeLengths = len( codeLengthDistribution(codeLengths))
    return (signature,alternation,maximalCodeLength,numberOfDistinctCodeLengths)

class statisticsTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(statistics([]),("",0,0,0))
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(statistics([1]),("E",1,0,1))
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(statistics([1,1]),("EEI",1,1,1))
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(statistics([1,1,4]),("EEIEI",2,2,2))
    def test_exponentialSequence(self):
        """ExponentialSequence."""
        w = [1,2,4,8,16,32]
        (s,a,maxCodelength,nbDistinctCodeLengths) = statistics(w)
        self.assertEqual(s,"EEIEIEIEIEI")
        self.assertEqual(a,5)
        # self.assertEqual(codelengths,[5,5,4,3,2,1])
        self.assertEqual(maxCodelength,5)
        self.assertEqual(nbDistinctCodeLengths,5)


def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
