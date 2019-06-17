#######################
# R. Bisdorff 
# cOutrankingdigraphs.py module tests for nose
# December 2016
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTests*.py
# # Current $Revision: 1.8 $
########################

from cIntegerOutrankingDigraphs import *
from cSparseIntegerOutrankingDigraphs import *
from cRandPerfTabs import *
from time import time

def testSparseModelFitness():
    print('==>> Testing sparse modeling fitness')
    MP = True
    Nsim = 1
    nbrOfActions = 100
    minimalComponentSize=1
    statistics = {'correlation': 0.0, 'determination': 0.0}
    for s in range(Nsim):
        print(s)
        tp = cRandomCBPerformanceTableau(numberOfActions=nbrOfActions,seed=s)
        bg1 = SparseIntegerOutrankingDigraph(tp,quantiles=4,quantilesOrderingStrategy='average',OptimalQuantileOrdering=True,
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                    Threading=MP,Debug=False)
        bg1.showDecomposition()
        bg2 = IntegerBipolarOutrankingDigraph(tp, Threading=MP,Comments=False,Debug=False)
        # bg2 = SparseIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='optimistic',OptimalQuantileOrdering=False,
        #                         LowerClosed=False,
        #                        minimalComponentSize=100,
        #                             Threading=MP,Comments=False,Debug=False)
        #bg2.showDecomposition()
        #bg2._computeQuantileOrdering(Debug=False)
        #print(bg2.components['c1'])        
        corr = bg2.computeOrdinalCorrelation(bg1)
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)

def testCQRModelFitness():
    print('==>> Testing cQuantilesRanking fitness')
    MP = True
    Nsim = 1
    nbrOfActions = 100
    minimalComponentSize=1
    statistics = {'correlation': 0.0, 'determination': 0.0}
    for s in range(Nsim):
        print(s)
        tp = cRandomCBPerformanceTableau(numberOfActions=nbrOfActions,seed=s)
        bg1 = cQuantilesRankingDigraph(tp,quantiles=4,quantilesOrderingStrategy='optimal',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                    Threading=MP,Debug=False)
        
        bg1.showDecomposition()
        #bg1Ordering = list(reversed(bg1.boostedRanking))
        bg2 = IntegerBipolarOutrankingDigraph(tp, Threading=MP,Comments=False,Debug=False)
        #bg2.showDecomposition()
        #bg2._computeQuantileOrdering(Debug=False)
        #print(bg2.components['c1'])
        corr = bg2.computeOrdinalCorrelation(bg1)
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)

def testEstimateCorrelation():
    print('==>> Testing Correlation estimation fitness')
    import random
    MP = True
    Nsim = 1
    nbrOfActions = 5000
    sampleSize = 200
    minimalComponentSize = 1
    statistics = {'correlation': 0.0, 'determination': 0.0}
    for s in range(Nsim):
        print(s)
        tp = cRandomCBPerformanceTableau(numberOfActions=nbrOfActions,seed=s)
        bg1 = cQuantilesRankingDigraph(tp,quantiles=4,quantilesOrderingStrategy='optimal',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                    Threading=MP,Debug=False)
        
        corr = bg1.estimateRankingCorrelation(sampleSize,s)
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)
