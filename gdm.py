import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from depths import depths

class ExternalNode:
    """Given a partially sorted array W, and a poition in it, create the corresponding External node.
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
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.leftRange == other.leftRange and self.rightRange == other.rightRange and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)

class PureNode:
    """Given a partially sorted array W, and two indicators left and right describing a range in W,
    represent a pure node, which leaves have for weights exactly the range [left,right[ in sorted(W).
    The weight is computed only at request.

>>> W = PartiallySortedArray([150,140,130,120,110,32,16,10,10,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,1)
>>> z = PureNode(W,x,y)
>>> z2 = PureNode(W,x,y)
>>> print(z == z2)
True
>>> x3 = ExternalNode(W,0)
>>> y3 = ExternalNode(W,1)
>>> z3 = PureNode(W,x3,y3)
>>> print(z == z3)
True
>>> print(z.weight())
20
>>> print(x.weight())
10
>>> print(y.weight())
10
"""
    def __init__(self, partiallySortedArray, left, right):
        self.partiallySortedArray = partiallySortedArray
        self.left = left
        self.right = right
        assert left.rightRange == right.leftRange, "Error: The leaves of those nodes are not consecutive in the codeTree."
        self.leftRange = left.leftRange
        self.rightRange = right.rightRange
        if left.CachedValueOfWeight == None or right.CachedValueOfWeight == None:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = left.CachedValueOfWeight + right.CachedValueOfWeight
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.rangeSum(self.leftRange,self.rightRange)
        return self.CachedValueOfWeight
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.leftRange == other.leftRange and self.rightRange == other.rightRange and self.left == other.left and self.right == other.right and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)


class MixedNode:
    """Internal Node which leaves are separated by a pivot.

Its weight is computed at construction (mostly to simplify the complexity of analysis of the GDM algorithm),
but it could equally be computed recursively in a lazy variant of the algorithm (future work). 

Note: the implementation could be optimized (a lot) by computing the weight only when it is required (as in the commented code), but I don't know how to analize the resulting computing time yet.
I left it as it is so that the measures of the number of queries performed correspond to the state of the complexity analysis in the CPM 2016 paper.

>>> W = PartiallySortedArray([150,140,130,120,110,32,16])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,1)
>>> z = MixedNode(x,y)
>>> print(x.weight())
16
>>> print(y.weight())
32
>>> print(z.weight())
48
>>> z2 = MixedNode(x,y) 
>>> print(z == z2)
True
>>> x3 = ExternalNode(W,0)
>>> y3 = ExternalNode(W,1)
>>> z3 = MixedNode(x3,y3)
>>> print(z==z3)
True
"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.CachedValueOfWeight =  left.weight() + right.weight()
        # self.CachedValueOfWeight =  None
    def weight(self):
        # if self.CachedValueOfWeight == None:
        #     self.CachedValueOfWeight =   (self.left).weight() + (self.right).weight()
        return self.CachedValueOfWeight
    def __cmp__(self,other):
        return self.left == other.left and self.right == other.right and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    
        
    
def gdmCodeTree(frequencies):
    """Given a sorted list of weights, return a code tree of minimal
    redundancy according to the GDM algorithm.

    """
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    elif len(frequencies)==2:
        return PureNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))
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
        frequencies = []
        self.assertEqual(gdmCodeTree(frequencies),None)
    def test_singleton(self):
        """Singleton input."""
        frequencies = [10]
        self.assertEqual(gdmCodeTree(frequencies),ExternalNode(frequencies,0))
    def test_twoWeights(self):
        """Two Weights."""
        W = [10,10]
        self.assertEqual(gdmCodeTree(W),PureNode(W,ExternalNode(W,0),ExternalNode(W,1)))
    # def test_fourEqualWeights(self):
    #     """Four Equal Weights."""
    #     self.assertEqual(gdmCodeTree([10,10,10,10]),[40,[20,0,1],[20,2,3]])
    # def test_threeWeights(self):
    #     """Three Weights."""
    #     self.assertEqual(gdmCodeTree([10,10,40]),[60,[20,0,1],[30,2]])
    
    
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
            
        

