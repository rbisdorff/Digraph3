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
from cRandPerfTabs import Random3ObjectivesPerformanceTableau as cR3ObjPT
#from randomPerfTabs import Random3ObjectivesPerformanceTableau as R3ObjPT
#from outrankingDigraphs import BipolarOutrankingDigraph
from time import time

def testcIntegerOutrankingDigraph():
    t = cR3ObjPT(seed=1)
    gi = IntegerBipolarOutrankingDigraph(t)
    gi.showShort()
    print(gi)
    gi.showRelationTable()

def testconvert2DecimalValuation():
    t = cR3ObjPT(numberOfActions=13,numberOfCriteria=7,seed=2)
    g = IntegerBipolarOutrankingDigraph(t)
    print(g)
    g.convertValuation2Decimal()
    print(g)
    print(g.valuationdomain)
    g.recodeValuation(-1,1)
    print(g.valuationdomain)
    g.showRelationMap()
    t.showPerformanceTableau()
    g.convertEvaluationFloatToDecimal()
    t.showHTMLPerformanceTableau()
    
    
    
        
        

   
