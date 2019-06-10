#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsBigOutrankingDigraph.py
########################

from digraphs import *
from sparseOutrankingDigraphs import *
from time import time

def testSparseOutrankingDigraph():
    print('==>> Testing SparseOutrankingDigraph instantiation')
    MP = True
    t0 = time()
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=100,
                                             BigData=True)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=10,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                               minimalComponentSize=1,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    t0 = time()
    g = BipolarOutrankingDigraph(tp,Normalized=True,Threading=MP)
    print(time()-t0)
    print(total_size(g))
    t0 = time()
    print("Big outranking digraph's correlation with standard outranking digraph")
    print(bg1.computeOrdinalCorrelation(g,Debug=False))
    print(time()-t0)
    nf = bg1.computeBoostedOrdering(orderingRule="NetFlows")
    preordering1 = bg1.ordering2Preorder(nf)
    print(nf,preordering1)
    print('Boosted Netflows ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
    ko = bg1.computeBoostedOrdering(orderingRule="Kohler")
    preordering2 = bg1.ordering2Preorder(ko)
    print(ko,preordering2)
    print('Boosted Kohler ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering2)))

def testMinimalComponentSize():
    print('==>> Testing PreRankedOutrankingDigraph with minimal Component Size instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=200,BigData=True,Threading=MP)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=5,
                                     quantilesOrderingStrategy='average',
                                    OptimalQuantileOrdering=True,
                                LowerClosed=False,
                               minimalComponentSize=5,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    bg1.showRelationTable()
    #tp = RandomCBPerformanceTableau(numberOfActions=200,BigData=True,Threading=MP)
    bg2 = PreRankedOutrankingDigraph(tp,quantiles=50,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                               minimalComponentSize=1,
                                    Threading=MP,Debug=False)
    print(bg2.computeDecompositionSummaryStatistics())
    bg2.showDecomposition()
    bg2.showRelationTable()
    print(bg1.computeOrdinalCorrelation(bg2,Debug=False))
    bg1.recodeValuation(-10,10,Debug=True)
    print(bg2.computeOrdinalCorrelation(bg1,Debug=False))
    print(bg2)

def testMPComments():
    print('==>> Testing commented PreRankedOutrankingDigraph construction')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=300,Threading=MP)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=20,quantilesOrderingStrategy='average',
                                 LowerClosed=False,
                                 minimalComponentSize=5,
                                 Threading=MP,
                                 Comments=True,
                                 Debug=False)
    print(bg1)
 
def testRelationMap():
    print('==>> Testing relation map construction')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=300,Threading=MP)
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=20,quantilesOrderingStrategy='average',
                                 LowerClosed=False,
                                 minimalComponentSize=5,
                                 Threading=MP,
                                 Comments=True,
                                 Debug=False)
    bg1.showRelationMap(fromIndex=0,toIndex=50,
                        symbols = {'max':'┬','positive': '+', 'median': ' ',
                               'negative': '-', 'min': '┴'} )
    bg1.showHTMLRelationMap(actionsSubset=bg1.boostedRanking)

def testActionRankOrder():
    print('==>> Testing action rank and order methods')
    MP = True
    tp = RandomCBPerformanceTableau(numberOfActions=100,Threading=MP)
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=10,quantilesOrderingStrategy='average',
                                 LowerClosed=False,
                                 minimalComponentSize=10,
                                 Threading=MP,
                                 Comments=False,
                                 Debug=False)
    rkg = bg1.boostedRanking
    assert bg1.actionRank(rkg[0],ranking=rkg) == 1, "error in actionRank fct"
    assert bg1.actionOrder(rkg[99],ordering=rkg) == 100, "error in actionOrder fct"

def testexportSortingGraphViz():
    print('==>> Testing graph viz export of sorting Hasse diagram')
    MP  = True
    nbrActions=100
    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,Threading=MP,
                                      seed=100)
    bg1 = PreRankedOutrankingDigraph(tp,CopyPerfTab=True,quantiles=20,
                                 quantilesOrderingStrategy='average',
                                 componentRankingRule='Copeland',
                                 LowerClosed=False,
                                 minimalComponentSize=1,
                                 Threading=MP,nbrOfCPUs=8,
                                 #tempDir='.',
                                 nbrOfThreads=8,
                                 Comments=False,Debug=False,
                                 save2File='testbgMP')
    print(bg1)
    bg1.showComponents()
    bg1.exportSortingGraphViz(actionsSubset=bg1.boostedRanking[:100])     
    
def testPreRankedConfidentOutrankingDigraph():
    print('==>> Testing PreRankedConfidentOutrankingDigraph ')
    MP  = True
    nbrActions=100
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions)
##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,Threading=MP)
##                                      seed=100)
    bg1 = PreRankedConfidentOutrankingDigraph(tp,CopyPerfTab=True,quantiles=5,
                                 quantilesOrderingStrategy='average',
                                 componentRankingRule='Copeland',
                                 LowerClosed=True,
                                 minimalComponentSize=1,
                                 Threading=False,nbrOfCPUs=8,
                                 #tempDir='.',
                                 nbrOfThreads=8,
                                 Comments=False,Debug=False,
                                 save2File='testbgMP')
    print(bg1)
    bg1.showComponents(direction='descending')
    bg1.showRelationMap()

def testConfidentVersusStdPreRankedOutrankingDigraph():
    print('==>> Testing confident versus standard PreRanked vesrion')
    MP  = True
    nbrActions=100
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions)
##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,Threading=MP)
##                                      seed=100)
    bg1 = PreRankedConfidentOutrankingDigraph(tp,CopyPerfTab=True,quantiles=5,
                                 quantilesOrderingStrategy='average',
                                 componentRankingRule='Copeland',
                                 LowerClosed=False,
                                 minimalComponentSize=1,
                                 Threading=False,nbrOfCPUs=4,
                                 #tempDir='.',
                                 nbrOfThreads=4,
                                 Comments=False,Debug=False,
                                 save2File='testbgconf')
    print(bg1)
    bg1.showComponents(direction='descending')
    bg2 = PreRankedOutrankingDigraph(tp,CopyPerfTab=True,quantiles=5,
                                 quantilesOrderingStrategy='average',
                                 componentRankingRule='Copeland',
                                 LowerClosed=False,
                                 minimalComponentSize=1,
                                 Threading=False,nbrOfCPUs=4,
                                 #tempDir='.',
                                 nbrOfThreads=4,
                                 Comments=False,Debug=False,
                                 save2File='testbgstd')
    print(bg2)
    bg2.showComponents(direction='descending')
    from weakOrders import WeakRankingOrder
    wr = WeakRankingOrder(bg1,[bg1.boostedRanking,bg2.boostedRanking])
    wr.exportGraphViz('fusion-cpr-pr',graphType="pdf")
