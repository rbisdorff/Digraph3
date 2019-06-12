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
    print('==>> Testing IntegerBipolarOutrankingDigraph instantiation')
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
    print('==>> Testing 2 Big Data conversion')
    t = R3ObjPT(numberOfActions=10,seed=1)
    print(t)
    g = BipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    print(g)
    g.showRelationTable()
    tbd = t.convert2BigData()
    gi = IntegerBipolarOutrankingDigraph(tbd)
    print(gi)
    gi.showRelationTable()

def testStandardConversion():
    print('==>> Testing 2 Standard conversion')
    t = cR3ObjPT(numberOfActions=10,seed=1)
    print(t)
    gi = IntegerBipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    print(gi)
    gi.showRelationTable()
    tstd = t.convert2Standard()
    g = BipolarOutrankingDigraph(tstd)
    print(g)
    g.showRelationTable()
    
def testSaveCPerformanceTableau():
    print('==>> Testing CPerformanceTableau saving and loading')
    t = cR3ObjPT(numberOfActions=5,seed=1)
    print(t)
    t.showPerformanceTableau()
    t.save('voir')
    g = IntegerBipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    g.showRelationTable()
    t1 = cPerformanceTableau('voir')
    print(t)
    t1.showPerformanceTableau()
    g1 = IntegerBipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    g1.showRelationTable()
    
        

   
