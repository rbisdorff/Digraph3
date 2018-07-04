#######################
# R. Bisdorff 
# Digraphs3 modules tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsRandomPerfTab.py
# # Current $Revision: 1.0 $
##################################################

from digraphs import *
from outrankingDigraphs import *
from decimal import Decimal
from weakOrders import *
from randomPerfTabs import *
from randomPerfTabs import _RandomS3PerformanceTableau\
     as RandomS3PerformanceTableau
from randomPerfTabs import _FullRandomPerformanceTableau as\
     FullRandomPerformanceTableau
from randomPerfTabs import _RandomCoalitionsPerformanceTableau as\
     RandomCoalitionsPerformanceTableau

def testRandomPerformanceTableau():
    print('==>> Testing Random Performance Tableau instantiation')
    t = RandomPerformanceTableau(numberOfActions=10,
                                 numberOfCriteria=7,
                                 commonMode=('normal',50,20),
                                 seed=100)
    t.showAll()
    print(t)
    print(t.computeWeightedAveragePerformances(isNormalized=True,
                                               lowValue=0.0,highValue=20.0))
    t1 = RandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('triangular',30,0.5),
                                 seed=1)
    t1.showStatistics()
    t2 = RandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('beta',None,None),
                                 seed=None)
    t2.showStatistics()
    t3 = RandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('beta',None,None),
                                 seed=1)
    g1 = BipolarOutrankingDigraph(t1,Normalized=True)
    g2 = BipolarOutrankingDigraph(t3,Normalized=True)
    corr= g1.computeOrdinalCorrelation(g2)
    print('==>',corr)
    assert corr['correlation'] != Decimal('1'), 'seed on RandomPerformance not OK !' 
    
def testRandomRankPerformanceTableau():
    print('==>> Testing Random Rank Performance Tableau instantiation')
    t = RandomRankPerformanceTableau(numberOfActions=10,
                                 numberOfCriteria=7,
                                 seed=100)
    t.showAll()
    print(t)
    print(t.computeWeightedAveragePerformances(isNormalized=True,
                                               lowValue=0.0,highValue=20.0))
    t1 = RandomRankPerformanceTableau(weightScale=(1,10),
                                     weightDistribution='random',
                                 seed=10)
    t1.showStatistics()

def testFullRandomPerformanceTableau():
    print('==>> Testing Full Random Performance Tableau instantiation')
    t = FullRandomPerformanceTableau(numberOfActions=10,
                                 numberOfCriteria=7,
                                 seed=100)
    t.showAll()
    print(t)
    print(t.computeWeightedAveragePerformances(isNormalized=True,
                                               lowValue=0.0,highValue=20.0))
    t = FullRandomPerformanceTableau(weightScale=(1,10),
                                 commonMode=('triangular',30,0.5),
                                 seed=None)
    t.showStatistics()
    t = FullRandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('beta',None,None),
                                 seed=None)
    t.showStatistics()


    
def testCBPerformanceTableau(): 
    print('*==>> random CB Performance Tableaux ------------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,\
                                   commonPercentiles={'ind':0.05,'pref':0.10,'veto':0.95},\
                                   weightDistribution="random",\
                                   weightScale=[1,2],\
                                   integerWeights=True,\
                                   commonMode=["normal",50.0,25.0],
                                   missingDataProbability=0.5,
                                   seed=100,Debug=True)
    print(t)
    t.saveXMCDA(fileName='randomPerformanceTableau',servingD3=False)
    t.showCriteria(Debug=False)
    t.showStatistics(Debug=True)
    t.showPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    g.exportGraphViz()

def testmpCBPerformanceTableau(): 
    print('*==>> random paraell CB Performance Tableaux ------------*')
    
    t = RandomCBPerformanceTableau(numberOfActions=10,\
                                   commonPercentiles={'ind':0.05,'pref':0.10,'veto':0.95},\
                                   weightDistribution="random",\
                                   weightScale=[1,2],\
                                   integerWeights=True,\
                                   commonMode=["normal",50.0,25.0],
                                   missingDataProbability=0.5,
                                   seed=100,Debug=True,
                                   Threading=True)
    t.showCriteria(Debug=False)
    t.showStatistics(Debug=True)

def test3ObjectivesPerformanceTableau():
    print('*==>> random 3 Objectives (Eco, Soc, Env) Performance Tableaux ------------*')
    t = Random3ObjectivesPerformanceTableau(numberOfActions=21,\
                            numberOfCriteria=13,\
                            commonScale=[0.0,50.0],\
                            commonThresholds = ((5.0,0.0),(10.0,0.0),(80.0,0.0)),
                            commonMode=['triangular','variable',0.5])
    print(t)
    t.saveXMCDA2('testY',servingD3=False)
    t.showCriteria(IntegerWeights=True)
    g = BipolarOutrankingDigraph(t)
    rbc = RankingByChoosingDigraph(g)
    rbc.showRankingByChoosing()

def testCoalitionsPerformanceTableau():
    print('*==>> random Coalitions Performance Tableaux ------------*')
    t = RandomCoalitionsPerformanceTableau(numberOfActions=13,\
                            numberOfCriteria=21,\
                            Coalitions=False,\
                            RandomCoalitions=True,\
                            commonScale=[0.0,50.0],\
                            commonThresholds = ((5.0,0.0),(10.0,0.0),(80.0,0.0)),
                            weightDistribution="equicoalitions")
    print(t)
    t.saveXMCDA2('testX',servingD3=False)
    t.showCriteria(IntegerWeights=True)
    g = BipolarOutrankingDigraph(t)
    rbc = RankingByChoosingDigraph(g)
    rbc.showRankingByChoosing()
    print(g.computeOrdinalCorrelation(rbc))

def testRandomCoalitionsPerformanceTableau():
    print('*==>> random S3 Performance Tableaux ------------*')
    t = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=7,\
                                   VariableGenerators=True,\
                                   commonThresholds=[(5.0,0.0),(10.0,0.0),(65.0,0.0)],\
                                   Debug=False,\
                                   OrdinalScales=False,\
                                   Coalitions=True,\
                                   RandomCoalitions=False)
    print(t)
    t.saveXMCDA2(fileName='randomS3PerformanceTableau',servingD3=False)
    for g in t.criteria:
        print('==>>', g, t.computeThresholdPercentile(g,'ind'))
        for a in t.actions:
            print(t.actions[a]['generators'][g])
    t = XMCDA2PerformanceTableau('randomS3PerformanceTableau')
    g = BipolarOutrankingDigraph(t)
    #g.defaultDiscriminationThresholds()
    g.showCriteria()
    g.showCriteriaCorrelationTable()
    t.showPerformanceTableau()
    g.showRelationTable()
    g.showRubyChoice()

def testPercentilesOfThresholds():
    print('*---------- test percentiles of variable thresholds --------*') 
    t = RandomCoalitionsPerformanceTableau(weightDistribution='equicoalitions',seed=100)
    t.computeDefaultDiscriminationThresholds(quantile={'ind':10.0,'pref':20.0,
                                                       'weakVeto':90.0,'veto':95.0})
    for g in [y for y in t.criteria]:
        print(g, t.criteria[g]['thresholds'])
        for th in t.criteria[g]['thresholds']:
            print(th)
            print(' variable:', end=' ')
            print(t.computeVariableThresholdPercentile(g,th,Debug=False))
            print(' constant:', end=' ') 
            print(t.computeThresholdPercentile(g,th))
    t.showPerformanceTableau()
    t.showCriteria(Debug=False)
    t.saveXMCDA2('testPerc',servingD3=False)

def testRandomPerformanceGenerators():
    print('*---------- test dynamic updates of a random performance tableau --------*') 
    t = RandomPerformanceTableau(numberOfActions=15,commonScale=(0,10),commonThresholds=[(10,0),(20,0),(90,0)],
                                           seed=100)
    t.showAll()
    rag1 = RandomPerformanceGenerator(t,actionNamePrefix='b',seed=100)
    sampleSize = 5
    rag1.randomActions(sampleSize)
    rag2 = RandomPerformanceGenerator(t,actionNamePrefix='c',seed=110)
    newActions = rag2.randomActions(nbrOfRandomActions=5)
    #t.showHTMLPerformanceHeatmap(Correlations=True)
 
def testRandomCBPerformanceGenerators():
    print('*---------- test dynamic updates of a random CB performance tableau --------*') 
    t = RandomCBPerformanceTableau(numberOfActions=10,
                                           seed=100)
    t.showAll()
    rag1 = RandomCBPerformanceGenerator(t,actionNamePrefix='b',seed=100)
    sampleSize = 5
    for s in range(sampleSize):
        newAction = rag1._randomAction()
        ak = newAction['action'].pop('key')
        t.actions[ak] = newAction['action']
        for ev in t.evaluation:
            for g in t.evaluation:
                t.evaluation[g][ak] = newAction['evaluation'][g]
    rag2 = RandomCBPerformanceGenerator(t,actionNamePrefix='c',seed=110)
    newPerfTab= rag2.randomPerformanceTableau(nbrOfRandomActions=10)
    t.updateDiscriminationThresholds(Comments=True)
    newPerfTab.showHTMLPerformanceHeatmap(Correlations=True)

def testRandom3ObjectivesPerformanceGenerators():
    print('*---------- test dynamic updates of a random 3 Objectives performance tableau --------*') 
    t = Random3ObjectivesPerformanceTableau(numberOfActions=10,OrdinalScales=True,
                                           seed=100)
    t.showAll()
    rag1 = Random3ObjectivesPerformanceGenerator(t,actionNamePrefix='b',seed=100)
    sampleSize = 5
    for s in range(sampleSize):
        newAction = rag1._randomAction()
        ak = newAction['action'].pop('key')
        t.actions[ak] = newAction['action']
        for ev in t.evaluation:
            for g in t.evaluation:
                t.evaluation[g][ak] = newAction['evaluation'][g]
    rag2 = Random3ObjectivesPerformanceGenerator(t,actionNamePrefix='c',seed=110)
    rag2.randomActions(nbrOfRandomActions=5)
    print(rag2.randomActions(2))
    #t.showHTMLPerformanceHeatmap(ndigits=0,Correlations=True)
