#######################
# R. Bisdorff 
# weaklyTransitiveDigraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsWeaklyTransitiveDigraph.py
# # Current $Revision: $
########################

from outrankingDigraphs import *
from weaklyTransitiveDigraphs import *

def testWeakTransitiveConstructors():
    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=15)
    print('=== >>> testing best and last fusion (default)')
    rcg0 = RankingByChoosingDigraph(g,Debug=False)
    rcg0.showPreOrder()
    print(rcg0.computeOrdinalCorrelation(g))
    print('=== >>> best') 
    rcg1 = RankingByChoosingDigraph(g,Best=True,Last=False,Debug=False)
    rcg1.showPreOrder()
    print(rcg1.computeOrdinalCorrelation(g))
    print('=== >>> last')
    rcg2 = RankingByChoosingDigraph(g,Best=False,Last=True,Debug=False)
    rcg2.showPreOrder()
    print(rcg2.computeOrdinalCorrelation(g))
    print('=== >>> bipolar best and last')
    rcg3 = RankingByChoosingDigraph(g,Best=False,Last=False,Debug=False)
    rcg3.showPreOrder()
    print(rcg3.computeOrdinalCorrelation(g))
    print('=== >>> principal preorder')
    rcf = PrincipalInOutDegreesOrdering(g,imageType="pdf",Debug=False)
    rcf.showPreOrder()
    print(rcf.computeOrdinalCorrelation(g))

