import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray

class ExternalNode:
    """Given a partially sorted array W, and a position in it, create the corresponding External node.
    The weight is computed only at request by performing a select query in the partiallySortedArray.

>>> W = PartiallySortedArray([150,140,130,120,110,32,16,10,10,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,0)
>>> z = ExternalNode(W,1)
>>> print(x == y)
True
>>> print(x == z)
False

"""
    def __init__(self, partiallySortedArray, position):
        self.partiallySortedArray = partiallySortedArray
        self.leftRange = position
        self.rightRange = position+1
        self.CachedValueOfWeight = None
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.select(self.leftRange)
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.
        """
        return [depth]
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.leftRange == other.leftRange and self.rightRange == other.rightRange and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    def __str__(self):
        return "["+str(self.CachedValueOfWeight)+"]"


class InternalNode:
    """Given a partially sorted array W and two pointers, builds a node of the codeTree for the GDM algorithm.  The weight is computed only at request.

>>> W = PartiallySortedArray([100,100,50,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,1)
>>> z = InternalNode(W,x,y)
>>> print(W.totalNbOfQueriesPerformed())
0
>>> print(x.weight())
10
>>> print(y.weight())
10
>>> print(z.weight())
20
>>> x2 = ExternalNode(W,3)
>>> y2 = ExternalNode(W,4)
>>> z2 = InternalNode(W,x2,y2)
>>> print(z2.weight())
200
>>> z3 = InternalNode(W,z,z2)
>>> print(z3.weight())
220
>>> print(z3.depths())
[2, 2, 2, 2]
"""
    def __init__(self, partiallySortedArray, left, right):
        self.partiallySortedArray = partiallySortedArray
        self.left = left
        self.right = right
        if(left.rightRange == right.leftRange and left.leftRange != None):
            self.leftRange = left.leftRange
            self.rightRange = right.rightRange
        else:
            self.leftRange = None
            self.rightRange = None
        if left.CachedValueOfWeight == None or right.CachedValueOfWeight == None:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = left.CachedValueOfWeight + right.CachedValueOfWeight
    def weight(self):
        if self.CachedValueOfWeight == None:
            if self.leftRange != None and self.rightRange != None:
                self.CachedValueOfWeight = self.partiallySortedArray.rangeSum(self.leftRange,self.rightRange)
            else:
                self.CachedValueOfWeight = self.left.weight() + self.right.weight()
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.
        """
        depthsOnLeft =  self.left.depths(depth+1)
        depthsOnRight = self.right.depths(depth+1)
        return depthsOnLeft+depthsOnRight
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.leftRange == other.leftRange and self.rightRange == other.rightRange and self.left == other.left and self.right == other.right and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    def __str__(self):
        return "("+str(self.CachedValueOfWeight)+","+str(self.left)+","+str(self.right)+")"
    
def gdmCodeTree(frequencies):
    """Given a partially sorted list of weights, return a code tree of minimal
    redundancy according to the GDM algorithm.

    """
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    elif len(frequencies)==2:
        return InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))
    # Phase "Initialization"
    nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))] 
    nbFrequenciesProcessed = 2
    # while nbFrequenciesProcessed < len(frequencies):
    # GROUP weights of similar weights: 
    r = frequencies.rank(nodes[0].weight())
    if (r-nbFrequenciesProcessed) % 2 == 1:
        nodes = [ExternalNode(frequencies,r-1)]+nodes
    for i in range((r-nbFrequenciesProcessed)//2):
        left = ExternalNode(frequencies,nbFrequenciesProcessed+2*i)
        right = ExternalNode(frequencies,nbFrequenciesProcessed+2*i+1)        
        nodes.append(InternalNode(frequencies,left,right))
    nbFrequenciesProcessed += r
    # DOCK those weights to the level of the next External node
    # while nodes[-1].weight() < frequencies.select(nbFrequenciesProcessed):
    #     for i in range(len(nodes)//2):
    #         nodes.append(InternalNode(frequencies,nodes[i],nodes[i+1]))
    # MERGE the internal nodes with the external nodes of similar weights
    # (to be implemented later by a binary search in the list of nodes)
    # WRAP-UP when there are only internal nodes left.
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes[-1].weight()
        for i in range( len(nodes) // 2):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    nodes[0].weight()
    return nodes[0]
class gdmCodeTreeTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        frequencies = PartiallySortedArray([])
        self.assertEqual(gdmCodeTree(frequencies),None)
    def test_singleton(self):
        """Singleton input."""
        frequencies = PartiallySortedArray([10])
        self.assertEqual(gdmCodeTree(frequencies),ExternalNode(frequencies,0))
    def test_twoWeights(self):
        """Two Weights."""
        W = PartiallySortedArray([10,10])
        T = gdmCodeTree(W)
        self.assertEqual(T,InternalNode(W,ExternalNode(W,0),ExternalNode(W,1)))
        L = T.depths()
        self.assertEqual(L,[1]*2)
    def test_fourEqualWeights(self):
        """Four Equal Weights."""
        W = PartiallySortedArray([10]*4)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(40,(20,[None],[None]),(None,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[2]*4)
    def test_sixteenEqualWeights(self):
        """Sixteen Equal Weights."""
        W = PartiallySortedArray([10]*16)
        T = gdmCodeTree(W)
        self.assertEqual(T.weight(),W.rangeSum(0,len(W)))        
        L = T.depths()
        self.assertEqual(L,[4]*16)
    def test_eightSimilarWeights(self):
        """Eight Similar Weights."""
        W = PartiallySortedArray([10,11,12,13,14,15,16,17])
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[3]*8)
    def test_threeEqualWeights(self):
        """Three Equal Weights."""
        W = PartiallySortedArray([10]*3)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(30,[10],(20,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
    def test_threeSimilarWeights(self):
        """Three Similar Weights."""
        W = PartiallySortedArray([12,11,10])
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(33,[12],(21,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
    
    
# def gdm(frequencies):
#     """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

#     """
#     # Degenerated cases
#     if len(frequencies) == 0 :
#         return []
#     elif len(frequencies)==1:
#         return [0]
#     elif len(frequencies)==2:
#         return [1,1]
#     codeTree = gdmCodeTree(frequencies)
#     codeLengths = depths(codeTree)
#     return codeLengths
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
            
        

