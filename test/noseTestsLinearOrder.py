#######################
# R. Bisdorff 
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsVotingDigraph.py
# # Current $Revision: 1.7 $
########################

from digraphs import *
#from perfTabs import *
from outrankingDigraphs import *
from linearOrders import *
from decimal import Decimal

##def testExtendedPrudentDigraph():
##    print('*-------- Testing ExtendedPrudentDigraph class -------')
##    t = RandomCBPerformanceTableau(numberOfActions=13)
##    t.save('testExtPrud')
##    g = BipolarOutrankingDigraph(t)
##    level = g.computePrudentBetaLevel(Debug=True)
##    gep = ExtendedPrudentDigraph(g,prudentBetaLevel=level,Debug=True)
##    gep.showRelationTable()

def testKemenyOrdering():
    print('*-------- Testing KemenyOrder class -------')
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.save('testKemeny')
    g = BipolarOutrankingDigraph(t)
    ke = KemenyOrder(g,Debug=True)

def testSlaterOrdering():
    print('*-------- Testing KemenyOrder class -------')
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.save('testKemeny')
    g = BipolarOutrankingDigraph(t)
    sl = SlaterOrder(g,Debug=True)

def testRankedPairsOrdering():
    print('*-------- Testing RankedPairsOrder class -------')
    t = RandomPerformanceTableau(numberOfActions=5)
    t.save()
    t.showPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    rp = RankedPairsOrder(g,isExtendedPrudent=False,Debug=True)
    rp.showRelationTable()
    eprp = RankedPairsOrder(g,isExtendedPrudent=True,Debug=True)
    eprp.showRelationTable()
    eprp.exportGraphViz('testorder')
    eprp.exportDigraphGraphViz('testdigraph')

def testKohlerOrdering():
    print("*==>> testing KohlerOrder Class ----*")
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.saveXMCDA2('testkohler')
    g = BipolarOutrankingDigraph(t)
    #g.showRelationTable()
    k = KohlerOrder(g,Debug=True)
    print(k.computeOrder())

def testNetFlowsOrdering():
    print("*==>> testing NetFlowsOrder Class ----*")
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.saveXMCDA2('testnf')
    g = BipolarOutrankingDigraph(t)
    #g.showRelationTable()
    nfo = NetFlowsOrder(g,coDual=False,Debug=True)
    print(nfo.computeOrder())

def testOutFlowsOrdering():
    print("*==>> testing OutFlowsOrder Class ----*")
    from linearOrders import _OutFlowsOrder
    t = RandomCBPerformanceTableau(numberOfActions=5)
    t.saveXMCDA2('testof')
    g = BipolarOutrankingDigraph(t)
    #g.showRelationTable()
    ofo = _OutFlowsOrder(g,coDual=False,Debug=True)
    print(ofo.computeOrder())

def testRandomLinearOrders():
    print("*==>> testing RandomLinearOrder Class ----*")
    g1 = RandomLinearOrder(numberOfActions=10,Debug=True)
    g1.showRelationTable()
    g2 = RandomLinearOrder(numberOfActions=10,Debug=True)
    g2.showRelationTable()
    print(g1.computeBipolarCorrelation(g2))
    g1 = RandomLinearOrder(numberOfActions=10,OutrankingModel=True,Debug=True)
    g1.showRelationTable()
    g2 = RandomLinearOrder(numberOfActions=10,OutrankingModel=True,Debug=True)
    g2.showRelationTable()
    print(g1.computeBipolarCorrelation(g2))

def testRankingCorrelations():
    print('*-------- Testing ranking qualities -------')
    from linearOrders import _OutFlowsOrder
    t = RandomCBPerformanceTableau(numberOfActions=7,numberOfCriteria=5,seed=100)
    g = BipolarOutrankingDigraph(t,Normalized=True)
    g.showRelationTable()
    print()
    print('==>> Kemeny ordering:')
    ke = KemenyOrder(g,Debug=False)
    #g.showRelationTable()
    print(ke.kemenyRanking)
    print(ke.kemenyOrder)
    print(g.computeOrdinalCorrelation(ke))
    print()
    print('==>> Slater ordering:')
    sl = SlaterOrder(g,Debug=False)
    #g.showRelationTable()
    print(sl.slaterRanking)
    print(sl.slaterOrder)
    corr = g.computeOrdinalCorrelation(sl)
    sl.showCorrelation(corr)
    print()
    print('==>> principal ordering:')
    pri = PrincipalOrder(g)
    #g.showRelationTable()
    print(pri.principalRanking)
    print(pri.principalOrder)
    print(g.computeOrdinalCorrelation(pri))
    print()
    print('==>> Copeland ordering:')
    cop = CopelandOrder(g)
    #g.showRelationTable()
    print(cop.copelandRanking)
    print(cop.copelandOrder)
    print(g.computeOrdinalCorrelation(cop))
    cop.showScores(direction='increasing')
    print()
    print('==>> net flows ordering:')
    nf = NetFlowsOrder(g)
    #g.showRelationTable()
    print(nf.netFlowsRanking)
    print(nf.netFlowsOrder)
    print(g.computeOrdinalCorrelation(nf))
    nf.showScores()
    print()
    print('==>> out flows ordering:')
    of = _OutFlowsOrder(g)
    #g.showRelationTable()
    print(of.outFlowsRanking)
    print(of.outFlowsOrder)
    print(g.computeOrdinalCorrelation(of))
    of.showScores(direction='increasing')
    print()
    print('==>> Kohler ordering:')
    ko = KohlerOrder(g)
    #g.showRelationTable()
    print(ko.kohlerRanking)
    print(ko.kohlerOrder)
    print(g.computeOrdinalCorrelation(ko))
    print()
    print('==>> ranked pairs ordering:')
    rp = RankedPairsOrder(g)
    #g.showRelationTable()
    print(rp.rankedPairsRanking)
    print(rp.rankedPairsOrder)
    print(g.computeOrdinalCorrelation(rp))
    print()
