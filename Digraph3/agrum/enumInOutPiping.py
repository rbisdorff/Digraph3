#!/usr/bin/env/python3

def enumWrapper(graph,Debug=False):
    """
    python subproecess piping wrapper for the
    C++/Agrum base chordless circuits enumeration.
    """
    from subprocess import Popen,PIPE
    p = Popen(args=['enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
    #fo = p.stdin
    Med = graph.valuationdomain['med']
    actions = [x for x in graph.actions]
    actions.sort()
    relation = graph.relation
    inputString = ''
    for i,x in enumerate(actions):
        for j,y in enumerate(actions):
            if i != j:
                if relation[x][y] > Med:
                    inputString += '%d %d\n' % (i+1,j+1)
    circuits = eval(p.communicate(input=inputString.encode('utf-8'))[0])
    if Debug:
        print(circuits)

    result = []
    for x in circuits:
        r = len(x) % 2
        ## if Debug:
        ##     print x, r
        if r != 1:
            oddCircuit = []
            for ino in x[:-1]:
                oddCircuit.append(actions[ino-1])
            result.append( ( oddCircuit, frozenset(oddCircuit) ) )        
    return result

    
# -------------   test pyWrapper
from time import time
from digraphs import *

sampleSize = 10
order = 75
arcProbability = 0.1

fileName = 'testPiping50-10.csv'
fo = open(fileName,'w')
fo.write('# test Piping sampleSize = %d, order = %d, arc probability = %.1f\n' %(sampleSize,order,arcProbability))
fo.write('"piping","nbp","tempfile","nbt"\n')

for s in range(sampleSize):
    print((s+1))
    ## t0 = time()
    #t = RandomCBPerformanceTableau(numberOfActions=25)
    #t = XMCDA2PerformanceTableau('testCpp')
    #g = BipolarOutrankingDigraph(t)
    g = RandomDigraph(order=order,arcProbability=arcProbability)
    #g.showRelationTable()
    ## print("Finished graph construction in ",time()-t0,'sec.')

    t0 = time()
    res = g.computeCppInOutPipingChordlessCircuits(Odd=False)
    ## print('number of odd circuits = ', len(res))
    ## print('Python piping time = ', time() - t0)
    tpipe = time() - t0
    resp = len(res)

    ## t0 = time()
    ## resw = enumWrapper(g,Debug=False)
    ## print('number of odd circuits = ', len(resw))
    ## print('C++/Agrum wrapper time = ', time() - t0)

    ## t0 = time()
    ## res = g.computeChordlessCircuits(Odd=True)
    ## print('number of odd circuits = ', len(res))
    ## print('Python time = ', time() - t0)

    t0 = time()
    res = g.computeCppChordlessCircuits(Odd=False)
    ## print('number of odd circuits = ', len(res))
    ## print('python cpp time = ', time() - t0)
    ttemp = time() - t0
    rest = len(res)

    fo.write('%.5f, %d, %.5f, %d\n' % (tpipe,resp,ttemp,rest))

fo.close

print(('see %s ' % fileName))
