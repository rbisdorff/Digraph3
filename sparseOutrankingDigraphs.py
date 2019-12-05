#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digraph3 collection of python3 modules for Algorithmic Decision Theory applications

Module for sparse pre-ranked outranking digraphs

Copyright (C) 2016-19  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from outrankingDigraphs import *
from sortingDigraphs import *
from time import time
from decimal import Decimal
from sparseOutrankingDigraphs import *

class SparseOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Abstract root class for linearly decomposed sparse digraphs.
    """
    def __repr__(self):
        """
        Default presentation method for pre-ranked sparse digraphs instances.
        """
        reprString = '*----- Object instance description ------*\n'
        reprString += 'Instance class    : %s\n' % self.__class__.__name__
        reprString += 'Instance name     : %s\n' % self.name
        reprString += '# Actions         : %d\n' % self.order
        reprString += '# Criteria        : %d\n' % self.dimension
        reprString += 'Sorting by        : %d-Tiling\n' % self.sortingParameters['limitingQuantiles']
        reprString += 'Ordering strategy : %s\n' % self.sortingParameters['strategy']
        reprString += 'Ranking rule      : %s\n' % self.componentRankingRule
        reprString += '# Components      : %d\n' % self.nbrComponents
        reprString += 'Minimal order     : %d\n' % self.minimalComponentSize
        reprString += 'Maximal order     : %d\n' % self.maximalComponentSize
        reprString += 'Average order     : %.1f\n' % (self.order/self.nbrComponents)
        reprString += 'fill rate         : %.3f%%\n' % (self.fillRate*100.0)
        reprString += '----  Constructor run times (in sec.) ----\n'
        try:
            reprString += '#Threads          : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            reprString += '#Threads          : %d\n' % self.nbrThreads
        reprString += 'Total time        : %.5f\n' % self.runTimes['totalTime']
        reprString += 'Data imput        : %.5f\n' % self.runTimes['dataInput']
        reprString += 'QuantilesSorting  : %.5f\n' % self.runTimes['sorting']
        reprString += 'Preordering       : %.5f\n' % self.runTimes['preordering']
        reprString += 'Decomposing       : %.5f\n' % self.runTimes['decomposing']
        try:
            reprString += 'Ordering          : %.5f\n' % self.runTimes['ordering']
        except:
            pass
        return reprString

    def relation(self,x,y,Debug=False):
        """
        Dynamic construction of the global outranking characteristic function *r(x S y)*.
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

    def computeDeterminateness(self):
        """
        Computes the Kendalll distance in % of self
        with the all median valued (indeterminate) digraph.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        actions = self.actions
        relation = self.relation
        order = self.order
        deter = Decimal('0.0')
        for x in actions:
            for y in actions:
                if x != y:
                    deter += abs(relation(x,y) - Med)
        deter = ( Decimal(str(deter)) / Decimal(str((order * (order-1)))) )
        return deter/(Decimal(str(Max-Med)))*Decimal('100')

    def computeOrderCorrelation(self, order, Debug=False):
        """
        Renders the ordinal correlation K of a sparse digraph instance
        when compared with a given linear order (from worst to best) of its actions

        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             Renders a dictionary with the key 'correlation' containing the actual bipolar correlation index and the key 'determination' containing the minimal determination level D of self and the other relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        .. warning::

             self must be a normalized outranking digraph instance !

        """

        selfMax = self.valuationdomain['max']
        if selfMax != Decimal('1'):
            print("Error: self's valuationdomain  must be normalized !")
            return
        n = len(order)
        corrSum = Decimal('0')
        determSum = Decimal('0')
        for i in range(n):
            x = order[i]
            for j in range(i+1,n):
                y = order[j]
                # x < y
                selfRelation = self.relation(x,y)
                otherRelation = -selfMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ
                # y > x
                selfRelation = self.relation(y,x)
                otherRelation = selfMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ

        if determSum > 0:
            correlation = corrSum / determSum
            n2 = (self.order*self.order) - self.order
            determination = determSum / Decimal(str(n2))
            determination /= selfMax

            return { 'correlation': correlation,\
                     'determination': determination }
        else:
            return { 'correlation': 0.0,\
                     'determination': 0.0 }

    def estimateRankingCorrelation(self,sampleSize=100,seed=1,Debug=False):
        import random
        random.seed(seed)
        actionKeys = [x for x in self.actions]
        sample = random.sample(actionKeys,sampleSize)
        if Debug:
            print(sample)
        preRankedSample = []
        for x in self.boostedRanking:
            if x in sample:
                preRankedSample.append(x)
        if Debug:
            print(preRankedSample)
        ptp = PartialPerformanceTableau(self,sample)
        from outrankingDigraphs import BipolarOutrankingDigraph
        pg = BipolarOutrankingDigraph(ptp,Normalized=True)
        corr = pg.computeRankingCorrelation(preRankedSample)
        return corr

    def sortingRelation(self,x,y,Debug=False):
        """
        Dynamic construction of the quantiles sorting characteristic function *r(x QS y)*.
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
            return Med
        elif self.components[cx]['rank'] > self.components[cy]['rank']:
            return Min
        else:
            return Max

    def showRelationMap(self,fromIndex=None,toIndex=None,symbols=None,actionsList=None):
        """
        Prints on the console, in text map format, the location of
        the diagonal outranking components of the sparse outranking digraph.

        By default, symbols = {'max':'┬','positive': '+', 'median': ' ',
                               'negative': '-', 'min': '┴'}

        Example::

            >>> from sparseOutrankingDigraphs import *
            >>> t = RandomCBPerformanceTableau(numberOfActions=50,seed=1)
            >>> bg = PreRankedOutrankingDigraph(t,quantiles=10,minimalComponentSize=5)
            >>> print(bg)
            *----- show short --------------*
            Instance name     : randomCBperftab_mp
            # Actions         : 50
            # Criteria        : 7
            Sorting by        : 10-Tiling
            Ordering strategy : average
            Ranking Rule      : Copeland
            # Components      : 7
            Minimal size      : 5
            Maximal size      : 13
            Median size       : 6
            fill rate         : 16.898%
            ----  Constructor run times (in sec.) ----
            Total time        : 0.08494
            QuantilesSorting  : 0.04339
            Preordering       : 0.00034
            Decomposing       : 0.03989
            Ordering          : 0.00024
            <class 'sparseOutrankingDigraphs.PreRankedOutrankingDigraph'> instance
            >>> bg.showRelationMap()
             ┬+++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴ ++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
             + ++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            --- -┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            -┴-+ ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴ ┬-+┬+┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴   +┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴+  +  ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴-+- ++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴  + ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴   -  ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴ +++-+++++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴+ +++++++++-+┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴+- +--+++++++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴--+ -++++++-+┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴++++ +-   ++ ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴--+-+ +++++++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴-+-++- ++++--┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴-++-++- + -+-┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴---- ++- + ++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴-+--++++- -++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴--- --+++ ++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴+-+-++-+-+ +┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴-+- -+++-++ ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  -  + + ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  -+ + ++┬++┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴++ +++++++++┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ -- -+-++  ┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴++++ ++++++-┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴----- ++-┬+┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  +++- -++-+┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴-----++ -++┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ +-+-+-+ -++┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴+   +++ ┬+┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴-- --+++  -┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴--┴+ -┴--+ ┬┬┬┬┬┬┬┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ +++++++┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴+ +++-+┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴--  +++┬┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴--    ++┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴+-+  +++┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ +- + --┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴---+++ +┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴- ┴-+++ ┬┬┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  ┬┬┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  ++ ┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ - -┬┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴ -+  ┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴  ┴  ┬
            ┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴
            Component ranking rule: Copeland
            >>>
        """
        if symbols == None:
            symbols = {'max':'┬','positive': '+', 'median': ' ',
                       'negative': '-', 'min': '┴'}
        relation = self.relation
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        if actionsList == None:
            ranking = self.boostedRanking
        else:
            ranking = actionsList
        if fromIndex == None:
            fromIndex = 0
        if toIndex == None:
            toIndex = len(ranking)
        for x in ranking[fromIndex:toIndex]:
            pictStr = ''
            for y in ranking[fromIndex:toIndex]:
                if relation(x,y) == Max:
                    pictStr += symbols['max']
                elif relation(x,y) == Min:
                    pictStr += symbols['min']
                elif relation(x,y) > Med:
                    pictStr += symbols['positive']
                elif relation(x,y) ==Med:
                    pictStr += symbols['median']
                elif relation(x,y) < Med:
                    pictStr += symbols['negative']
            print(pictStr)
        if actionsList == None:
            print('Component ranking rule: %s' % self.componentRankingRule)
        else:
            print('List of actions provided.')

    def showHTMLMarginalQuantileLimits(self):
        """
        shows the marginal quantiles limits.
        """
        for x in self.profiles:
            catKey = self.profiles[x]['category']
            self.profiles[x]['shortName']= '%.2f' % self.categories[catKey]['quantile']
        self.showHTMLPerformanceTableau(actionsSubset=self.profiles,
                                        title='Marginal performance quantiles')

    def showHTMLRelationMap(self,actionsSubset=None,\
                            Colored=True,\
                            tableTitle='Relation Map',\
                            relationName='r(x S y)',\
                            symbols=['+','&middot;','&nbsp;','&#150;','&#151;']
                            ):
        """
        Launches a browser window with the colored relation map of self.
        """
        import webbrowser
        fileName = '/tmp/relationMap.html'
        fo = open(fileName,'w')
        fo.write(self.htmlRelationMap(actionsSubset=None,
                                        Colored=Colored,
                                        tableTitle=tableTitle,
                                        symbols=symbols,
                                        ContentCentered=True,
                                        relationName=relationName))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)

    def showHTMLRelationTable(self):
        """
        Not yet availbale !
        """
        print('Method not yet implemented for This class of digraphs!')
        print('Try instead: self.showRelationTable()')

    def htmlRelationMap(self,actionsSubset=None,
                          tableTitle='Relation Map',
                          relationName='r(x R y)',
                          symbols=['+','&middot;','&nbsp;','-','_'],
                          Colored=True,
                          ContentCentered=True):
        """
        renders the relation map in actions X actions html table format.
        """
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        if actionsSubset == None:
            actionsList = self.boostedRanking
        else:
            actionsList = actionsSubset

        s  = '<!DOCTYPE html><html><head>\n'
        s += '<title>%s</title>\n' % 'Digraph3 relation map'
        s += '<style type="text/css">\n'
        if ContentCentered:
            s += 'td {text-align: center;}\n'
        s += 'td.na {color: rgb(192,192,192);}\n'
        s += '</style>\n'
        s += '</head>\n<body>\n'
        s += '<h1>%s</h1>' % tableTitle
        s += '<table border="0">\n'
        if Colored:
            s += '<tr bgcolor="#9acd32"><th>%s</th>\n' % relationName
        else:
            s += '<tr><th>%s</th>' % relationName

        for x in actionsList:
            if Colored:
                s += '<th bgcolor="#FFF79B">%s</th>\n' % (x)
            else:
                s += '<th>%s</th\n>' % (x)
        s += '</tr>\n'
        for x in actionsList:
            s += '<tr>'
            if Colored:
                s += '<th bgcolor="#FFF79B">%s</th>\n' % (x)
            else:
                s += '<th>%s</th>\n' % (x)
            for y in actionsList:
                if Colored:
                    if self.relation(x,y) == Max:
                        s += '<td bgcolor="#66ff66"><b>%s</b></td>\n' % symbols[0]
                    elif self.relation(x,y) > Med:
                        s += '<td bgcolor="#ddffdd">%s</td>' % symbols[1]
                    elif self.relation(x,y) == Min:
                        s += '<td bgcolor="#ff6666"><b>%s</b></td\n>' % symbols[4]
                    elif self.relation(x,y) < Med:
                        s += '<td bgcolor="#ffdddd">%s</td>\n' % symbols[3]
                    else:
                        s += '<td bgcolor="#ffffff">%s</td>\n' % symbols[2]
                else:
                    if self.relation(x,y) == Max:
                        s += '<td><b>%s</b></td>\n'  % symbols[0]
                    elif self.relation(x,y) > Med:
                        s += '<td>%s</td>\n' % symbols[1]
                    elif self.relation(x,y) == Min:
                        s += '<td><b>%s</b></td>\n' % symbols[4]
                    elif self.relation(x,y) < Med:
                        s += '<td>\n' % symbols[3]
                    else:
                        s += '<td>%s</td>\n' % symbols[2]
            s += '</tr>'
        s += '</table>\n'
        # legend
        s += '<span style="font-size: 100%">\n'
        s += '<table border="1">\n'
        s += '<tr><th align="left" colspan="5">Ranking rules:</th><td align="left" colspan="5">%s, %s quantile ordering</td></tr>\n'\
                                % (self.componentRankingRule,self.sortingParameters['strategy'])
        s += '<tr><th align="left" colspan="10"><i>Symbol legend</i></th></tr>\n'
        s += '<tr>'
        if Colored:
            s += '<td bgcolor="#66ff66" align="center">%s</td><td>certainly valid</td>\n' % symbols[0]
            s += '<td bgcolor="#ddffdd" align="center">%s</td><td>valid</td>\n' % symbols[1]
            s += '<td>%s</td><td>indeterminate</td>\n' % symbols[2]
            s += '<td bgcolor="#ffdddd" align="center">%s</td><td>invalid</td>\n' % symbols[3]
            s += '<td bgcolor="#ff6666" align="center">%s</td><td>certainly invalid</td>\n' % symbols[4]
        else:
            s += '<td align="center">%s</td><td>certainly valid</td>\n' % symbols[0]
            s += '<td align="center">%s</td><td>valid</td>\n' % symbols[1]
            s += '<td align="center">%s</td><td>indeterminate</td>\n' % symbols[2]
            s += '<td align="center">%s</td><td>invalid</td>\n' % symbols[3]
            s += '<td align="center">%s</td><td>certainly invalid</td>\n' % symbols[4]
        s += '</tr>'
        s += '</table>\n'
        s += '</span>\n'
        # html footer
        s += '</body>\n'
        s += '</html>\n'
        return s

    def computeOrdinalCorrelation(self, other, Debug=False):
        """
        Renders the ordinal correlation K of a SpareOutrakingDigraph instance
        when compared with a given compatible (same actions set) other Digraph instance.

        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             The global outranking relation of SparesOutrankingDigraph instances is contructed on the fly
             from the ordered dictionary of the components.

             Renders a dictionary with a 'correlation' key containing the actual bipolar correlation index K and a 'determination' key containing the minimal determination level D of self and the other relation, where

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             and where n is the number of actions considered.

             The correlation index K with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """

        if self.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the BigDigraph instance must be normalized !!')
                print(self.valuationdomain)
                return

        if issubclass(other.__class__,(Digraph)):
            # if Debug:
            #     print('other is a Digraph instance')
            if other.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the other digraph must be normalized !!')
                print(other.valuationdomain)
                return
        elif isinstance(other,(BigDigraph)):
            # if Debug:
            #     print('other is a BigDigraph instance')
            if other.valuationdomain['min'] != Decimal('-1.0'):
                print('Error: the other bigDigraph instance must be normalized !!')
                print(other.valuationdomain)
                return

        correlation = Decimal('0.0')
        determination = Decimal('0.0')

        for x in self.actions.keys():
            for y in self.actions.keys():
                if x != y:
                    selfRelation = self.relation(x,y)
                    try:
                        otherRelation = other.relation(x,y)
                    except:
                        otherRelation = other.relation[x][y]
                        #if Debug:
                        #    print(x,y,'self', selfRelation)
                        #    print(x,y,'other', otherRelation)
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
        """
        Prints on the console the decomposition structure of the sparse outranking digraph instance
        in *decreasing* (default) or *increasing* preference direction.
        """

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


    def computeDecompositionSummaryStatistics(self):
        """
        Returns the summary of the distribution of the length of
        the components as follows::

            summary = {'max': maxLength,
                       'median':medianLength,
                       'mean':meanLength,
                       'stdev': stdLength,
                       'fillrate': fillrate,
                                  (see computeFillRate()}
        """
        try:
            import statistics
        except:
            print('Error importing the statistics module.')
            print('You need to upgrade your Python to version 3.4+ !')
            return
        nc = self.nbrComponents
        compLengths = [comp['subGraph'].order\
                       for comp in self.components.values()]
        medianLength = statistics.median(compLengths)
        stdLength = statistics.pstdev(compLengths)
        summary = {
                   'min': self.minimalComponentSize,
                   'max': self.maximalComponentSize,
                   'median':medianLength,
                   'mean':self.order/nc,
                   'stdev': stdLength,
                   'fillrate': self.fillRate}
        return summary

    def recodeValuation(self,newMin=-1,newMax=1,Debug=False):
        """
        Specialization for recoding the valuation of all the partial digraphs and the component relation.
        By default the valuation domain is normalized to [-1;1]
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
        Renders a preordering (a list of list) of a ranking (best to worst) of decision actions in increasing preference direction.
        """
        #ordering = list(ranking)
        #ordering.reverse()
        preordering = [[x] for x in reversed(ranking)]
        return preordering

    def ordering2Preorder(self,ordering):
        """
        Renders a preordering (a list of list) of a linar order (worst to best) of decision actions in increasing preference direction.
        """
        preordering = [[x] for x in ordering]
        return preordering

    def computeFillRate(self):
        """
        Renders the sum of the squares (without diagonal) of the orders of the component's subgraphs
        over the square (without diagonal) of the big digraph order.
        """
        fillRate = sum((comp['subGraph'].order*(comp['subGraph'].order-1))\
                        for comp in self.components.values())
        return fillRate/( self.order*(self.order-1) )

    def exportGraphViz(self,fileName=None,actionsSubset=None,\
                       bestChoice=set(),worstChoice=set(),\
                       Comments=True,graphType='png',graphSize='7,7',
                       relation=None):
        """
        export GraphViz dot file  for graph drawing filtering.
        """
        import os
        
        if Comments:
            print('*---- exporting a dot file dor GraphViz tools ---------*')
        if actionsSubset == None:
            actionkeys = [x for x in self.actions]
        else:
            actionkeys = [x for x in actionsSubset]
        n = len(actionkeys)
        if relation == None:
            relation = self.relation
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        if bestChoice != set():
            rankBestString = '{rank=max; '
        if worstChoice != set():
            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nRubis Python Server (graphviz), R. Bisdorff, 2008", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = self.actions[actionkeys[i]]['shortName']
            except:
                try:
                    nodeName = self.actions[actionskeys[i]]['name']
                except:
                    nodeName = str(actionkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            if actionkeys[i] in bestChoice:
                node += ', style = "filled", color = gold];\n'
                rankBestString += 'n'+str(i+1)+' '
            elif actionkeys[i] in worstChoice:
                node += ', style = "filled", color = lightblue];\n'
                rankWorstString += 'n'+str(i+1)+' '
            else:
                node += '];\n'
            fo.write(node)
        if bestChoice != set():
            rankBestString += '}\n'
        if worstChoice != set():
            rankWorstString += '}\n'
##         for i in range(n):
##             edge = 'n'+str(i+1)
##             for j in range(n):
##                 if i != j and relation[actions[i]][actions[j]] > Med:
##                     edge0 = edge+'-> n'+str(j+1)+';\n'
##                     fo.write(edge0)
##                     j += 1
##             i += 1
        for i in range(n):
            for j in range(i+1, n):
                edge = 'n'+str(i+1)
                if relation(actionkeys[i],actionkeys[j]) > Med and relation(actionkeys[j],actionkeys[i])> Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both,style="setlinewidth(2)",color=black, arrowhead=normal, arrowtail=normal] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) > Med and relation(actionkeys[j],actionkeys[i])== Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowhead=normal, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) == Med and relation(actionkeys[j],actionkeys[i]) > Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowtail=normal, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) == Med and relation(actionkeys[j],actionkeys[i]) == Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=grey, arrowhead=empty, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) > Med and relation(actionkeys[j],actionkeys[i]) <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=black] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) == Med and relation(actionkeys[j],actionkeys[i]) <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=grey, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) < Med and relation(actionkeys[j],actionkeys[i]) >  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=back, color=black] ;\n'
                    fo.write(edge0)
                elif relation(actionkeys[i],actionkeys[j]) < Med and relation(actionkeys[j],actionkeys[i]) ==  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=back, color=grey, arrowtail=empty] ;\n'
                    fo.write(edge0)

        if bestChoice != set():
            fo.write(rankBestString)
        if worstChoice != set():
            fo.write(rankWorstString)
        fo.write('}\n')
        fo.close()
        if type(self) == CirculantDigraph:
            commandString = 'circo -T'+graphType+' '+dotName+' -o '+name+'.' + graphType
        # elif type(self) == RandomTree:
        #     commandString = 'neato -T'+graphType+' '+dotName+' -o '+name+'.' + graphType
        else:
            commandString = 'dot -Grankdir=BT -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType

        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

    def exportSortingGraphViz(self,fileName=None,\
                              actionsSubset=None,\
                              direction='decreasing',\
                       Comments=True,graphType='pdf',\
                       graphSize='7,7',\
                       fontSize=10,
                       relation=None,
                       Debug=False):
        """
        export GraphViz dot file for weak order (Hasse diagram) drawing
        filtering from SortingDigraph instances.

        Example::

            >>> print('==>> Testing graph viz export of sorting Hasse diagram')
            >>> MP  = True
            >>> nbrActions=100
            >>> tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,
            ...                         Threading=MP,
            ...                         seed=100)
            >>> bg = PreRankedOutrankingDigraph(tp,CopyPerfTab=True,quantiles=20,
            ...                             quantilesOrderingStrategy='average',
            ...                             componentRankingRule='Copeland',
            ...                             LowerClosed=False,
            ...                             minimalComponentSize=1,
            ...                            Threading=MP,nbrOfCPUs=8,
            ...                            #tempDir='.',
            ...                             nbrOfThreads=8,
            ...                             Comments=False,Debug=False)
            >>> print(bg)
            *----- show short --------------*
            Instance name     : randomCBperftab_mp
            # Actions         : 100
            # Criteria        : 7
            Sorting by        : 20-Tiling
            Ordering strategy : average
            Ranking rule      : Copeland
            # Components      : 36
            Minimal order     : 1
            Maximal order     : 11
            Average order     : 2.8
            fill rate         : 4.121%
            ----  Constructor run times (in sec.) ----
            Total time        : 0.15991
            QuantilesSorting  : 0.11717
            Preordering       : 0.00066
            Decomposing       : 0.04009
            Ordering          : 0.00000
            <class 'sparseOutrankingDigraphs.PreRankedOutrankingDigraph'> instance
            >>> bg.showComponents()
            *--- Relation decomposition in increasing order---*
            35: ['a010']
            34: ['a024', 'a060']
            33: ['a012']
            32: ['a018']
            31: ['a004', 'a054', 'a075', 'a082']
            30: ['a099']
            29: ['a065']
            28: ['a025', 'a027', 'a029', 'a041', 'a059']
            27: ['a063']
            26: ['a047', 'a066']
            25: ['a021']
            24: ['a007']
            23: ['a044']
            22: ['a037', 'a062', 'a090', 'a094', 'a098', 'a100']
            21: ['a005', 'a040', 'a051', 'a093']
            20: ['a015', 'a030', 'a052', 'a055', 'a064', 'a077']
            19: ['a006', 'a061']
            18: ['a049']
            17: ['a001', 'a033']
            16: ['a016', 'a028', 'a032', 'a035', 'a057', 'a079', 'a084', 'a095']
            15: ['a043']
            14: ['a002', 'a017', 'a023', 'a034', 'a067', 'a072', 'a073', 'a074', 'a088', 'a089', 'a097']
            13: ['a048']
            12: ['a078', 'a092']
            11: ['a070']
            10: ['a014', 'a026', 'a039', 'a058', 'a068', 'a083', 'a086']
            9: ['a008', 'a022', 'a038', 'a081', 'a091', 'a096']
            8: ['a020']
            7: ['a069']
            6: ['a045']
            5: ['a003', 'a009', 'a013', 'a031', 'a036', 'a056', 'a076']
            4: ['a042', 'a071']
            3: ['a085']
            2: ['a019', 'a080', 'a087']
            1: ['a046']
            0: ['a011', 'a050', 'a053']
            >>> bg.exportSortingGraphViz(actionsSubset=bg.boostedRanking[:100])

        .. image:: preRankedDigraph.png
           :alt: pre-ranked digraph
           :width: 400 px
           :align: center
        """
        import os
        from copy import copy, deepcopy

        def _safeName(t0):
            try:
                t = t0.split(sep="-")
                t1 = t[0]
                n = len(t)
                if n > 1:
                    for i in range(1,n):
                        t1 += '%s%s' % ('_',t[i])
                return t1
            except:
                print('Error in nodeName: %s !!' % t0, type(t0))
                return t0

        compKeys = list(self.components.keys())
        if direction != 'decreasing':
            compKeys.reverse()
        if Debug:
            print(compKeys)

        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        if actionsSubset == None:
            actionsKeys = [x for x in self.actions]
        else:
            actionsKeys = actionsSubset
        n = len(actionsKeys)
        if relation == None:
            relation = self.sortingRelation
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
##        if bestChoice != set():
##            rankBestString = '{rank=max; '
##        if worstChoice != set():
##            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\ntransitiveDigraphs module (graphviz)\\n R. Bisdorff, 2014", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionsKeys:
            try:
                nodeName = self.actions[x]['shortName']
            except:
                nodeName = str(x)
            node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                   % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        # same ranks for Hasses equivalence classes
        prtComp = []
        k = len(compKeys)
        for i in range(k):
            ich = [ x for x in self.components[compKeys[i]]['subGraph'].actions.keys() if x in actionsKeys]
            if ich != []:
                prtComp.append(ich)
                sameRank = '{ rank = same; '
                for x in ich:
                    sameRank += str(_safeName(x))+'; '
                sameRank += '}\n'
                print(i,sameRank)
                fo.write(sameRank)
        k = len(prtComp)
        print(prtComp)
        for i in range(1,k):
            for x in prtComp[i-1]:
                for y in prtComp[i]:
                    #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                    if self.sortingRelation(x,y) > self.valuationdomain['med']:
                        arcColor = 'black'
                        edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(x),_safeName(y),1,arcColor)
                        fo.write(edge)
                    elif self.sortingRelation(y,x) > self.valuationdomain['med']:
                        arcColor = 'black'
                        edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(y),_safeName(x),1,arcColor)
                        fo.write(edge)

        fo.write('}\n \n')
        fo.close()
        # restore original relation
        #self.relation = copy(originalRelation)

        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

########################
# multiprocessing workers
def _worker(input):
    for Comments,args in iter(input.get, 'STOP'):
        result = _decompose(*args)
        if Comments:
            print(result)

def _decompose(i, nc,tempDirName,componentRankingRule):
    global perfTab
    global decomposition
    from pickle import dumps
    from outrankingDigraphs import BipolarOutrankingDigraph
    from linearOrders import CopelandOrder,NetFlowsOrder

    comp = decomposition[i]
    nd = len(str(nc))
    compKey = ('c%%0%dd' % (nd)) % (i+1)
    compDict = {'rank':i}
    compDict['lowQtileLimit'] = comp[0][0]
    compDict['highQtileLimit'] = comp[0][1]
    compDict['score'] = (comp[2],comp[3],comp[4])
    pg = BipolarOutrankingDigraph(perfTab,
                    actionsSubset=comp[1],
                    WithConcordanceRelation=False,
                    WithVetoCounts=False,
                    CopyPerfTab=False,
                    Threading=False)
    if componentRankingRule == 'NetFlows':
        nf = NetFlowsOrder(pg)
        pg.ranking = nf.netFlowsRanking
    else:
        cop = CopelandOrder(pg)
        pg.ranking = cop.copelandRanking
    pg.__dict__.pop('criteria')
    pg.__dict__.pop('evaluation')
    pg.__class__ = Digraph
    compDict['subGraph'] = pg
    splitComponent = {'compKey':i,'compDict':compDict}
    foName = tempDirName+'/splitComponent-'+str(i)+'.py'
    fo = open(foName,'wb')
    fo.write(dumps(splitComponent,-1))
    fo.close()
    return '%d/%d (%d)' % (i,nc,pg.order)



class PreRankedOutrankingDigraph(SparseOutrankingDigraph,PerformanceTableau):
    """
    Main class for the multiprocessing implementation of pre-ranked sparse outranking digraphs.

    The sparse outranking digraph instance is decomposed with a q-tiling sort into a partition
    of quantile equivalence classes which are linearly ordered by average quantile limits (default).

    With each quantile equivalence class is associated a BipolarOutrankingDigraph object
    which is restricted to the decision actions gathered in this quantile equivalence class.

    See http://leopold-loewenheim.uni.lu/bisdorff/documents/DA2PL-RB-2016.pdf

    By default, the number of quantiles is set to a tenth of the number of decision actions,
    i.e. quantiles = order//10. The effective number of quantiles can be much lower for large orders;
    for instance quantiles = 250 gives good results for a digraph of order 25000.

    For other parameters settings, see the corresponding :py:class:`sortingDigraphs.QuantilesSortingDigraph` class.

    """
    def __init__(self,argPerfTab,\
                 quantiles=None,\
                 quantilesOrderingStrategy='average',\
                 LowerClosed=False,\
                 componentRankingRule='Copeland',\
                 minimalComponentSize=1,\
                 Threading=False,\
                 tempDir=None,\
                 #componentThreadingThreshold=50,\
                 nbrOfCPUs=1,\
                 nbrOfThreads=1,\
                 save2File=None,\
                 CopyPerfTab=True,\
                 Comments=False,\
                 Debug=False):
        """
        Constructor
        """
        global perfTab
        global decomposition

        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from multiprocessing import Pool
        from copy import copy, deepcopy

        ttot = time()

        # data input
        if Comments:
            print('Data input')
        
        t0 = time()
        perfTab = argPerfTab
        # setting quantiles sorting parameters
        if CopyPerfTab:
##            self.__dict__ = deepcopy(perfTab.__dict__)
            self.actions = deepcopy(perfTab.actions)
            self.criteria = deepcopy(perfTab.criteria)
            self.evaluation = deepcopy(perfTab.evaluation)
        else:
            self.__dict__.update(perfTab.__dict__)
##            self.actions = perfTab.actions
##            self.criteria = perfTab.criteria
##            self.evaluation = perfTab.evaluation
        self.name = perfTab.name + '_pr'
        na = len(self.actions)
        self.order = na
        self.runTimes = {}
        self.dimension = len(perfTab.criteria)
        self.runTimes = {'dataInput': (time() - t0) }
        if Comments:
            #print(self.runTimes)
            print('data input time: %.4f' % (self.runTimes['dataInput']))

        #######
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
            print('Computing the %d-quantiles sorting digraph of order %d ...' % (quantiles,na))
        qs = QuantilesSortingDigraph(argPerfTab=perfTab,\
                                     limitingQuantiles=quantiles,\
                                     LowerClosed=LowerClosed,\
                                     CompleteOutranking=False,\
                                     StoreSorting=True,\
                                     WithSortingRelation=False,\
                                     CopyPerfTab=CopyPerfTab,\
                                     Threading=Threading,\
                                     tempDir=tempDir,\
                                     nbrCores=nbrOfCPUs,\
                                     nbrOfProcesses=nbrOfThreads,\
                                     Comments=Comments,\
                                     Debug=Debug)
        self.valuationdomain = qs.valuationdomain
        self.profiles = qs.profiles
        self.categories = qs.categories
        self.sorting = qs.sorting
        self.evaluation = qs.evaluation
        self.runTimes['sorting'] =  time() - t0
        if Comments:
            print('sorting time: %.4f' % (self.runTimes['sorting']))
        
        # preordering
        if minimalComponentSize == None:
            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        self.componentRankingRule = componentRankingRule
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][0],item[0][1]),item[1],item[2],item[3],item[4]]\
                for item in self._computeQuantileOrdering(\
                    strategy=quantilesOrderingStrategy,\
                    Descending=True,Threading=Threading,nbrOfCPUs=nbrOfCPUs)]
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
        self.nd = len(str(nc))
        if not self.sortingParameters['Threading']:
            self.nbrThreads = 1
            components = OrderedDict()
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                #print('==>>',comp)
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = BipolarOutrankingDigraph(pt,
                                          WithConcordanceRelation=False,
                                          WithVetoCounts=False,
                                          Normalized=True,
                                          CopyPerfTab=False)
                pg.__dict__.pop('criteria')
                pg.__dict__.pop('evaluation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
                components[compKey]['score']=(comp[2],comp[3],comp[4])
        else:   # if self.sortingParameters['Threading'] == True:
            from copy import copy, deepcopy
            from pickle import dumps, loads, load, dump
            from multiprocessing import Process, Queue,active_children, cpu_count
            self.nbrThreads = nbrOfCPUs
            if Comments:
                print('Processing the %d components' % nc )
                print('with %d cores' % self.nbrThreads)
            #tdump = time()
            from tempfile import TemporaryDirectory,mkdtemp
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                ## tasks queue and workers launching
                NUMBER_OF_WORKERS = nbrOfCPUs
                tasksIndex = [(i,len(decomposition[i][1])) for i in range(nc)]
                tasksIndex.sort(key=lambda pos: pos[1],reverse=True)
                TASKS = [(Comments,(pos[0],nc,tempDirName,componentRankingRule)) for pos in tasksIndex]
                task_queue = Queue()
                for task in TASKS:
                    task_queue.put(task)
                for i in range(NUMBER_OF_WORKERS):
                    Process(target=_worker,args=(task_queue,)).start()
                #print('started')
                for i in range(NUMBER_OF_WORKERS):
                    task_queue.put('STOP')

                while active_children() != []:
                    pass
                if Comments:
                    print('Exit %d threads' % NUMBER_OF_WORKERS)

                components = OrderedDict()
                #componentsList = []
                boostedRanking = []
                for j in range(nc):
                    if Debug:
                        print('job',j)
                    fiName = tempDirName+'/splitComponent-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitComponent = loads(fi.read())
                    if Debug:
                        print('splitComponent',splitComponent)
                    components[splitComponent['compKey']] = splitComponent['compDict']
                    boostedRanking += splitComponent['compDict']['subGraph'].ranking
                self.boostedRanking = boostedRanking
                self.boostedOrder = list(reversed(self.boostedRanking))

        # storing components, fillRate and maximalComponentSize

        self.components = components
        fillRate = 0
        maximalComponentSize = 0
        for compKey,comp in components.items():
            pg = comp['subGraph']
            npg = pg.order
            if npg > maximalComponentSize:
                maximalComponentSize = npg
            fillRate += npg*(npg-1)
            for x in pg.actions.keys():
                self.actions[x]['component'] = compKey
        self.fillRate = fillRate/(self.order * (self.order-1))
        self.maximalComponentSize = maximalComponentSize




        # setting the component relation
        self.valuationdomain = {'min':Decimal('-1'),
                                'med':Decimal('0'),
                                'max':Decimal('1')}

        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )

        #  compute boosted ranking in not threaded exceution
        if not self.sortingParameters['Threading']:
            self.componentRankingRule = componentRankingRule
            t0 = time()
            self.boostedRanking = self.computeBoostedRanking(rankingRule=componentRankingRule)
            self.boostedOrder = list(reversed(self.boostedRanking))
            self.runTimes['ordering'] = time() - t0
        else:
            self.runTimes['ordering'] = 0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        ########
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)


    # ----- PreRankedOutrankingDigraph class methods ------------

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
        from operator import itemgetter
        if strategy == None:
            strategy = self.sortingParameters['strategy']
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility,lowLimit,notHighLimit =\
                     self.computeActionCategories(x,Comments=Comments,Debug=Debug,\
                                               Threading=Threading,\
                                               nbrOfCPUs = nbrOfCPUs)
            lowQtileLimit = self.categories[lowCateg]['lowLimit']
            highQtileLimit = self.categories[highCateg]['highLimit']
            lowQtileValue = self.categories[lowCateg]['quantile']
            highQtileValue = self.categories[highCateg]['quantile']
            if strategy == "average":
                lc = int(lowCateg)
                hc = int(highCateg)
                score1 = (lc + hc)
                score2 = hc
                score3 = (lc + hc)
                score4 = hc
            elif strategy == "optimistic":
                score1 = int(highCateg)
                score2 = int(lowCateg)
                score3 = int(highCateg)
                score4 = int(lowCateg)
            elif strategy == "pessimistic":
                score1 = int(lowCateg)
                score2 = int(highCateg)
                score3 = int(lowCateg)
                score4 = int(highCateg)
            else:  #strategy == "optimal":
                lc = float(lowCateg)
                hc = float(highCateg)
                score1 = (lc+hc)/2.0
                score2 = hc
                score3 = float(lowLimit) - float(notHighLimit)
                score4 = -float(notHighLimit)
            #print(score1,highQtileLimit,lowQtileLimit,lowCateg,highCateg,score2,score3,score4)
            #if Optimal:
            try:
                actionsCategories[(score1,score2,score3,score4,highQtileValue,\
                                   lowQtileValue,lowCateg,highCateg,highQtileLimit,lowQtileLimit)].append(a)
            except:
                actionsCategories[(score1,score2,score3,score4,highQtileValue,\
                                   lowQtileValue,lowCateg,highCateg,highQtileLimit,lowQtileLimit)] = [a]
##            else:
##                try:
##                    actionsCategories[(score1,highQtileValue,\
##                                       lowQtileValue,lowCateg,highCateg,highQtileLimit,lowQtileLimit)].append(a)
##                except:
##                    actionsCategories[(score1,highQtileValue,\
##                                       lowQtileValue,lowCateg,highCateg,highQtileLimit,lowQtileLimit)] = [a]
               

        #if Optimal:
        actionsCategIntervals = sorted(actionsCategories,key=itemgetter(0,1,2,3), reverse=True)
##        else:
##            actionsCategIntervals = sorted(actionsCategories,key=itemgetter(0), reverse=True)
      
        if Debug:
            print(actionsCategIntervals)
        compSize = self.minimalComponentSize

        if compSize <= 1:
            #if Optimal:
            if Descending:
                componentsIntervals = [[(item[8],item[9]),actionsCategories[item],item[0],item[6],item[7]]\
                                   for item in actionsCategIntervals]
            else:
                componentsIntervals = [[(item[9],item[8]),actionsCategories[item],item[0],item[6],item[7]]\
                                   for item in actionsCategIntervals]
##            else:
##                if Descending:
##                    componentsIntervals = [[(item[5],item[6]),actionsCategories[item],item[0],item[3],item[4]]\
##                                       for item in actionsCategIntervals]
##                else:
##                    componentsIntervals = [[(item[6],item[5]),actionsCategories[item],item[0],item[3],item[4]]\
##                                       for item in actionsCategIntervals]
                

        else:
            componentsIntervals = []
            nc = len(actionsCategIntervals)
            compContent = []
            for i in range(nc):
                currContLength = len(compContent)
                comp = actionsCategIntervals[i]
                #print(comp)
                #if Optimal:
                if currContLength == 0:
                    lowQtileLimit = comp[9]
                highQtileLimit = comp[8]
##                else:
##                    if currContLength == 0:
##                        lowQtileLimit = comp[6]
##                    highQtileLimit = comp[5]
                    
                compContent += actionsCategories[comp]
                if len(compContent) >= compSize or i == nc-1:
                    score = comp[0]
                    lowCateg = comp[6]
                    highCateg = comp[7]
                    if Descending:
                        highQtileLimit = comp[8]
                        lowQtileLimit = comp[9]
                        componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent,\
                                                    score,lowCateg,highCateg])
                    else:
                        highQtileLimit = comp[8]
                        lowQtileLimit = comp[9]
                        componentsIntervals.append([(lowQtileLimit,highQtileLimit),compContent,\
                                                    score,lowCateg,highCateg])
                    compContent = []
        if Debug:
            print(componentsIntervals)
        return componentsIntervals

    def computeActionCategories(self,action,Show=False,Debug=False,Comments=False,\
                             Threading=False,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        #qs = self.qs
        #qs = self
        Med = self.valuationdomain['med']
        categories = self.categories

        try:
            sortinga = self.sorting[action]
        except:
            sorting = self.computeSortingCharacteristics(action=action,Comments=Comments,\
                                                   Threading=Threading,\
                                                   nbrOfCPUs=nbrOfCPUs)
            sortinga = sorting[action]

        keys = []
        for c in categories.keys():
        #for c in self.orderedCategoryKeys():
            if Debug:
                print(action, c,sortinga[c])
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
        try:
            credibility = min(lowLimit,notHighLimit)
        except:
            credibility = Med
            notHighLimit = Med
        n = len(keys)
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



    def computeCriterion2RankingCorrelation(self,criterion,Threading=False,\
                                    nbrOfCPUs=None,Debug=False,
                                    Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the global linar ranking and the marginal criterion relation.

        """
        #print(criterion)
        gc = BipolarOutrankingDigraph(self,coalition=[criterion],
                                      Normalized=True,CopyPerfTab=False,
                                      Threading=Threading,nbrCores=nbrOfCPUs,
                                      Comments=Comments)
        globalOrdering = self.ranking2Preorder(self.boostedRanking)
        globalRelation = gc.computePreorderRelation(globalOrdering)
        corr = gc.computeOrdinalCorrelation(globalRelation)
        if Debug:
            print(corr)
        return corr

    def computeMarginalVersusGlobalRankingCorrelations(self,Sorted=True,ValuedCorrelation=False,
                                                          Threading=False,nbrCores=None,\
                                                          Comments=False):
        """
        Method for computing correlations between each individual criterion relation with the corresponding global ranking relation.

        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of available cores.
        """
        if Threading:
            from multiprocessing import Pool
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

    def showMarginalVersusGlobalRankingCorrelation(self,Sorted=True,\
                                                      Threading=False,\
                                                      nbrOfCPUs=None,Comments=True):
        """
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
            print('Marginal versus global linear ranking correlation')
            print('criterion | weight\t corr\t deter\t corr*deter')
            print('----------|------------------------------------------')
            for x in criteriaCorrelation:
                c = x[2]
                print('%9s |  %.2f \t %.3f \t %.3f \t %.3f' % (c,criteria[c]['weight'],x[0],x[1],x[0]*x[1]))

    def showActionSortingResult(self,action):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        Med = self.valuationdomain['med']
        print('Quantiles sorting result per decision action')
        res = self.sorting[action]
        for categ in self.categories.keys():
            if res[categ]['categoryMembership'] >= Med:
                print('%s: %.2f (%.2f,%.2f)' % (self.categories[categ]['name'],
                                                res[categ]['categoryMembership'],
                                                res[categ]['lowLimit'],
                                                res[categ]['notHighLimit'] ) )

##    def showActionsSortingResult(self,actionsSubset=None):
##        """
##        shows the quantiles sorting result all (default) of a subset of the decision actions.
##        """
##        print('Quantiles sorting result per decision action')
##        if actionsSubset==None:
##            for x in self.actions.keys():
##                self.computeActionCategories(x,Show=True)
##        else:
##            for x in actionsSubset:
##                self.computeActionCategories(x,Show=True)

    def showShort(self,fileName=None,WithFileSize=True):
        """
        Default (__repr__) presentation method for big outranking digraphs instances:

        >>> from sparseOutrankingDigraphs import *
        >>> t = RandomCBPerformanceTableau(numberOfActions=100,seed=1)
        >>> g = PreRankedOutrankingDigraph(t,quantiles=10)
        >>> print(g)
        *----- show short --------------*
        Instance name     : randomCBperftab_mp
        # Actions         : 100
        # Criteria        : 7
        Sorting by        : 10-Tiling
        Ordering strategy : average
        Ranking rule      : Copeland
        # Components      : 19
        Minimal size      : 1
        Maximal size      : 22
        Median size       : 2
        fill rate         : 0.116
        ----  Constructor run times (in sec.) ----
        Total time        : 0.14958
        QuantilesSorting  : 0.06847
        Preordering       : 0.00071
        Decomposing       : 0.07366
        Ordering          : 0.00130
        <class 'sparseOutrankingDigraphs.PreRankedOutrankingDigraph'> instance
        """
        #summaryStats = self.computeDecompositionSummaryStatistics()
        if fileName == None:
            print('*----- show short --------------*')
            print('Instance name     : %s' % self.name)
            print('# Actions         : %d' % self.order)
            print('# Criteria        : %d' % self.dimension)
            print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'])
            print('Ordering strategy : %s' % self.sortingParameters['strategy'])
            print('Ranking rule      : %s' % self.componentRankingRule)
            print('# Components      : %d' % self.nbrComponents)
            print('Minimal order     : %d' % self.minimalComponentSize)
            print('Maximal order     : %d' % self.maximalComponentSize)
            print('Average order     : %.1f' % (self.order/self.nbrComponents))
            print('Fill rate         : %.3f%%' % (self.fillRate*100.0))
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
            fo.write('Local ranking rule : %s\n' % self.componentRankingRule)
            fo.write('# Components       : %d\n' % self.nbrComponents)
            fo.write('Minimal size       : %d\n' % self.minimalComponentSize)
            fo.write('Maximal order      : %d\n' % self.maximalComponentSize)
            fo.write('Average order      : %.1f\n' % (self.order/self.nbrComponents))
            fo.write('Fill rate          : %.3f%%\n' % (self.fillRate*100.0))
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
        for comp in self.components.values():
            #comp = self.components[ck]
            try:
                actionsList += [(x,comp['subGraph'].actions[x]['name'],comp['subGraph'].actions[x]['comment'],) for x in comp['subGraph'].actions]
            except:
                actionsList += [(x,comp['subGraph'].actions[x]['name']) for x in comp['subGraph'].actions]
        actionsList.sort()
        print('List of decision actions')
        for ax in actionsList:
            try:
                print('%s: %s (%s)' % ax)
            except:
                print('%s: %s' % ax)

    def showCriteria(self,IntegerWeights=False,Debug=False):
        """
        print Criteria with thresholds and weights.
        """
        print('*----  criteria -----*')
        sumWeights = Decimal('0.0')
        for g in self.criteria:
            sumWeights += abs(self.criteria[g]['weight'])
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

    def showCriteriaQuantiles(self):
        self.showPerformanceTableau(actionsSubset=self.profiles)

    def showComponents(self,direction='increasing'):
        SparseOutrankingDigraph.showDecomposition(self,direction=direction)

    def showDecomposition(self,direction='decreasing'):

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
            sg = comp['subGraph']
            actions = [x for x in sg.actions]
            #if direction == 'decreasing':
            #print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],actions))
            #else:
            print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],actions))

    def computeCategoryContents(self,Reverse=False,Comments=False,StoreSorting=True,\
                                Threading=False,nbrOfCPUs=None):
        """
        Computes the sorting results per category.
        """
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(Comments=Comments,\
                                                     StoreSorting=StoreSorting,\
                                                     Threading=Threading,\
                                                     nbrOfCPUs=nbrOfCPUs)

        categoryContent = {}
        for c in self.categories:
            categoryContent[c] = []
            for x in self.actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)

        return categoryContent

    def showSorting(self,Descending=True,isReturningHTML=False,Debug=False):
        """
        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.

        """
        #from string import replace
        #from copy import copy, deepcopy

        try:
            categoryContent = self.categoryContent
        except:
            categoryContent = self.computeCategoryContents(StoreSorting=True)

        categoryKeys = list(self.categories.keys())
        if Descending:
            categoryKeys.reverse()
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = False

        if Descending:
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

##    def showHTMLRelationTable(self):
##        """
##        Not yet availbale !
##        """
##        print('Method not yet implemented for This class of digraphs!')
##        print('Try instead: self.showRelationTable()')

    def showRelationTable(self,compKeys=None):
        """
        Specialized for showing the quantiles decomposed relation table.
        Components are stored in an ordered dictionary.
        """
        components = self.components
        if compKeys == None:
            nc = self.nbrComponents
            print('%d quantiles decomposed relation table in decreasing order' % nc)
            for compKey,comp in components.items():
                #comp = components[compKey]
                pg = comp['subGraph']
                print('Component : %s' % compKey, end=' ')
                actions = [ x for x in pg.actions.keys()]
                print('%s' % actions)
                if pg.order > 1:
                    pg.showRelationTable()

        else:
            for compKey in compKeys:
                comp = components[compkey]
                pg = comp['subGraph']
                print('Relation table of component %s' % str(compKey))
                actions = [ x for x in pg.actions.keys()]
                print('%s' % actions)
                if pg.order > 1:
                    pg.showRelationTable()


    def computeBoostedRanking(self,rankingRule='Copeland'):
        """
        Renders an ordred list of decision actions ranked in
        decreasing preference direction following the rankingRule
        on each component.
        """
        from linearOrders import NetFlowsOrder,KohlerOrder,CopelandOrder
        ranking = []
        components = self.components
        # self.components is an ordered dictionary in decreasing preference
        for comp in components.values():
            #comp = self.components[cki]
            pg = comp['subGraph']
            if rankingRule == 'Copeland':
                opg = CopelandOrder(pg)
                ranking += opg.copelandRanking
            elif rankingRule == 'NetFlows':
                opg = NetFlowsOrder(pg)
                ranking += opg.netFlowsRanking
            elif rankingRule == 'Kohler':
                opg = KohlerOrder(pg)
                ranking += opg.kohlerRanking
        return ranking

    def computeBoostedOrdering(self,orderingRule='Copeland'):
        """
        Renders an ordred list of decision actions ranked in
        increasing preference direction following the orderingRule
        on each component.
        """
        ranking = self.computeBoostedRanking(rankingRule=orderingRule)
        ranking.reverse()
        return ranking

    def actionRank(self,action,ranking=None):
        """
        Renders the rank of a decision action in a given ranking

        If ranking == None, the self.boostedRanking attribute is used.
        """
        if ranking == None:
            ranking = self.boostedRanking
        return ranking.index(action) +1

    def actionOrder(self,action,ordering=None):
        """
        Renders the order of a decision action in a given ordering

        If ordering == None, the self.boostedOrder attribute is used.
        """
        if ordering == None:
            ordering = self.boostedOrder
        return ordering.index(action) +1

##    def htmlPerformanceHeatmap(self,argCriteriaList=None,
##                               argActionsList=None,
##                               SparseModel=True,
##                               minimalComponentSize=1,
##                               rankingRule='Copeland',
##                               quantiles=None,
##                               strategy='average',
##                               ndigits=2,
##                               contentCentered=True,
##                               colorLevels=None,
##                               pageTitle='Performance Heatmap',
##                               Correlations=False,
##                               Threading=False,
##                               nbrOfCPUs=None,
##                               Debug=False):
##        """
##        Specialization of the generic perfTabs method for spare outranking digraphs.
##
##        Renders the Brewer RdYlGn 5,7, or 9 levels colored heatmap of the performance table
##        actions x criteria in html format.
##        """
##        from decimal import Decimal
##        from digraphs import flatten
##
##        brewerRdYlGn9Colors = [(Decimal('0.1111'),'"#D53E4F"'),
##                               (Decimal('0.2222'),'"#F46D43"'),
##                               (Decimal('0.3333'),'"#FDAE61"'),
##                               (Decimal('0.4444'),'"#FEE08B"'),
##                               (Decimal('0.5555'),'"#FFFFBF"'),
##                               (Decimal('0.6666'),'"#D9EF8B"'),
##                               (Decimal('0.7777'),'"#A6D96A"'),
##                               (Decimal('0.8888'),'"#65BD63"'),
##                               (Decimal('1.000'),'"#1A9850"')]
##        brewerRdYlGn7Colors = [
##                               (Decimal('0.1429'),'"#F46D43"'),
##                               (Decimal('0.2857'),'"#FDAE61"'),
##                               (Decimal('0.4286'),'"#FEE08B"'),
##                               (Decimal('0.5714'),'"#FFFFBF"'),
##                               (Decimal('0.7143'),'"#D9EF8B"'),
##                               (Decimal('0.8571'),'"#A6D96A"'),
##                               (Decimal('1.0000'),'"#65BD63"')
##                               ]
##        brewerRdYlGn5Colors = [
##                               (Decimal('0.2'),'"#FDAE61"'),
##                               (Decimal('0.4'),'"#FEE08B"'),
##                               (Decimal('0.6'),'"#FFFFBF"'),
##                               (Decimal('0.8'),'"#D9EF8B"'),
##                               (Decimal('1.0'),'"#A6D96A"')
##                               ]
##        if colorLevels == None:
##            colorLevels = 7
##        if colorLevels == 7:
##            colorPalette = brewerRdYlGn7Colors
##        elif colorLevels == 9:
##            colorPalette = brewerRdYlGn9Colors
##        elif colorLevels == 5:
##            colorPalette = brewerRdYlGn5Colors
##        else:
##            colorPalette = brewerRdYlGn7Colors
##        nc = len(colorPalette)
##        backGroundColor   = '"#FFFFFF"'
##        naColor           = '"#FFFFFF"'
##        columnHeaderColor = '"#CCFFFF"'
##        rowHeaderColor    = '"#FFFFFF"'
##
##        html = '<!DOCTYPE html><html><head>\n'
##        html += '<title>%s</title>\n' % pageTitle
##        html += '<style type="text/css">\n'
##        #html += 'table {border-collapse: collapse;}'
##        if contentCentered:
##            html += 'td {text-align: center;}\n'
##        html += 'td.na {color: rgb(192,192,192);}\n'
##        html += '</style>\n'
##        html += '</head>\n<body>\n'
##        html += '<h2>%s</h2>\n' % pageTitle
##        if argActionsList == None:
##            actionsList = self.boostedRanking
##        else:
##            actionsList = argActionsList
##        na = len(actionsList)
##
##        if Debug:
##            print('1',actionsList)
##
##        criteria = self.criteria
##        if argCriteriaList == None:
##            if Correlations:
##                criteriaCorrelation =\
##                        self.computeMarginalVersusGlobalRankingCorrelations(\
##                                actionsList,ValuedCorrelation=True,Threading=Threading)
##                criteriaList = [c[1] for c in criteriaCorrelation]
##            else:
##                criteriaList = list(criteria.keys())
##                criteriaList.sort()
##                criteriaWeightsList = [(-criteria[g]['weight'],g) for g in criteriaList]
##                criteriaWeightsList.sort(reverse=False)
##                criteriaList = [g[1] for g in criteriaWeightsList]
##                criteriaCorrelation = None
##        else:
##            criteria = argCriteriaList
##            criteriaCorrelation = None
##
##        quantileColor={}
##        for x in actionsList:
##            quantileColor[x] = {}
##            for g in criteriaList:
##                quantilexg = self.computeActionCriterionQuantile(x,g)
##                if Debug:
##                    print(x,g,quantilexg)
##                if quantilexg != 'NA':
##                    for i in range(nc):
##                        if Debug:
##                            print(i, colorPalette[i][0])
##
##                        if quantilexg <= colorPalette[i][0]:
##                            quantileColor[x][g] = colorPalette[i][1]
##                            break
##                else:
##                    quantileColor[x][g] = naColor
##                if Debug:
##                    print(x,g,quantileColor[x][g])
##        # legend
####        html += '<i>Color legend: </i>\n'
####        html += '<table style="background-color:%s; border-collapse: collapse;" border="1">\n' % (backGroundColor)
####        html += '<tr bgcolor=%s><th>quantile</th>' % (columnHeaderColor)
####        for col in range(nc):
####            html += '<td bgcolor=%s>%s</td>' % (colorPalette[col][1],str(colorPalette[col][0]))
####        html += '</tr>\n'
####        html += '</table>\n'
##        # heatmap
##        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor)
##        html += '<tr bgcolor=%s><th>criteria</th>' % (columnHeaderColor)
##        for g in criteriaList:
##            try:
##                gName = self.criteria[g]['shortName']
##            except:
##                gName = str(g)
##            html += '<th>%s</th>' % (gName)
##        html += '</tr>\n'
##        html += '<tr><th bgcolor=%s>weights</th>' % (columnHeaderColor)
##        for g in criteriaList:
##            html += '<td align="center">%s</td>' % (str(self.criteria[g]['weight']))
##        html += '</tr>\n'
##        if criteriaCorrelation != None:
##            html += '<tr><th bgcolor=%s>tau<sup>(*)</sup></th>' % (columnHeaderColor)
##            for cg in criteriaCorrelation:
##                html += '<td align="center">%.2f</td>' % (cg[0])
##            html += '</tr>\n'
##        if Debug:
##            print(html)
##        for x in actionsList:
##            try:
##                xName = self.actions[x]['shortName']
##            except:
##                xName = str(x)
##            html += '<tr><th bgcolor=%s>%s</th>' % (rowHeaderColor,xName)
##            for g in criteriaList:
##                if self.evaluation[g][x] != Decimal("-999"):
##                    formatString = '<td bgcolor=%s align="right">%% .%df</td>' % (quantileColor[x][g],ndigits)
##                    html += formatString % (self.evaluation[g][x])
##                else:
##                    html += '<td bgcolor=%s class="na">NA</td>' % naColor
##                if Debug:
##                    print(html)
##            html += '</tr>\n'
##        html += '</table>\n'
##        # legend
##        html += '<i>Color legend: </i>\n'
##        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor)
##        html += '<tr bgcolor=%s><th>quantile</th>' % (columnHeaderColor)
##        #html += '<td bgcolor=%s>&nbsp;[%.2f - %.2f[&nbsp;</td>' % (colorPalette[0][1],0.0,colorPalette[0][0])
##        for col in range(0,nc):
##            html += '<td bgcolor=%s>&nbsp;%.2f&#037;</td>' % (colorPalette[col][1],
##                                                                   #colorPalette[col-1][0],
##                                                                   colorPalette[col][0]*Decimal('100.0'))
##        html += '</tr>\n'
##        html += '</table>\n'
##        if criteriaCorrelation != None:
##            html += '<i>(*) tau: Ordinal (Kendall) correlation between marginal criterion and global ranking relation.</i>\n'
##        html += '<i>Ranking rule</i>: <b>%s</b><br/>\n' % rankingRule
##        html += '</body></html>'
##        return html

    def computeNewSortingCharacteristics(self, actions, relation, Comments=False):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "actions x in A belongs to category c in C",
        i.e. x outranks low category limit and does not outrank
        the high category limit (if LowerClosed).
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        categories = self.categories

        LowerClosed = self.sortingParameters['LowerClosed']

        if Comments:
            if LowerClosed:
                print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
            else:
                print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        sorting = {}
        nq = self.sortingParameters['limitingQuantiles']
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
                #if Comments:
                #    print('%s in %s: low = %.2f, high = %.2f' % \
                #          (x, c,lowLimit,notHighLimit), end=' ')
                if Comments:
                    print('%s in %s - %s\t' % (x, categories[c]['lowLimit'],categories[c]['highLimit'],), end=' ')
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][c]['lowLimit'] = lowLimit
                sorting[x][c]['notHighLimit'] = notHighLimit
                sorting[x][c]['categoryMembership'] = categoryMembership

                if Comments:
                    #print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
                    print('%.2f\t\t %.2f\t\t %.2f\n' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))

        return sorting

    def computeNewActionCategories(self,action,sorting,Debug=False,Comments=False):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        keys = []
        for c in self.categories:
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
                                     self.categories[keys[0]]['lowLimit'],\
                                     self.categories[keys[0]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[0],\
                    credibility
        else:
            if Comments:
                print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                     self.categories[keys[0]]['lowLimit'],\
                                     self.categories[keys[-1]]['highLimit'],\
                                     action,\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility

    def showNewActionCategories(self,action,sorting):
        """
        Prints the union of categories in which the given action is sorted positively or null into.
        """
        self.computeNewActionCategories(action,sorting,Comments=True)


    def showNewActionsSortingResult(self,actions,sorting,Debug=False):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showNewActionCategories(x,sorting,Debug=Debug)

##############
class PreRankedConfidentOutrankingDigraph(PreRankedOutrankingDigraph,PerformanceTableau):
    """
    Main class for the multiprocessing implementation of pre-ranked sparse confident outranking digraphs.

    The sparse outranking digraph instance is decomposed with a confident q-tiling sort into a partition
    of quantile equivalence classes which are linearly ordered by average quantile limits (default).

    With each quantile equivalence class is associated a ConfidentBipolarOutrankingDigraph object
    which is restricted to the decision actions gathered in this quantile equivalence class.

    By default, the number of quantiles is set to a tenth of the number of decision actions,
    i.e. quantiles = order//10. The effective number of quantiles can be much lower for large orders;
    for instance quantiles = 250 gives good results for a digraph of order 25000.

    For other parameters settings, see the corresponding classes:
    :py:class:`sortingDigraphs.QuantilesSortingDigraph` and :py:class:`outrankingDigraphs.ConfidentBipolarOutrankingDigraph` .

    """
    def __init__(self,argPerfTab,\
                 quantiles=None,\
                 quantilesOrderingStrategy='average',\
                 LowerClosed=False,\
                 componentRankingRule='Copeland',\
                 minimalComponentSize=1,\
                 distribution = 'triangular',
                 betaParameter = 2,
                 confidence = 90.0,
                 Threading=False,\
                 tempDir=None,\
                 #componentThreadingThreshold=50,\
                 nbrOfCPUs=1,\
                 nbrOfThreads=1,\
                 save2File=None,\
                 CopyPerfTab=True,\
                 Comments=False,\
                 Debug=False):

        global perfTab
        global decomposition

        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from multiprocessing import Pool
        from copy import copy, deepcopy

        ttot = time()

        # setting name
        t0 = time()
        perfTab = argPerfTab
        # setting quantiles sorting parameters
        if CopyPerfTab:
            self.__dict__ = deepcopy(perfTab.__dict__)
##            self.actions = deepcopy(perfTab.actions)
##            self.criteria = deepcopy(perfTab.criteria)
##            self.evaluation = deepcopy(perfTab.evaluation)
        else:
            self.__dict__.update(perfTab.__dict__)
##            self.actions = perfTab.actions
##            self.criteria = perfTab.criteria
##            self.evaluation = perfTab.evaluation
        self.name = perfTab.name + '_conf_pr'
        na = len(self.actions)
        self.order = na
        self.dimension = len(perfTab.criteria)
        self.componentRankingRule = componentRankingRule
        self.runTimes = {}
        self.runTimes['dataInput'] = time() - t0

        #######
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
            print('Computing the %d-quantiles sorting digraph of order %d ...' % (quantiles,na))
        qs = QuantilesSortingDigraph(argPerfTab=perfTab,\
                                     limitingQuantiles=quantiles,\
                                     LowerClosed=LowerClosed,\
                                     CompleteOutranking=False,\
                                     StoreSorting=False,\
                                     WithSortingRelation=True,\
                                     hasNoVeto=True,
                                     CopyPerfTab=CopyPerfTab,\
                                     Threading=Threading,\
                                     tempDir=tempDir,\
                                     nbrCores=nbrOfCPUs,\
                                     nbrOfProcesses=nbrOfThreads,\
                                     Comments=Comments,\
                                     Debug=Debug)
        self.runTimes['sorting'] = time() - t0
        self.valuationdomain = qs.valuationdomain
        self.profiles = qs.profiles
        self.categories = qs.categories
        # compute sorting likelyhoods
        self.bipolarConfidenceLevel = (confidence/100.0)*2.0 -1.0
        self.distribution = distribution
        self.betaParameter = betaParameter
        self.evaluation = qs.evaluation
        self.sortingRelation = qs.relation

        self.likelihoods = self.computeCLTLikelihoods(distribution=distribution,
                                                      betaParameter=betaParameter,
                                                      Debug=Debug)

        self.confidentRelation = self._computeConfidentRelation(qs.relation,Debug=Debug)

       # compute quantiles sorting result
        categories = self.categories.keys()
        actions = self.actions
        relation = self.confidentRelation
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        sorting = {}
        nq = quantiles-1
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

        self.sorting = sorting

        # compute category contents
        categoryContent = {}
        for c in self.categories:
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)
        self.categoryContent = categoryContent


        if CopyPerfTab:
            self.evaluation = deepcopy(perfTab.evaluation)
        else:
            self.evaluation = perfTab.evaluation

        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
        if minimalComponentSize == None:
            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        self.componentRankingRule = componentRankingRule
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][0],item[0][1]),item[1],item[2],item[3],item[4]]\
                for item in self._computeQuantileOrdering(\
                    strategy=quantilesOrderingStrategy,\
                    Descending=True,Threading=Threading,nbrOfCPUs=nbrOfCPUs)]
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
        self.nd = len(str(nc))
        if not self.sortingParameters['Threading']:
            components = OrderedDict()
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                #print('==>>',comp)
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = BipolarOutrankingDigraph(pt,
                                          WithConcordanceRelation=False,
                                          WithVetoCounts=False,
                                          Normalized=True,
                                          CopyPerfTab=False)
                pg.__dict__.pop('criteria')
                pg.__dict__.pop('evaluation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
                components[compKey]['score']=(comp[2],comp[3],comp[4])
        else:   # if self.sortingParameters['Threading'] == True:
                from copy import copy, deepcopy
                from pickle import dumps, loads, load, dump
                from multiprocessing import Process, Queue,active_children, cpu_count
                if Comments:
                    print('Processing the %d components' % nc )
                    print('Threading ...')
                #tdump = time()
                from tempfile import TemporaryDirectory,mkdtemp
                with TemporaryDirectory(dir=tempDir) as tempDirName:
                    ## tasks queue and workers launching
                    NUMBER_OF_WORKERS = nbrOfCPUs
                    tasksIndex = [(i,len(decomposition[i][1])) for i in range(nc)]
                    tasksIndex.sort(key=lambda pos: pos[1],reverse=True)
                    TASKS = [(Comments,(pos[0],nc,tempDirName,componentRankingRule)) for pos in tasksIndex]
                    task_queue = Queue()
                    for task in TASKS:
                        task_queue.put(task)
                    for i in range(NUMBER_OF_WORKERS):
                        Process(target=_worker,args=(task_queue,)).start()
                    print('started')
                    for i in range(NUMBER_OF_WORKERS):
                        task_queue.put('STOP')

                    while active_children() != []:
                        pass
                    if Comments:
                        print('Exit %d threads' % NUMBER_OF_WORKERS)

                    components = OrderedDict()
                    #componentsList = []
                    boostedRanking = []
                    for j in range(nc):
                        if Debug:
                            print('job',j)
                        fiName = tempDirName+'/splitComponent-'+str(j)+'.py'
                        fi = open(fiName,'rb')
                        splitComponent = loads(fi.read())
                        if Debug:
                            print('splitComponent',splitComponent)
                        components[splitComponent['compKey']] = splitComponent['compDict']
                        boostedRanking += splitComponent['compDict']['subGraph'].ranking
                    self.boostedRanking = boostedRanking
                    self.boostedOrder = list(reversed(self.boostedRanking))

        # storing components, fillRate and maximalComponentSize

        self.components = components
        fillRate = 0
        maximalComponentSize = 0
        for compKey,comp in components.items():
            pg = comp['subGraph']
            npg = pg.order
            if npg > maximalComponentSize:
                maximalComponentSize = npg
            fillRate += npg*(npg-1)
            for x in pg.actions.keys():
                self.actions[x]['component'] = compKey
        self.fillRate = fillRate/(self.order * (self.order-1))
        self.maximalComponentSize = maximalComponentSize




        # setting the component relation
        self.valuationdomain = {'min':Decimal('-1'),
                                'med':Decimal('0'),
                                'max':Decimal('1')}

        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )

        #  compute boosted ranking in not threaded exceution
        if not self.sortingParameters['Threading']:
            t0 = time()
            self.boostedRanking = self.computeBoostedRanking(rankingRule=componentRankingRule)
            self.boostedOrder = list(reversed(self.boostedRanking))
            self.runTimes['ordering'] = time() - t0
        else:
            self.runTimes['ordering'] = 0
        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        ########
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)


    # ----- class methods ------------


    def computeCLTLikelihoods(self,distribution="triangular",
                              betaParameter=None,
                              Debug=False):
        """
        Renders the pairwise CLT likelihood of the at least as good as relation
        neglecting all considerable large performance differences polarisations.
        """
        from decimal import Decimal
        from math import sqrt
        #from random import gauss
        sumWeights = Decimal('0')
        criteriaList = [x for x in self.criteria]
        m = len(criteriaList)

        weightSquares = {}
        for g in criteriaList:
            gWeight = abs(self.criteria[g]['weight'])
            weightSquares[g] = gWeight*gWeight
            sumWeights += gWeight
        concordanceRelation = self._recodeConcordanceValuation(\
                                self.sortingRelation,sumWeights,Debug=Debug)

        ccf = {}
        if distribution == 'uniform':
            varFactor = Decimal('1')/Decimal('3')
        elif distribution == 'triangular':
            varFactor = Decimal('1')/Decimal('6')
        elif distribution == 'beta':
            if betaParameter != None:
                a = Decimal(str(betaParameter))
            else:
                a = self.betaParameter
            varFactor = Decimal('1')/(Decimal('2')*a + Decimal('1'))
        ## elif distribution == 'beta(4,4)':
        ##     varFactor = Decimal('1')/Decimal('9')
        for x in concordanceRelation:
            ccf[x] = {}
            for y in concordanceRelation[x]:
                ccf[x][y] = {'std': Decimal('0.0')}
                for c in criteriaList:
                    ccf[x][y][c] = self.criterionCharacteristicFunction(c,x,y)
                    ccf[x][y]['std'] += abs(ccf[x][y][c])*weightSquares[c]
##                    if Debug:
##                        print(c,x,y,ccf[x][y][c])
                ccf[x][y]['std'] = sqrt(varFactor*ccf[x][y]['std'])
##                if Debug:
##                    print(x,y,ccf[x][y]['std'])
        lh = {}
        for x in concordanceRelation:
            lh[x] = {}
            for y in concordanceRelation[x]:

                mean = float(concordanceRelation[x][y])
                std = float(ccf[x][y]['std'])
                lh[x][y] = -self._myGaussCDF(mean,std,0.0)
                if Debug:
                    print(x,y,lh[x][y])
        return lh

    def _computeConfidentRelation(self,
                               sortingRelation,
                               likelihoodLevel=None,
                               Debug=False):
        """
        Renders the relation cut at likelihood level.
        """

        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']

        if likelihoodLevel == None:
            likelihoodLevel = self.bipolarConfidenceLevel

        print(likelihoodLevel)
        confidenceCutLevel = Med
        confidentRelation = {}
        #actionsList = [x for x in self.actions]

        for x in self.likelihoods:
            lhx = self.likelihoods[x]
            confidentRelation[x] = {}
            for y in lhx:
                lhxy = lhx[y]
                if abs(lhxy) >= likelihoodLevel:
                    confidentRelation[x][y] = sortingRelation[x][y]
                else:
                    confidentRelation[x][y] = Med
                    level = abs(sortingRelation[x][y])
                    if level < Max and level > confidenceCutLevel:
                        confidenceCutLevel = level
                if Debug:
                    print(x,y,sortingRelation[x][y],self.likelihoods[x][y],confidentRelation[x][y])
            self.confidenceCutLevel = confidenceCutLevel
        return confidentRelation

    def _recodeConcordanceValuation(self,oldRelation,sumWeights,Debug=False):
        """
        Recodes the characteristic valuation according
        to the parameters given.
        """
        if Debug:
            print(oldRelation,sumWeights)
        from copy import copy as deepcopy

##        oldMax = Decimal('1')
##        oldMin = Decimal('-1')
##        oldMed = Decimal('0')
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']
        oldAmplitude = oldMax - oldMin
        if Debug:
            print('old: ',oldMin, oldMed, oldMax, oldAmplitude)

        newMin = -sumWeights
        newMax = sumWeights
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))
        newAmplitude = newMax - newMin
        if Debug:
            print('new: ', newMin, newMed, newMax, newAmplitude)

##        actions = [x for x in self.actions]
        newRelation = {}
        for x in oldRelation:
            newRelation[x] = {}
            for y in oldRelation[x]:
                if oldRelation[x][y] == oldMax:
                    newRelation[x][y] = newMax
                elif oldRelation[x][y] == oldMin:
                    newRelation[x][y] = newMin
                elif oldRelation[x][y] == oldMed:
                    newRelation[x][y] = newMed
                else:
                    newRelation[x][y] = newMin +\
                        ((oldRelation[x][y] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(x,y,oldRelation[x][y],newRelation[x][y])

        return newRelation

    def _myGaussCDF(self,mean,sigma,x,Bipolar=True):
        """
        Bipolar error function of z = (x-mu)/sigma) divided by sqrt(2).
        If Bipolar = False,
        renders the Gauss cdf(z) = [erf( z ) + 1] / 2
        sqrt(2) = 1.4142135623731
        """
        #print(mean,sigma,x)
        from math import sqrt,erf
        try:
            z = (x - mean) / (sigma * 1.4142135623731)
        except:
            z = x
        if Bipolar:
            return erf(z)
        else:
            return 0.5 + 0.5*erf(z)

    def showRelationTable(self,IntegerValues=False,
                          actionsSubset= None,
                          Sorted=True,
                          LikelihoodDenotation=True,
                          hasLatexFormat=False,
                          hasIntegerValuation=False,
                          relation=None,
                          Debug=False):
        """
        prints the relation valuation in actions X actions table format.
        """
        if LikelihoodDenotation:
            try:
                likelihoods = self.likelihoods
            except:
                LikelihoodDenotation = False
        if Debug:
            print(LikelihoodDenotation)
        if actionsSubset == None:
            actions = self.actions
        else:
            actions = actionsSubset

        if relation == None:
            relation = self.confidentRelation

        print('* ---- Outranking Relation Table -----')
        if LikelihoodDenotation:
            print('r/(lh) | ', end=' ')
        else:
            print(' r()   | ', end=' ')
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(x,x)]
        if Sorted:
            actionsList.sort()

        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = IntegerValues

        for x in actionsList:
            print("'"+x[0]+"'\t", end=' ')
        print('\n-------|------------------------------------------------------------')
        for x in actionsList:
            if hasLatexFormat:
                print("$"+x[0]+"$ & ", end=' ')
            else:
                print(" '"+x[0]+"' |", end=' ')
            for y in actionsList:
                if hasIntegerValuation:
                    if hasLatexFormat:
                        print('$%+d$ &' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        print('%+d' % (relation[x[1]][y[1]]), end=' ')
                else:
                    if hasLatexFormat:
                        print('$%+.2f$ & ' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        print(' %+.2f ' % (relation[x[1]][y[1]]), end=' ')

            if hasLatexFormat:
                print(' \\cr')
            else:
                print()
            if LikelihoodDenotation:
                headString = "' "+x[0]+"' "
                formatStr = ' ' * len(headString)
                print(formatStr+'|', end=' ')
                for y in actionsList:
                    if x != y:
                        print('(%+.2f)' % (likelihoods[x[1]][y[1]]), end=' ')
                    else:
                        print(' ( - ) ', end=' ')
                print()

        print('Valuation domain : [%+.3f; %+.3f] ' % (self.valuationdomain['min'],
                                                   self.valuationdomain['max']))
        print('Uncertainty model: %s(a=%.1f,b=%.1f) ' % (self.distribution,
                                                         self.betaParameter,
                                                         self.betaParameter)
                                                         )
        print('Likelihood domain: [-1.0;+1.0] ')
        print('Likelihood level : %.2f (%.2f%%) ' % (self.bipolarConfidenceLevel,
                                                     (self.bipolarConfidenceLevel+1.0)/2.0))

        print('Determinateness  : %.3f ' % self.computeDeterminateness() )
        print('\n')

#######################################################################
#######################################################################
#----------test classes and methods ----------------
if __name__ == "__main__":

    from time import time
##    t = XMCDA2PerformanceTableau('project_7')
##    tenv = PartialPerformanceTableau(t,objectivesSubset=['Eco'])
##    pre = PreRankedOutrankingDigraph(tenv,Debug=True)
##    print(pre.computeOrderCorrelation(pre.boostedOrder))
##    tenv.showHTMLPerformanceHeatmap()
    MP  = False
    nbrActions=1000
##    t0 = time()
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,seed=100)
##    tp = XMCDA2PerformanceTableau('the_cs_2016')

##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,Threading=MP,
##                                     seed=100)
    bg1 = PreRankedOutrankingDigraph(tp,CopyPerfTab=True,quantiles=4,
                                 quantilesOrderingStrategy='optimal',
                                 componentRankingRule='NetFlows',
                                 LowerClosed=True,
                                 minimalComponentSize=1,
                                 Threading=MP,nbrOfCPUs=8,
                                 #tempDir='.',
                                 nbrOfThreads=8,
                                 Comments=True,Debug=False,
                                 save2File='testbgMP')
    bg1.showDecomposition(direction='decreasing')

    seed= 1
    sampleSize = 100
##    import random
##    random.seed(seed)
##    actionKeys = [x for x in bg1.actions]
##    sample = random.sample(actionKeys,sampleSize)
##    print(sample)
##    print(bg1.boostedRanking)
##    preRankedSample = []
##    for x in bg1.boostedRanking:
##        if x in sample:
##            preRankedSample.append(x)
##    print(preRankedSample)
##    ptp = PartialPerformanceTableau(tp,sample)
##    from outrankingDigraphs import BipolarOutrankingDigraph
##    pg = BipolarOutrankingDigraph(ptp,Normalized=True)
##    print(pg.computeRankingCorrelation(preRankedSample))
    print(bg1.estimateRankingCorrelation(sampleSize,seed))
