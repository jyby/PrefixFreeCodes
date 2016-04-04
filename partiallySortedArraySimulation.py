import unittest, doctest, copy

class PartiallySortedArray(): 
    """A class receiving an unsorted array, supporting rank, select and partialSum operators on it in the most greedy way.

    """

    def __init__(self,A):
        """Create a Partially Sorted Array supporting rank, select and partialSum operators from a simple array.

        """
        self.values = sorted(A)
        self.partialSums = [0]*(len(self.values)) 
        sumSoFar = 0
        for i in range(len(self.values)):
            sumSoFar +=  self.values[i]      
            self.partialSums[i] = sumSoFar

    def __len__(self):
        """Number of Elements in the Partially Sorted Array.

>>> S = PartiallySortedArray([50,40,30,20,10])
>>> len(S)
5
        """
        return(len(self.values))



def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
    
