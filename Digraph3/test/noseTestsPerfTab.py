#######################
# R. Bisdorff 
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsPerfTab.py
# # Current $Revision: 1.3 $
########################

from digraphs import *
from outrankingDigraphs import *
from decimal import Decimal
from weakOrders import *

def testPerformanceTableau():
    print('==>> Testing Performance Tableau instantiation')
    t = RandomPerformanceTableau()
    t.showAll()
    t.save('tempperftab')
    tb = PerformanceTableau('tempperftab')
    tb.showAll()
    g = BipolarOutrankingDigraph(tb)
    g.showAll()

def testPartialPerformanceTableau():
    print('==>> Testing PartialPerformance Tableau instantiation')
    t = RandomCoalitionsPerformanceTableau(numberOfActions=10,
                                           numberOfCriteria=5,
                                           Coalitions=False,
                                           RandomCoalitions=True,
                                           weightDistribution="equicoalitions")
    t.showAll()
    pt1 = PartialPerformanceTableau(t)
    pt1.showAll()
    pt2 = PartialPerformanceTableau(t,actionsSubset=['a01','a02'],criteriaSubset=['g01','g03'])
    pt2.showAll()

def testConstantPerformanceTableau():
    print('==>> Testing ConstantPerformance Tableau instantiation')
    t = RandomCoalitionsPerformanceTableau(numberOfActions=10,
                                           numberOfCriteria=5,
                                           Coalitions=False,
                                           RandomCoalitions=True,
                                           weightDistribution="equicoalitions")
    tc = ConstantPerformanceTableau(t)
    tc.showAll()
    tc.showStatistics()

def testRandomPerformanceTableau():
    print('==>> Testing Random Performance Tableau instantiation')
    t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=7,commonMode=('normal',50,20))
    t.showAll()
    print(t.computeWeightedAveragePerformances(isNormalized=True,lowValue=0.0,highValue=20.0))

def testNormalizedPerformanceTableau():
    print('*-------- Testing Normalization of Performance Tableaux  -------')
    t = RandomCBPerformanceTableau()
    t.showCriteria()
    t.showPerformanceTableau()
    tn = NormalizedPerformanceTableau(t,Debug=True)
    tn.showCriteria()
    tn.showPerformanceTableau()

def testhasOddWeightsAlgebra():
    print('*--------- Testing hasOddWeightsAlgebra test ------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,numberOfCriteria=13,commonThresholds=None,commonPercentiles={'ind':5,'pref':10,'veto':90},weightDistribution="random", weightScale=None,integerWeights=True,commonScale=[0.0,100.0],commonMode=["normal",50.0,25.0],Debug=False)
    print(t.hasOddWeightAlgebra(Debug=True))

def testRandomS3PerformanceTableau():
    print('*==>> various tests for random performance tableaux -----*')
    t = RandomS3PerformanceTableau(numberOfActions=20,numberOfCriteria=13,commonThresholds=[(2.5,0.0),(5.0,0.0),(30.0,0.0)])
    t.saveXMCDA()
    #t = XMCDAPerformanceTableau('temp')
    g = Electre3OutrankingDigraph(t)
    #g = BipolarOutrankingDigraph(t)
    g.showVetos()
    print(g.showVetos(cutLevel=60.0,realVetosOnly=True))
    #g.showEvaluationStatistics()
    print(g.computeVetoesStatistics())
    g.showCriteria()
    gini = g.computeConcentrationIndex(list(range(len(g.actions))),g.outDegreesDistribution())
    print('gini: %2.4f' % (gini))
    ## g.showStatistics()
    percentages = [0,20,33,40,50,60,66,75,80,100]
    percentiles = g.computeValuationPercentiles(g.actions,percentages)
    print('Percentiles:')
    for p in percentages:
        print('%d : %.2f ' % (p,percentiles[p]))
    percentiles = [20,33,40,50,60,66,75,80]
    percentages = g.computeValuationPercentages(g.actions,percentiles)
    print('Percentages: ')
    for p in percentiles:
        print('%d : %.3f ' % (p,percentages[p]))

def testXMLSaveReadPerformanceTableau():
    print('*==>> testing XML save and read performance tableaus ----*')
    t = RandomPerformanceTableau()
    t.showAll()
    t.saveXML(name='randperftabXML',category='standard',subcategory='random',author='RB',reference='Digraph implementation')
    t1 = XMLPerformanceTableau('randperftabXML')
    t1.showAll()
    g = BipolarOutrankingDigraph(t1)
    g.showRubyChoice()
    print('Name : ',t1.name)
    print('Actions : ', t1.actions)
    print('Criteria : ', t1.criteria)
    print('Evaluations :', t1.evaluation)

def testPerformanceTableauStatistics():
    print('*==>> performanceTableau statistics ---------*')
    t = FullRandomPerformanceTableau(commonScale=(0.0,100.0),numberOfCriteria=10,numberOfActions=10,commonMode=('triangular',30.0,0.7))
    t.showStatistics()
    print(t.computeNormalizedDiffEvaluations(lowValue=0.0,highValue=100.0,withOutput=True,Debug=True))
    t = RandomCBPerformanceTableau()
    t.showStatistics()
    t.showEvaluationStatistics()
    
def testXMCDAPerformanceTableauLoading():
    print('*==>> XMCDA Performance tableau loading ---*')
    t = XMCDAPerformanceTableau('temp')
    t.showPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    g.save('testdecimal')
    gd = Digraph('testdecimal')

def testPerformanceDifferencesPerCriteria():
    print('*==>> verifying  performance differences per criteria ---*')
    g = RandomBipolarOutrankingDigraph()
    g.showPerformanceTableau()
    g.computePerformanceDifferences(Comments=True)
    
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

def testRandomS3PerformanceTableau():
    print('*==>> random S3 Performance Tableaux ------------*')
    t = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=7,\
                                   VariableGenerators=True,\
                                   commonThresholds=[(5.0,0.0),(10.0,0.0),(65.0,0.0)],\
                                   Debug=False,\
                                   OrdinalScales=False,\
                                   Coalitions=False,\
                                   RandomCoalitions=True)
    t.saveXMCDA(fileName='randomS3PerformanceTableau',servingD3=False)
    for g in t.criteria:
        print('==>>', g, t.computeThresholdPercentile(g,'ind'))
        for a in t.actions:
            print(t.actions[a]['generators'][g])
    t = XMCDAPerformanceTableau('randomS3PerformanceTableau')
    g = Electre3OutrankingDigraph(t)
    #g.defaultDiscriminationThresholds()
    g.showCriteria()
    g.showCriteriaCorrelationTable()
    t.showPerformanceTableau()
    g.showRelationTable()
    g.showRubyChoice()

def testPercentilesOfThresholds():
    print('*---------- test percentiles of variable thresholds --------*') 
    t = RandomS3PerformanceTableau()
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

def testXMCDA2SaveReadPerformanceTableau():
    print('*==>> save and read XMCDA-2.0 PerformanceTableau instances ----*')
    t = RandomS3PerformanceTableau(numberOfActions=5,numberOfCriteria=15,weightDistribution="random",weightScale=(1,13),integerWeights=True,commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0),(60.0,0.0)],RandomCoalitions=True,commonMode=['beta',0.5,None])
    #t.showAll()
    #t = RandomCBPerformanceTableau(numberOfActions=5,numberOfCriteria=7,weightDistribution="random",weightScale=(1,7),integerWeights=True)
    t.saveXMCDA('test')
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    t1 = XMCDAPerformanceTableau('test')
    g1 = BipolarOutrankingDigraph(t1)
    g1.showRelationTable()
    t1.saveXMCDA2('test1')
    t2 = XMCDAPerformanceTableau('test')
    g2 = BipolarOutrankingDigraph(t2)
    g2.showRelationTable()
    
def testStringIOXMCDA2Encoding():
    print('*---- test mapped memory XMCDA2 encoding for performanceTableau ---*')
    T = PerformanceTableau()
    problemTextmmap = T.saveXMCDA2(isStringIO=True)
    problemText = T.saveXMCDA2String()
    if problemTextmmap != problemText:
        print('Error')
        fo = open('problemTextmmap.txt','w')
        fo.write(problemTextmmap)
        fo.close()
        fo = open('problemText.txt','w')
        fo.write(problemText)
        fo.close()     
        exit(1)

def testMajorityQuantilesRanking():
    print('*------ test majority qualtiles extraction and ranking ----*')
    t = RandomCBPerformanceTableau(numberOfCriteria=7,numberOfActions=6,weightDistribution='random')
    t.showStatistics()
    t.showPerformanceTableau()
    html = t.showAllQuantiles()
    print(t.computeQuantiles(Debug=False))
    t.showQuantileSort()
    
def testPartialPerfTabs():
    print('*------ test partial performance tableau object ----*')
    t = RandomCBPerformanceTableau(numberOfCriteria=13,
                                   numberOfActions=20,
                                   weightDistribution='equiobjectives',
                                   integerWeights=True,
                                   Debug=False)
    t.showAll()
    t.save('testSize1')
    pt1 = PartialPerformanceTableau(t)
    pt1.showAll()
    pt2 = PartialPerformanceTableau(t,actionsSubset=['a01','a02'],
                                    criteriaSubset=['g01','g03'])
    pt2.showAll()
    
def testSaveCSV():
    print('*---- test CSV storing of performance table ----*')
    t = RandomCBPerformanceTableau(numberOfCriteria=5,
                                   numberOfActions=7,
                                   weightDistribution='equiobjectives',
                                   integerWeights=True,
                                   Debug=False)
    t.showAll()
    t.saveCSV('testCSVSaving',Sorted=True,Debug=True)

def testHTMPerformanceHeatmap():
    print('*------ test performance heatmap -----*')
    t = RandomCBPerformanceTableau(numberOfCriteria=5,
                                   numberOfActions=7,
                                   weightDistribution='equiobjectives',
                                   integerWeights=True,
                                   Debug=False)
    actionsList = [x for x in t.actions.keys()]
    criteriaList = [g for g in t.criteria.keys()]
    print(t.htmlPerformanceHeatmap(actionsList=actionsList,
                                   criteriaList=criteriaList,
                                   colorLevels=9,
                                   Correlations=True,
                                   ndigits=4,
                                   Debug=True))
    
