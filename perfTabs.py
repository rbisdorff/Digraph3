#!/usr/bin/env python3
"""
Python implementation of digraphs
Module for working with performance tableaux  
Copyright (C) 2011-2019  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: 1.37 $"
# $Source: /home/cvsroot/Digraph/perfTabs.py,v $

from perfTabs import *
import json
import decimal
from digraphsTools import *
from decimal import Decimal
from collections import OrderedDict
from ast import literal_eval

# ----------  old XML handling ------------------
try:
    from xml.sax import *
except:
    print('XML extension will not work with this Python version!')

########################################################################################################################
#######                                                MCSRDecimalEncoder                                         ######
#######                                                         START                                             ######
########################################################################################################################
##
###extension of the json encoder to encode decimals added by Ian
##class _DecimalJSONEncoder(json.JSONEncoder):
##
##    def default(self,obj):
##
##        if isinstance(obj,decimal.Decimal):
##            #cast into float so that the native encoder can handle the rest
##            #since the result is a string only the string representation is used,
##            # which is still identical to the decimal value
##            return float(obj)
##        else:
##            return obj.__dict__
##        return json.JSONEncoder.default(self, obj)
##
########################################################################################################################
#######                                                MCSRDecimalEncoder                                         ######
#######                                                         END                                               ######
########################################################################################################################




class PerformanceTableau(object):
    """
In this *Digraph3* module, the root :py:class:`perfTabs.PerformanceTableau` class provides a generic **performance table model**. A given object of this class consists in:

     1. a set of potential decision **actions** : an ordered dictionary describing the potential decision actions or alternatives with 'name' and 'comment' attributes,
     2. an optional set of decision **objectives**: an ordered dictionary with name, comment, weight and list of concerned criteria per objective,
     3. a coherent family of **criteria**: a ordered dictionary of criteria functions used for measuring the performance of each potential decision action with respect to the preference dimension captured by each criterion,
     4. the **evaluations**: a dictionary of performance evaluations for each decision action or alternative on each criterion function.

Structure::

       actions = OrderedDict([('a1', {'name': ..., 'comment': ...}),
                  ('a2', {'name': ..., 'comment': ...}),
                  ...])
       objectives = OrderedDict([
                   ('obj1', {'name': ..., 'comment': ..., 'weight': ..., 'criteria': ['g1', ...]}),
                   ('obj2', {'name': ..., 'comment', ..., 'weight': ..., 'criteria': ['g2', ...]}),
                   ...])
       criteria = OrderedDict([
            ('g1', {'weight':Decimal("3.00"),
                    'scale': (Decimal("0.00"),Decimal("100.00")),
                    'thresholds' : {'pref': (Decimal('20.0'), Decimal('0.0')),
                                    'ind': (Decimal('10.0'), Decimal('0.0')),
                                    'veto': (Decimal('80.0'), Decimal('0.0'))},
                    'objective': 'obj1',
                    }),
            ('g2', {'weight':Decimal("5.00"),
                    'scale': (Decimal("0.00"),Decimal("100.00")),
                    'thresholds' : {'pref': (Decimal('20.0'), Decimal('0.0')),
                                          'ind': (Decimal('10.0'), Decimal('0.0')),
                                          'veto': (Decimal('80.0'), Decimal('0.0'))},
                    'objective': 'obj2',
                    }),
            ...])
       evaluation = {'g1': {'a1':Decimal("57.28"),'a2':Decimal("99.85"), ...},
                     'g2': {'a1':Decimal("88.12"),'a2':Decimal("33.25"), ...},
                     ...}

With the help of the :py:class:`perfTabs.RandomPerformanceTableau` class let us generate for illustration a random performance tableau concerning 7 decision actions or alternatives denoted *a01*, *a02*, ..., *a07*:
    >>> from randomPerfTabs import RandomPerformanceTableau
    >>> rt = RandomPerformanceTableau(seed=100)
    >>> rt.showActions()
        *----- show decision action --------------*
        key:  a01
          short name: a01
          name:       random decision action
          comment:    RandomPerformanceTableau() generated.
        key:  a02
          short name: a02
          name:       random decision action
          comment:    RandomPerformanceTableau() generated.
        key:  a03
          short name: a03
          name:       random decision action
          comment:    RandomPerformanceTableau() generated.
        ...
        ...
        key:  a07
        name:       random decision action
        comment:    RandomPerformanceTableau() generated.
    >>> ...
   
In this example we consider furthermore a family of seven equisignificant cardinal criteria functions *g01*, *g02*, ..., *g07*, measuring the performance of each alternative on a rational scale form 0.0 to 100.00. In order to capture the evaluation's uncertainty and imprecision, each criterion function *g1* to *g7* admits three performance discrimination thresholds of 10, 20 and 80 pts for warranting respectively any indifference, preference and veto situations: 
    >>> rt.showCriteria(IntegerWeights=True)
        *----  criteria -----*
        g1 'RandomPerformanceTableau() instance'
          Scale = (0.0, 100.0)
          Weight = 1 
          Threshold ind : 10.00 + 0.00x ; percentile:  0.20
          Threshold veto : 80.00 + 0.00x ; percentile:  0.93
          Threshold pref : 20.00 + 0.00x ; percentile:  0.28
        g2 'RandomPerformanceTableau() instance'
          Scale = (0.0, 100.0)
          Weight = 1 
          Threshold ind : 10.00 + 0.00x ; percentile:  0.18
          Threshold veto : 80.00 + 0.00x ; percentile:  1.0
          Threshold pref : 20.00 + 0.00x ; percentile:  0.37
        g3 'RandomPerformanceTableau() instance'
          Scale = (0.0, 100.0)
          Weight = 1 
          Threshold ind : 10.00 + 0.00x ; percentile:  0.15
          Threshold veto : 80.00 + 0.00x ; percentile:  0.96
          Threshold pref : 20.00 + 0.00x ; percentile:  0.29
        ...
        ...
        g7 'RandomPerformanceTableau() instance'
          Scale = (0.0, 100.0)
          Weight = 1 
          Threshold ind : 10.00 + 0.00x ; percentile:  0.17
          Threshold veto : 80.00 + 0.00x ; percentile:  0.97
          Threshold pref : 20.00 + 0.00x ; percentile:  0.37
    >>> ...

The performance evaluations of each decision alternative on each criterion are gathered in a *performance tableau*:
    >>> rt.showPerformanceTableau()
        *----  performance tableau -----*
        criteria | weights |   'a01'   'a02'   'a03'    ...   'a12'   'a13'   
        ---------|----------------------------------------------------------------
           'g1'  |   1     |   14.57   45.49   77.08    ...   93.30   94.71  
           'g2'  |   1     |   33.54   30.94   76.80    ...   55.54   90.12  
           'g3'  |   1     |   81.80   16.04   64.85    ...   23.72   44.82  
           'g4'  |   1     |   63.78   90.23   12.66    ...   52.82   34.33  
           'g5'  |   1     |   85.42   36.30   48.36    ...   76.70   51.36  
           'g6'  |   1     |   49.35   58.27   14.72    ...   21.91   30.99  
           'g7'  |   1     |   62.12   65.08   74.87    ...   38.98   93.64  
    >>> ...

    """

    def __repr__(self):
        """
        Default presentation method for PerformanceTableau instances.
        """
        reprString = '*------- PerformanceTableau instance description ------*\n'
        reprString += 'Instance class   : %s\n' % self.__class__.__name__
        try:
            reprString += 'Seed             : %s\n' % str(self.randomSeed)
        except:
            pass
        reprString += 'Instance name    : %s\n' % self.name
        reprString += '# Actions        : %d\n' % len(self.actions)
        try:
            reprString += '# Objectives     : %d\n' % len(self.objectives)
        except:
            pass       
        reprString += '# Criteria       : %d\n' % len(self.criteria)
        reprString += 'Attributes       : %s\n' % list(self.__dict__.keys())     
        return reprString

    def __init__(self,filePerfTab=None,isEmpty=False):
        from decimal import Decimal
        from collections import OrderedDict
        if filePerfTab != None:
            fileName = filePerfTab + '.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(filePerfTab)
            try:
                self.actions = argDict['actions']
            except:
                self.actions = argDict['actionset']
            try:
                self.objectives = argDict['objectives']
                for obj in self.objectives:
                    self.objectives[obj]['weight'] = Decimal(self.objectives[obj]['weight'])
            except:
                pass
            try:
                self.weightset = argDict['weightset']
                self.thresholds = argDict['threshold']
                self.criteria = {}
                for g in argDict['criteria']:
                    self.criteria[g] = {'weight':Decimal(str(self.weightset[g])),
                                        'thresholds': self.thresholds[g]}
            except:
                self.criteria = argDict['criteria']
            try:
                self.weightPreorder = argDict['weightorder']
            except:
                self.weightPreorder = self.computeWeightPreorder()
            self.evaluation = argDict['evaluation']
        elif not isEmpty:
            import copy
            from randomPerfTabs import RandomPerformanceTableau
            temp = RandomPerformanceTableau()
            self.name = copy.deepcopy(temp.name)
            self.actions = copy.deepcopy(temp.actions)
            self.criteria = copy.deepcopy(temp.criteria)
            self.weightPreorder = temp.computeWeightPreorder()
            self.evaluation = copy.deepcopy(temp.evaluation)
        else:
            self.name = "empty_instance"
            self.actions = {}
            self.criteria = {}
            self.weightPreorder = {}
            self.evaluation = {}
            

    def hasOddWeightAlgebra(self,Debug=False):
        """
        Verify if the given criteria[self]['weight'] are odd or not.
        Return a Boolen value.
        """
        from digraphs import powerset
        criteria = self.criteria
        w = []
        for g in criteria:
            w.append(criteria[g]['weight'])
        if Debug:
            print('weights = ', w)
        Eorig = list(range(len(w)))
        E = set(Eorig)
        OddWeightAlgebra = True
        for X in powerset(E):
            Xc = set(Eorig) - X
            if Debug:
                print(X, Xc)
            sumX = Decimal("0")
            for x in X:
                sumX += w[x]
            sumXc = Decimal("0")
            for x in Xc:
                sumXc += w[x]
            if Debug:
                print(sumX, sumXc)
            if sumX == sumXc:
                #print sumX, sumXc
                OddWeightAlgebra = False
                break
        return OddWeightAlgebra

        
    def computeWeightedAveragePerformances(self,isNormalized=False, lowValue=0.0, highValue=100.0, isListRanked=False):
        """
        Compute normalized weighted average scores
        Normalization transforms by default all the scores into a
        common 0-100 scale. A lowValue and highValue parameter
        can be provided for a specific normalisation.
        """
        actions = self.actions
        criteria = self.criteria
        if isNormalized:
            normSelf = NormalizedPerformanceTableau(self,lowValue=lowValue,highValue=highValue)
            evaluation = normSelf.evaluation
        else:
            evaluation = self.evaluation

        sumWeights = Decimal('0.0')
        for g in dict.keys(criteria):
            sumWeights += abs(criteria[g]['weight'])

        weightedAverage = {} 
        for x in dict.keys(actions):
            weightedAverage[x] = Decimal('0.0')
            for g in dict.keys(criteria):
                weightedAverage[x] += evaluation[g][x] * criteria[g]['weight'] / sumWeights
        if isListRanked:
            ranked = []
            for x in weightedAverage:
                ranked.append((weightedAverage[x],x))
            ranked.sort(reverse=True)
            return ranked
        else:
            return weightedAverage
        
    def showActions(self,Alphabetic=False):
        """
        presentation methods for decision actions or alternatives
        """
        print('*----- show decision action --------------*')
        actions = self.actions
        if Alphabetic:
            actionsKeys = [x for x in self.actions.keys()]
            actionsKeys.sort()
            for x in actionsKeys:
                print('key: ',x)
                try:
                    print('  short name:',actions[x]['shortName'])
                except KeyError:
                    pass
                print('  name:      ',actions[x]['name'])
                try:
                    print('  comment:   ',actions[x]['comment'])
                except KeyError:
                    pass
                print()
        else:
            for x in self.actions:
                print('key: ',x)
                try:
                    print('  short name:',actions[x]['shortName'])
                except KeyError:
                    pass
                print('  name:      ',actions[x]['name'])
                try:
                    print('  comment:   ',actions[x]['comment'])
                except KeyError:
                    pass
                print()

    def showPairwiseComparison(self,a,b,hasSymetricThresholds=True,Debug=False,isReturningHTML=False,hasSymmetricThresholds=True):
        """
        renders the pairwise comprison parameters on all criteria
        in html format
        """
        from outrankingDigraphs import BipolarOutrankingDigraph
        evaluation = self.evaluation
        criteria = self.criteria
        if Debug:
            print('a,b =', a, b)
        if a != b:
            if isReturningHTML:
                html  = '<h1>Pairwise Comparison</h1>'
                html += '<h2>Comparing actions : (%s,%s)</h2>' % (a,b)
                html += '<table style="background-color:White" border="1">'
                html += '<tr bgcolor="#9acd32">'
                html += '<th>crit.</th><th>wght.</th> <th>g(x)</th> <th>g(y)</th> <th>diff</th> <th>ind</th> <th>wp</th> <th>p</th> <th>concord</th> <th>wv</th> <th>v</th> <th>polarisation</th>'
                html += '</tr>'
            else:
                print('*------------  pairwise comparison ----*')
                print('Comparing actions : (%s, %s)' % (a,b))
                print('crit. wght.  g(x)  g(y)    diff  \t| ind     wp      p    concord \t|  wv   v   weak veto veto')
                print('-------------------------------  \t ----------------------------- \t ----------------')                
            concordance = 0
            sumWeights = 0
            criteriaList = [x for x in criteria]
            criteriaList.sort()
            for c in criteriaList:
                sumWeights += abs(criteria[c]['weight'])
                if evaluation[c][a] != Decimal('-999') and evaluation[c][b] != Decimal('-999'):		
                    try:
                        indx = criteria[c]['thresholds']['ind'][0]
                        indy = criteria[c]['thresholds']['ind'][1]
                        if hasSymmetricThresholds:
                            ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            ind = indx +indy * abs(evaluation[c][a])
                    except:
                        ind = None
                    try:
                        wpx = criteria[c]['thresholds']['weakPreference'][0]
                        wpy = criteria[c]['thresholds']['weakPreference'][1]
                        if hasSymmetricThresholds:
                            wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                    except:
                        wp = None
                    try:
                        px = criteria[c]['thresholds']['pref'][0]
                        py = criteria[c]['thresholds']['pref'][1]
                        if hasSymmetricThresholds:
                            p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            p = px + py * abs(evaluation[c][a])
                    except:
                        p = None
                    if criteria[c]['weight'] > Decimal('0'):
                        d = evaluation[c][a] - evaluation[c][b]
                    else:
                        d = evaluation[c][b] - evaluation[c][a]
                    lc0 = BipolarOutrankingDigraph._localConcordance(self,d,ind,wp,p)
                    if ind != None:
                        ind = round(ind,2)
                    if wp != None:
                        wp = round(wp,2)
                    if p != None:
                        p = round(p,2)
                    if isReturningHTML:
                        html += '<tr>'
                        html += '<td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td> <td>%2.2f</td> <td>%2.2f</td> <td>%+2.2f</td> <td>%s</td>  <td>%s</td>  <td>%s</td>   <td>%+.2f</td>' % (c,criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*abs(criteria[c]['weight']))
                    else:
                         print(c, '  %.2f  %2.2f  %2.2f  %+2.2f \t| %s  %s  %s   %+.2f \t|' % (criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*criteria[c]['weight']), end=' ')
                    concordance = concordance + (lc0 * abs(criteria[c]['weight']))
                    try:
                        wvx = criteria[c]['thresholds']['weakVeto'][0]
                        wvy = criteria[c]['thresholds']['weakVeto'][1]
                        if hasSymmetricThresholds:
                            wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            wv = wvx + wvy * abs(evaluation[c][a])
                    except:
                        wv = None
                    try:
                        vx = criteria[c]['thresholds']['veto'][0]
                        vy = criteria[c]['thresholds']['veto'][1]
                        if hasSymmetricThresholds:
                            v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            v = vx + vy * abs(evaluation[c][a])
                    except:
                        v = None
                    veto = BipolarOutrankingDigraph._localVeto(self,d,wv,v)
                    try:
                        negativeVeto = BipolarOutrankingDigraph._localNegativeVeto(self,d,wv,v)
                        hasBipolarVeto = True
                    except:
                        hasBipolarVeto = False
                    if hasBipolarVeto:
                        if v != None:
                            if d >= v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, negativeVeto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ddffdd">%+2.2f</td>' % (v, negativeVeto)
                            elif d <= -v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, -veto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                            else:
                                if not isReturningHTML:                                
                                    print()
                                else:
                                    html += '</tr>'
                        elif wv != None:
                            if d >= wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, negativeVeto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ddffdd">%+2.2f</td>' % (wv, negativeVeto)
                            elif d <= -wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, -veto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if not isReturningHTML:
                                    print()
                                else:
                                    html += '</tr>'
                        else:
                            if not isReturningHTML:
                                print()
                            else:
                                html += '</tr>'
                    else:
                        ## unipolar case  Electre III for instance
                        if veto > Decimal("-1.0"):
                            if wv != None:
                                if v != None:
                                    if not isReturningHTML:
                                        print(' %2.2f %2.2f %+2.2f' % (wv, v, veto))
                                    else:
                                        html += '<td>%2.2f</td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, v, veto)
                                else:
                                    if not isReturningHTML:
                                        print(' %2.2f       %+2.2f' % (wv, -veto))
                                    else:
                                        html += '<td>%2.2f</td> <td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if v != None:
                                    if not isReturningHTML:
                                        print('       %2.2f %+2.2f' % (v, veto))
                                    else:
                                        html += '<td></td> <td>%2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                                else:
                                    if not isReturningHTML:
                                        print()
                                    else:
                                        html += '</tr>'
                        
                else:
                    if evaluation[c][a] == Decimal("-999"):
                        eval_c_a = 'NA'
                    else:
                        eval_c_a = '%2.2f' % evaluation[c][a]
                    if evaluation[c][b] == Decimal("-999"):
                        eval_c_b = 'NA'
                    else:
                        eval_c_b = '%2.2f' % evaluation[c][b]
                    
                    if not isReturningHTML:
                        print(c,'    %s %s' % (eval_c_a,eval_c_b))
                    else:
                        html += '<td bgcolor="#FFEEAA" align="center">%s</td> <td>%s</td><td>%s</td><td>%s</td><td></td><td></td><td></td><td></td><td>%.2f</td></tr>' % (c, criteria[c]['weight'],eval_c_a,eval_c_b, self.valuationdomain['med']*criteria[c]['weight'])
            if not isReturningHTML:
                print('             ----------------------------------------')
                print(' Valuation in range: %+.2f to %+.2f; global concordance: %+.2f' % (-sumWeights,sumWeights,concordance))
            else:
                html += '</tr></table>'
                html += '<b>Valuation in range: %+.2f to %+.2f; global concordance: %+.2f </b>' % (-sumWeights,sumWeights,concordance)
        if isReturningHTML:
            return html

    
    def showCriteria(self,IntegerWeights=False,Alphabetic=False,ByObjectives=False,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
        criteria = self.criteria
        try:
            objectives = self.objectives
        except:
            ByObjectives = False
        print('*----  criteria -----*')
##        sumWeights = Decimal('0.0')
##        for g in criteria:
##            sumWeights += criteria[g]['weight']
        sumWeights = sum([abs(criteria[g]['weight']) for g in criteria])
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
                            print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                    except:
                        pass
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
                        print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
                except:
                    pass
                print()

    def showObjectives(self):
        if 'objectives' in self.__dict__:
            print('*------ decision objectives -------"')
            
            for obj in self.objectives:
                                                   
                print('%s: %s' % (obj, self.objectives[obj]['name']))
                                                   
                for g in self.objectives[obj]['criteria']:
                    print('  ', g, self.criteria[g]['name'], self.criteria[g]['weight'])
                                                   
                print('  Total weight: %.2f (%d criteria)\n'\
                      % (self.objectives[obj]['weight'],len(self.objectives[obj]['criteria'])))
        else:
            print('The performance tableau does not contain objectives.')

    def showWeightPreorder(self):
        """
        Renders a preordering of the the criteria signficance weights. 
        """
        print('*------- weights preordering --------*')
        wpo = self.computeWeightPreorder()
        n = len(wpo)
        for i in range(0,n-1):
            print(wpo[i], '(%s) <' % self.criteria[wpo[i][0]]['weight'])
        print(wpo[-1], '(%s)' % self.criteria[wpo[-1][0]]['weight'])
            
    def convertInsite2Standard(self):
        """
        Convert in site a bigData formated Performance tableau back into a standard formated PerformanceTableau instance.
        """
        self.convertWeight2Decimal()
        self.convertEvaluation2Decimal()
        self.convertDiscriminationThresholds2Decimal()

    def convertInsite2BigData(self):
        """
        Convert in site a standard formated Performance tableau into a bigData formated instance.
        """
        self.convertWeight2Integer()
        self.convertEvaluation2Float()
        self.convertDiscriminationThresholds2Float()

    def convert2BigData(self):
        """
        Renders a cPerformanceTableau instance, by converting the action keys to integers and evaluations to floats, including the discrimination thresholds, the case given.
        """
        from collections import OrderedDict
        from cRandPerfTabs import cPerformanceTableau
        from copy import deepcopy
        t = PerformanceTableau(isEmpty=True)
        t.name = 'bgd_' + self.name
        att = [a for a in self.__dict__]
        att.remove('name')
        att.remove('actions')
        att.remove('evaluation')
        for a in att:
            t.__dict__[a] = deepcopy(self.__dict__[a])
        # convert action keys to integers
        t.convertWeight2Integer()
        t.convertDiscriminationThresholds2Float()
        actions = self.actions
        newActions = OrderedDict()
        for i,x in enumerate(actions):
            newKey = i
            newActions[newKey] = actions[x]
        # convert evaluation access keys
        evaluation = self.evaluation
        newEvaluation = {}
        for g in t.criteria:
            newEvaluation[g] = {}
            for i,x in enumerate(actions):
                newKey = i
                newEvaluation[g][newKey] = float(evaluation[g][x])
        t.actions = newActions
        t.evaluation = newEvaluation
        # change the object class
        t.__class__ = cPerformanceTableau
        return t
        
    def convertWeight2Integer(self):
        """
        Convert significance weights from Decimal format
        to int format.
    """
        criteria = self.criteria
        for g in criteria:
            criteria[g]['weight'] = int(criteria[g]['weight'])
        self.criteria = criteria

    def convertEvaluation2Float(self):
        """
        Convert evaluations from decimal format to float
        """
        from decimal import Decimal
        evaluation = self.evaluation
        actions = self.actions
        criteria = self.criteria
        for g in criteria:
            for x in actions:
                if evaluation[g][x] != Decimal('-999'):
                    evaluation[g][x] = float(evaluation[g][x])
        self.evaluation = evaluation

    def convertDiscriminationThresholds2Float(self):
        criteria = self.criteria
        for g in criteria:
            for th in criteria[g]['thresholds']:
                d = criteria[g]['thresholds'][th]
                d1 = (float(d[0]),float(d[1]))
                criteria[g]['thresholds'][th] = d1

    def convertDiscriminationThresholds2Decimal(self):
        from decimal import Decimal
        criteria = self.criteria
        for g in criteria:
            for th in criteria[g]['thresholds']:
                d = criteria[g]['thresholds'][th]
                d1 = (Decimal(str(d[0])),Decimal(str(d[1])))
                criteria[g]['thresholds'][th] = d1

 
    def convertWeight2Decimal(self):
        """
        Convert significance weights from obsolete float format
        to decimal format.
        """
        from decimal import Decimal
        criteria = self.criteria
        criteriaList = [x for x in self.criteria]
        for g in criteriaList:
            criteria[g]['weight'] = Decimal(str(criteria[g]['weight']))
        self.criteria = criteria

    def convertEvaluation2Decimal(self):
        """
        Convert evaluations from obsolete float format to decimal format
        """
        from decimal import Decimal
        evaluation = self.evaluation
        actionsList = [x for x in self.actions]
        criteriaList = [x for x in self.criteria]
        for g in criteriaList:
            for x in actionsList:
                evaluation[g][x] = Decimal(str(evaluation[g][x]))
        self.evaluation = evaluation

    def convertWeights2Negative(self):
        """
        Negates the weights of criteria to be minimzed.
        """
        from decimal import Decimal
        criteria = self.criteria
        evaluation = self.evaluation
        for g in criteria:
            critg = criteria[g]
            if critg['preferenceDirection'] == 'min':
                critg['weight'] = -abs(critg['weight'])
                valg = evaluation[g]
                for x in valg:
                    if valg[x] != Decimal('-999'):
                        #print(g,x,valg[x])
                        valg[x] = abs(valg[x])
        self.criteria = criteria
        self.evaluation = evaluation

    def convertWeights2Positive(self):
        """
        Negates the weights of criteria to be minimzed.
        """
        from decimal import Decimal
        criteria = self.criteria
        evaluation = self.evaluation
        for g in criteria:
            critg = criteria[g]
            if critg['preferenceDirection'] == 'min':
                critg['weight'] = abs(critg['weight'])
                valg = evaluation[g]
                for x in valg:
                    if valg[x] != Decimal('-999'):
                        #print(g,x,valg[x])
                        valg[x] = -abs(valg[x])
        self.criteria = criteria
        self.evaluation = evaluation
        
    def computePerformanceDifferences(self,Comments = False,
                                      Debug = False,
                                      NotPermanentDiffs=True,
                                      WithMaxMin=False):
        """
        Adds to the criteria dictionary the ordered list of all observed performance differences.
        """
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
        if Debug:
            Comments = True
        if Comments:
            print('Compute performance differences on each criterion')
        #criteriaList = [x for x in self.criteria]
        #criteriaList.sort()
        actionsList = list(dict.keys(actions))
        n = len(actionsList)
        if NotPermanentDiffs:
            performanceDifferences = {}
        for c in criteria.keys():
            ed = Decimal(str(criteria[c]['scale'][1])) - Decimal(str(criteria[c]['scale'][0]))
            md = Decimal('0')
            #diff = set()
            diffList = []
            for i in range(n):
                xi = evaluation[c][actionsList[i]]
                if xi != Decimal('-999'):
                    for j in range(i+1,n):
                        xj = self.evaluation[c][actionsList[j]]
                        if xj != Decimal('-999'):
                            delta = abs(xi - xj)
                            if delta < ed:
                                ed = delta
                            if delta > md:
                                md = delta
                            #diff.add(delta)
                            diffList.append(delta)
                            if Debug:
                                print('-->> i,j, evaluation[actionsList[i]],evaluation[actionsList[j]], delta, ed,md',\
                                      i,j, evaluation[c][actionsList[i]],evaluation[c][actionsList[j]],\
                                      delta, ed,md,diffList)
            criteria[c]['minimalPerformanceDifference'] = ed
            criteria[c]['maximalPerformanceDifference'] = md
            #diffList = list(diff)
            diffList.sort()
            if NotPermanentDiffs:
                if WithMaxMin:
                    performanceDifferences[c] = (diffList,ed,md)
                else:
                    performanceDifferences[c] = diffList
            else:
                criteria[c]['performanceDifferences'] = diffList
                if Comments:
                    print(' -->', c, ': ', criteria[c]['minimalPerformanceDifference'],\
                          criteria[c]['maximalPerformanceDifference'])
                    print(len(criteria[c]['performanceDifferences']),criteria[c]['performanceDifferences'])
                    print(criteria[c]['performanceDifferences'][0], criteria[c]['performanceDifferences'][-1])

        if NotPermanentDiffs:
            return performanceDifferences
        
    def mpComputePerformanceDifferences(self,NotPermanentDiffs=True,nbrCores=None,Debug=False):
        """
        Adds to the criteria dictionary the ordered list of all observed performance differences.
        """
        criteria = self.criteria
        from multiprocessing import Pool
        #from os import cpu_count
        if Debug:
            print('Compute performance differences on each criterion in parallel')
       
        #criteriaList = [x for x in self.criteria]
        #criteriaList.sort()

        with Pool(nbrCores) as proc:
            performanceDifferences = proc.map(self.computeCriterionPerformanceDifferences,criteriaList)
        
        #for i in range(len(criteriaList)):
        #    c = criteriaList[i]
        for c in criteria.keys():
            if not NotPermanentDiffs:
                criteria[c]['performanceDifferences'] = performanceDifferences[i][0]
            criteria[c]['minimalPerformanceDifference'] = performanceDifferences[i][1]
            criteria[c]['maximalPerformanceDifference'] = performanceDifferences[i][2]

        return performanceDifferences


    def computeCriterionPerformanceDifferences(self,c, Comments = False,
                                      Debug = False):
        """
        Renders the ordered list of all observed performance differences on the given criterion.
        """
        evaluation = self.evaluation
        criteria = self.criteria
        actions = self.actions
        if Debug:
            Comments = True
        if Comments:
            print('Compute performance differences on criterion %s' % c)
        actionsList = list(dict.keys(actions))
        n = len(actionsList)
        ed = Decimal(str(criteria[c]['scale'][1])) - Decimal(str(criteria[c]['scale'][0]))
        md = Decimal('0')
        #diff = set()
        diffList = []
        for i in range(n):
            xi = evaluation[c][actionsList[i]]
            if xi != Decimal('-999'):
                for j in range(i+1,n):
                    xj = evaluation[c][actionsList[j]]
                    if xj != Decimal('-999'):
                        delta = abs(xi - xj)
                        if delta < ed:
                            ed = delta
                        if delta > md:
                            md = delta
                        #diff.add(delta)
                        diffList.append(delta)
                        if Debug:
                            print('-->> i,j, evaluation[actionsList[i]],evaluation[actionsList[j]], delta, ed,md',\
                                  i,j, evaluation[c][actionsList[i]],evaluation[c][actionsList[j]],\
                                  delta, ed,md,diffList)
        criteria[c]['minimalPerformanceDifference'] = ed
        criteria[c]['maximalPerformanceDifference'] = md
        #diffList = list(diff)
        diffList.sort()
        if Comments:
            print(' -->', c, ': ', criteria[c]['minimalPerformanceDifference'],\
                  criteria[c]['maximalPerformanceDifference'])
            print(len(diffList),diffList)
            print(diffList[0], diffList[-1])
        
        return (diffList,ed,md)
            
    def computeActionCriterionPerformanceDifferences(self,refAction,refCriterion,comments = False, Debug = False):
        """
        computes the performances differences observed between the reference action and the others on the given criterion
        """
        evaluation = self.evaluation
        actions = self.actions
        if Debug:
            comments = True
        if comments:
            print('Compute performance differences for action %s on criterion %s' % (refAction, refCriterion))

        diff = []
        for x in dict.keys(actions):
            if x != refAction:
                xr = evaluation[refCriterion][refAction]
                xo = evaluation[refCriterion][x]
                if xr != Decimal('-999') and xo != Decimal('-999'):
                    delta = abs(evaluation[refCriterion][refAction] - evaluation[refCriterion][x])
                    diff.append(delta)
                    if Debug:
                        print('-->> refAction, x, evaluation[refAction], evaluation[x], delta,diff',\
                              refAction,x, evaluation[refCriterion][refAction],evaluation[refCriterion][x], delta,diff)

        diff.sort()
        return diff

    def computeActionCriterionQuantile(self,action,criterion,Debug=False):
        """
        renders the quantile of the performance of action on criterion
        """
        perfsy = self.evaluation[criterion]
        if Debug:
            print(action,criterion)
        perfx = self.evaluation[criterion][action]
        if perfx != Decimal('-999'):
            try:
                indx = self.criteria[criterion]['thresholds']['ind'][0]\
                       + self.criteria[criterion]['thresholds']['ind'][1]*perfx
                ## indx = self.criteria[criterion]['thresholds']['ind'][0] + self.criteria[criterion]['thresholds']['pref'][1]*perfx
            except:
                indx = Decimal('0')
            quantile = float(len([y for y in perfsy\
                                  if (y in self.actions) and (perfsy[y] != Decimal(-999)) and \
                                  #(perfsy[y] <= perfx+indx)]) )/float(len(self.actions))
                                  (perfsy[y] <= perfx)]) )/float(len(self.actions))
            return quantile
        else:
            return 'NA'

    def _computeLimitingQuantiles(self,g,frequencies,LowerClosed=True,Debug=False,PrefThresholds=True):
        """
        Renders the list of limiting quantiles *q(p)* on criteria *g* for *p* in *frequencies* 
        """
        from math import floor
        from copy import copy, deepcopy
        gValues = []
        for x in self.actions:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,self.evaluation[g][x])
            if self.evaluation[g][x] != Decimal('-999'):
                gValues.append(self.evaluation[g][x])
        gValues.sort()
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
        if Debug:
            print(limitingQuantiles)
        if LowerClosed:
            limitingQuantiles = limitingQuantiles[:-1]
        else:
            limitingQuantiles = limitingQuantiles[1:]
        if Debug:
            print(limitingQuantiles)
        # computing the quantiles on criterion g
        gQuantiles = []
        if LowerClosed:
            # we ignorethe 1.00 quantile and replace it with +infty
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

    def computeQuantiles(self,Debug=False):
        """
        renders a quantiles matrix action x criterion with the performance quantile of action on criterion
        """
        #actionsList = [x for x in self.actions]
        #criteriaList = list(self.criteria.keys())
##        
##        if Debug:
##            print(actionsList,criteriaList)
        actions = self.actions
        quantiles = {}
        for x in dict.keys(actions):
            quantiles[x] = self.computeActionQuantile(x,Debug)
        self.quantiles = quantiles
        if Debug:
            print(quantiles)
        return quantiles

    def computeActionQuantile(self,action,Debug=True):
        """
        renders the overall performance quantile of action
        """
        #criteriaList = [x for x in self.criteria]
        criteria = self.criteria
        criteriaQuantiles = []
        sumWeights = 0
        for g in dict.keys(criteria):
            agq = self.computeActionCriterionQuantile(action,g,Debug)
            if agq != 'NA':
                sumWeights += criteria[g]['weight']
                criteriaQuantiles.append((agq,float(criteria[g]['weight'])))
        criteriaQuantiles.sort()
        i = 0
        currentQuantile = 0.0
        currentWeight = 0.0
        minQuantile = criteriaQuantiles[i][0] 
        minWeight = criteriaQuantiles[i][1]
        majority = float(sumWeights)/2.0
        if Debug:
            print(majority,i, currentWeight,minWeight, currentQuantile, minQuantile)
        while minWeight < majority:
            i += 1
            currentQuantile = minQuantile
            currentWeight = minWeight
            minQuantile = criteriaQuantiles[i][0] 
            minWeight += criteriaQuantiles[i][1]
        if Debug:
            print(i, currentWeight,minWeight, currentQuantile, minQuantile)
        actionQuantile = currentQuantile + (majority-currentWeight)/(minWeight-currentWeight)*(minQuantile-currentQuantile)
        if Debug:
            print('quantile for %s = %.3f' % (action,actionQuantile))
        return actionQuantile

            
    def csvAllQuantiles(self, fileName='quantiles'):
        """
        save quantiles matrix criterionxaction in CSV format
        """
        actions = self.actions
        criteria = self.criteria
        fileNameExt = fileName+'.csv'
        fo = open(fileNameExt,'w')
##        criteriaList = [x for x in self.criteria]
##        criteriaList.sort()
##        actionsList = [x for x in self.actions]
##        actionsList.sort()
        fo.write('# saved quantiles matrix from performance tableau %s \n' % self.name)
        fo.write('"quantiles",')
        n = len(actions)
        i = 0
        for x in dict.keys(actions):
            #x = actionsList[i]
            if i < n-1:
                fo.write('"%s",' % x)
            else:
                fo.write('"%s"\n' % x)
            i += 1
        print('\nweights  | ', end=' ') 
        for g in dict.keys(criteria):
            fo.write('"%s",' % g)
            i = 0
            for x in dict.keys(actions):
                qval = self.computeActionCriterionQuantile(x,g,Debug=False)
                if i < n-1:
                    if qval != 'NA':
                        fo.write('%.2f,' % qval)
                    else:
                        fo.write('NA,')
                else:
                    if qval != 'NA':
                        fo.write('%.2f\n' % qval)
                    else:
                        fo.write('NA\n')
                i += 1
        fo.close()


    def showAllQuantiles(self,Sorted=True):
        """
        prints the performance quantiles tableau in the session console.
        """
        self.computeAllQuantiles(Sorted=Sorted,Comments=True)

    def showHTMLPerformanceQuantiles(self,Sorted=True):
        """
        shows the performance quantiles tableau in a browser window.
        """
        import webbrowser
        fileName = '/tmp/performanceQuantiles.html'
        fo = open(fileName,'w')
        fo.write(self.computeAllQuantiles(Sorted=Sorted,Comments=False))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
        
    def computeAllQuantiles(self,Sorted=True,Comments=False):
        """
        renders a html string showing the table of
        the quantiles matrix action x criterion
        """
        criteria = self.criteria
        criteriaList = list(criteria.keys())
        if Sorted:
            criteriaList.sort()
        actions = self.actions
        actionsList = list(actions.keys())
        if Sorted:
            actionsList.sort()
        html = '<table style="background-color:White;" border="1">\n'
        if Comments:
            print('criteria | ', end=' ')
        html += '<tr bgcolor="#9acd32"><th>criteria</th>'
        for g in criteriaList:
            if Comments:
                print(str(g) + '\t', end=' ')
            html += '<th>%s</th>' % (g)
        print()
        html += '</tr>\n'
        if Comments:
            print('\nweights  | ', end=' ') 
        html += '<tr style="text-align: center;" bgcolor="#FFF79B"><td>weights</td>'
        for g in criteriaList:
            if Comments:
                print(str(criteria[g]['weight']) + '\t', end=' ')
            html += '<td >%s</td>' % (criteria[g]['weight'])
        html += '</tr>\n'
        if Comments:
            print('\n-----------------------------------------------------')
        for x in actionsList:
            if Comments:
                print(str(x) + '   | ', end=' ')
            html += '<tr><th  bgcolor="#FFF79B">%s</th>' % (x)
            for g in criteriaList:
                qval = self.computeActionCriterionQuantile(x,g,Debug=False)
                if qval != 'NA':
                    if Comments:
                        print('%.2f\t' % qval, end=' ')
                    html += '<td>%.2f</td>' % (qval)
                else:
                    if Comments:
                        print('NA\t', end=' ')
                    html += '<td>NA</td>'
            if Comments:
                print()
            html += '</tr>\n'
                                          
        html += '</table>\n'
        return html

    def computeQuantileOrder(self,q0=3,q1=0,Threading=False,nbrOfCPUs=1,Comments=False):
        """
        Renders a linear ordering of the decision actions from a simulation of pre-ranked outranking digraphs.

        The pre-ranking simulations range by default from
        quantiles=q0 to quantiles=min( 100, max(10,len(self.actions)/10]) ).

        The actions are ordered along a decreasing Borda score of their ranking results.
        
        """
        from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
        from operator import itemgetter
        n = len(self.actions)
        kBestFrequency = OrderedDict([(x,[0 for r in range(n+1)]) for x in self.actions])
        ordering = []
        if q1 <= q0:
            q1 = min(100,max(11,n//10))
        for q in range(q0,q1):
            pr = PreRankedOutrankingDigraph(self,quantiles=q,LowerClosed=False,
                                    minimalComponentSize=1,
                                    CopyPerfTab=True,Threading=Threading,
                                    nbrOfCPUs=nbrOfCPUs)
            for r in range(n):
                rbest = pr.boostedOrder[r]
                kBestFrequency[rbest][r] += 1
        for x in self.actions:
            stats = kBestFrequency[x]
            for i in range(n):
                stats[n] += (i+1)*stats[i]
        Stats = [(x,-kBestFrequency[x][n],kBestFrequency[x][:-1]) for x in self.actions]
        bestStatistics = sorted(Stats,key=itemgetter(1,2),reverse=True)
        quantileOrder = [x[0] for x in bestStatistics]
        if Comments:
            print(bestStatistics)
            print(quantileOrder)
        return quantileOrder

    def computeQuantileRanking(self,q0=3,q1=0,Threading=False,nbrOfCPUs=1,Comments=False):
        """
        Renders a linear ranking of the decision actions from a simulation of pre-ranked outranking digraphs.

        The pre-ranking simulations range by default from
        quantiles=q0 to qantiles=min( 100, max(10,len(self.actions)/10) ).

        The actions are ordered along an increasing Borda score of their ranking results.
        
        """
        ranking = self.computeQuantileOrder(q0=q0,q1=q1,\
                                          Threading=Threading,nbrOfCPUs=nbrOfCPUs,\
                                              Comments=Comments)
        ranking.reverse()
        if Comments:
            print(ranking)
        return ranking
        
    def computeQuantileSort(self):
        """
        shows a sorting of the actions from decreasing majority quantiles
        """
        self.computeQuantiles()
        actionsSorting = []
        for x in list(self.actions.keys()):
            actionsSorting.append((self.quantiles[x],x))
        actionsSorting.sort(reverse=True)
        return actionsSorting

    def computeQuantilePreorder(self,Comments=True,Debug=False):
        """
        computes the preorder of the actions obtained from decreasing majority quantiles. The quantiles are recomputed with a call to the self.computeQuantileSort() method.
        """
        quantiles = self.computeQuantileSort()
        quantiles.sort(reverse=True)
        if Debug:
            Comments = True
        if Comments:
            print(quantiles)
        actionsPreorder = []
        currLevel = 0.0
        currEquivalenceClass = []
        for x in quantiles:
            if Debug:
                print(currLevel,x)
            if x[0] >= currLevel:
                currEquivalenceClass.append(x[1])
                if Debug:
                    print(currEquivalenceClass)
            else:
                currEquivalenceClass.sort()
                actionsPreorder.append(currEquivalenceClass)
                if Debug:
                    print(actionsPreorder)
                currEquivalenceClass = [x[1]]
            currLevel = x[0]
        currEquivalenceClass.sort()
        actionsPreorder.append(currEquivalenceClass)
        if Comments:
            print(actionsPreorder)
        return actionsPreorder

    def showQuantileSort(self,Debug=False):
        """
        Wrapper of computeQuantilePreorder() for the obsolete showQuantileSort() method.
        """
        self.computeQuantilePreorder(Debug=Debug,Comments=True)
 
    def computeDefaultDiscriminationThresholds(self,criteriaList=None,
                                               quantile = {'ind':10,'pref':20,'weakVeto':60,'veto':80},
                                               Debug = False,
                                               Comments = False):
        """
        updates the discrimination thresholds with the percentiles
        from the performance differences.
        Parameters: quantile = {'ind': 10, 'pref': 20, 'weakVeto': 60, 'veto: 80}.
        
        """
        import math
        
        if Debug:
            Comments = True
            
        if Comments:
            print('Installs default discrimination thresholds on each criterion')

#        performanceDifferences = self.computePerformanceDifferences(Debug=Debug,Comments=Comments)
        criteria = self.criteria
        if criteriaList == None:
            criteriaList = [x for x in dict.keys(criteria)]
            #criteriaList.sort()
        for c in criteriaList:
            performanceDifferences,minDiff,maxDiff = self.computeCriterionPerformanceDifferences(c,
                                                            Comments=Comments,Debug=Debug)
            #vx = self.criteria[c]['performanceDifferences']
            vx = performanceDifferences
            nv = len(vx)
            if Debug:
                print('=====>',c)
                print(vx)
                print(nv)
            threshold = {}
            for x in quantile:
                if Debug:
                    print('-->', x, quantile[x], end=' ')

                if quantile[x] == -1:
                    pass
                else:
                    if quantile[x] == 0:
                        threshold[x] = vx[0]
                    elif quantile[x] == 100:
                        threshold[x] = vx[nv-1]
                    else:
                        kq = int(math.floor(float(quantile[x]*(nv-1))/100.0))
                        r = ((nv-1)*quantile[x]) % 100
                        if Debug:
                            print(kq,r, end=' ')

                        ## if kq == nv-1:
                        ##     kqplus = nv-1
                        ## else:
                        ##     kq_1 = kq - 1
                        threshold[x] = vx[kq] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq+1]-vx[kq])
                        if Debug:
                            print(threshold[x])

            
            criteria[c]['thresholds'] = {}
            for x in threshold:
                criteria[c]['thresholds'][x] = (threshold[x],Decimal('0.0'))

            if Comments:
                print('criteria',c,' default thresholds:')
                print(criteria[c]['thresholds'])


    def computeThresholdPercentile(self,criterion,threshold, Debug=False):
        """
        computes for a given criterion the quantile
        of the performance differences of a given constant threshold.
        """
        criteria = self.criteria
        try:
            performanceDifferences = criteria[criterion]['performanceDifferences']
        except:
            #self.computePerformanceDifferences(Debug=Debug)
            #performanceDifferences = self.criteria[criterion]['performanceDifferences']
            performanceDifferences,minDiff,maxDiff = self.computeCriterionPerformanceDifferences(criterion)
        if Debug:
            print("performanceDifferences = ",performanceDifferences)
        try:
            quantile = criteria[criterion]['thresholds'][threshold][0]     
        except:
            return None
        if Debug:
            print('quantile', quantile)
        nv = len(performanceDifferences)
        i = 0
        while i < nv and performanceDifferences[i] <= quantile:
            if Debug:
                print(i, quantile, performanceDifferences[i])
            i += 1
        percentile = float(i)/float(nv)
        if Debug:
            print('i = ', i, 'nv = ', nv)
            print('percentile =', percentile)
        return percentile

    def computeVariableThresholdPercentile(self,criterion, threshold, Debug=False):
        """
        computes for a given criterion the quantile
        of the performance differences of a given threshold.
        """
        try:
            th = self.criteria[criterion]['thresholds'][threshold]
        except:
            return None

##        actionsList = [x for x in self.actions]
##        actionsList.sort()
        actions = self.actions
        evaluation = self.evaluation
        count = 0
        total = 0
        for a in dict.keys(actions):
            performanceDifferences = self.computeActionCriterionPerformanceDifferences(a,criterion,Debug)
            if Debug:
                print('performanceDifferences:', performanceDifferences)
            na = len(performanceDifferences)
            total += na
            i = 0
            quantile = Decimal(str(th[0])) + abs(evaluation[criterion][a])*Decimal(str(th[1]))
            if Debug:
                print('a,na,self.evaluation[criterion][a],th[0],th[1],quantile',\
                      a,na,evaluation[criterion][a],th[0],th[1],quantile)
            while i < na and performanceDifferences[i] <= quantile:
                if Debug:
                    print('i, quantile, performanceDifferences[i]',i, quantile, performanceDifferences[i])
                i += 1
            count += i
            if Debug:
                print('a,na,final i', a,na,i)
        percentile = float(count)/float(total)
        if Debug:
            print('count = ', count, 'total = ', total)
            print('percentile =', percentile)   
        return percentile

    def showPerformanceTableau(self,Transposed=False,actionsSubset=None,\
                               fromIndex=None,toIndex=None,Sorted=True,ndigits=2):
        """
        Print the performance Tableau.
        """
        from decimal import Decimal
        print('*----  performance tableau -----*')
        criteriaList = list(self.criteria)
        if Sorted:
            criteriaList.sort()
        if actionsSubset == None:
            actionsList = list(self.actions)
            if Sorted:
                actionsList.sort()
        else:
            actionsList = list(actionsSubset)
        if fromIndex == None:
            fromIndex = 0
        if toIndex == None:
            toIndex=len(actionsList)
        # view criteria x actions
        if Transposed:
            print('criteria | weights |', end=' ')
            for x in actionsList:
                print('\''+str(x)+'\'  ', end=' ')
            print('\n---------|-----------------------------------------')
            formatString = '%% .%df ' % ndigits
            for g in criteriaList:
                print('   \''+str(g)+'\'  |   '+str(self.criteria[g]['weight'])+'   | ', end=' ')
                for i in range(fromIndex,toIndex):
                    x = actionsList[i]
                    evalgx = self.evaluation[g][x]
                    if evalgx == Decimal('-999'):
                        print(' NA ', end=' ')
                    else:                    
                        print(formatString % (evalgx), end=' ')
                print()
        # view actions x criteria
        else:
            print('Criteria | ', end=' ')
            for g in criteriaList:
                print('\''+str(g)+'\'  ', end=' ')
            print('\nActions  | ', end=' ')
            for g in criteriaList:
                print('  %s   ' % str(self.criteria[g]['weight'] ), end=' ')          
            print('\n---------|-----------------------------------------')
            formatString = '%% .%df ' % ndigits
            for i in range(fromIndex,toIndex):
                x = actionsList[i]
                print('   \''+str(self.actions[x]['name'])+'\'   |' , end=' ')
                for g in criteriaList:
                    evalgx = self.evaluation[g][x]
                    if evalgx == Decimal('-999'):
                        print('  NA  ', end=' ')
                    else:                    
                        print(formatString % (evalgx), end=' ')
                print()
            

    def saveCSV(self,fileName='tempPerfTab',Sorted=True,criteriaList=None,actionsList=None,ndigits=2,Debug=False):
        """1
        Store the performance Tableau self Actions x Criteria in CSV format.
        """
        import itertools as IT
        import collections
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        
        fileNameExt = fileName + '.csv'        
        print('*Storing performance tableau in CSV format in file %s'\
              % fileNameExt)
        if criteriaList == None:
            criteriaList = list(dict.keys(criteria))
            if sorted:
                criteriaList.sort()
        ng = len(criteriaList)
        if Debug:
            print(criteriaList)
        if actionsList == None:
            actionsList = list(dict.keys(actions))
            if sorted:
                actionsList.sort()
        else:
            actionsList = flatten(actionsList)
        if Debug:
            print(actionsList)
        na = len(actionsList)
        formatStr = '%%.%.df' % ndigits
        if Debug:
            print('formatString:',formatStr)
        fo = open(fileNameExt,'w')
        ## header row
        writeStr = '"criteria","name","weight","scale","prefDir","thresholds",'
        for i in range(na-1):
            writeStr += '"%s",' % actionsList[i]
        writeStr += '"%s"\n' % actionsList[na-1]
        if Debug:
            print(writeStr)
        fo.write(writeStr)
        ## writing performance data
        for g in criteriaList:
            writeStr = '"%s",' % g
            writeStr += '"%s",' % str(self.criteria[g]['name'])
            writeStr += '"%s",' % self.criteria[g]['weight']
            writeStr += '"%s",' % str(self.criteria[g]['scale'])
            writeStr += '"%s",' % str(self.criteria[g]['preferenceDirection'])
            writeStr += '"%s",' % str(self.criteria[g]['thresholds'])
            for i in range(na-1):
                writeStr += formatStr % evaluation[g][actionsList[i]] + ','
            writeStr += formatStr % evaluation[g][actionsList[na-1]] + '\n'
            if Debug:
                print(writeStr)
            fo.write(writeStr)
        fo.close()
        

    def computeMinMaxEvaluations(self,criteria=None,actions=None):
        """
        renders minimum and maximum performances on each criterion
        in dictionary form: {'g': {'minimum': x, 'maximum': x}}
        """
        evaluation = self.evaluation 
        if criteria == None:
            criteria = self.criteria
            criteriaKeys = [x for x in dict.keys(criteria)]
        else:
            criteriaKeys = criteria
        if actions == None:
            actions = self.actions
            actionsKeys = [x for x in dict.keys(actions)]
        else:
            actionsKeys = actions
        result = {}
        for g in criteriaKeys:
            result[g] = {}
            evaluations = []
            for x in actionsKeys:
                val = evaluation[g][x]
                if val != Decimal('-999'):
                    evaluations.append(val)
            n = len(evaluations)
            if n > 1:
                evaluations.sort()
                result[g]['minimum'] = evaluations[0]
                result[g]['maximum'] = evaluations[-1]
            elif n == 1:
                result[g]['minimum'] = evaluations[0]
                result[g]['maximum'] = evaluations[0]
            else:
                result[g]['minimum'] = Decimal('-999')
                result[g]['maximum'] = Decimal('-999')
        return result

    def showHTMLCriteria(self,criteriaSubset=None,Sorted=True,\
                         ndigits=2,\
                         title=None):
        """
        shows the criteria in the system browser view.
        """
        import webbrowser
        fileName = '/tmp/criteriaView.html'
        fo = open(fileName,'w')
        fo.write(self._htmlCriteriaView(criteria=criteriaSubset,Sorted=Sorted,\
                                           ndigits=ndigits,\
                                           title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)

    def _htmlCriteriaView(self,criteria=None,Sorted=False,\
                         ndigits=2,title='Family of Criteria'):
        """
        Renders a html view of the in the XMCDA2 format.
        """
        if title == None:
            html = '<h1>%s: Family of Criteria</h1>' % self.name
        else:
            html = '<h1>%s</h1>' % title            
        if criteria == None:
            criteria = self.criteria
        criteriaList = [x for x in criteria]
        if Sorted:
            criteriaList.sort()
        
        html += """<table border="1">
        <tr bgcolor="#9acd32">
        <th rowspan="2">#</th>
        <th rowspan="2">Identifyer</th>
        <th rowspan="2">Name</th>
        <th rowspan="2">Comment</th>
        <th rowspan="2">Weight</th>
        <th colspan="3">Scale</th>
        <th colspan="5">Thresholds (ax + b)</th>
        </tr>
        <tr bgcolor="#9acd32">
        <th>direction</th>
        <th>min</th>
        <th>max</th>
        <th>indifference</th>
        <th>preference</th>
        <th>veto</th>
        </tr>"""
        i = 0
        for g in criteriaList:
            i += 1
            critg = criteria[g]
            #print(g,critg)
            html += '<tr><td align="center">%s</td>' % i
            try:
                html += '<th bgcolor="#FFF79B">%s</th>' % critg['shortName']
            except:
                html += '<th bgcolor="#FFF79B">%s</th>' % g
            try:
                html += '<td>%s</td><td>%s</td>' % (critg['name'],critg['comment'])
            except:
                html += '<td>%s</td><td>No comment</td>' % (critg['name'])
            html += '<td align="center">%.2f</td>' % critg['weight']
            html += '<td align="center">%s</td>' % critg['preferenceDirection']
            html += '<td align="center">%.2f</td>' % critg['scale'][0]
            html += '<td align="center">%.2f</td>' % critg['scale'][1]

            try:
                if critg['thresholds']['ind'] != None:
                    html += '<td align="center">%.2fx + %.2f</td>' %\
                                (critg['thresholds']['ind'][1],\
                                 critg['thresholds']['ind'][0])                
            except:
                html += '<td></td>'
                
            try:
                if critg['thresholds']['pref'] != None:
                    html += '<td align="center">%.2fx + %.2f</td>' %\
                                (critg['thresholds']['pref'][1],\
                                 critg['thresholds']['pref'][0])                
            except:
                html += '<td></td>'
            try:
                if critg['thresholds']['veto'] != None:
                    html += '<td align="center">%.2fx + %.2f</td>' %\
                                (critg['thresholds']['veto'][1],\
                                 critg['thresholds']['veto'][0])                
            except:
                html += '<td></td>'

            html += '</tr>'
            
        html += '</table>'
        return html
        
        
    def showHTMLPerformanceTableau(self,actionsSubset=None,\
                                   fromIndex=None,toIndex=None,\
                                   isSorted=True,\
                                   Transposed=False,ndigits=2,\
                                   ContentCentered=True,title=None):
        """
        shows the html version of the performance tableau in a browser window.
        """
        import webbrowser
        fileName = '/tmp/performanceTable.html'
        fo = open(fileName,'w')
        fo.write(self._htmlPerformanceTableau(actions=actionsSubset,\
                                             fromIndex=fromIndex,\
                                             toIndex=toIndex,\
                                             isSorted=isSorted,\
                                           Transposed=Transposed,\
                                           ndigits=ndigits,
                                           ContentCentered=ContentCentered,
                                           title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
           
            
    def _htmlPerformanceTableau(self,actions=None,\
                               fromIndex=None,\
                               toIndex=None,\
                               isSorted=False,\
                             Transposed=False,ndigits=2,\
                             ContentCentered=True,
                             title=None):
        """
        Renders the performance tableau citerion x actions in html format.
        """
        criteria = self.criteria
        minMaxEvaluations = self.computeMinMaxEvaluations()
        if title == None:
            html = '<h1>Performance table %s</h1>' % self.name
        else:
            html = '<h1>%s</h1>' % title            
        criteriaKeys = list(criteria.keys())
        if isSorted:
            criteriaKeys.sort()
        if actions == None:
            actions = self.actions
            actionsKeys = list(self.actions.keys())
        else:
            actionsKeys = [x for x in actions]
        if isSorted:
            actionsKeys.sort()
        evaluation = self.evaluation
        if ContentCentered:
            alignFormat = 'center'
        else:
            alignFormat = 'right'
        if Transposed:
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>criterion</th>'
            if fromIndex == None:
                fromIndex = 0
            if toIndex == None:
                toIndex = len(actionsKeys)
            for i in range(fromIndex,toIndex):
                x = actionsKeys[i]
                try:
                    xName = actions[x]['shortName']
                except:
                    xName = str(x)
                html += '<th bgcolor="#FFF79B">%s</th>' % (xName)
            html += '</tr>'
            for g in criteriaKeys:
                try:
                    gName = criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (gName)
                for x in actionsKeys:
                    if self.evaluation[g][x] != Decimal("-999"):
                        if minMaxEvaluations[g]['minimum'] == minMaxEvaluations[g]['maximum']:
                            formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        elif self.evaluation[g][x] == minMaxEvaluations[g]['minimum']:
                            formatString = '<td bgcolor="#ffddff"  align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        elif self.evaluation[g][x] == minMaxEvaluations[g]['maximum']:
                            formatString = '<td bgcolor="#ddffdd" align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        else:
                            formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                            
                    else:
                        html += '<td align="center"><span style="color: LightGrey;font-size:75%; ">NA</span></td>'
                html += '</tr>'
            html += '</table>'
        else:
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>criteria</th>'
            for g in criteriaKeys:
                try:
                    gName = criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<th bgcolor="#FFF79B">%s</th>' % (gName)
            html += '</tr>'
            html += '<tr bgcolor="#9acd32"><th>weight</th>'
            for g in criteriaKeys:
                gWeight = criteria[g]['weight']
                html += '<th bgcolor="#FFF79B">%.2f</th>' % (gWeight)
            html += '</tr>'
            if fromIndex == None:
                fromIndex = 0
            if toIndex == None:
                toIndex = len(actionsKeys)
            #for x in actionsKeys:
            for i in range(fromIndex,toIndex):
                x = actionsKeys[i]
                try:
                    xName = actions[x]['shortName']
                except:
                    xName = str(x)
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (xName)
                for g in criteriaKeys:
                    if self.criteria[g]['weight'] < Decimal('0'):
                        if self.evaluation[g][x] != Decimal("-999"):
                            if minMaxEvaluations[g]['minimum'] == minMaxEvaluations[g]['maximum']:
                                formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            elif self.evaluation[g][x] == minMaxEvaluations[g]['minimum']:
                                formatString = '<td bgcolor="#ddffdd"  align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            elif self.evaluation[g][x] == minMaxEvaluations[g]['maximum']:
                                formatString = '<td bgcolor="#ffddff" align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            else:
                                formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                        else:
                            html += '<td align="center"><span style="color: LightGrey;font-size:75%;">NA</span></td>'
                    else:
                        if self.evaluation[g][x] != Decimal("-999"):
                            if minMaxEvaluations[g]['minimum'] == minMaxEvaluations[g]['maximum']:
                                formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            elif self.evaluation[g][x] == minMaxEvaluations[g]['minimum']:
                                formatString = '<td bgcolor="#ffddff"  align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            elif self.evaluation[g][x] == minMaxEvaluations[g]['maximum']:
                                formatString = '<td bgcolor="#ddffdd" align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                            else:
                                formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                                html += formatString % (evaluation[g][x])
                        else:
                            html += '<td align="center"><span style="color: LightGrey;font-size:75%;">NA</span></td>'
                        
                html += '</tr>'
            html += '</table>'
            
        return html



##    # MCSR serialization added by Ian
##    def to_JSON(self):
##        """
##        Convert the performance table .__dict__ into a JSON string
##        """
##        return json.dumps(self.__dict__,sort_keys=True, indent=4, cls=_DecimalJSONEncoder)
##
##
########################################################################################################################
#######                                                showHTMLMCSRPerformanceTableau                             ######
#######                                                         START                                             ######
########################################################################################################################
##
##    def _showHTMLMCSRPerformanceTableau(self,ndigits=2,title='Min/Max Performance Tableau'):
##
##        """
##        Ask the server for an HTML representation of the performance tableau.
##
##        """
##        import gzip
##        RESTurl = "http://leopold-loewenheim.uni.lu/MCSR_REST_Service/Master_Thesis/performance_Tableau"
##        params = gzip.compress(json.dumps({'typeDict':self.to_JSON(),'precision':ndigits,'title':title}).encode('utf-8'))
##        jsonHeader = {'content-Type': 'application/json','content-Encoding': 'gzip'}
##
##        #urllib
##        import urllib.request
##        req = urllib.request.Request(url=RESTurl, data=params, headers=jsonHeader)
##        resp = urllib.request.urlopen(req)
##        data = resp.read()
##        htmlResp = data.decode('utf-8')
##
##        import tempfile
##        temp=tempfile.NamedTemporaryFile(mode='w+t',delete=False)
##        temp.write(htmlResp)
##        temp.seek(0)
##
##        from urllib.request import pathname2url
##        import os
##        filePath = 'file:{}'.format(pathname2url(os.path.abspath(temp.name)))
##
##        import webbrowser
##        webbrowser.open(filePath)
##
##        temp.close
###
########################################################################################################################
#######                                                showHTMLMCSRPerformanceTableau                              ######
#######                                                         END                                             ######
########################################################################################################################
##
##
##    # precision string needed to round decimals
##    def _calcPrecision(self,ndigits):
##        if(ndigits!=0):
##            precision='0.'
##        else:
##            precision='0'
##        for x in range(ndigits):
##            precision+='0'
##        return precision
##
##
########################################################################################################################
#######                                                computeMCSRPerformanceTableau                              ######
#######                                                         START                                             ######
########################################################################################################################
##    def _computeMCSRPerformanceTableau(self,isSorted=True,
##                               ndigits=2,title='Min/Max Performance Tableau',Debug=False):
##
##        """
##        Computes the performance table in a JSON compatible format with minima and maxima. Used by the Web API.
##
##        For a performance tableau with 5 criteria one obtains for instance
##        the following ordered dictionary in return::
##
##            OrderedDict([
##                ('title', 'Min/Max Performance Tableau'),
##                ('precision', 2),
##                ('criteriaList', OrderedDict([('0','g5'), ('1','g2'), ('2','g4'), ('3','g1'), ('4','g3')]),
##                ('quantiles', OrderedDict([
##                                           ('0',{'a1':OrderedDict([
##                                                             ('0',{'quantile':Decimal('3'), 'qantileClass':'minimum'}),
##                                                             ('1',{'quantile':Decimal('-17.92'), 'qantileClass':'default'}),
##                                                             ('2',{'quantile':Decimal('26.68'), 'qantileClass':'maximum'}),
##                                                             ('3',{'quantile':'NaN, 'qantileClass':'NaN'}),
##                                                             ('4',{'quantile':Decimal('-33.99'), 'qantileClass':'default'})
##                                           ])}),
##                                           ('1',{'a2':OrderedDict([
##                                                             ('0',{'quantile':Decimal('6'), 'qantileClass':'minimum'}),
##                                                             ('1',{'quantile':Decimal('-30.71'), 'qantileClass':'default'}),
##                                                             ('2',{'quantile':'NaN', 'qantileClass':'NaN'}),
##                                                             ('3',{'quantile':Decimal('8'), 'qantileClass':'maximum'}),
##                                                             ('4',{'quantile':Decimal('-77.77'), 'qantileClass':'default'})
##                                           ])}),
##                                           ('2', ...
##                ]))...
##            ]))
##
##        """
##
##        if Debug: print('/nSTART: computeMCSRPerformanceTableau')
##
##        from collections import OrderedDict
##        from decimal import Decimal
##        from digraphs import flatten
##        performanceTableau = {}
##        performanceTableau['title'] = title
##
##        min="minimum"
##        max="maximum"
##
##        minMaxEvaluations = self.computeMinMaxEvaluations()
##
##        performanceTableau["precision"] = ndigits
##
##        if Debug: print('/nSTART: Calculating criteria list')
##
##        #need a dict, but list(self.criteria) is not a dict
##        #therefore I need to construct criteriaList as a dict first
##        criteriaList = {}
##        tempCriteria= list(self.criteria)
##        if isSorted:
##            tempCriteria.sort()
##        for index,c in enumerate(tempCriteria):
##            criteriaList[str(index)] = c
##        criteriaList = OrderedDict(sorted(criteriaList.items(),key=lambda index: int(index[0])))
##
##        if Debug: print('/nDONE: Calculating criteria list')
##
##        performanceTableau["criteriaList"] = criteriaList
##
##        actionsList = list(self.actions)
##        if isSorted:
##            actionsList.sort()
##
##        precision = self._calcPrecision(ndigits)
##
##        if Debug: print('/nSTART: Calculating quantiles')
##
##        quantiles=OrderedDict()
##        for index, x in enumerate(actionsList):
##            quantiles[str(index)] = OrderedDict()
##            quantiles[str(index)][x] = {}
##            for gKey,gValue in criteriaList.items():
##                quantilexg = self.computeActionCriterionQuantile(x,gValue)
##                if quantilexg != 'NA':
##                    quantile=self.evaluation[gValue][x]
##                    constantQuantile = (minMaxEvaluations[gValue]['minimum'] == minMaxEvaluations[gValue]['maximum'])
##                    if quantile != Decimal("-999"):
##                        if ((quantile == minMaxEvaluations[gValue]['minimum']) and (not constantQuantile)):
##                            quantiles[str(index)][x][gKey]={'quantile':quantile.quantize(Decimal(precision),rounding=decimal.ROUND_DOWN),
##                                                            'quantileClass':min}
##                        elif ((quantile == minMaxEvaluations[gValue]['maximum']) and (not constantQuantile)):
##                            quantiles[str(index)][x][gKey]={'quantile':quantile.quantize(Decimal(precision),rounding=decimal.ROUND_DOWN),
##                                                            'quantileClass':max}
##                        else:
##                            quantiles[str(index)][x][gKey]={'quantile':quantile.quantize(Decimal(precision),rounding=decimal.ROUND_DOWN),
##                                                            'quantileClass':"default"}
##
##                else:
##                    quantiles[str(index)][x][gKey]={'quantile':"NaN",
##                                                            'quantileClass':"NaN"}
##                    # break
##            quantiles[str(index)]={x:OrderedDict(sorted(quantiles[str(index)][x].items(),key=lambda index: int(index[0])))}
##
##        if Debug: print('/nDONE: Calculating quantiles')
##
##        quantiles=OrderedDict(sorted(quantiles.items(),key=lambda index: int(index[0])))
##        performanceTableau['quantiles'] = quantiles
##
##        if Debug: print('/nDONE: computeMCSRPerformanceTableau')
##
##        return performanceTableau
##
########################################################################################################################
#######                                                computeMCSRPerformanceTableau                            ######
#######                                                         END                                             ######
########################################################################################################################
##
##
########################################################################################################################
#######                                                computeMCSRPerformanceHeatmap                              ######
#######                                                         START                                             ######
########################################################################################################################
##    def _computeMCSRPerformanceHeatmap(self,criteriaList=None,
##                               actionsList=None,
##                               ndigits=2,
##                               colorLevels=7,
##                               Ranked=True,
##                               title='Performance Heatmap',
##                               Correlations=False,
##                               Threading=False,
##                               Debug=False):
##        """
##        Computes the Brewer RdYlGn colored heatmap of the performance table
##        actions x criteria in ordered dictionary format. Three color levels (5,7 or 9)
##        are provided. Used by the Web API.
##
##        For a performance tableau with 5 criteria, colorLevels=5 and
##        Correlations = True, one obtains for instance
##        the following ordered dictionary in return::
##
##            OrderedDict([
##                ('title', 'Performance Heatmap'),
##                ('precision', 2),
##                ('colorPalette', OrderedDict([
##                                  ('0',{'quantile':Decimal('0.2'),'quantileClass':'q5_1'}),
##                                  ('1',{'quantile':Decimal('0.4'),'quantileClass':'q5_2'}),
##                                  ('2',{'quantile':Decimal('0.6'),'quantileClass':'q5_3'}),
##                                  ('3',{'quantile':Decimal('0.8'),'quantileClass':'q5_4'}),
##                                  ('4',{'quantile':Decimal('1.0'),'quantileClass':'q5_5'})
##                ])),
##                ('criteriaList', OrderedDict([('0','g5'), ('1','g2'), ('2','g4'), ('3','g1'), ('4','g3')]),
##                ('criteriaCorrelations', OrderedDict([
##                                                     ('0',Decimal('0.71428')),
##                                                     ('1',Decimal('0.48571')),
##                                                     ('2',Decimal('0.40952')),
##                                                     ('3',Decimal('0.35238')),
##                                                     ('4',Decimal('0.16190'))
##                ])),
##                ('quantiles', OrderedDict([
##                                           ('0',{'a1':OrderedDict([
##                                                             ('0',{'quantile':Decimal('3'), 'qantileClass':'q5-2'}),
##                                                             ('1',{'quantile':Decimal('-17.92'), 'qantileClass':'q5-5'}),
##                                                             ('2',{'quantile':Decimal('26.68'), 'qantileClass':'q5-2'}),
##                                                             ('3',{'quantile':Decimal('1'), 'qantileClass':'q5-1'}),
##                                                             ('4',{'quantile':Decimal('-33.99'), 'qantileClass':'q5-3'})
##                                           ])}),
##                                           ('1',{'a2':OrderedDict([
##                                                             ('0',{'quantile':Decimal('6'), 'qantileClass':'q5-3'}),
##                                                             ('1',{'quantile':Decimal('-30.71'), 'qantileClass':'q5-5'}),
##                                                             ('2',{'quantile':Decimal('66.35'), 'qantileClass':'q5-4'}),
##                                                             ('3',{'quantile':Decimal('8'), 'qantileClass':'q5-5'}),
##                                                             ('4',{'quantile':Decimal('-77.77'), 'qantileClass':'q5-3'})
##                                           ])}),
##                                           ('2', ...
##                ]))...
##            ]))
##
##        """
##        if Debug: print('/nSTART: computeMCSRPerformanceHeatmap')
##
##        from collections import OrderedDict
##        from decimal import Decimal
##        from digraphs import flatten
##        heatmap = OrderedDict()
##        heatmap['title'] = title
##
##        heatmap["precision"] = ndigits
##
##        brewerRdYlGn9Colors = {'0':{'quantile':Decimal('0.1111'),'quantileClass':"q9_1"},
##                               '1':{'quantile':Decimal('0.2222'),'quantileClass':"q9_2"},
##                               '2':{'quantile':Decimal('0.3333'),'quantileClass':"q9_3"},
##                               '3':{'quantile':Decimal('0.4444'),'quantileClass':"q9_4"},
##                               '4':{'quantile':Decimal('0.5555'),'quantileClass':"q9_5"},
##                               '5':{'quantile':Decimal('0.6666'),'quantileClass':"q9_6"},
##                               '6':{'quantile':Decimal('0.7777'),'quantileClass':"q9_7"},
##                               '7':{'quantile':Decimal('0.8888'),'quantileClass':"q9_8"},
##                               '8':{'quantile':Decimal('1.0000'),'quantileClass':"q9_9"}
##                               }
##
##        brewerRdYlGn7Colors = {'0':{'quantile':Decimal('0.1429'),'quantileClass':'q7_1'},
##                               '1':{'quantile':Decimal('0.2857'),'quantileClass':'q7_2'},
##                               '2':{'quantile':Decimal('0.4286'),'quantileClass':'q7_3'},
##                               '3':{'quantile':Decimal('0.5714'),'quantileClass':'q7_4'},
##                               '4':{'quantile':Decimal('0.7143'),'quantileClass':'q7_5'},
##                               '5':{'quantile':Decimal('0.8571'),'quantileClass':'q7_6'},
##                               '6':{'quantile':Decimal('1.0000'),'quantileClass':'q7_7'}
##        }
##
##        brewerRdYlGn5Colors = {'0':{'quantile':Decimal('0.2'),'quantileClass':'q5_1'},
##                               '1':{'quantile':Decimal('0.4'),'quantileClass':'q5_2'},
##                               '2':{'quantile':Decimal('0.6'),'quantileClass':'q5_3'},
##                               '3':{'quantile':Decimal('0.8'),'quantileClass':'q5_4'},
##                               '4':{'quantile':Decimal('1.0'),'quantileClass':'q5_5'}
##        }
##
##        if colorLevels == 7:
##            colorPalette = brewerRdYlGn7Colors
##        elif colorLevels == 9:
##            colorPalette = brewerRdYlGn9Colors
##        elif colorLevels == 5:
##            colorPalette = brewerRdYlGn5Colors
##        else:
##            colorPalette = brewerRdYlGn7Colors
##
##        colorPalette = OrderedDict(sorted(colorPalette.items()))
##        heatmap['colorPalette'] = colorPalette
##
##        nc = len(colorPalette)
##
##        if Debug: print('/nSTART: Calculating action list')
##
##        if Ranked and actionsList == None:
##            # from weakOrders import QuantilesRankingDigraph
##            # qsr = QuantilesRankingDigraph(self,LowerClosed=True,
##            #                               Threading=Threading,
##            #                               Debug=Debug)
##            # actionsList = [x for x in flatten(qsr.computeQsRbcRanking())]
##            from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
##            prg = PreRankedOutrankingDigraph(self,LowerClosed=True,
##                                             Threading=Threading,Debug=Debug)
##            actionsList = prg.computeBoostedRanking()
##        else:
##            if actionsList == None:
##                actionsList = list(self.actions.keys())
##                actionsList.sort()
##
##        if Debug: print('/nDONE: Calculating action list')
##
##        if Debug: print('/nSTART: Calculating criteria list and correlations/weights')
##
##        if criteriaList == None:
##            from outrankingDigraphs import OutrankingDigraph
##            if Correlations:
##                criteriaCorrelations = OutrankingDigraph.showMarginalVersusGlobalOutrankingCorrelation(
##                    qsr,
##                    Threading=Threading,
##                    Comments=False)
##                criteriaList={}
##                correlations={}
##
##                criteriaWeightsList = [(self.criteria[g]['weight'],g) for g in self.criteria.keys()]
##                criteriaWeightsList.sort(reverse=True)
##
##                criteriaWeights={}
##                for index,c in enumerate(criteriaCorrelations):
##                    criteriaList[str(index)]=c[1]
##                    correlations[str(index)]=c[0]
##                    for indexW,g in enumerate(criteriaWeightsList):
##                     if (g[1]==c[1]):
##                         criteriaWeights[str(index)]=g[0]
##                         break
##            else:
##                criteriaWeightsList = [(self.criteria[g]['weight'],g) for g in self.criteria.keys()]
##                criteriaWeightsList.sort(reverse=True)
##                criteriaList={}
##                criteriaWeights={}
##                for index,g in enumerate(criteriaWeightsList):
##                    criteriaList[str(index)]=g[1]
##                    criteriaWeights[str(index)]=g[0]
##
##                criteriaCorrelations = None
##        else:
##            criteriaCorrelations = None
##
##        if Debug: print('/nDONE: Calculating criteria list and correlations/weights')
##
##        criteriaList= OrderedDict(sorted(criteriaList.items(),key=lambda index: int(index[0])))
##        heatmap['criteriaList'] = criteriaList
##
##        if criteriaCorrelations != None:
##            correlations= OrderedDict(sorted(correlations.items(),key=lambda index: int(index[0])))
##            heatmap['criteriaCorrelations'] = correlations
##
##            criteriaWeights= OrderedDict(sorted(criteriaWeights.items(),key=lambda index: int(index[0])))
##            heatmap['criteriaWeights'] = criteriaWeights
##        else:
##            criteriaWeights= OrderedDict(sorted(criteriaWeights.items(),key=lambda index: int(index[0])))
##            heatmap['criteriaWeights'] = criteriaWeights
##
##        precision = self._calcPrecision(ndigits)
##
##        if Debug: print('/nSTART: Calculating quantiles')
##
##        quantiles=OrderedDict()
##        for index, x in enumerate(actionsList):
##            quantiles[str(index)] = OrderedDict()
##            quantiles[str(index)][x] = {}
##            for gKey,gValue in criteriaList.items():
##                quantilexg = self.computeActionCriterionQuantile(x,gValue)
##                if Debug:
##                    print(x,gValue,quantilexg)
##                if quantilexg != 'NA':
##                    for i in range(nc):
##                        if Debug:
##                            print(i, colorPalette[str(i)]['quantile'])
##
##                        if quantilexg <= colorPalette[str(i)]['quantile']:
##                            quantiles[str(index)][x][gKey]={'quantile':self.evaluation[gValue][x].quantize(Decimal(precision),rounding=decimal.ROUND_DOWN),
##                                             'quantileClass':colorPalette[str(i)]['quantileClass']}
##                            break
##                else:
##                    quantiles[str(index)][x][gKey]={'quantile':"NaN",
##                                             'quantileClass':"NaN"}
##                if Debug:
##                    print(x,gValue,quantiles[index][x][gValue])
##            quantiles[str(index)]={x:OrderedDict(sorted(quantiles[str(index)][x].items(),key=lambda index: int(index[0])))}
##
##        if Debug: print('/nSTART: Calculating quantiles')
##
##
##        heatmap['quantiles'] = OrderedDict(sorted(quantiles.items(),key=lambda index: int(index[0])))
##
##        if Debug: print('/nDONE: computeMCSRPerformanceHeatmap')
##        return heatmap 
##
########################################################################################################################
#######                                                computeMCSRPerformanceHeatmap                            ######
#######                                                         END                                             ######
########################################################################################################################

    def showHTMLPerformanceHeatmap(self,actionsList=None,\
                                   fromIndex=None,\
                                   toIndex=None,\
                                   criteriaList=None,\
                                   colorLevels=7,\
                                   pageTitle=None,\
                                   ndigits=2,\
                                   SparseModel=False,\
                                   minimalComponentSize=1,\
                                   rankingRule='Copeland',\
                                   quantiles=None,\
                                   strategy='average',\
                                   Correlations=False,\
                                   Threading=False,\
                                   nbrOfCPUs=None,\
                                   Debug=False):
        """
        shows the html heatmap version of the performance tableau in a browser window
        (see perfTabs.htmlPerformanceHeatMap() method ).

        **Parameters**:

              - *actionsList* and *criteriaList*, if provided,  give the possibility to show the decision alternatives, resp. criteria, in a given ordering.
              - *ndigits* = 0 may be used to show integer evaluation values.
              - If no *actionsList* is provided, the decision actions are ordered from the best to the worst. This
                ranking is obtained by default with the Copeland rule applied on a standard *BipolarOutrankingDigraph*.
                When the *SparseModel* flag is put to *True*, a sparse *PreRankedOutrankingDigraph* construction is used instead.                
              - The *minimalComponentSize* allows to control the fill rate of the pre-ranked model.
                If *minimalComponentSize* = *n* (the number of decision actions) both the pre-ranked model will be
                in fact equivalent to the standard model.
              - It may interesting in some cases to use *rankingRule* = 'NetFlows'.
              - Quantiles used for the pre-ranked decomposition are put by default to *n*
                (the number of decision alternatives) for *n* < 50. For larger cardinalities up to 1000, quantiles = *n* /10.
                For bigger performance tableaux the *quantiles* parameter may be set to a much lower value
                not exceeding usually 1000.
              - The pre-ranking may be obtained with three ordering strategies for the
                quantiles equivalence classes: 'average' (default), 'optimistic' or  'pessimistic'.
              - With *Correlations* = *True* and *criteriaList* = *None*, the criteria will be presented from left to right in decreasing
                order of the correlations between the marginal criterion based ranking and the global ranking used for
                presenting the decision alternatives.
              - For large performance Tableaux, *multiprocessing* techniques may be used by setting
                *Threading* = *True* in order to speed up the computations; especially when *Correlations* = *True*.
              - By default, the number of cores available, will be detected. It may be efficient in a HPC context
                to indicate the exact number of singled threaded cores in fact allocated to the job.


        >>> from randomPerfTabs import RandomPerformanceTableau
        >>> rt = RandomPerformanceTableau(seed=100)
        >>> rt.showHTMLPerformanceHeatmap(colorLevels=5,Correlations=True)

        .. image:: perfTabsExample.png
           :alt: HTML heat map of the performance tableau
           :width: 600 px
           :align: center
        
        """
        import webbrowser
        fileName = '/tmp/performanceHeatmap.html'
        fo = open(fileName,'w')
        if pageTitle == None:
            pageTitle = 'Heatmap of Performance Tableau \'%s\'' % self.name
            
        fo.write(self._htmlPerformanceHeatmap(argCriteriaList=criteriaList,
                                             argActionsList=actionsList,
                                             fromIndex=fromIndex,
                                             toIndex=toIndex,
                                             SparseModel=SparseModel,
                                             minimalComponentSize=minimalComponentSize,
                                             rankingRule=rankingRule,
                                             quantiles=quantiles,
                                             strategy=strategy,
                                             ndigits=ndigits,
                                             colorLevels=colorLevels,
                                             pageTitle=pageTitle,
                                             Correlations=Correlations,
                                             Threading=Threading,
                                             nbrOfCPUs=1,
                                             Debug=Debug))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)

    def _htmlPerformanceHeatmap(self,argCriteriaList=None,
                               argActionsList=None,
                               fromIndex=None,
                               toIndex=None,
                               SparseModel=False,
                               minimalComponentSize=1,
                               rankingRule='Copeland',
                               quantiles=None,
                               strategy='average',
                               ndigits=2,
                               ContentCentered=True,
                               colorLevels=None,
                               pageTitle='Performance Heatmap',
                               Correlations=False,
                               Threading=False,
                               nbrOfCPUs=1,
                               Debug=False):
        """       
        Renders the Brewer RdYlGn 5,7, or 9 levels colored heatmap of the performance table
        actions x criteria in html format.

        See the corresponding perfTabs.showHTMLPerformanceHeatMap() method.
        """
        from decimal import Decimal
                    
        brewerRdYlGn9Colors = [(Decimal('0.1111'),'"#D53E4F"'),
                               (Decimal('0.2222'),'"#F46D43"'),
                               (Decimal('0.3333'),'"#FDAE61"'),
                               (Decimal('0.4444'),'"#FEE08B"'),
                               (Decimal('0.5555'),'"#FFFFBF"'),
                               (Decimal('0.6666'),'"#D9EF8B"'),
                               (Decimal('0.7777'),'"#A6D96A"'),
                               (Decimal('0.8888'),'"#65BD63"'),
                               (Decimal('1.000'),'"#1A9850"')]
        brewerRdYlGn7Colors = [
                               (Decimal('0.1429'),'"#F46D43"'),
                               (Decimal('0.2857'),'"#FDAE61"'),
                               (Decimal('0.4286'),'"#FEE08B"'),
                               (Decimal('0.5714'),'"#FFFFBF"'),
                               (Decimal('0.7143'),'"#D9EF8B"'),
                               (Decimal('0.8571'),'"#A6D96A"'),
                               (Decimal('1.0000'),'"#65BD63"')
                               ]
        brewerRdYlGn5Colors = [
                               (Decimal('0.2'),'"#FDAE61"'),
                               (Decimal('0.4'),'"#FEE08B"'),
                               (Decimal('0.6'),'"#FFFFBF"'),
                               (Decimal('0.8'),'"#D9EF8B"'),
                               (Decimal('1.0'),'"#A6D96A"')
                               ]
        if colorLevels == None:
            colorLevels = 7
        if colorLevels == 7:
            colorPalette = brewerRdYlGn7Colors
        elif colorLevels == 9:
            colorPalette = brewerRdYlGn9Colors
        elif colorLevels == 5:
            colorPalette = brewerRdYlGn5Colors
        else:
            colorPalette = brewerRdYlGn7Colors
        nc = len(colorPalette)
        backGroundColor   = '"#FFFFFF"'
        naColor           = '"#FFFFFF"'
        columnHeaderColor = '"#CCFFFF"'
        rowHeaderColor    = '"#FFFFFF"'

        html = '<!DOCTYPE html><html><head>\n'
        html += '<title>%s</title>\n' % 'Digraph3 performance heat map'
        html += '<style type="text/css">\n'
        #html += 'table {border-collapse: collapse;}'
        if ContentCentered:
            html += 'td {text-align: center;}\n'
        html += 'td.na {color: rgb(192,192,192);}\n'
        html += '</style>\n'
        html += '</head>\n<body>\n'
        html += '<h2>%s</h2>\n' % pageTitle
        
        if argCriteriaList == None:
            argCriteriaList = list(self.criteria.keys())
            criteriaList = None
        else:
            criteriaList = argCriteriaList

        if argActionsList == None: # actions ranking is needed
            if rankingRule == None:
                rankingRule = 'Copeland'
            
            na = len(self.actions)
            if SparseModel:
                from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
                if quantiles == None:
                    if na < 100:
                        q = 5
                    else:
                        q = None
                else:
                    q = quantiles
                g = PreRankedOutrankingDigraph(self,quantiles=q,LowerClosed=False,
                                               minimalComponentSize=minimalComponentSize,
                                           componentRankingRule=rankingRule,Threading=Threading,
                                           nbrOfCPUs=nbrOfCPUs)
                actionsList = g.boostedRanking
                
            else: # standard outranking model
                from outrankingDigraphs import BipolarOutrankingDigraph
                g = BipolarOutrankingDigraph(self,actionsSubset=argActionsList,Normalized=True)
                if rankingRule == 'NetFlows':
                    actionsList = g.computeNetFlowsRanking()
                elif rankingRule == 'Kohler':
                    actionsList = g.computeKohlerRanking()
                elif rankingRule == 'RankedPairs':
                    from linearOrders import RankedPairsOrder
                    rp = RankedPairsOrder(g)
                    actionsList = rp.computeRanking()
                elif rankingRule == 'ArrowRaynaud':
                    actionsList = g.computeArrowRaynaudRanking()
                else: # default ranking rule
                    actionsList = g.computeCopelandRanking()

            if SparseModel:
                rankCorrelation = None
            else:
                rankCorrelation = g.computeOrderCorrelation(list(reversed(actionsList)))
            if Debug:
                print('1',actionsList)
                print('2',rankCorrelation)
        else:  # actions list given
            actionsList = argActionsList
            Correlations = False
            rankCorrelation = None
            
        ##########
        criteria = self.criteria
        if criteriaList == None:
            if Correlations:
                criteriaCorrelation =\
                        g.computeMarginalVersusGlobalRankingCorrelations(\
                                actionsList,ValuedCorrelation=True,Threading=Threading,
                                nbrCores=nbrOfCPUs)
                criteriaList = [c[1] for c in criteriaCorrelation]
            else:
                criteriaList = list(criteria.keys())
                criteriaList.sort()
                criteriaWeightsList = [(-criteria[g]['weight'],g) for g in criteriaList]
                criteriaWeightsList.sort(reverse=False)
                criteriaList = [g[1] for g in criteriaWeightsList]
                criteriaCorrelation = None
        else:
            criteriaList = list(criteria.keys())
            if argActionsList != None:
                Correlations = False
            if Correlations:
                criteriaCorrelation =\
                        g.computeMarginalVersusGlobalRankingCorrelations(\
                                actionsList,ValuedCorrelation=True,Threading=Threading,
                                nbrCores=nbrOfCPUs)
            else:
                criteriaCorrelation = None
        quantileColor={}
        for x in actionsList:
            quantileColor[x] = {}
            for g in criteriaList:
                quantilexg = self.computeActionCriterionQuantile(x,g)
                if Debug:
                    print(x,g,quantilexg)
                if quantilexg != 'NA':
                    if self.criteria[g]['weight'] > Decimal('0.0'):
                        for i in range(nc):
                            if Debug:
                                print(i, colorPalette[i][0])

                            if quantilexg <= colorPalette[i][0]:
                                quantileColor[x][g] = colorPalette[i][1]
                                break
                    else: # negative weight and reversed quatile coloring
                        for i in range(nc):
                            if Debug:
                                print(i, colorPalette[nc-i-1][0])

                            if quantilexg <= colorPalette[i][0]:
                                quantileColor[x][g] = colorPalette[nc-i-1][1]
                                break        
                else:
                    quantileColor[x][g] = naColor
                if Debug:
                    print(x,g,quantileColor[x][g])
        # legend            
##        html += '<i>Color legend: </i>\n'
##        html += '<table style="background-color:%s; border-collapse: collapse;" border="1">\n' % (backGroundColor) 
##        html += '<tr bgcolor=%s><th>quantile</th>' % (columnHeaderColor)
##        for col in range(nc):
##            html += '<td bgcolor=%s>%s</td>' % (colorPalette[col][1],str(colorPalette[col][0]))
##        html += '</tr>\n'
##        html += '</table>\n'
        # heatmap
        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor) 
        html += '<tr bgcolor=%s><th>criteria</th>' % (columnHeaderColor)
        for g in criteriaList:
            try:
                gName = self.criteria[g]['shortName']
            except:
                gName = str(g)
            html += '<th>%s</th>' % (gName)
        html += '</tr>\n'
        html += '<tr><th bgcolor=%s>weights</th>' % (columnHeaderColor)
        for g in criteriaList:
            html += '<td align="center">%+.2f</td>' % (self.criteria[g]['weight'])
        html += '</tr>\n'
        if criteriaCorrelation != None:
            html += '<tr><th bgcolor=%s>tau<sup>(*)</sup></th>' % (columnHeaderColor)
            for cg in criteriaCorrelation:
                html += '<td align="center">%+.2f</td>' % (cg[0])
            html += '</tr>\n'
        if Debug:
            print(html)
        if fromIndex == None:
            fromIndex=0
        if toIndex == None:
            toIndex = len(actionsList)
        for i in range(fromIndex,toIndex):
            x = actionsList[i]
            try:
                xName = self.actions[x]['shortName']
            except:
                xName = str(x)
            html += '<tr><th bgcolor=%s>%s</th>' % (rowHeaderColor,xName)
            for g in criteriaList:
                if self.evaluation[g][x] != Decimal("-999"):
                    formatString = '<td bgcolor=%s align="right">%% .%df</td>' % (quantileColor[x][g],ndigits)
                    html += formatString % (self.evaluation[g][x])
                else:
                    html += '<td bgcolor=%s class="na">NA</td>' % naColor
                if Debug:
                    print(html)
            html += '</tr>\n'
        html += '</table>\n'
        # legend
        html += '<i>Color legend: </i>\n'
        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor) 
        html += '<tr bgcolor=%s><th>quantile</th>' % (columnHeaderColor)
        #html += '<td bgcolor=%s>&nbsp;[%.2f - %.2f[&nbsp;</td>' % (colorPalette[0][1],0.0,colorPalette[0][0])
        for col in range(0,nc):
            html += '<td bgcolor=%s>&nbsp;%.2f&#037;</td>' % (colorPalette[col][1],
                                                                   #colorPalette[col-1][0],
                                                                   colorPalette[col][0]*Decimal('100.0'))
        html += '</tr>\n'
        html += '</table>\n'
        if criteriaCorrelation != None:
            html += '<b>(*) tau:</b> <i>Ordinal (Kendall) correlation between marginal criterion and global ranking relation</i><br/>\n'
        if rankCorrelation != None:
            html += '<i>Ranking rule</i>: <b>%s</b><br/>\n' % rankingRule
            html += '<i>Ordinal (Kendall) correlation between global ranking and global outranking relation:</i> <b>%+.3f</b><br/>\n' % (rankCorrelation['correlation'])
            html += '</body></html>'
        return html

    def computeWeightPreorder(self):
        """
        renders the weight preorder following from the given
        criteria weights in a list of increasing equivalence
        lists of criteria. 
        """
        try:
            return self.weightorder
        except:
            pass
        criteria = self.criteria
        # generate weightslist
        weightslist = []
        for g in criteria:
            weightslist.append((abs(criteria[g]['weight']),g))
        weightslist.sort()
        # generate weightPreorder
        weightPreorder = []
        cur = 0
        i = 0
        weightclass = []
        for i in range(len(weightslist)):
            if weightslist[i][0] == weightslist[cur][0]:
                weightclass.append(weightslist[i][1])
            else:
                cur = i
                weightPreorder.append(weightclass)
                weightclass = [weightslist[i][1]]
            i += 1        
        weightPreorder.append(weightclass)
        return weightPreorder
   
    def showAll(self):
        """
        Show fonction for performance tableau
        """
        criteria = self.criteria
        evaluation = self.evaluation
        print('*-------- show performance tableau -------*')
        print('Name         :', self.name)
        print('Actions      :', self.actions)
        print('Criteria     :')       
        for g in criteria:
            print(' criterion name        :', g)
            print('   scale: ', criteria[g]['scale'], end=' ')
            print(', weight: %.3f ' % (criteria[g]['weight']), end=' ')
            try:
                print('   thresholds:', criteria[g]['thresholds'])
            except:
                pass
            print()
        print('Weights preorder :', self.weightPreorder)
        print('Evaluations      :')
        for g in evaluation:
            print(g, evaluation[g])

    def showEvaluationStatistics(self):
        """
        renders the variance and standard deviation of
        the values observed in the performance Tableau.
        """
        import math
        from decimal import Decimal
        
        print('*---- Evaluation statistics ----*')
        average = Decimal('0.0')
        n = Decimal('0.0')
        for g in self.criteria:
            for x in self.actions:
                average += self.evaluation[g][x]
                n += 1
        average = average/n
        print('average      : %2.2f ' % (average))
        variance = Decimal('0.0')
        for g in self.criteria:
            for x in self.actions:
                variance += (self.evaluation[g][x]-average)*(self.evaluation[g][x]-average)
        variance = variance/n
        print('variance     : %2.2f ' % (variance))
        stddev = math.sqrt(variance)
        print('std deviation: %2.2f ' % (stddev))      

    def save(self,fileName='tempperftab',isDecimal=True,valueDigits=2):
        """
        Persistant storage of Performance Tableaux.
        """
        print('*--- Saving performance tableau in file: <' + str(fileName) + '.py> ---*')
        actions = self.actions
        try:
            objectives = self.objectives
        except:
            objectives = {}
        criteria = self.criteria
        evaluation = self.evaluation
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved performance Tableau: \n')
        fo.write('from decimal import Decimal\n')
        fo.write('from collections import OrderedDict\n')
        # actions
        fo.write('actions = OrderedDict([\n')
        for x in actions:
            fo.write('(\'%s\', {\n' % str(x))
            for it in self.actions[x].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.actions[x][it])) )
            fo.write('}),\n')
##            try:
##                xnameString = actions[x]['name']
##            except:
##                xnameString = str(x)
##            try:
##                xcommentString = actions[x]['comment']
##            except:
##                xcommentString = ''
##            fo.write('(\'%s\', {\'name\': \'%s\',\'comment\':\'%s\'}),\n' %(x,xnameString,xcommentString))
##            
        fo.write('])\n')
        # objectives
        fo.write('objectives = OrderedDict([\n')
        for obj in objectives:
            fo.write('(\'%s\', {\n' % str(obj))
            for it in self.objectives[obj].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.objectives[obj][it])))
            fo.write('}),\n')
##            fo.write( '(\'%s\', {\'name\': \'%s\',\n' % (obj,objectives[obj]['name']) )
##            weightString = '%%.%df' % (valueDigits)
##            objString = '\'criteria\': %s, \'weight\':'+weightString+'}),\n'
##            fo.write(objString % (objectives[obj]['criteria'],\
##                                                                objectives[obj]['weight']))  
        fo.write('])\n')            
        # criteria
        fo.write('criteria = OrderedDict([\n') 
        for g in criteria:
            fo.write('(\'%s\', {\n' % str(g))
            for it in self.criteria[g].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.criteria[g][it])))
            fo.write('}),\n')
##            fo.write('(\'' +str(g)+'\', {\n')
##            try:
##                fo.write('\'name\': \'%s\',\n' % criteria[g]['name']) 
##            except:
##                pass
##            try:
##                fo.write('\'objective\': \'%s\',\n' % criteria[g]['objective']) 
##            except:
##                pass
            
##            if isDecimal:
##                #fo.write('\'weight\':Decimal("'+str(criteria[g]['weight'])+'"),\'scale\': (Decimal("'+str(criteria[g]['scale'][0])+'"),Decimal("'+str(criteria[g]['scale'][1])+'")),\n')
##                #fo.write('\'thresholds\' :' + str(criteria[g]['thresholds']) + '},\n')
##                weightScaleString = '\'weight\':Decimal("%%.%df"),\'scale\': (Decimal("%%.%df"),Decimal("%%.%df")),\n' % (valueDigits,valueDigits,valueDigits)
##                fo.write(weightScaleString % (criteria[g]['weight'],criteria[g]['scale'][0],criteria[g]['scale'][1]))
##                try:
##                    fo.write('\'thresholds\' : %s }),\n' % ( str(criteria[g]['thresholds']) ) )
##                except:
##                    fo.write('}),\n')
##            else:
##                fo.write('\'weight\':'+str(criteria[g]['weight'])+',\'scale\':'+str(criteria[g]['scale'])+',\n')
##                try:
##                    fo.write('\'thresholds\' :' + str(criteria[g]['thresholds']) + '}),\n')
##                except:
##                    fo.write('}),\n')
##            
        fo.write('])\n')
        # evaluation
        fo.write('evaluation = {\n')
        for g in criteria:
            fo.write('\'' +str(g)+'\': {\n')
            for x in actions:
                if Decimal:
                    #fo.write('\'' + str(x) + '\':Decimal("' + str(evaluation[g][x]) + '"),\n')
                    evaluationString = '\'%%s\':Decimal("%%.%df"),\n' % (valueDigits)
                    fo.write(evaluationString % (x,evaluation[g][x]) )
                else:
                    fo.write('\'' + str(x) + '\':' + str(evaluation[g][x]) + ',\n')
                    
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()

    def saveXML(self,name='temp',category='standard',subcategory='standard',author='digraphs Module (RB)',reference='saved from Python'):
        """
        save temporary performance tableau self in XML format.
        """
        print('*----- saving performance tableau in XML format  -------------*')        
        nameExt = name+'.xml'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="performanceTableau.xsl"?>\n')
        fo.write('<!DOCTYPE digraph SYSTEM "digraphs.dtd">\n')
        fo.write('<performancetableau ')
        fo.write('category="'+str(category)+'" subcategory="'+str(subcategory)+'">\n')
        fo.write('<header>\n')
        fo.write('<name>')
        fo.write(nameExt)
        fo.write('</name>\n')       
        fo.write('<author>')
        fo.write(author)
        fo.write('</author>\n')
        fo.write('<reference>')
        fo.write(reference)
        fo.write('</reference>\n')
        fo.write('</header>')
        listActions = list(self.actions)
        listActions.sort()
        na = len(listActions)
        fo.write('<actions>\n')
        for i in range(na):
            fo.write('<action>')
            fo.write(str(listActions[i]))
            fo.write('</action>\n')
        fo.write('</actions>\n')
        criteria = self.criteria
        fo.write('<criteria>\n')
        for g in criteria:
            fo.write('<criterion>\n')
            fo.write('<critname>'+str(g)+'</critname>\n')
            fo.write('<scale>\n')
            fo.write('<min>'+str(criteria[g]['scale'][0])+'</min>\n')
            fo.write('<max>'+str(criteria[g]['scale'][1])+'</max>\n')
            fo.write('</scale>\n')
            fo.write('<thresholds>\n')
            fo.write('<indifference>'+str(criteria[g]['thresholds']['ind'])+'</indifference>\n')
            fo.write('<preference>'+str(criteria[g]['thresholds']['pref'])+'</preference>\n')
            try:
                fo.write('<weakVeto>'+str(criteria[g]['thresholds']['weakVeto'])+'</weakVeto>\n')
            except:
                pass
            fo.write('<veto>'+str(criteria[g]['thresholds']['veto'])+'</veto>\n')
            fo.write('</thresholds>\n')
            #fo.write('<weight>'+str(criteria[g]['weight'])+'</weight>\n')
            fo.write('<weight>%.3f</weight>\n' % (criteria[g]['weight']) )
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')
        evaluation = self.evaluation
        fo.write('<evaluations>\n')
        for g in criteria:
            fo.write('<evaluation>\n')
            fo.write('<critname>'+str(g)+'</critname>\n')
            for i in range(na):
                fo.write('<evalactions>\n')
                fo.write('<action>')       
                fo.write(str(listActions[i]))
                fo.write('</action>\n')                    
                fo.write('<value>')
                fo.write(str(evaluation[g][listActions[i]]))
                fo.write('</value>\n')
                fo.write('</evalactions>\n')
            fo.write('</evaluation>\n')        
        fo.write('</evaluations>\n')        
        fo.write('</performancetableau>\n')         
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMLRubis(self,name='temp',category='Rubis',subcategory='new D2 version',author='digraphs Module (RB)',reference='saved from Python'):
        """
        save temporary performance tableau self in XML Rubis format.
        """
        import codecs
        print('*----- saving performance tableau in XML Rubis format  -------------*')        
        nameExt = name+'.xml'
        fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="rubisPerformanceTableau.xsl"?>\n')
        #fo.write('<!DOCTYPE rubisPerformaceTableau SYSTEM "http://localhost/rubisServer/Schemas/rubisPerformanceTableau-1.0/rubisPerformanceTableau.dtd">\n')
        fo.write('<rubisPerformanceTableau xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="rubisPerformanceTableau.xsd" ')
        fo.write('category="'+str(category)+'" subcategory="'+str(subcategory)+'">\n')
        fo.write('<comment>Performance Tableau in XML Rubis format.</comment>\n')
        fo.write('<header>\n')
        fo.write('<name>')
        fo.write(nameExt)
        fo.write('</name>\n')       
        fo.write('<author>')
        fo.write(author)
        fo.write('</author>\n')
        fo.write('<reference>')
        fo.write(reference)
        fo.write('</reference>\n')
        fo.write('</header>\n')
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<actions>\n')
        fo.write('<comment>Potential decision actions.</comment>\n')
        for i in range(na):
            fo.write('<action id="%s">\n' % (actionsList[i]))
            fo.write('<name>')
            try:
                fo.write(str(actions[actionsList[i]]['name']))
            except:
                pass
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                pass
            fo.write('</comment>\n')
            fo.write('</action>\n')
        fo.write('</actions>\n')
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo.write('<criteria>\n')
        fo.write('<comment>Rubis family of criteria.</comment>\n')
        for g in criteriaList:   
            fo.write('<criterion id="%s" category="%s">\n' % (g,'performance') )
            fo.write('<name>%s</name>\n' % (criteria[g]['name']) )
            fo.write('<comment>%s</comment>\n' % (criteria[g]['comment']) )
            fo.write('<scale>\n')
            #fo.write('<min>'+unicode(criteria[g]['scale'][0])+'</min>\n')
            #fo.write('<max>'+unicode(criteria[g]['scale'][1])+'</max>\n')
            fo.write('<min>%.2f</min>\n' % (criteria[g]['scale'][0]) )
            fo.write('<max>%.2f</max>\n' % (criteria[g]['scale'][1]) )
            fo.write('</scale>\n')
            fo.write('<thresholds>\n')
            try:
                fo.write('<indifference>(%.2f,%.3f)</indifference>\n' % (criteria[g]['thresholds']['ind']) )
            except:
                pass
            try:
                fo.write('<weakPreference>(%.2f,%.3f)</weakPreference>\n' % (criteria[g]['thresholds']['weakPreference']) )
            except:
                pass
            try:
                fo.write('<preference>(%.2f,%.3f)</preference>\n' % (criteria[g]['thresholds']['pref']) )
            except:
                pass
            try:
                fo.write('<weakVeto>(%.2f,%.3f)</weakVeto>\n' % (criteria[g]['thresholds']['weakVeto']) )
            except:
                pass
            try:
                fo.write('<veto>(%.2f,%.3f)</veto>\n' % (criteria[g]['thresholds']['veto']) )
            except:
                pass
            fo.write('</thresholds>\n')
            fo.write('<weight>%.2f</weight>\n' % (criteria[g]['weight']) )
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')
        evaluation = self.evaluation
        fo.write('<evaluations>\n')
        fo.write('<comment>Rubis Performance Table.</comment>\n')
        for g in criteriaList:
            fo.write('<evaluation>\n')
            fo.write('<criterionID>'+str(g)+'</criterionID>\n')
            for i in range(na):
                fo.write('<performance>\n')
                fo.write('<actionID>')       
                fo.write(str(actionsList[i]))
                fo.write('</actionID>\n')                    
                fo.write('<value>')
                fo.write('%.2f' % (evaluation[g][actionsList[i]]) )
                fo.write('</value>\n')
                fo.write('</performance>\n')
            fo.write('</evaluation>\n')        
        fo.write('</evaluations>\n')        
        fo.write('</rubisPerformanceTableau>\n')         
        fo.close()
        print('File: ' + nameExt + ' saved !')


    def saveXMCDA(self,fileName='temp',category='New XMCDA Rubis format',user='digraphs Module (RB)',version='saved from Python session',variant='Rubis',valuationType='standard',servingD3=True):
        """
        save performance tableau object self in XMCDA format.
        """
        import codecs
        print('*----- saving performance tableau in XMCDA format  -------------*')        
        nameExt = fileName+'.xmcda'
        fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2008/UMCDA-ML-1.0 umcda-ml-1.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2008/UMCDA-ML-1.0" instanceID="void">\n'))
       # write description
        fo.write('<caseReference>\n')
        fo.write('<title>Performance Tableau in XMCDA format.</title>\n')   
        fo.write('<id>%s</id>\n' % (fileName) )
        fo.write('<name>%s</name>\n' % (nameExt) )
        fo.write('<type>root</type>\n')
        fo.write('<author>%s</author>\n' % (user) )
        fo.write('<version>%s</version>\n' % (version) )
        fo.write('</caseReference>\n')
        # write methodData
        fo.write('<methodData>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Method data</subTitle>\n')   
        fo.write('<id>%s</id>\n' % ('Rubis') )
        fo.write('<name>%s</name>\n' % ('Rubis best choice method') )
        fo.write('<type>methodData</type>\n')
        fo.write('<version>%s</version>\n' % ('1.0'))
        fo.write('</description>\n')
        fo.write('<parameters>\n')
        fo.write('<parameter>\n')
        fo.write('<name>%s</name>\n' % ('variant') )
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (variant))
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('<parameter>\n')
        fo.write('<name>%s</name>\n' % ('valuationType') )
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (valuationType) )
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('<parameter>\n')
        fo.write('<name>%s</name>\n' % ('significanceThreshold') )
        fo.write('<value>\n')
        fo.write('<label>%.2f</label>\n' % (0.5) )
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('</parameters>\n')
        fo.write('</methodData>\n')
        #  save alternatives
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Potential decision actions.</subTitle>\n')
        fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('</description>\n')                  
        for i in range(na):
            fo.write('<alternative id="%s">\n' % (actionsList[i]))
            fo.write('<description>\n')
            fo.write('<name>')
            try:
                fo.write(str(actions[actionsList[i]]['name']))
            except:
                pass
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                pass
            fo.write('</comment>\n')
            fo.write('</description>\n')                  
            fo.write('<alternativeType>potential</alternativeType>\n')  
            fo.write('<status>active</status>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        # save criteria
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo.write('<criteria>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Family of criteria.</subTitle>\n')
        fo.write('<type>%s</type>\n' % ('criteria'))
        fo.write('</description>\n')       
        for g in criteriaList:   
            fo.write('<criterion id="%s" >\n' % (str(g)) )
            fo.write('<description>\n')
            try:
                fo.write('<name>%s</name>\n' % (str(criteria[g]['name'])) )
            except:
                fo.write('<name>%s</name>\n' % (str(g)) )
                
            fo.write('<type>%s</type>\n' % ('criterion'))            
            try:
                fo.write('<comment>%s</comment>\n' % (str(criteria[g]['comment'])) )
            except:
                fo.write('<comment>%s</comment>\n' % ('No comment') )
            fo.write('<version>%s</version>\n' % ('performance') )
            fo.write('</description>\n')
            fo.write('<status>active</status>\n')
            try:
                if criteria[g]['IntegerWeights']:
                    fo.write('<significance><integer>%d</integer></significance>\n' % (criteria[g]['weight']) )
                else:
                    fo.write('<significance><real>%.2f</real></significance>\n' % (criteria[g]['weight']) )
            except:
                fo.write('<significance><real>%.2f</real></significance>\n' % (criteria[g]['weight']) )
            fo.write('<criterionFunction category="%s" subCategory="%s" >\n' % ('Rubis','performance'))
            fo.write('<scale>\n')
            fo.write('<quantitative>\n')
            try:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % (criteria[g]['preferenceDirection']) )
                if criteria[g]['preferenceDirection'] == 'min':
                    #pdir = -1
                    pdir = 1
                else:
                    pdir = 1
 
            except:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % ('max') )
                pdir = 1
            fo.write('<min><real>%.2f</real></min>\n' % (criteria[g]['scale'][0]) )
            fo.write('<max><real>%.2f</real></max>\n' % (criteria[g]['scale'][1]) )

            fo.write('</quantitative>\n')
            fo.write('</scale>\n')
            fo.write('<thresholds>\n')
            try:
                if criteria[g]['thresholds']['ind'] != None:
                    fo.write('<threshold><type>ind</type>\n')
                    if criteria[g]['thresholds']['ind'][1] != 0.0:
                        fo.write('<function><linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['ind'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</linear></function>\n')
                    else:
                        fo.write('<function><constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</constant></function>\n')                       
                    fo.write('</threshold>\n')
                
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakPreference'] != None:
                    fo.write('<threshold><type>weakPreference</type>\n')
                    if criteria[g]['thresholds']['weakPreference'][1] != 0.0:
                        fo.write('<function><linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakPreference'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</linear></function>\n')
                    else:
                        fo.write('<function><constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</constant></function>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['pref'] != None:
                    fo.write('<threshold><type>pref</type>\n')
                    if criteria[g]['thresholds']['pref'][1] != 0.0:
                        fo.write('<function><linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['pref'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</linear></function>\n')
                    else:
                        fo.write('<function><constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</constant></function>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakVeto'] != None:
                    fo.write('<threshold><type>weakVeto</type>\n')
                    if criteria[g]['thresholds']['weakVeto'][1] != 0.0:
                        fo.write('<function><linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakVeto'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                        fo.write('</linear></function>\n')
                    else:
                        fo.write('<function><constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                        fo.write('</constant></function>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['veto'] != None:
                    fo.write('<threshold><type>veto</type>\n')
                    if criteria[g]['thresholds']['veto'][1] != 0.0:
                        fo.write('<function><linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['veto'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['veto'][0]) )
                        fo.write('</linear></function>\n')
                    else:
                        fo.write('<function><constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['veto'][0]) )
                        fo.write('</constant></function>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            fo.write('</thresholds>\n')
            fo.write('</criterionFunction>\n')
            fo.write('</criterion>\n')
        #fo.write('<majorityThreshold><value><real>0.5</real></value></majorityThreshold>\n')
        fo.write('</criteria>\n')
        # save performance table
        evaluation = self.evaluation
        fo.write('<performanceTable>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Rubis Performance Table.</subTitle>\n')
        fo.write('<type>%s</type>\n' % ('performanceTable'))            
        fo.write('</description>\n')
        for g in criteriaList:
            fo.write('<criterionEvaluations>\n')
            fo.write('<criterionID>'+str(g)+'</criterionID>\n')
            try:
                if self.criteria[g]['preferenceDirection'] == 'min':
                    pdir = -1
                else:
                    pdir = 1
            except:
                pdir = 1

            for i in range(na):
                fo.write('<evaluation>\n')
                fo.write('<alternativeID>')       
                fo.write(str(actionsList[i]))
                fo.write('</alternativeID>\n')                    
                fo.write('<value><real>')
                fo.write('%.2f' % (pdir*evaluation[g][actionsList[i]]) )
                fo.write('</real></value>\n')
                fo.write('</evaluation>\n')
            fo.write('</criterionEvaluations>\n')
        fo.write('</performanceTable>\n')        
        fo.write('</xmcda:XMCDA>\n')         
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMCDA2(self,fileName='temp',\
                   category='XMCDA 2.0 Extended format',\
                   user='digraphs Module (RB)',\
                   version='saved from Python session',\
                   title='Performance Tableau in XMCDA-2.0 format.',\
                   variant='Rubis',\
                   valuationType='bipolar',\
                   servingD3=False,\
                   isStringIO=False,\
                   stringNA='NA',\
                   comment='produced by saveXMCDA2()',\
                   hasVeto=True):
        """
        save performance tableau object self in XMCDA 2.0 format including decision objectives, the case given.
        """
        import codecs
        if not isStringIO:
            print('*----- saving performance tableau in XMCDA 2.0 format  -------------*')
        nameExt = fileName+'.xml'
        if isStringIO:
            comment='produced by stringIO()'
            import io
            ## ms = 100 * len(self.actions) + 500 * len(self.criteria) * 20 * len(self.evaluation)
            ## print 'estimated mapped memory size = %d' % (ms)
            ##fo = mmap.mmap(-1,ms)
            fo = io.StringIO()
        else:
            #nameExt = fileName+'.xmcda2'
            fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/XMCDA-2.0.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0" instanceID="void">\n'))

        # write description
        fo.write('<projectReference id="%s" name="%s">\n' % (fileName,nameExt))
        fo.write('<title>%s</title>\n' % (str(title)) )  
        fo.write('<author>%s</author>\n' % (user) )
        fo.write('<version>%s</version>\n' % (version) )
        fo.write('<comment>%s</comment>\n' % (str(comment)) )
        fo.write('</projectReference>\n')

        # write methodParameters
        fo.write('<methodParameters id="%s" name="%s" mcdaConcept="%s">\n' % ('Rubis','Rubis best choice method','methodData'))
        fo.write('<description>\n')
        fo.write('<subTitle>Method parameters</subTitle>\n')   
        fo.write('<version>%s</version>\n' % ('1.0'))
        fo.write('</description>\n')
        fo.write('<parameters>\n')
        fo.write('<parameter name="%s">\n' % ('variant'))
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (variant))
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('<parameter name="%s">\n' % ('valuationType') )
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (valuationType) )
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('</parameters>\n')
        fo.write('</methodParameters>\n')

        #  save alternatives
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives mcdaConcept="%s">\n' % ('alternatives'))
        fo.write('<description>\n')
        fo.write('<subTitle>Potential decision actions.</subTitle>\n')
        fo.write('</description>\n')                  
        for i in range(na):
            try:
                actionName = str(actions[actionsList[i]]['name'])
            except:
                actionName = ''
            fo.write('<alternative id="%s" name="%s" mcdaConcept="%s">\n' % (actionsList[i],actionName,'potentialDecisionAction'))
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                pass
            fo.write('</comment>\n')
            fo.write('</description>\n')                  
            fo.write('<type>real</type>\n')  
            fo.write('<active>true</active>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')

        # save objectives

        try:
            objectivesList = [x for x in self.objectives]
            objectivesList.sort()
            objectives = self.objectives
            fo.write('<objectives mcdaConcept="objectives">\n')
            fo.write('<description>\n')
            fo.write('<subTitle>Set of decision objectives</subTitle>\n')
            fo.write('</description>\n')
            for obj in objectivesList:
                try:
                    objectiveName = str(objectives[obj]['name'])
                except:
                    objectiveName = str(obj)
                fo.write('<objective id="%s" name="%s" mcdaConcept="%s">\n' % (str(obj),objectiveName,'objective' ) )
                fo.write('<description>\n')                
                try:
                    fo.write('<comment>%s</comment>\n' % (str(objective[obj]['comment'])) )
                except:
                    fo.write('<comment>%s</comment>\n' % ('No comment') )
                fo.write('<version>%s</version>\n' % ('Rubis') )
                fo.write('</description>\n')
                fo.write('<active>true</active>\n')
                fo.write('<weight><value><real>%.2f</real></value></weight>\n' % (objectives[obj]['weight']) )
                try:
                    objCriteria = [x for x in self.criteria if self.criteria[x]['objective'] == obj]
                    fo.write('<objectiveCriteria>%s</objectiveCriteria>\n' % (str(objCriteria)) )
                except:
                    pass
                fo.write('</objective>\n')
            fo.write('</objectives>\n')
        except:
            pass

        # save criteria
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo.write('<criteria mcdaConcept="criteria">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Family of criteria.</subTitle>\n')
        fo.write('</description>\n')       
        for g in criteriaList:
            try:
                criterionName = str(criteria[g]['name'])
            except:
                criterionName = str(g)

            fo.write('<criterion id="%s" name="%s" mcdaConcept="%s">\n' % (str(g),criterionName,'criterion' ) )
            fo.write('<description>\n')                
            try:
                fo.write('<comment>%s</comment>\n' % (str(criteria[g]['comment'])) )
            except:
                fo.write('<comment>%s</comment>\n' % ('No comment') )
            fo.write('<version>%s</version>\n' % ('performance') )
            fo.write('</description>\n')
            fo.write('<active>true</active>\n')
            try:
                fo.write('<criterionObjective>%s</criterionObjective>\n' %(criteria[g]['objective']) )
            except:
                pass
            try:
                if criteria[g]['IntegerWeights']:
                    fo.write('<criterionValue><value><integer>%d</integer></value></criterionValue>\n' % (criteria[g]['weight']) )
                else:
                    fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight']) )
            except:
                fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight']) )
            fo.write('<scale>\n')
            fo.write('<quantitative>\n')
            try:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % (criteria[g]['preferenceDirection']) )
                if criteria[g]['preferenceDirection'] == 'min':
                    #pdir = -1
                    pdir = 1
                else:
                    pdir = 1

            except:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % ('max') )
                pdir = 1
            fo.write('<minimum><real>%.2f</real></minimum>\n' % (criteria[g]['scale'][0]) )
            fo.write('<maximum><real>%.2f</real></maximum>\n' % (criteria[g]['scale'][1]) )

            fo.write('</quantitative>\n')
            fo.write('</scale>\n')
            try:
                if len(criteria[g]['thresholds']) != 0:
                    fo.write('<thresholds>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['ind'] != None:
                    fo.write('<threshold id="ind" name="indifference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['ind'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['ind'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
                
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakPreference'] != None:
                    fo.write('<threshold id="weakPreference" name="weak Preference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['weakPreference'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakPreference'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['pref'] != None:
                    fo.write('<threshold id="pref" name="preference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['pref'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['pref'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            if hasVeto:
                try:
                    if criteria[g]['thresholds']['weakVeto'] != None:
                        fo.write('<threshold id="weakVeto" name="weak veto" mcdaConcept="performanceDiscriminationThreshold">\n')
                        if criteria[g]['thresholds']['weakVeto'][1] != 0.0:
                            fo.write('<linear>\n')
                            fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakVeto'][1]) )
                            fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                            fo.write('</linear>\n')
                        else:
                            fo.write('<constant>\n')
                            fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                            fo.write('</constant>\n')                       
                        fo.write('</threshold>\n')
                except:
                    pass
                try:
                    if criteria[g]['thresholds']['veto'] != None:
                        fo.write('<threshold id="veto" name="veto" mcdaConcept="performanceDiscriminationThreshold">\n')
                        if criteria[g]['thresholds']['veto'][1] != 0.0:
                            fo.write('<linear>\n')
                            fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['veto'][1]) )
                            fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['veto'][0]) )
                            fo.write('</linear>\n')
                        else:
                            fo.write('<constant>\n')
                            fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['veto'][0]) )
                            fo.write('</constant>\n')                       
                        fo.write('</threshold>\n')
                except:
                    pass
            try:
                if len(criteria[g]['thresholds']) != 0:
                    fo.write('</thresholds>\n')
            except:
                pass
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')

        # save performance table
        evaluation = self.evaluation
        fo.write('<performanceTable mcdaConcept="performanceTable">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Rubis Performance Table.</subTitle>\n')
        fo.write('</description>\n')
        for i in range(len(actionsList)):
            fo.write('<alternativePerformances>\n')
            fo.write('<alternativeID>'+str(actionsList[i])+'</alternativeID>\n')
            for g in criteriaList:
                try:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        if self.criteria[g]['weight'] > Decimal('0'):
                            pdir = Decimal('-1')
                        else:
                            pdir = Decimal('1')
                    else:
                        pdir = Decimal('1')
                except:
                    pdir = Decimal('1')

                fo.write('<performance>\n')
                fo.write('<criterionID>')       
                fo.write(g)
                fo.write('</criterionID>\n')
                if evaluation[g][actionsList[i]] == Decimal('-999'):
                    val = evaluation[g][actionsList[i]]
                else:
                    val = pdir*evaluation[g][actionsList[i]]
                if val == Decimal("-999"):
                    fo.write('<value><NA>')
                    fo.write('%s' % stringNA )
                    fo.write('</NA></value>\n')
                    fo.write('</performance>\n')
                else:
                    fo.write('<value><real>')
                    fo.write('%.2f' % val )
                    fo.write('</real></value>\n')
                    fo.write('</performance>\n')                    
            fo.write('</alternativePerformances>\n')
        fo.write('</performanceTable>\n')        
        fo.write('</xmcda:XMCDA>\n')
        if isStringIO:
            problemText = fo.getvalue()
            fo.close            
            return problemText
        else:
            fo.close()
            print('File: ' + nameExt + ' saved !')

    def _saveXMCDA2(self,fileName='temp',\
                   category='XMCDA 2.0 format',\
                   user='digraphs Module (RB)',\
                   version='saved from Python session',\
                   title='Performance Tableau in XMCDA-2.0 format.',\
                   variant='Rubis',\
                   valuationType='bipolar',\
                   servingD3=True,\
                   isStringIO=False,\
                   stringNA='NA',\
                   comment='produced by saveXMCDA2()',\
                   hasVeto=True):
        """
        save performance tableau object self in XMCDA 2.0 format.
        """
        import codecs
        if not isStringIO:
            print('*----- saving performance tableau in XMCDA 2.0 format  -------------*')
        nameExt = fileName+'.xml'
        if isStringIO:
            comment='produced by stringIO()'
            import io
            ## ms = 100 * len(self.actions) + 500 * len(self.criteria) * 20 * len(self.evaluation)
            ## print 'estimated mapped memory size = %d' % (ms)
            ##fo = mmap.mmap(-1,ms)
            fo = io.StringIO()
        else:
            #nameExt = fileName+'.xmcda2'
            fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/XMCDA-2.0.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0" instanceID="void">\n'))

        # write description
        fo.write('<projectReference id="%s" name="%s">\n' % (fileName,nameExt))
        fo.write('<title>%s</title>\n' % (str(title)) )  
        fo.write('<author>%s</author>\n' % (user) )
        fo.write('<version>%s</version>\n' % (version) )
        fo.write('<comment>%s</comment>\n' % (str(comment)) )
        fo.write('</projectReference>\n')

        # write methodParameters
        fo.write('<methodParameters id="%s" name="%s" mcdaConcept="%s">\n' % ('Rubis','Rubis best choice method','methodData'))
        fo.write('<description>\n')
        fo.write('<subTitle>Method parameters</subTitle>\n')   
        fo.write('<version>%s</version>\n' % ('1.0'))
        fo.write('</description>\n')
        fo.write('<parameters>\n')
        fo.write('<parameter name="%s">\n' % ('variant'))
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (variant))
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('<parameter name="%s">\n' % ('valuationType') )
        fo.write('<value>\n')
        fo.write('<label>%s</label>\n' % (valuationType) )
        fo.write('</value>\n')
        fo.write('</parameter>\n')
        fo.write('</parameters>\n')
        fo.write('</methodParameters>\n')

        #  save alternatives
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives mcdaConcept="%s">\n' % ('alternatives'))
        fo.write('<description>\n')
        fo.write('<subTitle>Potential decision actions.</subTitle>\n')
        fo.write('</description>\n')                  
        for i in range(na):
            try:
                actionName = str(actions[actionsList[i]]['name'])
            except:
                actionName = ''
            fo.write('<alternative id="%s" name="%s" mcdaConcept="%s">\n' % (actionsList[i],actionName,'potentialDecisionAction'))
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                pass
            fo.write('</comment>\n')
            fo.write('</description>\n')                  
            fo.write('<type>real</type>\n')  
            fo.write('<active>true</active>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')

        # save criteria
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo.write('<criteria mcdaConcept="criteria">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Family of criteria.</subTitle>\n')
        fo.write('</description>\n')       
        for g in criteriaList:
            try:
                criterionName = str(criteria[g]['name'])
            except:
                criterionName = str(g)

            fo.write('<criterion id="%s" name="%s" mcdaConcept="%s">\n' % (str(g),criterionName,'criterion' ) )
            fo.write('<description>\n')                
            try:
                fo.write('<comment>%s</comment>\n' % (str(criteria[g]['comment'])) )
            except:
                fo.write('<comment>%s</comment>\n' % ('No comment') )
            fo.write('<version>%s</version>\n' % ('performance') )
            fo.write('</description>\n')
            fo.write('<active>true</active>\n')
            try:
                if criteria[g]['IntegerWeights']:
                    fo.write('<criterionValue><value><integer>%d</integer></value></criterionValue>\n' % (criteria[g]['weight']) )
                else:
                    fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight']) )
            except:
                fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight']) )
            fo.write('<scale>\n')
            fo.write('<quantitative>\n')
            try:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % (criteria[g]['preferenceDirection']) )
                if criteria[g]['preferenceDirection'] == 'min':
                    #pdir = -1
                    pdir = 1
                else:
                    pdir = 1

            except:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % ('max') )
                pdir = 1
            fo.write('<minimum><real>%.2f</real></minimum>\n' % (criteria[g]['scale'][0]) )
            fo.write('<maximum><real>%.2f</real></maximum>\n' % (criteria[g]['scale'][1]) )

            fo.write('</quantitative>\n')
            fo.write('</scale>\n')
            try:
                if len(criteria[g]['thresholds']) != 0:
                    fo.write('<thresholds>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['ind'] != None:
                    fo.write('<threshold id="ind" name="indifference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['ind'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['ind'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['ind'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
                
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakPreference'] != None:
                    fo.write('<threshold id="weakPreference" name="weak Preference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['weakPreference'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakPreference'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakPreference'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if criteria[g]['thresholds']['pref'] != None:
                    fo.write('<threshold id="pref" name="preference" mcdaConcept="performanceDiscriminationThreshold">\n')
                    if criteria[g]['thresholds']['pref'][1] != 0.0:
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['pref'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['pref'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            if hasVeto:
                try:
                    if criteria[g]['thresholds']['weakVeto'] != None:
                        fo.write('<threshold id="weakVeto" name="weak veto" mcdaConcept="performanceDiscriminationThreshold">\n')
                        if criteria[g]['thresholds']['weakVeto'][1] != 0.0:
                            fo.write('<linear>\n')
                            fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakVeto'][1]) )
                            fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                            fo.write('</linear>\n')
                        else:
                            fo.write('<constant>\n')
                            fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakVeto'][0]) )
                            fo.write('</constant>\n')                       
                        fo.write('</threshold>\n')
                except:
                    pass
                try:
                    if criteria[g]['thresholds']['veto'] != None:
                        fo.write('<threshold id="veto" name="veto" mcdaConcept="performanceDiscriminationThreshold">\n')
                        if criteria[g]['thresholds']['veto'][1] != 0.0:
                            fo.write('<linear>\n')
                            fo.write('<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['veto'][1]) )
                            fo.write('<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['veto'][0]) )
                            fo.write('</linear>\n')
                        else:
                            fo.write('<constant>\n')
                            fo.write('<real>%.2f</real>\n' % (criteria[g]['thresholds']['veto'][0]) )
                            fo.write('</constant>\n')                       
                        fo.write('</threshold>\n')
                except:
                    pass
            try:
                if len(criteria[g]['thresholds']) != 0:
                    fo.write('</thresholds>\n')
            except:
                pass
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')

        # save performance table
        evaluation = self.evaluation
        fo.write('<performanceTable mcdaConcept="performanceTable">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Rubis Performance Table.</subTitle>\n')
        fo.write('</description>\n')
        for i in range(len(actionsList)):
            fo.write('<alternativePerformances>\n')
            fo.write('<alternativeID>'+str(actionsList[i])+'</alternativeID>\n')
            for g in criteriaList:
                try:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        pdir = Decimal('-1')
                    else:
                        pdir = Decimal('1')
                except:
                    pdir = Decimal('1')

                fo.write('<performance>\n')
                fo.write('<criterionID>')       
                fo.write(g)
                fo.write('</criterionID>\n')
                val = pdir*evaluation[g][actionsList[i]]
                if val == Decimal("-999"):
                    fo.write('<value><NA>')
                    fo.write('%s' % stringNA )
                    fo.write('</NA></value>\n')
                    fo.write('</performance>\n')
                else:
                    fo.write('<value><real>')
                    fo.write('%.2f' % val )
                    fo.write('</real></value>\n')
                    fo.write('</performance>\n')                    
            fo.write('</alternativePerformances>\n')
        fo.write('</performanceTable>\n')        
        fo.write('</xmcda:XMCDA>\n')
        if isStringIO:
            problemText = fo.getvalue()
            fo.close            
            return problemText
        else:
            fo.close()
            print('File: ' + nameExt + ' saved !')

    def saveXMCDA2String(self,fileName='temp',category='XMCDA 2.0 format',\
                         user='digraphs Module (RB)',version='saved from Python session',\
                         title='Performance Tableau in XMCDA-2.0 format.',variant='Rubis',\
                         valuationType='bipolar',servingD3=True,comment='produced by stringIO()',\
                         stringNA='NA'):
        """
        save performance tableau object self in XMCDA 2.0 format.
        !!! obsolete: replaced by the isStringIO in the saveXMCDA2 method !!!
        """
        import codecs
        nameExt = fileName+'.xml'
        fo = str('')
        fo += '<?xml version="1.0" encoding="UTF-8"?>\n'
        if servingD3:
            fo += '<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n'
        else:
            fo += '<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n'
        fo += str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/XMCDA-2.0.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0" instanceID="void">\n')

        # write description
        fo += '<projectReference id="%s" name="%s">\n' % (fileName,nameExt)
        fo += '<title>%s</title>\n' % (str(title))  
        fo += '<author>%s</author>\n' % (str(user)) 
        fo += '<version>%s</version>\n' % (str(version)) 
        fo += '<comment>%s</comment>\n' % (str(comment)) 
        fo += '</projectReference>\n'

        # write methodParameters
        fo += '<methodParameters id="%s" name="%s" mcdaConcept="%s">\n' % ('Rubis','Rubis best choice method','methodData')
        fo += '<description>\n'
        fo += '<subTitle>Method parameters</subTitle>\n'   
        fo += '<version>%s</version>\n' % ('1.0')
        fo += '</description>\n'
        fo += '<parameters>\n'
        fo += '<parameter name="%s">\n' % ('variant')
        fo += '<value>\n'
        fo += '<label>%s</label>\n' % (variant)
        fo += '</value>\n'
        fo += '</parameter>\n'
        fo += '<parameter name="%s">\n' % ('valuationType')
        fo += '<value>\n'
        fo += '<label>%s</label>\n' % (valuationType) 
        fo += '</value>\n'
        fo += '</parameter>\n'
        fo += '</parameters>\n'
        fo += '</methodParameters>\n'

        #  save alternatives
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo += '<alternatives mcdaConcept="%s">\n' % ('alternatives')
        fo += '<description>\n'
        fo += '<subTitle>Potential decision actions.</subTitle>\n'
        fo += '</description>\n'                  
        for i in range(na):
            try:
                actionName = str(actions[actionsList[i]]['name'])
            except:
                actionName = ''
            fo += '<alternative id="%s" name="%s" mcdaConcept="%s">\n' % (actionsList[i],actionName,'potentialDecisionAction')
            fo += '<description>\n'
            fo += '<comment>'
            try:
                fo += str(actions[actionsList[i]]['comment'])
            except:
                pass
            fo += '</comment>\n'
            fo += '</description>\n'                  
            fo += '<type>real</type>\n'  
            fo += '<active>true</active>\n'
            fo += '</alternative>\n'
        fo += '</alternatives>\n'

        # save objectives

        try:
            objectivesList = [x for x in self.objectives]
            objectivesList.sort()
            objectives = self.objectives
            fo += '<objectives mcdaConcept="objectives">\n'
            fo += '<description>\n'
            fo += '<subTitle>Set of decision objectives</subTitle>\n'
            fo += '</description>\n'
            for obj in objectivesList:
                try:
                    objectiveName = str(objectives[obj]['name'])
                except:
                    objectiveName = str(obj)
                fo += '<objective id="%s" name="%s" mcdaConcept="%s">\n' % (str(obj),objectiveName,'objective' ) 
                fo += '<description>\n'
                try:
                    fo += '<comment>%s</comment>\n' % (str(objective[obj]['comment'])) 
                except:
                    fo += '<comment>%s</comment>\n' % ('No comment')
                fo += '<version>%s</version>\n' % ('Rubis')
                fo += '</description>\n'
                fo += '<active>true</active>\n'
                fo += '<weight><value><real>%.2f</real></value></weight>\n' % (objectives[obj]['weight'])
                try:
                    objCriteria = [x for x in self.criteria if self.criteria[x]['objective'] == obj]
                    fo += '<objectiveCriteria>%s</objectiveCriteria>\n' % (str(objCriteria))
                except:
                    pass
                fo += '</objective>\n'
            fo += '</objectives>\n'
        except:
            pass

        # save criteria
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo += '<criteria mcdaConcept="criteria">\n'
        fo += '<description>\n'
        fo += '<subTitle>Family of criteria.</subTitle>\n'
        fo += '</description>\n'       
        for g in criteriaList:
            try:
                criterionName = str(criteria[g]['name'])
            except:
                criterionName = str(g)

            fo += '<criterion id="%s" name="%s" mcdaConcept="%s">\n' % (str(g),criterionName,'criterion' )
            fo += '<description>\n'                
            try:
                fo += '<comment>%s</comment>\n' % (str(criteria[g]['comment'])) 
            except:
                fo += '<comment>%s</comment>\n' % ('No comment')
            fo += '<version>%s</version>\n' % ('performance')
            fo += '</description>\n'
            fo += '<active>true</active>\n'
            try:
                fo += '<criterionObjective>%s</criterionObjective>\n' %(criteria[g]['objective'])
            except:
                pass
            try:
                if criteria[g]['IntegerWeights']:
                    fo += '<criterionValue><value><integer>%d</integer></value></criterionValue>\n' % (criteria[g]['weight'])
                else:
                    fo += '<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight'])
            except:
                fo += '<criterionValue><value><real>%.2f</real></value></criterionValue>\n' % (criteria[g]['weight'])
            fo += '<scale>\n'
            fo += '<quantitative>\n'
            try:
                fo += '<preferenceDirection>%s</preferenceDirection>\n' % (criteria[g]['preferenceDirection'])
                if criteria[g]['preferenceDirection'] == 'min':
                    #pdir = -1
                    pdir = 1
                else:
                    pdir = 1

            except:
                fo += '<preferenceDirection>%s</preferenceDirection>\n' % ('max')
                pdir = 1
            fo += '<minimum><real>%.2f</real></minimum>\n' % (criteria[g]['scale'][0])
            fo += '<maximum><real>%.2f</real></maximum>\n' % (criteria[g]['scale'][1])

            fo += '</quantitative>\n'
            fo += '</scale>\n'
            fo += '<thresholds>\n'
            try:
                if criteria[g]['thresholds']['ind'] != None:
                    fo += '<threshold id="ind" name="indifference" mcdaConcept="performanceDiscriminationThreshold">\n'
                    if criteria[g]['thresholds']['ind'][1] != 0.0:
                        fo += '<linear>\n'
                        fo += '<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['ind'][1])
                        fo += '<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['ind'][0])
                        fo += '</linear>\n'
                    else:
                        fo += '<constant>\n'
                        fo += '<real>%.2f</real>\n' % (criteria[g]['thresholds']['ind'][0])
                        fo += '</constant>\n'                       
                    fo += '</threshold>\n'
                
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakPreference'] != None:
                    fo += '<threshold id="weakPreference" name="weak Preference" mcdaConcept="performanceDiscriminationThreshold">\n'
                    if criteria[g]['thresholds']['weakPreference'][1] != 0.0:
                        fo += '<linear>\n'
                        fo += '<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakPreference'][1])
                        fo += '<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakPreference'][0])
                        fo += '</linear>\n'
                    else:
                        fo += '<constant>\n'
                        fo += '<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakPreference'][0])
                        fo += '</constant>\n'                       
                    fo += '</threshold>\n'
            except:
                pass
            try:
                if criteria[g]['thresholds']['pref'] != None:
                    fo += '<threshold id="pref" name="preference" mcdaConcept="performanceDiscriminationThreshold">\n'
                    if criteria[g]['thresholds']['pref'][1] != 0.0:
                        fo += '<linear>\n'
                        fo += '<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['pref'][1])
                        fo += '<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['pref'][0])
                        fo += '</linear>\n'
                    else:
                        fo += '<constant>\n'
                        fo += '<real>%.2f</real>\n' % (criteria[g]['thresholds']['pref'][0])
                        fo += '</constant>\n'                       
                    fo += '</threshold>\n'
            except:
                pass
            try:
                if criteria[g]['thresholds']['weakVeto'] != None:
                    fo += '<threshold id="weakVeto" name="weak veto" mcdaConcept="performanceDiscriminationThreshold">\n'
                    if criteria[g]['thresholds']['weakVeto'][1] != 0.0:
                        fo += '<linear>\n'
                        fo += '<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['weakVeto'][1])
                        fo += '<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['weakVeto'][0])
                        fo += '</linear>\n'
                    else:
                        fo += '<constant>\n'
                        fo += '<real>%.2f</real>\n' % (criteria[g]['thresholds']['weakVeto'][0])
                        fo += '</constant>\n'                       
                    fo += '</threshold>\n'
            except:
                pass
            try:
                if criteria[g]['thresholds']['veto'] != None:
                    fo += '<threshold id="veto" name="veto" mcdaConcept="performanceDiscriminationThreshold">\n'
                    if criteria[g]['thresholds']['veto'][1] != 0.0:
                        fo += '<linear>\n'
                        fo += '<slope><real>%.2f</real></slope>\n' % (pdir*criteria[g]['thresholds']['veto'][1])
                        fo += '<intercept><real>%.2f</real></intercept>\n' % (criteria[g]['thresholds']['veto'][0])
                        fo += '</linear>\n'
                    else:
                        fo += '<constant>\n'
                        fo += '<real>%.2f</real>\n' % (criteria[g]['thresholds']['veto'][0])
                        fo += '</constant>\n'                       
                    fo += '</threshold>\n'
            except:
                pass
            fo += '</thresholds>\n'
            fo += '</criterion>\n'
        fo += '</criteria>\n'

        # save performance table
        evaluation = self.evaluation
        fo += '<performanceTable mcdaConcept="performanceTable">\n'
        fo += '<description>\n'
        fo += '<subTitle>Rubis Performance Table.</subTitle>\n'
        fo += '</description>\n'
        for i in range(len(actionsList)):
            fo += '<alternativePerformances>\n'
            fo += '<alternativeID>'+str(actionsList[i])+'</alternativeID>\n'
            for g in criteriaList:
                fo += '<performance>\n'
                fo += '<criterionID>'       
                fo += g
                fo += '</criterionID>\n'
                val = pdir*evaluation[g][actionsList[i]]
                if val == Decimal("-999"):
                    fo += '<value><NA>'
                    fo += '%s' % stringNA
                    fo += '</NA></value>\n'
                else: 
                    try:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            pdir = Decimal('-1')
                        else:
                            pdir = Decimal('1')
                    except:
                        pdir = Decimal('1')
                    fo += '<value><real>'
                    fo += '%.2f' % (pdir*evaluation[g][actionsList[i]])
                    fo += '</real></value>\n'
                fo += '</performance>\n'
            fo += '</alternativePerformances>\n'
        fo += '</performanceTable>\n'        
        fo += '</xmcda:XMCDA>\n'
        return fo
     


    ## def showStatistics(self,withOutput=False,Comments=True):
    ##     """
    ##     show version of the computeStatistics method for PerformanceTableau instances
    ##     """
    ##     self.computeStatistics(withOutput=withOutput,Comments=Comments)

    def computeNormalizedDiffEvaluations(self,lowValue=0.0,highValue=100.0,withOutput=False,Debug=False):
        """
        renders and csv stores (withOutput=True) the
        list of normalized evaluation differences observed on the family of criteria
        Is only adequate if all criteria have the same
        evaluation scale. Therefore the performance tableau is normalized to 0.0-100.0 scales.
        """
        self.normalizeEvaluations(lowValue=lowValue,highValue=highValue)
        if Debug:
            self.showPerformanceTableau()
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
        diffEvaluations = []
        if withOutput:
            fileoutName = self.name + '_diff.csv'
            fo = open(fileoutName, 'w')
            fo.write('# Evaluation differences statistics \n')
            fo.write('"diffperf"\n')
        for g in criteria:
            for x in actions:
                for y in actions:
                    if x != y:
                        diffxy = evaluation[g][x] - evaluation[g][y]
                        diffEvaluations.append(diffxy)
                        if Debug:
                            print('diffxy = evaluation[g][x] = evaluation[g][y]', diffxy, ' = ', evaluation[g][x], ' - ', evaluation[g][y])
                        if withOutput:
                            fo.write('%.2f\n' % diffxy)                
        if withOutput:
            fo.close()
        self.diffEvaluations = diffEvaluations

        return diffEvaluations

    
    def showStatistics(self,Debug=False):
        """
        show statistics concerning the evaluation distributions
        on each criteria.
        """
        import math
        criteriaKeys = [x for x in self.criteria]
        criteriaKeys.sort()
        nc = len(self.criteria)
        evaluation = self.evaluation
        actions = self.actions
        n = len(actions)
        print('*-------- Performance tableau summary statistics -------*')
        print('Instance name      :', self.name)
        print('#Actions           :', n)
        print('#Criteria          :', nc)
        print('*Statistics per Criterion*')
        for g in criteriaKeys:
            print('Criterion name       :', g)
            print('Criterion weight     :', self.criteria[g]['weight'])
            averageEvaluation = Decimal('0.0')
            varianceEvaluation = Decimal('0.0')
            Max = Decimal(str(self.criteria[g]['scale'][1]))
            Min = Decimal(str(self.criteria[g]['scale'][0]))
            minEvaluation = Max
            maxEvaluation = Min
            evaluationList = []
            for x in actions:
                if evaluation[g][x] != Decimal('-999'):
                    evaluationList.append(evaluation[g][x])
                    averageEvaluation += evaluation[g][x]
                    varianceEvaluation += evaluation[g][x]**Decimal('2')
                    if evaluation[g][x] < minEvaluation:
                        minEvaluation = evaluation[g][x]
                    if evaluation[g][x] > maxEvaluation:
                        maxEvaluation = evaluation[g][x]
            evaluationList.sort()
            na = len(evaluationList)
            if Debug:
                print(evaluationList)
            try:
                if self.criteria[g]['preferenceDirection'] == 'max':
                    print('  criterion scale      : %.2f - %.2f' % (Min, Max))
                else:
                    print('  criterion scale      : %.2f - %.2f' % (-Max, Min))
            except:
                print('  criterion scale    : %.2f - %.2f' % (Min, Max))
            print('  # missing evaluations : %d'   % (n-na))
            # !! index on evaluation List goes from 0 to na -1 !!
            if na > 5:
                rankQ1 = na / 4.0
                lowRankQ1 = int(math.floor(rankQ1))
                proportQ1 = Decimal(str(rankQ1 - lowRankQ1))
                quantileQ1 = evaluationList[lowRankQ1] + (proportQ1 * (evaluationList[lowRankQ1+1]-evaluationList[lowRankQ1]) )
                #print rankQ1, lowRankQ1, proportQ1

                rankQ2 = na / 2.0
                lowRankQ2 = int(math.floor(rankQ2))
                proportQ2 = Decimal(str(rankQ2 - lowRankQ2))
                
                quantileQ2 = evaluationList[lowRankQ2] + (proportQ2 * ( evaluationList[lowRankQ2+1] - evaluationList[lowRankQ2]) )

                rankQ3 = (na * 3.0) / 4.0
                lowRankQ3 = int(math.floor(rankQ3))
                proportQ3 = Decimal(str(rankQ3 - lowRankQ3))
                              
                quantileQ3 = evaluationList[lowRankQ3] + ( proportQ3 * (evaluationList[lowRankQ3+1]-evaluationList[lowRankQ3]) )
                    
                averageEvaluation /= Decimal(str(na))
                varianceEvaluation = varianceEvaluation/na - averageEvaluation**Decimal('2')
                stdDevEvaluation = math.sqrt(varianceEvaluation)
                print('  mean evaluation       : %.2f' % (averageEvaluation))
                print('  standard deviation    : %.2f' % (stdDevEvaluation))
                print('  maximal evaluation    : %.2f' % (maxEvaluation))
                print('  quantile Q3 (x_75)    : %.2f' % (quantileQ3))
                print('  median evaluation     : %.2f' % (quantileQ2))
                print('  quantile Q1 (x_25)    : %.2f' % (quantileQ1))
                print('  minimal evaluation    : %.2f' % (minEvaluation))
                averageAbsDiffEvaluation = Decimal('0.0')
                varianceDiffEvaluation = Decimal('0.0')
                nd = 0
                for x in actions:
                    for y in actions:
                        if evaluation[g][x] != Decimal('-999') and evaluation[g][y] != Decimal('-999'):
                            diffxy = (evaluation[g][x] - evaluation[g][y])
                            averageAbsDiffEvaluation += abs(diffxy)
                            varianceDiffEvaluation += diffxy**Decimal('2')
                            nd += 1
    #            print '  Sum of evaluation differences = ', averageAbsDiffEvaluation
                averageAbsDiffEvaluation /= Decimal(str(nd))
                ## averageDiffEvaluation == 0 per construction  
                varianceDiffEvaluation = varianceDiffEvaluation/Decimal(str(nd))
                stdDevDiffEvaluation = math.sqrt(varianceDiffEvaluation)
                print('  mean absolute difference      : %.2f' % (averageAbsDiffEvaluation))
                print('  standard difference deviation : %.2f' % (stdDevDiffEvaluation))

    def normalizeEvaluations(self,lowValue=0.0,highValue=100.0,Debug=False):
        """
        recode the evaluations between lowValue and highValue on all criteria
        """
        ##from math import copysign
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
        lowValue = Decimal(str(lowValue))
        highValue = Decimal(str(highValue))
        amplitude = highValue-lowValue
        if Debug:
            print('lowValue', lowValue, 'amplitude', amplitude)
        criterionKeys = [x for x in criteria]
        actionKeys = [x for x in actions]
        normEvaluation = {}
        for g in criterionKeys:
            #print(g, criteria[g]['weight'], criteria[g]['preferenceDirection'])
            normEvaluation[g] = {}
            glow = Decimal(str(criteria[g]['scale'][0]))
            ghigh = Decimal(str(criteria[g]['scale'][1]))
            gamp = ghigh - glow
            if Debug:
                print('-->> g, glow, ghigh, gamp', g, glow, ghigh, gamp)
            for x in actionKeys:
                if evaluation[g][x] != Decimal('-999'):
                    evalx = abs(evaluation[g][x])
                    if Debug:
                        print(evalx)
                    normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                    try:
                        if criteria[g]['preferenceDirection'] == 'max':
                            normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)
                            #print('passing here',normEvaluation[g][x])
                            
                        elif criteria[g]['preferenceDirection'] == 'min':
                        #else:
                            normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*(-amplitude))
                            #print('passing here',normEvaluation[g][x])
                    except:
                        if criteria[g]['weight'] > Decimal('0.0'):
                            self.criteria[g]['preferenceDirection'] = 'max'
                            normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                        else:
                            self.criteria[g]['preferenceDirection'] = 'min'
                            normEvaluation[g][x] = -(lowValue + ((evalx-glow)/gamp)*amplitude)
                        
                    if Debug:
                        print(criteria[g]['preferenceDirection'], evaluation[g][x], normEvaluation[g][x])
                else:
                    normEvaluation[g][x] = Decimal('-999')
                    
        return normEvaluation

    def restoreOriginalEvaluations(self,lowValue=0.0,highValue=100.0,Debug=False):
        """
        recode the evaluations to their original values on all criteria
        """
        evaluation = self.evaluation
        criteria = self.criteria
        lowValue = Decimal(str(lowValue))
        highValue = Decimal(str(highValue))
        amplitude = highValue-lowValue
        if Debug:
            print('lowValue', lowValue, 'amplitude', amplitude)
        criterionKeys = [x for x in evaluation]
        restoredEvaluation = {}
        for g in criterionKeys:
            restoredEvaluation[g] = {}
            glow = Decimal(str(criteria[g]['scale'][0]))
            ghigh = Decimal(str(criteria[g]['scale'][1]))
            gamp = ghigh - glow
            if Debug:
                print('-->> g, glow, ghigh, gamp', g, glow, ghigh, gamp)
            for x in evaluation[g]:
                if evaluation[g][x] != Decimal('-999'):
                    evalx = abs(evaluation[g][x])
                    if Debug:
                        print(evalx)
                    ## normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                    try:
                        if criteria[g]['preferenceDirection'] == 'min':
                            sign = Decimal('-1')
                        else:
                            sign = Decimal('1')
                        #normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)*sign
                        restoredEvaluation[g][x] = (glow + ((evalx-lowValue)/amplitude)*gamp)*sign
                    except:
                        self.criteria[g]['preferenceDirection'] = 'max'
                        restoredEvaluation[g][x] = glow+ ((evalx-lowValue)/amplitude)*gamp
                        
                    if Debug:
                        print(criteria[g]['preferenceDirection'], evaluation[g][x], restoredEvaluation[g][x])
                else:
                    restoredEvaluation[g][x] = Decimal('-999')
                    
        return restoredEvaluation

#-----------------------
class EmptyPerformanceTableau(PerformanceTableau):
    """
    Template for PerformanceTableau objects.
    """
    def __init__(self):
        from collections import OrderedDict
        self.name = 'PerfTab-template'
        self.objectives = OrderedDict()
        self.criteria = OrderedDict()
        self.actions = OrderedDict()
        self.evaluation = {}

#-----------------------
class PartialPerformanceTableau(PerformanceTableau):
    """
    Constructor for partial performance tableaux concerning a subset of actions and/or criteria and/or objectives
    """
    def __init__(self,inPerfTab,actionsSubset=None,criteriaSubset=None,objectivesSubset=None):
        from copy import deepcopy
        from collections import OrderedDict
        from randomPerfTabs import RandomCBPerformanceTableau,\
                                   Random3ObjectivesPerformanceTableau,\
                                   RandomPerformanceTableau
        self.__class__ = inPerfTab.__class__
        # name
        self.name = 'partial-'+inPerfTab.name
        # actions
        if actionsSubset != None:
            actions = OrderedDict()
            for x in actionsSubset:
                actions[x] = deepcopy(inPerfTab.actions[x])
        else:
            actions = deepcopy(inPerfTab.actions)
        self.actions = actions
        actionsTypeStatistics = {}
        for x in inPerfTab.actions:
            if type(inPerfTab) == RandomCBPerformanceTableau:
                xType = inPerfTab.actions[x]['type']
            elif type(inPerfTab) == Random3ObjectivesPerformanceTableau:
                self.objectiveSupportingTypes = inPerfTab.objectiveSupportingTypes
                xType = 'Soc' + inPerfTab.actions[x]['profile']['Soc']
                xType += 'Eco' + inPerfTab.actions[x]['profile']['Eco']
                xType += 'Env' + inPerfTab.actions[x]['profile']['Env']
            else:
                xType = 'NA'
            try:
                actionsTypeStatistics[xType] += 1
            except:
                actionsTypeStatistics[xType] = 1
        self.actionsTypeStatistics = actionsTypeStatistics
        
        # objectives & criteria
        objectives = OrderedDict()
        HasObjectives = True
        if objectivesSubset == None:
            try:
                objectives = deepcopy(inPerfTab.objectives)
            except:
                HasObjectives = False
            if criteriaSubset != None:
                criteria = OrderedDict()
                if HasObjectives:
                    for obj in objectives.keys():
                        objectives[obj]['criteria'] = []
                for g in criteriaSubset:
                    criteria[g] = deepcopy(inPerfTab.criteria[g])
##                    if HasObjectives:
                    try:
                        obj = inPerfTab.criteria[g]['objective']
                        objectives[obj]['criteria'].append(g)
                    except:
                        pass
            else:
                criteria = deepcopy(inPerfTab.criteria)
        else:
            objectives = OrderedDict()
            criteria = OrderedDict()
            if criteriaSubset == None:
                criteriaSubset = list(inPerfTab.criteria.keys())
            for obj in objectivesSubset:
                objectives[obj] = deepcopy(inPerfTab.objectives[obj])
                objectives[obj]['criteria'] = []
                for g in inPerfTab.objectives[obj]['criteria']:
                    if g in criteriaSubset:
                        criteria[g] = deepcopy(inPerfTab.criteria[g])
                        objectives[obj]['criteria'].append(g)
        self.objectives = objectives
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
        
        self.criteria = criteria
        self.weightPreorder = self.computeWeightPreorder()
        # evaluations
        try:
            self.valueDigits = perfTab.valueDigits
        except:
            self.valueDigits = 2

        evaluation = {}
        for g in criteria.keys():
            evaluation[g] = {}
            for x in actions.keys():
                evaluation[g][x] = deepcopy(inPerfTab.evaluation[g][x])
        self.evaluation = evaluation
        
#-----------------------
class ConstantPerformanceTableau(PerformanceTableau):
    """
    Constructor for (partially) constant performance tableaux.

    *Parameter*:
    
        * *actionsSubset* selects the actions to be set at equal constant performances,
        * *criteriaSubset* select the concerned subset of criteria,
        * The *position* parameter (default = median performance) selects the constant performance in the respective scale of each performance criterion.
    
    """
    def __init__(self,inPerfTab,actionsSubset=None,criteriaSubset=None,
                 position=0.5):
        from copy import deepcopy
        
        self.name = 'constant-'+inPerfTab.name

        try:
            self.description = deepcopy(inPerfTab.description)
        except:
            pass

        self.actions = deepcopy(inPerfTab.actions)
        if actionsSubset == None:
            actionsSubset = self.actions

        self.criteria = deepcopy(inPerfTab.criteria)
        if criteriaSubset == None:
            criteriaSubset = self.criteria

        self.weightPreorder = self.computeWeightPreorder()

        self.evaluation = deepcopy(inPerfTab.evaluation)

        actionsKeys = [x for x in actionsSubset]
        criteriaKeys = [g for g in criteriaSubset]
        for g in criteriaKeys:
            constantPerformance = (self.criteria[g]['scale'][1] - \
                    self.criteria[g]['scale'][0]) * position
            for x in actionsKeys:
                self.evaluation[g][x] = Decimal(str(constantPerformance))
                                    
                                    
# ----------------------
class NormalizedPerformanceTableau(PerformanceTableau):
    """
    specialsation of the PerformanceTableau class for
    constructing normalized, 0 - 100, valued PerformanceTableau
    instances from a given argPerfTab instance.
    """
    def __init__(self,argPerfTab=None,lowValue=0,highValue=100,coalition=None,Debug=False):
        import copy
        from decimal import Decimal
        if isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        elif argPerfTab == None:
            print('Error: a valid PerformanceTableau instance is required !')
            perfTab = None
        else:
            perfTab = argPerfTab      
        self.name = 'norm_'+ perfTab.name
        try:
            self.description = copy.deepcopy(perfTab.description)
        except:
            pass
        self.actions = copy.deepcopy(perfTab.actions)
        self.criteria = copy.deepcopy(perfTab.criteria)
        self.evaluation = copy.deepcopy(perfTab.evaluation)
        self.evaluation = self.normalizeEvaluations(lowValue,highValue,Debug)
        criteria = self.criteria        
        for g in criteria:
            if criteria[g]['weight'] < 0:
                criteria[g]['weight'] = -criteria[g]['weight']
            try:
                for th in criteria[g]['thresholds']:
                    empan = Decimal(str(criteria[g]['scale'][1]-criteria[g]['scale'][0]))
                    intercept = criteria[g]['thresholds'][th][0]/empan*(Decimal(str(highValue-lowValue)))
                    slope = criteria[g]['thresholds'][th][1]
                    criteria[g]['thresholds'][th] = (intercept,slope)
            except:
                pass
            criteria[g]['scale'] = [lowValue,highValue]
        self.criteria = criteria
            
        

#########################################
# specializations of the generic PerformanceTableau Class

class _RandomPerformanceTableau(PerformanceTableau):
    """
    Obsolete class definition. Please use the corresponding randomPerfTabs module class instead.
    """
    def __init__(self,numberOfActions = None,\
                 numberOfCriteria = None,\
                 weightDistribution = None,\
                 weightScale=None,\
                 integerWeights=True,\
                 commonScale = [0.0,100.0],\
                 commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0)],\
                 commonMode = None,\
                 valueDigits = 2,\
                 Debug = False):
        import sys,random,time,math
        self.name = 'randomperftab'
        
        # generate actions
        if numberOfActions == None:
            numberOfActions = 13
        actionsIndex = list(range(numberOfActions+1))
        actionsIndex.remove(0)
        actionsList = []
        for a in actionsIndex:
            if a < 10:
                actionName = 'a0'+str(a)
            else:
                actionName = 'a'+str(a)
            actionsList.append(actionName)
        actions = {}
        for x in actionsList:
            actions[x] = {}
            actions[x]['name'] = 'random decision action'
            actions[x]['comment'] = 'RandomPerformanceTableau() generated.'
        self.actions = actions
        # generate criterialist
        if numberOfCriteria == None:
            numberOfCriteria = 7
        criteriaList = []
        criteriaIndex = list(range(numberOfCriteria+1))
        criteriaIndex.remove(0)
        for g in criteriaIndex:
            if g < 10:
                criterionName = 'g0'+str(g)
            else:
                criterionName = 'g'+str(g)
            criteriaList.append(criterionName)
        # generate weights
        if weightDistribution == None:
            weightDistribution = 'random'
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for g in criteriaList:
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
                i += 1
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant' or weightDistribution == 'equiobjectives':
            weightScale = (1,1)
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary
        criteria = {}
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; commonMode='+str(commonMode)
        i = 0
        for g in criteriaList:
            criteria[g] = {}
            criteria[g]['name']='digraphs.RandomPerformanceTableau() instance'
            criteria[g]['comment']=commentString
            try:
                commonThresholds[0]=(Decimal(str(commonThresholds[0][0])),Decimal(str(commonThresholds[0][1])))
                commonThresholds[1]=(Decimal(str(commonThresholds[1][0])),Decimal(str(commonThresholds[1][1])))
                commonThresholds[2]=(Decimal(str(commonThresholds[2][0])),Decimal(str(commonThresholds[2][1])))
                commonThresholds[3]=(Decimal(str(commonThresholds[3][0])),Decimal(str(commonThresholds[3][1])))
             
                criteria[g]['thresholds'] = {'ind':commonThresholds[0],'pref':commonThresholds[1],'weakVeto':commonThresholds[2],'veto':commonThresholds[3]}
            except:
                commonThresholds[0]=(Decimal(str(commonThresholds[0][0])),Decimal(str(commonThresholds[0][1])))
                commonThresholds[1]=(Decimal(str(commonThresholds[1][0])),Decimal(str(commonThresholds[1][1])))
                commonThresholds[2]=(Decimal(str(commonThresholds[2][0])),Decimal(str(commonThresholds[2][1])))                
                criteria[g]['thresholds'] = {'ind':commonThresholds[0],'pref':commonThresholds[1],'veto':commonThresholds[2]}
            #commonScale = (Decimal(str(commonScale[0])),Decimal(str(commonScale[1])))
            criteria[g]['scale'] = commonScale
            if integerWeights:
                criteria[g]['weight'] = weightsList[i]
            else:
                criteria[g]['weight'] = weightsList[i]/sumWeights
            i += 1
        self.criteria = criteria
        # generate evaluations
        if commonMode == None:
            commonMode = ['uniform',None,None]
        t = time.time()
        digits=valueDigits
        random.seed(t)
        evaluation = {}
        if str(commonMode[0]) == 'uniform':          
            for g in criteria:
                evaluation[g] = {}
                for a in actionsList:
                    ## randeval = random.randint(commonScale[0],commonScale[1])
                    randeval = random.uniform(commonScale[0],commonScale[1])
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
        elif str(commonMode[0]) == 'triangular':
            m = commonScale[0]
            M = commonScale[1]
            if commonMode[1] == None:
                xm = (commonScale[1]-commonScale[0])/2.0
            else:
                xm = commonMode[1]
            if commonMode[2] == None:
                r  = 0.5
            else:
                r  = commonMode[2]
            for g in criteria:
                evaluation[g] = {}
                for a in actionsList:
                    u = random.random()
                    if u < r:
                        randeval = m + math.sqrt(u/r)*(xm-m)                   
                    else:
                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))

        elif str(commonMode[0]) == 'beta':
            m = commonScale[0]
            M = commonScale[1]
            if commonMode[1] == None:
                xm = 0.5
            else:
                xm = commonMode[1]
                
            if commonMode[2] == None:
                if xm > 0.5:
                    beta = 2.0
                    alpha = 1.0/(1-xm)
                else:
                    alpha = 2.0
                    beta = 1.0/xm
            else:
                alpha = commonMode[2][0]
                beta = commonMode[2][1]
            if Debug:
                print('alpha,beta', alpha,beta)
            for g in criteria:
                evaluation[g] = {}
                for a in actionsList:
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    if Debug:
                        print('xm,alpha,beta,u,m,M,randeval',xm,alpha,beta,u,m,M,randeval)

        elif str(commonMode[0]) == 'normal':
            if commonMode[1] == None:
                mu = (commonScale[1]-commonScale[0])/2.0
            else:
                mu = commonMode[1]
            if commonMode[2] == None:
                sigma = (commonScale[1]-commonScale[0])/4.0
            else:
                sigma = commonMode[2]
            for g in criteria:
                evaluation[g] = {}
                for a in actionsList:
                    notfound = True 
                    while notfound:
                        randeval = random.normalvariate(mu,sigma)
                        if randeval >= commonScale[0] and  randeval <= commonScale[1]:
                            notfound = False
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))

        
        else:
            print('mode error in random evaluation generator !!')
            print(str(commonMode[0]))
            #sys.exit(1)
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

# -----------------
class _RandomRankPerformanceTableau(PerformanceTableau):
    """
    Obsolete class definition. Please use the corresponding randomPerfTabs module class instead.
    """
    def __init__(self,numberOfActions = None, numberOfCriteria = None,\
                 weightDistribution = None, weightScale=None,\
                 commonThresholds = None, integerWeights=True,\
                 Debug = False):
        """
            Parameters:
            number of actions,
            number criteria,
            weightDistribution := equisignificant|random (default)
            weightScale=(1,numberOfCriteria (default when random))
            integerWeights = Boolean (True = default) 
            commonThresholds = {'ind':(0,0),'pref':(1,0),'veto':(numberOfActions,0)} (default)
        """
        import sys,random,time,math
        self.name = 'rankperftab'
        
        # generate actions
        if numberOfActions == None:
            numberOfActions = 13
        actionsIndex = list(range(numberOfActions+1))
        actionsIndex.remove(0)
        actionsList = []
        for a in actionsIndex:
            if a < 10:
                actionName = 'a0'+str(a)
            else:
                actionName = 'a'+str(a)
            actionsList.append(actionName)
        actions = {}
        for x in actionsList:
            actions[x] = {}
            actions[x]['name'] = 'random decision action'
            actions[x]['comment'] = 'RandomRankPerformanceTableau() generated.'
        self.actions = actions
        # generate criterialist
        if numberOfCriteria == None:
            numberOfCriteria = 7
        criteriaList = []
        criteriaIndex = list(range(numberOfCriteria+1))
        criteriaIndex.remove(0)
        for g in criteriaIndex:
            if g < 10:
                criterionName = 'g0'+str(g)
            else:
                criterionName = 'g'+str(g)
            criteriaList.append(criterionName)
        # generate weights
        if weightDistribution == None:
            weightDistribution = 'random'
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for g in criteriaList:
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
                i += 1
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightScale = (1,1)
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary
        criteria = {}
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; integerWeights='+str(integerWeights)
        commentString += '; commonThresholds='+str(commonThresholds)
        i = 0
        for g in criteriaList:
            criteria[g] = {}
            criteria[g]['name']='digraphs.RandomRankPerformanceTableau() instance'
            criteria[g]['comment']=commentString
            try:
                indThreshold  =(Decimal(str(commonThresholds['ind'][0])),Decimal(str(commonThresholds['ind'][1])))
                prefThreshold =(Decimal(str(commonThresholds['pref'][0])),Decimal(str(commonThresholds['pref'][1])))
                vetoThreshold =(Decimal(str(commonThresholds['veto'][0])),Decimal(str(commonThresholds['veto'][1])))
             
                criteria[g]['thresholds'] = {'ind':indThreshold,'pref':prefThreshold,'veto':vetoThreshold}
            except:
                indThreshold  = ( Decimal("0"), Decimal("0") )
                prefThreshold = ( Decimal("1"), Decimal("0") )
                vetoThreshold = ( Decimal(str(numberOfActions)), Decimal("0") )               
                criteria[g]['thresholds'] = { 'ind':indThreshold,\
                                              'pref':prefThreshold,\
                                              'veto': vetoThreshold
                                              }
            commonScale = ( Decimal("0"), Decimal(numberOfActions) )
            criteria[g]['scale'] = commonScale
            if integerWeights:
                criteria[g]['weight'] = weightsList[i]
            else:
                criteria[g]['weight'] = weightsList[i]/sumWeights
            i += 1
        self.criteria = criteria
        # generate evaluations
        t = time.time()
        random.seed(t)
        evaluation = {}       
        for g in criteria:
            evaluation[g] = {}
            choiceRange = list(range(1,numberOfActions+1))
            for a in actionsList:
                randeval = random.choice(choiceRange)
                evaluation[g][a] = Decimal( str(randeval) )
                choiceRange.remove(randeval)
        
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

# ------------------------------


class _FullRandomPerformanceTableau(PerformanceTableau):
    """
    Obsolete class definition. Please use the corresponding randomPerfTabs module class instead.
    """

    def __init__(self,numberOfActions = None, numberOfCriteria = None, weightDistribution = None, weightScale=None, integerWeights = True, commonScale = None, commonThresholds = None, commonMode = None, valueDigits=2,Debug = False):
        import sys,random,time,math
        self.name = 'fullrandomperftab'
        # randomizer init
        t = time.time()
        random.seed(t)
        # generate random actions
        if numberOfActions == None:
            numberOfActions = random.randint(10,31)
        actionsIndex = list(range(numberOfActions+1))
        actionsIndex.remove(0)
        actionsList = []
        for a in actionsIndex:
            if a < 10:
                actionName = 'a0'+str(a)
            else:
                actionName = 'a'+str(a)
            actionsList.append(actionName)
        actions = {}
        for x in actionsList:
            actions[x] = {}
            actions[x]['name'] = 'random decision action'
            actions[x]['comment'] = 'FullRandomPerformanceTableau() generated.'
        self.actions = actions
        # generate random criterialist
        if numberOfCriteria == None:
            numberOfCriteria = random.randint(5,21)
        criteriaList = []
        criteriaIndex = list(range(numberOfCriteria+1))
        criteriaIndex.remove(0)
        for g in criteriaIndex:
            if g < 10:
                criterionName = 'g0'+str(g)
            else:
                criterionName = 'g'+str(g)
            criteriaList.append(criterionName)
        # generate random weights
        if weightDistribution == None:
            majorityWeight = numberOfCriteria + 1
            #weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('fixed',[1,majorityWeight],4)]
            weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3)]
            weightMode = random.choice(weightModesList)
            weightDistribution = weightMode[0]
            weightScale =  weightMode[1]
        else:
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightMode=[weightDistribution,weightScale]
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = 0.0
            i = 0
            for g in criteriaList:
                weightsList.append(random.randint(weightScale[0],weightScale[1]))
                sumWeights += weightsList[i]
                i += 1
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = 0.0
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(weightScale[1])
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(weightScale[0])
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant' or weightDistribution == 'equiobjectives':
            weightScale = (1,1)
            weightsList = []
            sumWeights = 0.0
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(weightScale[1])
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(weightScale[0])
                    sumWeights += weightScale[0]
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary with random thresholds
        if commonScale == None:
            commonScale = [0.0,100.0]
        criteria = {}
        i = 0
        for g in criteriaList:
            criteria[g] = {}
            criteria[g]['name'] = 'random criterion'
            t = time.time()
            if commonThresholds == None:        
                thresholds = []
                thresholds.append((round(random.uniform(0.0,commonScale[1]/5.0),valueDigits),0.0))
                thresholds.append((round(random.uniform(thresholds[0][0],commonScale[1]/3.0),valueDigits),0.0))
                thresholds.append((round(random.uniform(commonScale[1]*2.0/3.0,commonScale[1]),valueDigits),0.0))
                thresholds.append((round(random.uniform(thresholds[2][0],commonScale[1]),valueDigits),0.0))
                
            else:
                thresholds = commonThresholds
            ## print thresholds
            try:
                criteria[g]['thresholds'] = {
                    'ind':(Decimal(str(thresholds[0][0])),Decimal(str(thresholds[0][1]))),
                    'pref':(Decimal(str(thresholds[1][0])),Decimal(str(thresholds[1][1]))),
                    'weakVeto':(Decimal(str(thresholds[2][0])),Decimal(str(thresholds[2][1]))),
                    'veto':(Decimal(str(thresholds[3][0])),Decimal(str(thresholds[3][1]))),
                    }
            except:
                criteria[g]['thresholds'] = {
                    'ind':(Decimal(str(thresholds[0][0])),Decimal(str(thresholds[0][1]))),
                    'pref':(Decimal(str(thresholds[1][0])),Decimal(str(thresholds[1][1]))),
                    'veto':(Decimal(str(thresholds[2][0])),Decimal(str(thresholds[2][1]))),
                    }               
            criteria[g]['scale'] = commonScale
            if integerWeights:
                criteria[g]['weight'] = Decimal(str(weightsList[i]))
            else:
                criteria[g]['weight'] = Decimal(str(weightsList[i]))/Decimal(str(sumWeights))
            i += 1
        # generate random evaluations
        x30=commonScale[1]*0.3
        x50=commonScale[1]*0.5
        x70=commonScale[1]*0.7
        randomLawsList = [['uniform',commonScale[0],commonScale[1]],
                          ('triangular',x30,0.33),('triangular',x30,0.50),('triangular',x30,0.75),
                          ('triangular',x50,0.33),('triangular',x50,0.50),('triangular',x50,0.75),
                          ('triangular',x70,0.33),('triangular',x70,0.50),('triangular',x70,0.75),
                          ('normal',x30,20.0),('normal',x30,25.0),('normal',x30,30.0),
                          ('normal',x50,20.0),('normal',x50,25.0),('normal',x50,30.0),
                          ('normal',x70,20.0),('normal',x70,25.0),('normal',x70,30.0)]
        evaluation = {}
        for g in criteriaList:
            evaluation[g] = {}
            if commonMode == None:
                randomMode = random.choice(randomLawsList)
            else:
                randomMode = commonMode
            if randomMode[0] == 'uniform':
                randomMode[1] = commonScale[0]
                randomMode[2] = commonScale[1]
            criteria[g]['randomMode'] = randomMode
            if randomMode[0] != 'beta':
                if randomMode[1] == None and randomMode[2] == None:
                    commentString = randomMode[0] + ', default, default'
                elif randomMode[1] != None and randomMode[2] == None:
                    commentString = randomMode[0]+', %.2f, default' % float(randomMode[1])
                elif randomMode[1] == None and randomMode[2] != None:
                    commentString = randomMode[0]+', default, %.2f' % (float(randomMode[2]))
                else:
                    commentString = randomMode[0]+', %.2f, %.2f' % (float(randomMode[1]),float(randomMode[2]))
            else:
                if randomMode[1] != None and randomMode[2] != None:
                    commentString = randomMode[0]+', %.2f, (%.4f,%.4f)' % (float(randomMode[1]),float(randomMode[2][0]),float(randomMode[2][1]))
                elif randomMode[1] == None and randomMode[2] != None:
                    commentString = randomMode[0]+', default, (%.4f,%.4f)' % (float(randomMode[2][0]),float(randomMode[2][1]))
                if randomMode[1] != None and randomMode[2] == None:
                    commentString = randomMode[0]+', %.2f, default' % (float(randomMode[1]))
                else:
                    commentString = randomMode[0]+', default,default'
                    
                
            criteria[g]['comment'] = 'Evaluation generator: '+commentString
            digits = valueDigits
            if str(randomMode[0]) == 'uniform':          
                evaluation[g] = {}
                for a in actionsList:
                    randeval = random.uniform(commonScale[0],commonScale[1])
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
            elif str(randomMode[0]) == 'triangular':
                m = commonScale[0]
                M = commonScale[1]
                try:
                    if commonMode[1] == None:
                        xm = (M-m)/2.0
                    else:
                        xm = commonMode[1]
                except:
                    xm = (M-m)/2.0
                try:    
                    if commonMode[2] == None:
                        r  = 0.5
                    else:
                        r  = commonMode[2]
                except:
                    r  = 0.5
                for a in actionsList:
                    u = random.random()
                    if u < r:
                        randeval = m + math.sqrt(u/r)*(xm-m)                
                    else:
                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))

            elif str(randomMode[0]) == 'normal':
                try:
                    if commonMode[1] == None:
                        mu = (commonScale[1]-commonScale[0])/2.0
                    else:
                        mu = commonMode[1]
                except:
                    mu = (commonScale[1]-commonScale[0])/2.0
                try:
                    if commonMode[2] == None:
                        sigma = (commonScale[1]-commonScale[0])/4.0
                    else:
                        sigma = commonMode[2]
                except:
                    sigma = (commonScale[1]-commonScale[0])/4.0
                for a in actionsList:
                    notfound = True 
                    while notfound:
                        randeval = random.normalvariate(mu,sigma)
                        if randeval >= commonScale[0] and  randeval <= commonScale[1]:
                            notfound = False
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))

            elif str(randomMode[0]) == 'beta':
                m = commonScale[0]
                M = commonScale[1]
                if commonMode[1] == None:
                    xm = 0.5
                else:
                    xm = commonMode[1]
                
                if commonMode[2] == None:
                    if xm > 0.5:
                        beta = 2.0
                        alpha = 1.0/(1.0 - xm)
                    else:
                        alpha = 2.0
                        beta = 1.0/xm
                else:
                    alpha = commonMode[2][0]
                    beta = commonMode[2][1]
                if Debug:
                    print('alpha,beta', alpha,beta)
                for a in actionsList:
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    if Debug:
                        print('xm,alpha,beta,u,m,M,randeval',xm,alpha,beta,u,m,M,randeval)
                    
        # install self object attributes

        self.criteriaWeightMode = weightMode
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()


    def showAll(self):
        """
        Show fonction for performance tableau of full random outranking digraph.
        """
        criteria = self.criteria
        evaluation = self.evaluation
        print('*-------- show performance tableau -------*')
        print('Name         :', self.name)
        print('Actions      :', self.actions)
        print('Criteria     :')       
        for g in criteria:
            print('  criterion name:', g, end=' ')
            print(', scale: ', criteria[g]['scale'], end=' ')
            print(', weight: %.3f ' % (criteria[g]['weight']))
            print('  thresholds:', criteria[g]['thresholds'])
            print('  evaluations generation mode: ', criteria[g]['randomMode'])
            print()
        print('  Weights generation mode: ', self.criteriaWeightMode)
        print('  Weights preorder       : ', self.weightPreorder)
        print('Evaluations            :')
        for g in evaluation:
            print(g, evaluation[g])

class _RandomCoalitionsPerformanceTableau(PerformanceTableau):
    """
    Obsolete class definition. Please use the corresponding randomPerfTabs module class instead.
    """

    def __init__(self,numberOfActions = None, numberOfCriteria = None,
                 weightDistribution = None, weightScale=None,
                 integerWeights = True, commonScale = None,
                 commonThresholds = None, commonMode = None,
                 valueDigits=2, Coalitions=True, VariableGenerators=True,
                 OrdinalScales=False, Debug=False, RandomCoalitions=False,
                 vetoProbability=None, Electre3=True):
        
        import sys,random,time,math
        self.name = 'randomCoalitionsPerfTab'
        # randomizer init
        t = time.time()
        random.seed(t)
        if RandomCoalitions:
            Coalitions=False
        # generate random actions
        if numberOfActions == None:
            #numberOfActions = random.randint(10,31)
            numberOfActions = 20
        actionsIndex = list(range(numberOfActions+1))
        actionsIndex.remove(0)
        actionsList = []
        for a in actionsIndex:
            if a < 10:
                actionName = 'a0'+str(a)
            else:
                actionName = 'a'+str(a)
            actionsList.append(actionName)
        actions = {}
        for x in actionsList:
            actions[x] = {}
            actions[x]['name'] = 'random decision action'
            actions[x]['comment'] = 'RandomCoalitionsPerformanceTableau() generated.'
            actions[x]['generators'] = {}
        self.actions = actions
        # generate random criterialist
        if numberOfCriteria == None:
            ## numberOfCriteria = random.randint(5,21)
            numberOfCriteria = 13
        criteriaList = []
        criteriaIndex = list(range(numberOfCriteria+1))
        criteriaIndex.remove(0)
        for g in criteriaIndex:
            if g < 10:
                criterionName = 'g0'+str(g)
            else:
                criterionName = 'g'+str(g)
            criteriaList.append(criterionName)
        # generate random weights
        if weightDistribution == None:
            ## majorityWeight = numberOfCriteria + 1
            ## #weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('fixed',[1,majorityWeight],4)]
            ## weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3)]
            ## weightMode = random.choice(weightModesList)
            weightMode = ('equisignificant',(1,1))
            weightDistribution = weightMode[0]
            weightScale =  weightMode[1]
        else:
            weightMode=[weightDistribution,weightScale]
        if weightDistribution == 'random':
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for g in criteriaList:
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
                i += 1
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            if weightScale == None:
                weightScale = (1,numberOfCriteria)            
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant'\
          or weightDistribution == 'equiobjectives'\
          or weightDistribution == 'equicoalitions':
            weightScale = (1,1)            
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary with random thresholds
        if commonScale == None:
            commonScale = (0.0,100.0)
        if Coalitions:
            criterionCoalitionsList=[('A',None),('B',None),('C',None)]
        elif RandomCoalitions:
            bin = {}
            nbrcrit = len(criteriaList)
            for i in range(nbrcrit):
                bin[i] = set()
            for i in range(nbrcrit):
                p = random.randint(0,nbrcrit-1)
                bin[p].add(criteriaList[i])
            partition = []
            for i in range(nbrcrit):
                ni = len(bin[i])
                if ni > 0:
                    partition.append((ni,bin[i]))
            partition.sort(reverse=True)
            criterionCoalitionsList = []
            for i in range(len(partition)):
                criterionCoalitionsList.append((chr(ord("A")+i),partition[i][1]))
            Coalitions = True
            if Debug:
                print(criterionCoalitionsList)
        criteria = {}

        for gi in range(len(criteriaList)):
            g = criteriaList[gi]
            criteria[g] = {}
            if RandomCoalitions:
                for criterionCoalition in criterionCoalitionsList:
                    if g in criterionCoalition[1]:
                        criteria[g]['coalition'] = criterionCoalition[0]
                        if Debug:
                            print('==>>>', criteria[g]['coalition'])
            elif Coalitions:
                criterionCoalition = random.choice(criterionCoalitionsList)
                criteria[g]['coalition'] = criterionCoalition[0]
            criteria[g]['preferenceDirection'] = 'max'           
            if Coalitions:
                criteria[g]['name'] = 'random criterion of coalition %s' % (criteria[g]['coalition'])
            else:
                criteria[g]['name'] = 'random criterion'            
            t = time.time()
            if commonThresholds == None:        
                ## thresholds = []
                ## thresholds.append((round(random.uniform(0.0,commonScale[1]/5.0),valueDigits),0.0))
                ## thresholds.append((round(random.uniform(thresholds[0][0],commonScale[1]/3.0),valueDigits),0.0))
                ## thresholds.append((round(random.uniform(commonScale[1]*2.0/3.0,commonScale[1]),valueDigits),0.0))
                ## thresholds.append((round(random.uniform(thresholds[2][0],commonScale[1]),valueDigits),0.0))
                
                if OrdinalScales:
                    thresholds = [(1.0,0.0),(2.001,0.0),(8.001,0.0)]
                else:
                    span = commonScale[1] - commonScale[0]
                    thresholds = [(0.05001*span,0),(0.10001*span,0.0),(0.60001*span,0.0)]
            else:
                thresholds = commonThresholds
            ## print thresholds
            if Electre3:
                thitems = ['ind','pref','veto']
            else:
                thitems = ['ind','pref','weakVeto','veto']
            if vetoProbability != None:
                randVeto = random.uniform(0.0,1.0)
                if randVeto > vetoProbability:
                    thitems = ['ind','pref']
            criteria[g]['thresholds'] = {}
            for t in range(len(thitems)):
                criteria[g]['thresholds'][thitems[t]] =\
                   (Decimal(str(thresholds[t][0])),Decimal(str(thresholds[t][1])))
                
            criteria[g]['scale'] = commonScale
            if integerWeights:
                criteria[g]['weight'] = weightsList[gi]
            else:
                criteria[g]['weight'] = weightsList[gi] / sumWeights

        # determine equisignificant coalitions
        coalitionsCardinality = {}
        for gi in range(len(criteriaList)):
            g = criteriaList[gi]
            try:
                coalitionsCardinality[criteria[g]['coalition']] += 1
            except:
                coalitionsCardinality[criteria[g]['coalition']] = 1
        if Debug:
            print(coalitionsCardinality)
        weightsProduct = 1
        for coalition in coalitionsCardinality:
            weightsProduct *= coalitionsCardinality[coalition]
        if Debug:
            print(weightsProduct)
        if weightDistribution == 'equicoalitions':
            for gi in range(len(criteriaList)):
                g = criteriaList[gi]
                criteria[g]['weight'] =\
                    weightsProduct // coalitionsCardinality[criteria[g]['coalition']]
                if Debug:
                    print(criteria[g]['weight'])
                
        # allocate (criterion,action) to coalition supporting type
        if Coalitions:
            coalitionSupportingType = ['+','~','-']
            for x in actionsList:
                for c in criterionCoalitionsList:
                    if Debug:
                        print(criterionCoalitionsList,c)
                    self.actions[x][str(c[0])]=random.choice(coalitionSupportingType)
                    self.actions[x]['name'] =\
                        self.actions[x]['name'] + ' '+ str(c[0]) + str(self.actions[x][str(c[0])])                
                    
        # generate evaluations
        evaluation = {}
        for g in criteriaList:
            evaluation[g] = {}
            if commonMode == None:
                #randomMode = random.choice(randomLawsList)
                randomMode = ['triangular',50.0,0.50]               
            else:
                randomMode = commonMode
            if randomMode[0] == 'uniform':
                randomMode[1] = commonScale[0]
                randomMode[2] = commonScale[1]
                
            criteria[g]['randomMode'] = randomMode
            if Coalitions:
                commentString = 'Variable '+randomMode[0]+(' performance generator with random low (-), medium (~) or high (+) parameters.')
            else:
                if randomMode[0] == 'triangular':
                    if VariableGenerators:
                        commentString = 'triangular law with variable mode (m) and probability repartition (p).'
                    else:
                        commentString = 'triangular law with constant mode (m) and probability repartition (p).'

                else:
                    if VariableGenerators:
                        commentString = 'Variable '+randomMode[0]+(' law with randomly chosen low, medium or high parameters.')
                    ## elif Coalitions:
                    ##     commentString = 'Coalition : %s ' % (criteria[g]['coalition'])
                    else:
                        commentString = 'Constant '+randomMode[0]+(' law with parameters = %s, %s' % (str(randomMode[1]),str(randomMode[2])))
                    
            criteria[g]['comment'] = commentString
            digits = valueDigits
            
            if str(randomMode[0]) == 'uniform':          
                for a in actionsList:
                    
                    if VariableGenerators:
                        randomRangesList = [(commonScale[0],commonScale[1]), (commonScale[0],commonScale[0]+0.3*(commonScale[1]-commonScale[0])), (commonScale[0],commonScale[0]+0.7*(commonScale[1]-commonScale[0]))]
                        randomRange = random.choice(randomRangesList)         
                        randeval = random.uniform(randomRange[0],randomRange[1])
                    else:
                        randomRange = (randomMode[1],randomMode[2]) 
                        randeval = random.uniform(randomMode[1],randomMode[2])
                    self.actions[a]['generators'][g] = (randomMode[0],randomRange)
                    if OrdinalScales:
                        randeval /= 10.0
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))

            elif str(randomMode[0]) == 'beta':
                for a in actionsList:
                    m = commonScale[0]
                    M = commonScale[1]
                    if Coalitions:
                        if self.actions[a][criteria[g]['coalition']] == '+':
                            # mode = 75, stdev = 15
                            #xm = 75
                            alpha = 5.8661
                            beta = 2.62203
                        elif self.actions[a][criteria[g]['coalition']] == '~':
                            # nmode = 50, stdev = 15
                            #xm = 50
                            alpha = 5.05556
                            beta = 5.05556
                        elif self.actions[a][criteria[g]['coalition']] == '-':
                            # mode = 25, stdev = 15
                            # xm = 25
                            alpha = 2.62203
                            beta = 5.8661                         
                    else:
                        if VariableGenerators:
                            randomModesList = [0.3,0.5,0.7]
                            xm = random.choice(randomModesList)
                        else:
                            xm = randomMode[1]
                        if xm > 0.5:
                            beta = 2.0
                            alpha = 1.0/(1-xm)
                        else:
                            alpha = 2.0
                            beta = 1.0 / xm
                    if Debug:
                        print('alpha,beta', alpha,beta)
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    if Debug:
                        print('xm,alpha,beta,u,m,M,randeval',xm,alpha,beta,u,m,M,randeval)
                    self.actions[a]['generators'][g] = ('beta',alpha,beta)
                    if OrdinalScales:
                        randeval /= 10.0
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
    
            elif str(randomMode[0]) == 'triangular':
                for a in actionsList:
                    m = commonScale[0]
                    M = commonScale[1]
                    if VariableGenerators:
                        randomModesList = [30.0,50.0,70.0]
                        xm = random.choice(randomModesList)
                    else:
                        xm = randomMode[1]
                    r  = randomMode[2]
                    self.actions[a]['generators'][g] = (randomMode[0],xm,r)
                    u = random.random()
                    #print 'm,xm,M,r,u', m,xm,M,r,u 
                    if u < r:
                        #randeval = m + (math.sqrt(r*u*(m-xm)**2))/r
                        randeval = m + math.sqrt(u/r)*(xm-m)
                    else:
                        #randeval = (M*r - M + math.sqrt((-1+r)*(-1+u)*(M-xm)**2))/(-1+r)
                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
                    if OrdinalScales:
                        randeval /= 10.0
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                   
                    #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]

     
            ## elif str(randomMode[0]) == 'normal':
            ##     mu = randomMode[1]
            ##     sigma = randomMode[2]
            ##     for a in actionsList:
            ##         notfound = True 
            ##         while notfound:
            ##             randeval = random.normalvariate(mu,sigma)
            ##             if randeval >= commonScale[0] and  randeval <= commonScale[1]:
            ##                 notfound = False
            ##         evaluation[g][a] = Decimal(str(round(randeval,digits)))
        # install self object attributes

        self.criteriaWeightMode = weightMode
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

class _RandomS3PerformanceTableau(_RandomCoalitionsPerformanceTableau):
    """
    Obsolete dummy class for backports.
    """

class _RandomCBPerformanceTableau(PerformanceTableau):
    """
    Obsolete class definition. Please use the corresponding randomPerfTabs module class instead.
    """


    def __init__(self,numberOfActions = None, \
                 numberOfCriteria = None, \
                 weightDistribution = None,
                 weightScale=None,\
                 integerWeights = True,
                 commonScale = None, commonThresholds = None,\
                 commonPercentiles= None,\
                 commonMode = None,\
                 valueDigits=2, Debug=False,Comments=False):
        """
        Constructor for RadomCBPerformanceTableau instances.
        
        """

        import sys,random,time,math,copy
        
        self.name = 'randomCBperftab'
        # randomizer init
        t = time.time()
        random.seed(t)
        # generate random actions
        if numberOfActions == None:
            numberOfActions = random.randint(10,31)
        actionsIndex = list(range(numberOfActions+1))
        actionsIndex.remove(0)
        actionsList = []
        for a in actionsIndex:
            if a < 10:
                actionName = 'a0'+str(a)
            else:
                actionName = 'a'+str(a)
            actionsList.append(actionName)
        actions = {}
        actionsTypesList = ['cheap','neutral','advantageous']
        for x in actionsList:
            actions[x] = {}
            actions[x]['type'] = random.choice(actionsTypesList)
            actions[x]['name'] = 'random %s decision action' % (actions[x]['type'])
            actions[x]['comment'] = 'RandomCBPerformanceTableau() generated.'
        self.actions = actions

        # generate random criterialist
        if numberOfCriteria == None:
            numberOfCriteria = random.randint(5,21)
        criteriaList = []
        criteriaIndex = list(range(numberOfCriteria+1))
        criteriaIndex.remove(0)
        for g in criteriaIndex:
            if g < 10:
                criterionName = 'g0'+str(g)
            else:
                criterionName = 'g'+str(g)
            criteriaList.append(criterionName)
        if Debug:
            print(criteriaList)
            
        # generate criteria dictionary
        ## if commonScale == None:
        ##     commonScale = (0.0,100.0)
        criterionTypesList = ['max','max','min']
        minScaleTypesList = ['cardinal','cardinal','cardinal','ordinal']
        maxScaleTypesList = ['ordinal','ordinal','cardinal']
        criteria = {}
        i = 0
        criterionTypeCounter = {'min':0,'max':0}
        for g in criteriaList:
            #criterionScale = commonScale
            criteria[g] = {}
            criterionType = random.choice(criterionTypesList)
            criterionTypeCounter[criterionType] += 1
            criteria[g]['preferenceDirection'] = criterionType
            if criterionType == 'min':
                scaleType = random.choice(minScaleTypesList)
            else:
                scaleType = random.choice(maxScaleTypesList)
            criteria[g]['scaleType'] = scaleType
            if criterionType == 'min':
                if scaleType == 'ordinal':
                    criteria[g]['name'] = 'random ordinal cost criterion'
                else:
                    criteria[g]['name'] = 'random cardinal cost criterion'
            else:
                if scaleType == 'ordinal':
                    criteria[g]['name'] = 'random ordinal benefit criterion'
                else:
                    criteria[g]['name'] = 'random cardinal benefit criterion'
            ## t = time.time()
            ## random.seed(t)
            if Debug:
                print("g, criteria[g]['scaleType'], criteria[g]['scale']", g, criteria[g]['scaleType'], end=' ')

            # commonScale parameter is obsolete
            commonScale = None
            if criteria[g]['scaleType'] == 'cardinal':
                #if commonScale == None:
                criterionScale = (0.0, 100.0)
                ## criteria[g]['scale'] = criterionScale      
            elif criteria[g]['scaleType'] == 'ordinal':
                ## if Debug:
                ##     print commonScale
                ## if commonScale == None:
                ##     criterionScale = (0, 10)
                ## else:
                criterionScale = (0, 10)
            else:
                criterionScale = (0.0, 100.0)
            criteria[g]['scale'] = criterionScale
            if Debug:
                print(criteria[g]['scale'])

        # generate random weights
        if weightDistribution == None:
            ## weightDistribution = 'equiobjectives'
            weightDistribution = 'fixed'
            weightScale = (1,1)
            weightMode=[weightDistribution,weightScale]
            ## majorityWeight = numberOfCriteria + 1
            ## #weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('fixed',[1,majorityWeight],4)]
            ## weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('balanced',[1,1],4)]
            ## weightMode = random.choice(weightModesList)
            ## weightDistribution = weightMode[0]
            ## weightScale =  weightMode[1]
        else:
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightMode=[weightDistribution,weightScale]
            
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for g in criteriaList:
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
                i += 1
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightScale = (1,1)
            weightMode=[weightDistribution,weightScale]
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if g == 'g1':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equiobjectives':
            weightScale = (max(1,criterionTypeCounter['min']),max(1,criterionTypeCounter['max']))
            weightMode=[weightDistribution,weightScale]
            weightsList = []
            sumWeights = Decimal('0.0')
            for g in criteriaList:
                if criteria[g]['preferenceDirection'] == 'min':
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))
        if Debug:
            print(weightsList, sumWeights)

        for i,g in enumerate(criteriaList):
            ## if Debug:
            ##     print 'criterionScale = ', criterionScale
            if integerWeights:
                criteria[g]['weight'] = weightsList[i]
            else:
                criteria[g]['weight'] = weightsList[i] / sumWeights
            i += 1

            if Debug:
                print(criteria[g])

        # generate random evaluations
        ## x30=criterionScale[1]*0.3
        ## x50=criterionScale[1]*0.5
        ## x70=criterionScale[1]*0.7
        ## if Debug:
        ##     print 'g, x30,x50,x70', g, x30,x50,x70
        ## randomLawsList = [['uniform',criterionScale[0],criterionScale[1]],
        ##                   ('triangular',x30,0.33),('triangular',x30,0.50),('triangular',x30,0.75),
        ##                   ('triangular',x50,0.33),('triangular',x50,0.50),('triangular',x50,0.75),
        ##                   ('triangular',x70,0.33),('triangular',x70,0.50),('triangular',x70,0.75),
        ##                   ('normal',x30,20.0),('normal',x30,25.0),('normal',x30,30.0),
        ##                   ('normal',x50,20.0),('normal',x50,25.0),('normal',x50,30.0),
        ##                   ('normal',x70,20.0),('normal',x70,25.0),('normal',x70,30.0)]
        
        evaluation = {}
        for g in criteriaList:
            criterionScale = criteria[g]['scale']
            amplitude = criterionScale[1] - criterionScale[0]
            x30=criterionScale[0] + amplitude*0.3
            x50=criterionScale[0] + amplitude*0.5
            x70=criterionScale[0] + amplitude*0.7
            if Debug:
                print('g, criterionx30,x50,x70', g, criteria[g], x30,x50,x70)
            evaluation[g] = {}
            if commonMode == None:
                #randomMode = random.choice(randomLawsList)
                randomMode = ['triangular',x50,0.50]               
            elif commonMode[0] == None:
                #randomMode = random.choice(randomLawsList)
                randomMode = ['triangular',x50,0.50]               
            else:
                randomMode = commonMode
            if randomMode[0] == 'uniform':
                randomMode[1] = criterionScale[0]
                randomMode[2] = criterionScale[1]
            criteria[g]['randomMode'] = randomMode
            if randomMode[0] == 'triangular':
                commentString = 'triangular law with variable mode (m) and probability repartition (p = 0.5). Cheap actions: m = 30%; neutral actions: m = 50%; advantageous actions: m = 70%.'
            elif randomMode[0] == 'normal':
                commentString = 'truncated normal law with variable mean (mu) and standard deviation (stdev = 20%). Cheap actions: mu = 30%; neutral actions: mu = 50%; advantageous actions: mu = 70%.'
            elif randomMode[0] == 'beta':
                commentString = 'beta law with variable mode xm and standard deviation (stdev = 15%). Cheap actions: xm = 30%; neutral actions: xm = 50%; advantageous actions: xm = 70%.'

            ## else:
            ##     if randomMode[1] != None and randomMode[2] != None:
            ##         commentString = randomMode[0]+', %.2f, %.2f' % (float(randomMode[1]),float(randomMode[2]))
            ##     elif randomMode[1] != None and randomMode[2] == None:
            ##         commentString = randomMode[0]+', %.2f, default' % (float(randomMode[1]))
            ##     elif randomMode[1] == None and randomMode[2] != None:
            ##         commentString = randomMode[0]+', default, %.2f' % (float(randomMode[2]))
            ##     else:
            ##         commentString = randomMode[0]+', default, default'
                    
            if Debug:
                print('commonMode = ', commonMode)
                print('randomMode = ', randomMode)
                   
            criteria[g]['comment'] = 'Evaluation generator: ' + commentString
            digits = valueDigits
            if str(randomMode[0]) == 'uniform':          
                evaluation[g] = {}
                for a in actionsList:
                    randeval = random.uniform(criterionScale[0],criterionScale[1])
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
            elif str(randomMode[0]) == 'triangular':
                for a in actionsList:
                    m = criterionScale[0]
                    M = criterionScale[1]
                    #r  = randomMode[2]
                    #xm = randomMode[1]
                    if actions[a]['type'] == 'advantageous':
                        xm = x70
                        r = 0.50
                    elif actions[a]['type'] == 'cheap':
                        xm = x30
                        r = 0.50
                    else:
                        xm = x50
                        r = 0.50
                        
                    deltaMinus = 1.0 - (criterionScale[0]/xm)
                    deltaPlus  = (criterionScale[1]/xm) - 1.0

                    u = random.random()
                    #print 'm,xm,M,r,u', m,xm,M,r,u 
                    if u < r:
                        #randeval = m + (math.sqrt(r*u*(m-xm)**2))/r
                        randeval = m + math.sqrt(u/r)*(xm-m)
                    else:
                        #randeval = (M*r - M + math.sqrt((-1+r)*(-1+u)*(M-xm)**2))/(-1+r)
                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
                    
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                    #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]
                        
            elif str(randomMode[0]) == 'normal':
                #mu = randomMode[1]
                #sigma = randomMode[2]
                for a in actionsList:
                    ## amplitude = criterionScale[1]-criterionScale[0]
                    ## x70 = criterionScale[0] + 0.7 * amplitude
                    ## x50 = criterionScale[0] + 0.5 * amplitude
                    ## x30 = criterionScale[0] + 0.3 * amplitude
                    
                    if actions[a]['type'] == 'advantageous':
                        mu = x70
                        sigma = 0.20 * amplitude
                    elif actions[a]['type'] == 'cheap':
                        mu = x30
                        sigma = 0.20 * amplitude
                    else:
                        mu = x50
                        sigma = 0.25 * amplitude
                    notfound = True 
                    while notfound:
                        randeval = random.normalvariate(mu,sigma)
                        ## if Debug:
                        ##     print 'g,commonScale,randeval', g,commonScale,randeval
                        if randeval >= criterionScale[0] and  randeval <= criterionScale[1]:
                            notfound = False
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
            elif str(randomMode[0]) == 'beta':
                m = criterionScale[0]
                M = criterionScale[1]
                ## if commonMode[1] == None:
                ##     xm = 0.5
                ## else:
                ##     xm = commonMode[1]
                
                ## if commonMode[2] == None:
                ##     if xm > 0.5:
                ##         beta = 2.0
                ##         alpha = 1.0/(1.0 - xm)
                ##     else:
                ##         alpha = 2.0
                ##         beta = 1.0/xm
                ## else:
                ##     alpha = commonMode[2][0]
                ##     beta = commonMode[2][1]
                ## if Debug:
                ##     print 'alpha,beta', alpha,beta
                for a in actionsList:
                    if actions[a]['type'] == 'advantageous':
                        # xm = 0.7 sdtdev = 0.15
                        alpha = 5.8661
                        beta = 2.62203
                    elif actions[a]['type'] == 'cheap':
                        # xm = 0.3, stdev = 0.15
                        alpha = 2.62203
                        beta = 5.8661
                    else:
                        # xm = 0.5, stdev = 0.15
                        alpha = 5.05556
                        beta = 5.05556
                    
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                    ## if Debug:
                    ##     print 'alpha,beta,u,m,M,randeval',alpha,beta,u,m,M,randeval
                        

 
        if Debug:
            print(evaluation)

        ## # restrict ordinal criteria to integer (0 - 10) scale
        ## for g in criteriaList:
        ##     if criteria[g]['scaleType'] == 'ordinal':
        ##         for a in actionsList:
        ##             ## if Debug:
        ##             ##     print 'commonThresholds = ', commonThresholds
        ##             ##     print '-- >>', evaluation[g][a],
        ##             if commonThresholds == None:
        ##                 ## evaluation[g][a] = Decimal(str(round(evaluation[g][a]/Decimal("10.0"),0)))
        ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
        ##             else:
        ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],-1)))
        ##             ## if Debug:
        ##             ##     print evaluation[g][a]
        # restrict ordinal criteria to integer values
        for g in criteriaList:
            if criteria[g]['scaleType'] == 'ordinal':
                for a in actionsList:
                    if Debug:
                        print('-- >>', evaluation[g][a], end=' ')
                    evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
                    if Debug:
                        print(evaluation[g][a])
            
        
            # generate discrimination thresholds
        self.criteriaWeightMode = weightMode
        self.criteria = copy.deepcopy(criteria)
        self.evaluation = copy.deepcopy(evaluation)
        self.weightPreorder = self.computeWeightPreorder()
        performanceDifferences = self.computePerformanceDifferences(NotPermanentDiffs=True,Debug=False)
        if Debug:
            print('commonPercentiles=', commonPercentiles)
        if commonPercentiles == None:
            quantile = {'ind':5, 'pref':10 , 'veto':95}
        else:
            quantile = commonPercentiles
        for c in criteriaList:
            if self.criteria[c]['scaleType'] == 'cardinal':
                self.criteria[c]['thresholds'] = {}
                #vx = self.criteria[c]['performanceDifferences']
                vx = performanceDifferences[c]
                nv = len(vx)
                if Debug:
                    print('=====>',c)
                    print(vx)
                    print(nv)
                threshold = {}
                for x in quantile:
                    if Debug:
                        print('-->', x, quantile[x], end=' ')

                    if quantile[x] == -1:
                        pass
                    else:
                        if quantile[x] == 0:
                            threshold[x] = vx[0]
                        elif quantile[x] == 100:
                            threshold[x] = vx[nv-1]
                        else:
                            kq = int(math.floor(float(quantile[x]*(nv-1))/100.0))
                            r = ((nv-1)*quantile[x])% 100
                            if Debug:
                                print(kq,r, end=' ')

                            ## if kq == nv-1:
                            ##     kqplus = nv-1
                            ## else:
                            ##     kq_1 = kq - 1
                            threshold[x] = vx[kq] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq+1]-vx[kq])
                            if Debug:
                                print(threshold[x])



                for x in threshold:
                    self.criteria[c]['thresholds'][x] = (threshold[x],Decimal('0.0'))

            if Comments:
                print('criteria',c,' default thresholds:')
                print(self.criteria[c]['thresholds'])



##class _ThreadedRandomCBPerformanceTableau(PerformanceTableau):
##    """
##    Full automatic parallel generation of random
##    Cost versus Benefit oriented performance tableaux with multiprocessing ressources
##    Still under construction !
##
##    Parameters:
##        | see the RandomCBPerformanceTableau class
##        | numberOfCores := limit multiprocessing to a given number of computing cores
##
##    .. warning::
##
##        Minimal number of decision actions required is 3 ! 
##
##    """
##
##    def __init__(self, numberOfCores = 8,\
##                 numberOfActions = None, \
##                 numberOfCriteria = None, \
##                 weightDistribution = None,
##                 weightScale=None,\
##                 integerWeights = True,
##                 commonScale = None, commonThresholds = None,\
##                 commonPercentiles= None,\
##                 commonMode = None,\
##                 valueDigits=2, Debug=False,Comments=False):
##        """
##        Constructor for RadomCBPerformanceTableau instances.
##        
##        """
##
##        import sys,random,time,math,copy
##        
##        self.name = 'randomCBperftab'
##        # randomizer init
##        t = time.time()
##        random.seed(t)
##        # generate random actions
##        if numberOfActions == None:
##            numberOfActions = random.randint(10,31)
##        actionsIndex = list(range(numberOfActions+1))
##        actionsIndex.remove(0)
##        actionsList = []
##        for a in actionsIndex:
##            if a < 10:
##                actionName = 'a0'+str(a)
##            else:
##                actionName = 'a'+str(a)
##            actionsList.append(actionName)
##        actions = {}
##        actionsTypesList = ['cheap','neutral','advantageous']
##        for x in actionsList:
##            actions[x] = {}
##            actions[x]['type'] = random.choice(actionsTypesList)
##            actions[x]['name'] = 'random %s decision action' % (actions[x]['type'])
##            actions[x]['comment'] = 'RandomCBPerformanceTableau() generated.'
##        self.actions = actions
##
##        # generate random criterialist
##        if numberOfCriteria == None:
##            numberOfCriteria = random.randint(5,21)
##        criteriaList = []
##        criteriaIndex = list(range(numberOfCriteria+1))
##        criteriaIndex.remove(0)
##        for g in criteriaIndex:
##            if g < 10:
##                criterionName = 'g0'+str(g)
##            else:
##                criterionName = 'g'+str(g)
##            criteriaList.append(criterionName)
##        if Debug:
##            print(criteriaList)
##            
##        # generate criteria dictionary
##        ## if commonScale == None:
##        ##     commonScale = (0.0,100.0)
##        criterionTypesList = ['max','max','min']
##        minScaleTypesList = ['cardinal','cardinal','cardinal','ordinal']
##        maxScaleTypesList = ['ordinal','ordinal','cardinal']
##        criteria = {}
##        i = 0
##        criterionTypeCounter = {'min':0,'max':0}
##        for g in criteriaList:
##            #criterionScale = commonScale
##            criteria[g] = {}
##            criterionType = random.choice(criterionTypesList)
##            criterionTypeCounter[criterionType] += 1
##            criteria[g]['preferenceDirection'] = criterionType
##            if criterionType == 'min':
##                scaleType = random.choice(minScaleTypesList)
##            else:
##                scaleType = random.choice(maxScaleTypesList)
##            criteria[g]['scaleType'] = scaleType
##            if criterionType == 'min':
##                if scaleType == 'ordinal':
##                    criteria[g]['name'] = 'random ordinal cost criterion'
##                else:
##                    criteria[g]['name'] = 'random cardinal cost criterion'
##            else:
##                if scaleType == 'ordinal':
##                    criteria[g]['name'] = 'random ordinal benefit criterion'
##                else:
##                    criteria[g]['name'] = 'random cardinal benefit criterion'
##            ## t = time.time()
##            ## random.seed(t)
##            if Debug:
##                print("g, criteria[g]['scaleType'], criteria[g]['scale']", g, criteria[g]['scaleType'], end=' ')
##
##            # commonScale parameter is obsolete
##            commonScale = None
##            if criteria[g]['scaleType'] == 'cardinal':
##                #if commonScale == None:
##                criterionScale = (0.0, 100.0)
##                ## criteria[g]['scale'] = criterionScale      
##            elif criteria[g]['scaleType'] == 'ordinal':
##                ## if Debug:
##                ##     print commonScale
##                ## if commonScale == None:
##                ##     criterionScale = (0, 10)
##                ## else:
##                criterionScale = (0, 10)
##            else:
##                criterionScale = (0.0, 100.0)
##            criteria[g]['scale'] = criterionScale
##            if Debug:
##                print(criteria[g]['scale'])
##
##        # generate random weights
##        if weightDistribution == None:
##            ## weightDistribution = 'equiobjectives'
##            weightDistribution = 'fixed'
##            weightScale = (1,1)
##            weightMode=[weightDistribution,weightScale]
##            ## majorityWeight = numberOfCriteria + 1
##            ## #weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('fixed',[1,majorityWeight],4)]
##            ## weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('balanced',[1,1],4)]
##            ## weightMode = random.choice(weightModesList)
##            ## weightDistribution = weightMode[0]
##            ## weightScale =  weightMode[1]
##        else:
##            if weightScale == None:
##                weightScale = (1,numberOfCriteria)
##            weightMode=[weightDistribution,weightScale]
##            
##        if weightDistribution == 'random':
##            weightsList = []
##            sumWeights = Decimal('0.0')
##            i = 0
##            for g in criteriaList:
##                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
##                sumWeights += weightsList[i]
##                i += 1
##            weightsList.reverse()
##        elif weightDistribution == 'fixed':
##            weightsList = []
##            sumWeights = Decimal('0.0')
##            for g in criteriaList:
##                if g == 'g1':
##                    weightsList.append(Decimal(str(weightScale[1])))
##                    sumWeights += weightScale[1]
##                else:
##                    weightsList.append(Decimal(str(weightScale[0])))
##                    sumWeights += weightScale[0]
##            weightsList.reverse()
##        elif weightDistribution == 'equisignificant':
##            weightScale = (1,1)
##            weightMode=[weightDistribution,weightScale]
##            weightsList = []
##            sumWeights = Decimal('0.0')
##            for g in criteriaList:
##                if g == 'g1':
##                    weightsList.append(Decimal(str(weightScale[1])))
##                    sumWeights += weightScale[1]
##                else:
##                    weightsList.append(Decimal(str(weightScale[0])))
##                    sumWeights += weightScale[0]
##            weightsList.reverse()
##        elif weightDistribution == 'equiobjectives':
##            weightScale = (max(1,criterionTypeCounter['min']),max(1,criterionTypeCounter['max']))
##            weightMode=[weightDistribution,weightScale]
##            weightsList = []
##            sumWeights = Decimal('0.0')
##            for g in criteriaList:
##                if criteria[g]['preferenceDirection'] == 'min':
##                    weightsList.append(Decimal(str(weightScale[1])))
##                    sumWeights += weightScale[1]
##                else:
##                    weightsList.append(Decimal(str(weightScale[0])))
##                    sumWeights += weightScale[0]
##        else:
##            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))
##        if Debug:
##            print(weightsList, sumWeights)
##
##        for i,g in enumerate(criteriaList):
##            ## if Debug:
##            ##     print 'criterionScale = ', criterionScale
##            if integerWeights:
##                criteria[g]['weight'] = weightsList[i]
##            else:
##                criteria[g]['weight'] = weightsList[i] / sumWeights
##            i += 1
##
##            if Debug:
##                print(criteria[g])
##
##        # generate random evaluations
##        ## x30=criterionScale[1]*0.3
##        ## x50=criterionScale[1]*0.5
##        ## x70=criterionScale[1]*0.7
##        ## if Debug:
##        ##     print 'g, x30,x50,x70', g, x30,x50,x70
##        ## randomLawsList = [['uniform',criterionScale[0],criterionScale[1]],
##        ##                   ('triangular',x30,0.33),('triangular',x30,0.50),('triangular',x30,0.75),
##        ##                   ('triangular',x50,0.33),('triangular',x50,0.50),('triangular',x50,0.75),
##        ##                   ('triangular',x70,0.33),('triangular',x70,0.50),('triangular',x70,0.75),
##        ##                   ('normal',x30,20.0),('normal',x30,25.0),('normal',x30,30.0),
##        ##                   ('normal',x50,20.0),('normal',x50,25.0),('normal',x50,30.0),
##        ##                   ('normal',x70,20.0),('normal',x70,25.0),('normal',x70,30.0)]
##        
##        evaluation = {}
##        for g in criteriaList:
##            criterionScale = criteria[g]['scale']
##            amplitude = criterionScale[1] - criterionScale[0]
##            x30=criterionScale[0] + amplitude*0.3
##            x50=criterionScale[0] + amplitude*0.5
##            x70=criterionScale[0] + amplitude*0.7
##            if Debug:
##                print('g, criterionx30,x50,x70', g, criteria[g], x30,x50,x70)
##            evaluation[g] = {}
##            if commonMode == None:
##                #randomMode = random.choice(randomLawsList)
##                randomMode = ['triangular',x50,0.50]               
##            elif commonMode[0] == None:
##                #randomMode = random.choice(randomLawsList)
##                randomMode = ['triangular',x50,0.50]               
##            else:
##                randomMode = commonMode
##            if randomMode[0] == 'uniform':
##                randomMode[1] = criterionScale[0]
##                randomMode[2] = criterionScale[1]
##            criteria[g]['randomMode'] = randomMode
##            if randomMode[0] == 'triangular':
##                commentString = 'triangular law with variable mode (m) and probability repartition (p = 0.5). Cheap actions: m = 30%; neutral actions: m = 50%; advantageous actions: m = 70%.'
##            elif randomMode[0] == 'normal':
##                commentString = 'truncated normal law with variable mean (mu) and standard deviation (stdev = 20%). Cheap actions: mu = 30%; neutral actions: mu = 50%; advantageous actions: mu = 70%.'
##            elif randomMode[0] == 'beta':
##                commentString = 'beta law with variable mode xm and standard deviation (stdev = 15%). Cheap actions: xm = 30%; neutral actions: xm = 50%; advantageous actions: xm = 70%.'
##
##            ## else:
##            ##     if randomMode[1] != None and randomMode[2] != None:
##            ##         commentString = randomMode[0]+', %.2f, %.2f' % (float(randomMode[1]),float(randomMode[2]))
##            ##     elif randomMode[1] != None and randomMode[2] == None:
##            ##         commentString = randomMode[0]+', %.2f, default' % (float(randomMode[1]))
##            ##     elif randomMode[1] == None and randomMode[2] != None:
##            ##         commentString = randomMode[0]+', default, %.2f' % (float(randomMode[2]))
##            ##     else:
##            ##         commentString = randomMode[0]+', default, default'
##                    
##            if Debug:
##                print('commonMode = ', commonMode)
##                print('randomMode = ', randomMode)
##                   
##            criteria[g]['comment'] = 'Evaluation generator: ' + commentString
##            digits = valueDigits
##            if str(randomMode[0]) == 'uniform':          
##                evaluation[g] = {}
##                for a in actionsList:
##                    randeval = random.uniform(criterionScale[0],criterionScale[1])
##                    if criteria[g]['preferenceDirection'] == 'max':
##                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                    else:
##                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##            elif str(randomMode[0]) == 'triangular':
##                for a in actionsList:
##                    m = criterionScale[0]
##                    M = criterionScale[1]
##                    #r  = randomMode[2]
##                    #xm = randomMode[1]
##                    if actions[a]['type'] == 'advantageous':
##                        xm = x70
##                        r = 0.50
##                    elif actions[a]['type'] == 'cheap':
##                        xm = x30
##                        r = 0.50
##                    else:
##                        xm = x50
##                        r = 0.50
##                        
##                    deltaMinus = 1.0 - (criterionScale[0]/xm)
##                    deltaPlus  = (criterionScale[1]/xm) - 1.0
##
##                    u = random.random()
##                    #print 'm,xm,M,r,u', m,xm,M,r,u 
##                    if u < r:
##                        #randeval = m + (math.sqrt(r*u*(m-xm)**2))/r
##                        randeval = m + math.sqrt(u/r)*(xm-m)
##                    else:
##                        #randeval = (M*r - M + math.sqrt((-1+r)*(-1+u)*(M-xm)**2))/(-1+r)
##                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
##                    
##                    if criteria[g]['preferenceDirection'] == 'max':
##                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                    else:
##                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##                    #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]
##                        
##            elif str(randomMode[0]) == 'normal':
##                #mu = randomMode[1]
##                #sigma = randomMode[2]
##                for a in actionsList:
##                    ## amplitude = criterionScale[1]-criterionScale[0]
##                    ## x70 = criterionScale[0] + 0.7 * amplitude
##                    ## x50 = criterionScale[0] + 0.5 * amplitude
##                    ## x30 = criterionScale[0] + 0.3 * amplitude
##                    
##                    if actions[a]['type'] == 'advantageous':
##                        mu = x70
##                        sigma = 0.20 * amplitude
##                    elif actions[a]['type'] == 'cheap':
##                        mu = x30
##                        sigma = 0.20 * amplitude
##                    else:
##                        mu = x50
##                        sigma = 0.25 * amplitude
##                    notfound = True 
##                    while notfound:
##                        randeval = random.normalvariate(mu,sigma)
##                        ## if Debug:
##                        ##     print 'g,commonScale,randeval', g,commonScale,randeval
##                        if randeval >= criterionScale[0] and  randeval <= criterionScale[1]:
##                            notfound = False
##                    if criteria[g]['preferenceDirection'] == 'max':
##                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                    else:
##                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##            elif str(randomMode[0]) == 'beta':
##                m = criterionScale[0]
##                M = criterionScale[1]
##                ## if commonMode[1] == None:
##                ##     xm = 0.5
##                ## else:
##                ##     xm = commonMode[1]
##                
##                ## if commonMode[2] == None:
##                ##     if xm > 0.5:
##                ##         beta = 2.0
##                ##         alpha = 1.0/(1.0 - xm)
##                ##     else:
##                ##         alpha = 2.0
##                ##         beta = 1.0/xm
##                ## else:
##                ##     alpha = commonMode[2][0]
##                ##     beta = commonMode[2][1]
##                ## if Debug:
##                ##     print 'alpha,beta', alpha,beta
##                for a in actionsList:
##                    if actions[a]['type'] == 'advantageous':
##                        # xm = 0.7 sdtdev = 0.15
##                        alpha = 5.8661
##                        beta = 2.62203
##                    elif actions[a]['type'] == 'cheap':
##                        # xm = 0.3, stdev = 0.15
##                        alpha = 2.62203
##                        beta = 5.8661
##                    else:
##                        # xm = 0.5, stdev = 0.15
##                        alpha = 5.05556
##                        beta = 5.05556
##                    
##                    u = random.betavariate(alpha,beta)
##                    randeval = (u * (M-m)) + m
##                    if criteria[g]['preferenceDirection'] == 'max':
##                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                    else:
##                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##                    ## if Debug:
##                    ##     print 'alpha,beta,u,m,M,randeval',alpha,beta,u,m,M,randeval
##                        
##
## 
##        if Debug:
##            print(evaluation)
##
##        ## # restrict ordinal criteria to integer (0 - 10) scale
##        ## for g in criteriaList:
##        ##     if criteria[g]['scaleType'] == 'ordinal':
##        ##         for a in actionsList:
##        ##             ## if Debug:
##        ##             ##     print 'commonThresholds = ', commonThresholds
##        ##             ##     print '-- >>', evaluation[g][a],
##        ##             if commonThresholds == None:
##        ##                 ## evaluation[g][a] = Decimal(str(round(evaluation[g][a]/Decimal("10.0"),0)))
##        ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
##        ##             else:
##        ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],-1)))
##        ##             ## if Debug:
##        ##             ##     print evaluation[g][a]
##        # restrict ordinal criteria to integer values
##        for g in criteriaList:
##            if criteria[g]['scaleType'] == 'ordinal':
##                for a in actionsList:
##                    if Debug:
##                        print('-- >>', evaluation[g][a], end=' ')
##                    evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
##                    if Debug:
##                        print(evaluation[g][a])
##            
##        
##            # generate discrimination thresholds
##        self.criteriaWeightMode = weightMode
##        self.criteria = copy.deepcopy(criteria)
##        self.evaluation = copy.deepcopy(evaluation)
##        self.weightPreorder = self.computeWeightPreorder()
##        performanceDifferences = self.computePerformanceDifferences(NotPermanentDiffs=True,Debug=False)
##        if Debug:
##            print('commonPercentiles=', commonPercentiles)
##        if commonPercentiles == None:
##            quantile = {'ind':5, 'pref':10 , 'veto':95}
##        else:
##            quantile = commonPercentiles
##        for c in criteriaList:
##            if self.criteria[c]['scaleType'] == 'cardinal':
##                self.criteria[c]['thresholds'] = {}
##                #vx = self.criteria[c]['performanceDifferences']
##                vx = performanceDifferences[c]
##                nv = len(vx)
##                if Debug:
##                    print('=====>',c)
##                    print(vx)
##                    print(nv)
##                threshold = {}
##                for x in quantile:
##                    if Debug:
##                        print('-->', x, quantile[x], end=' ')
##
##                    if quantile[x] == -1:
##                        pass
##                    else:
##                        if quantile[x] == 0:
##                            threshold[x] = vx[0]
##                        elif quantile[x] == 100:
##                            threshold[x] = vx[nv-1]
##                        else:
##                            kq = int(math.floor(float(quantile[x]*(nv-1))/100.0))
##                            r = ((nv-1)*quantile[x])% 100
##                            if Debug:
##                                print(kq,r, end=' ')
##
##                            ## if kq == nv-1:
##                            ##     kqplus = nv-1
##                            ## else:
##                            ##     kq_1 = kq - 1
##                            threshold[x] = vx[kq] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq+1]-vx[kq])
##                            if Debug:
##                                print(threshold[x])
##
##
##
##                for x in threshold:
##                    self.criteria[c]['thresholds'][x] = (threshold[x],Decimal('0.0'))
##
##            if Comments:
##                print('criteria',c,' default thresholds:')
##                print(self.criteria[c]['thresholds'])
               
#############################33
# XML encoded stored PerformanceTableau Class instances
# class XMLPerformanceTableau(PerformanceTableau):
#     """
#     Specialization of the general PerformanceTableau class for reading
#     stored XML formatted instances.
#     """

#     def __init__(self,fileName='testperftabXML'):
#         from xml.sax import make_parser
#         xmlPerformanceTableau = _XMLPerformanceTableauHandler()
#         saxParser = make_parser()
#         saxParser.setContentHandler(xmlPerformanceTableau)
#         fileNameExt = fileName + '.xml'
#         fo = open(fileNameExt,'r')
#         saxParser.parse(fo)
#         self.name = xmlPerformanceTableau.name
#         self.category = xmlPerformanceTableau.category
#         self.subcategory = xmlPerformanceTableau.subcategory  
#         self.actions = xmlPerformanceTableau.actions
#         self.criteria = xmlPerformanceTableau.criteria
#         self.evaluation = xmlPerformanceTableau.evaluation
#         self.weightPreorder = self.computeWeightPreorder()

# class _XMLRubisPerformanceTableau(PerformanceTableau):
#     """
#     Specialization of the general PerformanceTableau class for reading
#     stored XML formatted instances. Using the inbuilt module
#     xml.etree (for Python 2.5+).

#     Param: fileName (without the extension .xml). 
#     """
    
#     def __init__(self,fileName='rubisPerformanceTableau'):
#         from xml.etree import ElementTree
#         try:
#             fileNameExt = fileName + '.xml'
#             fo = open(fileNameExt,mode='r')
#         except:
#             try:
#                 fileNameExt = fileName + '.xmcda'
#                 fo = open(fileNameExt,mode='r')
#             except:
#                 fileNameExt = fileName + '.xmcda2'
#                 fo = open(fileNameExt,mode='r')
#         rubisPerformanceTableau = ElementTree.parse(fo).getroot()
#         self.comment = rubisPerformanceTableau.find('comment').text
#         self.category = rubisPerformanceTableau.attrib['category']
#         self.subcategory = rubisPerformanceTableau.attrib['subcategory']
#         self.name = rubisPerformanceTableau.find('header').find('name').text
#         self.author = rubisPerformanceTableau.find('header').find('author').text
#         self.reference = rubisPerformanceTableau.find('header').find('reference').text
#         actions = {}
#         ## actions['comment'] = rubisPerformanceTableau.find('actions').find('comment').text
#         for x in rubisPerformanceTableau.find('actions').findall('action'):
#             actions[x.attrib['id']] = {}
#             actions[x.attrib['id']]['name'] = x.find('name').text
#             actions[x.attrib['id']]['comment'] = x.find('comment').text
#         self.actions = actions
#         criteria = {}
#         ##criteria['comment'] = rubisPerformanceTableau.find('criteria').find('comment').text
#         for g in rubisPerformanceTableau.find('criteria').findall('criterion'):
#             criteria[g.attrib['id']] = {}
#             criteria[g.attrib['id']]['name'] = g.find('name').text
#             criteria[g.attrib['id']]['comment'] = g.find('comment').text
#             criteria[g.attrib['id']]['scale'] = {}
#             Min = Decimal(g.find('scale').find('min').text)
#             Max = Decimal(g.find('scale').find('max').text)
#             ##criteria[g.attrib['id']]['scale'] = str((Min,Max))
#             criteria[g.attrib['id']]['scale'] = (Min,Max)
#             criteria[g.attrib['id']]['thresholds'] = {}
#             try:
#                 th = self.stripsplit(g.find('thresholds').find('indifference').text)
#                 criteria[g.attrib['id']]['thresholds']['ind'] = (Decimal(str(th[0])),Decimal(str(th[1])))
#             except:
#                 pass
#             try:
#                 th = self.stripsplit(g.find('thresholds').find('weakPreference').text)
#                 criteria[g.attrib['id']]['thresholds']['weakPreference'] = (Decimal(str(th[0])),Decimal(str(th[1])))
#             except:
#                 pass
#             try:
#                 th = self.stripsplit(g.find('thresholds').find('preference').text)
#                 criteria[g.attrib['id']]['thresholds']['pref'] = (Decimal(str(th[0])),Decimal(str(th[1])))
#             except:
#                 pass
#             try:
#                 th = self.stripsplit(g.find('thresholds').find('weakVeto').text)
#                 criteria[g.attrib['id']]['thresholds']['weakVeto'] = (Decimal(str(th[0])),Decimal(str(th[1])))
#             except:
#                 pass
#             try:
#                 th = self.stripsplit(g.find('thresholds').find('veto').text)
#                 criteria[g.attrib['id']]['thresholds']['veto'] = (Decimal(str(th[0])),Decimal(str(th[1])))
#             except:
#                 pass
#                 ## criteria[g.attrib['id']]['thresholds']['veto'] = (Max + 1.0,0.0)
#             criteria[g.attrib['id']]['weight'] = Decimal(g.find('weight').text)     
#         self.criteria = criteria
#         evaluation = {}
#         ##evaluation['comment'] = rubisPerformanceTableau.find('evaluations').find('comment').text
#         for v in rubisPerformanceTableau.find('evaluations').findall('evaluation'):
#             g = v.find('criterionID').text
#             evaluation[g] = {}
#             for x in v.findall('performance'):
#                 evaluation[g][x.find('actionID').text]=Decimal(x.find('value').text)   
#         self.evaluation = evaluation

# ##         self.actions = xmlPerformanceTableau.actions
# ##         self.criteria = xmlPerformanceTableau.criteria
# ##         self.evaluation = xmlPerformanceTableau.evaluation
#         self.weightPreorder = self.computeWeightPreorder()

#     def stripsplit(self,th):
#         """ extract thresholds new Python 3 compatible version """
#         import string
#         ## th = string.split(string.lstrip(string.rstrip(th,')'),'('),',')
#         th = th.rstrip(')')
#         th = th.lstrip('(')
#         th = th.split(',')
#         res = (th[0].strip(),th[1].strip())
#         return res      

# class _OldXMCDAPerformanceTableau(PerformanceTableau):
#     """
#     Specialization of the general PerformanceTableau class for reading
#     stored XMCDA formatted instances. Using the inbuilt module
#     xml.etree (for Python 2.5+).

#     Param: fileName (without the extension .xml or .xmcda). 
#     """
    
#     def __init__(self,fileName='temp'):
#         from xml.etree import ElementTree
#         fileNameExt = fileName + '.xmcda'
#         try:
#             fo = open(fileNameExt,mode='r')
#         except:
#             fileNameExt = fileName + '.xml'
#             try:
#                 fo = open(fileNameExt,mode='r')
#             except:
#                 print("Error: file %s{.xmcda|.xml} not found !" % (fileName))
        
#         xmcdaPerformanceTableau = ElementTree.parse(fo).getroot()
#         # get description
#         description = {}
#         for elem in [x for x in xmcdaPerformanceTableau.find('caseReference').getchildren()]:
#             if elem.tag == 'bibliography':
#                 description[elem.tag] = {'description': {'subSubTitle': 'Bibliography'}}
#                 i = 0
#                 for bibEntry in [x for x in elem.findall('bibEntry')]:
#                     i += 1
#                     description[elem.tag][i] = bibEntry.text 
#             else:
#                 description[elem.tag] = elem.text
#         self.description = description
#         try:
#             self.name = description['name']
#         except:
#             pass
#         try:
#             self.author = description['user']
#         except:
#             pass
#         try:
#             self.reference = description['comment']
#         except:
#             pass
#         # get method Data
#         parameter = {}
#         for elem in [x for x in xmcdaPerformanceTableau.find('methodData').find('parameters').getchildren()]:
#             tag = elem.find('name').text
#             try:
#                 value = elem.find('value').find('label').text
#             except:
#                 try:
#                     value = float(elem.find('value').find('real').text)
#                 except:
#                     value = int(elem.find('value').find('integer').text)                        
#             parameter[tag] = value
#         self.parameter = parameter
#         actions = {}
#         # get alternatives' description
#         description = {}
#         for elem in [x for x in xmcdaPerformanceTableau.find('alternatives').find('description').getchildren()]:
#             description[elem.tag] = elem.text
#         self.actionsDescription = description
#         # get alternatives
#         for x in xmcdaPerformanceTableau.find('alternatives').findall('alternative'):
#             try:
#                 if x.find('status').text == 'active':
#                     Active = True
#                 else:
#                     Active = False
#             except:
#                 Active = True
#             if Active:
#                 actions[x.attrib['id']] = {}
#                 for elem in [y for y in x.find('description').getchildren()]:
#                     actions[x.attrib['id']][elem.tag] = elem.text
#         self.actions = actions
#         criteria = {}
#         # get criteria' description
#         description = {}
#         for elem in [x for x in xmcdaPerformanceTableau.find('criteria').find('description').getchildren()]:
#             description[elem.tag] = elem.text
#         self.criteriaDescription = description
#         ## get criteria
#         for g in xmcdaPerformanceTableau.find('criteria').findall('criterion'):
#             try:
                
#                 if g.find('status').text == 'active':
#                     Active = True
#                 else:
#                     Active = False
#             except:
#                 Active = True
#             if Active:
#                 criteria[g.attrib['id']] = {}
#                 for elem in [y for y in g.find('description').getchildren()]:
#                     criteria[g.attrib['id']][elem.tag] = elem.text
#                 criteria[g.attrib['id']]['scale'] = {}
#                 Min = float(g.find('criterionFunction').find('scale').find('quantitative').find('min').find('real').text)
#                 Max = float(g.find('criterionFunction').find('scale').find('quantitative').find('max').find('real').text)
#                 ##criteria[g.attrib['id']]['scale'] = str((Min,Max))
#                 criteria[g.attrib['id']]['scale'] = (Min,Max)
#                 try:
#                     criteria[g.attrib['id']]['weight'] = float(g.find('significance').find('real').text)
#                 except:
#                     criteria[g.attrib['id']]['weight'] = int(g.find('significance').find('integer').text)
#                 try:
#                     criteria[g.attrib['id']]['preferenceDirection'] = g.find('criterionFunction').find('scale').find('quantitative').find('preferenceDirection').text
#                     if criteria[g.attrib['id']]['preferenceDirection'] == 'min':
#                         pdir = -1
#                     else:
#                         pdir = 1
#                 except:
#                     pdir = 1

#                 criteria[g.attrib['id']]['thresholds'] = {}
#                 for th in g.find('criterionFunction').find('thresholds').findall('threshold'):
#                     try:
#                         try:
#                             intercept = float(th.find('function').find('linear').find('intercept').find('real').text)
#                         except:
#                             intercept = int(th.find('function').find('linear').find('intercept').find('integer').text)
#                         slope = float(th.find('function').find('linear').find('slope').find('real').text)
#                     except:
#                         try:
#                             intercept = float(th.find('function').find('constant').find('real').text)
#                         except:
#                             intercept = float(th.find('function').find('constant').find('integer').text)
#                         slope = 0.0
#                     ## criteria[g.attrib['id']]['thresholds'][th.find('type').text] = (intercept,pdir*slope)
#                     criteria[g.attrib['id']]['thresholds'][th.find('type').text] = (intercept,slope)

#         self.criteria = criteria
#         # get evaluations' description
#         description = {}
#         for elem in [x for x in xmcdaPerformanceTableau.find('performanceTable').find('description').getchildren()]:
#             description[elem.tag] = elem.text
#         self.evaluationDescription = description
#         # get evaluations
#         evaluation = {}
#         for v in xmcdaPerformanceTableau.find('performanceTable').findall('criterionEvaluations'):
#             g = v.find('criterionID').text
#             try:
#                 if self.criteria[g]['preferenceDirection'] == 'min':
#                     pdir = -1
#                 else:
#                     pdir = 1
#             except:
#                 pdir = 1
#             evaluation[g] = {}
#             for x in v.findall('evaluation'):
#                 try:
#                     value = x.find('value').find('integer').text
#                     evaluation[g][x.find('alternativeID').text]=int(value) * pdir
#                 except:
#                     value = x.find('value').find('real').text
#                     evaluation[g][x.find('alternativeID').text]=float(value) * pdir
#         self.evaluation = evaluation
#         # compute weigth preoder
#         self.weightPreorder = self.computeWeightPreorder()

class _XMCDAPerformanceTableau(PerformanceTableau):
    """
    Specialization of the general PerformanceTableau class for reading
    stored XMCDA formatted instances with exact decimal numbers.
    Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param: fileName (without the extension .xml or .xmcda).   
    
    """
    
    def __init__(self,fileName='temp'):
        
        from xml.etree import ElementTree
        
        fileNameExt = fileName + '.xmcda'
        try:
            fo = open(fileNameExt,mode='r')
        except:
            fileNameExt = fileName + '.xml'
            try:
                fo = open(fileNameExt,mode='r')
            except:
                fileNameExt = fileName + '.xmcda2'
                try:
                    fo = open(fileNameExt,mode='r')
                except:
                    print("Error: file %s{.xmcda(2)|.xml} not found !" % (fileName))
        
        xmcdaPerformanceTableau = ElementTree.parse(fo).getroot()
        # get description
        description = {}
        for elem in [x for x in xmcdaPerformanceTableau.find('caseReference').getchildren()]:
            if elem.tag == 'bibliography':
                description[elem.tag] = {'description': {'subSubTitle': 'Bibliography'}}
                i = 0
                for bibEntry in [x for x in elem.findall('bibEntry')]:
                    i += 1
                    description[elem.tag][i] = bibEntry.text 
            else:
                description[elem.tag] = elem.text
        self.description = description
        try:
            self.name = description['name']
        except:
            pass
        try:
            self.author = description['user']
        except:
            pass
        try:
            self.reference = description['comment']
        except:
            pass
        # get method Data
        parameter = {}
        for elem in [x for x in xmcdaPerformanceTableau.find('methodData').find('parameters').getchildren()]:
            tag = elem.find('name').text
            try:
                value = elem.find('value').find('label').text
            except:
                try:
                    value = Decimal(elem.find('value').find('real').text)
                except:
                    value = Decimal(elem.find('value').find('integer').text)                        
            parameter[tag] = value
        self.parameter = parameter
        actions = {}
        # get alternatives' description
        description = {}
        for elem in [x for x in xmcdaPerformanceTableau.find('alternatives').find('description').getchildren()]:
            description[elem.tag] = elem.text
        self.actionsDescription = description
        # get alternatives
        for x in xmcdaPerformanceTableau.find('alternatives').findall('alternative'):
            try:
                if x.find('status').text == 'active':
                    Active = True
                else:
                    Active = False
            except:
                Active = True
            if Active:
                actions[x.attrib['id']] = {}
                for elem in [y for y in x.find('description').getchildren()]:
                    actions[x.attrib['id']][elem.tag] = elem.text
        self.actions = actions
        criteria = {}
        # get criteria' description
        description = {}
        for elem in [x for x in xmcdaPerformanceTableau.find('criteria').find('description').getchildren()]:
            description[elem.tag] = elem.text
        self.criteriaDescription = description
        ## get criteria
        for g in xmcdaPerformanceTableau.find('criteria').findall('criterion'):
            try:
                
                if g.find('status').text == 'active':
                    Active = True
                else:
                    Active = False
            except:
                Active = True
            if Active:
                criteria[g.attrib['id']] = {}
                for elem in [y for y in g.find('description').getchildren()]:
                    criteria[g.attrib['id']][elem.tag] = elem.text
                criteria[g.attrib['id']]['scale'] = {}
                Min = Decimal(g.find('criterionFunction').find('scale').find('quantitative').find('min').find('real').text)
                Max = Decimal(g.find('criterionFunction').find('scale').find('quantitative').find('max').find('real').text)
                ##criteria[g.attrib['id']]['scale'] = str((Min,Max))
                criteria[g.attrib['id']]['scale'] = (Min,Max)
                try:
                    criteria[g.attrib['id']]['weight'] = Decimal(g.find('significance').find('real').text)
                except:
                    criteria[g.attrib['id']]['weight'] = Decimal(g.find('significance').find('integer').text)
                try:
                    criteria[g.attrib['id']]['preferenceDirection'] = g.find('criterionFunction').find('scale').find('quantitative').find('preferenceDirection').text
                    if criteria[g.attrib['id']]['preferenceDirection'] == 'min':
                        pdir = Decimal('-1.0')
                    else:
                        pdir = Decimal('1.0')
                except:
                    pdir = Decimal('1.0')

                criteria[g.attrib['id']]['thresholds'] = {}
                for th in g.find('criterionFunction').find('thresholds').findall('threshold'):
                    try:
                        try:
                            intercept = Decimal(th.find('function').find('linear').find('intercept').find('real').text)
                        except:
                            intercept = Decimal(th.find('function').find('linear').find('intercept').find('integer').text)
                        slope = Decimal(th.find('function').find('linear').find('slope').find('real').text)
                    except:
                        try:
                            intercept = Decimal(th.find('function').find('constant').find('real').text)
                        except:
                            intercept = Decimal(th.find('function').find('constant').find('integer').text)
                        slope = Decimal('0.0')
                    ## criteria[g.attrib['id']]['thresholds'][th.find('type').text] = (intercept,pdir*slope)
                    criteria[g.attrib['id']]['thresholds'][th.find('type').text] = (intercept,slope)

        self.criteria = criteria
        # get evaluations' description
        description = {}
        for elem in [x for x in xmcdaPerformanceTableau.find('performanceTable').find('description').getchildren()]:
            description[elem.tag] = elem.text
        self.evaluationDescription = description
        # get evaluations
        evaluation = {}
        for v in xmcdaPerformanceTableau.find('performanceTable').findall('criterionEvaluations'):
            g = v.find('criterionID').text
            try:
                if self.criteria[g]['preferenceDirection'] == 'min':
                    pdir = Decimal('-1')
                else:
                    pdir = Decimal('1')
            except:
                pdir = Decimal('1')
            evaluation[g] = {}
            for x in v.findall('evaluation'):
                try:
                    value = x.find('value').find('integer').text
                    evaluation[g][x.find('alternativeID').text]=Decimal(value) * pdir
                except:
                    value = x.find('value').find('real').text
                    evaluation[g][x.find('alternativeID').text]=Decimal(value) * pdir
        self.evaluation = evaluation
        # compute weigth preoder
        self.weightPreorder = self.computeWeightPreorder()

class XMCDA2PerformanceTableau(PerformanceTableau):
    """
    Specialization of the general PerformanceTableau class for reading
    stored XMCDA 2.0 formatted instances with exact decimal numbers.
    Using the inbuilt module xml.etree (for Python 2.5+).

    Parameters:
        * fileName is given without the extension ``.xml`` or ``.xmcda``,
        * HasSeparatedWeights in XMCDA 2.0.0 encoding (default = False),
        * HasSeparatedThresholds in XMCDA 2.0.0 encoding (default = False),
        * stringInput: instantiates from an XMCDA 2.0 encoded string argument.
           
    """
    #from collections import OrderedDict
    
    def __init__(self,fileName='temp',HasSeparatedWeights=False,
                 HasSeparatedThresholds=False,stringInput=None,
                 Debug=False):
        
        from xml.etree import ElementTree
        if stringInput == None:
            fileNameExt = fileName + '.xmcda2'
            try:
                fo = open(fileNameExt,mode='r')
            except:
                fileNameExt = fileName + '.xml'
                try:
                    fo = open(fileNameExt,mode='r')
                except:
                    print("Error: file %s{.xmcda2|.xml} not found !" % (fileName))
        else:
            from io import StringIO
            try:
                fo = StringIO(stringInput)
            except:
                print("Error: stringInput %s !" % (str(stringInput)))
            
        XMCDA = ElementTree.parse(fo).getroot()
        # get name
        try:
            self.name = XMCDA.find('projectReference').attrib['name']
        except:
            self.name = 'temp'
        # get description
        description = {}
        for elem in [x for x in XMCDA.find('projectReference').getchildren()]:
            if elem.tag == 'bibliography':
                description[elem.tag] = {'description': {'subSubTitle': 'Bibliography'}}
                i = 0
                for bibEntry in [x for x in elem.findall('bibEntry')]:
                    i += 1
                    description[elem.tag][i] = bibEntry.text 
            else:
                description[elem.tag] = elem.text
        self.description = description
        try:
            self.author = description['user']
        except:
            pass
        try:
            self.reference = description['comment']
        except:
            pass
        # get method Parameters
        parameter = {}
            
        if XMCDA.find('methodParameters').find('parameters') != None:
            for elem in XMCDA.find('methodParameters').find('parameters').findall('parameter'):
                tag = elem.attrib['name']
                try:
                    value = elem.find('value').find('label').text
                except:
                    try:
                        value = Decimal(elem.find('value').find('real').text)
                    except:
                        try:
                            value = Decimal(elem.find('value').find('integer').text)
                        except:
                            value = None
                parameter[tag] = value
                #print tag,value
        self.parameter = parameter
        actions = OrderedDict()
        # get alternatives' description
        description = {}
        for elem in [x for x in XMCDA.find('alternatives').find('description').getchildren()]:
            description[elem.tag] = elem.text
        self.actionsDescription = description
        # get alternatives
        for x in XMCDA.find('alternatives').findall('alternative'):
            try:
                if x.find('active').text == 'true':
                    Active = True
                else:
                    Active = False
            except:
                Active = True
            if Active:
                actions[x.attrib['id']] = {}
                actions[x.attrib['id']]['name'] = x.attrib['name']
                try:
                    for elem in [y for y in x.find('description').getchildren()]:
                        actions[x.attrib['id']][elem.tag] = elem.text
                except:
                    pass
        self.actions = actions
        
        if XMCDA.find('objectives') != None:  # objectives are defined
            objectives = OrderedDict()
            # get objectives' description
            if XMCDA.find('objectives').find('description') != None:
                description = {}
                for elem in [x for x in XMCDA.find('criteria').find('description').getchildren()]:
                    description[elem.tag] = elem.text
                self.objectivesDescription = description
            ## get objectives
            for obj in XMCDA.find('objectives').findall('objective'):
                if Debug:
                    print('converting objective %s data' % obj.attrib['id'])
                try:             
                    if obj.find('active').text == 'true':
                        Active = True
                    else:
                        Active = False
                except:
                    Active = True
                if Active:
                    objectives[obj.attrib['id']] = {}
                    #name
                    objectives[obj.attrib['id']]['name'] =obj.attrib['name']
                    #description
                    for elem in [y for y in obj.find('description').getchildren()]:
                        objectives[obj.attrib['id']][elem.tag] = elem.text
                    if obj.find('weight') != None:
                        try:
                            objectives[obj.attrib['id']]['weight'] = Decimal(obj.find('weight').find('value').find('real').text)
                        except:
                            criteria[obj.attrib['id']]['weight'] = Decimal(obj.find('weight').find('value').find('integer').text)
                    if obj.find('objectiveCriteria') != None:
                        objectives[obj.attrib['id']]['criteria'] = literal_eval(obj.find('objectiveCriteria').text)
            self.objectives = objectives
        else:  # no objectives are given
            pass
        
        criteria = OrderedDict()
        # get criteria' description
        if XMCDA.find('criteria').find('description') != None:
            description = {}
            for elem in [x for x in XMCDA.find('criteria').find('description').getchildren()]:
                description[elem.tag] = elem.text
            self.criteriaDescription = description
        ## get criteria
        for g in XMCDA.find('criteria').findall('criterion'):
            if Debug:
                print('converting criterion %s data' % g.attrib['id'])
            try:             
                if g.find('active').text == 'true':
                    Active = True
                else:
                    Active = False
            except:
                Active = True
            if Active:
                criteria[g.attrib['id']] = {}
                #name
                criteria[g.attrib['id']]['name'] =g.attrib['name']
                #description
                for elem in [y for y in g.find('description').getchildren()]:
                    criteria[g.attrib['id']][elem.tag] = elem.text
                try:
                    criteria[g.attrib['id']]['objective'] = g.find('criterionObjective').text
                except:
                    pass
                #prefrenceDirection
                criteria[g.attrib['id']]['preferenceDirection'] = g.find('scale').find('quantitative').find('preferenceDirection').text
                if criteria[g.attrib['id']]['preferenceDirection'] == 'min':
                    pdir = Decimal('-1')
                else:
                    pdir = Decimal('1')
                #scale
                criteria[g.attrib['id']]['scale'] = {}
                Min = Decimal(g.find('scale').find('quantitative').find('minimum').find('real').text)
                Max = Decimal(g.find('scale').find('quantitative').find('maximum').find('real').text)
                criteria[g.attrib['id']]['scale'] = (Min,Max)
                ##criteria[g.attrib['id']]['scale'] = (Min*pdir,Max*pdir)
                #weights
                if not HasSeparatedWeights:
                    try:
                        cv = g.find('criterionValue')
                        try:
                            criteria[g.attrib['id']]['weight'] = Decimal(cv.find('value').find('real').text)
                        except:
                            criteria[g.attrib['id']]['weight'] = Decimal(cv.find('value').find('integer').text)
                    except:
                        HasSeparatedWeights = True
                #thresholds
                criteria[g.attrib['id']]['thresholds'] = {}
                if not HasSeparatedThresholds:                    
                    if g.find('thresholds') != None:
                        for th in g.find('thresholds').findall('threshold'):
                            try:
                                try:
                                    intercept = Decimal(th.find('linear').find('intercept').find('real').text)
                                except:
                                    intercept = Decimal(th.find('linear').find('intercept').find('integer').text)
                                slope = Decimal(th.find('linear').find('slope').find('real').text)
                            except:
                                try:
                                    intercept = Decimal(th.find('constant').find('real').text)
                                except:
                                    intercept = Decimal(th.find('constant').find('integer').text)
                                slope = Decimal('0.0')
                            ## criteria[g.attrib['id']]['thresholds'][th.attrib['id']] = (intercept,pdir*slope)
                            criteria[g.attrib['id']]['thresholds'][th.attrib['id']] = (intercept,slope)


        # get separated criteria weights
        if HasSeparatedWeights:
            for cv in XMCDA.find('criteriaValues').findall('criterionValue'):
                g = cv.find('criterionID').text
                try:
                    w = cv.find('value').find('real').text
                except:
                    w = cv.find('value').find('integer').text
                criteria[cv.find('criterionID').text]['weight'] = Decimal(w)

        # get separated criteria thresholds
        if HasSeparatedThresholds:
            try:
                for cth in XMCDA.find('criteriaThresholds').findall('criterionThresholds'):
                    g = cth.find('criterionID').text
                    for th in cth.find('thresholds').findall('threshold'):
                        try:
                            try:
                                intercept = Decimal(th.find('linear').find('intercept').find('real').text)
                            except:
                                intercept = Decimal(th.find('linear').find('intercept').find('integer').text)
                            slope = Decimal(th.find('linear').find('slope').find('real').text)
                        except:
                            try:
                                intercept = Decimal(th.find('constant').find('real').text)
                            except:
                                intercept = Decimal(th.find('constant').find('integer').text)
                            slope = Decimal('0.0')
                        ## criteria[g]['thresholds'][th.attrib['id']] = (intercept,pdir*slope)
                        criteria[g]['thresholds'][th.attrib['id']] = (intercept,slope)
            except:
                pass

        # allocate final criteria dictionary        
        self.criteria = criteria
                    
        # get coalitions
        

        
        # get evaluations' description
        description = {}
        for elem in [x for x in XMCDA.find('performanceTable').find('description').getchildren()]:
            description[elem.tag] = elem.text
        self.evaluationDescription = description
        # get evaluations
        evaluationAP = {}
        for v in XMCDA.find('performanceTable').findall('alternativePerformances'):
            a = v.find('alternativeID').text
            evaluationAP[a] = {}
            for x in v.findall('performance'):
                try:
                    value = x.find('value').find('integer').text
                    evaluationAP[a][x.find('criterionID').text]=Decimal(value)
                except:
                    try:
                        value = x.find('value').find('real').text
                        evaluationAP[a][x.find('criterionID').text]=Decimal(value)
                    except:
                        evaluationAP[a][x.find('criterionID').text]=Decimal('-999')
        self.evaluationAP = evaluationAP
        evaluation = {}
        for g in self.criteria:
            try:
                if self.criteria[g]['preferenceDirection'] == 'min':
                    if self.criteria[g]['weight'] > Decimal('0'):
                        pdir = Decimal('-1')
                    else:
                        pdir = Decimal('1')
                else:
                    pdir = Decimal('1')
            except:
                pdir = Decimal('1')
            evaluation[g] = {}
            for a in self.actions:
                if evaluationAP[a][g] != Decimal('-999'):
                    evaluation[g][a] = evaluationAP[a][g] * pdir
                else:
                    evaluation[g][a] = evaluationAP[a][g]
        self.evaluation = evaluation
        # compute weigth preoder

        
        self.weightPreorder = self.computeWeightPreorder()

###########
class CSVPerformanceTableau(PerformanceTableau):
    """
    Reading stored CSV encoded actions x criteria PerformanceTableau instances, Using the inbuilt module csv.

    Param:
        fileName (without the extension .csv).
    """
    def __init__(self,fileName='temp',Debug=True):
        from csv import reader
        from collections import OrderedDict

        try:
            fileNameExt = fileName + '.csv'
            fi = open(fileNameExt,'r')
            csvReader = reader(fi)
            csvText = [x for x in csvReader]
            if Debug:
                print('input',csvText)
        except:
            print("Error: File %s.csv not found !!" % (fileName))
            
        self.name = fileName
        self.reference = 'CSV PerformanceTableau input method.'
        # actions dictionary
        na = len(csvText[0])-1
        if Debug:
            print(na)
        for i in range(6,na+1):
            print(i,csvText[0][i])
        self.actions = OrderedDict([(csvText[0][i],{'name':csvText[0][i],'comment':'potential decision action'}) for i in range(6,na+1)])

        # criteria dictionary
        ng = len(csvText)-1
        for j in range(1,ng+1):
            print(j,csvText[j][0])
        self.criteria = OrderedDict([(csvText[j][0],{'comment':'performance criteria'}) for j in range(1,ng+1)])

        # criteria characteristics
        for j in range(1,ng+1):
            g = csvText[j][0]
            self.criteria[g]['name']  = csvText[j][1]          
            self.criteria[g]['weight']  = Decimal(csvText[j][2])
            self.criteria[g]['scale']  = eval(csvText[j][3]) 
            self.criteria[g]['preferenceDirection'] = csvText[j][4]
            self.criteria[g]['thresholds']  = eval(csvText[j][5])
            print(self.criteria[g])
 
        # evaluation tableaut.ev
        evaluation = {}
        for j in range(1,ng+1):
            evaluation[csvText[j][0]] = {}
            for i in range(6,na+1):
                evaluation[csvText[j][0]][csvText[0][i]] = Decimal(csvText[j][i])
        self.evaluation = evaluation

           
            

#----------test Digraph class ----------------
if __name__ == "__main__":
    
    from digraphs import *
    from outrankingDigraphs import *
    import sortingDigraphs
    import linearOrders
    from transitiveDigraphs import *
    from randomPerfTabs import *
    from time import time
    
    print('*-------- Testing classes and methods -------')

##    t = FullRandomPerformanceTableau(commonScale=(0.0,100.0),numberOfCriteria=10,numberOfActions=10,commonMode=('triangular',30.0,0.7))
    ## t.showStatistics()
    t = Random3ObjectivesPerformanceTableau(numberOfCriteria=13,
                                   numberOfActions=10,
                                   weightDistribution='equiobjectives',
                                   IntegerWeights=True,
                                   #NegativeWeights=False,
                                   Debug=False,
                                   missingDataProbability=0.1,
                                   seed=10,
                                            #Threading=False
                                            )
    t.showWeightPreorder()
   
    
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. August 2015                  *')
    print('* $Revision: 1.37 $                 *')                   
    print('*************************************')

#############################
# Log record for changes:
# $Log: perfTabs.py,v $
# Revision 1.37  2012/12/24 15:18:21
# compatibility patch for old (-2008) python performance tableaux
#############################
