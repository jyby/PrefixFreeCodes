import unittest, doctest, copy
# from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple
from vanLeeuwen import vanLeeuwen
from gdm import INITIALIZE, GROUP, DOCK,  MERGE, WRAPUP, gdmCodeTree, gdm 
from codeTree import ExternalNode, InternalNode,  nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

class GeneralTest(unittest.TestCase):
    def test_INIT1(self):
        """Alpha Equal One. Two Weights."""
        frequencies = PartiallySortedArray([10,10])
        nbFrequenciesProcessed,nodes = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        
    def test_INIT2(self):
        """Alpha Equal One. Various Weights."""
        frequencies = PartiallySortedArray([10]*8)
        nbFrequenciesProcessed,nodes = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        
    def test_INIT3(self):
        """Exponential Sequence."""
        frequencies = PartiallySortedArray([10,20,40,80,160,320,640,1280,2560])
        nbFrequenciesProcessed,nodes = INITIALIZE(frequencies)
        self.assertEqual(len(nodes),1)
        self.assertEqual(nbFrequenciesProcessed,2)
        self.assertEqual(nodeListToString(nodes),'[(rangeSum(0,2),[select(0)],[select(1)])]')
        self.assertEqual(nodeListToWeightList(nodes),[30])
        
    def test_GROUP1(self):
        """Basic Example.
"""       
        frequencies = PartiallySortedArray([10,10,11,13,14,15,20,30])
        nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
        nbFrequenciesProcessed = 2
        nbFrequenciesProcessed,newNodes = GROUP(frequencies,nbFrequenciesProcessed,nodes[-1].weight())
        self.assertEqual(nodeListToString(newNodes),'[[select(2)], [select(3)], [select(4)], [select(5)], [select(6)]]')
        self.assertEqual(nodeListToWeightList(newNodes),[11, 13, 14, 15, 20])

    def test_DOCK1(self):
        """Number of nodes to dock equal to a power of three."""
        frequencies = PartiallySortedArray([8]*4+[32])
        nbFrequenciesProcessed = 0
        nbFrequenciesProcessed,nodes = GROUP(frequencies,nbFrequenciesProcessed,8)
        nodes = DOCK(frequencies,nodes,32)
        self.assertEqual(nodeListToString(nodes),'[(rangeSum(0,4),(rangeSum(0,2),[select(0)],[select(1)]),(16,[select(2)],[8]))]')
        self.assertEqual(nodeListToWeightList(nodes),[32])
    def test_DOCK2(self):
        """Number of nodes to dock is a power of two minus one."""
        frequencies = PartiallySortedArray([14,13,12,11,10,9,8,256])
        nbFrequenciesProcessed = 0
        nbFrequenciesProcessed,nodes = GROUP(frequencies,nbFrequenciesProcessed,15)
        self.assertEqual(nodeListToString(nodes),'[[select(0)], [select(1)], [select(2)], [select(3)], [select(4)], [select(5)], [select(6)]]')
        nodes = DOCK(frequencies,nodes,255)
        self.assertEqual(nodeListToString(nodes),'[(77,(31,[14],(17,[select(0)],[select(1)])),(46,(rangeSum(2,4),[select(2)],[select(3)]),(25,[select(4)],[select(5)])))]')
        self.assertEqual(nodeListToWeightList(nodes),[77])

        
    def test_MERGE1(self):
        """Interleaved union of two lists.
        """
        frequencies = PartiallySortedArray([8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,30])
        nbFrequenciesProcessed = 0
        nbFrequenciesProcessed,externalNodes = GROUP(frequencies,nbFrequenciesProcessed,16)
        internalNodes = []
        for i in range(4):
            internalNodes.append(InternalNode(frequencies,externalNodes[2*i],externalNodes[2*i+1]))
        self.assertEqual(nodeListToWeightList(internalNodes),[17, 21, 25, 29])
        nbFrequenciesProcessed,externalNodes = GROUP(frequencies,8,32)
        self.assertEqual(nodeListToWeightList(externalNodes),[16, 18, 20, 22, 24, 26, 28, 30])
        nodes = MERGE(internalNodes,externalNodes)
        self.assertEqual(nodeListToWeightList(nodes),[16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30])
        self.assertEqual(nodeListToString(nodes),'[[16], (17,[select(0)],[select(1)]), [18], [20], (21,[select(2)],[select(3)]), [22], [24], (25,[select(4)],[select(5)]), [26], [28], (29,[select(6)],[select(7)]), [30]]')
        
    def test_TREE1(self):
        """Empty input."""
        frequencies = PartiallySortedArray([])
        self.assertEqual(gdmCodeTree(frequencies),None)
        
    def test_TREE2(self):
        """Alpha Equal One. Singleton input."""
        frequencies = PartiallySortedArray([10])
        self.assertEqual(gdmCodeTree(frequencies),ExternalNode(frequencies,0))
        
    def test_TREE3(self):
        """Alpha Equal One. Two Weights."""
        W = PartiallySortedArray([10,10])
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(20,[select(0)],[select(1)])")
        L = T.depths()
        self.assertEqual(L,[1]*2)
        
    def test_TREE4(self):
        """Alpha Equal One. Four Equal Weights."""
        W = PartiallySortedArray([10]*4)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),'(40,(20,[select(0)],[select(1)]),(20,[10],[10]))')
        L = T.depths()
        self.assertEqual(L,[2]*4)
        
    def test_TREE5(self):
        """Alpha Equal One. Sixteen Equal Weights."""
        W = PartiallySortedArray([10]*16)
        T = gdmCodeTree(W)
        self.assertEqual(T.weight(),W.rangeSum(0,len(W)))        
        L = T.depths()
        self.assertEqual(L,[4]*16)
        
    def test_TREE6(self):
        """Alpha Equal One. Eight Similar Weights."""
        W = PartiallySortedArray([10,11,12,13,14,15,16,17])
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[3]*8)
        
    def test_TREE7(self):
        """Alpha Equal One. Three Equal Weights."""
        W = PartiallySortedArray([10]*3)
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(30,[10],(20,[select(0)],[select(1)]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
        
    def test_TREE8(self):
        """Alpha Equal One. Three Similar Weights."""
        W = PartiallySortedArray([12,11,10])
        T = gdmCodeTree(W)
        self.assertEqual(str(T),"(33,[12],(21,[select(0)],[select(1)]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
        
    def test_TREE9(self):
        """Alpha Equal Two. Single very small weight."""
        W = PartiallySortedArray([1]+[8]*3)
        T = gdmCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[2]*4)
        
    # def test_TREE10(self):
    #     """Exponential Sequence. (No need to dock ever.)"""
    #     frequencies = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
    #     frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
    #     self.assertEqual(nodeListToString(nodes),"[(3,[select(0)],[select(1)])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(7,(3,[select(0)],[select(1)]),[4])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(15,(7,(3,[select(0)],[select(1)]),[4]),[8])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(31,(15,(7,(3,[select(0)],[select(1)]),[4]),[8]),[16])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(63,(31,(15,(7,(3,[select(0)],[select(1)]),[4]),[8]),[16]),[32])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(127,(63,(31,(15,(7,(3,[select(0)],[select(1)]),[4]),[8]),[16]),[32]),[64])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(255,(127,(63,(31,(15,(7,(3,[select(0)],[select(1)]),[4]),[8]),[16]),[32]),[64]),[128])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(511,(255,(127,(63,(31,(15,(7,(3,[select(0)],[select(1)]),[4]),[8]),[16]),[32]),[64]),[128]),[256])]")
    
    # def test_TREE11(self):
    #     """Super Exponential Sequence. (Still no need to dock?)"""
    #     frequencies = PartiallySortedArray([1,4,16,64,256])
    #     frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
    #     self.assertEqual(nodeListToString(nodes),"[(5,[select(0)],[select(1)])]")
    #     frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(5,[select(0)],[select(1)])]")
    #     frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(21,(5,[select(0)],[select(1)]),[16])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(21,(5,[select(0)],[select(1)]),[16])]")
    #     frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(21,(5,[select(0)],[select(1)]),[16])]")
    #     frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(85,(21,(5,[select(0)],[select(1)]),[16]),[64])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(85,(21,(5,[select(0)],[select(1)]),[16]),[64])]")
    #     frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(85,(21,(5,[select(0)],[select(1)]),[16]),[64])]")
    #     frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(341,(85,(21,(5,[select(0)],[select(1)]),[16]),[64]),[256])]")
    #     frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    #     self.assertEqual(nodeListToString(nodes),"[(341,(85,(21,(5,[select(0)],[select(1)]),[16]),[64]),[256])]")
    #     frequencies,nodes = WRAPUP(frequencies,nodes)
    #     self.assertEqual(nodeListToString(nodes),"[(341,(85,(21,(5,[select(0)],[select(1)]),[16]),[64]),[256])]")

#     def testTREE12(self):
#         """Exponential Sequence with large steps."""
#         frequencies = PartiallySortedArray([1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256])
#         frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
#         self.assertEqual(nodeListToString(nodes),"[(2,[select(0)],[select(1)]), (rangeSum(2,4),[select(2)],[select(3)])]")
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)]))]")
#         frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])]")
#         frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4]))]")
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4]))]")
#         frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32])]")
#         frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(78,[32],(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32]))]")
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(78,[32],(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32]))]")
#         frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(206,(78,[32],(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32])),[128])]")
#         frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(334,[128],(206,(78,[32],(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32])),[128]))]")
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         self.assertEqual(nodeListToString(nodes),"[(334,[128],(206,(78,[32],(46,(14,[4],(10,(6,(2,[select(0)],[select(1)]),(4,[select(2)],[select(3)])),[4])),[32])),[128]))]")
#         # frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         # self.assertEqual(nodeListToString(nodes),"")
#         # frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#         # self.assertEqual(nodeListToString(nodes),"")
#         frequencies,nodes = WRAPUP(frequencies,nodes)
#         self.assertEqual(nodeListToString(nodes),"")

    # def test_TREE13(self):
    #     """Alpha Equal Three. Single very small weight."""
    #     frequencies = [1]+[8]*3+[32]*3
    #     W = PartiallySortedArray(frequencies)
    #     T = gdmCodeTree(W)
    #     L = T.depths()
    #     self.assertEqual(sorted(L),sorted(vanLeeuwen(frequencies)))

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """        
    # def test(self):
    #     """Generic test"""
    #     testPFCAlgorithm(gdm, "GDM")
    def testFourEqualWeights(self):
        """Four Equal Weights"""
        self.assertEqual(gdm([1,1,1,1]),[2,2,2,2])
#     def testEightEqualWeights(self):
#         """Eight Equal Weights"""
#         self.assertEqual(gdm([1]*8),[3]*8)
#     def test_ExponentialSequence(self):
#         """Exponential Sequence. (No docking required ever)"""
#         W = [1,2,4,8,16,32,64,128,256]
#         self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
#     def test_SuperExponentialSequence(self):
#         """Super Exponential Sequence. (Still no docking required ever)"""
#         W = [1,4,16,64,256]
#         self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
#     # def test_ExponentialSequenceWithLongSteps(self):
#     #     """Exponential Sequence With Long Steps."""
#     #     W = [1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256]
#     #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
#     # def test_ExponentialSequenceWithVeryLongSteps(self):
#     #     """Exponential Sequence With Very Long Steps."""
#     #     W = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256]
#     #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
#     # def test_SequenceRequiringMixing(self):
#     #     """Sequence requiring Mixing."""
#     #     W = [32,33,33,34,34,35,35,36,36,37,37,38,38,39,39,40,40,63,63,64,64,66,68,70,72,74,126]
#     #     self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
#     # def test_AlphaEqualTwoWithMinorMixing(self):
#     #     """Alpha Equal Two. Minor Mixing between Internal Nodes and External Nodes"""
#     #     W = [1]*8+[7]*3
#     #     L = gdm(W)
#     #     self.assertEqual(sorted(L),[2]*3+[5]*8)
#     # def test_AlphaEqualTwoTightMatch(self):
#     #     """Alpha Equal Two. Tight match between Internal Node and External Node"""
#     #     W = [1]*8+[8]*3
#     #     L = gdm(W)
#     #     self.assertEqual(sorted(L),[2]*3+[5]*8)
#     # def test_AlphaEqualTwoLargeGap(self):
#     #     """Alpha Equal Two. Large gab between the weight of the Internal Node and the weights of the largest external nodes."""
#     #     W = [1]*8+[32]*3
#     #     L = gdm(W)
#     #     self.assertEqual(sorted(L),[2]*3+[5]*8)
#     # def test_AlphaEqualThreeWithoutMixing(self):
#     #     """Alpha Equal Three with no Mixing."""
#     #     W = [1]*4+[4]*3+[16]*3
#     #     L = gdm(W)
#     #     self.assertEqual(sorted(L),[2]*3+[4]*3+[6]*4)
#     # def test_AlphaEqualFourWithoutMixing(self):
#     #     """Alpha Equal Three with no Mixing."""
#     #     W = [1]*4+[4]*3+[16]*3+[128]*3
#     #     L = gdm(W)
#     #     self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))



        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

