#!/usr/bin/env python3
"""
Digraph3 collection of python3 modules for Algorithmic Decision Theory applications

Module for incremental outranking digraphs

Copyright (C) 2016  Raymond Bisdorff

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from outrankingDigraphs import *
from sortingDigraphs import *
from time import time
from decimal import Decimal
from sparseOutrankingDigraphs import *


class PerformanceQuantiles(object):
    """
    Gathers the incremental performance quantiles representation of a
    given performance tableau.

    Example python session:
    >>> import performanceQuantiles
    >>> from randomPerfTabs import RandomCBPerformanceTableau, 
    >>> from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator
    >>> frequencies = [0.0,0.25,0.5,0.75,1.0]
    >>> nbrActions=1000
    >>> nbrCrit = 7
    >>> tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCrit,seed=105)
    >>> pq = PerformanceQuantiles(tp,frequencies,LowerClosed=True,Debug=False)
    >>> pq.showActions()
    >>> pq.showCriteria()
    >>> tpg = PerfTabGenerator(tp,seed=105)
    >>> newActions = []
    >>> for i in range(100):
    >>>     newAction = tpg.randomAction()
    >>>     newActions.append(newAction)
    >>>     pq.updateQuantiles(newActions,t=None)
    >>> pq.showActions()
    >>> pq.showCriteria()
    """
    
    def __init__(self,perfTab,frequencies,LowerClosed=True,Debug=False):
        from copy import deepcopy
        from collections import OrderedDict
        self.Debug = Debug
        self.T = len(perfTab.actions)
        try:
            self.objectives = perfTab.objectives
        except:
            self.objectives = None
        self.criteria = deepcopy(perfTab.criteria)
        self.LowerClosed = LowerClosed
        self.quantilesFrequencies = [Decimal(str(q)) for q in sorted(frequencies)]
        np = len(self.quantilesFrequencies)
        limitingQuantiles = {}
        cdf = {}
        for g in self.criteria:
            limitingQuantiles[g] = self._computeLimitingQuantiles(perfTab,g,
                                                                     frequencies,
                                                                     LowerClosed=LowerClosed)
            if self.Debug:
                print(g,limitingQuantiles[g])
            cdf[g] = OrderedDict([(limitingQuantiles[g][i],self.quantilesFrequencies[i]) for i in range(np)]) 
        self.limitingQuantiles = limitingQuantiles
        self.cdf = cdf
        

    def _computeLimitingQuantiles(self,perfTab,g,frequencies,LowerClosed=True,Debug=False,PrefThresholds=True):
        """
        Renders the list of limiting quantiles *q(p)* on criteria *g* for *p* in *frequencies* 
        """
        from math import floor
        from copy import copy, deepcopy
        if self.Debug:
            Debug = True
        gValues = []
        for x in perfTab.actions:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,perfTab.evaluation[g][x])
            if perfTab.evaluation[g][x] != Decimal('-999'):
                gValues.append(perfTab.evaluation[g][x])
        gValues.sort()
        self.criteria[g]['minValue'] = gValues[0]
        self.criteria[g]['maxValue'] = gValues[-1]
        if PrefThresholds:
            try:
                gPrefThrCst = self.criteria[g]['thresholds']['pref'][0]
                gPrefThrSlope = self.criteria[g]['thresholds']['pref'][1]
            except:
                gPrefThrCst = Decimal('0')
                gPrefThrSlope = Decimal('0')            
        n = len(gValues)
        if Debug:
            print('g,n,gValues',g,n,gValues)
##        if n > 0:
##        nf = Decimal(str(n+1))
        nf = Decimal(str(n))
        limitingQuantiles = [Decimal(str(q)) for q in frequencies]
        limitingQuantiles.sort()
        #self.limitingQuantiles = limitingQuantiles
        if Debug:
            print(limitingQuantiles)
##        if LowerClosed:
##            limitingQuantiles = limitingQuantiles[:-1]
##        else:
##            limitingQuantiles = limitingQuantiles[1:]
        if Debug:
            print(limitingQuantiles)
        # computing the quantiles on criterion g
        gQuantiles = []
        if LowerClosed:
            # we ignore the 1.00 quantile and replace it with +infty
            for q in limitingQuantiles:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
                    if rq > 0 and PrefThresholds:
                        quantile += gPrefThrCst + quantile*gPrefThrSlope
                else :
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        #quantile = Decimal('100.0')
                        quantile = gValues[-1]
                    else:
                        #quantile = Decimal('200.0')
                        quantile = gValues[-1] * 2
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)               

        else:  # upper closed categories
            # we ignore the quantile 0.0 and replace it with -\infty            
            for q in limitingQuantiles:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq == 0:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        #quantile = Decimal('-200.0')
                        quantile = gValues[0] - (gValues[-1] * 2)
                    else:
                        #quantile = Decimal('-100.0')
                        quantile = gValues[0] - gValues[-1]
                elif rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
                    if PrefThresholds:
                        quantile -= gPrefThrCst - quantile*gPrefThrSlope
                else:
                    if n > 0:
                        quantile = gValues[n-1]
                    else:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            quantile = Decimal('-200.0')
                        else:
                            quantile = Decimal('-100.0')     
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)
##        else:
##            gQuantiles = []
        if Debug:
            print(g,LowerClosed,self.criteria[g]['preferenceDirection'],gQuantiles)
        return gQuantiles


    def _interpolateQuantile(self,x,newq,newp):
        if self.Debug:
            print(x,newq,newp)
        np = len(newp)
        i = 0
        while i < np:
            if x < newp[i]:
                ix = i
                if self.Debug:
                    print(ix, newp[ix-1],newq[ix-1],newp[ix],newq[ix])
                            # nsq[0] 
                diffq = newp[ix]-newp[ix-1]
                if diffq > 0.0:
                    return newq[ix-1]+ (x-newp[ix-1])/diffq*(newq[ix]-newq[ix-1])
                else: # avoid dividing by 0
                    return newq[ix-1]
                i = np
            elif x == newp[i]:
                ix = i
                if self.Debug:
                    print(ix, newp[ix],newq[ix])
                return newq[ix]
            else: # x > newp[i]
                ix = i
                i += 1       

##    def showCriteriaQuantiles(self):
        
    def showActions(self):
        print("""No decision actions are actually being stored!
Only the cumulated density function per criteria of so far
observed performance evaluations are kept.
The number of so far observed evaluations is %d.
        """ % self.T)

    def showCriteria(self,IntegerWeights=False,Alphabetic=False,ByObjectives=False,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
        if self.Debug:
            Debug = True
            
        criteria = self.criteria
        try:
            objectives = self.objectives
        except:
            ByObjectives = False
        print('*----  criteria -----*')
##        sumWeights = Decimal('0.0')
##        for g in criteria:
##            sumWeights += criteria[g]['weight']
        sumWeights = sum([criteria[g]['weight'] for g in criteria])
        if ByObjectives:
            for obj in objectives.keys():
                criteriaList = [g for g in criteria if criteria[g]['objective']==obj]
                for g in criteriaList:
                    try:
                        criterionName = '%s/' % objectives[criteria[g]['objective']]['name']                                        
                    except:
                        criterionName = ''
                    try:
                        criterionName += criteria[g]['name']
                    except:
                        pass
                    print(g, repr(criterionName))
                    
                    print('  Scale =', criteria[g]['scale'])
                    if IntegerWeights:
                        print('  Weight = %d ' % (criteria[g]['weight']))
                    else:
                        weightg = criteria[g]['weight']/sumWeights
                        print('  Weight = %.3f ' % (weightg))
                    try:
                        for th in criteria[g]['thresholds']:
                            if Debug:
                                print('-->>>', th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1])
                            print('  Threshold %s : %.2f + %.2fx' %\
                                  (th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1]), end=' ')
                            #print self.criteria[g]['thresholds'][th]
                            #print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                    except:
                        pass
                    #print(self.limitingQuantiles[g])
                    
                    for i in range(len(self.quantilesFrequencies)):
                        q = self.quantilesFrequencies[i]
                        if i > 0:
                            print('%.2f : %.2f' % (q,self.limitingQuantiles[g][i]) )
                        else:
                            print('%.2f : %.2f' % (q,self.criteria[g]['minValue']) )
                            
                    print()
        else:
            criteriaList = list(self.criteria.keys())
            if Alphabetic:
                criteriaList.sort()
            for g in criteriaList:
                try:
                    criterionName = '%s/' % objectives[criteria[g]['objective']]['name']                                        
                except:
                    criterionName = ''
                try:
                    criterionName += criteria[g]['name']
                except:
                    pass
                print(g, repr(criterionName))
                
                print('  Scale =', criteria[g]['scale'])
                if IntegerWeights:
                    print('  Weight = %d ' % (criteria[g]['weight']))
                else:
                    weightg = criteria[g]['weight']/sumWeights
                    print('  Weight = %.3f ' % (weightg))
                try:
                    for th in criteria[g]['thresholds']:
                        if Debug:
                            print('-->>>', th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1])
                        print('  Threshold %s : %.2f + %.2fx'\
                              % (th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1]), end=' ')
                        #print self.criteria[g]['thresholds'][th]
                        #print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                except:
                    pass
                #print(self.limitingQuantiles[g])
                print('  p    : q(p')
                if self.LowerClosed:
                    nq = len(self.quantilesFrequencies)
                    for i in range(nq):
                        q = self.quantilesFrequencies[i]
                        #print(q,self.limitingQuantiles[g])
                        if i < (nq-1):
                            print('%.2f : %.2f' % (q,self.limitingQuantiles[g][i]) )
                        else:
                            print('%.2f : %.2f' % (q,self.criteria[g]['maxValue'])   )                 
                else:  # upperclosed quantile bins
                    nq = len(self.quantilesFrequencies)
                    for i in range(nq):
                        q = self.quantilesFrequencies[i]
                        #print(q,self.limitingQuantiles[g])
                        if i > 0:
                            print('%.2f : %.2f' % (q,self.limitingQuantiles[g][i]) )
                        else:
                            print('%.2f : %.2f' % (q,self.criteria[g]['minValue'])   )                 
                print()

    def _updateCriterionQuantiles(self,g,newValues):
##        newValues.sort()
##        print(g,newValues)
        #self.Debug = True
        from collections import OrderedDict
        # get present state of the quantiles
        #s = self.state
        p = self.quantilesFrequencies
        np = len(p)
        q = self.limitingQuantiles[g]
        cdf = self.cdf[g]
        t = self.T
        oldfrq = [p[i]*(t+1) for i in range(np)]
        if self.Debug:
            print(q)
            print(p)
            print(cdf)
            print(oldfrq)
            print(t)
        # new observations
        nv = sorted(newValues)
        nt = len(nv)
        if self.Debug:
            print(nv,nt)

        # Init results newq and newp
        # Init indexes: i in q & p & oldfrq, j in nv, ins = # insertions
        newp = [Decimal('0.0')]
        if nv[0] < q[0]:
            newq= [nv[0]]
            ins = 1
            j = 1
            i = 0
        elif nv[0] > q[0] :
            newq = [q[0]]
            j = 0
            ins = 0
            i = 1
        else:
            newq = [q[0]]
            j = 1
            ins = 0
            i = 1
     

        # compute new cumulative densities
        while i < np:
            while j < nt and i < np:
                #print(i,j)
                if nv[j] > q[i]:
                    newq.append(q[i])
                    # ins += 0
                    newp.append(cdf[q[i]]+ins)
                    i += 1                        
                elif nv[j] < q[i]:
                    if nv[j] > newq[-1]:
                        newq.append(nv[j])
                        # ins += 1
                        # interpolate cdf of nv[j]
                        cdfnv = cdf[q[i-1]] + (nv[j]-q[i-1])/(q[i]-q[i-1])*cdf[q[i]] + ins
                        newp.append(cdfnv)
                    else:
                        newp[-1] += 1
                    ins += 1
                    j +=1
                else: # nv[j] = q[i]
                    newp[-1] += 1
                    ins += 1
                    j += 1
            if j == nt:
                for ni in range(i,np):
                    newq.append(q[ni])
                    newp.append(cdf[q[ni]]+ins)
                    #ins += 0
                i = np
        for nj in range(j,nt):
            ins += 1
            if newq[-1] < nv[nj]:
                newq.append(nv[nj])
                newp.append(newp[-1]+1)
            else:
                newp[-1] += 1
        if self.Debug:
            self.newp = newp
            self.newq = newq
            print(newp)
            print(newq)
                    
        # renormalising frequencies
        if self.Debug:
            print('#inserts = %d' % ins)
        t += len(nv)
        for i in range(len(newq)):
            newp[i] /= newp[-1]
        if self.Debug:
            print('p \t q \ (t+1)*q')
            for i in range(len(newq)):
                print('%.3f \t %.2f \t %.2f' % (newp[i],newq[i],newp[i]*(t)) )
            print('t = %d' % t)

        # compute new state by interpolation
        ns = OrderedDict([(p[0],newq[0])])
        if self.Debug:
            print(p)
        np = len(p)
        for i in range(1,np):
            x = p[i]
            if self.Debug:
                print(x)
            ns[x] = self._interpolateQuantile(x,newq,newp)
        if self.Debug:
            print(ns)
        
        # store new state
        state = ns
        self.state = state
        q = [state[x] for x in state]
        q.sort()
        self.limitingQuantiles[g] = q
        for p in state:
            cdf[state[p]] = p
        self.cdf[g] = cdf

        
    def updateQuantiles(self,newActions,t=None):
        """
        Update the PerformanceQuantiles with a set of new random decision actions.
        Parameter *t* allows to take more or less into account the historical situtaion.
        For instance, *t=0* does not take into account at all any past observations.
        Otherwise, if *t=None* (the default setting), the new observations become less and less
        influential compared to the historical data.
       """
        if t != None:
            self.T = t
        for g in self.criteria:
            gNewValues = []
            for x in newActions:
                gNewValues.append(x['evaluation'][g])
            self._updateCriterionQuantiles(g,gNewValues)
        self.T += len(newActions)  
    




#####################################################################
#######################################################################
#----------test classes and methods ----------------
if __name__ == "__main__":

    import performanceQuantiles
    from randomPerfTabs import RandomCBPerformanceTableau, 
    from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator

    frequencies = [0.0,0.25,0.5,0.75,1.0]
    nbrActions=100
    nbrCrit = 7
    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,
                                    numberOfCriteria=nbrCrit,seed=105)
    pq = PerformanceQuantiles(tp,frequencies,LowerClosed=True,Debug=False)
    #print(pq.limitingQuantiles)
    pq.showActions()
    pq.showCriteria()
    tpg = PerfTabGenerator(tp,seed=105)
    newActions = []
    for i in range(100):
        newAction = tpg.randomAction()
        newActions.append(newAction)
    #print(newActions)
    pq.updateQuantiles(newActions,t=None)
    pq.showActions()
    pq.showCriteria()
    newActions = []
    for i in range(5):
        newAction = tpg.randomAction()
        newActions.append(newAction)
    #print(newActions)
    pq.updateQuantiles(newActions)
    pq.showActions()
    pq.showCriteria()

