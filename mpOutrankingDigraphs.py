#!/usr/bin/env python3
"""
New Python3.12+ compatible multiprocessing implementation of bipolarvalued outranking digraphs for Linux and MacOS.

The unsafe *fork* multiprocessing start-method is replaced with the safer *forkserver* method.

Shared pool data and given performance tableau are preloaded by the *forkserver*. 

Copyright (C) 2023  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""


__version__ = "Revision: Py3.12"


import multiprocessing
import os

# # init poolData.py module with  forkserver preload example variables
# if not os.path.exists('./poolData.py'):
#      Normalized = False
#      ndigits = 4
# else:
#     from poolData import *
if not os.path.exists('./sharedPerfTab.py'):
    from randomPerfTabs import RandomPerformanceTableau
    pt = RandomPerformanceTableau(numberOfActions=1,numberOfCriteria=1)
    pt.save('sharedPerfTab',Comments=False)
else:
    from sharedPerfTab import *

def worker_func(keys):
    from decimal import Decimal
    relation = {}
    considerableDiffs = {}
    ks = keys.split('_')
    i = ks[0]
    x = ks[1]
    actionKeys = [a for a in actions]
    relation[x] = {}
    considerableDiffs[x] = {}
    for y in actionKeys:
        relation[x].update({y : Decimal('0')})
        considerableDiffs[x].update({y: {'positive':0, 'negative': 0}})
    sumWeights = Decimal('0')
    for g in criteria:
        sumWeights += criteria[g]['weight']
        try:
            ind = criteria[g]['thresholds']['ind']
        except:
            ind = NA
        try:
            pref = criteria[g]['thresholds']['pref']
        except:
            pref = NA
        try:
            veto = criteria[g]['thresholds']['veto']
        except:
            veto = NA
        xval = evaluation[g][x]
        if xval != NA:
            for y in actionKeys:
                yval = evaluation[g][y]
                if yval != NA:
                    if ind != NA and pref != NA:
                        if (xval - yval) >= -(ind[0] + xval*ind[1]):
                            relation[x][y] += criteria[g]['weight']
                        elif (xval - yval) <= -(pref[0] + xval*pref[1]):
                            relation[x][y] -= criteria[g]['weight']
                    else:
                        if (xval - yval) >= Decimal('0'):
                            relation[x][y] += criteria[g]['weight']
                        elif (xval - yval) < Decimal('0'):
                            relation[x][y] -= criteria[g]['weight']
                    if veto != NA:
                        if (xval - yval) >= (veto[0] + max(xval*veto[1],yval*veto[1])):
                            considerableDiffs[x][y]['positive'] += 1
                        elif (xval - yval) <= -(veto[0] + max(xval*veto[1],yval*veto[1])):
                            considerableDiffs[x][y]['negative'] -= 1
                if considerableDiffs[x][y]['positive'] > 0 and considerableDiffs[x][y]['negative'] < 0:
                    relation[x][y] = Decimal('0')
                elif relation[x][y] > Decimal('0'):
                    if considerableDiffs[x][y]['positive'] > 0:
                        relation[x][y] = sumWeights
                    elif considerableDiffs[x][y]['negative'] < 0:
                        relation[x][y] = Decimal('0')
                elif relation[x][y] < Decimal('0'):
                    if considerableDiffs[x][y]['positive'] > 0:
                        relation[x][y] = Decimal('0')
                    elif considerableDiffs[x][y]['negative'] < 0:
                        relation[x][y] = -sumWeights
                elif relation[x][y] == Decimal('0'):
                    if considerableDiffs[x][y]['positive'] > 0:
                        relation[x][y] = sumWeights
                    elif considerableDiffs[x][y]['negative'] < 0:
                        relation[x][y] = -sumWeights
                # print(g,x,y,xval,yval,(xval-yval),relation[x][y])
                  


    return [relation, considerableDiffs]

from outrankingDigraphs import BipolarOutrankingDigraph
class MPOutrankingDigraph(BipolarOutrankingDigraph):
    """
    New *forkserver* start-method based MP implementation of the BipolarOutrankingDigraph class.

    *Parameters*:
        * perfTab: in memory instance of PerformanceTableau class.
        * Normalized: the valuation domain is set by default to the sum of the criteria weights. If True, the valuation domain is recoded to [-1.0,+1.0].
        * ndigits: number of decimal digits of the chracteristic valuation, by default set to 4.
        * nbrCores: controls the maximal number of cores that will be used in the multiprocessing phases. If None is given, the os.cpu_count method is used in order to determine the number of available cores on the SMP machine.
    
    *Usage example*
         (11th Gen Intel® Core™ i5-11400 × 12, 16.0 GiB, Python3.12.0):

    >>> from randomPerfTabs import *
    >>> pt1 = RandomCBPerformanceTableau(
    ...         numberOfActions=1000,numberOfCriteria=13,
    ...         seed=10)
    >>> from mpOutrankingDigraphs import MPOutrankingDigraph
    >>> bg = MPOutrankingDigraph(pt1,Normalized=False,nbrCores=12)
    >>> bg
     *--- Saving performance tableau in file: <sharedPerfTab.py> ---*
      saved actual poolData.py module
     *------- Object instance description ------*
      Instance class       : MPOutrankingDigraph
      Instance name        : rel_randomCBperftab
      Actions              : 1000
      Criteria             : 13
      Size                 : 550012
      Determinateness (%)  : 71.12
      Valuation domain     : [-60.00;60.00]
      Attributes           : ['name', 'actions', 'order',
                              'criteria', 'objectives',
                              'NA', 'evaluation', 'nbrThreads',
                              'relation', 'considerableDiffsCount',
                              'valuationdomain', 'gamma',
                              'notGamma', 'runTimes']
      ----  Constructor run times (in sec.) ----
      Total time       : 4.64133
      Data input       : 0.01220
      Compute relation : 3.95451
      Gamma sets       : 0.67462
      Threads          : 12
    
    """
    def __repr__(self):
        """
        Default presentation method for MPBipolarOutrankingDigraph instance.
        """
        reprString = '*------- Object instance description ------*\n'
        reprString += 'Instance class       : %s\n' % self.__class__.__name__
        reprString += 'Instance name        : %s\n' % self.name
        reprString += 'Actions              : %d\n' % self.order
        reprString += 'Criteria             : %d\n' % len(self.criteria)
        reprString += 'Size                 : %d\n' % self.computeSize()
        reprString += 'Determinateness (%%)  : %.2f\n' %\
                      self.computeDeterminateness(InPercents=True)
        reprString += 'Valuation domain     : [%.2f;%.2f]\n' \
            % (self.valuationdomain['min'],self.valuationdomain['max'])
        #reprString += 'Valuation domain : %s\n' % str(self.valuationdomain)
        reprString += 'Attributes           : %s\n' % list(self.__dict__.keys())
        #try:
        val1 = self.runTimes['totalTime']
        val2 = self.runTimes['dataInput']
        val3 = self.runTimes['computeRelation']
        val4 = self.runTimes['gammaSets']
        reprString += '----  Constructor run times (in sec.) ----\n'
        reprString += 'Total time         : %.5f\n' % val1
        reprString += 'Data input         : %.5f\n' % val2
        reprString += 'Compute relation   : %.5f\n' % val3
        try:
            val3n = self.runTimes['normalizeRelation']
            reprString += 'Normalize relation : %.5f\n' % val3n
        except:
             pass
        reprString += 'Gamma sets         : %.5f\n' % val4
        try:
            reprString += 'Threads            : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            reprString += 'Threads            : %d\n' % self.nbrThreads
        #except:
        #    pass
        return reprString

    def __init__(self,perfTab,Normalized=False,ndigits=4,nbrCores=None):
        from decimal import Decimal
        from time import time, sleep
        from perfTabs import PerformanceTableau
        runTimes = {}
        t0 = time()
        PerformanceTableau.save(perfTab,'sharedPerfTab')
        while not os.path.exists('./sharedPerfTab.py'):
            sleep(1)
        # # code snippet for alternate module importing    
        # inPT = __import__(argPerfTab)
        # print(inPT)
        # for att in dir(inPT):
            # print(att)
            # if att == 'actions':
            #     self.actions = actions
            #     #print(self.actions)
            #     self.order = len(self.actions)
            # elif att == 'criteria':
            #     self.criteria = criteria
            #     #print(self.criteria)
            # elif att == 'evaluation':
            #     self.evaluation = evaluation
            # elif att == 'NA':
            #     try:
            #         self.NA = NA
            #     except:
            #         self.NA = Decimal('-999')
            # elif att == 'objectives':
            #     self.objectives = objectives
        self.name = 'rel_' + perfTab.name
        self.actions = perfTab.actions
        self.order = len(self.actions)
        self.criteria = perfTab.criteria
        try:
            self.objectives = perfTab.objectives
        except:
            self.objectives = {}
        self.NA = perfTab.NA
        self.evaluation = perfTab.evaluation
        runTimes['dataInput'] = time() - t0
        t1 = time()
        # construct relation
        actionKeys = [x for x in self.actions]
        pargs = {}
        n = self.order
        # # sharing parameters with a prelodable poolData.py module
        # fo = open('./poolData.py','w')
        # fo.write( 'Normalized = %s\n' % str(Normalized) )
        # fo.write( 'ndigits = %d\n' % ndigits )
        # fo.close()
        # while not os.path.exists('./poolData.py'):
        #      sleep(1)
        # print('saved actual poolData.py module')
        ctx_mp = multiprocessing.get_context('forkserver')
        # ctx_mp.set_forkserver_preload(['poolData','sharedPerfTab'])
        ctx_mp.set_forkserver_preload(['sharedPerfTab'])
        if nbrCores is None:
            cores = ctx_mp.cpu_count()
        else:
            cores = nbrCores
        self.nbrThreads = cores
        with ctx_mp.Pool(processes=cores) as pool:
            relation = {}
            considerableDiffs = {}
            for x in self.actions:
                relation[x] = {}
                considerableDiffs[x] = {}
            tasks = []
            for i in range(n):
                keys = '%s_%s' % (str(i),str(actionKeys[i]))
                tasks.append(keys)
            #print(tasks)
            for result in pool.imap(worker_func, tasks):
                #print(result[0])
                relation.update(result[0])
                considerableDiffs.update(result[1])
        
        while multiprocessing.active_children() != []:
            pass
        self.relation = relation
        self.largePerformanceDifferencesCount = considerableDiffs
        # valuationdamain
        sumWeights = Decimal('0')
        for g in self.criteria:
            sumWeights += self.criteria[g]['weight']
        self.valuationdomain = {'min': Decimal(str(-sumWeights)),
                                'med': Decimal('0'),
                                'max': Decimal(str(sumWeights))}
        if Normalized:
            tn = time()
            self.recodeValuation(ndigits=ndigits)
            runTimes['normalizeRelation'] = time() - tn
        runTimes['computeRelation'] = time() - t1
        t2 = time()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['gammaSets'] = time() - t2
        runTimes['totalTime'] = time() - t0
        self.runTimes = runTimes
        #print(runTimes)
        
###################################
# testing the module
if __name__ == '__main__':
    from perfTabs import PerformanceTableau
    from randomPerfTabs import *
    from time import time,sleep
    pt1 = RandomCBPerformanceTableau(numberOfActions=300,
                                     numberOfCriteria=13,
                                     IntegerWeights=True,
                                     seed=10)
    #pt1.showCriteria()
    #pt1 = PerformanceTableau('sharedPerfTab')
    #pt1.showPerformanceTableau()
    from mpOutrankingDigraphs import MPOutrankingDigraph
    bg = MPOutrankingDigraph(pt1,ndigits=4,Normalized=False,nbrCores=12)
    #bg.showRelationTable(hasLPDDenotation=True)
    print(bg)
    #bg.showPairwiseOutrankings('a4','a7')
    #from outrankingDigraphs import BipolarOutrankingDigraph
    #bg1 = BipolarOutrankingDigraph(pt1,Threading=False)
    #bg1.showRelationTable(hasLPDDenotation=True)
    #print(bg1)
    #bg1.showPairwiseOutrankings('a1','a5')
    #bg.showRelationTable()
    #bg.recodeValuation()
    #from linearOrders import *
    #nf = NetFlowsRanking(bg)
    #print(nf)
    #bg.showHTMLPerformanceHeatmap(toIndex=20,Correlations=True,
    #                              colorLevels=5,outrankingModel='this')
    