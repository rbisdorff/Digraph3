#######################
# R. Bisdorff
# graphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsGraphs.py
# # Current $Revision:  $
########################
from graphs import *

def testGridGraph():
    print('==>> Testing GridGraph instantiation')
    g = GridGraph(n=4,m=4)
    g.showShort()

def testSnakeGraph():
    print('==>> Testing SnakeGraph instantiation')
    s = SnakeGraph(p=4,q=7)
    s.showShort()
    s.exportGraphViz('4_7_snake',lineWidth=3,arcColor="red")

def testGraph():
    print('==>> Testing Graph instantiation')
    g = RandomGraph(order=7,edgeProbability=0.5)
    g.save('testGraph')
    gs = Graph('testGraph')
    g.showShort()
    gs.showShort()
    g.computeChordlessCycles(Comments=True,Debug=True)
    g._saveEdges(Agrum=True)
    g.exportGraphViz('testGraphViz')
    print(g.computeNeighbourhoodDepthDistribution(Debug=False))
    for v in g.vertices:
        print(v,g.computeNeighbourhoodDepth(v))
    print(g.isConnected(), g.computeComponents())
    g.exportGraphViz()
    print('diameter: ',g.computeDiameter())
    g.showMIS()
    g.showCliques()

def testRandomGraphs():
    print('==>> Testing Random Graph instantiations')
    g = RandomFixedDegreeSequenceGraph(seed=100)
    g.showShort()
    g.exportGraphViz('testRandomFixedDegreeSequence')
    rg = RandomRegularGraph(seed=100)
    rg.showShort()
    rg.exportGraphViz('testRandomRegularGraph')
    rfs = RandomFixedSizeGraph(seed=100,Debug=True)
    rfs.showShort()
    rfs.exportGraphViz()

def testGraph2Digraph():
    print('==>> Testing Graph2Digraph coversion')
    g = RandomGraph(order=7,edgeProbability=0.5)
    dg = g.graph2Digraph()
    dg.showShort()
    dg.showRelationTable()
    dg.exportGraphViz('testDigraphViz')
    dg.showStatistics()

def testRandomTree():
    print('==>> Testing RandomTree class instantiation')
    g = RandomTree(order=30)
    print(g.depthFirstSearch(Debug=True))
    g.exportGraphViz('testTreeViz')
    for x in g.vertices:
        print(x, g.vertices[x]['startDate'], g.vertices[x]['endDate'])

def testQColoring():
    print('==>> Testing Q_Coloring class instantiation')
    g = GridGraph(n=6,m=6)
    g.showShort()
    qc = Q_Coloring(g,nSim=1000,colors=['gold','lightblue','lightcoral'],Debug=False)
    qc.checkFeasibility(Comments=True)
    qc.exportGraphViz()

def testIsingModel():
    print('==>> Testing Ising Model class instantiation')
    g = GridGraph(n=15,m=15)
    g.showShort()
    im = IsingModel(g,beta=0.3,nSim=100000,Debug=False)
    im.exportGraphViz(colors=['lightblue','lightcoral'])

def testMISModel():
    print('==>> Testing MIS Model class instantiation')
    g = Graph(numberOfVertices=20,edgeProbability=0.075)
    g.showShort()
    g.showMIS()
    im = MISModel(g,nSim=10000,Debug=False)
    im.checkMIS(Comments=True)
    print('MIS       = ',im.mis)
    print('Covered   = ',im.misCover)
    print('Uncovered = ',im.unCovered)
    print('MIS size  = ',len(im.mis))
    im.exportGraphViz(misColor='coral')
    im.save()

def testMetropolisChain():
    print('==>> Testing Metropolis chain class instantiation')
    g = Graph(numberOfVertices=30,edgeProbability=0.2)
    #g.save('test')
    probs = {}
    n = g.order
    i = 0
    verticesList = [x for x in g.vertices]
    verticesList.sort()
    for x in verticesList:
        probs[x] = (n - i)/(n*(n+1)/2)
        i += 1
    met = MetropolisChain(g,probs)
    frequency = met.checkSampling(verticesList[0],nSim=30000)
    for x in verticesList:
        try:
            print(x,probs[x],frequency[x])
        except:
            print(x,0.0,0.0)
    met.showTransitionMatrix()
    met.saveCSVTransition()

def testTriangulatedGrid():
    print('==>> Testing TriangulatedGrid class instantiation')
    g = TriangulatedGrid(n=15,m=15)
    im = IsingModel(g,beta=0.441,nSim=30000,Debug=False)
    H = im.computeSpinEnergy()
    print( 'Spin energy = %d/%d = %.3f' % (H,im.size,H/im.size) )
    print(im.SpinEnergy)
    im.exportGraphViz(edgeColor='lightgrey',graphSize="(5,5)",graphType="pdf",colors=['gold','coral'])

def testRandomSpanningForest():
    print('==>> Testing RandomSpanningForest class instantiation')
    p = RandomGraph(order=10,edgeProbability=0.1,seed=100)
    p.randomDepthFirstSearch(seed=1)
    p.exportGraphViz(WithSpanningTree=True)
    print(p.dfs)
    spt = RandomSpanningForest(p,seed=1)
    print(spt.dfs)
    spt.exportGraphViz()

def testRandomSpanningTree():
    print('==>> Testing RandomSpanningTree class instantiation')
    p = RandomGraph(order=10,edgeProbability=0.5,seed=100)
    ust = RandomSpanningTree(p,seed=1)
    print(ust.dfs)
    ust.exportGraphViz(WithSpanningTree=True)

def testRandomGraphsModels():
    print('==>> Testing random graph models')
    c = CycleGraph()
    c.showShort()
    g = RandomGraph(seed=100)
    g.showShort()
    g = RandomFixedDegreeSequenceGraph(seed=100)
    g.showShort()
    rg = RandomRegularGraph(seed=100)
    rg.showShort()
    rfs = RandomFixedSizeGraph(order=5,size=7,seed=100,Debug=True)
    rfs.showShort()

def testBestDeterminedSpanningForest():
    print('==>> Testing BestDeterminedSpanningForest class instantiation')
    g = RandomValuationGraph(order=5,seed=202)
    g.save()
    g.exportGraphViz()
    mt = BestDeterminedSpanningForest(g,Debug=True)
    print(mt)
    mt.exportGraphViz(layout="circo")

def testLineGraphs():
    print('==>> Testing line graphs construction')
    g = CycleGraph(order=6)
    print(g)
    g.showShort()
    lg = LineGraph(g)
    print(lg)
    lg.exportGraphViz('testLineGraph')
    lg.showShort()
    llg = LineGraph(lg)
    print(llg)
    llg.showShort()
    lg.showMIS()
    maxMatching = g.computeMaximumMatching(Comments=False)
    g.exportGraphViz(layout='circo',matching=maxMatching)

def testPermutationGraphs():
    print('==>> Testing permutation graphs construction')
    g = PermutationGraph(permutation=[4,3,6,1,5,2])
    print(g)
    g.exportGraphViz()
    g.exportPermutationGraphViz()
    g.computeMinimalVertexColoring(Comments=True,Debug=True)
    g.exportGraphViz(WithVertexColoring=True)
    g.exportPermutationGraphViz(WithEdgeColoring=True)
    rg = RandomPermutationGraph(order=6,seed=100)
    print(rg)
    print('permutation:',rg.computePermutation())
    dg = g.transitiveOrientation()
    print(dg)
    dg.exportGraphViz()
    rgd = -rg
    print(rgd)

def testGraphOrientations():
    print('==>> Testing graph orientations')
    g = RandomGraph(order=6,edgeProbability=0.5,seed=100)
    og = g.computeOrientedDigraph()
    print('Transitivity degree: %.3f' % og.transitivityDegree)
    gd = -g
    ogd = gd.computeOrientedDigraph()
    print('Dual transitivity degree: %.3f' % ogd.transitivityDegree)

def testGraphTransitiveOrientations():
    from digraphs import FusionDigraph
    print('==>> Testing graph orientations')
    g = RandomGraph(order=8,edgeProbability=0.4,seed=4335)
    print(g)
    #g = CycleGraph(order=7)
    g.exportGraphViz('testg')
    og = g.computeTransitivelyOrientedDigraph(PartiallyDetermined=True)
    if og != None:
        print(og)
        print('Transitivity degree: %.3f' % og.transitivityDegree)
    gd = -g
    ogd = gd.computeTransitivelyOrientedDigraph(PartiallyDetermined=True)
    if ogd != None:
        print(ogd)
        print('Dual transitivity degree: %.3f' % ogd.transitivityDegree)
    fog = FusionDigraph(og,ogd,operator='o-max')
    s1 = fog.computeCopelandRanking()
    fogd = FusionDigraph((-og),ogd,operator='o-max')
    s2 = fogd.computeCopelandRanking()
    print(s1)
    print(s2)
    permutation = g.computePermutation(s1,s2)
    print(permutation)
    pga = PermutationGraph(permutation)
    pga.exportGraphViz('testpga')
    pgb = PermutationGraph(permutation=[5, 2, 4, 1, 6, 7, 8, 3])
    pgb.exportGraphViz('testpgb')
    pgc = PermutationGraph(permutation=[4, 2, 8, 3, 1, 5, 6, 7])
    pgc.exportGraphViz('testpgc')
    pgd = PermutationGraph(permutation=[6, 1, 2, 3, 8, 5, 7, 4])
    pgd.exportGraphViz('testpgd')

def testIntervalGraphs():
    print('==>> Testing interval graph property')
    g = RandomGraph(order=8,edgeProbability=0.4,seed=4335)
    print(g)
    print(g.isTriangulated())
    print((-g).isComparabilityGraph())
    print(g.isIntervalGraph(Comments=True))
    print(g.isSplitGraph(Comments=True))
    print(g.isPermutationGraph(Comments=True))

def testIntervalIntersectionsGraphs():
    print('==>> Testing split graph property')
    g = RandomIntervalIntersectionsGraph(order=8)
    print(g)
    print(g.intervals)
    print(g.isIntervalGraph(Comments=True))
    print(g.isSplitGraph(Comments=True))

def testBreadthFirstSearch():
    print('==>> Testing breadth first search algorithm')
    g = RandomGraph(order=8)
    g.save('testbfs')
    g = Graph('testbfs')
    g.exportGraphViz()
    print(g.breadthFirstSearch('v1',Debug=True))

def testPerfectGraphDetection():
    print('==>> Testing perfect graph property detection')
    g = RandomGraph(order=15,edgeProbability=0.5)
    g.save('testperf')
    g.exportGraphViz('perfect')
    print('Graph %s is perfect ? %s' %\
          ('testperf',str(g.isPerfectGraph(Comments=False))) )    

def testGraphGirthComputation():
    print('==>> Testing graph (odd and even) girth computation')
    g = RandomGraph(order=9,edgeProbability=0.5)
    print(g.isPerfectGraph(Comments=True))
    g.computeGirth(girthType="odd",Comments=True)
    g.computeGirth(girthType="even",Comments=True)
    g.computeGirth(Comments=True)
