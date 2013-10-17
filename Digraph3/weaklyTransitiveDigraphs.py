#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python3+ implementation of digraphs
# Based on Python 2 $Revision: 1.697 $
# Copyright (C) 2006-2013  Raymond Bisdorff
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
from weaklyTransitiveDigraphs import *

class WeaklyTransitiveDigraph(Digraph):
    """
    Abstract class for weakly transitive digraphs specialized methods.
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


class RankingByChoosingDigraph(WeaklyTransitiveDigraph):
    """
    Specialization of generic Digraph class for ranking by choosing results.
    """
    def __init__(self,other,Best=True,
                 Last=True,CoDual=False,
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
                    relFusion[x][y] = digraph.omin((relBest[x][y],relLast[x][y]))
            self.relation=relFusion

        self.computeRankingByChoosing()
        if Debug:
            self.showRankingByChoosing()
            print(digraph.computeOrdinalCorrelation(self))
                
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class PrincipalInOutDegreesOrdering(WeaklyTransitiveDigraph):
    """
    Specialization of generic Digraph class for ranking by fusion
    of the principal orders of in- and outdegrees.
    """
    def __init__(self,other,imageType=None,plotFileName=None,Debug=False):
        from copy import deepcopy
        from linearOrders import PrincipalOrder
        digraph = deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        self.actions = digraph.actions
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        pl = PrincipalOrder(digraph,Colwise=False,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        pc = PrincipalOrder(digraph,Colwise=True,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        pf = FusionDigraph(pl,pc)
        self.relation = deepcopy(pf.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.computeRankingByChoosing(CoDual=False)
        if Debug:
            print(self.computeOrdinalCorrelation(digraph))

        

#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from outrankingDigraphs import *
    from weaklyTransitiveDigraphs import *

    g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=15)
    print('=== >>> best and last fusion (default)')
    rcg0 = RankingByChoosingDigraph(g,Debug=False)
    rcg0.showPreOrder()
    print(rcg0.computeOrdinalCorrelation(g))
##    rcg.showRankingByChoosing()
##    rcg1 = RankingByChoosingDigraph(rcg,CoDual=True)
##    rcg1.showRankingByChoosing()
##    print(rcg1.computeOrdinalCorrelation(rcg))
    print('=== >>> best') 
    rcg1 = RankingByChoosingDigraph(g,Best=True,Last=False,Debug=False)
    rcg1.showPreOrder()
    print(rcg1.computeOrdinalCorrelation(g))
    print('=== >>> last')
    rcg2 = RankingByChoosingDigraph(g,Best=False,Last=True,Debug=False)
    rcg2.showPreOrder()
    print(rcg2.computeOrdinalCorrelation(g))
    print('=== >>> bipolar best and last')
    rcg3 = RankingByChoosingDigraph(g,Best=False,Last=False,Debug=False)
    rcg3.showPreOrder()
    print(rcg3.computeOrdinalCorrelation(g))
    print('=== >>> principal preorder')
    rcf = PrincipalInOutDegreesOrdering(g,imageType="pdf",Debug=False)
    rcf.showPreOrder()
    print(rcf.computeOrdinalCorrelation(g))

    
    
