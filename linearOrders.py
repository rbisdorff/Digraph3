#!/usr/bin/env python3
"""
Python3 implementation of linear orders
Dependancy: digraphs module
Copyright (C) 2011-2025  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: Python 3.13.2 $"


# from digraphsTools import *
from digraphs import *
from linearOrders import *

#--------- Decimal precision --------------
from decimal import Decimal

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
        if prudentBetaLevel is None:
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
    def __init__(self):
        print('Abstract root class')
        
    def computeRanking(self):
        """
        computes the linear ordering from lowest (best, rank = 1) to highest (worst rank=n)
        of an instance of the LinearOrcer class by sorting by outdegrees (gamma[x][0]).
        """
        from operator import itemgetter
        degrees = []
        for x in self.actions:
            degrees.append((len(self.gamma[x][0]),x))
        degrees.sort(reverse=True,key=itemgetter(0))
        ranking = []
        for x in degrees:
            ranking.append(x[1])
        return ranking

    def computeOrder(self):
        """
        computes the linear ordering from lowest (worst) to highest (best)
        of an instance of the LinearOrcer class by sorting by indegrees (gamma[x][1]).
        """
        from operator import itemgetter
        degrees = []
        for x in self.actions:
            degrees.append((len(self.gamma[x][1]),x))
        degrees.sort(reverse=True,key=itemgetter(0))
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
        linear_order = self.computeOrder()
        html = ''
        html += '<table border = 1>'
        html += '<tr bgcolor="#9acd32"><th colspan="2">Ranking result</th></tr>'
        for x in linear_order:
            try:
                name = self.actions[x]['name']
            except:
                name = x
            html += '<tr><th bgcolor="#FFF79B">%s</th><td>%s</td></tr>' \
                                               % (x,name)
        html += '</table>'
        return html

    def htmlRanking(self):
        """
        returns the html encoded presentation of a linear order
        """
        linear_ranking = self.computeRanking()
        html = ''
        html += '<table border = 1>'
        html += '<tr bgcolor="#9acd32"><th colspan="2">Ranking result</th></tr>'
        for x in linear_ranking:
            try:
                name = self.actions[x]['name']
            except:
                name = x
            html += '<tr><th bgcolor="#FFF79B">%s</th><td>%s</td></tr>' \
                                              % (x,name)
        html += '</table>'
        return html
    
    def exportDigraphGraphViz(self,fileName=None, firstChoice=set(),
                              bestChoice=set(),lastChoice=set(),
                              worstChoice=set(),Comments=True,
                              graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName,firstChoice=set(),
                               bestChoice=bestChoice,lastChoice=set(),
                               worstChoice=worstChoice,
                               Comments=Comments,graphType=graphType,
                               graphSize=graphSize)

    def exportGraphViz(self,fileName=None, isValued=True,
                       firstChoice=set(),lastChoice=set(),
                       bestChoice=set(),worstChoice=set(),
                       Comments=True,graphType='png',
                       graphSize='7,7',bgcolor='cornsilk'):
        """
        export GraphViz dot file  for linear order drawing filtering.
        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        #actionkeys = [x for x in self.actions]
        actionkeys = self.computeOrder()
        n = len(actionkeys)
        relation = self.relation
        Med = self.valuationdomain['med']
        i = 0
        if fileName is None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        if firstChoice != set():
            bestChoice = firstChoice
        if bestChoice != set():
            rankBestString = '{rank=max; '
        if lastChoice != set():
            worstChoice = lastChoice
        if worstChoice != set():
            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        if bgcolor is not None:
            fo.write('graph [ bgcolor = %s, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' \
                                % (bgcolor))
        else:
            fo.write('graph [ fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')          
        fo.write('\\nDigraph3 (graphviz), R. Bisdorff, 2015", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            nodeName = str(actionkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            node += '];\n'         
            fo.write(node)
        for i in range(n-1):
            for j in range(i+1,i+2):
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
                        KemenyIndex += float(other.relation[x][y])\
                                       * copysign(1.0,self.relation[x][y])
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
    def __init__(self,numberOfActions=10,
                 Debug=False,OutrankingModel=False,
                 Valued=False,seed=None):
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
class RankedPairsRanking(LinearOrder):
    """
    instantiates the Ranked Pairs Ranking from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,Dual=False,
                 Valued=False,
                 #isExtendedPrudent=False,
                 Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the ranked pairs (Lexmin Dias-Lamboray) rule
        Parameter: isExtendedPrudent 
        """
        from copy import copy, deepcopy
        from operator import itemgetter
        # construct ranked pairs

        if Dual:
            other = DualDigraph(other)
        if Debug:
            other.showRelationTable()
            
        relation = other.relation
##        actions = [x for x in other.actions]
##        actions.sort()
        actions = other.actions
        n = len(actions)

        isValued = False # obsolete
        
        listPairs = []
        for x in actions:
            for y in (z for z in actions if z != x):
                linkCharacteristic = relation[x][y]-relation[y][x]
                listPairs.append((linkCharacteristic,(x,y),x,y))
        listPairs.sort(key=itemgetter(0),reverse=True)
##                listPairs.append((-linkCharacteristic,(x,y),x,y))
##        listPairs.sort(reverse=True)
        if Debug:
            print(listPairs)
    
        g = IndeterminateDigraph(order=n)
        g.actions = actions
        if isValued:
            g.valuationdomain = {'min':Decimal('-3'),
                                 'med': Decimal('0'),
                                 'max': Decimal('3')}
        else:
            g.valuationdomain = {'min':Decimal('-1'),
                                 'med': Decimal('0'),
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
        isValued=False # obsolete
        for pair in listPairs:
            if Debug:
                print(pair)
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
                Detected = g.detectChordlessCircuits()
                if Detected:
                    if Debug:
                        print('Circuit detected !!')
                    g.relation[x][y] = relxy
                    g.relation[y][x] = relyx         
                else:
                    if Debug:
                        print('added: (%s,%s) characteristic: %.2f (%.1f)'\
                              % (x,y, other.relation[x][y],g.relation[x][y]))
                        print('added: (%s,%s) characteristic: %.2f (%.1f)'\
                              % (y,x, other.relation[y][x],g.relation[y][x]))

        
        self.name = other.name + '_ranked'        
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        if Valued:
            self.valuationdomain = other.valuationdomain
        else:
            self.valuationdomain = g.valuationdomain
##        if Leximin:
##            self.relation = (-g).relation
##        else:
        self.relation = g.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        #self.rankedPairsOrder = self.computeOrder()
        if Dual: # inverting ranking and order
            rankedPairsOrder = self.computeRanking()
            self.rankedPairsOrder = rankedPairsOrder
            rankedPairsRanking = self.computeOrder()
            #self.rankedPairsRanking = list(reversed(rankedPairsOrder))
            self.rankedPairsRanking = rankedPairsRanking
        else:
            rankedPairsRanking = self.computeRanking()
            self.rankedPairsRanking = rankedPairsRanking
            rankedPairsOrder = self.computeOrder()
            #self.rankedPairsOrder = list(reversed(rankedPairsRanking))
            self.rankedPairsOrder = rankedPairsOrder

        if Valued:
            self.relation = other.computeValuedRankingRelation(rankedPairsRanking)
    
        if Debug:
            print('Ranked Pairs Ranking = ', self.rankedPairsRanking)

class RankedPairsOrder(RankedPairsRanking):
    """
    Dummy for RankedPairsRanking class
    """
#----------------  
class KohlerRanking(LinearOrder):
    """
    instantiates the Kohler Order from
    a given bipolar-valued Digraph instance.

    The ranking and ordering results are stored respectively in
    the *self.kohlerRanking* and the *self.kohlerOrder* attributes.

    

    .. note:: The Kohler ranking rule is *not* invariant under the codual transform
    
    """
    def __init__(self,other,
                 Valued=False,
                 CoDual=False,Debug=False,Comments=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Kohler rule.

        When *Valued==True*, the ranked relation keeps the concordantly
        riented other outranking characteristic values.
        The discordant characteritic values are set to the indeterminate value.

        .. note:: The Kohler ranking rule is *not* invariant under the codual transform
        
        """
        from copy import copy, deepcopy
        from collections import OrderedDict
        
        # construct ranked pairs
        if CoDual:
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
                
            
        actionsList = [x for x in other.actions]
        #actions.sort()
        n = len(actionsList)
        
        # instatiates a Digraph template
        g = IndeterminateDigraph(order=n)
        g.actions = other.actions
        g.valuationdomain = {'min':Decimal('-1'),
                             'med': Decimal('0'),
                             'max': Decimal('1')}
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
        self.kohlerOrder = list(reversed(kohlerRanking))
        
        if Debug:
            print('Kohler ranks: ', kohlerRanking)

        n = len(g.actions)
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        Max = g.valuationdomain['max']
        if Valued:
            for i in range(n):
                for j in range(i+1,n):
                    x = kohlerOrder[i][1]
                    y = kohlerOrder[j][1]
                    g.relation[x][y] = max(Med,other.relation[x][y])
                    g.relation[y][x] = min(Med,other.relation[y][x])
        else:
            for i in range(n):
                for j in range(i+1,n):
                    x = kohlerOrder[i][1]
                    y = kohlerOrder[j][1]
                    g.relation[x][y] = Max
                    g.relation[y][x] = Min
            
        self.name = other.name + '_ranked'        
        self.actions = copy(other.actions)
        self.order = len(self.actions)
        if Valued:
            self.valuationdomain = copy(other.valuationdomain)
        else:
            self.valuationdomain = copy(g.valuationdomain)
        self.relation = copy(g.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        #self.kohlerOrder = self.computeOrder()
        if Debug:
            self.showRelationTable()
        if Comments:
            print('Kohler ranking: ', self.kohlerRanking)
            print('Kohler ordering: ', self.kohlerOrder)

class KohlerOrder(KohlerRanking):
    """
    Dummy for KohlerRanking class
    """

class NetFlowsRanking(LinearOrder):
    """
    instantiates the *NetFlows* ranking  and ordering from
    a given bipolar-valued Digraph instance *other*.

    The ranking and ordering results are stored in the *self.netFlowsRanking*,
    respectively *self.netFlowsOrder*, attributes. 

    When *Valued==True*, the ranked relation keeps the concordantly oriented other
    outranking characteristic values. The discordant characteritic values are set
    to the indeterminate value.

    .. note:: The NetFlows ranking rule is invariant under the codual transform
    """
    
    def __init__(self,other,CoDual=False,Valued=False,Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the net flows ordering rule.


        """

        #from copy import deepcopy
        from collections import OrderedDict
        from time import time
        from operator import itemgetter
        from copy import copy

        if Debug:
            Comments=True

        # prepare local variables
        tt = time()
        runTimes = OrderedDict()
        if CoDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = otherCoDual.relation
        else:
            otherRelation = other.relation
        n = len(other.actions)
        actions = other.actions
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,
                           'med': Med,
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        incnetFlows = []
        decnetFlows = []
        if other.valuationdomain['med'] == Med:
            if Debug:
                print('standard')
            for x in actions:
                incxnetFlows = sum((otherRelation[x][y] - otherRelation[y][x])\
                                 for y in actions)
                decxnetFlows = sum((otherRelation[y][x] - otherRelation[x][y])\
                                 for y in actions)
##                xnetflows = sum((otherRelation[x][y])\
##                                 for y in actions)
                incnetFlows.append((incxnetFlows,x))
                decnetFlows.append((decxnetFlows,x))
                if Debug:
                    print(x,incxnetFlows,decxnetFlows)
        else:
            otherMax = other.valuationdomain['max']
            otherMin = other.valuationdomain['min']
            
            for x in actions:
                incxnetFlows = sum((otherRelation[x][y] +\
                                (otherMax - otherRelation[y][x] + otherMin))\
                                 for y in actions)
                decxnetFlows = sum((otherRelation[y][x] +\
                                (otherMax - otherRelation[x][y] + otherMin))\
                                 for y in actions)
                incnetFlows.append((incxnetFlows,x))
                decnetFlows.append((decxnetFlows,x))
                if Debug:
                    print(x,incxnetflows,decxnetFlows)
        # sorting with keeping the actions initial ordering
        # in case of ties
        incnetFlows.sort(key=itemgetter(0))
        decnetFlows.sort(key=itemgetter(0))
        decnetFlows = [(-x[0],x[1]) for x in decnetFlows]
        self.incnetFlowScores = incnetFlows
        self.decnetFlowScores = decnetFlows
        self.netFlows = decnetFlows          # backwards compatibility
        if Comments:
            print('Increasing Net Flows :')
            for x in incnetFlows:
                print( '%s : %.3f' % (x[1],x[0]) )
            print('Decreasing Net Flows :')
            for x in decnetFlows:
                print( '%s : %.3f' % (x[1],x[0]) )

        netFlowsOrder = [x[1] for x in incnetFlows]
        self.netFlowsOrder = netFlowsOrder
        netFlowsRanking = [x[1] for x in decnetFlows]
        self.netFlowsRanking = netFlowsRanking
        if Debug:
            print(self.netFlowsRanking)
            print(self.netFlowsOrder)
        if Comments:
            print('NetFlows Ranking:')
            print(netFlowsRanking)
        runTimes['netFlows'] = time() - tnf

        # init relation
        tr = time()
        actionKeys = [x for x in actions] 
        if Valued:        
            for x in actionKeys:
                xi = netFlowsRanking.index(x)
                selfRelation[x] = {}
                for y in actionKeys:
                    yj = netFlowsRanking.index(y)
                    if xi < yj:
                        selfRelation[x][y] = max(Med, otherRelation[x][y])
                    elif xi == yj:
                        selfRelation[x][y] = Med
                    else:
                        selfRelation[x][y] = min(Med, otherRelation[x][y])
        else:
            for x in actionKeys:
                xi = netFlowsRanking.index(x)
                selfRelation[x] = {}
                for y in actionKeys:
                    yj = netFlowsRanking.index(y)
                    if xi < yj:
                        selfRelation[x][y] = Max
                    elif xi == yj:
                        selfRelation[x][y] = Med
                    else:
                        selfRelation[x][y] = Min            
        runTimes['relation'] = time() - tr      
        
        # store self attributes
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        if not Valued:
            self.valuationdomain = valuationdomain
        else:
            self.valuationdomain = copy(other.valuationdomain)
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Net flow scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.decnetFlowScores:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in self.incnetFlowScores:
                print('%s \t %.2f' %(x[1],x[0]))

class NetFlowsOrder(NetFlowsRanking):
    """
    Dummy for NetFlowsRanking class
    """

class IteratedNetFlowsRanking(LinearOrder):
    """
    instantiates the iterated NetFlows order from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,CoDual=False,Valued=False,
                 Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the iterated NetFlows rules
        """
        from copy import copy, deepcopy
        from collections import OrderedDict
        from operator import itemgetter
        # construct ranked pairs
        if CoDual:
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
        g.valuationdomain = {'min':Decimal('-1'),
                             'med': Decimal('0'),
                             'max': Decimal('1')}
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
            knetFlows.sort(key=itemgetter(0))
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
            knetFlows.sort(key=itemgetter(0))
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

        iteratedNetFlowsRanking = [x for x in rank]
        self.iteratedNetFlowsRanking = iteratedNetFlowsRanking
        iteratedNetFlowsOrdering = [x for x in order]
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
            print('Iterated NetFlows ranking : ', self.iteratedNetFlowsRanking)
            print('Iterated NetFlows ordering: ', self.iteratedNetFlowsOrdering)

class IteratedCopelandRanking(LinearOrder):
    """
    instantiates the iterated Copeland ranking from
    a given bipolar-valued Digraph instance
    """
    def __init__(self,other,CoDual=False,Valued=False,
                 Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the iterated Copeland rules
        """
        from copy import copy, deepcopy
        from collections import OrderedDict
        # construct ranked pairs
        if CoDual:
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
        g.valuationdomain = {'min':Decimal('-1'),
                             'med': Decimal('0'),
                             'max': Decimal('1')}
        g.relation = {}
        for x in g.actions:
            g.relation[x] = {}
            for y in g.actions:
                g.relation[x][y] = g.valuationdomain['med']

        # construct ranking
        actionsList = [x for x in g.actions]
        c = PolarisedDigraph(other)

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
                        kxnetFlows += c.relation[x][y] - c.relation[y][x]
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
                        kxnetFlows += c.relation[x][y] - c.relation[y][x]
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

        iteratedCopelandRanking = [x for x in rank]
        self.iteratedCopelandRanking = iteratedCopelandRanking
        iteratedCopelandOrdering = [x for x in order]
        self.iteratedCopelandOrder = iteratedCopelandOrdering
        
        if Debug:
            print('Iterated Copeland ranks: ', iteratedCopelandRanking)
            print('Iterated Copeland ordering: ', iteratedCopelandOrdering)

        if Valued:
            n = len(g.actions)
            for i in range(n):
                for j in range(i+1,n):
                    x = iteratedCopelandRanking[i]
                    y = iteratedCopelandRanking[j]
                    g.relation[x][y] = rank[x]['Copeland']
                    g.relation[y][x] = -rank[x]['Copeland']
        else:
            n = len(g.actions)
            for i in range(n):
                for j in range(i+1,n):
                    x = iteratedCopelandRanking[i]
                    y = iteratedCopelandRanking[j]
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
            print('Iterated Copelans ranking: ', self.iteratedCopelandRanking)

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
        from operator import itemgetter

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
        valuationdomain = {'min': Min,
                           'med': Med,
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        outFlows = []
        if other.valuationdomain['med'] == Med:
            for x in actions:
                xoutFlows = sum((otherRelation[x][y])\
                                 for y in actions)
                outFlows.append((xoutFlows,x))
        else:
            otherMax = other.valuationdomain['max']
            otherMin = other.valuationdomain['min']
            
            for x in actions:
                xoutFlows = sum((otherRelation[x][y])\
                                 for y in actions)
                outFlows.append((xoutFlows,x))
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        outFlows.sort(reverse=True,key=itemgetter(0))
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
#------------
class PolarisedBachetRanking(LinearOrder):
    """    
    Instantiates the Bachet Ranking and Ordering from a given bipolar-valued *Digraph* instance *other*.

    *Parameters*

        - *orderLimit* : maximal length of the *other.actions* dictionary.

        - *actionsList* : a given ordering of the other.actions dictionary. 

        - *BestQualified*: if True (default) both the given *actionsList* and its reversed version are ranked and the best correlated of both rankings is returned.

        - *randomized*: integer number (default = 0) of random orderings of the other.actions that are ranked and the best correlated is eventually returned.

        - *Optimal*: (False by default) all possible permutations of the given other.actions ordering are ranked and the best correlated ranking is eventually returned.
    

    For each action *x* in *other.actions*, the polarised integer row vector of the *other.relation* attribute without the reflexive terms defines a *Bachet vector* which correponds to a significance weight *rbx* of its **outrankingness credibility**. Similarly, the corresponding polarised integer column vector in the *other.relation* attribute without the reflexive terms defines a *Bachet vector* whose negation correponds to a significance weight *-cbx* of its **not outrankedness credibility**.

    Taking now the sum *rbx + (-cbx)* of both credibilities gives us per action *x* a Bachet fitness score of the statement that *x* may be *first-ranked*. Sorting in decreasing (resp. increasing) order these Bachet fitness scores gives the *Bachet ranking*, respective *ordering*, result. Both results are stored in the *self.bachetRanking* resp. *self.bachetOrder* attribute. 

    Like the Copeland and the NetFlows rules, the Bachet ranking rule is *invariant* under the *codual* transform. The Bachet rule is furthermore, like the Copeland rule, also *Condorcet consistent*, i.e. when the outranking digraph models a linear relation, its Bachet ranking result will be consistent with this linear outranking relation.

    >>> print("*==>> testing BachetRanking Class ----*")
    >>> from outrankingDigraphs import RandomBipolarOutrankingDigraph
    >>> g = RandomBipolarOutrankingDigraph(numberOfActions=9,seed=1)
    >>> from linearOrders import BachetRanking
    >>> print('*---- solely given ordering of the actions')
    >>> ba1 = PolariseBachetRanking(g,BestQualified=False)
    >>> ba1.showScores()
     Bachet scores in descending order
     action 	 score
     a2 	 14768.00
     a8 	 10061.00
     a9 	 9264.00
     a3 	 8211.00
     a6 	 1394.00
     a7 	 1317.00
     a4 	 1294.00
     a5 	 -3846.00
     a1 	 -5849.00
    >>> print(g.computeRankingCorrelation(ba1.bachetRanking))
     {'correlation': 0.3935624213996805, 'determination': 0.408625}
    >>> print('*---- given and reversed ordering of the actions')
    >>> ba2 = PolarisedBachetRanking(g,BestQualified=True)
    >>> ba2.showScores() 
     Bachet scores in descending order
     action 	 score
     a2 	 14768.00
     a8 	 10061.00
     a9 	 9264.00
     a3 	 8211.00
     a6 	 1394.00
     a7 	 1317.00
     a4 	 1294.00
     a5 	 -3846.00
     a1 	 -5849.00
    >>> print(g.computeRankingCorrelation(ba2.bachetRanking))
     {'correlation': 0.46511675333945146, 'determination': 0.408625}
    >>> print('*---- using 10 random ordering and their reversed versions')
    >>> ba3 = PolarisedBachetRanking(g,BestQualified=True,randomized=10)
    >>> ba3.showScores()
     Bachet scores in descending order
     action 	 score
     a2 	 15092.00
     a9 	 8884.00
     a3 	 8533.00
     a8 	 8493.00
     a7 	 1771.00
     a6 	 -246.00
     a4 	 -990.00
     a5 	 -4234.00
     a1 	 -6323.00
    >>> print(g.computeRankingCorrelation(ba3.bachetRanking))
     {'correlation': 0.7585058291696407, 'determination': 0.408625}

    
    .. note::

       Mind that the Bachet numbering system is a positional {-1,0,1} numeral system that is isomorphic to the {0,1,2} base 3 numeral system. A Bachet ranking result is therefore depending on the very ordering of the rows and columns of the *other.relation* attribute when there is a lack of transitivity observed in the relation. It is hence recommended (*BestQualified=True* setting by default) to compute a first Bachet ranking result with the given order of the *other.actions* atribute and a second one with the reversed order. The best qualified of both ranking results is eventually returned.

       Mind also that the integer value range of Bachet numbers gets quickly huge with the length of the given row and column chracteristic vectors. The digraph *orderLimit* parameter is therefore set by default to 50, allowing to tackle integer values in the huge integer range +-358948993845926294385124. When there is need to tackle digraphs of larger order, this *orderLimit* parameter may be adjusted.

       When the ranking result appears suspiciously uncorrelated with the given outranking digraph, it is recommended to set the *randomized* parameter to a positive integer *n*. In this case, *n* random orderings of the decision actions with their reversed versions will be used for generating Bachet rankings. The best correlated ranking will eventually be returned.   
    
    """
    def __init__(self,other,CoDual=False,actionsList=None,
                 orderLimit=50,
                 BestQualified=True,
                 randomized=0,seed=None,
                 Optimal=False,
                 Polarised=False,
                 Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Bachet ordering rule
        """

        # check orderLimit
        if Debug:
            print('orderLimit',orderLimit)
        if other.order > orderLimit:
            print('!!! Error: the given digraph order %d is greater than the allowed orderLimit %d. ' % (other.order,orderLimit))
            return
        from collections import OrderedDict
        from time import time
        from operator import itemgetter
        import arithmetics as ar
        from copy import deepcopy
        if Debug:
            Comments=True
        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if CoDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = deepcopy(otherCoDual.relation)
            if Debug:
                otherCoDual.showRelationTable()
                print(otherCoDual.valuationdomain)
        else:
            otherRelation = deepcopy(other.relation)
        n = len(other.actions)
        if actionsList is None:
            #actions = [x for x in reversed(other.actions)]
            actions = deepcopy(other.actions)
        else:
            actions = OrderedDict()
            for x in actionsList:
                actions[x] = deepcopy(other.actions[x])
        gamma = other.gamma
        selfRelation = {}
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max,
                           'hasIntegerValuation':True}
        # with Condorcet Digraph valuation
        if not Polarised:
            c = PolarisedDigraph(other,level=other.valuationdomain['med'],\
                                 StrictCut=True,KeepValues=False)
            if Debug:
                print(c)
            c.recodeValuation(ndigits=0)
            cRelation = c.relation
        else:
            c = other
            cRelation = otherRelation
        
        runTimes['prepareLocals'] = time()-tt

        if Optimal:
            t0 = time()
                        # with Condorcet Digraph valuation

            maximalRankings = []
            correlation = -1.0
            from digraphsTools import all_perms
            actions = [x for x in other.actions]
            for p in all_perms(actions): 
                ba = PolarisedBachetRanking(c,orderLimit=orderLimit,
                                   Polarised=True,
                                   BestQualified=False,
                                   actionsList=p)
                corr = other.computeRankingCorrelation(ba.bachetRanking)
                if corr['correlation'] > correlation:
                    correlation = corr['correlation']
                    bar = ba
                    if Comments:
                        print(p,correlation,bar.bachetRanking)
            self.runTimes = bar.runTimes
            self.runTimes['bachet'] = time()-t0
            self.name = other.name + '_optimal_ranked'
            self.decBachetScores = bar.decBachetScores
            self.incBachetScores = bar.incBachetScores
            self.bachetRanking = bar.bachetRanking
            self.bachetOrder = bar.bachetOrder
            self.correlation = correlation
            self.actions = bar.actions
            self.order = bar.order
            self.valuationdomain = bar.valuationdomain
            self.relation = bar.relation
            self.gamma = bar.gamma,
            self.notGamma = bar.notGamma
            self.runTimes['totalTime'] = time()-tt
            return

        elif randomized > 0:
            t0 = time()
            import random
            random.seed(seed)
            #from random import shuffle
            randomActions = [x for x in actions]
            correlation = -1.0
            bar = None
            for i in range(randomized):
                random.shuffle(randomActions) 
                ba = PolarisedBachetRanking(c,orderLimit=orderLimit,
                                   Polarised=True,
                                   BestQualified=True,
                                   actionsList=randomActions)
                corr = other.computeRankingCorrelation(ba.bachetRanking)
                if corr['correlation'] > correlation:
                    correlation = corr['correlation']
                    bar = ba
            self.runTimes = bar.runTimes
            self.runTimes['bachet'] = time()-t0
            self.name = other.name + '_randomized_ranked'
            self.decBachetScores = bar.decBachetScores
            self.incBachetScores = bar.incBachetScores
            self.bachetRanking = bar.bachetRanking
            self.bachetOrder = bar.bachetOrder
            self.correlation = correlation
            self.actions = bar.actions
            self.order = bar.order
            self.valuationdomain = bar.valuationdomain
            self.relation = bar.relation
            self.gamma = bar.gamma,
            self.notGamma = bar.notGamma
            self.runTimes['totalTime'] = time()-tt
            return

        else: # not randomized
            
            if BestQualified:
                #Optimal = True
                if Comments:
                    print('Both Bachet ranking with the given order and the reversed order of the decision actions are computed and the best qualified is eventually returned')
            tnf = time()
            incBachetScores = []
            decBachetScores = []
            if BestQualified:
                incBachetRevScores = []
                decBachetRevScores = []

            # with Condorcet Digraph valuation
            #c = PolarisedDigraph(other,level=other.valuationdomain['med'],\
            #                 StrictCut=True,KeepValues=False)
            #if Debug:
            #    print(c)
            #c.recodeValuation(ndigits=0)
            # ## moved above the Optimal section
            if Polarised:
                cRelation = otherRelation
            else:
                cRelation = c.relation


            for x in actions:
                vecx = [int(cRelation[x][y]) for y in actions if y != x]
                vecy = [int(cRelation[y][x]) for y in actions if y != x]
                if Debug:
                    print(vecx,vecy)
                bx = ar.BachetNumber(vector=vecx)
                by = ar.BachetNumber(vector=vecy)
                bScore = bx + (-by)
                #bScore = bx
                #bScore = bx + by
                incBachetScores.append((bScore.value(),x))
                decBachetScores.append((bScore.value(),x))
                if BestQualified:
                    bRevScore = bx.reverse() + (-by.reverse())
                    incBachetRevScores.append((bRevScore.value(),x))
                    decBachetRevScores.append((bRevScore.value(),x))
            # reversed sorting with keeping the actions initial ordering
            # in case of ties
            if Debug:
                print(incBachetScores,decBachetScores)
            incBachetScores.sort(key=itemgetter(0))
            decBachetScores.sort(reverse=True,key=itemgetter(0))
            if BestQualified:
                if Debug:
                    print(incBachetRevScores,decBachetRevScores)
                incBachetRevScores.sort(key=itemgetter(0))
                decBachetRevScores.sort(reverse=True,key=itemgetter(0))

            decBachetScores = [(x[0],x[1]) for x in decBachetScores]
            incBachetScores = [(x[0],x[1]) for x in incBachetScores]               
            #self.decBachetScores = decBachetScores
            #self.incBachetScores = incBachetScores
            if Debug:
                print(incBachetScores,decBachetScores)
            if BestQualified:
                decBachetRevScores = [(x[0],x[1]) for x in decBachetRevScores]
                incBachetRevScores = [(x[0],x[1]) for x in incBachetRevScores]               
                #self.decBachetRevScores = decBachetRevScores
                #self.incBachetRevScores = incBachetRevScores
                if Debug:
                    print(incBachetRevScores,decBachetRevScores)


        if Comments:
            print('Bachet decreasing scores')
            for x in decBachetScores:
                print( '%s : %d' %( x[1],x[0] ) )
            if BestQualified:
                print('reversed Bachet decreasing scores')
                for x in decBachetRevScores:
                    print( '%s : %d' %( x[1],x[0] ) )


        bachetRanking = [x[1] for x in decBachetScores]
        bachetOrder = [x[1] for x in incBachetScores]
        if Debug:
            print(bachetRanking,bachetOrder)

        if BestQualified:
            bachetRevRanking =  [x[1] for x in decBachetRevScores]
            bachetRevOrder = [x[1] for x in incBachetRevScores]
            corr = other.computeRankingCorrelation(bachetRanking)
            corrRev = other.computeRankingCorrelation(bachetRevRanking)
            if corrRev['correlation'] > corr['correlation']:
                bachetRanking = bachetRevRanking
                decBachetScores = decBachetRevScores
                bachetOrder = bachetRevOrder
                incBachetScores = incBachetRevScores

        self.bachetRanking = bachetRanking
        self.bachetOrder = bachetOrder
        self.decBachetScores = decBachetScores
        self.incBachetScores = incBachetScores
        if Comments:
            print('Bachet Ranking:')
            print(bachetRanking)

        runTimes['bachet'] = time() - tnf

        # init relation
        tr = time()
        actionsList = [x for x in actions]
        relation = {}
        for x in actionsList:
            xi = bachetRanking.index(x)
            relation[x] = {}
            #print(x,xi)
            for y in actionsList:
                yj = bachetRanking.index(y)
                #print(x,xi,y,yj,max(Med,cRelation[x][y]) )
                if xi < yj:                    
                    relation[x][y] = Max
                elif xi == yj:
                    relation[x][y] = Med
                else:
                    relation[x][y] = Min
                #print(x,xi,y,yj,relation[x][y] )
        runTimes['relation'] = time() - tr

        # store attributes
        if BestQualified:
            self.name = other.name + '_best_ranked'
        else:
            self.name = other.name + '_ranked'         
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = deepcopy(relation)
        if not Polarised:
            corr = other.computeRankingCorrelation(self.bachetRanking)
            self.correlation = corr['correlation']
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Bachet scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.decBachetScores:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in self.incBachetScores:
                print('%s \t %.2f' %(x[1],x[0]))
         
class PolarisedBachetOrder(PolarisedBachetRanking):
    """
    Dummy for PolarisedBachetRanking class
    """

#------------
class BachetRanking(LinearOrder):
    """    
    Instantiates the Bachet Ranking and Ordering from a given bipolar-valued *Digraph* instance *other*.

    *Parameters*

        - *orderLimit* : maximal length of the *other.actions* dictionary.

        - *actionsList* : a given ordering of the other.actions dictionary. 

        - *BestQualified*: if True (default) both the given *actionsList* and its reversed version are ranked and the best correlated of both rankings is returned.

        - *randomized*: integer number (default = 0) of random orderings of the other.actions that are ranked and the best correlated is eventually returned.

        - *Optimal*: (False by default) all possible permutations of the given other.actions ordering are ranked and the best correlated ranking is eventually returned.
    

    For each action *x* in *other.actions*, the row vector of the *other.relation* attribute without the reflexive terms defines a *Bachet vector* which correponds to a significance weight *rbx* of its **outrankingness credibility**. Similarly, the corresponding column vector in the *other.relation* attribute without the reflexive terms defines a *Bachet vector* whose negation correponds to a significance weight *-cbx* of its **negated outrankedness credibility**.

    Taking now the sum *rbx + (-cbx)* of both credibilities gives us per action *x* a valued Bachet fitness score of the statement that *x* may be *first-ranked*. Sorting in decreasing (resp. increasing) order these Bachet fitness scores gives the *Bachet ranking*, respective *ordering*, result. Both results are stored in the *self.bachetRanking* resp. *self.bachetOrder* attribute. 

    Like the Copeland and the NetFlows rules, the Bachet ranking rule is *invariant* under the *codual* transform. The Bachet rule is however, unlike the Copeland rule, not necessarily  *Condorcet consistent*.

    >>> print("*==>> testing BachetRanking Class ----*")
    >>> from outrankingDigraphs import RandomBipolarOutrankingDigraph
    >>> g = RandomBipolarOutrankingDigraph(numberOfActions=9,seed=1)
    >>> from linearOrders import BachetRanking
    >>> print('*---- solely given ordering and the reverse of the actions')
    >>> ba1 = BachetRanking(g,BestQualified=True)
    >>> ba1.showScores() 
     Bachet scores in descending order
     action 	 score
     a2 	 3126.01
     a5 	 1660.68
     a9 	 1439.05
     a3 	 490.35
     a6 	 288.43
     a4 	 -59.94
     a8 	 -107.58
     a7 	 -270.58
     a1 	 -2948.69
    >>> print(g.computeRankingCorrelation(ba1.bachetRanking))
     {'correlation': 0.6314945107236328, 'determination': 0.408625}
    >>> print('*---- using 100 random orderings and their reversed versions')
    >>> ba2 = BachetRanking(g,randomized=100)
    >>> ba2.showScores()
     Bachet scores in descending order
     action 	 score
     a2 	 3580.93
     a9 	 2725.92
     a5 	 1773.33
     a6 	 672.79
     a8 	 -115.16
     a4 	 -489.13
     a3 	 -652.16
     a7 	 -1102.77
     a1 	 -1550.40
    >>> print(g.computeRankingCorrelation(ba3.bachetRanking))
     {'correlation': 0.7459841609734544, 'determination': 0.408625}

    
    .. note::

       Mind that the Bachet numbering system is a positional {-1,0,1} numeral system that is isomorphic to the {0,1,2} base 3 numeral system. A Bachet ranking result is therefore depending on the very ordering of the rows and columns of the *other.relation* attribute when there is a lack of transitivity observed in the relation. It is hence recommended (*BestQualified=True* setting by default) to compute a first Bachet ranking result with the given order of the *other.actions* atribute and a second one with the reversed order. The best qualified of both ranking results is eventually returned.

       Mind also that the integer value range of Bachet numbers gets quickly huge with the length of the given row and column chracteristic vectors. The digraph *orderLimit* parameter is therefore set by default to 50, allowing to tackle integer values in the huge integer range +-358948993845926294385124. When there is need to tackle digraphs of larger order, this *orderLimit* parameter may be adjusted.

       When the ranking result appears suspiciously uncorrelated with the given outranking digraph, it is recommended to set the *randomized* parameter to a positive integer *n*. In this case, *n* random orderings of the decision actions with their reversed versions will be used for generating Bachet rankings. The best correlated ranking will eventually be returned.   
    
    """
    def __init__(self,other,CoDual=False,actionsList=None,
                 orderLimit=50,
                 BestQualified=True,
                 randomized=0,seed=None,
                 Optimal=False,
                 #Polarised=False,
                 Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Bachet ordering rule
        """

        # check orderLimit
        if Debug:
            print('orderLimit',orderLimit)
        if other.order > orderLimit:
            print('!!! Error: the given digraph order %d is greater than the allowed orderLimit %d. ' % (other.order,orderLimit))
            return
        from collections import OrderedDict
        from time import time
        from operator import itemgetter
        import arithmetics as ar
        from copy import deepcopy
        if Debug:
            Comments=True
        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if CoDual:
            otherCoDual = CoDualDigraph(other)
            otherRelation = deepcopy(otherCoDual.relation)
            if Debug:
                otherCoDual.showRelationTable()
                print(otherCoDual.valuationdomain)
        else:
            otherRelation = deepcopy(other.relation)
        n = len(other.actions)
        if actionsList is None:
            #actions = [x for x in reversed(other.actions)]
            actions = deepcopy(other.actions)
        else:
            actions = OrderedDict()
            for x in actionsList:
                actions[x] = deepcopy(other.actions[x])
        gamma = other.gamma
        selfRelation = {}
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max,
                           'hasIntegerValuation':True}
        # with Condorcet Digraph valuation
##        if not Polarised:
##            c = PolarisedDigraph(other,level=other.valuationdomain['med'],\
##                                 StrictCut=True,KeepValues=False)
##            if Debug:
##                print(c)
##            c.recodeValuation(ndigits=0)
##            cRelation = c.relation
##        else:
        c = other
        cRelation = otherRelation
        
        runTimes['prepareLocals'] = time()-tt

        if Optimal:
            t0 = time()
                        # with Condorcet Digraph valuation

            maximalRankings = []
            correlation = -1.0
            from digraphsTools import all_perms
            actions = [x for x in other.actions]
            for p in all_perms(actions): 
                ba = BachetRanking(c,orderLimit=orderLimit,
                                   #Polarised=True,
                                   BestQualified=False,
                                   actionsList=p)
                corr = other.computeRankingCorrelation(ba.bachetRanking)
                if corr['correlation'] > correlation:
                    correlation = corr['correlation']
                    bar = ba
                    if Comments:
                        print(p,correlation,bar.bachetRanking)
            self.runTimes = bar.runTimes
            self.runTimes['bachet'] = time()-t0
            self.name = other.name + '_optimal_ranked'
            self.decBachetScores = bar.decBachetScores
            self.incBachetScores = bar.incBachetScores
            self.bachetRanking = bar.bachetRanking
            self.bachetOrder = bar.bachetOrder
            self.correlation = correlation
            self.actions = bar.actions
            self.order = bar.order
            self.valuationdomain = bar.valuationdomain
            self.relation = bar.relation
            self.gamma = bar.gamma,
            self.notGamma = bar.notGamma
            self.runTimes['totalTime'] = time()-tt
            return

        elif randomized > 0:
            t0 = time()
            import random
            random.seed(seed)
            #from random import shuffle
            randomActions = [x for x in actions]
            correlation = -1.0
            bar = None
            for i in range(randomized):
                random.shuffle(randomActions) 
                ba = BachetRanking(c,orderLimit=orderLimit,
                                   #Polarised=True,
                                   BestQualified=True,
                                   actionsList=randomActions)
                corr = other.computeRankingCorrelation(ba.bachetRanking)
                if corr['correlation'] > correlation:
                    correlation = corr['correlation']
                    bar = ba
            self.runTimes = bar.runTimes
            self.runTimes['bachet'] = time()-t0
            self.name = other.name + '_randomized_ranked'
            self.decBachetScores = bar.decBachetScores
            self.incBachetScores = bar.incBachetScores
            self.bachetRanking = bar.bachetRanking
            self.bachetOrder = bar.bachetOrder
            self.correlation = correlation
            self.actions = bar.actions
            self.order = bar.order
            self.valuationdomain = bar.valuationdomain
            self.relation = bar.relation
            self.gamma = bar.gamma,
            self.notGamma = bar.notGamma
            self.runTimes['totalTime'] = time()-tt
            return

        else: # not randomized
            
            if BestQualified:
                #Optimal = True
                if Comments:
                    print('Both Bachet ranking with the given order and the reversed order of the decision actions are computed and the best qualified is eventually returned')
            tnf = time()
            incBachetScores = []
            decBachetScores = []
            if BestQualified:
                incBachetRevScores = []
                decBachetRevScores = []

            # with Condorcet Digraph valuation
            #c = PolarisedDigraph(other,level=other.valuationdomain['med'],\
            #                 StrictCut=True,KeepValues=False)
            #if Debug:
            #    print(c)
            #c.recodeValuation(ndigits=0)
            # ## moved above the Optimal section
##            if Polarised:
##                cRelation = otherRelation
##            else:
            cRelation = otherRelation


            for x in actions:
                vecx = [cRelation[x][y] for y in actions if y != x]
                vecy = [cRelation[y][x] for y in actions if y != x]
                if Debug:
                    print(vecx,vecy)
                bx = ar.BachetNumber(vector=vecx)
                by = ar.BachetNumber(vector=vecy)
                bScore = bx + (-by)
                #bScore = bx
                #bScore = bx + by
                incBachetScores.append((bScore.value(),x))
                decBachetScores.append((bScore.value(),x))
                if BestQualified:
                    bRevScore = bx.reverse() + (-by.reverse())
                    incBachetRevScores.append((bRevScore.value(),x))
                    decBachetRevScores.append((bRevScore.value(),x))
            # reversed sorting with keeping the actions initial ordering
            # in case of ties
            if Debug:
                print(incBachetScores,decBachetScores)
            incBachetScores.sort(key=itemgetter(0))
            decBachetScores.sort(reverse=True,key=itemgetter(0))
            if BestQualified:
                if Debug:
                    print(incBachetRevScores,decBachetRevScores)
                incBachetRevScores.sort(key=itemgetter(0))
                decBachetRevScores.sort(reverse=True,key=itemgetter(0))

            decBachetScores = [(x[0],x[1]) for x in decBachetScores]
            incBachetScores = [(x[0],x[1]) for x in incBachetScores]               
            #self.decBachetScores = decBachetScores
            #self.incBachetScores = incBachetScores
            if Debug:
                print(incBachetScores,decBachetScores)
            if BestQualified:
                decBachetRevScores = [(x[0],x[1]) for x in decBachetRevScores]
                incBachetRevScores = [(x[0],x[1]) for x in incBachetRevScores]               
                #self.decBachetRevScores = decBachetRevScores
                #self.incBachetRevScores = incBachetRevScores
                if Debug:
                    print(incBachetRevScores,decBachetRevScores)


        if Comments:
            print('Bachet decreasing scores')
            for x in decBachetScores:
                print( '%s : %.f' %( x[1],x[0] ) )
            if BestQualified:
                print('reversed Bachet decreasing scores')
                for x in decBachetRevScores:
                    print( '%s : %f' %( x[1],x[0] ) )


        bachetRanking = [x[1] for x in decBachetScores]
        bachetOrder = [x[1] for x in incBachetScores]
        if Debug:
            print(bachetRanking,bachetOrder)

        if BestQualified:
            bachetRevRanking =  [x[1] for x in decBachetRevScores]
            bachetRevOrder = [x[1] for x in incBachetRevScores]
            corr = other.computeRankingCorrelation(bachetRanking)
            corrRev = other.computeRankingCorrelation(bachetRevRanking)
            if corrRev['correlation'] > corr['correlation']:
                bachetRanking = bachetRevRanking
                decBachetScores = decBachetRevScores
                bachetOrder = bachetRevOrder
                incBachetScores = incBachetRevScores

        self.bachetRanking = bachetRanking
        self.bachetOrder = bachetOrder
        self.decBachetScores = decBachetScores
        self.incBachetScores = incBachetScores
        if Comments:
            print('Bachet Ranking:')
            print(bachetRanking)

        runTimes['bachet'] = time() - tnf

        # init relation
        tr = time()
        actionsList = [x for x in actions]
        relation = {}
        for x in actionsList:
            xi = bachetRanking.index(x)
            relation[x] = {}
            #print(x,xi)
            for y in actionsList:
                yj = bachetRanking.index(y)
                #print(x,xi,y,yj,max(Med,cRelation[x][y]) )
                if xi < yj:                    
                    relation[x][y] = Max
                elif xi == yj:
                    relation[x][y] = Med
                else:
                    relation[x][y] = Min
                #print(x,xi,y,yj,relation[x][y] )
        runTimes['relation'] = time() - tr

        # store attributes
        if BestQualified:
            self.name = other.name + '_best_ranked'
        else:
            self.name = other.name + '_ranked'         
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = deepcopy(relation)
        #if not Polarised:
        corr = other.computeRankingCorrelation(self.bachetRanking)
        self.correlation = corr['correlation']
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Bachet scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.decBachetScores:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in self.incBachetScores:
                print('%s \t %.2f' %(x[1],x[0]))
         
class BachetOrder(BachetRanking):
    """
    Dummy for BachetRanking class
    """

#-------------
class CopelandRanking(LinearOrder):
    """
    Instantiates the Copeland Ranking and Order from
    a given bipolar-valued Digraph instance *other*.

    When *Gamma* == *True*, the Copeland scores for each action *x* 
    are computed with the help of the *other.gamma* attribute as
    the difference between outdegrees *gamma[x][0]* and indegrees *gamma[x][1]*.
    If *False*, they are computed as the sum of the differences
    between the polarised *other* outranking characteristics.

    The Copeland ranking and the Copeland ordering are stored in
    the attributes *self.copelandRanking* and *self.copelandOrder*.

    When *Valued == *True*, the *other* outranking characteristic values,
    concordant with the Copeland ranking, are kept whereas
    the discordant ones are set to the indeterminate value.

    .. note:: The Copeland ranking rule is invariant under the codual transform
    
    """
    def __init__(self,other,CoDual=False,Gamma=False,
                 Valued=False,
                 Comments=False,Debug=False):
        """
        constructor for generating a linear order
        from a given other digraph following
        the Copeland ordering rule
        """

        #from copy import deepcopy
        from collections import OrderedDict
        from time import time
        from operator import itemgetter
        if Debug:
            Comments=True
        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        if CoDual:
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
        notGamma = other.notGamma
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
                copelandScore = len(gamma[x][0]) + len(gamma[x][1])
                incCopelandScores.append((copelandScore,x))
                decCopelandScores.append((copelandScore,x))
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
                    if x != y:
                        copelandScore += cRelation[x][y] - cRelation[y][x]
                        if Debug:
                            print(x,y,cRelation[x][y],
                                  -cRelation[y][x],copelandScore)
                incCopelandScores.append((copelandScore,x))
                decCopelandScores.append((copelandScore,x))

        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        incCopelandScores.sort(key=itemgetter(0))
        decCopelandScores.sort(reverse=True,key=itemgetter(0))
        self.decCopelandScores = decCopelandScores
        self.incCopelandScores = incCopelandScores
    
        if Comments:
            print('Copeland decreasing scores')
            for x in decCopelandScores:
                print( '%s : %d' %( x[1],int(x[0]) ) )
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
        tr = time()
        actionsList = [x for x in actions]
        relation = {}
        for x in actionsList:
            xi = copelandRanking.index(x)
            relation[x] = {}
            for y in actionsList:
                yj = copelandRanking.index(y)
                if xi < yj:
                    relation[x][y] = max(Med, otherRelation[x][y])
                elif xi == yj:
                    relation[x][y] = Med
                else:
                    relation[x][y] = min(Med, otherRelation[x][y])
        runTimes['relation'] = time() - tr
        
        # store attributes
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Copeland scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.decCopelandScores:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in self.incCopelandScores:
                print('%s \t %.2f' %(x[1],x[0]))
         
class CopelandOrder(CopelandRanking):
    """
    Dummy for CopelandRanking class
    """

########  instantiates optimal linear orderings

# class MedianRanking(LinearOrder):
#     """
#     instantiates the ranking of highest mean marginal correlation and lowest amplitude from
#     a given bipolar-valued Digraph instance of small order 
#     """
#     def __init__(self,other,orderLimit=7,
#                  Threading=False,nbrOfCPUs=1,
#                  Comments=False,Debug=False):
#         """
#         constructor for generating a linear order
#         from a given other digraph by exact enumeration
#         of all permutations of actions.
#         """
#         if other.order > orderLimit:
#             print('Digraph order %d to high. The default limit (7) may be changed with the oderLimit argument.' % (other.order) )
#             return
                  
#         from digraphs import all_perms
#         from copy import copy,deepcopy
#         from decimal import Decimal
        
#         Min = other.valuationdomain['min']
#         Max = other.valuationdomain['max']
#         Med = other.valuationdomain['med']
#         #relation = copy(other.relation)
#         medianRankings = other.computeMedianRanking(orderLimit=orderLimit,
#                                                     Threading=Threading,
#                                                     nbrOfCPUs=nbrOfCPUs,
#                                                     Comments=Comments,
#                                                     Debug=Debug)
#         # [0] = ordered actions list, [1] = maximal marginal corrleation index,
#         # [2] = minimal marginal correlation amplitude,
        
#         medianRanking = medianRankings[0]
#         maxMarginalCorrelation = medianRankings[1]
#         minMarginalCorrelationAmplitude = medianRanking[2]
#         maximalRankings = deepcopy(other.maximalRankings)
        
#         if medianRankings is None:
#             print('Intantiation error: unable to compute a median ranking !!!')
#             print('Digraph order %d is required to be lower than 8!' % n)
#             return
#         if Debug:
#             print(medianRankings,other.maximalRankings)
        
#         # instatiates a Digraph template
#         actions = deepcopy(other.actions)
#         Min = Decimal('-1.0')
#         Max = Decimal('1.0')
#         Med = Decimal('0.0')
#         valuationdomain = {'min': Min, 'med': Med, 'max': Max}
#         relation = {}
#         n = len(actions)
#         self.order = n
#         for i in range(n):
#             x = medianRanking[i]
#             relation[x] = {}
#             for j in range(n):
#                 y = medianRanking[j]
#                 relation[x][y] = Med
#                 if i < j:
#                     relation[x][y] = Max
#                     try:
#                         relation[y][x] = Min
#                     except:
#                         relation[y] = {x: Min}
#                 elif i > j:
#                     relation[x][y] = Min
#                     try:
#                         relation[y][x] = Max
#                     except:
#                         relation[y] = {y: Max}

#         self.name = other.name + '_ranked'        
#         self.actions = actions
#         self.order = n
#         self.valuationdomain = valuationdomain
#         self.relation = relation
#         self.gamma = self.gammaSets()
#         self.notGamma = self.notGammaSets()
#         self.medianRanking = medianRanking
#         self.maxMarginalCorrelation = maxMarginalCorrelation
#         self.minMarginalCorrelationAmplitude = minMarginalCorrelationAmplitude
#         self.maximalRankings = maximalRankings
#         self.medianOrder = list(reversed(list(medianRanking)))
#         if Debug:
#             self.showRelationTable()
#             print('Median Ranking = ', self.medianRanking)

class KemenyRanking(LinearOrder):
    """
    Instantiates the Kemeny Ranking wrt the outranking relation from
    a given bipolar-valued Digraph instance of small order.
    Multiple Kemeny rankings are sorted in decreasing order of their mean marginal correlations
    and the resulting Kemeny ranking is the first one in this list.
    """
    def __init__(self,other,orderLimit=7,Valued=False,Debug=False):
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
##        kemenyRankings = other.computeKemenyRanking(orderLimit=orderLimit,Debug=False)
##        # [0] = ordered actions list, [1] = maximal Kemeny index
##        
##        kemenyRanking = kemenyRankings[0]
##        maxKemenyIndex = kemenyRankings[1]
##        maximalRankings = deepcopy(other.maximalRankings)
        kemenyRankings = other.computeKemenyRanking(orderLimit=orderLimit,Debug=False)
        if kemenyRankings is None:
            print('Intantiation error: unable to compute the Kemeny Order !!!')
            print('Digraph order %d is required to be lower than 8!' % n)
            return
##        elif len(other.maximalRankings) == 1:
##            kemenyRanking = kemenyRankings[0]
##            maxKemenyIndex = kemenyRankings[1]
##            maximalRankings = list(other.maximalRankings)
        else:
            from operator import itemgetter
            orderedMaximalRankings = []
            for r in other.maximalRankings:
                try:
                    margCorr = other.computeRankingConsensusQuality(r)
                except:
                    kemenyRanking = kemenyRankings[0]
                    maxKemenyIndex = kemenyRankings[1]
                    maximalRankings = list(other.maximalRankings)
                    break
                orderedMaximalRankings.append(('%.4f' % (margCorr[1]), '%.4f' \
                                               % (margCorr[2]),r))
            if len(orderedMaximalRankings) > 1:
                s = sorted(orderedMaximalRankings,key=itemgetter(1))
                s = sorted(s,key=itemgetter(0),reverse=True)
                orderedMaximalRankings = s
                kemenyRanking = orderedMaximalRankings[0][2]
            else:
                kemenyRanking = kemenyRankings[0]
            maxKemenyIndex = kemenyRankings[1]
            maximalRankings = list(other.maximalRankings)
            
        if Debug:
            print(kemenyRankings,maximalRankings,orderedMaximalRankings)
        
        # instatiates a Digraph template
        actions = deepcopy(other.actions)
        Min = Decimal('-1.0')
        Max = Decimal('1.0')
        Med = Decimal('0.0')
        valuationdomain = {'min': Min, 'med': Med, 'max': Max}
        if not Valued:
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
        else:
            relation = other.computeValuedRankingRelation(kemenyRanking)

        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = len(actions)
        self.valuationdomain = valuationdomain
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.kemenyRanking = kemenyRanking
        self.maxKemenyIndex = maxKemenyIndex
        self.maximalRankings = maximalRankings
        self.orderedMaximalRankings = orderedMaximalRankings
        self.kemenyOrder = list(reversed(list(kemenyRanking)))
        if Debug:
            self.showRelationTable()
            print('Kemeny Ranking = ', self.kemenyRanking)


class KemenyOrder(KemenyRanking):
    """
    Dummy class
    """

class SlaterRanking(KemenyRanking):
    """
    Instantiates a Slater ranking by instantiating a *KemenyRanking* from the Condorcet Digraph -the median cut polarised digraph- of a given bipolar-valued Digraph instance. 
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

class SlaterOrder(SlaterRanking):
    """
    Dummy class
    """
        
########  instantiates principal scores' ordering

class PrincipalOrder(LinearOrder):
    """
    instantiates the order from the scores obtained by the first
    princiapl axis of the eigen deomposition of the covariance of the
    outdegrees of the valued digraph 'other'.
    """
    def __init__(self,other,Colwise=True,imageType=None,
                 plotFileName="principalOrdering",
                 tempDir=None,Comments=False,Debug=False):
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
        from operator import itemgetter
        
        Min = other.valuationdomain['min']
        Max = other.valuationdomain['max']
        Med = other.valuationdomain['med']
        actionsList = [x for x in other.actions]
        actionsList.sort()
        n = len(actionsList)
        relation = deepcopy(other.relation)
        with TemporaryDirectory(dir=tempDir) as tempDirName:
            principalScores = other.computePrincipalScores(Colwise=Colwise,
                                                      imageType=imageType,
                                                      plotFileName=plotFileName,
                                                      tempDir=tempDir,
                                                      Debug=Debug)
        # [ (score1,action_(1)), (score2,action_(2)), ...] 
        if principalScores is None:
            print('Intantiation error: unable to compute the principal Order !!!')
            return
        if Debug:
            print(principalScores)
        self.principalScores = principalScores
        if Comments:
            for x in principalScores:
                print('%s: %-3f' % (x[1],x[0]) )
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
                self.principalColwiseScores.sort(reverse=True,key=itemgetter(0))
            else:
                self.principalRowwiseScores =\
                    [(-x,y) for (x,y) in principalScores]
                self.principalRowwiseScores.sort(reverse=True,key=itemgetter(0))
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.principalRanking = self.computeRanking()
        self.principalOrder = self.computeOrder()
        
        if Debug:
            print('Principal Order = ', self.computeOrder())
            print('principal ordered relation table:')
            self.showRelationTable()

##################################################### 
#----------test  linearOrders module classes  ----------------
#        for testing ongoing developmens
####################################
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
    * Digraph3 linearOrders module                     *
    * Copyright (C) 2011-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)
    import random
    from time import time
    print('*-------- Testing class and methods -------')

    Threading = False
    res = open('testrandomized.csv','w')
    res.write('"seed","ba1","cop","ba2","nf"\n')
    sampleSize = 1
    #t = Random3ObjectivesPerformanceTableau(numberOfActions=10,seed=1)
    for sample in range(sampleSize):
        print(sample)
        seed = random.randint(1,1000000)
        seed = 1
    ##    t = CircularPerformanceTableau()
        #t.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=5)
        #t = PerformanceTableau('testLin')
        t = RandomCBPerformanceTableau(numberOfActions=7,
                                       numberOfCriteria=13,seed=20)
        g = BipolarOutrankingDigraph(t)
        #g = RandomDigraph(order=7)
        revba1 = [x for x in reversed(g.actions)]
        ba1 = BachetRanking(g,CoDual=True,
                            orderLimit=75,BestQualified=True,
                            Comments=True,Debug=True,
                            actionsList=g.actions,
                            )
        #print(ba1)
        corrba1 = g.computeRankingCorrelation(ba1.bachetRanking)
        print('ba1',ba1.bachetRanking,corrba1)
        cop = CopelandRanking(g,Comments=False,Gamma=False)
        print(cop.copelandRanking)
        corrcop = g.computeRankingCorrelation(cop.copelandRanking)
        print('cop',cop.copelandRanking,corrcop)
        nf = NetFlowsRanking(g)
        corrnf = g.computeRankingCorrelation(nf.netFlowsRanking)
        print('nf',nf.netFlowsRanking,corrnf)
        ke = KemenyRanking(g,orderLimit=9)
        corrke = g.computeRankingCorrelation(ke.kemenyRanking)
        print('ke',ke.kemenyRanking,corrke)
        randomActions = [x for x in g.actions]
        #print(randomActions)
        random.shuffle(randomActions)
        #revba1 = [x for x in reversed(ba1.bachetRanking)]
        revba2 = [x for x in reversed(g.actions)]
        #print(randomActions)
        #print(revba1)
        ba2 = BachetRanking(g,Comments=False,
                            CoDual=True,
                            randomized=100,seed=11,
                            #actionsList=g.actions,
                            )
        #print(ba2)
        corrba2 = g.computeRankingCorrelation(ba2.bachetRanking)
        print('ba2',ba2.bachetRanking,corrba2)
        ba3 = BachetRanking(g,Comments=False,BestQualified=False,
                            CoDual=True,
                            Optimal=True,Debug=True,
                            )
        corrba3 = g.computeRankingCorrelation(ba3.bachetRanking)
        print('ba3',ba3.bachetRanking,corrba3)
        print('%d,%.4f,%.4f,%.4f,%.4f\n' % (seed,corrba1['correlation'],
                                           corrcop['correlation'],
                                        corrba2['correlation'],
                                        corrnf['correlation']) )
        res.write('%d,%.4f,%.4f,%.4f,%.4f\n' % (seed,corrba1['correlation'],
                                           corrcop['correlation'],
                                        corrba2['correlation'],
                                        corrnf['correlation']) )
    res.close()
        
    
     
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
        
    print('*************************************')
    print('* R.B.                              *')
    print('* $Revision: Python3.10 $           *')                   
    print('*************************************')

#############################
