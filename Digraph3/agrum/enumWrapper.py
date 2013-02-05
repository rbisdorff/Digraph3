#!/usr/bin/env/python

def enumWrapper(graph,Debug=False):
    """
    python wrapper for the C++/Agrum base chordless circuits enumeration
    """
    import os
    from tempfile import NamedTemporaryFile
    fo = NamedTemporaryFile(delete=False)
    tempFileName = fo.name
    Med = graph.valuationdomain['med']
    actions = [x for x in graph.actions]
    actions.sort()
    relation = graph.relation
    na = range(len(actions))
    for i in na:
        for j in na:
            if i != j:
                if relation[actions[i]][actions[j]] > Med:
                    fo.write('%d %d\n' % (i+1,j+1))
    fo.close()
    if Debug:
        print 'see file: ', tempFileName
    resultFile = tempFileName+'.py'
    try:
        os.system('enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
    except:
        print 'Error !!!'
        return None
    if Debug:
        print resultFile
    execfile(str(resultFile))
    if Debug:
        print locals()['circuitsList']
    circuits = locals()['circuitsList']
    result = []
    for x in circuits:
        r = len(x) % 2
        if Debug:
            print x, r
        if r != 1:
            oddCircuit = []
            for ino in x[:-1]:
                oddCircuit.append(actions[ino-1])
            result.append( ( oddCircuit, frozenset(oddCircuit) ) )        
    return result

    
# -------------   test pyWrapper
from time import time
from digraphs import *
t = RandomRankPerformanceTableau(numberOfActions=20)
#t = XMCDA2PerformanceTableau('testCpp')
g = BipolarOutrankingDigraph(t)
#g.showRelationTable()
t0 = time()
print "Finished graph construction in ",time()-t0,'sec-'
t0 = time()
resw = enumWrapper(g,Debug=False)
print 'number of odd circuits = ', len(resw)
print 'C++/Agrum wrapper time = ', time() - t0
to = time()
res = g.computeChordlessCircuits()
print 'number of odd circuits = ', len(res)
print 'Python time = ', time() - t0
