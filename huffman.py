import unittest, doctest, copy
import heapq

def extractDepths(tree,depths,depth=0):
    """Simple recursive function listing the leaves and their depths).

        >>> depths = []
        >>> extractDepths([1],[],0)
    """
    if len(tree) == 1:
        depths.append(depth)
    elif len(tree) == 3:
        (weight,childL,childR) = tree
        extractDepths(childL,leaves,depth+1)
        extractDepths(childR,leaves,depth+1)
    
def huffman(frequencies):
    """Implementation in Python of the "Huffman" algorithm.

       This is an heap-based implementation of the method originally described by Huffman in 1952.

       It receives as input an array of integer frequencies of symbols.
       It returns
          - an array partially sorting those frequencies and
          - an array of the same size containing the associated code lengths forming an optimal prefix free code for those frequencies.

    """
    if len(frequencies) == 0 :
        return [],[]
    if len(frequencies) < 3 :
        return frequencies,[1]*len(frequencies)
    trees = list(frequencies)
    heapq.heapify(trees)
    while len(trees) > 1:
        childR = heapq.heappop(trees)
        childL = heapq.heappop(trees)
        parent = [childL[0]+childR[0], childL, childR]
        heapq.heappush(trees, parent)
    depths = []     
    extractDepths(trees[0],depths,depth=0)
    return(frequencies,depths)
    
class HuffmanTest(unittest.TestCase):
    """Basic tests for the Huffman algorithm computing optimal prefix free codes.

    """
                
    def testExtractLeaves(self):
        """Test Extract Leaves on single node.
        """
        leaves = []
        extractDepths([1],leaves,0)
        self.assertEqual(leaves,[0])

    def testSizeZeroInstance(self):
        """Test what happens on empty array.
        """
        self.assertEqual(huffman([]),([],[]))

    def testSizeOneInstance(self):
        """Test what happens on singleton.
        """
        self.assertEqual(huffman([1]),([1],[1]))

    def testSizeTwoInstance(self):
        """Test what happens on simple pair.
        """
        self.assertEqual(huffman([1,76]),([1,76],[1,1]))

    
    
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

