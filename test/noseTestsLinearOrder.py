#######################
# R. Bisdorff 
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsVotingDigraph.py
# # Current $Revision: 1.7 $
########################

from digraphs import *
from perfTabs import *
from linearOrders import *
from decimal import Decimal

def testExtendedPrudentDigraph():
    print('*-------- Testing ExtendedPrudentDigraph class -------')
    t = RandomCBPerformanceTableau(numberOfActions=13)
    t.save('testExtPrud')
    g = BipolarOutrankingDigraph(t)
    level = g.computePrudentBetaLevel(Debug=True)
    gep = ExtendedPrudentDigraph(g,prudentBetaLevel=level,Debug=True)
    gep.showRelationTable()


def testRankedPairsOrdering():
    print('*-------- Testing RankedPairsOrder class -------')
    t = RandomPerformanceTableau(numberOfActions=5)
    t.save()
    t.showPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    rp = RankedPairsOrder(g,isExtendedPrudent=False,Debug=True)
    rp.showRelationTable()
    eprp = RankedPairsOrder(g,isExtendedPrudent=True,Debug=True)
    eprp.showRelationTable()
    eprp.exportGraphViz('testorder')
    eprp.exportDigraphGraphViz('testdigraph')

def testKohlerOrdering():
    print("*==>> testing KohlerOrder Class ----*")
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.saveXMCDA2('testkohler')
    g = BipolarOutrankingDigraph(t)
    #g.showRelationTable()
    k = KohlerOrder(g,Debug=True)
    print(k.computeOrder())

def testNetFlowsOrdering():
    print("*==>> testing NetFlowsOrder Class ----*")
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.saveXMCDA2('testkohler')
    g = BipolarOutrankingDigraph(t)
    #g.showRelationTable()
    nfo = NetFlowsOrder(g,coDual=False,Debug=True)
    print(nfo.computeOrder())

def testRandomLinearOrders():
    print("*==>> testing RandomLinearOrder Class ----*")
    g1 = RandomLinearOrder(numberOfActions=10,Debug=True)
    g1.showRelationTable()
    g2 = RandomLinearOrder(numberOfActions=10,Debug=True)
    g2.showRelationTable()
    print(g1.computeBipolarCorrelation(g2))
    g1 = RandomLinearOrder(numberOfActions=10,OutrankingModel=True,Debug=True)
    g1.showRelationTable()
    g2 = RandomLinearOrder(numberOfActions=10,OutrankingModel=True,Debug=True)
    g2.showRelationTable()
    print(g1.computeBipolarCorrelation(g2))
