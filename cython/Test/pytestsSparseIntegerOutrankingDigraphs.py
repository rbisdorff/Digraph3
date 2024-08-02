#######################
# R. Bisdorff 2016
# cythonized OutrankingDigraphs tests for nose
# (..$ pip3 install pytest  # installing the pytest environment)
# ..$ pytest -vs pytestTestsSparseOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

# if __name__ == '__main__':
#     from sys import platform
#     if platform == 'darwin':
#         print('start_method set to fork')
#         from multiprocessing import set_start_method, get_start_method, freeze_support
#         set_start_method('fork')
#         print(get_start_method())
#         freeze_support()


from cIntegerOutrankingDigraphs import *
from cSparseIntegerOutrankingDigraphs import *
from cRandPerfTabs import *
from time import time

def testSparseOutrankingDigraph():
    print('==>> Testing SparseOutrankingDigraph instantiation')
    MP = False
    t0 = time()
    ctp = cRandom3ObjectivesPerformanceTableau(numberOfActions=100,seed=100)
    print(ctp)
    print(time()-t0)
    print(total_size(ctp.evaluation))
    bg1 = SparseIntegerOutrankingDigraph(ctp,quantiles=10,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                                CopyPerfTab=True,
                               minimalComponentSize=1,
                                    Threading=MP,Debug=False,
                                      Comments=True)
    print(bg1)
    print(bg1.computeCopelandRanking())
    print(bg1.computeCopelandOrder())
    print(bg1.computeNetFlowsRanking())
    print(bg1.computeNetFlowsOrder())
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    t0 = time()
    gi = IntegerBipolarOutrankingDigraph(ctp,Threading=MP)
    print(time()-t0)
    print(total_size(gi))
    t0 = time()
    print("Sparse outranking digraph's correlation with standard outranking digraph")
    print(bg1.computeOrdinalCorrelation(gi,Debug=False))
    print(time()-t0)
    print(bg1.computeCopelandRanking())
    print(bg1.computeCopelandOrder())
    print(bg1.computeNetFlowsRanking())
    print(bg1.computeNetFlowsOrder())

def testMinimalComponentSize():
    print('==>> Testing SparseOutrankingDigraph with minimal Component Size instantiation')
    MP = False
    t0 = time()
    tp = cRandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = SparseIntegerOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
                                LowerClosed=True,
                                CopyPerfTab=True,
                               minimalComponentSize=5,
                                    Threading=MP,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    bg1.showRelationTable()
    tp = cRandomPerformanceTableau(numberOfActions=200,seed=None)
    print(tp.criteria)
    bg2 = SparseIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=20,
                                    Threading=MP,Debug=False)
    print(bg2.computeDecompositionSummaryStatistics())
    bg2.showDecomposition(direction="increasing")
    bg2.showDecomposition()
    print(bg1.computeOrdinalCorrelation(bg2,Debug=False))
    print(bg2.computeOrdinalCorrelation(bg2,Debug=False))
    print(bg2)
    bg2.showRelationMap(0,50)

def testBestChoiceRecommendation():
    print('==>> Testing ordinal correlations')
    MP = True
    tp = cRandomCBPerformanceTableau(numberOfActions=200,Threading=MP,seed=None)
    print(tp)
    bg2 = SparseIntegerOutrankingDigraph(tp,quantiles=35,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=10,
                                    Threading=MP,
                                         tempDir='.',
                                         Debug=False)
    t0=time();print(bg2.computeDeterminateness());print(time()-t0,'sec.')
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
    seed = 0
    for s in range(Nsim):
        s += 1
        print(s)
        tp = cRandom3ObjectivesPerformanceTableau(numberOfActions=nbrOfActions,numberOfCriteria=nbrOfCriteria,seed=s)
        print(tp)
        tp.showObjectives()
        bg1 = SparseIntegerOutrankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                             Threading=MP,tempDir='.',Debug=False)
        bg2 = SparseIntegerOutrankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=nbrOfActions,
                                             Threading=MP,tempDir='.',Comments=False,Debug=False)
        corr = bg1.computeOrdinalCorrelation(bg2,Debug=False)
        fo = open(fileName,'a')
        fo.write('%.3f,%.3f\n' %(corr['correlation'],corr['determination']))
        fo.close()
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)

def testcQuantilesRankingFitness():
    print('==>> Testing cQuantilesRanking fitness')
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
        tp = cRandom3ObjectivesPerformanceTableau(numberOfActions=nbrOfActions,numberOfCriteria=nbrOfCriteria)
        tp.showObjectives()
        bg1 = cQuantilesRankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                                CopyPerfTab=True,
                               minimalComponentSize=minimalComponentSize,
                                       Threading=MP,tempDir='.',Debug=False)
        print(bg1)
        bg2 = cQuantilesRankingDigraph(tp,quantiles=qTiles,quantilesOrderingStrategy='average',
                                LowerClosed=False,
                               minimalComponentSize=nbrOfActions,
                                       Threading=MP,tempDir='.',Comments=False,Debug=False)
        print(bg2)
        corr = bg1.computeOrdinalCorrelation(bg2,Debug=False)
        fo = open(fileName,'a')
        fo.write('%.3f,%.3f\n' %(corr['correlation'],corr['determination']))
        fo.close()
        statistics['correlation'] += corr['correlation']
        statistics['determination'] += corr['determination']
    statistics['correlation'] /= Nsim
    statistics['determination'] /= Nsim
    print(statistics)

        
        

   
