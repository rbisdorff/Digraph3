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

import cython

from cOutrankingDigraphs import *
from cSortingDigraphs import *
from time import time
from decimal import Decimal
from cBigOutrankingDigraphs import *

class BigDigraph(object):
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
        print('Total time        : %.5f' % self.runTimes['totalTime'])
        print('QuantilesSorting  : %.5f' % self.runTimes['sorting'])
        print('Preordering       : %.5f' % self.runTimes['preordering'])
        print('Decomposing       : %.5f' % self.runTimes['decomposing'])
        try:
            print('Ordering          : %.5f' % self.runTimes['ordering'])
        except:
            pass
        return '%s instance' % str(self.__class__)
    
    @cython.locals(x=cython.int,y=cython.int)
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
    
    @cython.locals(x=cython.int)
    def showRelationMap(self,fromIndex=None,toIndex=None,symbols=None):
        """
        Prints on the console, in text map format, the location of
        the diagonal outranking components of the big outranking digraph.

        By default, symbols = {'max':'┬','positive': '+', 'median': ' ',
                               'negative': '-', 'min': '┴'}

        The default ordering of the output is following the quantiles sorted boosted net flows ranking rule
        from best to worst actions. Further available ranking rules are Kohler's (rankingRule="kohler")
        and Tideman's ranked pairs rule (rankingRule="rankedPairs").
        
        Example::

            >>> from bigOutrankingDigraphs import *
            >>> t = RandomCBPerformanceTableau(numberOfActions=50,seed=1)
            >>> bg = BigOutrankingDigraphMP(t,quantiles=10,minimalComponentSize=5)
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
            <class 'bigOutrankingDigraphs.BigOutrankingDigraphMP'> instance         
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
        if fromIndex == None:
            fromIndex = 0
        if toIndex == None:
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

        
    @cython.locals(x=cython.int,y=cython.int)
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
                            self.components[ck]['subGraph'].actions)\
                           for ck in self.components)

        if issubclass(other.__class__,(Digraph)):
            otherActionsList = [( 'c01', other.actions)]
        else:
            otherActionsList = ((ck,
                                 other.components[ck]['subGraph'].actions)\
                           for ck in other.components)
        #if Debug:
        #    print(selfActionsList)
        #    print(otherActionsList)
        
        correlation = Decimal('0.0')
        determination = Decimal('0.0')

        for ckx in selfActionsList:
            for x in ckx[1]:
                for cky in otherActionsList:
                    for y in cky[1]:
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

    @cython.locals(x=cython.int)
    def ranking2Preorder(self,ranking):
        """
        Renders a preordering (a list of list) of a ranking (best to worst) of decision actions in increasing preference direction.
        """
        #ordering = list(ranking)
        #ordering.reverse()
        preordering = [[x] for x in reversed(ranking)]
        return preordering

    @cython.locals(x=cython.int)
    def ordering2Preorder(self,ordering):
        """
        Renders a preordering (a list of list) of a linar order (worst to best) of decision actions in increasing preference direction.
        """
        preordering = [[x] for x in ordering]
        return preordering

    @cython.locals(fillRate=cython.double)
    def computeFillRate(self):
        """
        Renders the sum of the squares (without diagonal) of the orders of the component's subgraphs
        over the square (without diagonal) of the big digraph order. 
        """
        fillRate = sum((comp['subGraph'].order*comp['subGraph'].order-1)\
                        for comp in self.components.values())
        return fillRate/( self.order*(self.order-1) )

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

#from weakOrders import QuantilesRankingDigraph
class BigOutrankingDigraph(BigDigraph,PerformanceTableau):
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
    
    @cython.locals(x=cython.int,
                   quantiles=cython.int,
                   na=cython.int,
                   dimension=cython.int,
                   nc=cython.int,
                   nd=cython.int,
                   LowerClosed=cython.bint,
                   minimalComponentSize=cython.int,
                   Threading=cython.bint,
                   CopyPerfTan=cython.bint,
                   Comments=cython.bint,
                   Debug=cython.bint,
                   ttot=cython.double,
                   t0=cython.double,
                   tw=cython.double,
                   tdump=cython.double,
                   fillRate=cython.double,
                   maximalComponentSize=cython.int,
                   #nbrOfCPUs=cython.int,
                   #nbrOfThreads=cython.int,
                   #quantilesOrderingStrategy=cython.p_char,
                   #componentRankingRule=cython.p_char
                   )
    def __init__(self,argPerfTab,\
                 quantiles=0,\
                 quantilesOrderingStrategy="average",\
                 LowerClosed=True,\
                 componentRankingRule="Copeland",\
                 minimalComponentSize=1,\
                 Threading=False,\
                 tempDir=None,\
                 #componentThreadingThreshold=50,\
                 nbrOfCPUs=None,\
                 nbrOfThreads=None,\
                 save2File=None,\
                 CopyPerfTab=True,\
                 Comments=False,\
                 Debug=False):
        
        from digraphs import Digraph
        from cSortingDigraphs import QuantilesSortingDigraph
        from collections import OrderedDict
        from time import time
        from os import cpu_count
        from multiprocessing import Pool
        from copy import copy, deepcopy

        if cython.compiled:
            print('Cythonized BigOutrankingDigraph class')
        else:
            print('Pure Python BigOutrankingDigraph class')
   
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
        qs = QuantilesSortingDigraph(argPerfTab=perfTab,\
                                     limitingQuantiles=quantiles,\
                                     LowerClosed=LowerClosed,\
                                     CompleteOutranking=False,\
                                     StoreSorting=True,\
                                     WithSortingRelation=False,\
                                     CopyPerfTab=CopyPerfTab,\
                                     Threading= self.sortingParameters['Threading'],\
                                     tempDir=tempDir,\
                                     nbrCores=nbrOfCPUs,\
                                     nbrOfProcesses=nbrOfThreads,\
                                     Comments=Comments,\
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
        nd = len(str(nc))
        self.nd = nd
        if not self.sortingParameters['Threading']:
            components = OrderedDict()
            for i in range(1,nc+1):
                comp = decomposition[i-1]
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
        else:   # if self.sortingParameters['Threading'] == True:
            from copy import copy, deepcopy
            from pickle import dumps, loads, load, dump
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
                    self.lTest = lTest
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    from copy import deepcopy
                    from perfTabs import PartialPerformanceTableau
                    from cOutrankingDigraphs import BipolarOutrankingDigraph
                    chdir(self.workingDirectory)
                    if self.Debug:
                        print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadID)))
                        print('lTest',self.lTest)
                    fi = open('dumpPerfTab.py','rb')
                    perfTab = loads(fi.read())
                    fi.close()
                    fi = open('dumpDecomp.py','rb')
                    decomposition = loads(fi.read())
                    fi.close()
                    nc = len(decomposition)
                    nd = len(str(nc))
                    for i in self.lTest:
                        comp = decomposition[i]
                        if self.Debug:
                            print(i, comp)
                        compKey = ('c%%0%dd' % (nd)) % (i+1)
                        compDict = {compKey: {}}
                        compDict = {'rank':i}
                        pt = PartialPerformanceTableau(perfTab,actionsSubset=comp[1])
                        compDict['lowQtileLimit'] = comp[0][1]
                        compDict['highQtileLimit'] = comp[0][0]
                        compDict['subGraph'] = BipolarOutrankingDigraph(pt,
                                                                        Normalized=True,
                                                                        WithConcordanceRelation=False,
                                                                        WithVetoCounts=False,
                                                                        CopyPerfTab=False)     
                        compDict['subGraph'].__dict__.pop('criteria')
                        compDict['subGraph'].__dict__.pop('evaluation')
                        compDict['subGraph'].__class__ = Digraph
                        splitComponent = (compKey,compDict)
                        if self.Debug:
                            print(compDict)
                        foName = 'splitComponent-'+str(i)+'.py'
                        fo = open(foName,'wb')
                        fo.write(dumps(splitComponent,-1))
                        fo.close()
                    
            if Comments:
                print('Processing the %d components' % nc )
                print('Threading ...')
            tdump = time()
            from tempfile import TemporaryDirectory,mkdtemp
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                #use this below dedented if the tempory directory should not be deleted
                #tempDirName = mkdtemp(dir=tempDir)
                selfFileName = tempDirName +'/dumpPerfTab.py'
                if Debug:
                    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                dump(perfTab,fo,-1)
                fo.close()
                if Comments:
                    print('dumping perfTab: %.5f' % (time() - tdump))
                selfFileName = tempDirName +'/dumpDecomp.py'
                if Debug:
                    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                pd = dumps(decomposition,-1)
                fo.write(pd)
                fo.close()
                if Comments:
                    print('dumping time: %.5f' % (time() - tdump))

                if nbrOfCPUs == None:
                    nbrOfCPUs = cpu_count()
                if nbrOfThreads == None:
                    nbrOfThreads = nbrOfCPUs-1
                nbrOfLocals = self.order//nbrOfThreads
                if nbrOfLocals*nbrOfThreads < self.order:
                    nbrOfLocals += 1
                if Comments:
                    print('Nbr of components',nc)            
                    print('Nbr of threads = ',nbrOfThreads)
                    print('Nbr of locals/job',nbrOfLocals)
                nbrOfThreadsUsed = 0
                i = 0
                for j in range(nbrOfThreads):
                    if Comments:
                        print('thread = %d/%d' % (j+1,nbrOfThreads),end="...")
                    lTest = []
                    threadLoad = 0
                    while threadLoad <= nbrOfLocals and i < (nc):
                        lTest.append(i)
                        threadLoad += len(decomposition[i][1])
                        i += 1
                    #for i in range(start,stop):
                    #    if len(decomposition[i][1]) < componentThreadingThreshold:
                    #        lTest.append(i)
                    #    else:
                    #        bigPartialGraphs.append(i)
                    if Comments:
                        print('Threaded:',[len(decomposition[i][1]) for i in lTest])
                        #print('Kept    :',[len(decomposition[i][1]) for i in bigPartialGraphs])
                    if lTest != []:
                        process = myThread(j,tempDirName,lTest,Debug)
                        process.start()
                        nbrOfThreadsUsed += 1
                #nbg = len(bigPartialGraphs)
                while active_children() != []:
                    pass
                if Comments:
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
        self.fillRate = fillRate / (na*(na-1))
        self.maximalComponentSize = maximalComponentSize
        self.components = components

        # setting the component relation
        self.valuationdomain = {'min':Decimal('-1'),
                                'med':Decimal('0'),
                                'max':Decimal('1')}
       
        self.runTimes['decomposing'] = time() - t0
        if Comments:
            print('decomposing time: %.4f' % self.runTimes['decomposing']  )
        # Kohler ranking-by-choosing all components
        self.componentRankingRule = componentRankingRule
        t0 = time()
        self.boostedRanking = self.computeBoostedRanking(rankingRule=componentRankingRule)
        self.boostedOrder = list(reversed(self.boostedRanking))
        self.runTimes['ordering'] = time() - t0

        if Comments:
            print('ordering time: %.4f' % self.runTimes['ordering']  )
        
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)
        if save2File != None:
            self.showShort(fileName=save2File)
            

    # ----- class methods ------------


    @cython.locals(x=cython.int,
                   i=cython.int,
                   nc=cython.int,
                   Descending=cython.bint,
                   Threading=cython.bint,
                   Debug=cython.bint,
                   Comments=cython.bint)
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
        for x in self.actions:
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
                    lowQtileLimit = comp[0][1]
                highQtileLimit = comp[0][2]
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
        
        
    @cython.locals(action=cython.int,
                   Show=cython.bint,
                   Debug=cython.bint,
                   Comments=cython.bint)
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
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,Comments=Comments,\
                                                   Threading=Threading,\
                                                   nbrOfCPUs=nbrOfCPUs)      
        keys = []
        for c in categories.keys():
        #for c in self.orderedCategoryKeys():
            Above = False
            if sorting[action][c]['categoryMembership'] >= Med:
                Above = True
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']    
                keys.append(c)
                if Debug:
                    print(action, c, sorting[action][c])
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

    def computeCriterion2RankingCorrelation(self,criterion,Threading=False,\
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
        globalOrdering = self.ranking2Preorder(self.boostedRanking)
        globalRelation = gc.computePreorderRelation(globalOrdering)
        corr = gc.computeOrdinalCorrelation(globalRelation)
        if Debug:
            print(corr)
        return corr

    def computeMarginalVersusGlobalOutrankingCorrelations(self,Sorted=True,ValuedCorrelation=False,
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

    def showMarginalVersusGlobalOutrankingCorrelation(self,Sorted=True,\
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

    def showShort(self,fileName=None,WithFileSize=True):
        """
        Default (__repr__) presentation method for big outranking digraphs instances:
        
        >>> from bigOutrankingDigraphs import *
        >>> t = RandomCBPerformanceTableau(numberOfActions=100,seed=1)
        >>> g = BigOutrankingDigraphMP(t,quantiles=10)
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
        <class 'bigOutrankingDigraphs.BigOutrankingDigraphMP'> instance        
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
        for comp in self.components.values:
            #comp = self.components[ck]
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

    def showComponents(self,direction='increasing'):
        BigOutrankingDigraph.showDecomposition(self,direction=direction)

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

    def computeBoostedOrdering(self,orderingRule='Copeland'):
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

#----------test classes and methods ----------------
if __name__ == "__main__":
    
    from time import time
    from weakOrders import QuantilesRankingDigraph
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    MP  = False
    nbrActions=1000
##    t0 = time()
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,seed=100,BigData=True)

##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,Threading=MP,seed=100)

    bg1 = BigOutrankingDigraph(tp,CopyPerfTab=True,quantiles=50,
                                 quantilesOrderingStrategy='average',
                                 componentRankingRule='NetFlows',
                                 LowerClosed=True,
                                 minimalComponentSize=10,
                                 Threading=MP,nbrOfCPUs=8,
                                 #tempDir='.',
                                 nbrOfThreads=8,
                                 Comments=False,Debug=False,
                                 save2File='testbgMP')
    print(bg1)
    

