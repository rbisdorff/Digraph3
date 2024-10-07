#!/usr/bin/env python3
"""
c-Extension for the Digraph3 collection.
Module cQuantilesRankingDigraphs.py is a c-compiled partial version of the corresponding :py:mod:`sparseOutrankingDigraphs` module for handling quantiles ranking digraphs of very large order.

Copyright (C) 2024  Raymond Bisdorff 
"""
######################

cdef extern from "detertest.h":
    int ABS(int a);

cimport cython
import sys
from time import time, sleep
from decimal import Decimal
from multiprocessing import Process

#####################################
# multiprocessing workers
class _myThread1(Process):
    def __init__(self, 
                 int t,
                 perfTab,
                 splitIndex,
                 tempDirName,
                 decomposition,
                 compIndex,
                 componentRankingRule,
                 bint Comments=False,
                 bint Debug=False):

        Process.__init__(self)
        self.t = t
        self.perfTab = perfTab
        self.splitIndex = splitIndex
        self.tempDirName = tempDirName
        self.decomposition = decomposition
        self.compIndex = compIndex
        self.componentRankingRule = componentRankingRule
        self.Debug = Debug
        self.Comments = Comments

    def run(self):

        cdef int nd, spi, i, t, nc
        cdef dict splitComponents
        from pickle import dumps, loads
        # when sharing with file exchange
        #fiName = tempDirName+'/perfData.py'
        #fi = open(fiName,'rb')
        #perfTab = loads(fi.read())
        #fi.close()
        t = self.t
        perfTab = self.perfTab
        splitIndex = self.splitIndex
        tempDirName = self.tempDirName
        decomposition = self.decomposition
        nc = len(decomposition)
        compIndex = self.compIndex
        componentRankingRule = self.componentRankingRule
        Comments = self.Comments
        Debug = self.Debug
        if Comments:
            print('Starting thread %d, (%d, %d)' % (t+1,splitIndex[0],splitIndex[1]),flush=True)
        splitComponents = {}
        for spi in range(splitIndex[0],splitIndex[1]):
            i = compIndex[spi]
            try:
                comp = decomposition[i]
            except:
                print('Error', i, splitIndex)

            nd = len(str(nc))
            compKey = ('c%%0%dd' % (nd)) % (i+1)
            compDict = {'rank':i}
            compDict['lowQtileLimit'] = comp[0][1]
            compDict['highQtileLimit'] = comp[0][0]
            pg = IntegerBipolarOutrankingDigraph(perfTab,
                        actionsSubset=comp[1],
                        WithConcordanceRelation=False,
                        WithVetoCounts=False,
                        CopyPerfTab=False,
                        Threading=False)
            if componentRankingRule == 'Copeland':
                componentRanking = pg.computeCopelandRanking()
            else:
                componentRanking = pg.computeNetFlowsRanking()
            compDict['componentRanking'] = componentRanking
            splitComponents[i] = compDict
            #splitComponent = {'compKey':i,'compDict':compDict}
        foName = tempDirName+'/splitComponents-'+str(t)+'.py'
        fo = open(foName,'wb')
        fo.write(dumps(splitComponents,-1))
        fo.close()
            #print('Saved: %s' % foName)
        
#######################

from cIntegerOutrankingDigraphs import IntegerBipolarOutrankingDigraph
from cRandPerfTabs import cPartialPerformanceTableau
from cIntegerSortingDigraphs import IntegerQuantilesSortingDigraph
import cSparseIntegerOutrankingDigraphs as SIOD

class cQuantilesRankingDigraph(SIOD.SparseIntegerOutrankingDigraph):
    """
    Cythonized version of the cQuantlesRanking class for the multiprocessing implementation of multiple criteria quantiles ranking of very big performance tableaux - > 100000. This version was developped on the Luxembourg national supercomputer MeluXina (https://docs.lxp.lu/). The author gratefully acknowledges the LuxProvide teams for granting access to the HPC resources and for their kind operational support.

    *Parameters*:
        * argPerfTab, a cPerformanceTableau object or a file name of such a stored object,
        * quantiles=4, higher values may give more convincing ranking results.
        * quantilesOrderingStrategy= {"optimal" (default) | 'average'},
        * LowerClosed=False,
        * componentRankingRule={'Copeland' (default) | 'NetFlows' },
        * minimalComponentSize=1, higher values my result in lower run times and better ranking results,
        * Threading=False,
        * startMethod={ 'spawn' (default) | 'forkserver' | 'fork' },
        * tempDir= './' by default,
        * nbrOfSorters=cpu_count() by default,
        * nbrOfRankers=nbrOfSorters by default
        * save2File=None: allows to save a short object description,
        * CopyPerfTab=False: If *True* allows to show coloured performance heatmaps of the ranking results,
        * Comments=False,
        * Debug=False.

    
    By default, the number of quantiles q is set to quartiles. However, the ranking quality gets better with a finer grained quantiles decomposition. 
    
    For other parameters settings, see the corresponding :py:class:`sparseOutrankingDigraphs.PreRankedOutrankingDigraph` class.

    Example Python session:

    >>> from cRandPerfTabs import *
    >>> t = cRandomPerformanceTableau(numberOfActions=1000,seed=100)
    >>> from cQuantilesRankingDigraphs import *
    >>> qr = cQuantilesRankingDigraph(t,quantiles=5,Threading=True)
    >>> qr
    *----- Object instance description --------------*
    Instance class     : cQuantilesRankingDigraph
    Instance name      : cRandomperftab_mp
    Actions            : 1000
    Criteria           : 7
    Sorting by         : 5-Tiling
    Ordering strategy  : optimal
    Ranking rule       : Copeland
    Components         : 166
    Minimal order      : 1
    Maximal order      : 47
    Average order      : 6.0
    fill rate          : 1.625%
    Attributes         : ['runTimes', 'name', 'actions', 'order', 
                          'dimension', 'sortingParameters', 'nbrOfSorters', 
                          'startMethod', 'valuationdomain', 'profiles', 
                          'categories', 'sorting', 'minimalComponentSize', 
                          'decomposition', 'nbrComponents', 'nd', 
                          'nbrOfRankers', 'components', 'fillRate', 
                          'maximalComponentSize', 'componentRankingRule', 
                          'boostedRanking']
    ----  Constructor run times (in sec.) ----
    Sorting threads    : 8
    Ranking threads    : 8
    StartMethod        : spawn
    Total time         : 0.25518
    Data input         : 0.00003
    QuantilesSorting   : 0.07712
    Preordering        : 0.00356
    Components ranking : 0.17355


    >>> print(bg.boostedRanking[:10],' ... ',bg.boostedRanking[-10:] )
     [131, 488, 551, 75, 446, 663, 245, 364, 250, 348]  
      ...  
     [825, 145, 955, 276, 621, 444, 54, 55, 898, 666]
    
    """
    def __repr__(self):
        """
        Presentation method for cQuantilesRankingDigraph instances.
        """
        reprString = '*----- Object instance description --------------*\n'
        reprString += 'Instance class     : %s\n' % self.__class__.__name__
        reprString += 'Instance name      : %s\n' % self.name
        reprString += 'Actions            : %d\n' % self.order
        reprString += 'Criteria           : %d\n' % self.dimension
        reprString += 'Sorting by         : %d-Tiling\n' % self.sortingParameters['limitingQuantiles']
        reprString += 'Ordering strategy  : %s\n' % self.sortingParameters['strategy']
        reprString += 'Ranking rule       : %s\n' % self.componentRankingRule
        reprString += 'Components         : %d\n' % self.nbrComponents
        reprString += ' Minimal order     : %d\n' % self.minimalComponentSize
        reprString += ' Maximal order     : %d\n' % self.maximalComponentSize
        reprString += ' Average order     : %.1f\n' % (self.order/self.nbrComponents)
        reprString += 'fill rate          : %.3f%%\n' % (self.fillRate*100.0)    
        reprString += 'Attributes         : %s\n' % list(self.__dict__.keys())
        reprString += '----  Constructor run times (in sec.) ----\n'
        if self.nbrOfSorters is not None:
            reprString += 'Sorting threads    : %s\n' % str(self.nbrOfSorters)
            reprString += 'Ranking threads    : %s\n' % str(self.nbrOfRankers)
            reprString += 'StartMethod        : %s\n' % self.startMethod
        reprString += 'Total time         : %.5f\n' % self.runTimes['totalTime']
        reprString += 'Data input         : %.5f\n' % self.runTimes['dataInput']
        reprString += 'QuantilesSorting   : %.5f\n' % self.runTimes['sorting']
        reprString += 'Preordering        : %.5f\n' % self.runTimes['preordering']
        reprString += 'Components ranking : %.5f\n' % self.runTimes['componentsRanking']
        reprString += 'Post Threading     : %.5f\n' % self.runTimes['postThreading']

        return reprString
    
    def __init__(self,argPerfTab,
                 int quantiles=4,
                 quantilesOrderingStrategy="optimal",
                 bint LowerClosed=False,
                 componentRankingRule="Copeland",
                 int minimalComponentSize=1,
                 bint Threading=False,
                 startMethod=None,
                 tempDir='.',
                 nbrOfCPUs=None,
                 nbrOfSorters=None,
                 nbrOfRankers=None,
                 save2File=None,
                 bint CopyPerfTab=False,
                 bint Comments=False,
                 bint Debug=False,
                 bint Configuring=False):

        cdef int i, j, t, totalWeight = 0
        #cdef int nbrOfLocals,nbrOfThreadsUsed,threadLoad
        cdef double ttot, t0, tw, tdump
        cdef int maximalComponentSize = 0
        #cdef array.array lTest=array.array('i')
        cdef int NA
        cdef list jobs,boostedRankingList,boostedRanking,blr

        #global perfTab
        #global decomposition

        from digraphs import Digraph
        #from cIntegerSortingDigraphs import IntegerQuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        #from multiprocessing import Pool
        import multiprocessing as mp
        mpctx = mp.get_context(startMethod)
        Pool = mpctx.Pool
        from copy import copy, deepcopy
        #from cIntegerOutrankingDigraphs import IntegerBipolarOutrankingDigraph 

        if Comments:
            print('Cythonized cQuantilesRankingDigraph HPC class')
   
        ttot = time()
        self.runTimes = {}
        # data input
        t0 = time()
        perfTab = argPerfTab
        self.name = perfTab.name + '_mp'
        # setting quantiles sorting parameters
        if CopyPerfTab:
            self.actions = deepcopy(perfTab.actions)
            self.criteria = deepcopy(perfTab.criteria)
            criteria = self.criteria
            self.evaluation = deepcopy(perfTab.evaluation)
            evaluation = self.evaluation
            self.NA = deepcopy(perfTab.NA)
            NA = self.NA
            
        else:
            self.actions = perfTab.actions
            #self.actionsOrig = [x for x in perfTab.actions]
            criteria = perfTab.criteria
            evaluation = perfTab.evaluation
            NA = perfTab.NA
            
        na = len(self.actions)
        self.order = na
        dimension = len(criteria)
        self.dimension = dimension
        for g in criteria:
            criteria[g]['weight'] = int(criteria[g]['weight'])
            totalWeight += criteria[g]['weight']
        self.runTimes['dataInput'] = time()-t0
        
        #######
        self.sortingParameters = {}
        self.sortingParameters['limitingQuantiles'] = quantiles
        self.sortingParameters['strategy'] = quantilesOrderingStrategy
        self.sortingParameters['LowerClosed'] = LowerClosed
        self.sortingParameters['Threading'] = Threading
        self.sortingParameters['StartMethod'] = startMethod
        self.sortingParameters['PrefThresholds'] = False
        self.sortingParameters['hasNoVeto'] = False
        #self.nbrOfCPUs = nbrOfCPUs
        # quantiles sorting
        t0 = time()
        if Comments:        
            print('Computing the %d-quantiles sorting digraph of order %d ...' % (quantiles,na))
        if Threading:
            import multiprocessing as mp
            if nbrOfCPUs is not None:
                nbrOfSorters = nbrOfCPUs
                nbrOfRankers = nbrOfSorters
            else:
                if nbrOfSorters is None:
                    nbrOfSorters = mp.cpu_count()
            if startMethod is None:
                startMehod = 'spawn'
            self.nbrOfSorters = nbrOfSorters
            self.startMethod = startMethod
        else:
            self.nbrThreads = 0
            self.startMethod = None
            self.nbrOfSorters = 1
            self.numberOfRankers = 1
        #from cIntegerSortingDigraphs import IntegerQuantilesSortingDigraph    
        qs = IntegerQuantilesSortingDigraph(argPerfTab=perfTab,
                                     limitingQuantiles=quantiles,
                                     LowerClosed=LowerClosed,
                                     CompleteOutranking=False,
                                     StoreSorting=True,
                                     CopyPerfTab=CopyPerfTab,
                                     Threading=Threading,
                                     startMethod=startMethod,
                                     tempDir=tempDir,
                                     nbrCores=nbrOfSorters,
                                     Comments=Comments,
                                     Debug=Debug)
        self.runTimes['sorting'] = time() - t0
        self.valuationdomain = qs.valuationdomain
        self.profiles = qs.profiles
        self.categories = qs.categories
        self.sorting = qs.sorting
        if Comments:
            print(qs)
            print('sorting time: %.4f' % (self.runTimes['sorting']))
        # preordering
##        if minimalComponentSize == None:
##            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][0],item[0][1]),item[1]]\
                for item in self._computeQuantileOrdering(
                    strategy=quantilesOrderingStrategy,     
                    Descending=True,
                    Threading=Threading,
                    startMethod=startMethod,
                        nbrOfCPUs=nbrOfSorters)]
        if Debug:
            print(decomposition)
        self.decomposition = decomposition
        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('weak ordering execution time: %.4f' % self.runTimes['preordering']  )
        t0 = time()
        nc = len(decomposition)
        tasksIndex = [(i,len(decomposition[i][1])) for i in range(nc)]
        tasksIndex.sort(key=lambda pos: pos[1],reverse=True)
        maximalComponentSize = tasksIndex[0][1]
        if Configuring:
            print('Number of tasks %d' % nc)
            print('Maximal component size %d !' % maximalComponentSize)
            Continue = input('Continue? Default Y / No :')
            if Continue == 'No':
                print('Abandoning the execution')
                sys.exit(1)
        else:
            if Comments:
                print('Maximal component size: %d' % maximalComponentSize)
        tc = time() - t0
        # setting components
        t0 = time()
        nc = len(decomposition)
        self.nbrComponents = nc
        nd = len(str(nc))
        self.nd = nd
        ### not threding
        if not Threading:
            self.nbrOfRankers = 1
            maximalComponentSize = 0
            components = OrderedDict()
            boostedRanking = []
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                compActions = comp[1]
                nca = len(compActions)
                if nca > maximalComponentSize:
                    maximalComponentSize = nca
                pt = cPartialPerformanceTableau(perfTab,actionsSubset=compActions)
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = IntegerBipolarOutrankingDigraph(pt,
                                          WithConcordanceRelation=False,
                                          WithVetoCounts=False,
                                          #Normalized=True,
                                          CopyPerfTab=False)
                if quantilesOrderingStrategy == 'Copeland':
                    componentRanking = pg.computeCopelandRanking()
                else:
                    componentRanking = pg.computeNetFlowsRanking()
                #pg.__dict__.pop('criteria')
                #pg.__dict__.pop('evaluation')
                #pg.__class__ = IntegerDigraph
                components[compKey]['componentRanking'] = componentRanking
                boostedRanking += componentRanking
            self.runTimes['componentsRanking'] = time() -t0
        else:   # if Threading == True:
            t0 = time()
            from copy import copy, deepcopy
            from pickle import dumps, loads, load, dump
            import multiprocessing as mp
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            self.startMethod = mpctx.get_start_method()
            Process = mpctx.Process
            Queue = mpctx.Queue
            active_children = mpctx.active_children
            #nbrCores = mpctx.cpu_count()
            if nbrOfRankers is None:
                nbrOfRankers = mpctx.cpu_count()
            self.nbrOfRankers = nbrOfRankers
            if Comments:
                print('Processing the %d components' % nc )
                print('Threading ... Test0')
            #tdump = time()
            from tempfile import TemporaryDirectory,mkdtemp
            maximalComponentSize = 0
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                from time import sleep
                #td = TemporaryDirectory(dir=tempDir,delete=False)
                #tempDirName = td.name
                #foName = tempDirName+'/perfData.py'
                #fo = open(foName,'wb')
                #fo.write(dumps(perfTab,-1))
                #fo.close()

                ## tasks queue and workers launching
                NUMBER_OF_WORKERS = nbrOfRankers
                
                from digraphsTools import qtilingIndexList
                compIndex = [i for i in range(nc)]
                from random import shuffle
                shuffle(compIndex)
                splitTasksIndex = qtilingIndexList(compIndex,NUMBER_OF_WORKERS)

                if Debug:
                    print(splitTasksIndex)
                tasksIndex = [(i,len(decomposition[i][1])) for i in range(nc)]
                tasksIndex.sort(key=lambda pos: pos[1],reverse=True)
                maximalComponentSize = tasksIndex[0][1]
                if Comments:
                    print('Maximal component size: %d' % maximalComponentSize)
                # TASKS = [(Comments,(pos[0],nc,tempDirName,
                #               perfTab,decomposition,
                #               componentRankingRule)) for pos in tasksIndex]
                #TASKS = [(Comments,(i,pos,nc,tempDirName,
                #        decomposition,compIndex,
                #        componentRankingRule)) for i,pos in enumerate(splitTasksIndex)]
                #jobs = []
                for t in range(NUMBER_OF_WORKERS):
                    splitIndex = splitTasksIndex[t]
                    #print(t,splitIndex)
                    thread = _myThread1(t,perfTab,
                                             splitIndex,
                                             tempDirName,
                                             decomposition,
                                             compIndex,
                                             componentRankingRule,
                                             Comments,
                                             Debug)
                    thread.start()
                    #jobs.append(thread)
                    #Process(target=_worker1,args=(task_queue,)).start()
                if Comments:
                    print('started')
                    
                #for i in range(NUMBER_OF_WORKERS):
                #    task_queue.put('STOP')                   
                #for proc in jobs:
                #    proc.join()
                
                nch = len(active_children())
                while nch > 0:
                    #if Debug:
                    #    print('active_children:',nch,flush=True)
                    nch = len(active_children())
                    sleep(1)
                    
                if Comments:
                    print('Exit %d threads' % NUMBER_OF_WORKERS,flush=True)
                

                # ####  post-threading operations    
                # components = OrderedDict()
                # #componentsList = []
                # boostedRanking = []
                # for j in range(nc):
                #     if Debug:
                #         print('job',j)
                #     fiName = tempDirName+'/splitComponent-'+str(j)+'.py'
                #     if Debug:
                #         print(j,fiName)
                #     try:
                #         fi = open(fiName,'rb')
                #         splitComponent = loads(fi.read())
                #         if Debug:
                #             print(j,'OK')
                #         fi.close()
                #     except:
                #         print(j, 'Error: missing component!')
                #     if Debug:
                #         print('splitComponent',j,splitComponent)
                #     components[splitComponent['compKey']] = splitComponent['compDict']
                #     boostedRanking += splitComponent['compDict']['componentRanking']
                ####  post-threading operations    
                components = OrderedDict()
                boostedRankingList = []
                for t in range(NUMBER_OF_WORKERS):
                    if Debug:
                        print('job',t)
                    fiName = tempDirName+'/splitComponents-'+str(t)+'.py'
                    if Debug:
                        print(t,fiName)
                    try:
                        fi = open(fiName,'rb')
                        splitComponents = loads(fi.read())
                        if Debug:
                            print(t,'OK')
                        fi.close()
                    except:
                        print(t, 'Error: missing component!')
                    if Debug:
                        print('splitComponents',t,splitComponents)
                    for i in splitComponents:
                        components[i] = splitComponents[i]
                        boostedRankingList.append((i,splitComponents[i]['componentRanking']))
                #print(boostedRankingList)
                boostedRankingList.sort()
                boostedRanking = []
                for brl in boostedRankingList:
                    boostedRanking += brl[1]
                
                self.runTimes['componentsRanking'] = time() - t0
            if Comments:
                print('Ranking time: %.4f' % self.runTimes['componentsRanking']  )

        # storing components, fillRate and maximalComponentSize

        t0 = time()
        self.components = components
        fillRate = 0
        #maximalComponentSize = 0
        for compKey,comp in components.items():
            #pg = comp['subGraph']
            componentRanking = components[compKey]['componentRanking']
            npg = len(componentRanking)
            #if npg > maximalComponentSize:
            #    maximalComponentSize = npg
            fillRate += npg*(npg-1)
            for x in componentRanking:
                self.actions[x]['component'] = compKey
        self.fillRate = fillRate/(self.order * (self.order-1))
        self.maximalComponentSize = maximalComponentSize

        # setting the boosted ranking
        
        self.valuationdomain = {'min': -totalWeight,
                                'med': 0,
                                'max': totalWeight}
       
        self.runTimes['postThreading'] = time() - t0
        if Comments:
            print('postThreading : %.4f' % self.runTimes['postThreading']  )
        # Kohler ranking-by-choosing all components
        self.componentRankingRule = componentRankingRule
        t0 = time()
        #self.boostedRanking = self.computeBoostedRanking(rankingRule=componentRankingRule)
        #self.boostedOrder = list(reversed(self.boostedRanking))
        self.boostedRanking = boostedRanking
        
        self.runTimes['totalTime'] = time() - (ttot+tc) 
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File,WithFileSize=False)
            

    # ----- cQuantilesRankingDigraph class methods ------------
    

    def _computeQuantileOrdering(self,strategy=None,
                                bint Descending=True,
                                bint  Threading=False,
                                 startMethod=None,
                                nbrOfCPUs=None,
                                bint Debug=False,
                                bint Comments=False):
        """
        Renders the quantile interval of the decision actions.
        
        *Parameters*:
            * QuantilesdSortingDigraph instance
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
              in the uppest, the lowest or the average potential quantile.
        
        """
        cdef int x,i,nc,currentContLength,CompSize
        cdef int lc,hc,score1,score2,score3,score4

        #print('===>')
        from operator import itemgetter

        if strategy == None:
            strategy = self.sortingParameters['strategy']
        #actions = [key for key in self.actions if key not in self.profiles]
        actionsCategories = {}
        for x in self.actions:
            #print(x)
            a,lowCateg,highCateg,credibility,rLowLimit,rNotHighLimit =\
                     self.computeActionCategories(x,Comments=Comments,Debug=False,\
                                               Threading=Threading,\
                                                  startMethod=startMethod,\
                                               nbrOfCPUs = nbrOfCPUs)
            #print(a,lowCateg,highCateg,credibility,lowLimit,notHighLimit)
            lowQtileValue = self.categories[lowCateg]['lowLimitValue']
            highQtileValue = self.categories[highCateg]['highLimitValue']
            lowQtileLimit = self.categories[lowCateg]['lowLimit']
            highQtileLimit = self.categories[highCateg]['highLimit']
            if strategy == "optimal":  # default
                lc = int(lowCateg)
                hc = int(highCateg)
                score1 = lc + hc
                score2 = hc
                score3 = rLowLimit - rNotHighLimit
                score4 = -rNotHighLimit              
            elif strategy == "average":
                lc = int(lowCateg)
                hc = int(highCateg)
                score1 = lc + hc
                score2 = rLowLimit - rNotHighLimit
                score3 = lc + hc
                score4 = rLowLimit - rNotHighLimit
            elif strategy == "optimistic":
                score1 = int(highCateg)
                score2 = -rNotHighLimit
                score3 = int(lowCateg)
                score4 = rLowLimit
            else:    # strategy == "pessimistic":
                score1 = int(lowCateg)
                score2 = rLowLimit
                score3 = int(highCateg)
                score4 = -rNotHighLimit
            #print(x,a,score1,highQtileValue,lowQtileValue,lowCateg,highCateg,\
            #     score2, score3, score4,highQtileLimit,lowQtileLimit)
            try:
                actionsCategories[(score1,score2,score3,score4,\
                                   highQtileValue,lowQtileValue,\
                                   lowCateg,highCateg,\
                                   highQtileLimit,lowQtileLimit)].append(a)
            except:
                actionsCategories[(score1,score2,score3,score4,\
                                   highQtileValue,lowQtileValue,\
                                   lowCateg,highCateg,\
                                   highQtileLimit,lowQtileLimit)] = [a]
            # try:
            #     actionsCategories[(score1,\
            #                        highQtileValue,lowQtileValue,\
            #                        lowCateg,highCateg,\
            #                        score2,score3,score4,\
            #                        highQtileLimit,lowQtileLimit)].append(a)
            # except:
            #     actionsCategories[(score1,\
            #                        highQtileValue,lowQtileValue,\
            #                        lowCateg,highCateg,\
            #                        score2,score3,score4,\
            #                        highQtileLimit,lowQtileLimit)] = [a]
        #if Debug:
        #    print(actionsCategories)

        actionsCategKeys = list(actionsCategories.keys())
        actionsCategIntervals = sorted(actionsCategKeys,key=itemgetter(0,1,2,3), reverse=True)
#        actionsCategIntervals = sorted(actionsCategKeys,key=itemgetter(0,5,6,7), reverse=True)

        if Debug:
            print(actionsCategIntervals)
        compSize = self.minimalComponentSize
        
        if compSize == 1:
            if Descending:
                componentsIntervals = [[(item[8],item[9]),actionsCategories[item],item[0],item[3],item[4]]\
                                   for item in actionsCategIntervals]
            else:
                componentsIntervals = [[(item[9],item[8]),actionsCategories[item],item[0],item[3],item[4]]\
                                   for item in actionsCategIntervals]
                
        else:
            componentsIntervals = []
            nc = len(actionsCategIntervals)
            compContent = []
            for i in range(nc):
                currContLength = len(compContent)
                comp = actionsCategIntervals[i]
                #print(comp)
                if currContLength == 0:
                    lowQtileLimit = comp[9]
                highQtileLimit = comp[8]             
                compContent += actionsCategories[comp]
                if len(compContent) >= compSize or i == nc-1:
                    score = comp[0]
                    lowCateg = comp[3]
                    highCateg = comp[4]
                    if Descending:
                        componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent,\
                                                    score,lowCateg,highCateg])
                    else:
                        componentsIntervals.append([(lowQtileLimit,highQtileLimit),compContent,\
                                                    score,lowCateg,highCateg])
                    compContent = []
        #if Debug:
        #    print(componentsIntervals)
        return componentsIntervals        

    def computeActionCategories(self,int action,
                                    bint Show=False,
                                    bint Debug=False,
                                    bint Comments=False,
                                bint Threading=False,
                                startMethod=None,
                                nbrOfCPUs=None):
        """
        *Parameters*:
            * action (int key),
            * Show=False,
            * Debug=False,
            * Comments=False,
            * Threading=False,
            * startMethod='spawn'
            * nbrOfCPUs=1.

        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        cdef int n,Med,lowLimit=0,notHighLimit=0,credibility
        #qs = self.qs
        #qs = self
        Med = self.valuationdomain['med']
        categories = self.categories
        
        try:
            sortinga = self.sorting[action]
        except:
            sorting = self.computeSortingCharacteristics(action=action,Comments=Comments,\
                                                   Threading=Threading,\
                                                         nbrOfCPUs=nbrOfCPUs,
                                                         startMethod=startMethod)
            sortinga = sorting[action]
            
        keys = []
        for c in categories.keys():
        #for c in self.orderedCategoryKeys():
            Above = False
            if sortinga[c]['categoryMembership'] >= Med:
                Above = True
                if sortinga[c]['lowLimit'] > Med:
                    lowLimit = sortinga[c]['lowLimit']
                if sortinga[c]['notHighLimit'] > Med:
                    notHighLimit = sortinga[c]['notHighLimit']    
                keys.append(c)
                if Debug:
                    print(action, c, sortinga[c])
            elif Above:
                break
        n = len(keys)
        try:
            credibility = min(lowLimit,notHighLimit)
        except:
            credibility = Med
        if n == 0:
            return None
        elif n == 1:
            if Show:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     categories[keys[0]]['lowLimit'],\
                                     categories[keys[0]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[0],\
                    credibility,\
                    lowLimit,\
                    notHighLimit
            # return action,\
            #         keys[0],\
            #         keys[0],\
            #         credibility,\
            #         lowLimit,\
            #         notHighLimit
        else:
            if Show:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     categories[keys[0]]['lowLimit'],\
                                     categories[keys[-1]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility,\
                    lowLimit,\
                    notHighLimit
            # return action,\
            #         keys[0],\
            #         keys[-1],\
            #         credibility,\           
            #         lowLimit,\
            #         notHighLimit

    def computeCriterion2RankingCorrelation(self,criterion,
                                            bint Threading=False,\
                                    nbrOfCPUs=None,
                                            startMethod=None,
                                    bint Debug=False,
                                    bint Comments=False):
        """
        *Parameters*:
            * criterion,
            * Threading=False,
            * nbrOfCPUs=1,
            * Debug=False,
            * Comments=False.

        Renders the ordinal correlation coefficient between
        the global outranking and the marginal criterion relation.
        
        """
        gc = IntegerBipolarOutrankingDigraph(self,coalition=[criterion],
                                      Normalized=True,CopyPerfTab=False,
                                      Threading=Threading,nbrCores=nbrOfCPUs,
                                      Comments=Comments)
        globalOrdering = self.ranking2Preorder(self.boostedRanking)
        globalRelation = gc.computePreorderRelation(globalOrdering)
        corr = gc.computeOrdinalCorrelation(globalRelation)
        if Debug:
            print(corr)
        return corr

    def computeMarginalVersusGlobalOutrankingCorrelations(self,
                                bint Sorted=True,
                                bint ValuedCorrelation=False,
                                bint Threading=False,
                                startMethod=None,
                                nbrCores=None,\
                                bint Comments=False):
        """
        *Parameters*:
            * Sorted=True,
            * ValuedCorrelation=False,
            * Threading=False,
            * nbrCores=None,
            * Comments=False.

        Method for computing correlations between each individual criterion relation with the corresponding
        global outranking relation.
        
        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of
        available cores.
        """
        cdef int i
        if Threading:
            import multiprocessing as mp
            mpctx = mp.get_context(startMethod)
            Pool = mpctx.Pool
            #from multiprocessing import Pool
            from os import cpu_count
            if nbrCores == None:
                nbrCores= cpu_count()
            criteriaList = [x for x in self.criteria]
            with Pool(nbrCores) as proc:   
                correlations = proc.map(self.computeCriterion2RankingCorrelation,criteriaList)
            if ValuedCorrelation:
                criteriaCorrelation = [(correlations[i]['correlation']*\
                                        correlations[i]['determination'],criteriaList[i]) for i in range(len(criteriaList))]
            else:
                criteriaCorrelation = [(correlations[i]['correlation'],criteriaList[i]) for i in range(len(criteriaList))]
        else:
            #criteriaList = [x for x in self.criteria]
            criteria = self.criteria
            criteriaCorrelation = []
            for c in dict.keys(criteria):
                corr = self.computeCriterion2RankingCorrelation(c,Threading=False)
                if ValuedCorrelation:
                    criteriaCorrelation.append((corr['correlation']*corr['determination'],c))            
                else:
                    criteriaCorrelation.append((corr['correlation'],c))            
        if Sorted:
            criteriaCorrelation.sort(reverse=True)
        return criteriaCorrelation   

    def relation(self, int x, int y):
        """
        *Parameters*:
            * x (int action key),
            * y (int action key).

        Dynamic construction of the global outranking characteristic function *r(x S y)*.
        """
        cdef int Min, Med, Max, rx, ry
        
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        
        if x == y:
            return Med

        boostedRanking = self.boostedRanking
        rx = boostedRanking.index(x)
        ry = boostedRanking.index(y)

        if rx > ry:
            return Min
        elif ry > rx:
            return Max
        else:
            return Med

    def showMarginalVersusGlobalOutrankingCorrelation(self,
                                                      bint Sorted=True,\
                                                      bint Threading=False,\
                                                      nbrOfCPUs=None,
                                                      startMethod=None,\
                                                      bint Comments=True):
        """
        *Parameters*:
            * Sorted=True,
            * Threading=False,
            * nbrOfCPUs=1,
            * Comments=True.

        Show method for computeCriterionCorrelation results.
        """
        criteria = self.criteria
        criteriaCorrelation = []
        for c in criteria:
            corr = self.computeCriterion2RankingCorrelation(c,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            criteriaCorrelation.append((corr['correlation'],corr['determination'],c))
        if Sorted:
            criteriaCorrelation.sort(reverse=True)
        if Comments:
            print('Marginal versus global outranking correlation')
            print('criterion | weight\t corr\t deter\t corr*deter')
            print('----------|------------------------------------------')
            for x in criteriaCorrelation:
                c = x[2]
                print('%9s |  %.2f \t %.3f \t %.3f \t %.3f' % (c,criteria[c]['weight'],x[0],x[1],x[0]*x[1]))

    def showActionsSortingResult(self,actionsSubset=None):
        """
        *Parameter*:
            * actionsSubset=None.

        Shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        print('Quantiles sorting result per decision action')
        if actionsSubset==None:
            for x in self.actions:
                self.computeActionCategories(x,Show=True)
        else:
            for x in actionsSubset:
                self.computeActionCategories(x,Show=True)

    def showShort(self,fileName=None,bint WithFileSize=False):
        """
        *Parameter*:
            * WithFileSize=False.

        Default (__repr__) presentation method for big outranking digraphs instances:
        """
        #summaryStats = self.computeDecompositionSummaryStatistics()
        from digraphs import total_size
        if fileName == None:
            print('*----- show short --------------*')
            print('Instance name     : %s' % self.name)
            print('Actions           : %d' % self.order)
            print('Criteria          : %d' % self.dimension)
            print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
            print('Ordering strategy : %s' % self.sortingParameters['strategy'])
            print('Ranking rule      : %s' % self.componentRankingRule)
            print('# Components      : %d' % self.nbrComponents)
            print('Minimal order     : %d' % self.minimalComponentSize)
            print('Maximal order     : %d' % self.maximalComponentSize)
            print('Average order     : %.1f' % (self.order/self.nbrComponents))
            print('Fill rate         : %.3f%%' % (self.fillRate*100.0))
            print('----  Constructor run times (in sec.) ----')
            print('Threads           : %d' % self.nbrThreads)
            print('Start mthod       : %s' % self.startMethod)
            print('Total time        : %.5f' % self.runTimes['totalTime'])
            print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
            print('Preordering       : %.5f' % self.runTimes['preordering'])
            print('Decomposing       : %.5f' % self.runTimes['decomposing'])
            try:
                print('Ordering          : %.5f' % self.runTimes['ordering'])
            except:
                pass
        else:
            fo = open(fileName,'a')
            fo.write('*----- show short --------------*\n')
            fo.write('Instance name      : %s\n' % self.name)
            if WithFileSize:
                fo.write('Size (in bytes)    : %d\n' % total_size(self))
            fo.write('# Actions          : %d\n' % self.order)
            fo.write('# Criteria         : %d\n' % self.dimension)
            fo.write('Sorting by         : %d-Tiling\n' % self.sortingParameters['limitingQuantiles'])
            fo.write('Ordering strategy  : %s\n' % self.sortingParameters['strategy'])
            fo.write('Local ranking rule : %s\n' % self.componentRankingRule)
            fo.write('# Components       : %d\n' % self.nbrComponents)
            fo.write('Minimal size       : %d\n' % self.minimalComponentSize)
            fo.write('Maximal order      : %d\n' % self.maximalComponentSize)
            fo.write('Average order      : %.1f\n' % (self.order/self.nbrComponents))
            fo.write('Fill rate          : %.3f%%\n' % (self.fillRate*100.0))
            fo.write('*-- Constructor run times (in sec.) --*\n')
            fo.write('# Threads          : %d\n' % self.nbrOfCPUs)
            fo.write('Total time         : %.5f\n' % self.runTimes['totalTime'])
            fo.write('QuantilesSorting   : %.5f\n' % self.runTimes['sorting'])
            fo.write('Preordering        : %.5f\n' % self.runTimes['preordering'])
            fo.write('Decomposing        : %.5f\n' % self.runTimes['decomposing'])
            try:
                fo.write('Ordering           : %.5f\n' % self.runTimes['ordering'])
            except:
                pass
            fo.close()

    def showActions(self):
        """
        Prints out the actions disctionary.
        """
        cdef int x
        print('List of decision actions')
        for x in self.actions:
            print('%d: %s' % (x,self.actions[x]['name']) )

    def showCriteria(self, bint IntegerWeights=False, bint Debug=False):
        """
        *Parameters*:
            * IntegerWeights=False,
            * Debug=False.

        print Criteria with thresholds and weights.
        """
        cdef int sumWeights = 0
        print('*----  criteria -----*')
        #sumWeights = 0
        for g in self.criteria:
            sumWeights += self.criteria[g]['weight']
        criteriaList = [c for c in self.criteria]
        criteriaList.sort()
        for c in criteriaList:
            critc = self.criteria[c]
            try:
                criterionName = critc['name']
            except:
                criterionName = ''
            print(c, repr(criterionName))
            print('  Scale =', critc['scale'])
            if IntegerWeights:
                print('  Weight = %d ' % (critc['weight']))
            else:
                weightg = critc['weight']/sumWeights
                print('  Weight = %.3f ' % (weightg))
            try:
                for th in critc['thresholds']:
                    if Debug:
                        print('-->>>', th,critc['thresholds'][th][0],
                              critc['thresholds'][th][1])
                    print('  Threshold %s : %.2f + %.2fx' %\
                          (th,critc['thresholds'][th][0],
                           critc['thresholds'][th][1]), end=' ')
            except:
                pass
            print()

    def showComponents(self, direction='increasing'):
        """
        *Parameter*:
            * direction='increasing'.

        """
        self.showDecomposition(direction=direction)

    def showDecomposition(self, direction='decreasing'):
        """
        *Parameter*:
            * direction='increasing'.

        """        
        print('*--- quantiles decomposition in %s order---*' % (direction) )
        #compKeys = [compKey for compKey in self.components.keys()]
        # the components are ordered from best (1) to worst (n)
        compKeys = [c for c in self.components]
        if direction != 'decreasing':    
            compKeys.sort(reverse=True)
        else:
            pass
        for compKey in compKeys:
            comp = self.components[compKey]
            print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],comp['componentRanking']) )
                

    def showRelationTable(self, bint IntegerValues=True, compKeys=None):
        """
        *Parameters*:
            * IntegerValues=True,
            * compKeys=None.

        Specialized for showing the quantiles decomposed relation table.
        Components are stored in an ordered dictionary.
        """
        cdef int nc
        components = self.components
        if compKeys == None:
            nc = self.nbrComponents
            print('%d quantiles decomposed relation table in decreasing order' % nc)
            for compKey,comp in components.items():
                ranking = comp['componentRanking']
                print('Component : %s' % compKey, end=' ')
                print('%s' % ranking)
                    
        else:
            for compKey in compKeys:
                comp = components[compKey]
                ranking = comp['componentRanking']
                print('Relation table of component %s' % str(compKey))
                print('%s' % ranking)

    def computeDeterminateness(self, bint InPercent=True):
        """
        *Parameter*:
            * InPercent=True.

        Computes the Kendalll distance in % of self
        with the all median valued (indeterminate) digraph.

        deter = (sum_{x,y in X} abs[r(xSy) - Med])/(oder*order-1)
        """
        
        cdef int Max, Med, order, x, y
        cdef float sumDeter=0.0
        cdef float deter
        
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']

        actions = self.actions
        relation = self.relation
        order = self.order

        for x in actions:
            for y in actions:
                if x != y:
                    sumDeter += float(ABS(relation(x,y) - Med))

        deter = float(sumDeter) / float((order * (order-1)))
        if InPercent:
            return deter/(Max-Med)*100.0
        else:
            return deter



########################################################33
