import unittest,doctest
# from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from codeTree import Interval, ExternalNode, InternalNode, nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

def INITIALIZE(frequencies):
    """Given a partially sorted array, initialize the list of internal nodes with the two first external nodes:

>>> frequencies = PartiallySortedArray([90,80,70,60,50,40,30,20,10])
>>> frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
>>> print(len(nodes))
2
>>> print(nodeListToString(nodes))
[[select(0)], [select(1)]]

Note that the weight of those external nodes is not computed yet, for a reason:
the function GROUP will join those two nodes, and compute the weight of the resulting node, *without* ordering those nodes between themselves. It saves only one comparison but it's the spirit that counts. So the cached value of those two nodes is still None:

>>> print(nodes[0].CachedValueOfWeight,nodes[1].CachedValueOfWeight)
(None, None)

Beware: don't base yourself on the content of the list when printed (print(nodeListToStringOfWeights(nodes))): this depends of the implementation of PartiallySortedArray!

"""
    assert(len(frequencies)>1)
    nodes = []
    nodes.append(ExternalNode(frequencies,0))
    nodes.append(ExternalNode(frequencies,1))
    nbFrequenciesProcessed = 2
    return frequencies,nodes,nbFrequenciesProcessed


def GROUP(frequencies,nbFrequenciesProcessed, maxWeight):
    """Given a partially sorted array of frequencies,  the number of frequencies already transformed into nodes, and a weight w, 
       returns the new value of nbFrequenciesProcessed and a vector of new nodes made of the frequencies less than or requal to w.

>>> frequencies = PartiallySortedArray([10,10,11,13,14,15,20,30])
>>> nodes = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
>>> nbFrequenciesProcessed = 2
>>> nbFrequenciesProcessed,newNodes = GROUP(frequencies,nbFrequenciesProcessed,nodes[-1].weight())
>>> print(nodeListToString(newNodes))
[[select(2)], [select(3)], [select(4)], [select(5)], [select(6)]]

At the end of the process (as before it), all the nodes are within a factor of two of each other:

>>> nodeListToWeightList(newNodes)
[11, 13, 14, 15, 20]
"""
    r = frequencies.rankRight(maxWeight)
    newNodes = [] 
    for i in range(nbFrequenciesProcessed,r):
        newNodes.append(ExternalNode(frequencies,i))
    return nbFrequenciesProcessed,newNodes

def DOCK(frequencies,nbFrequenciesProcessed,nodes,maxWeight):
    """Given a partially sorted array of frequencies and the number of frequencies already processed, a set of internal nodes whose weight is all within a factor of two, and a weight maxWeight;
group the internal nodes two by two until at least one internal node has weight larger than maxWeight; and
return the resulting set of nodes.

Note that when the weight of the last node of the list is compute, at each iteration of the main loop, the partially sorted array is partially reordered to make sure that this node's weight correspond to what it would be if the array was fully sorted.

>>> frequencies = PartiallySortedArray([8]*4+[32])
>>> nbFrequenciesProcessed = 0
>>> nbFrequenciesProcessed,nodes = GROUP(frequencies,nbFrequenciesProcessed,8)
>>> nodeListToString(nodes)
'[[select(0)], [select(1)], [select(2)], [select(3)]]'
>>> nodes = DOCK(frequencies,nbFrequenciesProcessed,nodes,32)
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


# def MERGE(frequencies,nodes,nbFrequenciesProcessed):
#     """Merge the list of Internal nodes with the external nodes of weights within a factor of two of it.

# """
#     r = frequencies.rank( 2 * nodes[0].weight() )
#     internalNodesToMerge = nodes
#     externalNodesToMerge = []
#     for p in range(nbFrequenciesProcessed,r):
#         externalNodesToMerge.append(ExternalNode(frequencies,p))
#     nbFrequenciesProcessed = r
#     nodes = []
#     while( len(internalNodesToMerge)>0 and len(externalNodesToMerge)>0 ):
#         children = []
#         for i in range(2):
#             if len(externalNodesToMerge)==0 or ( len(internalNodesToMerge)>0  and internalNodesToMerge[0].weight() < externalNodesToMerge[0].weight() ) :
#                 children.append(internalNodesToMerge[0])
#                 internalNodesToMerge = internalNodesToMerge[1:]
#             else:
#                 children.append(externalNodesToMerge[0])
#                 externalNodesToMerge = internalNodesToMerge[1:]
#         nodes.append(InternalNode(frequencies,children[0],children[1]))
#     nodes = internalNodesToMerge + externalNodesToMerge + nodes
#     return frequencies,nodes,nbFrequenciesProcessed


# def WRAPUP(frequencies,nodes):
#     """Combine the internal nodes of a list until only one is left.

# """
#     while len(nodes) > 1:
#         if len(nodes) % 2 == 1:
#             nodes[-1].weight()
#         for i in range( len(nodes) // 2):
#             nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
#             nodes = nodes[2:]
#     nodes[0].weight()
#     return frequencies,nodes

# def gdmCodeTree(frequencies):
#     """Given a partially sorted list of weights, return a code tree of minimal
# redundancy according to the GDM algorithm.

# >>> print(gdmCodeTree(PartiallySortedArray([1,1,1,1])))
# (4,(2,[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)]))
# """
#     if len(frequencies) == 0 :
#         return None
#     elif len(frequencies)==1:
#         return ExternalNode(frequencies,0)
#     frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
#     while nbFrequenciesProcessed < len(frequencies):
#         frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#     frequencies,nodes = WRAPUP(frequencies,nodes)
#     return nodes[0]

# def gdm(frequencies):
#     """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

# >>> print(gdm([1,1,1,1]))
# [2, 2, 2, 2]
# >>> print(gdm([1,2,4,8,16,32,64,128,256]))
# [8, 8, 7, 6, 5, 4, 3, 2, 1]

# """
#     # Degenerated cases
#     if len(frequencies) == 0 :
#         return []
#     elif len(frequencies)==1:
#         return [0]
#     elif len(frequencies)==2:
#         return [1,1]
#     codeTree = gdmCodeTree(PartiallySortedArray(frequencies))
#     codeLengths = codeTree.depths()
#     return codeLengths

        
# def main():
#     unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    # main()
            
        

