#######################
# R. Bisdorff
# pytest functions for the transitiveDigraphs module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from digraphs import *
from dynamicProgramming import *
from time import time


def testDynamicMinProgramming():
    print('*====>>>> test dynamic programming solutions ----')
    print(' => preference direction set to min')
    dg = RandomDynamicProgrammingDigraph(order=12,
                                         maxStages=4,
                                         costsRange=(5,10),
                                         preferenceDirection='min',
                                         seed=2)
    print(dg.optimalPath)
    print(dg.bestSum)
    print(dg.preferenceDirection)
    dg.exportGraphViz('testDPmin')

def testSavingDynamicProgrammingDigraphs():
    print(' => test saving and reloading')
    dg = RandomDynamicProgrammingDigraph(order=12,
                                         maxStages=4,
                                         costsRange=(5,10),
                                         preferenceDirection='min',
                                         seed=2)
    dg.save()
    dg1 = DynamicProgrammingDigraph('tempDPdigraph')
    print(dg1.optimalPath)
    print(dg1.bestSum)
    print(dg1.preferenceDirection)

def testDynamicMaxProgramming():
    print('*====>>>> test dynamic programming solutions ----')
    print(' => preference direction set to min')
    
    print(' => preference direction set to max')
    dg2 = RandomDynamicProgrammingDigraph(order=12,
                                         maxStages=4,
                                         costsRange=(5,10),
                                         preferenceDirection='max',
                                         seed=2)
    print(dg2.optimalPath)
    print(dg2.bestSum)
    print(dg2.preferenceDirection)
    dg2.exportGraphViz('testDPmax')
    
