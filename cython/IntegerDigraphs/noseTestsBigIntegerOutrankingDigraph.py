#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsBigOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

from cIntegerOutrankingDigraphs import *
from cBigIntegerOutrankingDigraphs import *
from cRandPerfTabs import Random3ObjectivesPerformanceTableau as cR3ObjPT
#from randomPerfTabs import Random3ObjectivesPerformanceTableau as R3ObjPT
#from outrankingDigraphs import BipolarOutrankingDigraph
from time import time

def testbigOutrankingDigraph():
    print('==>> Testing bigOutrankingDigraph instantiation')
    #from outrankingDigraphs import BipolarOutrankingDigraph
    MP = True
    t0 = time()
    ctp = cR3ObjPT(numberOfActions=100,seed=100)
    #tp = R3ObjPT(numberOfActions=100,seed=100)
    print(time()-t0)
    print(total_size(ctp.evaluation))
    bg1 = BigIntegerOutrankingDigraph(ctp,quantiles=10,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                                CopyPerfTab=True,
                               minimalComponentSize=1,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    t0 = time()
    gi = IntegerBipolarOutrankingDigraph(ctp,Threading=MP)
    #g = BipolarOutrankingDigraph(tp,Normalized=True,Threading=MP)
    print(time()-t0)
    print(total_size(gi))
    t0 = time()
    print("Big outranking digraph's correlation with standard outranking digraph")
    print(bg1.computeOrdinalCorrelation(gi,Debug=False))
    print(time()-t0)

def testMinimalComponentSize():
    print('==>> Testing bigOutrankingDigraph with minimal Component Size instantiation')
    MP = True
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigIntegerOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                                CopyPerfTab=True,
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
                               minimalComponentSize=20,
                                    Threading=MP,Debug=False)
    print(bg2.computeDecompositionSummaryStatistics())
    bg2.showDecomposition(direction="increasing")
    bg2.showDecomposition()
    #bg2.showRelationTable()
    print(bg1.computeOrdinalCorrelation(bg2,Debug=False))
    #bg1.recodeValuation(-1,1,Debug=True)
    print(bg2.computeOrdinalCorrelation(bg2,Debug=False))
    print(bg2)
    bg2.showRelationMap(0,50)

def testBestChoiceRecommendation():
    print('==>> Testing ordinal correlations')
    MP = True
    tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    bg2 = BigIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=10,
                                    Threading=MP,Debug=False)
    t0=time();print(bg2.computeDeterminateness());print(time()-t0,'sec.')
    #bg2.showHTMLRelationMap(0,0,Colored=True)
    bg2.showBestChoiceRecommendation(Comments=False)

def testSparseModelFitness():
    print('==>> Testing sparse modeling fitness')
    MP = True
    Nsim = 2
    nbrOfActions = 300
    nbrOfCriteria = 13
    qTiles = 25
    minimalComponentSize=1
    fileName = 'res3Obj%d.csv' % nbrOfActions
    fo = open(fileName,'w')
    fo.write('"c","d"\n')
    fo.close()
    statistics = {'correlation': 0.0, 'determination': 0.0}
    for s in range(Nsim):
        print(s)
        #tp = RandomCBPerformanceTableau(numberOfActions=nbrOfActions,numberOfCriteria=nbrOfCriteria,seed=s)
        tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrOfActions,numberOfCriteria=nbrOfCriteria)
        tp.showObjectives()
        bg1 = BigIntegerOutrankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                    Threading=MP,Debug=False)
        #bg1.showDecomposition()
        bg2 = BigIntegerOutrankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=nbrOfActions,
                                    Threading=MP,Comments=False,Debug=False)
        #bg2.showDecomposition()
        #bg2._computeQuantileOrdering(Debug=False)
        #print(bg2.components['c1'])
        corr = bg1.computeOrdinalCorrelation(bg2,Debug=False)
        fo = open(fileName,'a')
        fo.write('%.3f,%.3f\n' %(corr['correlation'],corr['determination']))
        fo.close()
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)
    
        
        

   
