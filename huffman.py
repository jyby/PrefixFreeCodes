"""A simple implementation of Huffman's algorithm computing minimal
prefix free codes from unsorted weights.  The main function is
huffman, imported with "from huffman import huffman".

Given a list of weights, return a representation of
an optimal prefix free code, as a list of codelengths.

Runs in time within O(n lg n) in the worst case over instances of sizes n.
"""

import unittest, doctest
import heapq
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from depths import depths

def huffmanCodeTree(frequencies):
    """Given an unsorted list of of at least two weights, return a code tree of minimal
    redundancy according to Huffman's's algorithm.

    """
    if frequencies == []:
        return []
    elif len(frequencies) == 1:
        return [frequencies[0]]
    trees = []
    for w in frequencies:
        trees.append([w])
    heapq.heapify(trees)
    while len(trees) > 1:
        left = heapq.heappop(trees)
        right = heapq.heappop(trees)
        parent = [left[0]+right[0], left, right]
        heapq.heappush(trees, parent)
    return trees[0]

class TestHuffmanCodeTree(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(huffmanCodeTree([]),[])
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(huffmanCodeTree([1]),[1])
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(huffmanCodeTree([1,1]),[2, [1], [1]])
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(huffmanCodeTree([1,1,4]),[6, [2, [1], [1]], [4]])



        
def huffman(W):
    """Implementation in Python of the "Huffman" algorithm.

       This is an heap-based implementation of the method originally described by Huffman in 1952.

       It receives as input an array of integer frequencies of symbols.
       It returns an array of the same size containing the associated code lengths forming an optimal prefix free code for those frequencies.

    """
    if W == []:
        return []
    elif len(W) == 1:
        return [0]
    elif len(W) == 2:
        return [1,1]
    tree = huffmanCodeTree(W)
    codeLengths = depths(tree)
    return codeLengths
    
class HuffmanTest(unittest.TestCase):
    """Basic tests for the Huffman algorithm computing optimal prefix free codes.

    """
    def test(self):
        """Generic test"""
        testPFCAlgorithm(huffman, "Huffman")
    def testSixWeights(self):
        """Six Weights"""
        self.assertEqual(compressByRunLengths(huffman([1,1,1,1,1,1])),[(3,4),(2,2)])
    def testTwoLevels(self):
        """Two Leaf levels"""
        self.assertEqual(compressByRunLengths(huffman([1,1,1,1,8,8,8])),[(4,4),(2,3)])
    def testWith28Ones(self):
        """28 ones"""
        self.assertEqual(compressByRunLengths(huffman([1]*28)),[(5,24),(4,4)])
    def testThreeLevelsValuesDoNotMingle(self):
        """Three Leaf levels, and values do not mingle"""
        self.assertEqual(compressByRunLengths(huffman([1]*32+[10,13,15])),[(6,32),(3,2),(2,1)])
    def testIntermediateStepWith16And12(self):
        """Intermediate step"""
        self.assertEqual(compressByRunLengths(huffman([16,12,10,13,15])),[(3,2),(2,3)])
    def testIntermediateStepWith8And4(self):
        """Intermediate step"""
        self.assertEqual(compressByRunLengths(huffman([8,8,8,4,10,13,15])),[(4,2),(3,3),(2,2)])
    def testThreeLevelsValuesMingle(self):
        """Three Leaf levels, and values mingle"""
        self.assertEqual(compressByRunLengths(huffman([1]*28+[10,13,15])),[(7,8),(6,20),(3,1),(2,2)])
    
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

