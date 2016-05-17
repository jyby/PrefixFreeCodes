import unittest,doctest
from depths import depths

def statistics(W):
    """Given a list of weights, return 
- the EI signature, 
- the Alternation,
- the vector of codelengths.
 
>>> statistics([1,1,4])
('EEIEI', 2, [2,2,1])
"""

    if W==[]:
        return ("",0)
    elif len(W)==1:
        return ("E",1)
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
    codeLengths = trees.depth()
    return (signature,alternation,codeLengths)

class statisticsTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(statistics([]),("",0))
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(statistics([1]),("E",1))
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(statistics([1,1]),("EEI",1))
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(statistics([1,1,4]),("EEIEI",2))
    def test_exponentialSequence(self):
        """ExponentialSequence."""
        w = [1,2,4,8,16,32]
        (s,a) = statistics(w)
        self.assertEqual(s,"EEIEIEIEIEI")
        self.assertEqual(a,5)





def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
