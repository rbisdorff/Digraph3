#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsBigOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

from digraphs import *
from bigOutrankingDigraphs import *
from time import time

def testbigOutrankingDigraph():
    print('==>> Testing bigOutrankingDigraph instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=100,Threading=MP)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigOutrankingDigraphMP(tp,quantiles=10,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                               minimalComponentSize=None,
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
    nf = bg1.computeBoostedNetFlowsOrder()
    preordering1 = bg1.ordering2Preorder(nf)
    print('Boosted Netflows ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
    ko = bg1.computeBoostedKohlerOrder()
    preordering2 = bg1.ordering2Preorder(ko)
    print('Boosted Kohler ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering2)))
    rp = bg1.computeBoostedRankedPairsOrder()
    preordering3 = bg1.ordering2Preorder(rp)
    print('Boosted Ranked Pairs ranking correlation with complete outranking relation')
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering3)))

def testMinimalComponentSize():
    print('==>> Testing bigOutrankingDigraph with minimal Component Size instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigOutrankingDigraphMP(tp,quantiles=5,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=5,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    bg1.showRelationTable()
    bg2 = BigOutrankingDigraphMP(tp,quantiles=50,quantilesOrderingStrategy='average',
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
    

