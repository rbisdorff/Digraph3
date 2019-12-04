#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
c-Extension for the Digraph3 collection.
Module cRandPerfTabs.py is a c-compiled version of the
:py:mod:`randomPerfTabs` module for generating random performance tableaux of Big Data type,
ie with integer action keys and float performance evaluations.

Conversions methods are provided
to switch from the standard to the BigData format and back.  

Copyright (C) 2018  Raymond Bisdorff

"""
__version__ = "cython 0.27.3"

from perfTabs import *
#from decimal import Decimal
from collections import OrderedDict

#########################################
# generators for random PerformanceTableaux
class cPerformanceTableau(PerformanceTableau):
    """
    Root class for cythonized performace tableau instances.

    *Parameter*:
        - filePerfTab = None (default). Loads a cPerformanceTableau instance from a stored file in python format named *filePerfTab* (without the .py extension).

    """

    def __init__(self,filePerfTab=None):
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
            except:
                pass
            self.criteria = argDict['criteria']
            try:
                self.weightPreorder = argDict['weightorder']
            except:
                self.weightPreorder = self.computeWeightPreorder()
            self.evaluation = argDict['evaluation']
            self.convertInsite2BigData()
        else:
            self.name = "empty_instance"
            self.actions = OrderedDict()
            self.criteria = OrderedDict()
            self.weightPreorder = {}
            self.evaluation = {}

    def convertInsite2BigData(self):
        """
        Converts in site weights, evaluations and discrimination thresholds to bigData float format.
        """ 
        self.convertWeight2Integer()
        self.convertEvaluation2Float()
        self.convertDiscriminationThresholds2Float()

    def convert2Standard(self):
        """
        Renders a standard :py:class:`perfTabs.PerformanceTableau` class instance from a deepcopy of a BigData instance.
        """
        from perfTabs import PerformanceTableau
        from copy import deepcopy
        from collections import OrderedDict
        from decimal import Decimal
        t = PerformanceTableau(isEmpty=True)
        t.name = 'std_' + self.name
        att = [a for a in self.__dict__]
        att.remove('name')
        att.remove('actions')
        att.remove('evaluation')
        for a in att:
            t.__dict__[a] = deepcopy(self.__dict__[a])
        actions = OrderedDict()
        for x in self.actions:
            xName = self.actions[x]['name']
            try:
                sName = self.actions[x]['shortName']
            except KeyError:
                sName = xName
            actions[xName] = {'id':x,'name': xName,
                              'shortname': sName}
        t.actions = actions
        evaluation = {}
        for g in t.criteria:
            evaluation[g] = {}
            for x in self.actions:
                xName = self.actions[x]['name']
                evaluation[g][xName] = Decimal(str(self.evaluation[g][x]))
        t.evaluation = evaluation
        cPerformanceTableau.convertWeight2Decimal(t)
        #cPerformanceTableau.convertEvaluation2Decimal(t)
        cPerformanceTableau.convertDiscriminationThresholds2Decimal(t)
        return t

    def convertInsite2Standard(self):
        """
        Converts in site weights, evaluations and discrimination thresholds to standard Decimal format.
        """
        self.convertWeight2Decimal()
        self.convertEvaluation2Decimal()
        self.convertDiscriminationThresholds2Decimal()

    def convertInsite2BigData(self):
        """
        Converts in site weights, evaluations and discrimination thresholds to bigData float format.
        """
        self.convertWeight2Decimal()
        self.convertEvaluation2Decimal()
        self.convertDiscriminationThresholds2Decimal()
        
    def convertWeight2Integer(self):
        """
        Converts significance weights from Decimal
        to int format.
        """
        criteria = self.criteria
        for g in criteria:
            criteria[g]['weight'] = int(criteria[g]['weight'])
        self.criteria = criteria

    def convertWeight2Decimal(self):
        """
        Converts significance weights from int to  Decimal format.
        """
        from decimal import Decimal
        criteria = self.criteria
        for g in criteria:
            criteria[g]['weight'] = Decimal(str(criteria[g]['weight']))
        self.criteria = criteria

    def convertEvaluation2Float(self):
        """
        Converts evaluations from Decimal to float format.
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

    def convertEvaluation2Decimal(self,int ndigits=2):
        """
        Converts evaluations from float to Decimal format.
        """
        cdef int x
        from decimal import Decimal
        evaluation = self.evaluation
        actions = self.actions
        criteria = self.criteria
        fstr = '%%.%df' % ndigits
        for g in criteria:
            for x in actions:
                if evaluation[g][x] != Decimal('-999'):
                    evaluation[g][x] = Decimal(fstr % evaluation[g][x])
        self.evaluation = evaluation

    def convertDiscriminationThresholds2Float(self):
        """
        Converts perrformance discrimination thresholds from Decimal to float format.
        """
        criteria = self.criteria
        for g in criteria:
            for th in criteria[g]['thresholds']:
                d = criteria[g]['thresholds'][th]
                d1 = (float(d[0]),float(d[1]))
                criteria[g]['thresholds'][th] = d1

    def convertDiscriminationThresholds2Decimal(self):
        """
        Converts perrformance discrimination thresholds from float to Decimal format.
        """
        from decimal import Decimal
        criteria = self.criteria
        for g in criteria:
            for th in criteria[g]['thresholds']:
                d = criteria[g]['thresholds'][th]
                d1 = (Decimal(str(d[0])),Decimal(str(d[1])))
                criteria[g]['thresholds'][th] = d1

    def showCriteria(self,IntegerWeights=True,Alphabetic=False,ByObjectives=True,Debug=False):
        """
        Prints self.criteria with thresholds and weights.

        *Parameters*:
            * IntegerWeights=True,
            * Alphabetic=False,
            * ByObjectives=True,
            * Debug=False
        
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
                    try:
                        print('Random generator:  %s' % criteria[g]['randomMode'])
                    except:
                        pass
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
                try:
                    print('Random generator:  %s' % criteria[g]['randomMode'])
                except:
                    pass
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

    def showPerformanceTableau(self,bint Transposed=False,actionsSubset=None,\
                               int fromIndex=-1,int toIndex=-1,bint Sorted=False,ndigits=2):
        """
        Print the object's performance tableau.

        *Parameters*:
            - Transposed = False (default = actions x criteria) | True (criteria x actions)
            - actionsSubset = None
            - fromIndex = -1 (by default put to 0)
            - toIndex = -1 (by default put to len(self.actions)
            - Sorted = False (default) | True
            - ndigits = 2 (default)
        
        """
        cdef int i, x
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
        if fromIndex == -1:
            fromIndex = 0
        if toIndex == -1:
            toIndex=len(actionsList)
        # view criteria x actions
        if Transposed:
            print('criteria | weights |', end=' ')
            for x in actionsList:
                print('\''+str(self.actions[x]['name'])+'\'  ', end=' ')
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
            print('  Criteria| ', end=' ')
            for g in criteriaList:
                print('\''+str(g)+'\'  ', end=' ')
            print('\nActions\  | ', end=' ')
            for g in criteriaList:
                print('  %s   ' % str(self.criteria[g]['weight'] ), end=' ')          
            print('\n----------|-----------------------------------------')
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


    def normalizeEvaluations(self,lowValue=0.0,highValue=100.0,bint Debug=False):
        """
        Recodes the evaluations between lowValue and highValue on all criteria.

        *Parameters*:
            * lowValue=0.0,
            * highValue=100.0,
            * Debug=False
            
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

    def showHTMLPerformanceHeatmap(self,actionsList=None,
                                   criteriaList=None,
                                   colorLevels=7,
                                   pageTitle=None,
                                   ndigits=2,
                                   SparseModel=False,
                                   minimalComponentSize=1,
                                   rankingRule='Copeland',
                                   quantiles=None,
                                   strategy='average',
                                   Correlations=False,
                                   Threading=False,
                                   nbrOfCPUs=None,
                                   Debug=False):
        """
        shows the html heatmap version of the performance tableau in a browser window
        (see perfTabs.htmlPerformanceHeatMap() method ).

        **Parameters**:

              * *actionsList* and *criteriaList*, if provided,  give the possibility to show the decision alternatives, resp. criteria, in a given ordering.
              * *ndigits* = 0 may be used to show integer evaluation values.
              * If no *actionsList* is provided, the decision actions are ordered from the best to the worst. This ranking is obtained by default with the Copeland rule applied on a standard *BipolarOutrankingDigraph*. When the *SparseModel* flag is put to *True*, a sparse *PreRankedOutrankingDigraph* construction is used instead.                
              * The *minimalComponentSize* allows to control the fill rate of the pre-ranked model. If *minimalComponentSize* = *n* (the number of decision actions) both the pre-ranked model will be in fact equivalent to the standard model.
              * It may interesting in some cases to use *rankingRule* = 'NetFlows'.
              * Quantiles used for the pre-ranked decomposition are put by default to *n* (the number of decision alternatives) for *n* < 50. For larger cardinalities up to 1000, quantiles = *n* /10. For bigger performance tableaux the *quantiles* parameter may be set to a much lower value not exceeding usually 1000.
              * The pre-ranking may be obtained with three ordering strategies for the quantiles equivalence classes: 'average' (default), 'optimistic' or  'pessimistic'.
              * With *Correlations* = *True* and *criteriaList* = *None*, the criteria will be presented from left to right in decreasing order of the correlations between the marginal criterion based ranking and the global ranking used for presenting the decision alternatives.
              * For large performance Tableaux, *multiprocessing* techniques may be used by setting.
              *  *Threading* = *True* in order to speed up the computations; especially when *Correlations* = *True*.
              * By default, the number of cores available, will be detected. It may be necessary in a HPC context to indicate the exact number of singled threaded cores that are actually allocated to the running job.

        >>> from cRandomPerfTabs import RandomPerformanceTableau
        >>> rt = RandomPerformanceTableau(seed=100)
        >>> rt.showHTMLPerformanceHeatmap(colorLevels=5,Correlations=True)

        .. image:: perfTabsExample.png
           :alt: HTML heat map of the performance tableau
           :width: 600 px
           :align: center
        
        """
        import webbrowser

        ## convert to std
        self.convertInsite2Standard()
        
        fileName = '/tmp/performanceHeatmap.html'
        fo = open(fileName,'w')
        if pageTitle == None:
            pageTitle = 'Heatmap of Performance Tableau \'%s\'' % self.name
            
        fo.write(self._htmlPerformanceHeatmap(argCriteriaList=criteriaList,
                                             argActionsList=actionsList,
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

        ### convert back to Bgd
        self.convertInsite2BigData()

    def save(self,fileName='tempperftab',valueDigits=2):
        """
        Persistant storage of Performance Tableaux.
        """
        print('*--- Saving cPerformanceTableau instance in file: <' + str(fileName) + '.py> ---*')
        actions = self.actions
        try:
            objectives = self.objectives
        except:
            objectives = {}
        criteria = self.criteria
        evaluation = self.evaluation
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved cPerformanceTableau: \n')
        fo.write('from collections import OrderedDict\n')
        # actions
        fo.write('actions = OrderedDict([\n')
        for x in actions:
            fo.write('(%d, {\n' % x)
            for it in self.actions[x].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.actions[x][it])) )
            fo.write('}),\n')
        fo.write('])\n')
        # objectives
        fo.write('objectives = OrderedDict([\n')
        for obj in objectives:
            fo.write('(\'%s\', {\n' % str(obj))
            for it in self.objectives[obj].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.objectives[obj][it])))
            fo.write('}),\n')
        fo.write('])\n')            
        # criteria
        fo.write('criteria = OrderedDict([\n') 
        for g in criteria:
            fo.write('(\'%s\', {\n' % str(g))
            for it in self.criteria[g].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.criteria[g][it])))
            fo.write('}),\n')
        fo.write('])\n')
        # evaluation
        fo.write('evaluation = {\n')
        for g in criteria:
            fo.write('\'' +str(g)+'\': {\n')
            for x in actions:
                evaluationString = '%%d:%%.%df,\n' % (valueDigits)
                fo.write(evaluationString % (x,evaluation[g][x]) )    
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()


############ Specialized cPerformanceTableau models ################


class cPartialPerformanceTableau(cPerformanceTableau):
    """
    Constructor for partial performance tableaux concerning a subset of actions and/or criteria and/or objectives.

    *Parameters*:
        - inPerfTab: valid cPerformanceTableau object instance
        - actionsSubset = None
        - criteriaSubset = None
        - objectivesSubset = None

    .. note::
        Returns the case given a partial deep copy of the *inPerfTab* object.

    """
    def __init__(self,inPerfTab,actionsSubset=None,criteriaSubset=None,objectivesSubset=None):
        cdef int key
        
        from copy import deepcopy
        from collections import OrderedDict
        from cRandPerfTabs import cRandomCBPerformanceTableau,\
                                  cRandom3ObjectivesPerformanceTableau,\
                                  cRandomPerformanceTableau
        self.__class__ = inPerfTab.__class__
        # name
        self.name = 'partial-'+inPerfTab.name
        # actions
        na = len(inPerfTab.actions)
        actions = OrderedDict()
        if actionsSubset != None:
            for x in actionsSubset:
                intKey = int(x)
                actions[intKey] = deepcopy(inPerfTab.actions[x])
        else:
                actions = deepcopy(inPerfTab.actions)
        self.actions = actions
        actionsTypeStatistics = {}
        for x in inPerfTab.actions:
            if type(inPerfTab) == cRandomCBPerformanceTableau:
                xType = inPerfTab.actions[x]['type']
            elif type(inPerfTab) == cRandom3ObjectivesPerformanceTableau:
                #self.objectiveSupportingTypes = inPerfTab.objectiveSupportingTypes
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


class cRandomPerformanceTableau(cPerformanceTableau):
    """
    Specialization of the cPerformanceTableau class for generating a temporary
    random performance tableau.

    *Parameters*:
        * numberOfActions := nbr of decision actions.
        * numberOfCriteria := number performance criteria.
        * weightDistribution := 'random' (default) | 'fixed' | 'equisignificant'.
             | If 'random', weights are uniformly selected randomly
             | form the given weight scale;
             | If 'fixed', the weightScale must provided a corresponding weights
             | distribution;
             | If 'equisignificant', all criterion weights are put to unity.
        * weightScale := [Min,Max] (default =[1,numberOfCriteria].
        * IntegerWeights := True (in the BigData format)
        * commonScale := [Min;Max]; common performance measuring scales (default = [0;100])
        * commonThresholds := [(q0,q1),(p0,p1),(v0,v1)]; common indifference(q), preference (p)
          and considerable performance difference discrimination thresholds.
        * commonMode := common random distribution of random performance measurements:
             | ('uniform',Min,Max), uniformly distributed between min and max values. 
             | ('normal',mu,sigma), truncated Gaussion distribution. 
             | ('triangular',mode,repartition), generalized triangular distribution 
             | ('beta',mode,(alpha,beta)), by default Mode=None, alpha=beta=2.
        * valueDigits := <integer>, precision of performance measurements
          (2 decimal digits by default).
        
    Code example::
        >>> from cRandPerfTabs import RandomPerformanceTableau
        >>> t = RandomPerformanceTableau(numberOfActions=3,numberOfCriteria=1,seed=100)
        >>> t.actions
        OrderedDict([
        (1: {'name': '#1'}),
        (2: {'name': '#2'}),
        (3: {'name': '#3'})
        ])
        >>> t.criteria
        OrderedDict([
        ('g1': {'thresholds': {'ind' : (10.0, 0.0) ),
                                   'veto': (80.0, 0.0) ),
                                   'pref': (20.0, 0.0) },
                    'scale': (0.0, 100.0),
                    'weight': 1,
                    'name': 'cRandPerfTabs.RandomPerformanceTableau() instance',
                    'comment': 'Arguments: weightDistribution=random;
                        weightScale=(1, 1); commonMode=None'}).
        ])
        >>> t.evaluation
        {'g01': {1: 45.95, 2: 95.17, 3: 17.47.}}

    """
    def __init__(self,long numberOfActions = 13,\
                 int numberOfCriteria = 7,\
                 weightDistribution = 'equisignificant',\
                 weightScale=None,\
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
        self.randomSeed = seed
        import random
        random.seed(seed)
        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr

        # seeting tableau name
        self.name = 'cRandomperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            actionName = ('#%%0%dd' % (nd)) % (i)
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
            criteria[g]['preferenceDirection'] = 'max'
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
                    evaluation[c][x] = -999

        # store object dict
        self.actions = actions
        self.criteria = criteria
        self.evaluation = evaluation
        # store weights preorder
        self.weightPreorder = self.computeWeightPreorder()

# -----------------
class cRandomRankPerformanceTableau(cPerformanceTableau):
    """
    Specialization of the cPerformanceTableau class for generating a temporary
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
        self.randomSeed = seed
        import random
        random.seed(seed)

        # set name
        self.name = 'randrankperftab'
        
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            actionName = ('#%%0%dd' % (nd)) % (i)
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


class _cRandomCoalitionsPerformanceTableau(cPerformanceTableau):
    """
    Full automatic generation of performance tableaux with random coalitions of criteria

    *Parameters*:
        * numberOf Actions := 20 (default)
        * number of Criteria := 13 (default)
        * weightDistribution := 'equisignificant' (default with all weights = 1.0), 'random', 'fixed' (default w_1 = numberOfCriteria-1, w_{i!=1} = 1
        * weightScale := [1,numerOfCriteria] (random default), [w_1, w_{i!=1] (fixed)
        * commonScale := (0.0, 100.0) (default)
        * commonThresholds := [(1.0,0.0),(2.001,0.0),(8.001,0.0)] if OrdinalSacles, [(0.10001*span,0),(0.20001*span,0.0),(0.80001*span,0.0)] with span = commonScale[1] - commonScale[0].
        * commonMode := ['triangular',50.0,0.50] (default), ['uniform',None,None], ['beta', None,None] (three alpha, beta combinations (5.8661,2.62203) chosen by default for high('+'), medium ('~') and low ('-') evaluations.
        * valueDigits := 2 (default, for cardinal scales only)
        * Coalitions := True (default)/False, three coalitions if True
        * VariableGenerators := True (default) / False, variable high('+'), medium ('~') or low ('-') law generated evaluations.
        * OrdinalScales := True / False (default)
        * Debug := True / False (default)
        * RandomCoalitions = True / False (default) zero or more than three coalitions if Coalitions == False.
        * vetoProbability := x in ]0.0-1.0[ / None (default), probability that a cardinal criterion shows a veto preference discrimination threshold.
        
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
        self.randomSeed = seed
        import random
        random.seed(seed)
        if RandomCoalitions:
            Coalitions=False

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            
        from collections import OrderedDict
            
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            actionKey = ('#%%0%dd' % (nd)) % (i)
            #if BigData:
            actions[i] = {'shortName':actionKey,
                          'name': actionKey}
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
        span = commonScale[1] - commonScale[0]
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
            # if commonThresholds == None:                        
            #     span = commonScale[1] - commonScale[0]
            #     thresholds = [(0.05001*span,0),(0.10001*span,0.0),(0.60001*span,0.0)]
            # else:
            #     thresholds = commonThresholds
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
                    ##self.actions[a]['generators'][g] = (randomMode[0],randomRange)
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
                    ## self.actions[a]['generators'][g] = ('beta',alpha,beta)
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
                    ## self.actions[a]['generators'][g] = (randomMode[0],xm,r)
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

class cRandom3ObjectivesPerformanceTableau(cPerformanceTableau):
    """
    Specialization of the cPerformanceTableau
    for 3 objectives: *Eco*, *Soc* and *Env*.

    Each decision action is qualified at random as weak (-), fair (~) or good (+)
    on each of the three objectives.
    
    *Parameters*:
        * numberOf Actions := 20 (default),
        * number of Criteria := 13 (default),
        * weightDistribution := 'equiobjectives' (default)
                              | 'equisignificant' (weights set all to 1)
                              | 'random' (in the range 1 to numberOfCriteria),
        * weightScale := [1,numerOfCriteria] (random default),
        * commonScale := (0.0, 100.0) (default)
                | (0.0,10.0) if OrdinalScales == True,
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
        * valueDigits := 2 (default, for cardinal scales only),
        * vetoProbability := x in ]0.0-1.0[ (0.5 default), probability that a cardinal criterion shows a veto preference discrimination threshold.
        * missingDataProbability := x in ]0.0-1.0[ (0.05 default), probability that an action x criterion evaluation is missing.
        * Debug := True / False (default).
        
    """

    def __init__(self, int numberOfActions = 20, int numberOfCriteria = 13,\
                 weightDistribution = 'equiobjectives', weightScale=None,\
                 #integerWeights = True,\
                 bint OrdinalScales=False,\
                 commonScale = None,\
                 commonThresholds = None, commonMode = None,\
                 int valueDigits=2,\
                 float vetoProbability=0.5,\
                 float missingDataProbability = 0.05,\
                 #BigData=False,\
                 seed= None,\
                 bint Debug=False):

        cdef int nd, i, t, x, a, digits, weightsProduct = 1, objWeight=0
        cdef float span, randVeto, randeval, m, M, r, alpha, beta, xm=0.0, u      
        # naming
        self.name = 'random3ObjectivesPerfTab'
        # randomizer init
        self.randomSeed = seed
        import random
        random.seed(seed)

        from randomNumbers import ExtendedTriangularRandomVariable as RNGTr            

            
        # generate actions
        nd = len(str(numberOfActions))
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            actionKey = ('#%%0%dd' % (nd)) % (i)
            actions[i] = {'name': actionKey, 'shortName': actionKey}                 
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
            if OrdinalScales:
                commonScale = (0.0,10.0)
            else:
                commonScale = (0.0,100.0)
        span = commonScale[1] - commonScale[0]

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
            # if commonThresholds == None:                    
            #     span = commonScale[1] - commonScale[0]
            #     thresholds = [(0.05001*span,0),(0.10001*span,0.0),(0.60001*span,0.0)]
            # else:
            #     thresholds = commonThresholds
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
                #actions[x][obj]=ost[0]
                # actions[x]['name'] =\
                #     actions[x]['name'] + ' '+ str(obj) + ost[1]
                #profile[obj] = actions[x][obj]
                profile[obj] = ost[1]
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
                randomMode = list(commonMode)
            if randomMode[0] == 'uniform' and randomMode[1] == None:
                randomMode[1] = commonScale[0]
                randomMode[2] = commonScale[1]
                
            criteria[g]['randomMode'] = randomMode
            # if randomMode[1] == 'variable':
            #     commentString = 'Variable '+randomMode[0]+(' performance generator with low (-), medium (~) or high (+) parameters.')
            # else:
            #     commentString = 'Constant '+randomMode[0]+(' law with parameters = %s, %s' % (str(randomMode[1]),str(randomMode[2])))
                    
            # print(g,criteria[g],commentString)
            # criteria[g]['comment'] = commentString
            digits = valueDigits
            
            if str(randomMode[0]) == 'uniform':          
                for a in actions:
                    aobj = criteria[g]['objective']
                    aobjSt = actions[a]['profile'][aobj]
                    if randomMode[1] == 'variable':
                        aobj = criteria[g]['objective']
                        #if actions[a]['profile'][aobj] == '-':
                        if aobjSt == '-':
                            randomRange = (commonScale[0],
                                           commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                        #elif actions[a]['profile'][aobj] == '~':
                        elif aobjSt == '~':
                            randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                           commonScale[0]+0.7*(commonScale[1]-commonScale[0]))
                        #elif actions[a]['profile'][aobj] == '+':
                        elif aobjSt == '+':
                            randomRange = (commonScale[0]+0.3*(commonScale[1]-commonScale[0]),
                                          commonScale[1])       
                        #actions[a]['comment'] = ': %s %s' % (randomMode[0],randomRange)
                    else:
                        randomRange = (commonScale[1],commonScale[2]) 
                    randeval = random.uniform(randomRange[0],randomRange[1])
                    #actions[a]['generators'][g] = (randomMode[0],randomRange)
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)

            elif str(randomMode[0]) == 'beta':
                for a in actions:
                    aobj = criteria[g]['objective']
                    aobjSt = actions[a]['profile'][aobj]
                    m = commonScale[0]
                    M = commonScale[1]
                    if randomMode[1] == 'variable':
                        #if actions[a][criteria[g]['objective']] == '+':
                        if aobjSt == '+':
                            # mode = 75, stdev = 15
                            #xm = 75
                            alpha = 5.8661
                            beta = 2.62203
                        #elif actions[a][criteria[g]['objective']] == '~':
                        elif aobjSt == '~':
                            # nmode = 50, stdev = 15
                            #xm = 50
                            alpha = 5.05556
                            beta = 5.05556
                        #elif actions[a][criteria[g]['objective']] == '-':
                        elif aobjSt == '-':
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
                    #actions[a]['generators'][g] = ('beta',alpha,beta)
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][a] = round(randeval,digits)
                    else:
                        evaluation[g][a] = -round(randeval,digits)
    
            elif str(randomMode[0]) == 'triangular':
                for a in actions:
                    aobj = criteria[g]['objective']
                    aobjSt = actions[a]['profile'][aobj]
                    m = commonScale[0]
                    M = commonScale[1]
                    span = commonScale[1]-commonScale[0]
                    if randomMode[1] == 'variable':
                        #if actions[a][criteria[g]['objective']] == '+':
                        if aobjSt == '+':
                            xm = 0.7*span
                        #elif actions[a][criteria[g]['objective']] == '~':
                        elif aobjSt == '~':
                            xm = 0.5*span
                        #elif actions[a][criteria[g]['objective']] == '-':
                        elif aobjSt == '-':
                            xm = 0.3*span
                    else:
                        xm = randomMode[1]
                    r  = randomMode[2]
                    #actions[a]['generators'][g] = (randomMode[0],xm,r)
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
            else:
                print('Error: invalid random number generator %s !!!' % (str(randomMode)) )

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
                if random.random() < missingDataProbability:
                    sevalg[x] = -999

    def showObjectives(self):
        print('*------ show objectives -------"')
        for obj in self.objectives:
                                               
            print('%s: %s' % (obj, self.objectives[obj]['name']))
                                               
            for g in self.objectives[obj]['criteria']:
                print('  ', g, self.criteria[g]['name'], self.criteria[g]['weight'])
                                               
            print('  Total weight: %.2f (%d criteria)\n'\
                  % (self.objectives[obj]['weight'],len(self.objectives[obj]['criteria'])))

    def showActions(self,Alphabetic=False):
        """
        *Parameter*:
            * Alphabetic=False
            
        """
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
class cRandomCBPerformanceTableau(cPerformanceTableau):
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
        * missingDataProbability := x in ]0.0-1.0[ (0.05 default), probability that an action x criterion evaluation is missing.

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
                 float missingDataProbability = 0.05,\
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
        self.randomSeed = seed
        import random
        random.seed(seed)

        # generate actions
        nd = len(str(numberOfActions))
        actionsTypesList = ['cheap','neutral','advantageous']        
        actions = OrderedDict()
        for i in range(1,numberOfActions+1):
            actionType = random.choice(actionsTypesList)
            actionName = ('#%%0%dd' % (nd)) % (i)
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
                    evaluation[g][x] = -999

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
                    if evx != -999:
                        for y in actions.keys():
                            evy = self.evaluation[g][y]
                            if x != y and evy != -999:
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
class cNormalizedPerformanceTableau(cPerformanceTableau):
    """
    specialsation of the cPerformanceTableau class for
    constructing normalized, 0 - 100, valued PerformanceTableau
    instances from a given argPerfTab instance.

    *Parameters*:
        * argPerfTab=None,
        * lowValue=0.0,
        * highValue=100.0,
        * coalition=None,
        * Debug=False
        
    """
    def __init__(self,argPerfTab=None,float lowValue=0.0,float highValue=100.0,coalition=None,bint Debug=False):
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
        recode the evaluations between lowValue and highValue on all criteria.

        *Parameters*:
            * lowValue=0.0,
            * highValue=100.0,
            * Debug=False
            
        """
        cdef int x
        cdef float amplitude
        from decimal import Decimal
        criteria = self.criteria
        actions = self.actions
        evaluation = self.evaluation
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
                if evaluation[g][x] != -999:
                    evalx = abs(evaluation[g][x])
                    if Debug:
                        print(evalx)
                    try:
                        if criteria[g]['preferenceDirection'] == 'min':
                            sign = -1
                        else:
                            sign = 1
                        normEvaluation[g][x] = (lowValue + ((evalx-glow)/gamp)*amplitude)*sign
                    except:
                        self.criteria[g]['preferenceDirection'] = 'max'
                        normEvaluation[g][x] = lowValue + ((evalx-glow)/gamp)*amplitude
                        
                    if Debug:
                        print(criteria[g]['preferenceDirection'], evaluation[g][x], normEvaluation[g][x])
                else:
                    normEvaluation[g][x] = -999
                    
        return normEvaluation

#############################
