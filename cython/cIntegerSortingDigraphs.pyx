#!/usr/bin/env python3
"""
c-Extension for the Digraph3 collection.
Module cIntegerSortingDigraphs.py is a c-compiled part of the
:py:mod:`sortingDigraphs` module for sorting with cIntegerOutrankingDigraphs ressources.  

Copyright (C) 2018  Raymond Bisdorff

"""
#######################
#import cython

from digraphs import *
from cIntegerOutrankingDigraphs import *
from cIntegerSortingDigraphs import *


      
class IntegerQuantilesSortingDigraph(IntegerBipolarOutrankingDigraph):
    """
    *Parameters*:
        * argPerfTab=None,
        * limitingQuantiles=4,
        * LowerClosed=False,
        * PrefThresholds=True,
        * hasNoVeto=False,
        * outrankingType = "bipolar",
        * CompleteOutranking = False,
        * StoreSorting=False,
        * CopyPerfTab=False,
        * Threading=False,
        * tempDir=None,
        * nbrCores=None,
        * nbrOfProcesses=None,
        * Comments=False,
        * Debug=False.

    Cythonized c-Extension of the :py:class:`sortingDigraphs.QuantilesSortingDigraph` class  for the sorting of very large sets of alternatives into quantiles delimited ordered classes.

    A :py:class:`cIntegerOutrankingDigraphs.IntegerBipolarOutrankingDigraph` class specialisation.
   
    .. note::

        We generally require an PerformanceTableau instance or a valid filename.
        If no limitingQuantiles parameter quantity is given, a default profile with the limiting quartiles Q0,Q1,Q2, Q3 and Q4 is used on each criteria. 

        By default, upper closed limits of categories are used in the sorting algorithm.

    Example Python session:
        >>> from cRandPerfTabs import *
        >>> t = RandomPerformanceTableau(numberOfActions=25)
        >>> from cIntegerSortingDigraphs import *
        >>> so = IntegerQuantilesSortingDigraph(t,limitingQuantiles='quintiles')
        >>> so.showSorting()
        *--- Sorting results in descending order ---*
        ]0.80 - 1.00]: 	 [10, 17, 23, 24]
        ]0.60 - 0.80]: 	 [0, 2, 4, 5, 6, 10, 11, 12, 17, 19, 23]
        ]0.40 - 0.60]: 	 [1, 2, 3, 8, 9, 12, 13, 14, 16, 18, 19, 20, 21, 22]
        ]0.20 - 0.40]: 	 [7, 13, 15, 20]
        ]< - 0.20]: 	 []
        >>> so.showSorting(Reverse=False)
        *--- Sorting results in ascending order ---*
        ]< - 0.20]: 	 []
        ]0.20 - 0.40]: 	 [7, 13, 15, 20]
        ]0.40 - 0.60]: 	 [1, 2, 3, 8, 9, 12, 13, 14, 16, 18, 19, 20, 21, 22]
        ]0.60 - 0.80]: 	 [0, 2, 4, 5, 6, 10, 11, 12, 17, 19, 23]
        ]0.80 - 1.00]: 	 [10, 17, 23, 24]
        >>> so.showQuantileOrdering(strategy='average')
        ]0.80-1.00] : [24]
        ]0.60-1.00] : [10, 17, 23]
        ]0.60-0.80] : [0, 4, 5, 6, 11]
        ]0.40-0.80] : [2, 12, 19]
        ]0.40-0.60] : [1, 3, 8, 9, 14, 16, 18, 21, 22]
        ]0.20-0.60] : [13, 20]
        ]0.20-0.40] : [7, 15]

    """
    def __init__(self,argPerfTab=None,\
                 limitingQuantiles=4,\
                 bint LowerClosed=False,\
                 bint PrefThresholds=True,\
                 bint hasNoVeto=False,\
                 outrankingType = "bipolar",\
                 #bint IntegerValued=True,\
                 #WithSortingRelation=False,\
                 bint CompleteOutranking = False,\
                 bint StoreSorting=False,\
                 bint CopyPerfTab=False,\
                 bint AddProfiles2Actions=False,\
                 bint Threading=False,\
                 tempDir=None,\
                 nbrCores=None,\
                 bint Comments=False,
                 bint Debug=False):
        """
        Constructor for IntegerQuantilesSortingDigraph instances.

        """
        cdef int k, i, ox, totalWeight = 0
        cdef double tt,t0
        cdef float q, lowValue=0.0, highValue=100.0
        from cRandPerfTabs import cNormalizedPerformanceTableau
        global actions
        global criteria
        global evaluation
        global valuationdomain
        global categories
        global profiles
        
        
        from time import time
        from copy import deepcopy
        # if CopyPerfTab:
        #     copy2self = deepcopy
        # else:
        #     copy2self = copy
        #from decimal import Decimal

        tt = time()
        # import the performance tableau
        if argPerfTab == None:
            print('Error: a valid performance tableau is required!')
        else:
            perfTab = argPerfTab
        # normalize the actions as a dictionary construct
        if isinstance(perfTab.actions,list):
            actions = OrderedDict()
            for ox in perfTab.actions:
                actions[x] = {'name': str(ox)}
        else:
            if CopyPerfTab:
                actions = deepcopy(perfTab.actions)
            else:
                actions = perfTab.actions
        self.actions = actions

        # keep a copy of the original actions set before adding the profiles
        #actionsOrig = OrderedDict(actions)
        #actionsOrig = [x for x in self.actions]
        #self.actionsOrig = actionsOrig

        #  normalizing the performance tableau
        #normPerfTab = cNormalizedPerformanceTableau(perfTab)
        normPerfTab = perfTab

        # instantiating the performance tableau part
        criteria = normPerfTab.criteria
        #if IntegerValued:
        for g in criteria:
            criteria[g]['weight'] = int(criteria[g]['weight'])
            totalWeight += criteria[g]['weight']
        self.criteria = criteria
        self.totalWeight = totalWeight
        #self.convertWeightFloatToDecimal()
        evaluation = normPerfTab.evaluation
        self.evaluation = evaluation
        #self.convertEvaluationFloatToDecimal()
        self.runTimes = {'dataInput': time()-tt}

        t0 = time()
        #  compute the limiting quantiles
        if isinstance(limitingQuantiles,list):
            self.name = 'sorting_with_given_quantiles'
            newLimitingQuantiles = []
            for q in limitingQuantiles:
                newLimitingQuantiles.append(q)
            limitingQuantiles = newLimitingQuantiles
            if Debug:
                print('convert to decimal!',limitingQuantiles)
        else:
            limitingQuantiles = self._computeQuantiles(limitingQuantiles,Debug=Debug)
        self.limitingQuantiles = limitingQuantiles

        if Debug:
            print('limitingQuantiles',self.limitingQuantiles)

        self.runTimes['computeLimits'] = time() - t0

        t0 = time()
        # supposing all criteria scales between 0.0 and 100.0
        # with preference direction = max
        self.LowerClosed = LowerClosed
        #lowValue = 0.0
        #highValue = 100.00
        categories = OrderedDict()
        k = len(limitingQuantiles)-1
        if LowerClosed:
            #for i in range(0,k-1):
            for i from 0 <= i < (k-1):
                categories[str(i+1)] = {'name':'[%.2f - %.2f['\
                %(limitingQuantiles[i],limitingQuantiles[i+1]),\
                                'order':i+1,\
                                'lowLimit': '[%.2f' % (limitingQuantiles[i]),
                                        'highLimit': '%.2f[' % (limitingQuantiles[i+1]),
                                'lowLimitValue': '%.2f' % (limitingQuantiles[i]),
                                'highLimitValue': '%.2f' % (limitingQuantiles[i+1])}
            categories[str(k)] = {'name':'[%.2f - <['\
                %(limitingQuantiles[k-1]), 'order':k,\
                                  'lowLimit': '[%.2f' % (limitingQuantiles[k-1]),\
                                  'highLimit': '<[',                
                                  'lowLimitValue': '%.2f' % (limitingQuantiles[k-1]),\
                                  'highLimitValue': '%.2f' % (limitingQuantiles[k]) }                 
        else:
            categories[str(1)] = {'name':']< - %.2f]'\
                %(limitingQuantiles[1]), 'order':1,
                    'highLimit': '%.2f]' % (limitingQuantiles[1]),\
                                  'lowLimit': ']<',                                  
                    'highLimitValue': '%.2f' % (limitingQuantiles[1]),\
                    'lowLimitValue': '%.2f' % (limitingQuantiles[0])}                                  
            #for i in range(1,k):
            for i from 1 <= i < k:
                categories[str(i+1)] = {'name':']%.2f - %.2f]'\
                %(limitingQuantiles[i],limitingQuantiles[i+1]), 'order':i+1,
                        'lowLimit': ']%.2f' % (limitingQuantiles[i]),
                                        'highLimit': '%.2f]' % (limitingQuantiles[i+1]),
                        'lowLimitValue': '%.2f' % (limitingQuantiles[i]),
                        'highLimitValue': '%.2f' % (limitingQuantiles[i+1])}
        self.categories = categories
        if Debug:
            print('categories',self.categories)
            print('list',list(dict.keys(categories)))

        criteriaCategoryLimits = {}
        criteriaCategoryLimits['LowerClosed'] = LowerClosed
        self.criteriaCategoryLimits = criteriaCategoryLimits
        for g in dict.keys(criteria):
            gQuantiles = self._computeLimitingQuantiles(g,\
                            PrefThresholds=PrefThresholds,Debug=Debug)
##            if Debug:
##                print(g,gQuantiles)
            criteriaCategoryLimits[g] = gQuantiles
##            for c in categories:
##                criteriaCategoryLimits[g][c]={
##                    'minimum':gQuantiles[(int(c)-1)],
##                    'maximum':gQuantiles[int(c)]
##                    }
        self.criteriaCategoryLimits = criteriaCategoryLimits
        if Debug:
            print('CriteriaCategoryLimits',criteriaCategoryLimits)

        self.runTimes['categories'] = time() - t0

        # set the category limits type (LowerClosed = True is default)
        # self.criteriaCategoryLimits['LowerClosed'] = LowerClosed
        # print 'LowerClosed', LowerClosed

        t0 = time()
        # add the catogory limits to the actions set
        profiles = OrderedDict()
        #profileLimits = set()
        for c in categories:
            if LowerClosed:
                cKey = c+'-m'
            else:
                cKey = c+'-M'
            #profileLimits.add(cKey)
            if LowerClosed:
                if AddProfiles2Actions:
                    actions[cKey] = {'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            else:
                if AddProfiles2Actions:
                    actions[cKey] = {'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            for g in dict.keys(criteria):
                if LowerClosed:
                    evaluation[g][cKey] = criteriaCategoryLimits[g][int(c)-1]
                else:
                    evaluation[g][cKey] = criteriaCategoryLimits[g][int(c)]

        self.profiles = profiles
        profileLimits = list(profiles.keys())
        #profileLimits.sort()
        self.profileLimits = profileLimits
        
        if Debug:
            print('self.profiles',profiles)
            print('self.profileLimits',profileLimits)
            
        #self.convertEvaluationFloatToDecimal()
        self.runTimes['computeProfiles'] = time() - t0

        t0 = time()
        # construct outranking relation
        self.hasNoVeto = hasNoVeto
        Min = -totalWeight
        Max = totalWeight
        Med = 0
        valuationdomain = {'min': Min, 'med':Med ,'max':Max }
        self.valuationdomain = valuationdomain

        if LowerClosed:
            initialArg = actions
            terminalArg = profiles
        else:
            initialArg  = profiles
            terminalArg = actions
        self.relation = self._constructRelationWithThreading(
                                                   #criteria, global
                                                   #evaluation, global
                                                   initial=initialArg,
                                                   terminal=terminalArg,
                                                   hasNoVeto=hasNoVeto,
                                                   hasBipolarVeto=True,
                                                   WithConcordanceRelation=False,
                                                   WithVetoCounts=False,       
                                                    Threading=Threading,
                                                        tempDir=tempDir,
                                                    nbrCores=nbrCores,
                                                    Comments=Comments,
                                                    #WithSortingRelation=WithSortingRelation,
                                                    StoreSorting=StoreSorting)
            
        self.runTimes['computeRelation'] = time() - t0

        # restore original actions set
        #actions = [x for x in self.actions if x not in self.profiles]
        #perfTab.actions = actions
        #self.actions = actions
        self.order = len(self.actions)

        self.runTimes['totalTime'] = time() - tt

### --------  class methods

    def __repr__(self):
        """
        Default presentation method for IntegerQuantilesSortingDigraph instance.
        """
        String =  '*-----  Object instance description -----------*\n'
        String += 'Instance class      : %s\n' % self.__class__.__name__
        String += 'Instance name       : %s\n' % self.name
        String += '# Actions           : %d\n' % len(self.actions)
        String += '# Criteria          : %d\n' % len(self.criteria)
        String += '# Quantile profiles : %d\n' % len(self.profiles)
        String += 'Attributes: %s\n' % list(self.__dict__.keys())
        String += '*------  Constructor run times (in sec.) ------*\n'
        try:
            String += '#Threads         : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            String += '#Threads         : %d\n' % self.nbrThreads
        String += 'Total time       : %.5f\n' % self.runTimes['totalTime']
        String += 'Data input       : %.5f\n' % self.runTimes['dataInput']
        String += 'Quantile limits  : %.5f\n' % self.runTimes['computeLimits']
        String += 'Quantile classes : %.5f\n' % self.runTimes['categories']
        String += 'Limit profiles   : %.5f\n' % self.runTimes['computeProfiles']
        String += 'Sorting relation : %.5f\n' % self.runTimes['computeRelation']
        return String 

    def _constructRelationWithThreading(self,
                           #criteria,\ global
                           # evaluation,\ global
                           initial=None,\
                           terminal=None,\
                           bint hasNoVeto=False,\
                           bint hasBipolarVeto=True,\
                           bint Debug=False,\
                           bint hasSymmetricThresholds=True,\
                           bint Threading=False,\
                           tempDir=None,\
                           bint WithConcordanceRelation=False,\
                           bint WithVetoCounts=False,\
                           StoreSorting=True,\
                           nbrCores=None,Comments=False):
        """
        Specialization of the corresponding BipolarOutrankingDigraph method
        """
        cdef int n, ns, nq, ni, nt, nbrOfJobs, nit, i, j, Min, Max, Med
        cdef bint LowerClosed, InitialSplit
        global actions
        global criteria
        global evaluation
        global valuationdomain
        global categories
        global profiles
        
        from array import array        
        from multiprocessing import cpu_count
        from cIntegerOutrankingDigraphs import IntegerBipolarOutrankingDigraph
        
        LowerClosed = self.criteriaCategoryLimits['LowerClosed']        

        if not Threading or cpu_count() < 2:
            # set parameters for non threading
            self.nbrThreads = 1
            Min = valuationdomain['min']
            Med = valuationdomain['med']
            Max = valuationdomain['max']
            

            # compute sorting relation
            # !! concordance relation and veto counts need a complex constructor
            ## if (not hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
            ##     constructRelation = self._constructRelation
            ## else:
            constructRelation = IntegerBipolarOutrankingDigraph._constructRelationSimple

            relation = constructRelation(self,
                                    criteria,\
                                    evaluation,\
                                    initial=initial,\
                                    terminal=terminal,\
                                    hasNoVeto=hasNoVeto,\
                                    hasBipolarVeto=hasBipolarVeto,\
                                    Debug=Debug,\
                                    hasSymmetricThresholds=hasSymmetricThresholds)

            # compute quantiles sorting result
            if LowerClosed:
                actions = initial
            else:
                actions = terminal
            categories = self.categories.keys()
            sorting = {}
            nq = len(self.limitingQuantiles) - 1
            for x in actions:
                sorting[x] = {}
                for c in categories:
                    sorting[x][c] = {}
                    if LowerClosed:
                        cKey= c+'-m'
                    else:
                        cKey= c+'-M'
                    if LowerClosed:
                        lowLimit = relation[x][cKey]
                        if int(c) < nq:
                            cMaxKey = str(int(c)+1)+'-m'
                            notHighLimit = Max - relation[x][cMaxKey] + Min
                        else:
                            notHighLimit = Max
                    else:
                        if int(c) > 1:
                            cMinKey = str(int(c)-1)+'-M'
                            lowLimit = Max - relation[cMinKey][x] + Min
                        else:
                            lowLimit = Max
                        notHighLimit = relation[cKey][x]
                    categoryMembership = min(lowLimit,notHighLimit)
                    sorting[x][c]['lowLimit'] = lowLimit
                    sorting[x][c]['notHighLimit'] = notHighLimit
                    sorting[x][c]['categoryMembership'] = categoryMembership

            if StoreSorting:
                self.sorting = sorting

            # compute category contents
            categoryContent = {}
            for c in self.orderedCategoryKeys():
                categoryContent[c] = []
                for x in actions:
                    if sorting[x][c]['categoryMembership'] >= Med:
                        categoryContent[c].append(x)
            self.categoryContent = categoryContent

            return relation
            
        ##
        else:  # parallel computation
            from copy import copy, deepcopy
            from io import BytesIO
            from pickle import Pickler, dumps, loads, load
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            #Debug=True
            class myThread(Process):
                def __init__(self, int threadID,digraph,\
                             bint InitialSplit, tempDirName,\
                             splitActions,\
                             bint hasNoVeto=False,
                             bint hasBipolarVeto=True,\
                             bint hasSymmetricThresholds=True,
                             bint Debug=False):
                    
                    Process.__init__(self)
                    self.threadID = threadID
                    self.digraph = digraph
                    self.InitialSplit = InitialSplit
                    self.workingDirectory = tempDirName
                    self.splitActions = splitActions
                    self.hasNoVeto = hasNoVeto
                    self.hasBipolarVeto = hasBipolarVeto,
                    self.hasSymmetricThresholds = hasSymmetricThresholds,
                    self.Debug = Debug

                def run(self):

                    cdef int x, nq, Min, Med, Max, lowLimit, notHighLimit
                    cdef bint LowerClosed
                    global actions
                    global criteria
                    global evaluation
                    global valuationdomain
                    global categories
                    global profiles

                    from io import BytesIO
                    from pickle import Pickler, dumps, loads
                    from os import chdir
                    from array import array
                    from cIntegerOutrankingDigraphs import IntegerBipolarOutrankingDigraph
                    
                    chdir(self.workingDirectory)
##                    if Debug:
##                        print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadId)))
                    #fi = open('dumpSelf.py','rb')
                    #digraph = loads(fi.read())
                    #fi.close()
                    Min = valuationdomain['min']
                    Med = valuationdomain['med']
                    Max = valuationdomain['max']
                    splitActions = self.splitActions
                    constructRelation = IntegerBipolarOutrankingDigraph._constructRelationSimple
                    if self.InitialSplit:
                        initialIn = splitActions
                        terminalIn = profiles
                    else:
                        initialIn = profiles
                        terminalIn = splitActions
                    splitRelation = constructRelation(self.digraph,criteria,evaluation,\
                                            initial=initialIn,\
                                            terminal=terminalIn,\
                                            hasNoVeto=self.hasNoVeto,\
                                            hasBipolarVeto=self.hasBipolarVeto,\
                                            Debug=False,\
                                            hasSymmetricThresholds=self.hasSymmetricThresholds)
                    foName = 'splitRelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitRelation,-1))
                    fo.close()
                    # compute quantiles sorting result
                    LowerClosed = self.digraph.criteriaCategoryLimits['LowerClosed']
                    nq = len(self.digraph.limitingQuantiles) - 1
                    categories = self.digraph.categories.keys()
                    sorting = {}
                    nq = len(self.digraph.limitingQuantiles) - 1
                    for x in splitActions:
                        sorting[x] = {}
                        for c in categories:
                            sorting[x][c] = {}
                            if LowerClosed:
                                cKey= c+'-m'
                            else:
                                cKey= c+'-M'
                            if LowerClosed:
                                lowLimit = splitRelation[x][cKey]
                                if int(c) < nq:
                                    cMaxKey = str(int(c)+1)+'-m'
                                    notHighLimit = Max - splitRelation[x][cMaxKey] + Min
                                else:
                                    notHighLimit = Max
                            else:
                                if int(c) > 1:
                                    cMinKey = str(int(c)-1)+'-M'
                                    lowLimit = Max - splitRelation[cMinKey][x] + Min
                                else:
                                    lowLimit = Max
                                notHighLimit = splitRelation[cKey][x]
                            categoryMembership = min(lowLimit,notHighLimit)
                            sorting[x][c]['lowLimit'] = lowLimit
                            sorting[x][c]['notHighLimit'] = notHighLimit
                            sorting[x][c]['categoryMembership'] = categoryMembership

                    if StoreSorting:
                        #self.sorting = sorting
                        foName = 'splitSorting-'+str(self.threadID)+'.py'
                        fo = open(foName,'wb')
                        fo.write(dumps(sorting,-1))
                        fo.close()

                    # compute category contents
                    categoryContent = {}
                    for c in self.digraph.orderedCategoryKeys():
                        categoryContent[c] = array('i')
                        for x in splitActions:
                            if sorting[x][c]['categoryMembership'] >= Med:
                                categoryContent[c].append(x)

                    #self.categoryContent = categoryContent
                    foName = 'splitCategoryContent-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(categoryContent,-1))
                    fo.close()
                    
                # .......
             
            if Comments:
                print('Threading ...')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                from copy import copy, deepcopy

                # #selfDp = copy(self)
                # selfFileName = tempDirName +'/dumpSelf.py'
                # if Debug:
                #     print('temDirName, selfFileName', tempDirName,selfFileName)
                # fo = open(selfFileName,'wb')
                # fo.write(dumps(self,-1))
                # fo.close()

                if nbrCores == None:
                    nbrCores = cpu_count()
                if Comments:
                    print('Nbr of cpus = ',nbrCores)
                # set number of threads
                self.nbrThreads = nbrCores
                actions2Split = array('i')
                ni = len(initial)
                nt = len(terminal)
                if LowerClosed:
                    n = ni
                    actions2Split.extend(initial)
                    InitialSplit = True
                else:
                    n = nt
                    actions2Split.extend(terminal)
                    InitialSplit = False
##                if Debug:
##                    print('InitialSplit, actions2Split', InitialSplit, actions2Split)
            
                nit = n//nbrCores
                nbrOfJobs = nbrCores
                if nit*nbrCores < n:
                    nit += 1
                while nit*(nbrOfJobs-1) >= n:
                    nbrOfJobs -= 1
                if Comments:
                    print('nbr of actions to split',n)
                    print('nbr of jobs = ',nbrOfJobs)    
                    print('nbr of splitActions = ',nit)

                relation = {}
                Med = valuationdomain['med']
                for ix in initial:
                    relation[ix] = {}
                    rx = relation[ix]
                    for iy in terminal:
                        rx[iy] = Med
                i = 0
                actionsRemain = set(actions2Split)
                splitActionsList = []
                #for j in range(nbrOfJobs):
                for j from 0 <= j < nbrOfJobs:
                    if Comments:
                        print('Thread = %d/%d' % (j+1,nbrOfJobs),end=" ")
                    splitActions=[]
                    #for k in range(nit):
                    for k from 0 <= k < nit:
                        if j < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = array('i',list(actionsRemain))
                        i += 1
                    if Comments:
                        print('%d' % (len(splitActions)) )
##                    if Debug:
##                        print(splitActions)
                    actionsRemain = actionsRemain - set(splitActions)
##                    if Debug:
##                        print(actionsRemain)
                    splitActionsList.append(splitActions)
##                    foName = tempDirName+'/splitActions-'+str(j)+'.py'
##                    fo = open(foName,'wb')
##                    spa = dumps(splitActions,-1)
##                    fo.write(spa)
##                    fo.close()
                    splitThread = myThread(j,self,InitialSplit,
                                           tempDirName,splitActions,
                                           hasNoVeto,hasBipolarVeto,
                                           hasSymmetricThresholds,Debug)
                    splitThread.start()
##                    splitThread.join()
                    
                while active_children() != []:
                    pass

                if Comments:    
                    print('Exiting computing threads')
                sorting = {}
                categoryContent = {}
                relation = {}
                ns = len(splitActionsList)
                #for j in range(len(splitActionsList)):
                for j from 0 <= j < ns:
                    # update category contents
                    fiName = tempDirName+'/splitCategoryContent-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitCategoryContent = loads(fi.read())
                    categoryContent.update(splitCategoryContent)
                    # update sorting result
                    if StoreSorting:
                        fiName = tempDirName+'/splitSorting-'+str(j)+'.py'
                        fi = open(fiName,'rb')
                        splitSorting = loads(fi.read())
                        sorting.update(splitSorting)
                    ## if Comments:
                    ##     print('Collect result ',j)
                self.categoryContent = categoryContent
                if StoreSorting:
                    self.sorting = sorting
                
    def showActionCategories(self,int action,bint Debug=False,bint Comments=True,\
                             bint Threading=False,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !

        *Parameters*:
            * action key (int),
            * Debug = False | True,
            * Comments = True | False,
            * Threading = False | True
            * nbrOfCPUs = None.

        """
        Med = self.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,\
                                                     Comments=Debug,\
                                                     Threading=Threading,
                                                     StoreSorting=False,
                                                     nbrOfCPUs=nbrOfCPUs)
        catKeys = self.orderedCategoryKeys()
        lowLimit = sorting[action][catKeys[0]]['lowLimit']
        notHighLimit = sorting[action][catKeys[-1]]['notHighLimit']
        keys = [catKeys[0],catKeys[-1]]  # action is sorted by default in all categories 
        for c in self.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                    keys[0] = c  # the highest lowLimit is remembered
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                    keys[1] = c  # the highest notHighLimit (lowest HigLimit) is remembered
                if Debug:
                    print(action, c, sorting[action][c],keys)
        credibility = min(lowLimit,notHighLimit)
        if Comments:
            print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                 self.categories[keys[0]]['name'],\
                                 self.categories[keys[1]]['name'],\
                                 action,\
                                 credibility,lowLimit,notHighLimit) )
        return action,\
                keys[0],\
                keys[1],\
                credibility            

    def showActionsSortingResult(self,actionSubset=None,bint Debug=False):
        """
        Shows the quantiles sorting result of all (default) or a subset of the decision actions.

        *Parameters*:
            * actionSubset = None,
            * Debug=False.

        """
        if actionSubset == None:
            actions = self.actions
            actions.sort()
        else:
            actions = [x for x in flatten(actionSubset)]
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showActionCategories(x,Debug=Debug)
 

    def showWeakOrder(self,Descending=True):
        """
        *Parameter*:
            * Descending=True.

        """
        from decimal import Decimal
        from weakOrders import WeakOrder
        try:
            cC = self.categoryContent
        except:
            cC = self.computeCategoryContents(StoreSorting=True)
        
        if Descending:
            cCKeys = self.orderedCategoryKeys(Reverse = True)
        else:
            cCKeys = self.orderedCategoryKeys(Reverse = False)
        n = len(cC)
        n2 = n//2
        ordering = []
        
        for i in range(n2):
            if i == 0:
                x = cC[cCKeys[i]]
                y = cC[cCKeys[n-i-1]]
                setx = set(x)
                sety = set(y) - setx
            else:
                x = list(set(cC[cCKeys[i]]) - (setx | sety))
                setx = setx | set(x)
                y = list(set(cC[cCKeys[n-i-1]]) - (setx | sety))
                sety = sety | set(y)
            if x != [] or y != []:
                ordering.append( ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ) )
        if 2*n2 < n:
            if n2 == 0:
                x = cC[cCKeys[n2]]
            else:
                x = list(set(cC[cCKeys[n2]]) - (setx | sety))
            ordering.append( ( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),x) ) )
        
        weakOrdering = {'result':ordering}

        WeakOrder.showWeakOrder(self,weakOrdering)


    def _computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                Debug=False,
                                     Threading=False,
                                     nbrOfCPUs=None):
        """
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order,
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
              in the uppest, the lowest or the average potential quantile,
            * Debug=False,
            * Threading=False,
            * nbrOfCPUs=None.
        
        """
        if strategy == None:
            try:
                strategy = self.sortingParameters['strategy']
            except:
                strategy = 'average'
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug,\
                            Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            if strategy == "optimistic":
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(int(lowCateg),int(highCateg))].append(a)
                except:
                    actionsCategories[(int(lowCateg),int(highCateg))] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))] = [a]
            else:  # optimistic by default
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]      
                
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)

        return actionsCategIntervals


    def computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                HTML=False,
                                Comments=False,
                                Debug=False):
        """
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order,
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average'(default) }
              in the uppest, the lowest or the average potential quantile,
            * HTML = False | True (for generating a HTML version of the result),
            * Comments = False| True,
            * Debug = False | True.
        
        """
        if strategy == None:
            strategy = 'average'
        if HTML:
            html = '<h1>Quantiles preordering</h1>'
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>quantile limits</th>'
            html += '<th>%s sorting</th>' % strategy
            html += '</tr>'
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            if strategy == "optimistic":
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(int(lowCateg),int(highCateg))].append(a)
                except:
                    actionsCategories[(int(lowCateg),int(highCateg))] = [a]
            elif strategy == "average":
                lc = int(lowCateg)
                hc = int(highCateg)
                ac = (lc+hc)
                try:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))] = [a]
            else:  # optimistic by default
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]      
                
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)
        weakOrdering = []
        for item in actionsCategIntervals:
            #print(item)
            if Comments:
                if strategy == "optimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><tdbgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])                            
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                elif strategy == "pessimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])

                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )                   
                elif strategy == "average":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][2])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
            weakOrdering.append(item[1])
        if HTML:
            html += '</table>'
            return html
        else:
            return weakOrdering

    def showQuantileOrdering(self,strategy=None):
        """
        *Parameter*:
            * strategy=None ('average' by default').

        Dummy show method for the commenting computeQuantileOrdering() method.
        """
        self.computeQuantileOrdering(strategy=strategy,Comments=True)


    def computeWeakOrder(self,Descending=True,Debug=False):
        """
        *Parameters*:
            * Descending=True,
            * Debug=False.

        Specialisation for QuantilesSortingDigraphs.
        """
        from decimal import Decimal
        try:
            cC = self.categoryContent
        except:
            cC = self.computeCategoryContents(StoreSorting=True)
        if Debug:
            print(cC)
        if Descending:
            cCKeys = self.orderedCategoryKeys(Reverse = True)
        else:
            cCKeys = self.orderedCategoryKeys(Reverse = False)
        if Debug:
            print('cCKeys',cCKeys)
        n = len(cC)
        n2 = n//2
        if Debug:
            print('n,n2',n,n2)
        ordering = []
        
        for i in range(n2):
            if i == 0:
                x = cC[cCKeys[i]]
                y = cC[cCKeys[n-i-1]]
                setx = set(x)
                sety = set(y) - setx
            else:
                x = list(set(cC[cCKeys[i]]) - (setx | sety))
                setx = setx | set(x)
                y = list(set(cC[cCKeys[n-i-1]]) - (setx | sety))
                sety = sety | set(y)
            if Debug:
                print('i,x,y,setx,sety',i,x,y,setx,sety)
            if x != [] or y != []:
                ordering.append( ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ))
            if Debug:
                print(i, ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ) )
        if 2*n2 < n:
            if n2 == 0:
                x = cC[cCKeys[n2]]
            else:
                x = list(set(cC[cCKeys[n2]]) - (setx | sety))
            ordering.append( ( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),[]) ) )
            if Debug:
                print('median term',( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),[]) ))
        if Debug:
            print(ordering)
        
        orderingList = []
        n = len(ordering)
        for i in range(n):
            x = ordering[i][0][1]
            if x != []:
                orderingList.append(x)
        for i in range(n):
            y = ordering[n-i-1][1][1]
            if y != []:
                orderingList.append(y)

        return orderingList

    def showOrderedRelationTable(self,direction="decreasing"):
        """
        *Parameter*:
            * direction = "decreasing" | "increasing".

        Showing the relation table in decreasing (default) or increasing order.
        """
        if direction == "decreasing":
            Descending = True
        else:
            Descending = False

        weakOrdering = self.computeWeakOrder(Descending)
        
        actionsList = []
        for eq in weakOrdering:
            #print(eq)
            eq.sort()
            for x in eq:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error !: missing action(s) %s in ordered table.')
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=self.relation,\
                                Sorted=False,\
                                ReflexiveTerms=False)
        

    def _computeQuantiles(self,x,bint Debug=False):
        """
        renders the limiting quantiles
        """
        from math import floor
        if isinstance(x,int):
            n = x
        elif x == None:
            n = 4
        elif x == 'bitiles':
            n = 2
        elif x == 'tritiles':
            n = 3
        elif x == 'quartiles':
            n = 4
        elif x == 'quintiles':
            n = 5
        elif x == 'sextiles':
            n = 6
        elif x == 'septiles':
            n = 7
        elif x == 'octiles':
            n = 8
        elif x == 'deciles':
            n = 10
        elif x == 'dodeciles':
            n = 20
        elif x == 'centiles':
            n = 100
        elif x == 'automatic':
            pth = [5]
            for g in self.criteria:
                try:
                    pref = self.criteria[g]['thresholds']['ind'][0] + \
                           (self.criteria[g]['thresholds']['ind'][1]*100.0)
                    pth.append(pref)
                except:
                    pass
            amp = max(1,min(pth))
            n = int(100.0/amp)
            if Debug:
                print('Detected preference thresholds = ',pth)
                print('amplitude, n',amp,n)

        limitingQuantiles = []
        for i in range(n+1):
            limitingQuantiles.append( i / float(n) )
        self.name = 'sorting_with_%d-tile_limits' % n
        return limitingQuantiles
                                         
    def _computeLimitingQuantiles(self,g,bint Debug=False,bint PrefThresholds=True):
        """
        Renders the list of limiting quantiles on criteria g
        """
        from math import floor
        from copy import copy, deepcopy
        LowerClosed = self.criteriaCategoryLimits['LowerClosed']
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
                gPrefThrCst = 0.0
                gPrefThrSlope = 0.0            
        n = len(gValues)
        if Debug:
            print('g,n,gValues',g,n,gValues)
##        if n > 0:
##        nf = Decimal(str(n+1))
        #nf = Decimal(str(n))
        nf = float(n)
        limitingQuantiles = copy(self.limitingQuantiles)
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
            # we ignore the 1.00 quantile and replace it with +infty
            for q in self.limitingQuantiles:
                r = (nf * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq < (n-1):
                    quantile = gValues[rq]\
                        + ( (r-rq)*(gValues[rq+1]-gValues[rq]) )
                    if rq > 0 and PrefThresholds:
                        quantile += gPrefThrCst + quantile*gPrefThrSlope
                else :
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        quantile = 100.0
                    else:
                        quantile = 200.0
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)               

        else:  # upper closed categories
            # we ignore the quantile 0.0 and replace it with -\infty            
            for q in self.limitingQuantiles:
                r = (nf * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq == 0:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        quantile = -200.0
                    else:
                        quantile = -100.0
                elif rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-rq)*(gValues[rq+1]-gValues[rq]))
                    if PrefThresholds:
                        quantile -= gPrefThrCst - quantile*gPrefThrSlope
                else:
                    if n > 0:
                        quantile = gValues[n-1]
                    else:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            quantile = -200.0
                        else:
                            quantile = -100.0     
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)
##        else:
##            gQuantiles = []
        if Debug:
            print(g,LowerClosed,self.criteria[g]['preferenceDirection'],gQuantiles)
        return gQuantiles

    def getActionsKeys(self,action=None,bint withoutProfiles=True):
        """
        *Parameters*:
            * action=None,
            * withoutProfiles=True.
 
        Extract normal actions keys()
        """
        profiles = set([x for x in list(self.profiles.keys())])
        if action == None:
            actionsExt = set([x for x in list(self.actions.keys())])
            if withoutProfiles:
                return actionsExt - profiles
            else:
                return actionsExt | profiles
        else:
            return set([action])           

    def orderedCategoryKeys(self,bint Reverse=False):
        """
        *Parameter*:
            * Reverse=False.

        Renders the ordered list of category keys
        based on self.categories['order'] numeric values.
        """
        orderedCategoryKeys = list(self.categories.keys())
        if Reverse:
            orderedCategoryKeys.reverse()
        return orderedCategoryKeys

    def computeCategoryContents(self,bint Reverse=False,bint Comments=False,bint StoreSorting=True,\
                                Threading=False,nbrOfCPUs=None):
        """
        *Parameters*:
            *  Reverse=False,
            * Comments=False,
            * StoreSorting=True,
            * Threading=False,
            * nbrOfCPUs=None.

        Computes the sorting results per category.
        """
        cdef int x
        actions = list(self.getActionsKeys())
        actions.sort()
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(Comments=Comments,\
                                                     StoreSorting=StoreSorting,\
                                                     Threading=Threading,\
                                                     nbrOfCPUs=nbrOfCPUs)

        categoryContent = {}
        for c in self.orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)
        
        return categoryContent

    def computeSortingCharacteristics(self, action=None,bint Comments=False,\
                                      bint StoreSorting=False,bint Debug=False,\
                                        bint Threading=False, int nbrOfCPUs=1):
        """
        *Parameters*:
            * action=None,
            * Comments=False,
            * StoreSorting=False,
            * Debug=False,
            * Threading=False,
            * nbrOfCPUs=None.

        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        cdef int Min, Max, Med, nbrOfThreads, na
        cdef bint LowerClosed
        
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        try:
            return self.sorting
        except:
            pass
        if action != None:
            storeSorting = False
        actions = list(self.getActionsKeys(action))
        na = len(actions)
##        if Debug:
##            print(actions)
            
        #categories = list(self.orderedCategoryKeys())
        categories = list(self.categories.keys())
        selfRelation = self.relation
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        if Threading and action==None:
            from multiprocessing import Process, active_children
            from pickle import dumps, loads, load
            from os import cpu_count
            from time import time
##            if Comments:
##                self.Debug = True
            class myThread(Process):
                def __init__(self, int threadID, tempDirName,
                             int nq, int Min, int Max, bint LowerClosed, bint Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    #self.actions = actions
                    self.nq = nq
                    self.Min = Min
                    self.Max = Max
                    self.LowerClosed = LowerClosed
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
##                    if self.Debug:
##                        print("Starting working in %s on %s" % (self.workingDirectory, str(self.threadID)))
##                        print('actions,catKeys',self.actions,self.catKeys)
                    fi = open('dumpSelfRelation.py','rb')
                    #context = loads(fi.read())
                    relation = loads(fi.read())
                    fi.close()
                    fi = open('dumpCategories.py','rb')
                    #context = loads(fi.read())
                    catKeys = loads(fi.read())
                    fi.close()
                    fi = open('dumpActions%d.py' % self.threadID,'rb')
                    #context = loads(fi.read())
                    actions = loads(fi.read())
                    fi.close()
##                    Min = context.valuationdomain['min']
##                    Max = context.valuationdomain['max']
                    Min = self.Min
                    Max = self.Max
                    LowerClosed = self.LowerClosed
                    sorting = {}
                    nq = self.nq
                    #nq = len(context.limitingQuantiles) - 1
                    #actions = self.actions
                    #catKeys = self.catKeys
                    #relation = context.relation
                    for x in actions:
                        sorting[x] = {}
                        sorx = sorting[x]
                        for c in catKeys:
                            sorx[c] = {}
                            if LowerClosed:
                                cKey= c+'-m'
                            else:
                                cKey= c+'-M'
                            if LowerClosed:
                                lowLimit = relation[x][cKey]
                                if int(c) < nq:
                                    cMaxKey = str(int(c)+1)+'-m'
                                    notHighLimit = Max - relation[x][cMaxKey] + Min
                                else:
                                    notHighLimit = Max
                            else:
                                if int(c) > 1:
                                    cMinKey = str(int(c)-1)+'-M'
                                    lowLimit = Max - relation[cMinKey][x] + Min
                                else:
                                    lowLimit = Max
                                notHighLimit = relation[cKey][x]
##                            cMinKey= c+'-m'
##                            cMaxKey= c+'-M'
##                            if LowerClosed:
##                                lowLimit = context.relation[x][cMinKey]
##                                notHighLimit = Max - context.relation[x][cMaxKey] + Min
##                            else:
##                                lowLimit = Max - context.relation[cMinKey][x] + Min
##                                notHighLimit = context.relation[cMaxKey][x]
                            if Debug:
                                print('%s in %s: low = %.2f, high = %.2f' % \
                                      (x, c,lowLimit,notHighLimit), end=' ')
                            categoryMembership = min(lowLimit,notHighLimit)
                            sorx[c]['lowLimit'] = lowLimit
                            sorx[c]['notHighLimit'] = notHighLimit
                            sorx[c]['categoryMembership'] = categoryMembership
##                            if self.Debug:
##                                print('\t %.2f \t %.2f \t %.2f\n' % (sorting[x][c]['lowLimit'],\
##                                   sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
##                        if self.Debug:
##                            print(sorting[x])
                    foName = 'sorting-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(sorting,-1))
                    fo.close()
            if Comments:
                print('Threaded computing of sorting characteristics ...')        
            from tempfile import TemporaryDirectory,mkdtemp
            tempDirName = mkdtemp()
            td = time()
            selfFileName = tempDirName +'/dumpSelfRelation.py'
##            if Debug:
##                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            pd = dumps(selfRelation,-1)
            fo.write(pd)
            fo.close()
            selfFileName = tempDirName +'/dumpCategories.py'
##            if Debug:
##                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            pd = dumps(categories,-1)
            fo.write(pd)
            fo.close()            
            if nbrOfCPUs == None:
                nbrOfCPUs = cpu_count()-1
            if Comments:
                print('Dump relation: %.5f' % (time()-td))
                print('Nbr of actions',na)
                
            
            nbrOfJobs = na//nbrOfCPUs
            if nbrOfJobs*nbrOfCPUs < na:
                nbrOfJobs += 1
            if Comments:
                print('Nbr of threads = ',nbrOfCPUs)
                print('Nbr of jobs/thread',nbrOfJobs)
            nbrOfThreads = 0
            nq = len(self.limitingQuantiles) -1
            Max = self.valuationdomain['max']
            Min = self.valuationdomain['min']
            for j in range(nbrOfCPUs):
                if Comments:
                    print('thread = %d/%d' % (j+1,nbrOfCPUs),end="...")
                start= j*nbrOfJobs
                if (j+1)*nbrOfJobs < na:
                    stop = (j+1)*nbrOfJobs
                else:
                    stop = na
                thActions = actions[start:stop]
##                if Debug:
##                    print(thActions)
                if thActions != []:
                    selfFileName = tempDirName +'/dumpActions%d.py' % j
                    fo = open(selfFileName,'wb')
                    pd = dumps(thActions,-1)
                    fo.write(pd)
                    fo.close()            
                    process = myThread(j,tempDirName,nq,Min,Max,
                                       LowerClosed,Debug)
                    process.start()
                    nbrOfThreads += 1
                    #process.join()
                    
            while active_children() != []:
                pass
                #sleep(1)
                
            if Comments:
                print('Exit %d threads' % nbrOfThreads)
            sorting = {}
            for th in range(nbrOfThreads):
##                if Debug:
##                    print('job',th)
                fiName = tempDirName+'/sorting-'+str(th)+'.py'
                fi = open(fiName,'rb')
                sortingThread = loads(fi.read())
##                if Debug:
##                    print('sortingThread',sortingThread)
                sorting.update(sortingThread)
        # end of Threading
        else: # with out Threading 
            sorting = {}
            nq = len(self.limitingQuantiles) - 1
            for x in actions:
                sorting[x] = {}
                for c in categories:
                    sorting[x][c] = {}
                    if LowerClosed:
                        cKey= c+'-m'
                    else:
                        cKey= c+'-M'
                    if LowerClosed:
                        lowLimit = selfRelation[x][cKey]
                        if int(c) < nq:
                            cMaxKey = str(int(c)+1)+'-m'
                            notHighLimit = Max - selfRelation[x][cMaxKey] + Min
                        else:
                            notHighLimit = Max
                    else:
                        if int(c) > 1:
                            cMinKey = str(int(c)-1)+'-M'
                            lowLimit = Max - selfRelation[cMinKey][x] + Min
                        else:
                            lowLimit = Max
                        notHighLimit = selfRelation[cKey][x]
##                    cMinKey= c+'-m'
##                    cMaxKey= c+'-M'
##                    if LowerClosed:
##                        lowLimit = self.relation[x][cMinKey]
##                        notHighLimit = Max - self.relation[x][cMaxKey] + Min
##                    else:
##                        lowLimit = Max - self.relation[cMinKey][x] + Min
##                        notHighLimit = self.relation[cMaxKey][x]
##                    if Debug:
##                        print('%s in %s: low = %.2f, high = %.2f' % \
##                              (x, c,lowLimit,notHighLimit), end=' ')
                    categoryMembership = min(lowLimit,notHighLimit)
                    sorting[x][c]['lowLimit'] = lowLimit
                    sorting[x][c]['notHighLimit'] = notHighLimit
                    sorting[x][c]['categoryMembership'] = categoryMembership

##                    if Debug:
##                        print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
        if StoreSorting:
            self.sorting = sorting
        return sorting

    def showSortingCharacteristics(self, action=None):
        """
        *Parameter*:
            * action=None.

        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,StoreSorting=True)

        actions = self.getActionsKeys(action)
            
        categories = self.orderedCategoryKeys()

        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        if LowerClosed:
            print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
        else:
            print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        for x in actions:
            for c in categories:
                print('%s in %s - %s\t' % (x, self.categories[c]['lowLimit'],\
                        self.categories[c]['highLimit'],), end=' ')
                print('%.2f\t\t %.2f\t\t %.2f' %\
                      (sorting[x][c]['lowLimit'],\
                       sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
            print()


    def showHTMLQuantileOrdering(self,bint Descending=True,strategy='average'):
        """
        *Parameters*:
            * Descending=True,
            * strategy='average'.

        Shows the html version of the quantile preordering in a browser window.

        The ordring strategy is either:
            * **optimistic**, following the upper quantile limits (default),
            * **pessimistic**, following the lower quantile limits,
            * **average**, following the average of the upper and lower quantile limits.
        """
        import webbrowser
        fileName = '/tmp/preOrdering.html'
        fo = open(fileName,'w')
        fo.write(self.computeQuantileOrdering(Descending=Descending,
                                              strategy=strategy,
                                              HTML=True,
                                              Comments=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)


    def showHTMLSorting(self,bint Reverse=True):
        """
        "Parameter*:
            * Reverse=True.

        Shows the html version of the sorting result in a browser window.
        """
        import webbrowser
        fileName = '/tmp/sorting.html'
        fo = open(fileName,'w')
        fo.write(self.showSorting(Reverse=Reverse,isReturningHTML=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)


    def showSorting(self,bint Reverse=True,bint isReturningHTML=False,bint Debug=False):
        """
        *Parameters*:
            * Reverse=True,
            * isReturningHTML=False,
            * Debug=False.

        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.
        
        """
        #from string import replace
        from copy import copy, deepcopy

        try:
            categoryContent = self.categoryContent
        except:
            categoryContent = self.computeCategoryContents(StoreSorting=True)

        categoryKeys = self.orderedCategoryKeys(Reverse=Reverse)
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True

        if Reverse:
            print('\n*--- Sorting results in descending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in descending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
        else:
            print('\n*--- Sorting results in ascending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in ascending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'

        for c in categoryKeys:
            # categoryContent[c].sort()
            print('%s:' % (self.categories[c]['name']), end=' ')
            print('\t',categoryContent[c])
            if isReturningHTML:
                #html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (limprevc,limc)
                html += '<tr><td bgcolor="#FFF79B">%s</td>' % (self.categories[c]['name'])
                catString = str(categoryContent[c])
                html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')

        if isReturningHTML:
            html += '</table>'
            return html

    def computeSortingRelation(self,categoryContents=None,bint Debug=False,bint StoreSorting=True,
                               bint Threading=False,nbrOfCPUs=None,bint Comments=False):
        """
        *Parameters*:
            * categoryContents=None,
            * Debug=False,
            * StoreSorting=True,
            * Threading=False,
            * nbrOfCPUs=None,
            * Comments=False.

        constructs a bipolar sorting relation using the category contents.
        """
        try:
            categoryContents = self.categoryContent
        except:
            pass
        if categoryContents == None:
            categoryContents = self.computeCategoryContents(StoreSorting=StoreSorting,\
                                Threading=Threading,nbrOfCPUs=nbrOfCPUs,Comments=Comments)
        #categoryKeys = self.orderedCategoryKeys()
        #categoryKeys = list(self.categories.keys())
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        actions = [x for x in self.actions]
        currActions = set(actions)
        sortingRelation = {}
        for x in actions:
            sortingRelation[x] = {}
            for y in actions:
                sortingRelation[x][y] = Med
                
        if Debug:
            print('categoryContents',categoryContents)
        #for i in categoryKeys:
        for c in self.categories.keys():
            ibch = set(categoryContents[c])
            ribch = set(currActions) - ibch
            if Debug:
                print('ibch,ribch',ibch,ribch)
            for x in ibch:
                for y in ibch:
                    sortingRelation[x][y] = Med
                    sortingRelation[y][x] = Med
                for y in ribch:
                    sortingRelation[x][y] = Min
                    sortingRelation[y][x] = Max
            currActions = currActions - ibch
        return sortingRelation


###-------------
## #############################
## # Log record for changes:
## # $Log: cIntegerSortingDigraphs.py,v $
## #############################
