#!/usr/bin/env/python3

def detectWrapper(graph,Debug=True):
    """
    python wrapper for the C++/Agrum base chordless circuits detection
    """
    import os
    from tempfile import NamedTemporaryFile
    fo = NamedTemporaryFile('w',delete=False)
    tempFileName = fo.name
    Med = graph.valuationdomain['med']
    actions = [x for x in graph.actions]
    #actions.sort()
    relation = graph.relation
    na = list(range(len(actions)))
    for i in na:
        for j in na:
            if i != j:
                if relation[actions[i]][actions[j]] > Med:
                    fo.write('%d %d\n' % (i+1,j+1))
    fo.close()
    resultFile = tempFileName+'.py'
    os.system('./detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
    exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'))
    if Debug:
        print('see file: ', tempFileName)
        print(resultFile)
        print(locals()['circuitsList'])
    circuits = locals()['circuitsList']
    if circuits != []:
        Detected = True
        if Debug:
            print('A chordless circuit has been detected !')
            print('certificate: ', circuits)
    else:
        Detected = False
        if Debug:
            print('No chordless circuit has been detected !')
            print('certificate: ', circuits)

    return Detected

    
# -------------   test pyWrapper
from time import time
from digraphs import *
t0 = time()
#t = RandomRankPerformanceTableau(numberOfActions=100)
#t = XMCDA2PerformanceTableau('testCpp')
#g = BipolarOutrankingDigraph(t)
#g.showRelationTable()
g = RandomDigraph(order=200,arcProbability=0.03)
print("Finished graph construction in ",time()-t0,'sec-')
t0 = time()
if detectWrapper(g,Debug=False):
    print('Chordless Circuit(s) detected !')
else:
    print('No Chordless Circuit detected !')
print('C++/Agrum wrapper time = ', time() - t0)
t0 = time()
if g.detectCppChordlessCircuits():
    print('Chordless Circuit(s) detected !')
else:
    print('No Chordless Circuit detected !')
print('C++/Agrum wrapper time = ', time() - t0)
## t0 = time()
## if len(g.computeChordlessCircuits()) != 0:
##     print 'Chordless Circuit(s) detected !'
## else:
##     print 'No Chordless Circuit detected !'
## print 'Python time = ', time() - t0
    
