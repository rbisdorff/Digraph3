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

def testRandomPerformanceTableau():
    print('==>> Testing Random Performance Tableau instantiation')
    t = RandomPerformanceTableau(numberOfActions=10,
                                 numberOfCriteria=7,
                                 commonMode=('normal',50,20),
                                 seed=100)
    t.showAll()
    print(t.computeWeightedAveragePerformances(isNormalized=True,
                                               lowValue=0.0,highValue=20.0))
    t = RandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('triangular',30,0.5),
                                 seed=None)
    t.showStatistics()
    t = RandomPerformanceTableau(weightScale=(1,10),
                                 commonScale=(0.0,50),
                                 commonMode=('beta',None,None),
                                 seed=None)
    t.showStatistics()

def testFullRandomPerformanceTableau():
    print('==>> Testing Full Random Performance Tableau instantiation')
    t = FullRandomPerformanceTableau(numberOfActions=10,
                                 numberOfCriteria=7,
                                 seed=100)
    t.showAll()
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


# def testRandomS3PerformanceTableau():
#     print('*==>> various tests for random performance tableaux -----*')
#     t = RandomS3PerformanceTableau(numberOfActions=20,numberOfCriteria=13,commonThresholds=[(2.5,0.0),(5.0,0.0),(30.0,0.0)])
#     t.saveXMCDA()
#     #t = XMCDAPerformanceTableau('temp')
#     g = Electre3OutrankingDigraph(t)
#     #g = BipolarOutrankingDigraph(t)
#     g.showVetos()
#     print(g.showVetos(cutLevel=60.0,realVetosOnly=True))
#     #g.showEvaluationStatistics()
#     print(g.computeVetoesStatistics())
#     g.showCriteria()
#     gini = g.computeConcentrationIndex(list(range(len(g.actions))),g.outDegreesDistribution())
#     print('gini: %2.4f' % (gini))
#     ## g.showStatistics()
#     percentages = [0,20,33,40,50,60,66,75,80,100]
#     percentiles = g.computeValuationPercentiles(g.actions,percentages)
#     print('Percentiles:')
#     for p in percentages:
#         print('%d : %.2f ' % (p,percentiles[p]))
#     percentiles = [20,33,40,50,60,66,75,80]
#     percentages = g.computeValuationPercentages(g.actions,percentiles)
#     print('Percentages: ')
#     for p in percentiles:
#         print('%d : %.3f ' % (p,percentages[p]))

    
def testCBPerformanceTableau(): 
    print('*==>> random CB Performance Tableaux ------------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,\
                                   commonPercentiles={'ind':5,'pref':10,'veto':95},\
                                   weightDistribution="random",\
                                   weightScale=[1,2],\
                                   integerWeights=True,\
                                   commonMode=["normal",50.0,25.0])
    t.saveXMCDA(fileName='randomPerformanceTableau',servingD3=False)
    t.showCriteria(Debug=False)
    g = BipolarOutrankingDigraph(t)
    g.exportGraphViz()

def testCoalitionsPerformanceTableau():
    print('*==>> random Coalitions Performance Tableaux ------------*')
    t = RandomCoalitionsPerformanceTableau(numberOfActions=13,\
                                           numberOfCriteria=21,\
                                           Coalitions=False,\
                                           RandomCoalitions=True,\
                                           weightDistribution="equicoalitions")
    t.saveXMCDA2('test',servingD3=False)
    t.showCriteria(IntegerWeights=True)
    g = BipolarOutrankingDigraph(t)
    g.computeRankingByChoosing(CoDual=False)
    g.showRankingByChoosing()
    prg = PrincipalInOutDegreesOrdering(g,imageType="pdf")
    prg.showWeakOrder()
    print(g.computeOrdinalCorrelation(prg))

def testRandomCoalitionsPerformanceTableau():
    print('*==>> random S3 Performance Tableaux ------------*')
    t = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=7,\
                                   VariableGenerators=True,\
                                   commonThresholds=[(5.0,0.0),(10.0,0.0),(65.0,0.0)],\
                                   Debug=False,\
                                   OrdinalScales=False,\
                                   Coalitions=True,\
                                   RandomCoalitions=False)
    t.saveXMCDA2(fileName='randomS3PerformanceTableau',servingD3=False)
    for g in t.criteria:
        print('==>>', g, t.computeThresholdPercentile(g,'ind'))
        for a in t.actions:
            print(t.actions[a]['generators'][g])
    t = XMCDAPerformanceTableau('randomS3PerformanceTableau')
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
    t.computeDefaultDiscriminationThresholds(quantile={'ind':10.0,'pref':20.0,'weakVeto':90.0,'veto':95.0})
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
    t.showHTMLPerformanceHeatmap(Correlations=True)

