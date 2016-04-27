import unittest,doctest
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple

Interval = namedtuple('Interval','left right')

class ExternalNode:
    """Given a partially sorted array W, and a position in it, create the corresponding External node.
The weight is computed only at request by performing a select query in the partiallySortedArray.

>>> W = PartiallySortedArray([150,140,130,120,110,32,16,10,10,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,0)
>>> z = ExternalNode(W,1)
>>> print(x == y)
True
>>> print(x == z)
False

"""
    def __init__(self, partiallySortedArray, position):
        self.position = position
        self.partiallySortedArray = partiallySortedArray
        self.interval = Interval(position,position+1)
        self.CachedValueOfWeight = None
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.select(self.interval[0])
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.
        """
        return [depth]
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.interval == other.interval and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    def __str__(self):
        if self.CachedValueOfWeight == None:
            return "[select("+str(self.position)+")]"
        else:
            return "["+str(self.CachedValueOfWeight)+"]"


class InternalNode:
    """Given a partially sorted array W and two pointers, builds a node of the codeTree for the GDM algorithm.  The weight is computed only at request.

>>> W = PartiallySortedArray([100,100,50,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,1)
>>> z = InternalNode(W,x,y)
>>> print(W.totalNbOfQueriesPerformed())
0
>>> print(x.weight())
10
>>> print(y.weight())
10
>>> print(z.weight())
20
>>> x2 = ExternalNode(W,3)
>>> y2 = ExternalNode(W,4)
>>> z2 = InternalNode(W,x2,y2)
>>> print(z2.weight())
200
>>> z3 = InternalNode(W,z,z2)
>>> print(z3.weight())
220
>>> print(z3.depths())
[2, 2, 2, 2]

"""
    def __init__(self, partiallySortedArray, left, right):
        self.partiallySortedArray = partiallySortedArray
        self.left = left
        self.right = right
        if(left.interval != None and right.interval != None and left.interval.right == right.interval.left):
            self.interval = Interval(left.interval.left,right.interval.right)
        else:
            self.interval = None
        if left.CachedValueOfWeight == None or right.CachedValueOfWeight == None:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = left.CachedValueOfWeight + right.CachedValueOfWeight
    def weight(self):
        if self.CachedValueOfWeight == None:
            if self.interval != None:
                self.CachedValueOfWeight = self.partiallySortedArray.rangeSum(self.interval.left,self.interval.right)
            else:
                self.CachedValueOfWeight = self.left.weight() + self.right.weight()
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.

"""
        depthsOnLeft =  self.left.depths(depth+1)
        depthsOnRight = self.right.depths(depth+1)
        return depthsOnLeft+depthsOnRight
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.interval == other.interval and self.left == other.left and self.right == other.right and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    def __str__(self):
        string = "("+str(self.CachedValueOfWeight)+","+str(self.left)+","+str(self.right)+")"
        return string


def nodeListToString(nodes):
    """Given a list of nodes, returns a string listing the trees in the list.

>>> w = PartiallySortedArray([1,2,3,4])
>>> x = ExternalNode(w,0)
>>> y = InternalNode(w,ExternalNode(w,1),ExternalNode(w,2))
>>> z = ExternalNode(w,3)
>>> print(x.weight(),y.weight())
(1, 5)
>>> l = [x,y,z]
>>> print(nodeListToString(l))
[[1], (5,[None],[None]), [None]]
"""
    output = "["
    for i in range(len(nodes)-1):
        output += str(nodes[i])+", "
    output += str(nodes[-1])
    output += "]"
    return output

def nodeListToStringOfWeights(nodes):
    """Given a list of nodes, returns a string listing the weights of the nodes in the list.

>>> w = PartiallySortedArray([10,20,30,40])
>>> l = [ExternalNode(w,0),InternalNode(w,ExternalNode(w,1),ExternalNode(w,2)),ExternalNode(w,3)]
>>> print(nodeListToStringOfWeights(l))
[10, 50, 40]
"""
    output = "["
    for i in range(len(nodes)-1):
        output += str(nodes[i].weight())+", "
    output += str(nodes[-1].weight())
    output += "]"
    return output

def nodeListToWeightList(nodes):
    """Given a list of nodes, returns the list of the weights of the nodes in the list.

>>> w = PartiallySortedArray([10,20,30,40])
>>> l = [ExternalNode(w,0),InternalNode(w,ExternalNode(w,1),ExternalNode(w,2)),ExternalNode(w,3)]
>>> print(nodeListToWeightList(l))
[10, 50, 40]
"""
    l = []
    for i in range(len(nodes)):
        l.append(nodes[i].weight())
    return l


        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

