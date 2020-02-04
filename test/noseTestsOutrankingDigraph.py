#######################
# R. Bisdorff 
# outrankingDigraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

from digraphs import *
from outrankingDigraphs import *
from time import time
from randomPerfTabs import _RandomS3PerformanceTableau\
     as RandomS3PerformanceTableau
from randomPerfTabs import _FullRandomPerformanceTableau as\
     FullRandomPerformanceTableau
from randomPerfTabs import _RandomCoalitionsPerformanceTableau as\
     RandomCoalitionsPerformanceTableau

def testElectre3OutrankingDigraph():
    print('==>> Testing Electre 3 Outranking Digraph instantiation')
    g = RandomElectre3OutrankingDigraph(numberOfActions=5)
    g.showAll()
    g.showStatistics()
    g.showPerformanceTableau()

def testOrdinalOutrankingDigraph():

    print('==>> Testing Ordinal Outranking Digraph instantiation')
    t = RandomCBPerformanceTableau(NegativeWeights=False,seed=1)
    g = OrdinalOutrankingDigraph(t)
    g.showAll()
    t1 = RandomCBPerformanceTableau(NegativeWeights=True,seed=1)
    g1 = OrdinalOutrankingDigraph(t1)
    g1.showAll()

def testUnanimousOutrankingDigraph():

    print('==>> Testing Unanimous Outranking Digraph instantiation')
    t = RandomCBPerformanceTableau(NegativeWeights=False,seed=1)
    g = OrdinalOutrankingDigraph(t)
    g.showAll()
    t1 = RandomCBPerformanceTableau(NegativeWeights=True,seed=1)
    g1 = OrdinalOutrankingDigraph(t1)
    g1.showAll()


def testRobustOutrankingDigraph():
    print('==>> Testing Robust Outranking Digraph instantiation')
    t = RandomCBPerformanceTableau(NegativeWeights=False,seed=1)
    g = RobustOutrankingDigraph(t)
    g.showPreKernels()
    g.showGoodChoices()
    g.showBadChoices()
    t1 = RandomCBPerformanceTableau(NegativeWeights=True,seed=1)
    g1 = RobustOutrankingDigraph(t1)
    g1.showPreKernels()
    g1.showGoodChoices()
    g1.showBadChoices()

def testDissimilarityDigraph():
    print('==>> Testing Dissimilarity Digraph instantiation')
    f = DissimilarityOutrankingDigraph()
    f.showAll()
    f.showStatistics()

def testPolarisedOutrankingDigraph():
    print('==>> Testing PolarisedOutrankingDigraph instantiation')
    t = FullRandomPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    print(g.valuationdomain)
    ch = PolarisedOutrankingDigraph(g,level=50,AlphaCut=False,KeepValues=True)
    ch.showAll()
    ch.showStatistics()

def testFullRandomOutrankingDigraph():
    print('*==>> testing full random outranking Digraphs ----*')
    t = FullRandomPerformanceTableau()
    #t = RandomCBPerformanceTableau()
    t.showAll()
    g = BipolarOutrankingDigraph(t)
    g.showCriteria()
    g.showPerformanceTableau()
    g.showEvaluationStatistics()
    ## g.showStatistics()
    g.showVetos(realVetosOnly=True)
    print('criteria significance concentration: ', g.computeWeightsConcentrationIndex())

def testElectre3OutrankingDigraph():
    print('*==>> testing Electre III outranking Digraphs ----*')
    t = FullRandomPerformanceTableau(numberOfActions=10)
    g3 = Electre3OutrankingDigraph(t)
    g3.showRelationTable()
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()

def testForcedBestSingleChoice():
    print('*==>> testing forced best single choice  ----*')
    t = FullRandomPerformanceTableau(numberOfActions=15)
    g = BipolarOutrankingDigraph(t)
    g.showRubyChoice()
    print(g.forcedBestSingleChoice())

def testBipolarOutrankingDigraph():
    print('*==>> bipolar outranking  ----*')
    t = RandomPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    g.showAll()
    print(g)
    print(g.valuationdomain)
    print('unrelated pairs:')
    print(g.computeUnrelatedPairs())
    print('more or less unrelated pairs:')
    print(g.computeMoreOrLessUnrelatedPairs())
    g.showVetos()

def testComputeRubisChoice():
    print('*==>> Test ruby BCR ---*')
    t = RandomPerformanceTableau(numberOfActions=7)
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    g.showRubisBestChoiceRecommendation(ChoiceVector=True,Comments=True)
    g.showRubyChoice(Comments=True,_OldCoca=True)
    g.showStatistics()
    print(g)
    
def testMoreOrlessRelatedPairs():
    print('*==>> test more or less unrelated pairs extraction ---*')
    #g = BipolarIntegerOutrankingDigraph()
    g = Electre3OutrankingDigraph()
    g.showRelationTable()
    print(g.valuationdomain)
    print('unrelated pairs:')
    print(g.computeUnrelatedPairs())
    print('more or less unrelated pairs:')
    print(g.computeMoreOrLessUnrelatedPairs())
    g.showVetos()

def testXMLRubisSaveReadMethods():
    print('*==>> test rubisOutrankingDigraph XML saving ------------*')
    t = FullRandomPerformanceTableau(numberOfActions=5,commonMode=['uniform',None,None],IntegerWeights=True)
    t.save('testperf')

    g = BipolarOutrankingDigraph(t)
    g.saveXMLRubisOutrankingDigraph('testrel',servingD3=False)
    g.showVetos()

# def testXMLRubisIntegerOutrankingSave():
#     print('*==>> test rubisIntegerOutrankingDigraph XML saving ------------*')
#     t = FullRandomPerformanceTableau(numberOfActions=5,commonMode=['uniform',None,None],IntegerWeights=True)
#     t.saveXMLRubis()
#     gi = BipolarIntegerOutrankingDigraph(t)
#     gi.saveXMLRubisOutrankingDigraph('testint',servingD3=False)
#     gi.showRelationTable()
#     gi.showRubyChoice(Comments=True)

def testRobustoutranking():
    print('*==>> robust outranking ------------------*')
    t0 = FullRandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5)
    t0.saveXMCDA2('testXMLRubis')
    t = XMCDA2PerformanceTableau('testXMLRubis')
    g = BipolarOutrankingDigraph(t)
    g.saveXMLRubisOutrankingDigraph('test1',servingD3=False)
    go = OrdinalOutrankingDigraph(t)
    go.saveXMLRubisOutrankingDigraph('testo',servingD3=False)
    gu = UnanimousOutrankingDigraph(t)
    gu.saveXMLRubisOutrankingDigraph('testu',servingD3=False)
    gc = BipolarOutrankingDigraph(t)
    gc.saveXMLRubisOutrankingDigraph('testc',servingD3=False)
    gr = OldRobustOutrankingDigraph(t)
    gr.saveXMLRubisOutrankingDigraph('testr',servingD3=False)

def testPairwiseComparisons():
    print('*==>> test show pairwise comparison-------*')
    t = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5)
    g = BipolarOutrankingDigraph(t)
    for x in g.actions:
        for y in g.actions:
            g.showPairwiseComparison(x,y)

def testPairwiseCompleteComparisons():
    print('*==>> test pairwise complete comparison-------*')
    #t = FullRandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5)
    #t = XMLRubisPerformanceTableau('BMPTV-358rubis')
    t = RandomCBPerformanceTableau(numberOfActions=10,numberOfCriteria=7)
    #t = PerformanceTableau('testCorr')
    #t = XMCDAPerformanceTableau('randomPerformanceTableau')
    t.saveXMCDA2('testCorr')
    t = XMCDA2PerformanceTableau('testCorr')
    g = BipolarOutrankingDigraph(t) 
    g.showCriteriaCorrelationTable()
    g.showPerformanceTableau()
    g.export3DplotOfCriteriaCorrelation('criteriaCorrelation',Type="pdf",Comments=True)
    #g.export3DplotOfCriteriaCorrelation(Type="jpeg")
    #g.export3DplotOfCriteriaCorrelation(Type="xfig")
    #g.export3DplotOfCriteriaCorrelation(Type="interactive")

def testCriteriaHierarchy():
    print('*==>> show Criteria Hierarchy --------------*')
    t = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5,commonMode=('uniform',None,None))
    ## t = XMCDAPerformanceTableau('thierrysChoice-xmcda')
    ## print t.parameter
    ## ## t = PerformanceTableau('studentenspiegel')
    g = BipolarOutrankingDigraph(t)
    #g.saveXMCDAOutrankingDigraph('testXMCDADigraph',valuationType='bipolar', relationName='Stilde')
    g.showCriteriaCorrelationTable()
    g.showCriteriaHierarchy()
    #g.export3DplotOfCriteriaCorrelation(plotFileName="tempplot",Type="png",Comments=True,bipolarFlag=True,dist=False,centeredFlag=True)

def testCriteriaNetFlows():
    print('*==>> show Criteria net flows --------------*')
    g = RandomBipolarOutrankingDigraph()
    print(g.computeSingleCriteriaNetflows())
    g.saveSingleCriterionNetflows()

def testXMCDARubisRecommendation():
    print('*==>> save XMCDA Rubis Recommendation --------------*')
    t = FullRandomPerformanceTableau(numberOfActions=10,numberOfCriteria=10)
    #t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=20,commonMode=('uniform',None,None))
    t.saveXMCDA(servingD3=False)
    #t.showAll()
    #g = OldRobustOutrankingDigraph(t)
    #g.saveXMCDAOutrankingDigraph('testXMCDAOutrankingDigraph',servingD3=False,variant='robustness',category='Robust Rubis',relationName='S_rob')
    g = BipolarOutrankingDigraph(t)
    g.saveXMCDAOutrankingDigraph('testXMCDAOutrankingDigraph',servingD3=False,variant='standard',category='Rubis',relationName='Stilde')


def testPerformanceDifferencesPerCriteria():
    print('*==>> verifying  performance differences per criteria ---*')
    g = RandomBipolarOutrankingDigraph()
    g.showPerformanceTableau()
    g.computePerformanceDifferences(Comments=True)

def testDefaultDiscriminationThresholds():
    print('* ---- verify default discrimination thresholds ----*')
    t = RandomCBPerformanceTableau(numberOfActions=13,numberOfCriteria=7)
    g = BipolarOutrankingDigraph(t)
    print('outranking original')
    g.showRelationTable()
    g.showCriteria()
    import copy
    g.computeDefaultDiscriminationThresholds(quantile={'ind':10,'pref':20,'weakPreference':60,'veto':80},Debug=True)
    g0 = copy.deepcopy(g)
    g0.computeDefaultDiscriminationThresholds(quantile={'ind':0})
    g0.relation=g._constructRelation(g.criteria,g.evaluation)
    g0.name = 'rel_tournament'
    print('weak tournament')        
    g0.showRelationTable()
    g0.showCriteria()
    g0.computeODistance(g,comments=True)
    gn = copy.deepcopy(g)
    gn.computeDefaultDiscriminationThresholds(quantile={'ind':100})      
    gn.relation=g._constructRelation(g.criteria,g.evaluation)
    gn.name = 'rel_complete'
    #g.showCriteria()
    d0kn = gn.computeODistance(g0)
    print('maximal distance:', d0kn)      
    print('original distance:', gn.computeODistance(g))   
    gn.showRelationTable()

def testRubisRanking():
    print('*-------  test rubisRanking -----*')
    t = RandomCBPerformanceTableau(numberOfActions=9,numberOfCriteria=5,IntegerWeights=False,commonPercentiles={'ind':10,'pref':20,'veto':60},valueDigits=4)
    ## t.save('test',valueDigits=4)
    ## t = PerformanceTableau('test')
    ## t = XMCDAPerformanceTableau('Ronda08')
    g = BipolarOutrankingDigraph(t)
    print(g.valuationdomain)
    ## g.showCriteriaCorrelationTable()
    g.computeSingletonRanking(Comments = True)
    print(g.valuationdomain)


def testGlobalOutrankingCorrelation():
    print('*----- test global outranking correlation -----*')
    t = RandomCBPerformanceTableau(numberOfActions=5,numberOfCriteria=3)
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    g.showCriteriaCorrelationTable()
    criteriaList = [x for x in t.criteria]
    medianKCorrelation = {}
    print(criteriaList)
    for x in criteriaList:
        gx = BipolarOutrankingDigraph(t,coalition=[x])
        print('crtierion : ',x)
        gx.showRelationTable()
        ## medianKCorrelation[x] = -((g.crispKDistance(gx)*Decimal("2.0")) - Decimal("1.0")) 
        medianKCorrelation[x] = g.bipolarKDistance(gx) 
        #print medianKCorrelation[x]
    print('median K-Correlation:', medianKCorrelation)

def testElectre3OutrankingDigraph():
    print('*----- test Electre3 outranking Digraph -----*')
    t3 = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=13,weightDistribution="random",weightScale=(1,13),IntegerWeights=True,commonThresholds=[(2.5,0.1),(5.0,0.15),(50.0,0.0),(60.0,0.0)],RandomCoalitions=True,commonMode=['beta',0.5,None],Electre3=False, vetoProbability=0.5)
    gs3 = Electre3OutrankingDigraph(t3,hasNoVeto=False)
    print(gs3.computeVetos(realVetosOnly=True))
    g = BipolarOutrankingDigraph(t3)
    gnv = BipolarOutrankingDigraph(t3,hasNoVeto=True)
    g.showRelationTable()
    gnv.showRelationTable()
    actionsList=[x for x in g.actions]
    actionsList.sort()
    for x in actionsList:
        for y in actionsList:
            print(x, y, gnv.relation[x][y]-g.relation[x][y])
    g.showRelationTable()
    gs3.showPairwiseComparison('a07','a03')
    g.showPairwiseComparison('a07','a03')

def testsaveXMCDA2RubisChoiceRecommendation():
    print('*----- test saveXMCDA2RubisChoiceRecommendation -----*')
    t = Random3ObjectivesPerformanceTableau(numberOfActions=5,numberOfCriteria=7,
                                   weightDistribution="random",weightScale=(1,1),
                                   IntegerWeights=True,
                                   commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0),(60.0,0.0)],
                                   commonMode=['beta',0.5,None])
    g1 = BipolarOutrankingDigraph(t)
    g1.showRelationTable()
    g1.saveXMCDA2RubisChoiceRecommendation('testRubisChoiceRecommendation')

def testXMCDA2RobustChoiceRecommendation():
    print('*----- test XMCDA2 Robust Choice Recommendation -----*')
    t = Random3ObjectivesPerformanceTableau(numberOfActions=5,numberOfCriteria=7,
                                            weightDistribution="random",weightScale=(1,1),
                                            IntegerWeights=True,
                                            commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0),(60.0,0.0)],
                                            commonMode=['beta',0.5,None])
    g = OldRobustOutrankingDigraph(t)
    g.saveXMCDA2RubisChoiceRecommendation()

def testBipolarVetos():
    print('*----- test bipolar vetos -----*')
    t = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
    t.save()
    gnv = BipolarOutrankingDigraph(t,hasBipolarVeto=True)
    gnv.exportGraphViz('gnvtest')
    g = BipolarOutrankingDigraph(t,hasBipolarVeto=False)
    gnv.exportGraphViz('gtest')
    asymg = AsymmetricPartialDigraph(g)
    asymg.exportGraphViz('asymgtest')
    asymgnv = AsymmetricPartialDigraph(gnv)
    asymgnv.exportGraphViz('asymgnvtest')

def testLPDCount():
    print('*---- test large performance differences count and denotation ----*')
    T = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(50.0,0.0),(60.0,0.0)])
    G = BipolarOutrankingDigraph(T,hasBipolarVeto=True)
    G.showRelationTable(hasLPDDenotation=True)

def testGridDigraphs():
    print('*---- test grid digraphs -----*')
    G = GridDigraph(n=5,m=5,hasMedianSplitOrientation=True)
    from time import time
    G.showStatistics()
    t0 = time()
    G.computeChordlessCircuits()
    t1 = time()
    print(len(G.circuitsList), t1-t0)
    G.showChordlessCircuits()

def testEquiSignificanceMajorityOutrankingDigraph():
    print('*---- test equi-significance majority outranking digraphs ---*')
    t = FullRandomPerformanceTableau(numberOfActions=7,numberOfCriteria=13)
    g = EquiSignificanceMajorityOutrankingDigraph(t)
    print(g.computeWeightPreorder())
    g.showRelationTable()
    gr = RobustOutrankingDigraph(t)
    gr.showRelationTable()
    
def testStringIOXMCDA2Encoding():
    print('*---- test mapped memory XMCDA2 encoding for performanceTableau ---*')
    T = PerformanceTableau()
    problemTextmmap = T.saveXMCDA2(isStringIO=True,servingD3=False)
    problemText = T.saveXMCDA2String(servingD3=False)
    if problemTextmmap != problemText:       
        print('Error')
        fo = open('problemTextmmap.txt','w')
        fo.write(problemTextmmap)
        fo.close()
        fo = open('problemText.txt','w')
        fo.write(problemText)
        fo.close()
        exit(1)
        
def testHTMLTables():
    print('*--- test rendering html formatted Performance and Relation Tables ---*')
    g = RandomOutrankingDigraph()
    print(g._htmlRelationTable(isColored=True))
    t = RandomPerformanceTableau()
    print(t._htmlPerformanceTableau())

def testActionsCorrelation():
    print('*---- test computing actions correlation table and digraph ---*')
    g = RandomOutrankingDigraph()
    g.showStatistics()
    print(g.computeActionsComparisonCorrelations())
    g.saveCriteriaCorrelationTable('crit.prn')
    g.saveActionsCorrelationTable('act.prn')
    g.export3DplotOfActionsCorrelation('actionsCorrelation')

        
def testRankingRules():
    print('*-------- Testing Ranking Rules -------')
    t = RandomPerformanceTableau(numberOfActions=5)
    t.save()
    t.showPerformanceTableau()
    scores = t.computeWeightedAveragePerformances(isNormalized=True,lowValue=0.0,highValue=20.0)
    ranking = []
    for x in t.actions:
        ranking.append((scores[x],x))
    ranking.sort(reverse=True)
    print(ranking)
    g = BipolarOutrankingDigraph(t)
    g.exportGraphViz()
    gcd = CoDualDigraph(g)
    gcd.exportGraphViz()
##    gcd.computeRankedPairsOrder(Debug=True)
##    print(gcd.computeRankedPairsOrder())

    gcd.computeKemenyOrder(Debug=True)
    print(gcd.computeKemenyRanking(isProbabilistic=True, seed=1,sampleSize=500))    
    gcd.computeSlaterOrder(Debug=True)
    print(gcd.computeSlaterOrder(isProbabilistic=True, seed=1,sampleSize=500))

##def testQuantilesRanking():
##    print('*---- test quantiles ranking procedures -----*')
##    g = RandomBipolarOutrankingDigraph()
##    gcd = CoDualDigraph(g)
##    print(gcd.bestRanks())
##    print(gcd.worstRanks())
##    p = Preorder(gcd,'best')
##    strc = StrongComponentsCollapsedDigraph(p)
##    strc.showComponents()
##    p = Preorder(gcd,'worst')
##    strc = StrongComponentsCollapsedDigraph(p)
##    strc.showComponents()

def testPairwiseClusterComparison():
    print('*----- test paiwise cluster comparisons ----*')
    t = RandomCBPerformanceTableau(numberOfActions=10)
    g = BipolarOutrankingDigraph(t)
    actionsList = [x for x in list(g.actions.keys())]
    K1 = actionsList[5:]
    K2 = actionsList[:5]
    print(g.valuationdomain)
    g.computePairwiseClusterComparison(K1, K2, Debug=True)
    
   
def testRankingByChoosing():
    print('*----- test ranking by iterated best and worst choosing ----*')
    t = RandomCBPerformanceTableau(numberOfActions=10)
    g = BipolarOutrankingDigraph(t)
    g.computeRankingByChoosing(Debug=True)
    g.showRankingByChoosing()
    g.exportGraphViz(bestChoice=set(g.rankingByChoosing['result'][0][0][1]),
                     worstChoice=set(g.rankingByChoosing['result'][0][1][1]))
    rankingByChoosingRelation = g.computeRankingByChoosingRelation()
    print('Correlation with ranking by choosing result ', g.computeOrdinalCorrelation(rankingByChoosingRelation))
    g.showRelationTable(relation=rankingByChoosingRelation)

def testQuantileSorting():
    print('*----- test quantile sorting ----*')
    t = RandomCBPerformanceTableau(numberOfActions=10)
    g = BipolarOutrankingDigraph(t)
    print('Quantiles sorting')
    print(t.computeQuantileSort())
    t.showQuantileSort()
    quantileSortRelation = g.computeQuantileSortRelation(Debug=True)
    print('Correlation with ranking by quantile sorting result ', g.computeOrdinalCorrelation(quantileSortRelation))
    g.showRelationTable(relation=quantileSortRelation)

def testOrdinalCorrelations():
    print('*------ test ordinal correlation between rankings ----*')
    t = RandomCBPerformanceTableau(numberOfActions=7,weightDistribution='equiobjectives')
    g = BipolarOutrankingDigraph(t)
    g.recodeValuation(-1.0,1.0)
    g.computeRankingByChoosing(Debug=False)
    g.showRankingByChoosing()
    print('Quantiles sorting')
    print(t.computeQuantileSort())
    t.showQuantileSort()
    g.exportGraphViz(bestChoice=set(g.rankingByChoosing['result'][0][0][1]),
                     worstChoice=set(g.rankingByChoosing['result'][0][1][1]))
    rankingByChoosingRelation = g.computeRankingByChoosingRelation()
    quantileSortRelation = g.computeQuantileSortRelation(Debug=False)
    print('Correlation with ranking by choosing result ', g.computeOrdinalCorrelation(rankingByChoosingRelation))
    print('Correlation with ranking by quantile sorting result ', g.computeOrdinalCorrelation(quantileSortRelation))

def testIterateRankingByChoosing():
    print('*----- test iterating chordless circuits elimination ranking by choosing ----*')
    t = RandomCBPerformanceTableau(numberOfActions=7,weightDistribution='equiobjectives')
    g = BipolarOutrankingDigraph(t)
    g.recodeValuation(-1.0,1.0)
    g.iterateRankingByChoosing(Comments=True,Debug=False)

def testStochasticOutrankingDigraphs():
    print('*------ test stochastic bipolar outranking digraphs ----*')
    from outrankingDigraphs import StochasticBipolarOutrankingDigraph
    from transitiveDigraphs import RankingByChoosingDigraph
    t = RandomCBPerformanceTableau(numberOfActions=13,\
                                    numberOfCriteria=13,\
                                    weightDistribution='equiobjectives')
    t.save('test')
    t = PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t)
    g.recodeValuation(-1,1)
    g.showRelationTable()
    gmc = StochasticBipolarOutrankingDigraph(t,Normalized=False,\
                                             sampleSize=50,\
                                             likelihood=0.05,\
                                             Debug=False,\
                                             samplingSeed=1)
    gmc.showRelationTable()
    gmc.showRelationStatistics('medians')
    gmc.showRelationStatistics('likelihoods')
    for x in gmc.actions:
        for y in gmc.actions:
            print('==>>',x,y)
            print('Q4',gmc.relationStatistics[x][y]['Q4'])
            print('Q3',gmc.relationStatistics[x][y]['Q3'])
            print('probQ3',gmc.computeCDF(x,y,gmc.relationStatistics[x][y]['Q3']))
            print('Q2',gmc.relationStatistics[x][y]['median'])
            print('mean',gmc.relationStatistics[x][y]['mean'])
            print('Q1',gmc.relationStatistics[x][y]['Q1'])
            print('probQ1',gmc.computeCDF(x,y,gmc.relationStatistics[x][y]['Q1']))
            print('Q0',gmc.relationStatistics[x][y]['Q0'])
            print('pv',gmc.relationStatistics[x][y]['likelihood'])
            print('prob0',gmc.computeCDF(x,y,0.0))            
            print('sd',gmc.relationStatistics[x][y]['sd'])
    
    grbc = RankingByChoosingDigraph(g)
    grbc.showWeakOrder()
    gmcrbc = RankingByChoosingDigraph(gmc)
    gmcrbc.showWeakOrder()

def testRandomWeightsLaws():
    print('*------- test random laws for stochastic outranking ------*')
    t = RandomCBPerformanceTableau(numberOfActions=5,\
                                   numberOfCriteria=7,\
                                   weightDistribution='equiobjectives',
                                   )
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t)
    g.recodeValuation(-1,1)
    g.showRelationTable()

    print('Triangular')
    gmc = StochasticBipolarOutrankingDigraph(t,Normalized=True,\
                                             distribution='triangular',\
                                             sampleSize=100,likelihood=0.1,\
                                             Debug=False,samplingSeed=1)
    gmc.showRelationTable()
    gmc.recodeValuation(-100,100)
    gmc.showRelationStatistics('medians')
    gmc.showRelationStatistics('likelihoods')

    print('Uniform')
    gmc1 = StochasticBipolarOutrankingDigraph(t,Normalized=True,\
                                              distribution='uniform',\
                                              spread = 0.5,\
                                             sampleSize=100,likelihood=0.1,\
                                             Debug=False,samplingSeed=1)
    gmc1.showRelationTable()
    gmc1.recodeValuation(-100,100)
    gmc1.showRelationStatistics('medians')
    gmc1.showRelationStatistics('likelihoods')

    print('Beta(2,2)')
    gmc2 = StochasticBipolarOutrankingDigraph(t,Normalized=True,\
                                              distribution='beta(2,2)',\
                                             sampleSize=100,likelihood=0.1,\
                                             Debug=False,samplingSeed=1)
    gmc2.showRelationTable()
    gmc2.recodeValuation(-100,100)
    gmc2.showRelationStatistics('medians')
    gmc2.showRelationStatistics('likelihoods')

    print('Beta(12,12)')
    gmc3 = StochasticBipolarOutrankingDigraph(t,Normalized=True,\
                                              distribution='beta(4,4)',\
                                              spread = 0.5,\
                                             sampleSize=100,likelihood=0.1,\
                                             Debug=False,samplingSeed=1)
    gmc3.showRelationTable()
    gmc3.recodeValuation(-100,100)
    gmc3.showRelationStatistics('medians')
    gmc3.showRelationStatistics('likelihoods')

def testConfidentBipolarOutrankingDigraphs():
    print('*------- test random laws for stochastic outranking ------*')
    t = RandomCBPerformanceTableau(numberOfActions=7,\
                                   numberOfCriteria=13,\
                                   weightDistribution='equiobjectives',
                                   )
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    lg = ConfidentBipolarOutrankingDigraph(t,Debug=True)
    lg.showRelationTable(LikelihoodDenotation=False)
    lg.showRelationTable(LikelihoodDenotation=True)
    lg = ConfidentBipolarOutrankingDigraph(t,confidence=95,
                                           distribution="uniform",Debug=False)
    lg.showRelationTable(LikelihoodDenotation=True)
    lg = ConfidentBipolarOutrankingDigraph(t,confidence=75,
                                        distribution="beta",Debug=False)
    lg.showRelationTable(LikelihoodDenotation=True)
    lg = ConfidentBipolarOutrankingDigraph(t,distribution="beta",
                                           betaParameter=7.5,Debug=False)
    lg.showRelationTable(LikelihoodDenotation=True)

def testShowMarginalVersusGlobalOutrankingCorrelation():
    print('*-------- MarginalVersusGlobalOutranking -------')
    t = RandomCBPerformanceTableau(numberOfActions=10,\
                                  numberOfCriteria=13,\
                                  weightDistribution='equiobjectives',
                                  )
    g = BipolarOutrankingDigraph(t,Threading=False)
    g.showMarginalVersusGlobalOutrankingCorrelation()

def testComputeMarginalVersusGlobalOutrankingCorrelations():
    print('*-------- Threaded MarginalVersusGlobalOutranking -------')
    t = RandomCBPerformanceTableau(numberOfActions=50,\
                                   numberOfCriteria=21,\
                                   weightDistribution='equiobjectives',
                                   seed=100) 
    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=True)    
    Threading = True
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalOutrankingCorrelations(Threading=Threading)
    print(time()-t0)
    print(criteriaCorrelations)
    Threading = False
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalOutrankingCorrelations(Threading=Threading)
    print(time()-t0)
    print(criteriaCorrelations)

def testComputeMarginalVersusGlobalRankingCorrelations():
    print('*-------- Threaded MarginalVersusGlobalOutranking -------')
    t = RandomCBPerformanceTableau(numberOfActions=50,\
                                   numberOfCriteria=21,\
                                   weightDistribution='equiobjectives',
                                   seed=100) 
    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=True)
    ranking = g.computeNetFlowsRanking()
    Threading = True
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalRankingCorrelations(ranking,
                            Threading=Threading)
    print(time()-t0)
    print(criteriaCorrelations)
    Threading = False
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalRankingCorrelations(ranking,
                            Threading=Threading)
    print(time()-t0)
    print(criteriaCorrelations)

def testXMCDARubisSolver():
    print('*------ test xmcda module ----*')
    t = RandomCBPerformanceTableau(numberOfActions=5,\
                                   numberOfCriteria=7,\
                                   weightDistribution='equiobjectives',\
                                   )
    t.saveXMCDA2('testXMCDA')
    import xmcda
    xmcda.saveXMCDARubisBestChoiceRecommendation(\
        problemFileName='testXMCDA',\
        valuationType=None)
    xmcda.saveXMCDARubisBestChoiceRecommendation(\
        problemFileName='testXMCDA',\
        valuationType='noVeto')
    xmcda.saveXMCDARubisBestChoiceRecommendation(\
        problemFileName='testXMCDA',\
        valuationType='confident')
    xmcda.saveXMCDARubisBestChoiceRecommendation(\
        problemFileName='testXMCDA',\
        valuationType='robust')

##def testRubisRestServer():
##    print('*------ test RubisRestServer class ----*')
##    from time import sleep
##    t = RandomCBPerformanceTableau(numberOfActions=5,\
##                                   numberOfCriteria=7,\
##                                   weightDistribution='equiobjectives',
##                                   )
##    t.saveXMCDA2('test')
##    t = XMCDA2PerformanceTableau('test')
##    solver1 = RubisRestServer(Debug=True)
##    solver1.ping()
##    solver1.submitProblem(t,valuation='robust',Debug=True)
##    sleep(5)
##    solver1.saveXMCDA2Solution()
##    solver2 = RubisRestServer(Debug=True)
##    solver2.submitXMCDA2Problem('test',Debug=False)
##    sleep(5)
##    solver2.saveXMCDA2Solution()

def testFusionLDigraph():
    print('==>> Testing FusionLDigraph instantiation')
    t = Random3ObjectivesPerformanceTableau()
    geco = BipolarOutrankingDigraph(t,coalition=t.objectives['Eco']['criteria'],Normalized=True)
    genv = BipolarOutrankingDigraph(t,coalition=t.objectives['Env']['criteria'],Normalized=True)
    gsoc = BipolarOutrankingDigraph(t,coalition=t.objectives['Soc']['criteria'],Normalized=True)
    gfus = FusionLDigraph([geco,genv,gsoc],operator='o-max')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    print(g.computeOrdinalCorrelation(gfus))
