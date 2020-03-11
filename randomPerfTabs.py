#!/usr/bin/env python3
"""
Python implementation of digraphs
Module for generating random performance tableaux  
Copyright (C) 2015-2020  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: 1.01 $"
# $Source: /home/cvsroot/Digraph/randomPerfTabs.py,v $

from perfTabs import PerformanceTableau
from decimal import Decimal
from collections import OrderedDict

#########################################
# generators for random PerformanceTableaux

class RandomPerformanceTableau(PerformanceTableau):
    """
    Specialization of the generic :py:class:`perftabs.PerformanceTableau` class for generating a temporary random performance tableau.

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
        * commonThresholds := [(q0,q1),(p0,p1),(v0,v1)]; common indifference(q), preference (p) and considerable performance difference discrimination thresholds. q0, p0 and v0 are expressed in percentige of the common scale amplitude: Max - Min.
        * commonMode := common random distribution of random performance measurements (default = ('beta',None,(2,2)) ):
             | ('uniform',None,None), uniformly distributed between min and max values. 
             | ('normal',mu,sigma), truncated Gaussion distribution. 
             | ('triangular',mode,repartition), generalized triangular distribution 
             | ('beta',mod,(alpha,beta)), mode in ]0,1[.
        * valueDigits := <integer>, precision of performance measurements
          (2 decimal digits by default).
        * missingDataProbability := 0 <= x <= 1.0; probability of missing performance evaluation on a criterion for an alternative (default 0.025).        

    Code example:
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
    def __init__(self,numberOfActions = 13,\
                 actionNamePrefix = 'a',\
                 numberOfCriteria = 7,\
                 weightDistribution = 'equisignificant',\
                 weightScale=None,\
                 IntegerWeights=True,\
                 commonScale = (0.0,100.0),\
                 commonThresholds = ((2.5,0.0),(5.0,0.0),(80.0,0.0)),\
                 commonMode = ('beta',None,(2,2)),\
                 valueDigits = 2,\
                 missingDataProbability = 0.025,\
                 BigData=False,\
                 seed = None,\
                 Debug = False):
        
        import sys,time,math
        from copy import copy

        # fixing the seed (None by default)
        self.randomSeed = seed
        import random
        random.seed(seed)
        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr
        
        # seeting tableau name
        self.name = 'randomperftab'
        self.BigData = BigData
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            if BigData:
                actionName = ('%s%%0%dd' % (actionNamePrefix,nd)) % (i)
                actions[i] = {'name': actionName}
            else:   
                actionKey = ('%s%%0%dd' % (actionNamePrefix,nd)) % (i)
                actions[actionKey] = {'shortName':actionKey,
                        'name': 'action #%d' % i,
                        'comment': 'RandomPerformanceTableau() generated.' }
                
#        # generate weights
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(numberOCriteria):
                if i == 0:
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant' or\
             weightDistribution == 'equiobjectives':
            weightScale = (1,1)
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):
                if i == 0:
                    weightsList.append(Decimal(str(weightScale[1])))
                    sumWeights += weightScale[1]
                else:
                    weightsList.append(Decimal(str(weightScale[0])))
                    sumWeights += weightScale[0]
            weightsList.reverse()
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!'\
                  % (weightDistribution))
        self.sumWeights = sumWeights

        # generate criteria dictionary
        if commonMode == None:
            #commonMode = ['uniform',None,None]
            commonMode = ['beta',None,(2,2)]
        ngd = len(str(numberOfCriteria))
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
            criteria[g]['name'] = 'RandomPerformanceTableau() instance'
            criteria[g]['comment'] = commentString
            criteria[g]['preferenceDirection'] = 'max'
            try:
                veto = round(commonThresholds[3][0]*commonAmplitude/100.0,digits)
                ind = round(commonThresholds[0][0]*commonAmplitude/100.0,digits)
                pref = round(commonThresholds[1][0]*commonAmplitude/100.0,digits)
                weakVeto = round(commonThresholds[2][0]*commonAmplitude/100.0,digits)
                indThresholds=(Decimal(str(ind)),Decimal(str(commonThresholds[0][1])))
                prefThresholds=(Decimal(str(pref)),Decimal(str(commonThresholds[1][1])))
                weakVetoThresholds=(Decimal(str(weakVeto)),Decimal(str(commonThresholds[2][1])))
                vetoThresholds=(Decimal(str(veto)),Decimal(str(commonThresholds[3][1])))
                criteria[g]['thresholds'] = {'ind':indThresholds,
                                             'pref':prefThresholds,
                                             'weakVeto':weakVetoThresholds,
                                             'veto':vetoThresholds}
            except:
                ind = round((commonThresholds[0][0]/100.0)*commonAmplitude,digits)
                pref = round(commonThresholds[1][0]*commonAmplitude/100.0,digits)
                veto = round(commonThresholds[2][0]*commonAmplitude/100.0,digits)
                indThresholds=(Decimal(str(ind)),Decimal(str(commonThresholds[0][1])))
                prefThresholds=(Decimal(str(pref)),Decimal(str(commonThresholds[1][1])))
                vetoThresholds=(Decimal(str(veto)),Decimal(str(commonThresholds[2][1])))                
                criteria[g]['thresholds'] = {'ind':indThresholds,
                                             'pref':prefThresholds,
                                             'veto':vetoThresholds}
            criteria[g]['scale'] = commonScale
            if IntegerWeights:
                criteria[g]['weight'] = weightsList[i]
            else:
                criteria[g]['weight'] = weightsList[i]/sumWeights
        #self.criteria = criteria
        
        # generate evaluations
        digits=valueDigits
        self.digits = digits
        self.commonScale = commonScale
        self.commonMode = commonMode

        evaluation = {}        
        if str(commonMode[0]) == 'uniform':          
            for g in criteria:
                evaluation[g] = {}
                for a in actions:
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
            rdseed = random.random()
            rng = RNGTr(m,M,xm,r,seed=rdseed)
            for g in criteria:
                evaluation[g] = {}
                for a in actions:
##                    u = random.random()
##                    if u < r:
##                        randeval = m + math.sqrt(u/r)*(xm-m)                   
##                    else:
##                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
##                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    evaluation[g][a] = Decimal(str(round(rng.random(),digits)))
                    

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
                for a in actions:
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
        # randomly insert missing data
        self.missingDataProbability = missingDataProbability 
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


class RandomPerformanceGenerator(object):
    """
    Generic wrapper for generating new decision actions or performance tableaux
    with random evaluations generated with a given performance tableau model of type:
    RandomPerformanceTableau, RandomCBPerformanceTableau,
    or Random3ObjectivesPerformanceTableau.

    The return format of generated new set of random actions is schown below.
    This return may be directly feeded to the PerformanceQuantiles.updateQuantiles() method.

    >>> from randomPerfTabs import *
    >>> t = RandomPerformanceTableau(seed=100)
    >>> t
    *------- PerformanceTableau instance description ------*
    Instance class   : RandomPerformanceTableau
    Seed             : 100
    Instance name    : randomperftab
    # Actions        : 13
    # Criteria       : 7
    Attributes       : [
    'randomSeed', 'name', 'BigData', 'sumWeights', 'digits', 'commonScale',
    'commonMode', 'missingDataProbability', 'actions', 'criteria',
    'evaluation', 'weightPreorder']
    >>> rpg = RandomPerformanceGenerator(t,seed= 100)
    >>> newActions = rpg.randomActions(2)
    >>> print(newActions)
    {'actions': OrderedDict([
    ('a14', {'shortName': 'a14',
             'name': 'random decision action',
             'comment': 'RandomPerformanceGenerator'}),
    ('a15', {'shortName': 'a15',
             'name': 'random decision action',
             'comment': 'RandomPerformanceGenerator'})]),
    'evaluation': {
    'g1': {'a14': Decimal('15.17'), 'a15': Decimal('80.87')},
    'g2': {'a14': Decimal('44.51'), 'a15': Decimal('62.74')},
    'g3': {'a14': Decimal('57.87'), 'a15': Decimal('64.24')},
    'g4': {'a14': Decimal('58.0'), 'a15': Decimal('26.99')},
    'g5': {'a14': Decimal('24.22'), 'a15': Decimal('21.18')},
    'g6': {'a14': Decimal('29.1'), 'a15': Decimal('73.09')},
    'g7': {'a14': Decimal('96.58'), 'a15': Decimal('-999')}}}
    >>> newTableau = rpg.randomPerformanceTableau(2)
    >>> newTab.showPerformanceTableau()
    *----  performance tableau -----*
    criteria | weights | 'a17'   'a18'   
    ---------|-----------------------------------------
       'g1'  |   1   |   55.80   22.03  
       'g2'  |   1   |   57.78   33.83  
       'g3'  |   1   |   80.54   31.83  
       'g4'  |   1   |   31.15   69.98  
       'g5'  |   1   |   46.25   48.80  
       'g6'  |   1   |   42.24   82.88  
       'g7'  |   1   |   57.31   41.66  
    
    """
    def __init__(self,argPerfTab,actionNamePrefix='a',\
                 instanceCounter=None,seed=None):
        from randomPerfTabs import _RandomStdPerformanceGenerator,\
                                  _RandomCBPerformanceGenerator,\
                                  _Random3ObjectivesPerformanceGenerator
        from performanceQuantiles import PerformanceQuantiles
        if argPerfTab.__class__ == RandomPerformanceTableau:
            self.__class__ = _RandomStdPerformanceGenerator
            return _RandomStdPerformanceGenerator.__init__(self,argPerfTab,\
                            actionNamePrefix=actionNamePrefix,\
                            instanceCounter=instanceCounter,seed=seed)
        elif argPerfTab.__class__ == RandomCBPerformanceTableau:
            self.__class__ = _RandomCBPerformanceGenerator
            return _RandomCBPerformanceGenerator.__init__(self,argPerfTab,\
                            actionNamePrefix=actionNamePrefix,\
                            instanceCounter=instanceCounter,seed=seed)
        elif argPerfTab.__class__ == Random3ObjectivesPerformanceTableau:
            self.__class__ = _Random3ObjectivesPerformanceGenerator
            return _Random3ObjectivesPerformanceGenerator.__init__(self,argPerfTab,\
                            actionNamePrefix=actionNamePrefix,\
                            instanceCounter=instanceCounter,seed=seed)
        elif argPerfTab.__class__ == PerformanceQuantiles:
            if argPerfTab.perfTabType == 'RandomPerformanceTableau':
                self.__class__ = _RandomStdPerformanceGenerator
                return _RandomStdPerformanceGenerator.__init__(self,argPerfTab,\
                            actionNamePrefix=actionNamePrefix,\
                            instanceCounter=instanceCounter,seed=seed)
            elif argPerfTab.perfTabType == 'RandomCBPerformanceTableau':
                self.__class__ = _RandomCBPerformanceGenerator
                return _RandomCBPerformanceGenerator.__init__(self,argPerfTab,\
                                actionNamePrefix=actionNamePrefix,\
                                instanceCounter=instanceCounter,seed=seed)
            elif argPerfTab.perfTabType == 'Random3ObjectivesPerformanceTableau':
                self.__class__ = _Random3ObjectivesPerformanceGenerator
                return _Random3ObjectivesPerformanceGenerator.__init__(self,argPerfTab,\
                                actionNamePrefix=actionNamePrefix,\
                                instanceCounter=instanceCounter,seed=seed)
            

    def randomActions(self,nbrOfRandomActions=1):
        """
        Generates nbrOfRandomActions.
        """
        from collections import OrderedDict
        criteria = self.perfTab.criteria
        n = self.counter + nbrOfRandomActions
        self.nd = len(str(n))  
        newActions = OrderedDict()
        newEvaluation ={}
        for g in criteria:
            newEvaluation[g] = {}
        for i in range(nbrOfRandomActions):
            newAction = self._randomAction()
            newKey = newAction['action'].pop('key')
            newActions[newKey] = newAction['action']
            for g in criteria:
                newEvaluation[g][newKey] = newAction['evaluation'][g]
        return {'actions': newActions, 'evaluation': newEvaluation}

    def randomPerformanceTableau(self,nbrOfRandomActions=1):
        """
        Generates nbrOfRandomActions.
        """
        from collections import OrderedDict
        from perfTabs import EmptyPerformanceTableau
        from randomPerfTabs import RandomPerformanceTableau,\
             RandomCBPerformanceTableau,\
             Random3ObjectivesPerformanceTableau
        newPerfTab = EmptyPerformanceTableau()
        try:
            if self.perfTab.perfTabType == 'PerformanceQuantiles':
                if self.perfTab.perfTabType != 'RandomPerformanceTableau':
                    newPerfTab.__class__ = RandomPerformanceTableau
                elif self.perfTab.perfTabType != 'RandomCBPerformanceTableau':
                    newPerfTab.__class__ = RandomCBPerformanceTableau
                elif self.perfTab.perfTabType != 'Random3ObjectivesPerformanceTableau':
                    newPerfTab.__class__ = Random3ObjectivesPerformanceTableau
                else:
                    print('Error')
                    return None
        except:
            newPerfTab.__class__ = self.perfTab.__class__
        newPerfTab.name = self.perfTab.name
        try:
            newPerfTab.objectives = self.perfTab.objectives
        except:
            newPerfTab.objectives = OrderedDict()
        criteria = self.perfTab.criteria 
        newPerfTab.criteria = criteria
        newActions = OrderedDict()
        newEvaluation ={}
        for g in criteria:
            newEvaluation[g] = {}
        n = self.counter + nbrOfRandomActions
        self.nd = len(str(n))
        for i in range(nbrOfRandomActions):
            newAction = self._randomAction()
            newKey = newAction['action'].pop('key')
            newActions[newKey] = newAction['action']
            for g in criteria:
                newEvaluation[g][newKey] = newAction['evaluation'][g]
        newPerfTab.actions = newActions
        newPerfTab.evaluation = newEvaluation
        return newPerfTab


class _RandomStdPerformanceGenerator(RandomPerformanceGenerator):
    """
    Generator for genrating new decision actions from a
    given <RandomPerformanceTableau> model.
    """
    def __init__(self,argPerfTab,actionNamePrefix='a',
                 instanceCounter=0,seed=None):
        """
        Set the initial state of the random generator.
        """
        import random
        random.seed(seed)

        self.random = random
        self.perfTab = argPerfTab
        self.actionNamePrefix = actionNamePrefix
        if instanceCounter == None:
            self.counter = len(argPerfTab.actions)
        else:
            self.counter = instanceCounter
        self.nd = len(str(self.counter))

        self.commonMode = argPerfTab.commonMode
        if str(self.commonMode[0]) == 'triangular':
            from randomNumbers import ExtendedTriangularRandomVariable as RNGTr
            rdseed = random.random()
            self.rng = RNGTr(m,M,xm,r,seed=rdseed)
            
        self.commonScale = argPerfTab.commonScale

      
    def _randomAction(self,Debug=False):
        """
        Returns
        ``{'action': key, 'evaluation': {'g1': Decimal(...), 'g2': Decimal(...), ... }}``
        """
        # generate action key
        self.counter += 1
        actionKey = ('%s%%0%dd' % (self.actionNamePrefix,self.nd)) % (self.counter)
        action = {'shortName':actionKey,
                        'name': 'random decision action',
                        'comment': 'RandomPerformanceGenerator',
                        #'type': actionType,
                        'key': actionKey}

        # generate random evaluation

        random = self.random
        commonMode = self.commonMode
        commonScale = self.commonScale
        digits = self.perfTab.digits
        criteria = self.perfTab.criteria

        evaluation = {}
        
        if str(commonMode[0]) == 'uniform':          
            for g in criteria:
                evaluation[g] = {}
                randeval = random.uniform(commonScale[0],commonScale[1])
                evaluation[g] = Decimal(str(round(randeval,digits)))
                    
        elif str(self.commonMode[0]) == 'triangular':
            for g in criteria:
                evaluation[g] = Decimal(str(round(rng.random(),digits)))
                    
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
                u = random.betavariate(alpha,beta)
                randeval = (u * (M-m)) + m
                evaluation[g] = Decimal(str(round(randeval,digits)))

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
                notfound = True 
                while notfound:
                    randeval = random.normalvariate(mu,sigma)
                    if randeval >= commonScale[0] and  randeval <= commonScale[1]:
                        notfound = False
                evaluation[g] = Decimal(str(round(randeval,digits)))

        # randomly insert missing data
        missingDataProbability = self.perfTab.missingDataProbability
        for c in criteria:
            if random.random() < missingDataProbability:
                evaluation[c] = Decimal('-999')

        # return a new random decision alternative
        return {'action': action,'evaluation':evaluation}

##    def randomUpdate(self,nbrOfRandomActions=1):
##        """
##        Updates *self.perfTab* with *n* = *nbrOfActions* new random decision alternatives.
##
##        .. note::
##
##            The update will modify the generator's given performance tableau instance by,
##            either adding new actions with their random evaluations,
##            or updating the performances of already existing decision actions.
##        """
##        actions = self.perfTab.actions
##        criteria = self.perfTab.criteria
##        evaluation = self.perfTab.evaluation
##        for i in range(nbrOfRandomActions):
##            newAction = self._randomAction()
##            newEvaluation = newAction['evaluation']
##            newKey = newAction['action']['key']
##            actions[newKey] = newAction['action']
##            for g in criteria:
##                evaluation[g][newKey] = newEvaluation[g]
                
##################
#-----------------
class RandomAcademicPerformanceTableau(PerformanceTableau):
    """
    Specialization of the PerformanceTableau class for generating a temporary
    academic performance tableau with random grading results performances
    of a number of students in different academic courses (see Lecture 4: Grading
    of the Algorithmic decision Theory Course http://hdl.handle.net/10993/37933 )
    
    *Parameters*:
        * number of students,
        * number of courses,
        * weightDistribution := equisignificant | random (default, see RandomPerformanceTableau)
        * weightScale := (1, 1 | numberOfCourses (default when random))
        * IntegerWeights := Boolean (True = default)
        * commonScale := (0,20) (default)
        * ndigits := 0
        * WithTypes := Boolean (False = default)
        * commonMode := ('triangular',xm=14,r=0.25)
        * commonThresholds (default) := {
            | 'ind':(0,0),
            | 'pref':(1,0),
            | } (default)
        
    When parameter *WithTypes* is set to *True*, the students are randomly allocated
    to one of the four categories: *weak* (1/6), *fair* (1/3), *good* (1/3),
    and *excellent* (1/3), in the bracketed proportions.
    In a default 0-20 grading range, the random range of a weak student is 0-10,
    of a fair student 4-16, of a good student 8-20, and of an excellent student 12-20.
    The random grading generator follows a double triangular probablity law
    with *mode* equal to the middle of the random range and *median repartition* of
    probability each side of the mode.

    >>> from randomPerfTabs import RandomAcademicPerformanceTableau
    >>> t = RandomAcademicPerformanceTableau(numberOfStudents=7,
    ...              numberOfCourses=5, missingDataProbability=0.03,
    ...              WithTypes=True, seed=100)
    >>> t
     *------- PerformanceTableau instance description ------*
     Instance class   : RandomAcademicPerformanceTableau
     Seed             : 100
     Instance name    : randstudPerf
     # Actions        : 7
     # Criteria       : 5
     Attributes       : ['randomSeed', 'name', 'actions',
                         'criteria', 'evaluation', 'weightPreorder']
    >>> t.showPerformanceTableau()
     *----  performance tableau -----*
      Courses |  'g1' 'g2' 'g3' 'g4' 'g5' 
        ECTS  |   5    1    5    4    3   
     ---------|--------------------------
        's1f' |  12   10   14   14   13  
        's2g' |  14   12   16   12   14  
        's3g' |  13   10   NA   12   17  
        's4f' |  10   13   NA   13   12  
        's5e' |  17   12   16   17   12  
        's6g' |  17   17   12   16   14  
        's7e' |  12   13   13   16   NA  
    >>> t.weightPreorder
     [['g2'], ['g5'], ['g4'], ['g1', 'g3']]

    The random instance generated here with seed = 100 results in a set of only
    excellent (2), good (3) and fair (2) student performances. We observe 3 missing grades (NA).
    We may show a statistical summary per course (performance criterion) with more than 5 grades.
    
    >>> t.showStatistics()
     *-------- Performance tableau summary statistics -------*
     Instance name      : randstudPerf
     #Actions           : 7
     #Criteria          : 5
     *Statistics per Criterion*
     Criterion name       : g1
     Criterion weight     : 5
      criterion scale      : 0.00 - 20.00
      # missing evaluations : 0
      mean evaluation       : 13.57
      standard deviation    : 2.44
      maximal evaluation    : 17.00
      quantile Q3 (x_75)    : 17.00
      median evaluation     : 13.50
      quantile Q1 (x_25)    : 12.00
      minimal evaluation    : 10.00
      mean absolute difference      : 2.69
      standard difference deviation : 3.45
     Criterion name       : g2
     Criterion weight     : 1
      criterion scale      : 0.00 - 20.00
      # missing evaluations : 0
      mean evaluation       : 12.43
      standard deviation    : 2.19
      maximal evaluation    : 17.00
      quantile Q3 (x_75)    : 14.00
      median evaluation     : 12.50
      quantile Q1 (x_25)    : 11.50
      minimal evaluation    : 10.00
      mean absolute difference      : 2.29
      standard difference deviation : 3.10
     Criterion name       : g3
     Criterion weight     : 5
      criterion scale      : 0.00 - 20.00
      # missing evaluations : 2
     Criterion name       : g4
     Criterion weight     : 4
      criterion scale      : 0.00 - 20.00
      # missing evaluations : 0
      mean evaluation       : 14.29
      standard deviation    : 1.91
      maximal evaluation    : 17.00
      quantile Q3 (x_75)    : 16.25
      median evaluation     : 15.00
      quantile Q1 (x_25)    : 12.75
      minimal evaluation    : 12.00
      mean absolute difference      : 2.12
      standard difference deviation : 2.70
     Criterion name       : g5
     Criterion weight     : 3
      criterion scale      : 0.00 - 20.00
      # missing evaluations : 1
      mean evaluation       : 13.67
      standard deviation    : 1.70
      maximal evaluation    : 17.00
      quantile Q3 (x_75)    : 15.50
      median evaluation     : 14.00
      quantile Q1 (x_25)    : 12.50
      minimal evaluation    : 12.00
      mean absolute difference      : 1.78
      standard difference deviation : 2.40

    """
    def __init__(self,numberOfStudents = 10, numberOfCourses = 5,\
                 weightDistribution = 'random', weightScale = (1,5),\
                 commonScale = (0,20), ndigits = 0,\
                 WithTypes = False,\
                 commonMode = ('triangular',12,0.25),\
                 commonThresholds = None, IntegerWeights = True,\
                 BigData = False, missingDataProbability = 0.0,\
                 seed = None,\
                 Debug = False):
        """
        """
        # didactic
        if WithTypes:
            types = ['weak','fair','fair','good','good','excellent']
            nt = len(types)
        # set random seed
        self.randomSeed = seed
        import random
        random.seed(seed)

        # set name
        self.name = 'randstudPerf'

        # generate actions
        numberOfActions = numberOfStudents
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            if WithTypes:
                ri = random.randint(0,nt-1)
            if BigData:
                actionName = ('s%%0%dd' % (nd)) % (i+1)
                actions[i] = {'name': actionName}
                if WithTypes:
                    actions[i]['type'] = types[ri]
                    actions[i]['name'] = '%s%s' % (actions[i]['name'],(actions[i]['type'])[0])
                
            else:   
                actionKey = ('s%%0%dd' % (nd)) % (i+1)
                if WithTypes:
                    actions[actionKey]= {'type': types[ri],
                        'shortName': '%s%s' % (actionKey,types[ri][0]),
                        'name': 'student %s%s' % (actionKey,types[ri][0]),
                        'comment': 'RandomAcademicPerformanceTableau() generated.'}
                else:
                    actions[actionKey] = {'shortName':actionKey,
                        'name': 'student %s' % actionKey,
                        'comment': 'RandomAcademicPerformanceTableau() generated.' }
            
        # generate the criteria weights
        numberOfCriteria = numberOfCourses 
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for i in range(numberOfCriteria):
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightScale = (1,1)
            weightsList = [Decimal(str(weightScale[0])) for i in range(numberOfCriteria)]
            sumWeights = sum(weightsList)
        else:
            print('!!! Error: wrong course weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary
        ngd = len(str(numberOfCriteria))
        criteria = OrderedDict()
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; IntegerWeights='+str(IntegerWeights)
        commentString += '; commonThresholds='+str(commonThresholds)
        commentString += '; missingDataProbability='+str(missingDataProbability)
        commentString += '; WithTypes=='+str(WithTypes)

    
        for i in range(numberOfCriteria):
            g = ('g%%0%dd' % ngd) % (i+1)
            criteria[g] = {}
            criteria[g]['name']='RandomAcademicPerformanceTableau() instance'
            criteria[g]['comment']=commentString
            try:
                indThreshold  =(Decimal(str(commonThresholds['ind'][0])),
                                Decimal(str(commonThresholds['ind'][1])))
                prefThreshold =(Decimal(str(commonThresholds['pref'][0])),
                                Decimal(str(commonThresholds['pref'][1])))
                
##                vetoThreshold =(Decimal(str(commonThresholds['veto'][0])),
##                                Decimal(str(commonThresholds['veto'][1])))
             
                criteria[g]['thresholds'] = {'ind':indThreshold,
                                             'pref':prefThreshold}
##                                             'veto':vetoThreshold}
            except:
                indThreshold  = ( Decimal("0"), Decimal("0") )
                prefThreshold = ( Decimal("1"), Decimal("0") )
#                vetoThreshold = ( Decimal(str(numberOfActions)), Decimal("0") )               
                criteria[g]['thresholds'] = { 'ind':indThreshold,\
                                              'pref':prefThreshold,
 #                                             'veto': vetoThreshold
                                              }
            criteria[g]['scale'] = commonScale
            criteria[g]['preferenceDirection'] = 'max'
                                             
            if IntegerWeights:
                criteria[g]['weight'] = weightsList[i]
            else:
                criteria[g]['weight'] = weightsList[i]/sumWeights
                
        # generate evaluations
        digits = ndigits
        evaluation = {}
        # evaluation ranges for student types
        if WithTypes:
            randEvalRanges = {'weak':(commonScale[0],commonScale[1]*0.5),
                    'fair':(commonScale[0]+commonScale[1]*0.2,commonScale[1]*0.8),
                    'good':(commonScale[0]+commonScale[1]*0.4,commonScale[1]),
                    'excellent':(commonScale[0]+commonScale[1]*0.6,commonScale[1])}
        # install the triangular RNG if necessary
        if str(commonMode[0]) == 'triangular':
            from randomNumbers import ExtendedTriangularRandomVariable as RNGTr
        # generate all individual random evaluations
        for g in criteria:
            evaluation[g] = {}       
            for x in actions:
                if WithTypes:
                    rangex = randEvalRanges[actions[x]['type']]
                    if Debug:
                        print(actions[x],rangex)
                #--------
                if str(commonMode[0]) == 'uniform':              
                    if WithTypes:
                        randeval = random.uniform(rangex[0],rangex[1])
                    else:
                        randeval = random.uniform(commonScale[0],commonScale[1])
                    evaluation[g][x] = Decimal(str(round(randeval,digits)))
                # ---------        
                elif str(commonMode[0]) == 'triangular':
                    #from randomNumbers import ExtendedTriangularRandomVariable as RNGTr
                    if WithTypes:
                        rdseed = random.random()
                        rng = RNGTr(rangex[0],rangex[1],min(rangex[1],\
                                    commonMode[1]),commonMode[2],seed=rdseed)
                    else:
                        rdseed = random.random()
                        rng = RNGTr(commonScale[0],commonScale[1],\
                                    commonMode[1],commonMode[2],seed=rdseed)    
                    evaluation[g][x] = Decimal(str(round(rng.random(),digits)))
                #-------------------       
                elif str(commonMode[0]) == 'beta':
                    if WithTypes:
                        m = rangex[0]
                        M = rangex[1]
                    else:
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
                    u = random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    evaluation[g][x] = Decimal(str(round(randeval,digits)))

        # randomly insert missing data
        # self.missingDataProbability = missingDataProbability
        for c in criteria:
            for x in actions:
                if random.random() < missingDataProbability:
                    evaluation[c][x] = Decimal('-999')

        # install object items
        self.actions = actions
        self.criteria = criteria
        self.evaluation = evaluation
        self.weightPreorder = self.computeWeightPreorder()

    def showPerformanceTableau(self,Transposed=False,studentsSubset=None,\
                               fromIndex=None,toIndex=None,Sorted=True,ndigits=0):
        """
        Print the performance Tableau.
        """
        from decimal import Decimal
        print('*----  performance tableau -----*')
        criteriaList = list(self.criteria)
        if Sorted:
            criteriaList.sort()
        if studentsSubset == None:
            actionsList = list(self.actions)
            if Sorted:
                actionsList.sort()
        else:
            actionsList = list(studentsSubset)
        if fromIndex == None:
            fromIndex = 0
        if toIndex == None:
            toIndex=len(actionsList)
        # view criteria x actions
        if Transposed:
            print(' Courses | ETCS |', end=' ')
            for x in actionsList:
                xName = self.actions[x]['shortName']
                print('\''+xName+'\'', end=' ')
            print('\n---------|-----------------------------------------')
            formatString = ' %%0%d.%df ' % (2,ndigits)
            for g in criteriaList:
                print('  \'' +str(g)+'\'  |  '+str(self.criteria[g]['weight'])+'   |', end='  ')
                for i in range(fromIndex,toIndex):
                    x = actionsList[i]
                    evalgx = self.evaluation[g][x]
                    if evalgx == Decimal('-999'):
                        print(' NA ', end='  ')
                    else:                    
                        print(formatString % (evalgx), end='  ')
                print()
        # view actions x criteria
        else:
            print(' Courses | ', end=' ')
            for g in criteriaList:
                print('\''+str(g)+'\'', end=' ')
            print('\n   ECTS  | ', end='  ')
            for g in criteriaList:
                print(' %s  ' % str(self.criteria[g]['weight'] ), end='  ')          
            print('\n---------|-----------------------------------------')
            formatString = ' %%0%d.%df ' % (2,ndigits)
            for i in range(fromIndex,toIndex):
                x = actionsList[i]
                print('  \''+str(self.actions[x]['shortName'])+'\' |' , end='   ')
                for g in criteriaList:
                    evalgx = self.evaluation[g][x]
                    if evalgx == Decimal('-999'):
                        print(' NA ', end='  ')
                    else:                    
                        print(formatString % (evalgx), end='  ')
                print()


    def showHTMLPerformanceTableau(self,studentsSubset=None,isSorted=True,\
                                   Transposed=False,ndigits=0,\
                                   ContentCentered=True,title=None):
        """
        shows the html version of the academic performance tableau in a browser window.
        """
        import webbrowser
        fileName = '/tmp/performanceTable.html'
        fo = open(fileName,'w')
        fo.write(self._htmlPerformanceTable(actions=studentsSubset,isSorted=isSorted,\
                                           Transposed=Transposed,\
                                           ndigits=ndigits,
                                           ContentCentered=ContentCentered,
                                           title=title))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
           
            
    def _htmlPerformanceTable(self,actions=None,isSorted=False,\
                             Transposed=False,ndigits=0,\
                             ContentCentered=True,
                             title=None):
        """
        Renders the performance table citerion x actions in html format.
        """
        criteria = self.criteria
        minMaxEvaluations = self.computeMinMaxEvaluations()
        if title == None:
            html = '<h1>Random Student Gradings</h1>'
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
            html += '<tr bgcolor="#9acd32"><th>Courses<br/>(ECTS)</th>'
            for x in actionsKeys:
                try:
                    xName = actions[x]['shortName']
                except:
                    xName = str(x)
                html += '<th bgcolor="#FFF79B">%s</th>' % (xName)
            html += '</tr>'
            for g in criteriaKeys:
                try:
                    gName = '%s (%d)' % (criteria[g]['shortName'],criteria[g]['weight'])
                except:
                    gName = '%s (%d)' % (g,int(criteria[g]['weight']))
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (gName)
                for x in actionsKeys:
                    if self.evaluation[g][x] != Decimal("-999"):
                        if self.evaluation[g][x] < Decimal('10'):
                            formatString = '<td bgcolor="#ffddff"  align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        elif minMaxEvaluations[g]['minimum'] == minMaxEvaluations[g]['maximum']:
                            formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
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
            html += '<tr bgcolor="#9acd32"><th>Courses</th>'
            for g in criteriaKeys:
                try:
                    gName = criteria[g]['shortName']
                except:
                    gName = str(g)
                html += '<th bgcolor="#FFF79B">%s</th>' % (gName)
            html += '</tr>'
            html += '<tr><th bgcolor="#9acd32" >ECTS</th>'
            for g in criteriaKeys:
                gweight = criteria[g]['weight']
                html += '<td  align="center" bgcolor="#FFF79B" ><i>%d</i></td>' % (int(gweight))
            html += '</tr>'
            for x in actionsKeys:
                try:
                    xName = actions[x]['shortName']
                except:
                    xName = str(x)
                html += '<tr><th bgcolor="#FFF79B">%s</th>' % (xName)
                for g in criteriaKeys:
                    if self.evaluation[g][x] != Decimal("-999"):
                        if self.evaluation[g][x] < Decimal('10'):
                            formatString = '<td bgcolor="#ffddff"  align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        elif minMaxEvaluations[g]['minimum'] == minMaxEvaluations[g]['maximum']:
                            formatString = '<td align="%s">%% .%df</td>' % (alignFormat,ndigits)
                            html += formatString % (evaluation[g][x])
                        #elif self.evaluation[g][x] == minMaxEvaluations[g]['minimum']:
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
                                            
    
#-----------------
class RandomRankPerformanceTableau(PerformanceTableau):
    """
    Specialization of the PerformanceTableau class for generating a temporary
    random performance tableau with multiple criteria ranked (without ties)
    performances of a given number of decision actions.
    On each criterion, all decision actions are hence lineraly ordered.
    The :py:class:`randomPerfTabs.RandomRankPerformanceTableau` class
    is matching the :py:class:`votingDigraphs.RandomLinearVotingProfiles`
    class (see http://hdl.handle.net/10993/37933 Lecture 2 : Voting of
    the Algorithmic Decision Theory Course)
        
    *Parameters*:
        * number of actions,
        * number of performance criteria,
        * weightDistribution := equisignificant | random (default, see RandomPerformanceTableau)
        * weightScale := (1, 1 | numberOfCriteria (default when random))
        * IntegerWeights := Boolean (True = default). Weights are negative, as all the criteria preference directions are 'min', as the rank performance is to be minimized. 
        * commonThresholds (default) := {
            | 'ind':(0,0),
            | 'pref':(1,0),
            | 'veto':(numberOfActions,0)
            | } (default)

    >>> t = RandomRankPerformanceTableau(numberOfActions=3,numberOfCriteria=2)
    >>> t.showObjectives()
    The performance tableau does not contain objectives.
    >>> t.showCriteria()
    *----  criteria -----*
    g1 'Random criteria (voter)'
      Scale = (Decimal('0'), Decimal('3'))
      Weight = -1 # ranks to be minimal 
      Threshold ind : 0.00 + 0.00x ; percentile:  0.0
      Threshold pref : 1.00 + 0.00x ; percentile:  0.667
      Threshold veto : 3.00 + 0.00x ; percentile:  1.0
    g2 'Random criteria (voter)'
      Scale = (Decimal('0'), Decimal('3'))
      Weight = -1 # ranks to be minimal
      Threshold ind : 0.00 + 0.00x ; percentile:  0.0
      Threshold pref : 1.00 + 0.00x ; percentile:  0.667
      Threshold veto : 3.00 + 0.00x ; percentile:  1.0
    >>> t.showActions()
    *----- show decision action --------------*
    key:  a1
      short name: a1
      name:       random decision action (candidate)
      comment:    RandomRankPerformanceTableau() generated.
    key:  a2
      short name: a2
      name:       random decision action (candidate)
      comment:    RandomRankPerformanceTableau() generated.
    key:  a3
      short name: a3
      name:       random decision action (candidate)
      comment:    RandomRankPerformanceTableau() generated.
    >>> t.showPerformanceTableau()
    *----  performance tableau -----*
    criteria | weights | 'a1' 'a2' 'a3'   
    ---------|--------------------------
       'g1'  |    -1   |   3    1    2  
       'g2'  |    -1   |   2    1    3  

    """
    def __init__(self,numberOfActions = 13, numberOfCriteria = 7,\
                 weightDistribution = 'equisignificant', weightScale=None,\
                 commonThresholds = None, IntegerWeights=True,\
                 BigData=False,\
                 seed = None,\
                 Debug = False):
        """
        Constructor of random ranks performance tableaux. 
        """

        # set random seed
        self.randomSeed = seed
        import random
        random.seed(seed)

        # set name
        self.name = 'randrankperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            if BigData:
                actionName = ('a%%0%dd' % (nd)) % (i+1)
                actions[i] = {'name': actionName}
            else:   
                actionKey = ('a%%0%dd' % (nd)) % (i+1)
                actions[actionKey] = {'shortName':actionKey,
                        'name': 'random decision actions (candidate)',
                        'comment': 'Random Ranks' }
        # generate the criteria weights
        if weightScale == None:
            weightScale = (1,numberOfCriteria)
        if weightDistribution == 'random':
            weightsList = []
            sumWeights = Decimal('0.0')
            i = 0
            for i in range(numberOfCriteria):
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'equisignificant':
            weightScale = (1,1)
            weightsList = [Decimal(str(weightScale[0])) for i in range(numberOfCriteria)]
            sumWeights = sum(weightsList)
        else:
            print('!!! Error: wrong criteria weight distribution mode: %s !!!!' % (weightDistribution))

        # generate criteria dictionary
        ngd = len(str(numberOfCriteria))
        criteria = OrderedDict()
        commentString = 'Arguments: '
        commentString += '; weightDistribution='+str(weightDistribution)
        commentString += '; weightScale='+str(weightScale)
        commentString += '; IntegerWeights='+str(IntegerWeights)
        commentString += '; commonThresholds='+str(commonThresholds)
    
        for i in range(numberOfCriteria):
            g = ('g%%0%dd' % ngd) % (i+1)
            criteria[g] = {}
            criteria[g]['name']='Random criteria (voter)'
            criteria[g]['comment']=commentString
            criteria[g]['preferenceDirection'] = 'min'
            try:
                indThreshold  =(Decimal(str(commonThresholds['ind'][0])),
                                Decimal(str(commonThresholds['ind'][1])))
                prefThreshold =(Decimal(str(commonThresholds['pref'][0])),
                                Decimal(str(commonThresholds['pref'][1])))
                vetoThreshold =(Decimal(str(commonThresholds['veto'][0])),
                                Decimal(str(commonThresholds['veto'][1])))
             
                criteria[g]['thresholds'] = {'ind':indThreshold,
                                             'pref':prefThreshold,
                                             'veto':vetoThreshold}
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
            # weights are negative
            if IntegerWeights:
                criteria[g]['weight'] = -weightsList[i]
            else:
                criteria[g]['weight'] = -weightsList[i]/sumWeights
                
        # generate evaluations
        evaluation = {}       
        for g in criteria:
            evaluation[g] = {}
            choiceRange = list(range(1,numberOfActions+1))
            for a in actions:
                randeval = random.choice(choiceRange)
                evaluation[g][a] = Decimal( str(randeval) )
                choiceRange.remove(randeval)

        # install object items
        self.actions = actions
        self.criteria = criteria
        self.evaluation = evaluation
        self.sumWeights = sumWeights
        self.weightPreorder = self.computeWeightPreorder()

# ------------------------------


class _FullRandomPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of random performance tableaux
    """

    def __init__(self,numberOfActions = None,
                 numberOfCriteria = None,
                 weightDistribution = None,
                 weightScale=None,
                 IntegerWeights = True,
                 commonScale = None,
                 commonThresholds = None,
                 commonMode = None,
                 valueDigits=2,
                 seed = None,
                 Debug = False):
        # import OrderedDict container
        from collections import OrderedDict
        # set name
        self.name = 'fullrandomperftab'

        # set random seaad
        self.randomSeed = seed
        import random
        random.seed(seed)

        # generate random actions
        if numberOfActions == None:
            numberOfActions = random.randint(7,30)
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            actions[actionKey] = {'shortName':actionKey,
                    'name': 'random decision action',
                    'comment': 'RandomRankPerformanceTableau() generated.' }
        self.actions = actions
        actionsList = [x for x in actions.keys()]

        # generate criterialist
        if numberOfCriteria == None:
            numberOfCriteria = random.randint(5,21)
            
        ng = len(str(numberOfCriteria))
        criteriaList = [('g%%0%dd' % ng) % (i+1)\
                        for i in range(numberOfCriteria)]               
        criteriaList.sort()

        # generate random weights
        if weightDistribution == None:
            majorityWeight = numberOfCriteria + 1
            weightModesList = [('fixed',[1,1],1),
                               ('random',[1,3],2),
                               ('random',[1,numberOfCriteria],3)]
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
            for i in range(len(criteriaList)):
                g = criteriaList[i]
                weightsList.append(random.randint(weightScale[0],weightScale[1]))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = 0.0
            for i in range(len(criteriaList)):
                if i == 0:
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
            for i in range(len(criteriaList)):
                if i == 0:
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
        criteria = OrderedDict()
        for i in range(len(criteriaList)):
            g = criteriaList[i]
            criteria[g] = {}
            criteria[g]['name'] = 'random criterion'
            #t = time.time()
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
            if IntegerWeights:
                criteria[g]['weight'] = Decimal(str(weightsList[i]))
            else:
                criteria[g]['weight'] = Decimal(str(weightsList[i]))/Decimal(str(sumWeights))

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
        for i in range(len(criteriaList)):
            g = criteriaList[i]
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
                from randomNumbers import ExtendedTriangularRandomVariable as RNG
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
                rdseed = random.random()
                rng = RNG(m,M,xm,r,seed=rdseed)
                for a in actionsList:
##                    u = random.random()
##                    if u < r:
##                        randeval = m + math.sqrt(u/r)*(xm-m)                
##                    else:
##                        randeval = M - math.sqrt((1-u)/(1-r))*(M-xm)
##                    evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    evaluation[g][a] = Decimal(str(round(rng.random(),digits)))

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
    Full automatic generation of performance tableaux with random coalitions of criteria

    Parameters:
        | numberOf Actions := 20 (default)
        | number of Criteria := 13 (default)
        | weightDistribution := 'equisignificant' (default with all weights = 1.0), 'random', 'fixed' (default w_1 = numberOfCriteria-1, w_{i!=1} = 1
        | weightScale := [1,numerOfCriteria] (random default), [w_1, w_{i!=1] (fixed)
        | IntegerWeights := True (default) / False
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

    def __init__(self,numberOfActions = None, numberOfCriteria = None,\
                 weightDistribution = None, weightScale=None,\
                 IntegerWeights = True, commonScale = None,\
                 commonThresholds = None, commonMode = None,\
                 valueDigits=2, Coalitions=True, VariableGenerators=True,\
                 OrdinalScales=False, Debug=False, RandomCoalitions=False,\
                 vetoProbability=None,\
                 BigData=False,\
                 seed= None,\
                 Electre3=True):
        
        # naming
        self.name = 'randomCoalitionsPerfTab'
        # randomizer init
        self.randomSeed = seed
        import random
        random.seed(seed)
        if RandomCoalitions:
            Coalitions=False

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            
        from collections import OrderedDict
            
        # generate actions
        if numberOfActions == None:
            numberOfActions = 13
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(numberOfActions):
            actionKey = ('a%%0%dd' % (nd)) % (i+1)
            if BigData:
                actions[i] = {'shortName':actionKey,
                              'name': actionKey,
                              'generators': {}}
            else:   
                actions[actionKey] = {'shortName':actionKey,
                        'name': 'random decision action',
                        'comment': 'RandomCoalitionsPerformanceTableau() generated.',
                        'generators': {}}
        self.actions = actions
        actionsList = [x for x in actions.keys()]
        #actionsList.sort()
        
        # generate criterialist
        if numberOfCriteria == None:
            numberOfCriteria = 7
        ng = len(str(numberOfCriteria))
        criteriaList = [('g%%0%dd' % ng) % (i+1)\
                        for i in range(numberOfCriteria)]
        #criteriaList.sort()
        
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
            for i in range(len(criteriaList)):               
                weightsList.append(Decimal(str(random.randint(weightScale[0],
                                                              weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            if weightScale == None:
                weightScale = (1,numberOfCriteria)            
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(len(criteriaList)):
                if i == 0:
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
            for i in range(len(criteriaList)):
                if i == 0:
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
            if IntegerWeights:
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

class Random3ObjectivesPerformanceTableau(PerformanceTableau):
    """
    Specialization of the :py:class:`perfTabs.PerformanceTableau` class 
    for 3 objectives: *Eco*, *Soc* and *Env*. Each decision action
    is qualified randomly as weak (-), fair (~) or good (+)
    on each of the three objectives.
    
    Generator arguments:
        * numberOf Actions := 20 (default)
        * shortNamePrefix := 'a' (default)
        * number of Criteria := 13 (default)
        * weightDistribution := 'equiobjectives' (default)
                              | 'equisignificant' (weights set all to 1)
                              | 'random' (in the range 1 to numberOfCriteria)
        * weightScale := [1,numerOfCriteria] (random default)
        * IntegerWeights := True (default) / False
        * OrdinalScales := True / False (default), if True commonScale is set to (0,10)
        * NegativeWeights := True (default) / False. If False, evaluations to be minimized are negative.
        * negativeWeightProbability := [0,1] (default 0.10), 'min' preference direction probability  
        * commonScale := (Min, Max)
                | when common Scale = False, (0.0,10.0) by default if OrdinalScales == True and CommonScale=None,
                | and (0.0,100.0) by default otherwise 
        * commonThresholds := ((Ind,Ind_slope),(Pref,Pref_slope),(Veto,Veto_slope)) with
                | Ind < Pref < Veto in [0.0,100.0] such that 
                | (Ind/100.0*span + Ind_slope*x) < (Pref/100.0*span + Pref_slope*x) < (Pref/100.0*span + Pref_slope*x)
                | By default [(0.05*span,0.0),(0.10*span,0.0),(0.60*span,0.0)] if OrdinalScales=False
                | By default [(0.1*span,0.0),(0.2*span,0.0),(0.8*span,0.0)] otherwise
                | with span = commonScale[1] - commonScale[0].
        * commonMode := ['triangular','variable',0.50] (default), A constant mode may be provided.
                | ['uniform','variable',None], a constant range may be provided.
                | ['beta','variable',None] (three alpha, beta combinations:
                | (5.8661,2.62203),(5.05556,5.05556) and (2.62203, 5.8661)
                | chosen by default for 'good', 'fair' and 'weak' evaluations. 
                | Constant parameters may be provided.
        * valueDigits := 2 (default, for cardinal scales only)
        * vetoProbability := x in ]0.0-1.0[ (0.5 default), probability that a cardinal criterion shows a veto preference discrimination threshold.
        * Debug := True / False (default)

    .. warning::

        Minimal number required of criteria is 3!

    >>> from randomPerfTabs import Random3ObjectivesPerformanceTableau
    >>> t = Random3ObjectivesPerformanceTableau(numberOfActions=5,numberOfCriteria=3,seed=1)
    >>> t
    *------- PerformanceTableau instance description ------*
    Instance class   : Random3ObjectivesPerformanceTableau
    Seed             : 1
    Instance name    : random3ObjectivesPerfTab
    # Actions        : 5
    # Objectives     : 3
    # Criteria       : 3
    Attributes       : ['name', 'valueDigits', 'BigData', 'OrdinalScales',
                        'missingDataProbability', 'negativeWeightProbability',
                        'randomSeed', 'sumWeights', 'valuationPrecision',
                        'commonScale', 'objectiveSupportingTypes',
                        'actions', 'objectives', 'criteriaWeightMode',
                        'criteria', 'evaluation', 'weightPreorder']
    >>> t.showObjectives()
    *------ show objectives -------"
    Eco: Economical aspect
       g1 criterion of objective Eco 1
      Total weight: 1.00 (1 criteria)
    Soc: Societal aspect
       g2 criterion of objective Soc 1
      Total weight: 1.00 (1 criteria)
    Env: Environmental aspect
       g3 criterion of objective Env 1
      Total weight: 1.00 (1 criteria)
    >>> t.showActions()
    *----- show decision action --------------*
    key:  a1
      short name:  a1
      name:       random decision action Eco+ Soc- Env+
      profile:    {'Eco': 'good', 'Soc': 'weak', 'Env': 'good'}
    key:  a2
      short name:  a2
      name:       random decision action Eco~ Soc+ Env~
      profile:    {'Eco': 'fair', 'Soc': 'good', 'Env': 'fair'}
    key:  a3
      short name:  a3
      name:       random decision action Eco~ Soc~ Env-
      profile:    {'Eco': 'fair', 'Soc': 'fair', 'Env': 'weak'}
    key:  a4
      short name:  a4
      name:       random decision action Eco~ Soc+ Env+
      profile:    {'Eco': 'fair', 'Soc': 'good', 'Env': 'good'}
    key:  a5
      short name:  a5
      name:       random decision action Eco~ Soc+ Env~
      profile:    {'Eco': 'fair', 'Soc': 'good', 'Env': 'fair'}
    >>> t.showPerformanceTableau()
    *----  performance tableau -----*
    criteria | weights |  'a1'   'a2'   'a3'   'a4'   'a5'   
    ---------|---------------------------------------------
    'g1Eco'  |    1    | 36.29  85.17  34.49    NA   56.58  
    'g2Soc'  |    1    | 55.00  56.33    NA   67.36  72.22  
    'g3Env'  |    1    | 66.58  48.71  21.59    NA     NA  
    >>>
        
    """

    def __init__(self,numberOfActions=20,shortNamePrefix='a',numberOfCriteria=13,\
                 weightDistribution='equiobjectives',weightScale=None,\
                 IntegerWeights=True,OrdinalScales=False,\
                 NegativeWeights=False,negativeWeightProbability=0.0,\
                 commonScale=None,commonThresholds=None,commonMode=None,\
                 valueDigits=2,\
                 vetoProbability=0.5,\
                 missingDataProbability = 0.05,\
                 BigData=False,\
                 seed=None,\
                 Debug=False):
        
        # naming
        self.name = 'random3ObjectivesPerfTab'
        self.valueDigits = valueDigits
        self.BigData = BigData
        self.OrdinalScales = OrdinalScales
        self.missingDataProbability = missingDataProbability
        self.negativeWeightProbability = negativeWeightProbability
        # randomizer init
        self.randomSeed = seed
        from random import Random
        _random = Random(seed)
        _random1 = Random(seed)
        _random2 = Random(seed)

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            

            
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1, numberOfActions+1):
            actionKey = shortNamePrefix+('%%0%dd' % (nd)) % (i)
            if BigData:
                actions[i] = {'name': actionKey,'generators': {}}
            else:      
                actions[actionKey] = {'shortName': '%s' % (actionKey),
                        'name': 'action %s' % actionKey,
                        'comment': '3 Objectives',
                        'generators': {}}
##        self.actions = actions
##        actionsList = [x for x in self.actions]
##        actionsList.sort()
               
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
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):               
                weightsList.append(Decimal(str(_random.randint(weightScale[0],
                                                              weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        else:
            weightDistribution = 'equiobjectives'
            weightMode = (weightDistribution,None)
            weightScale = (1,1)
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):
                weightsList.append(Decimal(str(weightScale[0])))
                sumWeights += weightScale[0]

        # store sum of weights and precision level
        self.sumWeights = sumWeights
        self.valuationPrecision = Decimal('0.1')/sumWeights
        
        # generate objectives dictionary
        objectives = OrderedDict([(
            'Eco', {'name':'Economical aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'}),
            ('Soc', {'name': 'Societal aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'}),
            ('Env',{'name':'Environmental aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'})
            ])


        # generate criteria dictionary with random thresholds
        
        ng = len(str(numberOfCriteria)) 
        if commonScale == None:
            if OrdinalScales:
                commonScale = (0,10)
            else:
                commonScale = (0.0,100.0)
        self.commonScale = commonScale

        criteria = OrderedDict()
        objectivesKeys = [key for key in objectives]
        #objectivesKeys.sort()
        #randChoice1 = Random(seed)
        ng = len(str(numberOfCriteria))
        for i in range(numberOfCriteria):
            if i == 0:
                criterionObjective = 'Eco'
            elif i == 1:
                criterionObjective = 'Soc'
            elif i == 2:
                criterionObjective = 'Env'
            else:    
                #criterionObjective = _random.choice(objectivesKeys)
                objInd = _random1.randint(1,len(objectivesKeys))
                criterionObjective = objectivesKeys[objInd-1]
            if criterionObjective == 'Eco':
                g = ('ec%%0%dd' % ng) % (i+1)
            elif criterionObjective == 'Soc':
                g = ('so%%0%dd' % ng) % (i+1)
            else:
                g = ('en%%0%dd' % ng) % (i+1)
            criteria[g] = {}
           #print(g,criterionObjective,objectivesKeys)
            criteria[g]['objective'] = criterionObjective
            if _random.random() > negativeWeightProbability:
                criteria[g]['preferenceDirection'] = 'max'
            else:
                criteria[g]['preferenceDirection'] = 'min'
            criteria[g]['name'] = 'criterion of objective %s' % (criterionObjective)
            criteria[g]['shortName'] = g + criterionObjective[0:2]
            span = commonScale[1] - commonScale[0]
            if commonThresholds == None:                    
                if OrdinalScales:
                    thresholds = [(0.1001*span,0.0),(0.2001*span,0.0),(0.8001*span,0.0)]
                else:
                    #span = commonScale[1] - commonScale[0]
                    thresholds = [(0.05001*span,0.0),(0.10001*span,0.0),(0.60001*span,0.0)]
            else:
                #span = commonScale[1] - commonScale[0]
                thresholds = [(commonThresholds[0][0]/100.0*span,commonThresholds[0][1]),\
                              (commonThresholds[1][0]/100.0*span,commonThresholds[1][1]),\
                              (commonThresholds[2][0]/100.0*span,commonThresholds[2][1])]
            if Debug:
                print(g,thresholds)
            thitems = ['ind','pref','veto']
            randVeto = _random.uniform(0.0,1.0)
            if randVeto > vetoProbability or vetoProbability == None:
                    thitems = ['ind','pref']
            criteria[g]['thresholds'] = {}
            for t in range(len(thitems)):
                criteria[g]['thresholds'][thitems[t]] =\
                   (Decimal(str(thresholds[t][0])),Decimal(str(thresholds[t][1])))
                
            criteria[g]['scale'] = commonScale
            if criteria[g]['preferenceDirection'] == 'max':
                if IntegerWeights:
                    criteria[g]['weight'] = weightsList[i]
                else:
                    criteria[g]['weight'] = weightsList[i] / sumWeights
            else:
                if NegativeWeights:
                    if IntegerWeights:
                        criteria[g]['weight'] = weightsList[i]
                    else:
                        criteria[g]['weight'] = weightsList[i] / sumWeights
                else:
                    if IntegerWeights:
                        criteria[g]['weight'] = -weightsList[i]
                    else:
                        criteria[g]['weight'] = -weightsList[i] / sumWeights


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
            weightsProduct = 1
            for oi in objectivesCardinality:
                weightsProduct *= objectivesCardinality[oi]
            if Debug:
                print(weightsProduct)
            for g in criteria:
                gweight = weightsProduct // objectivesCardinality[criteria[g]['objective']]
                if criteria[g]['preferenceDirection'] == 'max':
                    criteria[g]['weight'] = gweight
                else:
                    if NegativeWeights:
                        criteria[g]['weight'] = -gweight
                    else:
                        criteria[g]['weight'] = gweight
                if Debug:
                    print(weightsProduct)
                    print(objectivesCardinality[criteria[g]['objective']])
                    print(criteria[g]['weight'])
                
        # allocate (criterion,action) to coalition supporting type
        objectiveSupportingTypes = [('good','+'),('fair','~'),('weak','-')]
        self.objectiveSupportingTypes = objectiveSupportingTypes
        #randChoice2 = Random(seed)
        for x in actions:
            profile = {}
            for obj in objectives:
                if Debug:
                    print(objectives,obj)
                ostInd = _random2.randint(1,len(objectiveSupportingTypes))
                ost = objectiveSupportingTypes[ostInd-1]
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
                    randeval = _random.uniform(randomRange[0],randomRange[1])
                    actions[a]['generators'][g] = (randomMode[0],randomRange)
                    if OrdinalScales:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))

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
                        xm = randomMode[1]
                        if xm > 0.5:
                            beta = 2.0
                            alpha = 1.0/(1-xm)
                        else:
                            alpha = 2.0
                            beta = 1.0 / xm
                    if Debug:
                        print('alpha,beta', alpha,beta)
                    u = _random.betavariate(alpha,beta)
                    randeval = (u * (M-m)) + m
                    if Debug:
                        print('xm,alpha,beta,u,m,M,randeval',xm,alpha,beta,u,m,M,randeval)
                    actions[a]['generators'][g] = ('beta',alpha,beta)
                    if OrdinalScales:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))
    
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
                        rdseed = _random.randint(1,pow(2,32))
                    else:
                        try:
                            rdseed += 1
                        except:
                            rdseed = seed
                    rngtr = RNGTr(m,M,xm,r,seed=rdseed)
                    randeval = rngtr.random()
                    if OrdinalScales:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,0)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))
                    else:
                        if criteria[g]['preferenceDirection'] == 'max':
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            if criteria[g]['weight'] < Decimal('0'):
                                evaluation[g][a] = Decimal(str(round(randeval,0)))
                            else:
                                evaluation[g][a] = Decimal(str(-round(randeval,0)))
                   
                    if Debug:
                        print(randeval, criteria[g]['preferenceDirection'], evaluation[g][a])
            else:
                print('Error: invalid random number generator %s !!!' % commonPar) 

        # install self object attributes

        for obj in objectives:
            objCriteria = [g for g in criteria if criteria[g]['objective'] == obj]
            objectives[obj]['criteria'] = objCriteria
            objWeight = Decimal('0')
            for g in objCriteria:
                objWeight += abs(criteria[g]['weight'])
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
                if _random.random() < missingDataProbability:
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

class _Random3ObjectivesPerformanceGenerator(RandomPerformanceGenerator):
    """
    Generator for new decision actions with random evaluation following a
    given Random3ObjectivesPerformanceTableau model.
    """
    def __init__(self,argPerfTab,actionNamePrefix='a',
                 instanceCounter=0,seed=None,Debug=False):
        """
        Set the initial state of the random generator.
        """
        import random
        random.seed(seed)
        self.random = random
        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr
        self.RNGTr = RNGTr
        self.perfTab = argPerfTab
        self.actionNamePrefix = actionNamePrefix
        if instanceCounter == None:
            try:
                self.counter = len(argPerfTab.actions)
            except:
                self.counter = 0
        else:
            self.counter = instanceCounter
        self.nd = len(str(self.counter))
        self.Debug = Debug
        
    def _randomAction(self):
        """
        Returns a dictionary with following content:

        { 'action': { 'key': actionKey, 'shortName': ..., 'name': ...,  ... },                        
        'evaluation': {'g1': Decimal(...), 'g2': Decimal(...), ... }  }
        """
        # generate random evaluation
        Debug = self.Debug
        random = self.random
        try:
            digits = self.perfTab.valueDigits
        except:
            digits = 2
        criteria = self.perfTab.criteria
        objectives = self.perfTab.objectives
        objectiveSupportingTypes = self.perfTab.objectiveSupportingTypes
        commonScale = self.perfTab.commonScale
        OrdinalScales = self.perfTab.OrdinalScales

        # generate action key and record
        self.counter += 1
        if self.perfTab.BigData:
            actionName = ('%s%%0%dd' % (self.actionNamePrefix,self.nd)) % (self.counter)
            actionKey = self.counter
            action = {'shortName': actionName,
                              'name': actionName,
                              'key': actionKey,
                              'generators': {}}
        else:   
            actionKey = ('%s%%0%dd' % (self.actionNamePrefix,self.nd)) % (self.counter)
            action = {'shortName':actionKey,
                        'name': 'random decision action',
                        'comment': '3 Objectives',
                        'key': actionKey,
                        'generators': {}}

        # allocate coalition supporting types
        profile = {}
        for obj in objectives:
            if Debug:
                print(objectives,obj)
            ost = random.choice(objectiveSupportingTypes)
            action[obj]=ost[0]
            action['name'] =\
                    action['name'] + ' '+ str(obj) + ost[1]
            profile[obj] = action[obj]
        action['profile'] = profile
        if Debug:
            print(action)
        
        # generate random evaluations
        evaluation = {}
        for g in criteria:
            randomMode= criteria[g]['randomMode']
            aobj = criteria[g]['objective']

            # uniform distribution
            if str(randomMode[0]) == 'uniform':          
                if randomMode[1] == 'variable':
                    #aobj = criteria[g]['objective']
                    if actions['profile'][aobj] == 'weak':
                        randomRange = (commonScale[0],
                                       commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                    elif action['profile'][aobj] == 'fair':
                        randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                       commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                    elif action['profile'][aobj] == 'good':
                        randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                      commonScale[1])       
                    action['comment'] += ': %s %s' % (randomMode[0],randomRange)
                else:
                    randomRange = (commonScale[1],commonScale[2]) 
                randeval = random.uniform(randomRange[0],randomRange[1])
                action['generators'][g] = (randomMode[0],randomRange)
                if OrdinalScales:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,0)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,0)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,0)))
                else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,digits)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,digits)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,digits)))
                        
            # beta distribution
            elif str(randomMode[0]) == 'beta':
                m = commonScale[0]
                M = commonScale[1]
                if randomMode[1] == 'variable':
                    if action['profile'][aobj] == 'good':
                        # mode = 75, stdev = 15
                        #xm = 75
                        alpha = 5.8661
                        beta = 2.62203
                    elif action['profile'][aobj] == 'fair':
                        # nmode = 50, stdev = 15
                        #xm = 50
                        alpha = 5.05556
                        beta = 5.05556
                    elif action['profile'][aobj] == 'weak':
                        # mode = 25, stdev = 15
                        # xm = 25
                        alpha = 2.62203
                        beta = 5.8661                         
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
                action['generators'][g] = ('beta',alpha,beta)
                if OrdinalScales:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,0)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,0)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,0)))
                else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,digits)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,digits)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,digits)))
            # triangular
            elif str(randomMode[0]) == 'triangular':
                m = commonScale[0]
                M = commonScale[1]
                span = commonScale[1]-commonScale[0]
                if randomMode[1] == 'variable':
                    if action['profile'][aobj] == 'good':
                        xm = 0.7*span
                    elif action['profile'][aobj] == 'fair':
                        xm = 0.5*span
                    elif action['profile'][aobj] == 'weak':
                        xm = 0.3*span
                else:
                    xm = randomMode[1]
                r  = randomMode[2]
                action['generators'][g] = (randomMode[0],xm,r)
                # setting a speudo random seed
                rdseed = random.random()
                rngtr = self.RNGTr(m,M,xm,r,seed=rdseed)
                randeval = rngtr.random()
                if OrdinalScales:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,0)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,0)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,0)))
                else:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g] = Decimal(str(round(randeval,digits)))
                    else:
                        if criteria[g]['weight'] > Decimal('0'):
                            evaluation[g] = Decimal(str(-round(randeval,digits)))
                        else:
                            evaluation[g] = Decimal(str(round(randeval,digits)))
               
                if Debug:
                    print(randeval, criteria[g]['preferenceDirection'], evaluation[g])
                        
        if Debug:
            print(evaluation)

        # randomly insert missing data
        missingDataProbability = self.perfTab.missingDataProbability
        for g in criteria:
            if random.random() < missingDataProbability:
                evaluation[g] = Decimal('-999')

        # return a new random decision alternative
        return {'action': action,'evaluation':evaluation}

##    def randomUpdate(self,nbrOfRandomActions=1):
##        """
##        Updates *self.perfTab* with *n* = *nbrOfActions* new random decision alternatives.
##
##        .. note::
##
##            The update will modify the generator's given performance tableau instance by,
##            either adding new actions with their random evaluations,
##            or updating the performances of already existing decision actions.
##        """
##        actions = self.perfTab.actions
##        criteria = self.perfTab.criteria
##        evaluation = self.perfTab.evaluation
##        for i in range(nbrOfRandomActions):
##            newAction = self._randomAction()
##            newEvaluation = newAction['evaluation']
##            newKey = newAction['action'].pop('key')
##            actions[newKey] = newAction['action']
##            for g in criteria:
##                evaluation[g][newKey] = newEvaluation[g]


#---------------
class _Random3ObjectivesPerformanceTableau(_RandomCoalitionsPerformanceTableau):
    """
    Specialization of the RandomCoalitionsPerformanceTableau
    for 3 objectives: *A*, *B* and *C*.

    Each decision action is qualified at random as weak (-), fair (~) or good (+)
    on each of the three objectives. The action comment shows for each objective the respective position (- ,~, +)
    of the evaluation mode, for instance (*A* - *B* + *C* ~).
    
    Generator parameters are described in the parent class.
    
    .. note::

        If the mode of the triangular districbution is set to 'variable',
        three modes at 0.3 (-), 0.5 (~), respectively 0.7 (+) of the common scale span
        are set at random for each coalition and action.
    
    """
    def __init__(self,numberOfActions = 20, numberOfCriteria = 13,\
                 weightDistribution = 'equiobjectives', weightScale=None,\
                 IntegerWeights = True, commonScale = (0.0,100.0),\
                 commonThresholds = [(5.0,0.0),(10.0,0.0),(60.0,0.0)],\
                 commonDistribution = ['triangular','variable',0.5],\
                 missingDataProbability = 0.05,\
                 valueDigits=2,\
                 BigData=False,\
                 Debug=False, 
                 seed= None):
        from copy import deepcopy
        import random
        random.seed(seed)
        
        if commonDistribution[1] == 'variable':
            VariableGenerators = True
            commonMode = [commonDistribution[0],
                          (commonScale[0]+commonScale[1])/2.0,
                          commonDistribution[2]]
        else:
            VariableGenerators = False
        if weightDistribution == 'equiobjectives':
            weightDistribution = 'equicoalitions'
        t = RandomCoalitionsPerformanceTableau(numberOfActions=numberOfActions,
                                               numberOfCriteria=numberOfCriteria,
                                               weightDistribution=weightDistribution,
                                               weightScale=weightScale,
                                               IntegerWeights=IntegerWeights,
                                               commonScale =commonScale,
                                               commonThresholds=commonThresholds,
                                               commonMode=commonDistribution,
                                               VariableGenerators=VariableGenerators,
                                               valueDigits=valueDigits,
                                               BigData=BigData,
                                               Debug=Debug, seed=seed)

        self.__dict__ = t.__dict__
        for g in self.criteria:
            if self.criteria[g]['name'] == 'random criterion of coalition A':
                self.criteria[g]['name'] = 'random economic criterion'
                self.criteria[g]['objective'] = 'Eco'
            elif self.criteria[g]['name'] == 'random criterion of coalition B':
                self.criteria[g]['name'] = 'random societal criterion'
                self.criteria[g]['objective'] = 'Soc'
            elif self.criteria[g]['name'] == 'random criterion of coalition C':
                self.criteria[g]['name'] = 'random environmental criterion'
                self.criteria[g]['objective'] = 'Env'
                
        self.objectives = OrderedDict({
            'Eco': {'name':'Economical aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'},
            'Soc': {'name': 'Societal aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'},
            'Env': {'name':'Environmental aspect',
                  'comment': 'Random3ObjectivesPerformanceTableau generated'}
            })
        
        for obj in self.objectives:
            objCriteria = [g for g in self.criteria if self.criteria[g]['objective'] == obj]
            #objCriteria.sort()
            self.objectives[obj]['criteria'] = objCriteria
            objWeight = Decimal('0')
            for g in objCriteria:
                objWeight += self.criteria[g]['weight']
            self.objectives[obj]['weight'] = objWeight

        #actionsList = [x for x in self.actions]
        for x in dict.keys(self.actions):
            if 'A- B- C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc- Env-)'
                self.actions[x]['profile'] = {'Eco': 'weak', 'Soc': 'weak','Env': 'weak'}
            elif 'A~ B- C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc- Env-)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'weak','Env': 'weak'}
            elif 'A+ B- C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc- Env-)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'weak','Env': 'weak'}
            elif 'A- B~ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc~ Env-)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'fair','Env': 'weak'}
            elif 'A~ B~ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc~ Env-)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'fair','Env': 'weak'}
            elif 'A+ B~ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc~ Env-)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'fair','Env': 'weak'}
            elif 'A- B+ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc+ Env-)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'good','Env': 'weak'}
            elif 'A~ B+ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc+ Env-)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'good','Env': 'weak'}
            elif 'A+ B+ C-' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc+ Env-)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'good','Env': 'weak'}
            elif 'A- B- C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc- Env~)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'weak','Env': 'fair'}
            elif 'A~ B- C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc- Env~)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'weak','Env': 'fair'}
            elif 'A+ B- C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc- Env~)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'weak','Env': 'fair'}
            elif 'A- B~ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc~ Env~)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'fair','Env': 'fair'}
            elif 'A~ B~ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc~ Env~)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'fair','Env': 'fair'}
            elif 'A+ B~ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc~ Env~)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'fair','Env': 'fair'}
            elif 'A- B+ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc+ Env~)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'good','Env': 'fair'}
            elif 'A~ B+ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc+ Env~)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'good','Env': 'fair'}
            elif 'A+ B+ C~' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc+ Env~)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'good','Env': 'fair'}
            elif 'A- B- C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc- Env+)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'weak','Env': 'good'}
            elif 'A~ B- C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc- Env+)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'weak','Env': 'good'}
            elif 'A+ B- C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc- Env+)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'weak','Env': 'good'}
            elif 'A- B~ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc~ Env+)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'fair','Env': 'good'}
            elif 'A~ B~ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc~ Env+)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'fair','Env': 'good'}
            elif 'A+ B~ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc~ Env+)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'fair','Env': 'good'}
            elif 'A- B+ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco- Soc+ Env+)'
                self.actions[x]['profile'] ={'Eco': 'weak', 'Soc': 'good','Env': 'good'}
            elif 'A~ B+ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco~ Soc+ Env+)'
                self.actions[x]['profile'] ={'Eco': 'fair', 'Soc': 'good','Env': 'good'}
            elif 'A+ B+ C+' in self.actions[x]['name']:
                self.actions[x]['name'] = 'random decision action (Eco+ Soc+ Env+)'
                self.actions[x]['profile'] ={'Eco': 'good', 'Soc': 'good','Env': 'good'}
            self.actions[x]['comment'] = 'Random3ObjectivesPerformanceTableau() generated'

##        criteriaList = [g for g in self.criteria]
##        criteriaList.sort()
##        actionsList = [x for x in self.actions]
##        actionsList.sort()
        for g in dict.keys(self.criteria):
            for x in dict.keys(self.actions):
                if random.random() < missingDataProbability:
                    self.evaluation[g][x] = Decimal('-999')
                
    def showActions(self,Alphabetic=False):
        print('*----- show decision action --------------*')
        actions = self.actions
        if Alphabtic:
            actionsKeys = [x for x in dict.keys(actions)]
            actionsKeys.sort()
            for x in actionsKeys:
                print('key: ',x)
                print('  name:      ',actions[x]['name'])
                print('  profile:   ',actions[x]['profile'])
        else:
            for x in actions.keys():
                print('key: ',x)
                print('  name:      ',actions[x]['name'])
                print('  profile:   ',actions[x]['profile'])
        
#---------------
class RandomCBPerformanceTableau(PerformanceTableau):
    """
    Full automatic generation of random Costs versus Benefits
    oriented performance tableaux.

    Parameters:
    
        * If numberOfActions == None, a uniform random number between 10 and 31 of cheap, neutral or advantageous actions (equal 1/3 probability each type) actions is instantiated.
        * If numberOfCriteria == None, a uniform random number between 5 and 21 of cost or benefit criteria. Cost criteria have probability 1/3, whereas benefit criteria respectively 2/3 probability to be generated. However, at least one criterion of each kind is always instantiated.
        * weightDistribution := {'equiobjectives'|'fixed'|'random'|'equisignificant'} By default, the sum of significance of the cost criteria is set equal to the sum of the significance of the benefit criteria. 
        * Default weightScale for 'random' weightDistribution is 1 - numberOfCriteria.
        * If NegativeWeights = True | False (default), the performance evaluation of the criteria with a 'min' preference direction will be positive, otherwise they will be negative.
        * Parameter commonScale is not used. The scale of cost criteria is cardinal or ordinal (0-10) with probability 1/4, respectively 3/4, whereas the scale of benefit criteria is ordinal or cardinal with probabilities 2/3, respectively 1/3.
        * All cardinal criteria are evaluated with decimals between 0.0 and 100.0 wheras all ordinal criteria are evaluated with integers between 0 and 10.
        * commonThresholds parameter is not used. Preference discrimination is specified as percentiles of concerned performance differences (see below).
        * CommonPercentiles = {'ind':0.05, 'pref':0.10, 'veto':'95} are expressed in percentiles of the observed performance differences and only concern cardinal criteria.

    .. note::

        Minimal number required of criteria is 2, and minimal number
        required of decision actions is 3 !
    
    >>> from randomPerfTabs import RandomCBPerformanceTableau
    >>> t = RandomCBPerformanceTableau(numberOfActions=5,numberOfCriteria=3,seed=1)
    >>> t
    *------- PerformanceTableau instance description ------*
    Instance class   : RandomCBPerformanceTableau
    Seed             : 1
    Instance name    : randomCBperftab
    # Actions        : 5
    # Objectives     : 2
    # Criteria       : 3
    Attributes       : ['randomSeed', 'name', 'digits', 'BigData',
                        'missingDataProbability', 'commonPercentiles',
                        'samplingSize', 'Debug', 'actionsTypesList',
                        'sumWeights', 'valuationPrecision', 'actions',
                        'objectives', 'criteriaWeightMode', 'criteria',
                        'evaluation', 'weightPreorder']
    >>> t.showObjectives()
    *------ show objectives -------"
    C: Costs
       c1 random ordinal cost criterion 2
      Total weight: 2.00 (1 criteria)
    B: Benefits
       b1 random ordinal benefit criterion 1
       b2 random cardinal benefit criterion 1
      Total weight: 2.00 (2 criteria)
    >>> t.showCriteria()
    *----  criteria -----*
    c1 'Costs/random ordinal cost criterion'
      Scale = (0, 10)
      Weight = 2
    b1 'Benefits/random ordinal benefit criterion'
      Scale = (0, 10)
      Weight = 1 
    b2 'Benefits/random cardinal benefit criterion'
      Scale = (0.0, 100.0)
      Weight = 1 
      Threshold ind : 4.70 + 0.00x ; percentile:  0.1
      Threshold pref : 4.70 + 0.00x ; percentile:  0.1
      Threshold veto : 30.84 + 0.00x ; percentile:  1.0
    >>> t.showActions()
    *----- show decision action --------------*
    key:  a1
      short name: a1c
      name:       random cheap decision action
      comment:    Cost-Benefit
    key:  a2
      short name: a2a
      name:       random advantageous decision action
      comment:    Cost-Benefit
    key:  a3
      short name: a3c
      name:       random cheap decision action
      comment:    Cost-Benefit
    key:  a4
      short name: a4n
      name:       random neutral decision action
      comment:    Cost-Benefit
    key:  a5
      short name: a5c
      name:       random cheap decision action
      comment:    Cost-Benefit
    >>> t.showPerformanceTableau()
    *----  performance tableau -----*
    criteria | weights |   'a1'   'a2'   'a3'   'a4'   'a5'   
    ---------|-----------------------------------------
       'b1'  |    1    |   4.00   8.00   5.00   4.00   6.00  
       'b2'  |    1    |  36.70  31.65  23.90  10.56  41.40  
       'c1'  |    2    |    NA   -5.00  -3.00  -8.00  -3.00  
    >>> ...  

    """

    def __init__(self,numberOfActions = 13,\
                 numberOfCriteria = 7,\
                 name = 'randomCBperftab',\
                 weightDistribution = 'equiobjectives',\
                 weightScale=None,\
                 IntegerWeights = True,\
                 NegativeWeights = False,\
                 #commonScale = None, commonThresholds = None,\
                 commonPercentiles= None,\
                 samplingSize = 100000,\
                 commonMode = None,\
                 valueDigits = 2,\
                 missingDataProbability = 0.01,\
                 BigData=False,\
                 seed = None,\
                 Threading = False,\
                 nbrCores = None,\
                 Debug=False,Comments=False):
        """
        Constructor for RadomCBPerformanceTableau instances.
        
        """

        import sys,math,copy
        import random

        # randomizer init
        self.randomSeed = seed
        random.seed(seed)

        # store argument values
        self.name = name
        self.digits = valueDigits
        self.BigData = BigData
        self.missingDataProbability = missingDataProbability
        self.commonPercentiles = commonPercentiles
        self.samplingSize = samplingSize
        self.Debug = Debug
        
        # generate actions
        if numberOfActions == None:
            numberOfActions = random.randint(10,31)
        nd = len(str(numberOfActions))
        self.actionsTypesList = ['cheap','neutral','advantageous']        
        actions = OrderedDict()
        actionsTypesList = self.actionsTypesList
        for i in range(1,numberOfActions+1):
            actionType = random.choice(actionsTypesList)
            if BigData:
                actionName = ('%%0%dd' % (nd)) % (i)
                actions[i] = {'shortName':actionName+actionType[0],
                              'name':actionName+actionType[0],
                              'type': actionType}
            else:   
                actionKey = ('a%%0%dd' % (nd)) % (i)
                actions[actionKey] = {'shortName':actionKey+actionType[0],
                        'name': 'action %s' % (actionKey),
                        'comment': 'Cost-Benefit',
                        'type': actionType}
        # generate objectives
        objectives = OrderedDict([
            ('C', {'name': 'Costs', 'criteria':[]}),
            ('B', {'name': 'Benefits', 'criteria':[]}),
            ])
        
        # generate criteria
        if numberOfCriteria == None:
            numberOfCriteria = random.randint(5,21)
        ng = len(str(numberOfCriteria))
        criterionTypesList = ['max','max','min']
        minScaleTypesList = ['cardinal','cardinal','cardinal','ordinal']
        maxScaleTypesList = ['ordinal','ordinal','cardinal']
        criterionTypeCounter = {'min':0,'max':0}
        criteria = OrderedDict()
        for i in range(numberOfCriteria):
            # at least one cost and one benefit criterion is selected
            if i == 0:
                criterionType = 'min'
            elif i == 1:
                criterionType = 'max'
            else:
                criterionType = random.choice(criterionTypesList)
            criterionTypeCounter[criterionType] += 1
            if criterionType == 'min':
                g = ('c%%0%dd' % ng) % (criterionTypeCounter[criterionType])
            else:
                g = ('b%%0%dd' % ng) % (criterionTypeCounter[criterionType])               
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
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):
                weightsList.append(Decimal(str(random.randint(weightScale[0],weightScale[1]))))
                sumWeights += weightsList[i]
            weightsList.reverse()
        elif weightDistribution == 'fixed':
            weightsList = []
            sumWeights = Decimal('0.0')
            for i in range(numberOfCriteria):
                if i == 0:
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
            for i in range(len(criteriaList)):
                if i == 0:
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
            for g in criteria:
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

        # store sum of weights and valuation precision
        self.sumWeights = sumWeights
        self.valuationPrecision = Decimal('0.1')/sumWeights

        for i,g in enumerate(criteria):
            ## if Debug:
            ##     print 'criterionScale = ', criterionScale
            if NegativeWeights:
                if criteria[g]['preferenceDirection'] == "max":
                    Sgn = Decimal('1.0')
                else:
                    Sgn = Decimal('-1.0')
                if IntegerWeights:
                    criteria[g]['weight'] = Sgn * weightsList[i]
                else:
                    criteria[g]['weight'] = Sgn * weightsList[i] / sumWeights
                i += 1
            else:
                if IntegerWeights:
                    criteria[g]['weight'] = weightsList[i]
                else:
                    criteria[g]['weight'] = weightsList[i] / sumWeights
                i += 1
                

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
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        if NegativeWeights:
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
        
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
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        if NegativeWeights:
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                        #evaluation[g][a] = Decimal(str(-round(randeval,digits)))
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
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        if NegativeWeights:
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                        #evaluation[g][a] = Decimal(str(-round(randeval,digits)))
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
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        if NegativeWeights:
                            evaluation[g][a] = Decimal(str(round(randeval,digits)))
                        else:
                            evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                        #evaluation[g][a] = Decimal(str(-round(randeval,digits)))
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
                    evaluation[g][a] = Decimal(str(round(evaluation[g][a],0)))
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
        from randomNumbers import IncrementalQuantilesEstimator
        est = IncrementalQuantilesEstimator(nbuf=nbuf)
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
                    criteria[g]['thresholds'][q] = (Decimal(str(est.report(quantile[q]))),Decimal('0'))
            
            if Comments:
                print('criteria',g,' default thresholds:')
                print(criteria[g]['thresholds'])
    
        # update criteria
        self.criteria = criteria


    def updateDiscriminationThresholds(self,Comments=False,Debug=False):
        """
        Recomputes performance discrimination thresholds from commonPercentiles.

        .. note::

            Overwrites all previous criterion discrimination thresholds !
            
        """
        actions = self.actions
        n = len(actions)
        n2 = (n*n) - n
        if n < 1000:
            nbuf = 1000
        else:
            nbuf = n
        samplingSize = self.samplingSize
        if n2 < samplingSize:
            samplingSize = n2
        from randomNumbers import IncrementalQuantilesEstimator
        est = IncrementalQuantilesEstimator(nbuf=nbuf)
        commonPercentiles = self.commonPercentiles
        if Debug:
            print('commonPercentiles=', commonPercentiles)
        if commonPercentiles == None:
            quantile = OrderedDict({'ind':0.05, 'pref':0.10 , 'veto':0.95})
        else:
            quantile = commonPercentiles
        criteria = self.criteria
        for g in criteria:
            criteria[g]['thresholds'] = OrderedDict()
            if criteria[g]['scaleType'] == 'cardinal' and n > 1:
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
                    criteria[g]['thresholds'][q] = (Decimal(str(est.report(quantile[q]))),Decimal('0'))
            
            if Comments:
                print('criteria',g,' default thresholds:')
                print(criteria[g]['thresholds'])

class _RandomCBPerformanceGenerator(RandomPerformanceGenerator):
    """
    Generator of new decision actions with random evaluations using
    the model parameters provided by a given RandomCBPerformanceTableau instance.

    """
    def __init__(self,argPerfTab,actionNamePrefix='a',
                 instanceCounter=None,seed=None):
        """
        Set the initial state of the random generator.
        """
        import random
        random.seed(seed)

        self.random = random
        self.perfTab = argPerfTab
        self.actionNamePrefix = actionNamePrefix
        if instanceCounter == None:
            self.counter = len(argPerfTab.actions)
        else:
            self.counter = instanceCounter
        self.nd = len(str(self.counter))
       
    def _randomAction(self):
        """
        Returns a dictionary with following content::

             { 'action': { 'key': actionKey, 'shortName': ..., 'name': ...,  
                      'type': 'neutral'|'advantageous'|'cheap'},
                      'evaluation': {'g1': Decimal(...), 
                                     'g2': Decimal(...), ... }}.
        
        """
        # generate action key
        self.counter += 1
        actionType = self.random.choice(self.perfTab.actionsTypesList)
        if self.perfTab.BigData:
            actionName = ('%s%%0%dd' % (self.actionNamePrefix,self.nd)) % (self.counter)
            actionKey = self.counter
            action = {'shortName': actionName+actionType[0],
                              'name': actionName+actionType[0],
                              'type': actionType,
                              'key': actionKey}
        else:   
            actionKey = ('%s%%0%dd' % (self.actionNamePrefix,self.nd)) % (self.counter)
            action = {'shortName':actionKey+actionType[0],
                        'name': 'random %s decision action' % (actionType),
                        'comment': 'Cost-Benefit',
                        'type': actionType,
                        'key': actionKey}

        # generate random evaluation

        random = self.random
        digits = self.perfTab.digits
        criteria = self.perfTab.criteria
        
        # generate random evaluations
        Debug = self.perfTab.Debug
        evaluation = {}
        for g in criteria:
            criterionScale = criteria[g]['scale']
            amplitude = criterionScale[1] - criterionScale[0]
            if amplitude < Decimal('11.0'):
                digits = 0
            x30=criterionScale[0] + amplitude*0.3
            x50=criterionScale[0] + amplitude*0.5
            x70=criterionScale[0] + amplitude*0.7
            if Debug:
                print('g, criterionx30,x50,x70', g, criteria[g], x30,x50,x70)
            evaluation[g] = {}
            randomMode = criteria[g]['randomMode']
            if str(randomMode[0]) == 'uniform':          
                randeval = random.uniform(criterionScale[0],criterionScale[1])
                if criteria[g]['preferenceDirection'] == 'max':
                    evaluation[g] = Decimal(str(round(randeval,digits)))
                else:
                    if criteria[g]['weight'] < Decimal('0'):
                        evaluation[g][a] = Decimal(str(round(randeval,digits)))
                    else:
                        evaluation[g][a] = Decimal(str(-round(randeval,digits)))
                    #evaluation[g] = Decimal(str(-round(randeval,digits)))
            elif str(randomMode[0]) == 'triangular':
                from math import sqrt
                m = criterionScale[0]
                M = criterionScale[1]
                #r  = randomMode[2]
                #xm = randomMode[1]
                if action['type'] == 'advantageous':
                    xm = x70
                    r = 0.50
                elif action['type'] == 'cheap':
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
                    randeval = m + sqrt(u/r)*(xm-m)
                else:
                    #randeval = (M*r - M + math.sqrt((-1+r)*(-1+u)*(M-xm)**2))/(-1+r)
                    randeval = M - sqrt((1-u)/(1-r))*(M-xm)
                
                if criteria[g]['preferenceDirection'] == 'max':
                    evaluation[g] = Decimal(str(round(randeval,digits)))
                else:
                    if criteria[g]['weight'] > Decimal('0'):
                        evaluation[g] = Decimal(str(-round(randeval,digits)))
                    else:
                        evaluation[g] = Decimal(str(round(randeval,digits)))
                #print randeval, criteria[g]['preferenceDirection'], evaluation[g][a]
                        
            elif str(randomMode[0]) == 'normal':
                ## amplitude = criterionScale[1]-criterionScale[0]
                ## x70 = criterionScale[0] + 0.7 * amplitude
                ## x50 = criterionScale[0] + 0.5 * amplitude
                ## x30 = criterionScale[0] + 0.3 * amplitude
                
                if action['type'] == 'advantageous':
                    mu = x70
                    sigma = 0.20 * amplitude
                elif action['type'] == 'cheap':
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
                    evaluation[g] = Decimal(str(round(randeval,digits)))
                else:
                    if criteria[g]['weight'] > Decimal('0'):
                        evaluation[g] = Decimal(str(-round(randeval,digits)))
                    else:
                        evaluation[g] = Decimal(str(round(randeval,digits)))
            elif str(randomMode[0]) == 'beta':
                m = criterionScale[0]
                M = criterionScale[1]
                if action['type'] == 'advantageous':
                    # xm = 0.7 sdtdev = 0.15
                    alpha = 5.8661
                    beta = 2.62203
                elif action['type'] == 'cheap':
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
                    evaluation[g] = Decimal(str(round(randeval,digits)))
                else:
                    if criteria[g]['weight'] > Decimal('0'):
                        evaluation[g] = Decimal(str(-round(randeval,digits)))
                    else:
                        evaluation[g] = Decimal(str(round(randeval,digits)))
                if Debug:
                    print('alpha,beta,u,m,M,randeval',alpha,beta,u,m,M,randeval)
                        
        if Debug:
            print(evaluation)

        # randomly insert missing data
        missingDataProbability = self.perfTab.missingDataProbability
        for g in criteria:
            if random.random() < missingDataProbability:
                evaluation[g] = Decimal('-999')

        # return a new random decision alternative
        return {'action': action,'evaluation':evaluation}
    
##    def randomUpdate(self,nbrOfRandomActions=1):
##        """
##        Updates *self.perfTab* with *n* = *nbrOfActions* new random decision alternatives.
##
##        .. note::
##
##            The update will modify the generator's given performance tableau instance by,
##            either adding new actions with their random evaluations,
##            or updating the performances of already existing decision actions.
##        """
##        actions = self.perfTab.actions
##        criteria = self.perfTab.criteria
##        evaluation = self.perfTab.evaluation
##        for i in range(nbrOfRandomActions):
##            newAction = self._randomAction()
##            newEvaluation = newAction['evaluation']
##            newKey = newAction['action'].pop('key')
##            actions[newKey] = newAction['action']
##            for g in criteria:
##                evaluation[g][newKey] = newEvaluation[g]

        

##############################
class _RandomS3PerformanceTableau(_RandomCoalitionsPerformanceTableau):
    """
    Obsolete dummy class for backports.
    """

#----------test Digraph class ----------------
if __name__ == "__main__":
    
    print('*-------- Testing classes and methods -------')

    from digraphs import *
    from outrankingDigraphs import BipolarOutrankingDigraph
    from randomPerfTabs import *
##    t = RandomAcademicPerformanceTableau(numberOfStudents=10,numberOfCourses=5,
##                                         commonMode=('uniform',None,None),
##                                         missingDataProbability=0.01)
    t = RandomAcademicPerformanceTableau(numberOfStudents=10,numberOfCourses=10,
                                commonMode=('triangular',14,0.4),
                                missingDataProbability=0.01,
                                WithTypes=True,
                                seed=1)
    print('transposed')
    t.showPerformanceTableau(Transposed=True)
    print('not transposed')
    t.showPerformanceTableau(Transposed=False)
    #t.showHTMLPerformanceTableau(Transposed=True)
    #t.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=5,ndigits=0)
                                             



##    from time import time
##    t0 = time()
##    t = RandomCBPerformanceTableau(numberOfActions=20,
##                                   numberOfCriteria=13,
##                                   samplingSize=100000,
##                                   BigData=True,
##                                   seed=100)
##    print(time()-t0)
##    t.saveXMCDA2('test2')
##    t.showCriteria()
    # t = Random3ObjectivesPerformanceTableau(numberOfActions=10,
    #                                         numberOfCriteria=13,
    #                                         OrdinalScales=False,
    #                                         commonScale=None,
    #                                         weightDistribution='equiobjectives',
    #  #weightScale=(1,5),
    #                                         commonMode=('triangular','variable',None),
    #                                         vetoProbability=0.5,
    #                                         NegativeWeights=False,
    #                                         negativeWeightProbability=0.25,
    #                                         seed=120,Debug=False)

    # t.showObjectives()
    # t.showCriteria()
    # t.showPerformanceTableau()
    # t.csvAllQuantiles('q')
    # t.showAllQuantiles()
    # t.showStatistics()
    
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
##    t = Random3ObjectivesPerformanceTableau(numberOfActions=10,OrdinalScales=True,
##                                            commonScale=(0.0,10.0),
##                                            commonThresholds=((0.1,0.0),(0.2,0.0),(0.6,0.0)),
##                                           seed=100)
##    t.showAll()
##    rag1 = Random3ObjectivesPerformanceGenerator(t,\
##                actionNamePrefix='b',seed=100)
##    sampleSize = 5
##    rag1.randomActions(sampleSize)
##    #t.showHTMLPerformanceHeatmap(Correlations=True)
##    rag2 = Random3ObjectivesPerformanceGenerator(t,actionNamePrefix='c',seed=110)
##    #rag2.randomUpdate(nbrOfRandomActions=5)
##    print(rag2.randomActions(2))
##    ntp = rag2.randomPerformanceTableau(nbrOfRandomActions=10)
##    #t.showHTMLPerformanceHeatmap(ndigits=0,Correlations=True)
##    # t.updateDiscriminationThresholds(Comments=True,Debug=True)
    
    
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
     
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. August 2011                    *')
    print('* $Revision: 1.37 $                *')                   
    print('*************************************')

#############################
