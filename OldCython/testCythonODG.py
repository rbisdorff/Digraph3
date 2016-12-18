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
#import cBigOutrankingDigraphsDev as Bg
#import cBigOutrankingDigraphsDev as cBg
from cOutrankingDigraphsDev import *
#from bigOutrankingDigraphs import *
from time import time
from os import path
from randomPerfTabs import Random3ObjectivesPerformanceTableau

# parameters
sampleSize = 100
MP = True
nbrOfCPUs = 6
nbrActions = 500
nbrCriteria = 21
commonPar=('beta','variable',None)
qtiles = 50
minimalSize = 10
seed = 55
fileName = 'CythonA%dObj21q%ds%dc%dgaia164.csv' % (nbrActions,qtiles,minimalSize,nbrOfCPUs)
# write header row
if path.isfile(fileName):
	pass
else:
	fo = open(fileName,'w')
	fo.write('"tt","tti","dt","dti","rl","rli","gs","gsi","sd"\n')
	fo.close()

for s in range(sampleSize):
    seed += 1
    print('sample %d\n' % (s+1))
    # main starting
    tp1 = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                   Threading=MP,
                                    BigData=True,
#                                    nbrCores=nbrOfCPUs,
                                    seed=seed)
    print(tp1.name)
    #t0 = time()
    g1 = BipolarOutrankingDigraph(tp1,Threading=MP,nbrCores=nbrOfCPUs)

    print(g1)
    
    tp2 = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                        Threading=MP,
                                        BigData=True,
#                                        nbrCores=nbrOfCPUs,
                                        seed=seed)

    g2 = IntegerBipolarOutrankingDigraph(tp2,Threading=MP,nbrCores=nbrOfCPUs)

    print(g2)
    fo = open(fileName,'a')
    wstr = '%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d\n'\
             % (g1.runTimes['totalTime'],g2.runTimes['totalTime'],\
                g1.runTimes['dataInput'],g2.runTimes['dataInput'],\
                g1.runTimes['computeRelation'],g2.runTimes['computeRelation'],\
                g1.runTimes['gammaSets'],g2.runTimes['gammaSets'],seed)
    fo.write(wstr)
    fo.close()
    print(wstr)
# .....
print('results in file = %s' % fileName)



    

