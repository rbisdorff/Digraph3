#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 nose   # installing the nose test environment)
# ..$ nosetests3 -vs noseTestsIntegerOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################

#from cIntegerOutrankingDigraphs import *
from cIntegerOutrankingDigraphs import *
from cRandPerfTabs import cRandom3ObjectivesPerformanceTableau as cR3ObjPT
from randomPerfTabs import Random3ObjectivesPerformanceTableau as R3ObjPT
from outrankingDigraphs import BipolarOutrankingDigraph
from time import time

def testcIntegerOutrankingDigraph():
    tc = cR3ObjPT(seed=1)
    print(tc)
    gi = IntegerBipolarOutrankingDigraph(tc,Threading=True,nbrCores=4)
    print(gi)
    gi.showRelationTable()
    tcstd = tc.convert2Standard()
    g = BipolarOutrankingDigraph(tcstd)
    print(g)
    g.showRelationTable()

def testBigDataConversion():
    t = R3ObjPT(numberOfActions=50,seed=1)
    print(t)
    g = BipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    print(g)
    g.showRelationTable()
    tbd = t.convert2BigData()
    gi = IntegerBipolarOutrankingDigraph(tbd)
    print(gi)
    gi.showRelationTable()
    
    
        
        

   
