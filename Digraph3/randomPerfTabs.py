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
        * numberOfActions := nbr of decision actions.
        * numberOfCriteria := number performance criteria.
        * weightDistribution := 'random' (default) | 'fixed' | 'equisignificant'.
             | If 'random', weights are uniformly selected randomly
             | form the given weight scale;
             | If 'fixed', the weightScale must provided a corresponding weights
             | distribution;
             | If 'equisignificant', all criterion weights are put to unity.
        * weightScale := [Min,Max] (default =[1,numberOfCriteria].
        * IntegerWeights := True (default) | False (normalized to proportions of 1.0).
        * commonScale := [Min;Max]; common performance measuring scales (default = [0;100])
        * commonThresholds := [q,p,v]; common indifference(q), preference (p)
          and considerable performance difference discrimination thresholds.
        * commonMode := common random distribution of random performance measuremenats:
             | ('uniform',Min,Max), uniformly distributed between min and max values. 
             | ('normal',mu,sigma), truncated Gaussion distribution. 
             | ('triangular',mode,repartition), generalized triangular distribution 
             | ('beta',alpha,beta).
        * valueDigits := <integer>, precision of performance measurements
          (2 decimal digits by default).
        
    Code example::
        >>> from randomPerfTabs import RandomPerformanceTableau
        >>> t = RandomPerformanceTableau(numberOfActions=3,numberOfCriteria=1)
        >>> t.actions
            {'a1': {'comment': 'RandomPerformanceTableau() generated.', 'name': 'random decision action'},
             'a2': {'comment': 'RandomPerformanceTableau() generated.', 'name': 'random decision action'},
             'a3': {'comment': 'RandomPerformanceTableau() generated.', 'name': 'random decision action'}}
        >>> t.criteria
            {'g1': {'thresholds': {'ind' : (Decimal('10.0'), Decimal('0.0')),
                                   'veto': (Decimal('80.0'), Decimal('0.0')),
                                   'pref': (Decimal('20.0'), Decimal('0.0'))},
                    'scale': [0.0, 100.0],
                    'weight': Decimal('1'),
                    'name': 'digraphs.RandomPerformanceTableau() instance',
                    'comment': 'Arguments: ; weightDistribution=random;
                        weightScale=(1, 1); commonMode=None'}}

        >>> t.evaluation
            {'g01': {'a02': Decimal('94.22'),
                     'a03': Decimal('72.38'),
                     'a01': Decimal('46.89')
                    }
            }

    """
    def __init__(self,numberOfActions = 13,\
                 numberOfCriteria = 7,\
                 weightDistribution = None,\
                 weightScale=None,\
                 integerWeights=True,\
                 commonScale = [0.0,100.0],\
                 commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0)],\
                 commonMode = None,\
                 valueDigits = 2,\
                 seed = None,
                 Debug = False):
        
        import sys,time,math
        from copy import copy

        # fixing the seed (None by default)
        import random
        random.seed(seed)

        # seeting tableau name
        self.name = 'randomperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = dict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            actions[actionKey] = {'shortName':actionKey,
                    'name': 'random decision action',
                    'comment': 'RandomPerformanceTableau() generated.' }
        self.actions = copy(actions)
        actionsList = [x for x in self.actions]
        actionsList.sort()
        
        # generate criterialist
        criteriaList = [('g%%0%dd' % nd) % (i+1)\
                        for i in range(numberOfCriteria)]
        
#        # generate weights
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
        digits=valueDigits
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
                 seed = None,
                 Debug = False):
        """
        *Parameters*:
            - number of actions,
            - number criteria,
            - weightDistribution := equisignificant|random
            - weightScale=(1,numberOfCriteria (default when random))
            - integerWeights = Boolean (True = default) 
            - commonThresholds = {'ind':(0,0),'pref':(1,0),'veto':(numberOfActions,0)} (default)
        """
        #imports
        from copy import copy

        # set random seed
        import random
        random.seed(seed)

        # set name
        self.name = 'randrankperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = dict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            actions[actionKey] = {'shortName':actionKey,
                    'name': 'random decision action',
                    'comment': 'RandomRankPerformanceTableau() generated.' }
        self.actions = copy(actions)
        actionsList = [x for x in self.actions]
        actionsList.sort()
        
        # generate criterialist
        criteriaList = [('g%%0%dd' % nd) % (i+1)\
                        for i in range(numberOfCriteria)]
        
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
            criteria[g]['name']='randomPerfTabs.RandomRankPerformanceTableau() instance'
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
        self.criteria = copy(criteria)
        # generate evaluations
        evaluation = {}       
        for g in criteria:
            evaluation[g] = {}
            choiceRange = list(range(1,numberOfActions+1))
            for a in actionsList:
                randeval = random.choice(choiceRange)
                evaluation[g][a] = Decimal( str(randeval) )
                choiceRange.remove(randeval)
        
        self.evaluation = copy(evaluation)
        self.weightPreorder = self.computeWeightPreorder()

# ------------------------------


class FullRandomPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of random performance tableaux
    """

    def __init__(self,numberOfActions = None,
                 numberOfCriteria = None,
                 weightDistribution = None,
                 weightScale=None,
                 integerWeights = True,
                 commonScale = None,
                 commonThresholds = None,
                 commonMode = None,
                 valueDigits=2,
                 seed = None,
                 Debug = False):

        # set name
        self.name = 'fullrandomperftab'

        # set random seaad
        import random
        random.seed(seed)

        # generate random actions
        nd = len(str(numberOfActions))
        actions = dict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            actions[actionKey] = {'shortName':actionKey,
                    'name': 'random decision action',
                    'comment': 'RandomRankPerformanceTableau() generated.' }
        self.actions = copy(actions)
        actionsList = [x for x in self.actions]
        actionsList.sort()

        # generate criterialist
        criteriaList = [('g%%0%dd' % nd) % (i+1)\
                        for i in range(numberOfCriteria)]

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
        self.criteria = copy(criteria)
        self.evaluation = copy(evaluation)
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

#----------test Digraph class ----------------
if __name__ == "__main__":

    from randomPerfTabs import *
    from outrankingDigraphs import BipolarOutrankingDigraph

    t = RandomRankPerformanceTableau(numberOfActions=10,numberOfCriteria=7,seed=100)
    t.showAll()
    t.showHTMLPerformanceHeatmap(Correlations=True)
    g = BipolarOutrankingDigraph(t,Normalized=True)
    
    print('*-------- Testing classes and methods -------')

     
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. August 2011                    *')
    print('* $Revision: 1.37 $                *')                   
    print('*************************************')

#############################
