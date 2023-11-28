#!/usr/bin/env python3
"""

Python3 implementation of digraphs
Module for working with performance tableaux  
Copyright (C) 2011-2023  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: Python 3.10"

from perfTabs import *
import json
import decimal
# from digraphsTools import *
from decimal import Decimal
from collections import OrderedDict
from ast import literal_eval

class PerformanceTableau(object):
    """
In this *Digraph3* module, the root :py:class:`perfTabs.PerformanceTableau` class provides a generic **performance table model**. A given object of this class consists in:

     * A set of potential decision **actions** : an ordered dictionary describing the potential decision actions or alternatives with 'name' and 'comment' attributes,
     * An optional set of decision **objectives**: an ordered dictionary with name, comment, weight and list of concerned criteria per objective,
     * A coherent family of **criteria**: a ordered dictionary of criteria functions used for measuring the performance of each potential decision action with respect to the preference dimension captured by each criterion,
     * The **evaluation**: a dictionary of performance evaluations for each decision action or alternative on each criterion function,
     * The NA numerical symbol: Decimal('-999') by default representing missing evaluation data.

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
                     'g2': {'a1':Decimal("88.12"),'a2':Decimal("-999"), ...},
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
   
In this example we consider furthermore a family of seven equisignificant cardinal criteria functions *g01*, *g02*, ..., *g07*, measuring the performance of each alternative on a rational scale form 0.0 to 100.00. In order to capture the evaluation's uncertainty and imprecision, each criterion function *g1* to *g7* admits three performance discrimination thresholds of 10, 20 and 80 pts for warranting respectively any indifference, preference and veto situations: 
    >>> rt.showCriteria(IntegerWeights=True)
    *----  criteria -----*
    g1 RandomPerformanceTableau() instance
      Preference direction: max
      Scale = (0.00, 100.00)
      Weight = 1 
      Threshold ind : 2.50 + 0.00x ; percentile: 6.06
      Threshold pref : 5.00 + 0.00x ; percentile: 12.12
      Threshold veto : 80.00 + 0.00x ; percentile: 100.00
    g2 RandomPerformanceTableau() instance
      Preference direction: max
      Scale = (0.00, 100.00)
      Weight = 1 
      Threshold ind : 2.50 + 0.00x ; percentile: 7.69
      Threshold pref : 5.00 + 0.00x ; percentile: 14.10
      Threshold veto : 80.00 + 0.00x ; percentile: 100.00
    g3 RandomPerformanceTableau() instance
      Preference direction: max
      Scale = (0.00, 100.00)
      Weight = 1 
      Threshold ind : 2.50 + 0.00x ; percentile: 6.41
      Threshold pref : 5.00 + 0.00x ; percentile: 6.41
      Threshold veto : 80.00 + 0.00x ; percentile: 100.00
        ...
        ...
    g7 RandomPerformanceTableau() instance
      Preference direction: max
      Scale = (0.00, 100.00)
      Weight = 1 
      Threshold ind : 2.50 + 0.00x ; percentile: 3.85
      Threshold pref : 5.00 + 0.00x ; percentile: 11.54
      Threshold veto : 80.00 + 0.00x ; percentile: 100.00

The performance evaluations of each decision alternative on each criterion are gathered in a *performance tableau*:
    >>> rt.showPerformanceTableau()
    *----  performance tableau -----*
    Criteria |  'g1'    'g2'    'g3'    'g4'    'g5'    'g6'    'g7'   
    Actions  |    1       1       1       1       1       1       1    
    ---------|-------------------------------------------------------
     'a01'   |  15.17   62.22   39.35   31.83   38.81   56.93   64.96  
     'a02'   |  44.51   44.23   32.06   69.98   67.45   65.57   79.38  
     'a03'   |  57.87   19.10   47.67   48.80   38.93   83.87   75.11  
     'a04'   |  58.00   27.73   14.81   82.88   19.26   34.99   49.30  
     'a05'   |  24.22   41.46   79.70   41.66   94.95   49.56   43.74  
     'a06'   |  29.10   22.41   67.48   12.82   65.63   79.43   15.31  
     'a07'   |   NA     21.52   13.97   21.92   48.00   42.37   59.94  
     'a08'   |  82.29   56.90   90.72   75.74    7.97   42.39   31.39  
     'a09'   |  43.90   46.37   80.16   15.45   34.86   33.75   26.80  
     'a10'   |  38.75   16.22   69.62   6.05    71.81   38.60   59.02  
     'a11'   |  35.84   21.53   45.49    9.96   31.66   57.38   40.85  
     'a12'   |  29.12   51.16   22.03   60.55   41.14   62.34   49.12  
     'a13'   |  34.79   77.01   33.83   27.88   53.58   34.95   45.20  

    """

    def __repr__(self):
        """
        Default presentation method for PerformanceTableau instances.
        """
        reprString = '*------- PerformanceTableau instance description ------*\n'
        reprString += 'Instance class     : %s\n' % self.__class__.__name__
        try:
            reprString += 'Seed               : %s\n' % str(self.randomSeed)
        except:
            pass
        reprString += 'Instance name      : %s\n' % self.name
        reprString += 'Actions            : %d\n' % len(self.actions)
        try:
            reprString += 'Objectives         : %d\n' % len(self.objectives)
        except:
            pass       
        reprString += 'Criteria           : %d\n' % len(self.criteria)
        reprString += 'NaN proportion (%%) : %.1f\n' \
            % (self.computeMissingDataProportion(InPercents=True) )
        reprString += 'Attributes         : %s\n' \
                    % list(self.__dict__.keys())     
        return reprString

    def __init__(self,filePerfTab=None,isEmpty=False):
        from decimal import Decimal
        from collections import OrderedDict
        if filePerfTab is not None:
            fileName = filePerfTab + '.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(filePerfTab)
            try:
                self.description = argDict['description']
            except:
                pass
            ###
            try:
                self.actions = argDict['actions']
            except:
                self.actions = argDict['actionset']
            ###
            try:
                self.objectives = argDict['objectives']
                for obj in self.objectives:
                    self.objectives[obj]['weight'] = Decimal(self.objectives[obj]['weight'])
            except:
                self.objectives = OrderedDict()
            ####
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
            self.setObjectiveWeights()
            ###
            try:
                self.NA = argDict['NA']
            except:
                self.NA = Decimal('-999')
            evaluation = argDict['evaluation']
            for g in self.criteria:
                for x in self.actions:
                    if evaluation[g][x] == Decimal('-999'):
                        evaluation[g][x] = self.NA
            self.evaluation = evaluation
            
        elif not isEmpty:
            from copy import deepcopy
            from randomPerfTabs import RandomPerformanceTableau
            temp = RandomPerformanceTableau()
            self.name = deepcopy(temp.name)
            self.actions = deepcopy(temp.actions)
            self.criteria = deepcopy(temp.criteria)
            self.weightPreorder = temp.computeWeightPreorder()
            self.evaluation = deepcopy(temp.evaluation)
            self.NA = deepcopy(temp.NA)
        else:
            self.name = "empty_instance"
            self.actions = {}
            self.criteria = {}
            self.weightPreorder = {}
            self.evaluation = {}
            self.NA = Decimal('-999')
            
    def replaceNA(self,newNA=None,Comments=False):
        """
        Replaces the current self.NA symbol with the *newNA* symbol of type <Decimal>. If newNA is None, the defauklt value Decimal('-999') is used.
        """
        if newNA is None:
            newNA = Decimal('-999')
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
        NA = self.NA
        count = 0
        for g in criteria:
            if criteria[g]['preferenceDirection'] == 'max':
                if newNA >= criteria[g]['scale'][0] \
                         and newNA <= criteria[g]['scale'][1]:
                    print('Warning!!: newNA included in criterion %s scale' \
                                                                % (g))
                    print(criteria[g]['scale'],newNA)
            else:
                if newNA >= -criteria[g]['scale'][1] \
                   and newNA <= -criteria[g]['scale'][0]:
                    print('Warning!!: newNA included in criterion %s scale' \
                                                               % (g))
                    print(-criteria[g]['scale'][0],newNA,
                          -criteria[g]['scale'][1])

            for x in actions:
                if evaluation[g][x] == NA:
                    evaluation[g][x] = newNA
                    count += 1
        if Comments:
            print('replaced %d' % (count), NA, 'with', newNA)
        self.NA = newNA

    def setObjectiveWeights(self,Debug=False):
        """
        Set the objective weights to the sum of the corresponding criteria significance weights.
        """
        objectives = self.objectives
        criteria = self.criteria
        objWeights = {}
        for obj in objectives:
            for g in objectives[obj]['criteria']:
                try:
                    objWeights[obj] += criteria[g]['weight']
                except:
                    objWeights[obj] = criteria[g]['weight']
        for obj in objectives:
            try:
                objectives[obj]['weight'] = objWeights[obj]
            except:
                objectives[obj]['weight'] = Decimal('0.0')
            
    def hasOddWeightAlgebra(self,Debug=False):
        """
        Verify if the given criteria[self]['weight'] are odd or not.
        Return a Boolen value.
        """
        from digraphsTools import powerset
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
        Compute normalized weighted average scores by ignoring missing data.
        When *isNormalized* == True (False by default), 
        transforms all the scores into a common 0-100 scale. 
        A lowValue and highValue parameter
        can be provided for a specific normalisation.
        """
        from operator import itemgetter
        actions = self.actions
        criteria = self.criteria
        NA = self.NA
        if isNormalized:
            normSelf = NormalizedPerformanceTableau(self,lowValue=lowValue,highValue=highValue)
            evaluation = normSelf.evaluation
        else:
            evaluation = self.evaluation

        #sumWeights = Decimal('0.0')
        #for g in dict.keys(criteria):
        #    sumWeights += abs(criteria[g]['weight'])

        weightedAverage = {} 
        for x in dict.keys(actions):
            sumWeights = Decimal('0.0')
            weightedAverage[x] = Decimal('0.0')
            for g in dict.keys(criteria):
                if evaluation[g][x] != NA:
                    sumWeights += abs(criteria[g]['weight'])
                    weightedAverage[x] \
                        += evaluation[g][x] * criteria[g]['weight'] \
                                            / sumWeights
        if isListRanked:
            ranked = []
            for x in weightedAverage:
                ranked.append((weightedAverage[x],x))
            ranked.sort(reverse=True,key=itemgetter(0))
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

    def showPairwiseComparison(self,a,b,
                               hasSymetricThresholds=True,
                               Debug=False,
                               isReturningHTML=False,
                               hasSymmetricThresholds=True):
        """
        renders the pairwise comprison parameters on all criteria
        in html format
        """
        from outrankingDigraphs import BipolarOutrankingDigraph
        evaluation = self.evaluation
        NA = self.NA
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
                if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                    try:
                        indx = criteria[c]['thresholds']['ind'][0]
                        indy = criteria[c]['thresholds']['ind'][1]
                        if hasSymmetricThresholds:
                            ind = indx +indy \
                                 * max(abs(evaluation[c][a]),
                                       abs(evaluation[c][b]))
                        else:
                            ind = indx +indy * abs(evaluation[c][a])
                    except:
                        ind = None
                    try:
                        wpx = criteria[c]['thresholds']['weakPreference'][0]
                        wpy = criteria[c]['thresholds']['weakPreference'][1]
                        if hasSymmetricThresholds:
                            wp = wpx + wpy \
                                * max(abs(evaluation[c][a]),
                                      abs(evaluation[c][b]))
                    except:
                        wp = None
                    try:
                        px = criteria[c]['thresholds']['pref'][0]
                        py = criteria[c]['thresholds']['pref'][1]
                        if hasSymmetricThresholds:
                            p = px + py \
                                * max(abs(evaluation[c][a]),
                                      abs(evaluation[c][b]))
                        else:
                            p = px + py * abs(evaluation[c][a])
                    except:
                        p = None
                    if criteria[c]['weight'] > Decimal('0'):
                        d = evaluation[c][a] - evaluation[c][b]
                    else:
                        d = evaluation[c][b] - evaluation[c][a]
                    lc0 = BipolarOutrankingDigraph._localConcordance(self,
                                                                     d,ind,
                                                                     wp,p)
                    if ind is not None:
                        ind = round(ind,2)
                    if wp is not None:
                        wp = round(wp,2)
                    if p is not None:
                        p = round(p,2)
                    if isReturningHTML:
                        html += '<tr>'
                        html += '<td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td> <td>%2.2f</td> <td>%2.2f</td> <td>%+2.2f</td> <td>%s</td>  <td>%s</td>  <td>%s</td>   <td>%+.2f</td>' % (c,criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*abs(criteria[c]['weight']))
                    else:
                         print(c, '  %.2f  %2.2f  %2.2f  %+2.2f \t| %s  %s  %s   %+.2f \t|' % (criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*criteria[c]['weight']), end=' ')
                    concordance = concordance \
                                  + (lc0 * abs(criteria[c]['weight']))
                    try:
                        wvx = criteria[c]['thresholds']['weakVeto'][0]
                        wvy = criteria[c]['thresholds']['weakVeto'][1]
                        if hasSymmetricThresholds:
                            wv = wvx + wvy \
                                 * max(abs(evaluation[c][a]),
                                       abs(evaluation[c][b]))
                        else:
                            wv = wvx + wvy * abs(evaluation[c][a])
                    except:
                        wv = None
                    try:
                        vx = criteria[c]['thresholds']['veto'][0]
                        vy = criteria[c]['thresholds']['veto'][1]
                        if hasSymmetricThresholds:
                            v = vx + vy \
                                * max(abs(evaluation[c][a]),
                                      abs(evaluation[c][b]))
                        else:
                            v = vx + vy * abs(evaluation[c][a])
                    except:
                        v = None
                    veto = BipolarOutrankingDigraph._localVeto(self,d,wv,v)
                    try:
                        negativeVeto \
                         = BipolarOutrankingDigraph._localNegativeVeto(self,
                                                                      d,wv,v)
                        hasBipolarVeto = True
                    except:
                        hasBipolarVeto = False
                    if hasBipolarVeto:
                        if v is not None:
                            if d >= v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' \
                                              % (v, negativeVeto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ddffdd">%+2.2f</td>' % (v, negativeVeto)
                            elif d <= -v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' \
                                          % (v, -veto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                            else:
                                if not isReturningHTML:                                
                                    print()
                                else:
                                    html += '</tr>'
                        elif wv is not None:
                            if d >= wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' \
                                          % (wv, negativeVeto))
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
                            if wv is not None:
                                if v is not None:
                                    if not isReturningHTML:
                                        print(' %2.2f %2.2f %+2.2f' \
                                              % (wv, v, veto))
                                    else:
                                        html += '<td>%2.2f</td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, v, veto)
                                else:
                                    if not isReturningHTML:
                                        print(' %2.2f       %+2.2f' % (wv, -veto))
                                    else:
                                        html += '<td>%2.2f</td> <td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if v is not None:
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
                    if evaluation[c][a] == self.NA:
                        eval_c_a = 'NA'
                    else:
                        eval_c_a = '%2.2f' % evaluation[c][a]
                    if evaluation[c][b] == self.NA:
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
                            print('  Threshold %s : %.2f + %.2fx' \
                                  % (th,criteria[g]['thresholds'][th][0],
                                     criteria[g]['thresholds'][th][1]), end=' ')
                            print('; percentile: %.2f' \
                            % (self.computeVariableThresholdPercentile(g,th,Debug)*100.0) )
                    except:
                        pass
                    print()
        else:
            criteriaList = list(self.criteria.keys())
            if Alphabetic:
                criteriaList.sort()
            for g in criteriaList:
                cg = criteria[g]
                print(g, cg['name'])
                try:
                    prefDir = cg['preferenceDirection']
                except:
                    prefDir = 'max'
                print('  Preference direction:', prefDir)
                print('  Scale = (%.2f, %.2f)' %\
                        (cg['scale'][0],cg['scale'][1]) )
                if IntegerWeights:
                    print('  Weight = %d ' % (cg['weight']))
                else:
                    weightg = cg['weight']/sumWeights
                    print('  Weight = %.3f ' % (weightg))
                try:
                    for th in cg['thresholds']:
                        if Debug:
                            print('-->>>', th,cg['thresholds'][th][0],
                                              cg['thresholds'][th][1])
                        print('  Threshold %s : %.2f + %.2fx'\
                            % (th,cg['thresholds'][th][0],
                               cg['thresholds'][th][1]), end=' ')
                        #print self.criteria[g]['thresholds'][th]
                        print('; percentile: %.2f' \
                % (self.computeVariableThresholdPercentile(g,th,Debug)*100.0) )
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
                      % (self.objectives[obj]['weight'],
                         len(self.objectives[obj]['criteria'])))
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
        NA = self.NA
        for g in criteria:
            for x in actions:
                if evaluation[g][x] != NA:
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
        NA = self.NA
        for g in criteria:
            critg = criteria[g]
            if critg['preferenceDirection'] == 'min':
                critg['weight'] = -abs(critg['weight'])
                valg = evaluation[g]
                for x in valg:
                    if valg[x] != NA:
                        #print(g,x,valg[x])
                        valg[x] = abs(valg[x])
        self.criteria = criteria
        self.evaluation = evaluation

    def convertWeights2Positive(self):
        """
        Sets negative weights back to positive weights and negates corresponding evaluation grades.
        """
        from decimal import Decimal
        criteria = self.criteria
        evaluation = self.evaluation
        NA = self.NA
        for g in criteria:
            critg = criteria[g]
            if critg['preferenceDirection'] == 'min':
                critg['weight'] = abs(critg['weight'])
                valg = evaluation[g]
                for x in valg:
                    if valg[x] != NA:
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
        NA = self.NA
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
                if xi != NA:
                    for j in range(i+1,n):
                        xj = self.evaluation[c][actionsList[j]]
                        if xj != NA:
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
                    print(' -->', c, ': ',
                          criteria[c]['minimalPerformanceDifference'],\
                          criteria[c]['maximalPerformanceDifference'])
                    print(len(criteria[c]['performanceDifferences']),
                          criteria[c]['performanceDifferences'])
                    print(criteria[c]['performanceDifferences'][0],
                          criteria[c]['performanceDifferences'][-1])

        if NotPermanentDiffs:
            return performanceDifferences
        
    def mpComputePerformanceDifferences(self,NotPermanentDiffs=True,nbrCores=None,Debug=False):
        """
        Adds to the criteria dictionary the ordered list of all observed performance differences.
        """
        criteria = self.criteria
        #from multiprocessing import Pool
        #from os import cpu_count
        import multiprocessing as mp
        mpctx = mp.get_context('fork')
        Pool = mpctx.Pool
        cpu_count = mpctx.cpu_count

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
        NA = self.NA
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
            if xi != NA:
                for j in range(i+1,n):
                    xj = evaluation[c][actionsList[j]]
                    if xj != NA:
                        delta = abs(xi - xj)
                        if delta < ed:
                            ed = delta
                        if delta > md:
                            md = delta
                        #diff.add(delta)
                        diffList.append(delta)
                        if Debug:
                            print('-->> i,j, evaluation[actionsList[i]],evaluation[actionsList[j]], delta, ed,md', i,j, evaluation[c][actionsList[i]],
                                  evaluation[c][actionsList[j]],
                                  delta, ed,md,diffList)
        criteria[c]['minimalPerformanceDifference'] = ed
        criteria[c]['maximalPerformanceDifference'] = md
        #diffList = list(diff)
        diffList.sort()
        if Comments:
            print(' -->', c, ': ',
                  criteria[c]['minimalPerformanceDifference'],
                  criteria[c]['maximalPerformanceDifference'])
            print(len(diffList),diffList)
            print(diffList[0], diffList[-1])
        
        return (diffList,ed,md)
            
    def computeActionCriterionPerformanceDifferences(self,refAction,refCriterion,comments = False, Debug = False):
        """
        computes the performances differences observed between the reference action and the others on the given criterion
        """
        evaluation = self.evaluation
        NA = self.NA
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
                if xr != NA and xo != NA:
                    delta = abs(evaluation[refCriterion][refAction] - evaluation[refCriterion][x])
                    diff.append(delta)
                    if Debug:
                        print('-->> refAction, x, evaluation[refAction], evaluation[x], delta,diff', refAction,x, evaluation[refCriterion][refAction],
                              evaluation[refCriterion][x], delta,diff)

        diff.sort()
        return diff

    def computeActionCriterionQuantile(self,action,criterion,strategy='average',Debug=False):
        """
        renders the quantile of the performance of action on criterion
        """
        perfsy = self.evaluation[criterion]
        NA = self.NA
        if Debug:
            print(action,criterion)
        perfx = self.evaluation[criterion][action]
        if perfx != NA:
            try:
                indx = self.criteria[criterion]['thresholds']['ind'][0]\
                + self.criteria[criterion]['thresholds']['ind'][1]*perfx
                ## indx = self.criteria[criterion]['thresholds']['ind'][0] + self.criteria[criterion]['thresholds']['pref'][1]*perfx
            except:
                indx = Decimal('0')
            validperfsy = [y for y in perfsy\
                           if (y in self.actions) and (perfsy[y] != NA)]
            n = len(validperfsy)
            qhigh = [y for y in validperfsy if (perfsy[y] <= perfx)]
            nqhigh = len(qhigh)
            if strategy == 'average':
                qlow = [y for y in validperfsy if (perfsy[y] < perfx)]
                nqlow = len(qlow)
                quantile = (float(nqlow + nqhigh)/float(2))/float(n)
            else:
                quantile = float(nqhigh) / float(n)
            return quantile
        else:
            return 'NA'

    def _computeLimitingQuantiles(self,g,frequencies,LowerClosed=True,Debug=False,PrefThresholds=True):
        """
        Renders the list of limiting quantiles *q(p)* on criteria *g* for *p* in *frequencies* 
        """
        from math import floor
        from copy import copy, deepcopy
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        NA = self.NA
        gValues = []
        for x in actions:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,evaluation[g][x])
            if evaluation[g][x] != NA:
                gValues.append(evaluation[g][x])
        gValues.sort()
        if PrefThresholds:
            try:
                gPrefThrCst = criteria[g]['thresholds']['pref'][0]
                gPrefThrSlope = criteria[g]['thresholds']['pref'][1]
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
                    if criteria[g]['preferenceDirection'] == 'min':
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
                    if criteria[g]['preferenceDirection'] == 'min':
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
                        if criteria[g]['preferenceDirection'] == 'min':
                            quantile = Decimal('-200.0')
                        else:
                            quantile = Decimal('-100.0')     
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)
##        else:
##            gQuantiles = []
        if Debug:
            print(g,LowerClosed,criteria[g]['preferenceDirection'],gQuantiles)
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

    def computeActionQuantile(self,action,Debug=False):
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

    def showHTMLPerformanceQuantiles(self,Sorted=True,htmlFileName=None):
        """
        shows the performance quantiles tableau in a browser window.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self.computeAllQuantiles(Sorted=Sorted,Comments=False))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)
        
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
        ranking = self.computeQuantileOrder(q0=q0,q1=q1,
                         Threading=Threading,nbrOfCPUs=nbrOfCPUs,
                         Comments=Comments)
        ranking.reverse()
        if Comments:
            print(ranking)
        return ranking
        
    def computeQuantileSort(self):
        """
        shows a sorting of the actions from decreasing majority quantiles
        """
        from operator import itemgetter
        self.computeQuantiles()
        actionsSorting = []
        for x in list(self.actions.keys()):
            actionsSorting.append((self.quantiles[x],x))
        actionsSorting.sort(reverse=True,key=itemgetter(0))
        return actionsSorting

    def computeQuantilePreorder(self,Comments=True,Debug=False):
        """
        computes the preorder of the actions obtained from decreasing majority quantiles. The quantiles are recomputed with a call to the self.computeQuantileSort() method.
        """
        from operator import itemgetter
        quantiles = self.computeQuantileSort()
        quantiles.sort(reverse=True,key=itemgetter(0))
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
        if criteriaList is None:
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
                print('a,na,self.evaluation[criterion][a],th[0],th[1],quantile',
                      a,na,evaluation[criterion][a],th[0],th[1],quantile)
            while i < na and performanceDifferences[i] <= quantile:
                if Debug:
                    print('i, quantile, performanceDifferences[i]',
                          i, quantile, performanceDifferences[i])
                i += 1
            count += i
            if Debug:
                print('a,na,final i', a,na,i)
        percentile = float(count)/float(total)
        if Debug:
            print('count = ', count, 'total = ', total)
            print('percentile =', percentile)   
        return percentile

    def showPerformanceTableau(self,Transposed=False,actionsSubset=None,
                               fromIndex=None,toIndex=None,Sorted=True,ndigits=2):
        """
        Print the performance Tableau.
        """
        from decimal import Decimal
        NA = self.NA
        print('*----  performance tableau -----*')
        criteriaList = list(self.criteria)
        if Sorted:
            criteriaList.sort()
        if actionsSubset is None:
            actionsList = list(self.actions)
            if Sorted:
                actionsList.sort()
        else:
            actionsList = list(actionsSubset)
        if fromIndex is None:
            fromIndex = 0
        if toIndex is None:
            toIndex=len(actionsList)
        # view criteria x actions
        if Transposed:
            print('criteria | weights |', end=' ')
            for x in actionsList:
                print('\''+str(x)+'\'  ', end=' ')
            print('\n---------|-----------------------------------------')
            formatString = '%% .%df ' % ndigits
            for g in criteriaList:
                print('   \''+str(g) + '\'  |   ' + str(self.criteria[g]['weight'])\
                            + '   | ', end=' ')
                for i in range(fromIndex,toIndex):
                    x = actionsList[i]
                    evalgx = self.evaluation[g][x]
                    if evalgx == NA:
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
                try:
                    print('   \''+str(self.actions[x]['shortName']) + '\'   |' , end=' ')
                except KeyError:
                    print('   \''+str(x) + '\'   |' , end=' ')        
                for g in criteriaList:
                    evalgx = self.evaluation[g][x]
                    if evalgx == NA:
                        print('  NA  ', end=' ')
                    else:                    
                        print(formatString % (evalgx), end=' ')
                print()
            

    def saveCSV(self,fileName='tempPerfTab',
                Sorted=True,criteriaList=None,
                actionsList=None,ndigits=2,Debug=False):
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
        if criteriaList is None:
            criteriaList = list(dict.keys(criteria))
            if sorted:
                criteriaList.sort()
        ng = len(criteriaList)
        if Debug:
            print(criteriaList)
        if actionsList is None:
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
        
    def computeMissingDataProportion(self,InPercents=False,Comments=False):
        """
        Renders the proportion of missing data, 
        i.e. NA == Decimal('-999') entries in self.evaluation.
        """
        
        naCount = 0
        entryCount = 0
        NA = self.NA

        for g in self.criteria:
            for x in self.actions:
                entryCount += 1
                if self.evaluation[g][x] == NA:
                    naCount += 1

        try:
            res = naCount/entryCount
        except:
            res = 0.0
            if Comments:
                print('!!! Empty performance tableau !!!')
        if InPercents:
            res *= 100.0
        if Comments:
            print('Missing data proportion: %.3f' % (res))
        else:
            return res
   
    def computeMinMaxEvaluations(self,criteria=None,actions=None):
        """
        renders minimum and maximum performances on each criterion
        in dictionary form: {'g': {'minimum': x, 'maximum': x}}
        """
        evaluation = self.evaluation
        NA = self.NA
        if criteria is None:
            criteria = self.criteria
            criteriaKeys = [x for x in dict.keys(criteria)]
        else:
            criteriaKeys = criteria
        if actions is None:
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
                if val != NA:
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
                result[g]['minimum'] = NA
                result[g]['maximum'] = NA
        return result

    def showHTMLCriteria(self,criteriaSubset=None,Sorted=True,
                         ndigits=2,title=None,htmlFileName=None):
        """
        shows the criteria in the system browser view.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self._htmlCriteriaView(criteria=criteriaSubset,
                                        Sorted=Sorted,
                                        ndigits=ndigits,
                                        title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)

    def _htmlCriteriaView(self,criteria=None,Sorted=False,
                         ndigits=2,title='Family of Criteria'):
        """
        Renders a html view of the in the XMCDA2 format.
        """
        if title is None:
            html = '<h1>%s: Family of Criteria</h1>' % self.name
        else:
            html = '<h1>%s</h1>' % title            
        if criteria is None:
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
            formatString = '<td align="center">%%.%df</td>' % ndigits
            html += formatString % critg['weight']
            html += '<td align="center">%s</td>' % critg['preferenceDirection']
            html += formatString % critg['scale'][0]
            html += formatString % critg['scale'][1]

            formatString = '<td align="center">%%.%dfx + %%.%df</td>' % (ndigits,ndigits)
            try:
                if critg['thresholds']['ind'] is not None:
                    html += formatString %\
                                (critg['thresholds']['ind'][1],
                                 critg['thresholds']['ind'][0])                
            except:
                html += '<td></td>'
                
            try:
                if critg['thresholds']['pref'] is not None:
                    html += formatString %\
                                (critg['thresholds']['pref'][1],
                                 critg['thresholds']['pref'][0])                
            except:
                html += '<td></td>'
            try:
                if critg['thresholds']['veto'] is not None:
                    html += formatString %\
                                (critg['thresholds']['veto'][1],
                                 critg['thresholds']['veto'][0])                
            except:
                html += '<td></td>'

            html += '</tr>'
            
        html += '</table>'
        return html
        
        
    def showHTMLPerformanceTableau(self,actionsSubset=None,
                                   fromIndex=None,toIndex=None,
                                   isSorted=False,
                                   Transposed=False,ndigits=2,
                                   ContentCentered=True,title=None,
                                   htmlFileName=None):
        """
        shows the html version of the performance tableau in a browser window.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self._htmlPerformanceTableau(actions=actionsSubset,
                                             fromIndex=fromIndex,
                                             toIndex=toIndex,
                                             isSorted=isSorted,
                                             Transposed=Transposed,
                                             ndigits=ndigits,
                                             ContentCentered=ContentCentered,
                                             title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)
            
    def _htmlPerformanceTableau(self,actions=None,
                               fromIndex=None,
                               toIndex=None,
                               isSorted=False,
                             Transposed=False,ndigits=2,
                             ContentCentered=True,
                             title=None):
        """
        Renders the performance tableau citerion x actions in html format.
        """
        criteria = self.criteria
        NA = self.NA
        minMaxEvaluations = self.computeMinMaxEvaluations()
        if title is None:
            html = '<h1>Performance table %s</h1>' % self.name
        else:
            html = '<h1>%s</h1>' % title            
        criteriaKeys = list(criteria.keys())
        if isSorted:
            criteriaKeys.sort()
        if actions is None:
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
            if fromIndex is None:
                fromIndex = 0
            if toIndex is None:
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
                    if self.evaluation[g][x] != NA:
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
            if fromIndex is None:
                fromIndex = 0
            if toIndex is None:
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
                        if self.evaluation[g][x] != NA:
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
                        if self.evaluation[g][x] != NA:
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

    def showHTMLPerformanceHeatmap(self,actionsList=None,
                                   WithActionNames=False,
                                   fromIndex=None,
                                   toIndex=None,
                                   Transposed=False,
                                   criteriaList=None,
                                   colorLevels=7,
                                   pageTitle=None,
                                   ndigits=2,
                                   SparseModel=False,
                                   outrankingModel = 'standard',
                                   minimalComponentSize=1,
                                   rankingRule='NetFlows',
                                   StoreRanking=True,
                                   quantiles=None,
                                   strategy='average',
                                   Correlations=False,
                                   htmlFileName=None,
                                   Threading=False,
                                   nbrOfCPUs=None,
                                   Debug=False):
        """
        shows the html heatmap version of the performance tableau in a browser window
        (see perfTabs.htmlPerformanceHeatMap() method ).

        **Parameters**:
        
        * *actionsList* and *criteriaList*, if provided,  give the possibility to show
          the decision alternatives, resp. criteria, in a given ordering.
        * *WithActionNames* = True (default False) will show the action names instead of the short names or the identifyers.
        * *ndigits* = 0 may be used to show integer evaluation values.
        * *colorLevels* may be 3, 5, 7, or 9. 
        * When no *actionsList* is provided, the decision actions are ordered from the best to the worst. This
          ranking is obtained by default with the Copeland rule applied on a standard *BipolarOutrankingDigraph*.
        * When the *SparseModel* flag is put to *True*, a sparse *PreRankedOutrankingDigraph* construction is used instead.
        * the *outrankingModel* parameter (default = 'standard') allows to switch to alternative BipolarOutrankingDigraph constructors, like 'confident' or 'robust' models. When called from a bipolar-valued outrankingDigraph instance, *outrankingModel* = 'this' keeps the current outranking model without recomputing by default the standard outranking model.            
        * The *minimalComponentSize* allows to control the fill rate of the pre-ranked model.
          When *minimalComponentSize* = *n* (the number of decision actions) both the pre-ranked model will be
          in fact equivalent to the standard model.
        * *rankingRule* = 'NetFlows' (default) | 'Copeland' | 'Kohler' | 'RankedPairs' | 'ArrowRaymond'
          | 'IteratedNetFlows' | 'IteraredCopeland'. See tutorial on ranking mith multiple incommensurable criteria.
        * when the *StoreRanking* flag is set to *True*, the ranking result is storted in *self*.
        * Quantiles used for the pre-ranked decomposition are put by default to *n*
          (the number of decision alternatives) for *n* < 50. For larger cardinalities up to 1000, quantiles = *n* /10.
          For bigger performance tableaux the *quantiles* parameter may be set to a much lower value
          not exceeding usually 10.
        * The pre-ranking may be obtained with three ordering strategies for the
          quantiles equivalence classes: 'average' (default), 'optimistic' or  'pessimistic'.
        * With *Correlations* = *True* and *criteriaList* = *None*, the criteria will be presented from left to right in decreasing
          order of the correlations between the marginal criterion based ranking and the global ranking used for
          presenting the decision alternatives.
        * For large performance Tableaux, *multiprocessing* techniques may be used by setting
          *Threading* = *True* in order to speed up the computations; especially when *Correlations* = *True*.
        * By default, the number of cores available, will be detected. It may be necessary in a HPC context to indicate the exact number of singled threaded cores in fact allocated to the multiprocessing job.


        >>> from randomPerfTabs import RandomPerformanceTableau
        >>> rt = RandomPerformanceTableau(seed=100)
        >>> rt.showHTMLPerformanceHeatmap(colorLevels=5,Correlations=True)

        .. image:: perfTabsExample.png
           :alt: HTML heat map of the performance tableau
           :width: 600 px
           :align: center
        
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        if pageTitle is None:
            pageTitle = 'Heatmap of Performance Tableau \'%s\'' % self.name
            
        fo.write(self._htmlPerformanceHeatmap(argCriteriaList=criteriaList,
                                             argActionsList=actionsList,
                                            WithActionNames=WithActionNames,
                                             fromIndex=fromIndex,
                                             Transposed=Transposed,
                                             toIndex=toIndex,
                                             SparseModel=SparseModel,
                                              outrankingModel=outrankingModel,
                                             minimalComponentSize=minimalComponentSize,
                                             rankingRule=rankingRule,
                                             StoreRanking=StoreRanking,
                                             quantiles=quantiles,
                                             strategy=strategy,
                                             ndigits=ndigits,
                                             colorLevels=colorLevels,
                                             pageTitle=pageTitle,
                                             Correlations=Correlations,
                                             Threading=Threading,
                                             nbrOfCPUs=nbrOfCPUs,
                                             Debug=Debug))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)

    def _htmlPerformanceHeatmap(self,argCriteriaList=None,
                                argActionsList=None,
                                WithActionNames=False,
                                fromIndex=None,
                                toIndex=None,
                                Transposed=False,
                                SparseModel=False,
                                outrankingModel='standard',
                                minimalComponentSize=1,
                                rankingRule=None,
                                StoreRanking=False,
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
        Renders the Brewer RdYlGn 3, 5, 7, or 9 levels colored heatmap of the performance table
        actions x criteria in html format.

        See the corresponding perfTabs.showHTMLPerformanceHeatMap() method.
        """
        from decimal import Decimal
        from operator import itemgetter            
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
        brewerRdYlGn3Colors = [
                               (Decimal('0.3333'),'"#FEE08B"'),
                               (Decimal('0.6666'),'"#FFFFBF"'),
                               (Decimal('1.0'),'"#D9EF8B"'),
                               ]
        if colorLevels is None:
            colorLevels = 7
        if colorLevels == 7:
            colorPalette = brewerRdYlGn7Colors
        elif colorLevels == 9:
            colorPalette = brewerRdYlGn9Colors
        elif colorLevels == 5:
            colorPalette = brewerRdYlGn5Colors
        elif colorLevels == 3:
            colorPalette = brewerRdYlGn3Colors
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
        
        if argCriteriaList is None:
            argCriteriaList = list(self.criteria.keys())
            criteriaList = None
        else:
            criteriaList = argCriteriaList

##        if rankingRule is None:
##            rankingRule = 'NetFlows'

        if argActionsList is None: # actions ranking is needed
            
            na = len(self.actions)
            if SparseModel:
                from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
                if quantiles is None:
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
                rankCorrelation = None
                
            else: # standard outranking model
                if outrankingModel == 'standard':
                    from outrankingDigraphs import BipolarOutrankingDigraph
                    g = BipolarOutrankingDigraph(self,actionsSubset=argActionsList,Normalized=True)
                elif outrankingModel == 'confident':
                    from outrankingDigraphs import ConfidentBipolarOutrankingDigraph
                    g = ConfidentBipolarOutrankingDigraph(self,Normalized=True)
                elif outrankingModel == 'robust':
                    from outrankingDigraphs import RobustOutrankingDigraph
                    g = RobustOutrankingDigraph(self)
                elif outrankingModel == 'this':
                    g = self                 
                else:
                    print('!!! Error: outrankingModel "%s" is not implemented !!!' % outrankingModel )
                    
                if rankingRule == 'NetFlows':
                    actionsList = g.computeNetFlowsRanking()
                    if StoreRanking:
                        self.netFlowsRanking = actionsList
                if rankingRule == 'Copeland':
                    actionsList = g.computeCopelandRanking()
                    if StoreRanking:
                        self.copelandRanking = actionsList
                elif rankingRule == 'Kohler':
                    actionsList = (~(-g)).computeKohlerRanking()
                    if StoreRanking:
                        self.kohlerRanking = actionsList
                elif rankingRule == 'RankedPairs':
                    from linearOrders import RankedPairsOrder
                    rp = RankedPairsOrder(g)
                    actionsList = rp.computeRanking()
                    if StoreRanking:
                        self.rankedPairsRanking = actionsList
                elif rankingRule == 'ArrowRaynaud':
                    actionsList = g.computeArrowRaynaudRanking()
                    if StoreRanking:
                        self.arrowRaynaudRanking = actionsList
                elif rankingRule == 'IteratedNetFlows':
                    from linearOrders import IteratedNetFlowsRanking
                    inf = IteratedNetFlowsRanking(g)
                    actionsList = inf.iteratedNetFlowsRanking
                    if StoreRanking:
                        self.iteratedNetFlowsRanking = actionsList
                elif rankingRule == 'IteratedCopeland':
                    from linearOrders import IteratedCopelandRanking
                    icop = IteratedCopelandRanking(g)
                    actionsList = icop.iteratedCopelandRanking
                    if StoreRanking:
                        self.iteratedCopelandRanking = actionsList
                elif rankingRule is None:
                    actionsList = list(self.actions.keys())
                else: # default ranking rule
                    actionsList = g.computeNetFlowsRanking()
                    rankingRule='NetFlows'
                    if StoreRanking:
                        self.netFlowsRanking = actionsList
                rankCorrelation = g.computeOrderCorrelation(list(reversed(actionsList)))

        else:  # actions list given
            actionsList = argActionsList
            rankingRule = None
            #Correlations = False
            rankCorrelation = None
            if SparseModel:
                rankCorrelation = None
            else:
                from outrankingDigraphs import BipolarOutrankingDigraph
                g = BipolarOutrankingDigraph(self,actionsSubset=argActionsList,Normalized=True)
                rankCorrelation = g.computeOrderCorrelation(list(reversed(actionsList)))
        if Debug:
            print('1',actionsList)
            print('2',rankCorrelation)
            
        ##########
        criteria = self.criteria
        NA = self.NA
        if criteriaList is None:
            if Correlations:
                marginalCorrelations = g.computeRankingConsensusQuality(actionsList)
                criteriaCorrelation = marginalCorrelations[0]
                meanMarginalCriteriaCorrelation = marginalCorrelations[1]
                sdMarginalCriteriaCorrelation = marginalCorrelations[2]             
                criteriaList = [c[1] for c in criteriaCorrelation]
            else:
                criteriaList = list(criteria.keys())
                criteriaList.sort()
                criteriaWeightsList = [(-criteria[g]['weight'],g) for g in criteriaList]
                criteriaWeightsList.sort(reverse=False,key=itemgetter(0))
                criteriaList = [g[1] for g in criteriaWeightsList]
                criteriaCorrelation = None
                rankCorrelation = None
        else:
            criteriaList = list(criteria.keys())
            if Correlations:
                marginalCorrelations = g.computeRankingConsensusQuality(actionsList)
                criteriaCorrelation = marginalCorrelations[0]
                meanMarginalCriteriaCorrelation = marginalCorrelations[1]
                sdMarginalCriteriaCorrelation = marginalCorrelations[2]             
            else:
                criteriaCorrelation = None
                rankCorrelation = None
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
        if Transposed:
            html += '<table style="background-color:%s;" border="1">\n' \
                                 % (backGroundColor) 
            html += '<tr bgcolor=%s><th>criteria</th>' % (columnHeaderColor)
            html += '<th>weight</th>'
            if Correlations:
                html += '<th>tau*</th>'
            if fromIndex is None:
                fromIndex = 0
            if toIndex is None:
                toIndex = len(actionsList)
            for i in range(fromIndex,toIndex):
                x = actionsList[i]
                try:
                    xName = actions[x]['shortName']
                except:
                    xName = str(x)
                html += '<th bgcolor="#FFF79B">%s</th>' % (xName)
            html += '</tr>\n'
            gn = len(criteriaList)
            for i in range(gn):
                g = criteriaList[i]
                try:
                    gName = self.criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (gName)
                html += '<td align="center">%+.2f</td>' % (self.criteria[g]['weight'])
                if criteriaCorrelation is not None:
                    cg = criteriaCorrelation[i]
                    html += '<td align="center">%+.2f</td>' % (cg[0])
                if Debug:
                    print(html)
                if fromIndex is None:
                    fromIndex = 0
                if toIndex is None:
                    toIndex = len(actionsList)
                for j in range(fromIndex,toIndex):
                    x = actionsList[j]
                    try:
                        xName = self.actions[x]['shortName']
                    except:
                        xName = str(x)
                    if self.evaluation[g][x] != NA:
                        formatString = '<td bgcolor=%s align="right">%% .%df</td>' \
                                                % (quantileColor[x][g],ndigits)
                        html += formatString % (self.evaluation[g][x])
                    else:
                        html += '<td bgcolor=%s class="na">NA</td>' % naColor
                html += '</tr>'
                if Debug:
                    print(html)
            html += '</table>\n'
        else: # standard actions x criteria layout
            html += '<table style="background-color:%s;" border="1">\n' \
                                         % (backGroundColor) 
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
                html += '<td align="center">%+.2f</td>' \
                            % (self.criteria[g]['weight'])
            html += '</tr>\n'
            if criteriaCorrelation is not None:
                html += '<tr><th bgcolor=%s>tau<sup>(*)</sup></th>' \
                                    % (columnHeaderColor)
                for cg in criteriaCorrelation:
                    html += '<td align="center">%+.2f</td>' % (cg[0])
                html += '</tr>\n'
            if Debug:
                print(html)
            if fromIndex is None:
                fromIndex=0
            if toIndex is None:
                toIndex = len(actionsList)
            for i in range(fromIndex,toIndex):
                x = actionsList[i]
                if WithActionNames:
                    xName = '%s (%s)' % (self.actions[x]['name'],str(x))
                    html += '<tr><th bgcolor=%s align="left">%s</th>' \
                                      % (rowHeaderColor,xName)
                else:
                    try:
                        xName = self.actions[x]['shortName']
                    except:
                        xName = str(x)
                    html += '<tr><th bgcolor=%s>%s</th>' % (rowHeaderColor,xName)
                for g in criteriaList:
                    if self.evaluation[g][x] != NA:
                        formatString = '<td bgcolor=%s align="right">%% .%df</td>' \
                                                      % (quantileColor[x][g],ndigits)
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
        for col in range(0,nc):
            html += '<td bgcolor=%s>&nbsp;%.2f&#037;</td>' \
                % (colorPalette[col][1],
                   colorPalette[col][0]*Decimal('100.0'))
        html += '</tr>\n'
        html += '</table>\n'
        if criteriaCorrelation is not None:
            html += '<b>(*) tau:</b> <i>Ordinal (Kendall) correlation between</i><br><i>marginal criterion and global ranking relation</i><br/>\n'
        if rankCorrelation is not None:
            html += '<i>Outranking model</i>: <b>%s</b>, <i>Ranking rule</i>: <b>%s</b><br/>\n' % (outrankingModel,rankingRule)
            html += '<i>Ordinal (Kendall) correlation between</i><br/><i>global ranking and global outranking relation:</i> <b>%+.3f</b><br/>\n' % (rankCorrelation['correlation'])
            html += '<i>Mean marginal correlation (a)               :</i> <b>%+.3f</b><br/>\n' % (meanMarginalCriteriaCorrelation)
            html += '<i>Standard marginal correlation deviation (b) :</i> <b>%+.3f</b><br/>\n' % (sdMarginalCriteriaCorrelation)
            html += '<i>Ranking fairness (a) - (b)                  :</i> <b>%+.3f</b><br/>\n' % (float(meanMarginalCriteriaCorrelation) - sdMarginalCriteriaCorrelation)
            html += '</body></html>'
        return html

    def _computeRankingConsensusQuality(self,ranking,Comments=False,Threading=False,nbrOfCPUs=1):
        """
        Renders the marginal criteria correlations with a given ranking with summary.
        """
        from outrankingDigraphs import BipolarOutrankingDigraph
        from math import sqrt
        g = BipolarOutrankingDigraph(self,Normalized=True)
        criteria = self.criteria
        marginalCorrelations \
            = g.computeMarginalVersusGlobalRankingCorrelations(
                                ranking,ValuedCorrelation=True,
                                Threading=Threading,
                                nbrCores=nbrOfCPUs)
        ncrit = Decimal(str(len(marginalCorrelations)))
        meanMarginalCorrelation = Decimal('0.0')
        varMarginalCorrelation = Decimal('0.0')
        moment4 = Decimal('0.0')
        sumWeights = Decimal('0.0')
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            sumWeights += abs(criteria[cg[1]]['weight'])
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            meanMarginalCorrelation += cg[0]*cgw
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            varMarginalCorrelation += ((cg[0]-meanMarginalCorrelation)**2)*cgw
            moment4 += ((cg[0]-meanMarginalCorrelation)**4)*cgw
            #varMarginalCorrelation += (cg[0]**2)*cgw
        #meanMarginalCriteriaCorrelation /= ncrit
        #varMarginalCriteriaCorrelation /= ncrit
        #varMarginalCorrelation -= meanMarginalCorrelation*meanMarginalCriteriaCorrelation
        sdMarginalCorrelation = sqrt(varMarginalCorrelation)
        kurtosis = moment4 -3
        # showing the results
        if Comments:
            print('Consensus quality of ranking:')
            print(ranking)
            print('criterion (weight): correlation')
            print('-------------------------------')
            for cg in marginalCorrelations:
                print('%s (%.3f): %+.3f' % (cg[1],abs(criteria[cg[1]]['weight'])/sumWeights,cg[0]) )
            print('Summary:')
            print('Weighted mean marginal correlation (a): %+.3f' % meanMarginalCorrelation)
            print('Standard deviation (b)                : %+.3f' % sdMarginalCorrelation)
            print('Ranking fairness (Kurtosis a^4/b^4)   : %+.3f' % kurtosis)
        return (marginalCorrelations,meanMarginalCorrelation,sdMarginalCorrelation)



    def computeRankingConsensusQuality(self,ranking,Comments=False,Threading=False,nbrOfCPUs=1):
        """
        Renders the marginal criteria correlations with a given ranking with summary.
        """
        from outrankingDigraphs import BipolarOutrankingDigraph
        from math import sqrt
        g = BipolarOutrankingDigraph(self,Normalized=True)
        criteria = self.criteria
        marginalCorrelations \
                     =  g.computeMarginalVersusGlobalRankingCorrelations(
                                ranking,ValuedCorrelation=True,Threading=Threading,
                                nbrCores=nbrOfCPUs)
        ncrit = Decimal(str(len(marginalCorrelations)))
        meanMarginalCorrelation = Decimal('0.0')
        varMarginalCorrelation = Decimal('0.0')
        sumWeights = Decimal('0.0')
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            sumWeights += abs(criteria[cg[1]]['weight'])
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            meanMarginalCorrelation += cg[0]*cgw
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            varMarginalCorrelation += ((cg[0]-meanMarginalCorrelation)**2)*cgw
            #varMarginalCorrelation += (cg[0]**2)*cgw
        #meanMarginalCriteriaCorrelation /= ncrit
        #varMarginalCriteriaCorrelation /= ncrit
        #varMarginalCorrelation -= meanMarginalCorrelation*meanMarginalCriteriaCorrelation
        sdMarginalCorrelation = sqrt(varMarginalCorrelation) 
        # showing the results
        if Comments:
            print('Consensus quality of ranking:')
            print(ranking)
            print('criterion (weight): correlation')
            print('-------------------------------')
            for cg in marginalCorrelations:
                print('%s (%.3f): %+.3f' % (cg[1],abs(criteria[cg[1]]['weight'])/sumWeights,cg[0]) )
            print('Summary:')
            print('Weighted mean marginal correlation (a): %+.3f' % meanMarginalCorrelation)
            print('Standard deviation (b)                : %+.3f' % sdMarginalCorrelation)
            print('Ranking fairness (a)-(b)              : %+.3f' \
                       % (float(meanMarginalCorrelation) - sdMarginalCorrelation) )
        return (marginalCorrelations,
                meanMarginalCorrelation,
                sdMarginalCorrelation)
        
    def showRankingConsensusQuality(self,ranking):
        """
        shows the marginal criteria correlations with a given ranking with summary.
        """
        self.computeRankingConsensusQuality(ranking,Comments=True)

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
        NA = self.NA
        evaluation = self.evaluation
        criteria = self.criteria
        actions = self.actions
        
        print('*---- Evaluation statistics ----*')
        average = Decimal('0.0')
        n = Decimal('0.0')
        for g in criteria:
            for x in actions:
                if evaluation[g][x] != NA:
                    average += evaluation[g][x]
                    n += 1
        average = average/n
        print('average      : %2.2f ' % (average))
        variance = Decimal('0.0')
        for g in criteria:
            for x in actions:
                if evaluation[g][x] != NA:
                    variance += (evaluation[g][x]-average)*(evaluation[g][x]-average)
        variance = variance/n
        print('variance     : %2.2f ' % (variance))
        stddev = math.sqrt(variance)
        print('std deviation: %2.2f ' % (stddev))      

    def save(self,fileName='tempperftab',isDecimal=True,
             valueDigits=2,Comments=True):
        """
        Persistant storage of Performance Tableaux.
        """
        if Comments:
            print('*--- Saving performance tableau in file: <' \
              + str(fileName) + '.py> ---*')
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
        # name
        fo.write("name = \'%s\'\n" % fileName)
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
            gKeys = list(self.criteria[g].keys())
            for it in gKeys:
                fo.write('\'%s\': %s,\n' % (it,repr(self.criteria[g][it])))
            if 'preferenceDirection' not in gKeys:
                fo.write('\'preferenceDirection\': \'max\' \n')
            fo.write('}),\n')
        fo.write('])\n')
        # missing data symbol
        try:
            fo.write("NA = Decimal('%s')\n" % (str(self.NA)) )
        except:
            fo.write("NA = Decimal('-999')\n")
        # evaluations
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

    def _saveXML(self,name='temp',category='standard',
                 subcategory='standard',author='digraphs Module (RB)',
                 reference='saved from Python'):
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
            fo.write('<indifference>'+str(criteria[g]['thresholds']['ind'])\
                                                     +'</indifference>\n')
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

    def _saveXMLRubis(self,name='temp',category='Rubis',subcategory='new D2 version',author='digraphs Module (RB)',reference='saved from Python'):
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


    def _saveXMCDA(self,fileName='temp',category='New XMCDA Rubis format',user='digraphs Module (RB)',version='saved from Python session',variant='Rubis',valuationType='standard',servingD3=True):
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
                if criteria[g]['thresholds']['ind'] is not None:
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
                if criteria[g]['thresholds']['weakPreference'] is not None:
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
                if criteria[g]['thresholds']['pref'] is not None:
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
                if criteria[g]['thresholds']['weakVeto'] is not None:
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
                if criteria[g]['thresholds']['veto'] is not None:
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

    def saveXMCDA2(self,fileName='temp',
                   category='XMCDA 2.0 Extended format',
                   user='digraphs Module (RB)',
                   version='saved from Python session',
                   title='Performance Tableau in XMCDA-2.0 format.',
                   variant='Rubis',
                   valuationType='bipolar',
                   servingD3=False,
                   isStringIO=False,
                   stringNA='NA',
                   comment='produced by saveXMCDA2()',
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
                if criteria[g]['thresholds']['ind'] is not None:
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
                if criteria[g]['thresholds']['weakPreference'] is not None:
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
                if criteria[g]['thresholds']['pref'] is not None:
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
                    if criteria[g]['thresholds']['weakVeto'] is not None:
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
                    if criteria[g]['thresholds']['veto'] is not None:
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
                if evaluation[g][actionsList[i]] == self.NA:
                    val = evaluation[g][actionsList[i]]
                else:
                    val = pdir*evaluation[g][actionsList[i]]
                if val == self.NA:
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
            fo.close()
            return problemText
        else:
            fo.close()
            print('File: ' + nameExt + ' saved !')

    def _saveXMCDA2(self,fileName='temp',
                   category='XMCDA 2.0 format',
                   user='digraphs Module (RB)',
                   version='saved from Python session',
                   title='Performance Tableau in XMCDA-2.0 format.',
                   variant='Rubis',
                   valuationType='bipolar',
                   servingD3=True,
                   isStringIO=False,
                   stringNA='NA',
                   comment='produced by saveXMCDA2()',
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
                if criteria[g]['thresholds']['ind'] is not None:
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
                if criteria[g]['thresholds']['weakPreference'] is not None:
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
                if criteria[g]['thresholds']['pref'] is not None:
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
                    if criteria[g]['thresholds']['weakVeto'] is not None:
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
                    if criteria[g]['thresholds']['veto'] is not None:
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
        NA = self.NA
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
                if val == NA:
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

    def saveXMCDA2String(self,fileName='temp',category='XMCDA 2.0 format',
                         user='digraphs Module (RB)',version='saved from Python session',
                         title='Performance Tableau in XMCDA-2.0 format.',variant='Rubis',
                         valuationType='bipolar',servingD3=True,comment='produced by stringIO()',
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
                if criteria[g]['thresholds']['ind'] is not None:
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
                if criteria[g]['thresholds']['weakPreference'] is not None:
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
                if criteria[g]['thresholds']['pref'] is not None:
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
                if criteria[g]['thresholds']['weakVeto'] is not None:
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
                if criteria[g]['thresholds']['veto'] is not None:
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
        NA = self.NA
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
                if val == NA:
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
        NA = self.NA
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
                        if evaluation[g][x] != NA and evaluation[g][y] != NA:
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
        NA = self.NA
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
                if evaluation[g][x] != NA:
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
                        if evaluation[g][x] != NA and evaluation[g][y] != NA:
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
        NA = self.NA
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
                if evaluation[g][x] != NA:
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
                    normEvaluation[g][x] = NA
                    
        return normEvaluation

    def quantizeCriterionEvaluations(self,g,q,ndigits=2,Debug=True):
        """
        q-tile evaluation of criterion q
        """
        actions = self.actions
        criterion = self.criteria[g]
        evaluation = self.evaluation
        NA = self.NA
        actionKeys = [x for x in actions]
        quantilesFrequencies = []
        for i in range(q+1):
            quantilesFrequencies.append( Decimal(str(i)) / Decimal(str(q)) )
        criterionActionsQuantiles = {}
        formatString = '%%.%df' % ndigits
        criterionValues = [evaluation[g][x] for x in actionKeys if
                               evaluation[g][x] != NA]
        criterionValues.sort()
        ng = len(criterionValues)
        criterionActionsQuantiles = {}
        for x in actionKeys:
            indxinf = criterionValues.index(evaluation[g][x])
            lx = [v for v in criterionValues if v <= evaluation[g][x]]
            indxsup = len(lx)
            indx = ((indxinf+indxsup)/2)/ng
            actionQuantile = Decimal(formatString % indx)
            aq = 0
            for qfreq in quantilesFrequencies:
                if actionQuantile < qfreq:
                    criterionActionsQuantiles[x] = aq
                    break
                else:
                    aq += 1
        if Debug:
            print(g)
            print(criterionActionsQuantiles)
        self.criteria[g]['comment'] = '%s-tiled evaluations' % q
        self.criteria[g]['thresholds'] = {'ind': (Decimal('0.0'), Decimal('0.0')),
                                          'pref': (Decimal('1.0'), Decimal('0.0'))}
        self.criteria[g]['scale'] = (1,q)
        self.evaluation[g] = criterionActionsQuantiles
   
    def restoreOriginalEvaluations(self,lowValue=0.0,highValue=100.0,Debug=False):
        """
        recode the evaluations to their original values on all criteria
        """
        evaluation = self.evaluation
        NA = self.NA
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
                if evaluation[g][x] != NA:
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
                    restoredEvaluation[g][x] = NA
                    
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
        self.NA = None

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
        if inPerfTab.__class__ in [RandomCBPerformanceTableau,
                                   Random3ObjectivesPerformanceTableau,
                                   RandomPerformanceTableau]:
            self.__class__ = inPerfTab.__class__
        # name
        self.name = 'partial-'+inPerfTab.name
        # actions
        if actionsSubset is not None:
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
        if objectivesSubset is None:
            try:
                objectives = deepcopy(inPerfTab.objectives)
            except:
                HasObjectives = False
            if criteriaSubset is not None:
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
            if criteriaSubset is None:
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

        try:
            self.NA = perfTab.NA
        except:
            self.NA = Decimal('-999')
        
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
        if actionsSubset is None:
            actionsSubset = self.actions

        self.criteria = deepcopy(inPerfTab.criteria)
        if criteriaSubset is None:
            criteriaSubset = self.criteria

        self.weightPreorder = self.computeWeightPreorder()

        self.evaluation = deepcopy(inPerfTab.evaluation)
        try:
            self.NA = deepcopy(inPerfTab.NA)
        except:
            self.NA = Decimal('-999')

        actionsKeys = [x for x in actionsSubset]
        criteriaKeys = [g for g in criteriaSubset]
        for g in criteriaKeys:
            constantPerformance = (self.criteria[g]['scale'][1] - \
                    self.criteria[g]['scale'][0]) * position
            for x in actionsKeys:
                self.evaluation[g][x] = Decimal(str(constantPerformance))
                                    
#-----------------------
class CircularPerformanceTableau(PerformanceTableau):
    """
    Constructor for circular performance tableaux.
    """
    def __init__(self,order=5,scale=(0.0,100.0),NoPolarisation=True):
        from copy import deepcopy
        from randomPerfTabs import RandomPerformanceTableau
        self.name = 'circular-%s-PT' % str(order)

        t = RandomPerformanceTableau(numberOfActions=order,
                                     numberOfCriteria=order)
        self.actions = deepcopy(t.actions)
        self.criteria = deepcopy(t.criteria)
        if NoPolarisation:
            for g in self.criteria:
                giThs = self.criteria[g]['thresholds']
                giThs.pop('veto')
        self.weightPreorder = t.computeWeightPreorder()
        self.evaluation = deepcopy(t.evaluation)
        self.NA = deepcopy(t.NA)
        step = scale[1]/order
        grades = [i * step for i in range(order)]
        criteriaList = [g for g in self.criteria]
        actionsList = [x for x in self.actions]
        for i in range(order):
            gi = criteriaList[i]
            for j in range(order):
                xj = actionsList[j]
                self.evaluation[gi][xj] = Decimal(str(grades[j]))
            lastGrade = grades.pop()
            grades.insert(0,lastGrade)      
                                    
# ----------------------
class NormalizedPerformanceTableau(PerformanceTableau):
    """
    specialsation of the PerformanceTableau class for
    constructing normalized, 0 - 100, valued PerformanceTableau
    instances from a given argPerfTab instance.
    """
    def __init__(self,argPerfTab=None,lowValue=0,highValue=100,
                 coalition=None,Debug=False):
        from copy import deepcopy
        from decimal import Decimal
        if isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        elif argPerfTab is None:
            print('Error: a valid PerformanceTableau instance is required !')
            perfTab = None
        else:
            perfTab = argPerfTab      
        self.name = 'norm_'+ perfTab.name
        try:
            self.description = deepcopy(perfTab.description)
        except:
            pass
        self.actions = deepcopy(perfTab.actions)
        self.criteria = deepcopy(perfTab.criteria)
        self.evaluation = deepcopy(perfTab.evaluation)
        try:
            self.NA = deepcopy(perfTab.NA)
        except:
            self.NA = Decimal('-999')
        self.evaluation = self.normalizeEvaluations(lowValue,highValue,Debug)
        criteria = self.criteria        
        for g in criteria:
            if criteria[g]['weight'] < 0:
                criteria[g]['weight'] = -criteria[g]['weight']
            try:
                for th in criteria[g]['thresholds']:
                    empan = Decimal(str(criteria[g]['scale'][1]-criteria[g]['scale'][0]))
                    intercept = criteria[g]['thresholds'][th][0]/empan\
                                * (Decimal(str(highValue-lowValue)))
                    slope = criteria[g]['thresholds'][th][1]
                    criteria[g]['thresholds'][th] = (intercept,slope)
            except:
                pass
            criteria[g]['scale'] = [lowValue,highValue]
        self.criteria = criteria        

# ----------------------
##class QunantizedPerformanceTableau(PerformanceTableau):
##    """
##    specialsation of the PerformanceTableau class for
##    constructing quantized valued PerformanceTableau
##    instances from a given argPerfTab instance.
##    """
##    def __init__(self,argPerfTab=None,
##                 criteriaSubset=None,Debug=False):
##        from copy import deepcopy
##        from decimal import Decimal
##        if isinstance(argPerfTab,(str)):
##            perfTab = PerformanceTableau(argPerfTab)
##        elif argPerfTab is None:
##            print('Error: a valid PerformanceTableau instance is required !')
##            perfTab = None
##        else:
##            perfTab = argPerfTab      
##        self.name = 'norm_'+ perfTab.name
##        try:
##            self.description = deepcopy(perfTab.description)
##        except:
##            pass
##        self.actions = deepcopy(perfTab.actions)
##        self.criteria = deepcopy(perfTab.criteria)
##        self.evaluation = deepcopy(perfTab.evaluation)
##        try:
##            self.NA = deepcopy(perfTab.NA)
##        except:
##            self.NA = Decimal('-999')
##        self.evaluation = self.normalizeEvaluations(lowValue,highValue,Debug)
##        criteria = self.criteria        
##        for g in criteria:
##            if criteria[g]['weight'] < 0:
##                criteria[g]['weight'] = -criteria[g]['weight']
##            try:
##                for th in criteria[g]['thresholds']:
##                    empan = Decimal(str(criteria[g]['scale'][1]-criteria[g]['scale'][0]))
##                    intercept = criteria[g]['thresholds'][th][0]/empan\
##                                * (Decimal(str(highValue-lowValue)))
##                    slope = criteria[g]['thresholds'][th][1]
##                    criteria[g]['thresholds'][th] = (intercept,slope)
##            except:
##                pass
##            criteria[g]['scale'] = [lowValue,highValue]
##        self.criteria = criteria        

###################################
# Specialisations
###################################

class XMCDA2PerformanceTableau(PerformanceTableau):
    """
    For reading stored XMCDA 2.0 formatted instances with exact decimal numbers.
    Using the inbuilt module xml.etree (for Python 2.5+).

    Parameters:
        * fileName is given without the extension ``.xml`` or ``.xmcda``,
        * HasSeparatedWeights in XMCDA 2.0.0 encoding (default = False),
        * HasSeparatedThresholds in XMCDA 2.0.0 encoding (default = False),
        * stringInput: instantiates from an XMCDA 2.0 encoded string argument.

    !! *Obsolete by now* !!
           
    """
    #from collections import OrderedDict
    
    def __init__(self,fileName='temp',HasSeparatedWeights=False,
                 HasSeparatedThresholds=False,stringInput=None,
                 Debug=False):
        
        from xml.etree import ElementTree
        if stringInput is None:
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
        #for elem in [x for x in XMCDA.find('projectReference').getchildren()]:
        for elem in [x for x in XMCDA.find('projectReference')]:
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
            
        if XMCDA.find('methodParameters').find('parameters') is not None:
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
        #for elem in [x for x in XMCDA.find('alternatives').find('description').getchildren()]:
        for elem in [x for x in XMCDA.find('alternatives').find('description')]:
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
                    #for elem in [y for y in x.find('description').getchildren()]:
                    for elem in [y for y in x.find('description')]:
                        actions[x.attrib['id']][elem.tag] = elem.text
                except:
                    pass
        self.actions = actions
        
        if XMCDA.find('objectives') is not None:  # objectives are defined
            objectives = OrderedDict()
            # get objectives' description
            if XMCDA.find('objectives').find('description') is not None:
                description = {}
                #for elem in [x for x in XMCDA.find('criteria').find('description').getchildren()]:
                for elem in [x for x in XMCDA.find('criteria').find('description')]:
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
                    #for elem in [y for y in obj.find('description').getchildren()]:
                    for elem in [y for y in obj.find('description')]:
                        objectives[obj.attrib['id']][elem.tag] = elem.text
                    if obj.find('weight') is not None:
                        try:
                            objectives[obj.attrib['id']]['weight'] = Decimal(obj.find('weight').find('value').find('real').text)
                        except:
                            criteria[obj.attrib['id']]['weight'] = Decimal(obj.find('weight').find('value').find('integer').text)
                    if obj.find('objectiveCriteria') is not None:
                        objectives[obj.attrib['id']]['criteria'] = literal_eval(obj.find('objectiveCriteria').text)
            self.objectives = objectives
        else:  # no objectives are given
            pass
        
        criteria = OrderedDict()
        # get criteria' description
        if XMCDA.find('criteria').find('description') is not None:
            description = {}
            #for elem in [x for x in XMCDA.find('criteria').find('description').getchildren()]:
            for elem in [x for x in XMCDA.find('criteria').find('description')]:
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
                #for elem in [y for y in g.find('description').getchildren()]:
                for elem in [y for y in g.find('description')]:
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
                    if g.find('thresholds') is not None:
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
        NA = Decimal('-999')
        self.NA = NA
        description = {}
        #for elem in [x for x in XMCDA.find('performanceTable').find('description').getchildren()]:
        for elem in [x for x in XMCDA.find('performanceTable').find('description')]:
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
                        evaluationAP[a][x.find('criterionID').text]=NA
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
                if evaluationAP[a][g] != NA:
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
    def __init__(self,fileName='temp',Debug=False):
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
        # objectives dictionary
        self.objectives = OrderedDict()
        # criteria dictionary
        ng = len(csvText)-1
        for j in range(1,ng+1):
            print(j,csvText[j][0])
        self.criteria = OrderedDict([(csvText[j][0],{'comment':'performance criteria'}) for j in range(1,ng+1)])

        # criteria attributes
        for j in range(1,ng+1):
            g = csvText[j][0]
            self.criteria[g]['name']  = csvText[j][1]          
            self.criteria[g]['weight']  = Decimal(csvText[j][2])
            self.criteria[g]['scale']  = eval(csvText[j][3]) 
            self.criteria[g]['preferenceDirection'] = csvText[j][4]
            self.criteria[g]['thresholds']  = eval(csvText[j][5])
            print(self.criteria[g])
        self.weightPreorder = self.computeWeightPreorder()
 
        # evaluation tableau
        evaluation = {}
        for j in range(1,ng+1):
            evaluation[csvText[j][0]] = {}
            for i in range(6,na+1):
                evaluation[csvText[j][0]][csvText[0][i]] = Decimal(csvText[j][i])
        self.evaluation = evaluation
        self.NA = Decimal('-999')

#----------test Digraph class ----------------
if __name__ == "__main__":
    
    from digraphs import *
    from perfTabs import *
    from outrankingDigraphs import *
    import sortingDigraphs
    from linearOrders import *
    from transitiveDigraphs import *
    from randomPerfTabs import *
    from time import time
    import random

    print("""
    ****************************************************
    * Digraph3 perfTabs module                         *
    * Copyright (C) 2011-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)
    
    print('*-------- Testing classes and methods -------')
    
    randomSeed = random.randint(1,1000)
##    t = CircularPerformanceTableau(order=7)
##    t.showPerformanceTableau()
    t = RandomCBPerformanceTableau(numberOfCriteria=21,
                                   numberOfActions=13,
                                   weightDistribution='equiobjectives',
                                   IntegerWeights=True,
                                   NegativeWeights=False,
                                   missingDataProbability=0.05,
                                   seed=randomSeed,
                                   Debug=False)
    # t.computeOutrankingConsensusQuality()
#     t.showPerformanceTableau()
#     t.computeMissingDataProportion(InPercents=False,Comments=True)
#     t.replaceNA(Decimal('-999'),Comments=True)
#     t.computeMissingDataProportion(InPercents=False,Comments=True)
                    
#     t.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=5,
#                                  rankingRule='NetFlows',Transposed=False)
# ##    t.showHTMLPerformanceHeatmap(outrankingModel='this',
# ##                                   Correlations=True,colorLevels=5,
# ##                                rankingRule='NetFlows',Transposed=False)
#     t.showHTMLPerformanceHeatmap(outrankingModel='confident',
#                                  Correlations=True,colorLevels=5,
#                                  rankingRule='NetFlows',Transposed=False)
#     t.showHTMLPerformanceHeatmap(outrankingModel='robust',
#                                  Correlations=True,colorLevels=5,
#                                  rankingRule='NetFlows',Transposed=False)

#     g = RobustOutrankingDigraph(t)
#     g.showHTMLPerformanceHeatmap(outrankingModel='this',
#                                    Correlations=True,colorLevels=5,
#                                  rankingRule='NetFlows',Transposed=False)    
#     t.save('testow')
#     t1 = PerformanceTableau('testow')
#     t1.showObjectives()
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. August 2015                  *')
    print('* $Revision: Python3.9 $            *')                   
    print('*************************************')

#############################
# Log record for changes:
# $Log: perfTabs.py,v $
# Revision 1.37  2012/12/24 15:18:21
# compatibility patch for old (-2008) python performance tableaux
#############################
