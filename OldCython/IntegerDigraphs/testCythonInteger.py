#!/usr/bin/env python3
# Python 3 implementation of digraphs
# sub-module for big outranking digraphs
# Copyright (C) 2015  Raymond Bisdorff
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#######################
import outrankingDigraphs as ODG
import cBigOutrankingDigraphs as Bg
import cBigIntegerOutrankingDigraphs as iBg
#from bigOutrankingDigraphs import *
from time import time
from os import path
from cRandPerfTabs import Random3ObjectivesPerformanceTableau as cR3ObjPT
from randomPerfTabs import Random3ObjectivesPerformanceTableau as R3ObjPT
from multiprocessing import set_start_method

# parameters
sampleSize = 10
MP = True
nbrOfCPUs = 4
nbrOfThreads = 4
nbrOfSubProcesses = 2
#set_start_method('fork')
componentThreadingThreshold = 50
nbrActions = 2500
nbrCriteria = 21
commonPar=('beta','variable',None)
qtiles = 75
minimalSize = 10
seed = 10
fileName = 'CythonA%dObj21q%ds%dc%dhome.csv' % (nbrActions,qtiles,minimalSize,nbrOfCPUs)
# write header row
if path.isfile(fileName):
	pass
else:
	fo = open(fileName,'w')
	fo.write('"tt","tti","pr","pri","dc","dci","s","si","sd"\n')
	fo.close()

for s in range(sampleSize):
    seed += 1
    print('sample %d\n' % (s+1))
    # main starting
    t0 = time()
    tp1 = R3ObjPT(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                   Threading=MP,
                                    BigData=True,
#                                    nbrCores=nbrOfCPUs,
                                    seed=seed)
    print(tp1.name)
    print(time()-t0)
    #t0 = time()
    bg1 = Bg.BigOutrankingDigraph(tp1,quantiles=qtiles,
                               quantilesOrderingStrategy='average',
                               minimalComponentSize=minimalSize,
                               LowerClosed=False,
                               Threading=MP,
                               nbrOfCPUs=nbrOfCPUs,
                               nbrOfThreads=nbrOfThreads,
                               CopyPerfTab=False,
                               Comments=True,
                               Debug=False)

    print(bg1)
    t0 = time()
    tp2 = cR3ObjPT(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                        Threading=MP,
                                        #BigData=True,
#                                        nbrCores=nbrOfCPUs,
                                        seed=seed)
    print(tp2.name)
    print(time()-t0)
    bg2 = iBg.BigIntegerOutrankingDigraph(tp2,quantiles=qtiles,
                               quantilesOrderingStrategy='average',
                               minimalComponentSize=minimalSize,
                               LowerClosed=False,
                               Threading=MP,
                               CopyPerfTab=False,
                               nbrOfCPUs=nbrOfCPUs,
                               nbrOfThreads=nbrOfCPUs,
                               nbrOfSubProcesses=nbrOfSubProcesses,
                               componentThreadingThreshold=componentThreadingThreshold,
                               Comments=True,
                               Debug=False)

    print(bg2)
    ## bg2.showActions()
    ## bg2.showCriteria()
    ## bg2.showDecomposition()
    ## bg2.showRelationTable()
    ## print(bg2.computeBoostedRanking())
    ## bg2.showRelationMap(toIndex=80)
    #print(bg2.computeBoostedOrdering())
    #bg1.recodeValuation(-720,720)
    #print(bg1.valuationdomain)
    #g = ODG.BipolarIntegerOutrankingDigraph(tp2)
    #print(bg2.computeOrdinalCorrelation(g,Debug=True))
    
    
    fo = open(fileName,'a')
    wstr = '%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d\n'\
             % (bg1.runTimes['totalTime'],bg2.runTimes['totalTime'],\
                bg1.runTimes['preordering'],bg2.runTimes['preordering'],\
                bg1.runTimes['decomposing'],bg2.runTimes['decomposing'],\
                bg1.runTimes['sorting'],bg2.runTimes['sorting'],seed)
    fo.write(wstr)
    fo.close()
    print(wstr)
# .....
print('results in file = %s' % fileName)



    

