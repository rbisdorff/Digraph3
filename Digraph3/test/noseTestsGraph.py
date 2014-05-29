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
    g = RandomGraph(order=7,edgeProbability=0.5)
    dg = g.graph2Digraph()
    dg.showShort()
    dg.showRelationTable()
    dg.exportGraphViz('testDigraphViz')
    dg.showStatistics()

def testRandomTree():
    g = RandomTree(order=30)
    print(g.depthFirstSearch(Debug=True))
    g.exportGraphViz('testTreeViz')
    for x in g.vertices:
        print(x, g.vertices[x]['startDate'], g.vertices[x]['endDate'])

def testQColoring():
    g = GridGraph(n=6,m=6)
    g.showShort()
    qc = Q_Coloring(g,colors=['gold','lightblue','lightcoral'],Debug=False)
    qc.checkFeasibility(Comments=True)
    qc.exportGraphViz()
