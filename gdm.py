import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayGreedyImplementation import PartiallySortedArray
from depths import depths


def EISignature(W):
    """Given a list of weights, return the EI signature of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EISignature([1,1,4])
    "EEIEI"
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

class EISignature(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EISignature([]),[])
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EISignature([1]),"E")
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EISignature([1,1]),"EEI")
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EISignature([1,1,4]),"EEIEI")


def gdm(frequencies):
    """Implementation in Python of the "Group Dock and Merge" algorithm.

       This algorithm is supposed to compute optimal prefix free codes in time o(n lg n) for various classes of instances.  

       It receives as input an array of integer frequencies of symbols.
       It returns
          - an array partially sorting those frequencies and
          - an array of the same size containing the associated code lengths forming an optimal prefix free code for those frequencies.

    """
    # Degenerated cases
    if len(frequencies) == 0 :
        return []
    elif len(frequencies)==1:
        return [0]
    elif len(frequencies)==2:
        return [1,1]
    # Initialization
    externals = PartiallySortedArray(frequencies)
    nbExternalProcessed = 2;
    currentMinExternal = externals.select(3)
    currentMinInternal = externals.partialSum(2)
    internals = [(externals.partialSum(2),1,2)]
    # Loop
    # while nbExternalProcessed < len(externals):
        # Group
        # r = externals.rank(currentMinInternal)
        # Dock
        # Merge
    # Conclusion
    return []

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """
        
    def test(self):
        """Generic test"""
        testPFCAlgorithm(gdm, "GDM")
    # def testSixWeights(self):
    #     """Six Weights"""
    #     self.assertEqual(compressByRunLengths(gdm([1,1,1,1,1,1])),[(3,4),(2,2)])
    
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

