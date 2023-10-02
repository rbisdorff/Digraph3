#######################
# R. Bisdorff
# pytest functions for the digraphs module
# ..$python3 -m pip install pytest  # installing the pytest package
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
    if not g.automorphismGenerators():
        print('nauty software not installed !!')
        print('On Ubuntu try: $sudo apt-get nauty ')
    else:
        g.showMIS()
        g.showOrbits(g.misset)
        print('grpsize', g.automorphismGroupSize)
        for choice in g.misset:
           g.computeOrbit(choice,True)

def testPerrinMis():
    print("==>> Testing perrinMIS.c generated missets read in from file !")
    g = CirculantDigraph(order=10,circulants=[1,-1])
    g.readPerrinMisset('../testreadmisset.dat')
    print(g.misset)
    try:
        g.automorphismGenerators()
    except:
        print('nauty software not installed !!')
        print('On Ubuntu try: $sudo apt-get nauty ')
        return
    g.showOrbitsFromFile('../testreadmisset.dat')
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
    try:
        g.automorphismGenerators()
    except:
        print('nauty software not installed !!')
        print('On Ubuntu try: $sudo apt-get nauty ')
        return
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
    g.isTransitive(Comments=True)

def testSymmetryDegree():
    print("==>> Testing the symmetry degree ---")
    g = RandomDigraph()
    g.showStatistics()
    d = g.computeSymmetryDegree()
    print('n0/n1', d)
    g.isSymmetric(Comments=True)

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

def testConvertValuation2Integer():
    print('*==>> testing convertValuation2Integer ----*')
    g = RandomValuationDigraph(ndigits=3)
    g.convertValuation2Integer(InSite=False,Comments=True)
    g.convertValuation2Integer(InSite=True,Comments=True)
    g.convertValuation2Integer(InSite=False,Comments=True)
    
def testKneserDigraph():
    print('*==>> testing Kneser digraphs ------*')
    g = KneserDigraph(n=5,j=2)
    g.showShort()
    g.showStatistics()
    if g.automorphismGenerators():
        print(g.automorphismGroupSize)
        g.showMIS()
        g.showOrbits(g.misset,withListing=False)

def testGridDigraphs():
    print('*==>> testing Grid digraphs ------*')
    g = GridDigraph(n=5,m=5)
    g.showShort()
    if g.automorphismGenerators():
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

def testWeakTournaments():
    print('*==>> weak tournaments ----*')
    t = RandomWeakTournament(order=5,ndigits=3)
    t.showRelationTable(ndigits=3)
    t = RandomWeakTournament(order=5,weaknessDegree=0.5)
    t.showRelationTable()
    t = RandomWeakTournament(order=5,IntegerValuation=True)
    t.showRelationTable()

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
    t.showCriteria(Debug=False)
    g = BipolarOutrankingDigraph(t)
    g.exportGraphViz()
    #t.showPerformanceTableau()
    g.showRelationTable()

def testPercentilesOfThresholds():
    print('*---------- test percentiles of variable thresholds --------*')
    t = RandomPerformanceTableau()
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
    t.saveXMCDA2('test')
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

def testExportPrincipalImage():
    print('*------- test exportRelationPCAImage --------*')
    t = RandomCBPerformanceTableau(numberOfActions=10,weightDistribution="equiobjectives")
    g = BipolarOutrankingDigraph(t)
    g.save('test')
    g = Digraph('test')
    g.showRelationTable()
    g.exportPrincipalImage('bipolar',bgcolor='lightblue')
    g.recodeValuation(0,2)
    g.exportPrincipalImage('monopolar',pictureFormat='xfig',fontcolor='black',fontsize='1.2')
   

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

def testFusionOperators():
    print('*------- test fusion operators ------*')
    from randomDigraphs import RandomValuationDigraph
    g1 = RandomValuationDigraph(order=5,seed=1)
    g2 = RandomValuationDigraph(order=5,seed=2)
    g3 = RandomValuationDigraph(order=5,seed=3)
    from digraphs import FusionLDigraph
    g1.showRelationTable()
    g2.showRelationTable()
    g3.showRelationTable()
    print('===> o-max')
    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-max')
    fga.showRelationTable()
    print('===> o-min')
    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-min')
    fga.showRelationTable()
    print('===> o-average')
    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-average')
    fga.showRelationTable()
    print('===> o-average, weights = [1,2,3]')
    fga = FusionLDigraph([g1,g2,g3],weights=[1,2,3],operator='o-average')
    fga.showRelationTable()

def testShortestPathLengthsComputation():
    print('*------- shortest path lengths ------*')
    from outrankingDigraphs import RandomBipolarOutrankingDigraph
    g = RandomBipolarOutrankingDigraph(seed=None)
    g.computeShortestPathLengths(Comments=True)
    g.computeDigraphCentres(Comments=True)
    g.computeShortestPathLengths(WeakPaths=True,Comments=True)
    g.computeDigraphCentres(WeakDistances=True,Comments=True)
    print(g)

def testBipartitePartialDigraph():
    print('*------- bipartite partial digraph extraction ----*')
    t = RandomCBPerformanceTableau(numberOfActions=10,weightDistribution="equiobjectives")
    from ratingDigraphs import RatingByRelativeQuantilesDigraph
    rrq = RatingByRelativeQuantilesDigraph(t,quantiles=5,LowerClosed=True)
    from digraphs import BipartitePartialDigraph
    bpg = BipartitePartialDigraph(rrq,rrq.actionsOrig,rrq.profiles)
    rrq.computeOrdinalCorrelation(bpg)
     
