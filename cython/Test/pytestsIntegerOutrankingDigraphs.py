#######################
# R. Bisdorff 
# bigOutrankingdigraphs.py module tests for nose
#
# (..$ pip3 install pytest  # installing the pytest environment)
# ..$ pytest -vs pyTestsIntegerOutrankingDigraph.py
# # Current $Revision: 1.8 $
########################
# if __name__ == '__main__':
#     from sys import platform
#     if platform == 'darwin':
#         print('start_method set to fork')
#         from multiprocessing import set_start_method, get_start_method, freeze_support
#         set_start_method('fork')
#         print(get_start_method())
#         freeze_support()

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
    gi = IntegerBipolarOutrankingDigraph(tc,Threading=True,
                                         startMethod='spawn',nbrCores=4)
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
    gi = IntegerBipolarOutrankingDigraph(tbd,Threading=True,startMethod='forkserver')
    print(gi)
    gi.showRelationTable()

def testStandardConversion():
    print('==>> Testing 2 Standard conversion')
    t = cR3ObjPT(numberOfActions=10,seed=1)
    print(t)
    gi = IntegerBipolarOutrankingDigraph(t,Threading=True,startMethod='fork',nbrCores=4)
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
    g = IntegerBipolarOutrankingDigraph(t,Threading=True,startMethod='spawn',nbrCores=4)
    print(g)
    g.showRelationTable()
    t1 = cPerformanceTableau('voir')
    print(t)
    t1.showPerformanceTableau()
    g1 = IntegerBipolarOutrankingDigraph(t,Threading=True,nbrCores=4)
    print(g1)
    g1.showRelationTable()

def testCopelandOrdering():
    print('==>> Testing Copeland order computation')
    t = cR3ObjPT(numberOfActions=10,seed=1)
    print(t)
    t.showPerformanceTableau()
    g = IntegerBipolarOutrankingDigraph(t,Threading=True,startMethod=None,nbrCores=4)
    print(g)
    print(g.computeCopelandRanking())
    print(g.computeCopelandOrder())
    g.showRelationMap()

    
        

   
