import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayGreedyImplementation import PartiallySortedArray
from depths import depths

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
            
        

