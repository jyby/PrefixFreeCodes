import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple
from vanLeeuwen import vanLeeuwen
from gdm import gdmCodeTree,gdm,EIAlternation,EISignature, ExternalNode, InternalNode


class gdmCodeTreeTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        frequencies = PartiallySortedArray([])
        self.assertEqual(gdmCodeTree(frequencies),None)
    def test_singleton(self):
        """Alpha Equal One. Singleton input."""
        frequencies = PartiallySortedArray([10])
        self.assertEqual(gdmCodeTree(frequencies),ExternalNode(frequencies,0))
    def test_twoWeights(self):
        """Alpha Equal One. Two Weights."""
        W = PartiallySortedArray([10,10])
        T = gdmCodeTree(W)
        # self.assertEqual(T,InternalNode(W,ExternalNode(W,0),ExternalNode(W,1)))
        L = T.depths()
        self.assertEqual(L,[1]*2)
    def test_fourEqualWeights(self):
        """Alpha Equal One. Four Equal Weights."""
        W = PartiallySortedArray([10]*4)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(40,(20,[None],[None]),(None,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[2]*4)
    def test_sixteenEqualWeights(self):
        """Alpha Equal One. Sixteen Equal Weights."""
        W = PartiallySortedArray([10]*16)
        T = gdmCodeTree(W)
        self.assertEqual(T.weight(),W.rangeSum(0,len(W)))        
        L = T.depths()
        self.assertEqual(L,[4]*16)
    def test_eightSimilarWeights(self):
        """Alpha Equal One. Eight Similar Weights."""
        W = PartiallySortedArray([10,11,12,13,14,15,16,17])
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[3]*8)
    def test_threeEqualWeights(self):
        """Alpha Equal One. Three Equal Weights."""
        W = PartiallySortedArray([10]*3)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(30,[10],(20,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
    def test_threeSimilarWeights(self):
        """Alpha Equal One. Three Similar Weights."""
        W = PartiallySortedArray([12,11,10])
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(33,[12],(21,[None],[None]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
    def test_AlphaEqualTwoSingleSmallWeight(self):
        """Alpha Equal Two. Single very small weight"""
        W = PartiallySortedArray([1]+[8]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[2]*4)
    def test_AlphaEqualWithMinorMixing(self):
        """Alpha Equal Two. Minor Mixing between Internal Nodes and External Nodes"""
        W = PartiallySortedArray([1]*8+[7]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualTwoTightMatch(self):
        """Alpha Equal Two. Tight match between Internal Node and External Node"""
        W = PartiallySortedArray([1]*8+[8]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualTwoLargeGap(self):
        """Alpha Equal Two. Large gab between the weight of the Internal Node and the weights of the largest external nodes."""
        W = PartiallySortedArray([1]*8+[32]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualThreeWithoutMixing(self):
        """Alpha Equal Three with no Mixing."""
        W = PartiallySortedArray([1]*4+[4]*3+[16]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(sorted(L),[2]*3+[4]*3+[6]*4)
    def test_ExponentialSequence(self):
        """Exponential Sequence."""
        W = [1,2,4,8,16,32,64,128,256]
        A = PartiallySortedArray(W)
        T = gdmCodeTree(A)
        L = T.depths()
        self.assertEqual(L,vanLeeuwen(W))
    def test_ExponentialSequenceWithLongSteps(self):
        """Exponential Sequence With Long Steps."""
        W = [1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256]
        A = PartiallySortedArray(W)
        T = gdmCodeTree(A)
        L = T.depths()
        self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))
    # def test_ExponentialSequenceWithVeryLongSteps(self):
    #     """Exponential Sequence With Very Long Steps."""
    #     W = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256]
    #     A = PartiallySortedArray(W)
    #     T = gdmCodeTree(A)
    #     L = T.depths()
    #     self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))
    # def test_SequenceRequiringMixing(self):
    #     """Sequence requiring Mixing."""
    #     W = [32,33,33,34,34,35,35,36,36,37,37,38,38,39,39,40,40,63,63,64,64,66,68,70,72,74,126]
    #     A = PartiallySortedArray(W)
    #     T = gdmCodeTree(A)
    #     L = T.depths()
    #     self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """        
    # def test(self):
    #     """Generic test"""
    #     testPFCAlgorithm(gdm, "GDM")
    def testFourEqualWeights(self):
        """Four Equal Weights"""
        self.assertEqual(gdm([1,1,1,1]),[2,2,2,2])
    # def testEightEqualWeights(self):
    #     """Eight Equal Weights"""
    #     self.assertEqual(gdm([1]*8),[3]*8)



        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

