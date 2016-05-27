import unittest,doctest
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from codeTree import Interval, ExternalNode, InternalNode, nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

def WRAPUP(frequencies,nodes):
    """Given a list of internal nodes (when there is no external nodes left), combine the nodes of the list until only one is left.
"""
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes[-1].weight()
        for i in range( len(nodes) // 2):
            nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
            nodes = nodes[2:]
    nodes[0].weight()
    return nodes

def dvlCodeTree(frequencies):
    """Given a partially sorted list of weights, return a code tree of minimal
redundancy according to the GDM algorithm.

>>> node = dvlCodeTree(PartiallySortedArray([1]*8+[4]*3))
>>> print(node.weight())
20
>>> print(node)
(20,(8,[4],[4]),(12,[4],(8,(rangeSum(0,4),(2,[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)])),(4,(rangeSum(4,6),[select(4)],[select(5)]),(2,[select(6)],[select(7)])))))

"""
    if len(frequencies) == 0 :
        return None
    elif len(frequencies)==1:
        return ExternalNode(frequencies,0)
    externals = [ExternalNode(frequencies,i) for i in range(2,len(frequencies))]
    internals = [InternalNode(frequencies,ExternalNode(frequencies,0),ExternalNode(frequencies,1))]
    while 0 < len(externals):
        # EE...E
        r = frequencies.rankRight(internals[0].weight())
        nbNodes = r-len(frequencies)+len(externals)
        nbPairs = nbNodes/2
        for i in range(0,nbPairs):
            internals.append(InternalNode(frequencies,externals[2*i],externals[2*i+1]))
        externals = externals[2*nbPairs:]
        # EI
        if 2*nbPairs < nbNodes:
            internals.append(InternalNode(frequencies, externals[0],internals[0]))
            externals = externals[1:]
            internals = internals[1:]
        # II...I
        while len(externals)>0 and len(internals)>1 and internals[-1].weight() <= externals[0].weight():
            nbPairsToForm = len(internals) // 2
            for i in range(nbPairsToForm):
                internals.append(InternalNode(frequencies,internals[2*i],internals[2*i+1]))
            internals = internals[2*nbPairsToForm:]
        # IE
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
    internals = WRAPUP(frequencies,internals)
    return internals[0]

def dvl(frequencies):
    """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the Deferred van Leeuwen's algorithm.

>>> print(dvl([1,1,1,1]))
[2, 2, 2, 2]

"""
    # Degenerated cases
    if len(frequencies) == 0 :
        return []
    elif len(frequencies)==1:
        return [0]
    elif len(frequencies)==2:
        return [1,1]
    codeTree = dvlCodeTree(PartiallySortedArray(frequencies))
    codeLengths = codeTree.depths()
    return codeLengths

        
# def main():
#     unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    # main()
            
        

