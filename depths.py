"""Some simple usefull function to extract the depths from a code tree.

"""
import unittest, doctest


def depths(tree, depth=0):
    """Given a code tree, return the (unsorted) list of the depths of its leaves.
    """
    if tree == []:
        return []
    assert len(tree) == 1 or len(tree) == 3
    if len(tree) == 1 :
        return [depth]
    else:
        (weigth, left, right) = tree
        depthsOnLeft =  depths(left,depth+1)
        depthsOnRight = depths(right,depth+1)
        return depthsOnLeft+depthsOnRight

class TestDepths(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(depths([]),[])
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(depths([1]),[0])
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(depths([2, [1], [1]]),[1,1])
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(depths([6, [2, [1], [1]], [4]]),[2,2,1])


        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()

