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

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint of an object and all of its contents.

    Automatically finds the contents of the following containers and
    their subclasses:  tuple, list, deque, dict, set, frozenset, Digraph and BigDigraph.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    See http://code.activestate.com/recipes/577504/  

    """
    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    
    try:
        from reprlib import repr
    except ImportError:
        pass

    # built-in containers and their subclasses
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                    }

    # Digraph3 objects 
    object_handler = lambda d: chain.from_iterable(d.__dict__.items())    
    handlers = {BigDigraph: object_handler,
                Digraph: object_handler,
                PerformanceTableau : object_handler,
                }
    
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

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
        elif self.componentRelation[cx][cy] < Med:
            return Min
        elif self.componentRelation[cx][cy] > Med:
            return Max 

    def relationOld(self,x,y,Debug=False):
        """
        Dynamic construction of the global digraph relation.
        """
        if x == y:
            return self.valuationdomain['med']
        
        selfActionsList = [(ck,
                            list(self.components[ck]['subGraph'].actions.keys()))\
                           for ck in self.components]
        if Debug:
            print(selfActionsList)

        precx = []
        Found = False
        for ckx in selfActionsList:
            
            if x in ckx[1]:    
                if Debug:
                    print(precx,ckx[1])
                if y in precx:
                    #print('self: %s < %s' % (x,y))
                    selfRelation = self.valuationdomain['min']
                elif y in ckx[1]:
                    #print('self: %s S %s' % (x,y))
                    selfRelation = self.components[ckx[0]]['subGraph'].relation[x][y] 
                else:
                    #print('self: %s > %s' % (x,y))
                    selfRelation = self.valuationdomain['max']
                if Debug:
                    print(selfRelation)
                Found = True
                break
            precx += ckx[1]
        if Found:
            return selfRelation
        else:
            return None
        
    
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
                print('Error: the BigDigraph instance must be normalized digraph !!')
        
        
        if issubclass(other.__class__,(Digraph)):
            if Debug:
                print('other is a Digraph instance')
            if other.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the other digraph must be normalized !!')
                return
        elif isinstance(other,(BigDigraph)):
            if Debug:
                print('other is a BigDigraph instance')
        
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
        import statistics
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

    def recodeValuation(self,newMin=-1,newMax=1):
        """
        Specialized for recoding the valuation of all the partial digraphs.
        By default the valuation domain is normalized ([-1.0;1.0])
        """
        nc = self.nbrComponents
        print('Recoding the valuation of %d subgraphs' % nc)
        compKeys = list(self.components.keys())
        compKeys.sort()
        for i in range(nc) :
            cki = compKeys[i]
            comp = self.components[cki]
            pg = comp['subGraph']
            pg.recodeValuation(newMin=newMin,newMax=newMax)
        Min = Decimal(str(newMin))
        Max = Decimal(str(newMax))
        Med = (Min+Max)/Decimal('2')
        self.valuationdomain = { 'min':Min, 'max':Max, 'med':Med }

class BigOutrankingDigraph(BigDigraph):
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
                 Threading=True,nbrOfCPUs=None,
                 Comments=False,
                 Debug=False):
        
        from sortingDigraphs import QuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
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
        if Threading:
            qs = QuantilesSortingDigraph(argPerfTab=perfTab,
                                            limitingQuantiles=quantiles,
                                            LowerClosed=LowerClosed,
                                            CompleteOutranking=False,
                                            Threading=True,
                                            nbrCores=nbrOfCPUs,
                                            Debug=Debug)
        else:
            qs = QuantilesSortingDigraph(argPerfTab=perfTab,
                                            limitingQuantiles=quantiles,
                                            LowerClosed=LowerClosed,
                                            CompleteOutranking=False,
                                            Threading=False,
                                            nbrCores=nbrOfCPUs,
                                            Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        if quantilesOrderingStrategy == 'average':
            decomposition = [((qs.categories[str(item[0][2])]['lowLimit'],
                                    qs.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in qs._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]
        elif quantilesOrderingStrategy == 'optimistic':
            decomposition = [((qs.categories[str(item[0][1])]['lowLimit'],
                                    qs.categories[str(item[0][0])]['highLimit']),item[1])\
                                  for item in qs._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]
        elif quantilesOrderingStrategy == 'pessimistic':
            decomposition = [((qs.categories[str(item[0][0])]['lowLimit'],
                                    qs.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in qs._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]

        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('weak ordering execution time: %.4f' % self.runTimes['preordering']  )
        # setting components
        t0 = time()
        components = OrderedDict()
        nc = len(decomposition)
        self.nbrComponents = nc
        nd = len(str(nc))
        for i in range(1,nc+1):
            comp = decomposition[i-1]
            compKey = ('c%%0%dd' % (nd)) % (i)
            components[compKey] = {'rank':i}
            pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
            components[compKey]['lowQtileLimit'] = comp[0][1]
            components[compKey]['highQtileLimit'] = comp[0][0]
            pg = BipolarOutrankingDigraph(pt,Normalized=True)
            pg.__dict__.pop('criteria')
            pg.__dict__.pop('evaluation')
            components[compKey]['subGraph'] = pg
            for x in comp[1]:
                self.actions[x]['component'] = compKey
        self.components = components

##        for ck in self.components:
##            for x in self.components[ck]['subGraph'].actions:
##                self.actions[x]['component'] = ck
                
        self.valuationdomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}

        compList = list(self.components.keys())
        compRel = {}
        for i in range(nc):
            cx = compList[i]
            compRel[cx] = {} 
            for j in range(nc):
                cy = compList[j]
                if self.components[cx]['rank'] < self.components[cy]['rank']:
                    compRel[cx][cy] = self.valuationdomain['max']
                elif self.components[cx]['rank'] > self.components[cy]['rank']:
                    compRel[cx][cy] = self.valuationdomain['min']
                else:
                    compRel[cx][cy] = self.valuationdomain['med']
        self.componentRelation = compRel
        
        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )
        # Kohler ranking-by-choosing all components
        t0 = time()
        self.boostedKohlerOrdering = self.computeBoostedKohlerOrdering()
        self.runTimes['ordering'] = time() - t0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)

    # ----- class methods ------------

    def __repr__(self,WithComponents=False):
        """
        Default presentation method for big outrankingDigraphs instances.
        """
        from sys import getsizeof
        print('*----- show short --------------*')
        print('Instance name     :', self.name)
        print('Size (in bytes)   :', total_size(self))
        print('# Actions         :', self.order)
        print('# Criteria        :', self.dimension)
        print('Sorting by        : %d-Tiling ' % self.sortingParameters['limitingQuantiles'])
        print('Ordering strategy :', self.sortingParameters['strategy'],'quantile')
        print('# Components      :', self.nbrComponents)
        if WithComponents:
            g.showDecomposition()
        print('----  Constructor run times (in sec.) ----')
        print('Total time        : %.5f' % self.runTimes['totalTime'])
        print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
        print('Preordering       : %.5f' % self.runTimes['preordering'])
        print('Decomposing       : %.5f' % self.runTimes['decomposing'])
        print('Ordering          : %.5f' % self.runTimes['ordering'])
        return 'Default presentation of BigOutrankingDigraphs'

    def showShort(self):
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
        print(g)

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

    def computeBoostedKohlerOrdering(self):
        """
        Renders an ordred list of decision actions in decreasing preference direction.
        """
        from linearOrders import KohlerOrder
        compKeys = list(self.components.keys())
        compKeys.sort()
        nc = self.nbrComponents
        ordering = []
        for i in range(nc) :
            cki = compKeys[i]
            comp = self.components[cki]
            pg = comp['subGraph']
            pko = KohlerOrder(pg)
            ordering += pko.computeOrder()
        return ordering    

#----------test classes and methods ----------------
if __name__ == "__main__":
    
    from time import time
    MP = False
    t0 = time()
    tp = RandomCBPerformanceTableau(numberOfActions=100,Threading=MP,
                                      seed=100)
    print(time()-t0)
    print(total_size(tp.evaluation))
    bg1 = BigOutrankingDigraph(tp,quantiles=10,quantilesOrderingStrategy='average',
                                    LowerClosed=True,
                                    Threading=False,Debug=False)
    print(bg1)
    print(total_size(bg1))
    print(bg1.computeDecompositionSummaryStatistics())
    bg1.showDecomposition()
    bg2 = BigOutrankingDigraph(tp,quantiles=5,quantilesOrderingStrategy='average',
                                    LowerClosed=False,
                                    Threading=MP,Debug=False)
    print(bg2)
    print(total_size(bg2))
    print(bg2.computeDecompositionSummaryStatistics())
    bg2.showDecomposition()
    bg1.recodeValuation(-1,1)
    t0 = time()
    g = BipolarOutrankingDigraph(tp,Normalized=False,Threading=MP)
    print(time()-t0)
    print(total_size(g))
    t0 = time()
    g.recodeValuation(-1,1)
    print(bg1.computeOrdinalCorrelation(g,Debug=False))
    print(time()-t0)
    

