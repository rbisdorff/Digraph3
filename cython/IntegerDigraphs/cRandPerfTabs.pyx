#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cPython implementation of digraphs
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

__version__ = "cython 1.0"

from perfTabs import *
#from decimal import Decimal
from collections import OrderedDict

#########################################
# generators for random PerformanceTableaux
class cPerformanceTableau(PerformanceTableau):
    """
    Abstract root class for cythenized performace tableau methods.
    """
    def convert2BigData(self):
        self.convertWeight2Integer()
        self.convertEvaluation2Float()
        self.convertDiscriminationThresholds2Float()

    def convert2Standard(self):
        self.convertWeight2Decimal()
        self.convertEvaluation2Decimal()
        self.convertDiscriminationThresholds2Decimal()
        
    def convertWeight2Integer(self):
        """
        Convert significance weights from Decimal format
        to int format.
        """
        criteria = self.criteria
        for g in criteria:
            criteria[g]['weight'] = int(criteria[g]['weight'])
        self.criteria = criteria

    def convertWeight2Decimal(self):
        """
        Convert significance weights from Decimal format
        to int format.
        """
        from decimal import Decimal
        criteria = self.criteria
        for g in criteria:
            criteria[g]['weight'] = Decimal(str(criteria[g]['weight']))
        self.criteria = criteria

    def convertEvaluation2Float(self):
        """
        Convert evaluations from decimal format to float
        """
        evaluation = self.evaluation
        actions = self.actions
        criteria = self.criteria
        for g in criteria:
            for x in actions:
                evaluation[g][x] = float(evaluation[g][x])
        self.evaluation = evaluation

    def convertEvaluation2Decimal(self):
        """
        Convert evaluations from decimal format to float
        """
        from decimal import Decimal
        evaluation = self.evaluation
        actions = self.actions
        criteria = self.criteria
        for g in criteria:
            for x in actions:
                evaluation[g][x] = Decimal('%.2f' % evaluation[g][x])
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

    def showCriteria(self,IntegerWeights=True,Alphabetic=False,ByObjectives=True,Debug=False):
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
                    print()
        else:
            criteriaList = list(dict.keys(criteria))
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
                print()

    def normalizeEvaluations(self,lowValue=0.0,highValue=100.0,Debug=False):
        """
        recode the evaluations between lowValue and highValue on all criteria
        """
        ##from math import copysign
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
##        lowValue = Decimal(str(lowValue))
##        highValue = Decimal(str(highValue))
        amplitude = highValue-lowValue
        if Debug:
            print('lowValue', lowValue, 'amplitude', amplitude)
        criterionKeys = [x for x in criteria]
        actionKeys = [x for x in actions]
        normEvaluation = {}
        for g in criterionKeys:
            normEvaluation[g] = {}
            glow = criteria[g]['scale'][0]
            ghigh = criteria[g]['scale'][1]
            gamp = ghigh - glow
            if Debug:
                print('-->> g, glow, ghigh, gamp', g, glow, ghigh, gamp)
            for x in actionKeys:
                if evaluation[g][x] != -999:
                    evalx = abs(evaluation[g][x])
                    if Debug:
                        print(evalx)
                    ## normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                    try:
                        if criteria[g]['preferenceDirection'] == 'min':
                            sign = -1
                        else:
                            sign = 1
                        normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)*sign
                        ## else:
                        ##     normEvaluation[g][x] = -(lowValue + ((evalx-glow)/gamp)*(-amplitude))
                    except:
                        self.criteria[g]['preferenceDirection'] = 'max'
                        normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                        
                    if Debug:
                        print(criteria[g]['preferenceDirection'], evaluation[g][x], normEvaluation[g][x])
                else:
                    normEvaluation[g][x] = Decimal('-999')
                    
        return normEvaluation


class RandomPerformanceTableau(cPerformanceTableau):
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
        * commonThresholds := [(q0,q1),(p0,p1),(v0,v1)]; common indifference(q), preference (p)
          and considerable performance difference discrimination thresholds.
        * commonMode := common random distribution of random performance measurements:
             | ('uniform',Min,Max), uniformly distributed between min and max values. 
             | ('normal',mu,sigma), truncated Gaussion distribution. 
             | ('triangular',mode,repartition), generalized triangular distribution 
             | ('beta',alpha,beta).
        * valueDigits := <integer>, precision of performance measurements
          (2 decimal digits by default).
        
    Code example::
        >>> from randomPerfTabs import RandomPerformanceTableau
        >>> t = RandomPerformanceTableau(numberOfActions=3,numberOfCriteria=1,seed=100)
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
            {'g01': {'a01': Decimal('45.95'),
                     'a02': Decimal('95.17'),
                     'a03': Decimal('17.47')
                    }
            }

    """
    def __init__(self,long numberOfActions = 13,\
                 int numberOfCriteria = 7,\
                 weightDistribution = 'equisignificant',\
                 weightScale=None,\
                 bint integerWeights=True,\
                 commonScale = (0.0,100.0),\
                 commonThresholds = ((10.0,0.0),(20.0,0.0),(80.0,0.0)),\
                 commonMode = None,\
                 int valueDigits = 2,\
                 float missingDataProbability = 0.0,\
                 bint BigData=True,\
                 seed = None,\
                 bint Debug = False):

        cdef int nd,ng,ngd,digits
        cdef long i,a,x
        cdef float ind, pref, weakVeto, veto, randeval, comonAmplitude, m, M, xm, r, beta, alpha, mu, sigma
        
        import sys,time,math
        from copy import copy

        # fixing the seed (None by default)
        import random
        random.seed(seed)
        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr

        # seeting tableau name
        self.name = 'cRandomperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionName = ('a%%0%dd' % (nd)) % (i+1)
            actions[i] = {'name': actionName}
                
#        # generate weights
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            for i in range(numberOfCriteria):
                weightsList.append(random.randint(weightScale[0],\
                                                  weightScale[1]))
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            for i in range(numberOfCriteria):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
            weightsList.reverse()
        elif weightDistribution == 'equisignificant' or\
           weightDistribution == 'equiobjectives':
            weightScale = (1,1)
            weightsList = []
            for i in range(numberOfCriteria):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!'\
                   % (weightDistribution) )

        # generate criteria dictionary
        ng = numberOfCriteria
        ngd = len(str(ng))
        criteria = OrderedDict()
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; commonMode='+str(commonMode)
        digits = valueDigits
        commonAmplitude = commonScale[1] - commonScale[0]
        
        for i in range(numberOfCriteria):
            g = ('g%%0%dd' % ngd) % (i+1)
            criteria[g] = {}
            criteria[g]['name']='RandomPerformanceTableau() instance'
            criteria[g]['comment']=commentString
            try:
                veto = round(commonThresholds[3][0]*commonAmplitude/100.0,digits)
                ind = round(commonThresholds[0][0]*commonAmplitude/100.0,digits)
                pref = round(commonThresholds[1][0]*commonAmplitude/100.0,digits)
                weakVeto = round(commonThresholds[2][0]*commonAmplitude/100.0,digits)
                indThresholds=(ind,commonThresholds[0][1])
                prefThresholds=(pref,commonThresholds[1][1])
                weakVetoThresholds=(weakVeto,commonThresholds[2][1])
                vetoThresholds=(veto,commonThresholds[3][1])
                criteria[g]['thresholds'] = {'ind':indThresholds,
                                             'pref':prefThresholds,
                                             'weakVeto':weakVetoThresholds,
                                             'veto':vetoThresholds}
            except:
                ind = round(commonThresholds[0][0]*commonAmplitude/100.0,digits)
                pref = round(commonThresholds[1][0]*commonAmplitude/100.0,digits)
                veto = round(commonThresholds[2][0]*commonAmplitude/100.0,digits)
                indThresholds=(ind,commonThresholds[0][1])
                prefThresholds=(pref,commonThresholds[1][1])
                vetoThresholds=(veto,commonThresholds[2][1])                
                criteria[g]['thresholds'] = {'ind':indThresholds,
                                             'pref':prefThresholds,
                                             'veto':vetoThresholds}
            criteria[g]['scale'] = commonScale
            criteria[g]['weight'] = weightsList[i]
        #self.criteria = criteria
        
        # generate evaluations
        if commonMode == None:
            commonMode = ['uniform',None,None]
        digits=valueDigits

        evaluation = {}        
        if str(commonMode[0]) == 'uniform':          
            for g in criteria:
                evaluation[g] = {}
                for a in actions:
                    ## randeval = random.randint(commonScale[0],commonScale[1])
                    randeval = random.uniform(commonScale[0],commonScale[1])
                    evaluation[g][a] = round(randeval,digits)
                    
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
            rng = RNGTr(m,M,xm,r)
            for g in criteria:
                evaluation[g] = {}
                for a in actions:
                    evaluation[g][a] = round(rng.random(),digits)
                    

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
                for a in actions:
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    evaluation[g][a] = round(randeval,digits)
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
                for a in actions:
                    notfound = True 
                    while notfound:
                        randeval = random.normalvariate(mu,sigma)
                        if randeval >= commonScale[0] and  randeval <= commonScale[1]:
                            notfound = False
                    evaluation[g][a] = round(randeval,digits)

        else:
            print('mode error in random evaluation generator !!')
            print(str(commonMode[0]))
            #sys.exit(1)
        # randomly insert missing data 
        for c in criteria:
            for x in actions:
                if random.random() < missingDataProbability:
                    evaluation[c][x] = Decimal('-999')

        # store object dict
        self.actions = actions
        self.criteria = criteria
        self.evaluation = evaluation
        # store weights preorder
        self.weightPreorder = self.computeWeightPreorder()

# -----------------
class RandomRankPerformanceTableau(cPerformanceTableau):
    """
    Specialization of the PerformanceTableau class for generating a temporary
    random performance tableau.

    Random generator for multiple criteria ranked (without ties) performances of a
    given number of decision actions. On each criterion,
    all decision actions are hence lineraly ordered. The RandomRankPerformanceTableau class is
    matching the RandomLinearVotingProfiles class (see the votingDigraphs module)  
        
    *Parameters*:
        * number of actions,
        * number of performance criteria,
        * weightDistribution := equisignificant | random (default, see RandomPerformanceTableau)
        * weightScale := (1, 1 | numberOfCriteria (default when random))
        * integerWeights := Boolean (True = default) 
        * commonThresholds (default) := {
            | 'ind':(0,0),
            | 'pref':(1,0),
            | 'veto':(numberOfActions,0)
            | } (default)

    """
    def __init__(self, long numberOfActions = 13, int numberOfCriteria = 7,\
                 weightDistribution = 'equisignificant', weightScale=None,\
                 commonThresholds = None,
                 seed = None,\
                 bint Debug = False):
        """
        """
        cdef int i, j, nd
        cdef float randeval 
        
        # set random seed
        import random
        random.seed(seed)

        # set name
        self.name = 'randrankperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionName = ('a%%0%dd' % (nd)) % (i+1)
            actions[i] = {'name': actionName}

        # generate the criteria weights
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            for j in range(numberOfCriteria):
                weightsList.append(random.randint(weightScale[0],weightScale[1]))
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightScale = (1,1)
            weightsList = [weightScale[0] for j in range(numberOfCriteria)]
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary
        ngd = len(str(numberOfCriteria))
        criteria = OrderedDict()
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; commonThresholds='+str(commonThresholds)
    
        for j in range(numberOfCriteria):
            g = ('g%%0%dd' % ngd) % (j+1)
            criteria[g] = {}
            criteria[g]['name']='RandomRankPerformanceTableau() instance'
            criteria[g]['comment']=commentString
            try:
                indThreshold  =(commonThresholds['ind'][0],
                                commonThresholds['ind'][1])
                prefThreshold =(commonThresholds['pref'][0],
                                commonThresholds['pref'][1])
                vetoThreshold =(commonThresholds['veto'][0],
                                commonThresholds['veto'][1])
             
                criteria[g]['thresholds'] = {'ind':indThreshold,
                                             'pref':prefThreshold,
                                             'veto':vetoThreshold}
            except:
                indThreshold  = (0.0, 0.0)
                prefThreshold = (1.0, 0.0)
                vetoThreshold = ( float(numberOfActions),0.0 )               
                criteria[g]['thresholds'] = { 'ind':indThreshold,\
                                              'pref':prefThreshold,\
                                              'veto': vetoThreshold
                                              }
            commonScale = ( 0.0, float(numberOfActions) )
            criteria[g]['scale'] = commonScale
            criteria[g]['weight'] = weightsList[j]
                
        # generate evaluations
        evaluation = {}       
        for g in criteria:
            evaluation[g] = {}
            choiceRange = list(range(1,numberOfActions+1))
            random.shuffle(choiceRange)
            for a in actions:
                randeval = float(choiceRange[a])
                evaluation[g][a] = randeval

        # install object items
        self.actions = actions
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

# ------------------------------


## class FullRandomPerformanceTableau(PerformanceTableau):
##     """
##     Full automatic generation of random performance tableaux
##     """

##     def __init__(self,numberOfActions = None,
##                  numberOfCriteria = None,
##                  weightDistribution = None,
##                  weightScale=None,
##                  integerWeights = True,
##                  commonScale = None,
##                  commonThresholds = None,
##                  commonMode = None,
##                  valueDigits=2,
##                  seed = None,
##                  Debug = False):
##         # import OrderedDict container
##         from collections import OrderedDict
##         # set name
##         self.name = 'fullrandomperftab'

##         # set random seaad
##         import random
##         random.seed(seed)

##         # generate random actions
##         if numberOfActions == None:
##             numberOfActions = random.randint(7,30)
##         nd = len(str(numberOfActions))
##         actions = OrderedDict()
##         for i in range(numberOfActions):
##             actionKey = ('a%%0%dd' % (nd)) % (i+1)
##             actions[actionKey] = {'shortName':actionKey,
##                     'name': 'random decision action',
##                     'comment': 'RandomRankPerformanceTableau() generated.' }
##         self.actions = actions
##         actionsList = [x for x in actions.keys()]

##         # generate criterialist
##         if numberOfCriteria == None:
##             numberOfCriteria = random.randint(5,21)
            
##         ng = len(str(numberOfCriteria))
##         criteriaList = [('g%%0%dd' % ng) % (i+1)\
##                         for i in range(numberOfCriteria)]               
##         criteriaList.sort()

##         # generate random weights
##         if weightDistribution == None:
##             majorityWeight = numberOfCriteria + 1
##             weightModesList = [('fixed',[1,1],1),
##                                ('random',[1,3],2),
##                                ('random',[1,numberOfCriteria],3)]
##             weightMode = random.choice(weightModesList)
##             weightDistribution = weightMode[0]
##             weightScale =  weightMode[1]
##         else:
##             if weightScale == None:
##                 weightScale = (1,numberOfCriteria)
##             weightMode=[weightDistribution,weightScale]
##         if weightDistribution == 'random':
##             weightsList = []
##             sumWeights = 0.0
##             for i in range(len(criteriaList)):
##                 g = criteriaList[i]
##                 weightsList.append(random.randint(weightScale[0],weightScale[1]))
##                 sumWeights += weightsList[i]
##             weightsList.reverse()
##         elif weightDistribution == 'fixed':
##             weightsList = []
##             sumWeights = 0.0
##             for i in range(len(criteriaList)):
##                 if i == 0:
##                     weightsList.append(weightScale[1])
##                     sumWeights += weightScale[1]
##                 else:
##                     weightsList.append(weightScale[0])
##                     sumWeights += weightScale[0]
##             weightsList.reverse()
##         elif weightDistribution == 'equisignificant' or weightDistribution == 'equiobjectives':
##             weightScale = (1,1)
##             weightsList = []
##             sumWeights = 0.0
##             for i in range(len(criteriaList)):
##                 if i == 0:
##                     weightsList.append(weightScale[1])
##                     sumWeights += weightScale[1]
##                 else:
##                     weightsList.append(weightScale[0])
##                     sumWeights += weightScale[0]
##             weightsList.reverse()
##         else:
##             print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

##         # generate criteria dictionary with random thresholds
##         if commonScale == None:
##             commonScale = [0.0,100.0]
##         criteria = OrderedDict()
##         for i in range(len(criteriaList)):
##             g = criteriaList[i]
##             criteria[g] = {}
##             criteria[g]['name'] = 'random criterion'
##             #t = time.time()
##             if commonThresholds == None:        
##                 thresholds = []
##                 thresholds.append((round(random.uniform(0.0,commonScale[1]/5.0),valueDigits),0.0))
##                 thresholds.append((round(random.uniform(thresholds[0][0],commonScale[1]/3.0),valueDigits),0.0))
##                 thresholds.append((round(random.uniform(commonScale[1]*2.0/3.0,commonScale[1]),valueDigits),0.0))
##                 thresholds.append((round(random.uniform(thresholds[2][0],commonScale[1]),valueDigits),0.0))
                
##             else:
##                 thresholds = commonThresholds
##             ## print thresholds
##             try:
##                 criteria[g]['thresholds'] = {
##                     'ind':(Decimal(str(thresholds[0][0])),Decimal(str(thresholds[0][1]))),
##                     'pref':(Decimal(str(thresholds[1][0])),Decimal(str(thresholds[1][1]))),
##                     'weakVeto':(Decimal(str(thresholds[2][0])),Decimal(str(thresholds[2][1]))),
##                     'veto':(Decimal(str(thresholds[3][0])),Decimal(str(thresholds[3][1]))),
##                     }
##             except:
##                 criteria[g]['thresholds'] = {
##                     'ind':(Decimal(str(thresholds[0][0])),Decimal(str(thresholds[0][1]))),
##                     'pref':(Decimal(str(thresholds[1][0])),Decimal(str(thresholds[1][1]))),
##                     'veto':(Decimal(str(thresholds[2][0])),Decimal(str(thresholds[2][1]))),
##                     }               
##             criteria[g]['scale'] = commonScale
##             if integerWeights:
##                 criteria[g]['weight'] = Decimal(str(weightsList[i]))
##             else:
##                 criteria[g]['weight'] = Decimal(str(weightsList[i]))/Decimal(str(sumWeights))

##         # generate random evaluations
##         x30=commonScale[1]*0.3
##         x50=commonScale[1]*0.5
##         x70=commonScale[1]*0.7
##         randomLawsList = [['uniform',commonScale[0],commonScale[1]],
##                           ('triangular',x30,0.33),('triangular',x30,0.50),('triangular',x30,0.75),
##                           ('triangular',x50,0.33),('triangular',x50,0.50),('triangular',x50,0.75),
##                           ('triangular',x70,0.33),('triangular',x70,0.50),('triangular',x70,0.75),
##                           ('normal',x30,20.0),('normal',x30,25.0),('normal',x30,30.0),
##                           ('normal',x50,20.0),('normal',x50,25.0),('normal',x50,30.0),
##                           ('normal',x70,20.0),('normal',x70,25.0),('normal',x70,30.0)]
##         evaluation = {}
##         for i in range(len(criteriaList)):
##             g = criteriaList[i]
##             evaluation[g] = {}
##             if commonMode == None:
##                 randomMode = random.choice(randomLawsList)
##             else:
##                 randomMode = commonMode
##             if randomMode[0] == 'uniform':
##                 randomMode[1] = commonScale[0]
##                 randomMode[2] = commonScale[1]
##             criteria[g]['randomMode'] = randomMode
##             if randomMode[0] != 'beta':
##                 if randomMode[1] == None and randomMode[2] == None:
##                     commentString = randomMode[0] + ', default, default'
##                 elif randomMode[1] != None and randomMode[2] == None:
##                     commentString = randomMode[0]+', %.2f, default' % float(randomMode[1])
##                 elif randomMode[1] == None and randomMode[2] != None:
##                     commentString = randomMode[0]+', default, %.2f' % (float(randomMode[2]))
##                 else:
##                     commentString = randomMode[0]+', %.2f, %.2f' % (float(randomMode[1]),float(randomMode[2]))
##             else:
##                 if randomMode[1] != None and randomMode[2] != None:
##                     commentString = randomMode[0]+', %.2f, (%.4f,%.4f)' % (float(randomMode[1]),float(randomMode[2][0]),float(randomMode[2][1]))
##                 elif randomMode[1] == None and randomMode[2] != None:
##                     commentString = randomMode[0]+', default, (%.4f,%.4f)' % (float(randomMode[2][0]),float(randomMode[2][1]))
##                 if randomMode[1] != None and randomMode[2] == None:
##                     commentString = randomMode[0]+', %.2f, default' % (float(randomMode[1]))
##                 else:
##                     commentString = randomMode[0]+', default,default'
                    
                
##             criteria[g]['comment'] = 'Evaluation generator: '+commentString
##             digits = valueDigits
##             if str(randomMode[0]) == 'uniform':          
##                 evaluation[g] = {}
##                 for a in actionsList:
##                     randeval = random.uniform(commonScale[0],commonScale[1])
##                     evaluation[g][a] = Decimal(str(round(randeval,digits)))
##             elif str(randomMode[0]) == 'triangular':
##                 from randomNumbers import ExtendedTriangularRandomVariable as RNG
##                 m = commonScale[0]
##                 M = commonScale[1]
##                 try:
##                     if commonMode[1] == None:
##                         xm = (M-m)/2.0
##                     else:
##                         xm = commonMode[1]
##                 except:
##                     xm = (M-m)/2.0
##                 try:    
##                     if commonMode[2] == None:
##                         r  = 0.5
##                     else:
##                         r  = commonMode[2]
##                 except:
##                     r  = 0.5
##                 rng = RNG(m,M,xm,r)
##                 for a in actionsList:
## ##                    u = random.random()
## ##                    if u < r:
## ##                        randeval = m + math.sqrt(u/r)*(xm-m)                
## ##                    else:
## ##                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
## ##                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     evaluation[g][a] = Decimal(str(round(rng.random(),digits)))

##             elif str(randomMode[0]) == 'normal':
##                 try:
##                     if commonMode[1] == None:
##                         mu = (commonScale[1]-commonScale[0])/2.0
##                     else:
##                         mu = commonMode[1]
##                 except:
##                     mu = (commonScale[1]-commonScale[0])/2.0
##                 try:
##                     if commonMode[2] == None:
##                         sigma = (commonScale[1]-commonScale[0])/4.0
##                     else:
##                         sigma = commonMode[2]
##                 except:
##                     sigma = (commonScale[1]-commonScale[0])/4.0
##                 for a in actionsList:
##                     notfound = True 
##                     while notfound:
##                         randeval = random.normalvariate(mu,sigma)
##                         if randeval >= commonScale[0] and  randeval <= commonScale[1]:
##                             notfound = False
##                     evaluation[g][a] = Decimal(str(round(randeval,digits)))

##             elif str(randomMode[0]) == 'beta':
##                 m = commonScale[0]
##                 M = commonScale[1]
##                 if commonMode[1] == None:
##                     xm = 0.5
##                 else:
##                     xm = commonMode[1]
                
##                 if commonMode[2] == None:
##                     if xm > 0.5:
##                         beta = 2.0
##                         alpha = 1.0/(1.0 - xm)
##                     else:
##                         alpha = 2.0
##                         beta = 1.0/xm
##                 else:
##                     alpha = commonMode[2][0]
##                     beta = commonMode[2][1]
##                 if Debug:
##                     print('alpha,beta', alpha,beta)
##                 for a in actionsList:
##                     u = random.betavariate(alpha,beta)
##                     randeval = (u * (M-m)) + m
##                     evaluation[g][a] = Decimal(str(round(randeval,digits)))
##                     if Debug:
##                         print('xm,alpha,beta,u,m,M,randeval',xm,alpha,beta,u,m,M,randeval)
                    
##         # install self object attributes

##         self.criteriaWeightMode = weightMode
##         self.criteria = criteria
##         self.evaluation = evaluation
##         self.weightPreorder = self.computeWeightPreorder()


##     def showAll(self):
##         """
##         Show fonction for performance tableau of full random outranking digraph.
##         """
##         criteria = self.criteria
##         evaluation = self.evaluation
##         print('*-------- show performance tableau -------*')
##         print('Name         :', self.name)
##         print('Actions      :', self.actions)
##         print('Criteria     :')       
##         for g in criteria:
##             print('  criterion name:', g, end=' ')
##             print(', scale: ', criteria[g]['scale'], end=' ')
##             print(', weight: %.3f ' % (criteria[g]['weight']))
##             print('  thresholds:', criteria[g]['thresholds'])
##             print('  evaluations generation mode: ', criteria[g]['randomMode'])
##             print()
##         print('  Weights generation mode: ', self.criteriaWeightMode)
##         print('  Weights preorder       : ', self.weightPreorder)
##         print('Evaluations            :')
##         for g in evaluation:
##             print(g, evaluation[g])

class RandomCoalitionsPerformanceTableau(cPerformanceTableau):
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

    def __init__(self, int numberOfActions = 13,\
                 int numberOfCriteria = 7,\
                 weightDistribution = None,\
                 weightScale=None,\
                 #integerWeights = True,\
                 commonScale = None,\
                 commonThresholds = None, commonMode = None,\
                 int valueDigits=2, bint Coalitions=True,\
                 bint VariableGenerators=True,\
                 bint Debug=False, bint RandomCoalitions=False,\
                 vetoProbability=None,\
                 #bint BigData=False,\
                 seed= None,\
                 ):

        cdef int nd, x, nbrcrit, a, weightsProduct=1, digits
        cdef float span, randeval, randVeto, m, M, r, alpha, beta, xm=0.0, u
        
        # naming
        self.name = 'cRandCoalitionsPerfTab'
        # randomizer init
        import random
        random.seed(seed)
        if RandomCoalitions:
            Coalitions=False

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            
        from collections import OrderedDict
            
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            #if BigData:
            actions[i] = {'shortName':actionKey,
                          'name': actionKey,
                          'generators': {}}
            ## else:   
            ##     actions[actionKey] = {'shortName':actionKey,
            ##             'name': 'random decision action',
            ##             'comment': 'RandomCoalitionsPerformanceTableau() generated.',
            ##             'generators': {}}
        self.actions = actions
        actionsList = [x for x in actions.keys()]
        #actionsList.sort()
        
        # generate criterialist
        nd = len(str(numberOfCriteria))
        criteriaList = [('g%%0%dd' % nd) % (j+1)\
                        for j in range(numberOfCriteria)]
        
        # generate random weights
        if weightDistribution == None:
            weightMode = ('equisignificant',(1,1))
            weightDistribution = weightMode[0]
            weightScale =  weightMode[1]
        else:
            weightMode=[weightDistribution,weightScale]
        if weightDistribution == 'random':
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightsList = []
            for j in range(len(criteriaList)):               
                weightsList.append(random.randint(weightScale[0],weightScale[1]))
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            if weightScale == None:
                weightScale = (1,numberOfCriteria)            
            weightsList = []
            for i in range(len(criteriaList)):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
            weightsList.reverse()
        elif weightDistribution == 'equisignificant'\
          or weightDistribution == 'equiobjectives'\
          or weightDistribution == 'equicoalitions':
            weightScale = (1,1)            
            weightsList = []
            for i in range(len(criteriaList)):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
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
        criteria = OrderedDict()

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
            if commonThresholds == None:                        
                span = commonScale[1] - commonScale[0]
                thresholds = [(0.05001*span,0),(0.10001*span,0.0),(0.60001*span,0.0)]
            else:
                thresholds = commonThresholds
            ## print thresholds
            #if Electre3:
            thitems = ['ind','pref','veto']
            ## else:
            ##     thitems = ['ind','pref','weakVeto','veto']
            if vetoProbability != None:
                randVeto = random.uniform(0.0,1.0)
                if randVeto > vetoProbability:
                    thitems = ['ind','pref']
            criteria[g]['thresholds'] = {}
            for t in range(len(thitems)):
                criteria[g]['thresholds'][thitems[t]] =\
                   (thresholds[t][0],thresholds[t][1])
                
            criteria[g]['scale'] = commonScale
            criteria[g]['weight'] = weightsList[gi]

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
        #weightsProduct = 1
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
        if Coalitions and VariableGenerators:
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
        for gi in range(len(criteriaList)):
            g = criteriaList[gi]
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
                        randomRangesList = [(commonScale[0],commonScale[1]),
                                            (commonScale[0],commonScale[0]+0.3*(commonScale[1]-commonScale[0])),
                                            (commonScale[0],commonScale[0]+0.7*(commonScale[1]-commonScale[0]))]
                        randomRange = random.choice(randomRangesList)         
                        randeval = random.uniform(randomRange[0],randomRange[1])
                    else:
                        randomRange = (randomMode[1],randomMode[2]) 
                        randeval = random.uniform(randomMode[1],randomMode[2])
                    self.actions[a]['generators'][g] = (randomMode[0],randomRange)
                    ## if OrdinalScales:
                    ##     randeval /= 10.0
                    ##     if criteria[g]['preferenceDirection'] == 'max':
                    ##         evaluation[g][a] = round(randeval,0)
                    ##     else:
                    ##         evaluation[g][a] = -round(randeval,0)
                    ## else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)

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
                            alpha = 5.0
                            beta = 5.0
                            
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
                    ## if OrdinalScales:
                    ##     randeval /= 10.0
                    ##     if criteria[g]['preferenceDirection'] == 'max':
                    ##         evaluation[g][a] = round(randeval,0)
                    ##     else:
                    ##         evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    ## else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
    
            elif str(randomMode[0]) == 'triangular':
                for a in actionsList:
                    m = commonScale[0]
                    M = commonScale[1]
                    if VariableGenerators:
                        span = commonScale[1]-commonScale[0]
                        randomModesList = [0.3*span,0.5*span,0.7*span]
                        xm = random.choice(randomModesList)
                    else:
                        xm = randomMode[1]
                    r  = randomMode[2]
                    self.actions[a]['generators'][g] = (randomMode[0],xm,r)
                    # setting a speudo random seed
                    rdseed = random.random()
                    rngtr = RNGTr(m,M,xm,r,seed=rdseed)

                    randeval = rngtr.random()
                    ## if OrdinalScales:
                    ##     randeval /= 10.0
                    ##     if criteria[g]['preferenceDirection'] == 'max':
                    ##         evaluation[g][a] = Decimal(str(round(randeval,0)))
                    ##     else:
                    ##         evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    ## else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
                   
        # install self object attributes

        self.criteriaWeightMode = weightMode
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

class Random3ObjectivesPerformanceTableau(cPerformanceTableau):
    """
    Specialization of the PerformanceTableau
    for 3 objectives: *Eco*, *Soc* and *Env*.

    Each decision action is qualified at random as weak (-), fair (~) or good (+)
    on each of the three objectives.
    
    Generator arguments:
        * numberOf Actions := 20 (default)
        * number of Criteria := 13 (default)
        * weightDistribution := 'equiobjectives' (default)
                              | 'equisignificant' (weights set all to 1)
                              | 'random' (in the range 1 to numberOfCriteria)
        * weightScale := [1,numerOfCriteria] (random default)
        * integerWeights := True (default) / False
        * OrdinalScales := True / False (default), if True commonScale is set to (0,10)
        * commonScale := (0.0, 100.0) (default if OrdinalScales == False)
        * commonThresholds := [(1.0,0.0),(2.001,0.0),(8.001,0.0)] if OrdinalScales == True, otherwise
                            | [(0.10001*span,0.0),(0.20001*span,0.0),(0.80001*span,0.0)] with span = commonScale[1] - commonScale[0].
        * commonMode := ['triangular','variable',0.50] (default), A constant mode may be provided.
                      | ['uniform','variable',None], a constant range may be provided.
                      | ['beta','variable',None] (three alpha, beta combinations (5.8661,2.62203)
                      |   chosen by default for 'good', 'fair' and 'weak' evaluations. Constant parameters may be provided.
        * valueDigits := 2 (default, for cardinal scales only)
        * vetoProbability := x in ]0.0-1.0[ (0.5 default), probability that a cardinal criterion shows a veto preference discrimination threshold.
        * Debug := True / False (default)
        
    """

    def __init__(self, int numberOfActions = 20, int numberOfCriteria = 13,\
                 weightDistribution = 'equiobjectives', weightScale=None,\
                 #integerWeights = True,\
                 #OrdinalScales=False,\
                 commonScale = None,\
                 commonThresholds = None, commonMode = None,\
                 int valueDigits=2,\
                 float vetoProbability=0.5,\
                 float missingProbability = 0.05,\
                 #BigData=False,\
                 seed= None,\
                 bint Debug=False):

        cdef int nd, i, t, x, a, digits, weightsProduct = 1, objWeight=0
        cdef float span, randVeto, randeval, m, M, r, alpha, beta, xm=0.0, u      
        # naming
        self.name = 'random3ObjectivesPerfTab'
        # randomizer init
        import random
        random.seed(seed)

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            

            
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            actions[i] = {'name': actionKey,'generators': {}}
                           
        # generate random weights
        if weightDistribution == 'equisignificant':
            weightMode = ('equisignificant',(1,1))
            weightScale =  weightMode[1]
            weightsList = [weightScale[0] for i in range(numberOfCriteria)]
        elif weightDistribution == 'random':
            weightMode = ('random',(1,numberOfCriteria))
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightsList = []
            for i in range(numberOfCriteria):               
                weightsList.append(random.randint(weightScale[0],
                                                              weightScale[1]))
                sumWeights += weightsList[i]
            weightsList.reverse()
        else:
            weightDistribution = 'equiobjectives'
            weightMode = (weightDistribution,None)
            weightScale = (1,1)
            weightsList = []
            for i in range(numberOfCriteria):
                weightsList.append(weightScale[0])

        # generate objectives dictionary
        objectives = OrderedDict({
            'Eco': {'name':'Economical aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'},
            'Soc': {'name': 'Societal aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'},
            'Env': {'name':'Environmental aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'}
            })


        # generate criteria dictionary with random thresholds
        
        if commonScale == None:
            commonScale = (0.0,100.0)

        criteria = OrderedDict()
        objectivesKeys = list(objectives.keys())
        nd = len(str(numberOfCriteria))
        for i in range(numberOfCriteria):
            g = ('g%%0%dd' % nd) % (i+1)
            criteria[g] = {}
            if i == 0:
                criterionObjective = 'Eco'
            elif i == 1:
                criterionObjective = 'Soc'
            elif i == 2:
                criterionObjective = 'Env'
            else:    
                criterionObjective = random.choice(objectivesKeys)
            criteria[g]['objective'] = criterionObjective
            criteria[g]['preferenceDirection'] = 'max'           
            criteria[g]['name'] = 'criterion of objective %s' % (criterionObjective)
            criteria[g]['shortName'] = g + criterionObjective[0:2]
            if commonThresholds == None:                    
                span = commonScale[1] - commonScale[0]
                thresholds = [(0.05001*span,0),(0.10001*span,0.0),(0.60001*span,0.0)]
            else:
                thresholds = commonThresholds
            if Debug:
                print(g,thresholds)
            thitems = ['ind','pref','veto']
            randVeto = random.uniform(0.0,1.0)
            if randVeto > vetoProbability or vetoProbability == None:
                    thitems = ['ind','pref']
            criteria[g]['thresholds'] = {}
            for t in range(len(thitems)):
                criteria[g]['thresholds'][thitems[t]] =\
                   (thresholds[t][0],thresholds[t][1])
                
            criteria[g]['scale'] = commonScale
            criteria[g]['weight'] = weightsList[i]

        # determine equisignificant objectives
        if weightMode[0] == 'equiobjectives':
            objectivesCardinality = {}
            for g in criteria:
                try:
                    objectivesCardinality[criteria[g]['objective']] += 1
                except:
                    objectivesCardinality[criteria[g]['objective']] = 1
            if Debug:
                print(objectivesCardinality)
            #weightsProduct = 1
            for oi in objectivesCardinality:
                weightsProduct *= objectivesCardinality[oi]
            if Debug:
                print(weightsProduct)
            for g in criteria:
                criteria[g]['weight'] =\
                    weightsProduct // objectivesCardinality[criteria[g]['objective']]
                if Debug:
                    print(criteria[g]['weight'])
                
        # allocate (criterion,action) to coalition supporting type
        objectiveSupportingType = [('good','+'),('fair','~'),('weak','-')]
        for x in actions:
            profile = {}
            for obj in objectives:
                if Debug:
                    print(objectives,obj)
                ost = random.choice(objectiveSupportingType)
                actions[x][obj]=ost[0]
                actions[x]['name'] =\
                    actions[x]['name'] + ' '+ str(obj) + ost[1]
                profile[obj] = actions[x][obj]
            actions[x]['profile'] = profile
            if Debug:
                print(x,actions[x])
        # generate evaluations
        
        evaluation = {}
        for g in criteria:
            evaluation[g] = {}
            if commonMode == None:
                randomMode = ['triangular','variable',0.50]               
            else:
                randomMode = commonMode
            if randomMode[0] == 'uniform' and randomMode[1] == None:
                randomMode[1] = commonScale[0]
                randomMode[2] = commonScale[1]
                
            criteria[g]['randomMode'] = randomMode
            if randomMode[1] == 'variable':
                commentString = 'Variable '+randomMode[0]+(' performance generator with low (-), medium (~) or high (+) parameters.')
            else:
                commentString = 'Constant '+randomMode[0]+(' law with parameters = %s, %s' % (str(randomMode[1]),str(randomMode[2])))
                    
            criteria[g]['comment'] = commentString
            digits = valueDigits
            
            if str(randomMode[0]) == 'uniform':          
                for a in actions:
                    if randomMode[1] == 'variable':
                        aobj = criteria[g]['objective']
                        if actions[a]['profile'][aobj] == 'weak':
                            randomRange = (commonScale[0],
                                           commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                        elif actions[a]['profile'][aobj] == 'fair':
                            randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                           commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                        elif actions[a]['profile'][aobj] == 'good':
                            randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                          commonScale[1])       
                        actions[a]['comment'] += ': %s %s' % (randomMode[0],randomRange)
                    else:
                        randomRange = (commonScale[1],commonScale[2]) 
                    randeval = random.uniform(randomRange[0],randomRange[1])
                    actions[a]['generators'][g] = (randomMode[0],randomRange)
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)

            elif str(randomMode[0]) == 'beta':
                for a in actions:
                    m = commonScale[0]
                    M = commonScale[1]
                    if randomMode[1] == 'variable':
                        if actions[a][criteria[g]['objective']] == 'good':
                            # mode = 75, stdev = 15
                            #xm = 75
                            alpha = 5.8661
                            beta = 2.62203
                        elif actions[a][criteria[g]['objective']] == 'fair':
                            # nmode = 50, stdev = 15
                            #xm = 50
                            alpha = 5.05556
                            beta = 5.05556
                        elif actions[a][criteria[g]['objective']] == 'weak':
                            # mode = 25, stdev = 15
                            # xm = 25
                            alpha = 2.62203
                            beta = 5.8661
                        else:
                            alpha = 5.05556
                            beta = 5.05556
                            
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
                    actions[a]['generators'][g] = ('beta',alpha,beta)
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
    
            elif str(randomMode[0]) == 'triangular':
                for a in actions:
                    m = commonScale[0]
                    M = commonScale[1]
                    span = commonScale[1]-commonScale[0]
                    if randomMode[1] == 'variable':
                        if actions[a][criteria[g]['objective']] == 'good':
                            xm = 0.7*span
                        elif actions[a][criteria[g]['objective']] == 'fair':
                            xm = 0.5*span
                        elif actions[a][criteria[g]['objective']] == 'weak':
                            xm = 0.3*span
                    else:
                        xm = randomMode[1]
                    r  = randomMode[2]
                    actions[a]['generators'][g] = (randomMode[0],xm,r)
                    # setting a speudo random seed
                    if seed == None:
                        rdseed = random.random()
                    else:
                        try:
                            rdseed += 1
                        except:
                            rdseed = seed
                    rngtr = RNGTr(m,M,xm,r,seed=rdseed)
                    randeval = rngtr.random()
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
                   
                    if Debug:
                        print(randeval, criteria[g]['preferenceDirection'], evaluation[g][a])

        # install self object attributes

        for obj in objectives:
            objCriteria = [g for g in criteria if criteria[g]['objective'] == obj]
            objectives[obj]['criteria'] = objCriteria
            objWeight = 0
            for g in objCriteria:
                objWeight += criteria[g]['weight']
            objectives[obj]['weight'] = objWeight

        # instantiate the peformance tableau slots
        self.actions = actions
        self.objectives = objectives
        self.criteriaWeightMode = weightMode
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

        # insert missing data
        for g in criteria:
            sevalg = self.evaluation[g]
            for x in actions:
                if random.random() < missingProbability:
                    sevalg[x] = Decimal('-999')

    def showObjectives(self):
        print('*------ show objectives -------"')
        for obj in self.objectives:
                                               
            print('%s: %s' % (obj, self.objectives[obj]['name']))
                                               
            for g in self.objectives[obj]['criteria']:
                print('  ', g, self.criteria[g]['name'], self.criteria[g]['weight'])
                                               
            print('  Total weight: %.2f (%d criteria)\n'\
                  % (self.objectives[obj]['weight'],len(self.objectives[obj]['criteria'])))

    def showActions(self,Alphabetic=False):
        print('*----- show decision action --------------*')
        actions = self.actions
        if Alphabetic:
            actionsKeys = [x for x in dict.keys(actions)]
            actionsKeys.sort()
            for x in actionsKeys:
                print('key: ',x)
                try:
                    print('  short name: ',actions[x]['shortName'])
                except:
                    pass
                print('  name:       ',actions[x]['name'])
                print('  profile:    ',actions[x]['profile'])
        else:
            for x in actions.keys():
                print('key: ',x)
                try:
                    print('  short name: ',actions[x]['shortName'])
                except:
                    pass
                print('  name:      ',actions[x]['name'])
                print('  profile:   ',actions[x]['profile'])
        
#---------------
class RandomCBPerformanceTableau(cPerformanceTableau):
    """
    Full automatic generation of random
    Cost versus Benefit oriented performance tableaux.

    Parameters:
    
        * If numberOfActions == None, a uniform random number between 10 and 31 of cheap, neutral or advantageous actions (equal 1/3 probability each type) actions is instantiated
        * If numberOfCriteria == None, a uniform random number between 5 and 21 of cost or benefit criteria (1/3 respectively 2/3 probability) is instantiated
        * weightDistribution := {'equiobjectives'|'fixed'|'random'|'equisignificant' (default = 'equisignificant')}
        * default weightScale for 'random' weightDistribution is 1 - numberOfCriteria
        * commonScale parameter is obsolete. The scale of cost criteria is cardinal or ordinal (0-10) with proabailities 1/4 respectively 3/4, whereas the scale of benefit criteria is ordinal or cardinal with probabilities 2/3, respectively 1/3.
        * All cardinal criteria are evaluated with decimals between 0.0 and 100.0 wheras all ordinal criteria are evaluated with integers between 0 and 10.
        * commonThresholds is obsolete. Preference discrimination is specified as percentiles of concerned performance differences (see below).
        * CommonPercentiles = {'ind':0.05, 'pref':0.10, ['weakveto':0.90,] 'veto':'95} are expressed in centiless (reversed for vetoes) and only concern cardinal criteria.

    .. warning::

        Minimal number of decision actions required is 3 ! 

    """

    def __init__(self, int numberOfActions = 13,\
                 int numberOfCriteria = 7,\
                 weightDistribution = 'equiobjectives',\
                 weightScale=None,\
                 #integerWeights = True,\
                 commonScale = None, commonThresholds = None,\
                 commonPercentiles= None,\
                 int samplingSize = 100000,\
                 commonMode = None,\
                 int valueDigits = 2,\
                 float missingDataProbability = 0.0,\
                 #BigData=False,\
                 seed = None,\
                 bint Threading = False,\
                 int nbrCores = 1,\
                 Debug=False,Comments=False):
        """
        Constructor for RadomCBPerformanceTableau instances.
        
        """
        
        cdef int nd, i, digits, a, sample, x, y, n, nbuf
        cdef long n2
        cdef float mu, sigma, randeval, alpha, beta, m, M, xm, r, deltaMinus, deltaPlus, u,
        cdef float amplitude, 
        
        import sys,math,copy
        
        self.name = 'randomCBperftab'
        # randomizer init
        import random
        random.seed(seed)

        # generate actions
        nd = len(str(numberOfActions))
        actionsTypesList = ['cheap','neutral','advantageous']        
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionType = random.choice(actionsTypesList)
            actionName = ('a%%0%dd' % (nd)) % (i+1)
            actions[i] = {'shortName':actionName+actionType[0],
                              'name':actionName+actionType[0],
                              'type': actionType}
        # generate objectives
        objectives = OrderedDict({
            'C': {'name': 'Costs', 'criteria':[]},
            'B': {'name': 'Benefits', 'criteria':[]},
            })
        
        # generate criteria
        nd = len(str(numberOfCriteria))
        criterionTypesList = ['max','max','min']
        minScaleTypesList = ['cardinal','cardinal','cardinal','ordinal']
        maxScaleTypesList = ['ordinal','ordinal','cardinal']
        criterionTypeCounter = {'min':0,'max':0}
        criteria = OrderedDict()
        for i in range(numberOfCriteria):
            if i == 0:
                criterionType = 'min'
            elif i == 1:
                criterionType = 'max'
            else:
                criterionType = random.choice(criterionTypesList)
            criterionTypeCounter[criterionType] += 1
            if criterionType == 'min':
                g = ('c%%0%dd' % nd) % (criterionTypeCounter[criterionType])
            else:
                g = ('b%%0%dd' % nd) % (criterionTypeCounter[criterionType])               
            criteria[g] = {}
            criteria[g]['preferenceDirection'] = criterionType
            if criterionType == 'min':
                scaleType = random.choice(minScaleTypesList)
            else:
                scaleType = random.choice(maxScaleTypesList)
            criteria[g]['scaleType'] = scaleType
            if criterionType == 'min':
                criteria[g]['objective'] = 'C'
                criteria[g]['shortName'] = g
                objectives['C']['criteria'].append(g)
                if scaleType == 'ordinal':
                    criteria[g]['name'] = 'random ordinal cost criterion'
                else:
                    criteria[g]['name'] = 'random cardinal cost criterion'
            else:
                criteria[g]['objective'] = 'B'
                objectives['B']['criteria'].append(g)
                criteria[g]['shortName'] = g
                if scaleType == 'ordinal':
                    criteria[g]['name'] = 'random ordinal benefit criterion'
                else:
                    criteria[g]['name'] = 'random cardinal benefit criterion'
            if Debug:
                print("g, criteria[g]['scaleType'], criteria[g]['scale']", g, criteria[g]['scaleType'], end=' ')

            # commonScale parameter is obsolete
            commonScale = None
            if criteria[g]['scaleType'] == 'cardinal':
                criterionScale = (0.0, 100.0)   
            elif criteria[g]['scaleType'] == 'ordinal':
                criterionScale = (0, 10)
            else:
                criterionScale = (0.0, 100.0)
            criteria[g]['scale'] = criterionScale
            if Debug:
                print(criteria[g]['scale'])

        # generate random weights
        if weightDistribution == None:
            weightDistribution = 'equiobjectives'
            #weightDistribution = 'fixed'
            weightScale = (1,1)
            weightMode=[weightDistribution,weightScale]
        else:
            if weightScale == None:
                weightScale = (1,numberOfCriteria)
            weightMode=[weightDistribution,weightScale]
            
        if weightDistribution == 'random':
            weightsList = []
            for i in range(numberOfCriteria):
                weightsList.append(random.randint(weightScale[0],weightScale[1]))
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            for i in range(numberOfCriteria):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightsList = []
            weightScale = (1,1)
            weightMode=[weightDistribution,weightScale]
            for i in range(len(criteriaList)):
                if i == 0:
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
            weightsList.reverse()
        elif weightDistribution == 'equiobjectives':
            weightScale = (max(1,criterionTypeCounter['min']),max(1,criterionTypeCounter['max']))
            weightMode=[weightDistribution,weightScale]
            weightsList = []
            for g in criteria:
                if criteria[g]['preferenceDirection'] == 'min':
                    weightsList.append(weightScale[1])
                else:
                    weightsList.append(weightScale[0])
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))
        if Debug:
            print(weightsList, sumWeights)

        for i,g in enumerate(criteria):
            ## if Debug:
            ##     print 'criterionScale = ', criterionScale
            criteria[g]['weight'] = weightsList[i]
            if Debug:
                print(criteria[g])
        for obj in objectives:
            objectives[obj]['weight'] = sum([criteria[g]['weight']\
                    for g in criteria if criteria[g]['objective'] == obj])

        # generate random evaluations
        
        evaluation = {}
        for g in criteria:
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

            if Debug:
                print('commonMode = ', commonMode)
                print('randomMode = ', randomMode)
                   
            criteria[g]['comment'] = 'Evaluation generator: ' + commentString
            digits = valueDigits
            if str(randomMode[0]) == 'uniform':          
                evaluation[g] = {}
                for a in actions:
                    randeval = random.uniform(criterionScale[0],criterionScale[1])
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
            elif str(randomMode[0]) == 'triangular':
                for a in actions:
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
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
                    #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]
                        
            elif str(randomMode[0]) == 'normal':
                #mu = randomMode[1]
                #sigma = randomMode[2]
                for a in actions:
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
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
            elif str(randomMode[0]) == 'beta':
                m = criterionScale[0]
                M = criterionScale[1]
                for a in actions:
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
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
                    ## if Debug:
                    ##     print 'alpha,beta,u,m,M,randeval',alpha,beta,u,m,M,randeval
                        

 
        if Debug:
            print(evaluation)
        # restrict ordinal criteria to integer values
        for g in criteria:
            if criteria[g]['scaleType'] == 'ordinal':
                for a in actions:
                    if Debug:
                        print('-- >>', evaluation[g][a], end=' ')
                    evaluation[g][a] = round(evaluation[g][a],0)
                    if Debug:
                        print(evaluation[g][a])
                        
        # randomly insert missing data 
        for g in criteria:
            for x in actions:
                if random.random() < missingDataProbability:
                    evaluation[g][x] = Decimal('-999')

        # final storage
        self.actions = actions
        self.objectives = objectives
        self.criteriaWeightMode = weightMode
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

        # compute discrimination thresholds from commonPercentiles
        n = len(self.actions)
        n2 = (n*n) - n
        if n < 1000:
            nbuf = 1000
        else:
            nbuf = n
        if n2 < samplingSize:
            samplingSize = n2
        from iqagent import IncrementalQuantileEstimator
        est = IncrementalQuantileEstimator(nbuf=nbuf)
        if Debug:
            print('commonPercentiles=', commonPercentiles)
        if commonPercentiles == None:
            quantile = OrderedDict({'ind':0.05, 'pref':0.10 , 'veto':0.95})
        else:
            quantile = commonPercentiles
        for g in criteria:
            criteria[g]['thresholds'] = OrderedDict()
            if criteria[g]['scaleType'] == 'cardinal' and len(actions) > 1:
                est.reset()
                sample = 0
                for x in actions.keys():
                    evx = self.evaluation[g][x]
                    if evx != Decimal('-999'):
                        for y in actions.keys():
                            evy = self.evaluation[g][y]
                            if x != y and evy != Decimal('-999'):
                                est.add( float( abs(evx-evy) ) )
                                sample += 1
                                if sample > samplingSize:
                                    break
                est._update()
                for q in quantile:
                    if Comments:
                        print('-->', q, quantile[q], end=' ')
                    criteria[g]['thresholds'][q] = (est.report(quantile[q]),0.0)
            
            if Comments:
                print('criteria',g,' default thresholds:')
                print(criteria[g]['thresholds'])
    
        # update criteria
        self.criteria = criteria
# ----------------------
class NormalizedPerformanceTableau(PerformanceTableau):
    """
    specialsation of the PerformanceTableau class for
    constructing normalized, 0 - 100, valued PerformanceTableau
    instances from a given argPerfTab instance.
    """
    def __init__(self,argPerfTab=None,lowValue=0,highValue=100,coalition=None,Debug=False):
        import copy
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
            try:
                for th in criteria[g]['thresholds']:
                    empan = criteria[g]['scale'][1]-criteria[g]['scale'][0]
                    intercept = criteria[g]['thresholds'][th][0]/empan*(Decimal(str(highValue-lowValue)))
                    slope = criteria[g]['thresholds'][th][1]
                    criteria[g]['thresholds'][th] = (intercept,slope)
            except:
                pass
            criteria[g]['scale'] = [lowValue,highValue]
        self.criteria = criteria

    def normalizeEvaluations(self,float lowValue=0.0,float highValue=100.0,bint Debug=False):
        """
        recode the evaluations between lowValue and highValue on all criteria
        """
        cdef int x
        cdef float amplitude
        from decimal import Decimal
        ##from math import copysign
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
        #owValue = Decimal(str(lowValue))
        #ighValue = Decimal(str(highValue))
        amplitude = highValue-lowValue
        if Debug:
            print('lowValue', lowValue, 'amplitude', amplitude)
        criterionKeys = [g for g in criteria]
        actionKeys = [x for x in actions]
        normEvaluation = {}
        for g in criterionKeys:
            normEvaluation[g] = {}
            glow = criteria[g]['scale'][0]
            ghigh = criteria[g]['scale'][1]
            gamp = ghigh - glow
            if Debug:
                print('-->> g, glow, ghigh, gamp', g, glow, ghigh, gamp)
            for x in actionKeys:
                if evaluation[g][x] != Decimal('-999'):
                    evalx = abs(evaluation[g][x])
                    if Debug:
                        print(evalx)
                    ## normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                    try:
                        if criteria[g]['preferenceDirection'] == 'min':
                            sign = -1
                        else:
                            sign = 1
                        normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)*sign
                        ## else:
                        ##     normEvaluation[g][x] = -(lowValue + ((evalx-glow)/gamp)*(-amplitude))
                    except:
                        self.criteria[g]['preferenceDirection'] = 'max'
                        normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                        
                    if Debug:
                        print(criteria[g]['preferenceDirection'], evaluation[g][x], normEvaluation[g][x])
                else:
                    normEvaluation[g][x] = Decimal('-999')
                    
        return normEvaluation



## class RandomS3PerformanceTableau(RandomCoalitionsPerformanceTableau):
##     """
##     Obsolete dummy class for backports.
##     """

## #----------test Digraph class ----------------
## if __name__ == "__main__":
    
##     print('*-------- Testing classes and methods -------')

##     from digraphs import *
##     from outrankingDigraphs import BipolarOutrankingDigraph
##     from weakOrders import QuantilesRankingDigraph
##     from randomPerfTabs import *
##     from time import time
##     t0 = time()
##     t = RandomCBPerformanceTableau(numberOfActions=20,
##                                    numberOfCriteria=13,
##                                    samplingSize=100000,
##                                    BigData=True,
##                                    seed=100)
##     print(time()-t0)
##     t.saveXMCDA2('test2')
##    t.showCriteria()
##    t = Random3ObjectivesPerformanceTableau(numberOfActions=100,
##                                            numberOfCriteria=13,
##                                            OrdinalScales=False,
##                                            commonScale=None,
##                                            weightDistribution='equiobjectives',
##     #weightScale=(1,5),
##                                            commonMode=('beta','variable',None),
##                                            vetoProbability=0.5,
##                                            seed=120)

    ## t.showObjectives()
    ## t.showCriteria()
    ## t.csvAllQuantiles('q')
    ## print(t.showAllQuantiles())
    
##    #t.showActions(Debug=True)
##    teco = PartialPerformanceTableau(t,criteriaSubset=t.objectives['Eco']['criteria'])
##    tenv = PartialPerformanceTableau(t,criteriaSubset=t.objectives['Env']['criteria'])
##    tsoc = PartialPerformanceTableau(t,criteriaSubset=t.objectives['Soc']['criteria'])
##    geco = BipolarOutrankingDigraph(teco)
##    genv = BipolarOutrankingDigraph(tenv)
##    gsoc = BipolarOutrankingDigraph(tsoc)
##    gfus = FusionLDigraph([geco,genv,gsoc])
##    scc = StrongComponentsCollapsedDigraph(gfus)
##    scc.showActions()
##    scc.exportGraphViz('sccFusionObjectives')
    
    
##    t.showStatistics()
##    t.showHTMLPerformanceTableau()
    
##    print('*---------- test percentiles of variable thresholds --------*') 
####    t = RandomCoalitionsPerformanceTableau(weightDistribution='equicoalitions',
####                                           seed=100)
##    t = RandomPerformanceTableau(commonThresholds=[(90,0),(100,0),(110,0)],
##                                           seed=100)
##    t.showAll()
##
##    t.computeDefaultDiscriminationThresholds(quantile={'ind':10.0,'pref':20.0,'weakVeto':90.0,'veto':95.0})
##    for g in [y for y in t.criteria]:
##        print(g, t.criteria[g]['thresholds'])
##        for th in t.criteria[g]['thresholds']:
##            print(th)
##            print(' variable:', end=' ')
##            print(t.computeVariableThresholdPercentile(g,th,Debug=False))
##            print(' constant:', end=' ') 
##            print(t.computeThresholdPercentile(g,th))
##    t.showPerformanceTableau()
##    t.showCriteria(Debug=False)
##    t.saveXMCDA2('testPerc',servingD3=False)
##    t.showHTMLPerformanceHeatmap(Correlations=True)
##
    

##    t = RandomPerformanceTableau(weightScale=(1,10),
##                                 commonScale=(0.0,50),
##                                 commonMode=('triangular',30,0.5),
##                                 seed=100)
####    t = RandomCoalitionsPerformanceTableau(numberOfActions=10,
####                                           numberOfCriteria=7,
####                                           commonMode=('beta',None,None),
####                                           weightDistribution='equicoalitions',
####                                           seed=100)
##    t.showAll()
##    t.showStatistics()
##    t.showCriteria()
##    
##    t = RandomRankPerformanceTableau(seed=100)
##    t.showAll()
##    t.showStatistics()
##    t.showCriteria()
    # t = RandomCBPerformanceTableau(seed=100)
    # t.showAll()
    # t.showStatistics()
    #  #t.showHTMLPerformanceHeatmap(Correlations=True)
    # g = BipolarOutrankingDigraph(t,Normalized=True)
    # g.showAll()
     
    ## print('*------------------*')
    ## print('If you see this line all tests were passed successfully :-)')
    ## print('Enjoy !')

    ## print('*************************************')
    ## print('* R.B. August 2011                    *')
    ## print('* $Revision: 1.37 $                *')                   
    ## print('*************************************')

#############################
