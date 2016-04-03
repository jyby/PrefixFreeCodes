import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayGreedyImplementation import PartiallySortedArray
from depths import depths

def gdmCodeTree(frequencies):
    """Given a sorted list of weights, return a code tree of minimal
    redundancy according to the GDM algorithm.

    """
    if len(frequencies) == 0 :
        return []
    elif len(frequencies)==1:
        return [0]
    elif len(frequencies)==2:
        return [frequencies[0]+frequencies[1],0,1]
    # Phase "Initialization" 
    externals = PartiallySortedArray(frequencies)
    internals = []
    currentMinExternal = externals.select(2)
    currentMinInternal = externals.rangeSum(0,1)
    internals.append([externals.rangeSum(0,1),0,1])
    nbExternalsPaired = 2
    # Phase "Group" 
    r = externals.rank(currentMinInternal)
    # Phase "Dock"
    while nbExternalsPaired < len(externals):
        internals.append([externals.rangeSum(nbExternalsPaired,nbExternalsPaired+1),nbExternalsPaired,nbExternalsPaired+1])
        nbExternalsPaired += 2
    # Phase "Conclusion" 
    while len(internals) > 1:
        left = internals[0]
        right = internals[1]
        internals= internals[2:]
        parent = [left[0] + right[0], left,right]
        internals.append(parent)
    return internals[0]
class gdmCodeTreeTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(gdmCodeTree([]),[])
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(gdmCodeTree([10]),[0])
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(gdmCodeTree([10,10]),[20,0,1])
    def test_fourEqualWeights(self):
        """Four Equal Weights."""
        self.assertEqual(gdmCodeTree([10,10,10,10]),[40,[20,0,1],[20,2,3]])
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(gdmCodeTree([10,10,40]),[60,[20,0,1],[30,2]])
    
    
def gdm(frequencies):
    """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

    """
    # Degenerated cases
    if len(frequencies) == 0 :
        return []
    elif len(frequencies)==1:
        return [0]
    elif len(frequencies)==2:
        return [1,1]
    codeTree = gdmCodeTree(frequencies)
    codeLengths = depths(codeTree)
    return codeLengths
# class GDMTest(unittest.TestCase):
#     """Basic tests for the GDM algorithm computing optimal prefix free codes.

#     """
        
#     def test(self):
#         """Generic test"""
#         testPFCAlgorithm(gdm, "GDM")
#     def testFourEqualWeights(self):
#         """Four Equal Weights"""
#         self.assertEqual(gdm([1,1,1,1]),[2,2,2,2])
#     def testEightEqualWeights(self):
#         """Eight Equal Weights"""
#         self.assertEqual(gdm([1]*8),[3]*8)

def EISignature(W):
    """Given a list of weights, return the EI signature of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EISignature([1,1,4])
    'EEIEI'
   """

    if W==[]:
        return ""
    elif len(W)==1:
        return "E"
    W = sorted(W)
    i = 0
    trees = []
    signature = ""
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            signature = signature + "E"
        else:
            left = trees[0]
            trees = trees[1:]
            signature = signature + "I"
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            signature = signature + "E"
        else:
            right = trees[0]
            trees = trees[1:]
            signature = signature + "I"
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    signature = signature + "I"
    return signature
class EISignatureTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EISignature([]),"")
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EISignature([1]),"E")
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EISignature([1,1]),"EEI")
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EISignature([1,1,4]),"EEIEI")

def EIAlternation(W):
    """Given a list of weights, return the EI signature of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EIAlternation([1,1,4])
    2
   """

    if W==[]:
        return 0
    elif len(W)==1:
        return 1
        W = sorted(W)
    i = 0
    trees = []
    previous = 'E'
    alternation = 0
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            previous = 'E'
        else:
            left = trees[0]
            trees = trees[1:]
            if previous == 'E':
                alternation += 1
            previous = 'I'
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            previous = 'E'
        else:
            right = trees[0]
            trees = trees[1:]
            if previous == 'E':
                alternation += 1
            previous = 'I'
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    if previous == 'E':
        alternation += 1
    return alternation    
class EIAlternationTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EIAlternation([]),0)
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EIAlternation([1]),1)
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EIAlternation([1,1]),1)
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EIAlternation([1,1,4]),2)


        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

