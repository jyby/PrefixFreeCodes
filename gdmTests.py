import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple
from vanLeeuwen import vanLeeuwen
from gdm import gdmCodeTree,gdm, ExternalNode, InternalNode, INITIALIZE, DOCK, MERGE, GROUP

class INITIALIZETest(unittest.TestCase):
    def test_AlphaEqualOneTwoWeights(self):
        """Alpha Equal One. Two Weights."""
        frequencies = PartiallySortedArray([10,10])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
    def test_AlphaEqualOneEighWeights(self):
        """Alpha Equal One. Various Weights."""
        frequencies = PartiallySortedArray([10]*8)
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),4)
        self.assertEqual(nbFrequenciesProcessed,8)
    def test_AlphaEqualOneNineWeights(self):
        """Alpha Equal One. Various Weights."""
        frequencies = PartiallySortedArray([10]*9)
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),5)
        self.assertEqual(nbFrequenciesProcessed,9)
    def test_AlphaEqualTwotEightWeights(self):
        """Alpha Equal One. Various Weights."""
        frequencies = PartiallySortedArray([10]*4+[21]*4)
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),2)
        self.assertEqual(nbFrequenciesProcessed,4)
    def test_ExponentialSequence(self):
        """Exponential Sequence."""
        frequencies = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)

class DOCKTest(unittest.TestCase):
    def test_AlphaEqualTwoConvergingToOneNode(self):
        """Alpha Equal Two. All last level docking to a single node."""
        frequencies = PartiallySortedArray([8]*4+[32])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(nbFrequenciesProcessed,4)
        self.assertEqual(len(nodes),1)
    def test_AlphaEqualTwoConvergingToTwoNodes(self):
        """Alpha Equal Two. Converging to four Nodes"""
        frequencies = PartiallySortedArray([8]*16+[32])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(nbFrequenciesProcessed,16)
        self.assertEqual(len(nodes),2)
    def test_ExponentialSequence(self):
        """Exponential Sequence."""
        frequencies = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        

class MERGETest(unittest.TestCase):
    def test_AlphaEqualTwoConvergingToOneNode(self):
        """Alpha Equal Two. All last level docking to a single node."""
        frequencies = PartiallySortedArray([8,9,10,11,12,13,14,15,17,21,25,29])
        nodes = [
            InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1)),
            InternalNode(frequencies,ExternalNode(frequencies,2),ExternalNode(frequencies,3)),
            InternalNode(frequencies,ExternalNode(frequencies,4),ExternalNode(frequencies,5)),
            InternalNode(frequencies,ExternalNode(frequencies,6),ExternalNode(frequencies,7))
        ]
        nbFrequenciesProcessed = 8
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(nbFrequenciesProcessed,12)
        self.assertEqual(len(nodes),4)
        # Check weights of nodes
        nodeWeightsAfterMerging = [8+9+17,10+11+21,12+13+25,14+15+29]
        for i in range(len(nodes)):
            self.assertEqual(nodes[i].weight(),nodeWeightsAfterMerging[i])
        # Check total Sum
        totalSum = 0
        for i in range(len(nodes)):
            totalSum += nodes[i].weight()
        self.assertEqual(totalSum,frequencies.rangeSum(0,len(frequencies)))
    def test_ExponentialSequence(self):
        """Exponential Sequence. (No need to dock ever.)"""
        frequencies = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        self.assertEqual(nodes[0].weight(),3)
        self.assertEqual(frequencies.select(2),4)        
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nodes[0].weight(),7)
        self.assertEqual(nbFrequenciesProcessed,3)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,4)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,5)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,6)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,7)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,8)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,9)
    def test_SuperExponentialSequence(self):
        """Super Exponential Sequence. (Still no need to dock?)"""
        frequencies = PartiallySortedArray([1,4,16,64,256])
        frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        self.assertEqual(nodes[0].weight(),5)
        self.assertEqual(frequencies.select(2),16)        
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,3)
        self.assertEqual(nodes[0].weight(),21)
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,4)
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,5)

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
        self.assertEqual(str(T),"(20,[None],[None])")
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
        """Alpha Equal Two. Single very small weight."""
        W = PartiallySortedArray([1]+[8]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[2]*4)

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """        
    # def test(self):
    #     """Generic test"""
    #     testPFCAlgorithm(gdm, "GDM")
    def testFourEqualWeights(self):
        """Four Equal Weights"""
        self.assertEqual(gdm([1,1,1,1]),[2,2,2,2])
    def testEightEqualWeights(self):
        """Eight Equal Weights"""
        self.assertEqual(gdm([1]*8),[3]*8)
    def test_ExponentialSequence(self):
        """Exponential Sequence. (No docking required ever)"""
        W = [1,2,4,8,16,32,64,128,256]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    # def test_ExponentialSequence(self):
    #     """Super Exponential Sequence. (Still no docking required ever)"""
    #     W = [1,4,16,64,256]
    #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    # def test_ExponentialSequenceWithLongSteps(self):
    #     """Exponential Sequence With Long Steps."""
    #     W = [1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256]
    #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    # def test_ExponentialSequenceWithVeryLongSteps(self):
    #     """Exponential Sequence With Very Long Steps."""
    #     W = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256]
    #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    # def test_SequenceRequiringMixing(self):
    #     """Sequence requiring Mixing."""
    #     W = [32,33,33,34,34,35,35,36,36,37,37,38,38,39,39,40,40,63,63,64,64,66,68,70,72,74,126]
    #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    # def test_AlphaEqualTwoWithMinorMixing(self):
    #     """Alpha Equal Two. Minor Mixing between Internal Nodes and External Nodes"""
    #     W = [1]*8+[7]*3
    #     L = gdm(W)
    #     self.assertEqual(sorted(L),[2]*3+[5]*8)
    # def test_AlphaEqualTwoTightMatch(self):
    #     """Alpha Equal Two. Tight match between Internal Node and External Node"""
    #     W = [1]*8+[8]*3
    #     L = gdm(W)
    #     self.assertEqual(sorted(L),[2]*3+[5]*8)
    # def test_AlphaEqualTwoLargeGap(self):
    #     """Alpha Equal Two. Large gab between the weight of the Internal Node and the weights of the largest external nodes."""
    #     W = [1]*8+[32]*3
    #     L = gdm(W)
    #     self.assertEqual(sorted(L),[2]*3+[5]*8)
    # def test_AlphaEqualThreeWithoutMixing(self):
    #     """Alpha Equal Three with no Mixing."""
    #     W = [1]*4+[4]*3+[16]*3
    #     L = gdm(W)
    #     self.assertEqual(sorted(L),[2]*3+[4]*3+[6]*4)



        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

