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
    Nsim = 5
    nbrOfActions = 100
    minimalComponentSize=1
    statistics = {'correlation': 0.0, 'determination': 0.0}
    for s in range(Nsim):
        print(s)
        tp = cRandomCBPerformanceTableau(numberOfActions=nbrOfActions,seed=s)
        bg1 = SparseIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                    Threading=MP,Debug=False)
        #bg1.showDecomposition()
        bg2 = SparseIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=100,
                                    Threading=MP,Comments=False,Debug=False)
        #bg2.showDecomposition()
        #bg2._computeQuantileOrdering(Debug=False)
        #print(bg2.components['c1'])
        corr = bg1.computeOrdinalCorrelation(bg2,Debug=False)
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)
    
        
        

   
