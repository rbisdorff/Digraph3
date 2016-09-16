#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsBigOutrankingDigraph.py
# # Current $Revision: 1.8 $
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
    print('Boosted Netflows ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
    ko = bg1.computeBoostedOrdering(orderingRule="Kohler")
    preordering2 = bg1.ordering2Preorder(ko)
    print('Boosted Kohler ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering2)))

def testMinimalComponentSize():
    print('==>> Testing PreRankedOutrankingDigraph with minimal Component Size instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=200,BigData=True,Threading=MP)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = PreRankedOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=5,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    bg1.showRelationTable()
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
