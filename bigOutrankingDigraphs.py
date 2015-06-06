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

class BigOutrankingDigraph(QuantilesSortingDigraph):
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
        
        from time import time
        from os import cpu_count
        
        ttot = time()
        # setting name
        perfTab = argPerfTab
        self.name = perfTab.name + '_mp'
        # setting quantiles sorting parameters
        na = len(perfTab.actions)
        self.order = na
        self.dimension = len(perfTab.criteria)
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
        self.components = {}
        nc = len(decomposition)
        self.nbrComponents = nc
        nd = len(str(nc))
        for i in range(1,nc+1):
            comp = decomposition[i-1]
            compKey = ('c%%0%dd' % (nd)) % (i)
            self.components[compKey] = {'rank':i}
            pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
            self.components[compKey]['lowQtileLimit'] = comp[0][1]
            self.components[compKey]['highQtileLimit'] = comp[0][0]
            self.components[compKey]['subGraph'] = BipolarOutrankingDigraph(pt)

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

    def __repr__(self,WithComponents=False):
        """
        Default presentation method for big outrankingDigraphs instances.
        """
        print('*----- show short --------------*')
        print('Instance name     :', self.name)
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
        for ck in self.components:
            comp = self.components[ck]
            pg = comp['subGraph']
            break
        print('*----  criteria -----*')
        sumWeights = Decimal('0.0')
        for g in pg.criteria:
            sumWeights += pg.criteria[g]['weight']
        criteriaList = [c for c in pg.criteria]
        criteriaList.sort()
        for c in criteriaList:
            try:
                criterionName = pg.criteria[c]['name']
            except:
                criterionName = ''
            print(c, repr(criterionName))
            print('  Scale =', pg.criteria[c]['scale'])
            if IntegerWeights:
                print('  Weight = %d ' % (pg.criteria[c]['weight']))
            else:
                weightg = pg.criteria[c]['weight']/sumWeights
                print('  Weight = %.3f ' % (weightg))
            try:
                for th in pg.criteria[c]['thresholds']:
                    if Debug:
                        print('-->>>', th,pg.criteria[c]['thresholds'][th][0],pg.criteria[c]['thresholds'][th][1])
                    print('  Threshold %s : %.2f + %.2fx' % (th,pg.criteria[c]['thresholds'][th][0],
                                                             pg.criteria[c]['thresholds'][th][1]), end=' ')
            except:
                pass
            print()

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
    t = RandomCBPerformanceTableau(numberOfActions=1000,Threading=True,seed=100)
    g = BigOutrankingDigraph(t,quantiles=100,quantilesOrderingStrategy='average',
                                    LowerClosed=True,
                                    Threading=True,Debug=False)
    print(g)
    print(g.computeDecompositionSummaryStatistics())
##    g.showActions()
##    g.showCriteria()
##    g.showRelationTable(['c14','c01'])
##    g.recodeValuation()
##    g.showRelationTable(['c14'])
##    print(g.computeBoostedKohlerOrdering())
    

