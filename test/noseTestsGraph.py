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
    g.saveEdges(Agrum=True)
    g.exportGraphViz('testGraphViz')

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
    g = Graph(numberOfVertices=30,edgeProbability=0.075)
    g.showShort()
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

def testTriangularGraph():
    print('==>> Testing TriangularGraph class instantiation')
    g = TriangularGraph(n=15,m=15)
    im = IsingModel(g,beta=0.441,nSim=30000,Debug=False)
    H = im.computeSpinEnergy()
    print( 'Spin energy = %d/%d = %.3f' % (H,im.size,H/im.size) )
    print(im.SpinEnergy)
    im.exportGraphViz(edgeColor='lightgrey',graphSize="(5,5)",graphType="pdf",colors=['gold','coral'])

