#######################
# R. Bisdorff
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsDigraph.py
# # Current $Revision: 1.53 $
########################

from digraphs import *
from outrankingDigraphs import *
from randomPerfTabs import _RandomS3PerformanceTableau\
     as RandomS3PerformanceTableau
from randomPerfTabs import _FullRandomPerformanceTableau as\
     FullRandomPerformanceTableau
from randomPerfTabs import _RandomCoalitionsPerformanceTableau as\
     RandomCoalitionsPerformanceTableau

def testShowMethods():

    print('==>> Testing printing of digraph data and parameters')
    g = RandomDigraph()
    g.showShort()
    g.recodeValuation(newMax=20,newMin=10)
    g.showAll()
    g.showStatistics()

def testQualChoices():

    print('==>> Testing qualified maximal choices extraction')
    g = RandomBipolarOutrankingDigraph(numberOfActions=5,numberOfCriteria=7)
    g.showMIS()
    g.showMaxDomIrred()
    g.showMaxAbsIrred()

    print('==>> Testing qualified minimal choices extraction')
    g = RandomValuationDigraph(order=5)
    g.showAll()
    g.showPreKernels()
    g.showMinDom()
    g.showMinAbs()

def testRandomDigraph():

    print('==>> Testing generating random digraphs')
    h = RandomDigraph(order=5)
    h.showStatistics()
    h.showAll()

def testSave1():
    print('==>> Testing save method for class instances')
    h = RandomDigraph(order=5)
    h.save()
    print('==>> Testing reload of saved digraph instance')
    f = Digraph('tempdigraph')
    f.showStatistics()

def testEmptyCompleteDigraph():
    print('==>> Testing empty and complete graph instantiation')
    g = EmptyDigraph(order=20, valuationdomain=(0,100))
    g.showAll()
    g.showStatistics()
    f = CompleteDigraph(valuationdomain=(-10,10))
    f.showAll()
    f.showStatistics()

def testPerformanceTableau():
    print('==>> Testing Performance Tableau instantiation')
    t = RandomPerformanceTableau()
    t.showAll()
    t.save('testSavePerftab')
    tb = PerformanceTableau('testSavePerftab')
    tb.showAll()
    g = BipolarOutrankingDigraph(tb)
    g.showAll()

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
    t = RandomCBPerformanceTableau(numberOfActions=10,numberOfCriteria=13,
                                   #commonThresholds=None,
                                   commonPercentiles={'ind':5,'pref':10,'veto':90},
                                   weightDistribution="random",
                                   weightScale=None,IntegerWeights=True,
                                   #commonScale=[0.0,100.0],
                                   commonMode=["normal",50.0,25.0],
                                   Debug=False)
    print(t.hasOddWeightAlgebra(Debug=True))

def testCirculantDigraph():
    print('==>> Testing CirculantDigraph instantiation')
    circ7 = CirculantDigraph()
    circ7.showAll()
    circ7.showStatistics()
    circ10 = CirculantDigraph(order=10)
    circ10.showAll()
    circ10.showStatistics()
    circ8 = CirculantDigraph(order=8,valuationdomain={'min':0,'max':1})
    circ8.showAll()
    circ8.showStatistics()
    k5 = CirculantDigraph(order=5,circulants=[-1,1,-2,2])
    k5.showAll()
    k5.showStatistics()

def testKernelsGenerator():
    print('==>> Testing kernels generators')
    g = RandomDigraph()
    g.showAll()
    print('Dominant Kernels')
    for choice in g.generateDomPreKernels():
        print(list(choice))
    print('Absorbent Kernels')
    for choice in g.generateAbsPreKernels():
        print(list(choice))

def testHertzMisGenerator():
    print("==>> Testing Hertz's MIS generator")
    c12 = CirculantDigraph(order=12)
    c12.showMIS_AH()

def testSymmetries():
    print("==>> Testing Symmetries in digraphs")
    g = CirculantDigraph(order=14,circulants=[1,-1])
    g.automorphismGenerators()
    g.showAutomorphismGenerators()
    print('grpsize', g.automorphismGroupSize)
    g.showMIS()
    g.showOrbits(g.misset)
    for choice in g.misset:
       g.computeOrbit(choice,True)

def testPerrinMis():
    print("==>> Testing perrinMIS.c generated missets read in from file !")
    g = CirculantDigraph(order=10,circulants=[1,-1])
    g.readPerrinMisset('testreadmisset.dat')
    print(g.misset)
    g.automorphismGenerators()
    g.showOrbitsFromFile('testreadmisset.dat')
    g.showOrbits(g.misset)

def testshowNonIsomorphicMIS(cycleOrder=10):
    print("==>> Testing perrinMIS C ressource and non isomorphic MIS generation")  
    import os
    commandString = ('echo %d| perrinMIS' % (cycleOrder))
    print(commandString)
    try:
        os.system(commandString)
    except:
        print('perrinMIS not installed !!')
        return
    g = CirculantDigraph(order=cycleOrder,circulants=[-1,1])
    g.automorphismGenerators()
    g.showOrbitsFromFile('curd.dat')

def testRandomRegularDigraph():
    print("==>> Testing random regular graph generation")
    g = RandomRegularDigraph(order=12,degree=4)
    g.showAll()
    g.showStatistics()

def testRandomFixedSizeDigraph():
    print("==>> Testing random fixed size digraph generation")
    g = RandomFixedSizeDigraph(order=12,size=40)
    g.showAll()
    g.showStatistics()

def testRandomFixedDegreeSequenceDigraph():
    print("==>> Testing random fixed degree sequence graph generation")
    g = RandomFixedDegreeSequenceDigraph(order=10,degreeSequence=[3,3,3,2,2,2,1,1,1,0])
    g.showAll()
    g.showStatistics()

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

def testKChoicesDigraph():
    print('*==>> testing k-choices digraph ----*')
    g = RandomDigraph(order=5)
    h = kChoicesDigraph(g)
    h.showAll()

def testTransitivityDegree():
    print("==>> Testing the transitivity degree ---")
    g = RandomDigraph()
    g.showStatistics()
    d = g.computeTransitivityDegree()
    print('n0/n1', d)

def testStrongComponents():
    print("==>> Testing the strong components ---")
    g = RandomBipolarOutrankingDigraph()
    g.showStatistics()
    print('strongComponents: ', g.strongComponents())

def testFixpointAlgorithmes():
    print("==>> Testing Pirlot's and Bisdorff's fixpoint algorithm ---")
    g = RandomValuationDigraph()
    g.showStatistics()
    print("Good Choices with Pirlot's algorithm")
    g.computeGoodPirlotChoices(Comments=True)
    print("Good Choices with Bisdorff's algorithm")
    g.computeGoodChoices(Comments=True)
    print(g.goodChoices)
    print('-------')
    print("Bad choices with Pirlot's algorithm")
    g.computeBadPirlotChoices(Comments=True)
    print("Bad Choices with Bisdorff's algorithm")
    g.computeBadChoices(Comments=True)
    print(g.badChoices)

# def testXMLSaveReadDigraph():
#     print('*==>> testing XML save and read procedure ----*')
#     g = RandomBipolarOutrankingDigraph()
#     g.showAll()
#     g.saveXML(name='randXML',category='outranking',subcategory='random',author='RB',reference='Digraph implementation')
#     g1 = XMLDigraph('randXML')
#     g1.showAll()

# def testXMLSaveReadPerformanceTableau():
#     print('*==>> testing XML save and read performance tableaus ----*')
#     t = RandomPerformanceTableau()
#     t.showAll()
#     t.saveXML(name='randperftabXML',category='standard',subcategory='random',author='RB',reference='Digraph implementation')
#     t1 = XMLPerformanceTableau('randperftabXML')
#     t1.showAll()
#     g = BipolarOutrankingDigraph(t1)
#     g.showRubyChoice()
#     print('Name : ',t1.name)
#     print('Actions : ', t1.actions)
#     print('Criteria : ', t1.criteria)
#     print('Evaluations :', t1.evaluation)

def testRandomValuationDigraph():
    print('*==>> testing RandomValuationDigraph ----*')
    g = RandomValuationDigraph(ndigits=3)
    h = PolarisedDigraph(g,0.70)
    h.showRelationTable()
    h.save('testPol')
    hp = Digraph('testPol')
    g.showRelationTable()
    g.save('testVal')
    gs = Digraph('testVal')

def testKneserDigraph():
    print('*==>> testing Kneser digraphs ------*')
    g = KneserDigraph(n=5,j=2)
    g.showShort()
    g.showStatistics()
    g.automorphismGenerators()
    print(g.automorphismGroupSize)
    g.showMIS()
    g.showOrbits(g.misset,withListing=False)

def testGridDigraphs():
    print('*==>> testing Grid digraphs ------*')
    g = GridDigraph(n=5,m=5)
    g.showShort()
    g.automorphismGenerators()
    print(g.automorphismGroupSize)
    g.showMIS_AH()
    g.showOrbits(g.hertzmisset,withListing=False)

def testGraphVizExport():
    print('*==>> graphViz dot & png file exportation ----*')
    g = RandomBipolarOutrankingDigraph(numberOfActions = 7)
    g.showRubyChoice(Comments=True)
    #g.exportGraphViz(fileName='gtest',bestChoice=g.bestChoice,worstChoice=g.worstChoice,Comments=False,graphType='png',graphSize='7,7')
    g.exportGraphViz(fileName='gtest',bestChoice=g.bestChoice,worstChoice=g.worstChoice,Comments=True,graphType='pdf',graphSize='7,7')

def testDigraphDecomposition():
    print('*==>> testing decomposition of digraphs -----*')
    g = RandomDigraph()
    g.showPreKernels()
    g.exportGraphViz()
    ga = AsymmetricPartialDigraph(g)
    ga.showAll()
    ga.showPreKernels()
    ga.exportGraphViz()
    gs = SymmetricPartialDigraph(g)
    gs.showAll()
    gs.showPreKernels()
    gs.exportGraphViz()

def testPerformanceTableauStatistics():
    print('*==>> performanceTableau statistics ---------*')
    t = FullRandomPerformanceTableau(commonScale=(0.0,100.0),numberOfCriteria=10,numberOfActions=10,commonMode=('triangular',30.0,0.7))
    t.showStatistics()
    print(t.computeNormalizedDiffEvaluations(lowValue=0.0,highValue=100.0,withOutput=True,Debug=True))
    t = RandomCBPerformanceTableau()
    t.showStatistics()
    t.showEvaluationStatistics()

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

def testZoomingValuations():
    print('*==>> zooming the valuation of digraphs ------*')
    g = RandomValuationDigraph()
    print(g.valuationdomain)
    print(g.relation)
    g.showRelationTable()
    g.zoomValuation(2.0)
    print(g.valuationdomain)
    print(g.relation)
    g.showRelationTable()
    g.zoomValuation(0.25)
    print(g.valuationdomain)
    print(g.relation)
    g.showRelationTable()

# def testXMCDASaveReadDigraph():
#     print('*==>> save XMCDA Digraph --------------*')
#     g = RandomValuationDigraph()
#     g.saveXMCDA('testXMCDADigraph',valuationType='bipolar', relationName='Stilde',servingD3=False)
#     g = XMCDADigraph('testXMCDADigraph')
#     g.showAll()

def testWeakTournaments():
    print('*==>> weak tournaments ----*')
    t = RandomWeakTournament(order=5,ndigits=3)
    t.showRelationTable(ndigits=3)
    t = RandomWeakTournament(order=5,weaknessDegree=0.5)
    t.showRelationTable()
    t = RandomWeakTournament(order=5,IntegerValuation=True)
    t.showRelationTable()

# def testXMCDAPerformanceTableauLoading():
#     print('*==>> XMCDA Performance tableau loading ---*')
#     t = RandomCBPerformanceTableau()
#     t.saveXMCDA('testxmcda')
#     t = XMCDAPerformanceTableau('testxmcda')
#     t.showPerformanceTableau()
#     g = BipolarOutrankingDigraph(t)
#     g.showRelationTable()
#     g.save('testdecimal')
#     gd = Digraph('testdecimal')

def testODistance():
    print('*==>> verifying ODistance between digraphs ---*')
    g1 = RandomValuationDigraph(order=3)
    print(g1.valuationdomain)
    g1.save()
    g2 = RandomValuationDigraph(order=3)
    g1.computeODistance(g2)
    #g1.recodeValuation(-1.0,1.0)
    g2.recodeValuation(-1.0,1.0)
    g1.computeODistance(g2)

def testPerformanceDifferencesPerCriteria():
    print('*==>> verifying  performance differences per criteria ---*')
    g = RandomBipolarOutrankingDigraph()
    g.showPerformanceTableau()
    g.computePerformanceDifferences(Comments=True)

def testCoca_BreakAdd_BrokenCocsDigraph():
    print('==>> Testing Coca_ BreakAdd_ and BrokenCocsDiGraph instantiation')
    g = RandomValuationDigraph(order=10)
    #g = RandomWeakTournament(order=5)
    #g.save('testCoca')
    #g = Digraph('testCoca')
    print(g.valuationdomain)
    gp = PolarisedDigraph(g,0.2)
    #gp = IndeterminateDigraph(order=5)
    h1 = CocaDigraph(digraph=gp,Comments=True)
    h1.save('rescoca2')
    h1.showAll()
    g = RandomValuationDigraph(order=10)
    h2 = BreakAddCocsDigraph(digraph=g,Comments=True)
    h2.save('resbradco2')
    h2.showAll()
##    t = RandomPerformanceTableau(25)
##    g = BipolarOutrankingDigraph(t)
    g = RandomValuationDigraph(order=10,seed=3)
    h3 = BrokenCocsDigraph(digraph=g,Comments=True)
    h3.save('resbreakco2')
    h3.showAll()
    
    #h.showRelationTable()
    #h.showRelation()

def testXORDigraph():
    print('*----- test XORDigraph -----*')
    g1 = RandomBipolarOutrankingDigraph(numberOfActions = 10, numberOfCriteria=1)
    g1.showShort()
    g1.showRelationTable()
    g2 = RandomBipolarOutrankingDigraph(numberOfActions = 10, numberOfCriteria=1)
    g2.showShort()
    g2.showRelationTable()
    gxor = XORDigraph(g1,g2,Debug=False)
    gxor.showShort()
    gxor.showRelationTable()

    print('size of XOR(g1,g2) = ', gxor.computeSize())
    print('crisp K-Distance d(g1,g2) = ', g1.crispKDistance(g2))
    print('bipolar K-Correlation d(g1,g2) = ', g1.bipolarKCorrelation(g2))
    print('bipolar K-Distance d(g2,g1) = ', g2.bipolarKDistance(g2))
    print('determination = ', g1.computeDeterminateness(),\
                              g2.computeDeterminateness(),\
                              gxor.computeDeterminateness())

def testIndeterminateDigraph():
    print('*----- test IndeterminateDigraph -----*')
    g = RandomValuationDigraph()
    m = IndeterminateDigraph(g)
    g.showShort()
    g.showRelationTable()

def testCBPerformanceTableau():
    print('*==>> random CB Performance Tableaux ------------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,\
                                   commonPercentiles={'ind':5,'pref':10,'veto':95},\
                                   weightDistribution="random",\
                                   weightScale=[1,2],\
                                   IntegerWeights=True,\
                                   commonMode=["normal",50.0,25.0])
    #t.showAll()
    #t = RandomCBPerformanceTableau(numberOfActions=13,numberOfCriteria=20,IntegerWeights=True,comments=False)
    t.saveXMCDA(fileName='randomPerformanceTableau',servingD3=False)
    t.showCriteria(Debug=False)
    #t = XMCDAPerformanceTableau('randomPerformanceTableau')
    g = BipolarOutrankingDigraph(t)
    #g.showCriteriaCorrelationTable()
    g.exportGraphViz()
    #t.showPerformanceTableau()
    #g.showRelationTable()
    #g.showRubyChoice()

def testRandomS3PerformanceTableau():
    print('*==>> random S3 Performance Tableaux ------------*')
    t = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=7,VariableGenerators=True,commonThresholds=[(5.0,0.0),(10.0,0.0),(65.0,0.0)],commonMode=['beta',0.5,None],Debug=False,OrdinalScales=False,Coalitions=False,RandomCoalitions=True)
    t.saveXMCDA2(fileName='randomS3PerformanceTableau',servingD3=False)
    for g in t.criteria:
        print('==>>', g, t.computeThresholdPercentile(g,'ind'))
        for a in t.actions:
            print(t.actions[a]['generators'][g])
    t = XMCDA2PerformanceTableau('randomS3PerformanceTableau')
    g = Electre3OutrankingDigraph(t)
    #g.defaultDiscriminationThresholds()
    g.showCriteria()
    g.showCriteriaCorrelationTable()
    ## ## g.exportGraphViz()
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

def testCriterionRelationTable():
    print('*---- testing criterion relation table ----*')
    t = RandomS3PerformanceTableau(numberOfActions=5,numberOfCriteria=5)
    g = Electre3OutrankingDigraph(t)
    for c in g.criteria:
        g.showCriterionRelationTable(c)
    ## gr = OldRobustOutrankingDigraph(t)
    ## gr.showRelationTable()
    ## go = BipolarOutrankingDigraph(t)
    for x in g.actions:
        for y in g.actions:
            g.showPairwiseComparison(x,y)
    ## go.showRelationTable()
    ## go.showPairwiseComparison('a03','a05')

def testAMPLDataFileGeneration():
    print('*----- save AMPL Data file from robust outranking digraph ---*')
    #t = RandomCBPerformanceTableau(numberOfActions=20,numberOfCriteria=7,weightDistribution="random",weightScale=(1,7),IntegerWeights=True,commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0)])
    t = RandomS3PerformanceTableau(numberOfActions=10,numberOfCriteria=15,weightDistribution="random",weightScale=(1,13),IntegerWeights=True,commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0)],RandomCoalitions=True,commonMode=['beta',0.5,None])
    t.saveXMCDA('temp1',servingD3=False)
    #t = XMCDAPerformanceTableau('temp1')
    gr = OldRobustOutrankingDigraph(t)
    gr.saveAMPLDataFile(Unique=True,Comments=True)
    #gr.showCriteria()
    gr.showRelationTable()
    #print go.relation['a13']['a11']

def testXMCDA2SaveReadDigraph():
    print('*==>> save and read XMCDA-2.0 Digraph instances --------------*')
    g = RandomOutrankingDigraph()
    g.recodeValuation(-1.0,1.0)
    g.saveXMCDA2('testXMCDA2Digraph',valuationType='bipolar', relationName='S',servingD3=False)
    g1 = XMCDA2Digraph('testXMCDA2Digraph')
    g1.showAll()
    g.showAll()

def testXMCDA2SaveReadPerformanceTableau():
    print('*==>> save and read XMCDA-2.0 PerformanceTableau instances ----*')
    #t = RandomS3PerformanceTableau(numberOfActions=5,numberOfCriteria=15,weightDistribution="random",weightScale=(1,13),IntegerWeights=True,commonThresholds=[(5.0,0.0),(10.0,0.0),(50.0,0.0),(60.0,0.0)],RandomCoalitions=True,commonMode=['beta',0.5,None])
    #t.showAll()
    t = RandomCBPerformanceTableau(numberOfActions=5,numberOfCriteria=7,weightDistribution="random",weightScale=(1,7),IntegerWeights=True)
    t.saveXMCDA('test')
    g = BipolarOutrankingDigraph(t)
    g.showRelationTable()
    t1 = XMCDA2PerformanceTableau('test')
    g1 = BipolarOutrankingDigraph(t1)
    g1.showRelationTable()

def testChordlessOddCircuits():

    print('*----- test chordlessCircuits extraction -----*')
    #g = RandomValuationDigraph(order=30)
    #g.exportGraphViz()
    g = RandomOutrankingDigraph(numberOfActions=10)
    #g = RandomDigraph(order=20)
    g.computeChordlessCircuits(Odd=False, Comments=True)
    ## g.showChordlessCircuits()
    ## g.computeChordlessCircuits(Odd=True, Comments=True)
    g.showChordlessCircuits()
    #g.showCircuits()
    import time
    t0 = time.time()
    gc = CocaDigraph(g,Comments=True)
    t1 = time.time()
    #gc.showChordlessCircuits()
    print('Execution time: ' + str(t1-t0) + 'sec.')
    print('CocaDigraph order: ', gc.order)
    #gc.showStatistics()
    #g.showRubyChoice()

def testRandomTournament():
    print('*----- test RandomTournament -----*')
    t = RandomTournament(order=5,ndigits=3,Crisp=False)
    t.showRelationTable()
    t = RandomTournament(order=5,Crisp=True)
    t.showRelationTable()
    t = RandomTournament(order=5,valuationDomain=(-10,10))
    t.showRelationTable()

def testChordlessCircuits():
    print('*----- test chordlessCircuits extraction -----*')
    g = RandomOutrankingDigraph(numberOfActions=10)
    g.computeChordlessCircuits(Odd=False, Comments=True)
    g.showChordlessCircuits()
    import time
    t0 = time.time()
    gc = CocaDigraph(g,Comments=True)
    t1 = time.time()
    print('Execution time: ' + str(t1-t0) + 'sec.')
    print('CocaDigraph order: ', gc.order)

def testIntegerRandomDigraph():
    print('==>> Testing Integer RandomDigraph() class instantiation ')
    g = RandomDigraph(order=10,IntegerValuation=True)
    g.save()
    g.computeChordlessCircuits(Comments=True,Debug=True)

def testStrongComponentsCollapsedDigraph():
    print('*---- test strong components collapsed digraph -----*')
    t = RandomCBPerformanceTableau(numberOfActions=13,numberOfCriteria=7)
    g = BipolarOutrankingDigraph(t)
    gscc = StrongComponentsCollapsedDigraph()
    gscc = StrongComponentsCollapsedDigraph(g)
    gscc.showActions()
    gscc.showRelationTable()
    gscc.exportGraphViz()

def testCoDualDigraph():
    print('*---- test codual digraph -----*')
    t = RandomCBPerformanceTableau(numberOfActions=13,numberOfCriteria=7)
    g = BipolarOutrankingDigraph(t)
    g.save('testcodual')
    gasym = AsymmetricPartialDigraph(g)
    gasym.exportGraphViz('gtest')
    gcd = CoDualDigraph(g)
    gcd.exportGraphViz('gcdtest')

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

def testHTMLMaps():
    from outrankingDigraphs import BipolarOutrankingDigraph
    from randomPerfTabs import RandomCBPerformanceTableau
    from linearOrders import CopelandOrder
    t1 = Random3ObjectivesPerformanceTableau(numberOfActions=10,seed=1)
    g = BipolarOutrankingDigraph(t1,Normalized=True)
    cop = CopelandOrder(g)
    print(g._htmlRelationMap(cop.copelandRanking))
    print(g._htmlRelationMap(Colored=False))

def testCoveringIndex():
    print('*--- test computing the covering index for a choice ---*')
    g = RandomDigraph(order = 10,arcProbability=0.4)
    g.computePreKernels()
    for kernel in g.dompreKernels:
        print(kernel, g.coveringIndex(kernel,direction='out'))
    for kernel in g.abspreKernels:
        print(kernel, g.coveringIndex(kernel,direction='in'))

def testActionsCorrelation():
    print('*---- test computing actions correlation table and digraph ---*')
    g = RandomOutrankingDigraph()
    g.showStatistics()
    print(g.computeActionsComparisonCorrelations())
    g.saveCriteriaCorrelationTable('crit.prn')
    g.saveActionsCorrelationTable('act.prn')
    g.export3DplotOfActionsCorrelation('actionsCorrelation')

# def testRandomTree():
#     print('*---- random tree instance generation ---*')
#     t = RandomTree(numberOfNodes=10)
#     t.showAll()
#     t.exportGraphViz()

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
    #gcd._computeRankedPairsOrder(Debug=True)
    #print(gcd._computeRankedPairsOrder())

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
##    p = _Preorder(gcd,'best')
##    strc = StrongComponentsCollapsedDigraph(p)
##    strc.showComponents()
##    p = _Preorder(gcd,'worst')
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

def testCoceDigraph():
    print('*----- test rxperimental CoceDigraph class ----*')
    from digraphs import _CoceDigraph
    t = RandomCBPerformanceTableau(numberOfActions=10)
    g = BipolarOutrankingDigraph(t)
    coceg = _CoceDigraph(g,Comments=True)
    coceg.computeChordlessCircuits()
    print(coceg.computeDeterminateness())
    print(coceg.computeDeterminateness())
    print(g.computeBipolarCorrelation(coceg))
    print(g.computeOrdinalCorrelation(coceg))

def testEquivDigraph():
    print('*----- test EquivDigraph class ----*')
    t = RandomCBPerformanceTableau(numberOfActions=10)
    g = BipolarOutrankingDigraph(t)
    t1 = RandomCBPerformanceTableau(numberOfActions=10)
    g1 = BipolarOutrankingDigraph(t1)
    equivg = EquivalenceDigraph(g,g1)
    print(equivg.computeDeterminateness())
    print(equivg.computeDeterminateness())
    print(g.computeBipolarCorrelation(equivg))
    print(g.computeOrdinalCorrelation(equivg))

def testUnaryOperatorsNegationInverse():
    print('*----- test negation and inverse operators (- ~) ----*')
    g1 = RandomValuationDigraph(Normalized=True,IntegerValuation=True)
    g1.showRelationTable()
    g1.computeValuationStatistics(Comments=True)
    dg1 = -g1
    dg1.showRelationTable()
    cg1 = ~g1
    cg1.showRelationTable()
    g1 = RandomOutrankingDigraph()
    cdg1 = -(~g1)
    cdg1.showRelationTable()
    cd = CoDualDigraph(g1)
    cd.showRelationTable()

##def testOptimalRankingByChoosing():
##    print('*-------  test optimalRankingByChoosing method ------*')
##    t = RandomCBPerformanceTableau(numberOfActions=20)
##    t.save('test')
##    t = PerformanceTableau('test')
##    g = BipolarOutrankingDigraph(t)
##    g.iterateRankingByChoosing(Odd=False,Debug=False,CoDual=True)
##    g.showRankingByChoosing()
##    print('-----------------')
##    rankings = g.optimalRankingByChoosing(Odd=True,Debug=False,CoDual=True,Comments=True)
##    print(rankings)
##    g.showRankingByChoosing()
##    print('-----------------')
##    #print('Prudent first choice: ',g.computePrudentBestChoiceRecommendation(CoDual=False,Debug=False,Comments=True))

def testExportPrincipalImage():
    print('*------- test exportRelationPCAImage --------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,weightDistribution="equiobjectives")
    g = BipolarOutrankingDigraph(t)
    g.save('test')
    g = Digraph('test')
    g.showRelationTable()
    g.exportPrincipalImage()

def testCompleteness():
    print('*------- test (Weakly) Completeness ------*')
    g = RandomValuationDigraph()
    g.showRelationTable()
    print('Relation %s is complete ? %s' % (g.name,str(g.isComplete(Debug=True))))
    print('Relation %s is weakly complete ? %s' % (g.name,str(g.isWeaklyComplete(Debug=True))))
    t = RandomCBPerformanceTableau(numberOfActions=9,numberOfCriteria=5,weightDistribution='equiobjectives')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    g.showRelationTable()
    print('Relation %s is complete ? %s' % (g.name,str(g.isComplete(Debug=True))))
    print('Relation %s is weakly complete ? %s' % (g.name,str(g.isWeaklyComplete(Debug=True))))
    gcd = CoDualDigraph(g)
    gcd.showRelationTable()
    print('Relation %s is complete ? %s' % (gcd.name,str(gcd.isComplete(Debug=True))))
    print('Relation %s is weakly complete ? %s' % (gcd.name,str(gcd.isWeaklyComplete(Debug=True))))    

def testGraphBorderInner():
    print('*------- test graph border and inners ------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,weightDistribution="equiobjectives")
    g = BipolarOutrankingDigraph(t)
    bg = GraphBorder(g,Debug=True)
    ig = GraphInner(g,Debug=True)
    rg = FusionDigraph(bg,ig)
    Digraph.exportGraphViz(rg,(g.name+'fused'))

def testmaxHoleSize():
    print('*------- test maximal hole size ------*')
    g = RandomValuationDigraph(order=20)
    g.computeMaxHoleSize(Comments=True)
    print('Nbr of holes', g.nbrOfHoles)
    print('Maximal hole size', g.maxHoleSize) 
