#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python implementation of linear orders
# Dependancy: digraphs 1.589+
# Current revision $Revision: 1.18 $
# Copyright (C) 2011  Raymond Bisdorff
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

__version__ = "$Revision: 1.18 $"
# $Source: /home/cvsroot/Digraph/linearOrders.py,v $

from digraphs import *
from linearOrders import *

#--------- Decimal precision --------------
from decimal import Decimal

#---------- general methods -----------------
# generate all permutations from a string or a list
# From Michael Davies's recipe:
# http://snippets.dzone.com/posts/show/753
## def all_perms(str):
##     if len(str) <=1:
##         yield str
##     else:
##         for perm in all_perms(str[1:]):
##             for i in range(len(perm)+1):
##                 yield perm[:i] + str[0:1] + perm[i:]

#--------- Partial Extended Prudent Digraph class ---------

class ExtendedPrudentDigraph(Digraph):
    """
    Instantiates the associated extended prudent
    codual of the digraph enstance.
    Instantiates as other.__class__ !
    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other,prudentBetaLevel=None,CoDual=False,Debug=False):
        from copy import copy as deepcopy
        self.__class__ = other.__class__
        self.name = 'extprud-'+other.name
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = deepcopy(other.evaluation)
        except AttributeError:
            pass

        if CoDual:
            gcd = CoDualDigraph(other)
        else:
            gcd = other
        if prudentBetaLevel == None:
            level = gcd.computePrudentBetaLevel(Debug=Debug)
        else:
            level = prudentBetaLevel
        gp = PolarisedDigraph(gcd, level=level, StrictCut=False)
        if Debug:
            gp.showRelationTable()
        gcdst = StrongComponentsCollapsedDigraph(gcd)
        if Debug:
            gcdst.showRelationTable()
            gcdst.exportGraphViz('debugSCC')
        stRelation = {}
        for x in other.actions:
            stRelation[x] = {}
            for y in other.actions:
                stRelation[x][y] = gp.valuationdomain['med']
        for cx in gcdst.actions:
            for x in cx:
                for cy in [z for z in gcdst.actions if z != cx]:
                    for y in cy:
                        if Debug:
                            print('cx, x,cy, y', cx,x,cy, y, gcdst.relation[cx][cy])
                        stRelation[x][y] = gcdst.relation[cx][cy]
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(gp.valuationdomain)
        actionsList = list(self.actions)
        #Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        #Min = self.valuationdomain['min']
        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                if Debug:
                    print('omax([gp.relation[x][y],stRelation[x][y]])',x,y,[gp.relation[x][y],stRelation[x][y]])
                relation[x][y] = self.omax([gp.relation[x][y],stRelation[x][y]])    
                ## if gp.relation[y][x] >= Med and stRelation[x][y] >= Med:
                ##     relation[x][y] = max(gp.relation[y][x],stRelation[x][y])
                ## elif gp.relation[y][x] <= Med and stRelation[x][y] <= Med:
                ##     relation[x][y] = min(gp.relation[y][x],stRelation[x][y])
                ## else:
                ##     relation[x][y] = Med
                ## if self.omax([gp.relation[y][x],stRelation[x][y]]) != relation[x][y]:
                ##     print 'Error!!!'
        self.relation = relation
        if Debug:
            self.showRelationTable()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    

# ------- Abstract Linear Order class

class LinearOrder(Digraph):
    """
    abstract class for digraphs which represent
    linear orders.
    """
    def computeOrder(self):
        """
        shows the linear order of an instance of the LinearOrcer class
        """
        degrees = []
        for x in [z for z in self.actions]:
            degrees.append((len(self.gamma[x][0]),x))
        degrees.sort(reverse=True)
        rankedPairsOrder = []
        for x in degrees:
            rankedPairsOrder.append(x[1])
        return rankedPairsOrder

    def htmlOrder(self):
        """
        returns the html encoded presentation of a linear order
        """
        linearOrder = self.computeOrder()
        html = ''
        html += '<table border = 1>'
        html += '<tr bgcolor="#9acd32"><th colspan="2">Ranking result</th></tr>'
        for x in linearOrder:
            try:
                name = self.actions[x]['name']
            except:
                name = x
            html += '<tr><th bgcolor="#FFF79B">%s</th><td>%s</td></tr>' % (x,name)
        html += '</table>'
        return html
    
    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),noSilent=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName, bestChoice=bestChoice,worstChoice=worstChoice,noSilent=noSilent,graphType=graphType,graphSize=graphSize)

    def exportGraphViz(self,fileName=None, isValued=True, bestChoice=set(),worstChoice=set(),noSilent=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file  for linear order drawing filtering.
        """
        import os
        if noSilent:
            print('*---- exporting a dot file dor GraphViz tools ---------*')
        #actionkeys = [x for x in self.actions]
        actionkeys = self.computeOrder()
        n = len(actionkeys)
        relation = self.relation
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if noSilent:
            print('Exporting to '+dotName)
        if bestChoice != set():
            rankBestString = '{rank=max; '
        if worstChoice != set():
            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\ndigraphs module (graphviz), R. Bisdorff, 2011", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            nodeName = str(actionkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            node += '];\n'         
            fo.write(node)
        for i in range(n-1):
            for j in range(i+1,i+2):
                #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                if isValued:
                    if self.relation[actionkeys[i]][actionkeys[i+1]] < Decimal('2'):
                        arcColor = 'grey'
                    else:
                        arcColor = 'black'
                else:
                    arcColor = 'black'
                edge = 'n%s-> n%s [dir=forward,style="setlinewidth(%d)",color=%s, arrowhead=normal] ;\n' % (i+1,i+2,self.relation[actionkeys[i]][actionkeys[i+1]],arcColor)
                
                fo.write(edge)
                     
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        fo.write('}\n')
        fo.close()
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')
    
    def computeKemenyIndex(self, other):
        """
        renders the Kemeny index of the self.relation (linear order)
        compared with a given bipolar-valued relation of a compatible
        other digraph (same nodes or actions).
        """
        try:
            from math import copysign
            CopySign = True
        except:
            CopySign = False
        KemenyIndex = 0.0
        actions = [x for x in self.actions]
        for x in actions:
            for y in actions:
                if x != y:
                    if CopySign:
                        KemenyIndex += float(other.relation[x][y])*copysign(1.0,self.relation[x][y])
                    else:
                        if self.relation[x][y] > 0:
                            KemenyIndex += float(other.relation[x][y])
                        elif self.relation[x][y] < 0:
                            KemenyIndex -= float(other.relation[x][y])
        return KemenyIndex 
            

######   instantiable class of linear orders

# ------- Random linear orders

class RandomLinearOrder(LinearOrder):
    """
    Instantiates random linear orders
    """
    def __init__(self,numberOfActions=10,Debug=False,OutrankingModel=False):
        """
        constructor for generating random instances of linear orders with a given number of actions (default=10).
        """
        from copy import copy as deepcopy
        from outrankingDigraphs import RandomOutrankingDigraph
        import random
        if OutrankingModel:
            g = RandomOutrankingDigraph(numberOfActions=numberOfActions)
        else:
            g = RandomDigraph(order=numberOfActions)
        g.recodeValuation(-1,1)
        actionsList = [x for x in g.actions]
        random.shuffle(actionsList)
        if Debug:
            print(g.actions, actionsList)
        self.name = 'randomLinearOrder'
        self.actions = deepcopy(g.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(g.valuationdomain)
        self.relation = deepcopy(g.relation)
        for i in range(self.order):
            x = actionsList[i]
            self.relation[x][x] = self.valuationdomain['med']
            for j in range(i+1,self.order):
                y = actionsList[j]
                self.relation[x][y] = self.valuationdomain['max']
                self.relation[y][x] = self.valuationdomain['min']
        self.gamma = self.gammaSets()
        self.notgamma = self.notGammaSets()
        if Debug:
            print(self.computeOrder())

        
######   instantiable class of linear orders
class RankedPairsOrder(LinearOrder):
    """
    instantiates the Extended Prudent Ranked Pairs Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False, Cpp=False, isValued=False,isExtendedPrudent=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the ranked pairs (Lexmin Dias-Lamboray) rule
        Parameter: isExtendedPrudent 
        """
        from copy import copy as deepcopy
        # construct ranked pairs

        if coDual:
            other = CoDualDigraph(other)
        if Debug:
            other.showRelationTable()
            
        relation = other.relation
        actions = [x for x in other.actions]
        actions.sort()
        n = len(actions)
        
        listPairs = []
        for x in actions:
            for y in [z for z in actions if z != x]:
                listPairs.append((-relation[x][y],(x,y),x,y))
        listPairs.sort(reverse=False)
        if Debug:
            print(listPairs)
        
        # instatiates a Digraph template
        if isExtendedPrudent:
            prudentBetaLevel = other.computePrudentBetaLevel(Debug=Debug)
            if prudentBetaLevel > other.valuationdomain['med']:
                if Debug:
                    print('Is extended prudent with level: %.2f !' % prudentBetaLevel)
                g = ExtendedPrudentDigraph(other,\
                 prudentBetaLevel=prudentBetaLevel,\
                 CoDual=coDual,Debug=Debug)
                g.recodeValuation(-3,3)
                Min = g.valuationdomain['min']
                Max = g.valuationdomain['max']
                Med = g.valuationdomain['med']
                for x in g.actions:
                    for y in g.actions:
                        if x != y:
                            if g.relation[x][y] > Med:
                                g.relation[x][y] = Max
                            elif g.relation[x][y] < Med:
                                g.relation[x][y] = Min
                            else:
                                g.relation[x][y] = Med
            else:
                g = IndeterminateDigraph(order=n)
                g.actions = actions
                if isValued:
                    g.valuationdomain = {'min':Decimal('-3'),\
                                         'med': Decimal('0'),\
                                         'max': Decimal('3')}
                else:
                    g.valuationdomain = {'min':Decimal('-1'),\
                                         'med': Decimal('0'),\
                                         'max': Decimal('1')}

                Min = g.valuationdomain['min']
                Max = g.valuationdomain['max']
                Med = g.valuationdomain['med']
                g.relation = {}
                for x in g.actions:
                    g.relation[x] = {}
                    for y in g.actions:
                        g.relation[x][y] = Med
                
        else:
            g = IndeterminateDigraph(order=n)
            g.actions = actions
            if isValued:
                g.valuationdomain = {'min':Decimal('-3'),\
                                     'med': Decimal('0'),\
                                     'max': Decimal('3')}
            else:
                g.valuationdomain = {'min':Decimal('-1'),\
                                     'med': Decimal('0'),\
                                     'max': Decimal('1')}
               
            Min = g.valuationdomain['min']
            Max = g.valuationdomain['max']
            Med = g.valuationdomain['med']
            g.relation = {}
            for x in g.actions:
                g.relation[x] = {}
                for y in g.actions:
                    g.relation[x][y] = Med

        if Debug:
            print('Starting the ranked pairs rule with the following partial order:')
            g.showRelationTable()
        for pair in listPairs:
            x = pair[2]
            y = pair[3]
            if g.relation[x][y] <= Med and g.relation[y][x] <= Med:
                if Debug:
                    print('next pair: ', pair[1],relation[x][y])
                relxy = g.relation[x][y]
                if isValued and relation[x][y] > Med:
                    g.relation[x][y] = Decimal('2')
                else:
                    g.relation[x][y] = Decimal('1')                    
                relyx = g.relation[y][x]
                if isValued and relation[y][x] < Med:
                    g.relation[y][x] = -Decimal('2')
                else:
                    g.relation[y][x] = -Decimal('1')
        
                g.gamma = g.gammaSets()
                g.notGamma = g.notGammaSets()
                Detected = False
                if Cpp:
                    Detected = g.detectCppChordlessCircuits()
                else:
                    Detected = g.detectChordlessCircuits()
                if Detected:
                    if Debug:
                        print('Circuit detected !!')
                    g.relation[x][y] = relxy
                    g.relation[y][x] = relyx         
                else:
                    if Debug:
                        print('added: (%s,%s) characteristic: %.2f (%.1f)' % (x,y, other.relation[x][y],g.relation[x][y]))
                        print('added: (%s,%s) characteristic: %.2f (%.1f)' % (y,x, other.relation[y][x],g.relation[y][x]))
                
        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(g.valuationdomain)
        self.relation = deepcopy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            print('Ranked Pairs Order = ', self.computeOrder())

    
class KohlerOrder(LinearOrder):
    """
    instantiates the Kohler Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Kohler rule 
        """
        from copy import copy as deepcopy
        # construct ranked pairs
        if coDual:
            otherCoDual = CoDualDigraph(other)
            relation = otherCoDual.relation
            Max = otherCoDual.valuationdomain['max']
            if Debug:
                otherCoDual.showRelationTable()
                print(otherCoDual.valuationdomain)
        else:
            relation = other.relation
            Max = other.valuationdomain['max']
            if Debug:
                other.showRelationTable()
                print(other.valuationdomain)
                
            
        actions = [x for x in other.actions]
        actions.sort()
        n = len(actions)
        
        # instatiates a Digraph template
        g = IndeterminateDigraph(order=n)
        g.actions = actions
        g.valuationdomain = {'min':Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
        g.relation = {}
        for x in g.actions:
            g.relation[x] = {}
            for y in g.actions:
                g.relation[x][y] = g.valuationdomain['med']


        actionsList = [x for x in g.actions]

        rank = {}
        k = 1
        while actionsList != []:
            maximin = []
            for x in actionsList:
                xmin = Max
                for y in actionsList:
                    if x != y:
                        if relation[x][y] < xmin:
                            xmin = relation[x][y]
                if Debug:
                    print('x, xmin', x, xmin)
                maximin.append((xmin,x))
            maximin.sort()
            if Debug:
                print(maximin, maximin[-1][1])
            rank[maximin[-1][1]] = {'rank':k,'majorityMargin':maximin[-1][0]}
            actionsList.remove(maximin[-1][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)

        kohlerOrder = []
        for x in rank:
            kohlerOrder.append((rank[x]['rank'],x))
        kohlerOrder.sort()
        if Debug:
            print('Kohler ranks: ', kohlerOrder)

        n = len(g.actions)
        for i in range(n):
            for j in range(i+1,n):
                x = kohlerOrder[i][1]
                y = kohlerOrder[j][1]
                g.relation[x][y] = g.valuationdomain['max']
                g.relation[y][x] = g.valuationdomain['min']

            
        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(g.valuationdomain)
        self.relation = deepcopy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            self.showRelationTable()
            print('Kohler order: ', self.computeOrder())

from sortingDigraphs import QuantilesSortingDigraph                                              
class BoostedKohlerOrder(KohlerOrder,QuantilesSortingDigraph):
    """
    Boosting the Kohler ranking-by-choosing rule
    with previous quantiles sorting-

    *Main parameters*:
          * limitingQuantiles are set by default to len(actions)//2
            for outranking digraph orders below 200.
            For higher orders, centiles are used by default.
          * strategies are: "optimistic" (default), "pessimistic" or "average"
          * Threading is on (True) by default for CPUs with more than 2 cores.

    .. warning::
    
          For larger orders a consistent size of several
          Giga bytes cpu memory is required!
          
    """

    def __init__(self,
                 argPerfTab=None,
                 limitingQuantiles=None,
                 LowerClosed=True,
                 strategy="optimistic",
                 PrefThresholds=False,
                 hasNoVeto=False,
                 outrankingType = "bipolar",
                 Threading=False,
                 nbrCores=None,
                 chunkSize=1,
                 Comments=True,
                 Debug=False):
        
        from copy import copy as deepcopy
        from multiprocessing import cpu_count
        from outrankingDigraphs import BipolarOutrankingDigraph
        from sortingDigraphs import QuantilesSortingDigraph
        from time import time

        ttot = time()

        # import the performance tableau
        if argPerfTab == None:
            print('Error: you must provide a valid PerformanceTableau object !!')
        else:
            perfTab = argPerfTab

        # quantiles sorting
        na = len(perfTab.actions)
        if limitingQuantiles == None:
            limitingQuantiles = na // 2
        self.sortingParameters = {}
        self.sortingParameters['limitingQuantiles'] = limitingQuantiles
        self.sortingParameters['strategy'] = strategy
        self.sortingParameters['LowerClosed'] = LowerClosed
        self.sortingParameters['PrefThresholds'] = PrefThresholds
        self.sortingParameters['hasNoVeto'] = hasNoVeto
        self.sortingParameters['Threading'] = Threading
        self.sortingParameters['nbrCores'] = nbrCores        
        if Comments:        
            print('Computing the %d-quantiles sorting digraph ...' % (limitingQuantiles))
        t0 = time()
        if Threading and cpu_count() > 2:    
            qs = QuantilesSortingDigraph(perfTab,
                         limitingQuantiles=limitingQuantiles,
                         LowerClosed=LowerClosed,
                         PrefThresholds=PrefThresholds,
                         hasNoVeto=hasNoVeto,
                         outrankingType = outrankingType,
                         Threading=True,
                         nbrCores=nbrCores,
                         CompleteOutranking = False)                
        else:
            qs = QuantilesSortingDigraph(perfTab,
                         limitingQuantiles=limitingQuantiles,
                         LowerClosed=LowerClosed,
                         PrefThresholds=PrefThresholds,
                         hasNoVeto=hasNoVeto,
                         outrankingType = outrankingType,
                         CompleteOutranking = True)

        self.runTimes = {'sorting': time() - t0}
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))

        # copying the quantiles sorting results
        t0 = time()
        self.name = 'boostedKohler-'+qs.name
        self.actions = deepcopy(qs.actions)
        self.order = len(self.actions)
        self.criteria = deepcopy(qs.criteria)
        self.evaluation = deepcopy(qs.evaluation)
        self.valuationdomain = deepcopy(qs.valuationdomain)
        self.sortingRelation = deepcopy(qs.relation)
        self.relation = deepcopy(qs.relation)
        self.categories = deepcopy(qs.categories)
        self.limitingQuantiles = deepcopy(qs.limitingQuantiles)
        self.criteriaCategoryLimits = deepcopy(qs.criteriaCategoryLimits)
        self.profiles = deepcopy(qs.profiles)
        self.runTimes = {'copying': time() - t0}
        if Comments:
            print('execution time: %.4f' % (self.runTimes['copying']))

        # preordering
        self.strategy = strategy
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
##        actionsSet = set([x for x in self.actions])
##        relation = {}
##        for x in actionsSet:
##            relation[x] = {}
##            for y in actionsSet:
##                relation[x][y] = Med
        tw = time()
        preOrdering = self.computeQuantileOrdering(strategy=strategy)
        nwo = len(preOrdering)
        preceedingActions = set([])
        followingActions = set([x for x in self.actions])
        catContent = {}
        for i in range(nwo):
            currActions = set(preOrdering[i])
            catContent[i+1] = preOrdering[i]
            if Debug:
                print(i+1,currActions)        
            for x in currActions:
                for y in preceedingActions:
                    self.relation[x][y] = Min
                    self.relation[y][x] = Max
                for y in followingActions:
                    self.relation[x][y] = Max
                    self.relation[y][x] = Min
            preceedingActions = preceedingActions | currActions
            followingActions = followingActions - currActions
            if Debug:
                print(preceedingActions)
                print(followingActions)
        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('preordering execution time: %.4f' % self.runTimes['preordering']  )

        # local Kohler ordering
        t0 = time()
        for c in range(1,nwo+1):
            if Debug:
                print(c, len(catContent[c]))
            pt = PartialPerformanceTableau(perfTab,catContent[c])
            gt = BipolarOutrankingDigraph(pt)
            ko = KohlerOrder(gt)
            ko.recodeValuation(-100,100)
            if Debug:
                ko.showRelationTable()
            for x in catContent[c]:
                for y in catContent[c]:
                    self.relation[x][y] = ko.relation[x][y]
        self.runTimes['localKohler'] = time() - t0

        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

        self.runTimes['totalTime'] = time() - ttot

    def computePreOrdering(self,Descending=True,strategy=None,Comments=False,Debug=False):
        """
        specialisation of the showWeakOrder method
        """
        if strategy == None:
            strategy = self.strategy
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
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
        weakOrdering = []
        for item in actionsCategIntervals:
            #print(item)
            if Comments:
                if strategy == "optimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                elif strategy == "pessimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )                   
                elif strategy == "average":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )

            weakOrdering.append(item[1])
        return weakOrdering


class NetFlowsOrder(LinearOrder):
    """
    instantiates the net flows Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the net flows ordering rule
        """

        # construct ranked pairs
        if coDual:
            otherCoDual = CoDualDigraph(other)
            relation = otherCoDual.relation
            #netFlows = otherCoDual.computeSingleCriteriaNetflows()
            Max = otherCoDual.valuationdomain['max']
            if Debug:
                otherCoDual.showRelationTable()
                print(otherCoDual.valuationdomain)
                #print netFlows
        else:
            relation = other.relation
            #netFlows = other.computeSingleCriteriaNetflows()
            Max = other.valuationdomain['max']
            if Debug:
                other.showRelationTable()
                print(other.valuationdomain)
                #print netFlows
                
            
        actions = [x for x in other.actions]
        actions.sort()
        n = len(actions)
        
        # instatiates a Digraph template
        g = IndeterminateDigraph(order=n)
        g.actions = actions
        g.valuationdomain = {'min':Decimal('-3'), 'med': Decimal('0'), 'max': Decimal('3')}
        g.relation = {}
        for x in g.actions:
            g.relation[x] = {}
            for y in g.actions:
                g.relation[x][y] = g.valuationdomain['med']

        netflows = {}
        netFlowsOrder = []
        for x in actions:
            netflows[x] = Decimal('0.0')      
            for y in actions:
                if y != x:
                    netflows[x] += relation[x][y] - relation[y][x]
            if Debug:
                print('netflow for %s = %.2f' % (x, netflows[x]))
            netFlowsOrder.append((netflows[x],x))
        netFlowsOrder.sort(reverse=True)
        if Debug:
            print(netFlowsOrder)

        n = len(g.actions)
        for i in range(n):
            for j in range(i+1,n):
                x = netFlowsOrder[i][1]
                y = netFlowsOrder[j][1]
                g.relation[x][y] = g.valuationdomain['max']
                g.relation[y][x] = g.valuationdomain['min']
         
        self.name = other.name + '_ranked'        
        self.actions = other.actions
        self.order = len(self.actions)
        self.valuationdomain = g.valuationdomain
        self.relation = g.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            self.showRelationTable()
            print(self.computeOrder())


########  instantiates optimal linear orderings

class KemenyOrder(LinearOrder):
    """
    instantiates the exact Kemeny Order from
    a given bipolar-valued Digraph instance of small order 
    """
    def __init__(self,other,orderLimit=7,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph by exact enumeration
        of all permutations of actions.
        """
        from digraphs import all_perms
        from copy import copy as deepcopy
        from decimal import Decimal
        
        Min = other.valuationdomain['min']
        Max = other.valuationdomain['max']
        Med = other.valuationdomain['med']
        actionsList = [x for x in other.actions] 
        n = len(actionsList)
        self.order = n
        relation = deepcopy(other.relation)
        kemenyOrder = other.computeKemenyOrder(orderLimit=orderLimit,Debug=Debug)
        if kemenyOrder == None:
            print('Intantiation error: unable to compute the Kemeny Order !!!')
            print('Digraph order %d is required to be lower than 8!' % n)
            return
        if Debug:
            print(KemenyOrder,other.maximalOrders)
        # instatiates a Digraph template
        
        g = IndeterminateDigraph(order=n)
        g.actions = deepcopy(other.actions)
        Min = Decimal('-1.0')
        Max = Decimal('1.0')
        Med = Decimal('0.0')
        g.valuationdomain = {'min': Min, 'med': Med, 'max': Max}
        g.relation = deepcopy(other.relation)
        for i in range(n):
            for j in range(i+1,n):
                x = kemenyOrder[0][i]
                y = kemenyOrder[0][j]
                if Debug:
                    print(x,y)
                g.relation[x][y] = Max
                g.relation[y][x] = Min

        for x in g.actions:
            g.relation[x][x] = Med

        if Debug:
            print('Kemeny ordered relation table:')
            g.showRelationTable()

        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(g.valuationdomain)
        self.relation = deepcopy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            print('Kemeny Order = ', self.computeOrder())

########  instantiates principal scores' ordering

class PrincipalOrder(LinearOrder):
    """
    instantiates the order from the scores obtained by the first
    princiapl axis of the eigen deomposition of the covariance of the
    outdegrees of the valued digraph 'other'.
    """
    def __init__(self,other,Colwise=True,imageType=None,
                 plotFileName="principalOrdering",Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph by using the first
        principal eigen vector of the covariance
        of the indegrees (Colwise=True/default) or
        of the outdegrees (Colwise=False).

        Implemented Image types are:
        None/default, "pdf", "png" and "xfig".

        The plot file name only matters with a non None image type.
        """
        from copy import copy as deepcopy
        from decimal import Decimal
        
        Min = other.valuationdomain['min']
        Max = other.valuationdomain['max']
        Med = other.valuationdomain['med']
        actionsList = [x for x in other.actions]
        actionsList.sort()
        n = len(actionsList)
        relation = deepcopy(other.relation)
        principalScores = other.computePrincipalOrder(Colwise=Colwise,
                                                      imageType=imageType,
                                                      plotFileName=plotFileName,
                                                      Debug=Debug)
        # [ (score1,action_(1)), (score2,action_(2)), ...] 
        if principalScores == None:
            print('Intantiation error: unable to compute the principal Order !!!')
            return
        if Debug:
            print(principalScores)
        # instatiates a Digraph template
        
        g = IndeterminateDigraph(order=n)
        g.actions = deepcopy(other.actions)
        Min = Decimal('-1.0')
        Max = Decimal('1.0')
        Med = Decimal('0.0')
        g.valuationdomain = {'min': Min, 'med': Med, 'max': Max}
        g.relation = deepcopy(other.relation)
        for i in range(n):
            for j in range(i+1,n):
                x = principalScores[i][1]
                y = principalScores[j][1]
                #if Debug:
                #    print(x,y)
                g.relation[x][y] = Max
                g.relation[y][x] = Min

        for x in g.actions:
            g.relation[x][x] = Max

        if Debug:
            print('principal ordered relation table:')
            g.showRelationTable()
        # check principal orientation with ordinal correlation sign
        corr = other.computeOrdinalCorrelation(g.relation)
        if corr['correlation'] < Decimal('0'):
            ReverseScores = True
            g = ~(g)
        else:
            ReverseScores = False
        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(g.valuationdomain)
        self.relation = deepcopy(g.relation)
        if ReverseScores == False: 
            if Colwise:
                self.principalColwiseScores = principalScores
            else:
                self.principalRowwiseScores = principalScores
        else:
            if Colwise:
                self.principalColwiseScores =\
                    [(-x,y) for (x,y) in principalScores]
                self.principalColwiseScores.sort(reverse=True)
            else:
                self.principalRowwiseScores =\
                    [(-x,y) for (x,y) in principalScores]
                self.principalRowwiseScores.sort(reverse=True)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            print('Principal Order = ', self.computeOrder())

#----------test  linearOrders module classes  ----------------
if __name__ == "__main__":
    import sys,array
    from time import time
    from digraphs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from linearOrders import *
    from weakOrders import *

    print("""
    ****************************************************
    * Python linearOrders module                       *
    * Copyright (C) 2011-2015 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    print('*-------- Testing class and methods -------')

    Threading = True
    
##    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
##                                   numberOfActions=200)
##    t.saveXMCDA2('test')
    #t = XMCDA2PerformanceTableau('uniSorting')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=Threading)
    bko = BoostedKohlerOrder(t,Threading=Threading,Debug=False)
    qr = QuantilesRankingDigraph(t,100,Threading=Threading)
    #bko.showSorting()
    #bko.showQuantileOrdering()
    #bko.showHTMLRelationTable(actionsList=bko.computeOrder())
    print(bko.runTimes)
    print(g.computeOrdinalCorrelation(bko))
    print(qr.runTimes)
    print(g.computeOrdinalCorrelation(qr))
    
    ## t = RandomRankPerformanceTableau(numberOfActions=20)
    ## t.saveXMCDA2('testRP')
    ## #t = XMCDA2PerformanceTableau('testRP')
    ## #g = Digraph('testLuisJune2')
    ## g = BipolarOutrankingDigraph(t)
    ## #g.showRelationTable()
    ## gcd = CoDualDigraph(g)
    ## #print gcd.valuationdomain
    ## #gcd.showRelationTable()
    ## gcd.exportGraphViz()
    ## print 'All ranking rules on S and/or codual S with ordinal distance to S'
    ## print 'S determinateness = ', g.computeDeterminateness()*g.order*(g.order-1)*100

    ## ## k = KemenyOrder(g)
    ## ## print 'Kemeny           : ', k.computeOrder(), k.computeKemenyIndex(g)
    ## t0 = time()
    ## rps = RankedPairsOrder(g,isExtendedPrudent=False,coDual=False,Debug=False)
    ## print 'RP on S          : ', rps.computeOrder(), rps.computeKemenyIndex(g),time()-t0,'sec.'
    ## t1 = time()
    ## rpeps = RankedPairsOrder(g,isExtendedPrudent=True,coDual=False,Debug=False)
    ## print 'RPEP on S        : ', rpeps.computeOrder(), rpeps.computeKemenyIndex(g),time()-t1,'sec.'
    ## t0 = time()
    ## rps = RankedPairsOrder(g,isExtendedPrudent=False,Cpp=True, coDual=False,Debug=False)
    ## print 'RP on S          : ', rps.computeOrder(), rps.computeKemenyIndex(g),time()-t0,'sec.'
    ## t1 = time()
    ## rpeps = RankedPairsOrder(g,isExtendedPrudent=True,Cpp=True, coDual=False,Debug=False)
    ## print 'RPEP on S        : ', rpeps.computeOrder(), rpeps.computeKemenyIndex(g),time()-t1,'sec.'
    ## ## rpcd = RankedPairsOrder(g,coDual=True,Debug=False)
    ## ## print 'RP on cdS        : ', rpcd.computeOrder(), rpcd.computeKemenyIndex(g)

    ## ## kos = KohlerOrder(g,coDual=False,Debug=False)
    ## ## print 'Kohler on S      : ', kos.computeOrder(),kos.computeKemenyIndex(g)
    ## ## kocd = KohlerOrder(g,coDual=True,Debug=False)
    ## ## print 'Kohler on codual : ', kocd.computeOrder(),kocd.computeKemenyIndex(g)

    ## ## nfs = NetFlowsOrder(g,coDual=False,Debug=False)
    ## ## print 'Net flows        : ', nfs.computeOrder(), nfs.computeKemenyIndex(g
    ## ##)
##    from outrankingDigraphs import RandomBipolarOutrankingDigraph
##    g1 = RandomBipolarOutrankingDigraph(Normalized=True)
##    g1.save('test')
##    g1 = Digraph('test')
##    g1.showRelationTable()
##    p = PrincipalOrder(g1,Colwise=True,imageType=None,Debug=False)
##    print(p.computeOrder())
##    print(g1.computeOrdinalCorrelation(p))
##    #p.showRelationTable()
##    rbc = RankingByChoosingDigraph(g1,Debug=False)
##    #rbc.showRelationTable()
##    pio = PrincipalInOutDegreesOrdering(g1,Debug=True)
    
##    g1.showRelationTable()
##    g2 = RandomLinearOrder(numberOfActions=10,Debug=True)
##    g2.showRelationTable()
##    print(g1.computeBipolarCorrelation(g2))
##    g1 = RandomLinearOrder(OutrankingModel=True, Debug=True)
##    g1.showRelationTable()
##    g2 = RandomLinearOrder(OutrankingModel=True,Debug=True)
##    g2.showRelationTable()
##    print(g1.computeBipolarCorrelation(g2))
##    
    
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
        
    print('*************************************')
    print('* R.B. June 2011                    *')
    print('* $Revision: 1.18 $                *')                   
    print('*************************************')

#############################
# Log record for changes:
# $Log: linearOrders.py,v $
# Revision 1.18  2012/10/26 11:25:28  bisi
# minor
#
# Revision 1.17  2012/09/14 08:12:13  bisi
# sync
#
# Revision 1.16  2012/09/14 05:03:21  bisi
# Added RandomLinearOrder class for generating random linear orders.
#
# Revision 1.12  2012/05/09 10:51:43  bisi
# GPL version 3 licensing installed
#
# Revision 1.9  2011/08/13 05:25:35  bisi
# addedd piping C++ subprocess for chordless circuits enumeration
#
# Revision 1.8  2011/08/12 08:59:51  bisi
# added agrum directory with C++ sources for chordless circuits enumeration adn detection
#
# Revision 1.2  2011/06/02 08:24:10  bisi
# Added NetFlowsOrder class implementing the Promethee ranking base on the net flows"
#
#############################
