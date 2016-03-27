import unittest, doctest, copy


def gdm(frequencies):
    """Implementation in Python of the "Group Dock and Merge" algorithm.

       This algorithm is supposed to compute optimal prefix free codes in time o(n lg n) for various classes of instances.  

       It receives as input an array of integer frequencies of symbols.
       It returns
          - an array partially sorting those frequencies and
          - an array of the same size containing the associated code lengths forming an optimal prefix free code for those frequencies.

    """
    if len(frequencies) == 0 :
        return [],[]


class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """
        
    def testTrivialInstance(self):
        """Test what happens on an empty Instance.
        """
        self.assertEqual(gdm([]),([],[]))

    
    
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

