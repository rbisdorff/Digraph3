#######################
# R. Bisdorff 
# weakOrders.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsWeakOrders.py
# # Current $Revision: $
########################

from outrankingDigraphs import *
from weakOrders import *

def testRankingByChoosingWithKernels():
    print('=== >>> testing best and last fusion (default)')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rcg0 = RankingByChoosingDigraph(g,Debug=False)
    rcg0.showWeakOrder()
    rcg0.showRankingByChoosing()
    print(rcg0.computeOrdinalCorrelation(g))
    print('=== >>> best') 
    rcg1 = RankingByBestChoosingDigraph(g,Debug=False)
    rcg1.showWeakOrder()
    print(rcg1.computeOrdinalCorrelation(g))
    print('=== >>> last')
    rcg2 = RankingByLastChoosingDigraph(g,Debug=False)
    rcg2.showWeakOrder()
    print(rcg2.computeOrdinalCorrelation(g))

def testOrderedRelationTableShowing():
    print('=== >>> testing ordered relation tables showing')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rbc = RankingByChoosingDigraph(g,Debug=False)
    rbc.showOrderedRelationTable()
    rbc.showOrderedRelationTable(direction='increasing')
    
def testPrincipalInOutDegreesRanking():
    print('=== >>> principal preorder')
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=10)
    rcf = PrincipalInOutDegreesOrdering(g,imageType="pdf",Debug=False)
    rcf.showWeakOrder()
    print(rcf.computeOrdinalCorrelation(g))

