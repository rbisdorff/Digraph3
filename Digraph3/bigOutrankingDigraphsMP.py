#!/usr/bin/env python3
# Python 3 implementation of digraphs
# sub-module for big outranking digraphs
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

from outrankingDigraphs import *
from sortingDigraphs import *
from time import time
from decimal import Decimal

##def total_size(o, handlers={}, verbose=False):
##    """ Returns the approximate memory footprint of an object and all of its contents.
##
##    Automatically finds the contents of the following containers and
##    their subclasses:  tuple, list, deque, dict, set, frozenset, Digraph and BigDigraph.
##    To search other containers, add handlers to iterate over their contents:
##
##        handlers = {SomeContainerClass: iter,
##                    OtherContainerClass: OtherContainerClass.get_elements}
##
##    See http://code.activestate.com/recipes/577504/  
##
##    """
##    from sys import getsizeof, stderr
##    from itertools import chain
##    from collections import deque
##    
##    try:
##        from reprlib import repr
##    except ImportError:
##        pass
##
##    # built-in containers and their subclasses
##    dict_handler = lambda d: chain.from_iterable(d.items())
##    all_handlers = {tuple: iter,
##                    list: iter,
##                    deque: iter,
##                    dict: dict_handler,
##                    set: iter,
##                    frozenset: iter,
##                    }
##
##    # Digraph3 objects 
##    object_handler = lambda d: chain.from_iterable(d.__dict__.items())    
##    handlers = {BigDigraph: object_handler,
##                Digraph: object_handler,
##                PerformanceTableau : object_handler,
##                }
##    
##    all_handlers.update(handlers)     # user handlers take precedence
##    seen = set()                      # track which object id's have already been seen
##    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__
##
##    def sizeof(o):
##        if id(o) in seen:       # do not double count the same object
##            return 0
##        seen.add(id(o))
##        s = getsizeof(o, default_size)
##
##        if verbose:
##            print(s, type(o), repr(o), file=stderr)
##
##        for typ, handler in all_handlers.items():
##            if isinstance(o, typ):
##                s += sum(map(sizeof, handler(o)))
##                break
##        return s
##
##    return sizeof(o)

class BigDigraph(object):
    """
    abstract root class for lineraly decomposed big digraphs (order > 1000) using multiprocessing ressources.
    """
    
    def relation(self,x,y,Debug=False):
        """
        Dynamic construction of the global digraph relation.
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        
        if x == y:
            return Med
        cx = self.actions[x]['component']
        cy = self.actions[y]['component']
        #print(x,cx,y,cy)
        if cx == cy:
            return self.components[cx]['subGraph'].relation[x][y]        
        elif self.components[cx]['rank'] > self.components[cy]['rank']:
            return Min
        else:
            return Max 
    
    def computeOrdinalCorrelation(self, other, Debug=False):
        """
        Renders the ordinal correlation K of a BigDigraph instance
        when compared with a given compatible (same actions set) other Digraph or
        BigDigraph instance.
        
        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             The global outranking relation of BigDigraph instances is contructed on the fly
             from the ordered dictionary of the components.

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """

        if self.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the BigDigraph instance must be normalized !!')
                print(self.valuationdomain)
                return
        
        if issubclass(other.__class__,(Digraph)):
            if Debug:
                print('other is a Digraph instance')
            if other.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the other digraph must be normalized !!')
                print(other.valuationdomain)
                return
        elif isinstance(other,(BigDigraph)):
            if Debug:
                print('other is a BigDigraph instance')
            if other.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the other bigDigraph instance must be normalized !!')
                print(other.valuationdomain)
                return
        
        selfActionsList = [(ck,
                            list(self.components[ck]['subGraph'].actions.keys()))\
                           for ck in self.components]
        if issubclass(other.__class__,(Digraph)):
            otherActionsList = [( 'c01', list(other.actions.keys()) )]
        else:
            otherActionsList = [(ck,
                            list(other.components[ck]['subGraph'].actions.keys()))\
                           for ck in other.components]
        if Debug:
            print(selfActionsList)
            print(otherActionsList)
        
        correlation = Decimal('0.0')
        determination = Decimal('0.0')

        for ckx in selfActionsList:
            for x in ckx[1]:
                for cky in otherActionsList:
                    for y in cky[1]:
                        if x != y:
                            selfRelation = self.relation(x,y)
                            try:
                                otherRelation = other.relation[x][y]
                            except:
                                otherRelation = other.relation(x,y)
                            if Debug:
                                print(x,y,'self', selfRelation)
                            if Debug:
                                print(x,y,'other', otherRelation)
                            corr = min( max(-selfRelation,otherRelation), max(selfRelation,-otherRelation) )
                            correlation += corr
                            determination += min( abs(selfRelation),abs(otherRelation) )

        if determination > Decimal('0.0'):
            correlation /= determination
            n2 = (self.order*self.order) - self.order
            return { 'correlation': correlation,\
                     'determination': determination / Decimal(str(n2)) }
        else:
            return {'correlation': Decimal('0.0'),\
                    'determination': determination}
        
    def showDecomposition(self,direction='decreasing'):
        
        print('*--- Relation decomposition in %s order---*' % (direction) )
        compKeys = [compKey for compKey in self.components]
        if direction != 'increasing':
            compKeys.sort()
        else:
            compKeys.sort(reverse=True)
        for compKey in compKeys:
            comp = self.components[compKey]
            sg = comp['subGraph']
            actions = [x for x in sg.actions]
            actions.sort()
            print('%s: %s' % (compKey,actions))


##    def __repr__(self,WithComponents=False):
##        """
##        Default presentation method for BigDigraph instances.
##        """
##        print('*----- show short --------------*')
##        print('Instance name     :', self.name)
##        print('Instance class    :', self.__class__)
##        print('# Nodes           :', self.order)
##        print('# Components      :', self.nbrComponents)
##        if WithComponents:
##            g.showDecomposition()
##        return 'Default presentation of BigDigraph instances'

    def computeDecompositionSummaryStatistics(self):
        """
        Returns the summary of the distribution of the length of
        the components as dictionary::
        
            summary = {'max': maxLength,
                       'median':medianLength,
                       'mean':meanLength,
                       'stdev': stdLength}
        """
        try:
            import statistics
        except:
            print('Error importing the statistics module.')
            print('You need to upgrade your Python to version 3.4+ !')
            return      
        self.componentStatistics = {}
        nc = self.nbrComponents
        compKeys = list(self.components.keys())
        compLengths = [self.components[ck]['subGraph'].order \
                       for ck in compKeys]
        medianLength = statistics.median(compLengths)
        meanLength = statistics.mean(compLengths)
        stdLength = statistics.pstdev(compLengths)
        summary = {
                   'median':medianLength,
                   'mean':meanLength,
                   'stdev': stdLength,
                   'max': max(compLengths)}
        return summary

    def recodeValuation(self,newMin=-1,newMax=1,Debug=False):
        """
        Specialized for recoding the valuation of all the partial digraphs and the component relation.
        By default the valuation domain is normalized ([-1.0;1.0])
        """
        # saving old and new valuation domain
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']
        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)
        newMin = Decimal(str(newMin))
        newMax = Decimal(str(newMax))
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))
        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)
        # loop over all components
##        nc = self.nbrComponents
        print('Recoding the valuation of a BigDigraph instance')
##        compKeys = list(self.components.keys())
##        oldRelation = self.componentRelation
##        newRelation = {}
        for cki in self.components.keys(): 
##            cki = compKeys[i]
            self.components[cki]['subGraph'].recodeValuation(newMin=newMin,newMax=newMax)
##            newRelation[cki] = {}
##            for j in range(nc):
##                ckj = compKeys[j]
##                if oldRelation[cki][ckj] == oldMax:
##                    newRelation[cki][ckj] = newMax
##                elif oldRelation[cki][ckj] == oldMin:
##                    newRelation[cki][ckj] = newMin
##                elif oldRelation[cki][ckj] == oldMed:
##                    newRelation[cki][ckj] = newMed
##                else:
##                    newRelation[cki][cki] = newMin + \
##                            ((oldRelation[cki][ckj] - oldMin)/oldAmplitude)*newAmplitude
##                    if Debug:
##                        print(cki,ckj,oldRelation[cki][ckj],newRelation[cki][ckj])
        # update valuation domain                       
        Min = Decimal(str(newMin))
        Max = Decimal(str(newMax))
        Med = (Min+Max)/Decimal('2')
        self.valuationdomain = { 'min':Min, 'max':Max, 'med':Med }
        # update componentRelation
##        self.componentRelation = newRelation


class BigOutrankingDigraphMP(BigDigraph,PerformanceTableau):
    """
    Multiprocessing implementation of the BipolarOutrankingDigraph class
    for large instances (order > 1000)

    The outranking digraph is with q-tiles sorting decomposed in a partition of more or
    quantile equivalence classes, which are lineraly ordred by average quantile limits. (default).

    To each quantile equivalence class is associated a BipolarOutrankingDigraph object
    which is restricted to the decision actions in this quantile class.

    By default, q is set to a tenth of the number of decision actions,
    ie q = order//10.

    For other parameters settings, see the corresponding QuantilesSortingDigraph class.

    """
    def __init__(self,argPerfTab=None,quantiles=None,
                 quantilesOrderingStrategy='average',
                 LowerClosed=True,
                 WithKohlerRanking=True,
                 minimalComponentSize=None,
                 Threading=True,nbrOfCPUs=None,
                 save2File=None,
                 Comments=False,
                 Debug=False):
        
        from digraphs import Digraph
        from sortingDigraphs import QuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from multiprocessing import Pool
        from copy import deepcopy
        
        ttot = time()
        # setting name
        perfTab = argPerfTab
        self.name = perfTab.name + '_mp'
        # setting quantiles sorting parameters
        self.actions = deepcopy(perfTab.actions)
        na = len(self.actions)
        self.order = na
        self.criteria = deepcopy(perfTab.criteria)
        self.dimension = len(perfTab.criteria)
        self.evaluation = deepcopy(perfTab.evaluation)
        if quantiles == None:
            quantiles = na//10
        self.sortingParameters = {}
        self.sortingParameters['limitingQuantiles'] = quantiles
        self.sortingParameters['strategy'] = quantilesOrderingStrategy
        self.sortingParameters['LowerClosed'] = LowerClosed
        self.sortingParameters['Threading'] = Threading
        self.sortingParameters['PrefThresholds'] = False
        self.sortingParameters['hasNoVeto'] = False
        self.nbrOfCPUSs = nbrOfCPUs
        # quantiles sorting
        t0 = time()
        if Comments:        
            print('Computing the %d-quantiles sorting digraph ...' % (quantiles))
        #if Threading:
        qs = QuantilesSortingDigraph(argPerfTab=perfTab,
                                        limitingQuantiles=quantiles,
                                        LowerClosed=LowerClosed,
                                        CompleteOutranking=False,
                                        Threading= self.sortingParameters['Threading'],
                                        nbrCores=nbrOfCPUs,
                                        Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
        self.qs = qs
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
        if minimalComponentSize == None:
            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][2],item[0][1]),item[1]]\
                                  for item in self._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]
        if Debug:
            print(decomposition)
        self.decomposition = decomposition
        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('weak ordering execution time: %.4f' % self.runTimes['preordering']  )
        # setting components
        t0 = time()
        nc = len(decomposition)
        self.nbrComponents = nc
        if Debug:
            print(nc)
        self.nd = len(str(nc))
        if not self.sortingParameters['Threading']:
            components = {}
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                #print(comp)
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                #print(perfTab,comp[1])
                pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = BipolarOutrankingDigraph(pt,Normalized=True)
                pg.__dict__.pop('criteria')
                pg.__dict__.pop('evaluation')
                pg.__dict__.pop('vetos')
                pg.__dict__.pop('negativeVetos')
                pg.__dict__.pop('largePerformanceDifferencesCount')
                pg.__dict__.pop('concordanceRelation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
        else:   # if self.sortingParameters['Threading'] == True:
            from copy import copy, deepcopy
            from pickle import dumps, loads, load
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            #Debug=True
            class myThread(Process):
                def __init__(self, threadID,\
                             tempDirName,\
                             Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    from copy import deepcopy
                    from perfTabs import PartialPerformanceTableau
                    from outrankingDigraphs import BipolarOutrankingDigraph
                    chdir(self.workingDirectory)
                    if Debug:
                        print("Starting working in %s on %s" % (self.workingDirectory, self.name))
                    fi = open('dumpSelf.py','rb')
                    context = loads(fi.read())
                    fi.close()
                    i = self.threadID
                    comp = context.decomposition[i]
                    if Debug:
                        print(i, comp)
                    compKey = ('c%%0%dd' % (context.nd)) % (i+1)
                    compDict = {compKey: {}}
                    compDict = {'rank':i}
                    pt = PartialPerformanceTableau(context,actionsSubset=comp[1])
                    compDict['lowQtileLimit'] = comp[0][1]
                    compDict['highQtileLimit'] = comp[0][0]
                    pg = BipolarOutrankingDigraph(pt,Normalized=True)     
                    pg.__dict__.pop('criteria')
                    pg.__dict__.pop('evaluation')
                    pg.__dict__.pop('vetos')
                    pg.__dict__.pop('negativeVetos')
                    pg.__dict__.pop('largePerformanceDifferencesCount')
                    pg.__dict__.pop('concordanceRelation')
                    pg.__class__ = Digraph
                    compDict['subGraph'] = deepcopy(pg)
                    splitComponent = (compKey,compDict)
                    if Debug:
                        print(compDict)
                    foName = 'splitComponent-'+str(i)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitComponent,-1))
                    fo.close()
                    
            print('Threading ...')        
            from tempfile import TemporaryDirectory,mkdtemp
            #with TemporaryDirectory() as tempDirName:
            tempDirName = mkdtemp()
            from copy import copy, deepcopy
            from time import sleep
            #selfDp = copy(self)
            selfFileName = tempDirName +'/dumpSelf.py'
            if Debug:
                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            #pd = dumps(selfDp,-1)
            pd = dumps(self,-1)
            fo.write(pd)
            fo.close()

            if nbrOfCPUs == None:
                nbrOfCPUs = cpu_count()-1
            print('Nbr of cpus = ',nbrOfCPUs)
            for j in range(nc):
                print('thread = ',j+1,end="...")
                process = myThread(j,tempDirName,Debug)
                process.start()
            while active_children() != []:
                sleep(1)
            print('Exit multithreading')
            componentsList = []
            for j in range(nc):
                if Debug:
                    print('job',j)
                fiName = tempDirName+'/splitComponent-'+str(j)+'.py'
                fi = open(fiName,'rb')
                splitComponent = loads(fi.read())
                if Debug:
                    print('splitComponent',splitComponent)
                componentsList.append(splitComponent)
            # end of Threading
        #print(componentsList)
        components = OrderedDict(componentsList)
        for compKey in components.keys():
            for x in components[compKey]['subGraph'].actions.keys():
                self.actions[x]['component'] = compKey
        self.components = components

        # setting the component relation
        self.valuationdomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
       
        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )
        # Kohler ranking-by-choosing all components
        if WithKohlerRanking:
            t0 = time()
            self.boostedKohlerRanking = self.computeBoostedKohlerRanking()
            self.runTimes['ordering'] = time() - t0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)
            

    # ----- class methods ------------

##    def _compMPComputation(self,j):
##        print('thread: %d' % j)
##        comp = self.decomposition[j-1]
##        compKey = self.compKeyStr % (j)
##        compDict = {'rank':j}
##        pt = PartialPerformanceTableau(self,actionsSubset=comp[1])
##        compDict['lowQtileLimit'] = comp[0][2]
##        compDict['highQtileLimit'] = comp[0][1]
##        pg = BipolarOutrankingDigraph(pt,Normalized=True)
##        pg.__dict__.pop('criteria')
##        pg.__dict__.pop('evaluation')
##        pg.__dict__.pop('vetos')
##        pg.__dict__.pop('negativeVetos')
##        pg.__dict__.pop('largePerformanceDifferencesCount')
##        pg.__dict__.pop('concordanceRelation')
##        pg.__class__ = Digraph
##        compDict['subGraph'] = pg
##        return compKey,compDict

    def __repr__(self,WithComponents=False):
        """
        Default presentation method for big outrankingDigraphs instances.
        """
        print('*----- show short --------------*')
        print('Instance name     : %s' % self.name)
        print('Size (in bytes)   : %d' % total_size(self))
        print('# Actions         : %d' % self.order)
        print('# Criteria        : %d' % self.dimension)
        print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
        print('Ordering strategy : %s' % self.sortingParameters['strategy'])
        print('# Components      : %d' % self.nbrComponents)
        print('Minimal size      : %d' % self.minimalComponentSize)
        print('Maximal size      : %d' % (self.computeDecompositionSummaryStatistics())['max'])
        print('Median size      : %d' % (self.computeDecompositionSummaryStatistics())['median'])
        if WithComponents:
            g.showDecomposition()
        print('----  Constructor run times (in sec.) ----')
        print('Total time        : %.5f' % self.runTimes['totalTime'])
        print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
        print('Preordering       : %.5f' % self.runTimes['preordering'])
        print('Decomposing       : %.5f' % self.runTimes['decomposing'])
        try:
            print('Ordering          : %.5f' % self.runTimes['ordering'])
        except:
            pass
        return 'Default presentation of BigOutrankingDigraphs'

    def _computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                Debug=False):
        """
        Renders the quantile interval of the decision actions.
        *Parameters*:
            * QuantilesdSortingDigraph instance
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
              in the uppest, the lowest or the average potential quantile.
        
        """
        if strategy == None:
            strategy = self.sortingParameters['strategy']
        actionsCategories = {}
        for x in self.actions.keys():
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            lowQtileLimit = self.qs.categories[lowCateg]['lowLimit']
            highQtileLimit = self.qs.categories[highCateg]['highLimit']
            if strategy == "optimistic":
                try:
                    actionsCategories[(highQtileLimit,highQtileLimit,lowQtileLimit)].append(a)
                except:
                    actionsCategories[(highQtileLimit,highQtileLimit,lowQtileLimit)] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(lowQtileLimit,highQtileLimit,lowQtileLimit)].append(a)
                except:
                    actionsCategories[(lowQtileLimit,highQtileLimit,lowQtileLimit)] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,highQtileLimit,lowQtileLimit)].append(a)
                except:
                    actionsCategories[(ac,highQtileLimit,lowQtileLimit)] = [a]
            else:
                print('Error: startegy %s unkonwon' % strategy)
                
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)

        CompSize = self.minimalComponentSize 
        if CompSize == 1:
            return actionsCategIntervals
        else:
            componentsIntervals = []
            nc = len(actionsCategIntervals)
            compContent = []
            for i in range(nc):
                currContLength = len(compContent)
                comp = actionsCategIntervals[i]               
                if currContLength == 0:
                    lowQtileLimit = comp[0][2]
                highQtileLimit = comp[0][1]
                compContent += comp[1]
                if len(compContent) >= CompSize or i == nc-1:
                    componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent])
                    compContent = []
            return componentsIntervals        
    

##    def _computeQuantileOrderingMP(self,strategy=None,
##                                Descending=True,
##                                Debug=False,
##                                nbrOfCPUs=None):
##        """
##        !!! Example of hopelessly inefficient multiprocessing of a rather simple task and insufficient granularity
##        """
##        from multiprocessing import Pool
##        from os import cpu_count
##        if nbrOfCPUs == None:
##            nbrOfCPUs = cpu_count()
##        if strategy == None:
##            strategy = self.sortingParameters['strategy']
##        actionsCategoriesList = [] 
##        actions = self.actions
##        showActionCategories = self.showActionCategories
##        with Pool() as pool:
##            actionsCategoriesList = [(a,lowCateg,highCateg,credibility) for\
##                                     a,lowCateg,highCateg,credibility in\
##                                     pool.map(showActionCategories,actions.keys())]
##        actionsCategories = OrderedDict()
##        for a,lowCateg,highCateg,credibility in actionsCategoriesList:
##            # too much non parallel work to do
##            if strategy == "optimistic":
##                try:
##                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
##                except:
##                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]
##            elif strategy == "pessimistic":
##                try:
##                    actionsCategories[(int(lowCateg),int(highCateg))].append(a)
##                except:
##                    actionsCategories[(int(lowCateg),int(highCateg))] = [a]
##            elif strategy == "average":
##                lc = float(lowCateg)
##                hc = float(highCateg)
##                ac = (lc+hc)/2.0
##                try:
##                    actionsCategories[(ac,int(highCateg),int(lowCateg))].append(a)
##                except:
##                    actionsCategories[(ac,int(highCateg),int(lowCateg))] = [a]
##            else:  # optimistic by default
##                try:
##                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
##                except:
##                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]      
##                
##        actionsCategIntervals = []
##        for interval in actionsCategories:
##            actionsCategIntervals.append([interval,\
##                                          actionsCategories[interval]])
##        actionsCategIntervals.sort(reverse=Descending)
##
##        return actionsCategIntervals

    def showActionCategories(self,action,Debug=False,Comments=False):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        qs = self.qs
        Med = qs.valuationdomain['med']
        sorting = qs.computeSortingCharacteristics(action=action,Comments=Debug)
        keys = []
        for c in qs.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                keys.append(c)
                if Debug:
                    print(action, c, sorting[action][c])
        n = len(keys)
        try:
            credibility = min(lowLimit,notHighLimit)
        except:
            credibility = Med
        if n == 0:
            return None
        elif n == 1:
            if Comments:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     qs.categories[keys[0]]['lowLimit'],\
                                     qs.categories[keys[0]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[0],\
                    credibility
        else:
            if Comments:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     qs.categories[keys[0]]['lowLimit'],\
                                     qs.categories[keys[-1]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility            

    def showActionsSortingResult(self,actionSubset=None,Debug=False):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        print('Quantiles sorting result per decision action')
        for x in actions.keys():
            self.showActionCategories(x,Debug=Debug,Comments=True)

    def showShort(self,fileName=None):
        """
        Default (__repr__) presentation method for big outranking digraphs instances:
        
        >>> from bigOutrankingDigraphs import *
        >>> t = RandomCBPerformanceTableau(numberOfActions=100)
        >>> g = BigOutrankingDigraph(t,quantiles=10)
        Threading ...
        Nbr of cpus =  7
        number of cores = 7
        nbr of actions to split 100
        nbr of jobs =  7
        nbr of splitActions =  15
        iteration =  1 15
        iteration =  2 15
        iteration =  3 15
        iteration =  4 15
        iteration =  5 15
        iteration =  6 15
        iteration =  7 10
        Exiting computing threads
        >>> print(g)
        *----- show short --------------*
        Instance name     : randomCBperftab_mp
        # Actions         : 100
        # Criteria        : 13
        Sorting by        : 10-Tiling 
        Ordering strategy : average quantile
        # Components      : 11
        ----  Constructor run times (in sec.) ----
        Total time        : 0.72743
        QuantilesSorting  : 0.51481
        Preordering       : 0.00292
        Decomposing       : 0.20469
        Ordering          : 0.00500
        Default presentation of BigOutrankingDigraphs
        
        """
        if fileName == None:
            print(self)
        else:
            fo = open(fileName,'a')
            fo.write('*----- show short --------------*')
            fo.write('Instance name      : %s\n' % self.name)
            fo.write('Size (in bytes)    : %d\n' % total_size(self))
            fo.write('# Actions          : %d\n' % self.order)
            fo.write('# Criteria         : %d\n' % self.dimension)
            fo.write('Sorting by         : %d-Tiling\n' % self.sortingParameters['limitingQuantiles'])
            fo.write('Ordering strategy  : %s\n' % self.sortingParameters['strategy'])
            fo.write('# Components       : %d\n' % self.nbrComponents)
            fo.write('Minimal size       : %d\n' % self.minimalComponentSize)
            fo.write('Maximal size       : %d\n' % (self.computeDecompositionSummaryStatistics())['max'])
            fo.write('Median size        : %d\n' % (self.computeDecompositionSummaryStatistics())['median'])
            fo.write('*-- Constructor run times (in sec.) --*\n')
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
        actionsList = []
        for ck in self.components:
            comp = self.components[ck]
            actionsList += [(x,comp['subGraph'].actions[x]['name'],comp['subGraph'].actions[x]['comment'],) for x in comp['subGraph'].actions]
        actionsList.sort()
        print('List of decision actions')
        for ax in actionsList:
            print('%s: %s (%s)' % ax)

    def showCriteria(self,IntegerWeights=False,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
        print('*----  criteria -----*')
        sumWeights = Decimal('0.0')
        for g in self.criteria:
            sumWeights += self.criteria[g]['weight']
        criteriaList = [c for c in self.criteria]
        criteriaList.sort()
        for c in criteriaList:
            try:
                criterionName = self.criteria[c]['name']
            except:
                criterionName = ''
            print(c, repr(criterionName))
            print('  Scale =', self.criteria[c]['scale'])
            if IntegerWeights:
                print('  Weight = %d ' % (self.criteria[c]['weight']))
            else:
                weightg = self.criteria[c]['weight']/sumWeights
                print('  Weight = %.3f ' % (weightg))
            try:
                for th in pg.criteria[c]['thresholds']:
                    if Debug:
                        print('-->>>', th,self.criteria[c]['thresholds'][th][0],self.criteria[c]['thresholds'][th][1])
                    print('  Threshold %s : %.2f + %.2fx' % (th,self.criteria[c]['thresholds'][th][0],
                                                             self.criteria[c]['thresholds'][th][1]), end=' ')
            except:
                pass
            print()

    def showComponents(self):
        BigOutrankingDigraph.showDecomposition(self)

    def showDecomposition(self,direction='decreasing'):
        
        print('*--- quantiles decomposition in %s order---*' % (direction) )
        compKeys = [compKey for compKey in self.components]
        if direction != 'increasing':
            compKeys.sort()
        else:
            compKeys.sort(reverse=True)
        for compKey in compKeys:
            comp = self.components[compKey]
            sg = comp['subGraph']
            actions = [x for x in sg.actions]
            actions.sort()
            print('%s. %s-%s : %s' % (compKey,comp['highQtileLimit'],comp['lowQtileLimit'],actions))

    def showRelationTable(self,compKeys=None):
        """
        Specialized for showing the quantiles decomposed relation table.
        """
        if compKeys == None:
            nc = self.nbrComponents
            print('%d quantiles decomposed relation table in decreasing order' % nc)
            compKeys = list(self.components.keys())
            compKeys.sort()
            for i in range(nc) :
                cki = compKeys[i]
                comp = self.components[cki]
                pg = comp['subGraph']
                print('Component :', cki)
                if pg.order > 1:
                    pg.showRelationTable()
        else:
            for compKey in compKeys:
                print('Relation table of component %s' % compKey)
                self.components[compKey]['subGraph'].showRelationTable()

    def computeBoostedKohlerRanking(self):
        """
        Renders an ordred list of decision actions ranked in
        decreasing preference direction following Kohler's rule
        on each component.
        """
        from linearOrders import KohlerOrder
##        from itertools import chain      
##        compKeys = list(self.components.keys())
##        compKeys.sort()
##        ranking = list(chain.from_iterable([self.components[ck]['subGraph'].computeKohlerRanking()\
##                                            for ck in compKeys]))
##        nc = self.nbrComponents
##
        ranking = []
        # self.components is an ordered dictionary in decreasing preference
        for cki in self.components:
            comp = self.components[cki]
            pg = comp['subGraph']
            pko = KohlerOrder(pg)
            ranking += pko.computeOrder()
        return ranking    

    def computeBoostedRankedPairsRanking(self):
        """
        Renders an ordred list of decision actions in decreasing preference direction following Tideman's Ranked Pairs rule on each component.
        """
        from linearOrders import KohlerOrder
        from itertools import chain
        
##        compKeys = list(self.components.keys())
##        compKeys.sort()
        ranking = list(chain.from_iterable(\
            [self.components[ck]['subGraph'].computeRankedPairsOrder()\
                                          for ck in self.components]))
        return ranking    

    def ranking2Preorder(self,ranking):
        """
        Renders a preordering (a list of list) of a ranking of decision actions in decreasing preference direction.
        """
        preordering = [[x] for x in ranking]
        return preordering

#----------test classes and methods ----------------
if __name__ == "__main__":
    
    from time import time
    MP  = True
    t0 = time()
##    tp = RandomCBPerformanceTableau(numberOfActions=200,Threading=MP,
##                                      seed=100)
    tp = RandomPerformanceTableau(numberOfActions=500,numberOfCriteria=21,
                                      seed=100)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigOutrankingDigraphMP(tp,quantiles=20,quantilesOrderingStrategy='average',
                                 LowerClosed=True,
                                 minimalComponentSize=1,
                                 Threading=MP,nbrOfCPUs=5,Debug=False)
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    print(bg1)
    #bg1.recodeValuation(-10,10,Debug=True)
    #print(total_size(bg1))
    
##    bg2 = BigOutrankingDigraph(tp,quantiles=100,quantilesOrderingStrategy='average',
##                                    LowerClosed=False,
##                                    Threading=MP,Debug=False)
##    print(bg2)
##    print(total_size(bg2))
##    print(bg2.computeDecompositionSummaryStatistics())
##    #bg2.showDecomposition()
##    t0 = time()
##    g = BipolarOutrankingDigraph(tp,Normalized=True,Threading=MP)
##    print(time()-t0)
##    print(total_size(g))
##    t0 = time()
##    print(bg1.computeOrdinalCorrelation(g,Debug=False))
##    print(bg2.computeOrdinalCorrelation(g,Debug=False))
##    print(bg2.computeOrdinalCorrelation(bg1,Debug=False))
##    print(time()-t0)
##    bg1.showShort('rest1.text')
##    bg2.showShort('rest2.text')
##    bg1.showShort()
##    
##    preordering1 = bg1.computeRankingPreordering()
##    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
##    preordering2 = bg2.computeRankingPreordering()
##    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering2)))
##    t0 = time()
##    test = Decimal('0')
##    for x in bg1.actions:
##        for y in bg1.actions:
##            test+=bg1.relation(x,y)
##    print('bg time:',time()-t0)
##    
##    t0 = time()
##    test = Decimal('0')
##    for x in g.actions:
##        for y in g.actions:
##            test+=g.relation[x][y]
##    print('g time:',time()-t0)
##    


    
