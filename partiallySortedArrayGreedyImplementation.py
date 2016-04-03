import unittest, doctest, copy


class PartiallySortedArray(): 
    """A class receiving an unsorted array, supporting rank, select and partialSum operators on it in the most greedy way.

    """

    def __init__(self,A):
        """Given an array A, copy them in Weights.
        """
        self.values = copy.copy(A)
        self.partialSums = [0]*(len(self.values)) 
        self.updatePartialSum(0,len(self.values))
        
    def __len__(self):
        return len(self.values)

    def PartitionByValue(self,w):
        return self.PartitionByValueInRange(w,0,len(self.values))
    def PartitionByValueInRange(self,w,left,right):
        """Return a triplet formed by 
        - the array of elements smaller than $w$;
        - the array of elements equal to $w$;
        - the array of elements larger than $w$.

        >>> T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        >>> T.PartitionByValueInRange(30,0,len(T.values))
        ([20, 10, 1], [30, 30, 30], [70, 60, 50, 40])
        """
        smaller = self.values[0:left]
        equal = []
        larger = []
        for weight in self.values[left:right]:
            if weight < w:
                smaller.append(weight)
            elif weight == w:
                equal.append(weight)
            else:
                larger.append(weight)
        # self.updatePartialSum(left,right)
        if left == 0:
            return (smaller,equal,larger+self.values[right:])
        else:
            return (self.values[:left]+smaller,
                    equal,
                    larger+self.values[right:])

    def rank(self,w):
        return self.rankAndPartitionInRange(w,0,len(self.values))
    def rankAndPartition(self,w):
        return self.rankAndPartitionInRange(w,0,len(self.values))
    def rankAndPartitionInRange(self,w,left,right):
        """Returns the number $r$ of elements strictly smaller than
        $w$ in the array $self.values$ and partitions this array so
        that 1) the $r$ elements smaller than $w$ are on the left; 2)
        the elements equal to $w$ are in positions $r+1$ and
        followings, marked by $1$ in the array $sefl.pivot$; and 3)
        the elements strictly larger than $w$ are to the right.

        >>> T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        >>> T.rankAndPartitionInRange(30,0,len(T.values))
        3
        >>> T.values
        [20, 10, 1, 30, 30, 30, 70, 60, 50, 40]
        """
        (smaller,equal,larger) = self.PartitionByValueInRange(w,0,len(self.values))
        self.values = smaller+equal+larger
        return len(smaller)

    def select(self,r):
        return self.selectAndPartitionInRange(r,0,len(self.values))
    def selectAndPartition(self,r):
        return self.selectAndPartitionInRange(r,0,len(self.values))
    def __getitem__(self,r):
        return self.selectAndPartition(r)
    def selectAndPartitionInRange(self,r,left,right):
        """Returns the $r$-th smallest element of $self.values$, and
        partition this array so that the $r-1$ smallest element are in
        positions $1$ to $r-1$, the $r$-th in position $r$, and the
        larger elements to its right.

        >>> T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        >>> T.selectAndPartitionInRange(5,0,len(T.values))
        30
        >>> T.values
        [20, 10, 1, 30, 30, 30, 70, 60, 50, 40]
        >>> T.selectAndPartitionInRange(0,0,len(T.values))
        1
        >>> T.values
        [1, 10, 20, 30, 30, 30, 70, 60, 50, 40]
        """
        assert 0 <= left <= right <= len(self.values)
        assert r in range(left,right), r
        pivot = self.values[r]
        (smaller,equal,larger) = self.PartitionByValueInRange(pivot,0,len(self.values))
        self.values = smaller+equal+larger        
        if r < len(smaller):
            return self.selectAndPartitionInRange(r,0,len(smaller))
        elif r > len(smaller)+len(equal):
            return self.selectAndPartitionInRange(r,len(smaller)+len(equal),len(self.values))
        else:
            return equal[0]

    def updatePartialSum(self,left,right):
        """Updates the partial sum vector between left and right.

        >>> T = PartiallySortedArray([1,1,1,1])
        >>> T.partialSums
        [1, 2, 3, 4]
        """
        if left > 0:
            partialSum = self.partialSums[left-1]
        else:
            partialSum = 0
        for i in range(left,right):
            partialSum +=  self.values[i]      
            self.partialSums[i] = partialSum
    def partialSum(self,right):
        self.selectAndPartition(right)
        self.updatePartialSum(0,right)
        return self.partialSums[right-1]
    def rangeSum(self,left,right):
        self.selectAndPartition(left)
        self.selectAndPartition(right)
        self.updatePartialSum(left,right)
        return self.partialSums[right-1]-self.partialSums[left-1]
            
class PartiallySortedArrayTest(unittest.TestCase):
    """Basic tests for algorithms computing prefix free codes.
    """
        
    def testUpdatePartialSumWithEightSortedDistinctWeights(self):
        W = [10,20,30,40,50,60,70,80]
        A = PartiallySortedArray(W)
        A.updatePartialSum(0,len(W))
        self.assertEqual(A.partialSums,[10,30,60,100,150,210,280,360])

    def testUpdatePartialSumWithFourUnSortedDistinctWeights(self):
        W = [40,30,20,10]
        A = PartiallySortedArray(W)
        A.updatePartialSum(0,len(W))
        self.assertEqual(A.partialSums,[40,70,90,100])

    def testUpdatePartialSumWithEightEqualWeights(self):
        W = [10]*8
        A = PartiallySortedArray(W)
        A.updatePartialSum(0,len(W))
        self.assertEqual(A.partialSums,[10,20,30,40,50,60,70,80])
        
    def testRangeSumOnEightSameWeights(self):
        W = [10]*8
        A = PartiallySortedArray(W)
        self.assertEqual(A.rangeSum(1,4),30)

    def testPartialSumOnOrderedArray(self):
        W = [10]*8
        A = PartiallySortedArray(W)
        self.assertEqual(A.partialSum(4),40)

    def testPartialSumOnDisorderedArray(self):
        W = [90,80,70,60,50,40,30,20,10]
        A = PartiallySortedArray(W)
        weightSum = A.partialSum(2)
        self.assertEqual(weightSum,30)

    # def testSelectOnFirstValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(0),1)
    #     self.assertEqual(T.values,[1,70,60,50,40,30,30,30,20,10])

    # def testSelectOnLastValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(9),70)
    #     self.assertEqual(T.values,[60,50,40,30,30,30,20,10,1,70])

    # def testSelectOnLargeNumbersOnRepeatedCentralValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(4),30)
    #     self.assertEqual(T.values,[20, 10, 1, 30, 30, 30, 70, 60, 50, 40])

    # def testSelectOnSmallNumbers(self):
    #     W = [9,8,7,6,5,4,3,2,1,0]
    #     A = PartiallySortedArray(W)
    #     self.assertEqual(A.select(0),0)
    #     self.assertEqual(A.values,[0,9,8,7,6,5,4,3,2,1])

    def testRankOnLastElement(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(60),8)
        self.assertEqual(T.values,[50,40,30,30,30,20,10,1,60,70])

    def testRankOnFirstElement(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(1),0)
        self.assertEqual(T.values,[1,70,60,50,40,30,30,30,20,10])

    def testRankOnMiddle(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(30),3)
        self.assertEqual(T.values,[20, 10, 1, 30, 30, 30, 70, 60, 50, 40])
        
    def testPartitionByValueOnLastValue(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.PartitionByValue(70),([60,50,40,30,30,30,20,10,1],[70],[]))

    def testPartitionByValueOnFirstValue(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.PartitionByValue(1),([],[1],[70,60,50,40,30,30,30,20,10]))

    def testPartitionByValueOnMiddleValue(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.PartitionByValue(30),([20, 10, 1], [30, 30, 30], [70, 60, 50, 40]))
        
    def testInitialize(self):
        W = [1,2,3,4,5,6,7,8]
        T = PartiallySortedArray(W)
        self.assertEqual(T.values,W)

def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
