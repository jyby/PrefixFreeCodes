"""A simple implementation of vanLeeuwen's algorithm computing minimal
prefix free codes from sorted weights.  The main function is
vanLeeuwen, imported with "from vanLeeuwen import vanLeeuwen".

Given a list of weights, return a representation of
an optimal prefix free code, as a list of codelengths.

Runs in linear time if the weights are already sorted, using the fact
that sorted(W) in python runs in linear time if W is already sorted, and
in time within O(n lg n) in the worst case over instances of sizes n.
"""

import unittest, doctest
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from depths import depths

def vanLeeuwen(W):
    """Given a list of weights, return the codelengths of
    an optimal prefix free code of minimal redundancy via van Leeuwen's algorithm.

    """
    if W==[]:
        return []
    elif len(W)==1:
        return [0]
    elif len(W)==2:
        return [1,1]
    Ws = sorted(W)
    tree = codeTree(Ws)
    codeLengths = depths(tree)
    return codeLengths

def codeTree(W):
    """Given a sorted list of weights, return a code tree of minimal
    redundancy according to vanLeeuwen's algorithm.
    """
    if W==[]:
        return []
    elif len(W)==1:
        return [W[0]]
    i = 0
    trees = []
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
        else:
            left = trees[0]
            trees = trees[1:]
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
        else:
            right = trees[0]
            trees = trees[1:]
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    return trees[0]

class TestCodeTree(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(codeTree([]),[])
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(codeTree([1]),[1])
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(codeTree([1,1]),[2, [1], [1]])
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(codeTree([1,1,4]),[6, [2, [1], [1]], [4]])

            
class vanLeeuwenTest(unittest.TestCase):
    """Basic tests for algorithms computing prefix free codes.
    """
    def test(self):
        """Generic test"""
        testPFCAlgorithm(vanLeeuwen, "vanLeeuwen")
    def testSixWeights(self):
        """Six Weights"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([1,1,1,1,1,1])),[(3,4),(2,2)])
    def testTwoLevels(self):
        """Two Leaf levels"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([1,1,1,1,8,8,8])),[(4,4),(2,3)])
    def testWith28Ones(self):
        """28 ones"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([1]*28)),[(5,24),(4,4)])
    def testThreeLevelsValuesDoNotMingle(self):
        """Three Leaf levels, and values do not mingle"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([1]*32+[10,13,15])),[(6,32),(3,2),(2,1)])
    def testIntermediateStepWith16And12(self):
        """Intermediate step"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([16,12,10,13,15])),[(3,2),(2,3)])
    def testIntermediateStepWith8And4(self):
        """Intermediate step"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([8,8,8,4,10,13,15])),[(4,2),(3,3),(2,2)])
    def testThreeLevelsValuesMingle(self):
        """Three Leaf levels, and values mingle"""
        self.assertEqual(compressByRunLengths(vanLeeuwen([1]*28+[10,13,15])),[(7,8),(6,20),(3,1),(2,2)])

def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()

