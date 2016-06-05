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
import cBigOutrankingDigraphs as Bg
import cBigOutrankingDigraphsDev as cBg
#from bigOutrankingDigraphs import *
from time import time
from os import path
from randomPerfTabs import Random3ObjectivesPerformanceTableau

# parameters
sampleSize = 100
MP = True
nbrOfCPUs = 6
nbrActions = 2000
nbrCriteria = 21
commonPar=('beta','variable',None)
qtiles = 50
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
    bg1 = Bg.BigOutrankingDigraph(tp1,quantiles=qtiles,
                               quantilesOrderingStrategy='average',
                               minimalComponentSize=minimalSize,
                               LowerClosed=False,
                               Threading=MP,
                               nbrOfCPUs=nbrOfCPUs,
                               CopyPerfTab=False,
                               Comments=True,
                               Debug=False)

    print(bg1)
    
    tp2 = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCriteria,
                                    weightDistribution='equiobjectives',
#                                    commonPercentiles={'ind':0.01,'pref':0.025,'veto':0.975},
                                        commonMode=commonPar,
#                                        Threading=MP,
                                        BigData=True,
#                                        nbrCores=nbrOfCPUs,
                                        seed=seed)

    bg2 = cBg.BigOutrankingDigraph(tp2,quantiles=qtiles,
                               quantilesOrderingStrategy='average',
                               minimalComponentSize=minimalSize,
                               LowerClosed=False,
                               Threading=MP,
                               CopyPerfTab=False,
                               nbrOfCPUs=nbrOfCPUs,
                               Comments=True,
                               Debug=False)

    print(bg2)
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



    

