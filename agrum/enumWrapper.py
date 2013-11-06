#!/usr/bin/env/python3

def enumWrapper(graph,Odd=False,Debug=False):
    """
    python wrapper for the C++/Agrum base chordless circuits enumeration
    """
    import os
    from tempfile import NamedTemporaryFile
    fo = NamedTemporaryFile('w',delete=False)
    tempFileName = fo.name
    Med = graph.valuationdomain['med']
    actions = [x for x in graph.actions]
    actions.sort()
    relation = graph.relation
    na = list(range(len(actions)))
    for i in na:
        for j in na:
            if i != j:
                if relation[actions[i]][actions[j]] > Med:
                    fo.write('%d %d\n' % (i+1,j+1))
    fo.close()
    if Debug:
        print('see file: ', tempFileName)
    resultFile = tempFileName+'.py'
    try:
        os.system('enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
    except:
        print('Error !!!')
        return None
    if Debug:
        print(resultFile)
    exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'))
    if Debug:
        print(locals()['circuitsList'])
    circuits = locals()['circuitsList']
    result = []
    for x in circuits:
        r = len(x) % 2
        if Debug:
            print(x, r)
        if Odd:
            if r != 1:
                oddCircuit = []
                for ino in x[:-1]:
                    oddCircuit.append(actions[ino-1])
                result.append( ( oddCircuit, frozenset(oddCircuit) ) )
        else:
            Circuit = []
            for ino in x[:-1]:
                Circuit.append(actions[ino-1])
            result.append( ( Circuit, frozenset(Circuit) ) )     
    return result

    
# -------------   test pyWrapper
from time import time
from digraphs import *
from outrankingDigraphs import *
Na = 150
OddFlag=False
t0 = time()
t = RandomRankPerformanceTableau(numberOfActions=Na)
t.save('testCpp')
t = PerformanceTableau('testCpp')
g = BipolarOutrankingDigraph(t)
#g.showRelationTable()
print("Finished graph construction in ",time()-t0,'sec.')
t0 = time()
resw = enumWrapper(g,Odd=OddFlag,Debug=False)
if OddFlag:
    print('number of odd chordless circuits = ', len(resw))
else:
    print('number of chordless circuits = ', len(resw))
print('C++/Agrum wrapper time = ', time() - t0)
to = time()
res = g.computeChordlessCircuits(Odd=OddFlag)
if OddFlag:
    print('number of odd chordless circuits = ', len(res))
else:
    print('number of chordless circuits = ', len(res))
print('Python time = ', time() - t0)
