import unittest, doctest, copy


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
        return [],[]
    if len(frequencies) < 3 :
        return frequencies,[1]*len(frequencies)    
    # Initialization
    externals = PartiallySortedArray(frequencies)
    nbExternalProcessed = 2;
    currentMinExternal = externals.select(3)
    currentMinInternal = externals.partialSum(2)
    internals = [(externals.partialSum(2),1,2)]
    # Loop
    while nbExternalProcessed < len(externals):
        # Group
        r = externals.rank(currentMinInternal)
        # Dock
        # Merge
    # Conclusion
        

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """
        
    def testSizeZeroInstance(self):
        """Test what happens on empty array.
        """
        self.assertEqual(gdm([]),([],[]))

    def testSizeOneInstance(self):
        """Test what happens on singleton.
        """
        self.assertEqual(gdm([1]),([1],[1]))

    def testSizeTwoInstance(self):
        """Test what happens on simple pair.
        """
        self.assertEqual(gdm([1,76]),([1,76],[1,1]))

    
    
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        
