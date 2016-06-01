import unittest,doctest
# from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from codeTree import Interval, ExternalNode, InternalNode, nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

def INITIALIZE(frequencies):
    """Given a partially sorted array, initialize the list of external nodes and the list of internal nodes with the two first external nodes:

>>> frequencies = PartiallySortedArray([90,80,70,60,50,40,30,20,10])
>>> frequencies,externals,internals = INITIALIZE(frequencies)
>>> print(nodeListToString(internals))
[(rangeSum(0,2),[select(0)],[select(1)])]

Note that the weight of those external nodes is not computed yet, for a reason:
the function GroupExternals will join those two nodes, and compute the weight of the resulting node, *without* ordering those nodes between themselves. It saves only one comparison but it's the spirit that counts. So the cached value of those two nodes is still None:

>>> print(internals[0].CachedValueOfWeight)
None

Beware: don't base yourself on the content of the list when printed (print(nodeListToStringOfWeights(nodes))): this depends of the implementation of PartiallySortedArray!

"""
    assert(len(frequencies)>1)
    externals = [ExternalNode(frequencies,i) for i in range(2,len(frequencies))]
    internals = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
    return frequencies,externals,internals

def GroupExternals(frequencies,externals,internals):
    """Given a partially sorted array of frequencies, a list of external nodes and a list of internal nodes, 
selects the external nodes of weight smaller than the smallest internal node, and pairs them two by two in internal node.
 
>>> frequencies = PartiallySortedArray([50, 50, 51, 52, 53, 54, 55, 1000])
>>> frequencies,externals,internals = INITIALIZE(frequencies)
>>> nodeListToWeightList(externals)
[51, 52, 53, 54, 55, 1000]
>>> nodeListToWeightList(internals)
[100]
>>> frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
>>> nodeListToWeightList(externals)
[1000]
>>> nodeListToWeightList(internals)
[103, 107, 155]
"""
    # EE...E
    r = frequencies.rankRight(internals[0].weight())
    nbNodes = r-len(frequencies)+len(externals)
    nbPairs = nbNodes/2
    for i in range(0,nbPairs):
        internals.append(InternalNode(frequencies,externals[0],externals[1]))
        externals = externals[2:]
    # EI
    if 2*nbPairs < nbNodes:
        internals.append(InternalNode(frequencies, externals[0],internals[0]))
        externals = externals[1:]
        internals = internals[1:]
    return frequencies,externals,internals

def DockInternals(frequencies,externals,internals):
    """Given a partially sorted array of frequencies and the number of frequencies already processed, a set of internal nodes whose weight is all within a factor of two, and a weight maxWeight;
group the internal nodes two by two until at least one internal node has weight larger than maxWeight; and
return the resulting set of nodes.

Note that when the weight of the last node of the list is computed, at each iteration of the main loop, the partially sorted array is partially reordered to make sure that this node's weight correspond to what it would be if the array was fully sorted.

>>> frequencies = PartiallySortedArray([8]*8+[255])
>>> frequencies,externals,internals = INITIALIZE(frequencies)
>>> frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
>>> frequencies,externals,internals = DockInternals(frequencies,externals,internals)
>>> nodeListToWeightList(internals)
[64]
>>> nodeListToWeightList(externals)
[255]
"""
    while len(externals)>0 and len(internals)>1 and internals[-1].weight() <= externals[0].weight():
        nbPairsToForm = len(internals) // 2
        for i in range(nbPairsToForm):
            internals.append(InternalNode(frequencies,internals[2*i],internals[2*i+1]))
        internals = internals[2*nbPairsToForm:]
    return frequencies,externals,internals

def MixInternalWithExternal(frequencies,externals,internals):
    """Given a partially sorted array of frequencies, a list of external nodes and a list of internal nodes, 
    
>>> frequencies = PartiallySortedArray([8]*8+[255])
>>> frequencies,externals,internals = INITIALIZE(frequencies)
>>> frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
>>> frequencies,externals,internals = DockInternals(frequencies,externals,internals)
>>> frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
>>> nodeListToWeightList(internals)
[319]
"""
    if len(externals)==1:
        if len(internals)==1:            
            internals = [InternalNode(frequencies,internals[0],externals[0])]
            externals = []
        else:
            if internals[1].weight() < externals[0].weight():
                internals = internals[2:]+[InternalNode(frequencies,internals[0],internals[1])]
            else:
                internals = internals[1:]+[InternalNode(frequencies,internals[0],externals[0])]
                externals = [] 
    elif len(externals)>1:
        if len(internals)==1:
            if internals[0].weight() < externals[1].weight():
                internals = internals[1:]+[InternalNode(frequencies,internals[0],externals[0])]
                externals = externals[1:] 
            else:
                internals.append(InternalNode(frequencies,externals[0],externals[1]))
                externals = externals[2:]
        else:
            children = []
            for i in range(2):            
                if len(externals)==0 or (len(internals)>0 and internals[0].weight() < externals[0].weight()) :
                    children.append(internals[0])
                    internals = internals[1:]
                else:
                    children.append(externals[0])
                    externals = externals[1:]
            internals.append(InternalNode(frequencies,children[0],children[1]))
    return frequencies,externals,internals


def pairTwoMinimumNodes(frequencies,externals,internals):
    """Given a partially sorted array of frequencies, a list of external nodes and a list of internal nodes, execute one step of van Leeuwen's algorithm.
"""    
    if len(internals)+len(externals)>1:
        children = []
        for i in range(2):            
            if len(externals)==0 or (len(internals)>0 and internals[0].weight() < externals[0].weight()) :
                children.append(internals[0])
                internals = internals[1:]
            else:
                children.append(externals[0])
                externals = externals[1:]
        internals.append(InternalNode(frequencies,children[0],children[1]))
    return frequencies,externals,internals

def WRAPUP(frequencies,nodes):
    """Given a list of internal nodes (when there is no external nodes left), combine the nodes of the list until only one is left.

>>> frequencies = PartiallySortedArray([1]*64)
>>> frequencies,externals,internals = INITIALIZE(frequencies)
>>> frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
>>> frequencies,internals = WRAPUP(frequencies,internals)
>>> nodeListToWeightList(internals)
[64]
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

>>> node = gdmCodeTree(PartiallySortedArray([1]*8+[4]*3))
>>> print(node.weight())
20
>>> print(node)
(20,(8,[4],[4]),(12,[4],(8,(rangeSum(0,4),(2,[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)])),(4,(rangeSum(4,6),[select(4)],[select(5)]),(2,[select(6)],[select(7)])))))
"""
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    frequencies,externals,internals = INITIALIZE(frequencies)
    while len(externals)>0 :
        frequencies,externals,internals = GroupExternals(frequencies,externals,internals)
        frequencies,externals,internals = DockInternals(frequencies,externals,internals)
        frequencies,externals,internals = MixInternalWithExternal(frequencies,externals,internals)
    frequencies,internals = WRAPUP(frequencies,internals)
    return internals[0]

def gdm(frequencies):
    """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

>>> print(gdm([1]*4+[8]*3))
[4, 4, 4, 4, 2, 2, 2]
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
            
        

