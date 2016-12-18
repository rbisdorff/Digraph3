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
######################

#import cython
cimport cython
from cpython cimport array
import array

cdef extern from "detertest.h":
    inline int ABS(int a)


from cIntegerOutrankingDigraphs import *
from cIntegerSortingDigraphs import *
from time import time
from decimal import Decimal
from cBigIntegerOutrankingDigraphs import *

class BigIntegerDigraph(object):
    """
    Abstract root class for linearly decomposed big digraphs (order > 1000)
    using multiprocessing ressources.
    """
    def __repr__(self):
        """
        Default presentation method for bigDigraphs instances.
        """
        print('*----- show short --------------*')
        print('Instance name     : %s' % self.name)
        print('# Actions         : %d' % self.order)
        print('# Criteria        : %d' % self.dimension)
        print('Sorting by        : %d-Tiling' % self.sortingParameters['limitingQuantiles'] )
        print('Ordering strategy : %s' % self.sortingParameters['strategy'] )
        print('Ranking rule      : %s' % self.componentRankingRule)
        print('# Components      : %d' % self.nbrComponents)
        print('Minimal order     : %d' % self.minimalComponentSize)
        print('Maximal order     : %d' % self.maximalComponentSize)
        print('Average order     : %.1f' % (self.order/self.nbrComponents) )
        print('fill rate         : %.3f%%' % (self.fillRate*100.0) )     
        print('----  Constructor run times (in sec.) ----')
        print('Nbr of threads    : %d' % self.nbrOfCPUs)
        print('Total time        : %.5f' % self.runTimes['totalTime'])
        print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
        print('Preordering       : %.5f' % self.runTimes['preordering'])
        print('Decomposing       : %.5f' % self.runTimes['decomposing'])
        try:
            print('Ordering          : %.5f' % self.runTimes['ordering'])
        except:
            pass
        return '%s instance' % str(self.__class__)

    def showBestChoiceRecommendation(self,Comments=False,ChoiceVector=False,Debug=False):
        """
        Update of rubisBestChoice Recommendation for big digraphs.
        To do: limit to best choice; worst choice should be a separate method()
        """
        from digraphs import Digraph as DG
        # best choices
        c1 = (list(self.components.keys()))[0]
        g1 = self.components[c1]['subGraph']
        if len(g1.actions) > 1:
            self.showRubisBestChoiceRecommendation(g1,Debug=Debug,ChoiceVector=False,Comments=Comments)
        else:
            actionsNames = [g1.actions[x]['name'] for x in g1.actions]
            print('Best choice recommendation: \'%s\'' % (actionsNames[0]))
        # worst choices
        cn = (list(self.components.keys()))[-1]
        gn = self.components[cn]['subGraph']
        if len(gn.actions) > 1:
            self.showRubisWorstChoiceRecommendation(gn,Debug=Debug,ChoiceVector=False,Comments=Comments)
        else:
            actionsNames = [gn.actions[x]['name'] for x in gn.actions]
            print('Worst choice recommendation: \'%s\'' % (actionsNames[-1]))


    def showRubisBestChoiceRecommendation(self,g1,
                                          Comments=False,
                                          ChoiceVector=True,
                                          Debug=False,
                                          _OldCoca=False,
                                          Cpp=False):
        """
        Renders the Rubis Best choice recommendation of the first component.
        """
        import copy,time
        if Debug:
            Comments = True
        print('***********************')
        print('Best Choice Recommendation')
        if Comments:
            print('All comments !!!')
        t0 = time.time()
        n0 = g1.order
        if _OldCoca:
            _selfwcoc = _CocaDigraph(g1,Cpp=Cpp,Comments=Comments)
            b1 = 0
        else:
            _selfwcoc = CocaDigraph(g1,Cpp=Cpp,Comments=Comments)
            b1 = _selfwcoc.brakings
        n1 = _selfwcoc.order
        nc = n1 - n0
        
        g1.relation_orig = copy.deepcopy(g1.relation)
        if nc > 0 or b1 > 0:
            g1.actions_orig = copy.deepcopy(g1.actions)
            g1.actions = copy.deepcopy(_selfwcoc.actions)
            g1.order = len(g1.actions)
            g1.relation = copy.deepcopy(_selfwcoc.relation)
        if Comments:
            print('List of pseudo-independent choices')
            print(g1.actions)
        g1.gamma = g1.gammaSets()
        g1.notGamma = g1.notGammaSets()
        if Debug:
            g1.showRelationTable()
        #self.showPreKernels()
        actions = set([x for x in g1.actions])
        g1.computePreKernels()
        #if Debug:
        #    print(self.dompreKernels,self.abspreKernels)
        g1.computeGoodChoices(Comments=Comments)
        g1.computeBadChoices(Comments=Comments)
        if Debug:
            print('good and bad choices: ',g1.goodChoices,g1.badChoices)
        t1 = time.time()
        print('* --- Best choice recommendation(s) ---*')
        print('  (in decreasing order of determinateness)   ')
        print('Credibility domain: ', g1.valuationdomain)
        Med = g1.valuationdomain['med']
        bestChoice = set()
        worstChoice = set()
        for gch in g1.goodChoices:
            if gch[0] <= Med:
                goodChoice = True
                for bch in g1.badChoices:
                    if gch[5] == bch[5]:
                        #if gch[0] == bch[0]:
                        if gch[3] == gch[4]:
                            if Comments:
                                print('null choice ')
                                g1.showChoiceVector(gch,
                                                      ChoiceVector=ChoiceVector)
                                g1.showChoiceVector(bch,
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        elif gch[4] > gch[3]:
                            if Comments:
                                print('outranked choice ')
                                g1.showChoiceVector(gch,
                                                      ChoiceVector=ChoiceVector)
                                g1.showChoiceVector(bch,
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        else:
                            goodChoice = True
                if goodChoice:
                    print(' === >> potential BCR ')
                    g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
                    if bestChoice == set():
                        bestChoice = gch[5]
            else:
                if Comments:
                    print('non robust best choice ')
                    g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
        # for bch in self.badChoices:
        #     if bch[0] <= Med:
        #         badChoice = True
        #         nullChoice = False
        #         for gch in self.goodChoices:
        #             if bch[5] == gch[5]:
        #                 #if gch[0] == bch[0]:
        #                 if bch[3] == bch[4]:
        #                     if Comments:
        #                         print('null choice ')
        #                         self.showChoiceVector(gch,ChoiceVector=ChoiceVector)
        #                         self.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        #                     badChoice = False
        #                     nullChoice = True
        #                 elif bch[3] > bch[4]:
        #                     if Comments:
        #                         print('outranking choice ')
        #                         self.showChoiceVector(gch,ChoiceVector=ChoiceVector)
        #                         self.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        #                     badChoice = False
        #                 else:
        #                     badChoice = True
        #         if badChoice:
        #             print(' === >> potential worst choice ')
        #             self.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        #             if worstChoice == set():
        #                 worstChoice = bch[5]
        #         elif nullChoice:
        #             print(' === >> ambiguous choice ')
        #             self.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        #             if worstChoice == set():
        #                 worstChoice = bch[5]

        #     else:
        #         if Comments:
        #             print('non robust worst choice ')
        #             self.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        print()
        print('Execution time: %.3f seconds' % (t1-t0))
        print('*****************************')
        self.bestChoice = bestChoice
        #self.worstChoice = worstChoice
        if nc > 0 or b1 > 0:
            g1.actions = copy.deepcopy(g1.actions_orig)
            g1.relation = copy.deepcopy(g1.relation_orig)
            g1.order = len(g1.actions)
            g1.gamma = g1.gammaSets()
            g1.notGamma = g1.notGammaSets()

    def showRubisWorstChoiceRecommendation(self,g1,
                                          Comments=False,
                                          ChoiceVector=True,
                                          Debug=False,
                                          _OldCoca=False,
                                          Cpp=False):
        """
        Renders the Rubis Worst choice recommendation of the first component.
        """
        import copy,time
        if Debug:
            Comments = True
        print('***********************')
        print('Worst Choice Recommendation')
        if Comments:
            print('All comments !!!')
        t0 = time.time()
        n0 = g1.order
        if _OldCoca:
            _selfwcoc = _CocaDigraph(g1,Cpp=Cpp,Comments=Comments)
            b1 = 0
        else:
            _selfwcoc = CocaDigraph(g1,Cpp=Cpp,Comments=Comments)
            b1 = _selfwcoc.brakings
        n1 = _selfwcoc.order
        nc = n1 - n0
        
        g1.relation_orig = copy.deepcopy(g1.relation)
        if nc > 0 or b1 > 0:
            g1.actions_orig = copy.deepcopy(g1.actions)
            g1.actions = copy.deepcopy(_selfwcoc.actions)
            g1.order = len(g1.actions)
            g1.relation = copy.deepcopy(_selfwcoc.relation)
        if Comments:
            print('List of pseudo-independent choices')
            print(g1.actions)
        g1.gamma = g1.gammaSets()
        g1.notGamma = g1.notGammaSets()
        if Debug:
            g1.showRelationTable()
        #self.showPreKernels()
        actions = set([x for x in g1.actions])
        g1.computePreKernels()
        #if Debug:
        #    print(self.dompreKernels,self.abspreKernels)
        g1.computeGoodChoices(Comments=Comments)
        g1.computeBadChoices(Comments=Comments)
        if Debug:
            print('good and bad choices: ',g1.goodChoices,g1.badChoices)
        t1 = time.time()
        print('* --- Best choice recommendation(s) ---*')
        print('  (in decreasing order of determinateness)   ')
        print('Credibility domain: ', g1.valuationdomain)
        Med = g1.valuationdomain['med']
        bestChoice = set()
        worstChoice = set()
        # for gch in g1.goodChoices:
        #     if gch[0] <= Med:
        #         goodChoice = True
        #         for bch in g1.badChoices:
        #             if gch[5] == bch[5]:
        #                 #if gch[0] == bch[0]:
        #                 if gch[3] == gch[4]:
        #                     if Comments:
        #                         print('null choice ')
        #                         g1.showChoiceVector(gch,
        #                                               ChoiceVector=ChoiceVector)
        #                         g1.showChoiceVector(bch,
        #                                               ChoiceVector=ChoiceVector)
        #                     goodChoice = False
        #                 elif gch[4] > gch[3]:
        #                     if Comments:
        #                         print('outranked choice ')
        #                         g1.showChoiceVector(gch,
        #                                               ChoiceVector=ChoiceVector)
        #                         g1.showChoiceVector(bch,
        #                                               ChoiceVector=ChoiceVector)
        #                     goodChoice = False
        #                 else:
        #                     goodChoice = True
        #         if goodChoice:
        #             print(' === >> potential BCR ')
        #             g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
        #             if bestChoice == set():
        #                 bestChoice = gch[5]
        #     else:
        #         if Comments:
        #             print('non robust best choice ')
        #             g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
        for bch in g1.badChoices:
            if bch[0] <= Med:
                badChoice = True
                nullChoice = False
                for gch in g1.goodChoices:
                    if bch[5] == gch[5]:
                        #if gch[0] == bch[0]:
                        if bch[3] == bch[4]:
                            if Comments:
                                print('null choice ')
                                g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
                                g1.showChoiceVector(bch,ChoiceVector=ChoiceVector)
                            badChoice = False
                            nullChoice = True
                        elif bch[3] > bch[4]:
                            if Comments:
                                print('outranking choice ')
                                g1.showChoiceVector(gch,ChoiceVector=ChoiceVector)
                                g1.showChoiceVector(bch,ChoiceVector=ChoiceVector)
                            badChoice = False
                        else:
                            badChoice = True
                if badChoice:
                    print(' === >> potential worst choice ')
                    g1.showChoiceVector(bch,ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]
                elif nullChoice:
                    print(' === >> ambiguous choice ')
                    g1.showChoiceVector(bch,ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]

            else:
                if Comments:
                    print('non robust worst choice ')
                    g1.showChoiceVector(bch,ChoiceVector=ChoiceVector)
        print()
        print('Execution time: %.3f seconds' % (t1-t0))
        print('*****************************')
        #self.bestChoice = bestChoice
        self.worstChoice = worstChoice
        if nc > 0 or b1 > 0:
            g1.actions = copy.deepcopy(g1.actions_orig)
            g1.relation = copy.deepcopy(g1.relation_orig)
            g1.order = len(g1.actions)
            g1.gamma = g1.gammaSets()
            g1.notGamma = g1.notGammaSets()

                  
    def relation(self, int x, int y):
        """
        Dynamic construction of the global outranking characteristic function *r(x S y)*.
        """
        cdef int Min, Med, Max, rx, ry
        
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        
        if x == y:
            return Med
        
        cx = self.actions[x]['component']
        cy = self.actions[y]['component']
        #print(self.components)
        rx = self.components[cx]['rank']
        ry = self.components[cy]['rank']
        
        if rx == ry:
            rxpg = self.components[cx]['subGraph'].relation
            return rxpg[x][y]
        elif rx > ry:
            return Min
        else:
            return Max
    
    #@cython.locals(x=cython.int)
    def showRelationMap(self,int fromIndex=0,int toIndex=0, symbols=None):
        """
        Prints on the console, in text map format, the location of
        the diagonal outranking components of the big outranking digraph.

        By default, symbols = {'max':'┬','positive': '+', 'median': ' ',
                               'negative': '-', 'min': '┴'}

        The default ordering of the output is following the quantiles sorted boosted net flows ranking rule
        from best to worst actions. Further available ranking rules are Kohler's (rankingRule="kohler")
        and Tideman's ranked pairs rule (rankingRule="rankedPairs").
        
        """
        cdef int x, y, Max, Med, Min
        
        if symbols == None:
            symbols = {'max':'┬','positive': '+', 'median': ' ',
                       'negative': '-', 'min': '┴'}
        relation = self.relation
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        if toIndex == 0:
            toIndex = len(self.boostedRanking)
        for x in self.boostedRanking[fromIndex:toIndex]:
            pictStr = ''
            for y in self.boostedRanking[fromIndex:toIndex]:
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
        print('Component ranking rule: %s' % self.componentRankingRule)

    def showHTMLRelationMap(self,int fromIndex=0,int toIndex=0,\
                            bint Colored=True,\
                            tableTitle='Big Relation Map',\
                            relationName='r(x S y)',\
                            symbols=['+','&middot;','&nbsp;','&#150;','&#151']
                            ):
        """
        Launches a browser window with the colored relation map of self.
        See corresponding Digraph.showRelationMap() method.

        Example::

            >>> from outrankingDigraphs import *
            >>> t = RandomCBPerformanceTableau(numberOfActions=25,seed=1)
            >>> g = BipolarOutrankingDigraph(t,Normalized=True)
            >>> gcd = ~(-g)  # strict outranking relation
            >>> gcd.showHTMLRelationMap(rankingRule="netFlows")
            
        .. image:: relationMap.png
           :alt: Browser view of a relation map
           :width: 600 px
           :align: center
    
   
        """
        import webbrowser
        fileName = '/tmp/relationMap.html'
        fo = open(fileName,'w')
        fo.write(self._htmlRelationMap(fromIndex=fromIndex,
                                      toIndex=toIndex,
                                      Colored=Colored,
                                      tableTitle=tableTitle,
                                      symbols=symbols,
                                      ContentCentered=True,
                                      relationName=relationName))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
        
        
    def _htmlRelationMap(self,int fromIndex=0,int toIndex=0,\
                            tableTitle='Big Relation Map',\
                          relationName='r(x R y)',\
                          #rankingRule='Copeland',\
                          symbols=['+','&middot;','&nbsp;','-','_'],\
                          bint Colored=True,\
                          bint ContentCentered=True):
        """
        renders the relation map in actions X actions html table format.
        """
        cdef int Min, Med, Max
        
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        # construct ranking and actionsList
        if toIndex == 0:
            toIndex = len(self.boostedRanking)

        actionsList = [(self.actions[x]['name'],x) for x in self.boostedRanking[fromIndex:toIndex]]
        # construct html text
        s  = '<!DOCTYPE html><html><head>\n'
        s += '<meta charset="UTF-8">\n'
        s += '<title>%s</title>\n' % 'Digraph3 relation map'
        s += '<style type="text/css">\n'
        if ContentCentered:
            s += 'td {text-align: center;}\n'
        s += 'td.na {color: rgb(192,192,192);}\n'
        s += '</style>\n'
        s += '</head>\n<body>\n'
        s += '<h1>%s</h1>' % tableTitle
        s += '<h2>Component ranking rule: %s</h2>' % self.componentRankingRule
        s += '<table border="0">\n'
        if Colored:
            s += '<tr bgcolor="#9acd32"><th>%s</th>\n' % relationName
        else:
            s += '<tr><th>%s</th>' % relationName

        for x in actionsList:
            if Colored:
                s += '<th bgcolor="#FFF79B">%s</th>\n' % (x[0])
            else:
                s += '<th>%s</th\n>' % (x[0])
        s += '</tr>\n'
        for x in actionsList:
            s += '<tr>'
            if Colored:
                s += '<th bgcolor="#FFF79B">%s</th>\n' % (x[0])
            else:
                s += '<th>%s</th>\n' % (x[0])
            for y in actionsList:
                if Colored:
                    if self.relation(x[1],y[1]) == Max:
                        s += '<td bgcolor="#66ff66"><b>%s</b></td>\n' % symbols[0]
                    elif self.relation(x[1],y[1]) > Med:
                        s += '<td bgcolor="#ddffdd">%s</td>' % symbols[1]
                    elif self.relation(x[1],y[1]) == Min:
                        s += '<td bgcolor="#ff6666"><b>%s</b></td\n>' % symbols[4]
                    elif self.relation(x[1],y[1]) < Med:
                        s += '<td bgcolor="#ffdddd">%s</td>\n' % symbols[3]
                    else:
                        #s += '<td bgcolor="#ffffff">%s</td>\n' % symbols[2]
                        s += '<td class="na">%s</td>\n' % symbols[2]
                else:
                    if self.relation(x[1],y[1]) == Max:
                        s += '<td><b>%s</b></td>\n'  % symbols[0]
                    elif self.relation(x[1],y[1]) > Med:
                        s += '<td>%s</td>\n' % symbols[1]
                    elif self.relation(x[1],y[1]) == Min:
                        s += '<td><b>%s</b></td>\n' % symbols[4]
                    elif self.relation(x[1],y[1]) < Med:
                        s += '<td>%s</td>\n' % symbols[3]
                    else:
                        s += '<td>%s</td>\n' % symbols[2]
            s += '</tr>'
        s += '</table>\n'
        # legend
        s += '<span style="font-size: 75%">\n'
        s += '<table border="1"><tr><th colspan="2"><i>Semantics</i></th></tr>\n'
        if Colored:
            s += '<tr><td bgcolor="#66ff66" align="center">%s</td><td>certainly valid</td></tr>\n' % symbols[0]
            s += '<tr><td bgcolor="#ddffdd" align="center">%s</td><td>valid</td></tr>\n' % symbols[1]
            s += '<tr><td>%s</td><td>indeterminate</td></tr>\n' % symbols[2]
            s += '<tr><td bgcolor="#ffdddd" align="center">%s</td><td>invalid</td></tr>\n' % symbols[3]
            s += '<tr><td bgcolor="#ff6666" align="center">%s</td><td>certainly invalid</td></tr>\n' % symbols[4]
            s += '</table>\n'
        else:
            s += '<tr><td align="center">%s</td><td>certainly valid</td></tr>\n' % symbols[0]
            s += '<tr><td align="center">%s</td><td>valid</td></tr>\n' % symbols[1]
            s += '<tr><td align="center">%s</td><td>indeterminate</td></tr>\n' % symbols[2]
            s += '<tr><td align="center">%s</td><td>invalid</td></tr>\n' % symbols[3]
            s += '<tr><td align="center">%s</td><td>certainly invalid</td></tr>\n' % symbols[4]
            s += '</table>\n'
        s += '</span>\n'
        # html footer
        s += '</body>\n'
        s += '</html>\n'
        return s


    #@cython.locals(x=cython.int,y=cython.int)
    def computeOrdinalCorrelation(self, other, bint Debug=False):
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
        cdef int x, y, sMax, oMax, selfMultiple=1, otherMultiple=1
        cdef int corr, determ, selfRelation, otherRelation
        cdef int corrSum=0, determSum=0
        cdef double correlation=0.0, determination=0.0
        
        ## if self.valuationdomain['min'] != Decimal('-1.0'):
        ##         print('Error: the BigDigraph instance must be normalized !!')
        ##         print(self.valuationdomain)
        ##         return

        sMax = self.valuationdomain['max']
        oMax = int(other.valuationdomain['max'])
        #if Debug:
        #    print('self Max', sMax)
        #    print('other Max', oMax)
        #if issubclass(other.__class__,(Digraph,BigIntegerDigraph)):
        #    if Debug:
        #        print('other is a %s instance' % other.__class__)
                #print('self', self.valuationdomain)
                #print('other', other.valuationdomain)
        if (oMax != sMax) :
            selfMultiple = oMax
            otherMultiple = sMax
        #if Debug:
        #    print('self', selfMultiple)
        #    print('other', otherMultiple)
        
        #     print('Error: the other digraph must be recoded !!')
        #     print('self', self.valuationdomain)
        #     print('other', other.valuationdomain)
        #     return
        for x in self.actions:
            for y in self.actions:
                if x != y:
                    selfRelation = self.relation(x,y) * selfMultiple
                    try:
                        otherRelation = other.relation(x,y) * otherMultiple
                    except:
                        otherRelation = int(other.relation[x][y]) * otherMultiple
                    #if Debug:
                    #   print(x,y,'self', selfRelation)
                    #   print(x,y,'other', otherRelation)
                    corr = min( max(-selfRelation,otherRelation),\
                                 max(selfRelation,-otherRelation) )
                    corrSum += corr
                    determ = min( abs(selfRelation),abs(otherRelation) )
                    determSum += determ

        if determSum > 0:
            correlation = float(corrSum) / float(determSum)
            n2 = (self.order*self.order) - self.order
            determination = (float(determSum) / n2)
            determination /= (sMax * selfMultiple)
            
            return { 'correlation': correlation,\
                     'determination': determination }
        else:
            return { 'correlation': 0.0,\
                     'determination': 0.0 }

    #@cython.locals(x=cython.int,y=cython.int)
    def computeRankingCorrelation(self, ranking, bint Debug=False):
        """
        Renders the ordinal correlation K of a BigDigraph instance
        when compared with a given linear ranking of its actions
        
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
        cdef int i, j, x, y, sMax, oMax, selfMultiple=1, otherMultiple=1
        cdef int corr, determ, selfRelation, otherRelation
        cdef int corrSum=0, determSum=0
        cdef double correlation=0.0, determination=0.0
        
        sMax = self.valuationdomain['max']
        # selfMultiple = 1
        otherMultiple = sMax
        n = len(ranking)
        for i in range(n-1):
            x = ranking[i]
            for j in range(i+1,n):
                y = ranking[j]
                selfRelation = self.relation(x,y)
                otherRelation = sMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ
                selfRelation = self.relation(y,x)
                otherRelation = -sMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ

        if determSum > 0:
            correlation = float(corrSum) / float(determSum)
            n2 = (self.order*self.order) - self.order
            determination = (float(determSum) / n2)
            determination /= (sMax * selfMultiple)
            
            return { 'correlation': correlation,\
                     'determination': determination }
        else:
            return { 'correlation': 0.0,\
                     'determination': 0.0 }

        
    def showDecomposition(self,direction='decreasing'):
        """
        Prints on the console the decomposition structure of the sparse outranking digraph instance
        in *decreasing* (default) or *increasing* preference direction.
        """
        cdef int x
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
        cdef int nc
        try:
            import statistics
        except:
            print('Error importing the statistics module.')
            print('You need to upgrade your Python to version 3.4+ !')
            return      
        nc = self.nbrComponents
        compLengths = [comp['subGraph'].order \
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

    def _recodeIntegerValuation(self,int otherMax=1,Debug=False):
        """
        Specialization for recoding the valuation of all the partial digraphs and the component relation.
        """
        # update valuation domain
        self.valuationdomain['max'] *= otherMax
        self.valuationdomain['min'] *= otherMax
        # update components' valuation domain and relation
        for cki in self.components.keys(): 
            pg = self.components[cki]['subGraph']
            pg.valuationdomain['min'] *= otherMax
            pg.valuationdomain['max'] *= otherMax
            for x in pg.actions:
                for y in pg.actions:
                    pg.relation[x][y] *= otherMax 

    #@cython.locals(x=cython.int)
    def ranking2Preorder(self,ranking):
        """
        Renders a preordering (a list of list) of a ranking (best to worst) of decision actions in increasing preference direction.
        """
        cdef int x
        #ordering = list(ranking)
        #ordering.reverse()
        preordering = [[x] for x in reversed(ranking)]
        return preordering

    #@cython.locals(x=cython.int)
    def ordering2Preorder(self,ordering):
        """
        Renders a preordering (a list of list) of a linar order (worst to best) of decision actions in increasing preference direction.
        """
        cdef int x
        preordering = [[x] for x in ordering]
        return preordering

    #@cython.locals(fillRate=cython.double)
    def computeFillRate(self,Debug=False):
        """
        Renders the sum of the squares (without diagonal) of the orders of the component's subgraphs
        over the square (without diagonal) of the big digraph order. 
        """
        
        fillRateSum = sum((comp['subGraph'].order*comp['subGraph'].order-1)\
                        for comp in self.components.values())
        n2 = self.order*(self.order-1)
        fillRate = float(fillRateSum)/n2
        return fillRate


########################
# multiprocessing workers
def worker(input):
    for Comments,args in iter(input.get, 'STOP'):
        result = decompose(*args)
        if Comments:
            print(result)

# def compute(func,args):
#     result = func(*args)
#     print( '%d/%d = %s' % \
#            (args[1], args[2],result))

def decompose(int i, int nc,tempDirName):
    cdef int nd
    global perfTab
    global decomposition
    from pickle import dumps
    comp = decomposition[i]
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
    pg.computeCopelandRanking()
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

#from weakOrders import QuantilesRankingDigraph
from cRandPerfTabs import PerformanceTableau
class BigIntegerOutrankingDigraph(BigIntegerDigraph,PerformanceTableau):
    """
    Main class for the multiprocessing implementation of big outranking digraphs.
    
    The big outranking digraph instance is decomposed with a q-tiling sort into a partition
    of quantile equivalence classes which are linearly ordered by average quantile limits (default).

    With each quantile equivalence class is associated a BipolarOutrankingDigraph object
    which is restricted to the decision actions gathered in this quantile equivalence class.

    By default, the number of quantiles q is set to a twentieth of the number of decision actions,
    ie q = order//10. The effective number of quantiles may be much lower for large orders;
    for instance quantiles = 250 may give good results for a digraph of order 25000.
    
    For other parameters settings, see the corresponding :py:class:`sortingDigraphs.QuantilesSortingDigraph` class.

    """
    
    def __init__(self,argPerfTab,\
                 int quantiles=0,\
                 quantilesOrderingStrategy="average",\
                 bint LowerClosed=False,\
                 componentRankingRule="Copeland",\
                 int minimalComponentSize=1,\
                 bint Threading=False,\
                 tempDir=None,\
                 int componentThreadingThreshold=50,\
                 int nbrOfSubProcesses=0,
                 int nbrOfCPUs=1,\
                 int nbrOfThreads=1,\
                 save2File=None,\
                 bint CopyPerfTab=False,\
                 bint Comments=False,\
                 bint Debug=False):

        cdef int i, j, totalWeight = 0
        cdef int nbrOfLocals,nbrOfThreadsUsed,threadLoad
        cdef double ttot, t0, tw, tdump
        cdef int maximalComponentSize
        cdef array.array lTest=array.array('i')

        global perfTab
        global decomposition

        from digraphs import Digraph
        from cIntegerSortingDigraphs import IntegerQuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        #from array import array
        from multiprocessing import Pool            
        #from cython.parallel import prange
        from copy import copy, deepcopy
        from cIntegerOutrankingDigraphs import IntegerBipolarOutrankingDigraph

        print('Cythonized BigIntegerOutrankingDigraph class')
   
        ttot = time()

        # setting name
        perfTab = argPerfTab
        self.name = perfTab.name + '_mp'
        # setting quantiles sorting parameters
        if CopyPerfTab:
            self.actions = deepcopy(perfTab.actions)
            self.criteria = deepcopy(perfTab.criteria)
            self.evaluation = deepcopy(perfTab.evaluation)
        else:
            self.actions = perfTab.actions
            self.criteria = perfTab.criteria
            self.evaluation = perfTab.evaluation
        na = len(self.actions)
        self.order = na
        dimension = len(perfTab.criteria)
        self.dimension = dimension
        for g in self.criteria:
            self.criteria[g]['weight'] = int(self.criteria[g]['weight'])
            totalWeight += self.criteria[g]['weight']
        
        #######
        if quantiles == 0:
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
        qs = IntegerQuantilesSortingDigraph(argPerfTab=perfTab,
                                     limitingQuantiles=quantiles,
                                     LowerClosed=LowerClosed,
                                     #IntegerValued=True,
                                     CompleteOutranking=False,
                                     StoreSorting=True,
                                     #WithSortingRelation=False,
                                     CopyPerfTab=CopyPerfTab,
                                     Threading= self.sortingParameters['Threading'],
                                     tempDir=tempDir,
                                     nbrCores=nbrOfCPUs,
                                     nbrOfProcesses=nbrOfThreads,
                                     #componentThreadingThreshold=50,
                                     Comments=Comments,
                                     Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
        self.valuationdomain = qs.valuationdomain
        self.profiles = qs.profiles
        self.categories = qs.categories
        self.sorting = qs.sorting
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))
        # preordering
##        if minimalComponentSize == None:
##            minimalComponentSize = 1
        self.minimalComponentSize = minimalComponentSize
        tw = time()
        quantilesOrderingStrategy = self.sortingParameters['strategy']
        ##if quantilesOrderingStrategy == 'average':
        decomposition = [[(item[0][0],item[0][1]),item[1]]\
                for item in self._computeQuantileOrdering(\
                    strategy=quantilesOrderingStrategy,\
                    Descending=True,
                    Threading=Threading,
                    nbrOfCPUs=nbrOfCPUs)]
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
        nd = len(str(nc))
        self.nd = nd
        if not self.sortingParameters['Threading']:
            components = OrderedDict()
            boostedRanking = []
            for i in range(1,nc+1):
                comp = decomposition[i-1]
                compKey = ('c%%0%dd' % (self.nd)) % (i)
                components[compKey] = {'rank':i}
                pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                components[compKey]['lowQtileLimit'] = comp[0][1]
                components[compKey]['highQtileLimit'] = comp[0][0]
                pg = IntegerBipolarOutrankingDigraph(pt,
                                          WithConcordanceRelation=False,
                                          WithVetoCounts=False,
                                          #Normalized=True,
                                          CopyPerfTab=False)
                boostedRanking += pg.computeCopelandRanking()
                pg.__dict__.pop('criteria')
                pg.__dict__.pop('evaluation')
                pg.__class__ = Digraph
                components[compKey]['subGraph'] = pg
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
                TASKS = [(Comments,(pos[0],nc,tempDirName)) for pos in tasksIndex]
                task_queue = Queue()
                for task in TASKS:
                    task_queue.put(task)
                for i in range(NUMBER_OF_WORKERS):
                    Process(target=worker,args=(task_queue,)).start()
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
                    boostedRanking += splitComponent['compDict']['subGraph'].copelandRanking

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
        
        self.valuationdomain = {'min': -totalWeight,
                                'med': 0,
                                'max': totalWeight}
       
        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )
        # Kohler ranking-by-choosing all components
        self.componentRankingRule = componentRankingRule
        t0 = time()
        #self.boostedRanking = self.computeBoostedRanking(rankingRule=componentRankingRule)
        #self.boostedOrder = list(reversed(self.boostedRanking))
        self.boostedRanking = boostedRanking
        self.runTimes['ordering'] = time() - t0

        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File,WithFileSize=False)
            

    # ----- class methods ------------

    def _computeQuantileOrdering(self,strategy=None,
                                bint Descending=True,
                                bint  Threading=False,
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
        cdef double lc,hc,score1,score2,score3,score4
        
        from operator import itemgetter

        if strategy == None:
            strategy = self.sortingParameters['strategy']
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility,lowLimit,notHighLimit =\
                     self.computeActionCategories(x,Comments=Comments,Debug=False,\
                                               Threading=Threading,\
                                               nbrOfCPUs = nbrOfCPUs)
            lowQtileLimit = self.categories[lowCateg]['lowLimit']
            highQtileLimit = self.categories[highCateg]['highLimit']
            if strategy == "optimistic":
                score1 = float(highCateg)
                score2 = -notHighLimit
                score3 = float(lowCateg)
                score4 = lowLimit
            elif strategy == "pessimistic":
                score1 = float(lowCateg)
                score2 = lowLimit
                score3 = float(highCateg)
                score4 = -notHighLimit
            else:   #strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                score1 = (lc+hc)/2.0
                score2 = float(highCateg)
                score3 = -notHighLimit
                score4 = lowLimit
            #print(score,highQtileLimit,lowQtileLimit,lowCateg,highCateg)
            try:
                actionsCategories[(score1,highQtileLimit,\
                                   lowQtileLimit,lowCateg,highCateg,score2,score3,score4)].append(a)
            except:
                actionsCategories[(score1,highQtileLimit,\
                                   lowQtileLimit,lowCateg,highCateg,score2,score3,score4)] = [a]
            # if strategy == "optimistic":
            #     score = highQtileLimit
            # elif strategy == "pessimistic":
            #     score = lowQtileLimit
            # else:   #strategy == "average":
            #     lc = float(lowCateg)
            #     hc = float(highCateg)
            #     score = (lc+hc)/2.0
            # # if Debug:
            # #     print(x,score,highQtileLimit,lowQtileLimit,lowCateg,highCateg)
            # try:
            #     actionsCategories[(score,highQtileLimit,lowQtileLimit,lowCateg,highCateg)].append(a)
            # except:
            #     actionsCategories[(score,highQtileLimit,lowQtileLimit,lowCateg,highCateg)] = [a]

        if Debug:
            print(actionsCategories)

        actionsCategKeys = list(actionsCategories.keys())
        actionsCategIntervals = sorted(actionsCategKeys,key=itemgetter(0,5,6,7), reverse=True)

        #if Debug:
        #    print(actionsCategIntervals)
        compSize = self.minimalComponentSize
        
        if compSize == 1:
            if Descending:
                componentsIntervals = [[(item[1],item[2]),actionsCategories[item],item[0],item[3],item[4]]\
                                   for item in actionsCategIntervals]
            else:
                componentsIntervals = [[(item[2],item[1]),actionsCategories[item],item[0],item[3],item[4]]\
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
                    lowQtileLimit = comp[2]
                highQtileLimit = comp[1]             
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
        if Debug:
            print(componentsIntervals)
        return componentsIntervals        

        # actionsCategIntervals = []
        # for interval in actionsCategories:
        #     actionsCategIntervals.append([interval,\
        #                                   actionsCategories[interval]])
        # actionsCategIntervals.sort(reverse=Descending)
        # if Debug:
        #     print(actionsCategIntervals)
        # CompSize = self.minimalComponentSize 
        # if CompSize == 1:
        #     if Descending:
        #         componentsIntervals = [[(item[0][1],item[0][2]),item[1],item[0][0],item[0][3],item[0][4]]\
        #                            for item in actionsCategIntervals]
        #     else:
        #         componentsIntervals = [[(item[0][2],item[0][1]),item[1],item[0][0],item[0][3],item[0][4]]\
        #                            for item in actionsCategIntervals]
                
        # else:
        #     componentsIntervals = []
        #     nc = len(actionsCategIntervals)
        #     compContent = []
        #     for i in range(nc):
        #         currContLength = len(compContent)
        #         comp = actionsCategIntervals[i]
        #         #print(comp)
        #         if currContLength == 0:
        #             lowQtileLimit = comp[0][2]
        #         highQtileLimit = comp[0][1]             
        #         compContent += comp[1]
        #         if len(compContent) >= CompSize or i == nc-1:
        #             score = comp[0][0]
        #             lowCateg = comp[0][3]
        #             highCateg = comp[0][4]
        #             if Descending:
        #                 componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent,\
        #                                             score,lowCateg,highCateg])
        #             else:
        #                 componentsIntervals.append([(lowQtileLimit,highQtileLimit),compContent,\
        #                                             score,lowCateg,highCateg])
        #             compContent = []
        # #if Debug:
        # #    print(componentsIntervals)
        # return componentsIntervals        

    def computeActionCategories(self,int action,
                                    bint Show=False,
                                    bint Debug=False,
                                    bint Comments=False,\
                             bint Threading=False,nbrOfCPUs=None):
        """
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
                                                   nbrOfCPUs=nbrOfCPUs)
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


    # ## @cython.locals(x=cython.int,
    # ##                i=cython.int,
    # ##                nc=cython.int,
    # ##                Descending=cython.bint,
    # ##                Threading=cython.bint,
    # ##                Debug=cython.bint,
    # ##                Comments=cython.bint)
    # def _computeQuantileOrdering(self,strategy=None,
    #                             bint Descending=True,
    #                              bint Threading=False,
    #                              nbrOfCPUs=None,
    #                             bint Debug=False,
    #                              bint Comments=False):
    #     """
    #     Renders the quantile interval of the decision actions.
        
    #     *Parameters*:
    #         * QuantilesdSortingDigraph instance
    #         * Descending: listing in *decreasing* (default) or *increasing* quantile order.
    #         * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
    #           in the uppest, the lowest or the average potential quantile.
        
    #     """
    #     cdef int x,i,nc,compSize
    #     cdef double ac
    #     if strategy == None:
    #         strategy = self.sortingParameters['strategy']
    #     actionsCategories = {}
    #     for x in self.actions:
    #         a,lowCateg,highCateg,credibility =\
    #                  self.computeActionCategories(x,Comments=Comments,Debug=False,\
    #                                            Threading=Threading,\
    #                                            nbrOfCPUs = nbrOfCPUs)
    #         lowQtileLimit = self.categories[lowCateg]['lowLimit']
    #         highQtileLimit = self.categories[highCateg]['highLimit']
    #         if strategy == "optimistic":
    #             try:
    #                 actionsCategories[(highQtileLimit,highQtileLimit,lowQtileLimit)].append(a)
    #             except:
    #                 actionsCategories[(highQtileLimit,highQtileLimit,lowQtileLimit)] = [a]
    #         elif strategy == "pessimistic":
    #             try:
    #                 actionsCategories[(lowQtileLimit,highQtileLimit,lowQtileLimit)].append(a)
    #             except:
    #                 actionsCategories[(lowQtileLimit,highQtileLimit,lowQtileLimit)] = [a]
    #         elif strategy == "average":
    #             lc = float(lowCateg)
    #             hc = float(highCateg)
    #             ac = (lc+hc)/2.0
    #             try:
    #                 actionsCategories[(ac,highQtileLimit,lowQtileLimit)].append(a)
    #             except:
    #                 actionsCategories[(ac,highQtileLimit,lowQtileLimit)] = [a]
    #         else:
    #             print('Error: startegy %s unkonwon' % strategy)
    #         #if Debug:
    #         #    print('action',a)
    #         #    print('actionsCategories',actionsCategories)
                
    #     actionsCategIntervals = []
    #     for interval in actionsCategories:
    #         actionsCategIntervals.append([interval,\
    #                                       actionsCategories[interval]])
    #     actionsCategIntervals.sort(reverse=Descending)
    #     #if Debug:
    #     #    print(actionsCategIntervals)
    #     CompSize = self.minimalComponentSize 
    #     if CompSize == 1:
    #         if Descending:
    #             componentsIntervals = [[(item[0][1],item[0][2]),item[1]]\
    #                                for item in actionsCategIntervals]
    #         else:
    #             componentsIntervals = [[(item[0][2],item[0][1]),item[1]]\
    #                                for item in actionsCategIntervals]
                
    #     else:
    #         componentsIntervals = []
    #         nc = len(actionsCategIntervals)
    #         compContent = []
    #         for i in range(nc):
    #             currContLength = len(compContent)
    #             comp = actionsCategIntervals[i]
    #             if currContLength == 0:
    #                 if Descending:
    #                     lowQtileLimit = comp[0][1]
    #                 else:
    #                     lowQtileLimit = comp[0][2]
    #             if Descending:
    #                 highQtileLimit = comp[0][2]
    #             else:
    #                 highQtileLimit = comp[0][1]
    #             compContent += comp[1]
    #             if len(compContent) >= CompSize or i == nc-1:
    #                 #if Descending:
    #                 #componentsIntervals.append([(highQtileLimit,lowQtileLimit),compContent])
    #                 #else:
    #                 compContent.sort()
    #                 componentsIntervals.append([(lowQtileLimit,highQtileLimit),compContent])
    #                 compContent = []
    #     if Debug:
    #         print(componentsIntervals)
    #     return componentsIntervals
        
    # ## @cython.locals(action=cython.int,
    # ##                Show=cython.bint,
    # ##                Debug=cython.bint,
    # ##                Comments=cython.bint)
    # def computeActionCategories(self,int action,
    #                             bint Show=False,
    #                             bint Debug=False,
    #                             bint Comments=False,\
    #                             bint Threading=False,nbrOfCPUs=None):
    #     """
    #     Renders the union of categories in which the given action is sorted positively or null into.
    #     Returns a tuple : action, lowest category key, highest category key, membership credibility !
    #     """
    #     cdef int n,Med,lowLimit=0,notHighLimit=0,credibility
    #     #qs = self.qs
    #     #qs = self
    #     Med = self.valuationdomain['med']
    #     categories = self.categories
    #     try:
    #         sorting = self.sorting
    #     except:
    #         sorting = self.computeSortingCharacteristics(action=action,Comments=Comments,\
    #                                                Threading=Threading,\
    #                                                nbrOfCPUs=nbrOfCPUs)      
    #     keys = []
    #     for c in categories.keys():
    #     #for c in self.orderedCategoryKeys():
    #         Above = False
    #         if sorting[action][c]['categoryMembership'] >= Med:
    #             Above = True
    #             if sorting[action][c]['lowLimit'] > Med:
    #                 lowLimit = sorting[action][c]['lowLimit']
    #             if sorting[action][c]['notHighLimit'] > Med:
    #                 notHighLimit = sorting[action][c]['notHighLimit']    
    #             keys.append(c)
    #             if Debug:
    #                 print(action, c, sorting[action][c])
    #         elif Above:
    #             break
    #     n = len(keys)
    #     try:
    #         credibility = min(lowLimit,notHighLimit)
    #     except:
    #         credibility = Med
    #     if n == 0:
    #         return None
    #     elif n == 1:
    #         if Show:
    #             print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
    #                                  self.categories[keys[0]]['lowLimit'],\
    #                                  self.categories[keys[0]]['highLimit'],\
    #                                  action,\
    #                                  credibility,lowLimit,notHighLimit) )
    #         return action,\
    #                 keys[0],\
    #                 keys[0],\
    #                 credibility
    #     else:
    #         if Show:
    #             print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
    #                                  self.categories[keys[0]]['lowLimit'],\
    #                                  self.categories[keys[-1]]['highLimit'],\
    #                                  action,\
    #                                  credibility,lowLimit,notHighLimit) )
    #         return action,\
    #                 keys[0],\
    #                 keys[-1],\
    #                 credibility            

    def computeCriterion2RankingCorrelation(self,criterion,
                                            bint Threading=False,\
                                    nbrOfCPUs=None,
                                    bint Debug=False,
                                    bint Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the global outranking and the marginal criterion relation.
        
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

    def computeMarginalVersusGlobalOutrankingCorrelations(self,
                                bint Sorted=True,
                                bint ValuedCorrelation=False,
                                bint Threading=False,nbrCores=None,\
                                bint Comments=False):
        """
        Method for computing correlations between each individual criterion relation with the corresponding
        global outranking relation.
        
        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of
        available cores.
        """
        cdef int i
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

    def showMarginalVersusGlobalOutrankingCorrelation(self,
                                                      bint Sorted=True,\
                                                      bint Threading=False,\
                                                      nbrOfCPUs=None,\
                                                      bint Comments=True):
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
            print('Marginal versus global outranking correlation')
            print('criterion | weight\t corr\t deter\t corr*deter')
            print('----------|------------------------------------------')
            for x in criteriaCorrelation:
                c = x[2]
                print('%9s |  %.2f \t %.3f \t %.3f \t %.3f' % (c,criteria[c]['weight'],x[0],x[1],x[0]*x[1]))

    def showActionsSortingResult(self,actionsSubset=None):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        print('Quantiles sorting result per decision action')
        if actionsSubset==None:
            for x in self.actions.keys():
                self.computeActionCategories(x,Show=True)
        else:
            for x in actionsSubset:
                self.computeActionCategories(x,Show=True)

    def showShort(self,fileName=None,bint WithFileSize=False):
        """
        Default (__repr__) presentation method for big outranking digraphs instances:
        """
        #summaryStats = self.computeDecompositionSummaryStatistics()
        from digraphs import total_size
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
            print('Nbr of thread     : %d' % self.nbrOfCPUs)
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
        actionsList = []
        for comp in self.components.values():
            #comp = self.components[ck]
            actionsList += [(x,comp['subGraph'].actions[x]['name']) for x in comp['subGraph'].actions]
        actionsList.sort()
        print('List of decision actions')
        for ax in actionsList:
            print('%s: %s' % ax)

    def showCriteria(self, bint IntegerWeights=False, bint Debug=False):
        """
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
        BigIntegerOutrankingDigraph.showDecomposition(self,direction=direction)

    def showDecomposition(self, direction='decreasing'):
        
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
            #if self.sortingParameters['LowerClosed']:
            print('%s. %s-%s : %s' % (compKey,comp['lowQtileLimit'],comp['highQtileLimit'],actions))
            #else:
            #    print('%s. %s-%s : %s' % (compKey,comp['highQtileLimit'],comp['lowQtileLimit'],actions))
                

    def showRelationTable(self, bint IntegerValues=True, compKeys=None):
        """
        Specialized for showing the quantiles decomposed relation table.
        Components are stored in an ordered dictionary.
        """
        cdef int nc
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
                    pg.showRelationTable(IntegerValues=IntegerValues)
                    
        else:
            for compKey in compKeys:
                comp = components[compkey]
                pg = comp['subGraph']
                print('Relation table of component %s' % str(compKey))
                actions = [ x for x in pg.actions.keys()]
                print('%s' % actions)
                if pg.order > 1:
                    pg.showRelationTable(IntegerValues=IntegerValues)                


    def computeBoostedRanking(self, rankingRule='Copeland'):
        """
        Renders an ordred list of decision actions ranked in
        decreasing preference direction following the net flows rule
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

    def computeBoostedOrdering(self, orderingRule='Copeland'):
        """
        Renders an ordred list of decision actions ranked in
        increasing preference direction following by default the Copeland rule
        on each component.
        """
        from linearOrders import NetFlowsOrder,KohlerOrder,CopelandOrder
        ordering = []
        components = self.components
        # self.components is an ordered dictionary in decreasing preference
        for comp in components.values():
            #comp = self.components[cki]
            pg = comp['subGraph']
            if orderingRule == 'Copeland':
                opg = CopelandOrder(pg)
                ordering += opg.copelandOrder
            elif orderingRule == 'NetFlows':
                opg = NetFlowsOrder(pg)
                ordering += opg.netFlowsOrder
            elif orderingRule == 'Kohler':
                opg = KohlerOrder(pg)
                ordering += opg.kohlerOrder
        return ordering

    def computeDeterminateness(self, bint InPercent=True):
        """
        Computes the Kendalll distance in % of self
        with the all median valued (indeterminate) digraph.

        deter = (sum_{x,y in X} abs[r(xSy) - Med])/(oder*order-1)
        """
        
        cdef int Max, Med, order, x, y, sumDeter=0
        cdef float deter
        
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']

        actions = self.actions
        relation = self.relation
        order = self.order

        for x in actions:
            for y in actions:
                if x != y:
                    sumDeter += ABS(relation(x,y) - Med)

        deter = float(sumDeter) / (order * (order-1))
        if InPercent:
            return deter/(Max-Med)*100.0
        else:
            return deter



########################################################33
