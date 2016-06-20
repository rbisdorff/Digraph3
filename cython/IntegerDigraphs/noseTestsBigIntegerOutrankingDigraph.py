#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsBigOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

from digraphs import *
from cBigIntegerOutrankingDigraphs import *
from cRandPerfTabs import *
from time import time

def testbigOutrankingDigraph():
    print('==>> Testing bigOutrankingDigraph instantiation')
    MP = True
    t0 = time()
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=100)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigIntegerOutrankingDigraph(tp,quantiles=10,quantilesOrderingStrategy='average',
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
    nf = bg1.computeBoostedRanking(rankingRule="NetFlows")
    preordering1 = bg1.ranking2Preorder(nf)
    print('Boosted Netflows ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
    ko = bg1.computeBoostedRanking(rankingRule="Kohler")
    preordering2 = bg1.ranking2Preorder(ko)
    print('Boosted Kohler ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering2)))

def testMinimalComponentSize():
    print('==>> Testing bigOutrankingDigraph with minimal Component Size instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigIntegerOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                               minimalComponentSize=5,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    bg1.showRelationTable()
    tp = RandomPerformanceTableau(numberOfActions=200,seed=None)
    #tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    #tp = Random3ObjectivesPerformanceTableau(numberOfActions=200,seed=None)
    bg2 = BigIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=1,
                                    Threading=MP,Debug=False)
    print(bg2.computeDecompositionSummaryStatistics())
    bg2.showDecomposition(direction="increasing")
    #bg2.showRelationTable()
    print(bg1.computeOrdinalCorrelation(bg2,Debug=True))
    #bg1.recodeValuation(-1,1,Debug=True)
    print(bg2.computeOrdinalCorrelation(bg2,Debug=True))
    print(bg2)
    bg2.showRelationMap(0,50)
    bg2.showHTMLRelationMap(0,0,Colored=True)
    t0=time();print(bg2.computeDeterminateness());print(time()-t0,'sec.')

## def testMPComments():
##     print('==>> Testing commented bigOutrankingDigraph construction')
##     MP = True
##     t0 = time()
##     tp = RandomCBPerformanceTableau(numberOfActions=300,Threading=MP,BigData=True)
##     print(time()-t0)
##     print(total_size(tp.evaluation))
##     bg1 = BigOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
##                                  LowerClosed=False,
##                                  minimalComponentSize=5,
##                                  Threading=MP,
##                                  Comments=True,
##                                  Debug=False)
##     print(bg1)
 
## def testRelationMap():
##     print('==>> Testing relation map construction')
##     MP = True
##     t0 = time()
##     tp = RandomCBPerformanceTableau(numberOfActions=300,Threading=MP,BigData=True)
##     bg1 = BigOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
##                                  LowerClosed=False,
##                                  minimalComponentSize=5,
##                                  Threading=MP,
##                                  Comments=True,
##                                  Debug=False)
##     bg1.showRelationMap(fromIndex=0,toIndex=50,
##                         symbols = {'max':'┬','positive': '+', 'median': ' ',
##                                'negative': '-', 'min': '┴'} )
   
