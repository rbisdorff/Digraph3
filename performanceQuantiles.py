#!/usr/bin/env python3
"""
Digraph3 collection of python3 modules for 
Algorithmic Decision Theory applications

Module for incremental performance quantiles computation

Copyright (C) 2016-2010 Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
from time import time
from decimal import Decimal
from perfTabs import PerformanceTableau

class PerformanceQuantiles(PerformanceTableau):
    """
    Implements the incremental performance quantiles representation of a
    given performance tableau.

    *Parameters*:

        * *perfTab*: may be either a PerformanceTableau object or the name of a previously saved PerformanceQuantiles instance
        * *NumberOfBins* may be either 'quartiles', 'deciles', ... or 'n', the integer number of bins.

    Example python session:
        >>> import performanceQuantiles
        >>> from randomPerfTabs import RandomCBPerformanceTableau
        >>> from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator
        >>> nbrActions=1000
        >>> nbrCrit = 7
        >>> tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,
        ...                                numberOfCriteria=nbrCrit,seed=105)
        >>> pq = performanceQuantiles.PerformanceQuantiles(tp,'quintiles',
        ...                                LowerClosed=True,Debug=False)
        >>> pq.showLimitingQuantiles(ByObjectives=True)
        *----  performance quantiles -----*
        Costs
        criteria  | weights |  '0.0'   '0.25'  '0.5'   '0.75'  '1.0'   
         ---------|--------------------------------------------------
            'c1'  |   6     | -97.12  -65.70  -46.08  -24.96   -1.85  
        Benefits
        criteria  | weights |  '0.0'   '0.25'  '0.5'   '0.75'  '1.0'   
         ---------|--------------------------------------------------
            'b1'  |   1     |   2.11   32.42   53.25   73.44   98.69 
            'b2'  |   1     |   0.00    3.00    5.00    7.00   10.00  
            'b3'  |   1     |   1.08   34.64   54.80   73.24   97.23  
            'b4'  |   1     |   0.00    3.00    5.00    7.00   10.00  
            'b5'  |   1     |   1.84   34.25   55.11   74.62   96.40  
            'b6'  |   1     |   0.00    3.00    5.00    7.00   10.00  
        >>> tpg = PerfTabGenerator(tp,seed=105)
        >>> newActions = tpg.randomActions(100)
        >>> pq.updateQuantiles(newActions,historySize=None)      
        >>> pq.showHTMLLimitingQuantiles(Transposed=True)

    .. image:: examplePerfQuantiles.png
        :alt: Example limiting quantiles html show method
        :width: 400 px
        :align: center

    """
    def __repr__(self):
        """
        Default presentation method for PerformanceQuantiles instances
        """
        reprString = '*------- PerformanceQuantiles instance description ------*\n'
        reprString += 'Instance class   : %s\n' % self.__class__.__name__
        try:
            reprString += 'Seed             : %s\n' % str(self.randomSeed)
        except:
            pass
        reprString += 'Instance name    : %s\n' % self.name
        #reprString += '# Actions        : %d\n' % len(self.actions)
        try:
            reprString += '# Objectives     : %d\n' % len(self.objectives)
        except:
            pass       
        reprString += '# Criteria       : %d\n' % len(self.criteria)
        reprString += '# Quantiles      : %d\n' % (len(self.quantilesFrequencies)-1)
        reprString += '# History sizes  : %s\n' % self.historySizes
   
        reprString += 'Attributes       : %s\n' % list(self.__dict__.keys())     
        return reprString

    
    def __init__(self,perfTab=None,numberOfBins=4,LowerClosed=True,Debug=False):
        from copy import deepcopy
        from collections import OrderedDict, defaultdict
        from randomPerfTabs import RandomCBPerformanceTableau,\
                                   Random3ObjectivesPerformanceTableau,\
                                   RandomPerformanceTableau
        
        if type(perfTab) != str:
            self.perfTabType = perfTab.__class__.__name__
            try:
                self.valueDigits = perfTab.valueDigits
            except:
                self.valueDigits = 2
            actionsTypeStatistics = {}
            for x in perfTab.actions:
                if type(perfTab) == RandomCBPerformanceTableau:
                    xType = perfTab.actions[x]['type']
                elif type(perfTab) == Random3ObjectivesPerformanceTableau:
                    self.objectiveSupportingTypes = perfTab.objectiveSupportingTypes
                    xType = 'Soc' + perfTab.actions[x]['profile']['Soc']
                    xType += 'Eco' + perfTab.actions[x]['profile']['Eco']
                    xType += 'Env' + perfTab.actions[x]['profile']['Env']
                else:
                    xType = 'NA'
                try:
                    actionsTypeStatistics[xType] += 1
                except:
                    actionsTypeStatistics[xType] = 1
            self.actionsTypeStatistics = actionsTypeStatistics
            try:
                self.objectives = perfTab.objectives
            except:
                self.objectives = None
            try:
                self.commonScale = perfTab.commonScale
            except:
                pass
            try:
                self.OrdinalScales = perfTab.OrdinalScales
            except:
                pass
            try:
                self.BigData = perfTab.BigData
            except:
                pass
            try:
                self.missingDataProbability = perfTab.missingDataProbability
            except:
                pass
            self.criteria = deepcopy(perfTab.criteria)
            self.LowerClosed = LowerClosed
            self.quantilesFrequencies = self._computeQuantilesFrequencies(numberOfBins,Debug=Debug)
            np = len(self.quantilesFrequencies)
            limitingQuantiles = {}
            cdf = {}
            self.historySizes = {}
            for g in self.criteria:
                self.historySizes[g] = 0
                limitingQuantiles[g] = self._computeLimitingQuantiles(perfTab,g)
                if Debug:
                    print(g,limitingQuantiles[g])
                cdf[g] = OrderedDict([(limitingQuantiles[g][i],self.quantilesFrequencies[i]) for i in range(np)])
            self.limitingQuantiles = limitingQuantiles
            self.cdf = cdf
##            if perfTab.__class__.__name__ == 'RandomPerformanceTableau':
##                from randomPerfTabs import RandomPerformanceGenerator
##                self.randomActionsGenerator = RandomPerformanceGenerator(perfTab)
##            elif perfTab.__class__.__name__ == 'RandomCBPerformanceTableau':
##                from randomPerfTabs import RandomCBPerformanceGenerator
##                self.randomActionsGenerator = RandomCBPerformanceGenerator(perfTab)
##            elif perfTab.__class__.__name__ == 'Random3ObjectivesPerformanceTableau':
##                from randomPerfTabs import Random3ObjectivesPerformanceGenerator
##                self.randomActionsGenerator = Random3ObjectivesPerformanceGenerator(perfTab)
##            else:
##                print('!!! Warning: the proposed performance tableau model does not provide a random decision actions generator !!!')
##                self.randomActionsGenerator = None
        elif type(perfTab) == str: # a stored instance file name is given
            print(perfTab)
            fileName = perfTab + '.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(perfTab)
            try:
                self.objectives = argDict['objectives']
            except:
                pass
            try:
                self.objectiveSupportingTypes = argDict['objectiveSupportingTypes']
            except:
                pass
            try:
                self.commonScale = argDict['commonScale']
            except:
                pass
            try:
                self.OrdinalScales = argDict['OrdinalScales']
            except:
                pass
            try:
                self.BigData = argDict['BigData']
            except:
                pass
            try:
                self.missingDataProbability = argDict['missingDataProbability']
            except:
                pass
            self.criteria = argDict['criteria']
            self.quantilesFrequencies = argDict['quantilesFrequencies']
            self.historySizes = argDict['historySizes']
            self.LowerClosed = argDict['LowerClosed']
            self.limitingQuantiles = argDict['limitingQuantiles']
            cdf = {}
            np = len(self.quantilesFrequencies)
            for g in self.criteria:
                cdf[g] = {}
                for i in range(np):
                    cdf[g][self.limitingQuantiles[g][i]] = self.quantilesFrequencies[i]
                #cdf[g] = OrderedDict([(self.limitingQuantiles[g][i],self.quantilesFrequencies[i]) for i in range(np)])
            self.cdf = cdf
            self.perfTabType = argDict['perfTabType']
            print(self.perfTabType)
##            if self.perfTabType == 'RandomPerformanceTableau':
##                from randomPerfTabs import RandomPerformanceGenerator
##                self.randomActionsGenerator = RandomPerformanceGenerator
##            elif self.perfTabType == 'RandomCBPerformanceTableau':
##                from randomPerfTabs import RandomCBPerformanceGenerator
##                self.randomActionsGenerator = RandomCBPerformanceGenerator
##            elif self.perfTabType == 'Random3ObjectivesPerformanceTableau':
##                from randomPerfTabs import Random3ObjectivesPerformanceGenerator
##                self.randomActionsGenerator = Random3ObjectivesPerformanceGenerator
##            else:
##                print('!!! Warning: the proposed performance tableau model does not provide a random decision actions generator !!!')
##                self.randomActionsGenerator = None
          
#---------  private class methods

    def _computeQuantilesFrequencies(self,x,Debug=False):
        """
        renders the quantiles frequencies
        """
        from math import floor
        if isinstance(x,int):
            n = x
        elif x == 'quartiles':
            n = 4
        elif x == 'quintiles':
            n = 5
        elif x == 'sextiles':
            n = 6
        elif x == 'heptiles':
            n = 7
        elif x == 'octiles':
            n = 8
        elif x == 'deciles':
            n = 10
        elif x == 'dodeciles':
            n = 20
        elif x == 'centiles':
            n = 100
        else:
            print("""Error: numberOfBins must be either an integer, None or
a string out of ['quartiles','quintiles','sextiles','heptiles
'octiles','deciles','dodeciles','centiles']""")
            return
        quantilesFrequencies = []
        for i in range(n+1):
            freqStr = '%.6f' % (Decimal(str(i)) / Decimal(str(n)))
            quantilesFrequencies.append(Decimal(freqStr))
        self.name = '%d-tiled_performances' % n
        if Debug:
            print(x,quantilesFrequencies)
        return quantilesFrequencies

    def _computeLimitingQuantiles(self,perfTab,g,Debug=False):
        """
        Renders the list of limiting quantiles *q(p)* on criteria *g* for *p* in *frequencies* 
        """
        from math import floor
        from copy import copy, deepcopy
        critg = self.criteria[g]
        gValues = []
        for x in perfTab.actions:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,perfTab.evaluation[g][x])
            if perfTab.evaluation[g][x] != Decimal('-999'):
                if critg['weight'] > Decimal('0'):
                    gValues.append(perfTab.evaluation[g][x])
                else:
                    gValues.append(-perfTab.evaluation[g][x])
        gValues.sort()
        if critg['weight'] > Decimal('0'):
            self.criteria[g]['minValue'] = gValues[0]
            self.criteria[g]['maxValue'] = gValues[-1]
        else:
            self.criteria[g]['minValue'] = -gValues[0]
            self.criteria[g]['maxValue'] = -gValues[-1]

##        if PrefThresholds:
##            try:
##                gPrefThrCst = self.criteria[g]['thresholds']['pref'][0]
##                gPrefThrSlope = self.criteria[g]['thresholds']['pref'][1]
##            except:
##                gPrefThrCst = Decimal('0')
##                gPrefThrSlope = Decimal('0')            
        n = len(gValues)
        self.historySizes[g] = n
        if Debug:
            print('g,n,gValues',g,n,gValues)
##        if n > 0:
##        nf = Decimal(str(n+1))
        nf = Decimal(str(n))
        quantilesFrequencies = self.quantilesFrequencies
        #limitingQuantiles = [Decimal(str(q)) for q in frequencies]
        #limitingQuantiles.sort()
        #self.limitingQuantiles = limitingQuantiles
        if Debug:
            print(quantilesFrequencies)
        # computing the quantiles on criterion g
        gQuantiles = []
        if self.LowerClosed:
            # we ignore the 1.00 quantile and replace it with +infty
            for q in quantilesFrequencies:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
##                    if rq > 0 and PrefThresholds:
##                        quantile += gPrefThrCst + quantile*gPrefThrSlope
                else :
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        #quantile = Decimal('100.0')
                        quantile = gValues[-1]
                    else:
                        #quantile = Decimal('200.0')
                        quantile = gValues[-1] 
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)               

        else:  # upper closed categories
            # we ignore the quantile 0.0 and replace it with -\infty            
            for q in quantilesFrequencies:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq == 0:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        #quantile = Decimal('-200.0')
                        quantile = gValues[0] 
                    else:
                        #quantile = Decimal('-100.0')
                        quantile = gValues[0] 
                elif rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
##                    if PrefThresholds:
##                        quantile -= gPrefThrCst - quantile*gPrefThrSlope
                else:
                    if n > 0:
                        quantile = gValues[n-1]
                    else:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            quantile = gValues[-1]
                        else:
                            quantile = gValues[-1]     
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)
##        else:
##            gQuantiles = []
        #if critg['weight'] < Decimal('0'):
        #    gQuantiles = [-quantile for quantile in gQuantiles]
        if Debug:
            print(g,self.LowerClosed,self.criteria[g]['preferenceDirection'],gQuantiles)
        return gQuantiles

    def _htmlLimitingQuantiles(self,Sorted=False,\
                             Transposed=False,ndigits=2,\
                             ContentCentered=True,
                             title=None):
        """
        Renders the limiting quantiles in table format:  citerion x limitss in html format.
        """
        criteria = self.criteria
        if title == None:
            html = '<h1>Performance quantiles</h1>'
        else:
            html = '<h1>%s</h1>' % title
        historySizes = [self.historySizes[g] for g in self.historySizes]
        html += '<p>Sampling sizes between %d and %d.</p>' % ( min(historySizes),max(historySizes))
##        if self.LowerClosed:
##            html += '<p>Quantile bins %s.</p>' % ('lowerclosed')
##        else:
##            html += '<p>Quantile bins %s.</p>' % ('upperclosed')
           
        criteriaKeys = [g for g in self.criteria]
        if Sorted:
            criteriaKeys.sort()
        limitingQuantiles = self.limitingQuantiles
        quantilesFrequencies = self.quantilesFrequencies
        nq = len(quantilesFrequencies)
        if ContentCentered:
            alignFormat = 'center'
        else:
            alignFormat = 'right'
        if Transposed:
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>criterion</th>'
            for x in quantilesFrequencies:
                xName = '%.2f' % x
                html += '<th bgcolor="#FFF79B">%s</th>' % (xName)
            html += '</tr>'
            for g in criteriaKeys:
                try:
                    gName = criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (gName)
                for i in range(nq):
                    formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                    if criteria[g]['preferenceDirection'] == 'max':
                        value = min(criteria[g]['scale'][1],max(criteria[g]['scale'][0],limitingQuantiles[g][i]))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            value = max(-criteria[g]['scale'][1],min(-criteria[g]['scale'][0],limitingQuantiles[g][i]))
                        else:
                            value = max(criteria[g]['scale'][0],min(criteria[g]['scale'][1],-limitingQuantiles[g][i]))
                    html += formatString % (value)
                html += '</tr>'
            html += '</table>'
        else:
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>criterion</th>'
            for g in criteriaKeys:
                try:
                    gName = criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<th bgcolor="#FFF79B">%s</th>' % (gName)
            html += '</tr>'
            for i in range(nq):
                xName = '%.2f' % quantilesFrequencies[i]
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (xName)
                for g in criteriaKeys:
                    formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                    if criteria[g]['preferenceDirection'] == 'max':
                        value = min(criteria[g]['scale'][1],max(criteria[g]['scale'][0],limitingQuantiles[g][i]))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            value = max(-criteria[g]['scale'][1],min(-criteria[g]['scale'][0],limitingQuantiles[g][i]))
                        else:
                            value = max(criteria[g]['scale'][0],min(criteria[g]['scale'][1],-limitingQuantiles[g][i]))
                    html += formatString % (value)
                html += '</tr>'
            html += '</table>'        
        return html

    def _interpolateQuantile(self,x,newq,newp,Debug=False):
        #Debug = self.Debug
        #Debug = True
        if Debug:
            print('==>>?')
            print('x')
            print(x)
            print('newq')
            print(newq)
            print('newp')
            print(newp)
        np = len(newp)
        i = 0
        while i < np-1: 
            if Debug:
                print(i)
            if x < newp[i]:
                ix = i+1
                if Debug:
                    print('x < newp[i]', x, newp[i],ix, newp[i-1],newq[ix-1],newp[i],newq[ix])
                            # nsq[0] 
                diffp = newp[i]-newp[i-1]
                if diffp > Decimal('0.0'):
                    res = newq[ix-1]+ ((x-newp[i-1])/diffp)*(newq[ix]-newq[ix-1])
                else: # avoid dividing by 0
                    res = newq[ix-1]
                if Debug:
                    print('res', res)
                return res
                #i = np
            
            elif x == newp[i+1]:
                ix = i+1
                res = newq[ix]
                if Debug:
                    print('x == newp[i]',ix, newp[ix],newq[ix],res)
                return res
                
            else: # x > newp[i]
                ix = i+1
                i += 1
                if Debug:
                    print('x > newp[i]', i,ix)
        # if x is in the last quantile class
        if i == np-1:
            if x < newp[i]:
                ix = i
                if Debug:
                    print('x < newp[i]', x, newp[i],ix, newp[i-1],newq[ix-1],newp[i],newq[ix])
                            # nsq[0] 
                diffp = newp[i]-newp[i-1]
                if diffp > Decimal('0.0'):
                    res = newq[ix-1]+ ((x-newp[i-1])/diffp)*(newq[ix]-newq[ix-1])
                else: # avoid dividing by 0
                    res = newq[ix-1]
                if Debug:
                    print('res', res)
                return res
                i = np
            else:    # x == newp[i]:
                ix = i
                res = newq[ix]
                if Debug:
                    print('x == newp[i]',ix, newp[ix],newq[ix],res)
                return res
            

    def _updateCriterionQuantiles(self,g,newValues,historySize=None,Debug=False):
        """
        See lecture about the iq-agent of the MICS-3 Computational Statistics Course.
        """
        #Debug = self.Debug
        #Debug = True
        if Debug:
            print('==>>', g,newValues)
        from collections import OrderedDict
        # get present state of the quantiles
        p = self.quantilesFrequencies
        np = len(p)
        q = self.limitingQuantiles[g]
        cdf = self.cdf[g]
        if historySize == None:
            t = self.historySizes[g]
        else:
            t = historySize
        oldfrq = [p[i]*(t+1) for i in range(np)]
        if Debug:
            print(q)
            print(p)
            print(cdf)
            print(oldfrq)
            print(t)
        # new observations
        nv = []
        for x in newValues:
            if x != -999:
##                if self.criteria[g]['weight'] < Decimal('0'):
##                    nv.append(-x)
##                else:
                nv.append(x)
        nv.sort()
        nt = len(nv)
        if Debug:
            print('nv,nt', nv,nt)
        ###
        if nt > 0: # there may be solely missing values observed on g
            # Init results newq and newp
            # Init indexes: i in q & p & oldfrq, j in nv, ins = # insertions
            newp = [Decimal('0.0')]
            if nv[0] < q[0]:
                self.criteria[g]['minValue'] = nv[0]
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
            if nv[-1] > q[-1]:
                self.criteria[g]['maxValue'] = nv[-1]

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
            if Debug:
                self.newp = newp
                self.newq = newq
                print(newp)
                print(newq)
                    
            # renormalising frequencies
            if Debug:
                print('#inserts = %d' % ins)
            t += len(nv)
            for i in range(len(newq)):
                newp[i] /= newp[-1]
            if Debug:
                print('p \t q \ (t+1)*q')
                for i in range(len(newq)):
                    print('%.3f \t %.2f \t %.2f' % (newp[i],newq[i],newp[i]*(t)) )
                print('t = %d' % t)

            # compute new state by interpolation
            nstate = {p[0]:newq[0]}
            if Debug:
                print('==>> ',p)
            np = len(p)
            for i in range(1,np):
                x = p[i]
                if Debug:
                    print(x)
                nstate[x] = self._interpolateQuantile(x,newq,newp,Debug=Debug)
            if Debug:
                print(nstate)
            
            # store new state
            q = [nstate[x] for x in nstate]
            q.sort()
            self.limitingQuantiles[g] = q
            cdf = {}
            for p in nstate:
                cdf[nstate[p]] = p
            self.cdf[g] = cdf
            self.historySizes[g] = t

#------------- public class methods
    def computeQuantileProfile(self,p,qFreq=None,Debug=False):
        """
        Renders the quantile *q(p)* on all the criteria.
        """
        from collections import OrderedDict
        from decimal import Decimal
        
        x = Decimal('%.2f' % p)
        if qFreq == None:
            qFreq = self.quantilesFrequencies
        quantiles = OrderedDict()
        for g in self.criteria:
            q = self.limitingQuantiles[g]
            quantiles[g] = self._interpolateQuantile(x,q,qFreq)
            if Debug:
                print(x, quantiles[g], q)
        return quantiles

    def save(self,fileName='tempPerfQuant',valueDigits=2):
        """
        Persistant storage of a PerformanceQuantiles instance.
        """
        print('*--- Saving performance quantiles in file: <' + str(fileName) + '.py> ---*')
        valueString = 'Decimal("%%.%df"),\n' % (valueDigits)
        objectives = self.objectives
        fileNameExt = str(fileName)+str('.py')
        with open(fileNameExt, 'w') as fo:
            fo.write('# Saved performance quantiles: \n')
            fo.write('from decimal import Decimal\n')
            fo.write('from collections import OrderedDict\n')
            # perfTabType
            fo.write('perfTabType = \'%s\'\n' % self.perfTabType)
            # objectives
            try:
                fo.write('objectiveSupportingTypes = %s\n' % str(self.objectiveSupportingTypes) )
            except:
                pass
            fo.write('objectives = OrderedDict([\n')
            if objectives != None:
                for obj in objectives:
                    fo.write('(\'%s\', {\n' % str(obj))
                    for it in self.objectives[obj].keys():
                        fo.write('\'%s\': %s,\n' % (it,repr(self.objectives[obj][it])))
                    fo.write('}),\n')
            fo.write('])\n')            
            # criteria
            try:
                fo.write('OrdinalScales = %s\n' % str(self.OrdinalScales))
            except:
                pass
            try:
                fo.write('BigData = %s\n' % str(self.BigData))
            except:
                pass
            try:
                fo.write('missingDataProbability = %s\n' % str(self.missingDataProbability))
            except:
                pass
            try:
                fo.write('commonScale = %s\n' % str(self.commonScale))
            except:
                pass
            criteria = self.criteria
            fo.write('criteria = OrderedDict([\n') 
            for g in criteria:
                fo.write('(\'%s\', {\n' % str(g))
                for it in self.criteria[g].keys():
                    fo.write('\'%s\': %s,\n' % (it,repr(self.criteria[g][it])))
                fo.write('}),\n')
            fo.write('])\n')
            # quanties frequencies
            quantilesFrequencies = self.quantilesFrequencies
            np = len(quantilesFrequencies)
            fo.write('quantilesFrequencies = [\n')
            for i in range(np):
                fo.write(valueString % quantilesFrequencies[i] )
            fo.write( ']\n')
            # history sizes
            historySizes = self.historySizes
            fo.write('historySizes = {\n')
            for g in criteria:
                fo.write('\'%s\': %d,' % (g,historySizes[g]) )
            fo.write( '}\n')
            # quantile limits
            fo.write('LowerClosed = %s\n' % repr(self.LowerClosed))
            limitingQuantiles = self.limitingQuantiles
            fo.write('limitingQuantiles = {\n')
            for g in criteria:
                fo.write('\'%s\': [\n' % g )
                for i in range(np):
                    fo.write(valueString % limitingQuantiles[g][i] )
                fo.write('],\n')
            fo.write( '}\n')       

        # fo.close() automatic
        
    def showActions(self):
        print("""No decision actions are actually being stored!
Only the cumulated density function per criteria of so far
observed performance evaluations are kept.
The number of so far observed evaluations per criteria are the following:
        """ )
        for g in self.criteria:
            print(g,self.historySizes[g])

    def showCriteria(self,IntegerWeights=False,Alphabetic=False,ByObjectives=True,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
##        if self.Debug:
##            Debug = True
            
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
                                  (th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1]))
                            #print self.criteria[g]['thresholds'][th]
                            #print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                    except:
                        pass
                    #print(self.limitingQuantiles[g])
                    print('  history size: %d' % self.historySizes[g])
                    print('  p    : quantile(p)')
                    if self.LowerClosed:
                        nq = len(self.quantilesFrequencies)
                        for i in range(nq):
                            q = self.quantilesFrequencies[i]
                            #print(q,self.limitingQuantiles[g])
                            if i < (nq-1):
                                print('%.2f :  %.2f' % (q,self.limitingQuantiles[g][i]) )
                            else:
                                print('%.2f :  %.2f' % (q,self.criteria[g]['maxValue'])   )                 
                    else:  # upperclosed quantile bins
                        nq = len(self.quantilesFrequencies)
                        for i in range(nq):
                            q = self.quantilesFrequencies[i]
                            #print(q,self.limitingQuantiles[g])
                            if i > 0:
                                print('%.2f : %.2f' % (q,self.limitingQuantiles[g][i]) )
                            else:
                                print('%.2f : %.2f' % (q,self.criteria[g]['minValue'])   )                 
                       
##                        for i in range(len(self.quantilesFrequencies)):
##                            q = self.quantilesFrequencies[i]
##                            if i > 0:
##                                print('%.2f : %.2f' % (q,self.limitingQuantiles[g][i]) )
##                            else:
##                                print('%.2f : %.2f' % (q,self.criteria[g]['minValue']) )
                                
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
                              % (th,criteria[g]['thresholds'][th][0],criteria[g]['thresholds'][th][1]))
                        #print self.criteria[g]['thresholds'][th]
                        #print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                except:
                    pass
                #print(self.limitingQuantiles[g])
                print('  history size: %d' % self.historySizes[g])
                print('  p    :  qantile(p')
                if self.LowerClosed:
                    nq = len(self.quantilesFrequencies)
                    for i in range(nq):
                        q = self.quantilesFrequencies[i]
                        #print(q,self.limitingQuantiles[g])
                        if i < (nq-1):
                            print('%.2f :  %.2f' % (q,self.limitingQuantiles[g][i]) )
                        else:
                            print('%.2f :  %.2f' % (q,self.criteria[g]['maxValue'])   )                 
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

    def showHTMLLimitingQuantiles(self,Sorted=True,\
                                   Transposed=False,ndigits=2,\
                                   ContentCentered=True,title=None):
        """
        shows the html version of the limiting quantiles in a browser window.
        """
        import webbrowser
        fileName = '/tmp/performanceTable.html'
        fo = open(fileName,'w')
        fo.write(self._htmlLimitingQuantiles(Sorted=Sorted,\
                                           Transposed=Transposed,\
                                           ndigits=ndigits,
                                           ContentCentered=ContentCentered,
                                           title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
           
            


    def showLimitingQuantiles(self,ByObjectives=False,Sorted=False,ndigits=2):
        """
        Prints the performance quantile limits in table format: criteria x limits.
        """
        criteria = self.criteria
        print('*----  performance quantiles -----*')
        quantiles = self.quantilesFrequencies
        nq = len(quantiles)
        limitingQuantiles = self.limitingQuantiles
        if ByObjectives:
            objectives = self.objectives
            for obj in objectives:
                print(objectives[obj]['name'])
                criteriaList = [g for g in criteria if criteria[g]['objective']==obj]
                if Sorted:
                    criteriaList.sort()
                print('criteria | weights |', end=' ')
                for x in quantiles:
                    print('\''+str(x)+'\'  ', end=' ')
                print('\n---------|-----------------------------------------')
                for g in criteriaList:
                    print('   \''+str(g)+'\'  |   '+str(criteria[g]['weight'])+'   | ', end=' ')
                    for i in range(nq):
                        formatString = '%% .%df ' % ndigits
                        if criteria[g]['preferenceDirection'] == 'max':
                            value = min(criteria[g]['scale'][1],max(criteria[g]['scale'][0],limitingQuantiles[g][i]))
                        else:
                            if criteria[g]['weight'] > Decimal('0'):
                                value = max(-criteria[g]['scale'][1],min(-criteria[g]['scale'][0],limitingQuantiles[g][i]))
                            else:
                                value = max(criteria[g]['scale'][0],min(criteria[g]['scale'][1],limitingQuantiles[g][i]))
                        print(formatString % (value), end=' ')
                    print()      
        else: 
            criteriaList = list(self.criteria)
            if sorted:
                criteriaList.sort()
            print('criteria | weights |', end=' ')
            for x in quantiles:
                print('\''+str(x)+'\'  ', end=' ')
            print('\n---------|-----------------------------------------')
            for g in criteriaList:
                print('   \''+str(g)+'\'  |   '+str(self.criteria[g]['weight'])+'   | ', end=' ')
                for i in range(nq):
                    formatString = '%% .%df ' % ndigits
                    if criteria[g]['preferenceDirection'] == 'max':
                        value = min(criteria[g]['scale'][1],max(criteria[g]['scale'][0],limitingQuantiles[g][i]))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            value = max(-criteria[g]['scale'][1],min(-criteria[g]['scale'][0],limitingQuantiles[g][i]))
                        else:
                            value = max(criteria[g]['scale'][0],min(criteria[g]['scale'][1],-limitingQuantiles[g][i]))
                    print(formatString % (value), end=' ')
                print()      

    def showCriterionStatistics(self,g,Debug=False):
        """
        show statistics concerning the evaluation distributions
        on each criteria.
        """
        import math
        criteria = self.criteria
        qFreq = self.quantilesFrequencies
        nc = len(qFreq)
        frequencies = ['%.2f' % p for p in qFreq]
        glimitingQuantiles = self.limitingQuantiles[g]
        #actions = self.actions
        #n = len(actions)
        print('*-------- Performance Quantiles statistics -------*')
        print('Instance name         :', self.name)
        print('Quantiles frequencies :', frequencies)
        print('Summary for criterion : %s' % g)
        print('  Criterion name      : %s' % criteria[g]['name'])
        print('  Comment             : %s' % self.criteria[g]['comment'])
        if criteria[g]['preferenceDirection'] == 'max':
            print('  Performance range   : [%.2f-%.2f]'\
              % (self.criteria[g]['scale'][0],self.criteria[g]['scale'][1]) )
        else:
            print('  Performance range   : [%.2f;%.2f]'\
              % (-self.criteria[g]['scale'][1],-self.criteria[g]['scale'][0]) )
        print('  Quantiles repartition :')
        print('    p%\t q(p)')  
        for i in range(nc):
            print('   %.0f\t %.2f' % (qFreq[i]*100, glimitingQuantiles[i]))               
##                print('  mean evaluation       : %.2f' % (averageEvaluation))
##                print('  standard deviation    : %.2f' % (stdDevEvaluation))
##                print('  maximal evaluation    : %.2f' % (maxEvaluation))
##                print('  quantile Q3 (x_75)    : %.2f' % (quantileQ3))
##                print('  median evaluation     : %.2f' % (quantileQ2))
##                print('  quantile Q1 (x_25)    : %.2f' % (quantileQ1))
##                print('  minimal evaluation    : %.2f' % (minEvaluation))

        
    def updateQuantiles(self,newData,historySize=None,Debug=False):
        """
        Update the PerformanceQuantiles with a set of new random decision actions.
        Parameter *historysize* allows to take more or less into account the historical situtaion.
        For instance, *historySize=0* does not take into account at all any past observations.
        Otherwise, if *historySize=None* (the default setting), the new observations become less and less
        influential compared to the historical data.
       """
##        if t != None:
##            self.historySizes = t
        try:
            newActions = newData['actions']
            newEvaluation = newData['evaluation']
        except:
            newActions = newData.actions
            newEvaluation = newData.evaluation
            
        for g in self.criteria:
            gNewValues = []
            gNewEvaluation = newEvaluation[g]
            for x in newActions:
                gNewValues.append(gNewEvaluation[x])
            self._updateCriterionQuantiles(g,gNewValues,historySize=historySize,Debug=Debug)
##        self.T += len(newActions)  
    




#####################################################################
#######################################################################
#----------test classes and methods ----------------
if __name__ == "__main__":

    from performanceQuantiles import *
    seed = 100
    nbrActions = 20
    nbrCrit = 13
##    from randomPerfTabs import RandomPerformanceTableau
##    from randomPerfTabs import RandomPerformanceGenerator as PerfTabGenerator
##    nbrActions=nbrActions
##    nbrCrit = nbrCrit
##    tp = RandomPerformanceTableau(numberOfActions=nbrActions,
##                                    numberOfCriteria=nbrCrit,seed=seed)
##    from randomPerfTabs import RandomCBPerformanceTableau
##    from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator
##    nbrActions=nbrActions
##    nbrCrit = nbrCrit
##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,
##                                    numberOfCriteria=nbrCrit,seed=seed)
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    from randomPerfTabs import RandomPerformanceGenerator as PerfTabGenerator
    nbrActions=nbrActions
    nbrCrit = nbrCrit
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,
                                             NegativeWeights=False,
                                             negativeWeightProbability=0.1,
                                    numberOfCriteria=nbrCrit,seed=seed)
    pq = PerformanceQuantiles(tp,5,LowerClosed=True,Debug=False)
    #print(pq.actionsTypeStatistics)
    #pq.showHTMLLimitingQuantiles(Transposed=True)
    #print(pq.limitingQuantiles)
    pq.showLimitingQuantiles(ByObjectives=False)
    #pq.showHTMLLimitingQuantiles(Transposed=True)
    #pq.showActions()
    #pq.showCriteria(ByObjectives=True)
    tpg = PerfTabGenerator(tp,seed=None)
    newActions = tpg.randomActions(10)
    pq.updateQuantiles(newActions,historySize=0)
    #pq.showHTMLLimitingQuantiles(Transposed=True)
    #tpg = PerfTabGenerator(tp,seed=None)
    newActions = tpg.randomActions(10)
    pq.updateQuantiles(newActions,historySize=0)
    #pq.showHTMLLimitingQuantiles(Transposed=True)
    pq.save('test')
    pq1 = PerformanceQuantiles('test')
    from randomPerfTabs import *
    rg = RandomPerformanceGenerator(pq1)
    newTab = rg.randomPerformanceTableau(10)
##    from sortingDigraphs import NormedQuantilesRatingDigraph
##    nqr1 = NormedQuantilesRatingDigraph(pq,newActions,\
##                                        rankingRule='best',\
##                                        Debug=False)
##    print(nqr1)
##    nqr1.showHTMLRatingHeatmap(pageTitle='Heat map of the qintiles rating',
##                                       colorLevels=7,
##                                       Correlations=True,
##                                       )
##    nqr1.showQuantilesRating()
##    nqr1.exportRatingGraphViz(Comments=False)
    #print(pq.computeQuantileProfile(0.5))
    #pq.save(fileName='testPerfQuant')

    #pq1 = PerformanceQuantiles(filePerfQuant='testPerfQuant')
    
