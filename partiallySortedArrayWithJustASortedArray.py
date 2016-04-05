import unittest, doctest, copy

class PartiallySortedArray(): 
    """A class receiving an unsorted array, supporting rank, select and partialSum operators on it in the most greedy way.

    """

    def __init__(self,A):
        """Create a Partially Sorted Array supporting rank, select and partialSum operators from a simple array.

        """
        self.values = sorted(A)

    def __len__(self):
        """Number of Elements in the Partially Sorted Array.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> len(S)
5
"""
        return(len(self.values))

    def select(self,r):
        """Element of the set such that r elements are smaller.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.select(2))
30
>>> print(S.select(0))
10
"""
        return(self.values[r])

    
    def rank(self,x):
        """Number of Elements in the set which are smaller than x.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.rank(40))
3
>>> print(S.rank(100))
5
>>> print(S.rank(-10))
0
"""
        rank = 0
        for i in range(len(self.values)):
            if self.values[i] < x:
                rank += 1                       
        return rank

    
    def partialSum(self,r):
        """Sum of the r smallest elements in the set.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.partialSum(2))
30
>>> print(S.partialSum(0))
0
"""
        partialSum = 0 
        for i in range(r):
            partialSum += self.values[i]
        return partialSum

    def rangeSum(self,left,right):
        """Sum of the elements which would be in range(left,right) in the sorted array.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.rangeSum(0,2))
30
>>> print(S.rangeSum(0,0))
0
"""
        partialSum = 0 
        for i in range(left,right):
            partialSum += self.values[i]
        return partialSum
        
        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
    