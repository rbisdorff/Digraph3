#!/usr/bin/env python3
# Python3+ implementation of digraphs
# Based on Python 2 $Revision: 1.697 $
# Copyright (C) 2006-2014  Raymond Bisdorff
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

__version__ = "Branch: 3.3 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

from digraphs import *
from perfTabs import *
from outrankingDigraphs import *
from weakOrders import *

class WeakOrder(Digraph):
    """
    Abstract class for weak orderings' specialized methods.
    """
    
    def showPreOrder(self,rankingByChoosing=None):
        """
        A show method for self.rankinByChoosing result.
        """
        if rankingByChoosing == None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                print('Error: You must first run self.computeRankingByChoosing(CoDual=True(default)|False) !')
            #rankingByChoosing = self.computeRankingByChoosing(Debug,CoDual)
                return
        else:
            rankingByChoosing = rankingByChoosing['result']
        print('Ranking by Choosing and Rejecting')
        space = ''
        n = len(rankingByChoosing)
        for i in range(n):
            if i+1 == 1:
                nstr='st'
            elif i+1 == 2:
                nstr='nd'
            elif i+1 == 3:
                nstr='rd'
            else:
                nstr='th'
            ibch = set(rankingByChoosing[i][0][1])
            iwch = set(rankingByChoosing[i][1][1])
            iach = iwch & ibch
            #print 'ibch, iwch, iach', i, ibch,iwch,iach
            ch = list(ibch)
            ch.sort()
            print(' %s%s%s ranked %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
            if len(iach) > 0 and i < n-1:
                print('  %s Ambiguous Choice %s' % (space,list(iach)))
                space += '  '
            space += '  '
        for i in range(n):
            if n-i == 1:
                nstr='st'
            elif n-i == 2:
                nstr='nd'
            elif n-i == 3:
                nstr='rd'
            else:
                nstr='th'
            space = space[:-2]
            ibch = set(rankingByChoosing[n-i-1][0][1])
            iwch = set(rankingByChoosing[n-i-1][1][1])
            iach = iwch & ibch
            #print 'ibch, iwch, iach', i, ibch,iwch,iach
            ch = list(iwch)
            ch.sort()
            if len(iach) > 0 and i > 0:
                space = space[:-2]
                print('  %s Ambiguous Choice %s' % (space,list(iach)))
            print(' %s%s%s last ranked %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))        

    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        Dummy name for showPreOrder() method
        """
        self.showPreOrder(rankingByChoosing=rankingByChoosing)        

class RankingByChoosingDigraph(WeakOrder):
    """
    Specialization of the abstract WeakOrderclass for 
    ranking-by-Rubis-choosing results.
    
    Example python3 session:
    
    >>> from outrankingDigraphs import *
    >>> t = RandomCBPerformanceTableau(numberOfActions=7,\ 
                numberOfCriteria=5,\ 
                weightDistribution='equiobjectives')
    >>> g = BipolarOutrankingDigraph(t,Normalized=True)
    >>> g.showRelationTable()
    * ---- Relation Table -----
      S   | 'a01'  'a02'  'a03'  'a04'  'a05'  'a06'  'a07'   
    ------|-------------------------------------------------
    'a01' | +0.00  +0.00  +0.67  +0.00  -0.67  -0.33  -0.17  
    'a02' | +0.00  +0.00  +1.00  +0.17  +0.00  -0.50  +0.33  
    'a03' | -0.33  -1.00  +0.00  -1.00  -0.67  -1.00  -0.33  
    'a04' | +0.00  +0.17  +1.00  +0.00  +0.00  -0.50  +0.00  
    'a05' | +0.67  +0.00  +1.00  +0.00  +0.00  -0.33  +1.00  
    'a06' | +0.67  +1.00  +1.00  +1.00  +0.33  +0.00  +0.33  
    'a07' | +0.67  +0.00  +1.00  +0.00  -0.17  -0.33  +0.00 
    >>> (~(-g)).exportGraphViz('weakOrdering')
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to converse-dual_rel_randomCBperftab.dot
    dot -Grankdir=BT -Tpng converse-dual_rel_randomCBperftab.dot 
       -o weakOrdering.png 
        
    .. image:: weakOrdering.png
        
    >>> from weakOrders import RankingByChoosingDigraph
    >>> rbc = RankingByChoosingDigraph(g)
    >>> rbc.showPreOrder()
    Ranking by Choosing and Rejecting
    1st ranked ['a06'] (0.50)
        2nd ranked ['a02', 'a04', 'a05'] (0.14)
        2nd last ranked ['a01', 'a04', 'a07'] (0.14)
    1st last ranked ['a03'] (0.72)
    >>> rbc.showRelationTable(actionsSubset =\ 
            ['a06','a02','a05','a04','a01','a07','a03'],\ 
            Sorted = False)
    * ---- Relation Table -----
      S   | 'a06'  'a02'  'a05'  'a04'	'a01'  'a07'  'a03'	  
    ------|-------------------------------------------------
    'a06' | +0.00  +1.00  +0.33	 +1.00	+0.67  +0.33  +1.00	 
    'a02' | -0.50  +0.00  +0.00  +0.00  +0.00  +0.33  +1.00	 
    'a05' | -0.33  +0.00  +0.00  +0.00  +0.67  +1.00  +1.00	 
    'a04' | -0.50  +0.00  +0.00	 +0.00	+0.00  +0.00  +1.00	 
    'a01' | -0.33  +0.00  -0.67	 +0.00	+0.00  +0.00  +0.67	 
    'a07' | -0.33  +0.00  -0.17	 +0.00	+0.00  +0.00  +1.00	 
    'a03' | -1.00  -1.00  -0.67	 -1.00	-0.33  -0.33  +0.00	 
    """
    def __init__(self,other,Best=True,
                 Last=True,
                 fusionOperator = "o-min",
                 CoDual=False,
                 Debug=False):
        from copy import deepcopy
        digraph=deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        self.actions = digraph.actions
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        if not Best and not Last:
            self.rankingByChoosing = digraph.computeRankingByChoosing(CoDual=CoDual)
            if Debug:
                digraph.showRankingByChoosing()
            self.relation = digraph.computeRankingByChoosingRelation()
        elif Best and not Last:
            digraph.computeRankingByBestChoosing(CoDual=CoDual)
            self.relation = digraph.computeRankingByBestChoosingRelation()
            if Debug:
                digraph.showRankingByBestChoosing()
        elif Last and not Best:
            digraph.computeRankingByLastChoosing(CoDual=CoDual)
            self.relation = digraph.computeRankingByLastChoosingRelation()
            if Debug:
                digraph.showRankingByLastChoosing()
        else:
            digraph.computeRankingByBestChoosing(CoDual=CoDual)
            relBest = digraph.computeRankingByBestChoosingRelation()
            if Debug:
                digraph.showRankingByBestChoosing()
            digraph.computeRankingByLastChoosing(CoDual=CoDual)
            relLast = digraph.computeRankingByLastChoosingRelation()
            if Debug:
                digraph.showRankingByLastChoosing()
            relFusion = {}
            for x in digraph.actions:
                relFusion[x] = {}
                for y in digraph.actions:
                    if fusionOperator == "o-max":
                        relFusion[x][y] = digraph.omax((relBest[x][y],relLast[x][y]))
                    elif fusionOperator == "o-min":
                        relFusion[x][y] = digraph.omin((relBest[x][y],relLast[x][y]))
                    else:
                        print('Error: invalid epistemic fusion operator %s' % operator)
                      
            self.relation=relFusion

        self.computeRankingByChoosing()
        if Debug:
            self.showRankingByChoosing()
            print(digraph.computeOrdinalCorrelation(self))
                
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class PrincipalInOutDegreesOrdering(WeakOrder):
    """
    Specialization of generic Digraph class for ranking by fusion
    of the principal orders of in- and outdegrees.
    """
    def __init__(self,other,fusionOperator="o-min",imageType=None,plotFileName=None,Debug=False):
        from copy import deepcopy
        from linearOrders import PrincipalOrder
        digraph = deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        if isinstance(digraph.actions,list):
            self.actions = {}
            for x in digraph.actions:
                self.actions[x] = {}
                self.actions[x]['name'] = x
        else:
            self.actions = deepcopy(digraph.actions)
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        pl = PrincipalOrder(digraph,Colwise=False,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        if Debug:
            print('Row wise: ')
            print(pl.principalRowwiseScores)
            pl.computeOrder()
        self.principalRowwiseScores = pl.principalRowwiseScores
        for x in pl.principalRowwiseScores:
            self.actions[x[1]]['principalRowwiseScore'] = x[0]
        pc = PrincipalOrder(digraph,Colwise=True,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        if Debug:
            print('Column wise: ')
            print(pc.principalColwiseScores)
            pc.computeOrder()
        self.principalColwiseScores = pc.principalColwiseScores
        for x in pc.principalColwiseScores:
            self.actions[x[1]]['principalColwiseScore'] = x[0]
        pf = FusionDigraph(pl,pc,operator=fusionOperator)
        self.relation = deepcopy(pf.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.computeRankingByChoosing()
        if Debug:
            print(self.computeOrdinalCorrelation(digraph))

    def showPrincipalScores(self, ColwiseOrder=False, RowwiseOrder=False):
        """
        show the princiapl scores
        """
        print('List of principal scores')
        if not ColwiseOrder and not RowwiseOrder:
            print('action \t colwise \t rowwise')
            for x in self.actions:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
        elif ColwiseOrder:
            print('Column wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalColwiseScores:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
        else:
            print('Row wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalRowwiseScores:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
                

#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from digraphs import *
    from outrankingDigraphs import *
    from weakOrders import *

    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                   numberOfActions=15)
    #t.saveXMCDA2('test')
    #t = XMCDA2PerformanceTableau('test')
    #g = BipolarOutrankingDigraph(t,Normalized=True)
    #g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=11)
    g = RandomValuationDigraph(order=11)
    print('=== >>> best and last fusion (default)')
    rcg0 = RankingByChoosingDigraph(g,fusionOperator="o-min",Debug=False)
    rcg0.showPreOrder()
    print(rcg0.computeOrdinalCorrelation(g))
    rcg0 = RankingByChoosingDigraph(g,fusionOperator="o-max",Debug=False)
    rcg0.showPreOrder()
    print(rcg0.computeOrdinalCorrelation(g))
##    rcg.showRankingByChoosing()
##    rcg1 = RankingByChoosingDigraph(rcg,CoDual=True)
##    rcg1.showRankingByChoosing()
##    print(rcg1.computeOrdinalCorrelation(rcg))
##    print('=== >>> best') 
##    rcg1 = RankingByChoosingDigraph(g,Best=True,Last=False,Debug=False)
##    rcg1.showPreOrder()
##    print(rcg1.computeOrdinalCorrelation(g))
##    print('=== >>> last')
##    rcg2 = RankingByChoosingDigraph(g,Best=False,Last=True,Debug=False)
##    rcg2.showPreOrder()
##    print(rcg2.computeOrdinalCorrelation(g))
##    print('=== >>> bipolar best and last')
##    rcg3 = RankingByChoosingDigraph(g,Best=False,Last=False,Debug=False)
##    rcg3.showPreOrder()
##    print(rcg3.computeOrdinalCorrelation(g))
##    print('=== >>> principal preorder')
    rcf1 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
                                        imageType=None,Debug=False)
    rcf1.showPreOrder()
    print(rcf1.computeOrdinalCorrelation(g))
    rcf2 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-max",
                                        imageType=None,Debug=False)
    rcf2.showPreOrder()
    print(rcf2.computeOrdinalCorrelation(g))
    #rcf.showPrincipalScores()
    rcf1.showPrincipalScores(ColwiseOrder=True)
    rcf1.showPrincipalScores(RowwiseOrder=True)

    
    
