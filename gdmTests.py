import unittest, doctest
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from vanLeeuwen import vanLeeuwen
from gdm import INITIALIZE, GroupExternals, DockInternals, MixInternalWithExternal, WRAPUP, gdmCodeTree, gdm 
from codeTree import ExternalNode, InternalNode,  nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

class GeneralTest(unittest.TestCase):
    def test_INIT1(self):
        """Alpha Equal One. Two Weights."""
        frequencies = PartiallySortedArray([10,10])
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToString(internals),'[(rangeSum(0,2),[select(0)],[select(1)])]')
        self.assertEqual(nodeListToWeightList(internals),[20])
        self.assertEqual(nodeListToWeightList(externals),[])
        
    def test_INIT2(self):
        """Alpha Equal One. Various Weights."""
        frequencies = PartiallySortedArray([10]*8)
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToString(internals),'[(rangeSum(0,2),[select(0)],[select(1)])]')
        self.assertEqual(nodeListToWeightList(internals),[20])
        self.assertEqual(nodeListToWeightList(externals),[10]*6)
        
    def test_INIT3(self):
        """Exponential Sequence."""
        frequencies = PartiallySortedArray([10,20,40,80,160,320,640,1280,2560])
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToString(internals),'[(rangeSum(0,2),[select(0)],[select(1)])]')
        self.assertEqual(nodeListToWeightList(internals),[30])
        self.assertEqual(nodeListToWeightList(externals),[40,80,160,320,640,1280,2560])
        
    def test_GroupExternals1(self):
        """Basic Example.
"""       
        frequencies = PartiallySortedArray([10,10,11,13,14,15,20,30])
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToWeightList(internals),[20])
        self.assertEqual(nodeListToWeightList(externals),[11,13,14,15,20,30])
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[24, 29, 40])
        self.assertEqual(nodeListToWeightList(externals),[30])

    def test_DockInternals1(self):
        """Number of nodes to dock equal to a power of three."""
        frequencies = PartiallySortedArray([8]*4+[32])
        frequencies,externals,internals = INITIALIZE(frequencies)
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[32])
        self.assertEqual(nodeListToWeightList(externals),[32])

    def test_DockInternals2(self):
        """Number of nodes to dock is a power of two minus one."""
        frequencies = PartiallySortedArray([14,13,12,11,10,9,8,256])
        frequencies,externals,internals = INITIALIZE(frequencies)
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[77])
        self.assertEqual(nodeListToWeightList(externals),[256])

    def test_Mix1(self):
        """All weights equal."""
        frequencies = PartiallySortedArray([8]*8)
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToWeightList(internals),[16])
        self.assertEqual(nodeListToWeightList(externals),[8]*6)
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[16]*4)
        self.assertEqual(nodeListToWeightList(externals),[])
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[16]*4)
        self.assertEqual(nodeListToWeightList(externals),[])
        frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[16]*4)
        self.assertEqual(nodeListToWeightList(externals),[])
        
    def test_Mix2(self):
        """Two Levels."""
        frequencies = PartiallySortedArray([8]*8+[255])
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToWeightList(internals),[16])
        self.assertEqual(nodeListToWeightList(externals),[8]*6+[255])
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[16]*4)
        self.assertEqual(nodeListToWeightList(externals),[255])
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[64])
        self.assertEqual(nodeListToWeightList(externals),[255])
        frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[319])
        self.assertEqual(nodeListToWeightList(externals),[])

    def test_Mix3(self):
        """Three Levels."""
        frequencies = PartiallySortedArray([8]*8+[255,1024])
        frequencies,externals,internals = INITIALIZE(frequencies)
        self.assertEqual(nodeListToWeightList(internals),[16])
        self.assertEqual(nodeListToWeightList(externals),[8]*6+[255,1024])
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[16]*4)
        self.assertEqual(nodeListToWeightList(externals),[255,1024])
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[64])
        self.assertEqual(nodeListToWeightList(externals),[255,1024])
        frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[319])
        self.assertEqual(nodeListToWeightList(externals),[1024])
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[319])
        self.assertEqual(nodeListToWeightList(externals),[1024])
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[319])
        self.assertEqual(nodeListToWeightList(externals),[1024])
        frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
        self.assertEqual(nodeListToWeightList(internals),[1343])
        self.assertEqual(nodeListToWeightList(externals),[])


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
        self.assertEqual(T.toStringWithAllWeightsCalculated(),'(40,(20,[10],[10]),(20,[10],[10]))')
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
        
    def test_TREE10(self):
        """Exponential Sequence."""
        W = PartiallySortedArray([1,2,4])
        T = gdmCodeTree(W)
        self.assertEqual(T.toStringWithAllWeightsCalculated(),'(7,(3,[1],[2]),[4])')
        L = T.depths()
        self.assertEqual(sorted(L),[1,2,2])

    def test_TREE12(self):
        """Exponential Sequence."""
        W = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
        T = gdmCodeTree(W)
        self.assertEqual(T.toStringWithAllWeightsCalculated(),'(511,(255,(127,(63,(31,(15,(7,(3,[1],[2]),[4]),[8]),[16]),[32]),[64]),[128]),[256])')
        L = T.depths()
        self.assertEqual(sorted(L),[1,2,3,4,5,6,7,8,8])

    

class GDMTest(unittest.TestCase):
    """Basic tests for the GDM algorithm computing optimal prefix free codes.

    """        
    def test(self):
        """Generic test"""
        testPFCAlgorithm(gdm, "GDM")
    def test1(self):
        """Four Equal Weights"""
        self.assertEqual(gdm([1,1,1,1]),[2,2,2,2])
    def test2(self):
        """Eight Equal Weights"""
        self.assertEqual(gdm([1]*8),[3]*8)
    def test3(self):
        """Exponential Sequence. (No docking required ever)"""
        W = [1,2,4,8,16,32,64,128,256]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    def test4(self):
        """Super Exponential Sequence. (Still no docking required ever)"""
        W = [1,4,16,64,256]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    def test5(self):
        """Exponential Sequence With Long Steps."""
        W = [1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    def test6(self):
        """Exponential Sequence With Very Long Steps."""
        W = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    def test7(self):
        """Sequence requiring Mixing."""
        W = [32,33,33,34,34,35,35,36,36,37,37,38,38,39,39,40,40,63,63,64,64,66,68,70,72,74,126]
        self.assertEqual(sorted(gdm(W)),sorted(vanLeeuwen(W)))
    def test8(self):
        """Alpha Equal Two. Minor Mixing between Internal Nodes and External Nodes"""
        W = [1]*8+[7]*3
        L = gdm(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test9(self):
        """Alpha Equal Two. Tight match between Internal Node and External Node"""
        W = [1]*8+[8]*3
        L = gdm(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test10(self):
        """Alpha Equal Two. Large gab between the weight of the Internal Node and the weights of the largest external nodes."""
        W = [1]*8+[32]*3
        L = gdm(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test11(self):
        """Alpha Equal Three with no Mixing."""
        W = [1]*4+[4]*3+[16]*3
        L = gdm(W)
        self.assertEqual(sorted(L),[2]*3+[4]*3+[6]*4)
    def test12(self):
        """Alpha Equal Three with no Mixing."""
        W = [1]*4+[4]*3+[16]*3+[128]*3
        L = gdm(W)
        self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))



        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

