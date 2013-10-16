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
from rankingByChoosingDigraphs import *

class RankingByChoosingDigraph(Digraph):
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
        self.__class__ = digraph.__class__
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


#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from outrankingDigraphs import *
    from rankingByChoosingDigraphs import RankingByChoosingDigraph

    g = RandomBipolarOutrankingDigraph(numberOfActions=7)
    print('=== >>> best and last fusion (default)')
    rcg0 = RankingByChoosingDigraph(g,Debug=True)
##    rcg.showRankingByChoosing()
##    rcg1 = RankingByChoosingDigraph(rcg,CoDual=True)
##    rcg1.showRankingByChoosing()
##    print(rcg1.computeOrdinalCorrelation(rcg))
    print('=== >>> best') 
    rcg1 = RankingByChoosingDigraph(g,Best=True,Last=False,Debug=True)
    print('=== >>> last')
    rcg2 = RankingByChoosingDigraph(g,Best=False,Last=True,Debug=True)
    print('=== >>> bipolar best and last')
    rcg3 = RankingByChoosingDigraph(g,Best=False,Last=False,Debug=True)

    
    
