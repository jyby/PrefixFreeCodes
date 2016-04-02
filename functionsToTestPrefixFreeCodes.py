import unittest, doctest, math

def expandRunLengths(R):
    """Given an unsorted list R of pairs (x,n), 
    returns a list of integer where each pair (x,n) is represented by a sequence of n copies of x.

    >>> expandRunLengths([(2,3),(3,4),(1,2)])
    [2, 2, 2, 3, 3, 3, 3, 1, 1]

    """
    L = []
    for (x,n) in R:
        for i in range(0,n):
            L.append(x)
    return L

def compressByRunLengths(L):
    """Given an unsorted list $L$ of integers, compress it into a list
    of pairs (x,n) such that $x$ occurs $n$ times in $L$.
    Makes tests much easier to write.

    """
    if L == []:
        return []
    elif len(L) == 1:
        return [(L[0],1)]
    L.sort(reverse=True)
    output = []
    i = 0
    while i < len(L):
        value = L[i]
        runLength = 1
        i+=1
        while i < len(L) and L[i] == value:
            runLength += 1
            i += 1
        output.append((value,runLength))
    return output
class TestCompressByRunLengths(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(compressByRunLengths([]),[])
    def test_singleton(self):
        """Singleton."""
        self.assertEqual(compressByRunLengths([0]),[(0,1)])
    def test_fourEqual(self):
        """Four equal values"""
        self.assertEqual(compressByRunLengths([1,1,1,1]),[(1,4)])
    def test_twoRuns(self):
        """Two Runs"""
        self.assertEqual(compressByRunLengths([2,2,2,1,1,1,1]),[(2,3),(1,4)])
    def test_threeRuns(self):
        """Three Runs"""
        self.assertEqual(compressByRunLengths([3,2,2,2,1]),[(3,1),(2,3),(1,1)])
        

def testPFCAlgorithm(prefixFreeCodeAlgorithm, nameAlgorithm=""):
    for name, W, answers in examplesOfWeights:
        codeLengths = prefixFreeCodeAlgorithm(W)
        compressedCodeLenghts = compressByRunLengths(codeLengths)
        assert respectsKraftInequality(compressedCodeLenghts), "Algorithm "+nameAlgorithm+" returns non prefix code on "+name+"."
        # assert codeIsPrefixFreeCodeMinimal(L,W), "Algorithm "+nameAlgorithm+" returns non minimal prefix code on "+name+"."
        # assert sorted(L,reverse=True) in answers,"Algorithm "+nameAlgorithm+" returns unknown code "+str(L)+"\n-- on instance '"+name+"'"+"\n-- (which is not in "+str(answers)+"."

examplesOfWeights = [
    ("Empty",
     [],
     [[]]),
    ("Pair",
     [1,1],
     [[(1,2)]]),
    ("Four equal Weights",
     [1,1,1,1],
     [[(2,4)]]),
    ("example from Huffman's article", 
     [1,3,4,4,4,4,6,6,10,10,10,18,20],
     [[(5,6),(4,3),(3,3),(2,1)]]),
    ("example from Wikipedia",
     [10,15,16,29,30],
     [[(3,2),(2,3)]]),
    ("example from Moffat and Turpin's article", 
     [1,1,1,1,1,2,2,2,2,3,3,6],
     [[(5,4),(4,4),(3,3),(2,1)], # There are more than one opt solution!
      [(5,2),(4,7),(3,2),(2,1)]]),
    ("example from Milidiu et al Fig.8a", 
     [2,2,2,3,3,3,3,4,4,5,7,7,9,11], 
     [[(5,4),(4,6),(3,4)]]),
    # ("example from Belal and Elmasry Fig.1", 
    #  [2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,5,5,5,5,5,9,9,9,9,9],
    #  []),
    ("example with $28$ ones",
     [1]*28,
     [[(5,24),(4,4)]]
     ),
    ("example with all $8$ weights within a factor of $2$", 
     [248,249,250,251,252,253,254,255],
     [[(3,8)]]),
    ("example with $6$ weights within a factor of $2$", 
     [250,251,252,253,254,255], 
     [[(3,4),(2,2)]]),
    ("example with weights from $2$ distinct classes of power of two, each ending at same level", 
     [4,5,6,7,253,254,255], 
     [[(4,4),(2,3)]]),
    ("example with weights from $2$ distinct classes of power of two, each ending at two levels", 
     [3,4,5,6,7,252,253,254,255], 
     [[(6,2),(5,3),(3,1),(2,3)]]),
    ("example with weights from $2$ distinct classes of power of two, smaller class results in two nodes above", 
     [1]*32+[14,15], 
     [[(6,32),(2,2)]]),
    ("example with weights from $2$ distinct classes of power of two, values mingle", 
     [1]*28+[10,15], 
     [[(6,24),(5,4),(2,2)]]),
    ("example with two log classes, not a power of two at top level, values do not mingle", 
     [1]*28+[17,17,17], 
     [[(7,24),(6,4),(2,3)]]),
    ("example with two log classes, not a power of two at top level, values do mingle", 
     [1]*28+[10,13,15], 
     [[(7,8),(6,20),(3,1),(2,2)]])
    ]

def respectsKraftInequality(L):
    """Checks if the given array $L$ of pairs $(codeLenght_i,nbWeights_i)$ 
    corresponds to a prefix free code by checking Kraft's inequality, i.e.
    $\sum_i nbWeights_i 2^{-codelenght_i} \leq 1$.
    """ 
    return KraftSum(L) <= 1 ;
def KraftSum(L):
    """Computes the Kraft sum of the prefix free code described by an
    array $L$ of pairs $(codeLenght_i,nbWeights_i)$ i.e.  
    $\sum_i nbWeights_i 2^{-codelenght_i}$.
    """
    if len(L)==0: 
        return 0
    terms = map( lambda x: x[1] * math.pow(2,-x[0]), L)
    return sum(terms)
class TestKraftSum(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(KraftSum([]),0)
    def test_singleton(self):
        """Singleton with one single symbol."""
        self.assertEqual(KraftSum([(0,1)]),1)
    def test_simpleCode(self):
        """Simple Code with code lenghts [1,2,2]."""
        self.assertEqual(KraftSum([(1,1),(2,2)]),1)
    def test_fourEqual(self):
        """Four equal weights"""
        self.assertEqual(KraftSum([(2,4)]),1)
    def test_HuffmanExample(self):
        """Example from Huffman's article"""
        self.assertEqual(KraftSum([(5,6),(4,3),(3,3),(2,1)]),1)
    def test_MoffatTurpinExample(self):
        """Example from Moffat and Turpin's article"""
        self.assertEqual(KraftSum([(5,4),(4,4),(3,3),(2,1)]),1)


def codeIsPrefixFreeCodeMinimal(L,W):
    """Checks if the prefix free code described by an array $L$ of
    pairs $(codeLenght_i,nbWeights_i)$ is minimal for weights $W$, by
    comparing the lenght of a code encoded with $L$ with the entropy
    of $W$.
    """
    return compressedTextLength(L,W) <= NTimesEntropy(W)+len(W)

def NTimesEntropy(W):
    """Returns N times the entropy, rounded to the next integer, as computed by
       $\lceil \sum_{i=1}^N W[i]/\sum(W) \log (sum(W) / W[i]) \rceil$.
       """
    if len(W)==0: 
        return 0
    assert min(W)>0
    sumWeights = sum(W)    
    terms = map( lambda x: x * math.log(x,2), W )
    return math.ceil(sumWeights * math.log(sumWeights,2) - sum(terms)) 
class TestNTimesEntropy(unittest.TestCase):
    def test_empty(self):
        """Empty input"""
        self.assertEqual(NTimesEntropy([]),0)
    def test_singleton(self):
        """Singleton"""
        self.assertEqual(NTimesEntropy([1]),0)
    def test_pair(self):
        """Pair"""
        self.assertEqual(NTimesEntropy([1,1]),2)
    def test_fourEqual(self):
        """Four equal weights"""
        self.assertEqual(NTimesEntropy([1,1,1,1]),8)
    def test_HuffmanExample(self):
        """Example from Huffman's article"""
        self.assertEqual(NTimesEntropy([1,3,4,4,4,4,6,6,10,10,10,18,20]),336)
    def test_MoffatTurpinExample(self):
        """Example from Moffat and Turpin's article"""
        self.assertEqual(NTimesEntropy([1,1,1,1,1,2,2,2,2,3,3,6]),84)

def compressedTextLength(L,W):
    """Computes the lengths of a text which frequencies are given by
    an array $W$, when it is compressed by a prefix free code
    described by an array $L$ of pairs $(codeLenght_i,nbWeights_i)$.
    """
    compressedTextLength = 0
    Ls = sorted(L, reverse=True)
    Ws = sorted(W)
    for (l,n) in Ls:
        compressedTextLength += l*sum(Ws[0:n])
        Ws = Ws[n:]
    return compressedTextLength
class TestcompressedTextLength(unittest.TestCase):
    def test_empty(self):
        """Empty input"""
        self.assertEqual(compressedTextLength([],[]),0)
    def test_pair(self):
        """Pair of symbols, arbitrary text"""
        self.assertEqual(compressedTextLength([(1,2)],[1,1]),2)
    def test_fourEqual(self):
        """Four equal weights"""
        self.assertEqual(compressedTextLength([(2,4)],[1,1,1,1]),8)
    def test_HuffmanExample(self):
        """Example from Huffman's article (compares with value compared by hand)"""
        self.assertEqual(compressedTextLength([(5,6),(4,3),(3,3),(2,1)],[1,3,4,4,4,4,6,6,10,10,10,18,20]),342)
    def test_MoffatTurpinExample(self):
        """Example from Moffat and Turpin's article (compares with entropy value)"""
        self.assertEqual(compressedTextLength([(5,4),(4,4),(3,3),(2,1)],[1,1,1,1,1,2,2,2,2,3,3,6]),84)


def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()

