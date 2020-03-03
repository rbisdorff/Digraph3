#!/usr/bin/env python3
"""
Python implementation of linear orders
Dependancy: digraphs module
Copyright (C) 2011-2020  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: 1.18 $"
# $Source: /home/cvsroot/Digraph/linearOrders.py,v $

from digraphsTools import *
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

class _ExtendedPrudentDigraph(Digraph):
    """
    Instantiates the associated extended prudent
    codual of the digraph enstance.
    Instantiates as other.__class__ !
    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other,prudentBetaLevel=None,CoDual=False,Debug=False):
        from digraphsTools import omax, omin
        from copy import copy, deepcopy
        self.__class__ = other.__class__
        self.name = 'extprud-'+other.name
        try:
            self.description = copy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = copy(other.evaluation)
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
        self.actions = copy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(gp.valuationdomain)
        actionsList = [x for x in self.actions]
        #Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        #Min = self.valuationdomain['min']
        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                if Debug:
                    print('omax(Med,[gp.relation[x][y],stRelation[x][y]])',x,y,[gp.relation[x][y],stRelation[x][y]])
                relation[x][y] = omax(Med,[gp.relation[x][y],stRelation[x][y]])    
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
    def computeRanking(self):
        """
        computes the linear ordering from lowest (best, rankk = 1) to highest (worst rank=n)
        of an instance of the LinearOrcer class by sorting by outdegrees (gamma[x][0]).
        """
        degrees = []
        for x in list(dict.keys(self.actions)):
            degrees.append((len(self.gamma[x][0]),x))
        degrees.sort(reverse=True)
        ranking = []
        for x in degrees:
            ranking.append(x[1])
        return ranking

    def computeOrder(self):
        """
        computes the linear ordering from lowest (worst) to highest (best)
        of an instance of the LinearOrcer class by sorting by indegrees (gamma[x][1]).
        """
        degrees = []
        for x in list(dict.keys(self.actions)):
            degrees.append((len(self.gamma[x][0]),x))
        degrees.sort(reverse=False)
        ordering = []
        for x in degrees:
            ordering.append(x[1])
        return ordering

    def showOrdering(self):
        """
        shows the linearly ordered actions in list format.
        """
        print(self.computeOrder())

    def showRanking(self):
        """
        shows the linearly ordered actions in list format.
        """
        print(self.computeRanking())
        
        
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

    def htmlRanking(self):
        """
        returns the html encoded presentation of a linear order
        """
        linearRanking = self.computeRanking()
        html = ''
        html += '<table border = 1>'
        html += '<tr bgcolor="#9acd32"><th colspan="2">Ranking result</th></tr>'
        for x in linearRanking:
            try:
                name = self.actions[x]['name']
            except:
                name = x
            html += '<tr><th bgcolor="#FFF79B">%s</th><td>%s</td></tr>' % (x,name)
        html += '</table>'
        return html
    
    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),Comments=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName, bestChoice=bestChoice,worstChoice=worstChoice,Comments=Comments,graphType=graphType,graphSize=graphSize)

    def exportGraphViz(self,fileName=None, isValued=True, bestChoice=set(),worstChoice=set(),Comments=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file  for linear order drawing filtering.
        """
        import os
        if Comments:
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
        if Comments:
            print('Exporting to '+dotName)
        if bestChoice != set():
            rankBestString = '{rank=max; '
        if worstChoice != set():
            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\ndigraphs module (graphviz), R. Bisdorff, 2015", size="')
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
                edge = 'n%s-> n%s [dir=forward,style="setlinewidth(%d)",color=%s, arrowhead=normal] ;\n' %\
                       (i+1,i+2,self.relation[actionkeys[i]][actionkeys[i+1]],arcColor)
                
                fo.write(edge)
                     
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        fo.write('}\n')
        fo.close()
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
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
    def __init__(self,numberOfActions=10,Debug=False,OutrankingModel=False,Valued=False,seed=None):
        """
        constructor for generating random instances of linear orders with a given number of actions (default=10).
        """
        import random
        random.seed(seed)
        if OutrankingModel:
            from outrankingDigraphs import RandomOutrankingDigraph
            g = RandomOutrankingDigraph(numberOfActions=numberOfActions)
        else:
            from randomDigraphs import RandomValuationDigraph
            g = RandomValuationDigraph(order=numberOfActions)
        g.recodeValuation(-1,1)
        actionsList = [x for x in g.actions]
        random.shuffle(actionsList)
        if Debug:
            print(g.actions, actionsList)
        self.name = 'randomLinearOrder'
        self.actions = g.actions
        self.order = len(self.actions)
        self.valuationdomain = g.valuationdomain
        self.relation = g.relation
        for i in range(self.order):
            x = actionsList[i]
            self.relation[x][x] = self.valuationdomain['med']
            for j in range(i+1,self.order):
                y = actionsList[j]
                if Valued:
                    self.relation[x][y] = abs(g.relation[x][y])
                    self.relation[y][x] = -abs(g.relation[y][x])
                else:
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
    def __init__(self,other,coDual=False,Leximin=False,\
                 Cpp=False, isValued=False,\
                 isExtendedPrudent=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the ranked pairs (Lexmin Dias-Lamboray) rule
        Parameter: isExtendedPrudent 
        """
        from copy import copy, deepcopy
        # construct ranked pairs

        if coDual:
            other = CoDualDigraph(other)
        if Debug:
            other.showRelationTable()
            
        relation = other.relation
##        actions = [x for x in other.actions]
##        actions.sort()
        actions = other.actions
        n = len(actions)
        
        listPairs = []
        for x in actions:
            for y in (z for z in actions if z != x):
                listPairs.append((-relation[x][y],(x,y),x,y))
        listPairs.sort(reverse=Leximin)
        if Debug:
            print(listPairs)
        
        # instatiates a Digraph template
        if isExtendedPrudent:
            prudentBetaLevel = other.computePrudentBetaLevel(Debug=Debug)
            if prudentBetaLevel > other.valuationdomain['med']:
                if Debug:
                    print('Is extended prudent with level: %.2f !' % prudentBetaLevel)
                g = _ExtendedPrudentDigraph(other,\
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
        self.valuationdomain = g.valuationdomain
        if Leximin:
            self.relation = (-g).relation
        else:
            self.relation = g.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.rankedPairsOrder = self.computeOrder()
        self.rankedPairsRanking = self.computeRanking()
        
        if Debug:
            print('Ranked Pairs Order = ', self.rankedPairsRanking)

    
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
        from copy import copy, deepcopy
        from collections import OrderedDict
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

        rank = OrderedDict()
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
        kohlerRanking = [x[1] for x in kohlerOrder]
        #kohlerRanking.reverse()
        self.kohlerRanking = kohlerRanking
        
        if Debug:
            print('Kohler ranks: ', kohlerRanking)

        n = len(g.actions)
        for i in range(n):
            for j in range(i+1,n):
                x = kohlerOrder[i][1]
                y = kohlerOrder[j][1]
                g.relation[x][y] = g.valuationdomain['max']
                g.relation[y][x] = g.valuationdomain['min']

            
        self.name = other.name + '_ranked'        
        self.actions = copy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(g.valuationdomain)
        self.relation = copy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.kohlerOrder = self.computeOrder()
        if Debug:
            self.showRelationTable()
            print('Kohler ranking: ', self.kohlerRanking)

class NetFlowsOrder(LinearOrder):
    """
    instantiates the net flows Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the net flows ordering rule
        """

        #from copy import deepcopy
        from collections import OrderedDict
        from time import time

        if Debug:
            Comments=True
        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if coDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = otherCoDual.relation
##            if Debug:
##                otherCoDual.showRelationTable()
##                print(otherCoDual.valuationdomain)
        else:
            otherRelation = other.relation
        n = len(other.actions)
        actions = other.actions
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        netFlows = []
        if other.valuationdomain['med'] == Med:
            if Debug:
                print('standard')
            for x in actions:
                xnetflows = sum((otherRelation[x][y] - otherRelation[y][x])\
                                 for y in actions)
##                xnetflows = sum((otherRelation[x][y])\
##                                 for y in actions)
                netFlows.append((xnetflows,x))
                if Debug:
                    print(x,xnetflows)
        else:
            otherMax = other.valuationdomain['max']
            otherMin = other.valuationdomain['min']
            
            for x in actions:
                xnetflows = sum((otherRelation[x][y] +\
                                (otherMax - otherRelation[y][x] + otherMin))\
                                 for y in actions)
                netFlows.append((xnetflows,x))
                if Debug:
                    print(x,xnetflows)
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        netFlows.sort(reverse=True)
        self.netFlows = netFlows
        if Comments:
            print('Net Flows :')
            for x in netFlows:
                print( '%s : %.3f' % (x[1],x[0]) )

        netFlowsRanking = [x[1] for x in netFlows]
        self.netFlowsRanking = netFlowsRanking
        netFlowsOrder = list(reversed(netFlowsRanking))
        self.netFlowsOrder = netFlowsOrder
        if Debug:
            print(self.netFlowsRanking)
            print(self.netFlowsOrder)
        if Comments:
            print('NetFlows Ranking:')
            print(netFlowsRanking)
        runTimes['netFlows'] = time() - tnf

        # init relation
        tr = time()
        for i in range(n):
            x = netFlowsRanking[i]
            selfRelation[x] = {}
            for j in range(n):
                y = netFlowsRanking[j]
                if i < j:
                    selfRelation[x][y] = Max
                else:
                    selfRelation[x][y] = Min
        runTimes['relation'] = time() - tr      
##        if Debug:
##            print(selfRelation) 
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes
##        if Debug:
##            self.showRelationTable()
##            self.showOrdering()

    def showScores(self,direction='descending'):
        print('Net flow scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.netFlows:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in reversed(self.netFlows):
                print('%s \t %.2f' %(x[1],x[0]))

class IteratedNetFlowsRanking(LinearOrder):
    """
    instantiates the iterated NetFlows order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Valued=False,Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the iterated NetFlows rules
        """
        from copy import copy, deepcopy
        from collections import OrderedDict
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

        # construct ranking
        actionsList = [x for x in g.actions]

        rank = OrderedDict()
        order = OrderedDict()
        k = 1
        while actionsList != []:
            knetFlows = []
            for x in actionsList:
                ca = 0
                kxnetFlows = Decimal('0')
                for y in actionsList:
                    if x != y:
                        kxnetFlows += relation[x][y] - relation[y][x]
                        ca += 2
                if Debug:
                    print('k,ca,kxnetFlows', k,ca, kxnetFlows)                        
                if ca > 0:
                    kxnetFlows = kxnetFlows / Decimal(str(ca))
                if Debug:
                    print('k,x,kxnetFlows', k,x, kxnetFlows)
                knetFlows.append((kxnetFlows,x))
            knetFlows.sort()
            if Comments:
                print('k,knetFlows, knetFlows[-1][1]',k,knetFlows, knetFlows[-1][1])
            rank[knetFlows[-1][1]] = {'rank':k,'netFlows':knetFlows[-1][0]}
            order[knetFlows[0][1]] = {'order':k,'netFlows':knetFlows[0][0]}
            
            actionsList.remove(knetFlows[-1][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        self.valuedRanks = rank
        # construct ordering
        actionsList = [x for x in g.actions]
        order = OrderedDict()
        k = 1
        while actionsList != []:
            knetFlows = []
            for x in actionsList:
                ca = 0
                kxnetFlows = Decimal('0')
                for y in actionsList:
                    if x != y:
                        kxnetFlows += relation[x][y] - relation[y][x]
                        ca += 2
                if Debug:
                    print('k,ca,kxnetFlows', k,ca, kxnetFlows)                        
                if ca > 0:
                    kxnetFlows = kxnetFlows / Decimal(str(ca))
                if Debug:
                    print('k,x,kxnetFlows', k,x, kxnetFlows)
                knetFlows.append((kxnetFlows,x))
            knetFlows.sort()
            if Comments:
                print('k,knetFlows, knetFlows[-1][1]',k,knetFlows, knetFlows[-1][1])
            order[knetFlows[0][1]] = {'order':k,'netFlows':knetFlows[0][0]}
            
            actionsList.remove(knetFlows[0][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        self.valuedOrdering = order 
        if Debug:
            print(rank)
            print(order)

##        iteratedNetFlowsRanking = []
##        for x in rank:
##            iteratedNetFlowsRanking.append((rank[x]['rank'],x))
        #iteratedNetFlowsOrder.sort()
        iteratedNetFlowsRanking = [x for x in rank]
        #kohlerRanking.reverse()
        self.iteratedNetFlowsRanking = iteratedNetFlowsRanking
##        for x in rank:
        #    iteratedNetFlowsOrder.append((order[x]['rank'],x))
        #iteratedNetFlowsOrder.sort()
        iteratedNetFlowsOrdering = [x for x in order]
        #kohlerRanking.reverse()
        self.iteratedNetFlowsOrdering = iteratedNetFlowsOrdering
        
        if Debug:
            print('Iterated netflows ranks: ', iteratedNetFlowsRanking)
            print('Iterated netflows ordering: ', iteratedNetFlowsOrdering)

        if Valued:
            n = len(g.actions)
            for i in range(n):
                for j in range(i+1,n):
                    x = iteratedNetFlowsRanking[i]
                    y = iteratedNetFlowsRanking[j]
                    g.relation[x][y] = rank[x]['netFlows']
                    g.relation[y][x] = -rank[x]['netFlows']
        else:
            n = len(g.actions)
            for i in range(n):
                for j in range(i+1,n):
                    x = iteratedNetFlowsRanking[i]
                    y = iteratedNetFlowsRanking[j]
                    g.relation[x][y] = g.valuationdomain['max']
                    g.relation[y][x] = g.valuationdomain['min']

            
        self.name = other.name + '_ranked'        
        self.actions = copy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(g.valuationdomain)
        self.relation = copy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            self.showRelationTable()
            print('Iterated NetFlows ranking: ', self.iteratedNetFlowsRanking)


class _OutFlowsOrder(LinearOrder):
    """
    instantiates the out flows Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the out flows ordering rule
        """

        #from copy import deepcopy
        from linearOrders import _OutFlowsOrder
        from collections import OrderedDict
        from time import time

        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if coDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = otherCoDual.relation
##            if Debug:
##                otherCoDual.showRelationTable()
##                print(otherCoDual.valuationdomain)
        else:
            otherRelation = other.relation
        n = len(other.actions)
        actions = other.actions
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        outFlows = []
        if other.valuationdomain['med'] == Med:
            for x in actions:
##                xoutFlows = sum((otherRelation[x][y] - otherRelation[y][x])\
##                                 for y in actions)
                xoutFlows = sum((otherRelation[x][y])\
                                 for y in actions)
                outFlows.append((xoutFlows,x))
        else:
            otherMax = other.valuationdomain['max']
            otherMin = other.valuationdomain['min']
            
            for x in actions:
##                xoutFlows = sum((otherRelation[x][y] +\
##                                (otherMax - otherRelation[y][x] + otherMin))\
##                                 for y in actions)
                xoutFlows = sum((otherRelation[x][y])\
                                 for y in actions)
                outFlows.append((xoutFlows,x))
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        outFlows.sort(reverse=True)
        self.outFlows = outFlows
##        if Debug:
##            print(outFlows)

        outFlowsRanking = [x[1] for x in outFlows]
        self.outFlowsRanking = outFlowsRanking
        outFlowsOrder = list(reversed(outFlowsRanking))
        self.outFlowsOrder = outFlowsOrder
##        if Debug:
##            print(self.outFlowsRanking)
##            print(self.outFlowsOrder)
        runTimes['outFlows'] = time() - tnf

        # init relation
        tr = time()
        for i in range(n):
            x = outFlowsRanking[i]
            selfRelation[x] = {}
            for j in range(n):
                y = outFlowsRanking[j]
                if i < j:
                    selfRelation[x][y] = Max
                else:
                    selfRelation[x][y] = Min
        runTimes['relation'] = time() - tr      
##        if Debug:
##            print(selfRelation) 
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes
##        if Debug:
##            self.showRelationTable()
##            self.showOrdering()

    def showScores(self,direction='descending'):
        print('Out flow scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.outFlows:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in reversed(self.outFlows):
                print('%s \t %.2f' %(x[1],x[0]))

class CopelandOrder(LinearOrder):
    """
    instantiates the Copeland Order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,coDual=False,Gamma=False,\
                 RankingRelation=True,Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Copeland ordering rule

        When Gamma == True, the Copeland scores
        are computed with the help of the gama functions as
        the difference between outdegrees and indegrees.
        If False, they are computed as the sum of the differences
        between the polarised outranking characteristics.

        When RankingRelation == True, *Copeland* scores equivalent classes are ordered
        in decreasing lexicographic order. Otherwise, they are ordered in increasing
        lexicographic order.
        
        """

        #from copy import deepcopy
        from collections import OrderedDict
        from time import time
        if Debug:
            Comments=True
        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if coDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = otherCoDual.relation
            if Debug:
                otherCoDual.showRelationTable()
                print(otherCoDual.valuationdomain)
        else:
            otherRelation = other.relation
        n = len(other.actions)
        actions = other.actions
        gamma = other.gamma
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        incCopelandScores = []
        decCopelandScores = []
        # with gamma functions
        if Gamma:
            for x in actions:
                copelandScore = len(gamma[x][0]) - len(gamma[x][1])
                incCopelandScores.append((copelandScore,x))
                decCopelandScores.append((-copelandScore,x))
        else: # with Condorcet Digraph valuation
            c = PolarisedDigraph(other,level=other.valuationdomain['med'],\
                             StrictCut=True,KeepValues=False)
            if Debug:
                print(c)
            c.recodeValuation()
            cRelation = c.relation
            for x in actions:
                copelandScore = Decimal('0')
                for y in actions:
                    copelandScore += cRelation[x][y] - cRelation[y][x]
                incCopelandScores.append((copelandScore,x))
                decCopelandScores.append((-copelandScore,x))
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        incCopelandScores.sort()
        decCopelandScores.sort()
        self.decCopelandScores = decCopelandScores
        self.incCopelandScores = incCopelandScores
    
        if Comments:
            print('Copeland decreasing scores')
            for x in decCopelandScores:
                print( '%s : %d' %( x[1],int(-x[0]) ) )
            print('Copeland increasing scores')
            for x in incCopelandScores:
                print( '%s : %d' %( x[1],int(x[0]) ) )

        copelandRanking = [x[1] for x in decCopelandScores]
        self.copelandRanking = copelandRanking
        copelandOrder = [x[1] for x in incCopelandScores]
        self.copelandOrder = copelandOrder

        if Comments:
            print('Copeland Ranking:')
            print(copelandRanking)
            
        runTimes['copeland'] = time() - tnf

        # init relation
        if RankingRelation:
            relOrdering = copelandRanking
        else:
            relOrdering = list(reversed(copelandOrder))
        tr = time()
        for i in range(n):
            x = relOrdering[i]
            selfRelation[x] = {}
            srx = selfRelation[x]
            for j in range(n):
                y = relOrdering[j]
                if i < j:
                    srx[y] = Max
                elif i == j:
                    srx[y] = Med
                else:
                    srx[y] = Min
        runTimes['relation'] = time() - tr      
        if Debug:
            print(selfRelation) 
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Copeland scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.decCopelandScores:
                print('%s \t %.2f' %(x[1],-x[0]))
        else:
            for x in reversed(self.incCopelandScores):
                print('%s \t %.2f' %(x[1],x[0]))
         


##class _CopelandOrder(LinearOrder):
##    """
##    instantiates the net Copeland Order from
##    a given bipolar-valued Digraph instance.
##    The Copeland ordering rule ranks the decision actions in decreasing order of the Copeland score,
##    which is the difference between the crisp outranking degree and crisp outranked degree;
##    actually the net flows orering of the corresponding Condorcet digraph.  
##    """
##    def __init__(self,other,coDual=False,Debug=False):
##        """
##        constructor for generating a linear order
##        from a given other digraph following
##        the Copeland ordering rule
##        """
##        from copy import copy,deepcopy
##        # construct ranked pairs
##        if coDual:
##            otherCoDual = CoDualDigraph(other)
##            relation = otherCoDual.relation
##            #netFlows = otherCoDual.computeSingleCriteriaNetflows()
##            Max = otherCoDual.valuationdomain['max']
##            if Debug:
##                otherCoDual.showRelationTable()
##                print(otherCoDual.valuationdomain)
##                #print netFlows
##        else:
##            relation = deepcopy(other.relation)
##            #netFlows = other.computeSingleCriteriaNetflows()
##            Max = other.valuationdomain['max']
##            if Debug:
##                other.showRelationTable()
##                print(other.valuationdomain)
##                #print netFlows
##                
##            
##        #actions = list(dict.keys(other.actions))
##        #actions.sort()
##        n = len(other.actions)
##        
##        # instatiates a Digraph template
##        g = IndeterminateDigraph(order=n)
##        g.actions = deepcopy(other.actions)
##        g.valuationdomain = {'min':Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
##        Med = g.valuationdomain['med']
##        Max = g.valuationdomain['max']
##        Min = g.valuationdomain['min']
##        g.relation = {}
##        for x in dict.keys(g.actions):
##            g.relation[x] = {}
##            for y in dict.keys(g.actions):
##                g.relation[x][y] = Med
##
##        copelandScores = {}
##        copelandScoresList = []
##        for x in g.actions:
##            xoutDegree = len(other.gamma[x][0])
##            xinDegree = len(other.gamma[x][1])
##            copelandScores[x] = (xinDegree - xoutDegree) # reversed sort
##            if Debug:
##                print('Copeland score for %s = %d' % (x, copelandScores[x]))
##            copelandScoresList.append((copelandScores[x],x))
##        copelandScoresList.sort()
##        copelandRanking = [x[1] for x in copelandScoresList]
##        self.copelandRanking = copelandRanking
##        if Debug:
##            print(copelandRanking)
##            
##        for i in range(n):
##            for j in range(i+1,n):
##                x = copelandScoresList[i][1]
##                y = copelandScoresList[j][1]
##                g.relation[x][y] = Max
##                g.relation[y][x] = Min
##                
##         
##        self.name = other.name + '_ranked'        
##        self.actions = g.actions
##        self.order = n
##        self.valuationdomain = g.valuationdomain
##        self.relation = g.relation
##        self.gamma = self.gammaSets()
##        self.notGamma = self.notGammaSets()
##        self.copelandOrder = list(reversed(list(copelandRanking)))
##        if Debug:
##            self.showRelationTable()
##            self.showOrdering()

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
        if other.order > orderLimit:
            print('Digraph order %d to high. The default limit (7) may be changed with the oderLimit argument.' % (other.order) )
            return
                  
        from digraphs import all_perms
        from copy import copy,deepcopy
        from decimal import Decimal
        
        Min = other.valuationdomain['min']
        Max = other.valuationdomain['max']
        Med = other.valuationdomain['med']
        #relation = copy(other.relation)
        kemenyRankings = other.computeKemenyRanking(orderLimit=orderLimit,Debug=False)
        # [0] = ordered actions list, [1] = maximal Kemeny index
        
        kemenyRanking = kemenyRankings[0]
        maxKemenyIndex = kemenyRankings[1]
        maximalRankings = deepcopy(other.maximalRankings)
        
        if kemenyRankings == None:
            print('Intantiation error: unable to compute the Kemeny Order !!!')
            print('Digraph order %d is required to be lower than 8!' % n)
            return
        if Debug:
            print(kemenyRankings,other.maximalRankings)
        
        # instatiates a Digraph template
        actions = deepcopy(other.actions)
        Min = Decimal('-1.0')
        Max = Decimal('1.0')
        Med = Decimal('0.0')
        valuationdomain = {'min': Min, 'med': Med, 'max': Max}
        relation = {}
        n = len(actions)
        self.order = n
        for i in range(n):
            x = kemenyRanking[i]
            relation[x] = {}
            for j in range(n):
                y = kemenyRanking[j]
                relation[x][y] = Med
                if i < j:
                    relation[x][y] = Max
                    try:
                        relation[y][x] = Min
                    except:
                        relation[y] = {x: Min}
                elif i > j:
                    relation[x][y] = Min
                    try:
                        relation[y][x] = Max
                    except:
                        relation[y] = {y: Max}

        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.kemenyRanking = kemenyRanking
        self.maxKemenyIndex = maxKemenyIndex
        self.maximalRankings = maximalRankings
        self.kemenyOrder = list(reversed(list(kemenyRanking)))
        if Debug:
            self.showRelationTable()
            print('Kemeny Ranking = ', self.kemenyRanking)

########  instantiates principal scores' ordering

class SlaterOrder(KemenyOrder):
    """
    Instantiates a SlaterOrder by instantiating a *KemenyOrder* from the Condorcet Digraph -the median cut polarised digraph
    given bipolarised digraph- of a given bipolar-valued Digraph instance. 
    """
    def __init__(self,other,orderLimit=7,Debug=False):
        """
        A constructor for generating a linear order
        from a given other digraph by exact enumeration
        """
        from digraphs import PolarisedDigraph
        from copy import copy,deepcopy
        c = PolarisedDigraph(other)
        sl = KemenyOrder(c,orderLimit=orderLimit,Debug=Debug)
        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(sl.valuationdomain)
        self.relation = deepcopy(sl.relation)
        self.slaterOrder = copy(sl.kemenyOrder)
        self.slaterRanking = copy(sl.kemenyRanking)
        self.slaterIndex = copy(sl.maxKemenyIndex)
        self.maximalRankings = copy(sl.maximalRankings)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        
########  instantiates principal scores' ordering

class PrincipalOrder(LinearOrder):
    """
    instantiates the order from the scores obtained by the first
    princiapl axis of the eigen deomposition of the covariance of the
    outdegrees of the valued digraph 'other'.
    """
    def __init__(self,other,Colwise=True,imageType=None,
                 plotFileName="principalOrdering",tempDir=None,Debug=False):
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
        from copy import copy, deepcopy
        from decimal import Decimal
        from tempfile import TemporaryDirectory
        
        Min = other.valuationdomain['min']
        Max = other.valuationdomain['max']
        Med = other.valuationdomain['med']
        actionsList = [x for x in other.actions]
        actionsList.sort()
        n = len(actionsList)
        relation = deepcopy(other.relation)
        with TemporaryDirectory(dir=tempDir) as tempDirName:
            principalScores = other.computePrincipalOrder(Colwise=Colwise,
                                                      imageType=imageType,
                                                      plotFileName=plotFileName,
                                                      tempDir=tempDir,
                                                      Debug=Debug)
        # [ (score1,action_(1)), (score2,action_(2)), ...] 
        if principalScores == None:
            print('Intantiation error: unable to compute the principal Order !!!')
            return
        if Debug:
            print(principalScores)
        # instatiates a Digraph template
        
        g = IndeterminateDigraph(order=n)
        actions = copy(other.actions)
        Min = Decimal('-1.0')
        Max = Decimal('1.0')
        Med = Decimal('0.0')
        valuationdomain = {'min': Min, 'med': Med, 'max': Max}
        relation = deepcopy(other.relation)
        for i in range(n):
            x = principalScores[i][1]
            relation[x] = {}
            for j in range(n):
                y = principalScores[j][1]
                relation[x][y] = Med
                if i < j:
                    relation[x][y] = Min
                    try:
                        relation[y][x] = Max
                    except:
                        relation[y] = {x: Max}
                elif i > j:
                    relation[x][y] = Max
                    try:
                        relation[y][x] = Min
                    except:
                        relation[y] = {x: Min}

        # check principal orientation with ordinal correlation sign
        corr = other.computeOrdinalCorrelation(relation)
        if corr['correlation'] < Decimal('0'):
            ReverseScores = True
            for i in range(n):
                x = principalScores[i][1]
                for j in range(n):
                    y = principalScores[j][1]
                    relation[x][y] = -relation[x][y]
        else:
            ReverseScores = False
        self.name = other.name + '_ranked'        
        self.actions = copy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = valuationdomain
        self.relation = relation
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
        self.principalRanking = self.computeRanking()
        self.principalOrder = self.computeOrder()
        
        if Debug:
            print('Principal Order = ', self.computeOrder())
            print('principal ordered relation table:')
            self.showRelationTable()

#----------test  linearOrders module classes  ----------------
if __name__ == "__main__":
    import sys,array
    from time import time
    from digraphs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from linearOrders import *
    from transitiveDigraphs import *
    from randomPerfTabs import *

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

    Threading = False
    print('*-------- Testing KemenyOrder class -------')
    t = RandomCBPerformanceTableau(numberOfActions=9,numberOfCriteria=13,seed=5)
    #t = PerformanceTableau('testLin')    
    g = BipolarOutrankingDigraph(t,Normalized=True)
    g.showRelationTable()
    print()
    print('==>> net flows ordering:')
    t0 = time()
    nf = NetFlowsOrder(g,Debug=True)
    g.showRelationTable(actionsSubset=nf.netFlowsRanking,Sorted=False)
    print(nf.netFlowsRanking)
    print(nf.netFlowsOrder)
    corr = g.computeOrdinalCorrelation(nf)
    g.showCorrelation(corr)
    print(time()-t0)
    #t.showHTMLPerformanceHeatmap(actionsList=nf.netFlowsRanking,Correlations=True)
    print()
    print('==>> iterated net flows ordering:')
    from linearOrders import IteratedNetFlowsOrder
    t0 = time()
    inf = IteratedNetFlowsOrder(g,Comments=True,Valued=False,Debug=False)
    inf.showRelationTable(actionsSubset=inf.iteratedNetFlowsRanking,Sorted=False)
    print(inf.iteratedNetFlowsRanking)
    print(inf.iteratedNetFlowsOrdering)
    print('netfloes')
    corr = g.computeOrdinalCorrelation(nf)
    g.showCorrelation(corr)
    print(time()-t0)
    print('iterated netflows')
    corr = g.computeOrderCorrelation(inf.iteratedNetFlowsRanking)
    g.showCorrelation(corr)
    corr = g.computeOrderCorrelation(inf.iteratedNetFlowsOrdering)
    g.showCorrelation(corr)

    #t.showHTMLPerformanceHeatmap(actionsList=inf.iteratedNetFlowsRanking,Correlations=True)
    print()
##    print('==>> Kemeny ordering:')
##    t0 = time()
##    ke = KemenyOrder(g,Debug=False,orderLimit=9)
##    #g.showRelationTable()
##    try:
##        print(ke.kemenyRanking)
##        print(ke.kemenyOrder)
##        corr = g.computeOrdinalCorrelation(ke)
##        ke.showCorrelation(corr)
##        print(ke.maximalRankings)
##        print(time()-t0)
##    except:
##        pass
##    print()
##    print('==>> slater ordering:')
##    sl = SlaterOrder(g,Debug=False,orderLimit=9)
##    #g.showRelationTable()
##    try:
##        print(sl.slaterRanking)
##        print(sl.slaterOrder)
##        corr = g.computeOrdinalCorrelation(sl)
##        sl.showCorrelation(corr)
##        print(sl.maximalRankings)
##        print(time()-t0)
##    except:
##        pass
##    print()
     
##    print('==>> principal ordering:')
##    t0 = time()    
##    pri = PrincipalOrder(g,tempDir=None)
##    g.showRelationTable(actionsSubset=pri.principalRanking)
##    print(pri.principalRanking)
##    print(pri.principalOrder)
##    print(g.computeOrdinalCorrelation(pri))
##    print(time()-t0)
##    print()
##    # print('==>> out flows ordering:')
##    # t0 = time()
##    # of = OutFlowsOrder(g)
##    # g.showRelationTable(actionsSubset=of.outFlowsRanking)
##    # print(of.outFlowsRanking)
##    # print(of.outFlowsOrder)
##    # print(g.computeOrdinalCorrelation(of))
##    # print(time()-t0)
##    # print()
##    print('==>> Copeland ordering:')
##    t0 = time()
##    cop = CopelandOrder(g,Comments=True)
##    g.showRelationTable(actionsSubset=cop.copelandRanking)
##    print(cop.copelandRanking)
##    print(cop.copelandOrder)
##    print(g.computeOrdinalCorrelation(cop))
##    print(time()-t0)
##    print()
##    print('==>> Kohler ordering:')
##    t0 = time()
##    ko = KohlerOrder(g)
##    g.showRelationTable(actionsSubset=ko.kohlerRanking)
##    print(ko.kohlerRanking)
##    print(ko.kohlerOrder)
##    print(g.computeOrdinalCorrelation(ko))
##    print(time()-t0)
##    print()
##    print('==>> ranked pairs ordering:')
##    t0 = time()
##    rp = RankedPairsOrder(g)
##    g.showRelationTable(actionsSubset=rp.rankedPairsRanking)
##    print(rp.rankedPairsRanking)
##    print(rp.rankedPairsOrder)
##    print(g.computeOrdinalCorrelation(rp))
##    print(time()-t0)
##    print()
##    print('==>> Leximin ordering:')
##    le = RankedPairsOrder((-g),Leximin=True)
##    g.showRelationTable()
##    print(le.rankedPairsOrder)
##    print((-g).computeOrdinalCorrelation(le))

    
##    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
##                                   numberOfActions=200)
##    t.saveXMCDA2('test')
##    t = XMCDA2PerformanceTableau('uniSorting')
##    #t = XMCDA2PerformanceTableau('test')
##    g = BipolarOutrankingDigraph(t,Normalized=True,Threading=Threading)
##    ko = KohlerOrder(g)
##    ko.showOrdering()
##    bko = BoostedKohlerOrder(t,strategy="average",Threading=Threading,Debug=False)
##    #qr = QuantilesRankingDigraph(t,100,Threading=Threading)
##    bko.showSorting()
##    bko.showOrdering()
##    #bko.showQuantileOrdering()
##    #bko.showHTMLRelationTable(actionsList=bko.computeOrder())
##    print(bko.runTimes)
##    print(g.computeOrdinalCorrelation(bko))
##    #print(qr.runTimes)
##    #print(g.computeOrdinalCorrelation(qr))
##    print(ko.computeOrdinalCorrelation(bko))
##    QuantilesRankingDigraph.exportSortingGraphViz(bko)
##    nf = NetFlowsOrder(g)
##    #nf.showRelationTable()
##    nf.showOrdering()
##    print(g.computeOrdinalCorrelation(nf))
    
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
