import unittest,doctest
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple
from vanLeeuwen import vanLeeuwen

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


def INITIALIZE(frequencies):
    """Given a partially sorted array, initialize the list of internal nodes.

"""
    nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))] 
    nbFrequenciesProcessed = 2
    return frequencies,nodes,nbFrequenciesProcessed

def GROUP(frequencies,nodes,nbFrequenciesProcessed):
    r = frequencies.rankRight(nodes[0].weight())        
    if len(nodes)==1 and r == nbFrequenciesProcessed: # if there is only one internal node and it is smaller than any external node
        nodes[0].weight()
        nodes = nodes[1:]+[InternalNode(frequencies,nodes[0],ExternalNode(frequencies,r))]
        nbFrequenciesProcessed += 1
    else:
        if (r-nbFrequenciesProcessed) % 2 == 1: # if there is an odd number of external nodes smaller than the smallest internal node,
            nodes = [ExternalNode(frequencies,r-1)]+nodes # promote the last external node by adding it directly to the list of nodes.
        for i in range((r-nbFrequenciesProcessed)//2): # pair the even number of nodes preceding it, andd add them to the list of nodes.
            left = ExternalNode(frequencies,nbFrequenciesProcessed+2*i)
            right = ExternalNode(frequencies,nbFrequenciesProcessed+2*i+1)        
            nodes.append(InternalNode(frequencies,left,right))
        nbFrequenciesProcessed = r
    return frequencies,nodes,nbFrequenciesProcessed

def MERGE(frequencies,nodes,nbFrequenciesProcessed):
    """Merge the list of Internal nodes with the external nodes of similar weight.

"""
    internalNodesToMerge = nodes
    externalNodesToMerge = []
    for p in range(nbFrequenciesProcessed,frequencies.rankRight(nodes[-1].weight())):
        externalNodesToMerge.append(ExternalNode(frequencies,p))
        nbFrequenciesProcessed += 1
    nodes = []
    while(len(internalNodesToMerge)>0 and len(externalNodesToMerge)>0):
        children = []
        for i in range(2):
            if len(externalNodesToMerge)==0 or internalNodesToMerge[0].weight() < externalNodesToMerge[0].weight() :
                children.append(internalNodesToMerge[0])
                internalNodesToMerge = internalNodesToMerge[1:]
            else:
                children.append(externalNodesToMerge[0])
                externalNodesToMerge = internalNodesToMerge[1:]
        nodes.append(InternalNode(frequencies,children[0],children[1]))
    nodes = internalNodesToMerge + externalNodesToMerge + nodes
    return frequencies,nodes,nbFrequenciesProcessed

def DOCK(frequencies,nodes,nbFrequenciesProcessed):
    """Given a set of internal nodes, group them two by two until at least one internal node has weight larger than the weight of the next External node (but smaller than twice this weight)

"""
    # print(str(nbFrequenciesProcessed)+" frequencies processed out of "+str(len(frequencies)))
    # print("First available external has weight "+str(frequencies.select(nbFrequenciesProcessed))+", while the largest internal node has weight "+str(nodes[-1].weight()))
    while len(nodes)>1 and nodes[-1].weight() <= frequencies.select(nbFrequenciesProcessed):
        # print(str(len(nodes))+" nodes left, of maximal weight "+str(nodes[-1].weight(),))
        nbPairsToForm = len(nodes) // 2
        for i in range(nbPairsToForm):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    return frequencies,nodes,nbFrequenciesProcessed

def WRAPUP(frequencies,nodes):
    """Combine the internal nodes of a list until only one is left.

"""
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes[-1].weight()
        for i in range( len(nodes) // 2):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    nodes[0].weight()
    return frequencies,nodes

def gdmCodeTree(frequencies):
    """Given a partially sorted list of weights, return a code tree of minimal
redundancy according to the GDM algorithm.

>>> print(gdmCodeTree(PartiallySortedArray([1,1,1,1])))
(4,(2,[None],[None]),(None,[None],[None]))
>>> print(gdmCodeTree(PartiallySortedArray([1,2,4,8,16,32,64,128,256])))
(511,(255,(127,(63,(31,(15,(7,(3,[None],[None]),[None]),[None]),[None]),[None]),[None]),[None]),[None])

"""
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
    while nbFrequenciesProcessed < len(frequencies):
        ### GROUP weights of similar weights: 
        frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
        if nbFrequenciesProcessed == len(frequencies):
            break
        frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
        frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
    frequencies,nodes = WRAPUP(frequencies,nodes)
    return nodes[0]

def gdm(frequencies):
    """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

>>> print(gdm([1,1,1,1]))
[2, 2, 2, 2]
>>> print(gdm([1,2,4,8,16,32,64,128,256]))
[8, 8, 7, 6, 5, 4, 3, 2, 1]

"""
    # Degenerated cases
    if len(frequencies) == 0 :
        return []
    elif len(frequencies)==1:
        return [0]
    elif len(frequencies)==2:
        return [1,1]
    codeTree = gdmCodeTree(PartiallySortedArray(frequencies))
    codeLengths = codeTree.depths()
    return codeLengths

        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

