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
    MP = False
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=100,Threading=MP,
                                      seed=100)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigOutrankingDigraph(tp,quantiles=10,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                               minimalComponentSize=1,
                                    Threading=False,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    t0 = time()
    g = BipolarOutrankingDigraph(tp,Normalized=True,Threading=MP)
    print(time()-t0)
    print(total_size(g))
    t0 = time()
    print(bg1.computeOrdinalCorrelation(g,Debug=False))
    print(time()-t0)
    preordering1 = bg1.computeRankingPreordering()
    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))

