import unittest, doctest, copy
from logSort import logSort


class PartiallySortedArray(): 
    """A class receiving an unsorted array, supporting rank and select operators on it while partially sorting it so that to perform at most $(n+q)\lg n$ compairsons on it in total for $q$ rank queries and unlimited amount of select queries.

    """

    def __init__(self,A):
        """Given an array A, copy them in Weights and initialize the
        arrays hasMoved and Pivots to bitvectors of same lenght filled
        with zeroes.
        """
        self.values = copy.copy(A)
        self.pivot = [0]*len(self.values)
        self.clusters = []
        self.partialSums = [0]*(len(self.values)) # self.partialSums[i] = sum(values[0:i+1])
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

    def findLeftAndRightPivots(self,r):
        return self.findLeftAndRightPivotsInRange(r,0,len(self.values))
    def findLeftAndRightPivotsInRange(self,r, left, right):
        """Return the positions of closest 1 in Pivot to the left and
        to the right of position $r$ in the subarray
        $self.values[left:right]$.

        >>> T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        >>> T.values = [10,1,20,40,30,30,30,50,70,60]
        >>> T.pivot  = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        >>> T.findLeftAndRightPivots(5)
        (2, 7)
        """
        assert left <= r <= right
        leftPivot = rightPivot = r
        while leftPivot > left and self.pivot[leftPivot] != 1:
            leftPivot -= 1
        while rightPivot < right and self.pivot[rightPivot] != 1:
            rightPivot += 1
        return (leftPivot,rightPivot)

    def binarySearch(self,w,left,right):
        """Search for the "insertion rank" of $w$ in the subarray
        $self.values[left:right]$ (i.e. excluding self.value[right]
        from the search), ignoring the fact that the array might be in
        disorder (which prohibits the use of bisect_left from bisect).
        
        >>> T = PartiallySortedArray([0,1,2,3,4,5,6,7,8,9])
        >>> T.binarySearch(4.5,0,len(T.values))
        5
        >>> T.binarySearch(-1,0,len(T.values))
        0
        >>> T.binarySearch(10,0,len(T.values))
        10
        >>> T = PartiallySortedArray([40,30,20,10,00,50,90,80,70,60])
        >>> T.binarySearch(50,0,len(T.values))
        5
        >>> T.binarySearch(45,0,len(T.values))
        5
        """
        assert left <= right
        while left != right:
            middle = (left+right)/2
            if w > self.values[middle]:
                left = middle+1
            else: # w <= self.values[middle]
                right = middle
        return left

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
        >>> T.pivot
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        """
        (leftPivot,rightPivot) = self.findLeftAndRightPivotsInRange(self.binarySearch(w,left,right),left,right)
        (smaller,equal,larger) = self.PartitionByValueInRange(w,leftPivot,rightPivot)
        for i in range(len(smaller),len(smaller)+len(equal)):
            self.pivot[i] = 1
        self.values = smaller+equal+larger
        return len(smaller)

    def select(self,r):
        return self.selectAndPartitionInRange(r,0,len(self.values))
    def selectAndPartition(self,r):
        return self.selectAndPartitionInRange(r,0,len(self.values))
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
        >>> T.pivot
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        >>> T.selectAndPartitionInRange(0,0,len(T.values))
        1
        >>> T.values
        [1, 10, 20, 30, 30, 30, 70, 60, 50, 40]
        >>> T.pivot
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
        """
        assert 0 <= left <= right <= len(self.values)
        assert r in range(left,right), r
        pivot = self.values[r]
        (leftPivot,rightPivot) = self.findLeftAndRightPivotsInRange(r,left,right)
        (smaller,equal,larger) = self.PartitionByValueInRange(pivot,left,right)
        for i in range(len(smaller),len(smaller)+len(equal)):
            self.pivot[i] = 1
        self.values = smaller+equal+larger        
        if r < len(smaller):
            return self.selectAndPartitionInRange(r,left,len(smaller))
        elif r > len(smaller)+len(equal):
            return self.selectAndPartitionInRange(r,len(smaller)+len(equal),right)
        else:
            return equal[0]

    def preorder(self):
        """Preorder the weights with logsort and Bubble Passes;
        placing the min and max in each cluster; initializing Pivots
        and PartialSums.
        """
        (self.values,self.clusters) = logSort(self.values)
        self.minBubblePass()
        self.pivot = [1]*len(self.values)
        self.maxBubblePass()
        self.minBubblePass()
        # self.updatePartialSum(0,len(self.values))

    def maxBubblePass(self):
        """Performs a single left to right bubble pass on the array Weights, marking
        in the array Pivot which elements have moved by a zero.
        """
        if(len(self.values)==0):
            return
        weight = self.values[0]
        for i in range(1,len(self.values)):
            if weight > self.values[i]:
                self.values[i-1]=self.values[i]
                self.pivot[i-1]=0
            elif weight < self.values[i]:
                self.values[i-1] = weight
                weight = self.values[i]                
            # else: weight == self.Weight[i] and there is nothing to do
        self.values[-1] = weight

    def minBubblePass(self):
        """Performs a single right to left bubble pass on the array
        Weights, marking in the array Pivot which elements
        have moved by a zero.
        """
        if(len(self.values)==0):
            return
        weight = self.values[-1]
        for i in reversed(range(0,len(self.values)-1)):
            if weight < self.values[i]:
                self.values[i+1]=self.values[i]
                self.pivot[i+1]=0
            elif weight > self.values[i]:
                self.values[i+1] = weight
                weight = self.values[i]                
            # else: weight == self.Weight[i] and there is nothing to do
        self.values[0] = weight

    def partialSum(self,right):
        self.selectAndPartition(right)
        return self.partialSums[right-1]

    def rangeSum(self,left,right):
        self.selectAndPartition(left)
        self.selectAndPartition(right)
        return self.partialSums[right-1]-self.partialSums[left-1]

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


            
class PartiallySortedArrayTest(unittest.TestCase):
    """Basic tests for algorithms computing prefix free codes.
    """
        
    def testMaxBubblePassOnSortedArray(self):
        """Test Max bubble pass on sorted array.
        """
        W = [1,2,3,4,5,6,7,8]
        T = PartiallySortedArray(W)
        T.pivot = [1]*len(T.values)
        T.maxBubblePass()
        self.assertEqual(T.values,W)
        self.assertEqual(T.pivot,[1,1,1,1,1,1,1,1])
 
    def testMaxBubblePassOnInvertedArray(self):
        """Test Max bubble pass on inverted array.
        """
        W = [8,7,6,5,4,3,2,1]
        T = PartiallySortedArray(W)
        T.pivot = [1]*len(T.values)
        T.maxBubblePass()
        self.assertEqual(T.values,[7,6,5,4,3,2,1,8])
        self.assertEqual(T.pivot,[0,0,0,0,0,0,0,1])

    def testMaxBubblePassOnShuffledArray(self):
        """Test Max bubble pass on Shuffled array.
        """
        T = PartiallySortedArray([4,3,2,1,5,8,7,6])
        T.pivot = [1]*len(T.values) # Testing max Bubble Pass form pivots set to 1.
        T.maxBubblePass()
        self.assertEqual(T.values,[3,2,1,4,5,7,6,8])
        self.assertEqual(T.pivot,[0,0,0,1,1,0,0,1])

    def testMinBubblePassOnSortedArray(self):
        """Test min bubble pass on sorted array.
        """
        W = [1,2,3,4,5,6,7,8]
        T = PartiallySortedArray(W)
        T.pivot = [1]*len(T.values) # Testing min buble pass from pivots set to 1
        T.minBubblePass()
        self.assertEqual(T.values,W)
        self.assertEqual(T.pivot,[1,1,1,1,1,1,1,1])

    def testMinBubblePassOnInvertedArray(self):
        """Test min bubble pass on inverted array.
        """
        W = [8,7,6,5,4,3,2,1]
        T = PartiallySortedArray(W)
        T.pivot = [1]*len(T.values)  # Testing min buble pass from pivots set to 1
        T.minBubblePass()
        self.assertEqual(T.values,[1,8,7,6,5,4,3,2])
        self.assertEqual(T.pivot,[1,0,0,0,0,0,0,0])

    def testMinBubblePassOnShuffledArray(self):
        """Test min bubble pass on Shuffled array.
        """
        T = PartiallySortedArray([4,3,2,1,5,8,7,6])
        T.pivot = [1]*len(T.values) # Testing min buble pass from pivots set to 1
        T.minBubblePass()
        self.assertEqual(T.values,[1,4,3,2,5,6,8,7])
        self.assertEqual(T.pivot,[1,0,0,0,1,1,0,0])

    def testPreorderOnSmallShuffledArray(self):
        """Test preorder pass on a small Shuffled array with one point already in place.
        """
        T = PartiallySortedArray([4,3,2,1,5,8,7,6])
        T.preorder()
        self.assertEqual(T.values,[1,2,3,4,5,6,7,8])
        self.assertEqual(T.pivot,[1, 1, 1, 1, 1, 1, 1, 1])

    def testPreorderOnLargeInvertedArray(self):
        """Test preorder pass on a large inverted array.
        """
        T = PartiallySortedArray([ 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        T.preorder()
        self.assertEqual(T.values,[1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 13, 12, 11, 10, 15])
        self.assertEqual(T.pivot,[1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1])

    def testPreorderOnTwoInvertedArraysConcatenated(self):
        """Test preorder pass on two inverted arrays concatenated.
        """
        T = PartiallySortedArray([ 7, 6, 5, 4, 3, 2, 1, 8, 15, 14, 13, 12, 11, 10, 9])
        T.preorder()
        self.assertEqual(T.values,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 13, 12, 11, 15])
        self.assertEqual(T.pivot,[1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1])

    def testUpdatePartialSum(self):
        W = [1]*8
        A = PartiallySortedArray(W)
        A.updatePartialSum(0,len(W))
        self.assertEqual(A.partialSums,[1,2,3,4,5,6,7,8])
        
    def testRangeSum(self):
        W = [1]*8
        A = PartiallySortedArray(W)
        self.assertEqual(A.rangeSum(1,4),3)

    def testPartialSumOnOrderedArray(self):
        W = [1]*8
        A = PartiallySortedArray(W)
        self.assertEqual(A.partialSum(1),1)

    # def testPartialSumOnDisorderedArray(self):
    #     W = [9,8,7,6,5,4,3,2,1]
    #     A = PartiallySortedArray(W)
    #     self.assertEqual(A.partialSum(2),3)
    #     print A.partialSums
    #     # self.assertEqual(A.rangeSum(4,5),9)

    # def testSelectOnFirstValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(0),1)
    #     self.assertEqual(T.values,[1,70,60,50,40,30,30,30,20,10])
    #     self.assertEqual(T.pivot,[0]*9+[1])

    # def testSelectOnLastValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(9),70)
    #     self.assertEqual(T.values,[60,50,40,30,30,30,20,10,1,70])
    #     self.assertEqual(T.pivot,[0]*9+[1])

    # def testSelectOnLargeNumbersOnRepeatedCentralValue(self):
    #     T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
    #     self.assertEqual(T.select(4),30)
    #     self.assertEqual(T.values,[20, 10, 1, 30, 30, 30, 70, 60, 50, 40])
    #     self.assertEqual(T.pivot,[0,  0, 0,  1,  1,  1,  0,  0,  0,  0])

    # def testSelectOnSmallNumbers(self):
    #     W = [9,8,7,6,5,4,3,2,1,0]
    #     A = PartiallySortedArray(W)
    #     self.assertEqual(A.select(0),0)
    #     self.assertEqual(A.values,[0,9,8,7,6,5,4,3,2,1])

    def testRankOnLastElement(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(60),9)
        self.assertEqual(T.values,[60,50,40,30,30,30,20,10,1,70])

    def testRankOnFirstElement(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(1),0)
        self.assertEqual(T.values,[1,70,60,50,40,30,30,30,20,10])

    def testRankOnMiddle(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        self.assertEqual(T.rank(30),3)
        self.assertEqual(T.values,[20, 10, 1, 30, 30, 30, 70, 60, 50, 40])
        self.assertEqual(T.pivot,[0,  0, 0,  1,  1,  1,  0,  0,  0,  0])

    def testFindLeftAndRightPivots(self):
        T = PartiallySortedArray([70,60,50,40,30,30,30,20,10,1])
        T.values = [10,1,20,40,30,30,30,50,70,60]
        T.pivot  = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        self.assertEqual(T.findLeftAndRightPivots(5),(2,7))
        
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
