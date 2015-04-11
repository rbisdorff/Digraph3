#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python implementation of digraphs
# submodule randomPerfTabs.py  for generating random performance tableaux  
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

__version__ = "$Revision: 1.01 $"
# $Source: /home/cvsroot/Digraph/randomPerfTabs.py,v $

from perfTabs import *

from decimal import Decimal

#########################################
# generators for random PerformanceTableaux

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
        import sys,random,time,math,copy
        self.name = 'randomperftab'
        
        # generate actions
        if numberOfActions == None:
            numberOfActions = 13
        actions = dict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % nd) % (i+1)
            actions[actionKey] = {'shortName':actionKey,
                                'name': 'random decision action',
                                'comment': 'RandomPerformanceTableau() generated.' }
        self.actions = copy.copy(actions)
        actionsList = [x for x in self.actions]
        actionsList.sorted()
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
        | weightDistribution := 'equisignificant' (default with all weights = 1.0), 'random', 'fixed' (default w_1 = numberOfCriteria-1, w_{i!=1} = 1
        | weightScale := [1,numerOfCriteria] (random default), [w_1, w_{i!=1] (fixed)
        | integerWeights := True (default) / False
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
        * fileName is given without the extension ``.xml`` or ``.xmcda``,
        * HasSeparatedWeights in XMCDA 2.0.0 encoding (default = False),
        * HasSeparatedThresholds in XMCDA 2.0.0 encoding (default = False),
        * stringInput: instantiates from an XMCDA 2.0 encoded string argument.
           
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
    from weakOrders import *
    
    print('*-------- Testing classes and methods -------')

##    t = FullRandomPerformanceTableau(commonScale=(0.0,100.0),numberOfCriteria=10,numberOfActions=10,commonMode=('triangular',30.0,0.7))
    ## t.showStatistics()
    t = RandomCBPerformanceTableau(numberOfCriteria=13,
                                   numberOfActions=20,
                                   weightDistribution='equiobjectives',
                                   integerWeights=True,
                                   Debug=False)
##    t = RandomCoalitionsPerformanceTableau(numberOfActions=20,
##                                           numberOfCriteria=13,
##                                           Coalitions=False,
##                                           RandomCoalitions=True,
##                                           weightDistribution="equicoalitions",
##                                           Debug=True)
##    t.showAll()
##    t.saveXMCDA2('test')
##    t = XMCDA2PerformanceTableau('spiegel2004')
##    t = XMCDA2PerformanceTableau('uniSorting')
    from weakOrders import *
    qsrbc = QuantilesRankingDigraph(t,LowerClosed=True,Threading=False)
    qsrbc.showSorting()
    actionsList = qsrbc.computeQsRbcRanking()
    
##    #t.saveCSV('testCSV',Sorted=False,actionsList=actionsList,Debug=True)
##    print(t.htmlPerformanceHeatmap(actionsList=actionsList,Debug=True))
##    t.showHTMLPerformanceHeatmap(actionsList=actionsList,colorLevels=7,Ranked=True)
    t.showHTMLPerformanceHeatmap(colorLevels=5,Correlations=True,Threading=False)
    t.showPerformanceTableau()
    t.showHTMLPerformanceTableau(Transposed=True)
##    t.showHTMLPerformanceHeatmap(colorLevels=7,Threading=False)
##    t.showHTMLPerformanceHeatmap()
##    pt1 = PartialPerformanceTableau(t)
##    pt1.showAll()
##    pt2 = PartialPerformanceTableau(t,actionsSubset=['a01','a02'],criteriaSubset=['g01','g03'])
##    pt2.showAll()
    
##    ## t = PerformanceTableau('test')
##    t.saveXMCDA2('test',servingD3=False)
##    t.showCriteria(IntegerWeights=True)
##    print(t.computeQuantiles(Debug=False))
##    t.showQuantileSort()
##    g = BipolarOutrankingDigraph(t)
##    s = sortingDigraphs.SortingDigraph(g)
##    s.showSorting()
##    g.computeRankingByChoosing(CoDual=False)
##    g.showRankingByChoosing()
##    prg = PrincipalInOutDegreesOrdering(g,imageType="pdf")
##    prg.showWeakOrder()
##    print(g.computeOrdinalCorrelation(prg))
     
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
