#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python implementation of digraphs
# submodule perfTabs.py  for performance tableaux  
# Current revision $Revision: 1.37 $
# Copyright (C) 2011  Raymond Bisdorff
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

__version__ = "$Revision: 1.37 $"
# $Source: /home/cvsroot/Digraph/perfTabs.py,v $

from perfTabs import *

from decimal import Decimal

# ----------  old XML handling ------------------
try:
    from xml.sax import *
except:
    print('XML extension will not work with this Python version!')

class _XMLPerformanceTableauHandler(ContentHandler):
    """
    A private handler to deal with performance tableaus stored in XML format.
    """

    inName = 0
    performanceTableauName = ''
    inActions = 0
    inAction = 0
    actionName = ''
    actions = []
    inCriteria = 0
    inCriterion = 0
    criterionName = ''
    inWeight = 0
    weightValue = ''
    criteria = {}
    inScale = 0
    scaleValue = '('
    inMin = 0
    minValue = ''
    inMax = 0
    maxValue = ''
    inValue = 0
    valueText = ''
    inThresholds = 0
    inIndifference = 0
    inPreference = 0
    inWeakveto = 0
    inVeto = 0
    inEvaluations = 0
    evaluation = {}
    inEvaluation = 0
    inEvalActions = 0
    
    
    def startElement(self,nodeName,attrs):
        if nodeName == 'performancetableau':          
            self.category = attrs.get("category", "")
            self.subcategory = attrs.get("subcategory", "")
            
        if nodeName == 'name':
            self.inName = 1
            
        if nodeName == 'actions':
            self.actions = []
            self.inActions = 1

        if nodeName == 'action':
            self.actionName = ''
            self.inAction = 1

        if nodeName == 'criteria':
            self.criteria = {}
            self.inCriteria = 1

        if nodeName == 'critname':
            self.criterionName = ''
            self.inCriterion = 1

        if nodeName == 'weight':
            self.weightValue = ''
            self.inWeight = 1

        if nodeName == 'scale':
            self.scaleValue = '('
            self.inScale = 1

        if nodeName == 'min':
            self.minValue = ''
            self.inMin = 1

        if nodeName == 'max':
            self.maxValue = ''
            self.inMax = 1

        if nodeName == 'thresholds':
            self.thresholds = {}
            self.inThresholds = 1

        if nodeName == 'indifference':
            self.valueText = ''
            self.inIndifference = 1

        if nodeName == 'preference':
            self.valueText = ''
            self.inPreference = 1

        if nodeName == 'weakveto':
            self.valueText = ''
            self.inWeakveto = 1

        if nodeName == 'veto':
            self.valueText = ''
            self.inVeto = 1

        if nodeName == 'evaluations':
            self.evaluation = {}
            self.inEvaluations = 1

        if nodeName == 'evaluation':
            self.inEvaluation = 1

        if nodeName == 'evalactions':
            self.inEvalActions = 1

        if nodeName == 'value':
            self.inValue = 1
        

    def endElement(self,nodeName):

        if nodeName == 'name':
            self.inName = 0
            self.name = str(self.performanceTableauName)

        if nodeName == 'action' and self.inActions == 1:
            self.actions.append(str(self.actionName))
            self.inAction = 0

        if nodeName == 'action' and self.inEvalActions == 1:
            self.inAction = 0
            self.valueText = ''

        if nodeName == 'critname' and self.inCriteria == 1:
            self.criterion = str(self.criterionName)
            self.criteria[self.criterion]={}
            self.inCriterion = 0

        if nodeName == 'critname' and self.inEvaluation == 1:
            self.criterion = str(self.criterionName)
            self.evaluation[self.criterion] = {}

        if nodeName == 'actions':
            self.inActions = 0
            
        if nodeName == 'weight':
            self.criteria[self.criterion]['weight'] = Decimal(self.weightValue)
            self.weightValue = ''
            self.inWeight = 0

        if nodeName == 'thresholds':
            self.criteria[self.criterion]['thresholds'] = self.thresholds
            self.thresholds = {}
            self.inThresholds = 0

        if nodeName == 'scale':
            scaleString = str(self.scaleValue) +')'
            self.criteria[self.criterion]['scale'] = eval(scaleString)
            self.scaleValue = '('
            self.inScale = 0

        if nodeName == 'min':
            self.scaleValue += str(self.minValue)+','
            self.minValue = ''
            self.inMin = 0

        if nodeName == 'max':
            self.scaleValue += str(self.maxValue)
            self.maxValue = ''
            self.inMax = 0

        if nodeName == 'indifference':
            value = eval(self.valueText)
            self.thresholds['ind'] = (Decimal(str(value[0])),Decimal(str(value[1])))
            self.valueText = ''
            self.inIndifference = 0

        if nodeName == 'preference':
            value = eval(self.valueText)
            self.thresholds['pref'] = (Decimal(str(value[0])),Decimal(str(value[1])))
            self.valueText = ''
            self.inPreference = 0

        if nodeName == 'weakveto':
            value = eval(self.valueText)
            self.thresholds['weakveto'] = (Decimal(str(value[0])),Decimal(str(value[1])))
            self.valueText = ''
            self.inWeakveto = 0

        if nodeName == 'veto':
            value = eval(self.valueText)
            self.thresholds['veto'] = (Decimal(str(value[0])),Decimal(str(value[1])))
            self.valueText = ''
            self.inVeto = 0
            
        if nodeName == 'criteria':
            self.inCriteria = 0

        if nodeName == 'evaluations':
            self.inEvaluations = 0

        if nodeName == 'evaluation':
            self.inEvaluation = 0

        if nodeName == 'evalactions':
            self.inEvalActions = 0

        if nodeName == 'value':
            self.evaluation[self.criterion][str(self.actionName)] = Decimal(self.valueText)

            self.inValue = 0


    def characters(self, ch):
        if self.inName:
            self.performanceTableauName += ch
        if self.inAction: 
            self.actionName += ch
        if self.inCriterion:
            self.criterionName += ch
        if self.inWeight:
            self.weightValue += ch
        if self.inMin:
            self.minValue += ch
        if self.inMax:
            self.maxValue += ch
        if self.inIndifference:
            self.valueText += ch
        if self.inPreference:
            self.valueText += ch
        if self.inWeakveto:
            self.valueText += ch
        if self.inVeto:
            self.valueText += ch
        if self.inValue:
            self.valueText += ch
        



class PerformanceTableau(object):
    """
    A general class for tacling MCDA performance tableaux.

    
    """
    def __init__(self,filePerfTab=None,isEmpty=False):
        
        if filePerfTab != None:
            fileName = filePerfTab + '.py'
            exec(compile(open(fileName).read(), fileName, 'exec'))
            self.name = str(filePerfTab)
            try:
                self.actions = locals()['actions']
            except:
                self.actions = locals()['actionset']
            try:
                self.weightset = locals()['weightset']
                self.thresholds = locals()['threshold']
                self.criteria = {}
                for g in locals()['criteria']:
                    self.criteria[g] = {'weight':Decimal(str(self.weightset[g])), 'thresholds': self.thresholds[g]}
                    
                
            except:
                self.criteria = locals()['criteria']
            try:
                self.weightPreorder = locals()['weightorder']
            except:
                self.weightPreorder = self.computeWeightPreorder()
            self.evaluation = locals()['evaluation']
        elif not isEmpty:
            import copy
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
        for g in criteria:
            sumWeights += criteria[g]['weight']

        weightedAverage = {} 
        for x in [z for z in actions]:
            weightedAverage[x] = Decimal('0.0')
            for g in [z for z in criteria]:
                weightedAverage[x] += evaluation[g][x] * criteria[g]['weight'] / sumWeights
        if isListRanked:
            ranked = []
            for x in weightedAverage:
                ranked.append((weightedAverage[x],x))
            ranked.sort(reverse=True)
            return ranked
        else:
            return weightedAverage
        
    
    def showCriteria(self,IntegerWeights=False,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
        print('*----  criteria -----*')
        sumWeights = Decimal('0.0')
        for g in self.criteria:
            sumWeights += self.criteria[g]['weight']
        criteriaList = [g for g in self.criteria]
        criteriaList.sort()
        for g in criteriaList:
            try:
                criterionName = self.criteria[g]['name']
            except:
                criterionName = ''
            print(g, repr(criterionName))
            print('  Scale =', self.criteria[g]['scale'])
            if IntegerWeights:
                print('  Weight = %d ' % (self.criteria[g]['weight']))
            else:
                weightg = self.criteria[g]['weight']/sumWeights
                print('  Weight = %.3f ' % (weightg))
            try:
                for th in self.criteria[g]['thresholds']:
                    if Debug:
                        print('-->>>', th,self.criteria[g]['thresholds'][th][0],self.criteria[g]['thresholds'][th][1])
                    print('  Threshold %s : %.2f + %.2fx' % (th,self.criteria[g]['thresholds'][th][0],self.criteria[g]['thresholds'][th][1]), end=' ')
                    #print self.criteria[g]['thresholds'][th]
                    print('; percentile: ',self.computeVariableThresholdPercentile(g,th,Debug))
            except:
                pass
            print() 
 
        
    def computePerformanceDifferences(self,comments = False, Debug = False):
        """
        Adds to the criteria dictionary the ordered list of all observed performance differences.
        """
        
        if Debug:
            comments = True
        if comments:
            print('Compute performance differences on each criterion')
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        actionsList = [x for x in self.actions]
        n = len(actionsList)

        for c in criteriaList:
            ed = Decimal(str(self.criteria[c]['scale'][1])) - Decimal(str(self.criteria[c]['scale'][0]))
            md = Decimal('0')
            #diff = set()
            diffList = []
            for i in range(n):
                for j in range(i+1,n):
                    delta = abs(self.evaluation[c][actionsList[i]] - self.evaluation[c][actionsList[j]])
                    if delta < ed:
                        ed = delta
                    if delta > md:
                        md = delta
                    #diff.add(delta)
                    diffList.append(delta)
                    if Debug:
                        print('-->> i,j, self.evaluation[actionsList[i]],self.evaluation[actionsList[j]], delta, ed,md', i,j, self.evaluation[c][actionsList[i]],self.evaluation[c][actionsList[j]], delta, ed,md,diffList)
            self.criteria[c]['minimalPerformanceDifference'] = ed
            self.criteria[c]['maximalPerformanceDifference'] = md
            #diffList = list(diff)
            diffList.sort()
            self.criteria[c]['performanceDifferences'] = diffList
            if comments:
                print(' -->', c, ': ', self.criteria[c]['minimalPerformanceDifference'], self.criteria[c]['maximalPerformanceDifference'])
                print(len(self.criteria[c]['performanceDifferences']),self.criteria[c]['performanceDifferences'])
                print(self.criteria[c]['performanceDifferences'][0], self.criteria[c]['performanceDifferences'][-1])

    def computeActionCriterionPerformanceDifferences(self,refAction,refCriterion,comments = False, Debug = False):
        """
        computes the performances differences observed between the reference action and the others on the given criterion
        """
        
        if Debug:
            comments = True
        if comments:
            print('Compute performance differences for action %s on criterion %s' % (refAction, refCriterion))

        otherActionsList = [x for x in self.actions]
        otherActionsList.remove(refAction)
        diff = []
        for x in otherActionsList:
            delta = abs(self.evaluation[refCriterion][refAction] - self.evaluation[refCriterion][x])
            diff.append(delta)
            if Debug:
                print('-->> refAction, x, evaluation[refAction], evaluation[x], delta,diff', refAction,x, self.evaluation[refCriterion][refAction],self.evaluation[refCriterion][x], delta,diff)

        diff.sort()
        return diff

    def computeActionCriterionQuantile(self,action, criterion,Debug=False):
        """
        renders the quantile of the performance of action on criterion
        """
        if Debug:
            print(action,criterion)
        perfx = self.evaluation[criterion][action]
        if perfx != -999:
            try:
                indx = self.criteria['thresholds']['ind'][0] + self.criteria[criterion]['thresholds']['ind'][1]*perfx
                ## indx = self.criteria['thresholds']['ind'][0] + self.criteria[criterion]['thresholds']['pref'][1]*perfx
            except:
                indx = Decimal('0')
            quantile = float(len([y for y in self.evaluation[criterion] if self.evaluation[criterion][y] <= perfx+indx]))/float(len(self.actions))
            return quantile
        else:
            return 'NA'

    def computeQuantiles(self,Debug=False):
        """
        renders a quantiles matrix action x criterion with the performance quantile of action on criterion
        """
        actionsList = [x for x in self.actions]
        criteriaList = list(self.criteria.keys())
        if Debug:
            print(actionsList,criteriaList)
        quantiles = {}
        for x in actionsList:
            quantiles[x] = self.computeActionQuantile(x,Debug)
        self.quantiles = quantiles
        return quantiles

    def computeActionQuantile(self,action,Debug=True):
        """
        renders the overall performance quantile of action
        """
        criteriaList = [x for x in self.criteria]
        criteriaQuantiles = []
        sumWeights = 0
        for g in criteriaList:
            agq = self.computeActionCriterionQuantile(action,g,Debug)
            if agq != 'NA':
                sumWeights += self.criteria[g]['weight']
                criteriaQuantiles.append((agq,float(self.criteria[g]['weight'])))
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
        fileNameExt = fileName+'.csv'
        fo = open(fileNameExt,'w')
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        actionsList = [x for x in self.actions]
        actionsList.sort()
        fo.write('# saved quantiles matrix from performance tableau %s \n' % self.name)
        fo.write('"quantiles",')
        n = len(actionsList)
        for i in range(n):
            x = actionsList[i]
            if i < n-1:
                fo.write('"%s",' % x)
            else:
                fo.write('"%s"\n' % x)
        print('\nweights  | ', end=' ') 
        for g in criteriaList:
            fo.write('"%s",' % g)
            for i in range(n):
                x = actionsList[i]
                if i < n-1:
                    fo.write('%.2f,' % self.computeActionCriterionQuantile(x,g,Debug=False) )
                else:
                    fo.write('%.2f\n' % self.computeActionCriterionQuantile(x,g,Debug=False) )                    
        fo.close()

        
    def showAllQuantiles(self):
        """
        renders a html string showing the table of
        the quantiles matrix action x criterion
        """
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        actionsList = [x for x in self.actions]
        actionsList.sort()
        html = '<table style="background-color:White;" border="1">\n'
        print('criteria | ', end=' ')
        html += '<tr bgcolor="#9acd32"><th>criteria</th>'
        for g in criteriaList:
            print(str(g) + '\t', end=' ')
            html += '<th>%s</th>' % (g)
        html += '</tr>\n'
        print('\nweights  | ', end=' ') 
        html += '<tr style="text-align: center;" bgcolor="#FFF79B"><td>weights</td>'
        for g in criteriaList:
            print(str(self.criteria[g]['weight']) + '\t', end=' ')
            html += '<td >%s</td>' % (self.criteria[g]['weight'])
        html += '</tr>\n'        
        print('\n-----------------------------------------------------')
        for x in actionsList:
            print(str(x) + '   | ', end=' ')
            html += '<tr><th  bgcolor="#FFF79B">%s</th>' % (x)
            for g in criteriaList:
                print('%.2f\t' % self.computeActionCriterionQuantile(x,g,Debug=False), end=' ')
                html += '<td>%.2f</td>' % (self.computeActionCriterionQuantile(x,g,Debug=False))
            print()
            html += '</tr>\n'
                                          
        html += '</table>\n'
        return html

    ## def showAllDiffQuantiles(self):
    ##     """
    ##     renders a html string showing the table of
    ##     the diff quantiles matrix action x criterion
    ##     """
    ##     criteriaList = [x for x in self.criteria]
    ##     criteriaList.sort()
    ##     actionsList = [x for x in self.actions]
    ##     actionsList.sort()
    ##     html = '<table style="background-color:White;" border="1">\n'
    ##     print 'criteria | ',
    ##     html += '<tr bgcolor="#9acd32"><th>criteria</th>'
    ##     for g in criteriaList:
    ##         print str(g) + '\t',
    ##         html += '<th>%s</th>' % (g)
    ##     html += '</tr>\n'
    ##     print '\nweights  | ', 
    ##     html += '<tr style="text-align: center;" bgcolor="#FFF79B"><td>weights</td>'
    ##     for g in criteriaList:
    ##         print str(self.criteria[g]['weight']) + '\t',
    ##         html += '<td >%s</td>' % (self.criteria[g]['weight'])
    ##     html += '</tr>\n'        
    ##     print '\n-----------------------------------------------------'
    ##     for x in actionsList:
    ##         print str(x) + '   | ',
    ##         html += '<tr><th  bgcolor="#FFF79B">%s</th>' % (x)
    ##         for g in criteriaList:
    ##             print '%.2f\t' % self.computeActionCriterionDiffQuantile(x,g,Debug=False),
    ##             html += '<td>%.2f</td>' % (self.computeActionCriterionDiffQuantile(x,g,Debug=False))
    ##         print
    ##         html += '</tr>\n'
                                          
    ##     html += '</table>\n'
    ##     return html
    
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
 
    def computeDefaultDiscriminationThresholds(self, quantile = {'ind':10,'pref':20,'weakVeto':60,'veto':80}, Debug = False, comments = False):
        """
        updates the discrimination thresholds with the percentiles
        from the performance differences.
        Parameters: quantile = {'ind': 10, 'pref': 20, 'weakVeto': 60, 'veto: 80}.
        
        """
        import math
        
        if Debug:
            comments = True
            
        if comments:
            print('Installs default discrimination thresholds on each criterion')

        self.computePerformanceDifferences(Debug,comments)
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        
        for c in criteriaList:
            vx = self.criteria[c]['performanceDifferences']
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

            
            self.criteria[c]['thresholds'] = {}
            for x in threshold:
                self.criteria[c]['thresholds'][x] = (threshold[x],Decimal('0.0'))

            if comments:
                print('criteria',c,' default thresholds:')
                print(self.criteria[c]['thresholds'])


    def computeThresholdPercentile(self,criterion, threshold, Debug=False):
        """
        computes for a given criterion the quantile
        of the performance differences of a given constant threshold.
        """
        try:
            performanceDifferences = self.criteria[criterion]['performanceDifferences']
        except:
            self.computePerformanceDifferences(Debug=Debug)
            performanceDifferences = self.criteria[criterion]['performanceDifferences']
        if Debug:
            print("performanceDifferences = ",performanceDifferences)
        try:
            quantile = self.criteria[criterion]['thresholds'][threshold][0]     
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

        
        actionsList = [x for x in self.actions]
        actionsList.sort()

        count = 0
        total = 0
        for a in actionsList:
            performanceDifferences = self.computeActionCriterionPerformanceDifferences(a,criterion,Debug)
            if Debug:
                print('performanceDifferences:', performanceDifferences)
            na = len(performanceDifferences)
            total += na
            i = 0
            quantile = Decimal(str(th[0])) + abs(self.evaluation[criterion][a])*Decimal(str(th[1]))
            if Debug:
                print('a,na,self.evaluation[criterion][a],th[0],th[1],quantile',a,na,self.evaluation[criterion][a],th[0],th[1],quantile)
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

    def showPerformanceTableau(self,sorted=True,ndigits=2):
        """
        Print the performance Tableau.
        """
        print('*----  performance tableau -----*')
        criteriaList = list(self.criteria)
        if sorted:
            criteriaList.sort()
        actionsList = list(self.actions)
        if sorted:
            actionsList.sort()
        print('criteria | weights |', end=' ')
        for x in actionsList:
            print('\''+str(x)+'\'  ', end=' ')
        print('\n---------|-----------------------------------------')
        for g in criteriaList:
            print('   \''+str(g)+'\'  |   '+str(self.criteria[g]['weight'])+'   | ', end=' ')
            for x in actionsList:
                formatString = '%% .%df ' % ndigits
                print(formatString % (self.evaluation[g][x]), end=' ')
            print()      


    def computeMinMaxEvaluations(self,criteria=None,actions=None):
        """
        renders minimum and maximum performances on each criterion
        in dictionary form: {'g': {'minimum': x, 'maximum': x}}
        """
        if criteria == None:
            criteria = [x for x in self.criteria]
        if actions == None:
            actions = [x for x in self.actions]
        result = {}
        for g in criteria:
            result[g] = {}
            evaluations = []
            for x in actions:
                evaluations.append(self.evaluation[g][x])
            evaluations.sort()
            result[g]['minimum'] = evaluations[0]
            result[g]['maximum'] = evaluations[-1]
        return result
            
    def htmlPerformanceTable(self,isSorted=True,ndigits=2):
        """
        Renders the performance table citerion x actions in html format.
        """
        minMaxEvaluations = self.computeMinMaxEvaluations()
        html = '<h1>Performance table</h1>'
        criteriaList = list(self.criteria)
        if isSorted:
            criteriaList.sort()
        actionsList = list(self.actions)
        if isSorted:
            actionsList.sort()
        html += '<table style="background-color:White;" border="1">'
        html += '<tr bgcolor="#9acd32"><th>criterion</th>'
        for x in actionsList:
            html += '<th bgcolor="#FFF79B">%s</th>' % (str(x))
        html += '</tr>'
        for g in criteriaList:
            html += '<tr><th bgcolor="#FFF79B">%s</th>' % (str(g))
            for x in actionsList:
                if self.evaluation[g][x] != Decimal("-999"):
                    if self.evaluation[g][x] == minMaxEvaluations[g]['minimum']:
                        formatString = '<td bgcolor="#ffddff"  align="right">%% .%df</td>' % ndigits
                        html += formatString % (self.evaluation[g][x])
                    elif self.evaluation[g][x] == minMaxEvaluations[g]['maximum']:
                        formatString = '<td bgcolor="#ddffdd" align="right">%% .%df</td>' % ndigits
                        html += formatString % (self.evaluation[g][x])
                    else:
                        formatString = '<td align="right">%% .%df</td>' % ndigits
                        html += formatString % (self.evaluation[g][x])
                        
                else:
                    html += '<td>&#32;</td>'
            html += '</tr>'
        html += '</table>'
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
            weightslist.append((criteria[g]['weight'],g))
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
        criteria = self.criteria
        evaluation = self.evaluation
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved performance Tableau: \n')
        fo.write('actions = {\n')
        for x in actions:
            fo.write('\'%s\': {\'name\': \'%s\'},\n' %(x,x))
        fo.write('}\n')
        fo.write('criteria = {\n') 
        for g in criteria:
            fo.write('\'' +str(g)+'\': {\n')
            if isDecimal:
                #fo.write('\'weight\':Decimal("'+str(criteria[g]['weight'])+'"),\'scale\': (Decimal("'+str(criteria[g]['scale'][0])+'"),Decimal("'+str(criteria[g]['scale'][1])+'")),\n')
                #fo.write('\'thresholds\' :' + str(criteria[g]['thresholds']) + '},\n')
                weightScaleString = '\'weight\':Decimal("%%.%df"),\'scale\': (Decimal("%%.%df"),Decimal("%%.%df")),\n' % (valueDigits,valueDigits,valueDigits)
                fo.write(weightScaleString % (criteria[g]['weight'],criteria[g]['scale'][0],criteria[g]['scale'][1]))
                try:
                    fo.write('\'thresholds\' : %s },\n' % ( str(criteria[g]['thresholds']) ) )
                except:
                    fo.write('},\n')
            else:
                fo.write('\'weight\':'+str(criteria[g]['weight'])+',\'scale\':'+str(criteria[g]['scale'])+',\n')
                try:
                    fo.write('\'thresholds\' :' + str(criteria[g]['thresholds']) + '},\n')
                except:
                    fo.write('},\n')
                
        fo.write('}\n')
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
                    pdir = -1
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

    def saveXMCDA2(self,fileName='temp',category='XMCDA 2.0 format',user='digraphs Module (RB)',version='saved from Python session',title='Performance Tableau in XMCDA-2.0 format.',variant='Rubis',valuationType='bipolar',servingD3=True,isStringIO=False,stringNA='NA',comment='produced by saveXMCDA2()',hasVeto=True):
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
                    pdir = -1
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

    def saveXMCDA2String(self,fileName='temp',category='XMCDA 2.0 format',user='digraphs Module (RB)',version='saved from Python session',title='Performance Tableau in XMCDA-2.0 format.',variant='Rubis',valuationType='bipolar',servingD3=True,comment='produced by stringIO()',stringNA='NA'):
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
                    pdir = -1
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
        evaluation scale. Therefore the performance tableai is normalized to 0.0-100.0 scales.
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

    
    def showStatistics(self):
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
        na = len(actions)
        print('*-------- Performance tableau summary statistics -------*')
        print('Instance name      :', self.name)
        print('#Actions           :', na)
        print('#Criteria          :', nc)
        print('*Statistics per Criterion*')
        averageSigma = Decimal('0.0')
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
                evaluationList.append(evaluation[g][x])
                averageEvaluation += evaluation[g][x]
                varianceEvaluation += evaluation[g][x]**Decimal('2')
                if evaluation[g][x] < minEvaluation:
                    minEvaluation = evaluation[g][x]
                if evaluation[g][x] > maxEvaluation:
                    maxEvaluation = evaluation[g][x]
            evaluationList.sort()
            #print evaluationList
            # !! index on evaluation List goes from 0 to na -1 !!
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
            try:
                if self.criteria[g]['preferenceDirection'] == 'max':
                    print('  criterion scale    : %.2f - %.2f' % (Min, Max))
                else:
                    print('  criterion scale    : %.2f - %.2f' % (-Max, Min))
            except:
                print('  criterion scale    : %.2f - %.2f' % (Min, Max))
            print('  mean evaluation    : %.2f' % (averageEvaluation))
            print('  standard deviation : %.2f' % (stdDevEvaluation))
            print('  maximal evaluation : %.2f' % (maxEvaluation))
            print('  quantile Q3 (x_75) : %.2f' % (quantileQ3))
            print('  median evaluation  : %.2f' % (quantileQ2))
            print('  quantile Q1 (x_25) : %.2f' % (quantileQ1))
            print('  minimal evaluation : %.2f' % (minEvaluation))
            averageAbsDiffEvaluation = Decimal('0.0')
            varianceDiffEvaluation = Decimal('0.0')
            nd = 0
            for x in actions:
                for y in actions:
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
            averageSigma += Decimal(str(stdDevDiffEvaluation))
        averageSigma /= Decimal(str(nc))
        ## print ':', self.weightPreorder
        ## print 'Average standard difference deviation : %.2f' % (averageSigma)


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
            normEvaluation[g] = {}
            glow = Decimal(str(criteria[g]['scale'][0]))
            ghigh = Decimal(str(criteria[g]['scale'][1]))
            gamp = ghigh - glow
            if Debug:
                print('-->> g, glow, ghigh, gamp', g, glow, ghigh, gamp)
            for x in actionKeys:
                evalx = abs(evaluation[g][x])
                if Debug:
                    print(evalx)
                ## normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                try:
                    if criteria[g]['preferenceDirection'] == 'min':
                        sign = Decimal('-1')
                    else:
                        sign = Decimal('1')
                    normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)*sign
                    ## else:
                    ##     normEvaluation[g][x] = -(lowValue + ((evalx-glow)/gamp)*(-amplitude))
                except:
                    self.criteria[g]['preferenceDirection'] = 'max'
                    normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                    
                if Debug:
                    print(criteria[g]['preferenceDirection'], evaluation[g][x], normEvaluation[g][x])
        return normEvaluation


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
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab == None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
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

class RandomPerformanceTableau(PerformanceTableau):
    """
    Specialization of the PerformanceTableau class for generating a temporary
    random performance tableau.

    Parameters:
        | actions := nbr of actions,
        | criteria := number criteria,
        | scale := [Min,Max],
        | thresholds := [q,p,v],
        | mode = [
             | ('uniform',None,None)
             | ('normal',mu,sigma)
             | ('triangular',mode,None)
             | ('beta',mode,(alpha,beta)],
        | weightDistribution := equivalent|random|fixed

    Code example::
        >>> from perfTabs import RandomCBPerformanceTableau
        >>> t = RandomCBPerformanceTableau(numberOfActions=3,numberOfCriteria=1)
        >>> t.actions
            {'a02': {'comment': 'RandomCBPerformanceTableau() generated.', 'type': 'advantageous', 'name': 'random advantageous decision action'},
            'a03': {'comment': 'RandomCBPerformanceTableau() generated.', 'type': 'advantageous', 'name': 'random advantageous decision action'},
            'a01': {'comment': 'RandomCBPerformanceTableau() generated.', 'type': 'neutral', 'name': 'random neutral decision action'}}
        >>> t.criteria
            {'g01': {'comment': 'Evaluation generator: triangular law with variable mode (m) and probability repartition (p = 0.5). Cheap actions: m = 30%; neutral actions: m = 50%; advantageous actions: m = 70%.',
            'performanceDifferences': [Decimal('21.84'), Decimal('25.49'), Decimal('47.33')],
            'scale': (0.0, 100.0),
            'minimalPerformanceDifference': Decimal('21.84'),
            'preferenceDirection': 'max',
            'weight': Decimal('1'),
            'randomMode': ['triangular', 50.0, 0.5],
                           'name': 'random cardinal benefit criterion',
                           'maximalPerformanceDifference': Decimal('47.33'),
                           'thresholds': {'ind': (Decimal('22.205'), Decimal('0.0')),
                                          'veto': (Decimal('45.146'), Decimal('0.0')),
                                          'pref': (Decimal('22.570'), Decimal('0.0'))},
            'scaleType': 'cardinal'}
            }

        >>> t.evaluation
            {'g01': {'a02': Decimal('94.22'),
                     'a03': Decimal('72.38'),
                     'a01': Decimal('46.89')
                    }
            }

    """
    def __init__(self,numberOfActions = None, numberOfCriteria = None, weightDistribution = None, weightScale=None, integerWeights=True, commonScale = [0.0,100.0], commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0)], commonMode = None, valueDigits = 2, Debug = False):
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
            sys.exit(1)
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

# -----------------
class RandomRankPerformanceTableau(PerformanceTableau):
    """
    Specialization of the PerformanceTableau class for generating a temporary
    random performance tableau.
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


class FullRandomPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of random performance tableaux
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

class RandomCoalitionsPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of performance tableaux with random coalitions of criteria

    Parameters:
        | numberOf Actions := 20 (default)
        | number of Criteria := 13 (default)
        | weightDistribution := 'equisignificant' (default with all weights = 1.0), 'random', 'equiobjectives', 'fixed' (default w_1 = numberOfCriteria-1, w_{i!=1} = 1
        | weightScale := [1,numerOfCriteria[ (random default), [w_1, w_{i!=1] (fixed)
        | interWeights := True (default) / False
        | commonScale := (0.0, 100.0) (default)
        | commonThresholds := [(1.0,0.0),(2.001,0.0),(8.001,0.0)] if OrdinalSacles, [(0.10001*span,0),(0.20001*span,0.0),(0.80001*span,0.0)] with span = commonScale[1] - commonScale[0].
        | commonMode := ['triangular',50.0,0.50] (default), ['uniform',None,None], ['beta', None,None] (three alpha, beta combinations (5.8661,2.62203) chosen by default for high('+'), medium ('~') and low ('-') evaluations.
        | valueDigits := 2 (default, for cardinal scales only)
        | Coalitions := True (default)/False, three coalitions if True
        | VariableGenerators := True (default) / False, variable high('+'), medium ('~') or low ('-') law generated evaluations.
        | OrdinalScales := True / False (default)
        | Debug := True / False (default)
        | RandomCoalitions = True / False (default) zero or more than three coalitions if Coalitions == False.
        | vetoProbability := x in ]0.0-1.0[ / None (default), probability that a cardinal criterion shows a veto preference discrimination threshold.
        | Electre3 := True (default) / False, no weakveto if True (obsolete)
        
    """

    def __init__(self,numberOfActions = None, numberOfCriteria = None, weightDistribution = None, weightScale=None, integerWeights = True, commonScale = None, commonThresholds = None, commonMode = None, valueDigits=2, Coalitions=True, VariableGenerators=True,OrdinalScales=False,Debug=False,RandomCoalitions=False,vetoProbability=None,Electre3=True):
        import sys,random,time,math
        self.name = 'randomCBperftab'
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
                criteria[g]['thresholds'][thitems[t]] = (Decimal(str(thresholds[t][0])),Decimal(str(thresholds[t][1])))
                
            criteria[g]['scale'] = commonScale
            if integerWeights:
                criteria[g]['weight'] = weightsList[gi]
            else:
                criteria[g]['weight'] = weightsList[gi] / sumWeights

        # allocate (criterion,action) to coalition supporting type
        if Coalitions:
            coalitionSupportingType = ['+','~','-']
            for x in actionsList:
                for c in criterionCoalitionsList:
                    if Debug:
                        print(criterionCoalitionsList,c)
                    self.actions[x][str(c[0])]=random.choice(coalitionSupportingType)
                    self.actions[x]['name'] = self.actions[x]['name'] + ' '+ str(c[0]) + str(self.actions[x][str(c[0])])                
                    
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

class RandomS3PerformanceTableau(RandomCoalitionsPerformanceTableau):
    """
    Obsolete dummy class for backports.
    """

class RandomCBPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of random
    Cost versus Benefit oriented performance tableaux.

    Parameters:
        | If numberOfActions == None, a uniform random number between 10 and 31 of cheap, neutral or advantageous actions (equal 1/3 probability each type) actions is instantiated
        | If numberOfCriteria == None, a uniform random number between 5 and 21 of cost or benefit criteria (1/3 respectively 2/3 probability) is instantiated
        | weightDistribution := {'equiobjectives'|'fixed'|'random'|'equisignificant' (default = 'equisignificant')}
        | default weightScale for 'random' weightDistribution is 1 - numberOfCriteria
        | commonScale parameter is obsolete. The scale of cost criteria is cardinal or ordinal (0-10) with proabailities 1/4 respectively 3/4, whereas the scale of benefit criteria is ordinal or cardinal with probabilities 2/3, respectively 1/3.
        | All cardinal criteria are evaluated with decimals between 0.0 and 100.0 wheras all ordinal criteria are evaluated with integers between 0 and 10.
        | commonThresholds is obsolete. Preference discrimination is specified as percentiles of concerned performance differences (see below).
        | CommonPercentiles = {'ind':5, 'pref':10, ['weakveto':90,] 'veto':95} are expressed in percents (reversed for vetoes) and only concern cardinal criteria.

    .. warning::

        Minimal number of decision actions required is 3 ! 

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
        self.computePerformanceDifferences(Debug=False)
        if Debug:
            print('commonPercentiles=', commonPercentiles)
        if commonPercentiles == None:
            quantile = {'ind':5, 'pref':10 , 'veto':95}
        else:
            quantile = commonPercentiles
        for c in criteriaList:
            if self.criteria[c]['scaleType'] == 'cardinal':
                self.criteria[c]['thresholds'] = {}
                vx = self.criteria[c]['performanceDifferences']
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

## class OldRandomCBPerformanceTableau(PerformanceTableau):
##     """
##     Full automatic generation of random
##     Cost versus Benefit oriented performance tableaux.

##     .. warning::

##         Minimal number of decision actions required is 3 ! 

##     """

##     def __init__(self,numberOfActions = None, \
##                  numberOfCriteria = None, \
##                  weightDistribution = None, weightScale=None,\
##                  integerWeights = True,
##                  commonScale = None, commonThresholds = None,\
##                  commonPercentiles= None,\
##                  commonMode = None,\
##                  valueDigits=2, Debug=False,Comments=False):
##         """
##         Constructor for RadomCBPerformanceTableau instances.
##         Parametrs description:
##         weightDistribution = {'fixed'|'random'|'equisignificant' (default = 1)}
##         weightScale default is 1 - numberOfCriteria
##         commonScale parameter is obsolete.
##         All cardinal criteria are evaluated between 0.0 and 100.0
##         and all ordinal criteria are integer evaluated between 0 and 10.
##         commonThresholds is obsolete.
##         CommonPercentiles = {'ind':5, 'pref':10, ['weakveto':90,] 'veto':95}
##         are expressed in percents (reversed for vetoes) and only
##         concern cardinal criteria.
        
##         """

##         import sys,random,time,math,copy
        
##         self.name = 'randomCBperftab'
##         # randomizer init
##         t = time.time()
##         random.seed(t)
##         # generate random actions
##         if numberOfActions == None:
##             numberOfActions = random.randint(10,31)
##         actionsIndex = range(numberOfActions+1)
##         actionsIndex.remove(0)
##         actionsList = []
##         for a in actionsIndex:
##             if a < 10:
##                 actionName = 'a0'+str(a)
##             else:
##                 actionName = 'a'+str(a)
##             actionsList.append(actionName)
##         actions = {}
##         actionsTypesList = ['cheap','neutral','advantageous']
##         for x in actionsList:
##             actions[x] = {}
##             actions[x]['type'] = random.choice(actionsTypesList)
##             actions[x]['name'] = 'random %s decision action' % (actions[x]['type'])
##             actions[x]['comment'] = 'RandomCBPerformanceTableau() generated.'
##         self.actions = actions

##         # generate random criterialist
##         if numberOfCriteria == None:
##             numberOfCriteria = random.randint(5,21)
##         criteriaList = []
##         criteriaIndex = range(numberOfCriteria+1)
##         criteriaIndex.remove(0)
##         for g in criteriaIndex:
##             if g < 10:
##                 criterionName = 'g0'+str(g)
##             else:
##                 criterionName = 'g'+str(g)
##             criteriaList.append(criterionName)
##         if Debug:
##             print criteriaList
            
##         # generate random weights
##         if weightDistribution == None:
##             weightDistribution = 'fixed'
##             weightScale = (1,1)
##             weightMode=[weightDistribution,weightScale]
##             ## majorityWeight = numberOfCriteria + 1
##             ## #weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('fixed',[1,majorityWeight],4)]
##             ## weightModesList = [('fixed',[1,1],1),('random',[1,3],2), ('random',[1,numberOfCriteria],3),('balanced',[1,1],4)]
##             ## weightMode = random.choice(weightModesList)
##             ## weightDistribution = weightMode[0]
##             ## weightScale =  weightMode[1]
##         else:
##             if weightScale == None:
##                 weightScale = (1,numberOfCriteria)
##             weightMode=[weightDistribution,weightScale]
            
##         if weightDistribution == 'random':
##             weightsList = []
##             sumWeights = Decimal('0.0')
##             i = 0
##             for g in criteriaList:
##                 weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
##                 sumWeights += weightsList[i]
##                 i += 1
##             weightsList.reverse()
##         elif weightDistribution == 'fixed':
##             weightsList = []
##             sumWeights = Decimal('0.0')
##             for g in criteriaList:
##                 if g == 'g1':
##                     weightsList.append(Decimal(str(weightScale[1])))
##                     sumWeights += weightScale[1]
##                 else:
##                     weightsList.append(Decimal(str(weightScale[0])))
##                     sumWeights += weightScale[0]
##             weightsList.reverse()
##         elif weightDistribution == 'equisignificant':
##             weightScale = (1,1)
##             weightMode=[weightDistribution,weightScale]
##             weightsList = []
##             sumWeights = Decimal('0.0')
##             for g in criteriaList:
##                 if g == 'g1':
##                     weightsList.append(Decimal(str(weightScale[1])))
##                     sumWeights += weightScale[1]
##                 else:
##                     weightsList.append(Decimal(str(weightScale[0])))
##                     sumWeights += weightScale[0]
##             weightsList.reverse()
##         else:
##             print '!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution)
##         if Debug:
##             print weightsList, sumWeights

##         # generate criteria dictionary
##         ## if commonScale == None:
##         ##     commonScale = (0.0,100.0)
##         criterionTypesList = ['max','max','min']
##         minScaleTypesList = ['cardinal','cardinal','cardinal','ordinal']
##         maxScaleTypesList = ['ordinal','ordinal','cardinal']
##         criteria = {}
##         i = 0
##         for g in criteriaList:
##             #criterionScale = commonScale
##             criteria[g] = {}
##             criterionType = random.choice(criterionTypesList)
##             criteria[g]['preferenceDirection'] = criterionType
##             if criterionType == 'min':
##                 scaleType = random.choice(minScaleTypesList)
##             else:
##                 scaleType = random.choice(maxScaleTypesList)
##             criteria[g]['scaleType'] = scaleType
##             if criterionType == 'min':
##                 if scaleType == 'ordinal':
##                     criteria[g]['name'] = 'random ordinal cost criterion'
##                 else:
##                     criteria[g]['name'] = 'random cardinal cost criterion'
##             else:
##                 if scaleType == 'ordinal':
##                     criteria[g]['name'] = 'random ordinal benefit criterion'
##                 else:
##                     criteria[g]['name'] = 'random cardinal benefit criterion'
##             ## t = time.time()
##             ## random.seed(t)
##             if Debug:
##                 print "g, criteria[g]['scaleType'], criteria[g]['scale']", g, criteria[g]['scaleType'],

##             # commonScale parameter is obsolete
##             commonScale = None
##             if criteria[g]['scaleType'] == 'cardinal':
##                 #if commonScale == None:
##                 criterionScale = (0.0, 100.0)
##                 ## criteria[g]['scale'] = criterionScale      
##             elif criteria[g]['scaleType'] == 'ordinal':
##                 ## if Debug:
##                 ##     print commonScale
##                 ## if commonScale == None:
##                 ##     criterionScale = (0, 10)
##                 ## else:
##                 criterionScale = (0, 10)
##             else:
##                 criterionScale = (0.0, 100.0)
##             criteria[g]['scale'] = criterionScale
##             if Debug:
##                 print criteria[g]['scale']
                
##             ## if Debug:
##             ##     print 'criterionScale = ', criterionScale
##             if integerWeights:
##                 criteria[g]['weight'] = weightsList[i]
##             else:
##                 criteria[g]['weight'] = weightsList[i] / sumWeights
##             i += 1

##             if Debug:
##                 print criteria[g]

##         # generate random evaluations
##         ## x30=criterionScale[1]*0.3
##         ## x50=criterionScale[1]*0.5
##         ## x70=criterionScale[1]*0.7
##         ## if Debug:
##         ##     print 'g, x30,x50,x70', g, x30,x50,x70
##         ## randomLawsList = [['uniform',criterionScale[0],criterionScale[1]],
##         ##                   ('triangular',x30,0.33),('triangular',x30,0.50),('triangular',x30,0.75),
##         ##                   ('triangular',x50,0.33),('triangular',x50,0.50),('triangular',x50,0.75),
##         ##                   ('triangular',x70,0.33),('triangular',x70,0.50),('triangular',x70,0.75),
##         ##                   ('normal',x30,20.0),('normal',x30,25.0),('normal',x30,30.0),
##         ##                   ('normal',x50,20.0),('normal',x50,25.0),('normal',x50,30.0),
##         ##                   ('normal',x70,20.0),('normal',x70,25.0),('normal',x70,30.0)]
        
##         evaluation = {}
##         for g in criteriaList:
##             criterionScale = criteria[g]['scale']
##             amplitude = criterionScale[1] - criterionScale[0]
##             x30=criterionScale[0] + amplitude*0.3
##             x50=criterionScale[0] + amplitude*0.5
##             x70=criterionScale[0] + amplitude*0.7
##             if Debug:
##                 print 'g, criterionx30,x50,x70', g, criteria[g], x30,x50,x70
##             evaluation[g] = {}
##             if commonMode == None:
##                 #randomMode = random.choice(randomLawsList)
##                 randomMode = ['triangular',x50,0.50]               
##             elif commonMode[0] == None:
##                 #randomMode = random.choice(randomLawsList)
##                 randomMode = ['triangular',x50,0.50]               
##             else:
##                 randomMode = commonMode
##             if randomMode[0] == 'uniform':
##                 randomMode[1] = criterionScale[0]
##                 randomMode[2] = criterionScale[1]
##             criteria[g]['randomMode'] = randomMode
##             if randomMode[0] == 'triangular':
##                 commentString = 'triangular law with variable mode (m) and probability repartition (p = 0.5). Cheap actions: m = 30%; neutral actions: m = 50%; advantageous actions: m = 70%.'
##             elif randomMode[0] == 'normal':
##                 commentString = 'truncated normal law with variable mean (mu) and standard deviation (stdev = 20%). Cheap actions: mu = 30%; neutral actions: mu = 50%; advantageous actions: mu = 70%.'
##             elif randomMode[0] == 'beta':
##                 commentString = 'beta law with variable mode xm and standard deviation (stdev = 15%). Cheap actions: xm = 30%; neutral actions: xm = 50%; advantageous actions: xm = 70%.'

##             ## else:
##             ##     if randomMode[1] != None and randomMode[2] != None:
##             ##         commentString = randomMode[0]+', %.2f, %.2f' % (float(randomMode[1]),float(randomMode[2]))
##             ##     elif randomMode[1] != None and randomMode[2] == None:
##             ##         commentString = randomMode[0]+', %.2f, default' % (float(randomMode[1]))
##             ##     elif randomMode[1] == None and randomMode[2] != None:
##             ##         commentString = randomMode[0]+', default, %.2f' % (float(randomMode[2]))
##             ##     else:
##             ##         commentString = randomMode[0]+', default, default'
                    
##             if Debug:
##                 print 'commonMode = ', commonMode
##                 print 'randomMode = ', randomMode
                   
##             criteria[g]['comment'] = 'Evaluation generator: ' + commentString
##             digits = valueDigits
##             if str(randomMode[0]) == 'uniform':          
##                 evaluation[g] = {}
##                 for a in actionsList:
##                     randeval = random.uniform(criterionScale[0],criterionScale[1])
##                     if criteria[g]['preferenceDirection'] == 'max':
##                         evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     else:
##                         evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##             elif str(randomMode[0]) == 'triangular':
##                 for a in actionsList:
##                     m = criterionScale[0]
##                     M = criterionScale[1]
##                     #r  = randomMode[2]
##                     #xm = randomMode[1]
##                     if actions[a]['type'] == 'advantageous':
##                         xm = x70
##                         r = 0.50
##                     elif actions[a]['type'] == 'cheap':
##                         xm = x30
##                         r = 0.50
##                     else:
##                         xm = x50
##                         r = 0.50
                        
##                     deltaMinus = 1.0 - (criterionScale[0]/xm)
##                     deltaPlus  = (criterionScale[1]/xm) - 1.0

##                     u = random.random()
##                     #print 'm,xm,M,r,u', m,xm,M,r,u 
##                     if u < r:
##                         #randeval = m + (math.sqrt(r*u*(m-xm)**2))/r
##                         randeval = m + math.sqrt(u/r)*(xm-m)
##                     else:
##                         #randeval = (M*r - M + math.sqrt((-1+r)*(-1+u)*(M-xm)**2))/(-1+r)
##                         randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
                    
##                     if criteria[g]['preferenceDirection'] == 'max':
##                         evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     else:
##                         evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##                     #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]
                        
##             elif str(randomMode[0]) == 'normal':
##                 #mu = randomMode[1]
##                 #sigma = randomMode[2]
##                 for a in actionsList:
##                     ## amplitude = criterionScale[1]-criterionScale[0]
##                     ## x70 = criterionScale[0] + 0.7 * amplitude
##                     ## x50 = criterionScale[0] + 0.5 * amplitude
##                     ## x30 = criterionScale[0] + 0.3 * amplitude
                    
##                     if actions[a]['type'] == 'advantageous':
##                         mu = x70
##                         sigma = 0.20 * amplitude
##                     elif actions[a]['type'] == 'cheap':
##                         mu = x30
##                         sigma = 0.20 * amplitude
##                     else:
##                         mu = x50
##                         sigma = 0.25 * amplitude
##                     notfound = True 
##                     while notfound:
##                         randeval = random.normalvariate(mu,sigma)
##                         ## if Debug:
##                         ##     print 'g,commonScale,randeval', g,commonScale,randeval
##                         if randeval >= criterionScale[0] and  randeval <= criterionScale[1]:
##                             notfound = False
##                     if criteria[g]['preferenceDirection'] == 'max':
##                         evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     else:
##                         evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##             elif str(randomMode[0]) == 'beta':
##                 m = criterionScale[0]
##                 M = criterionScale[1]
##                 ## if commonMode[1] == None:
##                 ##     xm = 0.5
##                 ## else:
##                 ##     xm = commonMode[1]
                
##                 ## if commonMode[2] == None:
##                 ##     if xm > 0.5:
##                 ##         beta = 2.0
##                 ##         alpha = 1.0/(1.0 - xm)
##                 ##     else:
##                 ##         alpha = 2.0
##                 ##         beta = 1.0/xm
##                 ## else:
##                 ##     alpha = commonMode[2][0]
##                 ##     beta = commonMode[2][1]
##                 ## if Debug:
##                 ##     print 'alpha,beta', alpha,beta
##                 for a in actionsList:
##                     if actions[a]['type'] == 'advantageous':
##                         # xm = 0.7 sdtdev = 0.15
##                         alpha = 5.8661
##                         beta = 2.62203
##                     elif actions[a]['type'] == 'cheap':
##                         # xm = 0.3, stdev = 0.15
##                         alpha = 2.62203
##                         beta = 5.8661
##                     else:
##                         # xm = 0.5, stdev = 0.15
##                         alpha = 5.05556
##                         beta = 5.05556
                    
##                     u = random.betavariate(alpha,beta)
##                     randeval = (u * (M-m)) + m
##                     if criteria[g]['preferenceDirection'] == 'max':
##                         evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     else:
##                         evaluation[g][a] = Decimal(str(-round(randeval,digits)))
##                     ## if Debug:
##                     ##     print 'alpha,beta,u,m,M,randeval',alpha,beta,u,m,M,randeval
                        

 
##         if Debug:
##             print evaluation

##         ## # restrict ordinal criteria to integer (0 - 10) scale
##         ## for g in criteriaList:
##         ##     if criteria[g]['scaleType'] == 'ordinal':
##         ##         for a in actionsList:
##         ##             ## if Debug:
##         ##             ##     print 'commonThresholds = ', commonThresholds
##         ##             ##     print '-- >>', evaluation[g][a],
##         ##             if commonThresholds == None:
##         ##                 ## evaluation[g][a] = Decimal(str(round(evaluation[g][a]/Decimal("10.0"),0)))
##         ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
##         ##             else:
##         ##                 evaluation[g][a] = Decimal(str(round(evaluation[g][a],-1)))
##         ##             ## if Debug:
##         ##             ##     print evaluation[g][a]
##         # restrict ordinal criteria to integer values
##         for g in criteriaList:
##             if criteria[g]['scaleType'] == 'ordinal':
##                 for a in actionsList:
##                     if Debug:
##                         print '-- >>', evaluation[g][a],
##                     evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
##                     if Debug:
##                         print evaluation[g][a]
            
        
##             # generate discrimination thresholds
##         self.criteriaWeightMode = weightMode
##         self.criteria = copy.deepcopy(criteria)
##         self.evaluation = copy.deepcopy(evaluation)
##         self.weightPreorder = self.computeWeightPreorder()
##         self.computePerformanceDifferences(Debug=False)
##         if Debug:
##             print 'commonPercentiles=', commonPercentiles
##         if commonPercentiles == None:
##             quantile = {'ind':5, 'pref':10 , 'veto':95}
##         else:
##             quantile = commonPercentiles
##         for c in criteriaList:
##             if self.criteria[c]['scaleType'] == 'cardinal':
##                 self.criteria[c]['thresholds'] = {}
##                 vx = self.criteria[c]['performanceDifferences']
##                 nv = len(vx)
##                 if Debug:
##                     print '=====>',c
##                     print vx
##                     print nv
##                 threshold = {}
##                 for x in quantile:
##                     if Debug:
##                         print '-->', x, quantile[x],

##                     if quantile[x] == -1:
##                         pass
##                     else:
##                         if quantile[x] == 0:
##                             threshold[x] = vx[0]
##                         elif quantile[x] == 100:
##                             threshold[x] = vx[nv-1]
##                         else:
##                             kq = int(math.floor(float(quantile[x]*(nv-1))/100.0))
##                             r = ((nv-1)*quantile[x])% 100
##                             if Debug:
##                                 print kq,r,

##                             ## if kq == nv-1:
##                             ##     kqplus = nv-1
##                             ## else:
##                             ##     kq_1 = kq - 1
##                             threshold[x] = vx[kq] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq+1]-vx[kq])
##                             if Debug:
##                                 print threshold[x]



##                 for x in threshold:
##                     self.criteria[c]['thresholds'][x] = (threshold[x],Decimal('0.0'))

##             if Comments:
##                 print 'criteria',c,' default thresholds:'
##                 print self.criteria[c]['thresholds']

                
#############################33
# XML encoded stored PerformanceTableau Class instances
class XMLPerformanceTableau(PerformanceTableau):
    """
    Specialization of the general PerformanceTableau class for reading
    stored XML formatted instances.
    """

    def __init__(self,fileName='testperftabXML'):
        from xml.sax import make_parser
        xmlPerformanceTableau = _XMLPerformanceTableauHandler()
        saxParser = make_parser()
        saxParser.setContentHandler(xmlPerformanceTableau)
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        saxParser.parse(fo)
        self.name = xmlPerformanceTableau.name
        self.category = xmlPerformanceTableau.category
        self.subcategory = xmlPerformanceTableau.subcategory  
        self.actions = xmlPerformanceTableau.actions
        self.criteria = xmlPerformanceTableau.criteria
        self.evaluation = xmlPerformanceTableau.evaluation
        self.weightPreorder = self.computeWeightPreorder()

class XMLRubisPerformanceTableau(PerformanceTableau):
    """
    Specialization of the general PerformanceTableau class for reading
    stored XML formatted instances. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param: fileName (without the extension .xml). 
    """
    
    def __init__(self,fileName='rubisPerformanceTableau'):
        from xml.etree import ElementTree
        try:
            fileNameExt = fileName + '.xml'
            fo = open(fileNameExt,mode='r')
        except:
            try:
                fileNameExt = fileName + '.xmcda'
                fo = open(fileNameExt,mode='r')
            except:
                fileNameExt = fileName + '.xmcda2'
                fo = open(fileNameExt,mode='r')
        rubisPerformanceTableau = ElementTree.parse(fo).getroot()
        self.comment = rubisPerformanceTableau.find('comment').text
        self.category = rubisPerformanceTableau.attrib['category']
        self.subcategory = rubisPerformanceTableau.attrib['subcategory']
        self.name = rubisPerformanceTableau.find('header').find('name').text
        self.author = rubisPerformanceTableau.find('header').find('author').text
        self.reference = rubisPerformanceTableau.find('header').find('reference').text
        actions = {}
        ## actions['comment'] = rubisPerformanceTableau.find('actions').find('comment').text
        for x in rubisPerformanceTableau.find('actions').findall('action'):
            actions[x.attrib['id']] = {}
            actions[x.attrib['id']]['name'] = x.find('name').text
            actions[x.attrib['id']]['comment'] = x.find('comment').text
        self.actions = actions
        criteria = {}
        ##criteria['comment'] = rubisPerformanceTableau.find('criteria').find('comment').text
        for g in rubisPerformanceTableau.find('criteria').findall('criterion'):
            criteria[g.attrib['id']] = {}
            criteria[g.attrib['id']]['name'] = g.find('name').text
            criteria[g.attrib['id']]['comment'] = g.find('comment').text
            criteria[g.attrib['id']]['scale'] = {}
            Min = Decimal(g.find('scale').find('min').text)
            Max = Decimal(g.find('scale').find('max').text)
            ##criteria[g.attrib['id']]['scale'] = str((Min,Max))
            criteria[g.attrib['id']]['scale'] = (Min,Max)
            criteria[g.attrib['id']]['thresholds'] = {}
            try:
                th = self.stripsplit(g.find('thresholds').find('indifference').text)
                criteria[g.attrib['id']]['thresholds']['ind'] = (Decimal(str(th[0])),Decimal(str(th[1])))
            except:
                pass
            try:
                th = self.stripsplit(g.find('thresholds').find('weakPreference').text)
                criteria[g.attrib['id']]['thresholds']['weakPreference'] = (Decimal(str(th[0])),Decimal(str(th[1])))
            except:
                pass
            try:
                th = self.stripsplit(g.find('thresholds').find('preference').text)
                criteria[g.attrib['id']]['thresholds']['pref'] = (Decimal(str(th[0])),Decimal(str(th[1])))
            except:
                pass
            try:
                th = self.stripsplit(g.find('thresholds').find('weakVeto').text)
                criteria[g.attrib['id']]['thresholds']['weakVeto'] = (Decimal(str(th[0])),Decimal(str(th[1])))
            except:
                pass
            try:
                th = self.stripsplit(g.find('thresholds').find('veto').text)
                criteria[g.attrib['id']]['thresholds']['veto'] = (Decimal(str(th[0])),Decimal(str(th[1])))
            except:
                pass
                ## criteria[g.attrib['id']]['thresholds']['veto'] = (Max + 1.0,0.0)
            criteria[g.attrib['id']]['weight'] = Decimal(g.find('weight').text)     
        self.criteria = criteria
        evaluation = {}
        ##evaluation['comment'] = rubisPerformanceTableau.find('evaluations').find('comment').text
        for v in rubisPerformanceTableau.find('evaluations').findall('evaluation'):
            g = v.find('criterionID').text
            evaluation[g] = {}
            for x in v.findall('performance'):
                evaluation[g][x.find('actionID').text]=Decimal(x.find('value').text)   
        self.evaluation = evaluation

##         self.actions = xmlPerformanceTableau.actions
##         self.criteria = xmlPerformanceTableau.criteria
##         self.evaluation = xmlPerformanceTableau.evaluation
        self.weightPreorder = self.computeWeightPreorder()

    def stripsplit(self,th):
        """ extract thresholds new Python 3 compatible version """
        import string
        ## th = string.split(string.lstrip(string.rstrip(th,')'),'('),',')
        th = th.rstrip(')')
        th = th.lstrip('(')
        th = th.split(',')
        res = (th[0].strip(),th[1].strip())
        return res      

class OldXMCDAPerformanceTableau(PerformanceTableau):
    """
    Specialization of the general PerformanceTableau class for reading
    stored XMCDA formatted instances. Using the inbuilt module
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
                print("Error: file %s{.xmcda|.xml} not found !" % (fileName))
        
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
                    value = float(elem.find('value').find('real').text)
                except:
                    value = int(elem.find('value').find('integer').text)                        
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
                Min = float(g.find('criterionFunction').find('scale').find('quantitative').find('min').find('real').text)
                Max = float(g.find('criterionFunction').find('scale').find('quantitative').find('max').find('real').text)
                ##criteria[g.attrib['id']]['scale'] = str((Min,Max))
                criteria[g.attrib['id']]['scale'] = (Min,Max)
                try:
                    criteria[g.attrib['id']]['weight'] = float(g.find('significance').find('real').text)
                except:
                    criteria[g.attrib['id']]['weight'] = int(g.find('significance').find('integer').text)
                try:
                    criteria[g.attrib['id']]['preferenceDirection'] = g.find('criterionFunction').find('scale').find('quantitative').find('preferenceDirection').text
                    if criteria[g.attrib['id']]['preferenceDirection'] == 'min':
                        pdir = -1
                    else:
                        pdir = 1
                except:
                    pdir = 1

                criteria[g.attrib['id']]['thresholds'] = {}
                for th in g.find('criterionFunction').find('thresholds').findall('threshold'):
                    try:
                        try:
                            intercept = float(th.find('function').find('linear').find('intercept').find('real').text)
                        except:
                            intercept = int(th.find('function').find('linear').find('intercept').find('integer').text)
                        slope = float(th.find('function').find('linear').find('slope').find('real').text)
                    except:
                        try:
                            intercept = float(th.find('function').find('constant').find('real').text)
                        except:
                            intercept = float(th.find('function').find('constant').find('integer').text)
                        slope = 0.0
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
                    pdir = -1
                else:
                    pdir = 1
            except:
                pdir = 1
            evaluation[g] = {}
            for x in v.findall('evaluation'):
                try:
                    value = x.find('value').find('integer').text
                    evaluation[g][x.find('alternativeID').text]=int(value) * pdir
                except:
                    value = x.find('value').find('real').text
                    evaluation[g][x.find('alternativeID').text]=float(value) * pdir
        self.evaluation = evaluation
        # compute weigth preoder
        self.weightPreorder = self.computeWeightPreorder()

class XMCDAPerformanceTableau(PerformanceTableau):
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

	fileName (without the extension .xml or .xmcda)
        HasSeparatedWeights - XMCDA 2.0.0 encoding (default = False)
        HasSeparatedThresholds - XMCDA 2.0.0 encoding (default = False)
        stringInput (default = None)
           
    """

    def __init__(self,fileName='temp',HasSeparatedWeights=False,HasSeparatedThresholds=False,stringInput=None):
        
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
        actions = {}
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
        criteria = {}
        # get criteria' description
        if XMCDA.find('criteria').find('description') != None:
            description = {}
            for elem in [x for x in XMCDA.find('criteria').find('description').getchildren()]:
                description[elem.tag] = elem.text
            self.criteriaDescription = description
        ## get criteria
        for g in XMCDA.find('criteria').findall('criterion'):
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
                    pdir = Decimal('-1')
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


#----------test Digraph class ----------------
if __name__ == "__main__":
    
    from digraphs import *
    from outrankingDigraphs import *
    import sortingDigraphs
    import linearOrders
    
    print('*-------- Testing classes and methods -------')

    ## t = FullRandomPerformanceTableau(commonScale=(0.0,100.0),numberOfCriteria=10,numberOfActions=10,commonMode=('triangular',30.0,0.7))
    ## t.showStatistics()
    ## print t.computeNormalizedDiffEvaluations(lowValue=0.0,highValue=100.0,withOutput=True,Debug=False)
    t = RandomCBPerformanceTableau(numberOfCriteria=1,numberOfActions=7,weightDistribution='equiobjectives')
    #t = RandomCoalitionsPerformanceTableau(numberOfActions=8,numberOfCriteria=1,Coalitions=True,RandomCoalitions=False)
    #t = PerformanceTableau('test')
    t.saveXMCDA2('test',servingD3=False)
    ## t.showAll()
    ## t.showCriteria()
    
    #t.showStatistics()
    ## t.showPerformanceTableau()

    ## html = t.showAllQuantiles()
    ## print t.computeQuantiles(Debug=False)
    t.showQuantileSort()
    ## g = BipolarOutrankingDigraph(t)
    ## s = sortingDigraphs.SortingDigraph(g)
    ## s.showSorting()
    ## g.computeRankingByChoosing(CoDual=False)
    ## g.showRankingByChoosing()
    ## bestChoice = g.rankingByChoosing[0][0][1]
    ## worstChoice= g.rankingByChoosing[0][1][1]
    ## g.exportGraphViz(bestChoice=bestChoice, worstChoice=worstChoice)
    ## rankingRelation = g.computeRankingByChoosingRelation()
    ## quantileSortRelation = g.computeQuantileSortRelation()
    ## g.recodeValuation(-1,1)
    ## print g.computeOrdinalCorrelation(rankingRelation)
    ## print g.computeOrdinalCorrelation(quantileSortRelation)
    ## #k = linearOrders.KemenyOrder(g)
    ## #print k.computeOrder()
    ## g.showPerformanceTableau()
    ## g.csvAllQuantiles()
    ## ## for x in t.actions:
    ## ##     t.computeActionQuantile(x,Debug=True)
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. August 2011                    *')
    print('* $Revision: 1.37 $                *')                   
    print('*************************************')

#############################
# Log record for changes:
# $Log: perfTabs.py,v $
# Revision 1.37  2012/12/24 15:18:21  bisi
# compatibility patch for old (-2008) python performance tableaux
#
# Revision 1.36  2012/07/19 12:38:55  bisi
# minor
#
# Revision 1.35  2012/07/17 06:14:47  bisi
# sync
#
# Revision 1.34  2012/06/19 14:13:13  bisi
# added quantile preording result
#
# Revision 1.25  2012/05/22 05:49:11  bisi
# activated new version of RandomCBPerformanceTableau class
# renamed RandomS3PerformanceTableau into RandomCoalitionsPerformanceTableau
#
# Revision 1.24  2012/05/22 04:34:49  bisi
# added equiobjectives weights generator to RandomCBPerformanceTableau()
#
# Revision 1.22  2012/05/09 10:51:43  bisi
# GPL version 3 licensing installed
#
# Revision 1.21  2012/04/26 10:50:41  bisi
# Added pairwise cluster comparison computation on Digraph class
#
# Revision 1.19  2012/01/10 19:25:16  bisi
# Added Spinx autodoc generation
#
# Revision 1.17  2011/12/26 14:50:00  bisi
# added html and csv save for allQuantiles matrix
#
# Revision 1.16  2011/12/26 08:39:15  bisi
# added median quantiles
#
# Revision 1.8  2011/08/22 18:34:55  bisi
# completed summary statistics
#
# Revision 1.7  2011/08/22 07:51:26  bisi
# refining showStatistics() method
#
# Revision 1.4  2011/08/19 13:19:14  bisi
# refactoring proportional threshold computation
#
# Revision 1.2  2011/08/07 18:06:16  bisi
# refactoring perfTabs.py module
#
# Revision 1.1  2011/08/07 13:55:08  bisi
# initial separation of digraphs and perfTabs modules
#############################