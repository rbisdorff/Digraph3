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
from bigOutrankingDigraphs import *

class BigDigraph(object):
    """
    abstract root class for lineraly decomposed big digraphs (order > 1000) using multiprocessing ressources.
    """
    def __repr__(self):
        """
        Default presentation method for bigDigraphs instances.
        """
        print('*----- show short --------------*')
        print('Instance name     : %s' % self.name)
        print('# Actions         : %d' % self.order)
        print('# Criteria        : %d' % self.dimension)
        print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
        print('Ordering strategy : %s' % self.sortingParameters['strategy'])
        print('# Components      : %d' % self.nbrComponents)
        print('Minimal size      : %d' % self.minimalComponentSize)
        print('Maximal size      : %d' % (self.computeDecompositionSummaryStatistics())['max'])
        print('Median size      : %d' % (self.computeDecompositionSummaryStatistics())['median'])
        print('----  Constructor run times (in sec.) ----')
        print('Total time        : %.5f' % self.runTimes['totalTime'])
        print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
        print('Preordering       : %.5f' % self.runTimes['preordering'])
        print('Decomposing       : %.5f' % self.runTimes['decomposing'])
        try:
            print('Ordering          : %.5f' % self.runTimes['ordering'])
        except:
            pass
        return '%s instance' % str(self.__class__)
    
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
        
        selfActionsList = ((ck,
                            list(self.components[ck]['subGraph'].actions.keys()))\
                           for ck in self.components)
        if issubclass(other.__class__,(Digraph)):
            otherActionsList = [( 'c01', list(other.actions.keys()) )]
        else:
            otherActionsList = ((ck,
                            list(other.components[ck]['subGraph'].actions.keys()))\
                           for ck in other.components)
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
        print('Recoding the valuation of a BigDigraph instance')
        for cki in self.components.keys(): 
            self.components[cki]['subGraph'].recodeValuation(newMin=newMin,newMax=newMax)
       # update valuation domain                       
        Min = Decimal(str(newMin))
        Max = Decimal(str(newMax))
        Med = (Min+Max)/Decimal('2')
        self.valuationdomain = { 'min':Min, 'max':Max, 'med':Med }

    def ranking2Preorder(self,ranking):
        """
        Renders a preordering (a list of list) of a ranking of decision actions in decreasing preference direction.
        """
        ordering = list(ranking)
        ordering.reverse()
        preordering = [[x] for x in ordering]
        return preordering

    def ordering2Preorder(self,ordering):
        """
        Renders a preordering (a list of list) of a ranking of decision actions in decreasing preference direction.
        """
        preordering = [[x] for x in ordering]
        return preordering


##    def computeCriterionCorrelation(self,criterion,Threading=False,\
##                                    nbrOfCPUs=None,Debug=False,
##                                    Comments=False):
##        """
##        Renders the ordinal correlation coefficient between
##        the global outranking and the marginal criterion relation.
##
##        If Threading, the 
##        """
##        gc = BipolarOutrankingDigraph(self,coalition=[criterion],
##                                      Normalized=True,CopyPerfTab=False,
##                                      Threading=Threading,nbrCores=nbrOfCPUs,
##                                      Comments=Comments)
##        corr = self.computeOrdinalCorrelation(gc)
##        if Debug:
##            print(corr)
##        return corr
##
##    def computeMarginalVersusGlobalOutrankingCorrelations(self,Sorted=True,
##                                                          Threading=False,nbrCores=None,\
##                                                          Comments=False):
##        """
##        Method for computing correlations between each individual criterion relation with the corresponding
##        global outranking relation.
##        
##        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.
##
##        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.
##
##        If nbrCores is not set, the os.cpu_count() function is used to determine the number of
##        available cores.
##        """
##        if Threading:
##            from multiprocessing import Pool
##            from os import cpu_count
##            if nbrCores == None:
##                nbrCores= cpu_count()
##            criteriaList = [x for x in self.criteria]
##            with Pool(nbrCores) as proc:   
##                correlations = proc.map(self.computeCriterionCorrelation,criteriaList)
##            criteriaCorrelation = [(correlations[i]['correlation'],criteriaList[i]) for i in range(len(criteriaList))]
##        else:
##            #criteriaList = [x for x in self.criteria]
##            criteria = self.criteria
##            criteriaCorrelation = []
##            for c in dict.keys(criteria):
##                corr = self.computeCriterionCorrelation(c,Threading=False)
##                criteriaCorrelation.append((corr['correlation'],c))            
##        if Sorted:
##            criteriaCorrelation.sort(reverse=True)
##        return criteriaCorrelation   
##
##    def showMarginalVersusGlobalOutrankingCorrelation(self,Sorted=True,Threading=False,\
##                                                      nbrOfCPUs=None,Comments=True):
##        """
##        Show method for computeCriterionCorrelation results.
##        """
##        criteria = self.criteria
##        #criteriaList = [x for x in self.criteria]
##        criteriaCorrelation = []
##        totCorrelation = Decimal('0.0')
##        for c in dict.keys(criteria):
##            corr = self.computeCriterionCorrelation(c,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
##            totCorrelation += corr['correlation']
##            criteriaCorrelation.append((corr['correlation'],c))
##        if Sorted:
##            criteriaCorrelation.sort(reverse=True)
##        if Comments:
##            print('Marginal versus global outranking correlation')
##            print('criterion | weight\t correlation')
##            print('----------|---------------------------')
##            for x in criteriaCorrelation:
##                c = x[1]
##                print('%9s |  %.2f \t %.3f' % (c,self.criteria[c]['weight'],x[0]))
##            print('Sum(Correlations) : %.3f' % (totCorrelation))
##            print('Determinateness   : %.3f' % (corr['determination']))

########################
class BigOutrankingDigraph(BigDigraph,PerformanceTableau):
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
    def __init__(self,argPerfTab=None,quantiles=None,\
                 quantilesOrderingStrategy='average',\
                 LowerClosed=True,\
                 WithKohlerOrdering=True,\
                 minimalComponentSize=None,\
                 Threading=True,\
                 nbrOfCPUs=None,\
                 save2File=None,\
                 Comments=False,\
                 Debug=False):
        
        from digraphs import Digraph
        from sortingDigraphs import QuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from copy import copy as deepcopy
        
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
                                        Threading=Threading,
                                        nbrCores=nbrOfCPUs,
                                        Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
        self.qs = qs
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        if quantilesOrderingStrategy == 'average':
            decomposition = [((qs.categories[str(item[0][2])]['lowLimit'],
                                    qs.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]
        elif quantilesOrderingStrategy == 'optimistic':
            decomposition = [((qs.categories[str(item[0][1])]['lowLimit'],
                                    qs.categories[str(item[0][0])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]
        elif quantilesOrderingStrategy == 'pessimistic':
            decomposition = [((qs.categories[str(item[0][0])]['lowLimit'],
                                    qs.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=quantilesOrderingStrategy,
                                         Descending=True)]

        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('weak ordering execution time: %.4f' % self.runTimes['preordering']  )
        # setting components
        t0 = time()
        if minimalComponentSize == None:
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
                pg.__dict__.pop('vetos')
                pg.__dict__.pop('negativeVetos')
                pg.__dict__.pop('largePerformanceDifferencesCount')
                pg.__dict__.pop('concordanceRelation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
                for x in comp[1]:
                    self.actions[x]['component'] = compKey
            self.components = components
            self.minimalComponentSize = 1
        else:  # with minimal component size
            components = OrderedDict()
            ndc = len(decomposition)
            nd = len(str(ndc))
            compNbr = 1
            compContent = []
            for i in range(1,ndc+1):
                currContLength = len(compContent)
                comp = decomposition[i-1]
                if currContLength == 0:
                    lowQtileLimit = comp[0][1]
                compContent += comp[1]

                if len(compContent) >= minimalComponentSize or i == ndc:
                    compKey = ('c%%0%dd' % (nd)) % (compNbr)
                    components[compKey] = {'rank':compNbr}
                    pt = PartialPerformanceTableau(perfTab,actionsSubset=compContent)
                    components[compKey]['lowQtileLimit'] = lowQtileLimit
                    components[compKey]['highQtileLimit'] = comp[0][0]
                    pg = BipolarOutrankingDigraph(pt,Normalized=True)
                    pg.__dict__.pop('criteria')
                    pg.__dict__.pop('evaluation')
                    pg.__class__ = Digraph
                    components[compKey]['subGraph'] = pg
                    for x in compContent:
                        self.actions[x]['component'] = compKey
                    compContent = []
                    compNbr += 1
            self.components = components
            self.minimalComponentSize = minimalComponentSize
            nc = len(components)
            self.nbrComponents = nc
        # setting the valuation domain
        self.valuationdomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )
        # Kohler ranking-by-choosing all components
        if WithKohlerOrdering:
            t0 = time()
            self.boostedKohlerOrder = self.computeBoostedKohlerOrder()
            self.runTimes['ordering'] = time() - t0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)
            

    # ----- class methods ------------

    def computeCriterionCorrelation(self,criterion,Threading=False,\
                                    nbrOfCPUs=None,Debug=False,
                                    Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the global outranking and the marginal criterion relation.
        
        """
        #print(criterion)
        gc = BipolarOutrankingDigraph(self,coalition=[criterion],
                                      Normalized=True,CopyPerfTab=False,
                                      Threading=Threading,nbrCores=nbrOfCPUs,
                                      Comments=Comments)
        globalOrdering = self.ranking2Preorder(self.boostedNetFlowsRanking)
        globalRelation = gc.computePreorderRelation(globalOrdering)
        corr = gc.computeOrdinalCorrelation(globalRelation)
        if Debug:
            print(corr)
        return corr

    def computeMarginalVersusGlobalOutrankingCorrelations(self,Sorted=True,
                                                          Threading=False,nbrCores=None,\
                                                          Comments=False):
        """
        Method for computing correlations between each individual criterion relation with the corresponding
        global outranking relation.
        
        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of
        available cores.
        """
        if Threading:
            from multiprocessing import Pool
            from os import cpu_count
            if nbrCores == None:
                nbrCores= cpu_count()
            criteriaList = [x for x in self.criteria]
            with Pool(nbrCores) as proc:   
                correlations = proc.map(self.computeCriterionCorrelation,criteriaList)
            criteriaCorrelation = [(correlations[i]['correlation'],criteriaList[i]) for i in range(len(criteriaList))]
        else:
            #criteriaList = [x for x in self.criteria]
            criteria = self.criteria
            criteriaCorrelation = []
            for c in dict.keys(criteria):
                corr = self.computeCriterionCorrelation(c,Threading=False)
                criteriaCorrelation.append((corr['correlation'],c))            
        if Sorted:
            criteriaCorrelation.sort(reverse=True)
        return criteriaCorrelation   

    def showMarginalVersusGlobalOutrankingCorrelation(self,Sorted=True,Threading=False,\
                                                      nbrOfCPUs=None,Comments=True):
        """
        Show method for computeCriterionCorrelation results.
        """
        criteria = self.criteria
        criteriaCorrelation = []
        for c in criteria:
            corr = self.computeCriterionCorrelation(c,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
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

    def _computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                Debug=False,
                                 Comments=False):
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
                     self.computeActionCategories(x,Comments=Comments)
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
    

    def _computeQuantileOrderingMP(self,strategy=None,
                                Descending=True,
                                Debug=False,
                                nbrOfCPUs=None):
        """
        !!! Example of hopelessly inefficient multiprocessing of a rather simple task and insufficient granularity
        """
        from multiprocessing import Pool
        from os import cpu_count
        if nbrOfCPUs == None:
            nbrOfCPUs = cpu_count()
        if strategy == None:
            strategy = self.sortingParameters['strategy']
        actionsCategoriesList = [] 
        actions = self.actions
        showActionCategories = self.showActionCategories
        with Pool(processes=nbrOfCPUs) as pool:
            actionsCategoriesList = [(a,lowCateg,highCateg,credibility) for\
                                     a,lowCateg,highCateg,credibility in\
                                     pool.map(showActionCategories,actions.keys())]
        actionsCategories = OrderedDict()
        for a,lowCateg,highCateg,credibility in actionsCategoriesList:
            # too much non parallel work to do
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

    def computeActionCategories(self,action,Debug=False,Show=False,Comments=False,Threading=False,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        qs = self.qs
        Med = qs.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = qs.computeSortingCharacteristics(action=action,Comments=Comments,Debug=Debug,\
                                                   Threading=Threading,nbrOfCPUs=nbrOfCPUs)
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
            if Show:
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
            if Show:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     qs.categories[keys[0]]['lowLimit'],\
                                     qs.categories[keys[-1]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility            

    def showActionsSortingResult(self,actionSubset=None):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        print('Quantiles sorting result per decision action')
        if actionsSubset==None:
            for x in actions.keys():
                self.computeActionCategories(x,Show=True)
        else:
            for x in actionsSubset:
                self.computeActionCategories(x,Show=True)

    def showShort(self,fileName=None,WithFileSize=True):
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
        summaryStats = self.computeDecompositionSummaryStatistics()
        if fileName == None:
            print('*----- show short --------------*')
            print('Instance name     : %s' % self.name)
            print('# Actions         : %d' % self.order)
            print('# Criteria        : %d' % self.dimension)
            print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
            print('Ordering strategy : %s' % self.sortingParameters['strategy'])
            print('# Components      : %d' % self.nbrComponents)
            print('Minimal size      : %d' % self.minimalComponentSize)
            print('Maximal size      : %d' % summaryStats['max'])
            print('Median size       : %d' % summaryStats['median'])
            print('----  Constructor run times (in sec.) ----')
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
            fo.write('# Components       : %d\n' % self.nbrComponents)
            fo.write('Minimal size       : %d\n' % self.minimalComponentSize)
            fo.write('Maximal size       : %d\n' % summaryStats['max'])
            fo.write('Median size        : %d\n' % summaryStats['median'])
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
        compKeys = [compKey for compKey in self.components.keys()]
        # the components are ordered from best (1) to worst (n)
        if direction != 'decreasing':
            compKeys.sort(reverse=True)
        else:
            pass
        for compKey in compKeys:
            comp = self.components[compKey]
            sg = comp['subGraph']
            actions = [x for x in dict.keys(sg.actions)]
            actions.sort()
            if self.sortingParameters['LowerClosed']:
                print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],actions))
            else:
                print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],actions))

    def showRelationTable(self,compKeys=None):
        """
        Specialized for showing the quantiles decomposed relation table.
        Components are stored in an ordered dictionary.
        """
        components = self.components
        if compKeys == None:
            nc = self.nbrComponents
            print('%d quantiles decomposed relation table in decreasing order' % nc)
            for compKey in components.keys():
                comp = components[compKey]
                pg = comp['subGraph']
                print('Component :', compKey, end=' ')
                actions = [ x for x in pg.actions.keys()]
                print('%s' % actions)
                if pg.order > 1:
                    pg.showRelationTable()
                    
        else:
            for compKey in compKeys:
                comp = components[compkey]
                pg = comp['subGraph']
                print('Relation table of component %s' % compKey)
                actions = [ x for x in pg.actions.keys()]
                print('%s' % actions)
                if pg.order > 1:
                    pg.showRelationTable()                

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
        for cki in dict.keys(self.components):
            comp = self.components[cki]
            pg = comp['subGraph']
            pko = KohlerOrder(pg)
            ranking += pko.computeRanking()
        return ranking

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
            ranking += pko.computeRanking()
        return ranking

    def computeBoostedKohlerOrder(self):
        """
        Renders an ordred list of decision actions ranked in
        increasing preference direction following Kohler's rule
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
        ordering = []
        compKeys = list(self.components.keys())
        compKeys.reverse()
        # self.components is an ordered dictionary in decreasing preference
        for cki in compKeys:
            comp = self.components[cki]
            pg = comp['subGraph']
            pko = KohlerOrder(pg)
            ordering += pko.computeOrder()
        return ordering
    
    def computeBoostedNetFlowsRanking(self):
        """
        Renders an ordred list of decision actions ranked in
        decreasing preference direction following the net flows rule
        on each component.
        """
        from linearOrders import NetFlowsOrder
        ranking = []
        # self.components is an ordered dictionary in decreasing preference
        for cki in self.components:
            comp = self.components[cki]
            pg = comp['subGraph']
            pko = NetFlowsOrder(pg)
            ranking += pko.computeRanking()
        return ranking

    def computeBoostedNetFlowsOrder(self):
        """
        Renders an ordred list of decision actions ranked in
        increasing preference direction following the net flowsa rule
        on each component.
        """
        from linearOrders import NetFlowsOrder
        ordering = []
        compKeys = list(self.components.keys())
        compKeys.reverse()
        # self.components is an ordered dictionary in decreasing preference
        for cki in compKeys:
            comp = self.components[cki]
            pg = comp['subGraph']
            ordering += pg.computeNetFlowsOrder()
        return ordering

    def computeBoostedRankedPairsRanking(self):
        """
        Renders an ordred list of decision actions in decreasing preference direction following Tideman's Ranked Pairs rule on each component.
        """
        from linearOrders import KohlerOrder
        from itertools import chain
        
##        compKeys = list(self.components.keys())
##        compKeys.sort()
        ranking = list(chain.from_iterable(\
            [self.components[ck]['subGraph'].computeRankedPairsRanking()\
                                          for ck in self.components]))
        return ranking    

    def computeBoostedRankedPairsOrder(self):
        """
        Renders an ordred list of decision actions in decreasing preference direction following Tideman's Ranked Pairs rule on each component.
        """
        from linearOrders import KohlerOrder
        from itertools import chain
        
        compKeys = list(self.components.keys())
        compKeys.reverse()
        ranking = list(chain.from_iterable(\
            [self.components[ck]['subGraph'].computeRankedPairsOrder()\
                                          for ck in compKeys]))
        return ranking    

##    def ranking2Preorder(self,ordering):
##        """
##        Renders a preordering (a list of list) of a ranking of decision actions in decreasing preference direction.
##        """
##        preordering = [[x] for x in ordering]
##        return preordering
##        

########################
from weakOrders import QuantilesRankingDigraph
class BigOutrankingDigraphMP(BigOutrankingDigraph,QuantilesRankingDigraph,PerformanceTableau):
    """
    Multiprocessing implementation of the BipolarOutrankingDigraph class
    for large instances (order > 1000)

    The outranking digraph is decomposed with a q-tiles sorting into a partition of
    quantile equivalence classes, which are lineraly ordred by average quantile limits. (default).

    To each quantile equivalence class is associated a BipolarOutrankingDigraph object
    which is restricted to a Digraph instance.

    By default, q is set to a tenth of the number of decision actions,
    ie q = order//10.

    For other parameters settings, see the corresponding QuantilesSortingDigraph class.

    """
    def __init__(self,argPerfTab=None,CopyPerfTab=True,
                 quantiles=None,
                 quantilesOrderingStrategy='average',
                 LowerClosed=True,
                 WithKohlerOrdering=False,
                 WithNetFlowsOrdering=True,
                 minimalComponentSize=None,
                 Threading=False,nbrOfCPUs=None,
                 nbrOfThreads=None,
                 save2File=None,
                 Comments=False,
                 Debug=False):
        
        from digraphs import Digraph
        from sortingDigraphs import QuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from multiprocessing import Pool
        from copy import copy, deepcopy
        
        ttot = time()
        # setting name
        perfTab = argPerfTab
        self.name = perfTab.name + '_mp'
        # setting quantiles sorting parameters
        if CopyPerfTab:
            copy2self = deepcopy
        else:
            copy2self = copy
        self.actions = copy2self(perfTab.actions)
        na = len(self.actions)
        self.order = na
        self.criteria = copy2self(perfTab.criteria)
        self.dimension = len(perfTab.criteria)
        self.evaluation = copy2self(perfTab.evaluation)
        if quantiles == None:
            quantiles = na//10
        self.sortingParameters = {}
        self.sortingParameters['limitingQuantiles'] = quantiles
        self.sortingParameters['strategy'] = quantilesOrderingStrategy
        self.sortingParameters['LowerClosed'] = LowerClosed
        self.sortingParameters['Threading'] = Threading
        self.sortingParameters['PrefThresholds'] = False
        self.sortingParameters['hasNoVeto'] = False
        self.nbrOfCPUs = nbrOfCPUs
        # quantiles sorting
        t0 = time()
        if Comments:        
            print('Computing the %d-quantiles sorting digraph ...' % (quantiles))
        #if Threading:
        qs = QuantilesSortingDigraph(argPerfTab=perfTab,CopyPerfTab=CopyPerfTab,
                                        limitingQuantiles=quantiles,
                                        LowerClosed=LowerClosed,
                                        CompleteOutranking=False,
                                        StoreSorting=True,
                                        WithSortingRelation=False,
                                        Threading= self.sortingParameters['Threading'],
                                        nbrCores=nbrOfCPUs,
                                        Comments=Comments,
                                        Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
#        self.qs = qs
        self.valuationdomain = qs.valuationdomain
        self.profiles = qs.profiles
        self.categories = qs.categories
        self.sorting = qs.sorting
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
        if minimalComponentSize == None:
            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][0],item[0][1]),item[1]]\
                for item in self._computeQuantileOrdering(\
                    strategy=quantilesOrderingStrategy,\
                    Descending=True,Threading=Threading,nbrOfCPUs=nbrOfThreads)]
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
            components = OrderedDict()
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                #print(comp)
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                #print(perfTab,comp[1])
                pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = BipolarOutrankingDigraph(pt,
                                              WithConcordanceRelation=False,
                                              WithVetoCounts=False,
                                              Normalized=True)
                pg.__dict__.pop('criteria')
                pg.__dict__.pop('evaluation')
                #pg.__dict__.pop('vetos')
                #pg.__dict__.pop('negativeVetos')
                #pg.__dict__.pop('largePerformanceDifferencesCount')
                #pg.__dict__.pop('concordanceRelation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
        else:   # if self.sortingParameters['Threading'] == True:
            from copy import copy, deepcopy
            from pickle import dumps, loads, load
            from multiprocessing import Process, active_children, cpu_count
            #Debug=True
            class myThread(Process):
                def __init__(self, threadID,\
                             tempDirName,\
                             lTest,\
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
                        print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadID)))
                        print('lTest',lTest)
                    fi = open('dumpSelf.py','rb')
                    context = loads(fi.read())
                    fi.close()
                    for i in lTest:
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
            #from copy import copy, deepcopy
            #from time import sleep
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
                nbrOfCPUs = cpu_count()
            if nbrOfThreads == None:
                nbrOfThreads = nbrOfCPUs-1
            print('Nbr of components',nc)
            nbrOfJobs = nc//nbrOfThreads
            if nbrOfJobs*nbrOfThreads < nc:
                nbrOfJobs += 1
##            if nbrOfJobs < nbrOfCPUs:
##                nbrOfJobs,nbrOfCPUs = nbrOfCPUs,nbrOfJobs
            print('Nbr of threads = ',nbrOfThreads)
            print('Nbr of jobs/thread',nbrOfJobs)
            nbrOfThreadsUsed = 0
            for j in range(nbrOfThreads):
                print('thread = %d/%d' % (j+1,nbrOfThreads),end="...")
                start= j*nbrOfJobs
                if (j+1)*nbrOfJobs < nc:
                    stop = (j+1)*nbrOfJobs
                else:
                    stop = nc
                lTest = list(range(start,stop))
                print(lTest)
                if lTest != []:
                    process = myThread(j,tempDirName,lTest,Debug)
                    process.start()
                    nbrOfThreadsUsed += 1
            while active_children() != []:
                pass
                #sleep(1)
            print('Exit %d threads' % nbrOfThreadsUsed)
            components = OrderedDict()
            #componentsList = []
            for j in range(nc):
                if Debug:
                    print('job',j)
                fiName = tempDirName+'/splitComponent-'+str(j)+'.py'
                fi = open(fiName,'rb')
                splitComponent = loads(fi.read())
                if Debug:
                    print('splitComponent',splitComponent)
                components[splitComponent[0]] = splitComponent[1]
            #print(componentsList)
            #components = OrderedDict(componentsList)
        # end of Threading
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
        if WithKohlerOrdering:
            t0 = time()
            self.boostedKohlerOrder = self.computeBoostedKohlerOrder()
            self.boostedKohlerRanking = list(self.boostedKohlerOrder)
            self.boostedKohlerRanking.reverse()
            self.runTimes['ordering'] = time() - t0
        if WithNetFlowsOrdering:
            t0 = time()
            self.boostedNetFlowsOrder = self.computeBoostedNetFlowsOrder()
            self.boostedNetFlowsRanking = list(self.boostedNetFlowsOrder)
            self.boostedNetFlowsRanking.reverse()
            self.runTimes['ordering'] = time() - t0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)
            

    # ----- class methods ------------



    def _computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                 Threading=False,
                                 nbrOfCPUs=None,
                                Debug=False,
                                 Comments=False):
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
                     self.computeActionCategories(x,Comments=Comments,Debug=Debug,\
                                               Threading=Threading,\
                                               nbrOfCPUs = nbrOfCPUs)
            lowQtileLimit = self.categories[lowCateg]['lowLimit']
            highQtileLimit = self.categories[highCateg]['highLimit']
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
        if Debug:
            print(actionsCategIntervals)
        CompSize = self.minimalComponentSize 
        if CompSize == 1:
            if Descending:
                componentsIntervals = [[(item[0][1],item[0][2]),item[1]]\
                                   for item in actionsCategIntervals]
            else:
                componentsIntervals = [[(item[0][2],item[0][1]),item[1]]\
                                   for item in actionsCategIntervals]
                
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
                    if Descending:
                        componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent])
                    else:
                        componentsIntervals.append([(lowQtileLimit,highQtileLimit),compContent])
                    compContent = []
        if Debug:
            print(componentsIntervals)
        return componentsIntervals        

    def computeActionCategories(self,action,Show=False,Debug=False,Comments=False,\
                             Threading=True,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        #qs = self.qs
        qs = self
        Med = qs.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,Comments=Comments,\
                                                   Threading=Threading,\
                                                   nbrOfCPUs=nbrOfCPUs)      
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
            if Show:
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
            if Show:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     qs.categories[keys[0]]['lowLimit'],\
                                     qs.categories[keys[-1]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility            
    

##    def showActionsSortingResult(self,actionSubset=None):
##        """
##        shows the quantiles sorting result all (default) of a subset of the decision actions.
##        """
##        print('Quantiles sorting result per decision action')
##        if actionsSubset==None:
##            for x in actions.keys():
##                self.computeActionCategories(x,Show=True)
##        else:
##            for x in actionsSubset:
##                self.computeActionCategories(x,Show=True)
##            

##    def showShort(self,fileName=None,WithFileSize=True):
##        """
##        Default (__repr__) presentation method for big outranking digraphs instances:
##        
##        >>> from bigOutrankingDigraphs import *
##        >>> t = RandomCBPerformanceTableau(numberOfActions=100)
##        >>> g = BigOutrankingDigraph(t,quantiles=10)
##        Threading ...
##        Nbr of cpus =  7
##        number of cores = 7
##        nbr of actions to split 100
##        nbr of jobs =  7
##        nbr of splitActions =  15
##        iteration =  1 15
##        iteration =  2 15
##        iteration =  3 15
##        iteration =  4 15
##        iteration =  5 15
##        iteration =  6 15
##        iteration =  7 10
##        Exiting computing threads
##        >>> print(g)
##        *----- show short --------------*
##        Instance name     : randomCBperftab_mp
##        # Actions         : 100
##        # Criteria        : 13
##        Sorting by        : 10-Tiling 
##        Ordering strategy : average quantile
##        # Components      : 11
##        ----  Constructor run times (in sec.) ----
##        Total time        : 0.72743
##        QuantilesSorting  : 0.51481
##        Preordering       : 0.00292
##        Decomposing       : 0.20469
##        Ordering          : 0.00500
##        Default presentation of BigOutrankingDigraphs
##        
##        """
##        if fileName == None:
##            print('*----- show short --------------*')
##            print('Instance name     : %s' % self.name)
##            print('# Actions         : %d' % self.order)
##            print('# Criteria        : %d' % self.dimension)
##            print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
##            print('Ordering strategy : %s' % self.sortingParameters['strategy'])
##            print('# Components      : %d' % self.nbrComponents)
##            print('Minimal size      : %d' % self.minimalComponentSize)
##            print('Maximal size      : %d' % (self.computeDecompositionSummaryStatistics())['max'])
##            print('Median size       : %d' % (self.computeDecompositionSummaryStatistics())['median'])
##            print('----  Constructor run times (in sec.) ----')
##            print('Total time        : %.5f' % self.runTimes['totalTime'])
##            print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
##            print('Preordering       : %.5f' % self.runTimes['preordering'])
##            print('Decomposing       : %.5f' % self.runTimes['decomposing'])
##            try:
##                print('Ordering          : %.5f' % self.runTimes['ordering'])
##            except:
##                pass
##        else:
##            fo = open(fileName,'a')
##            fo.write('*----- show short --------------*')
##            fo.write('Instance name      : %s\n' % self.name)
##            if WithFileSize:
##                fo.write('Size (in bytes)    : %d\n' % total_size(self))
##            fo.write('# Actions          : %d\n' % self.order)
##            fo.write('# Criteria         : %d\n' % self.dimension)
##            fo.write('Sorting by         : %d-Tiling\n' % self.sortingParameters['limitingQuantiles'])
##            fo.write('Ordering strategy  : %s\n' % self.sortingParameters['strategy'])
##            fo.write('# Components       : %d\n' % self.nbrComponents)
##            fo.write('Minimal size       : %d\n' % self.minimalComponentSize)
##            fo.write('Maximal size       : %d\n' % (self.computeDecompositionSummaryStatistics())['max'])
##            fo.write('Median size        : %d\n' % (self.computeDecompositionSummaryStatistics())['median'])
##            fo.write('*-- Constructor run times (in sec.) --*\n')
##            fo.write('Total time         : %.5f\n' % self.runTimes['totalTime'])
##            fo.write('QuantilesSorting   : %.5f\n' % self.runTimes['sorting'])
##            fo.write('Preordering        : %.5f\n' % self.runTimes['preordering'])
##            fo.write('Decomposing        : %.5f\n' % self.runTimes['decomposing'])
##            try:
##                fo.write('Ordering           : %.5f\n' % self.runTimes['ordering'])
##            except:
##                pass
##            fo.close()

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

##    def showComponents(self):
##        self.showDecomposition()
##


##    def computeBoostedKohlerRanking(self):
##        """
##        Renders an ordred list of decision actions ranked in
##        decreasing preference direction following Kohler's rule
##        on each component.
##        """
##        from linearOrders import KohlerOrder
##        from itertools import chain
##
##        components = self.components
####        compKeys = list(self.components.keys())
####        compKeys.sort()
##        ranking = list(chain.from_iterable([self.components[ck]['subGraph'].computeKohlerRanking()\
##                                            for ck in components.keys()]))
####        nc = self.nbrComponents
####
####        components = self.components
####        ranking = []
####        # self.components is an ordered dictionary in decreasing preference
####        for cki in components.keys():
####            comp = components[cki]
####            pg = comp['subGraph']
####            pko = KohlerOrder(pg)
####            ranking += pko.computeOrder()
##        return ranking    
##
##    def computeBoostedRankedPairsRanking(self):
##        """
##        Renders an ordred list of decision actions in decreasing preference direction following Tideman's Ranked Pairs rule on each component.
##        """
##        from linearOrders import RankedPairsOrder
##        from itertools import chain
##        
####        compKeys = list(self.components.keys())
####        compKeys.sort()
##        components = self.components
##        ranking = list(chain.from_iterable(\
##            [components[ck]['subGraph'].computeRankedPairsRanking()\
##                                          for ck in components.keys()]))
####        ranking = []
####        for cki in components.keys():
####            comp = components[cki]
####            pg = comp['subGraph']
####            prp = RankedPairsOrder(pg)
####            ranking += prp.computeOrder()
##        return ranking    

##    def ranking2Preorder(self,ranking):
##        """
##        Renders a preordering (a list of list) of a ranking of decision actions in decreasing preference direction.
##        """
##        ordering = list(ranking)
##        ordering.reverse()
##        preordering = [[x] for x in ranking]
##        return preordering

#----------test classes and methods ----------------
if __name__ == "__main__":
    
    from time import time
    from weakOrders import QuantilesRankingDigraph
    MP  = True
##    t0 = time()
##    tp = Random3ObjectivesPerformanceTableau(numberOfActions=500,seed=100)
##    tp = RandomCBPerformanceTableau(numberOfActions=500,Threading=MP,
##                                      seed=100)
    tp = RandomPerformanceTableau(numberOfActions=50,numberOfCriteria=21,
                                      seed=100)
##    print(time()-t0)
##    print(total_size(tp.evaluation))
##    t0 = time()
##    qr = QuantilesRankingDigraph(tp,75,strategy='average',Threading=MP)
##    print(time()-t0)
##    qr.showWeakOrder()
    bg1 = BigOutrankingDigraphMP(tp,CopyPerfTab=False,quantiles=75,quantilesOrderingStrategy='average',
                                 LowerClosed=False,WithNetFlowsOrdering=True,
                                 minimalComponentSize=5,
                                 Threading=MP,nbrOfCPUs=8,
                                 nbrOfThreads=4,
                                 Comments=False,Debug=False)
##    print(bg1.computeDecompositionSummaryStatistics())
##    bg1.showDecomposition(direction='decreasing')
    print(bg1)
##    bg1.showMarginalVersusGlobalOutrankingCorrelation(Threading=MP)
##    bg2 = BigOutrankingDigraphMP(tp,quantiles=75,quantilesOrderingStrategy='average',
##                                 LowerClosed=True,
##                                 minimalComponentSize=5,
##                                 Threading=MP,nbrOfCPUs=5,Debug=False)
##    print(bg2.computeDecompositionSummaryStatistics())
##    bg2.showDecomposition(direction='decreasing')
##    print(bg2)
##    #bg1.recodeValuation(-10,10,Debug=True)
##    #print(total_size(bg1))
    
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
##    preordering1 = bg1.ranking2Preorder(bg1.boostedKohlerRanking)
##    print(g.computeOrdinalCorrelation(qr))
##    print(g.computeOrdinalCorrelation(g.computePreorderRelation(preordering1)))
##    preordering2 = bg2.computeRankingPreordering()
##    preordering2 = bg1.ranking2Preorder(bg2.boostedKohlerRanking)
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


    

