import unittest,doctest
# from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from codeTree import Interval, ExternalNode, InternalNode, nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

def INITIALIZE(frequencies):
    """Given a partially sorted array, initialize the list of internal nodes with the two first external nodes:

>>> frequencies = PartiallySortedArray([90,80,70,60,50,40,30,20,10])
>>> nbFrequenciesProcessed,nodes = INITIALIZE(frequencies)
>>> print(nodeListToString(nodes))
[(rangeSum(0,2),[select(0)],[select(1)])]

Note that the weight of those external nodes is not computed yet, for a reason:
the function GROUP will join those two nodes, and compute the weight of the resulting node, *without* ordering those nodes between themselves. It saves only one comparison but it's the spirit that counts. So the cached value of those two nodes is still None:

>>> print(nodes[0].CachedValueOfWeight)
None

Beware: don't base yourself on the content of the list when printed (print(nodeListToStringOfWeights(nodes))): this depends of the implementation of PartiallySortedArray!

"""
    assert(len(frequencies)>1)
    nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
    nbFrequenciesProcessed = 2
    return nbFrequenciesProcessed,nodes

def DOCK(frequencies,nodes,maxWeight):
    """Given a partially sorted array of frequencies and the number of frequencies already processed, a set of internal nodes whose weight is all within a factor of two, and a weight maxWeight;
group the internal nodes two by two until at least one internal node has weight larger than maxWeight; and
return the resulting set of nodes.

Note that when the weight of the last node of the list is compute, at each iteration of the main loop, the partially sorted array is partially reordered to make sure that this node's weight correspond to what it would be if the array was fully sorted.

>>> frequencies = PartiallySortedArray([8]*4+[32])
>>> nbFrequenciesProcessed = 0
>>> nbFrequenciesProcessed,nodes = GROUP(frequencies,nbFrequenciesProcessed,8)
>>> nodeListToString(nodes)
'[[select(0)], [select(1)], [select(2)], [select(3)]]'
>>> nodes = DOCK(frequencies,nodes,32)
>>> nodeListToString(nodes)
'[(rangeSum(0,4),(rangeSum(0,2),[select(0)],[select(1)]),(16,[select(2)],[8]))]'
>>> nodeListToWeightList(nodes)
[32]
"""
    while len(nodes)>1 and nodes[-1].weight() <= maxWeight:
        nbPairsToForm = len(nodes) // 2
        for i in range(nbPairsToForm):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    return nodes

def GROUP(frequencies,nbFrequenciesProcessed, maxWeight):
    """Given a partially sorted array of frequencies,  the number of frequencies already transformed into nodes, and a weight w, 
returns the new value of nbFrequenciesProcessed and a vector of new nodes made of the frequencies less than or requal to w.

>>> frequencies = PartiallySortedArray([10,10,11,13,14,15,20,30])
>>> nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
>>> nbFrequenciesProcessed = 2
>>> nbFrequenciesProcessed,newNodes = GROUP(frequencies,nbFrequenciesProcessed,nodes[-1].weight())
>>> print(nodeListToString(newNodes))
[[select(2)], [select(3)], [select(4)], [select(5)], [select(6)]]
>>> print(nbFrequenciesProcessed)
7

At the end of the process (as before it), all the nodes are within a factor of two of each other:

>>> nodeListToWeightList(newNodes)
[11, 13, 14, 15, 20]
"""
    r = frequencies.rankRight(maxWeight)
    newNodes = []
    for i in range(nbFrequenciesProcessed,r):
        newNodes.append(ExternalNode(frequencies,i))
    nbFrequenciesProcessed = r
    return nbFrequenciesProcessed,newNodes

def MERGE(internalNodes,externalNodes):
    """Given two lists of nodes A and B, return a list containing the union of both.
    
The current implementation is crude, as a first draft.

>>> frequencies = PartiallySortedArray([8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,30])
>>> nbFrequenciesProcessed = 0
>>> nbFrequenciesProcessed,externalNodes = GROUP(frequencies,nbFrequenciesProcessed,16)
>>> internalNodes = []
>>> for i in range(4):   internalNodes.append(InternalNode(frequencies,externalNodes[2*i],externalNodes[2*i+1]))
>>> nodeListToString(externalNodes)
'[[select(0)], [select(1)], [select(2)], [select(3)], [select(4)], [select(5)], [select(6)], [select(7)], [select(8)]]'
>>> nodeListToWeightList(internalNodes)
[17, 21, 25, 29]
>>> nbFrequenciesProcessed,externalNodes = GROUP(frequencies,8,32)
>>> nodeListToString(externalNodes)
'[[select(8)], [select(9)], [select(10)], [select(11)], [select(12)], [select(13)], [select(14)], [select(15)]]'
>>> nodeListToWeightList(externalNodes)
[16, 18, 20, 22, 24, 26, 28, 30]

nodes = MERGE(internalNodes,externalNodes)
nodeListToWeightList(nodes)
[16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30]
nodeListToString(nodes)
'[[16], (17,[select(0)],[select(1)]), [18], [20], (21,[select(2)],[select(3)]), [22], [24], (25,[select(4)],[select(5)]), [26], [28], (29,[select(6)],[select(7)]), [30]]'

"""
    nodes = [] 
    while len(internalNodes)>0 and len(externalNodes)>0:
        if internalNodes[0].weight() < externalNodes[0].weight():
            nodes.append(internalNodes[0])
            internalNodes = internalNodes[1:]                                        
        else:
            nodes.append(externalNodes[0])
            externalNodes = externalNodes[1:]                                        
    if len(internalNodes)>0 :
        nodes = nodes + internalNodes
    else:
        nodes = nodes + externalNodes
    return nodes

def WRAPUP(frequencies,nodes):
    """Given a list of internal nodes (when there is no external nodes left), combine the nodes of the list until only one is left.

>>> frequencies = PartiallySortedArray([8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,30])
>>> nbFrequenciesProcessed = 0
>>> nbFrequenciesProcessed,externalNodes = GROUP(frequencies,nbFrequenciesProcessed,16)
>>> internalNodes = []
>>> for i in range(4):   internalNodes.append(InternalNode(frequencies,externalNodes[2*i],externalNodes[2*i+1]))
>>> nodeListToString(externalNodes)
'[[select(0)], [select(1)], [select(2)], [select(3)], [select(4)], [select(5)], [select(6)], [select(7)], [select(8)]]'
>>> nodes = WRAPUP(frequencies,internalNodes)
>>> nodeListToString(nodes)
'[(92,(rangeSum(0,4),(rangeSum(0,2),[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)])),(rangeSum(4,8),(rangeSum(4,6),[select(4)],[select(5)]),(rangeSum(6,8),[select(6)],[select(7)])))]'
>>> nodeListToWeightList(nodes)
[92]
>>> 
"""
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes[-1].weight()
        for i in range( len(nodes) // 2):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    nodes[0].weight()
    return nodes

def gdmCodeTree(frequencies):
    """Given a partially sorted list of weights, return a code tree of minimal
redundancy according to the GDM algorithm.

>>> node = gdmCodeTree(PartiallySortedArray([1]*8+[4]*3))
>>> print(node.weight())
20
>>> print(node)
(20,(8,[4],[4]),(12,[4],(8,(4,(2,[select(0)],[select(1)]),(2,[1],[1])),(4,(2,[1],[1]),(2,[1],[1])))))

"""
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    nbFrequenciesProcessed,nodes = INITIALIZE(frequencies)
    while nbFrequenciesProcessed < len(frequencies):
        nodes = DOCK(frequencies,nodes,frequencies.select(nbFrequenciesProcessed))
        nbFrequenciesProcessed,externalNodes = GROUP(frequencies,nbFrequenciesProcessed,nodes[-1].weight())
        nodes = MERGE(nodes,externalNodes)
    nodes = WRAPUP(frequencies,nodes)
    return nodes[0]

def gdm(frequencies):
    """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

>>> print(gdm([1,1,1,1]))
[2, 2, 2, 2]

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

        
# def main():
#     unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    # main()
            
        

