import unittest, doctest, copy, bisect

class PartiallySortedArray(): 
    """A class receiving an unsorted array, supporting rank, select and partialSum operators on it in the second most greedy way (the partial sums are computed only once). 

    """

    def __init__(self,A):
        """Create a Partially Sorted Array supporting rank, select and partialSum operators from a simple array.

        """
        self.values = sorted(A)
        self.partialSums = [0]*(len(self.values))
        partialSum = 0 
        for i in range(len(self.values)):
            partialSum +=  self.values[i]      
            self.partialSums[i] = partialSum
        self.nbRankQueriesProcessed = 0 
        self.nbSelectQueriesProcessed = 0 
        self.nbPartialSumQueriesProcessed = 0 
            
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
        self.nbSelectQueriesProcessed += 1
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
        self.nbRankQueriesProcessed += 1
        return bisect.bisect_left(self.values, x)

    def rankRight(self,x):
        """Number of Elements in the set which are smaller than or equal to x.

>>> S = PartiallySortedArray([50,40,40,40,40,30,20,10])
>>> print(S.rank(40))
3
>>> print(S.rankRight(40))
7
"""
        self.nbRankQueriesProcessed += 1
        return bisect.bisect_right(self.values, x)

    
    def partialSum(self,r):
        """Sum of the r smallest elements in the set.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.partialSum(2))
30
>>> print(S.partialSum(0))
0
"""
        if r <= 0:
            return 0
        else:
            self.nbPartialSumQueriesProcessed += 1
            return self.partialSums[r-1]

    def rangeSum(self,left,right):
        """Sum of the elements which would be in range(left,right) in the sorted array.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.rangeSum(0,2))
30
>>> print(S.rangeSum(0,0))
0
"""
        return self.partialSum(right)-self.partialSum(left)

    def totalNbOfQueriesPerformed(self):
        """Returns the total number of queries performed on the Partially Sorted Array.


>>> S = PartiallySortedArray([50,40,30,20,10])
>>> print(S.select(2))
30
>>> print(S.nbSelectQueriesProcessed)
1
>>> print(S.totalNbOfQueriesPerformed())
1
>>> print(S.select(0))
10
>>> print(S.totalNbOfQueriesPerformed())
2

"""
        return(self.nbRankQueriesProcessed+self.nbSelectQueriesProcessed+self.nbPartialSumQueriesProcessed)
        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
    
