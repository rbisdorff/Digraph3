#######################
# R. Bisdorff 
# weakOrders.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsWeakOrders.py
# # Current $Revision: $
########################

from outrankingDigraphs import *
from weakOrders import *
from time import time

def testRankingByChoosingWithKernels():
    print('=== >>> testing best and last fusion (default)')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rcg0 = RankingByChoosingDigraph(g,Debug=False)
    rcg0.showWeakOrder()
    rcg0.showRankingByChoosing()
    print(rcg0.computeOrdinalCorrelation(g))
    print('=== >>> best') 
    rcg1 = RankingByBestChoosingDigraph(g,Debug=False)
    rcg1.showWeakOrder()
    print(rcg1.computeOrdinalCorrelation(g))
    print('=== >>> last')
    rcg2 = RankingByLastChoosingDigraph(g,Debug=False)
    rcg2.showWeakOrder()
    rcg2.exportGraphViz(direction="worst")
    print(rcg2.computeOrdinalCorrelation(g))

def testOrderedRelationTableShowing():
    print('=== >>> testing ordered relation tables showing')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rbc = RankingByChoosingDigraph(g,Debug=False)
    rbc.showOrderedRelationTable()
    rbc.showOrderedRelationTable(direction='increasing')
    
def testPrincipalInOutDegreesRanking():
    print('=== >>> principal preorder')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rcf = PrincipalInOutDegreesOrdering(g,imageType="pdf",Debug=False)
    rcf.showWeakOrder()
    print(rcf.computeOrdinalCorrelation(g))
    rcf.exportGraphViz(direction="Colwise")

def testRBCThreadingOptions():
    print('===>>> test threading option')
    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                 numberOfActions=5)
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    print('=== >>> best and last fusion (default)')
    t0 = time()
    rcg0 = RankingByChoosingDigraph(g,\
                                                     fusionOperator="o-min",\
                                                     Debug=False,\
                                                     Threading=False)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcg0.showWeakOrder()
    t0 = time()
    rcg1 = RankingByChoosingDigraph(g,\
                                                     fusionOperator="o-min",\
                                                     Debug=False,\
                                                     Threading=True)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcg1.showWeakOrder()

def testPRIThreadingOptions():
    print('===>>> test threading option')
    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                 numberOfActions=10)
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    t0 = time()
    rcf1 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
                                           imageType=None,Debug=False,
                                           Threading=False)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcf1.showWeakOrder()
    t0 = time()
    rcf2 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
                                           imageType=None,Debug=False,\
                                           Threading=True)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcf2.showWeakOrder()
