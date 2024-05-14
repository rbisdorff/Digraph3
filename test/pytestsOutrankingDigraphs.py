#######################
# R. Bisdorff
# pytest functions for the outrankingDigraphs module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from outrankingDigraphs import *

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

def testPolarisedOutrankingDigraph():
    print('==>> Testing PolarisedOutrankingDigraph instantiation')
    t = RandomPerformanceTableau()
    g = BipolarOutrankingDigraph(t,Threading=True,startMethod='spawn')
    print(g.valuationdomain)
    ch = PolarisedOutrankingDigraph(g,level=0.50,AlphaCut=False,KeepValues=True)
    ch.showAll()
    ch.showStatistics()

def testForcedBestSingleChoice():
    print('*==>> testing forced best single choice  ----*')
    t = RandomCBPerformanceTableau(numberOfActions=15)
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
    g.showRelationTable(OddsDenotation=True)
    g.showRubisBestChoiceRecommendation(ChoiceVector=True,Comments=True)
    g.showRubyChoice(Comments=True,_OldCoca=True)
    g.showStatistics()
    print(g)
    
def testMoreOrlessRelatedPairs():
    print('*==>> test more or less unrelated pairs extraction ---*')
    t = RandomPerformanceTableau(numberOfActions=7)
    g = BipolarOutrankingDigraph(t)
    gcd = ~(-g)
    gcd.showRelationTable()
    print(gcd.valuationdomain)
    print('unrelated pairs:')
    print(gcd.computeUnrelatedPairs())
    print('more or less unrelated pairs:')
    print(gcd.computeMoreOrLessUnrelatedPairs())
    g.showVetos()

def testRobustoutranking():
    print('*==>> robust outranking ------------------*')
    t0 = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5)
    t0.saveXMCDA2('testXMLRubis')
    t = XMCDA2PerformanceTableau('testXMLRubis')
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    go = OrdinalOutrankingDigraph(t)
    go.showRelationTable()
    gu = UnanimousOutrankingDigraph(t)
    gu.showRelationTable()
    gc = BipolarOutrankingDigraph(t)
    gc.showRelationTable()
    gor = OldRobustOutrankingDigraph(t)
    gor.showRelationTable()
    
def testPairwiseComparisons():
    print('*==>> test show pairwise comparison-------*')
    t = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5)
    g = BipolarOutrankingDigraph(t)
    for x in g.actions:
        for y in g.actions:
            g.showPairwiseComparison(x,y)

def testPairwiseCompleteComparisons():
    print('*==>> test pairwise complete comparison-------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,numberOfCriteria=7)
    g = BipolarOutrankingDigraph(t) 
    g.showCriteriaCorrelationTable()
    g.showPerformanceTableau()
    g.export3DplotOfCriteriaCorrelation('criteriaCorrelation',pictureFormat="pdf",Comments=True)

def testCriteriaHierarchy():
    print('*==>> show Criteria Hierarchy --------------*')
    t = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=5,commonMode=('uniform',None,None))
    g = BipolarOutrankingDigraph(t)
    g.showCriteriaCorrelationTable()
    g.showCriteriaHierarchy()

def testCriteriaNetFlows():
    print('*==>> show Criteria net flows --------------*')
    g = RandomBipolarOutrankingDigraph()
    print(g.computeSingleCriteriaNetflows())
    g.saveSingleCriterionNetflows()

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
    d0kn = gn.computeODistance(g0)
    print('maximal distance:', d0kn)      
    print('original distance:', gn.computeODistance(g))   
    gn.showRelationTable()

def testRubisRanking():
    print('*-------  test rubisRanking -----*')
    t = RandomCBPerformanceTableau(numberOfActions=9,numberOfCriteria=5,IntegerWeights=False,commonPercentiles={'ind':10,'pref':20,'veto':60},valueDigits=4)
    g = BipolarOutrankingDigraph(t)
    print(g.valuationdomain)
    g.computeSingletonRanking(Comments = True)
    print(g.valuationdomain)

def testGlobalOutrankingCorrelation():
    print('*----- test global outranking correlation -----*')
    t = RandomCBPerformanceTableau(numberOfActions=15,numberOfCriteria=3)
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
        medianKCorrelation[x] = g.bipolarKDistance(gx) 
    print('median K-Correlation:', medianKCorrelation)

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
    t = RandomPerformanceTableau(numberOfActions=7,numberOfCriteria=13)
    g = EquiSignificanceMajorityOutrankingDigraph(t)
    print(g.computeWeightPreorder())
    g.showRelationTable()
    gr = RobustOutrankingDigraph(t)
    gr.showRelationTable()
            
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
##    g.saveCriteriaCorrelationTable('crit.prn')
##    g.saveActionsCorrelationTable('act.prn')
    g.export3DplotOfActionsCorrelation(plotFileName='actionsCorrelation')

        
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
    gcd.computeKemenyOrder(Debug=True)
    print(gcd.computeKemenyRanking(seed=1,sampleSize=500))    
    gcd.computeSlaterOrder(Debug=True)
    print(gcd.computeSlaterOrder(isProbabilistic=False, seed=1,sampleSize=500))

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
    t = RandomCBPerformanceTableau(numberOfActions=15,\
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
    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=True,startMethod='spawn')
    #Threading = True
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalOutrankingCorrelations(Threading=True,startMethod='spawn')
    print(time()-t0)
    print(criteriaCorrelations)
    #Threading = False
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalOutrankingCorrelations()
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
    criteriaCorrelations = g.computeMarginalVersusGlobalRankingCorrelations(ranking,Threading=Threading,startMethod=None)
    print(time()-t0)
    print(criteriaCorrelations)
    Threading = False
    t0 = time()
    criteriaCorrelations = g.computeMarginalVersusGlobalRankingCorrelations(ranking,
                            Threading=Threading)
    print(time()-t0)
    print(criteriaCorrelations)

def testComputeMarginalObjectivesVersusGlobalRankingCorrelations():
    print('*-------- Threaded MarginalVersusGlobalOutranking -------')
    t = RandomCBPerformanceTableau(numberOfActions=50,\
                                   numberOfCriteria=21,\
                                   weightDistribution='equiobjectives',
                                   seed=100) 
    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=True)
    ranking = g.computeNetFlowsRanking()
    Threading = True
    t0 = time()
    objectivesCorrelations = g.computeMarginalObjectivesVersusGlobalRankingCorrelations(
                               ranking,Comments=True,
                               Threading=Threading,
        startMethod=None)
    print(time()-t0)
    Threading = False
    t0 = time()
    objectivesCorrelations = g.computeMarginalObjectivesVersusGlobalRankingCorrelations(
                               ranking,Comments=True,
                               Threading=Threading)
    print(time()-t0)

def testFusionLDigraph():
    print('==>> Testing FusionLDigraph instantiation')
    t = Random3ObjectivesPerformanceTableau()
    geco = BipolarOutrankingDigraph(t,coalition=t.objectives['Eco']['criteria'],Normalized=True)
    genv = BipolarOutrankingDigraph(t,coalition=t.objectives['Env']['criteria'],Normalized=True)
    gsoc = BipolarOutrankingDigraph(t,coalition=t.objectives['Soc']['criteria'],Normalized=True)
    gfus = FusionLDigraph([geco,genv,gsoc],operator='o-max')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    print(g.computeOrdinalCorrelation(gfus))

def testAverageFusionLDigraphs():
    print('==>> Testing Average Fusion Digraphs instantiation')
    from random import randint
    t = Random3ObjectivesPerformanceTableau(numberOfActions=7,\
                                   numberOfCriteria=9,\
                                   vetoProbability=0.5,\
                                   seed=randint(1,1000))
    print(t)
    afg = UnOpposedBipolarOutrankingDigraph(t,Comments=True)
    afg.showRelationTable()
    afg = SymmetricAverageFusionOutrankingDigraph(t,Comments=True)
    afg.showRelationTable()
