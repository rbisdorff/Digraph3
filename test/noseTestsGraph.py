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
    p.exportGraphViz(withSpanningTree=True)
    print(p.dfs)
    spt = RandomSpanningForest(p,seed=1)
    print(spt.dfs)
    spt.exportGraphViz()

def testRandomSpanningTree():
    print('==>> Testing RandomSpanningTree class instantiation')
    p = RandomGraph(order=10,edgeProbability=0.5,seed=100)
    ust = RandomSpanningTree(p,seed=1)
    print(ust.dfs)
    ust.exportGraphViz(withSpanningTree=True)

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
    mt.exportGraphViz(layout="circo")

    
