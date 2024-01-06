#!/usr/bin/env python3
"""
Digraph3 collection of python3 modules for Algorithmic Decision Theory applications.

New Python3.12+ compatible multiprocessing implementation of bipolar-valued outranking digraphs for Linux and MacOS. The potentially unsafe default *fork* multiprocessing start-method may be either set to 'spawn' (default) or to 'forkserver'. Shared pool given performance tableau must be first saved in the current working directory in a file named 'sharedPerfTab'.

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
from time import time

from sharedPerfTab import *

def worker_func(actionKey):
    # computing the genuine bipolar-valued outranking situations
    # with considerable performance differences counts between
    # the given *actionKey* performance record and the complete set of
    # performance records
    # in: actionKey, out: relation, considerableDiffs

    # init the varia o be returned
    relation = {}
    considerableDiffs = {}
    x = actionKey
    relation[x] = {}
    considerableDiffs[x] = {}
    for y in actions:
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
            for y in actions:
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
                    # # for debugging
                    # print(g,criteria[g]['weight'],x,y,xval,yval,(xval-yval),relation[x][y])
                    
    # polarising the case given the outranking situation
    for y in actions:
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

    return [relation, considerableDiffs]

#-----------------
from outrankingDigraphs import BipolarOutrankingDigraph
class MPBipolarOutrankingDigraph(BipolarOutrankingDigraph):
    """
    New variable start-method based MP implementation of the BipolarOutrankingDigraph class.

    *Parameters*:
        * *Normalized*: the valuation domain is set by default to the sum of the criteria weights. If *True*, the valuation domain is recoded to [-1.0,+1.0].
        * *ndigits*: number of decimal digits of the characteristic valuation, by default set to 4.
        * *nbrCores*: controls the maximal number of cores that will be used in the multiprocessing phases. If *None* is given, the *os.cpu_count()* method is used in order to determine the number of available cores on the SMP machine.
        * *startMethod*: 'spawn' (default) | 'forkserver' | 'fork'
        * The given *PerformanceTableau* object is shared with the multiprocessing threads via importing a *sharedPerfTab.py* module stored in the current working directory and containing a saved *PerformanceTableau* object.

.. note:: The given *PerformanceTableau* must be previously saved in the working directory under the name 'sharedPerfTab'.
    
    *Usage example*

    (11th Gen Intel® Core™ i5-11400 × 12, 16.0 GiB memory, Ubuntu 23.10, Python3.12.0):

    >>> from randomPerfTabs import RandomCBPerformanceTableau
    >>> pt1 = RandomCBPerformanceTableau(
    ...         numberOfActions=1000,numberOfCriteria=13,
    ...         seed=10)
    >>> pt1.save('sharedPerfTab')
    >>> import os
    >>> while not os.path.exists('./sharedPerfTab.py'):
    ...     pass
    >>> from mpOutrankingDigraphs import MPBipolarOutrankingDigraph
    >>> bg = MPBipolarOutrankingDigraph(Normalized=True,ndigits=2,
    ...                                 nbrCores=8,startMeth='spawn')
    >>> bg
     *------- Object instance description ------*
     Instance class       : MPBipolarOutrankingDigraph
     Instance name        : rel_sharedPerfTab
     Actions              : 1000
     Criteria             : 13
     Size                 : 517128
     Determinateness (%)  : 66.83
     Valuation domain     : [-1.00;1.00]
     Attributes           : ['name', 'actions', 'order', 'criteria',
                     'objectives', 'NA', 'evaluation', 'nbrThreads',
                     'relation', 'largePerformanceDifferencesCount',
                     'valuationdomain', 'gamma', 'notGamma',
                     'runTimes', 'startMeth']
     ----  Constructor run times (in sec.) ----
     Threads            : 8
     Start method       : 'spawn'
     Total time         : 4.06436
     Data input         : 0.00000
     Compute relation   : 2.79447
     Normalize relation : 0.72327
     Gamma sets         : 0.54659
    

.. warning:: When using the *forkserver* or the *spawn* multiprocessing start-methods in a python script file, mind that both start-methods re-import into every multiprocessing thread the submitted program file. In order to avoid hence the program script from being recursively executed and producing loads of zombie threads before being killed by the OS, it is compulsory necessary to always explicitely protect the entry point of the main program code with the *if __name__ == '__main__':* condition. This is not necessary when using instead the classical Unix *fork* start-method where multiprocessing threads continue in fact the main program code from the point on where they were launched. 

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
        try:
            reprString += 'Threads            : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            reprString += 'Threads            : %d\n' % self.nbrThreads
        try:
            reprString += "Start method       : \'%s\'\n" % self.startMeth
        except:
            pass
        reprString += 'Total time         : %.5f\n' % val1
        reprString += 'Data input         : %.5f\n' % val2
        reprString += 'Compute relation   : %.5f\n' % val3
        try:
            val3n = self.runTimes['normalizeRelation']
            reprString += 'Normalize relation : %.5f\n' % val3n
        except:
             pass
        reprString += 'Gamma sets         : %.5f\n' % val4
        return reprString

    def __init__(self,WithGammaSets=True,
                 Normalized=False,ndigits=4,
                 startMeth='spawn',nbrCores=None):
        from decimal import Decimal
        from time import time
        runTimes = {}
        t0 = time()
        import sharedPerfTab as perfTab
        self.name = 'rel_sharedPerfTab'
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

        # compute relation
        t1 = time()
        ctx_in_main = multiprocessing.get_context(startMeth)
        self.startMeth = '%s' % ctx_in_main.get_start_method()
        relation = {}
        considerableDiffs = {}
        for x in actions:
            relation[x] = {}
            considerableDiffs[x] = {}
        if nbrCores is None:
            cores = ctx_in_main.cpu_count()
        else:
            cores = nbrCores
        self.nbrThreads = cores
        tasks = [x for x in actions]
        with ctx_in_main.Pool(processes=cores) as pool:
            #print(tasks)
            for result in pool.imap(worker_func, tasks):
                #print(result[0])
                relation.update(result[0])
                considerableDiffs.update(result[1])
        runTimes['computeRelation'] = time() - t1
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
        t2 = time()
        if WithGammaSets:
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        runTimes['gammaSets'] = time() - t2
        runTimes['totalTime'] = time() - t0
        self.runTimes = runTimes

    def showPolarisations(self):       
        """
        Prints out all negative and positive polarised outranking situations observed in the *MPBipolarOutrankingDigraph* instance.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        lpdCount = self.largePerformanceDifferencesCount
        relation = self.relation
        try:
            vetos = self.vetos
        except:
            vetos = []
        print('*----  Polarisations ----*')
        actionKeys = [a for a in self.actions]
        n = len(actionKeys)
        print('Considerable positive and negative performance differences')
        print('Outranking situationa polarised to indeterminate')
        print(' -----------------------------------------------')
        count = 0
        for i in range(n):
            x = actionKeys[i]
            for j in range(i+1,n):
                y = actionKeys[j]
                if lpdCount[x][y]['positive'] > 0 and \
                   lpdCount[x][y]['negative'] < 0:
                    count += 1
                    print( 'relation[%s][%s] = %.2f' % (x,y,relation[x][y]),
                           end= '; ' )
                    print( 'relation[%s][%s] = %.2f' % (y,x,relation[y][x]) )
        print('%d polarisations\n' % count)
        print('Considerable positive performance differences')
        print('Outranking situationa polarised')
        print('*----------------------------------------------------*')
        count = 0
        for i in range(n):
            x = actionKeys[i]
            for j in range(i+1,n):
                y = actionKeys[j]
                if lpdCount[x][y]['positive'] > 0 and \
                   lpdCount[x][y]['negative'] == 0:
                    count += 1
                    print( 'relation[%s][%s] = %.2f' % (x,y,relation[x][y]),
                           end= '; ' )
                    print( 'relation[%s][%s] = %.2f' % (y,x,relation[y][x]) )
        print('%d polarisations\n' % count)
        print('Considerable negative performance differences')
        print('Outranking situations polarised')
        print('*----------------------------------------------------*')
        count = 0
        for i in range(n):
            x = actionKeys[i]
            for j in range(i+1,n):
                y = actionKeys[j]
                if lpdCount[x][y]['positive'] == 0 and \
                   lpdCount[x][y]['negative'] < 0:
                    count += 1
                    print( 'relation[%s][%s] = %.2f' % (x,y,relation[x][y]),
                           end='; ' )
                    print( 'relation[%s][%s] = %.2f' % (y,x,relation[y][x]) )
        print('%d polarisations\n' % count)
        
#-----------------

###################################
# testing the module

if __name__ == '__main__':
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    pt = Random3ObjectivesPerformanceTableau(
                              numberOfActions=500,seed=2)
    pt.save('sharedPerfTab')
    print(pt)
    import os
    while not os.path.exists('./sharedPerfTab.py'):
        pass
    bg = MPBipolarOutrankingDigraph(Normalized=True,
                                    startMeth='forkserver',
                                    nbrCores=6)
    print(bg)
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
        
    print('*************************************')
    print('* R.B.                              *')
    print('* $Revision: Python3.12 $           *')                   
    print('*************************************')
