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
import cSparseIntegerOutrankingDigraphs as iBg
#from SparseOutrankingDigraphs import *
from time import time
from os import path
from cRandPerfTabs import *
from randomPerfTabs import Random3ObjectivesPerformanceTableau as R3ObjPT
from multiprocessing import set_start_method

# parameters
sampleSize = 1
MP = True
nbrOfCPUs = 8
nbrOfThreads = 8
nbrOfSubProcesses = 0
#set_start_method('fork')
#componentThreadingThreshold = 500
nbrActions = 50000
nbrCriteria = 21
#commonPar = ('beta','variable',None)
#commonPar = ('triangular','variable',0.5)
#commonPar = ('uniform','variable',None)
commonPar = None
qtiles = 5
minimalSize = 1
seed = 15
resFileName = 'CythonA%dObj21q%dms%dsd%dcpu%dhome.txt' % (nbrActions,qtiles,minimalSize,seed,nbrOfCPUs) 
# write header row
##if path.isfile(resFileName):
##	pass
##else:
##	fo = open(fileName,'w')
##	fo.write('"tti","pri","dci","si","sd"\n')
##	fo.close()

for s in range(sampleSize):
    seed += 1
    print('sample %d\n' % (s+1))
    # main starting
##    t0 = time()
##    tp1 = R3ObjPT(numberOfActions=nbrActions,
##                                    numberOfCriteria=nbrCriteria,
##                                    weightDistribution='equiobjectives',
###                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
##                                        commonMode=commonPar,
###                                   Threading=MP,
##                                    BigData=True,
###                                    nbrCores=nbrOfCPUs,
##                                    seed=seed)
##    print(tp1.name)
##    print(time()-t0)
##    #t0 = time()
##    bg1 = Bg.SparseOutrankingDigraph(tp1,quantiles=qtiles,
##                               quantilesOrderingStrategy='average',
##                               minimalComponentSize=minimalSize,
##                               LowerClosed=False,
##                               Threading=MP,
##                               nbrOfCPUs=nbrOfCPUs,
##                               nbrOfThreads=nbrOfThreads,
##                               CopyPerfTab=False,
##                               Comments=True,
##                               Debug=False)
##
##    print(bg1)
    t0 = time()
    tp2 = cRandom3ObjectivesPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                        Threading=MP,
                                        #BigData=True,
#                                        nbrCores=nbrOfCPUs,
                                        seed=seed)
    print(tp2)
    print(time()-t0)
#    bg2 = iBg.SparseIntegerOutrankingDigraph(tp2,quantiles=qtiles,
    bg2 = iBg.cQuantilesRankingDigraph(tp2,quantiles=qtiles,
                               quantilesOrderingStrategy='average',
                               minimalComponentSize=minimalSize,
                               LowerClosed=False,
                               componentRankingRule='NetFlows',
                               Threading=MP,
                               #CopyPerfTab=False,
                               nbrOfCPUs=nbrOfCPUs,
                               #nbrOfThreads=nbrOfCPUs,
                               #nbrOfSubProcesses=nbrOfSubProcesses,
                               #componentThreadingThreshold=componentThreadingThreshold,
                               Comments=True,
                               Debug=False)

    print(bg2)
    print(bg2.boostedRanking[:10])
    #bg2.showActions()
    #bg2.showCriteria()
    #bg2.showDecomposition()
    #g2.showComponents()
    #bg2.showRelationTable()
    
    #tp2.convertBigData2Standard()
    #tp2.showHTMLPerformanceHeatmap(actionsList=bg2.boostedRanking,rankingRule='NetFlows',Correlations=True)
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
    
    
##    fo = open(fileName,'a')
##    wstr = '%.4f,%.4f,%.4f,%.4f,%d\n'\
##             % (bg2.runTimes['totalTime'],\
##                bg2.runTimes['preordering'],\
##                bg2.runTimes['decomposing'],\
##                bg2.runTimes['sorting'],seed)
##    fo.write(wstr)
##    fo.close()
    #print(wstr)
    print(bg2)
    fo = open(resFileName,'a')
    fo.write('################\n')
    fo.write(str(tp2))
    fo.write(str(bg2))
    fo.close()
# .....
print('results in file <%s>.' % (resFileName))



    

