#!/Usr/bin/env python3

"""
Python3+ implementation of the digraphs module, root module of the Digraph3 resources.

Copyright (C) 2006-2019  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""

#######################

__version__ = "Branch: 3.5 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

from digraphsTools import *
from digraphs import *
from perfTabs import *
from randomPerfTabs import *

# #----------XML handling class obsolete -----------------
# try:
#     from xml.sax import *
# except:
#     print('XML extension will not work with this Python version!')

# class _XMLDigraphHandler(ContentHandler):
#     """
#     A private handler to deal with digraphs stored in XML format.
#     """

#     inName = 0
#     digraphName = ''
#     inAction = 0
#     actionName = ''
#     actions = []
#     iAction = ''
#     tAction = ''
#     inMin = 0
#     minText = ''
#     inMax = 0
#     maxText = ''
#     inValue = 0
#     valueText = ''
#     valuationdomain = {}
#     relation = {}


#     def startElement(self,nodeName,attrs):
#         if nodeName == 'digraph':
#             self.category = attrs.get("category", "")
#             self.subcategory = attrs.get("subcategory", "")

#         if nodeName == 'name':
#             self.inName = 1

#         if nodeName == 'nodes':
#             self.actions = []

#         if nodeName == 'node':
#             self.actionName = ''
#             self.inAction = 1

#         if nodeName == 'min':
#             self.inMin = 1

#         if nodeName == 'max':
#             self.inMax = 1

#         if nodeName == 'relation':
#             self.relation = {}
#             for x in self.actions:
#                 self.relation[x] = {}

#         if nodeName == 'i':
#             self.actionName = ''
#             self.inAction = 1

#         if nodeName == 't':
#             self.actionName = ''
#             self.inAction = 1

#         if nodeName == 'v':
#             self.valueText = ''
#             self.inValue = 1


#     def endElement(self,nodeName):

#         if nodeName == 'name':
#             self.inName = 0
#             self.name = str(self.digraphName)

#         if nodeName == 'node':
#             self.actions.append(str(self.actionName))
#             self.inAction = 0

#         if nodeName == 'min':
#             self.inMin = 0
#             self.valuationdomain['min'] = eval(self.minText)

#         if nodeName == 'max':
#             self.inMax = 0
#             self.valuationdomain['max'] = eval(self.maxText)

#         if nodeName == 'i':
#             self.inAction = 0
#             self.iAction = str(self.actionName)

#         if nodeName == 't':
#             self.inAction = 0
#             self.tAction = str(self.actionName)

#         if nodeName == 'v':
#             self.inValue = 0

#         if nodeName == 'arc':
#             self.relation[self.iAction][self.tAction] = eval(self.valueText)

#     def characters(self, ch):
#         if self.inName:
#             self.digraphName += ch
#         if self.inAction:
#             self.actionName += ch
#         if self.inMin:
#             self.minText += ch
#         if self.inMax:
#             self.maxText += ch
#         if self.inValue:
#             self.valueText += ch


#----------Digraph classes -----------------

class Digraph(object):
    
    """
    Genuine root class of all Digraph3 modules.
    See `tutorial working with the digraphs module <http://leopold-loewenheim.uni.lu/docDigraph3/tutorial.html#digraph-object-structure>`_ 

    All instances of the :py:class:`digraphs.Digraph` class contain at least the following components: 

    1. A collection of digraph nodes called **actions** (decision alternatives): a list, set or (ordered) dictionary of nodes with 'name' and 'shortname' attributes,
    2. A logical characteristic **valuationdomain**, a dictionary with three decimal entries: the minimum (-1.0, means certainly false), the median (0.0, means missing information) and the maximum characteristic value (+1.0, means certainly true),
    3. The digraph **relation** : a double dictionary indexed by an oriented pair of actions (nodes) and carrying a characteristic value in the range of the previous valuation domain,
    4. Its associated **gamma function** : a dictionary containing the direct successors, respectively predecessors of each action, automatically added by the object constructor,
    5. Its associated **notGamma function** : a dictionary containing the actions that are not direct successors respectively predecessors of each action, automatically added by the object constructor.

    A previously stored :py:class:`digraphs.Digraph` instance may be reloaded with the *file* argument::
    
        >>> from randomDigraphs import RandomValuationDigraph
        >>> dg = RandomValuationDigraph(order=3,Normalized=True,seed=1)
        >>> dg.save('testdigraph')
        Saving digraph in file: <testdigraph.py> 
        >>> from digraphs import Digraph
        >>> dg = Digraph(file='testdigraph') # without the .py extenseion
        >>> dg.__dict__
        {'name': 'testdigraph',
        'actions': {'a1': {'name': 'random decision action', 'shortName': 'a1'},
                    'a2': {'name': 'random decision action', 'shortName': 'a2'},
                    'a3': {'name': 'random decision action', 'shortName': 'a3'}},
        'valuationdomain': {'min': Decimal('-1.0'), 'med': Decimal('0.0'),
                                'max': Decimal('1.0'), 'hasIntegerValuation': False,},
        'relation': {'a1': {'a1': Decimal('0.0'), 'a2': Decimal('-0.66'), 'a3': Decimal('0.44')},
                     'a2': {'a1': Decimal('0.94'), 'a2': Decimal('0.0'), 'a3': Decimal('-0.84')},
                     'a3': {'a1': Decimal('-0.36'), 'a2': Decimal('-0.70'), 'a3': Decimal('0.0')}},
        'order': 3,
        'gamma': {'a1': ({'a3'}, {'a2'}), 'a2': ({'a1'}, set()), 'a3': (set(), {'a1'})},
        'notGamma': {'a1': ({'a2'}, {'a3'}),
                     'a2': ({'a3'}, {'a1', 'a3'}),
                     'a3': ({'a1', 'a2'}, {'a2'})}}
        >>>

    """

    def __repr__(self):
        """
        Default presentation method for Digraph instances.
        """
        reprString = '*------- Digraph instance description ------*\n'
        reprString += 'Instance class      : %s\n' % self.__class__.__name__
        reprString += 'Instance name       : %s\n' % self.name
        reprString += 'Digraph Order       : %d\n' % self.order
        reprString += 'Digraph Size        : %d\n' % self.computeSize()
        reprString += 'Valuation domain    : [%.2f;%.2f]\n'\
                      % (self.valuationdomain['min'],self.valuationdomain['max'])
        reprString += 'Determinateness (%%) : %.2f\n' % self.computeDeterminateness(InPercents=True)
        reprString += 'Attributes          : %s\n' % list(self.__dict__.keys())
       
        return reprString
    
    def __init__(self,file=None,order=7):
        #import digraphs,sys,copy
        from randomDigraphs import RandomValuationDigraph
        from decimal import Decimal
        if file == None:
            g = RandomValuationDigraph(order=order)
            self.name = g.name
            self.actions = g.actions
            self.order = len(self.actions)
            self.valuationdomain = g.valuationdomain
            self.convertValuationToDecimal()
            self.relation = g.relation
            self.convertRelationToDecimal()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        else:
            fileName = file+'.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'), argDict)
            self.name = file
            try:
                self.actions = argDict['actions']
            except: # for compatibility with Digraph2 versions
                self.actions = argDict['actionset']
            self.order = len(self.actions)
            self.valuationdomain = argDict['valuationdomain']
            self.convertValuationToDecimal()
            self.relation = argDict['relation']
            self.convertRelationToDecimal()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        try:
            self.reflections = argDict['reflections']
            self.rotations = argDict['rotations']
        except:
            pass

    def __neg__(self):
        """
        Make the negation operator -self available for Digraph instances. Returns a DualDigraph instance of self.
        """
        new = DualDigraph(self)
        new.__class__ = self.__class__
        return new

    def __invert__(self):
        """
        Make the inverting operator ~self available for Digraph instances. Returns a ConverseDigraph instance of self.
        """
        new = ConverseDigraph(self)
        new.__class__ = self.__class__
        return new

#-----------Dias/Castonguay/Longo/Jradi--------*
    
    def _triplets(self,Comments=False,Debug=False):
        """ p.15 """
        Med = self.valuationdomain['med']
        tG = []
        self.circuitsList = []
        for u in self.actions:
            outAsymGammaU = self.gamma[u][0] - self.gamma[u][1]
            inAsymGammaU = self.gamma[u][1] - self.gamma[u][0]
            for x in outAsymGammaU:
                for y in inAsymGammaU:
                    if x != y:
                        if str(u) < str(x) and str(u) < str(y):
##                            if Debug:
##                                print('x,u,y',x,u,y)
                            if self.relation[y][x] <= Med and\
                               self.relation[x][y] <= Med:
                                if Comments:
                                    print('Initial triplet: ',x,u,y)
                                tG.append((x,u,y))
                            elif self.relation[x][y] > Med and\
                              self.relation[y][x] <= Med:
                                circ = [y,u,x]
                                if Comments:
                                    print('Circuit certificate:', circ)
                                self.circuitsList.append((circ,frozenset(circ)))
        return tG

    #@timefn
    def computeChordlessCircuitsMP(self,Odd=False,\
                                   Threading=False,nbrOfCPUs=None,\
                                   Comments=False,Debug=False):
        """ 
        Multiprocessing version of computeChordlessCircuits().
        
        Renders the set of all chordless odd circuits detected in a digraph.
        Result (possible empty list) stored in <self.circuitsList>
        holding a possibly empty list tuples with at position 0 the
        list of adjacent actions of the circuit and at position 1
        the set of actions in the stored circuit.
        Inspired by Dias, Castonguay, Longo, Jradi, Algorithmica (2015).

        Returns a possibly empty list of tuples (circuit,frozenset(circuit)).

        If Odd == True, only circuits of odd length are retained in the result. 
        """

        tG = self._triplets(Comments=Comments)
        if Comments:
            print('There are %d starting triplets !' % len(tG) )
        blocked = {}
        for x in self.actions:
            blocked[x] = 0
        self.blocked = blocked
        if Threading:
            self.Odd = Odd
            self.Comments = Comments
            self.Debug = Debug
            from multiprocessing import Pool
            from os import cpu_count
            if nbrOfCPUs == None:
                nbrOfCPUs= cpu_count()
            with Pool(nbrOfCPUs) as proc:   
                circuits = proc.map(self._computeChordlessPathsFromInitialTriplet,tG)
                #print(circuits)
            for i in range(len(tG)):
                if Debug:
                    print(i,circuits[i])
                if circuits[i] != []:
                    for circ in circuits[i]:
                        #print(circ)
                        self.circuitsList.append(circ)
        else:
            for p in tG:
                u = p[1]
##                if Debug:
##                    print('===>>>',p,u)
                gammaU = (self.gamma[u][1] | self.gamma[u][0])
                for x in gammaU:
                    #print(x)
                    self.blocked[x] += 1
                self._ccVisit(p,u,Odd=Odd,Comments=Comments)
                for x in gammaU:
                    if self.blocked[x] > 0:
                        self.blocked[x] -= 1
        if Debug:
            print(self.circuitsList)
        return self.circuitsList

    def _computeChordlessPathsFromInitialTriplet(self,p):
        if self.Comments:
            print('===>> thread : ',p)
        Debug = self.Debug
        u = p[1]
        #blocked = self.blocked
        blocked = {}
        for x in self.actions:
            blocked[x] = 0
        circuits = []
        gammaU = (self.gamma[u][1] | self.gamma[u][0])
        for x in gammaU:
            blocked[x] += 1
        circuits,blocked = self._ccVisitMP(circuits,blocked,p,u,Odd=self.Odd)
        for x in gammaU:
            if blocked[x] > 0:
                blocked[x] -= 1
        if self.Comments:
            print(p,circuits)
##        for x in self.actions:
##            blocked[x] = 0
        if Debug:
            print(p,'return',circuits)
        return circuits

    def _ccVisitMP(self,circuits,blocked,p,u,
                   Odd=False):
        """ p.15 """
        Comments = self.Comments
        Debug = self.Debug
        Med = self.valuationdomain['med']
        ut = p[-1]
        u1 = p[0]
        inAsymGammaUt = self.gamma[ut][1] - self.gamma[ut][0]
        gammaUt = self.gamma[ut][0] | self.gamma[ut][1]
        if Debug:
            print(p,self.gamma[ut][1],ut,self.gamma[ut][0])
        for x in gammaUt:
            blocked[x] += 1
        for v in inAsymGammaUt:
            if str(v) > str(u) and blocked[v] == 1:
                p1 = p + tuple([v])
                if Debug:
                    print(p,p1)
                if self.relation[u1][v] > Med and\
                   self.relation[v][u1] <= Med:
                    if Odd:
                        if (len(p1) % 2) != 1:
                            OddFlag=False
                        else:
                            OddFlag = True
                    else:
                        OddFlag = True
                    if OddFlag:
                        circ = list(reversed(p1))
                        if Comments:
                            print(p,'circuit certificate: ',circ)
                        circuits.append((circ,frozenset(circ)))

                elif self.relation[u1][v] <= Med and\
                    self.relation[v][u1] <= Med :
                    if Debug:
                        print(p,'continue with ', p1)
                    circuits,blocked = self._ccVisitMP(circuits,blocked,
                                                    p1,u,Odd=Odd)
##                    circuits.append(circuits1)
                    if Debug:
                        print(p,circuits)
        for x in (gammaUt):
            if blocked[x] > 0:
                blocked[x] -= 1

        return circuits,blocked


###################################
    #@timefn
    def _computeChordlessCircuits(self,Odd=False,Comments=False,Debug=False):
        """ 
        Renders the set of all chordless odd circuits detected in a digraph.
        Result (possible empty list) stored in <self.circuitsList>
        holding a possibly empty list tuples with at position 0 the
        list of adjacent actions of the circuit and at position 1
        the set of actions in the stored circuit.
        Inspired by Dias, Castonguay, Longo, Jradi, Algorithmica (2015).

        Returns a possibly empty list of tuples (circuit,frozenset(circuit)).

        If Odd == True, only circuits of odd length are retained in the result. 
        """

        tG = self._triplets(Comments=Comments)
        if Comments:
            print('There are %d starting triplets !' % len(tG) )
        self.blocked = {}
        for u in self.actions:
            self.blocked[u] = 0
        for p in tG:
            u = p[1]
##            if Debug:
##                print('===>>>',p,u)
            gammaU = (self.gamma[u][1] | self.gamma[u][0])
            for x in gammaU:
                #print(x)
                self.blocked[x] += 1
            self._ccVisit(p,u,Odd=Odd,Comments=Comments)
            for x in gammaU:
                if self.blocked[x] > 0:
                    self.blocked[x] -= 1
        return self.circuitsList

    def _ccVisit(self,p,u,Odd=False,Comments=False,Debug=False):
        """ p.15 """
        Med = self.valuationdomain['med']
        ut = p[-1]
        u1 = p[0]
        inAsymGammaUt = self.gamma[ut][1] - self.gamma[ut][0]
        gammaUt = self.gamma[ut][0] | self.gamma[ut][1]
##        if Debug:
##            print(self.gamma[ut][1],ut,self.gamma[ut][0])
        for x in gammaUt:
            self.blocked[x] += 1

        for v in inAsymGammaUt:
            if str(v) > str(u) and self.blocked[v] == 1:
                p1 = p + tuple([v])
##                if Debug:
##                    print(p1)
                if self.relation[u1][v] > Med and\
                   self.relation[v][u1] <= Med:
                    if Odd:
                        if (len(p1) % 2) != 1:
                            OddFlag=False
                        else:
                            OddFlag = True
                    else:
                        OddFlag = True
                    if OddFlag:
                        circ = list(reversed(p1))
                        if Comments:
                            print('circuit certificate: ',circ)
                        self.circuitsList.append((circ,frozenset(circ)))

                elif self.relation[u1][v] <= Med and\
                    self.relation[v][u1] <= Med :
##                    if Debug:
##                        print('continue with ', p1)
                    self._ccVisit(p1,u,Odd=Odd,Comments=Comments)
                    
        for x in (gammaUt):
            if self.blocked[x] > 0:
                self.blocked[x] -= 1

        return
          
#----------------------------------------

    def computeMaxHoleSize(self,Comments=False):
        """
        Renders the length of the largest chordless cycle
        in the corresponding disjunctive undirected graph.
        """
        g = self.digraph2Graph(ConjunctiveConversion=False)
        cycles = g.computeChordlessCycles()
        nbrOfHoles = len(cycles)
        maxHS = 0
        for c in cycles:
            nc = len(c)
            if nc > maxHS:
                if Comments:
                    print('Cycle %s of length %d' %(str(c),nc) )
                maxHS = nc
        if Comments:
            print('# holes           = %d ' % nbrOfHoles )
            print('Maximal hole size = %d ' % maxHS )
        self.nbrOfHoles = nbrOfHoles
        self.maxHoleSize = maxHS
        return maxHS
                
#----------------------------------------

    def relationFct(self,x,y):
        """
        wrapper for self.relation dictionary access to ensure interoperability
        with the sparse and big outranking digraph implementation model.
        """
        return self.relation[x][y]
#------------------------------------

    def topologicalSort(self,Debug=False):
        """
        If self is acyclic, adds topological sort number to each node of self
        and renders ordered list of nodes. Otherwise renders None.
        Source: M. Golumbic Algorithmic Graph heory and Perfect Graphs,
        Annals Of Discrete Mathematics 57 2nd Ed. , Elsevier 2004, Algorithm 2.4 p.44.
        """
        def topSort(v,Debug=False):
            if Debug:
                print('in',self.i,v,self.gamma[v],self.dfsNbr[v],self.tsNbr[v])
            self.i += 1
            self.dfsNbr[v] = self.i
            for w in self.gamma[v][0]:
                if Debug:
                    print('successer',w,'of',v)
                if self.dfsNbr[w] == 0:
                    topSort(w,Debug=Debug)
                else:
                    if self.tsNbr[w] == 0:
                        self.Acyclic = False
            self.tsNbr[v]=self.j
            self.j -= 1
            if Debug:
                print('out',v,self.dfsNbr[v],self.tsNbr[v])

        self.Acyclic = True
        self.dfsNbr = {}
        self.tsNbr = {}
        for x in self.actions:
            self.dfsNbr[x]=0
            self.tsNbr[x]=0
        self.j = len(self.actions)
        self.i = 0
        for x in self.actions:
            if Debug:
                print(x,self.gamma[x])
            if self.dfsNbr[x] == 0:
                topSort(x,Debug=Debug)

        if self.Acyclic:
            tsLevels = [(x,self.tsNbr[x]) for x in self.tsNbr]
            ordering = [x[0] for x in sorted(tsLevels,\
                                             key = lambda tsLevels: tsLevels[1])]
            if Debug:
                print(tsLevels,ordering)
            return ordering
        else:
            if Debug:
                print('Digraph instance %s is not acyclic!' % self.name)
                print(self.dfsNbr,self.tsNbr)             
            return None
            
    def digraph2Graph(self,valuationDomain={'min':-1,'med':0,'max':1},
                      Debug=False,ConjunctiveConversion=True):
        """
        Convert a Digraph instance to a Graph instance.
        """
        from graphs import Graph
        from copy import copy, deepcopy
        g = Graph()
        g.name = self.name + '_graph'
        if type(self.actions) == list:
            g.vertices = {}
            for x in self.actions:
                g.vertices[x] = {'name': x, 'shortName': x}
        else:
            g.vertices = deepcopy(self.actions)    
        g.order = len(g.vertices)
        g.valuationDomain = valuationDomain
        gMin = valuationDomain['min']
        gMed = valuationDomain['med']
        gMax = valuationDomain['max']
        g.edges = {}
        verticesKeys = list(g.vertices.keys())
        dgMed = self.valuationdomain['med']
        for i in range(g.order):
            for j in range(i+1,g.order):
                x = verticesKeys[i]
                y = verticesKeys[j]
                vertex = frozenset([x,y])
                if ConjunctiveConversion:
                    edgeValue = min(self.relation[x][y],self.relation[y][x])
                else:
                    edgeValue = max(self.relation[x][y],self.relation[y][x])
                if edgeValue > dgMed:
                    g.edges[vertex] = gMax
                elif edgeValue < dgMed:
                    g.edges[vertex] = gMin
                else:
                    g.edges[vertex] = gMed
                if Debug:
                    print('x,y,self.relation[x][y],self.relation[y][x],vertex,g.edges[vertex]', x,y,self.relation[x][y],self.relation[y][x],vertex,g.edges[vertex])
        g.gamma = g.gammaSets()
        return g


    def computeRelationalStructure(self,Debug=False):
        """
        Renders the counted decomposition of the valued relations into
        the following type of links:
        gt '>', eq '=', lt '<', incomp '<>',
        leq '<=', geq '>=', indeterm '?'
        """
        counts = {'>':0,'=':0,'<':0,'<>':0,'<=':0,'>=':0,'?':0}
        actions = [x for x in self.actions]
        n = len(actions)
        relation = self.relation
        for x in actions:
            for y in actions:
                if Debug:
                    print(x,y, relation[x][y],relation[y][x], end=' ')
                if x != y:
                    if relation[x][y] > self.valuationdomain['med']:
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['='] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['>'] += 1
                        else:
                            counts['>='] += 1
                    elif relation[x][y] < self.valuationdomain['med']:
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['<'] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['<>'] += 1
                        else:
                            counts['<='] += 1
                    else:  # relation[y][x] == self.valuationdomain['med']
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['<='] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['>='] += 1
                        else:
                            counts['?'] += 1
                if Debug:
                    print(counts)
        nd = Decimal(str(n))
        if nd != Decimal('0'):
            counts['<'] = Decimal(str(counts['<']))/(nd*(nd-1))
            counts['<='] = Decimal(str(counts['<=']))/(nd*(nd-1))
            counts['>'] = Decimal(str(counts['>']))/(nd*(nd-1))
            counts['>='] = Decimal(str(counts['>=']))/(nd*(nd-1))
            counts['<>'] = Decimal(str(counts['<>']))/(nd*(nd-1))
            counts['='] = Decimal(str(counts['=']))/(nd*(nd-1))
            counts['?'] = Decimal(str(counts['?']))/(nd*(nd-1))
        return counts

    def computeRankingByLastChoosing(self,CoDual=False,CppAgrum=False,Debug=False):
        """
        Computes a weak preordring of the self.actions by iterating
        worst choice elagations.

        Stores in self.rankingByLastChoosing['result'] a list of (P-,worstChoice) pairs
        where P- gives the worst choice complement outranked
        average valuation via the computePairwiseClusterComparison
        method.

        If self.rankingByChoosing['CoDual'] is True, the ranking-by-last-chossing 
        was computed on the codual of self.
        """
        from copy import copy, deepcopy
        currG = deepcopy(self)
        remainingActions = [x for x in self.actions]
        rankingByLastChoosing = []
        worstChoice = (None,None)
        i = 0
        while len(remainingActions) > 1 and worstChoice[1] != []:
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = deepcopy(currG)
            currGcd.computeRubisChoice(CppAgrum=CppAgrum,Comments=False)
            #currGcd.computeGoodChoices(Comments=Debug)

            #currGcd.computeBadChoices(Comments=Debug)
            worstChoiceCandidates = []
            j = 0
            for ch in currGcd.badChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranked = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('worst', j, ch[5], k1, k1Outranked)
                    worstChoiceCandidates.append( ( min(-k1Outranked['P+'],k1Outranked['P-']), k1 ) )
                else:
                    worstChoiceCandidates.append((self.valuationdomain['max'],k1))
            worstChoiceCandidates.sort(reverse=True)
            try:
                worstChoice = worstChoiceCandidates[0]
            except:
                #print 'Error: no worst choice in currGcd'
                #currGcd.save('currGcd_errorWorst')
                worstChoice=(self.valuationdomain['med'],[])
            if Debug:
                print('worstChoice', i, worstChoice, worstChoiceCandidates)

            if (worstChoice[1] != []):
                rankingByLastChoosing.append(worstChoice)
            if len(worstChoice[1]) > 0:
                for x in worstChoice[1]:
                    try:
                        remainingActions.remove(x)
                    except:
                        pass
            if Debug:
                print( i, worstChoice, remainingActions, rankingByLastChoosing)

        if (worstChoice[1] == []):
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(worstChoice)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByLastChoosing.append(worstChoice)
            if Debug:
                print(rankingByLastChoosing)

        elif len(remainingActions) == 1:
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(worstChoice)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByLastChoosing.append(worstChoice)
            if Debug:
                print(rankingByLastChoosing)
        
        self.rankingByLastChoosing = {'CoDual': CoDual, 'result': rankingByLastChoosing}
        return {'CoDual': CoDual, 'result': rankingByLastChoosing}


    def computeRankingByChoosing(self,actionsSubset=None,CppAgrum=False,Debug=False,CoDual=False):
        """
        Computes a weak preordring of the self.actions by iterating
        jointly best and worst choice elagations.

        Stores in self.rankingByChoosing['result'] a list of ((P+,bestChoice),(P-,worstChoice)) pairs
        where P+ (resp. P-) gives the best (resp. worst) choice complement outranking
        (resp. outranked) average valuation via the computePairwiseClusterComparison
        method.

        If self.rankingByChoosing['CoDual'] is True, the ranking-by-choosing was computed on the codual of self.
        """
        from copy import copy, deepcopy
        currG = deepcopy(self)
        if actionsSubset == None:
            remainingActions = [x for x in self.actions]
        else:
            remainingActions = actionsSubset
        rankingByChoosing = []
        bestChoice = (None,None)
        worstChoice = (None,None)
        i = 0
        while len(remainingActions) > 2 and (bestChoice[1] != [] or worstChoice[1] != []):
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = deepcopy(currG)
            currGcd.computeRubisChoice(CppAgrum=CppAgrum,Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))
            #bestChoiceCandidates.sort(reverse=True)
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: str(choice[1]) ) # lexigr choices
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: -choice[0]) # sort by outranking power
            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                #print 'Error: no best choice in currGcd!'
                #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)

            #currGcd.computeBadChoices(Comments=Debug)
            worstChoiceCandidates = []
            j = 0
            for ch in currGcd.badChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranked = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('worst', j, ch[5], k1, k1Outranked)
                    worstChoiceCandidates.append( ( min(-k1Outranked['P+'],k1Outranked['P-']), k1 ) )
                else:
                    worstChoiceCandidates.append((self.valuationdomain['max'],k1))
            worstChoiceCandidates.sort(reverse=True)
            try:
                worstChoice = worstChoiceCandidates[0]
            except:
                #print 'Error: no worst choice in currGcd'
                #currGcd.save('currGcd_errorWorst')
                worstChoice=(self.valuationdomain['med'],[])
            if Debug:
                print('worstChoice', i, worstChoice, worstChoiceCandidates)

            if (bestChoice[1] != [] or worstChoice[1] != []):
                rankingByChoosing.append((bestChoice,worstChoice))

            if len(bestChoice[1]) > 0:
                for x in bestChoice[1]:
                    remainingActions.remove(x)
            if len(worstChoice[1]) > 0:
                for x in worstChoice[1]:
                    try:
                        remainingActions.remove(x)
                    except:
                        pass
            #print i, bestChoice, worstChoice, remainingActions, rankingByChoosing
        if (bestChoice[1] == [] and worstChoice[1] == []):
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(bestChoice,worstChoice)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByChoosing.append((bestChoice,worstChoice))
            if Debug:
                print(rankingByChoosing)
        elif len(remainingActions) == 2:
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = deepcopy(currG)
            currGcd.computeRubisChoice(Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))
            bestChoiceCandidates.sort(reverse=True)
            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                #print 'Error: no best choice in currGcd!'
                #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)
            ## ### unique worst choice left
            k1 = list(set(currG.actions)-set(bestChoice[1]))
            if Debug:
                print('singleton worst choice left',k1)
            if len(k1) > 0:
                ck1 = list(set(currG.actions)-set(k1))
                k1Outranked = currG.computePairwiseClusterComparison(k1,ck1)
                worstChoice = ( min(-k1Outranked['P+'],k1Outranked['P-']), k1 )
            else:
                worstChoice = (self.valuationdomain['max'],bestChoice[1])
            if Debug:
                print('worstChoice', i, worstChoice)
            rankingByChoosing.append((bestChoice,worstChoice))

        elif len(remainingActions) == 1:
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(bestChoice,worstChoice)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByChoosing.append((bestChoice,worstChoice))
            if Debug:
                print(rankingByChoosing)
                
        self.rankingByChoosing = {'CoDual': CoDual, 'result': rankingByChoosing}
        return {'CoDual': CoDual, 'result': rankingByChoosing}

    def computeRankingByBestChoosing(self,CoDual=False,CppAgrum=False,Debug=False,):
        """
        Computes a weak preordering of the self.actions by recursive
        best choice elagations.

        Stores in self.rankingByBestChoosing['result'] a list of (P+,bestChoice) tuples
        where P+ gives the best choice complement outranking
        average valuation via the computePairwiseClusterComparison
        method.

        If self.rankingByBestChoosing['CoDual'] is True, 
        the ranking-by-choosing was computed on the codual of self.
        """
        if Debug:
            print("===>>>> debugging computeByBestChoosing() digraphs methods")
        from copy import copy, deepcopy
        currG = copy(self)
        remainingActions = [x for x in self.actions]
        rankingByBestChoosing = []
        bestChoice = (None,None)
        i = 0
        while len(remainingActions) > 2 and bestChoice[1] != []:
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = copy(currG)
            currGcd.computeRubisChoice(CppAgrum=CppAgrum,Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print('flatening the choice:',ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))
            #bestChoiceCandidates.sort(reverse=True)
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: str(choice[1]) ) # lexigr choices
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: -choice[0]) # sort by outranking power
            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                if Debug:
                    print('Error: no best choice in currGcd!')
                    #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)

            if bestChoice[1] != []:
                if Debug:
                    print('bestChoice[1] != []:', bestChoice[1])
                rankingByBestChoosing.append(bestChoice)

            if len(bestChoice[1]) > 0:
                for x in bestChoice[1]:
                        remainingActions.remove(x)
            if Debug:
                print(i, bestChoice, remainingActions, rankingByBestChoosing)

        if bestChoice[1] == []:
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print('bestChoice[1] == []:', bestChoice)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            rankingByBestChoosing.append(bestChoice)
            if Debug:
                print(rankingByBestChoosing)

        elif len(remainingActions) == 2:
            if Debug:
                print('len(remainingActions) == 2:',remainingActions)
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = copy(currG)
            currGcd.computeRubisChoice(Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))

            bestChoiceCandidates.sort(reverse=True)
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)

            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                #print 'Error: no best choice in currGcd!'
                #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            rankingByBestChoosing.append(bestChoice)
            for x in bestChoice[1]:
                remainingActions.remove(x)
            if len(remainingActions) > 0:
                lastBestChoice = (self.valuationdomain['max'],remainingActions)
                rankingByBestChoosing.append(lastBestChoice)
            if Debug:
                print('lastBestChoice', i+1, lastBestChoice)

        elif len(remainingActions) == 1:
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print('!!! len(remainingActions) == 1: !!!', remainingActions)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            rankingByBestChoosing.append(bestChoice)
            if Debug:
                print(rankingByBestChoosing)
        self.rankingByBestChoosing = {'CoDual': CoDual, 'result': rankingByBestChoosing}
        return {'CoDual': CoDual, 'result': rankingByBestChoosing}

    def iterateRankingByChoosing(self,Odd=False,CoDual=False,Comments=True,Debug=False,Limited=None):
        """
        Renders a ranking by choosing result when progressively eliminating
        all chordless (odd only) circuits with rising valuation cut levels.

        Parameters
            CoDual = False (default)/True
            Limited = proportion (in [0,1]) * (max - med) valuationdomain
        """
        from copy import copy, deepcopy
        from time import time
        if Debug:
            Comments=True
        gcd = copy(self)

        qualmaj0 = gcd.valuationdomain['med']
        if Limited != None:
            maxLevel = gcd.valuationdomain['med'] + (gcd.valuationdomain['max']-gcd.valuationdomain['med'])*Decimal(str(Limited))
        else:
            maxLevel = gcd.valuationdomain['max']
        if Comments:
            print('Ranking by choosing and rejecting after progressive cut elimination of chordless (odd = %s) circuits' % (str(Odd)) )
            print('Evaluation domain: [ %.3f ; %.3f ]' % (gcd.valuationdomain['min'],gcd.valuationdomain['max']))
            print('Initial determinateness of the outranking relation: %.3f' % self.computeDeterminateness())
            print('Maximum level of circuits elimination: %.3f' % (maxLevel))
        i = 0
        qualmaj = gcd.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments)
        self.rankingByChoosing = None
        while qualmaj > qualmaj0:
            i += 1
            if Comments:
                print('--> Iteration %d' % (i))
                t0 = time()
            if Limited:
                if qualmaj <= maxLevel:
                    if qualmaj < gcd.valuationdomain['max']:
                        # strict cut only possible if < max
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                    else:
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
                else:
                    qualmaj = qualmaj0
                    if qualmaj < gcd.valuationdomain['max']:
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                    else:
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
            else:
                if qualmaj < gcd.valuationdomain['max']:
                    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                else:
                    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
                
            if Comments:
                print('Polarised determinateness = %.3f' % pg.computeDeterminateness())
            if qualmaj > gcd.valuationdomain['med']:
                self.rankingByChoosing = pg.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
                self.rankingByChoosing['PolarizationLevel'] = qualmaj
            elif i==1:
                self.rankingByChoosing = pg.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
                self.rankingByChoosing['PolarizationLevel'] = qualmaj
            if Comments:
                self.showRankingByChoosing()
                print('Execution time:', time()-t0, 'sec.')
                ## pgRankingByChoosingRelation = self.computeRankingByChoosingRelation()
                ## corr = self.computeOrdinalCorrelation(pgRankingByChoosingRelation)
                ## print 'Ordinal (Kendall) correlation with outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination'])
                ## corr = self.computeOrdinalCorrelation(pgRankingByChoosingRelation,MedianCut=True,Debug=Debug)
                ## print 'Ordinal (Kendall) correlation with median cut outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination'])
            qualmaj0 = qualmaj
            newLevel = pg.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
            if Limited != None:
                qualmaj = min(maxLevel,newLevel)
            else:
                qualmaj = newLevel
            if Comments:
                print(i,qualmaj0,newLevel,qualmaj)
        if i==0:
            self.rankingByChoosing = gcd.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
            self.rankingByChoosing['PolarizationLevel'] = qualmaj
        return self.rankingByChoosing

    def _optimalRankingByChoosing(self,Odd=True,CoDual=False,Comments=False,Debug=False,Limited=None):
        """
        Renders a ranking by choosing result when progressively eliminating
        all chordless (odd only by default) circuits with rising valuation cut levels.

        Parameters:
        
            * CoDual = False (default)/True
            * Limited = proportion (in [0,1]) * (max - med) of valuationdomain (default = None)

        Returns the highest correlated rankingByChoosing with self or 
        codual of self, depending on the CoDual flagg.
        """
        from copy import copy, deepcopy
        
        if Debug:
            Comments=True
        g = copy(self)
        if CoDual:
            gcd = ~(-g)
        else:
            gcd = copy(g)
            gcdcd = ~(-gcd)

        qualmaj0 = gcd.valuationdomain['min']
        if Limited != None:
            maxLevel = gcd.valuationdomain['med'] + (gcd.valuationdomain['max']-gcd.valuationdomain['med'])*Decimal(str(Limited))
        else:
            maxLevel = gcd.valuationdomain['max']
        if Comments:
            print('Ranking by choosing and rejecting after progressive cut elimination of chordless (odd = %s) circuits' % (str(Odd)) )
            print('Evaluation domain: [ %.3f ; %.3f ]' % (gcd.valuationdomain['min'],gcd.valuationdomain['max']))
            print('Initial determinateness of the outranking relation: %.3f' % self.computeDeterminateness())
            print('Maximum level of circuits elimination: %.3f' % (maxLevel))
        i = 0
        #qualmaj = gcd.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments)
        qualmaj = gcd.valuationdomain['med']
        self.rankingByChoosing = None
        rankings = []
        while qualmaj > qualmaj0 and qualmaj <= maxLevel:
            i += 1
            if Comments:
                print('--> Iteration %d' % (i))
            if Limited != None:
                if qualmaj <= maxLevel:
                    if qualmaj < gcd.valuationdomain['max']:
                        ## strict cut only possible if cut level qualmaj < max
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                    else:
                        pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
                else:
                    qualmaj = qualmaj0
                    #if qualmaj < gcd.valuationdomain['max']:
                    #    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                    #else:
                    #    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)

            else:
                if qualmaj < gcd.valuationdomain['max']:
                    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
                else:
                    pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
              
            if Comments:
                print('Polarised determinateness = %.3f' % pg.computeDeterminateness())
            rkg = pg.computeRankingByChoosing(CoDual=False,Debug=Debug)
            pgr = pg.computeRankingByChoosingRelation()
                
            if CoDual:
                corr = g.computeOrdinalCorrelation(pgr)
            else:
                corr = gcdcd.computeOrdinalCorrelation(pgr)
            rankings.append((corr['correlation'],qualmaj,rkg))
            #rankings.append((corr['correlation']*corr['determination'],qualmaj,rkg))
            if Comments:
                if Debug:
                    print(rankings)
                if CoDual:
                    g.showRankingByChoosing(rkg)
                else:
                    gcdcd.showRankingByChoosing(rkg)
            qualmaj0 = qualmaj
            newLevel = pg.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments)
            if Limited != None:
                if newLevel <= maxLevel:
                    qualmaj = newLevel
                else:
                    qualmaj0 = qualmaj
            else:
                qualmaj = newLevel
            if Debug:
                print('i,qualmaj0,newLevel,maxLevel,qualmaj',i,qualmaj0,newLevel,maxLevel,qualmaj)
            
        if i==0:
            self.rankingByChoosing = gcd.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
            self.rankingByChoosing['PolarizationLevel'] = qualmaj
        else:
            rankings.sort(reverse=True)
            self.rankingByChoosing = rankings[0][2]
            self.rankingByChoosing['PolarizationLevel'] =  rankings[0][1]
        if Comments:
            if Debug:
               print(rankings)
            if CoDual:
                g.showRankingByChoosing(self.rankingByChoosing)
            else:
                gcdcd.showRankingByChoosing(self.rankingByChoosing)
                
        return self.rankingByChoosing

        
    def _computePrudentBestChoiceRecommendation(self,CoDual=False,Comments=False,Debug=False,Limited=None):
        """
        Renders the best choice recommendation after eliminating
        all odd chordless circuits with a minimal cut of the valuation.
        """
        from copy import copy as deepcopy
        self.optimalRankingByChoosing(CoDual=CoDual,Comments=Comments,Debug=Debug,Limited=Limited)
        #if Comments:
        #    self.showRankingByChoosing()
        try:
            self.rankingByChoosing['result'][0][0][1].sort()
            return self.rankingByChoosing['result'][0][0][1]
        except:
            print("Error: no ranking by choosing result !!")
            return None

    def computePreRankingRelation(self,preRanking,Normalized=True,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        a given preRanking in decreasing levels (list of lists) result.
        """
        if Normalized:
            Max = Decimal('1')
            Med = Decimal('0')
            Min = Decimal('-1')
        else:   
            Max = self.valuationdomain['max']
            Med = self.valuationdomain['med']
            Min = self.valuationdomain['min']
            
        actions = list(self.actions.keys())
        currentActions = set(actions)
        preRankingRelation = {}
        for x in actions:
            preRankingRelation[x] = {}
            for y in actions:
                preRankingRelation[x][y] = Med

        for eqcl in preRanking:
            currRest = currentActions - set(eqcl)
            if Debug:
                print(currentActions, eqcl, currRest)
            for x in eqcl:
                for y in eqcl:
                    if x != y:
                        preRankingRelation[x][y] = Max
                        preRankingRelation[y][x] = Max

            for x in eqcl:
                for y in currRest:
                    preRankingRelation[x][y] = Max
                    preRankingRelation[y][x] = Min
            currentActions = currentActions - set(eqcl)
        return preRankingRelation

    def computePreorderRelation(self,preorder,Normalized=True,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        a given preordering in increasing levels (list of lists) result.
        """
        if Normalized:
            Max = Decimal('1')
            Med = Decimal('0')
            Min = Decimal('-1')
        else:   
            Max = self.valuationdomain['max']
            Med = self.valuationdomain['med']
            Min = self.valuationdomain['min']
            
        actions = list(self.actions.keys())
        currentActions = set(actions)
        preorderRelation = {}
        for x in actions:
            preorderRelation[x] = {}
            for y in actions:
                preorderRelation[x][y] = Med

        for eqcl in preorder:
            currRest = currentActions - set(eqcl)
            if Debug:
                print(currentActions, eqcl, currRest)
            for x in eqcl:
                for y in eqcl:
                    if x != y:
                        preorderRelation[x][y] = Max
                        preorderRelation[y][x] = Max

            for x in eqcl:
                for y in currRest:
                    preorderRelation[x][y] = Min
                    preorderRelation[y][x] = Max
            currentActions = currentActions - set(eqcl)
        return preorderRelation

    def computeRankingByChoosingRelation(self,rankingByChoosing=None,actionsSubset=None,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        the self.rankingByChoosing result.
        """
        from digraphsTools import omax, omin
        from copy import copy, deepcopy
        if rankingByChoosing==None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                print('Error: first run computeRankingByChoosing(CoDual=T/F) !')
                return None
        if Debug:
            print('actionsSubset,rankingByChoosing',actionsSubset,rankingByChoosing)
        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        if actionsSubset==None:
            actions = [x for x in self.actions]
        else:
            actions = copy(actionsSubset)
        if Debug:
            print(actions)
        currActions = set(actions)
        relation = self.relation
        rankingRelation = {}
        for x in actions:
            rankingRelation[x] = {}
            for y in actions:
                rankingRelation[x][y] = Med
                #print(x,y,rankingRelation[x][y])
        n = len(rankingByChoosing)
        for i in range(n):
            ibch = set(rankingByChoosing[i][0][1])
            iwch = set(rankingByChoosing[i][1][1])
            ribch = set(currActions) - ibch
            if Debug:
                print(ibch,iwch,ribch)
            for x in ibch:
                for y in ibch:
                    if x != y:
                        rankingRelation[x][y] = omax(Med,[rankingRelation[x][y],abs(relation[x][y])])
                        rankingRelation[y][x] = omax(Med,[rankingRelation[x][y],abs(relation[y][x])])
                for y in ribch:
                    #print(x,y)
                    #print(rankingRelation[x][y])
                    #print(relation[x][y])
                    rankingRelation[x][y] = omax(Med,[rankingRelation[x][y],abs(relation[x][y])])
                    rankingRelation[y][x] = omax(Med,[rankingRelation[y][x],-abs(relation[y][x])])
            riwch = set(currActions) - iwch
            for y in iwch:
                for x in iwch:
                    if x != y:
                        rankingRelation[x][y] = omax(Med,[rankingRelation[x][y],abs(relation[x][y])])
                        rankingRelation[y][x] = omax(Med,[rankingRelation[y][x],abs(relation[y][x])])
                for x in riwch:
                    rankingRelation[x][y] = omax(Med,[rankingRelation[x][y],abs(relation[x][y])])
                    rankingRelation[y][x] = omax(Med,[rankingRelation[y][x],-abs(relation[x][y])])
            currActions = currActions - (ibch | iwch)
        return rankingRelation

    def computeRankingByBestChoosingRelation(self,rankingByBestChoosing=None,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        the self.rankingByBestChoosing result.
        """
        if rankingByBestChoosing==None:
            try:
                rankingByBestChoosing = self.rankingByBestChoosing['result']
            except:
                print('Error: first run computeRankingByBestChoosing(CoDual=T/F) !')
                return None

        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        actions = [x for x in self.actions]
        currActions = set(actions)
        relation = self.relation
        rankingRelation = {}
        for x in actions:
            rankingRelation[x] = {}
            for y in actions:
                rankingRelation[x][y] = Med
        n = len(rankingByBestChoosing)
        if Debug:
            print('rankingByBestChoosing',rankingByBestChoosing)
        for i in range(n):
            ibch = set(rankingByBestChoosing[i][1])
            ribch = set(currActions) - ibch
            if Debug:
                print('ibch,ribch',ibch,ribch)
            for x in ibch:
                for y in ibch:
                    if x != y:
                        rankingRelation[x][y] = min( [abs(relation[x][y]),abs(relation[y][x])] )
                        rankingRelation[y][x] = min( [abs(relation[y][x]),abs(relation[x][y])] )
##                        rankingRelation[x][y] = self.omin( [rankingRelation[x][y],abs(relation[y][x])] )
##                        rankingRelation[y][x] = self.omin( [rankingRelation[y][x],abs(relation[x][y])] )
##                    if Debug and (x == 'a10' or y == 'a07') :
##                        print(x,y,rankingRelation[x][y],relation[x][y])
##                        print(y,x,rankingRelation[y][x],relation[y][x])
                for y in ribch:
##                    rankingRelation[x][y] = self.omin( [rankingRelation[x][y],abs(relation[y][x])] )
##                    rankingRelation[y][x] = self.omin( [rankingRelation[y][x],-abs(relation[x][y])] )
                    rankingRelation[x][y] = min( [abs(relation[x][y]),abs(relation[y][x])] )
                    rankingRelation[y][x] = -min( [abs(relation[y][x]),abs(relation[x][y])] )
##                    if Debug and (x == 'a10' or y == 'a07'):
##                        print('+',x,y,rankingRelation[x][y],relation[x][y])
##                        print('-',y,x,rankingRelation[y][x],relation[y][x])
            currActions = currActions - ibch
        return rankingRelation

 
    def computeRankingByLastChoosingRelation(self,rankingByLastChoosing=None,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        the self.rankingByLastChoosing result.
        """
        if rankingByLastChoosing==None:
            try:
                rankingByLastChoosing = self.rankingByLastChoosing['result']
            except:
                print('Error: first run computeRankingByLastChoosing(CoDual=T/F) !')
                return None

        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        actions = [x for x in self.actions]
        currActions = set(actions)
        relation = self.relation
        rankingRelation = {}
        for x in actions:
            rankingRelation[x] = {}
            for y in actions:
                rankingRelation[x][y] = Med
        n = len(rankingByLastChoosing)
        for i in range(n):
            iwch = set(rankingByLastChoosing[i][1])
            riwch = set(currActions) - iwch
            for x in iwch:
                for y in iwch:
##                    if Debug and (x == 'a10' and y == 'a08') :
##                        print(x,y,rankingRelation[x][y],relation[x][y])
##                        print(y,x,rankingRelation[x][y],relation[y][x])
                    if x != y:
##                        rankingRelation[x][y] = self.omin( [rankingRelation[x][y],abs(relation[y][x])] )
##                        rankingRelation[y][x] = self.omin( [rankingRelation[y][x],abs(relation[x][y])] )
                        rankingRelation[x][y] = min( [abs(relation[x][y]),abs(relation[y][x])] )
                        rankingRelation[y][x] = min( [abs(relation[y][x]),abs(relation[x][y])] )
                for y in riwch:
##                    if Debug and (x == 'a10' and y == 'a08') :
##                        print(x,y,rankingRelation[x][y],relation[x][y])
##                        print(y,x,rankingRelation[x][y],relation[y][x])
##                    rankingRelation[x][y] = self.omin( [rankingRelation[x][y],-abs(relation[y][x])] )
##                    rankingRelation[y][x] = self.omin( [rankingRelation[y][x],abs(relation[x][y])] )
                    rankingRelation[x][y] = -min( [abs(relation[x][y]),abs(relation[y][x])] )
                    rankingRelation[y][x] = min( [abs(relation[y][x]),abs(relation[x][y])] )
            currActions = currActions - iwch
        return rankingRelation

    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        A show method for self.rankinByChoosing result.

        .. warning::

             The self.computeRankingByChoosing(CoDual=False/True) method instantiating the self.rankingByChoosing slot is pre-required !
        """
        if rankingByChoosing == None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                print('Error: You must first run self.computeRankingByChoosing(CoDual=False(default)|True) !')
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
            print(' %s%s%s Best Choice %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
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
            print(' %s%s%s Worst Choice %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))
        corr1 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation(rankingByChoosing))
        print('Ordinal bipolar correlation with outranking relation: tau = %+.3f (D = %.1f)'% (corr1['correlation'],corr1['determination']))
        corr2 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation(rankingByChoosing),MedianCut=True)
        print('Ordinal bipolar correlation with median cut outranking relation: tau = %+.3f (D = %.1f)'% (corr2['correlation'],corr2['determination']))

    def showRankingByLastChoosing(self,rankingByLastChoosing=None,Debug=None):
        """
        A show method for self.rankinByChoosing result.

        .. warning::

             The self.computeRankingByLastChoosing(CoDual=False/True) method instantiating the self.rankingByChoosing slot is pre-required !
        """
        if rankingByLastChoosing == None:
            try:
                rankingByLastChoosing = self.rankingByLastChoosing['result']
            except:
                print('Error: You must first run self.computeRankingByLastChoosing(CoDual=False(default)|True) !')
                return
        else:
            rankingByLastChoosing = rankingByLastChoosing['result']
        print('Ranking by recursively rejecting')
        space = ''
        n = len(rankingByLastChoosing)
        for i in range(n):
            if i+1 == 1:
                nstr='st'
            elif i+1 == 2:
                nstr='nd'
            elif i+1 == 3:
                nstr='rd'
            else:
                nstr='th'
            iwch = set(rankingByLastChoosing[i][1])
            if Debug:
                print( 'ibch, iwch, iach', i, ibch,iwch,iach)
            ch = list(iwch)
            ch.sort()
            if nstr == 'st':
                print(' Last Choice %s (%.2f)' % (ch,rankingByLastChoosing[i][0]))

            else:
                print(' %s%s%s Last Choice %s (%.2f)' % (space,i+1,nstr,ch,rankingByLastChoosing[i][0]))
            space += '  '

    
    def showRankingByBestChoosing(self,rankingByBestChoosing=None):
        """
        A show method for self.rankinByBestChoosing result.

        .. warning::

             The self.computeRankingByBestChoosing(CoDual=False/True) method instantiating the self.rankingByBestChoosing slot is pre-required !
        """
        if rankingByBestChoosing == None:
            try:
                rankingByBestChoosing = self.rankingByBestChoosing['result']
            except:
                print('Error: You must first run self.computeRankingByBestChoosing(CoDual=False(default)|True) !')
                return
        else:
            rankingByBestChoosing = rankingByBestChoosing['result']
        print('Ranking by recursively best-choosing')
        space = ''
        n = len(rankingByBestChoosing)
        for i in range(n):
            if i+1 == 1:
                nstr='st'
            elif i+1 == 2:
                nstr='nd'
            elif i+1 == 3:
                nstr='rd'
            else:
                nstr='th'
            ibch = set(rankingByBestChoosing[i][1])
            ch = list(ibch)
            ch.sort()
            print(' %s%s%s Best Choice %s (%.2f)' % (space,i+1,nstr,ch,rankingByBestChoosing[i][0]))
            space += '  '

    def computeValuationStatistics(self,Sampling=False,Comments=False):
        """
        Renders the mean and variance of the valuation
        of the non reflexive pairs.
        """
        from math import sqrt
        mean = Decimal('0.0')
        squares = Decimal('0.0')
        #actions = self.actions
        #n = len(self.actions)
        
        n = self.order
        n2 = n * (n-1)
        n2d = Decimal(str(n2))
        relation = self.relation
        for x,rx in relation.items():
            for y,rxy in rx.items():
                if x != y:
                    mean += rxy
                    squares += rxy*rxy
        mean = mean / n2d
        if Sampling:
            var = ( squares / (n2d-Decimal('1')) ) - (mean * mean)
        else:
            var = squares / n2d - (mean * mean)
        stdDev = sqrt(var)
        if Comments:
            print('mean: %.5f, std. dev.: %.5f' % (mean,stdDev))
        return mean,stdDev

    def computeRankingCorrelation(self, ranking, Debug=False):
        """
        Renders the ordinal correlation K of a digraph instance
        when compared with a given linear ranking of its actions
        
        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """
        
        selfMax = self.valuationdomain['max']
        if selfMax != Decimal('1'):
            print("Error: self's valuationdomain  must be normalized !")
            return
        n = len(ranking)
        corrSum = 0
        determSum = 0
        for i in range(n-1):
            x = ranking[i]
            for j in range(i+1,n):
                y = ranking[j]
                # x > y
                selfRelation = self.relation[x][y]
                otherRelation = selfMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ
                # y < x
                selfRelation = self.relation[y][x]
                otherRelation = -selfMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ

        if determSum > 0:
            correlation = float(corrSum) / float(determSum)
            n2 = (self.order*self.order) - self.order
            determination = (float(determSum) / n2)
            determination /= float(selfMax)
            
            return { 'correlation': correlation,\
                     'determination': determination }
        else:
            return { 'correlation': 0.0,\
                     'determination': 0.0 }

    def computeOrderCorrelation(self, order, Debug=False):
        """
        Renders the ordinal correlation K of a digraph instance
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
                selfRelation = self.relation[x][y]
                otherRelation = -selfMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += corr
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += determ
                # y > x
                selfRelation = self.relation[y][x]
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


    def computeOrdinalCorrelationMP(self, other, MedianCut=False,
                                    Threading=True,nbrOfCPUs=None,
                                    Comments=False,Debug=False):
        """
        Multi processing version of the digraphs.computeOrdinalCorrelation() method.
        
        .. note::
             The relation filtering and the MedinaCut option are not implemented in the MP version.
             
        """

        from multiprocessing import cpu_count
        from copy import copy,deepcopy
        from itertools import product
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            print('Error: the digraph instance self must be normalized - self.recodeValuation(-1,1) -first !')
            return None
        else:
            g = self
        actionsList = [x for x in g.actions]
        n = g.order
        n2 = (n*(n-1))
        Med = g.valuationdomain['med']
        
        if not isinstance(other,(dict)):
            #if Debug:
            #    print('inputting a Digraph instance')
            if other.valuationdomain['min'] != Decimal('-1') or\
               other.valuationdomain['max'] != Decimal('1'):
                print('Error: the digraph instance other must be normalized - other.recodeValuation(-1,1) -first !')
                return None
            otherRelation = other.relation
        else:
            otherRelation = other
        #if Debug:
        #    print(otherRelation)
            
        correlation = Decimal('0')
        determination = Decimal('0')
        if Threading and cpu_count() > 4:
            from pickle import Pickler,dumps, loads, load
            from io import BytesIO
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID,TempDirName,Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    from decimal import Decimal
                    chdir(self.workingDirectory)
                    #Debug=False
                    #if Debug:
                    #    print("Starting working in %s on %s" % (self.workingDirectory, self.name))
                    fi = open('dumpActions.py','rb')
                    actionsList = loads(fi.read())
                    fi.close()
                    #if Debug:
                    #    print(self.threadID,actionsList)
                    fi = open('dumpRelation.py','rb')
                    relation = loads(fi.read())
                    fi.close()
                    #if Debug:
                    #    print(self.threadID,relation)
                    fi = open('dumpOtherRelation.py','rb')
                    otherRelation = loads(fi.read())
                    fi.close()
                    #if Debug:
                    #    print(self.threadID,relation)
                    fiName = 'splitActions-'+str(self.threadID)+'.py'
                    fi = open(fiName,'rb')
                    splitActions = loads(fi.read())
                    fi.close()
                    #if Debug:
                    #    print(self.threadID,splitActions)
                    # compute partial correlation
                    correlation = Decimal('0')
                    determination = Decimal('0')
                    for x in splitActions:
                        grx = g.relation[x]
                        orx = otherRelation[x]
                        for y in actionsList:
                            if x != y:
                                correlation += min( max(-grx[y],orx[y]),\
                                            max(grx[y],-orx[y]) )
                                determination += min( abs(grx[y]),\
                                                      abs(orx[y]) )
                                #if Debug:
                                #    print(x,y,g.relation[x][y],otherRelation[x][y],correlation,determination)
                    splitCorrelation = {'correlation': correlation,
                                        'determination': determination}
                    # write partial correlation relation 
                    foName = 'splitCorrelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitCorrelation,-1))
                    fo.close()

            # pre-threading operations
            if nbrOfCPUs == None:
                nbrOfCPUs = cpu_count()
            if Debug:
                print('Nbr of cpus = ',nbrOfCPUs)
            if Comments:
                print('Starting correlation computation with %d threads ...' % nbrOfCPUs)
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                selfFileName = tempDirName +'/dumpActions.py'
                #if Debug:
                #    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                pd = dumps(actionsList,-1)
                fo.write(pd)
                fo.close()
                selfFileName = tempDirName +'/dumpRelation.py'
                #if Debug:
                #    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                pd = dumps(self.relation,-1)
                fo.write(pd)
                fo.close()
                selfFileName = tempDirName +'/dumpOtherRelation.py'
                #if Debug:
                #    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                pd = dumps(otherRelation,-1)
                fo.write(pd)
                fo.close()

            
                nit = n//nbrOfCPUs
                nbrOfJobs = nbrOfCPUs
                if nit*nbrOfCPUs < n:
                    nit += 1
                while nit*(nbrOfJobs-1) >= n:
                    nbrOfJobs -= 1
                if Comments:
                    print('nbr of actions to split',n)
                    print('nbr of jobs = ',nbrOfJobs)    
                    print('nbr of splitActions = ',nit)
                    
                i = 0
                actions2Split = actionsList
                actionsRemain = set(actions2Split)
                for jb in range(nbrOfJobs):
                    if Comments:
                        print('Thread = %d/%d' % (jb+1,nbrOfJobs),end=" ")
                    splitActions=[]
                    for k in range(nit):
                        if jb < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = list(actionsRemain)
                        i += 1
                    #if Debug:
                    #    print(len(splitActions))
                    #    print(splitActions)
                    actionsRemain = actionsRemain - set(splitActions)
                    #if Debug:
                    #    print(actionsRemain)
                    foName = tempDirName+'/splitActions-'+str(jb)+'.py'
                    fo = open(foName,'wb')
                    spa = dumps(splitActions,-1)
                    fo.write(spa)
                    fo.close()
                    splitThread = myThread(jb,tempDirName,Debug)
                    splitThread.start()
                    
                while active_children() != []:
                    pass
                
                # post threading operations
                if Comments:    
                    print('Exiting computing threads')
                for jb in range(nbrOfJobs):
                    #if Debug:
                    #    print('Post job-%d/%d processing' % (jb+1,nbrOfJobs))
                    #    print('job',jb)
                    fiName = tempDirName+'/splitCorrelation-'+str(jb)+'.py'
                    fi = open(fiName,'rb')
                    splitCorrelation = loads(fi.read())
                    #if Debug:
                    #    print('splitCorrelation',splitCorrelation)
                    fi.close()
                    correlation += splitCorrelation['correlation']
                    determination += splitCorrelation['determination']          
                                            
        else: #  no Threading
            
            if Debug:
                print('No threading !')
##            correlation, determination = sum([
##                (min( max(-g.relation[x][y],otherRelation[x][y]),\
##                     max(g.relation[x][y],-otherRelation[x][y]) ),\
##                min( abs(g.relation[x][y]),\
##                     abs(otherRelation[x][y]) )) for \
##                (x,y) in product(g.actions, repeat = 2)])
            
##            for x,y in product(actions,repeat=1)
            for x in dict.keys(g.actions):
                grx = g.relation[x]
                orx = otherRelation[x]
                for y in dict.keys(g.actions):
                    if x != y:
                        corr = min( max(-grx[y],orx[y]),\
                                    max(grx[y],-orx[y]) )
                        correlation += corr
                        determination += min( abs(grx[y]),\
                                              abs(orx[y]) )
                        #if Debug:
                        #    print(x,y,g.relation[x][y],otherRelation[x][y],correlation,determination)
        
                        
        if determination > Decimal('0.0'):
            correlation /= determination
            return { 'correlation': correlation,\
                     'determination': determination / Decimal(str(n2)) }
        else:
            return {'correlation': Decimal('0.0'),\
                    'determination': determination}
        
    def computeOrdinalCorrelation(self, other, MedianCut=False, filterRelation=None, Debug=False):
        """
        Renders the bipolar correlation K of a
        self.relation when compared
        with a given compatible (same actions set)) digraph or
        a [-1,1] valued compatible relation (same actions set).

        If MedianCut=True, the correlation is computed on the median polarized relations.

        If filterRelation != None, the correlation is computed on the partial domain corresponding to the determined part of the filter relation.

        .. warning::

             Notice that the 'other' relation and/or the 'filterRelation',
             the case given, must both be normalized, ie [-1,1]-valued !
        
        K = sum_{x != y} [ min( max(-self.relation[x][y]),other.relation[x][y]), max(self.relation[x][y],-other.relation[x][y]) ]

        K /= sum_{x!=y} [ min(abs(self.relation[x][y]),abs(other.relation[x][y])) ]

        .. note::

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation[x][y]),abs(other.relation[x][y])) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """
        from copy import copy,deepcopy
        g = deepcopy(self)
        g.recodeValuation(-1,1)
        actions = g.actions
        Med = g.valuationdomain['med']
        
        if MedianCut:
            g = PolarisedDigraph(g,level=Decimal('0.0'),KeepValues=False,StrictCut=True)

        if not isinstance(other,(dict)):
            if Debug:
                print('inputting a Digraph instance')
            otherg = deepcopy(other)
            otherg.recodeValuation(-1,1)
            if MedianCut:
                otherg = PolarisedDigraph(otherg,level=Decimal('0.0'),KeepValues=False,StrictCut=True)
            otherRelation = otherg.relation
        else:
            otherRelation = deepcopy(other)
            
            if MedianCut:
                for x in dict.keys(actions):
                    rx = otherRelation[x]
                    for y in dict.keys(actions):
                        if x == y:
                            rx[y] = Decimal('0.0')
                        else:
                            if rx[y] > Med:
                                rx[y] = Decimal('1.0')
                            elif rx[y] < Med:
                                rx[y] = Decimal('-1.0')
                            else:
                                rx[y] = Decimal('0.0')

        correlation = Decimal('0.0')
        determination = Decimal('0.0')

        if filterRelation == None:
            n = len(actions)
            n2 = (n*(n-1))
            for x in dict.keys(actions):
                grx = g.relation[x]
                orx = otherRelation[x]
                for y in dict.keys(actions):
                    if x != y:
                        corr = min( max(-grx[y],orx[y]), max(grx[y],-orx[y]) )
                        correlation += corr
                        determination += min( abs(grx[y]),abs(orx[y]) )
                        if Debug:
                            print(x,y,grx[y],orx[y],correlation,determination)
        else:
            n = len(actions)
            n2 = (n*(n-1))
            for x in dict.keys(actions):
                for y in dict.keys(actions):
                    if x != y:
                        if filterRelation[x][y] != Med:
                            corr = min( max(-g.relation[x][y],otherRelation[x][y]), max(g.relation[x][y],-otherRelation[x][y]) )
                            correlation += corr
                            determination += min( abs(g.relation[x][y]),abs(otherRelation[x][y]) )
                            #determination += abs(corr)
                            if Debug:
                                print(x,y,g.relation[x][y],otherRelation[x][y],filterRelation[x][y],correlation,determination)
                        
        if determination > Decimal('0.0'):
            correlation /= determination
            return { 'MedianCut':MedianCut, 'correlation': correlation,\
                     'determination': determination / Decimal(str(n2)) }
        else:
            return {'MedianCut':MedianCut, 'correlation': Decimal('0.0'),\
                    'determination': determination}

    def computeBipolarCorrelation(self, other, MedianCut=False, filterRelation=None, Debug=False):
        """
        obsolete: dummy replacement for Digraph.computeOrdinalCorrelation method
        """
        return self.computeOrdinalCorrelation(other= other,MedianCut=MedianCut,\
                                              filterRelation=filterRelation,Debug=Debug)

    def showCorrelation(self,corr=None,ndigits=3):
        """
        Renders the valued ordinal correlation index, the crisp Kendall tau index and their epistemic determination degree.
        """
        if corr != None:
            print('Correlation indexes:')
            print( (' Crisp ordinal correlation  : %%+.%df' % ndigits) % corr['correlation'])
            print( (' Epistemic determination    :  %%.%df' % ndigits) % corr['determination'])
            print( (' Bipolar-valued equivalence : %%+.%df' % ndigits) % (corr['correlation']*corr['determination']) )
        else:
            print('Error: a computed correlation result is required !!!')  

    def computeKemenyIndex(self, otherRelation):
        """
        renders the Kemeny index of the self.relation
        compared with a given crisp valued relation of a compatible
        other digraph (same nodes or actions).
        """
        KemenyIndex = 0.0
        actions = self.actions
        for x in dict.keys(actions):
            srx = self.relation[x]
            orx = otherRelation[x]
            for y in dict.keys(actions):
                if x != y:
                    if orx[y] > Decimal('0'):
                        KemenyIndex += float(srx[y])
                    elif orx[y] < Decimal('0'):
                        KemenyIndex -= float(srx[y])
        return KemenyIndex

    def flatChoice(self,ch,Debug=False):
        """
        Converts set or list ch recursively to a flat list of items.
        """
        result = []
        for x in ch:
            if Debug:
                print(x)
            if isinstance(x,frozenset):
                for y in self.flatChoice(x,Debug):
                    result.append(y)
            else:
                result.append(x)
        if Debug:
            print(result)
        return result

    def convertValuationToDecimal(self):
        """
        Convert the float valuation limits to Decimals.
        """
        self.valuationdomain['min'] = Decimal(str(self.valuationdomain['min']))
        self.valuationdomain['med'] = Decimal(str(self.valuationdomain['med']))
        self.valuationdomain['max'] = Decimal(str(self.valuationdomain['max']))

    def convertRelationToDecimal(self):
        """
        Converts the float valued self.relation in a decimal valued one.
        """
        actions = self.actions
        relation = {}
        for x in actions:
            relation[x] = {}
            rx = relation[x]
            srx = self.relation[x]
            for y in actions:
                rx[y] = Decimal(str(srx[y]))
        self.relation = relation
        #return relation

    def bipolarKCorrelation(self, digraph,Debug=False):
        """
        Renders the bipolar Kendall correlation between two bipolar valued
        digraphs computed from the average valuation of the
        XORDigraph(self,digraph) instance.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other) Digraph method

        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        actions = self.actions
        n = len(actions)
        xor.recodeValuation(-1.0,1.0)

        kDistance = Decimal("0.0")
        for x in dict.keys(actions):
            for y in dict.keys(actions):
                if x != y:
                    kDistance += xor.relation[x][y]
        kDistance = Decimal(str(kDistance)) / Decimal(str((n * (n-1))))
        # the negation of the kDistance, i.e. -kDistance gives
        # the bipolar extended Kendall tau correlation
        return -kDistance

    def crispKDistance(self, digraph,Debug=False):
        """
        Renders the crisp Kendall distance between two bipolar valued
        digraphs.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other, MedianCut=True) Digraph method
        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        actions = self.actions
        n = len(actions)

        k2Distance = xor.computeSize()
        k2Distance = Decimal(str(k2Distance)) / Decimal(str((n * (n-1))))

        return k2Distance

    def bipolarKDistance(self, digraph,Debug=False):
        """
        Renders the bipolar crisp Kendall distance between two bipolar valued
        digraphs.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other, MedianCut=True) Digraph method

        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        #actions = [x for x in self.actions]
        n = len(self.actions)

        k2Distance = xor.computeCoSize() - xor.computeSize()
        k2Distance = Decimal(str(k2Distance)) / Decimal(str((n * (n-1))))

        return k2Distance

    def computeWeakCondorcetWinners(self):
        """
        Wrapper for weakCondorcetWinners().
        """
        return self.weakCondorcetWinners()

    def computeWeakCondorcetLoosers(self):
        """
        Wrapper for weakCondorcetLoosers().
        """
        return self.weakCondorcetLoosers()

    def weakCondorcetWinners(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] >= self.valuationdomain['med']
        for all y != x.
        """
        #actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        wCW = []
        for x,rx in relation.items():
            #rx = relation[x]
            Winner = True
            for y,rxy in rx.items():
                if x != y:
                    if rx[y] < Med:
                        Winner = False
                        break
            if Winner:
                wCW.append(x)
        try:
            wCW.sort()
        except:
            pass
        return wCW

    def weakCondorcetLoosers(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] <= self.valuationdomain['med']
        for all y != x.
        """
        #actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        wCL = []
        for x,rx in relation.items():
            #rx = relation[x]
            Looser = True
            for y,rxy in rx.items():
                if x != y:
                    if rx[y] > Med:
                        Looser = False
                        break
            if Looser:
                wCL.append(x)
        try:
            wCL.sort()
        except:
            pass
        return wCL

    def computeCondorcetWinners(self):
        """
        Wrapper for condorcetWinners().
        """
        return self.condorcetWinners()

    def computeCondorcetLoosers(self):
        """
        Wrapper for condorcetLoosers().
        """
        return self.condorcetLoosers()

    def condorcetWinners(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] > self.valuationdomain['med']
        for all y != x.
        """
        #actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        CW = []
        for x,rx in relation.items():
            #rx = relation[x]
            Winner = True
            for y,rxy in rx.items():
                if x != y:
                    if rxy <= Med:
                        Winner = False
                        break
            if Winner:
                CW.append(x)
        try:
            CW.sort()
        except:
            pass
        return CW

    def condorcetLoosers(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] < self.valuationdomain['med']
        for all y != x.
        """
        #actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        CL = []
        for x,rx in relation.items():
            #rx = relation[x]
            Looser = True
            for y,rxy in rx.items():
                if x != y:
                    if rxy >= Med:
                        Looser = False
                        break
            if Looser:
                CL.append(x)
        try:
            CL.sort()
        except:
            pass
        return CL

    def forcedBestSingleChoice(self):
        """
        Renders the set of most determined outranking singletons in self.
        """
        actions = self.actions
        relation = self.relation
        valuationList = []
        for x in dict.keys(actions):
            for y in dict.keys(actions):
                if relation[x][y] not in valuationList:
                    valuationList.append(relation[x][y])
        valuationList.sort()
        print('Credibility levels:', valuationList)
        bestSingleChoices = set( list(dict.keys(actions)) )
        i=0
        while bestSingleChoices != set():
            current = set(bestSingleChoices)
            i += 1
            print('i_bestSingleChoices:', i,  bestSingleChoices)
            print('level', valuationList[i])
            for x in current:
                #print 'x', x
                rx = relation[x]
                notBest = False
                for y in actions:
                    #print 'y', y, relation[x][y]
                    if x != y and rx[y] < valuationList[i]:
                        notBest = True
                if notBest:
                    bestSingleChoices.remove(x)

        print('final bestSingleChoice:', current)
        print('leveal of credibility:',  valuationList[i-1])
        return (valuationList[i-1], current)

    def computeMoreOrLessUnrelatedPairs(self):
        """
        Renders a list of more or less unrelated pairs.
        """
        actions = self.actions
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        moreOrLessUnrelatedPairs = []
        for x in dict.keys(actions):
            for y in dict.keys(actions):
                if x != y:
                    if relation[x][y] < Med and relation[x][y] > Min:
                        if relation[y][x] < Med and relation[y][x] > Min:
                            if ((y,x),(relation[y][x],relation[x][y])) not in moreOrLessUnrelatedPairs:
                                moreOrLessUnrelatedPairs.append(((x,y),(relation[x][y],relation[y][x])))
        return moreOrLessUnrelatedPairs

    def computeUnrelatedPairs(self):
        """
        Renders a list of more or less unrelated pairs.
        """
        actions = self.actions
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        unrelatedPairs = []
        for x in dict.keys(actions):
            for y in dict.keys(actions):
                if x != y:
                    if relation[x][y] < Med:
                        if relation[y][x] < Med:
                            if ((y,x),(relation[y][x],relation[x][y])) not in unrelatedPairs:
                                unrelatedPairs.append(((x,y),(relation[x][y],relation[y][x])))
        return unrelatedPairs

    def closeSymmetric(self):
        """
        Produces the symmetric closure of self.relation.
        """
        actions = set(self.actions)
        symRelation = {}
        relation = self.relation
        for x in relation:
            symRelation[x] = {} 
            for y in relation[x]:
                 symRelation[x][y] = max(relation[x][y],relation[y][x])
        self.relation = symRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeTransitivityDegree(self,Comments=False):
        """
        Renders the transitivity degree of a digraph.
        """
        import copy
        Med = self.valuationdomain['med']
        #actionsList = [x for x in self.actions]
        actions = self.actions
        relationOrig = copy.deepcopy(self.relation)
        self.closeTransitive()
        relation = self.relation
        n0 = Decimal('0')
        n1 = Decimal('0')
        for x in actions:
            rox = relationOrig[x]
            rx = relation[x]
            for y in actions:
                if rox[y] > Med:
                    n0 += 1
                if rx[y] > Med:
                    n1 += 1
        self.relation = copy.deepcopy(relationOrig)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if n1 > Decimal('0'):
            res = n0/n1
        else:
            res = Decimal('0')
        if Comments:
            print('Transitivity degree of graph <%s> : %.2f' %(self.name,res))
        return res

    def computeSizeTransitiveClosure(self):
        """
        Renders the size of the transitive closure of a digraph.
        """
        import copy
        Med = self.valuationdomain['med']
        #actionsList = [x for x in self.actions]
        relationOrig = copy.deepcopy(self.relation)
        self.closeTransitive()
        #relation = self.relation
        n1 = 0
        for rx in self.relation.values():
            for rxy in rx.values():
                if rxy > Med:
                    n1 += 1
        self.relation = copy.deepcopy(relationOrig)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        return n1


    def closeTransitive(self,Irreflexive=True,Reverse=False):
        """
        Produces the transitive closure of self.relation.
        """
        import copy
        actions = set(self.actions)
        relation = copy.deepcopy(self.relation)
        if Irreflexive:
            for x in actions:
                relation[x][x] = self.valuationdomain['min']        
        for x in actions:
            for y in actions:
                for z in actions:
                    if Reverse:
                        if min(relation[y][x],relation[x][z]) > self.valuationdomain['med']:
                            relation[y][z] = self.valuationdomain['min']
                    else:
                        relation[y][z] = max(relation[y][z],min(relation[y][x],relation[x][z]))
        self.relation = copy.deepcopy(relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def isCyclic(self, Debug=False):
        """
        checks the cyclicity of self.relation by checking
        for a reflexive loop in its transitive closure-

        .. warning::

             self.relation is supposed to be irreflexive !
        """
        import copy
        Med = self.valuationdomain['med']
        if Debug:
            print(Med)
        actions = set(self.actions)
        relation = copy.deepcopy(self.relation)

        isCyclic = False
        for x in actions:
            for y in actions:
                for z in actions:
                    relation[y][z] = max(relation[y][z],min(relation[y][x],relation[x][z]))

        if Debug:
            for x in actions:
                print('x, relation[x][x]', x, relation[x][x])
        for x in actions:
            if relation[x][x] > Med:
                isCyclic = True
                break

        return isCyclic

    def isWeaklyComplete(self, Debug=False):
        """
        checks the weakly completeness property of self.relation by checking
        for the absence of a link between two actions!!

        .. warning::
        
            The reflexive links are ignored !!
        """
        Med = self.valuationdomain['med']
        if Debug:
            print('Med = ', Med)
        listActions = [x for x in self.actions]
        n = len(listActions)
        relation = self.relation
        
        isWeaklyComplete = True
        for i in range(n):
            x = listActions[i]
            for j in range(i+1,n):
                y = listActions[j]
                if relation[x][y] < Med and relation[y][x] < Med:
                    isWeaklyComplete = False
                    if Debug:
                        print('x,y,relation[x][y],relation[y][x]',\
                              x, y, relation[x][y], relation[y][x])
                    break
            if not isWeaklyComplete:
                break
        return isWeaklyComplete

    def isComplete(self, Debug=False):
        """
        checks the completeness property of self.relation by checking
        for the absence of a link between two actions!!

        .. warning::
        
            The reflexive links are ignored !!
        """
        Med = self.valuationdomain['med']
        if Debug:
            print('Med = ', Med)
        listActions = [x for x in self.actions]
        n = len(listActions)
        relation = self.relation
        
        isComplete = True
        for i in range(n):
            x = listActions[i]
            for j in range(i+1,n):
                y = listActions[j]
                if relation[x][y] <= Med and relation[y][x] <= Med:
                    isComplete = False
                    if Debug:
                        print('x,y,relation[x][y],relation[y][x]',\
                              x, y, relation[x][y], relation[y][x])
                    break
            if not isComplete:
                break
        return isComplete

    def automorphismGenerators(self):
        """
        Adds automorphism group generators to the digraph instance.

        .. note::

            Dependency: Uses the dreadnaut command from the nauty software package. See https://www3.cs.stonybrook.edu/~algorith/implement/nauty/implement.shtml

            On Ubuntu Linux:
              ...$ sudo apt-get install nauty
        """
        import os
        Name = self.name
        self.savedre(Name)
        aindex = self.aindex
        arevindex = {}
        for i in aindex:
            arevindex[str(aindex[i])] = i
        print(arevindex)
        File0 = Name+'.dre'
        File1 = Name+'.auto'
        print('# automorphisms extraction from dre file #')
        print('# Using input file: ' + File0)
        String2 = "echo '<"+File0+' -m p >'+File1+" x' | dreadnaut"
        print(String2)
        os.system(String2)
        NoError = True
        try:
            f1 = open(File1,'r')
        except:
            print('The input file: ', File1,' could not be found!')
            print("Be sure that nauty's dreadnaut programm is available!")
            NoError = False
        if NoError:
            permutations = {}
            t = f1.readline()
            nl = 0
            while t[:1] != '':
                nl += 1
                if t[:1] == ' ':
                    ts = f1.readline()
                    while ts[:2] == '  ':
                        suite = 1
                        t = t + ts
                        ts = f1.readline()
                    permutation = t.split()
                    print('# permutation = '+ str(nl)+str(permutation))
                    permutations[str(nl)] = {}
                    for i in range(len(permutation)):
                        permutations[str(nl)][str(arevindex[str(i+1)])] = str(arevindex[str(permutation[i])])
                    t = ts
                else:
                    #print '# ', t
                    grpsize = ''
                    for i in range(len(t)):
                        #print t[i],
                        if t[i] == '=':
                            #print 'ok'
                            #grpsize = ''
                            for j in range(i+1,len(t)):
                                if t[j] != ';':
                                    #print t[j]
                                    grpsize += t[j]
                                else:
                                    break
                            break
                    #print eval(grpsize)
                    #t = f1.readline
                    break
            f1.close()
            self.reflections = {}
            self.permutations = permutations
            self.automorphismGroupSize = eval(grpsize)

    def showAutomorphismGenerators(self):
        """
        Renders the generators of the automorphism group.
        """
        print('*---- Automorphism group generators ----')
        NoError = True
        try:
            reflections = self.reflections
            permutations = self.permutations
        except:
            print('No permutations or reflections defined yet !!')
            NoError = False
        if NoError:
            print('Permutations')
            for g in permutations:
                print(self.permutations[g])
            print('Reflections')
            for g in reflections:
                print(self.reflexions[g])
        else:
            print('Run self.automorphismGenerators()')

    def showOrbits(self,InChoices,withListing=True):
        """
        Prints the orbits of Choices along the automorphisms of
        the Digraph instance.

        Example Python session for computing the non isomorphic MISs from the 12-cycle graph:

        >>> from digraphs import *
        >>> c12 = CirculantDigraph(order=12,circulants=[1,-1])
        >>> c12.automorphismGenerators()
        ...
          Permutations
          {'1': '1', '2': '12', '3': '11', '4': '10', '5': 
           '9', '6': '8', '7': '7', '8': '6', '9': '5', '10': 
           '4', '11': '3', '12': '2'}
          {'1': '2', '2': '1', '3': '12', '4': '11', '5': '10', 
           '6': '9', '7': '8', '8': '7', '9': '6', '10': '5', 
           '11': '4', '12': '3'}
          Reflections {}
        >>> print('grpsize = ', c12.automorphismGroupSize)
          grpsize = 24
        >>> c12.showMIS(withListing=False)
          *---  Maximal independent choices ---*
          number of solutions:  29
          cardinality distribution
          card.:  [0, 1, 2, 3, 4,  5,  6, 7, 8, 9, 10, 11, 12]
          freq.:  [0, 0, 0, 0, 3, 24,  2, 0, 0, 0,  0,  0,  0]
          Results in c12.misset
        >>> c12.showOrbits(c12.misset,withListing=False)
        ...
          *---- Global result ----
          Number of MIS:  29
          Number of orbits :  4
          Labelled representatives:
          1: ['2','4','6','8','10','12']
          2: ['2','5','8','11']
          3: ['2','4','6','9','11']
          4: ['1','4','7','9','11']
          Symmetry vector
          stabilizer size: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]
          frequency      : [0, 2, 0, 0, 0, 0, 0, 1, 0,  0,  0,  1, ...]

        *Figure*: The symmetry axes of the non isomorphic MISs of the 12-cycle:

        .. image:: c12.png
           :width: 400 px
           :align: center
           :alt: The 4 non isomorphic MIS of the 12-cycle graph

        *Reference*: R. Bisdorff and J.L. Marichal (2008). Counting non-isomorphic maximal independent sets of the n-cycle graph. *Journal of Integer Sequences*, Vol. 11 Article 08.5.7 (`openly accessible here <https://www.cs.uwaterloo.ca/journals/JIS/VOL11/Marichal/marichal.html>`_)

        """
        try:
            reflections = self.reflections
            permutations = self.permutations
            NoError = True
        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')
            NoError = False
        if NoError:
            Choices = InChoices.copy()
            print('*--- Isomorphic reduction of choices')
            Iso = set()
            v = [0 for i in range(1,self.automorphismGroupSize + 1)]
            print('Number of choices:', len(Choices))
            while Choices != set():
                sCur = Choices.pop()
                print()
                print('current representative: ',sCur)
                print('length   : ', len(sCur))
                IsosCur = set([sCur])
                Isos = set()
                while IsosCur != Isos:
                    Isos = IsosCur.copy()
                    IsosRes = IsosCur.copy()
                    for s in IsosCur:
                        for g in reflections:
                            cur = s
                            for a in reflections[g]:
                                if (a[0] in cur) and a[1] not in cur:
                                    cur = cur - set([a[0]])
                                    cur = cur | set([a[1]])
                                else:
                                    if a[1] in cur and a[0] not in cur:
                                        cur = cur - set([a[1]])
                                        cur = cur | set([a[0]])
                            IsosRes.add(cur)
                    IsosCur = IsosRes.copy()
                    for s in IsosCur:
                        for g in permutations:
                            cur = frozenset()
                            for x in s:
                                cur = cur | set([permutations[g][str(x)]])
                            IsosRes = IsosRes | set([cur])
                    IsosCur = IsosRes.copy()
                Iso.add(sCur)
                niso = len(Isos)
                print('number of isomorph choices', niso)
                v[(self.automorphismGroupSize//niso)-1] += 1
                if withListing:
                    print('isormorph choices')
                    for ch in Isos:
                        print(list(ch))
                print('Number of choices before : ', len(Choices) + 1)
                Choices = Choices - Isos
                print('Number of choices after  : ', len(Choices))
            print()
            print('*---- Global result ----')
            print('Number of choices: ', len(InChoices))
            print('Number of orbits : ', len(Iso))
            print('Labelled representatives:')
            for ch in Iso:
                print(list(ch))
            print()
            print('                     Symmetry vector')
            print('stabilizer size  : ', list(range(1,self.automorphismGroupSize + 1)))
            print('frequency        : ', v)
            self.orbits = Iso

    def showOrbitsFromFile(self,InFile,withListing=True):
        """
        Prints the orbits of Choices along the automorphisms of
        the digraph self by reading in the 0-1 misset file format.
        See the :py:func:`digraphs.Digraph.readPerrinMisset` method.
        """
        
        try:
            reflections = self.reflections
            permutations = self.permutations
        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')
            return
        try:
            f1 = open(InFile,'r')
        except:
            print('File %s not found ?' % InFile)
            return
        
        actions = [x for x in self.actions]
        print('*--- Isomorphic reduction of choices')
        Iso = set()
        misset = set()
        v = [0 for i in range(1,self.order + 1)]
        while 1:
            line = f1.readline()
            if not line: break
            sCur = set()
            for i in range(len(line)):
                if line[i] == '1':
                    sCur.add(actions[i])
            if sCur not in misset:
                print('current representative: ',sCur)
                print('length   : ', len(sCur))
                IsosCur = set([frozenset(sCur)])
                Isos = set()
                while IsosCur != Isos:
                    Isos = IsosCur.copy()
                    IsosRes = IsosCur.copy()
                    for s in IsosCur:
                        for g in reflections:
                            cur = s
                            for a in reflections[g]:
                                if (a[0] in cur) and a[1] not in cur:
                                    cur = cur - set([a[0]])
                                    cur = cur | set([a[1]])
                                else:
                                    if a[1] in cur and a[0] not in cur:
                                        cur = cur - set([a[1]])
                                        cur = cur | set([a[0]])
                            IsosRes.add(cur)
                    IsosCur = IsosRes.copy()
                    for s in IsosCur:
                        for g in permutations:
                            cur = frozenset()
                            for x in s:
                                cur = cur | set([permutations[g][x]])
                            IsosRes = IsosRes | set([cur])
                    IsosCur = IsosRes.copy()
                Iso = Iso | set([frozenset(sCur)])
                niso = len(Isos)
                print('number of isomorph choices', niso)
                v[((2*self.order)//niso)-1] += 1
                if withListing:
                    print('isormorph choices')
                    for ch in Isos:
                        print(list(ch))
                print('Number of choices before : ', len(misset) + 1)
                misset = misset | Isos
                print('Number of choices after  : ', len(misset))
        print()
        print('*---- Global result ----')
        print('Labelled representatives:')
        for ch in Iso:
            print(list(ch))
        print()
        print('Number of choices: ', len(misset))
        print('Number of orbits : ', len(Iso))
        print('symmetry vector  : ', list(range(1,self.order + 1)))
        print('frequency        : ', v)
        self.orbits = Iso

    # def _readPerrinMisset(self,file):
    #     """
    #     read method for 0-1-char-coded MISs from perrinMIS.c curd.dat file.
    #     """
    #     NoError = True
    #     try:
    #         f1 = open(file,'r')
    #     except:
    #         NoError = False
    #         print('The input file: ', file,' could not be found ?')

    #     if NoError:
    #         actions = [x for x in self.actions]
    #         nl = 0
    #         misset = set()
    #         while 1:
    #             line = f1.readline()
    #             if not line: break
    #             nl += 1
    #             mis = set()
    #             for i in range(len(line)):
    #                 if ord(line[i]) == 1:
    #                     mis.add(actions[i])
    #             #print mis
    #             misset = misset | set([frozenset(mis)])
    #         #print 'Reading ' + str(nl) + ' MISs.'
    #         self.misset = misset

    def readPerrinMisset(self,file='curd.dat'):
        """
        read method for 0-1-char-coded MISs by default from the perrinMIS.c curd.dat result file.
        """
        try:
            f1 = open(file,'r')
            noError = True
        except:
            noError = False
            print('The input file: ', file,' could not be found ?')

        if noError:
            actions = [x for x in self.actions]
            nl = 0
            misset = set()
            for line in f1.readlines():
                if not line: break
                nl += 1
                mis = set()
                for i in range(len(line)):
                    if line[i] == '1':
                        mis.add(actions[i])
                #print mis
                misset = misset | set([frozenset(mis)])
            #print 'Reading ' + str(nl) + ' MISs.'
            self.misset = misset


    def computeOrbit(self,choice,withListing=False):
        """
        renders the set of isomorph copies of a choice following
        the automorphism of the digraph self
        """
        try:
            reflections = self.reflections
            permutations = self.permutations
            if withListing:
                print('*- ----------------"')
                print('Compute orbit of choice: ',choice)
                print('follwoing  automorphisms of digraph: ', self.name)
                print('Automorphism group size: ', self.automorphismGroupSize)
                print('Generators:')
                print('Reflections: ', reflections)
                print('Permutations: ', permutations)
            IsosCur = set([choice])
            Isos = set()
            while IsosCur != Isos:
                Isos = IsosCur.copy()
                IsosRes = IsosCur.copy()
                for s in IsosCur:
                    for g in reflections:
                        cur = s
                        for a in reflections[g]:
                            if (a[0] in cur) and a[1] not in cur:
                                cur = cur - set([a[0]])
                                cur = cur | set([a[1]])
                            else:
                                if a[1] in cur and a[0] not in cur:
                                    cur = cur - set([a[1]])
                                    cur = cur | set([a[0]])
                        IsosRes.add(cur)
                IsosCur = IsosRes.copy()
                for s in IsosCur:
                    for g in permutations:
                        cur = frozenset()
                        for x in s:
                            cur = cur | set([permutations[g][x]])
                        IsosRes = IsosRes | set([cur])
                IsosCur = IsosRes.copy()
            if withListing:
                print('Orbit size: ', len(Isos))
                print('List of isormorph choices')
                for ch in Isos:
                    print(list(ch))
            return Isos

        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')

    def showActions(self):
        """
        presentation methods for digraphs actions
        """
        print('*----- show digraphs actions --------------*')
        actionsList = [x for x in self.actions]
        actionsList.sort()
        for x in actionsList:
            print('key: ',x)
            try:
                print('  short name:',self.actions[x]['shortName'])
            except:
                pass
            print('  name:      ',self.actions[x]['name'])
            print('  comment:   ',self.actions[x]['comment'])
            print()

    def showShort(self):
        """
        concise presentation method for genuine digraphs.
        """
        print('*----- show short --------------*')
        print('Digraph          :', self.name)
        print('Actions          :', self.actions)
        print('Valuation domain :', self.valuationdomain)
        self.components()

    def showAll(self):
        """Detailed show method for genuine digraphs.""" 
        print('*----- show detail -------------*')
        print('Digraph          :', self.name)
        print('*---- Actions ----*')
        #actionsList = [x for x in self.actions]
        actionsList = []
        for x in self.actions:
            if isinstance(x,frozenset):
                actionsList += [self.actions[x]['name']]
            else:
                actionsList += [str(x)]
        actionsList.sort()
        print(actionsList)
        print('*---- Characteristic valuation domain ----*')
        print(self.valuationdomain)
        self.showRelationTable()
        self.showComponents()
        gamma = self.gammaSets()
        notGamma = self.notGammaSets()
        print('Neighborhoods:')
        print('  Gamma     :')
        for x in gamma:
            print('\'%s\': in => %s, out => %s' % (x,gamma[x][1],gamma[x][0]))
        print('  Not Gamma :')
        for x in notGamma:
            print('\'%s\': in => %s, out => %s' % (x,notGamma[x][1],notGamma[x][0]))

    def showNeighborhoods(self):
        """
        Lists the gamma and the notGamma function of self.
        """
        gamma = self.gammaSets()
        notGamma = self.notGammaSets()
        print('Neighborhoods:')
        print('  Gamma     :')
        for x in gamma:
            print('\'%s\': in => %s, out => %s' % (x,gamma[x][1],gamma[x][0]))
        print('  Not Gamma :')
        for x in notGamma:
            print('\'%s\': in => %s, out => %s' % (x,notGamma[x][1],notGamma[x][0]))        

    def showRelation(self):
        """
        prints the relation valuation in ##.## format.
        """
        print('* ---- Relation -----', end=' ')
        actionsList = []
        for x in self.actions:
            if isinstance(x,frozenset):
                actionsList += [(self.actions[x]['name'],x)]
            else:
                actionsList += [(x,x)]
        #actionsList = [x for x in self.actions]
        actionsList.sort()
        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = False
        for x in actionsList:
            print()
            for y in actionsList:
                if hasIntegerValuation:
                    print('('+str(x[0])+', '+str(y[0])+') = '+' % .2f ' % (self.relation[x[1]][y[1]]))
                else:
                    print('('+str(x[0])+', '+str(y[0])+') = '+' %d ' % (self.relation[x[1]][y[1]]))

        print()

    def showRelationMap(self,symbols=None,rankingRule="Copeland"):
        """
        Prints on the console, in text map format, the location of
        certainly validated and certainly invalidated outranking situations.

        By default, symbols = {'max':'┬','positive': '+', 'median': ' ',
                               'negative': '-', 'min': '┴'}

        The default ordering of the output is following the Copeland ranking rule
        from best to worst actions. Further available ranking rules are net flows (rankingRule="netFlows"),
        Kohler's (rankingRule="kohler"), and Tideman's ranked pairs rule (rankingRule="rankedPairs").

        Example::

            >>> from outrankingDigraphs import *
            >>> t = RandomCBPerformanceTableau(numberOfActions=25,seed=1)
            >>> g = BipolarOutrankingDigraph(t,Normalized=True)
            >>> gcd = ~(-g)  # strict outranking relation
            >>> gcd.showRelationMap(rankingRule="netFlows")
             -   ++++++++  +++++┬+┬┬+
            - -   + +++++ ++┬+┬+++┬++
            ┴+  ┴ + ++  ++++┬+┬┬++┬++
            -   ++ - ++++-++++++┬++┬+
               - - - ++- ┬- + -+┬+-┬┬
            -----  -      -┬┬┬-+  -┬┬
            ----    --+-+++++++++++++
            -- --+- --++ ++ +++-┬+-┬┬
            ----  -  -+-- ++--+++++ +
            ----- ++- --- +---++++┬ +
            -- -- ---+ -++-+++-+ +-++
            -- --┴---+  + +-++-+ -  +
            ---- ┴---+-- ++--++++ - +
              --┴┴--  --- -  --+ --┬┬
             ---------+--+ ----- +-┬┬
            -┴---┴- ---+- + ---+++┬ +
            -┴┴--┴---+--- ++ -++--+++
            -----┴--- ---+-+- ++---+ 
            -┴┴--------------- --++┬ 
            --┴---------------- --+┬ 
            ┴--┴┴ -┴--┴┴-┴ --++  ++-+
            ----┴┴--------------- -  
            ┴┴┴----+-┴+┴---┴-+---+ ┴+
            ┴┴-┴┴┴-┴- - -┴┴---┴┴+ ┬ -
            ----┴┴-┴-----┴┴---  - -- 
            Ranking rule: netFlows
            >>> 

        """
        if symbols == None:
            symbols = {'max':'┬','positive': '+', 'median': ' ',
                       'negative': '-', 'min': '┴'}
        if rankingRule == "Copeland":
            ranking = self.computeCopelandRanking()
        elif rankingRule == "netFlows":
            ranking = self.computeNetFlowsRanking()
        elif rankingRule == "rankedPairs":
            ranking = self.computeRankedPairsRanking()
        else:
            rankingRule = "Alphabetic"
            ranking = [x for x in self.actions]
            ranking.sort()
        relation = self.relation
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        for x in ranking:
            rx = relation[x]
            pictStr = ''
            for y in ranking:
                if rx[y] == Max:
                    pictStr += symbols['max']
                elif rx[y] == Min:
                    pictStr += symbols['min']
                elif rx[y] > Med:
                    pictStr += symbols['positive']
                elif rx[y] ==Med:
                    pictStr += symbols['median']
                elif rx[y] < Med:
                    pictStr += symbols['negative']
            print(pictStr)
        print('Ranking rule: %s' % rankingRule)
      

    def showRelationTable(self,Sorted=True,\
                          IntegerValues=False,\
                          actionsSubset= None,\
                          relation=None,\
                          ndigits=2,\
                          ReflexiveTerms=True):
        """
        prints the relation valuation in actions X actions table format.
        """
        if actionsSubset == None:
            actions = self.actions
        else:
            actions = actionsSubset
        if relation == None:
            relation = self.relation
        print('* ---- Relation Table -----\n', end=' ')
        print(' S   | ', end=' ')
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(str(x),x)]
        if Sorted:
            actionsList.sort()
        #print actionsList
        #actionsList.sort()

        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = IntegerValues

        for x in actionsList:
            print("'"+x[0]+"'\t ", end=' ')
        print('\n------|-------------------------------------------')
        for x in actionsList:
            print(" '"+x[0]+"' | ", end=' ')
            for y in actionsList:
                if x != y:
                    if hasIntegerValuation:
                        print('%d\t' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        formatString = '%%2.%df\t' % ndigits
                        print(formatString % (relation[x[1]][y[1]]), end=' ')
                else:
                    if ReflexiveTerms:
                        if hasIntegerValuation:
                            print('%d\t' % (relation[x[1]][y[1]]), end=' ')
                        else:
                            formatString = '%%2.%df\t' % ndigits
                            print(formatString % (relation[x[1]][y[1]]), end=' ')
                    else:  
                        formatString = ' - \t'
                        print(formatString, end=' ')
            print('')
        if hasIntegerValuation:
            print('Valuation domain: [%d;%+d]'% (self.valuationdomain['min'],
                                                 self.valuationdomain['max']))
        else:
            formatString = 'Valuation domain: [%%2.%df;%%2.%df]\n' % (ndigits,ndigits)
            print( formatString % (self.valuationdomain['min'],
                                   self.valuationdomain['max']))
            
    def showHTMLRelationMap(self,actionsList=None,\
                            rankingRule='Copeland',\
                            Colored=True,\
                            tableTitle='Relation Map',\
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
        fo.write(self._htmlRelationMap(actionsSubset=actionsList,
                                      rankingRule=rankingRule,
                                        Colored=Colored,
                                        tableTitle=tableTitle,
                                        symbols=symbols,
                                        ContentCentered=True,
                                        relationName=relationName))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
        
        
    def _htmlRelationMap(self,tableTitle='Relation Map',\
                          relationName='r(x R y)',\
                          actionsSubset= None,\
                          rankingRule='Copeland',\
                          symbols=['+','&middot;','&nbsp;','-','_'],\
                          Colored=True,\
                          ContentCentered=True):
        """
        renders the relation map in actions X actions html table format.
        """
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        # construct ranking and actionsList
        if actionsSubset != None:
            ranking = actionsSubset
        else:
            if rankingRule == "Copeland":
                ranking = self.computeCopelandRanking()
            elif rankingRule == "netFlows":
                ranking = self.computeNetFlowsRanking()
            elif rankingRule == "rankedPairs":
                ranking = self.computeRankedPairsRanking()
            else:
                rankingRule = "Alphabetic"
                ranking = [x for x in self.actions]
                ranking.sort()
        actionsList = []
        for x in ranking:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except KeyError:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(str(x),str(x))]
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
        s += '<h2>Ranking rule: %s</h2>' % rankingRule
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
                    if self.relation[x[1]][y[1]] == Max:
                        s += '<td bgcolor="#66ff66"><b>%s</b></td>\n' % symbols[0]
                    elif self.relation[x[1]][y[1]] > Med:
                        s += '<td bgcolor="#ddffdd">%s</td>' % symbols[1]
                    elif self.relation[x[1]][y[1]] == Min:
                        s += '<td bgcolor="#ff6666"><b>%s</b></td\n>' % symbols[4]
                    elif self.relation[x[1]][y[1]] < Med:
                        s += '<td bgcolor="#ffdddd">%s</td>\n' % symbols[3]
                    else:
                        #s += '<td bgcolor="#ffffff">%s</td>\n' % symbols[2]
                        s += '<td class="na">%s</td>\n' % symbols[2]
                else:
                    if self.relation[x[1]][y[1]] == Max:
                        s += '<td><b>%s</b></td>\n'  % symbols[0]
                    elif self.relation[x[1]][y[1]] > Med:
                        s += '<td>%s</td>\n' % symbols[1]
                    elif self.relation[x[1]][y[1]] == Min:
                        s += '<td><b>%s</b></td>\n' % symbols[4]
                    elif self.relation[x[1]][y[1]] < Med:
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


    def showHTMLRelationTable(self,actionsList=None,\
                              relation=None,
                              IntegerValues=False,\
                              ndigits=2,\
                              Colored=True,\
                              tableTitle='Valued Adjacency Matrix',\
                              relationName='r(x S y)',\
                              ReflexiveTerms=False):
        """
        Launches a browser window with the colored relation table of self.
        """
        import webbrowser
        fileName = '/tmp/relationMap.html'
        fo = open(fileName,'w')
        fo.write(self._htmlRelationTable(actionsSubset=actionsList,
                                         relation=relation,
                                        isColored=Colored,
                                        ndigits=ndigits,
                                        hasIntegerValues=IntegerValues,
                                        tableTitle=tableTitle,
                                        relationName=relationName,
                                        ReflexiveTerms=ReflexiveTerms))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)
        
        
    def _htmlRelationTable(self,tableTitle='Valued Relation Table',
                           relation=None,
                          relationName='r(x R y)',
                          ndigits=2,
                          hasIntegerValues=False,
                          actionsSubset= None,
                          isColored=False,
                          ReflexiveTerms=False):
        """
        renders the relation valuation in actions X actions html table format.
        """
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        if actionsSubset == None:
            actions = self.actions
        else:
            actions = actionsSubset
        if relation == None:
            relation = self.relation
        s = ''
        s += '<h1>%s</h1>' % tableTitle
        s += '<table border="1">'
        if isColored:
            s += '<tr bgcolor="#9acd32"><th>%s</th>' % relationName
        else:
            s += '<tr><th>%s</th>' % relationName
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(str(x),x)]
        if actionsSubset == None:
            actionsList.sort()
        #print actionsList
        #actionsList.sort()
        if not hasIntegerValues: 
            try:
                hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
            except KeyError:
                hasIntegerValuation = hasIntegerValues
                self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        else:
            hasIntegerValuation = hasIntegerValues
            self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation

        for x in actionsList:
            if isColored:
                s += '<th bgcolor="#FFF79B">%s</th>' % (x[0])
            else:
                s += '<th>%s</th>' % (x[0])
        s += '</tr>'
        for x in actionsList:
            s += '<tr>'
            if isColored:
                s += '<th bgcolor="#FFF79B">%s</th>' % (x[0])
            else:
                s += '<th>%s</th>' % (x[0])
            for y in actionsList:
                if x == y:
                    if ReflexiveTerms:
                        if hasIntegerValuation:
                            if isColored:
                                if relation[x[1]][y[1]] > Med:
                                    s += '<td bgcolor="#ddffdd" align="right">%d</td>' % (relation[x[1]][y[1]])
                                elif relation[x[1]][y[1]] < Med:
                                    s += '<td bgcolor="#ffddff"  align="right">%d</td>' % (relation[x[1]][y[1]])
                                else:
                                    s += '<td bgcolor="#dddddd" align="right" >%d</td>' % (relation[x[1]][y[1]])
                            else:
                                s += '<td>%d</td>' % (relation[x[1]][y[1]])
                        else:
                            ndigitsFormat = '%%2.%df' % ndigits
                            if isColored:
                                if relation[x[1]][y[1]] > Med:
                                    formatStr = '<td bgcolor="#ddffdd" align="right">%s</td>' % ndigitsFormat 
                                    s += formatStr % (relation[x[1]][y[1]])
                                elif relation[x[1]][y[1]] < Med:
                                    formatStr = '<td  bgcolor="#ffddff" align="right">%s</td>' % ndigitsFormat
                                    s +=  formatStr % (relation[x[1]][y[1]])
                                else:
                                    formatStr = '<td  bgcolor="#dddddd" align="right">%s</td>' % ndigitsFormat
                                    s += formatStr % (relation[x[1]][y[1]])
                            else:
                                formatStr = '<td>%s</td>' % ndigitsFormat
                                s += formatStr % (relation[x[1]][y[1]])
                    else:
                        s += '<td bgcolor="#eeeeee" align="center"> &ndash; </td>'
                    
                else:
                    if hasIntegerValuation:
                        if isColored:
                            if relation[x[1]][y[1]] > Med:
                                s += '<td bgcolor="#ddffdd" align="right">%d</td>' % (relation[x[1]][y[1]])
                            elif relation[x[1]][y[1]] < Med:
                                s += '<td bgcolor="#ffddff"  align="right">%d</td>' % (relation[x[1]][y[1]])
                            else:
                                s += '<td bgcolor="#dddddd" align="right" >%d</td>' % (relation[x[1]][y[1]])
                        else:
                            s += '<td>%d</td>' % (relation[x[1]][y[1]])
                    else:
                        ndigitsFormat = '%%2.%df' % ndigits
                        if isColored:
                            if relation[x[1]][y[1]] > Med:
                                formatStr = '<td bgcolor="#ddffdd" align="right">%s</td>' % ndigitsFormat 
                                s += formatStr % (relation[x[1]][y[1]])
                            elif relation[x[1]][y[1]] < Med:
                                formatStr = '<td  bgcolor="#ffddff" align="right">%s</td>' % ndigitsFormat
                                s +=  formatStr % (relation[x[1]][y[1]])
                            else:
                                formatStr = '<td  bgcolor="#dddddd" align="right">%s</td>' % ndigitsFormat
                                s += formatStr % (relation[x[1]][y[1]])
                        else:
                            formatStr = '<td>%s</td>' % ndigitsFormat
                            s += formatStr % (relation[x[1]][y[1]])
            s += '</tr>'
        s += '</table>'
        if hasIntegerValuation:
            s += '<p>Valuation domain: [%d; %+d]</p>' % (Min,Max)
        else:
            s += '<p>Valuation domain: [%.2f; %+.2f]</p>' % (Min,Max)
            
        return s

    def showdre(self):
        """
        Shows relation in nauty format.
        """
        print('*----- show dre -------------*')
        actions = [x for x in self.actions]
        aindex = {}
        i = 1
        print('Actions index:')
        for x in actions:
            print(i,': ', str(x))
            aindex[x] = i
            i += 1
        Med = self.valuationdomain['med']
        relation = self.relation
        n = len(actions)
        print('n='+str(n)+' $=1 d g')
        for x in actions:
            res = str(aindex[x]) + ': '
            for y in actions:
                if relation[x][y] > Med:
                    res = res + str(aindex[y]) + ' '
            res = res + ';'
            print(res)

    def exportPrincipalImage(self, Reduced=False,\
                             Colwise=False,\
                             plotFileName=None,\
                             Type="png",\
                             TempDir='.',Comments=False):
        """
        Export as PNG (default) or PDF the principal projection of
        the valued relation using the three principal eigen vectors.

        .. warning::
        
            The method, writing and reading temporary files: 
            tempCol.r and rotationCol.csv, resp. tempRow.r and rotationRow.csv,
            by default in the working directory (./),
            is hence not safe for multiprocessing programs, unless a
            temporary dirctory is provided

        """
        
        if Comments:
            print('*----  export 3dplot of type %s -----' % (Type))
        if TempDir == None:
            TempDir = '.'
        import os,time
        if plotFileName == None:
            plotFileName = "%s/%s_principalImage" % (TempDir,self.name)
        if Colwise:
            plotFileName += "_Colwise"
        else:
            plotFileName += "_Rowwise"
        self.saveCSV('%s/exportTemp' % TempDir)
        if Colwise:
            fo = open('%s/tempCol.r' % TempDir,'w')
        else:
            fo = open('%s/tempRow.r' % TempDir,'w')
        fo.write("x = read.csv('%s/exportTemp.csv',row.names=1)\n" % TempDir)
        if Colwise:
            fo.write("x = t(x)\n")
        if Reduced:
            fo.write("x = (x-colMeans(x))/(sapply(x,sd)*sqrt(length(t(x))))\n")
        else:
            fo.write("x = (x-colMeans(x))\n")
        fo.write("X = as.matrix(x)\n")
        fo.write("A = X %*% t(X)\n")
        fo.write("E = eigen(A, symmetric=TRUE)\n")
        fo.write("P = E$values * t(E$vectors)\n")
        if Colwise:
            fo.write("write.csv(t(P),'%s/rotationCol.csv',row.names=F)\n" % TempDir)
        else:
            fo.write("write.csv(t(P),'%s/rotationRow.csv',row.names=F)\n" % TempDir)           
        if Type == None:
            # no principal image is required
            fo.close()
        else:
            fo.write("valprop = E$values/sum(E$values)\n")
            fo.write("pcaRes = list(x=X,eig=E,a=A,P=P,val=valprop)\n")
            fo.write("val = pcaRes$val\n")
            fo.write("nval = length(val)\n")
            if Type == "png":
                fo.write('png("%s/%s.png",width=480,height=480,bg="cornsilk")\n'\
                         % (TempDir,plotFileName) )
            elif Type == "jpeg":
                fo.write('jpeg("%s/%s.jpg",width=480,height=480,bg="cornsilk")\n'\
                         % (TempDir,plotFileName) )
            elif Type == "xfig":
                fo.write('xfig("%s/%s.fig",width=480,height=480,bg="cornsilk")\n'\
                         % (TempDir,plotFileName) )
            elif Type == "pdf":
                fo.write('pdf("%s/%s.pdf",width=6,height=6,bg="cornsilk",title="PCA of relation valuation")\n'\
                         % (TempDir,plotFileName) )
            else:
                print('Error: Plotting device %s not defined !' % (Type))
                return
            fo.write("par(mfrow=c(2,2))\n")
            fo.write("a1 = 1\n")
            fo.write("a2 = 2\n")
            fo.write("a3 = 3\n")
            fo.write('plot(pcaRes$P[a1,],pcaRes$P[a2,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 2:",val[a2]*100,"%"),asp=1)\n')
            fo.write("text(pcaRes$P[a1,],pcaRes$P[a2,],rownames(pcaRes$x),cex=0.75)\n")
            fo.write('abline(h=0,lty=2,col="gray")\n')
            fo.write('abline(v=0,lty=2,col="gray")\n')
            fo.write('plot(pcaRes$P[a2,],pcaRes$P[a3,],"n",xlab=paste("axis 2:",val[a2]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)\n')
            fo.write('text(pcaRes$P[a2,],pcaRes$P[a3,],rownames(pcaRes$x),cex=0.75)\n')
            fo.write('abline(h=0,lty=2,col="gray")\n')
            fo.write('abline(v=0,lty=2,col="gray")\n')
            fo.write('plot(pcaRes$P[a1,],pcaRes$P[a3,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)\n')
            fo.write('text(pcaRes$P[a1,],pcaRes$P[a3,],rownames(pcaRes$x),cex=0.75)\n')
            fo.write('abline(h=0,v=0,lty=2,col="gray")\n')
            fo.write('barplot(val[a1:nval]*100,names.arg=a1:nval,main="Axis inertia (in %)",col="orangered")\n')
            fo.write('dev.off()\n')
            fo.close()
        if Comments:
            if Colwise:
                os.system('(cd %s;env R -q --vanilla --verbose < tempCol.r 2>&1)' % TempDir)
            else:
                os.system('(cd %s;env R -q --vanilla --verbose < tempRow.r 2>&1)' % TempDir )               
        else:
            if Colwise:
                os.system('(cd %s;env R -q --vanilla < tempCol.r > /dev/null 2> /dev/null)' % TempDir)
            else:
                os.system('(cd %s;env R -q --vanilla < tempRow.r > /dev/null 2> /dev/null)' % TempDir)
                
        time.sleep(3)     
        if Type != None and Comments:
            print('See %/%s.%s ! ' % (TempDir,plotFileName,Type))
        
        
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
                if relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] > Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both,style="setlinewidth(2)",color=black, arrowhead=normal, arrowtail=normal] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] == Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowhead=normal, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] > Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowtail=normal, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] == Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=grey, arrowhead=empty, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=black] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=grey, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] < Med and relation[actionkeys[j]][actionkeys[i]] >  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=back, color=black] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] < Med and relation[actionkeys[j]][actionkeys[i]] ==  Med:
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

    def exportD3(self, fileName="index", Comments=True):
        """
    This function was designed and implemented by Gary Cornelius, 2014 for his bachelor thesis at the University of Luxembourg. 
    The thesis document with more explanations can be found
    `here <http://leopold-loewenheim.uni.lu/Digraph3/literature/>`_ .
    
    *Parameters*:
        * fileName, name of the generated html file, default = None (graph name as defined in python);
        * Comments, True = default;

    The idea of the project was to find a way that allows you to easily get details about certain nodes or edges of a directed graph in a dynamic format. 
    Therefore this function allows you to export a html file together with all the needed libraries, including the 
    D3 Library which we use for graph generation and the physics between nodes, which attracts or pushes nodes away from each other.

    Features of our graph include i.e. : 
        * A way to only inspect a node and it's neighbours 
        * Dynamic draging and freezing of the graph
        * Export of a newly created general graph

    You can find the list of fututres in the Section below which is arranged according to the graph type.
    
    *If the graph is an outrankingdigraphs*:
        * Nodes can be dragged and only the name and comment can be edited. 
        * Edges can be inspected but not edited for this purpose a special json array containing all possible pairwiseComparisions is generated.

    *If the graph is a general graph*:
        * Nodes can be dragged, added, removed and edited.
        * Edges can be added, removed, inverted and edited. But edges cannot be inspected.
        * The pairwiseComparisions key leads to an empty array {}.

    In both cases, undefined edges can be hidden and reappear after a simple reload.(right click - reload)

    *The generated files*:
        * d3.v3.js, contains the D3 Data-driven Documents source code, containing one small addition that we made in order to be able to easyly import links with a different formatself.
        * digraph3lib.js, contains our library. This file contains everything that we need from import of an XMCDA2 file, visualization of the graph to export of the changed graph.
        * d3export.json, usually named after the python graph name followed by a ticket number if the file is already present. It is the JSON file that is exported with the format "{"xmcda2": "some xml","pairwiseComparisions":"{"a01": "some html",...}"}.

    *Example 1*:
        #. python3 session:
            >>> from digraphs import RandomValuationDigraph
            >>> dg = RandomValuationDigraph(order=5,Normalized=True)
            >>> dg.exportD3()
            or
            >> dg.showInteractiveGraph()
    
        #. index.html:   
            * Main Screen:
                .. image:: randomvaluation_d3_main.png
            * Inspect function:
                .. image:: randomvaluation_d3_inspect.png

    .. note::
    
            If you want to use the automatic load in Chrome, try using the command: "python -m SimpleHTTPServer"
            and then access the index.html via "http://0.0.0.0:8000/index.html".
            In order to load the CSS an active internet connection is needed! 

        """
        import os
        import json
        import urllib
        import htmlmodel,json

        if Comments:
            print('*---- exporting all needed files ---------*')

        if fileName == "index":
            fileName = self.name

        file=fileName+".html"
        dst_dir=os.getcwd()
        basename = os.path.basename(file)
        head, tail = os.path.splitext(basename)
        dst_file = os.path.join(dst_dir, basename)
        # rename if necessary
        count = 0
        print(dst_file)
        while os.path.exists(dst_file):
            count += 1
            dst_file = os.path.join(dst_dir, '%s-%d%s' % (head, count, tail))

        actionkeys = [x for x in self.actions]
        n = len(actionkeys)
        relation = self.relation
        Med = self.valuationdomain['med']
        
        pageName=""
              
        
        fw = open("digraph3lib.js",'w')
        fw.write(htmlmodel.javascript())
        fw.close()
        if Comments:
            print("File: digraph3lib.js saved!")

        fw = open("d3.v3.js",'w')
        fw.write(htmlmodel.d3export())
        fw.close()
        if Comments:
            print("File: d3.v3.js saved!")
        pairwise={}
        try:
            for x in self.actions:
                pairwise[x]={}
            for x in actionkeys:
                for y in actionkeys:
                    if(not(x == y)):
                        pairwise[x][y] =  str(self.showPairwiseComparison(x,y,isReturningHTML=True))
        except:
            pairwise={}
        d3export={}
        if(pairwise):
            temp = "outranking_"+fileName
            self.saveXMCDA2(fileName=temp+"-"+str(count))
        else:
            temp = "general_"+fileName
            self.saveXMCDA2(fileName=temp+"-"+str(count))
        with open(temp+"-"+str(count)+".xmcda2","r") as myFile:
            data=myFile.read().replace("\n","")
        try:
            os.remove(temp+"-"+str(count)+".xmcda2")
        except OSError:
            pass
        d3export["xmcda2"]= str(data)
        d3export["pairwiseComparisions"] = json.dumps(pairwise)

        if(count==0):
            fw = open(temp+".json","w")
            if Comments:
                print("File: "+temp+".json saved!") 
        else:
            fw = open(temp+"-"+str(count)+".json","w")
            if Comments:
                print("File:"+temp+"-"+str(count)+".json saved!") 
        fw.write(json.dumps(d3export))
        fw.close()

        if(count==0):
            fw = open(fileName+".html","w")
            fw.write(htmlmodel.htmlmodel(jsonName=temp+".json"))
            pageName=fileName+".html"
            if Comments:
                print("File: "+fileName+".html generated!")
        else:
            fw = open(fileName+"-"+str(count)+".html",'w')
            fw.write(htmlmodel.htmlmodel(jsonName=temp+"-"+str(count)+".json"))
            pageName=fileName+"-"+str(count)+".html"
            if Comments:
                print("File: "+fileName+"-"+str(count)+".html generated!")
        fw.close()

        if Comments:
            print('*---- export done ---------*')
        return pageName

    def showInteractiveGraph(self):
        '''
        Save the graph and all needed files for the visualization of an interactive graph generated by the exportD3() function.
        For best experience make sure to use Firefox, because other browser restrict the loading of local files.
        '''
        import os,webbrowser
        newTab=2
        url = "file://"+os.getcwd()+"/%s" % self.exportD3()
        webbrowser=webbrowser.get("firefox")
        webbrowser.open(url,new=newTab)
    
            
    def savedre(self,fileName='temp'):
        """
        save digraph in nauty format.
        """
        print('*----- saving digraph in nauty dre format  -------------*')
        actions = [x for x in self.actions]
        Name = fileName+'.dre'
        aindex = {}
        i = 1
        print('Actions index:')
        for x in actions:
            print(i,': ', str(x))
            aindex[x] = i
            i += 1
        Med = self.valuationdomain['med']
        relation = self.relation
        n = len(actions)
        fo = open(Name,'w')
        fo.write('n='+str(n)+' $=1 d g\n')
        for x in actions:
            res = str(aindex[x]) + ': '
            for y in actions:
                if relation[x][y] > Med:
                    res = res + str(aindex[y]) + ' '
            res = res + ';\n'
            fo.write(res)
        fo.close()
        self.aindex = aindex.copy()

    def saveXML(self,fileName='temp',category='general',subcategory='general',author='digraphs Module (RB)',reference='saved from Python'):
        """
        save digraph in XML format.
        """
        print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = fileName+'.xml'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="digraphs.xsl"?>\n')
        fo.write('<!DOCTYPE digraph SYSTEM "digraphs.dtd">\n')
        fo.write('<digraph ')
        fo.write('category="' + category+'" subcategory="'+subcategory+'">\n')
        fo.write('<header>\n')
        fo.write('<name>')
        fo.write(nameExt)
        fo.write('</name>\n')
        fo.write('<author>')
        fo.write(author)
        fo.write('</author>\n')
        fo.write('<reference>')
        fo.write(reference)
        fo.write('</reference>\n')
        fo.write('</header>')
        actions = self.actions
        fo.write('<nodes>\n')
        for x in actions:
            fo.write('<node>')
            fo.write(str(x))
            fo.write('</node>\n')
        fo.write('</nodes>\n')
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        fo.write('<valuationdomain>\n')
        fo.write('<min>')
        fo.write(str(Min))
        fo.write('</min>\n')
        fo.write('<max>')
        fo.write(str(Max))
        fo.write('</max>\n')
        fo.write('</valuationdomain>\n')
        fo.write('<relation>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<arc>\n')
                fo.write('<i>')
                fo.write(str(x))
                fo.write('</i>\n')
                fo.write('<t>')
                fo.write(str(y))
                fo.write('</t>\n')
                fo.write('<v>')
                fo.write(str(relation[x][y]))
                fo.write('</v>\n')
                fo.write('</arc>\n')
        fo.write('</relation>\n')
        fo.write('</digraph>\n')
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMCDA(self,fileName='temp',relationName='R',category='random',subcategory='valued',author='digraphs Module (RB)',reference='saved from Python',valuationType='standard',servingD3=False):
        """
        save digraph in XMCDA format.
        """
        print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = fileName+'.xmcda'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2008/UMCDA-ML-1.0 umcda-ml-1.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2008/UMCDA-ML-1.0">\n'))
        # write description
        fo.write('<caseReference>\n')
        fo.write('<title>Valued Digraph in XMCDA format</title>\n')
        fo.write('<id>%s</id>\n' % (fileName) )
        fo.write('<name>%s</name>\n' % (self.name) )
        fo.write('<type>root</type>\n')
        fo.write('<user>%s</user>\n' % (author) )
        fo.write('<version>%s</version>\n' % (reference) )
        fo.write('</caseReference>\n')
        # write nodes
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives>\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('List of Alternatives'))
        fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('<comment>Potential decision actions.</comment>\n')
        fo.write('</description>\n')
        for i in range(na):
            fo.write('<alternative id="%s">\n' % (actionsList[i]))
            fo.write('<description>\n')
            fo.write('<name>')
            try:
                fo.write(str(actions[actionsList[i]]['name']))
            except:
                fo.write('nameless')
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                fo.write('No comment')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<alternativeType>potential</alternativeType>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        # write valued binary Relation
        fo.write('<relationOnAlternatives>\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Valued Binary Relation'))
        fo.write('<name>%s</name>\n' % (relationName) )
        fo.write('<type>%s</type>\n' % ('valuedBinaryRelation'))
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        fo.write('<valuationDomain>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valuation Domain'))
        fo.write('</description>\n')
        fo.write('<valuationType>%s</valuationType>\n' % (valuationType) )
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        fo.write('<minimum><real>%2.2f</real></minimum>\n' % (Min))
        fo.write('<maximum><real>%2.2f</real></maximum>\n' % (Max))
        fo.write('</valuationDomain>\n')
        fo.write('<arcs>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valued Adjacency Table'))
        try:
            category = self.category
            subcategory = self.subcategory
        except:
            pass
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<arc>\n')
                fo.write('<from><alternativeID>')
                fo.write(str(x))
                fo.write('</alternativeID></from>\n')
                fo.write('<to><alternativeID>')
                fo.write(str(y))
                fo.write('</alternativeID></to>\n')
                fo.write('<value><real>%2.2f' % (relation[x][y]) )
                fo.write('</real></value>\n')
                fo.write('</arc>\n')
        fo.write('</arcs>\n')
        fo.write('</relationOnAlternatives>\n')
        fo.write('</xmcda:XMCDA>\n')
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMCDA2(self,fileName='temp',fileExt='xmcda2',
                   Comments=True,relationName='R',relationType='binary',
                   category='random',subcategory='valued',
                   author='digraphs Module (RB)',reference='saved from Python',
                   valuationType='standard',digits=2,servingD3=False):
        """
        save digraph in XMCDA format.
        """
        if Comments:
            print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = fileName+"."+fileExt
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcdaXSL.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/UMCDA-2.0.0 file:../XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">\n'))
        # write description
        fo.write('<projectReference id="%s" name="%s">\n' % (fileName,self.name))
        fo.write('<title>Stored Digraph in XMCDA-2.0 format</title>\n')
        #fo.write('<id>%s</id>\n' % (fileName) )
        #fo.write('<name>%s</name>\n' % (self.name) )
        #fo.write('<type>root</type>\n')
        fo.write('<user>%s</user>\n' % (author) )
        fo.write('<version>%s</version>\n' % (reference) )
        fo.write('</projectReference>\n')
        # write nodes
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives mcdaConcept="Digraph nodes">\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Nodes of the digraph'))
        #fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('<comment>Set of nodes of the digraph.</comment>\n')
        fo.write('</description>\n')
        for i in range(na):
            try:
                alternativeName = str(actions[actionsList[i]]['name'])
            except:
                alternativeName = 'nameless'

            fo.write('<alternative id="%s" name="%s">\n' % (actionsList[i],alternativeName))
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                fo.write('No comment')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<type>real</type>\n')
            fo.write('<active>true</active>\n')
            fo.write('<reference>false</reference>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        # write valued binary Relation
        fo.write('<alternativesComparisons id="1" name="%s">\n' % (relationName))
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Randomly Valued Binary Relation'))
        #fo.write('<name>%s</name>\n' % (relationName) )
        #fo.write('<type>%s</type>\n' % ('valuedBinaryRelation'))
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        fo.write('<valuation name="valuationDomain">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valuation Domain'))
        fo.write('</description>\n')
        fo.write('<quantitative>')
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        if valuationType == 'integer':
            fo.write('<minimum><integer>%d</integer></minimum>\n' % (Min))
            fo.write('<maximum><integer>%d</integer></maximum>\n' % (Max))
        else:
            formatString = '%%2.%df' % (digits)
            fo.write('<minimum><real>')
            fo.write(formatString % (Min))
            fo.write('</real></minimum>\n')
            fo.write('<maximum><real>')
            fo.write(formatString % (Max))
            fo.write('</real></maximum>\n')
        fo.write('</quantitative>\n')
        fo.write('</valuation>\n')
        fo.write('<comparisonType>%s</comparisonType>\n' % (relationName))
        fo.write('<pairs>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valued Adjacency Table'))
        try:
            category = self.category
            subcategory = self.subcategory
        except:
            pass
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<pair>\n')
                fo.write('<initial><alternativeID>')
                fo.write(str(x))
                fo.write('</alternativeID></initial>\n')
                fo.write('<terminal><alternativeID>')
                fo.write(str(y))
                fo.write('</alternativeID></terminal>\n')
                if valuationType == 'bipolar':
                    formatString = '%%+2.%df' % (digits)
                else:
                    formatString = '%%2.%df' % (digits)
                fo.write('<value><real>')
                fo.write(formatString % (relation[x][y]) )
                fo.write('</real></value>\n')
                fo.write('</pair>\n')
        fo.write('</pairs>\n')
        fo.write('</alternativesComparisons>\n')
        fo.write('</xmcda:XMCDA>\n')
        fo.close()
        if Comments:
            print('File: ' + nameExt + ' saved !')


    def computeDensities(self,choice):
        """
        parameter: choice in self
        renders the four densitiy parameters:
        arc density, double arc density, single arc density, absence arc density.
        """
        actions = set(choice)
        relation = self.relation
        Med = self.valuationdomain['med']
        order = float(len(actions))
        d = 0.0
        dd = 0.0
        sd = 0.0
        ad = 0.0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        d += 1.0
                    if relation[x][y] > Med and relation[y][x] > Med:
                        dd += 1.0
                    if relation[x][y] > Med and relation[y][x] <= Med:
                        sd += 1.0
                    if relation[x][y] <= Med and relation[y][x] <= Med:
                        ad += 1.0
        d = d / (order*(order-1))
        dd / (order*(order-1))
        sd = (2*sd) / (order*(order-1))
        ad = ad / (order*(order-1))
        return d,dd,sd,ad

    def computeCutLevelDensities(self,choice,level):
        """
        parameter: choice in self, robustness level
        renders three robust densitiy parameters:
        robust double arc density,
        robust single arc density,
        robust absence arc densitiy.
        """
        actions = set(choice)
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        negLevel = Max - level + Min
        order = float(len(actions))
        rdd = 0.0
        rsd = 0.0
        rad = 0.0
        if level < Med or level >= Max:
            print('Error: robustness level too low or too high !!!')
        else:
            for x in actions:
                for y in actions:
                    if x != y:
                        if relation[x][y] > level and relation[y][x] > level:
                            rdd += 1.0
                        if relation[x][y] > level:
                            if relation[y][x] < negLevel:
                                rsd += 1.0
                        if relation[x][y] < negLevel and relation[y][x] < negLevel:
                            rad += 1.0
            rdd = rdd / (order*(order-1))
            rsd = (2*rsd) / (order*(order-1))
            rad = rad / (order*(order-1))
        density = {}
        density['double'] = rdd
        density['single'] = rsd
        density['absence'] = rad
        return density

    def computeAllDensities(self,choice=None):
        """
        parameter: choice in self
        renders six densitiy parameters:
        arc density, double arc density,
        single arc density, strict single arc density,
        absence arc density, strict absence arc densitiy.
        """
        if choice != None:
            actions = set(choice)
        else:
            actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        order = float(len(actions))
        d = 0.0
        dd = 0.0
        sd = 0.0
        ssd = 0.0
        ad = 0.0
        asd = 0.0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        d += 1.0
                    if relation[x][y] > Med and relation[y][x] > Med:
                        dd += 1.0
                    if relation[x][y] > Med:
                        if relation[y][x] < Med:
                            ssd += 1.0
                            sd += 1.0
                        elif relation[y][x] == Med:
                            sd += 1.0
                    if relation[x][y] <= Med and relation[y][x] <= Med:
                        ad += 1.0
                    if relation[x][y] < Med and relation[y][x] < Med:
                        asd += 1.0
        d = d / float(order*(order-1))
        dd = dd / float(order*(order-1))
        sd = (2*sd) / float(order*(order-1))
        ssd = (2*ssd) / float(order*(order-1))
        ad = ad / float(order*(order-1))
        asd = asd / float(order*(order-1))
        density = {}
        density['arc'] = d
        density['double'] = dd
        density['single'] = sd
        density['strictSingle'] = ssd
        density['absence'] = ad
        density['strictAbsence'] = asd
        return density

    def computeValuationLevels(self,choice=None, Debug=False):
        """
        renders the symmetric closure of the
        apparent valuations levels of self
        in an increasingly ordered list.
        If parameter choice is given, the
        computation is limited to the actions
        of the choice.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']

        if choice == None:
            actions = [x for x in self.actions]
        else:
            actions = [x for x in choice]

        relation = self.relation

        levels = set([Max,Min])
        for x in actions:
            for y in actions:
                levels.add(relation[x][y])
                levels.add(Max - relation[x][y] + Min)
        ## if Debug:
        ##     print levels
        levelsList = list(levels)
        levelsList.sort()
        if Debug:
            print('levelsList', levelsList)
        return levelsList

    def computePrudentBetaLevel(self, Debug=False):
        """
        computes alpha, ie the lowest valuation level, for which the
        bipolarly polarised digraph doesn't contain a chordless circuit.
        """
        Med = self.valuationdomain['med']
        valuationLevels= self.computeValuationLevels(Debug=Debug)
        if Debug:
            print('number of levels; %d' % len(valuationLevels))
        valuationLevels.reverse()
        for i in range(len([x for x in valuationLevels if x > Med])):
            level = valuationLevels[i+1]
            if Debug:
                print('checking level: ', level)
            gp = PolarisedDigraph(self,level=level)
            if len(gp.computeChordlessCircuits()) > 0:
                if Debug:
                    gp.showChordlessCircuits()
                    print('prudent order level = %s (med = %.2f)' % (str(valuationLevels[i-1]),Med))
                self.prudentBetaLevel = valuationLevels[i]
                return self.prudentBetaLevel

        self.prudentBetaLevel = Med
        if Debug:
            ## self.computeChordlessCircuits()
            ## self.showChordlessCircuits()
            print('prudent order level = %s = med' % str(Med))
        return Med

    def computeValuationPercentiles(self,choice, percentages, withValues=False):
        """
        Parameters: choice and list of percentages.
        renders a series of quantiles of the characteristics valuation of
        the arcs in the digraph.
        """
        relation = self.relation
        vx = []
        for x in choice:
            for y in choice:
                if x != y:
                    vx.append(relation[x][y])
        vx.sort()
        if withValues:
            print('values ', vx)
        nv = len(vx)
        percentile = {}
        for q in percentages:
            kq = q*nv//100
            r = (nv*q)% 100
            if q == 0:
                percentile[q] = vx[0]
            elif q == 100:
                percentile[q] = vx[nv-1]
            else:
                percentile[q] = vx[kq-1] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq]-vx[kq-1])
        return percentile

    def computeValuationPercentages(self,choice,percentiles,withValues=False):
        """
        Parameters: choice and list of percentages.
        renders a series of quantiles of the characteristics valuation of
        the arcs in the digraph.
        """
        relation = self.relation
        vx = []
        for x in choice:
            for y in choice:
                if x != y:
                    vx.append(relation[x][y])
        vx.sort()
        nv = len(vx)
        if withValues:
            print('values ', vx)
        np = len(percentiles)
        rv = [0.0 for i in range(np)]
        for val in vx:
            for i in range(np):
                if percentiles[i] > val:
                    rv[i] += 1.0
        percentages = {}
        for i in range(np):
            percentages[percentiles[i]] = rv[i]/float(nv)
        return percentages

    def computeAverageValuation(self):
        """
        Computes the bipolar average correlation between
        self and the crisp complete digraph of same order
        of the irreflexive and determined arcs of the digraph
        """
        Med = self.valuationdomain['med']
        relation = self.relation
        averageValuation = Decimal('0.0')
        determined = Decimal('0.0')
        #actionsList = [x for x in self.actions]
        nbDeterm = 0
        for x,rx in relation.items():
            for y,rxy in rx.items():
                if x != y:
                    if rxy != Med:
                        nbDeterm += 1
                        averageValuation += rxy
                        determined += abs(rxy)
        return averageValuation / determined

    def computeDeterminateness(self,InPercents=False):
        """
        Computes the Kendalll distance of self
        with the all median-valued indeterminate digraph of order n.

        Return the average determination of the irreflexive part of the digraph.

        *determination* = sum_(x,y) { abs[ r(xRy) - Med ] } / n(n-1)
        
        If *InPercents* is True, returns the average determination in percentage of
        (Max - Med) difference.

        >>> from outrankingDigraphs import BipolarOutrankingDigraph
        >>> from randomPerfTabs import Random3ObjectivesPerformanceTableau
        >>> t = Random3ObjectivesPerformanceTableau(numberOfActions=7,numberOfCriteria=7,seed=101)
        >>> g = BipolarOutrankingDigraph(t,Normalized=True)
        >>> g
        *------- Object instance description ------*
        Instance class      : BipolarOutrankingDigraph
        Instance name       : rel_random3ObjectivesPerfTab
        # Actions           : 7
        # Criteria          : 7
        Size                : 27
        Determinateness (%) : 65.67
        Valuation domain    : [-1.00;1.00]
        >>> print(g.computeDeterminateness())
        0.3134920634920634920634920638
        >>> print(g.computeDeterminateness(InPercents=True))
        65.67460317460317460317460320
        >>> g.recodeValuation(0,1)
        >>> g
        *------- Object instance description ------*
        Instance class      : BipolarOutrankingDigraph
        Instance name       : rel_random3ObjectivesPerfTab
        # Actions           : 7
        # Criteria          : 7
        Size                : 27
        Determinateness (%) : 65.67
        Valuation domain    : [0.00;1.00]
        >>> print(g.computeDeterminateness())
        0.1567460317460317460317460318
        >>> print(g.computeDeterminateness(InPercents=True))
        65.67460317460317460317460320

        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        relation = self.relation
        #actions = self.actions
        order = self.order
        D = Decimal('0.0')
        for x,rx in relation.items():
            for y,rxy in rx.items():
                if x != y:
                    D += abs(rxy - Med)
        if order > 1:
            determination = D / Decimal(str((order * (order-1))))
        else:
            determination = D
        if InPercents:
            return (determination / (Max-Med) + Decimal('1')) / Decimal('2') * Decimal('100.0')
        else:
            return determination

    def showStatistics(self):
        """
        Computes digraph statistics like order, size and arc-density.
        """
        #import array
        print('*----- general statistics -------------*')
        nbrcomp = len(self.components())
        nbrstrcomp = len(self.strongComponents())
        actions = [x for x in self.actions]
        relation = self.relation
        order = len(actions)
        size,undeterm,arcDensity = self.sizeSubGraph(actions)
        self.size = size
        self.undeterm = undeterm
        density = self.computeAllDensities(actions)
        self.arcDensity = density['arc']
        outDegrees = self.outDegreesDistribution()
        inDegrees = self.inDegreesDistribution()
        symDegrees = self.symDegreesDistribution()
        nbDepths = self.neighbourhoodDepthDistribution()
        nb = len(nbDepths)
        meanLength = 0.0
        for i in range(nb):
            meanLength += i * nbDepths[i]
        if nbDepths[nb-1] != 0:
            meanLength = 'infinity'
        else:
            meanLength = float(meanLength/order)

        self.meanNeighbourhoodDepth = meanLength

        self.digraphDiameter = self.diameter()

        self.agglomerationCoefficient,self.meanAgglomerationCoefficient = self.agglomerationDistribution()
        # Outranking determinateness
##        Max = self.valuationdomain['max']
##        Med = self.valuationdomain['med']
##        deter = Decimal('0.0')
##        for x,rx in relation.items():
##            for y,rxy in rx.items():
##                if x != y:
##                    # print(relation[x][y], Med)
##                    deter += abs(rxy - Med)
##        deter /= order * (order-1) * (Max - Med)
        deter = self.computeDeterminateness(InPercents=True)
        #  output results
        print('for digraph              : <' + str(self.name) + '.py>')
        print('order                    :', self.order, 'nodes')
        print('size                     :', self.size, 'arcs')
        print('# undetermined           :', self.undeterm, 'arcs')
        print('determinateness (in %%)   : %.2f' % (deter))
        print("arc density              : %.2f" % (density['arc']))
        print("double arc density       : %.2f" % (density['double']))
        print("single arc density       : %.2f" % (density['single']))
        print("absence density          : %.2f" % (density['absence']))
        print("strict single arc density: %.2f" % (density['strictSingle']))
        print("strict absence density   : %.2f" % (density['strictAbsence']))
        print('# components             : ', nbrcomp)
        print('# strong components      : ', nbrstrcomp)
        print('transitivity degree      : %.2f' % (self.computeTransitivityDegree()))

        print('                         :', list(range(len(outDegrees))))
        print('outdegrees distribution  :', list(outDegrees))
        print('indegrees distribution   :', list(inDegrees))
        print('mean outdegree           : %.2f' % (self.computeMeanOutDegree()))
        print('mean indegree            : %.2f' % (self.computeMeanInDegree()))
        print('                         :', list(range(len(symDegrees))))
        print('symmetric degrees dist.  :', list(symDegrees))
        print('mean symmetric degree    : %.2f' % (self.computeMeanSymDegree()))

        outgini = self.computeConcentrationIndex(list(range(len(outDegrees))),list(outDegrees))
        ingini = self.computeConcentrationIndex(list(range(len(inDegrees))),list(inDegrees))
        symgini = self.computeConcentrationIndex(list(range(len(symDegrees))),list(symDegrees))
        print('outdegrees concentration index    : %.4f' % (outgini))
        print('indegrees concentration index     : %.4f' % (ingini))
        print('symdegrees concentration index    : %.4f' % (symgini))
        listindex = list(range(order))
        listindex.append('inf')
        print('                                  :', listindex)
        print('neighbourhood depths distribution :', list(nbDepths))
        if meanLength != 'infinity':
            print("mean neighbourhood depth         : %.2f " % (meanLength))
        else:
            print('mean neighbourhood length         :', meanLength)
        print('digraph diameter                  :', self.digraphDiameter)
        print('agglomeration distribution        :')
        for i in range(order):
            print(actions[i], end=' ')
            print(": %.2f" % (self.agglomerationCoefficient[i]))
        print("agglomeration coefficient         : %.2f" % (self.meanAgglomerationCoefficient))

    def meanLength(self,Oriented=False):
        """
        Renders the (by default non-oriented) mean neighbourhoor depth of self.
        !!! self.order must be set previously !!!
        """
        nbDepths = self.neighbourhoodDepthDistribution(Oriented)
        nb = len(nbDepths)
        meanLength = 0.0
        for i in range(nb):
            meanLength += i * nbDepths[i]
        if nbDepths[nb-1] != 0:
            meanLength = 'infinity'
        else:
            meanLength = meanLength/float(self.order)
        return meanLength

    def meanDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        inDegrees = self.inDegreesDistribution()
        degrees = []
        nd = len(outDegrees)
        meanDegree = 0.0
        for i in range(nd):
            degrees.append(outDegrees[i]+inDegrees[i])
            meanDegree += i * (max(outDegrees[i],inDegrees[i]))
        if self.size == 0:
            meanDegree = 0
        else:
            meanDegree = meanDegree/float(2 * self.order)
        return meanDegree

    def computeMeanOutDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        nd = len(outDegrees)
        meanOutDegree = 0.0
        for i in range(nd):
            meanOutDegree += i * outDegrees[i]
        if self.size == 0:
            meanOutDegree = 0
        else:
            meanOutDegree = meanOutDegree/float(self.order)
        return meanOutDegree

    def computeMeanInDegree(self):
        """
        Renders the mean indegree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        inDegrees = self.inDegreesDistribution()
        nd = len(inDegrees)
        meanInDegree = 0.0
        for i in range(nd):
            meanInDegree += i * inDegrees[i]
        if self.size == 0:
            meanInDegree = 0
        else:
            meanInDegree = meanInDegree/self.order
        return meanInDegree

    def computeMedianOutDegree(self):
        """
        Renders the median outdegree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        nd = len(outDegrees)
        outDegreesList = []
        for d in range(nd):
            for x in range(outDegrees[d]):
                outDegreesList.append(d)
        outDegreesList.sort()
        #print 'outdegrees sorted', outDegreesList
        ndl = len(outDegreesList)
        if ndl % 2 == 0:
            medpos = ndl//2
            medianOutDegree = outDegreesList[medpos]
        else:
            medpos0 = ndl//2
            medpos1 = (ndl + 1)//2
            medianOutDegree =  (outDegreesList[medpos0] + outDegreesList[medpos1])/2
        return medianOutDegree

    def computeMedianSymDegree(self):
        """
        Renders the median symmetric degree of self.
        !!! self.size must be set previously !!!
        """
        symDegrees = self.symDegreesDistribution()
        nd = len(symDegrees)
        symDegreesList = []
        for d in range(nd):
            for x in range(symDegrees[d]):
                symDegreesList.append(d)
        nd = len(symDegrees)
        symDegreesList.sort()
        ndl = len(symDegreesList)
        if ndl % 2 == 0:
            medpos = ndl//2
            medianSymDegree = symDegreesList[medpos]
        else:
            medpos0 = ndl/2
            medpos1 = (ndl + 1)//2
            medianSymDegree =  (symDegreesList[medpos0] + symDegreesList[medpos1])/2
        return medianSymDegree

    def computeMeanSymDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = float(len(self.actions))
        symDegrees = self.symDegreesDistribution()
        nd = len(symDegrees)
        meanSymDegree = 0.0
        for i in range(nd):
            meanSymDegree += i * symDegrees[i]
        if self.size == 0:
            meanSymDegree = 0.0
        else:
            meanSymDegree = meanSymDegree/self.order
        return meanSymDegree

    def diameter(self, Oriented = False):
        """
        Renders the (by default non-oriented) diameter of the digraph instance
        """
        order = len(self.actions)
        nbDepths = self.neighbourhoodDepthDistribution(Oriented)
        nbDepths.reverse()
        if nbDepths[0] != 0:
            diameter = 'infinity'
        else:
            diameter = 0
            for i in range(len(nbDepths)):
                if nbDepths[i+1] != 0:
                    diameter = order - (i+1)
                    break
        return diameter

    def _graphDetermination(self,Normalized=True):
        """
        Output: average normalized (by default) arc determination:

        averageDeterm = ( sum_(x,y) [ abs( relf-relation[x][y] - Med )] / n ) / [( Max-Med ) if Normalized],

        where Med = self.valuationdomain['med'] and Max = self.valuationdomain['max'].
        
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        determ = Decimal("0.0")
        for x,rx in self.relation.items():
            for y,rxy in rx.items():
                if rxy > Med:
                    determ += rxy - Med
                else:
                    determ += Med - rxy
        if Normalized:
            averageDeterm = (determ / Decimal(str(self.order)))/(Max-Med)
        else:
            averageDeterm = (determ / Decimal(str(self.order)))
        return  averageDeterm

    def computeSize(self):
        """
        Renders the number of validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        #actions = [x for x in self.actions]
        #actions = self.actions
        #relation = self.relation
        size = 0
        for x,rx  in self.relation.items():
            for y,rxy in rx.items():
                if x != y:
                    if rxy > Med:
                        size += 1
        return size

    def computeCoSize(self):
        """
        Renders the number of non validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        #actions = [x for x in self.actions]
        #relation = self.relation
        coSize = 0
        for x,rx in self.relation.items():
            for y,rxy in rx.items():
                if x != y:
                    if rxy < Med:
                        coSize += 1
        return coSize

    def sizeSubGraph(self,choice):
        """
        Output: (size, undeterm,arcDensity).
        Renders the arc density of the induced subgraph.
        """
        Med = self.valuationdomain['med']
        relation = self.relation
        order = float(len(choice))
        size = 0
        undeterm = 0
        for x in choice:
            rx = relation[x]
            for y in choice:
                if x != y:
                    if rx[y] > Med:
                        size += 1
                    if rx[y] == Med:
                        undeterm += 1
        if len(choice) < 2:
            arcDensity = 0.0
        else:
            arcDensity = (size * 100.0)/ (order * (order - 1 ))
        return size, undeterm, arcDensity

    def agglomerationDistribution(self):
        """
        Output: aggloCoeffDistribution, meanCoeff
        Renders the distribution of agglomeration coefficients.
        """
        import array
        actions = [x for x in self.actions]
        order = len(actions)
        aggloCoeff = array.array('f', [0] * order)
        meanCoeff = 0.0
        for i in range(order):
            neighborhood = self.gamma[actions[i]][0] | self.gamma[actions[i]][1]
            size, undeterm, aggloCoeff[i] = self.sizeSubGraph(neighborhood)
            meanCoeff += aggloCoeff[i]
        if order == 0:
            meanCoeff = 0.0
        else:
            meanCoeff /= order
        return aggloCoeff, meanCoeff

    def outDegreesDistribution(self):
        """
        Renders the distribution of outdegrees.
        """
        import array
        order = len(self.actions)
        outDegrees = array.array('i', [0] * (order+1))
        for x in self.actions:
            nx = len(self.gamma[x][0])
            outDegrees[nx] += 1
        return outDegrees

    def computeConcentrationIndexTrapez(self,X,N):
        """
        Renders the Gini concentration index of the X serie.
        N contains the partial frequencies.
        Based on the triangles summation formula.
        """
        n = len(X)
        #dg = self.outDegreesDistribution()
        X = list(range(10))
        N = [0,0,0,0,0,0,0,0,0,0,]
        print('Xi ', X, N)
        Q = [0.0 for i in range(n)]
        F = [0.0 for i in range(n)]
        Qsum = 0.0
        for i in range(n):
            Qsum += X[i] * N[i]
        print('Qsum ',Qsum)
        F[0] = float(X[0])/float(n)
        Q[0] = 0.0
        for i in range(1,n,1):
            qi = (X[i] * N[i])/Qsum
            Q[i] += Q[i-1] + qi
            print('Q[i] i ', i, Q[i])
            fi = float(N[i])/n
            F[i] += F[i-1] + fi
            print('i, F[i]', i, F)
        f0 = float(N[0])/float(n)
        gini = 1.0 - (f0*Q[0])
        print('o gini ', gini)
        for i in range(1,n):
            fi = (float(N[i])/float(n))
            gini -= fi * (Q[i-1] + Q[i])
            print('i gini', i, gini)
        return gini

    def computeConcentrationIndex(self,X,N):
        """
        Renders the Gini concentration index of the X serie.
        N contains the partial frequencies.
        Based on the triangle summation formula.
        """
        Qsum = 0.0
        n = 0.0
        r = len(X)
        for i in range(r):
            n += N[i]
            Qsum += X[i] * N[i]
        if Qsum != 0.0:
            Q = [0.0 for i in range(r)]
            F = [0.0 for i in range(r)]
            F[0] = N[0]/n
            Q[0] = (X[0] * N[0])/Qsum
            for i in range(1,r,1):
                qi = (X[i] * N[i])/Qsum
                Q[i] += Q[i-1] + qi
                fi = N[i]/n
                F[i] += F[i-1] + fi
            gini = 0.0
            for i in range(r-1):
                gini += (F[i]*Q[i+1]) - (Q[i]*F[i+1])
        else:
            gini = -1
        return gini

    def inDegreesDistribution(self):
        """
        Renders the distribution of indegrees.
        """
        import array
        order = len(self.actions)
        inDegrees = array.array('i', [0] * (order+1))
        for x in self.actions:
            nx = len(self.gamma[x][1])
            inDegrees[nx] += 1
        return inDegrees

    def symDegreesDistribution(self):
        """
        Renders the distribution of symmetric degrees.
        """
        import array
        order = len(self.actions)
        symDegrees = array.array('i', [0] * ((2*order)+1))
        for x in self.actions:
            nx = len(self.gamma[x][0])+len(self.gamma[x][1])
            symDegrees[nx] += 1
        return symDegrees

    def neighbourhoodDepthDistribution(self, Oriented=False):
        """
        Renders the distribtion of neighbourhood depths.
        """
        import array,copy
        actions = set(self.actions)
        order = len(actions)
        nv = order + 1
        vecNeighbourhoodDepth = array.array('i', [0] * nv)
        for x in actions:
            nbx = 0
            neighbx = set([x])
            restactions = actions - neighbx
            while restactions != set() and nbx < order:
                nbx += 1
                iterneighbx = copy.copy(neighbx)
                for y in iterneighbx:
                    if Oriented:
                        neighbx = neighbx | self.gamma[y][0]
                    else:
                        neighbx = neighbx | self.gamma[y][0] | self.gamma[y][1]
                restactions = actions - neighbx
            if restactions != set():
                vecNeighbourhoodDepth[order] += 1
            else:
                vecNeighbourhoodDepth[nbx] += 1
        return vecNeighbourhoodDepth


    def neighbourhoodCollection(self, Oriented = False, Potential = False):
        """
        Renders the neighbourhood.
        """
        import array,copy
        actions = set(self.actions)
        order = len(actions)
        if Potential:
            weakGamma = self.weakGammaSets()
        neighbourhoods = {}
        for x in actions:
            nbx = 0
            neighbx = set([x])
            restactions = actions - neighbx
            while restactions != set() and nbx < order:
                nbx += 1
                iterneighbx = copy.copy(neighbx)
                for y in iterneighbx:
                    if Potential:
                        if Oriented:
                            neighbx = neighbx | weakGamma[y][0]
                        else:
                            neighbx = neighbx | weakGamma[y][0] | weakGamma[y][1]
                    else:
                        if Oriented:
                            neighbx = neighbx | self.gamma[y][0]
                        else:
                            neighbx = neighbx | self.gamma[y][0] | self.gamma[y][1]
                    restactions = actions - neighbx
            #print 'neighbx', neighbx
            neighbourhoods[x]= neighbx
        return neighbourhoods

    def strongComponents(self, setPotential = False):
        """
        Renders the set of strong components of self.
        """
        neighbourhoods = self.neighbourhoodCollection(Oriented = True, Potential = setPotential)
        strongComponents = set()
        for x in self.actions:
            componentx = set([x])
            for y in neighbourhoods[x]:
                if x in neighbourhoods[y]:
                    componentx = componentx | set([y])
            strongComponents = strongComponents | set([frozenset(componentx)])
        return strongComponents

    def showMIS(self,withListing=True):
        """
        Prints all maximal independent choices:
            Result in self.misset.

        """
        import time
        print('*---  Maximal independent choices ---*')
        t0 = time.time()
        self.misset = set()
        actions = set(self.actions)
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.MISgen(actions,frozenset()):
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.misset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.misset')

    def showMinDom(self,withListing=True):
        """
        Prints all minimal dominant choices:
            Result in self.domset.

        """
        import time
        print('*--- Computing minimal dominant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        cover = {}
        for x in actions:
            cover[x]=self.gamma[x][1] | set([x])
        dom1 = (frozenset(list(actions)),cover)
        #print dom1
        self.minset = set()
        self.minhistory = set()
        for choice in self.minimalChoices(dom1):
            pass
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.minset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.minset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('iteration history: ', len(self.minhistory))
        self.domset = self.minset.copy()
        print('Results in self.domset')

    def showMinAbs(self,withListing=True):
        """
        Prints minimal absorbent choices:
            Result in self.absset.

        """
        import time
        print('*--- Computing minimal absorbent choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        cover = {}
        for x in actions:
            cover[x]=self.gamma[x][0] | set([x])
        abs1 = (frozenset(list(actions)),cover)
        print(abs1)
        self.minset = set()
        self.minhistory = set()
        for choice in self.minimalChoices(abs1):
            pass
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.minset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.minset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('iteration history: ', len(self.minhistory))
        self.absset = self.minset.copy()
        print('Results in self.absset')

    def showMaxDomIrred(self,withListing=True):
        """
        Computing maximal +irredundant choices:
           Result in self.domirset.

        """
        import time
        print('*--- Computing maximal +irredundant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        self.domirset = set()
        for choice in self.plusirredundant(actions):
            add = 1
            mirsetit = self.domirset.copy()
            for mir in mirsetit:
                if mir < choice:
                    self.domirset.remove(mir)
                else:
                    if choice <= mir:
                        add = 0
                        break
            if add == 1:
                self.domirset.add(frozenset(choice))
        t1 = time.time()
        n = len(self.actions)
        v = [0 for i in range(n+1)]
        for choice in self.domirset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        print('number of solutions: ', len(self.domirset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.domirset')

    def showMaxAbsIrred(self,withListing=True):
        """
        Computing maximal -irredundant choices:
            Result in self.absirset.

        """
        import time
        print('*--- Computing maximal -irredundant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        self.absirset = set()
        for choice in self.absirredundant(actions):
            add = 1
            mirsetit = self.absirset.copy()
            for mir in mirsetit:
                if mir < choice:
                    self.absirset.remove(mir)
                else:
                    if choice <= mir:
                        add = 0
                        break
            if add == 1:
                self.absirset.add(frozenset(choice))
        t1 = time.time()
        n = len(self.actions)
        v = [0 for i in range(n+1)]
        for choice in self.absirset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        print('number of solutions: ', len(self.absirset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.absirset')


    def showPreKernels(self,withListing=True):
        """
        Printing dominant and absorbent preKernels:
            Result in self.dompreKernels and self.abspreKernels

        """
        import time
        print('*--- Computing preKernels ---*')
        actions = set(self.actions)
        n = len(actions)
        dompreKernels = set()
        abspreKernels = set()
        t0 = time.time()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                abspreKernels.add(choice[0][0])
        t1 = time.time()
        if withListing:
            print('Dominant preKernels :')
            for choice in dompreKernels:
                print(list(choice))
                print('   independence : ', self.intstab(choice))
                print('   dominance    : ', self.domin(choice))
                print('   absorbency   : ', self.absorb(choice))
                print('   covering     :  %.3f' % self.averageCoveringIndex(choice, direction='out'))
            print('Absorbent preKernels :')
            for choice in abspreKernels:
                print(list(choice))
                print('   independence : ', self.intstab(choice))
                print('   dominance    : ', self.domin(choice))
                print('   absorbency   : ', self.absorb(choice))
                print('   covered      :  %.3f' % self.averageCoveringIndex(choice, direction='in'))
        print('*----- statistics -----')
        print('graph name: ', self.name)
        print('number of solutions')
        print(' dominant kernels : ', len(dompreKernels))
        print(' absorbent kernels: ', len(abspreKernels))
        print('cardinality frequency distributions')
        print('cardinality     : ', list(range(n+1)))
        v = [0 for i in range(n+1)]
        for ch in dompreKernels:
            v[len(ch)] += 1
        print('dominant kernel : ',v)
        v = [0 for i in range(n+1)]
        for ch in abspreKernels:
            v[len(ch)] += 1
        print('absorbent kernel: ',v)
        print('Execution time  : %.5f sec.' % (t1-t0))

    def computePreKernels(self):
        """
        computing dominant and absorbent preKernels:
            Result in self.dompreKernels and self.abspreKernels
        """
        actions = set(self.actions)
        n = len(actions)
        dompreKernels = set()
        abspreKernels = set()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                abspreKernels.add(choice[0][0])
        self.dompreKernels = dompreKernels
        self.abspreKernels = abspreKernels


    def generateDomPreKernels(self):
        """
        Generate all dominant prekernels from independent choices generator.
        """
        actions = set(self.actions)
        for item in self.independentChoices(self.singletons()):
            choice = item[0][0]
            gammaDomChoice = item[0][1]
            restactions = actions - choice
            if restactions <= gammaDomChoice:
                yield choice

    def generateAbsPreKernels(self):
        """
        Generate all absorbent prekernels from independent choices generator.
        """
        actions = set(self.actions)
        for item in self.independentChoices(self.singletons()):
            choice = item[0][0]
            gammaAbsChoice = item[0][2]
            restactions = actions - choice
            if restactions <= gammaAbsChoice:
                yield choice

    def components(self):
        """Renders the list of connected components."""
        A = {}
        for x in self.actions:
            A[x] = 0
        ncomp = 1
        ConComp = []
        for x in A:
            Comp = set()
            if A[x] == 0:
                A[x] = ncomp
                Comp = Comp | set([x])
                Comp = Comp | self._collectcomps(x, A, ncomp)
            if len(Comp) > 0:
                ncomp = ncomp + 1
                ConComp = ConComp + [Comp]
        return ConComp

    def showComponents(self):
        """Shows the list of connected components of the digraph instance."""
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1

    def _collectcomps(self, x, A, ncomp):
        """ Internal recursive subroutine of the components method."""
        Comp = set()
        Nx = self.gamma[x][0] | self.gamma[x][1]
        for y in Nx:
            if A[y] == 0:
                A[y] = ncomp
                Comp.add(y)
                Comp = Comp | self._collectcomps(y, A, ncomp)
        return Comp

    def outDegrees(self):
        """
        renders the median cut outdegrees
        """
        outDegrees ={}
        for x in self.actions:
            outDegrees[x] = len(self.gamma[x][0])
        return outDegrees

    def inDegrees(self):
        """
        renders the median cut indegrees
        """
        inDegrees ={}
        for x in self.actions:
            inDegrees[x] = len(self.gamma[x][1])
        return inDegrees

    def _bestRanks(self):
        """
        renders best possible ranks from indegrees account
        """
        bestRanks = {}
        inDegrees = self.inDegrees()
        for x in self.actions:
            bestRanks[x] = inDegrees[x] + 1
        return bestRanks

    def _worstRanks(self):
        """
        renders worst possible ranks from outdegrees account
        """
        worstRanks = {}
        outDegrees = self.outDegrees()
        for x in self.actions:
            worstRanks[x] = self.order - outDegrees[x]
        return worstRanks


    def gammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the dominated, and set *ax* gathering
        the absorbed neighborhood.

        """
        Med = self.valuationdomain['med']
        actions = self.actions
        relation = self.relation
        gamma = {}
        for x in actions:
            dx = set()
            ax = set()
            rx = relation[x]
            for y in actions:
                if x != y:
                    if rx[y] > Med:
                        dx.add(y)
                    if relation[y][x] > Med:
                        ax.add(y)
            gamma[x] = (dx,ax)
        return gamma

    def notGammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the not dominated, and set *ax* gathering
        the not absorbed neighborhood.

        """
        Med = self.valuationdomain['med']
        actions = self.actions
        relation = self.relation
        notGamma = {}
        for x in actions:
            dx = set()
            ax = set()
            rx = relation[x]
            for y in actions:
                if x != y:
                    if rx[y] < Med:
                        dx.add(y)
                    if relation[y][x] < Med:
                        ax.add(y)
            notGamma[x] = (dx,ax)
        return notGamma


    def _gammaSets(self):
        """ Renders the dictionary of neighborhoods {node: (dx,ax)}"""
        gamma = {}
        for x in self.actions:
            dx = self.dneighbors(x)
            ax = self.aneighbors(x)
            gamma[x] = (dx,ax)
        return gamma

    def weakGammaSets(self):
        """ Renders the dictionary of neighborhoods {node: (dx,ax)}"""
        weakGamma = {}
        for x in self.actions:
            dx = self.weakDneighbors(x)
            ax = self.weakAneighbors(x)
            weakGamma[x] = (dx,ax)
        return weakGamma

    def _notGammaSets(self):
        """ Renders the dictionary of not neighborhoods {node: (dx,ax)} """
        notGamma = {}
        for x in self.actions:
            dx = self.notdneighbors(x)
            ax = self.notaneighbors(x)
            notGamma[x] = (dx,ax)
        return notGamma

    def weakDneighbors(self,node):
        """ Renders the set of dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[node][a] >= Med:
                nb.add(a)
        return nb

    def dneighbors(self,node):
        """ Renders the set of dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[node][a] > Med:
                nb.add(a)
        return nb

    def notdneighbors(self,node):
        """ Renders the set of not dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if a != node:
                if self.relation[node][a] < Med:
                    nb.add(a)
        return nb

    def aneighbors(self,node):
        """ Renders the set of absorbed in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[a][node] > Med:
                nb.add(a)
        return nb

    def weakAneighbors(self,node):
        """ Renders the set of absorbed in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[a][node] >= Med:
                nb.add(a)
        return nb

    def notaneighbors(self,node):
        """ Renders the set of absorbed not in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
##            if a != node:
##                if self.relation[a][node] < Med:
##                    nb.add(a)
            if a != node:
                if self.relation[a][node] < Med:
                    nb.add(a)
        return nb

    def singletons(self):
        """list of singletons and neighborhoods
           [(singx1, +nx1, -nx1, not(+nx1 or -nx1)),.... ]"""
        s = []
        for x in self.actions:
            indep = set(self.actions) - (self.gamma[x][0] | self.gamma[x][1])
            s = s + [(frozenset([x]),self.gamma[x][0],self.gamma[x][1],indep)]
        return s


    def MISgen(self,S,I):
        """
        generator of maximal independent choices (voir Byskov 2004):
            * S ::= remaining nodes;
            * I ::= current independent choice

        .. note::

                Inititalize: self.MISgen(self.actions.copy(),set())
             
        """
        if S == set():
            add = 1
            self.missetit = self.misset.copy()
            for mis in self.missetit:
                if mis < I:
                    self.misset.remove(mis)
                else:
                    if I <= mis:
                        add = 0
                        break
            if add == 1:
                self.misset = self.misset | frozenset([I])
                yield I
        else:
            v = S.pop()
            Sv = S - (self.gamma[v][0] | self.gamma[v][1])
            Iv = I | set([v])
            for choice in self.MISgen(Sv,Iv):
                yield choice
            for choice in self.MISgen(S,I):
                yield choice

    def independentChoices(self,U):
        """
        Generator for all independent choices with neighborhoods of a bipolar valued digraph:

        .. note::
        
               * Initiate with U = self.singletons().
               * Yields [(independent choice, domnb, absnb, indnb)].

        """
        if U == []:
            yield [(frozenset(),set(),set(),set(self.actions))]
        else:
            x = list(U.pop())
            for S in self.independentChoices(U):
                yield S
                if x[0] <=  S[0][3]:
                    Sxgamdom = S[0][1] | x[1]
                    Sxgamabs = S[0][2] | x[2]
                    Sxindep = S[0][3] &  x[3]
                    Sxchoice = S[0][0] | x[0]
                    Sx = [(Sxchoice,Sxgamdom,Sxgamabs,Sxindep)]
                    yield Sx

    def coveringIndex(self,choice,direction="out"):
        """
        Renders the covering index of a given choice in a set of objects,
        ie the minimum number of choice members that cover each
        non selected object.
        """
        from decimal import Decimal
        actions = set([x for x in self.actions])
        nonSelected = actions - choice
        n = len(choice)
        index = n
        for x in nonSelected:
            if direction == 'out':
                index = min( index, len(self.gamma[x][1] & choice) )
            else:
                index = min( index, len(self.gamma[x][0] & choice) )
        if n > 0:
            return Decimal(str(index))/Decimal(str(n))
        else:
            return Decimal("0.0")

    def averageCoveringIndex(self,choice,direction="out"):
        """
        Renders the average covering index of a given choice in a set of objects,
        ie the average number of choice members that cover each
        non selected object.
        """
        from decimal import Decimal
        choice = set(choice)
        actions = set([x for x in self.actions])
        nonSelected = actions - choice
        n = len(choice)
        m = len(nonSelected)
        index = 0
        for x in nonSelected:
            if direction == 'out':
                index += len(self.gamma[x][1] & choice)
            else:
                index += len(self.gamma[x][0] & choice)
        if n > 0 and m > 0:
            return ( Decimal(str(index))/Decimal(str(m)) ) / Decimal(str(n))
        elif n > 0:
            return Decimal("1.0")
        else:
            return Decimal("0.0")

    def zoomValuation(self,zoomFactor=1.0):
        """
        Zooms in or out, depending on the value of the zoomFactor provided,
        the bipolar valuation of a digraph.
        """

        zoomFactor = Decimal(str(zoomFactor))

        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']

        newMin = oldMin * zoomFactor
        newMax = oldMax * zoomFactor
        newMed = oldMed * zoomFactor

        actions = self.actions
        oldRelation = self.relation
        newRelation = {}
        for x in actions:
            newRelation[x] = {}
            for y in actions:
                newRelation[x][y] = oldRelation[x][y] * zoomFactor

        # install new values in self
        self.valuationdomain['max'] = newMax
        self.valuationdomain['min'] = newMin
        self.valuationdomain['med'] = newMed

        self.relation = newRelation


    def recodeValuation(self,newMin=-1.0,newMax=1.0,Debug=False):
        """
        Recodes the characteristic valuation domain according
        to the parameters given.

        .. note::

            Default values gives a normalized valuation domain

        """
        from decimal import Decimal
        
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']
        try:
            oldPrecision = self.valuationdomain['precision']
        except:
            oldPrecision = Decimal('0')

        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)

        newMin = Decimal(str(newMin))
        newMax = Decimal(str(newMax))
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))
        newPrecision = oldPrecision/oldMax

        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)
            print('old and new precison', oldPrecision, newPrecision) 

        actions = self.actions
        oldrelation = self.relation
        newrelation = {}
        for x in actions:
            newrelation[x] = {}
            nrx = newrelation[x]
            orx = oldrelation[x]
            for y in actions:
                if orx[y] == oldMax:
                    nrx[y] = newMax
                elif orx[y] == oldMin:
                    nrx[y] = newMin
                elif orx[y] == oldMed:
                    nrx[y] = newMed
                else:
                    nrx[y] = newMin + ((orx[y] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(x,y,orx[y],nrx[y])
        # install new values in self
        self.valuationdomain['max'] = newMax
        self.valuationdomain['min'] = newMin
        self.valuationdomain['med'] = newMed
        self.valuationdomain['precision'] = newPrecision
        self.valuationdomain['hasIntegerValuation'] = False
        self.relation = newrelation

    def dominantChoices(self,S):
        """
        Generates all minimal dominant choices of a bipolar valued digraph.

        .. note::

             Initiate with S = self.actions.copy().
             
        """
        Med = self.valuationdomain['med']
        add = 1
        domsetit = self.domset.copy()
        for dom in domsetit:
            if S < dom:
                self.domset.remove(dom)
            else:
                if S >= dom:
                    add = 0
                    break
        if add == 1:
            self.domset = self.domset | set([frozenset(S)])
            yield S
            for x in S:
                S1 = S - set([x])
                if self.domin(S1) > Med:
                    for choice in self.dominantChoices(S1):
                        yield choice

    def minimalChoices(self,S):
        """
        Generates all dominant or absorbent choices of a bipolar
        valued digraph.

        .. note:

           * Initiate with S = (actions, dict of dominant or absorbent closed neighborhoods)
           * See showMinDom and showMinAbs methods.

        """
        if S[0] not in self.minhistory:
            self.minhistory = self.minhistory | set([frozenset(S[0])])
            add = True
            minsetit = self.minset.copy()
            for minch in minsetit:
                if S[0] < minch:
                    self.minset.remove(minch)
                else:
                    if S[0] >= minch:
                        add = False
                        break
            if add:
                self.minset = self.minset | set([frozenset(S[0])])
                yield S
            for x in S[0]:
                Sxchoice = S[0] - set([x])
                Sx = (Sxchoice,{})
                covering = True
                for cover in S[1]:
                    coverx = S[1][cover] - set([x])
                    if coverx == set():
                        covering = False
                        break
                    Sx[1][cover] = coverx
                if covering:
                    for choice in self.minimalChoices(Sx):
                        yield choice

    def absorbentChoices(self,S):
        """
        Generates all minimal absorbent choices of a bipolar valued digraph.
        """
        Med = self.valuationdomain['med']
        add = 1
        abssetit = self.absset.copy()
        for absch in abssetit:
            if S < absch:
                self.absset.remove(absch)
            else:
                if S >= absch:
                    add = 0
                    break
        if add == 1:
            self.absset = self.absset | set([frozenset(S)])
            yield S
            for x in S:
                S1 = S - set([x])
                if self.absorb(S1) > Med:
                    for choice in self.absorbentChoices(S1):
                        yield choice

    def kChoices(self,A,k):
        """
        Renders all choices of length k from set A
        """
        import copy
        if k == 0:
            yield set()
        else:
            while len(A) > 0:
                x = A.pop()
                Ax = copy.copy(A)
                k1 = k - 1
                for ch in self.kChoices(Ax,k1):
                    yield ch | set([x])


    def powerset(self,U):
        """
        Generates all subsets of a set.
        """
        if U == set():
            yield set()
        else:
            U1 = set(U)
            x = U1.pop()
            for S in self.powerset(U1):
                yield S
                yield S | set([x])

    def plusirredundant(self,U):
        """
        Generates all +irredundant choices of a digraph.
        """
        Med = self.valuationdomain['med']
        if U == set():
            yield set()
        else:
            x = U.pop()
            for S in self.plusirredundant(U):
                yield S
                Sx = S | set([x])
                if self.domirred(Sx) > Med:
                    yield Sx

    def absirredundant(self,U):
        """
        Generates all -irredundant choices of a digraph.
        """
        Med = self.valuationdomain['med']
        if U == set():
            yield set()
        else:
            x = U.pop()
            for S in self.absirredundant(U):
                yield S
                S1 = S | set([x])
                if self.absirred(S1) > Med:
                    Sx = S | set([x])
                    yield Sx

    def intstab(self,choice):
        """
        Computes the independence degree of a choice.
        """
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        relation = self.relation
        deg = Min
        for a in choice:
            for b in choice:
                x = relation[a][b]
                if x > deg and a != b:
                    deg = x
        res = Max - deg + Min
        return res



    def domin(self,choice):
        """
        Renders the dominance degree of a choice.
        """
        deg = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        restactions = set(self.actions) - choice
        for a in restactions:
            dega = Min
            for b in choice:
                x = self.relation[b][a]
                if x > dega:
                    dega = x
            if dega < deg:
                deg = dega
        return deg

    def absorb(self,choice):
        """
        Renders the absorbency degree of a choice.
        """
        deg = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        restactions = set(self.actions) - choice
        for a in restactions:
            dega = Min
            for b in choice:
                x = self.relation[a][b]
                if x > dega:
                    dega = x
            if dega < deg:
                deg = dega
        return deg

    def domirred(self,choice):
        """
        Renders the crips +irredundance degree of a choice.
        """
        Med = self.valuationdomain['med']
        irred = 1
        if len(choice) > 1:
            for x in choice:
                if self.domirredx(choice,x) < Med:
                    irred = 0
                    break
        if irred == 1:
            return self.valuationdomain['max']
        else:
            return self.valuationdomain['min']

    def domirredval(self,choice,relation):
        """
        Renders the valued +irredundance degree of a choice.
        """
        #import array
        actions = self.actions
        n = len(actions)
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        Max = Decimal(str(self.valuationdomain['max']))
        for x in actions:
            relation[x][x] = Max
        result = Max
        for x in choice:
            nbclx = self.readabsvector(x,relation)
            nbclchoice = [Min for i in actions]
            restchoice = set(choice)
            restchoice.remove(x)
            for y in restchoice:
                nbcly = self.readabsvector(y,relation)
                nbclchoice = [max(nbclchoice[i],nbcly[i]) for i in range(n)]
            resultx = max([min(nbclx[i],self.contra(nbclchoice)[i]) for i in range(n)])
            result = min(result, resultx)
        return result

    def domirredx(self,choice,x):
        """
        Renders the crips +irredundance degree of node x in a choice.
        """
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        nx = self.gamma[x][0] | set([x])
        chx = choice - set([x])
        ny = set()
        for y in chx:
            ny = ny | self.gamma[y][0] | set([y])
        nxpriv = nx - ny
        if nxpriv == set():
            return Min
        else:
            return Max

    def absirredval(self,choice,relation):
        """
        Renders the valued -irredundance degree of a choice.
        """
        #import array
        actions = self.actions
        n = len(actions)
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        for x in actions:
            relation[x][x] = Max
        result = Max
        for x in choice:
            nbclx = self.readdomvector(x,relation)
            nbclchoice = [Decimal(str(Min)) for i in actions]
            restchoice = set(choice)
            restchoice.remove(x)
            for y in restchoice:
                nbcly = self.readdomvector(y,relation)
                nbclchoice = [max(nbclchoice[i],nbcly[i]) for i in range(n)]
            resultx = max([min(nbclx[i],self.contra(nbclchoice)[i]) for i in range(n)])
            result = min(result, resultx)
        return result

    def absirred(self,choice):
        """
        Renders the crips -irredundance degree of a choice.
        """
        Med = self.valuationdomain['med']
        irred = 1
        if len(choice) > 1:
            for x in choice:
                if self.absirredx(choice,x) < Med:
                    irred = 0
                    break
        if irred == 1:
            return self.valuationdomain['max']
        else:
            return self.valuationdomain['min']

    def absirredx(self,choice,x):
        """Computes the crips -irredundance degree of node x in a choice."""
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        nx = self.gamma[x][1] | set([x])
        chx = choice - set([x])
        ny = set()
        for y in chx:
            ny = ny | self.gamma[y][1] | set([y])
        nxpriv = nx - ny
        if nxpriv == set():
            return Min
        else:
            return Max

    def save(self,fileName='tempdigraph',option=None,DecimalValuation=True,decDigits=2):
        """Persistent storage of a Digraph class instance in the form of
            a python source code file"""
        print('*--- Saving digraph in file: <' + fileName + '.py> ---*')
        actions = self.actions
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved digraph instance\n')
        if DecimalValuation:
            fo.write('from decimal import Decimal\n')
        fo.write('actions = {\n')
        for x in actions:
            fo.write('\'' + str(x) + '\':\n')
            try:
                fo.write(str(actions[x])+',\n')
            except:
                fo.write('{\'name\': \'%s\'},\n' % str(x))
        fo.write('}\n')
        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = not DecimalValuation
        if not hasIntegerValuation:
            fo.write('valuationdomain = {\'hasIntegerValuation\': False, \'min\': Decimal("'+str(Min)+'"),\'med\': Decimal("'+str(Med)+'"),\'max\': Decimal("'+str(Max)+'")}\n')
        else:
            fo.write('valuationdomain = {\'hasIntegerValuation\': True, \'min\': '+str(Min)+',\'med\': '+str(Med)+',\'max\': '+str(Max)+'}\n')

        fo.write('relation = {\n')
        for x in actions:
            fo.write('\'' + str(x) + '\': {\n')
            for y in actions:
                if not hasIntegerValuation:
                    valueString = '\': %%.%df,\n' % (decDigits)
                    fo.write('\'' + str(y) + (valueString % relation[x][y]))
                    #fo.write('\'' + str(y) + '\': Decimal("' + str(relation[x][y]) + '"),\n')
                else:
                    fo.write('\'' + str(y) + '\':' + str(relation[x][y]) + ',\n')
            fo.write('},\n')
        fo.write( '}\n')
        if option == 'withAutomorphismGenerators':
            fo.write('reflections = {\n')
            for ga in self.reflections:
                fo.write('\' '+str(ga)+'\':'+str(self.reflections[ga])+',\n')
            fo.write('}\n')
            fo.write('permutations = {\n')
            for ga in self.permutations:
                fo.write("\'"+str(ga)+"\': {\n")
                for p in self.permutations[ga]:
                    fo.write('\''+str(p)+'\': \''+str(self.permutations[ga][p])+'\',\n')
                fo.write('},\n')
            fo.write('}\n')
        fo.close()

    def saveCSV(self,fileName='tempdigraph',Normalized=False,
                Dual=False,Converse=False,Diagonal=False,Debug=False):
        """Persistent storage of a Digraph class instance in the form of
            a csv file. """
        from copy import deepcopy
        import csv
        com = ''
        if Normalized:
            com += 'normalized'
            if Dual and Converse:
                com += ' and codual'
            elif Dual and not Converse:
                com += ' and dual'
            elif Converse:
                com += ' and converse'
        else:
            if Dual and Converse:
                com += 'codual'
            elif Dual and not Converse:
                com += 'dual'
            elif Converse:
                com += 'converse'
        
        if Debug:
            print('*--- Saving %s digraph in file: %s.csv> ---*' % (com,fileName))
        fileNameExt = str(fileName)+str('.csv')
        fo = open(fileNameExt, 'w')
        csvfo = csv.writer(fo,quoting=csv.QUOTE_NONNUMERIC)
        actionsList = [x for x in self.actions]
        actionsList.sort()
        headerText = ["d"] + actionsList
        if Debug:
            print(headerText)
        csvfo.writerow(headerText)
        dg = deepcopy(self)
        if Normalized:
            dg.recodeValuation(-1,1)
        Min = dg.valuationdomain['min']
        Med = dg.valuationdomain['med']
        if Dual:
            dg = -dg
        if Converse:
            dg = ~dg
        relation = dg.relation
        for x in actionsList:
            rowText = [x]
            for y in actionsList:
                if x == y:
                    if not Diagonal:
                        rowText.append(float(Min))
                    else:
                        rowText.append(float(relation[x][y]))
                else:
                    rowText.append(float(relation[x][y]))
            if Debug:
                print(rowText)
            csvfo.writerow(rowText)
        fo.close()

    def chordlessPaths(self,Pk,n2,Odd=False,Comments=False,Debug=False):
        """
        New procedure from Agrum study April 2009
        recursive chordless path extraction strating from path
        Pk = [n2, ...., n1] and ending in node n2.
        Optimized with marking of visited chordless P1s.
        """
        if Comments:
            Debug = True
        n1 = Pk[-1]
        self.visitedArcs.add((n1,n2))
        self.visitedArcs.add((n2,n1))
        med = self.valuationdomain['med']
        if self.relation[n1][n2] > med and self.relation[n2][n1] <= med:
            detectedChordlessPath = True
            #self.visitedArcs.add((n1,n2))
            #OddFlag = True
            if Debug:
                print('len(Pk)', Pk, len(Pk), len(Pk) % 2)

            if Odd:
                if (len(Pk) % 2) != 1:
                    OddFlag = False
                else:
                    OddFlag = True
            else:
                OddFlag = True

            if Debug:
                print('OddFlag: ', OddFlag)
            if OddFlag:
                #Pk.append(n2)
                self.xCC.append(Pk)
                if Debug:
                    print('Chordless circuit certificate -->>> ', Pk)
        else:
            detectedChordlessPath = False
            NBn1 = set(self.gamma[n1][0]-self.gamma[n1][1])
            while NBn1 != set():
                n = NBn1.pop()
                if (n1,n) not in self.visitedArcs and (n,n1) not in self.visitedArcs:
                    P = list(Pk)
                    noChord = True
                    for x in P[:-1]:
                        ## if x == n1:
                        ##     if self.relation[n][x] > med:
                        ##         noChord = False
                        ## elif x == n2:
                        if x == n2:
                            if self.relation[x][n] > med:
                                noChord = False
                                break
                        else:
                            if self.relation[x][n] > med or self.relation[n][x] > med:
                                noChord = False
                                break
                    if noChord:
                        P.append(n)
                        if Debug:
                            print('P,n2',P,n2)
                        if self.chordlessPaths(P,n2,Odd,Comments,Debug):
                            detectedChordlessPath = True
            #self.visitedArcs.add((n1,n2))
            if Debug:
                print('No further chordless path from ',n1,' to ', n2)
        return detectedChordlessPath

    def detectChordlessPath(self,Pk,n2,Comments=False,Debug=False):
        """
        New procedure from Agrum study April 2009
        recursive chordless path extraction starting from path
        Pk = [n2, ...., n1] and ending in node n2.
        Optimized with marking of visited chordless P1s.
        """
        if Comments:
            Debug = True
        n1 = Pk[-1]
        self.visitedArcs.add((n1,n2))
        self.visitedArcs.add((n2,n1))
        med = self.valuationdomain['med']

        if self.relation[n1][n2] > med and self.relation[n2][n1] <= med:
            Detected = True
            if Debug:
                print('Chordless circuit certificate -->>> ', Pk)
        else:
            Detected = False
            NBn1 = set(self.gamma[n1][0]-self.gamma[n1][1])
            while NBn1 != set():
                n = NBn1.pop()
                if (n1,n) not in self.visitedArcs and (n,n1) not in self.visitedArcs:
                    P = list(Pk)
                    noChord = True
                    for x in P[:-1]:
                        if x == n2:
                            if self.relation[x][n] > med:
                                noChord = False
                                break
                        else:
                            if self.relation[x][n] > med or self.relation[n][x] > med:
                                noChord = False
                                break
                    if noChord:
                        P.append(n)
                        if Debug:
                            print('P,n2',P,n2)
                        Detected = self.detectChordlessPath(P,n2,Comments,Debug)
                if Detected:
                        break
        return Detected

    def detectCppChordlessCircuits(self,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits detection
        exchange arguments with external temporary files.
        Returns a boolean value
        """
        import os
        from tempfile import mkstemp
        fd, tempFileName = mkstemp()
        fo = os.fdopen(fd,'w')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        fo.write('%d %d\n' % (i+1,j+1))
        fo.close()

        resultFile = tempFileName+'.py'
        if os.path.exists('/usr/bin/detectChordlessCircuits'):
            os.system('/usr/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/usr/local/bin/detectChordlessCircuits'):
            os.system('/usr/local/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/opt/local/bin/detectChordlessCircuits'):
            os.system('/opt/local/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/home/users/rbisdorff/bin/detectChordlessCircuits'):
            os.system('/home/users/rbisdorff/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        else:
            print('Error: detectChordlessCircuits binary could not be found !!!')
        argDict = {}
        exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'),argDict)
        circuits = argDict['circuitsList']
        if circuits == []:
            Detected = False
        else:
            Detected = True
        if Debug:
            print(resultFile)
            print(argDict['circuitsList'])
            if Detected:
                print('A chordless circuit has been detected !')
            else:
                print('No chordless circuit has been detected !')
            print('certificate: ', circuits)

        return Detected

    def computeCppInOutPipingChordlessCircuits(self,Odd=False,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits enumeration
        exchange arguments with external temporary files
        """
        import os
        from subprocess import Popen,PIPE

        if os.path.exists('/usr/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/usr/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        elif os.path.exists('/usr/local/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/usr/local/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        elif os.path.exists('/opt/local/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/opt/local/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        elif  os.path.exists('/home/users/rbisdorff/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/home/users/rbisdorff/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        else:
            print('Error: executable enumChordlessCircuitsInOutPiping not found !!!')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        inputString = ''
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        inputString += '%d %d \n' % (i+1,j+1)
        circuits = eval(p.communicate(input=inputString.encode('utf-8'))[0])
        if Debug:
            print(circuits)
        result = []
        history = set()
        for x in circuits:
            # !! a circuit has a length n + 1 !!
            if Odd:
                r = len(x) % 2
                ## if Debug:
                ##     print x, r
                if r != 1:
                    oddCircuit = []
                    for ino in x[:-1]:
                        oddCircuit.append(actions[ino-1])
                    circuitActions = [y for y in flatten(oddCircuit)]
                    circuitSet = frozenset(circuitActions)
                    if circuitSet not in history:
                        result.append( ( circuitActions, circuitSet ) )
                        history.add(circuitSet)
                    #result.append( ( oddCircuit, frozenset(oddCircuit) ) )
            else:
                allCircuit = []
                for ino in x[:-1]:
                    allCircuit.append(actions[ino-1])
                circuitActions = [y for y in flatten(allCircuit)]
                circuitSet = frozenset(circuitActions)
                if circuitSet not in history:
                    result.append( ( circuitActions, circuitSet ) )
                    history.add(circuitSet)
                #result.append( ( allCircuit, frozenset(allCircuit) ) )
        self.circuitsList = result
        return result

    def computeCppChordlessCircuits(self,Odd=False,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits enumeration
        exchange arguments with external temporary files
        """
        import os
        from tempfile import mkstemp
        from digraphsTools import flatten
        
        fd, tempFileName = mkstemp()
        fo = os.fdopen(fd,'w+b')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        inputString = ''
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        inputString += '%d %d \n' % (i+1,j+1)
        fo.write(inputString.encode('utf-8'))
        fo.close()
        ## if Debug:
        ##     print 'see file: ', tempFileName
        resultFile = tempFileName+'.py'
        if os.path.exists('/usr/bin/enumChordlessCircuits'):
            os.system('/usr/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/usr/local/bin/enumChordlessCircuits'):
            os.system('/usr/local/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/opt/local/bin/enumChordlessCircuits'):
            os.system('/opt/local/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/home/users/rbisdorff/bin/enumChordlessCircuits'):
            os.system('/home/users/rbisdorff/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        else:
            print('Error: enumChordlessCircuits binary not found !!!')
        argDict = {}
        exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'),argDict)
        circuits = argDict['circuitsList']
        if Debug:
            print(resultFile)
            print(argDict['circuitsList'])
        result = []
        history = set()
        for x in circuits:
            # !! a circuit has a length n + 1 !!
            if Odd:
                r = len(x) % 2
                ## if Debug:
                ##     print x, r
                if r != 1:
                    oddCircuit = []
                    for ino in x[:-1]:
                        oddCircuit.append(actions[ino-1])
                    circuitActions = [y for y in flatten(oddCircuit)]
                    circuitSet = frozenset(circuitActions)
                    if circuitSet not in history:
                        result.append( ( circuitActions, circuitSet ) )
                        history.add(circuitSet)
            else:
                allCircuit = []
                for ino in x[:-1]:
                    allCircuit.append(actions[ino-1])
                circuitActions = [y for y in flatten(allCircuit)]
                circuitSet = frozenset(circuitActions)
                if circuitSet not in history:
                    result.append( ( circuitActions, circuitSet ) )
                    history.add(circuitSet)
        self.circuitsList = result
        return result

    #@timefn
    def computeChordlessCircuits(self,Odd=False,Comments=False,Debug=False):
        """
        Renders the set of all chordless circuits detected in a digraph.
        Result is stored in <self.circuitsList>
        holding a possibly empty list of tuples with at position 0 the
        list of adjacent actions of the circuit and at position 1
        the set of actions in the stored circuit.

        When *Odd* is True, only chordless circuits with an odd length
        are collected.

        """
        #import copy
        from digraphsTools import flatten
        if Comments:
            if Odd:
                print('*--- chordless odd circuits ---*')
            else:
                print('*--- chordless circuits ---*')

        actionsList = list(self.actions)
        self.visitedArcs = set()
        chordlessCircuits = []       
        for x in actionsList:
            P = [x]
            if Comments:
                print('Starting from ', x)
            self.xCC = []
            if self.chordlessPaths(P,x,Odd,Comments,Debug):
                chordlessCircuits += self.xCC
        self.chordlessCircuits = chordlessCircuits
        if Comments:
            print('result:', len(self.chordlessCircuits), 'circuit(s)')
            print(self.chordlessCircuits)

        circuitsList = []
        history = set()
        for x in self.chordlessCircuits:
            #circuitsList.append( (x,frozenset(x)) )
            circuitActions = [y for y in flatten(x)]
            circuitSet = frozenset(circuitActions)
            if Comments:
                print('flattening', x, circuitActions)
            if circuitSet not in history:
                history.add(circuitSet)
                circuitsList.append( (circuitActions,circuitSet) )
        self.circuitsList = circuitsList
        return circuitsList

    def detectChordlessCircuits(self,Comments=False,Debug=False):
        """
        Detects a chordless circuit in a digraph.
        Returns a Boolean
        """
        if Comments:
            print('* ---- detecting a chordless circuit, the case given. ----*')

        actionsList = list(self.actions)
        self.visitedArcs = set()
        Detected = False

        for x in actionsList:
            P = [x]
            if Comments:
                print('Starting from ', x)
            self.xCC = []
            if self.detectChordlessPath(P,x,Comments,Debug):
                Detected = True
                break
        if Comments:
            if Detected:
                print('A chordless circuit has been detected !')
            else:
                print('No chordless circuit has been detected !')

        return Detected

    def showCircuits(self):
        """
        show methods for circuits observed in a Digraph instance.
        """
        try:
            if len(self.circuitsList) == 0:
                print('No circuits observed in this digraph.')
            else:
                print('*---- Chordless circuits ----*')
                print('%d circuits.' % (len(self.circuitsList)))
                for i,(circList,circSet) in enumerate(self.circuitsList):
                    deg = self.circuitMinCredibility(circList)
                    print('%d: ' % (i+1), circList, ', credibility : %.3f' % (deg))
        except:
            print('No circuits yet computed. Run computeChordlessCircuits()!')


    def showChordlessCircuits(self):
        """
        show methods for (chordless) circuits in a Digraph.
        Dummy for showCircuits().
        """
        Digraph.showCircuits(self)
##        print('*---- Chordless circuits ----*')
##        try:
##            for (circList,circSet) in self.circuitsList:
##                deg = self.circuitMinCredibility(circList)
##                print(circList, ', credibility :', deg)
##            print('%d circuits.' % (len(self.circuitsList)))
##        except:
##            print('No circuits computed. Run computeChordlessCircuits()!')

    def minimalValuationLevelForCircuitsElimination(self,Odd=True,Debug=False,Comments=False):
        """
        renders the minimal valuation level <lambda> that eliminates all
        self.circuitsList stored odd chordless circuits from self.

        .. warning::

            The <lambda> level polarised may still contain newly appearing chordless odd circuits !

        """
        # try:
        #     circuitslist = self.circuitslist
        # except:
        self.computeChordlessCircuits(Odd=Odd,Comments=Debug)
        circuitsList = self.circuitsList
        Med = self.valuationdomain['med']
        qualmaj = Med
        oddCircuitsList = [cc for cc in circuitsList if (len(cc[0])%2 == 1)]
        if Comments:
            print('Number of chordless circuits: ', len(circuitsList))
            print(circuitsList)
            print('Number of chordless odd circuits: ', len(oddCircuitsList))
            print(oddCircuitsList)
        for cc in circuitsList:
            circuit = cc[0]
            if Debug:
                print(circuit)
            ccqualmaj = self.circuitMinCredibility(circuit)
            ## n = len(circuit)
            ## for i in range(n-1):
            ##     x = cc[0][i]
            ##     y = cc[0][i+1]
            ##     if Debug:
            ##         print x, y, self.relation[x][y],y,x,self.relation[y][x]
            ##     if self.relation[x][y] > Med:
            ##         if self.relation[x][y] < ccqualmaj:
            ##             ccqualmaj = self.relation[x][y]
            ## else:
            ##     if self.relation[y][x] < Med:
            ##         if abs(self.relation[y][x]) < ccqualmaj:
            ##             ccqualmaj = abs(self.relation[y][x])
            if Debug:
                print('==>>', circuit, ccqualmaj)
            qualmaj = max(qualmaj,ccqualmaj)
        if Debug or Comments:
            # if Odd:
            #     print('Number of chordless odd circuits: ', len(oddCircuitsList))
            # else:
            #     print('Number of chordless circuits: ', len(circuitsList))
            print('Minimal cutting level for eliminating them: %.3f' % qualmaj)
        return qualmaj

    ## def minimalValuationLevelForCircuitsEliminationOld(self,Debug=False):
    ##     """
    ##     renders the minimal valuation level <lambda> that eliminates all
    ##     self.circuitsList stored odd chordless circuits from self.

    ##     .. warning::

    ##         The <lambda> level polarised may still contain newly appearing chordless odd circuits !

    ##     """
    ##     try:
    ##         circuitslist = self.circuitslist
    ##     except:
    ##         self.computeChordlessCircuits(Odd=True,Comments=Debug)
    ##         circuitsList = self.circuitsList
    ##     Max = self.valuationdomain['max']
    ##     Med = self.valuationdomain['med']
    ##     qualmaj = Med
    ##     for cc in circuitsList:
    ##         ccqualmaj = Max
    ##         if Debug:
    ##             print cc
    ##         circuit = cc[0]
    ##         circuit.append(cc[0][0])
    ##         if Debug:
    ##             print circuit
    ##         n = len(circuit)
    ##         for i in range(n-1):
    ##             x = cc[0][i]
    ##             y = cc[0][i+1]
    ##             if Debug:
    ##                 print x, y, self.relation[x][y],y,x,self.relation[y][x]
    ##             if self.relation[x][y] > Med:
    ##                 if self.relation[x][y] < ccqualmaj:
    ##                     ccqualmaj = self.relation[x][y]
    ##         else:
    ##             if self.relation[y][x] < Med:
    ##                 if abs(self.relation[y][x]) < ccqualmaj:
    ##                     ccqualmaj = abs(self.relation[y][x])
    ##         if Debug:
    ##             print '==>>', circuit, ccqualmaj
    ##         if ccqualmaj > qualmaj:
    ##             qualmaj = ccqualmaj
    ##     if Debug:
    ##         print qualmaj
    ##     return qualmaj

    def circuitMinCredibility(self,circ):
        """
        Renders the minimal linking credibility of a Chordless Circuit.
        """
        actions = self.actions
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = self.relation
        deg = Max
        circuit = list(circ)
        n = len(circuit)
        for i in range(n):
            x = circuit[i]
            for j in range(i+1,n):
                y =  circuit[j]
                if j == i+1:
                    deg = min(deg,max(relation[x][y],relation[y][x]))
        x = circuit[-1]
        y = circuit[0]
        deg = min(deg,max(relation[x][y],relation[y][x]))
        return deg

    def circuitMaxCredibility(self,circ):
        """
        Renders the maximal linking credibility of a Chordless Circuit.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        relation = self.relation
        deg = Min
        circuit = list(circ)
        n = len(circuit)
        for i in range(n):
            x = circuit[i]
            for j in range(i+1,n):
                y =  circuit[j]
                if j == i+1:
                    deg = max(deg,max(relation[x][y],relation[y][x]))
        x = circuit[-1]
        y = circuit[0]
        deg = max(deg,max(relation[x][y],relation[y][x]))
        return deg

    ## def circuitMinCredibilityOld(self,circuit):
    ##     """
    ##     Renders the minimal linking credibility of a COC.
    ##     """
    ##     actions = self.actions
    ##     Max = self.valuationdomain['max']
    ##     Med = self.valuationdomain['med']
    ##     relation = self.relation
    ##     deg = Max
    ##     for x in circuit:
    ##         for y in circuit:
    ##             if relation[x][y] > Med:
    ##                 deg = min(deg,relation[x][y])
    ##     return deg

    def circuitAverageCredibility(self,circ):
        """
        Renders the average linking credibility of a Chordless Circuit.
        """
        actions = self.actions
        n = len(actions)
        narcs = n * (n-1)
        relation = self.relation
        Min = self.valuationdomain['min']
        deg = Min
        circuit = list(circ)
        for x in circuit:
            for y in circuit:
                if x != y:
                    deg += abs(relation[x][y])
        deg = deg / Decimal(str(narcs))
        return deg

    def circuitCredibilities(self,circuit,Debug=False):
        """
        Renders the average linking credibilities and the minimal link of a Chordless Circuit.

        """
        if Debug:
            print(circuit)
        actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        if Min != -Max:
            # the characteristic valuation is not bipolar !
            maxAmplitude = abs(Max-Med) + abs(Min-Med)
            degP = Decimal('0')
            degN = Decimal('0')
            nParcs = 0
            nNarcs = 0
            minAmplitude = maxAmplitude
            minLink = None
            nc = len(circuit)
            for i in range(nc):
                x = circuit[i]
                #for j in range(i+1,nc):
                if i != nc -1:
                    y = circuit[i+1]
                else:
                    y = circuit[0]
                if Debug:
                    print(x,y,end=',')
                degP += (relation[x][y]-Med)
                nParcs += 1
                diffxy = abs(relation[x][y]-Med) + abs(relation[y][x]-Med)
                if Debug:
                    print(relation[x][y],relation[y][x],diffxy,end=',')
                if minAmplitude >= diffxy:
                    minAmplitude = diffxy
                    minLink = (x,y)
                if Debug:
                    print(minAmplitude,diffxy,minLink)
                degN += (relation[y][x]-Med)
                nNarcs += 1
        else:
            # the characteristic valuation is bipolar !
            maxAmplitude = abs(Max) + abs(Min)
            degP = Med
            degN = Med
            nParcs = 0
            nNarcs = 0
            minAmplitude = maxAmplitude
            minLink = None
            nc = len(circuit)
            for i in range(nc):
                x = circuit[i]
                #for j in range(i+1,nc):
                if i != nc -1:
                    y = circuit[i+1]
                else:
                    y = circuit[0]
                if Debug:
                    print(x,y,end=',')
                degP += relation[x][y]
                nParcs += 1
                diffxy = abs(relation[x][y]) + abs(relation[y][x])
                if Debug:
                    print(relation[x][y],relation[y][x],diffxy,end=',')
                if minAmplitude >= diffxy:
                    minAmplitude = diffxy
                    minLink = (x,y)
                if Debug:
                    print(minLink)
                degN += relation[y][x]
                nNarcs += 1            
        if nParcs != 0:
            degP /= Decimal(str(nParcs))
        if nNarcs != 0:
            degN /= Decimal(str(nNarcs))
        if Debug:
            print('degP,degN,minLink',degP,degN,minLink)
        return degP,degN,minLink

    def contra(self, v):
        """
        Parameter: choice.
        Renders the negation of a choice v characteristic's vector.
        """
        Max = Decimal(str(self.valuationdomain['max']))
        Min = Decimal(str(self.valuationdomain['min']))
        #print v
        nv = [Max - v[x] + Min for x in range(len(v))]
        return nv

    def sharpvec(self, v, w):
        """
        Paramaters: choice characteristic vectors.
        Renders the sharpest of two characteristic vectors v and w.
        """
        sv = [self.sharp(v[x],w[x]) for x in range(len(v))]
        return sv

    def sharp(self, x, y):
        """
        Paramaters: choice characteristic values.
        Renders the sharpest of two characteristic values x and y.
        """
        med = Decimal(str(self.valuationdomain['med']))
        if x >= med and y >= med:
            return max(x,y)
        elif x <= med and y <= med:
            return min(x,y)
        else:
            return med

    def inner_prod(self, v1, v2):
        """
        Parameters: two choice characteristic vectors
        Renders the inner product of two characteristic vetors.
        """
        res = Decimal(str(self.valuationdomain['min']))
        for i in range(len(v1)):
            res = max(res, min(v1[i],v2[i]))
        return res

    def matmult2(self, m, v):
        """
        Parameters: digraph relation and choice characteristic vector
        matrix multiply vector by inner production
        """
        return [self.inner_prod(r, v) for r in m]

    def readdomvector(self, x,relation):
        """
        Parameter: action x
        dominant out vector.
        """
        #import array
        actions = self.actions
        vec = [relation[y][x] for y in actions]
        return vec

    def readabsvector(self, x,relation):
        """
        Parameter: action x
        absorbent in vector.
        """
        #import array
        actions = self.actions
        vec = [relation[x][y] for y in actions]
        return vec

    # -----  graph restrictions methods

    def domkernelrestrict(self, prekernel):
        """
        Parameter: dominant prekernel
        Renders dominant prekernel restricted relation.
        """
        actions = self.actions
        relation = self.relation
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        relation_k = {}
        for x in actions:
            relation_k[x] = {}
            for y in actions:
                #relation_k[x][y] = {}
                if x == y:
                    relation_k[x][y] = Min
                elif x in prekernel and y in prekernel:
                    relation_k[x][y] = relation[x][y]
                elif x in prekernel and relation[x][y] > Med:
                    relation_k[x][y] = relation[x][y]
                elif y in prekernel and relation[x][y] < Med:
                    relation_k[x][y] = relation[x][y]
                else:
                    relation_k[x][y] = Med
        return relation_k

    def abskernelrestrict(self, prekernel):
        """
        Parameter: prekernel
        Renders absorbent prekernel restricted relation.
        """
        actions = self.actions
        relation = self.relation
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        relation_k = {}
        for x in actions:
            relation_k[x] = {}
            for y in actions:
                #relation_k[x][y] = {}
                if x == y:
                    relation_k[x][y] = Min
                elif x in prekernel and y in prekernel:
                    relation_k[x][y] = relation[x][y]
                elif x in prekernel and relation[x][y] < Med:
                    relation_k[x][y] = relation[x][y]
                elif y in prekernel and relation[x][y] > Med:
                    relation_k[x][y] = relation[x][y]
                else:
                    relation_k[x][y] = Med
        return relation_k


    def showRubyChoice(self,Comments=False,_OldCoca=True):
        """
        Dummy for showRubisBestChoiceRecommendation()
        needed for older versions compatibility.
        """
        self.showBestChoiceRecommendation(Comments=Comments,_OldCoca=_OldCoca)

    def showBestChoiceRecommendation(self,Comments=False,
                                          ChoiceVector=False,
                                          CoDual=True,
                                          Debug=False,
                                          _OldCoca=False,
                                          BrokenCocs=True,
                                          Cpp=False):
        """
        Renders the RuBis best choice recommendation.

        .. note::

            Computes by default the Rubis best choice recommendation on the corresponding strict (codual) outranking digraph.

            In case of chordless circuits, if supporting arcs are more credible
            than the reversed negating arcs, we collapse the circuits into hyper nodes.
            Inversely,  if supporting arcs are not more credible than the reversed negating arcs,
            we brake the circuits on their weakest arc.
         
        Usage example:
        
        >>> from outrankingDigraphs import *
        >>> t = Random3ObjectivesPerformanceTableau(seed=5)
        >>> g = BipolarOutrankingDigraph(t)
        >>> g.showBestChoiceRecommendation()
        ***********************
        RuBis Best Choice Recommendation (BCR)
        (in decreasing order of determinateness)   
        Credibility domain:  [-100.0, 100.0]
        === >> potential vest choices
        * choice              : ['a04', 'a14', 'a19', 'a20']
           independence        : 1.19
           dominance           : 4.76
           absorbency          : -59.52
           covering (%)        : 75.00
           determinateness (%) : 57.86
           - most credible action(s) = { 'a14': 23.81, 'a19': 11.90, 'a04': 2.38, 'a20': 1.19, }  
        === >> potential worst choices 
        * choice              : ['a03', 'a12', 'a17']
          independence        : 4.76
          dominance           : -76.19
          absorbency          : 4.76
          covering (%)        : 0.00
          determinateness (%) : 65.39
          - most credible action(s) = { 'a03': 38.10, 'a12': 13.10, 'a17': 4.76, }
        Execution time: 0.024 seconds
        *****************************

        """
        from copy import deepcopy
        from time import time
        if Debug:
            Comments = True
        print('***********************')
        #print('RuBis BCR')
        if Debug:
            print('All comments !!!')
            Comments=True
        t0 = time()
        n0 = self.order
        cpself = deepcopy(self)
        if CoDual:
            g = ~(-cpself)
        else:
            g = cpself
        if _OldCoca:
            _selfwcoc = CocaDigraph(g,Cpp=Cpp)
            b1 = 0
        elif BrokenCocs:
            #print('passed here!')
            _selfwcoc = BrokenCocsDigraph(g,Cpp=Cpp)
            b1 = _selfwcoc.breakings
        else:
            _selfwcoc = BreakAddCocsDigraph(g,Cpp=Cpp)
            b1 =  _selfwcoc.breakings
        n1 = _selfwcoc.order
        nc = n1 - n0
        
        #self.relation_orig = deepcopy(g.relation)
        if b1 > 0 or nc > 0:
            #self.actions_orig = deepcopy(g.actions)
            g.actions = deepcopy(_selfwcoc.actions)
            g.order = len(g.actions)
            g.relation = deepcopy(_selfwcoc.relation)
        if Debug:
            print('List of pseudo-independent choices')
            print(g.actions)
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        if Debug:
            g.showRelationTable()
        #self.showPreKernels()
        actions = set([x for x in g.actions])
        if Comments:
            g.showPreKernels()
        if Debug:
            print(g.dompreKernels,g.abspreKernels)
        g.computeGoodChoices(Comments=Debug)
        g.computeBadChoices(Comments=Debug)
        if Debug:
            print('good and bad choices: ',g.goodChoices,g.badChoices)
        t1 = time()
        print('Rubis best choice recommendation(s) (BCR)')
        print(' (in decreasing order of determinateness)   ')
        print('Credibility domain: [%.2f,%.2f]' % (g.valuationdomain['min'],\
                                                                        g.valuationdomain['max']) )
        Med = g.valuationdomain['med']
        bestChoice = set()
        worstChoice = set()
        for gch in g.goodChoices:
            if gch[0] >= Med:
                goodChoice = True
                for bch in g.badChoices:
                    if gch[5] == bch[5]:
                        #if gch[0] == bch[0]:
                        if gch[3] == gch[4]:
                            if Comments:
                                print('ambiguous (good) choice ')
                                g.showChoiceVector(gch,choiceType='good',
                                                      ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        elif gch[4] > gch[3]:
                            if Comments:
                                print('outranked (good) choice ')
                                g.showChoiceVector(gch,choiceType='good',
                                                      ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        else:
                            goodChoice = True
                if goodChoice:
                    print(' === >> potential best choice(s)')
                    g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                    if bestChoice == set():
                        bestChoice = gch[5]
            else:
                print(' === >> non robust best choice(s)')
                g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
        for bch in g.badChoices:
            if bch[0] >= Med:
                badChoice = True
                nullChoice = False
                for gch in g.goodChoices:
                    if bch[5] == gch[5]:
                        #if gch[0] == bch[0]:
                        if bch[3] == bch[4]:
                            if Comments:
                                print('ambiguous (bad) choice ')
                                g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                            badChoice = False
                            nullChoice = True
                        elif bch[3] > bch[4]:
                            if Comments:
                                print('outranking (bad) choice ')
                                g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                            badChoice = False
                        else:
                            badChoice = True
                if badChoice:
                    print(' === >> potential worst choice(s) ')
                    g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]
                elif nullChoice:
                    print(' === >> ambiguous choice(s)')
                    g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]

            else:
                print('=== >> non robust worst choice(s)')
                g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
        print()
        print('Execution time: %.3f seconds' % (t1-t0))
        print('*****************************')
        self.bestChoice = bestChoice
        self.worstChoice = worstChoice
        #if nc > 0 or b1 > 0:
##        self.actions = deepcopy(self.actions_orig)
##        self.relation = deepcopy(self.relation_orig)
##        self.order = len(self.actions)
##        self.gamma = self.gammaSets()
##        self.notGamma = self.notGammaSets()


    def showRubisBestChoiceRecommendation(self,**kwargs):
        """
        Dummy for backward portable showBestChoiceRecommendation().
        """
        self.showBestChoiceRecommendation(**kwargs)
        
#############

    def showHTMLBestChoiceRecommendation(self,pageTitle=None,
                                          ChoiceVector=False,
                                          CoDual=True,
                                          Debug=False,
                                          _OldCoca=False,
                                          BrokenCocs=True,
                                          Cpp=False):

        import webbrowser
        fileName = '/tmp/relationMap.html'
        fo = open(fileName,'w')
        fo.write(self.htmlBestChoiceRecommendation(\
            pageTitle=pageTitle,\
            ChoiceVector=ChoiceVector,\
            CoDual=CoDual,\
            Debug=Debug,\
            _OldCoca=_OldCoca,\
            BrokenCocs=BrokenCocs,\
            Cpp=Cpp))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)


    def htmlBestChoiceRecommendation(self,pageTitle=None,
                                          ChoiceVector=False,
                                     ContentCentered=True,
                                          CoDual=True,
                                          Debug=False,
                                          _OldCoca=False,
                                          BrokenCocs=True,
                                          Cpp=False):
        """
        Renders the RuBis best choice recommendation in a browser window.

        .. note::

            Computes by default the Rubis best choice recommendation on the corresponding strict (codual) outranking digraph.

            In case of chordless circuits, if supporting arcs are more credible
            than the reversed negating arcs, we collapse the circuits into hyper nodes.
            Inversely,  if supporting arcs are not more credible than the reversed negating arcs,
            we brake the circuits on their weakest arc.
         
        Usage example:
        
        >>> from outrankingDigraphs import *
        >>> t = Random3ObjectivesPerformanceTableau(seed=5)
        >>> g = BipolarOutrankingDigraph(t)
        >>> g.showHTMLBestChoiceRecommendation()

        """
        from copy import deepcopy
        from time import time
        if Debug:
            Comments = True
        # construct html text
        html  = '<!DOCTYPE html><html><head>\n'
        html += '<meta charset="UTF-8">\n'
        if pageTitle == None:
            pageTitle = 'Best Choice Recommendation'
        html += '<title>%s</title>\n' % pageTitle
        html += '<style type="text/css">\n'
        if ContentCentered:
            html += 'td {text-align: center;}\n'
        html += 'td.na {color: rgb(192,192,192);}\n'
        html += '</style>\n'
        html += '</head>\n<body>\n'
        html += '<h1>%s</h1>' % pageTitle
        html += '<h3>Outranking digraph: %s</h3>' % self.name
       
        #print('RuBis BCR')
        t0 = time()
        n0 = self.order
        cpself = deepcopy(self)
        if CoDual:
            g = ~(-cpself)
        else:
            g = cpself
        if _OldCoca:
            _selfwcoc = CocaDigraph(g,Cpp=Cpp)
            b1 = 0
        elif BrokenCocs:
            #print('passed here!')
            _selfwcoc = BrokenCocsDigraph(g,Cpp=Cpp)
            b1 = _selfwcoc.breakings
        else:
            _selfwcoc = BreakAddCocsDigraph(g,Cpp=Cpp)
            b1 =  _selfwcoc.breakings
        n1 = _selfwcoc.order
        nc = n1 - n0
        
        #self.relation_orig = deepcopy(g.relation)
        if b1 > 0 or nc > 0:
            #self.actions_orig = deepcopy(g.actions)
            g.actions = deepcopy(_selfwcoc.actions)
            g.order = len(g.actions)
            g.relation = deepcopy(_selfwcoc.relation)
        if Debug:
            print('List of pseudo-independent choices')
            print(g.actions)
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        if Debug:
            g.showRelationTable()
        #self.showPreKernels()
        actions = set([x for x in g.actions])
        if Debug:
            g.showPreKernels()
            print(g.dompreKernels,g.abspreKernels)
        g.computeGoodChoices(Comments=Debug)
        g.computeBadChoices(Comments=Debug)
        if Debug:
            print('good and bad choices: ',g.goodChoices,g.badChoices)

        t1 = time()
        if Debug:
            print('Rubis best choice recommendation(s) (BCR)')
            print(' (in decreasing order of determinateness)   ')
            print('Credibility domain: [%.2f,%.2f]' %\
                  (g.valuationdomain['min'],\
                   g.valuationdomain['max']) )
        html += '<p>Rubis best choice recommendation(s) (BCR)</br>\n'
        html += ' (in decreasing order of determinateness)</br>\n'
        html += 'Credibility domain: [%.2f,%.2f]</p>\n' %\
                  (g.valuationdomain['min'],\
                   g.valuationdomain['max'])
        Med = g.valuationdomain['med']
        bestChoice = set()
        worstChoice = set()
        for gch in g.goodChoices:
            if gch[0] >= Med:
                goodChoice = True
                for bch in g.badChoices:
                    if gch[5] == bch[5]:
                        #if gch[0] == bch[0]:
                        if gch[3] == gch[4]:
                            if Comments:
                                print('null (good) choice ')
                                g.showChoiceVector(gch,choiceType='good',
                                                      ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        elif gch[4] > gch[3]:
                            if Comments:
                                print('outranked (good) choice ')
                                g.showChoiceVector(gch,choiceType='good',
                                                      ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',
                                                      ChoiceVector=ChoiceVector)
                            goodChoice = False
                        else:
                            goodChoice = True
                if goodChoice:
                    if Debug:
                        print(' === >> potential best choice(s)')
                    html += '<h3>Potential best choice(s)</h3>\n'
                    
                    html += g.htmlChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                    if bestChoice == set():
                        bestChoice = gch[5]
            else:
                if Debug:
                    print(' === >> non robust best choice(s)')
                html += '<h3>Non robust best choice(s)</h3>\n'
                html += g.htmlChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
        for bch in g.badChoices:
            if bch[0] >= Med:
                badChoice = True
                nullChoice = False
                for gch in g.goodChoices:
                    if bch[5] == gch[5]:
                        #if gch[0] == bch[0]:
                        if bch[3] == bch[4]:
                            if Comments:
                                print('null (bad) choice ')
                                g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                            badChoice = False
                            nullChoice = True
                        elif bch[3] > bch[4]:
                            if Comments:
                                print('outranking (bad) choice ')
                                g.showChoiceVector(gch,choiceType='good',ChoiceVector=ChoiceVector)
                                g.showChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                            badChoice = False
                        else:
                            badChoice = True
                if badChoice:
                    if Debug:
                        print(' === >> potential worst choice(s) ')
                    html += '<h3>Potential worst choice(s)</h3>\n '
                    html += g.htmlChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]
                elif nullChoice:
                    if Debug:
                        print(' === >> ambiguous choice(s)')
                    html += '<h3>Ambiguous choice(s)</h3>\n'
                    html += g.htmlChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
                    if worstChoice == set():
                        worstChoice = bch[5]

            else:
                if Debug:
                    print('=== >> non robust worst choice(s)')
                html += '<h3>Non robust worst choice(s)</h3>\n'
                html += g.htmlChoiceVector(bch,choiceType='bad',ChoiceVector=ChoiceVector)
        if Debug:
            print()
            print('Execution time: %.3f seconds' % (t1-t0))
            print('*****************************')

        html += '<p>Execution time: %.3f seconds</p>\n' % (t1-t0)
        # html footer
        html += '</body>\n'
        html += '</html>\n'
        return html

        self.bestChoice = bestChoice
        self.worstChoice = worstChoice
        #if nc > 0 or b1 > 0:
##        self.actions = deepcopy(self.actions_orig)
##        self.relation = deepcopy(self.relation_orig)
##        self.order = len(self.actions)
##        self.gamma = self.gammaSets()
##        self.notGamma = self.notGammaSets()


    def computeRubyChoice(self,CppAgrum=False,Comments=False,_OldCoca=False):
        """
        dummy for computeRubisChoice()
        old versions compatibility.
        """
        self.computeRubisChoice(CppAgrum=CppAgrum,Comments=Comments,_OldCoca=_OldCoca)

    def computeRubisChoice(self,CppAgrum=False,Comments=False,_OldCoca=False,BrokenCocs=True,\
                           Threading=False,nbrOfCPUs=1):
        """
        Renders self.strictGoodChoices, self.nullChoices
        self.strictBadChoices, self.nonRobustChoices.

        CppgArum = False (default | true : use C++/Agrum digraph library
        for computing chordless circuits in self.

        .. warning::
            Changes in site the outranking digraph by
            adding or braking chordless odd outranking circuits.
            
        """
        #print('Passing here',_OldCoca)
        if Comments:
            from time import time
            t0 = time()
        # save original actions and relation
        from copy import deepcopy
        try:
            self.actions_orig = deepcopy(self.actions_orig)
        except:
            self.actions_orig = deepcopy(self.actions)
        #self.actions_orig = actions_orig
        self.relation_orig = deepcopy(self.relation)
        # computing Coca
        if Comments:
            print('*--- computing the COCA digraph --*')
        if _OldCoca:
            _selfwcoc = CocaDigraph(self,Cpp=CppAgrum,Comments=Comments)
            self.breakings = 0
        elif BrokenCocs:
            _selfwcoc = BrokenCocsDigraph(self,Cpp=CppAgrum,Comments=Comments,\
                                    Threading=Threading,nbrOfCPUs=nbrOfCPUs)            
            self.breakings = _selfwcoc.breakings
        else:
            _selfwcoc = BreakAddCocsDigraph(self,Cpp=CppAgrum,Comments=Comments,\
                                    Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            self.breakings = _selfwcoc.breakings
        if Comments:
            print('Execution time: %.3f seconds' % (time()-t0))
            _selfwcoc.showPreKernels()
        # transferring coca actions and relation
        self.actions = deepcopy(_selfwcoc.actions)
        self.order = len(self.actions)
        self.relation = deepcopy(_selfwcoc.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        # computing good and bad choices
        actions = set([x for x in self.actions])
        self.dompreKernels = set()
        self.abspreKernels = set()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                self.dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                self.abspreKernels.add(choice[0][0])
        self.computeGoodChoices(Comments=Comments)
        self.computeBadChoices(Comments=Comments)
        # sorting out the strict choices
        self.strictGoodChoices = set()
        self.nullChoices = set()
        self.strictBadChoices = set()
        self.nonRobustChoices = set()
        for gch in self.goodChoices:
            if gch[0] <= 0:
                goodChoice = True
                for bch in self.badChoices:
                    if gch[5] == bch[5]:
                        if gch[3] == gch[4]:
                            goodChoice = False
                            self.nullChoices.add(frozenset(gch[5]))
                        elif gch[4] > gch[3]:
                            goodChoice = False
                            self.strictBadChoices.add(frozenset(bch[5]))
                        else:
                            goodChoice = True
                if goodChoice:
                    self.strictGoodChoices.add(frozenset(gch[5]))
            else:
                self.nonRobustChoices.add(frozenset(gch[5]))
        if Comments:
            self.showGoodChoices()
            self.showBadChoices()
        #n1 = _selfwcoc.order
        #nc = n1 - n0
        #if nc > 0 or b1 > 0:
        #self.actions = self.actions_orig
        #self.relation = self.relation_orig
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _computeRubisChoice(self,CppAgrum=False,Comments=False,_OldCoca=False):
        """
        Renders self.strictGoodChoices, self.nullChoices
        self.strictBadChoices, self.nonRobustChoices.

        CppgArum = False (default | true : use C++/Agrum digraph library
        for computing chordless circuits in self.

        .. warning::
            Changes in site the outranking digraph by
            adding or braking chordless odd outranking circuits.
            
        """
        #print('Passing here',_OldCoca)
        import copy,time
        if Comments:
            print('*--- computing the COCA digraph --*')

        n0 = self.order
        t0 = time.time()
        if _OldCoca:
            _selfwcoc = _CocaDigraph(self,Cpp=CppAgrum,Comments=Comments)
            b1 = 0
        else:
            _selfwcoc = CocaDigraph(self,Cpp=CppAgrum,Comments=Comments)
            b1 = _selfwcoc.brakings
        t1 = time.time()
        if Comments:
            print('Execution time: %.3f seconds' % (t1-t0))
            _selfwcoc.showPreKernels()
        try:
            self.actions_orig = copy.deepcopy(self.actions_orig)
        except:
            self.actions_orig = copy.deepcopy(self.actions)
        #self.actions_orig = actions_orig
        self.relation_orig = copy.deepcopy(self.relation)

        self.actions = _selfwcoc.actions
        self.order = len(self.actions)
        self.relation = _selfwcoc.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        actions = set([x for x in self.actions])
        self.dompreKernels = set()
        self.abspreKernels = set()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                self.dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                self.abspreKernels.add(choice[0][0])
        self.computeGoodChoices(Comments=Comments)
        self.computeBadChoices(Comments=Comments)
        self.strictGoodChoices = set()
        self.nullChoices = set()
        self.strictBadChoices = set()
        self.nonRobustChoices = set()
        for gch in self.goodChoices:
            if gch[0] >= 0:
                goodChoice = True
                for bch in self.badChoices:
                    if gch[5] == bch[5]:
                        if gch[3] == gch[4]:
                            goodChoice = False
                            self.nullChoices.add(frozenset(gch[5]))
                        elif gch[4] > gch[3]:
                            goodChoice = False
                            self.strictBadChoices.add(frozenset(bch[5]))
                    else:
                        goodChoice = True
                    if goodChoice:
                        self.strictGoodChoices.add(frozenset(gch[5]))
            else:
                self.nonRobustChoices.add(frozenset(gch[5]))
        if Comments:
            self.showGoodChoices()
            self.showBadChoices()
        n1 = _selfwcoc.order
        nc = n1 - n0
        #if nc > 0 or b1 > 0:
        #self.actions = self.actions_orig
        #self.relation = self.relation_orig
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    

    def computeGoodChoiceVector(self,ker,Comments=False):
        """
        | Computing Characteristic values for dominant pre-kernels
        | using the von Neumann dual fixoint equation
        """
        import copy
        from operator import itemgetter
        temp = copy.deepcopy(self)
        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        #actions.sort()
        relation = temp.relation
        if Comments:
            print('--> kernel:', ker)
        choice = [y for y in ker]
##        degi = temp.intstab(ker)
##        dega = temp.absorb(ker)
##        degd = temp.domin(ker)
##        degirred = temp.domirredval(ker,relation)
##        degmd = min(degi,degd)
##        cover = temp.averageCoveringIndex(ker)
        relation_k = temp.domkernelrestrict(choice)
        n = len(actions)
        #vec1_a = array.array('f', [Max] * n)
        vec1_a = [Max for i in range(n)]
        #vec0_a = array.array('f', [Min] * n)
        vec0_a = [Min for i in range(n)]
        mat = [temp.readdomvector(x,relation_k) for x in actions]
        veclowa = vec0_a
        vechigha = vec1_a
        if Comments:
            print('initial low vector  :',veclowa)
            print('initial high vector :', vechigha)
        it = 1
        while veclowa != vechigha and it < 2*n*n:
            veclowb = temp.matmult2(mat,veclowa)
            vechighb = temp.matmult2(mat,vechigha)
            veclow = temp.contra(vechighb)
            vechigh = temp.contra(veclowb)
            if veclow == veclowa and vechigh == vechigha : break
            veclowa = veclow
            vechigha = vechigh
            if Comments:
                print(it, 'th low vector  :',veclowa)
                print(it, 'th high vector :',vechigha)
            it += 1
        if Comments:
            print('final low vector  :', veclowa)
            print('final high vector :', vechigha)
            print('#iterations       :', it)
        domvec = temp.sharpvec(veclowa,vechigha)
        determ = temp.determinateness(domvec)
        goodChoiceVector = []
        for i in range(n):
            goodChoiceVector.append((domvec[i],str(actions[i])))
        goodChoiceVector.sort(reverse=True)
        if Comments:
            print('Choice vector for dominant pre-kernel: %s' % str(ker))
            for i,item in enumerate(goodChoiceVector):
                print('%s: %+.2f' % (item[1],item[0]) )
        else:
            return goodChoiceVector        

    def computeKernelVector(self,kernel,Initial=True,Comments=False):
        """
        | Computing Characteristic values for dominant pre-kernels
        | using the von Neumann dual fixoint equation
        """
        import copy
        from operator import itemgetter
        temp = copy.deepcopy(self)
        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        #actions.sort()
        relation = temp.relation
        ker = set(kernel)
        if Comments:
            if Initial:
                print('--> Initial kernel:', ker)
            else:
                print('--> Terminal kernel:', ker)
        choice = [x for x in ker]
        if Initial:
            relation_k = temp.domkernelrestrict(choice)
        else:
            relation_k = temp.abskernelrestrict(choice)
        n = len(actions)
        #vec1_a = array.array('f', [Max] * n)
        vec1_a = [Max for i in range(n)]
        #vec0_a = array.array('f', [Min] * n)
        vec0_a = [Min for i in range(n)]
        if Initial:
            mat = [temp.readdomvector(x,relation_k) for x in actions]
        else:
            mat = [temp.readabsvector(x,relation_k) for x in actions]
        veclowa = vec0_a
        vechigha = vec1_a
        if Comments:
            print('initial low vector  :',veclowa)
            print('initial high vector :', vechigha)
        it = 1
        while veclowa != vechigha and it < 2*n*n:
            veclowb = temp.matmult2(mat,veclowa)
            vechighb = temp.matmult2(mat,vechigha)
            veclow = temp.contra(vechighb)
            vechigh = temp.contra(veclowb)
            if veclow == veclowa and vechigh == vechigha : break
            veclowa = veclow
            vechigha = vechigh
            if Comments:
                print(it, 'th low vector  :',veclowa)
                print(it, 'th high vector :',vechigha)
            it += 1
        if Comments:
            print('final low vector  :', veclowa)
            print('final high vector :', vechigha)
            print('#iterations       :', it)
        domvec = temp.sharpvec(veclowa,vechigha)
        determ = temp.determinateness(domvec)
        choiceVector = []
        for i in range(n):
            choiceVector.append((domvec[i],str(actions[i])))
        choiceVector.sort(reverse=True)
        if Comments:
            if Initial:
                print('Choice vector for initial pre-kernel: %s' % str(ker))
            else:
                print('Choice vector for terminal pre-kernel: %s' % str(ker))
            for i,item in enumerate(choiceVector):
                print('%s: %+.2f' % (item[1],item[0]) )
        else:
            return choiceVector        

                                
    def computeGoodChoices(self,Comments=False):
        """
        Computes characteristic values for potentially good choices.

        ..note::

             Return a tuple with following content:

             [(0)-determ,(1)degirred,(2)degi,(3)degd,(4)dega,(5)str(choice),(6)domvec,(7)cover]
             
        """
        import copy
        from operator import itemgetter
        temp = copy.deepcopy(self)
        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        relation = temp.relation
        domChoices = []
        if 'dompreKernels' not in dir(temp):
            if Comments:
                temp.showPreKernels()
            else:
                temp.computePreKernels()
        for ker in temp.dompreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.domirredval(ker,relation)
            degmd = min(degi,degd)
            cover = temp.averageCoveringIndex(ker)
            relation_k = temp.domkernelrestrict(choice)
            n = len(actions)
            #vec1_a = array.array('f', [Max] * n)
            vec1_a = [Max for i in range(n)]
            #vec0_a = array.array('f', [Min] * n)
            vec0_a = [Min for i in range(n)]
            mat = [temp.readdomvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            if Comments:
                print('initial veclow',veclowa)
                print('initial vechigh', vechigha)
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                if Comments:
                    print(it, 'th veclow  :',veclowa)
                    print(it, 'th vechigh :',vechigha)
                it += 1
            if Comments:
                print('final veclow  :', veclowa)
                print('final vechigh :', vechigha)
                print('#iterations    :', it)
            #domvec = temp.sharpvec(veclowa,vechigha)
            domvecsharp = temp.sharpvec(veclowa,vechigha)
            if Comments:
                print('final result   ;',domvecsharp)
            domvec = [(domvecsharp[i],str(actions[i])) for i in range(n)]
            domvec.sort(reverse=True)
            determ = temp.determinateness(domvec)
            domChoices.append([determ,degirred,degi,degd,-dega,str(choice),domvec,cover])
        domChoicesSort = sorted(domChoices,key=itemgetter(0,7,3,4),reverse=True)
        goodChoicesDic = {}
        for ch in domChoicesSort:
            ch[4] = -ch[4]
            ch[5] = eval(ch[5])
            goodChoicesDic[frozenset(ch[5])] = {'determ':ch[0],
                                    'degirred':ch[1],
                                    'degi':ch[2],
                                    'degd':ch[3],
                                    'dega':ch[4],
                                    'cover':ch[7],
                                    'bpv':ch[6]}

        self.goodChoices = domChoicesSort
        return goodChoicesDic

    def computeGoodPirlotChoices(self,Comments=False):
        """
        Characteristic values for potentially good choices
        using the Pirlot fixpoint algorithm.
        """
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        actions = list(self.actions.keys())
        n = len(actions)
        relation = self.relation
        domChoicesSort = []
        if 'dompreKernels' not in dir(self):
            self.computePreKernels()
        for ker in self.dompreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = self.intstab(ker)
            dega = self.absorb(ker)
            degd = self.domin(ker)
            degirred = self.domirredval(ker,relation)
            degmd = min(degi,degd)
            #vecmed = array.array('f', [Med] * n)
            #vecsol0 = array.array('f', [Min] * n)
            vecmed = [Med for i in range(n)]
            vecsol0 = [Min for i in range(n)]
            for x in range(n):
                if actions[x] in choice:
                    vecsol0[x] = Max
            if Comments:
                print('initial solution', vecsol0)
            mat0 = [self.readdomvector(x,relation) for x in actions]
            mat = self.irreflex(mat0)
            vecsol = vecsol0
            vecsolfin = vecmed
            it = 0
            while it < 2*n*n:
                vecsolfin = self.matmult2(mat,vecsol)
                if Comments:
                    print(it, 'th vecsol  :',vecsol)
                veccur = self.contra(vecsolfin)
                if vecsol == veccur : break
                vecsol = veccur
                it += 1
            if Comments:
                print('Final Solution=', vecsol)
            determ = self.determinateness(vecsol)
            domChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),vecsol])
        domChoicesSort.sort()
        for ch in domChoicesSort:
            ch[5] = eval(ch[5])
        self.goodChoices = domChoicesSort


    def computeBadPirlotChoices(self,Comments=False):
        """
        Characteristic values for potentially bad choices
        using the Pirlot's fixpoint algorithm.
        """
        import array
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        actions = list(self.actions.keys())
        n = len(actions)
        relation = self.relation
        absChoicesSort = []
        if 'abspreKernels' not in dir(self):
            self.computePreKernels()
        for ker in self.abspreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = self.intstab(ker)
            dega = self.absorb(ker)
            degd = self.domin(ker)
            degirred = self.absirredval(ker,relation)
            degmd = min(degi,degd)
            #vecmed = array.array('f', [Med] * n)
            #vecsol0 = array.array('f', [Min] * n)
            vecmed = [Med for i in range(n)]
            vecsol0 = [Min for i in range(n)]
            for x in range(n):
                if actions[x] in choice:
                    vecsol0[x] = Max
            if Comments:
                print('initial solution', vecsol0)
            mat0 = [self.readabsvector(x,relation) for x in actions]
            mat = self.irreflex(mat0)
            vecsol = vecsol0
            vecsolfin = vecmed
            it = 0
            while it < 2*n*n:
                vecsolfin = self.matmult2(mat,vecsol)
                if Comments:
                    print(it, 'th vesol :',vecsol)
                veccur = self.contra(vecsolfin)
                if vecsol == veccur : break
                vecsol = veccur
                it += 1
            if Comments:
                print('Final Solution=', vecsol)
            determ = self.determinateness(vecsol)
            absChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),vecsol])
        absChoicesSort.sort()
        for ch in absChoicesSort:
            ch[5] = eval(ch[5])
        self.badChoices = absChoicesSort

    def determinateness(self,vec,inPercent = True):
        """
        Renders the determinateness of a characteristic vector *vec* = 
        [(r(x),x),(r(y),y), ...] of length *n* in valuationdomain [Min,Med,Max]:
        
        *result* =  sum_x( abs(r(x)-Med) ) / ( n*(Max-Med) )

        If inPercent, *result* shifted (+1) and reduced (/2) to [0,1] range. 
        """
        Min = Decimal(str(self.valuationdomain['min']))
        Max = Decimal(str(self.valuationdomain['max']))
        Med = Decimal(str(self.valuationdomain['med']))
        result = Decimal('0.0')
        n = len(vec)
        for i in range(n):
            try:
                result += abs(vec[i][0]-Med)
            except:
                result += abs(vec[i]-Med)
            #print result
        result /= n*(Max-Med)
        #print result
        if inPercent:
            return (result + Decimal('1.0'))/Decimal('2.0')
        else:
            return result*(Max-Med)


    def computeBadChoices(self,Comments=False):
        """
        Computes characteristic values for potentially bad choices.

        .. note::

             Returns a tuple with following content:

             [(0)-determ,(1)degirred,(2)degi,(3)degd,(4)dega,(5)str(choice),(6)absvec]
             
        """
        import copy
        from operator import itemgetter

        temp = copy.deepcopy(self)

        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        relation = temp.relation
        absChoices = []
        if 'abspreKernels' not in dir(temp):
            temp.computePreKernels()
        for ker in temp.abspreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.absirredval(ker,relation)
            cover = temp.averageCoveringIndex(ker,direction="in")
            relation_k = temp.abskernelrestrict(choice)
            n = len(actions)
            #vec1_a = array.array('f', [Max] * n)
            #vec0_a = array.array('f', [Min] * n)
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readabsvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            if Comments:
                print('initial veclowa',veclowa)
                print('initial vechigha', vechigha)
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                if Comments:
                    print(it, 'th veclowa  :',veclowa)
                    print(it, 'th vechigha :',vechigha)
                it += 1
            if Comments:
                print('final veclowa',veclowa)
                print('final vechigha', vechigha)
            absvecsharp = temp.sharpvec(veclowa,vechigha)
            absvec = [(absvecsharp[i],str(actions[i])) for i in range(n)]
            absvec.sort(reverse=True)
            determ = temp.determinateness(absvec)
            absChoices.append([determ,degirred,degi,-degd,dega,str(choice),absvec,cover])
        absChoicesSort = sorted(absChoices,key=itemgetter(0,7,4,3),reverse=True)
        #absChoicesSort.sort()
        ## absChoicesSort.sort(reverse=True, key=itemgetter(7))
        ## for ch in absChoicesSort:
        ##     ch[5] = eval(ch[5])
        ## self.badChoices = absChoicesSort
        badChoicesDic = {}
        for ch in absChoicesSort:
            ch[3] = -ch[3]
            ch[5] = eval(ch[5])
            badChoicesDic[frozenset(ch[5])] = {'determ':ch[0],
                                    'degirred':ch[1],
                                    'degi':ch[2],
                                    'degd':ch[3],
                                    'dega':ch[4],
                                    'cover':ch[7],
                                    'bpv':ch[6]}
            
        self.badChoices = absChoicesSort
        
        return badChoicesDic

    def htmlChoiceVector(self,ch,ChoiceVector=True,choiceType="good"):
        """
        Show procedure for annotated bipolar choices.
        """
        from digraphsTools import flatten
        actions = [x for x in self.actions]
        Med = self.valuationdomain['med']
        determ = ch[0]
        degirred = ch[1]
        degi = ch[2]
        degd = ch[3]
        dega = ch[4]
        choice = [x for x in flatten(ch[5])]
        choice.sort()
        vec = ch[6]
        vec.sort(reverse=True)
        html  = '<p>Choice              : <b>%s</b><br/>\n ' % str(choice)
        #html += '  +-irredundancy      : %.2f<br/>\n' % (degirred)
        html += '  independence        : %.2f<br/>\n' % (degi)
        html += '  dominance           : %.2f<br/>\n' % (degd)
        html += '  absorbency          : %.2f<br/>\n' % (dega)
        if choiceType == "good":
            html += '  covering (%%): %.2f<br/>\n' %\
                ( self.averageCoveringIndex(choice,direction='out') * Decimal('100') )
        elif choiceType == "bad":
            html += '  covered (%%) : %.2f<br/>\n' %\
                ( self.averageCoveringIndex(choice,direction='in') * Decimal('100') )
        else:
            html += '  covering (%%): %.2f<br/>\n' %\
                ( self.averageCoveringIndex(choice) * Decimal('100') )            
            
        html += '  determinateness (in %%) : %.2f</p>\n' % (determ*Decimal('100.0'))
        if ChoiceVector:
            html += '<p>  - characteristic vector = {\n'
            for i in range(len(actions)):
                try:
                    choice = [x for x in eval(vec[i][1])]
                    choice.sort()
                    html += '\'%s\': %.2f,\n ' %  (str(choice),vec[i][0])
                except:
                    html += '\'%s\': %.2f,\n ' %  (vec[i][1],vec[i][0])
            html +='}</p>\n'
##        elif determ > Decimal('0'):
        else:
            html += '  - most credible action(s) = {\n'
            for i in range(len(actions)):
                if vec[i][0] > Med:
                    try:
                        choice = [x for x in eval(vec[i][1])]
                        choice.sort()
                        html += '\'%s\': %.2f,\n' %  (str(choice),vec[i][0])
                    except:
                        html += '\'%s\': %.2f,\n' %  (vec[i][1],vec[i][0])
            html += '}</p>\n'
        return html

    def showChoiceVector(self,ch,choiceType="good",ChoiceVector=True):
        """
        Show procedure for annotated bipolar choices.
        """
        from digraphsTools import flatten
        actions = [x for x in self.actions]
        Med = self.valuationdomain['med']
        determ = ch[0]
        degirred = ch[1]
        degi = ch[2]
        degd = ch[3]
        dega = ch[4]
        choice = [x for x in flatten(ch[5])]
        choice.sort()
        vec = ch[6]
        vec.sort(reverse=True)
        print('* choice              : ' + str(choice))
        #print('  +-irredundancy      : %.2f' % (degirred))
        print('  independence        : %.2f' % (degi))
        print('  dominance           : %.2f' % (degd))
        print('  absorbency          : %.2f' % (dega))
        if choiceType == "good":
            print('  covering (%)' + '        : %.2f' %\
                  ( self.averageCoveringIndex(choice,direction='out') * Decimal('100') ))
        elif choiceType == "bad":
            print('  covered (%) ' + '        : %.2f' %\
                  ( self.averageCoveringIndex(choice,direction='in') * Decimal('100') ))
        else:
            print('  covering (%)' + '        : %.2f' %\
                  ( self.averageCoveringIndex(choice) * Decimal('100') ))
            
        print("  determinateness (%)", end=' ')
        print(': %.2f' % (determ*Decimal('100.0')))
        if ChoiceVector:
            print('  - characteristic vector = {', end=' ')
            for i in range(len(actions)):
                #print('\'%s\': %.2f,' %  (str(actions[i]),vec[i]), end=' ')
                try:
                    choice = [x for x in eval(vec[i][1])]
                    choice.sort()
                    print('\'%s\': %.2f' %  (str(choice),vec[i][0]), end=', ')
                except:
                    print('\'%s\': %.2f' %  (vec[i][1],vec[i][0]), end=', ')
                
                #print('\'%s\': %.2f,' %  (vec[i][1],vec[i][0]), end=' ')
            print('}')
##        elif determ > Decimal('0'):
        else:
            print('  - most credible action(s) = {', end=' ')
            for i in range(len(actions)):
                if vec[i][0] > Med:
                    try:
                        choice = [x for x in eval(vec[i][1])]
                        choice.sort()
                        print('\'%s\': %.2f' %  (str(choice),vec[i][0]), end=', ')
                    except:
                        print('\'%s\': %.2f' %  (vec[i][1],vec[i][0]), end=', ')
            print('}')
            print()

    def showGoodChoices(self,Recompute=True):
        """
        Characteristic values for potentially good choices.
        """
        import array,copy
        from operator import itemgetter
        temp = copy.deepcopy(self)

        Max = temp.valuationdomain['max']
        Min = temp.valuationdomain['min']
        Med = temp.valuationdomain['med']
        actions = [x for x in temp.actions]
        n = len(actions)
        relation = temp.relation
        print('*** Potentially good choices ***')
        print('    valuationdomain', temp.valuationdomain)
        domChoices = []
        if 'dompreKernels' not in dir(temp) or Recompute:
            temp.computePreKernels()
        for ker in temp.dompreKernels:
            choice = [str(y) for y in ker]
            choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.domirredval(ker,relation)
            degmd = min(degi,degd)
            cover = temp.averageCoveringIndex(ker,direction="out")
            domChoices.append([degmd,degirred,degi,degd,-dega,str(choice),cover])
        domChoicesSort = sorted(domChoices,key=itemgetter(0,6,3,4),reverse=True)
        print('domChoicesSort', domChoicesSort)
        for ch in domChoicesSort:
            choice = ch[5]
            degirred = ch[1]
            degi = ch[2]
            degd = ch[3]
            dega = -ch[4]
            print('* choice           : ' + str(choice))
            #print('  +irredundance    : %.2f' % (degirred))
            print('  independence     : %.2f' % (degi))
            print('  dominance        : %.2f' % (degd))
            print('  absorbency       : %.2f' % (dega))
            relation_k = temp.domkernelrestrict(eval(choice))
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readdomvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                it += 1
            print('  + characteristic vector = [', end=' ')
            bestvec = temp.sharpvec(veclowa,vechigha)
            for i in range(len(actions)):
                print('\'' + str(actions[i]) + '\': ',bestvec[i], ' ', end=' ')
            print(']')
            print()

    def irreflex(self,mat):
        """
        Puts diagonal entries of mat to valuationdomain['min']
        """
        Min = self.valuationdomain['min']
        n = len(mat[0])
        for i in range(n):
            mat[i][i] = Min
        return mat

    def showBadChoices(self,Recompute=True):
        """
        Characteristic values for potentially bad choices.
        """
        import copy
        from operator import itemgetter
        temp = copy.deepcopy(self)

        Max = temp.valuationdomain['max']
        Min = temp.valuationdomain['min']
        Med = temp.valuationdomain['med']
        actions = [x for x in temp.actions]
        #actions.sort()
        relation = temp.relation
        print('*** Potentially bad choices ***')
        print('    valuationdomain', temp.valuationdomain)
        absChoices = []
        if 'abspreKernels' not in dir(temp) or Recompute:
            temp.computePreKernels()
        for ker in temp.abspreKernels:
            choice = [str(y) for y in ker]
            choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.absirredval(ker,relation)
            degmd = min(degi,dega)
            cover = temp.averageCoveringIndex(ker,direction="in")
            absChoices.append((degmd,degirred,degi,-degd,dega,str(choice),cover))
        absChoicesSort = sorted(absChoices,key=itemgetter(0,6,4,3),reverse=True)
        print('absChoicesSort', absChoicesSort)
        absChoicesSort.sort()
        for ch in absChoicesSort:
            choice = ch[5]
            degirred = ch[1]
            degi = ch[2]
            degd = -ch[3]
            dega = ch[4]
            print('* choice           : ' + str(choice))
            #print('  -irredundance    : %.2f' % (degirred))
            print('  independence     : %.2f' % (degi))
            print('  dominance        : %.2f' % (degd))
            print('  absorbency       : %.2f' % (dega))
            relation_k = temp.abskernelrestrict(eval(choice))
            n = len(actions)
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readabsvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                it += 1
            print('  - characteristic vector = [', end=' ')
            bestvec = temp.sharpvec(veclowa,vechigha)
            for i in range(len(actions)):
                print('\'' + str(actions[i]) + '\': ',bestvec[i], ' ', end=' ')
            print(']')
            print()

    def showMIS_AH(self,withListing=True):
        """
        Prints all MIS using the Hertz method.

        Result saved in self.hertzmisset.
        """
        import sys,random,copy,time
        relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        gamma = self.gammaSets()
        notGamma = self.notGammaSets()
        t0 = time.time()
        # MIS extraction
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. version 7(6)-25-Apr-06       *')
        print('*-----------------------------------*')
        print('*---- MIS extraction ----')
        t0 = time.time()
        # initialize MIS extraction
        hertzmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | gamma[i][0]
        if withListing:
            print('===>>> Initial solution : ', list(S))
        hertzmisset = hertzmisset | set([frozenset(S)])
        # initialize all variables
        R = V - S
        ns = len(S)
        n = self.order
        i = 0
        P  = [set() for x in range(n)]
        M  = [set() for x in range(n)]
        NR = [set() for x in range(n)]
        Q  = [set() for x in range(n)]
        v  = [0     for x in range(n)]
        NON_R = set()
        OUI_R = set()
        NON_S = set()
        OUI_S = set()
        hist = 0
        # core of the algorithm
        while i >= 0:
            hist += 1
            # Part 1
            for k in [x for x in NON_R if gamma[x][0] & (OUI_R | OUI_S) == set() and len(gamma[x][0] - NON_R - NON_S) == 1]:
                sr = gamma[k][0]-NON_R-NON_S
                if sr != set():
                    if sr < R:
                        P[i] = P[i] | sr
                        OUI_R = OUI_R | sr
                        r = sr.pop()
                        NR[i] = NR[i] | (gamma[r][0] & (R-NON_R))
                        NON_R = NON_R | (gamma[r][0] & R)
                        M[i] = M[i] | (gamma[r][0] & (S-NON_S))
                        NON_S = NON_S | (gamma[r][0] & S)
                        test = True
                        for vr in (R - OUI_R):
                            if gamma[vr][0] & ((S - NON_S) | OUI_R) == set():
                                test = False
                                break
                        if test == True:
                            hertzmisset = hertzmisset | set([frozenset((S - NON_S) | OUI_R)])
                    else:
                        Q[i] = Q[i] | sr
                        OUI_S = OUI_S | sr
                        r = sr.pop()
                        NR[i] = NR[i] | (gamma[r][0] & (R-NON_R))
                        NON_R = NON_R | (gamma[r][0] & R)

           # Part 2
            if (NON_R | OUI_R) != R:
                i +=1
                setPart2v = R - NON_R - OUI_R
                v[i] = setPart2v.pop()
                P[i] = set([v[i]])
                OUI_R = OUI_R | P[i]
                M[i] = gamma[v[i]][0] & (S - NON_S)
                NON_S = NON_S | M[i]
                NR[i] = gamma[v[i]][0] & (R - NON_R)
                NON_R = NON_R | NR[i]
                test = True
                for vr in (R - OUI_R):
                    if gamma[vr][0] & ((S - NON_S) | OUI_R) == set():
                        test = False
                        break
                if test == True:
                    hertzmisset = hertzmisset | set([frozenset((S - NON_S) | OUI_R)])
            else:
                i -= 1
                NR[i] = NR[i] | set([v[i+1]])
                NON_R = (NON_R - NR[i+1]) | set([v[i+1]])
                NON_S = NON_S - M[i+1]
                OUI_R = OUI_R - P[i+1]
                OUI_S = OUI_S - Q[i+1]
                Q[i+1] = set()

        # end of algorithm
        t1 = time.time()
        if withListing:
            print('*---- results ----*')
        v = [0 for i in range(n+1)]
        mislen = set()
        for ch in hertzmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
            mislen = mislen | set([len(ch)])
        print('*---- statistics ----*')
        print('mis lengths      : ', list(range(self.order+1)))
        print('frequency        : ', v)
        mislenlist = list(mislen)
        mislenlist.sort()
        print('mis lengths      : ', mislenlist)
        print('mis solutions    : ', len(hertzmisset))
        print('execution time   : %.5f sec.' % (t1 - t0))
        print('iteration history: ', hist)
        print('result in self.hertzmisset')
        # store global results
        self.mislen = mislenlist
        self.hertzmisset = hertzmisset
        # restore original relation and neigborhooods
        self.relation = relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showMIS_RB(self,withListing=True):
        """
        Prints all MIS using the Bisdorff method.

        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        t0 = time.time()
        # initialize MIS extraction
        newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        newmisset = newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                newmisset = newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        i = 0
        for mis in initmisset:
            print(list(mis[1]), mis[0])
            i +=1

        # MIS extraction
        print('*---- MIS extraction ----')
        mislen = set()   # list of MIS length observed
        S = initmisset[i-1][1]  # start with largest init MIS
        print('===>>> Initial solution : ', list(S))
        ns = len(S)

        print('--> iteration 0 ')
        mislen = mislen | set([ns])

        upmis = set()  # independent choices as MIS candidates
        R = V - S
        for r in R:   # add a node from outside S
            Sr = (S - self.gamma[r][0]) | set([r]) # Sr independent
            upmis = upmis | set([frozenset(Sr)])

        iter = 0
        uphistory = set()
        while upmis != set():
            iter += 1  # next iteration init
            print('--> up iteration: ', iter)
            upmisiter = copy.copy(upmis)
            print('potential choices: ', len(upmisiter))
            uphistory = uphistory | upmis
            upmis = set()
            # up movement
            for Sch in upmisiter:

                gammaSch = set()
                for x in Sch:
                    gammaSch = gammaSch | self.gamma[x][0]

                while (Sch | gammaSch) != V:
                    i = random.choice(list(V-Sch-gammaSch))
                    Sch = Sch | set([i])
                    gammaSch = gammaSch | self.gamma[i][0]

                if Sch not in newmisset:
                    mislen = mislen | set([len(Sch)])
                    newmisset = newmisset | set([frozenset(Sch)])

                    Rch = V - Sch
                    for r in Rch:   # add a node from outside S
                        Srch = (Sch - self.gamma[r][0]) | set([r]) # Sr independent
                        if Srch not in uphistory:
                            upmis = upmis | set([frozenset(Srch)])

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        mislenlist = list(mislen)
        mislenlist.sort()
        print('mis lengths   : ', mislenlist)
        print('mis solutions : ', len(newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('up-history    : ', len(uphistory))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. version Ronda  April 2006    *')
        print('*-----------------------------------*')
        # store global results
        self.mislen = mislenlist
        self.newmisset = newmisset
        # restore original relation and neigborhooods
        self.relation = relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showMIS_UD(self,withListing=True):
        """
        Prints all MIS using the Hertz-Bisdorff method.

        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        sys.setrecursionlimit(15000)
        self.relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.showAll()
        t0 = time.time()
        # initilaize MIS extraction
        self.newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        V = set(self.actions)
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        self.newmisset = self.newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                self.newmisset = self.newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        for mis in initmisset:
            print(list(mis[1]), mis[0])
        print('*---- same mises with up and down potentials ----')
        self.upmis = set()    # independent choices as MIS candidates
        self.downmis = set()  # covering choices as MIS candidates
        self.mislen = set()   # list of MIS length observed
        for mis in initmisset:
            S = mis[1]
            print('===>>> Inital solution : ', list(S))
            print('--> compute MIS of same size ', len(S))
            s = 0
            ns = mis[0]
            self.mislen = self.mislen | set([ns])
            V = set(self.actions)
            self.computeupdown1(s,S)  # compute all MIS of length ns
            iter = 0
            while self.upmis != set() or self.downmis != set():
                iter += 1  # next iteration init
                print('\n--> up iteration: ', iter)
                self.upmisiter = self.upmis.copy()
                self.upmis = set()
                self.downmisiter = self.downmis.copy()
                self.downmis = set()
                V = set(self.actions)
                # up movement
                for Sup in self.upmisiter:
                    Sch = Sup[0]
                    gammaSch = Sup[1]
                    while (Sch | gammaSch) != V:
                        i = random.choice(list(V-Sch-gammaSch))
                        Sch = Sch | set([i])
                        gammaSch = gammaSch | self.gamma[i][0]
                    if Sch not in self.newmisset:
                        self.mislen = self.mislen | set([len(Sch)])
                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                        s = 0
                        self.computeupdown1(s,Sch)
                # down movement
                print('\n*    <<< down potentials in', iter)
                for Sch in self.downmisiter:
                    for v in Sch:
                        if self.gamma[v][0] & Sch != set():
                            Sch = Sch - set([v])
                            gammaSch = set()
                            for x in Sch:
                                gammaSch = gammaSch | self.gamma[x][0]
                            if gammaSch & Sch == set():
                                if Sch | gammaSch == V:
                                    if Sch not in self.newmisset:
                                        self.mislen = self.mislen | set([len(Sch)])
                                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                                        self.computeupdown1(s,Sch)
                            else:
                                if Sch | gammaSch == V:
                                    self.downmis = self.downmis | set([frozenset(Sch)])

            print('solutions: ', len(self.newmisset))

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in self.newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        print('mis lengths   : ', list(self.mislen))
        print('mis solutions : ', len(self.newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. April 2006                   *')
        print('*-----------------------------------*')
        # restore original relation and neigborhooods
        self.relation = self.relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeupdown1(self, s, S):
        """
        Help method for show_MIS_HB2 method.
        fills self.newmisset, self.upmis, self.downmis.
        """
        Min = self.valuationdomain['min']
        V = set(self.actions)
        R = V - S
        print(s, end=' ') # recursion depth: traces the discovery of MISs
        s += 1
        for v in S: # choose a leaving node
            Sv = S - set([v])
            gammaSv = set() # recompute neighborhood
            for sv in Sv:
                gammaSv = gammaSv | self.gamma[sv][0]
            for r in R:   # add a node from outside S
                Svr = Sv | set([r])
                gammaSvr = gammaSv | self.gamma[r][0]
                if gammaSvr & Svr == set(): # if independent
                    if gammaSvr | Svr == V: # and if covering
                        if Svr not in self.newmisset:
                            #print 'MIS ', Svr
                            self.newmisset = self.newmisset | set([frozenset(Svr)])
                            self.computeupdown1(s,Svr)
                    else:                   # indep. and not covering
                        #print 'up ->',Svr
                        self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])
                elif Svr | gammaSvr == V:   # covering but not independent
                    #print 'down->',Svr
                    self.downmis = self.downmis | set([frozenset(Svr)])


    def showMIS_HB2(self,withListing=True):
        """
        Prints all MIS using the Hertz-Bisdorff method.

        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        sys.setrecursionlimit(15000)
        self.relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.showAll()
        t0 = time.time()
        # initilaize MIS extraction
        self.newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        V = set(self.actions)
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        self.newmisset = self.newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                self.newmisset = self.newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        for mis in initmisset:
            print(list(mis[1]), mis[0])
        print('*---- same mises with up and down potentials ----')
        self.upmis = set()    # independent choices as MIS candidates
        self.uphistory = set()
        self.downmis = set()  # covering choices as MIS candidates
        self.downhistory = set()
        self.mislen = set()   # list of MIS length observed
        for mis in initmisset:
            S = mis[1]
            print('===>>> Inital solution : ', list(S))
            print('--> compute MIS of same size ', len(S))
            s = 0
            ns = mis[0]
            self.mislen = self.mislen | set([ns])
            V = set(self.actions)
            self.computeupdown2(s,S)  # starting from S compute all MIS of same length
            iter = 0
            while self.upmis != set() or self.downmis != set():
                iter += 1  # next iteration init
                self.upmisiter = self.upmis.copy()
                self.uphistory = self.uphistory | self.upmis
                self.upmis = set()
                self.downmisiter = self.downmis.copy()
                self.downhistory = self.downhistory | self.downmis
                self.downmis = set()
                V = set(self.actions)
                # up movement
                print('\n  >>> up iteration: ', iter)
                for Sup in self.upmisiter:
                    Sch = Sup[0]
                    gammaSch = Sup[1]
                    while (Sch | gammaSch) != V:
                        i = random.choice(list(V-Sch-gammaSch))
                        Sch = Sch | set([i])
                        gammaSch = gammaSch | self.gamma[i][0]
                    if Sch not in self.newmisset:
                        self.mislen = self.mislen | set([len(Sch)])
                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                        s = 0
                        self.computeupdown2(s,Sch)
                # down movement
                print('\n*    <<< down potentials in', iter)
                for Sch in self.downmisiter:
                    for v in Sch:
                        if self.gamma[v][0] & Sch != set():
                            Sch = Sch - set([v])
                            gammaSch = set()
                            for x in Sch:
                                gammaSch = gammaSch | self.gamma[x][0]
                            if gammaSch & Sch == set():
                                if Sch | gammaSch == V and Sch not in self.newmisset:
                                    self.mislen = self.mislen | set([len(Sch)])
                                    self.newmisset = self.newmisset | set([frozenset(Sch)])
                                    s = 0
                                    self.computeupdown2(s,Sch)
                                #elif Sch not in self.uphistory:
                                    #print 'up ->',Sch
                                    #self.upmis = self.upmis | set([(frozenset(Sch),frozenset(gammaSch))])

                            else:
                                if Sch | gammaSch == V and Sch not in self.downhistory:
                                    self.downmis = self.downmis | set([frozenset(Sch)])

            print('solutions: ', len(self.newmisset))

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in self.newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        print('mis lengths   : ', list(self.mislen))
        print('mis solutions : ', len(self.newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. April 2006                   *')
        print('*-----------------------------------*')
        # restore original relation and neigborhooods
        self.relation = self.relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeupdown2irred(self, s, S):
        """
        Help method for show_MIS_HB1 method.
        Fills self.newmisset, self.upmis, self.downmis.
        """
        #import copy
        newmis = set([frozenset(S)])
        V = set(self.actions)
        s = 0
        while newmis != set():
            self.newmisset = self.newmisset | newmis
            S = newmis.pop()
            R = V - S
            print(s, end=' ') # recursion depth: traces the discovery of MISs
            s += 1
            #Siter = copy.copy(S)
            for v in S: # choose a leaving node
                Sv = S - set([v])
                gammaSv = set() # recompute Sv neighborhood
                for sv in Sv:
                    gammaSv = gammaSv | self.gamma[sv][0]
                privgammav = (self.gamma[v][0] | set([v])) - (gammaSv | Sv)
                for r in R:   # add a node from outside S
                    if privgammav <= self.gamma[r][0]:  # covering
                        Svr = Sv | set([r])
                        if self.gamma[r][0] & Sv == set():  # independent
                            if Svr not in self.newmisset:
                                print('new MIS ', Svr)
                                newmis = newmis | set([frozenset(Svr)])
                        else:
                            if Svr not in self.downhistory:
                                print('down->',Svr)
                                self.downmis = self.downmis | set([frozenset(Svr)])
                    else:
                        if self.gamma[r][0] & Sv == set():  # independent
                            Svr = Sv | set([r])
                            if Svr not in self.uphistory:
                                print('up ->',Svr)
                                gammaSvr = gammaSv | self.gamma[r][0]
                                self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])

    def computeupdown2(self, s, S):
        """
        Help method for show_MIS_HB1 method.
        Fills self.newmisset, self.upmis, self.downmis.
        """
        #import copy
        newmis = set([frozenset(S)])
        V = set(self.actions)
        s = 0
        while newmis != set():
            self.newmisset = self.newmisset | newmis
            S = newmis.pop()
            R = V - S
            print(s, end=' ') # recursion depth: traces the discovery of MISs
            s += 1
            #Siter = copy.copy(S)
            for v in S: # choose a leaving node
                Sv = S - set([v])
                gammaSv = set() # recompute neighborhood
                for sv in Sv:
                    gammaSv = gammaSv | self.gamma[sv][0]
                #privgammav = (self.gamma[v][0] | set([v])) - gammaSv
                for r in R:   # add a node from outside S
                    Svr = Sv | set([r])
                    gammaSvr = gammaSv | self.gamma[r][0]
                    if gammaSvr & Svr == set(): # if independent
                        if gammaSvr | Svr == V: # and if covering
                            if Svr not in self.newmisset:
                                #print 'new MIS ', Svr
                                newmis = newmis | set([frozenset(Svr)])
                        else:                   # indep. and not covering
                            if Svr not in self.uphistory:
                                #print 'up ->',Svr
                                self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])
                    elif Svr | gammaSvr == V:   # covering but not independent
                        if Svr not in self.downhistory:
                            #print 'down->',Svr
                            self.downmis = self.downmis | set([frozenset(Svr)])


    def computeODistance(self,op2,comments=False):
        """
        renders the squared normalized distance of
        two digraph valuations.

        .. note::

             op2 = digraphs of same order as self.
             
        """
        import math,copy

        op1 = copy.deepcopy(self)

        Debug = False

        if comments:
            print('* --- compute O Distance of two digraphs ---- *')
        ODistance = 0.0
        actionsList1 = [x for x in op1.actions]
        actionsList2 = [x for x in op2.actions]
        if len(actionsList1) != len(actionsList2):
            ODistance = None
            if comments:
                print('actionsList1', actionsList1)
                print('actionsList2', actionsList2)
                print('Error: Actions sets are not comaptible ?')
                print('       ODistance = None !!!')
        else:
            Minop1 = op1.valuationdomain['min']
            Maxop1 = op1.valuationdomain['max']
            Minop2 = op2.valuationdomain['min']
            Maxop2 = op2.valuationdomain['max']
            op1.recodeValuation(-1.0,1.0)
            op2.recodeValuation(-1.0,1.0)
            n = len(actionsList1)
            for i in range(n):
                for j in range(i+1,n):
                    ODistance += math.pow(op1.relation[actionsList1[i]][actionsList1[j]] - op2.relation[actionsList2[i]][actionsList2[j]],2)
                    if Debug:
                        print('==>>', end=' ')
                        print(actionsList1[i],actionsList1[j], 'op1 =', end=' ')
                        print(op1.relation[actionsList1[i]][actionsList1[j]])
                        print(actionsList2[i],actionsList2[j], 'op2 =', end=' ')
                        print(op2.relation[actionsList2[i]][actionsList2[j]])
                        print('ODistance +=', math.pow(op1.relation[actionsList1[i]][actionsList1[j]] - op2.relation[actionsList2[i]][actionsList2[j]],2))
            if comments:
                print('ODistance between',op1.name, ' and')
                print(op2.name, '=', ODistance)
            op1.recodeValuation(Minop1,Maxop1)
            op2.recodeValuation(Minop1,Maxop2)


        return ODistance

    def computeSingletonRanking(self,Comments = False, Debug = False):
        """
        Renders the sorted bipolar net determinatation of outrankingness
        minus outrankedness credibilities of all singleton choices.

        res = ((netdet,singleton,dom,absorb)+)

        """
        import copy

        valuationdomain = copy.deepcopy(self.valuationdomain)

        self.recodeValuation(0.0,100.0)


        sigs = [x[0] for x in self.singletons()]

        res = []
        for i in range(len(sigs)):
            if Debug:
                print(sigs[i], self.domin(sigs[i]) - self.absorb(sigs[i]))
            res.append((self.domin(sigs[i]) - self.absorb(sigs[i]),sigs[i],self.domin(sigs[i]),self.absorb(sigs[i])))

        res.sort(reverse=True)


        if Comments:
            for x in res:
                print("{%s} : %.3f " % ( [y for y in x[1]][0], (float(x[0]) + 100.0)/2.0 ))

        if Debug:
            print(res)

        self.recodeValuation(valuationdomain['min'],valuationdomain['max'])

        return res

    def showSingletonRanking(self,Comments = True, Debug = False):
        """
        Calls self.computeSingletonRanking(comments=True,Debug = False).
        Renders and prints the sorted bipolar net determinatation of outrankingness
        minus outrankedness credibilities of all singleton choices.

        res = ((netdet,sigleton,dom,absorb)+)

        """
        res = self.computeSingletonRanking(Comments,Debug)
        return res

    # def omax(self,L, Debug=False):
    #     """
    #     Epistemic **disjunction** for bipolar outranking characteristics
    #     computation: Med is the valuation domain median and L is a list of
    #     r-valued statement characteristics.

    #     With **positive** arguments, omax operates a **max**,
    #     with **negative** arguments, a **min**.

    #     The mixture of **both positive and negative** arguments results in
    #     an **indeterminate** value.

    #     Likewise to a mean, the *omax* operator is not associative. We therefore first assemble all positive, negative and null terms
    #     and operate omax on the three assembled arguments.
    #     """
    #     Med = self.valuationdomain['med']
    #     terms = list(L)
    #     termsPlus = []
    #     termsMinus = []
    #     termsNuls = []
    #     for i in range(len(terms)):
    #         if terms[i] > Med:
    #             termsPlus.append(terms[i])
    #         elif terms[i] < Med:
    #             termsMinus.append(terms[i])
    #         else:
    #             termsNuls.append(terms[i])
    #     if Debug:
    #         print('terms', terms)
    #         print('termsPlus',termsPlus)
    #         print('termsMinus', termsMinus)
    #         print('termsNuls', termsNuls)
    #     np = len(termsPlus)
    #     nm = len(termsMinus)
    #     if np > 0 and nm == 0:
    #         return max(termsPlus)
    #     elif nm > 0 and np == 0:
    #         return min(termsMinus)
    #     else:
    #         return Med

    # def omin(self,L, Debug=False):
    #     """
    #     Epistemic **conjunction** of a list L of bipolar outranking characteristics.
    #     Med is the given valuation domain median.

    #     With **positive** arguments, omax operates a **min**,
    #     with **negative** arguments, a **max**.

    #     The mixture of both **positive and negative** arguments results
    #     in an **indeterminate** value.

    #     Likewise to a mean, the *omin* operator is not associative. We therefore first assemble all positive, negative and null terms
    #     and operate omin on the three assembled arguments. 

    #     """
    #     Med = self.valuationdomain['med']
    #     terms = list(L)
    #     termsPlus = []
    #     termsMinus = []
    #     termsNuls = []
    #     for i in range(len(terms)):
    #         if terms[i] >= Med:
    #             termsPlus.append(terms[i])
    #         elif terms[i] <= Med:
    #             termsMinus.append(terms[i])
    #         else:
    #             termsNuls.append(terms[i])
    #     if Debug:
    #         print('terms', terms)
    #         print('termsPlus',termsPlus)
    #         print('termsMinus', termsMinus)
    #         print('termsNuls', termsNuls)
    #     np = len(termsPlus)
    #     nm = len(termsMinus)
    #     if np > 0:
    #         if nm > 0:
    #             return Med
    #         else:
    #             return min(termsPlus)
    #     else:
    #         if nm > 0:
    #             return max(termsMinus)
    #         else:
    #             return Med

    def _computeNetFlowsRankingDict(self,Stored=True,Debug=False):
        """
        Tenders an ordered dictionary of the actions (from best to worst)
        following the net flows ranking rule with rank and net flow attributes.
        """
        relation = self.relation
        actions = self.actions
        netFlows = []
        Med = self.valuationdomain['med']
        if Med == Decimal('0'):
            for x,rx in relation.items():
                xnetflows = sum(rx[y] - relation[y][x]\
                                for y in actions.keys())
##                if Debug:
##                    print('netflow for %s = %.2f' % (x, xnetflows))
                netFlows.append((-xnetflows,x))
                # reversed sorting with keeping the actions natural ordering
            
        else:
            Max = self.valuationdomain['max']
            Min = self.valuationdomain['min']
            for x,rx in rleation.items():
                xnetflows = sum(rx[y] + (Max - relation[y][x] + Min)\
                                for y in actions)
##                if Debug:
##                    print('netflow for %s = %.2f' % (x, xnetflows))
                netFlows.append((-xnetflows,x))
                # reversed sorting with keeping the actions natural ordering
        netFlows.sort()
##        if Debug:
##            print(netFlows)

        netFlowsRanking = OrderedDict()
        for k,item in enumerate(netFlows):
            netFlowsRanking[item[1]] = {'rank':k,'netFlow':-item[0]}
        if Stored:
            self.netFlowsRankingDict = netFlowsRanking
        return netFlowsRanking

    def computeNetFlowsRanking(self):
        """
        Renders an ordered list (from best to worst) of the actions
        following the net flows ranking rule.
        """
        try:
            return list(self.netFlowsRankingDict.keys())
        except AttributeError:
            netFlowsRankingDict = self._computeNetFlowsRankingDict()
            return list(netFlowsRankingDict.keys())

    def computeNetFlowsOrder(self):
        """
        Renders an ordered list (from worst to best) of the actions
        following the net flows ranking rule.
        """
        try:
            return list(reversed(list(self.netFlowsRankingDict.keys())))
        except AttributeError:
            netFlowsRankingDict = self._computeNetFlowsRankingDict()
            return list(reversed(list(netFlowsRankingDict.keys())))
        
    def _computeKohlerRankingDict(self,Debug=False):
        """
        Renders a ranking from the best to the worst of the actions following Kohler's rule as an
        ordered dictionary with rank and majorityMargin attributes.
        """
        Max = self.valuationdomain['max']
        actionsList = [x for x in self.actions]
        relation = self.relation
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
        return rank

    def computeKohlerOrder(self):
        """
        Renders an ordering (worst to best) of the actions following Kohler's rule.
        """
        ranking = self._computeKohlerRankingDict()
        res = [x for x in ranking]
        return list(reversed(res))
    
    def computeKohlerRanking(self):
        """
        Renders a ranking (best to worst) of the actions following Kohler's rule.
        """
        ranking = self._computeKohlerRankingDict()
        return [x for x in ranking]

    def _computeArrowRaynaudRankingDict(self,Debug=False):
        """
        Renders a ranking of the actions following Arrow&Raynaud's rule.
        """
        Min = self.valuationdomain['min']
        actionsList = [x for x in self.actions]
        n = len(actionsList)
        relation = self.relation
        rank = OrderedDict()
        k = 1
        while actionsList != []:
            minimax = []
            for x in actionsList:
                xmax = Min
                for y in actionsList:
                    if x != y:
                        if relation[x][y] > xmax:
                            xmax = relation[x][y]
                if Debug:
                    print('x, xmax', x, xmax)
                minimax.append((xmax,x))
            minimax.sort()
            if Debug:
                print(minimax, minimax[0][1])
            rank[minimax[0][1]] = {'rank':n-k+1,'majorityMargin':minimax[0][0]}
            actionsList.remove(minimax[0][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)
        return rank

    def computeArrowRaynaudOrder(self):
        """
        Renders a linear ordering from worst to best of the actions following Arrow&Raynaud's rule.
        """
        ranking = self._computeArrowRaynaudRankingDict()
        return [x for x in ranking]
    
    def computeArrowRaynaudRanking(self):
        """
        renders a linear ranking from best to worst of the actions following Arrow&Raynaud's rule.
        """
        ranking = self._computeArrowRaynaudRankingDict()
        res = [x for x in ranking]
        return list(reversed(res))

    def _computeCopelandRanking(self):
        """
        Renders a linear ranking from best to worst of the actions
        following Copelands's rule.
        """
        c = PolarisedDigraph(self)
        cRelation = c.relation
        actions = self.actions
        incCopelandScores = []
        decCopelandScores = []
        for x in actions:
            copelandScore = Decimal('0')
            for y in actions:
                copelandScore += cRelation[x][y] - cRelation[y][x]
            #actions[x]['score'] = copelandScore
            incCopelandScores.append((copelandScore,x))
            decCopelandScores.append((-copelandScore,x))

        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        incCopelandScores.sort()
        decCopelandScores.sort()
        self.incCopelandScores = incCopelandScores
        self.decCopelandScores = decCopelandScores
##        gamma = self.gamma
##        copelandScores = []
##        for x in self.actions:
##            copelandScore = len(gamma[x][1]) - len(gamma[x][0])
##            copelandScores.append((copelandScore,x))
##        # reversed sorting with keeping the actions initial ordering
##        # in case of ties
##        copelandScores.sort()
        copelandRanking = [x[1] for x in decCopelandScores]
        copelandOrder = [x[1] for x in incCopelandScores]
        self.copelandRanking = copelandRanking
        self.copelandOrder = copelandOrder

    def computeCopelandRanking(self):
        """
        renders a linear ranking from best to worst of the actions following Arrow&Raynaud's rule.
        """
        try:
            ranking = self.copelandRanking
        except:
            self._computeCopelandRanking()
            ranking = self.copelandRanking
        return ranking

    def computeCopelandOrder(self):
        """
        renders a linear ranking from best to worst of the actions following Arrow&Raynaud's rule.
        """
        try:
            ordering = self.copelandOrder
        except:
            self._computeCopelandRanking()
            ordering = self.copelandOrder
        return ordering

##    def _computeRankedPairsOrder(self,Cpp=False,Debug=False):
##        """
##        Renders an actions ordering from the worst to the best obtained from the
##        ranked pairs rule.
##        """
##        relation = self.relation
##        #actions = self.actions
##        actions = [x for x in self.actions]
##        actions.sort()
##
##        n = len(actions)
##
##        listPairs = []
##        for x,rx in relation.items():
##            for y,rxy in rx.items():
##                if x != y:
##                    listPairs.append((rxy,(x,y),x,y))
##        listPairs.sort(reverse=False)
##        if Debug:
##            print(listPairs)
##
##        g = IndeterminateDigraph(order=n)
##        g.actions = self.actions
##        g.valuationdomain = {'min':Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
##        Min = g.valuationdomain['min']
##        Max = g.valuationdomain['max']
##        Med = g.valuationdomain['med']
##        g.relation = {}
##        for x in g.actions:
##            g.relation[x] = {}
##            grx = g.relation[x]
##            for y in g.actions:
##                grx[y] = Med
##
##        rankedPairs = [x[1] for x in listPairs]
##        for pair in rankedPairs:
##            if Debug:
##                print('next pair: ', pair)
##            x = pair[0]
##            y = pair[1]
##            grxy = g.relation[x][y]
##            gryx = g.relation[y][x]
##            if grxy == Min and gryx == Min:
##                grxy = Max
##                g.gamma = g.gammaSets()
##                g.notGamma = g.notGammaSets()
##                if Cpp:
##                    circ = g.computeCppChordlessCircuits()
##                else:
##                    circ = g.computeChordlessCircuits()
##                if len(circ) != 0:
##                    if Debug:
##                        print(circ)
##                    grxy = Min
####                else:
####                    if Debug:
####                        print('added: (%s,%s) characteristic: %.2f' %\
####                              (x,y, self.relation[x][y]))
##
##        g.gamma = g.gammaSets()
##
##        outdegrees = []
##        for x in g.actions:
##            outdegrees.append((len(g.gamma[x][0]),x))
##        outdegrees.sort(reverse=True)
##
##        rankedPairsOrder = []
##        for x in outdegrees:
##            rankedPairsOrder.append(x[1])
##        if Debug:
##            print('Ranked Pairs Order = ', rankedPairsOrder)
##        return rankedPairsOrder
##
##    def _computeRankedPairsRanking(self):
##        """
##        Renders an actions ordering from the best to the worst obtained from the
##        ranked pairs rule.
##        """
##        ordering = self.computeRankedPairsOrder()
##        return list(reversed(ordering))

    def computeKemenyRanking(self,isProbabilistic=False,
                           orderLimit=7, seed=None,
                           sampleSize=1000, Debug=False):
        """
        Renders a ordering from worst to best of the actions with maximal Kemeny index.

        .. note::
        
             Returns a tuple: kemenyRanking (from best to worst), kemenyIndex.
             
        """
        from random import seed, shuffle
        from digraphsTools import all_perms


        Min = self.valuationdomain['min']
        relation = self.relation
        actions = [x for x in self.actions]
        n = len(actions)

        ## Monte Carlo computation of a Kemeny order
        if isProbabilistic:
            if seed != None:
                seed = seed
            a = list(actions)
            kemenyIndex = Decimal(str(n)) * Decimal(str(n)) *Min
            kemenyRanking = list(a)
            sampleSize = sampleSize

            for s in range(sampleSize):
                shuffle(a)
                kcurr = Decimal('0.0')
                kcurr = sum((relation[a[i]][a[j]] - relation[a[j]][a[i]])\
                            for i in range(n) for j in range(i+1,n))
##                for i in range(n):
##                    for j in range(i+1,n):
##                        kcurr += relation[a[i]][a[j]] - relation[a[j]][a[i]]

                if kcurr > kemenyIndex:
                    kemenyIndex = kcurr
                    kemenyRanking = list(a)
                    if Debug:
                        print(s, kemenyIndex)
            if Debug:
                print('Probabilistic Kemeny Ranking = ', kemenyRanking)
                print('Probabilistic Kemeny Index = ', kemenyIndex)
                print('with samplesize :            ', sampleSize)


        ## Exact computation of a Kemeny order
        ## respecting a maximum of marginal majority margins
        else:
            if n > orderLimit:
                return None
            kemenyIndex = Decimal(str(n)) * Decimal(str(n)) * Min
            s = 1
            maximalRankings = []
            for a in all_perms(list(actions)):
                kcurr = Decimal('0.0')
                s += 1
                kcurr = sum((relation[a[i]][a[j]] - relation[a[j]][a[i]])\
                            for i in range(n) for j in range(i+1,n))
##                for i in range(n):
##                    for j in range(i+1,n):
##                        kcurr += relation[a[i]][a[j]] - relation[a[j]][a[i]]
                if Debug:
                    print(s, a, kcurr)
                if kcurr > kemenyIndex:
                    kemenyIndex = kcurr
                    kemenyRanking = list(a)
                    maximalRankings = [kemenyRanking]
                    if Debug:
                        print(maximalRankings)
                elif kcurr == kemenyIndex:
                    maximalRankings.append(list(a))
                    if Debug:
                        print(maximalRankings)
                    
            self.maximalRankings = maximalRankings
            self.kemenyIndex = kemenyIndex
            if Debug:
                print('Exact Kemeny Orders = ', kemenyRanking)
                print('Exact Kemeny Index = ', kemenyIndex)
                print('# of permutations  = ', s)

        #kemenyOrder.reverse()
        return kemenyRanking, kemenyIndex

    def computeKemenyOrder(self,orderLimit=7,Debug=False):
        """
        Renders a ordering from worst to best of the actions with maximal Kemeny index.
        Return a tuple: kemenyOrder (from worst to best), kemenyIndex
        """
        try:
            ranking = list(self.maximalRankings[0])
            ranking.reverse()
        except AttributeError:
            self.computeKemenyRanking(orderLimit=orderLimit,Debug=Debug)
            ranking = list(self.maximalRankings[0])
            ranking.reverse()
        return ranking, self.kemenyIndex

    def computePrincipalOrder(self, plotFileName=None,\
                              Colwise=False, imageType=None,\
                              tempDir=None,\
                              Comments=False, Debug=False):
        """
        Renders a ordered list of self.actions using the decreasing scores from the
        first rincipal eigenvector of the covariance of the valued outdegrees of self.

        .. note::

           The method, relying on writing and reading temporary files by default in a temporary directory is threading and multiprocessing safe !
           (see Digraph.exportPrincipalImage method)

        """
        from csv import reader
        #from operator import itemgetter, attrgetter
        from tempfile import TemporaryDirectory,mkdtemp
##        if tempDir == None:
##            tempDirName = mkdtemp()
##        else:
##            tempDirName = TempDir
        tempd = TemporaryDirectory(dir=tempDir)
        tempDirName = tempd.name
        self.exportPrincipalImage(Colwise=Colwise,Comments=Comments,
                                  Type=imageType,
                                  plotFileName=plotFileName,
                                  TempDir=tempDirName,
                                  )
        if Colwise:
            fi = open('%s/rotationCol.csv' % tempDirName,'r')
        else:
            fi = open('%s/rotationRow.csv' % tempDirName,'r')
            
        csvReader = reader(fi)
        R = [x for x in csvReader]
        listActions = [x for x in self.actions]
        listActions.sort()
        principalScores = [(Decimal(R[i+1][0]),listActions[i])\
                           for i in range(len(listActions))]
        principalScores.sort(reverse=True)
        if Debug:
            print(principalScores)
        else:
            tempd.cleanup()
        return principalScores


    def computeSlaterRanking(self,isProbabilistic=False, seed=None, sampleSize=1000, Debug=False):
        """
        Renders a ranking of the actions with minimal Slater index.
        Return a tuple: slaterOrder, slaterIndex
        """
        from random import seed, shuffle
        try:
            from math import copysign
            CopySign = True
        except:
            CopySign = False
        from digraphsTools import all_perms


        Min = self.valuationdomain['min']
        relationOrig = self.relation
        minOrig = self.valuationdomain['min']
        maxOrig = self.valuationdomain['max']
        self.recodeValuation(-1,1)
        relation = self.relation
        actions = [x for x in self.actions]
        n = len(actions)

        ## Monte Carlo computation of a Slater order
        if isProbabilistic:
            if seed != None:
                seed = seed
            a = list(actions)
            slaterIndex = -(n*n)
            slaterRanking = list(a)
            sampleSize = sampleSize

            for s in range(sampleSize):
                shuffle(a)
                kcurr = 0
                for i in range(n):
                    for j in range(i+1,n):
                        if CopySign:
                            kcurr += copysign(1,relation[a[i]][a[j]]) - copysign(1,relation[a[j]][a[i]])
                        else:
                            if relation[a[i]][a[j]] > 0:
                                kcurr += 1
                            elif relation[a[i]][a[j]] < 0:
                                kcurr -= 1
                            if relation[a[j]][a[i]] > 0:
                                kcurr -= 1
                            elif relation[a[j]][a[i]] < 0:
                                kcurr += 1

                if kcurr > slaterIndex:
                    slaterIndex = kcurr
                    slaterRanking = list(a)
                    if Debug:
                        print(s, slaterIndex)
            if Debug:
                print('Probabilistic Slater Order = ', slaterRanking)
                print('Probabilistic Slater Index = ', slaterIndex)
                print('with samplesize :            ', sampleSize)


## Exact computation of a Slater order
## respecting a maximum of marginal majority margins
        else:

            slaterIndex = -(n*n)
            slaterOrder = list(actions)
            s = 0
            for a in all_perms(slaterOrder):
                kcurr = 0
                s += 1
                for i in range(n):
                    ai = a[i]
                    rai = relation[a[i]]
                    for j in range(i+1,n):
                        aj = a[j]
                        if CopySign:
                            kcurr += copysign(1,rai[aj]) -\
                                     copysign(1,relation[aj][ai])
                        else:
                            if rai[aj] > 0:
                                kcurr += 1
                            elif rai[aj] < 0:
                                kcurr -= 1
                            if relation[aj][ai] > 0:
                                kcurr -= 1
                            elif relation[aj][ai] < 0:
                                kcurr += 1
                        #kcurr += copysign(1,relation[a[i]][a[j]]) - copysign(1,relation[a[j]][a[i]])
                if Debug:
                    print(s, a, kcurr)
                if kcurr >= slaterIndex:
                    slaterIndex = kcurr
                    slaterRanking = list(a)
                    if Debug:
                        print(s, slaterRanking, slaterIndex)
            if Debug:
                print('Exact Slater Order = ', slaterRanking)
                print('Exact Slater Index = ', slaterIndex)
                print('# of permutations  = ', s)

        self.recodeValuation(minOrig,maxOrig)
        return slaterRanking, slaterIndex

    def computeSlaterOrder(self,isProbabilistic=False, seed=None, sampleSize=1000, Debug=False):
        """
        Reversed return from computeSlaterRanking method.
        """
        slaterOrder,slaterIndex = self.computeSlaterRanking(isProbabilistic=isProbabilistic,
                                                          seed=seed, sampleSize=sampleSize, Debug=Debug)
        slaterOrder.reverse()
        return slaterOrder,slaterIndex

    def computePairwiseClusterComparison(self, K1, K2, Debug=False):
        """
        Computes the pairwise cluster comparison credibility vector
        from bipolar-valued digraph g. with K1 and K2 disjoint
        lists of action keys from g actions disctionary.
        Returns the dictionary
        {'I': Decimal(),'P+':Decimal(),'P-':Decimal(),'R' :Decimal()}
        where one and only one item is strictly positive.
        """
        from decimal import Decimal
        relation = self.relation
        n = Decimal(str(len(K1)*len(K2)))
        if Debug:
            print('K1 = ', K1, ', K2 = ', K2, ', n = ', n)

        rK1SK2 = Decimal('0')
        rK2SK1 = Decimal('0')
        for x in K1:
            rx = relation[x]
            for y in K2:
                rK1SK2 += rx[y]
                rK2SK1 += relation[y][x]

        if Debug:
            print('r(K1 >= K2) = ', rK1SK2/n, ' r(K2 >= K1) = ', rK2SK1/n)

        rK1IK2 = min(rK1SK2,rK2SK1)/n
        rK1PK2 = min(rK1SK2,-rK2SK1)/n
        rK2PK1 = min(-rK1SK2,rK2SK1)/n
        rK1RK2 = min(-rK1SK2,-rK2SK1)/n

        if Debug:
            print('r(K1 = K2) = %.2f' % rK1IK2)
            print('r(K1 > K2) = %.2f' % rK1PK2)
            print('r(K1 < K2) = %.2f' % rK2PK1)
            print('r(K1 ? K2) = %.2f' % rK1RK2)

        return {'I': rK1IK2, 'P+': rK1PK2, 'P-' :rK2PK1, 'R' :  rK1RK2 }

# ------ CoverDigraph construction

class CoDualDigraph(Digraph):
    """
    Instantiates the associated codual -converse of the negation- from a deep copy of
    a given Digraph instance called *other*.

    .. note::

         Instantiates *self* as other.__class__ !
         And, deepcopies, the case given, the other.description, the other.criteria
         and the other.evaluation dictionaries into self.
    """

    def __init__(self,other,Debug=False):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'codual-'+other.name
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('relation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        relation = {}
        for x in self.actions:
            relation[x] = {}
            rx = relation[x]
            for y in self.actions:
                rx[y] = Max - other.relation[y][x] + Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


# ------ Cover construction

class CoverDigraph(Digraph):
    """
    Instantiates the associated cover relation -immediate neighbours- from
    a deep copy of a given Digraph called *other*. The Hasse diagram for instance is the cover
    relation of a transitive digraph.

    .. note::
    
        Instantiates as other.__class__ !
        Copies the case given the other.description, the other.criteria
        and the other.evaluation dictionaries into self.
        
    """

    def __init__(self,other, Debug=False):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'cover-'+other.name
        self.name = 'codual-'+other.name
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('relation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        # try:
        #     self.description = deepcopy(other.description)
        # except AttributeError:
        #     pass
        # try:
        #     self.criteria = deepcopy(other.criteria)
        # except AttributeError:
        #     pass
        # try:
        #     self.evaluation = deepcopy(other.evaluation)
        # except AttributeError:
        #     pass
        # self.actions = deepcopy(other.actions)
        # self.order = len(self.actions)
        # self.valuationdomain = deepcopy(other.valuationdomain)
        #actionsList = list(self.actions)
        #Max = Decimal('2')*other.valuationdomain['max']
        #Med = Decimal('0')
        #Min = -Max
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        relation = {}
        for x in self.actions:
            relation[x] = {}
            rx = relation[x]
            orx = other.relation[x]
            for y in self.actions:
                ory = other.relation[y]
                if y == x:
                    rx[y] = Med
                else:
                    coverXY = Max
                    for z in self.actions:
                        if z != x and z != y:
                            coverz = max(orx[z],(Max-ory[z]+Min))
                            coverXY = min(coverXY,coverz)
##                            if Debug:
##                                print(x,y,z,other.relation[x][z],(Max-other.relation[y][z]+Min),coverz,coverXY)
                    rx[y] = min(orx[y],coverXY)
        self.relation = relation
        #self.recodeValuation(other.valuationdomain['min'],other.valuationdomain['max'])
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# ------ Converse construction

class ConverseDigraph(Digraph):
    """
    Instantiates the associated converse or reciprocal version from
    a deep copy of a given Digraph called other.

    Instantiates as other.__class__ !

    Deep copies, the case given, the description, the criteria
    and the evaluation dictionaries into self.
    """

    def __init__(self,other):
        from copy import deepcopy
        self.__class__ = other.__class__
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('relation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        self.name = 'converse-'+other.name
        relation = {}
        for x in self.actions:
            relation[x] = {}
            rx = relation[x]
            for y in self.actions:
                rx[y] = other.relation[y][x]
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class FusionDigraph(Digraph):
    """
    Instantiates the epistemic disjunctive (default) or conjunctive fusion of 
    two given Digraph instances called dg1 and dg2.

    Parameter:

        * operator = "o-max (default)" | "o-min" : epistemic disjunctive, resp. conjunctive fusion operator.
    """

    def __init__(self,dg1,dg2,operator="o-max"):
        from copy import deepcopy
        from digraphsTools import omin, omax
        self.name = 'fusion-'+dg1.name+'-'+dg2.name
        self.actions = deepcopy(dg1.actions)
        self.order = len(dg1.actions)
        self.valuationdomain = deepcopy(dg1.valuationdomain)
        #actionsList = list(self.actions)
        #max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        fusionRelation = {}
        for x in self.actions:
            fusionRelation[x] = {}
            fx = fusionRelation[x]
            dg1x = dg1.relation[x]
            dg2x = dg2.relation[x]
            for y in self.actions:
                if operator == "o-min":
                    fx[y] = omin(Med,(dg1x[y],dg2x[y]))
                elif operator == "o-max":
                    fx[y] = omax(Med,(dg1x[y],dg2x[y]))
                else:
                    print('Error: invalid epistemic fusion operator %s' % operator)
        self.relation = fusionRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class FusionLDigraph(Digraph):
    """
    Instantiates the epistemic fusion a list L of Digraph instances.

    Parameter:

        * operator = "o-max" (default) | "o-min" : epistemic disjunctive or conjunctive fusion)
    """

    def __init__(self,L,operator="o-max"):
        from copy import deepcopy
        self.name = 'fusion-'+L[0].name
        self.actions = deepcopy(L[0].actions)
        self.order = len(L[0].actions)
        self.valuationdomain = deepcopy(L[0].valuationdomain)
        #actionsList = list(self.actions)
        #Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        fusionRelation = {}
        for x in self.actions:
            fusionRelation[x] = {}
            fx = fusionRelation[x]
            #gx = g.relation[x]
            for y in self.actions:
                args = [g.relation[x][y] for g in L]
                if operator == "o-min":
                    fx[y] = omin(Med,args)
                elif operator == "o-max":
                    fx[y] = omax(Med,args)
                else:
                    print('Error: invalid epistemic fusion operator %s' % operator)
        self.relation = fusionRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# -------- Graph Border and Inner

class GraphBorder(Digraph):
    """
    Instantiates the partial digraph induced by its border,
    i.e. be the union of its initial and terminal kernels.
    """
    def __init__(self,other,Debug=False):
        from copy import deepcopy
        if Debug:
            Digraph.exportGraphViz(other,other.name)

        self.__dict__ = deepcopy(other.__dict__)
        
        other.computePreKernels()
        if Debug:
            print('other.domprekernsls', other.dompreKernels)
        domBorderActions = set()
        for k in other.dompreKernels:    
            domBorderActions |= k
        if Debug:
            print('other.absprekernels',other.abspreKernels)
        absBorderActions = set()
        for k in other.abspreKernels:    
            absBorderActions |= k

        borderActions = domBorderActions | absBorderActions
        if Debug:
            print('border actions', borderActions)

        self.name = other.name + '_border'

        borderRelation = {}
        for x in self.actions:
            borderRelation[x] = {}
            #innerRelation[x] = {}
            for y in self.actions:
                if x in borderActions or y in borderActions:
                    borderRelation[x][y] = self.relation[x][y]
                else:
                    borderRelation[x][y] = self.valuationdomain['med']                                                            

        self.relation = borderRelation
        if Debug:
            Digraph.exportGraphViz(self,'border',bestChoice=domBorderActions,worstChoice=absBorderActions)


class GraphInner(Digraph):
    """
    Instantiates the partial digraph induced by the complement of its border,
    i.e. the nodes not included in the union of its initial and terminal kernels.
    """
    def __init__(self,other,Debug=False):
        from copy import deepcopy
        if Debug:
            Digraph.exportGraphViz(other,other.name)

        self.__dict__ = deepcopy(other.__dict__)

        other.computePreKernels()
        if Debug:
            print('other.domprekernsls', other.dompreKernels)
        domBorderActions = set()
        for k in other.dompreKernels:    
            domBorderActions |= k
        if Debug:
            print('other.absprekernels',other.abspreKernels)
        absBorderActions = set()
        for k in other.abspreKernels:    
            absBorderActions |= k

        borderActions = domBorderActions | absBorderActions
        if Debug:
            print('border actions', borderActions)

        self.name = other.name + '_inner'
        innerRelation = {}
        for x in self.actions:
            innerRelation[x] = {}
            for y in self.actions:
                if x in borderActions or y in borderActions:
                    innerRelation[x][y] = self.valuationdomain['med']
                else:
                    innerRelation[x][y] = self.relation[x][y]
                                                            

        self.relation = innerRelation
        if Debug:
            Digraph.exportGraphViz(self,'inner',bestChoice=domBorderActions,worstChoice=absBorderActions)


# ------ Preorder construction

class _Preorder(Digraph):
    """
    Instantiates the associated preorder from
    a given Digraph called other.

    Instantiates as other.__class__ !

    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other,direction="best",ranking=None):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'preorder-'+other.name
        self.name = 'codual-'+other.name
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('relation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        # try:
        #     self.description = deepcopy(other.description)
        # except AttributeError:
        #     pass
        # try:
        #     self.criteria = deepcopy(other.criteria)
        # except AttributeError:
        #     pass
        # try:
        #     self.evaluation = deepcopy(other.evaluation)
        # except AttributeError:
        #     pass
        # self.actions = deepcopy(other.actions)
        # self.order = len(self.actions)
        # self.valuationdomain = deepcopy(other.valuationdomain)
        actionsList = [x for x in self.actions]
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        relation = {}
        for x in self.actions:
            relation[x] = {}
            rx = relation[x]
            for y in self.actions:
                rx[y] = None
        
        if ranking == None:
            if direction == 'best':
                rank = other._bestRanks()
            else:
                rank = other._worstRanks()
        else:
            rank = ranking

        for i in range(self.order):
            x = actionsList[i]
            for j in range(i, self.order):
                y = actionsList[j]
                if rank[x] < rank[y]:
                    relation[x][y] = Max
                    relation[y][x] = Min
                elif rank[x] > rank[y]:
                    relation[x][y] = Min
                    relation[y][x] = Max
                else:
                    relation[x][y] = Max
                    relation[y][x] = Max

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# ------- XOR construction

class XORDigraph(Digraph):
    """
    Instantiates the XOR digraph of two bipolar
    digraphs d1 and d2 of same order.
    """

    def __init__(self,d1,d2,Debug = False):
        from copy import deepcopy
        self.name = 'XORDigraph'
        if d1.order != d2.order:
            if Debug:
                print("XORDigraph init ERROR:\n the input digraphs are not of the same order !")
            return None
        self.order = d1.order
        self.actions = deepcopy(d1.actions)
        #actions = [x for x in self.actions]
        Mind1 = d1.valuationdomain['min']
        Maxd1 = d1.valuationdomain['max']
        Mind2 = d2.valuationdomain['min']
        Maxd2 = d2.valuationdomain['max']
        if (Mind1 != Mind2) or (Maxd1 != Maxd2):
            if Debug:
                print('!!! valuation recoding required !!!')
                print(d1.name,d1.valuationdomain)
                print(d2.name,d2.valuationdomain)
            d1.recodeValuation(-1.0,1.0)
            d2.recodeValuation(-1.0,1.0)
            Recoded = True
        else:
            Recoded = False
        xorRelation = {}
        for x in self.actions:
            xorRelation[x] = {}
            xorx = xorRelation[x]
            d1x = d1.relation[x]
            d2x = d2.relation[x]
            for y in self.actions:
                xorx[y] = max( min(d1x[y],-d2x[y]), min(d2x[y],-d1x[y]) )
##                if Debug:
##                    print(x,y,d1.relation[x][y],d2.relation[x][y],xorRelation[x][y])

        self.relation = xorRelation
        if Recoded:
            self.valuationdomain = {'min': Decimal("-1.0"),
                                    'med': Decimal("0.0"),
                                    'max': Decimal("1.0")}
            d1.recodeValuation(Mind1,Maxd1)
            d2.recodeValuation(Mind2,Maxd2)
        else:
            self.valuationdomain = dict(d1.valuationdomain.items())
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class EquivalenceDigraph(Digraph):
    """
    Instantiates the logical equivalence digraph of two bipolar
    digraphs d1 and d2 of same order. Returns None if d1 and d2 are of different order
    """

    def __init__(self,d1,d2,Debug = False):
        from copy import deepcopy
        self.name = 'EquivDigraph'
        if d1.order != d2.order:
            print("EquivDigraph init ERROR:\n the input digraphs are not of the same order !")
            return None

        self.order = d1.order
        self.actions = deepcopy(d1.actions)
        #actions = [x for x in self.actions]

        Mind1 = d1.valuationdomain['min']
        Maxd1 = d1.valuationdomain['max']
        Mind2 = d2.valuationdomain['min']
        Maxd2 = d2.valuationdomain['max']
        if (Mind1 != Decimal("-1.0")) or (Maxd1 != Decimal("1.0")):
            if Debug:
                print('!!! d1 valuation recoding required !!!')
                print(d1.name,d1.valuationdomain)
            d1.recodeValuation(-1.0,1.0)
            RecodedD1 = True
        else:
            RecodedD1 = False
         
        if (Mind2 != Decimal("-1.0")) or (Maxd2 != Decimal("1.0")):
            if Debug:
                print('!!! d2 valuation recoding required !!!')
                print(d2.name,d2.valuationdomain)
            d2.recodeValuation(-1.0,1.0)
            RecodedD2 = True
        else:
            RecodedD2 = False

        equivRelation = {}
        for x in self.actions:
            equivRelation[x] = {}
            eqvx = equivRelation[x]
            d1x = d1.relation[x]
            d2x = d2.relation[x]
            for y in self.actions:
                eqvx[y] = min( max(-d1x[y],d2x[y]), max(-d2x[y],d1x[y]) )
##                if Debug:
##                    print(x,y,d1.relation[x][y],d2.relation[x][y],equivRelation[x][y])

        self.relation = equivRelation
        self.valuationdomain = {'min': Decimal("-1.0"),
                                'med': Decimal("0.0"),
                                'max': Decimal("1.0")}

        if RecodedD1:
            d1.recodeValuation(Mind1,Maxd1)
        if RecodedD2:
            d2.recodeValuation(Mind2,Maxd2)

        self.correlation = self.computeCorrelation()      
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeCorrelation(self):
        """
        Renders the global bipolar correlation index resulting from the pairwise
        equivalence valuations.
        """
        corr = Decimal('0')
        dterm = Decimal('0')
        #actions = [x for x in self.actions]
        #actions = self.actions
        relation = self.relation
        for x,rx in relation.items():
            for y,rxy in rx.items():
                if x != y:
                    corr += rxy
                    dterm += abs(rxy)
        n = self.order * (self.order-1)
        return {'correlation': float(corr)/float(dterm),
                'determination': float(dterm)/float(n)}


# ------- Specialisations of the Digraph class -----------


#class RandomDigraph(randomDigraphs.RandomDigraph):
#    """
#    dummy
#    """
class _RandomDigraph(Digraph):
    """
    .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomDigraph` constructor. 

     """

    def __init__(self,order=9,arcProbability=0.5,hasIntegerValuation=True, Bipolar=False):
        arcProbability = Decimal(str(arcProbability))
        if arcProbability > Decimal("1.0"):
            print('Error: arc probability too high !!')
        elif arcProbability < Decimal("0.0"):
            print('Error: arc probability too low !!')
        else:
            import copy
            from random import random
            g = EmptyDigraph(order=order, valuationdomain=(0.0,1.0))
            self.actions = copy.copy(g.actions)
            self.valuationdomain = copy.copy(g.valuationdomain)
            self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
            self.relation = {}
            for x in g.actions:
                self.relation[x] = {}
                for y in g.actions:
                    if x == y:
                        self.relation[x][y] = self.valuationdomain['min']
                    else:
                        if random() <= arcProbability:
                            self.relation[x][y] = self.valuationdomain['max']
                        else:
                            self.relation[x][y] = self.valuationdomain['min']
            self.order = order
            self.name = 'randomDigraph'
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()

#class RandomValuationDigraph(randomDigraphs.RandomValuationDigraph):
#    """
#    dummy
#    """
    
class _RandomValuationDigraph(Digraph):
    """
    .. warning::
    
       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomValuationDigraph` constructor. 

    """

    def __init__(self,order=9, ndigits=2, Normalized=False, hasIntegerValuation=False):
        import random
        self.name = 'randomValuationDigraph'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        precision = pow(10,ndigits)
        if hasIntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            if Normalized:
                 self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            else:
                self.valuationdomain = {'min':Decimal('0'), 'med':Decimal('0.5'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        random.seed()
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                if x == y:
                    relation[x][y] = self.valuationdomain['med']
                else:
                    if hasIntegerValuation:
                        relation[x][y] = (2*random.randrange(start=0,stop=precision)) - precision
                    elif Normalized:
                        relation[x][y] = (Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits))) * Decimal('2.0')) - Decimal('1.0')
                    else:
                        relation[x][y] = Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits)))
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class _RandomWeakTournament(Digraph):
    """
    .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomWeakTournament` constructor. 

    """

    def __init__(self,order=10,ndigits=2,hasIntegerValuation=False,weaknessDegree=0.25,Comments=False):
        import random
        from decimal import Decimal

        self.name = 'randomWeakTournament'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        random.seed()
        Max = pow(10,ndigits)
        Min = - Max
        Med = 0
        precision = Max
        dPrecision = Decimal(str(precision))
        if hasIntegerValuation:
            self.valuationdomain = {'hasIntegerValuation':True, 'min':Decimal(str(Min)), 'med':Decimal('0'), 'max':Decimal(str(Max))}
        else:
            self.valuationdomain = {'hasIntegerValuation':False, 'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = self.valuationdomain['med']

        actionsList = [x for x in actions]
        random.shuffle(actionsList)
        weaknessDegree = Decimal(str(weaknessDegree))
        forwardDegree = (Decimal('1.0') - weaknessDegree)/Decimal('2')

        #print actionsList
        n = len(actionsList)
        for i in range(n):
            for j in range(i,n):
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    relation[actionsList[i]][actionsList[j]] = self.valuationdomain['med']
                else:
                    u = Decimal(str(random.randint(0,precision)))/dPrecision
                    u1 = Decimal(str(random.randint(0,precision)))
                    u2 = Decimal(str(random.randint(0,precision)))

                    if u < weaknessDegree: # i = j
                        if hasIntegerValuation:
                            randeval1 = u1
                            randeval2 = u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = u2/dPrecision

                    elif u < forwardDegree: # i > j
                        if hasIntegerValuation:
                            randeval1 = u1
                            randeval2 = Min + u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = (Min + u2)/dPrecision

                    else: # j > i
                        if hasIntegerValuation:
                            randeval1 = Min + u1
                            randeval2 = u2
                        else:
                            randeval1 = (Min + u1)/dPrecision
                            randeval2 = u2/dPrecision

                    if hasIntegerValuation:
                        relation[actionsList[i]][actionsList[j]] = Decimal(str(randeval1))
                        relation[actionsList[j]][actionsList[i]] = Decimal(str(randeval2))
                    else:
                        relation[actionsList[i]][actionsList[j]] = Decimal(str(round(randeval1,ndigits)))
                        relation[actionsList[j]][actionsList[i]] = Decimal(str(round(randeval2,ndigits)))


        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

        if Comments:
             print(self.order*(self.order-1), self.computeRelationalStructure())


class _RandomTournament(Digraph):
    """
   .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomTournament` constructor. 

    """

    def __init__(self,order=10,ndigits=2,isCrisp=True,valuationDomain=None):
        import random
        from decimal import Decimal

        self.name = 'randomTournament'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        if valuationDomain == None:
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        else:
            self.valuationdomain = valuationDomain
        valuationRange = self.valuationdomain['max'] - self.valuationdomain['min']
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Decimal('0.0')
        random.seed()
        precision = pow(10,ndigits)
        actionsList = [x for x in actions]
        #print actionsList
        n = len(actionsList)
        for i in range(n):
            for j in range(i,n):
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    relation[actionsList[i]][actionsList[j]] = self.valuationdomain['med']
                else:
                    u = random.randint(0,precision)
                    if isCrisp:
                        if u < Decimal(str(precision))/Decimal('2'):
                            relation[actionsList[i]][actionsList[j]] = self.valuationdomain['min']
                            relation[actionsList[j]][actionsList[i]] = self.valuationdomain['max']
                        else:
                            relation[actionsList[i]][actionsList[j]] = self.valuationdomain['max']
                            relation[actionsList[j]][actionsList[i]] = self.valuationdomain['min']
                    else:
                        randeval = self.valuationdomain['min'] + Decimal(str(u))/Decimal(str(precision))*valuationRange
                        valuation = Decimal(str(round(randeval,ndigits)))
                        relation[actionsList[i]][actionsList[j]] = valuation
                        relation[actionsList[j]][actionsList[i]] = self.valuationdomain['max'] - valuation + self.valuationdomain['min']

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class _RandomFixedSizeDigraph(Digraph):
    """
    .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomFixedSizeDigraph` constructor. 

    """
    def __init__(self,order=7,size=14):
        import random,copy
        # check feasability
        r = (order * order) - order
        if size > r :
            print('Graph not feasable (1) !!')
        else:
            self.name = 'randomFixedSize'
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = []
            for x in actionlist:
                actions.append(str(x))
            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            Min = self.valuationdomain['min']
            Max = self.valuationdomain['max']
            random.seed()
            allarcs = []
            relation = {}
            for x in actions:
                relation[x] = {}
                for y in actions:
                    relation[x][y] = Min
                    if x != y:
                        allarcs.append((x,y))
            for i in range(size):
                arc = random.choice(allarcs)
                relation[arc[0]][arc[1]] = Max
                allarcs.remove(arc)
            self.relation = relation.copy()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()

class _RandomFixedDegreeSequenceDigraph(Digraph):
    """
    .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomFixedDegreeSequenceDigraph` constructor. 

    """
    def __init__(self,order=7,degreeSequence=[3,3,2,2,1,1,0]):
        import random,copy
        # check feasability
        degree = max(degreeSequence)
        if degree >= order:
            print('!!! Graph not feasable (1) !!!')
            print('Maximum degree > order !!!')
        else:
            sumdegrees = 0
            for i in range(order):
                sumdegrees += degreeSequence[i]
            r = sumdegrees % 2
            if r == 1:
                print('!!! Graph not feasable (1) !!!')
                print('Odd sum of degrees : ',sumdegrees,'!!')
            else:
                self.name = 'randomFixedDegreeSequence'
                self.order = order
                actionlist = list(range(order+1))
                actionlist.remove(0)
                actions = []
                for x in actionlist:
                    actions.append(str(x))
                self.actions = actions
                self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
                Min = self.valuationdomain['min']
                Max = self.valuationdomain['max']
                relation = {}
                for x in actions:
                    relation[x] = {}
                    for y in actions:
                        relation[x][y] = Min
                random.seed()
                # create a random pairing
                feasable = 0
                s = 0
                while feasable == 0 and s < 100:
                    s += 1
                    edges = []
                    cells = []
                    degreeseq = {}
                    i = 0
                    for x in actions:
                        degreeseq[x] = degreeSequence[i]
                        cells.append((x,degree))
                        i += 1
                    while len(cells) > 1:
                        cell = random.choice(cells)
                        cells.remove(cell)
                        xc = cell[0]
                        edgescur = []
                        copycells = copy.copy(cells)
                        while degreeseq[xc] > 0 and len(copycells) > 0:
                            other = random.choice(copycells)
                            copycells.remove(other)
                            edgescur.append((xc,other[0]))
                            degreeseq[other[0]] -= 1
                            degreeseq[xc] -= 1
                        edges += edgescur
                        for c in cells:
                            if degreeseq[c[0]] == 0:
                                cells.remove(c)
                    feasable = 1
                    for x in actions:
                        if degreeseq[x] != 0:
                            feasable = 0
                            break
                if feasable == 0:
                    print('Graph not feasable (2) !!')
                else:
                    for edge in edges:
                        relation[edge[0]][edge[1]] = Max
                        relation[edge[1]][edge[0]] = Max
                    self.relation = relation.copy()
                    self.gamma = self.gammaSets()

# class RandomTree(Digraph):
#     """
#     .. warning::

#        *Obsolete version!* Will be removed in the future. Instead, use
#        the new :py:class:`graphs.RandomTree` constructor. 

#     """
#     def __init__(self,numberOfNodes=5, ndigits=2, hasIntegerValuation=True):
#         from random import choice
#         from decimal import Decimal
#         self.name = 'randomTree'
#         self.order = numberOfNodes
#         actions = {}
#         nodes = [str(x+1) for x in range(numberOfNodes)]
#         for x in nodes:
#             actions[x] = {'name': 'node %s' % x}
#         self.actions = actions
#         print(actions)
#         precision = pow(10,ndigits)
#         if hasIntegerValuation:
#             self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
#         else:
#             self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
#         self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
#         # init relation dictionary
#         relation = {}
#         nodeKeys = [x for x in actions]
#         print(nodeKeys)
#         for x in nodeKeys:
#             relation[x] = {}
#             for y in nodeKeys:
#                 relation[x][y] = self.valuationdomain['min']
#         nodes = [x for x in range(len(nodeKeys))]
#         pruefer = []
#         for i in range(len(nodeKeys)-2):
#             pruefer.append(choice(nodes))
#         print(pruefer)
#         pairs = self.prufer_to_tree(pruefer)
#         for (i,j) in pairs:
#             relation[str(i+1)][str(j+1)] = Decimal('1.0')
#             relation[str(j+1)][str(i+1)] = Decimal('1.0')
#         self.relation = relation
#         self.gamma = self.gammaSets()
#         self.notGamma = self.notGammaSets()

#     def prufer_to_tree(self,a):
#         tree = []
#         T = list(range(0, len(a)+2))
#         print(T)
#         # the degree of each node is how many times it appears
#         # in the sequence
#         deg = [1]*len(T)
#         print(deg)
#         for i in a: deg[i] += 1

#         # for each node label i in a, find the first node j with degree 1 and add
#         # the edge (j, i) to the tree
#         for i in a:
#             for j in T:
#                 if deg[j] == 1:
#                     tree.append((i,j))
#                     # decrement the degrees of i and j
#                     deg[i] -= 1
#                     deg[j] -= 1
#                     break

#         last = [x for x in T if deg[x] == 1]
#         tree.append((last[0],last[1]))

#         return tree


class _RandomRegularDigraph(Digraph):
    """
    .. warning::

       *Obsolete version!* Will be removed in the future. Instead, use
       the new :py:class:`randomDigraphs.RandomRegularDigraph` constructor. 


    """
    def __init__(self,order=7,degree=2):
        import random,copy
        # check feasability
        r = (order * degree) % 2
        if degree >= order or r == 1:
            print('Graph not feasable (1) !!')
        else:
            self.name = 'randomRegular'
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = []
            for x in actionlist:
                actions.append(str(x))
            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            random.seed()
            # create a random pairing
            feasable = 0
            s = 0
            while feasable == 0 and s < 100:
                s += 1
                edges = []
                cells = []
                degreeseq = {}
                for x in actions:
                    degreeseq[x] = degree
                    cells.append((x,degree))
                while len(cells) > 1:
                    cell = random.choice(cells)
                    cells.remove(cell)
                    xc = cell[0]
                    edgescur = []
                    copycells = copy.copy(cells)
                    while degreeseq[xc] > 0 and len(copycells) > 0:
                        other = random.choice(copycells)
                        copycells.remove(other)
                        edgescur.append((xc,other[0]))
                        degreeseq[other[0]] -= 1
                        degreeseq[xc] -= 1
                    edges += edgescur
                    for c in cells:
                        if degreeseq[c[0]] == 0:
                            cells.remove(c)
                feasable = 1
                for x in actions:
                    if degreeseq[x] != 0:
                        feasable = 0
                        break
            if feasable == 0:
                print('Graph not feasable (2) !!')
            else:
                relation = {}
                for x in actions:
                    relation[x] = {}
                    for y in actions:
                        relation[x][y] = self.valuationdomain['min']
                for edge in edges:
                    relation[edge[0]][edge[1]] = Decimal('1.0')
                    relation[edge[1]][edge[0]] = Decimal('1.0')
                self.relation = relation.copy()
                self.gamma = self.gammaSets()
                self.notGamma = self.notGammaSets()
                self.componentslist = self.components()

class EmptyDigraph(Digraph):
    """
    Parameters:
        order > 0 (default=5); valuationdomain =(Min,Max).

    Specialization of the general Digraph class for generating
    temporary empty graphs of given order in {-1,0,1}.

    """
    def __init__(self,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        from collections import OrderedDict
        self.name = 'empty'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = OrderedDict()
        for x in actionlist:
            actions[str(x)] = {'name':str(x)}
        self.actions = actions
        Min = Decimal(str((valuationdomain[0])))
        Max = Decimal(str((valuationdomain[1])))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class IndeterminateDigraph(Digraph):
    """
    Parameters: order > 0; valuationdomain =(Min,Max).
    Specialization of the general Digraph class for generating
    temporary empty graphs of order 5 in {-1,0,1}.
    """
    def __init__(self,other=None,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        from collections import OrderedDict
        self.name = 'indeterminate'
        if other == None:
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = OrderedDict()
            for x in actionlist:
                actions[str(x)] = {'name':str(x)}

            Min = Decimal(str(valuationdomain[0]))
            Max = Decimal(str(valuationdomain[1]))
            Med = (Max + Min)/Decimal('2')
            self.valuationdomain = {'min':Min,'med':Med,'max':Max}

        else:
            self.__class__ = other.__class__
            self.order = other.order
            actions = other.actions
            self.valuationdomain = dict(other.valuationdomain.items())
            Med = self.valuationdomain['med']

        self.actions = actions

        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class CirculantDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary circulant digraphs.

    Parameters:
        | order > 0;
        | valuationdomain ={'min':m, 'max':M};
        | circulant connections = list of positive
               and/or negative circular shifts of value 1 to n.

    Default instantiation C_7:
        | order = 7,
        | valuationdomain = {'min':-1.0,'max':1.0},
        | circulants = [-1,1].

    Example session::

        >>> from digraphs import CirculantDigraph
        >>> c8 = CirculantDigraph(order=8,circulants=[1,3])
        >>> c8.exportGraphViz('c8')
        *---- exporting a dot file dor GraphViz tools ---------*
        Exporting to c8.dot
        circo -Tpng c8.dot -o c8.png
        # see below the graphviz drawing
        >>> c8.showChordlessCircuits()
        No circuits yet computed. Run computeChordlessCircuits()!
        >>> c8.computeChordlessCircuits()
        ...
        >>> c8.showChordlessCircuits()
        *---- Chordless circuits ----*
        ['1', '4', '7', '8'] , credibility : 1.0
        ['1', '4', '5', '6'] , credibility : 1.0
        ['1', '4', '5', '8'] , credibility : 1.0
        ['1', '2', '3', '6'] , credibility : 1.0
        ['1', '2', '5', '6'] , credibility : 1.0
        ['1', '2', '5', '8'] , credibility : 1.0
        ['2', '3', '6', '7'] , credibility : 1.0
        ['2', '3', '4', '7'] , credibility : 1.0
        ['2', '5', '6', '7'] , credibility : 1.0
        ['3', '6', '7', '8'] , credibility : 1.0
        ['3', '4', '7', '8'] , credibility : 1.0
        ['3', '4', '5', '8'] , credibility : 1.0
        12 circuits.
        >>>
        
    .. image:: c8.png
        :alt: circulant [1,3] digraph
        :width: 300 px
        :align: center

    """
    def __init__(self,order=7,valuationdomain = {'min':Decimal('-1.0'),'max':Decimal('1.0')},\
                 circulants = [-1,1],IndeterminateInnerPart=False):
        import sys,array,copy
        from collections import OrderedDict
        self.name = 'c'+str(order)
        self.order = order
        self.circulants = circulants
        actionlist = list(range(1,order+1))
        actions = OrderedDict()
        for x in actionlist:
            actions[str(x)] = {'name': str(x)}
        self.actions = actions
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        arcs = [] # circulant arcs
        for x in actionlist:
            for y in circulants:
                r = (x + y) % order
                if r == 0:
                    arcs.append((str(x), str(order)))
                else:
                    arcs.append((str(x), str(r)))
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if IndeterminateInnerPart:
                    relation[x][y] = Med
                else:
                    relation[x][y] = Min 
        for x in actions:
            for y in actions:
                if (x,y) in arcs:
                    relation[x][y] = Max
                    if (y,x) not in arcs:
                        relation[y][x] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Circulant graph : ', self.name)
        print('Order           : ', self.order)
        print('Circulants      : ', self.circulants)

class KneserDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary Kneser digraphs

    Parameters:
        | n > 0; n > j > 0;
        | valuationdomain ={'min':m, 'max':M}.

    Default instantiation as Petersen graph:
        n = 5, j = 2, valuationdomain = {'min':-1.0,'max':1.0}.

    """

    def __init__(self,n=5,j=2,valuationdomain = {'min':-1.0,'max':1.0}):
        import sys,array,copy
        self.name = 'kneser-'+str(n)+'-'+str(j)
        self.n = n
        self.j = j
        na = list(range(n+1))
        na.remove(0)
        ob = set()
        for x in na:
            ob.add(str(x))
        obActions = []
        for x in self.kChoices(ob,j):
            obActions.append(frozenset(x))
        order = len(obActions)
        self.order = order
        actions = []
        for i in range(order):
            actions.append(str(i+1))
        self.actions = actions
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        aindex = {}
        for i in range(order):
            aindex[actions[i]]=obActions[i]
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if aindex[x] & aindex[y] == set():
                    relation[x][y] = Max
                else:
                    relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Kneser graph    : ', self.name)
        print('n               : ', self.n)
        print('j               : ', self.j)
        print('order           : ', self.order)


class GridDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary Grid digraphs of dimension n times m.

    Parameters:
        n,m > 0; valuationdomain ={'min':m, 'max':M}.

    Default instantiation (5 times 5 Grid Digraph):
        n = 5, m=5, valuationdomain = {'min':-1.0,'max':1.0}.

    Randomly orientable with hasRandomOrientation=True (default=False).

    """

    def __init__(self,n=5,m=5,valuationdomain = {'min':-1.0,'max':1.0},
                 hasRandomOrientation=False,hasMedianSplitOrientation=False):
        import sys,array,copy
        self.name = 'grid-'+str(n)+'-'+str(m)
        self.n = n
        self.m = m
        na = list(range(n+1))
        na.remove(0)
        ma = list(range(m+1))
        ma.remove(0)
        actions = []
        gridNodes={}
        for x in na:
            for y in ma:
                action = str(x)+'-'+str(y)
                gridNodes[action]=(x,y)
                actions.append(action)
        order = len(actions)
        self.order = order
        self.actions = actions
        self.gridNodes = gridNodes
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if gridNodes[x][1] == gridNodes[y][1]:
                    if gridNodes[x][0] == gridNodes[y][0]-1 :
                        relation[x][y] = Max
                    elif gridNodes[x][0] == gridNodes[y][0]+1:
                        relation[x][y] = Max
                    else:
                        relation[x][y] = Min
                elif gridNodes[x][0] == gridNodes[y][0]:
                    if gridNodes[x][1] == gridNodes[y][1]-1:
                        relation[x][y] = Max
                    elif gridNodes[x][1] == gridNodes[y][1]+1:
                        relation[x][y] = Max
                    else:
                        relation[x][y] = Min
                else:
                    relation[x][y] = Min

        if hasRandomOrientation:
            import random
            random.seed()
            for x in actions:
                relation[x] = {}
                for y in actions:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            if random.random() > 0.5:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            if random.random() > 0.5:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        else:
                            relation[x][y] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            if random.random() > 0.5:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            if random.random() > 0.5:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        else:
                            relation[x][y] = Min
                    else:
                        relation[x][y] = Min

        elif hasMedianSplitOrientation:
            for x in actions:
                relation[x] = {}
                for y in actions:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            if gridNodes[y][1] <= gridNodes[x][0]:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        else:
                            relation[x][y] = Min

                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        else:
                            relation[x][y] = Min
                    else:
                        relation[x][y] = Min

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Grid graph    : ', self.name)
        print('n             : ', self.n)
        print('m             : ', self.m)
        print('order         : ', self.order)


class CompleteDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary complete graphs of order 5 in {-1,0,1} by default.

    Parameters:
        order > 0; valuationdomain=(Min,Max).

    """
    def __init__(self,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        self.name = 'complete'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = {}
        for x in actionlist:
            actions[str(x)] = {'name':str(x)}
        self.actions = actions
        Max = Decimal(str((valuationdomain[1])))
        Min = Decimal(str((valuationdomain[0])))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                if x == y:
                    relation[x][y] = Min
                else:
                    relation[x][y] = Max
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class RedhefferDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary Redheffer digraphs.

    https://en.wikipedia.org/wiki/Redheffer_matrix

    Parameters:
        order > 0; valuationdomain=(Min,Max).

    """
    ############### helper functions

    def __init__(self,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        self.name = 'Redheffer'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = {}
        for x in actionlist:
            actions[x] = {'name':str(x)}
        self.actions = actions
        Max = Decimal(str((valuationdomain[1])))
        Min = Decimal(str((valuationdomain[0])))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
##                if x == y:
##                    relation[x][y] = Min
                if x == 1 or y == 1:
                    relation[x][y] = Max
                elif x <= y and (y%x) == 0:
                    relation[x][y] = Max
                else:
                    relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class PolarisedDigraph(Digraph):
    """
    Renders the polarised valuation of a Digraph class instance:

    *Parameters*:
         * If level = None, a default strict 50% cut level (0 in a normalized [-1,+1] valuation domain) is used.
         * If KeepValues = False, the polarisation results in a crisp {-1,0,1}-valued result.
         * If AlphaCut = True a genuine one-sided True-oriented cut is operated.
         * If StrictCut = True, the cut level value is excluded resulting in an open polarised valuation domain.
           By default the polarised valuation domain is closed and the complementary indeterminate domain is open.

    """
    def __init__(self,digraph=None,level=None,KeepValues=True,AlphaCut=False,StrictCut=False):
        from copy import deepcopy
        if digraph == None:
            digraph = RandomValuationDigraph()
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        if level == None:
            #level = Max - (Max - Med)*Decimal('0.5')
            level = Med
            StrictCut = True
            KeepValues = False
        else:
            level = Decimal(str(level))
        self.name = 'cut_' + str(level)+ '_' + str(digraph.name)
        self.actions = deepcopy(digraph.actions)
        if AlphaCut:
            self.relation = self._constructAlphaCutRelation(digraph.relation,
                                                           level=level,
                                                           StrictCut=StrictCut)
        else:
            self.relation = self._constructBetaCutRelation(digraph.relation,
                                                          level=level,
                                                          KeepValues=KeepValues,
                                                          StrictCut=StrictCut)

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructBetaCutRelation(self,relationin, level, KeepValues=True,AlphaCut=False,StrictCut=False):
        """
        Parameters: relation and cut level.
        Flags: KeepValues (True), AlphaCut(False, unilateral cut), StrictCut (False)
        Renders the polarised relation.

        """
        Debug = False
        if Debug:
            print('Level, KeepValues,AlphaCut', level, KeepValues,AlphaCut)
        # determine the cut level
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        level = Decimal(str(level))
        compLevel = Max - level + Min
        if level < Med:
            print('Cut Level :', level, 'too low !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        elif level > Max:
            print('Cut Level :', level, 'too high !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        # change to a normalized [-1,0,1] valuation domain
        if KeepValues == False:
            Min = Decimal('-1')
            Max = Decimal('1')
            Med = Decimal('0')
            self.valuationdomain['min'] = Min
            self.valuationdomain['max'] = Max
            self.valuationdomain['med'] = Med
        # construct polarised relation
        actions = self.actions
        relationout = {}
        for a in actions:
            relationout[a] = {}
            for b in actions:
                if StrictCut:
                    if relationin[a][b] > level:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Max
                    elif relationin[a][b] < compLevel:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Min
                    else:
                        relationout[a][b] = Med
                else:
                    if relationin[a][b] >= level:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Max
                    elif relationin[a][b] <= compLevel:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Min
                    else:
                        relationout[a][b] = Med
        return relationout

    def _constructAlphaCutRelation(self,relationin, level, KeepValues=True,AlphaCut=False,StrictCut=False):
        """
        Parameters: relation and cut level.
        Renders the polarised relation.
        """
        Debug = False
        if Debug:
            print('Level, KeepValues,AlphaCut', level, KeepValues,AlphaCut)
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        level = Decimal(str(level))
        relationout = {}
        for a in actions:
            relationout[a] = {}
            for b in actions:
                if StrictCut:
                    if relationin[a][b] > level:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Max
                    else:
                        if KeepValues:
                            relationout[a][b] = Max - relationin[a][b] + Min
                        else:    
                            relationout[a][b] = Min
                else:
                    if relationin[a][b] >= level:
                        if KeepValues:
                            relationout[a][b] = relationin[a][b]
                        else:
                            relationout[a][b] = Max
                    else:
                        if KeepValues:
                            relationout[a][b] = Max - relationin[a][b] + Min
                        else:
                            relationout[a][b] = Min
        return relationout


class _MedianExtendedDigraph(Digraph):
    """
    Parameters:
        digraph + beta cut level between Med and Max.

    .. warning::

         The class is obsolete and is replaced by the genuine
         PolarisedDigraph class flagged with KeepValues=True.

    """
    def __init__(self,digraph=None,Level=None):
        from copy import copy,deepcopy
        if digraph == None:
            digraph = RandomValuationDigraph()
        self.valuationdomain = copy(digraph.valuationdomain)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        if Level == None:
            Level = Max - (Max - Med)*0.5
        self.name = 'cut_' + str(Level)+ '_' + str(digraph.name)
        self.actions = copy(digraph.actions)
        self.relation = self._constructRelation(digraph.relation, Level)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,relationin, Level):
        """
        Parameters: relation and cut level.
        Renders the polarised relation.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        CompLevel = Max - Level + Min
        if Level < Med:
            print('Cut Level :', Level, 'too low !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        else:
            relationout = {}
            for a in actions:
                relationout[a] = {}
                for b in actions:
                    if relationin[a][b] <= Level and relationin[a][b] >= CompLevel:
                        relationout[a][b] = Med
                    else:
                        relationout[a][b] = relationin[a][b]
        return relationout

class DualDigraph(Digraph):
    """
    Instantiates the dual ( = negated valuation) Digraph object from a deep copy of a given other Digraph instance.

    The relation constructor returns the dual of self.relation with generic formula:
        relationOut[a][b] = Max - self.relation[a][b] + Min
        where Max (resp. Min) equals valuation maximum (resp. minimum).

    .. note::

        In a bipolar valuation, the dual operator correspond to a simple changing of signs.

    """
    def __init__(self,other):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'dual_' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        #self.order = len(self.actions)
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        dualRelation = {}
        for a in actions:
            dualRelation[a] = {}
            for b in actions:
                dualRelation[a][b] = Max - self.relation[a][b] + Min
        self.relation = dualRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class _PreferenceDigraph(Digraph):
    """
    Obsolete constructor. Initiates the valued difference S(a,b) - S(b,a) of a Digraph instance.
    
    """
    def __init__(self,digraph):
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.name = 'dual_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self._constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,relationIn):
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                relationOut[a][b] = (relationIn[a][b] - relationIn[b][a])/Decimal('2.0')
        return relationOut

class AsymmetricPartialDigraph(Digraph):
    """
    Renders the asymmetric part of a Digraph instance.

    .. note::

         - The non asymmetric and the reflexive links are all put to the median indeterminate characteristic value!
         - The constructor makes a deep copy of the given Digraph instance!

    """
    def __init__(self,digraph):
        from copy import deepcopy
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        self.name = 'asymmetric_' + str(digraph.name)
        self.actions = deepcopy(digraph.actions)
        self.relation = self._constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,relationIn):
        """
        Returns the asymmetric part of the relationIn
        """
        actions = self.actions
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                if a != b:
                    if relationIn[a][b] >= Med and relationIn[b][a] <= Med:
                        relationOut[a][b] = relationIn[a][b]
                    elif relationIn[a][b] <= Med and relationIn[b][a] >= Med:
                        relationOut[a][b] = relationIn[a][b]
                    else:
                        relationOut[a][b] = Med
                else:  # reflexive terms are ignored
                    relationOut[a][b] = Med
        return relationOut

class SymmetricPartialDigraph(Digraph):
    """
    Renders the symmetric part of a Digraph instance.
    
    .. note::

          - The not symmetric and the reflexive links are all put to the median indeterminate characteristics value!.
          - The constructor makes a deep copy of the given Digraph instance!
          
    """
    def __init__(self,digraph):
        from copy import deepcopy
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        self.name = 'symmetric_' + str(digraph.name)
        self.actions = deepcopy(digraph.actions)
        self.relation = self._constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,relationIn):
        """
        Returns the symmetric part of the relationIn.

        """
        actions = self.actions
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                if a != b:
                    if relationIn[a][b] >= Med and relationIn[b][a] >= Med:
                        relationOut[a][b] = relationIn[a][b]
                    elif relationIn[a][b] <= Med and relationIn[b][a] <= Med:
                        relationOut[a][b] = relationIn[a][b]
                    else:
                        relationOut[a][b] = Med
                    ## relationOut[a][b] = min(relationIn[a][b],relationIn[b][a])
                else:
                    relationOut[a][b] = Med
        return relationOut

class kChoicesDigraph(Digraph):
    """
    Specialization of general Digraph class for instantiation
    a digraph of all k-choices collapsed actions.

    Parameters:
        | digraph := Stored or memory resident digraph instance
        | k := cardinality of the choices

    """
    def __init__(self,digraph=None,k=3):
        import random,sys,array
        from copy import deepcopy
        from collections import OrderedDict
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
        if digraph == None:
            digraph = RandomValuationDigraph()
            self.name = str(digraph.name)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph)):
            self.name = deepcopy(digraph.name)

        self.valuationdomain = deepcopy(digraph.valuationdomain)
        dactions = [x for x in digraph.actions]
        drelation = digraph.relation
        actions = OrderedDict()
        for kChoice in Digraph.kChoices(digraph,dactions,k):
            cn = '_'
            for x in kChoice:
                cn += str(x) + '_'
            commentString = '%d-choice candidate' % (k)
            actions[frozenset(kChoice)] = {'name': cn, 'comment': commentString}
        self.actions = actions
        self.order = len(self.actions)
        self.relation = self._computeRelation(drelation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def _computeRelation(self,relation):
        """
        computing the relation on kChoices
        """
        Min = self.valuationdomain['min']
        kChoices = self.actions
        krelation = {}
        for xch in kChoices:
            krelation[xch] = {}
            for ych in kChoices:
                krelation[xch][ych] = Min
                for x in (xch-ych):
                    for y in (ych-xch):
                        krelation[xch][ych] = max(krelation[xch][ych],relation[x][y])
        return krelation

#########

class _WeakCocaDigraph(Digraph):
    """
    Parameters:
        Stored or memory resident digraph instance.

    Specialization of general Digraph class for instantiation
    of weak chordless odd circuits augmented digraphs.

    """
    def __init__(self,digraph=None,comment=None):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph

        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'weakcocosilent =', silent
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = copy.copy(g.actions)
            self.valuationdomain = copy.copy(g.valuationdomain)
            self.relation = copy.copy(g.relation)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.copy(digraph.actions)
            self.valuationdomain = copy.copy(digraph.valuationdomain)
            self.relation = copy.copy(digraph.relation)
        else:
            fileName = digraph + 'py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = digraph
            self.actions = argDict['actionset']
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.weakCircuits = set()
        self.closureWeakChordlessOddCircuits(comment=silent)

    def closureWeakChordlessOddCircuits(self,comment=None):
        """
        Closure of cdordless odd circuits extraction.
        """
        newCircuits = None
        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'closuresilent=', silent
        while newCircuits != set():
            coc = set(self.weakCircuits)
            self.weakChordlessOddCircuits(comment=silent)
            self.addWeakCircuits(comment=silent)
            newCircuits = self.weakCircuits - coc

    def addWeakCircuits(self,comment=None):
        """
        Augmenting self with self.weakCircuits.
        """
        import copy,time
        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'addweaksilent = ', silent
        order0 = self.order
        actions = set(self.actions)
        weakCircuits = self.weakCircuits
        valuationdomain = self.valuationdomain
        weakGamma = self.weakGamma
        relation = self.relation
        for cycle in weakCircuits:
            cn = '_'
            dcycle = set()
            acycle = set()
            for x in cycle:
                cn = cn + str(x) + '_'
                dcycle = dcycle | weakGamma[x][0]
                dcycle = dcycle | set([x])
                acycle = acycle | weakGamma[x][1]
                acycle = acycle | set([x])
            weakGamma[cn]=(dcycle,acycle)
            for x in actions:
                if x in cycle:
                    dx0 = weakGamma[x][0] | set([cn])
                    dx1 = weakGamma[x][1] | set([cn])
                    weakGamma[x] = (dx0,dx1)
                    relxcn = relation[x]
                    relxcn[cn] = valuationdomain['max']
                    relation[x] = relxcn
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[x][y])
                        relxcn = relation[x]
                        relxcn[cn] = relxy
                        relation[x] = relxcn
            relcycle = {}
            for x in actions:
                if x in cycle:
                    relcycle[x] = valuationdomain['max']
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[y][x])
                    relcycle[x] = relxy
            relcycle[cn] = valuationdomain['min']
            relation[cn] = relcycle
            actions = actions | set([cn])
        self.actions = list(actions)
        self.order = len(actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        new = self.order - order0
        if not silent:
            if self.order == order0:
                print('  No weak circuits added !')
            else:
                print('  ',new,' weak circuit(s) added!')

    def showCircuits(self):
        """
        show methods for chordless odd circuits in CocaGraph
        """
        print('*---- Chordless odd circuits ----*')
        for circ in self.weakCircuits:
            deg = self.circuitMinCredibility(circ)
            print(list(circ), ', credibility :', deg)

#--------------------
class _CoceDigraph(Digraph):
    """
    Specialization of general Digraph class for instantiation of digraphs where
    all chordless odd circuits are eliminated by appropriate cuts of the valuation of the arcs.

    .. note::

        The method is only experimental and may easily lead to very sparse outranking digraphs with loads of undeterminate arcs.
        It is recommended to use instead the :py:class:`digraphs.BrokenCocsDigraph` class.
        
    Parameters:

        - digraph: Stored or memory resident digraph instance.
        - Cpp: using a C++/Agrum version of the Digraph.computeChordlessCircuits() method.
        - Piping: using OS pipes for data in- and output between Python and C++.

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,Comments=False,Debug=False):
        import random,sys,array
        from copy import deepcopy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph

        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = g.actions
            self.valuationdomain = g.valuationdomain
            self.relation = g.relation

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph,BipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = deepcopy(digraph.actions)
            self.valuationdomain = deepcopy(digraph.valuationdomain)
            self.relation = deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            argDict
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = digraph
            self.actions = argDict['actionset']
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        level,pg = self.iterateCocElimination(Comments=Comments, Debug=Debug)
        if pg != None:
            self.name = '%s_pol_%.2f' % (self.name,level)
            self.relation = pg.relation
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
            self.weakGamma = self.weakGammaSets()


    def iterateCocElimination(self,Comments=True,Debug=False):
        """
        Eliminates all chordless odd circuits with rising valuation cut levels.
        Renders a tuple (level,polarisedDigraph) where level is the
        necessary bipolar cut level for eliminating all chordless odd circuits,
        and polarisedDigraph is the resulting digraph instance.
        Renders (None,None) if no chordless odd circuit is detected.
        """
        from copy import deepcopy
        from time import time
        if Debug:
            Comments=True
        gcd = deepcopy(self)

        qualmaj0 = gcd.valuationdomain['med']
        if Comments:
            print('Chorless odd circuits elimination')
        i = 0
        qualmaj = gcd.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
        while qualmaj > qualmaj0:
            i += 1
            if Comments:
                print('--> Iteration %d' % (i))
                t0 = time()
            if qualmaj < gcd.valuationdomain['max']:
                pg = PolarisedDigraph(gcd,qualmaj,
                                      StrictCut=True,
                                      KeepValues=True)
            else:
                pg = PolarisedDigraph(gcd,qualmaj,
                                      StrictCut=False,
                                      KeepValues=True)
            qualmaj0 = qualmaj
            qualmaj = pg.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
        if i == 0:
            return (None,None)
        else:
            return (qualmaj0,pg)

#--------------------
class BrokenCocsDigraph(Digraph):
    """
    Specialization of general Digraph class for instantiation
    of chordless odd circuits broken digraphs.

    Parameters:

        - digraph: stored or memory resident digraph instance.
        - Cpp: using a C++/Agrum version of the Digraph.computeChordlessCircuits() method.
        - Piping: using OS pipes for data in- and output between Python and C++.

    All chordless odd circuits are broken at the weakest asymmetric link,
    i.e. a link :math:`(x, y)` with minimal difference between :math:`r(x S y)` and :math:`r(y S x)`.

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,\
                 Comments=False,Threading=False,nbrOfCPUs=1):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph,\
             RandomOutrankingDigraph, BipolarOutrankingDigraph, ConfidentBipolarOutrankingDigraph
        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
            print('Erreur: A valid Digraph instance is required!')
            return
        elif isinstance(digraph,(Digraph,OutrankingDigraph,\
                                 RandomOutrankingDigraph,BipolarOutrankingDigraph,\
                                 ConfidentBipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.deepcopy(digraph.actions)
            self.valuationdomain = copy.deepcopy(digraph.valuationdomain)
            try:
                self.valuationdomain['precision'] = digraph.valuationdomain['precision']
            except:
                self.valuationdomain['precision']  = Decimal('0')
            self.relation = copy.deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = digraph
            self.actions = argDict['actionset']
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.breakChordlessOddCircuits(Cpp=Cpp,Piping=Piping,\
                                         Comments=Comments,Threading=Threading,nbrOfCPUs=nbrOfCPUs)

    def breakChordlessOddCircuits(self,Cpp=False,Piping=False,\
                                    Comments=True,Debug=False,Threading=False,nbrOfCPUs=1):
        """
        Breaking of chordless odd circuits extraction.
        """
        newCircuits = None
        self.circuitsList = []
        self.brokenLinks = set()
        try:
            oldBreakings = self.breakings
        except:
            self.breakings = 0
        self.newBreakings = self.order
        #while newCircuits != set() or self.newBreakings != 0:
        i = 0
        while newCircuits != set():
            i += 1
            initialCircuits = set([x for cl,x in self.circuitsList])
            self.breakCircuits(Comments=Comments)
            if Cpp:
                if Piping:
                    self.computeCppInOutPipingChordlessCircuits(Odd=True,Debug=Debug)
                else:
                    self.computeCppChordlessCircuits(Odd=True,Debug=Debug)
            elif Threading:
                self.computeChordlessCircuitsMP(Odd=True,Comments=Debug,\
                                                Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            else:
                self.computeChordlessCircuits(Odd=True,Comments=Debug)
            newCircuits = set([x for cl,x in self.circuitsList])
            if Comments:
                print('--->> iteration %d:', i)
                print('newCircuits', newCircuits)


    def breakCircuits(self,Comments=False):
        """
        Break all cricuits in self.circuits.
        """
        import time
        from digraphsTools import flatten
        
        newBreakings = 0
        if not(isinstance(self.actions,dict)):
            actions = {}
            for x in self.actions:
                actions[x] = {'name':x}
        else:
            actions = self.actions
        circuitsList = self.circuitsList
        if Comments:
            print('list of circuits tp break : ', circuitsList)
        valuationdomain = self.valuationdomain
##        gamma = self.gamma
        relation = self.relation
        Med = valuationdomain['med']
        currentCircuits = list(circuitsList)
        for (cycleList,cycle) in circuitsList:
            degP,degN,minLink = self.circuitCredibilities(cycleList,Debug=Comments)
            if Comments:
                print(cycleList,cycle,degP,degN,minLink)
            if Comments:
                print('Breaking:',cycleList,degP,degN)
            actionsSubset = [x for x in flatten(cycle)]
            if Comments:
                self.showRelationTable(actionsSubset=actionsSubset)
            x = minLink[0]
            y = minLink[1]
            if Comments:
                print('Minimal link put to doubt: ', x,y)
            if (x,y) not in self.brokenLinks:
                relation[x][y] = Med
                relation[y][x] = Med
                self.brokenLinks.add((x,y))
                newBreakings += 1
            currentCircuits.remove((cycleList,cycle))

        self.actions = actions
        self.order = len(actions)
        self.relation = relation
        self.circuitsList = currentCircuits
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.breakings += newBreakings

    def showComponents(self):
        """Shows the list of connected components of the digraph instance."""
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            #component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1


#--------------------
class BreakAddCocsDigraph(Digraph):
    """
    Specialization of general Digraph class for instantiation
    of chordless odd circuits augmented digraphs.

    Parameters:

        - digraph: Stored or memory resident digraph instance.
        - Cpp: using a C++/Agrum version of the Digraph.computeChordlessCircuits() method.
        - Piping: using OS pipes for data in- and output between Python and C++.

    A chordless odd circuit is added if the cumulated credibility of the circuit supporting arcs is larger or
    equal to the cumulated credibility of the converse arcs. Otherwise, the circuit is broken at the weakest asymmetric link,
    i.e. a link (*x*, *y*) with minimal difference between r(*x* S *y*) - r(*y* S *x*).

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,\
                 Comments=False,Threading=False,nbrOfCPUs=1):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = g.actions
            self.valuationdomain = g.valuationdomain
            self.relation = g.relation

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph,BipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.deepcopy(digraph.actions)
            self.valuationdomain = copy.deepcopy(digraph.valuationdomain)
            try:
                self.valuationdomain['precision'] = digraph.valuationdomain['precision']
            except:
                self.valuationdomain['precision']  = Decimal('0')
            self.relation = copy.deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = digraph
            self.actions = argDict['actionset']
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.closureChordlessOddCircuits(Cpp=Cpp,Piping=Piping,\
                                         Comments=Comments,Threading=Threading,nbrOfCPUs=nbrOfCPUs)

    def closureChordlessOddCircuits(self,Cpp=False,Piping=False,\
                                    Comments=True,Debug=False,Threading=False,nbrOfCPUs=1):
        """
        Closure of chordless odd circuits extraction.
        """
        newCircuits = None
        self.circuitsList = []
        try:
            oldBreakings = self.breakings
        except:
            self.breakings = 0
        self.newBreakings = self.order
        #while newCircuits != set() or self.newBrakings != 0:
        while newCircuits != set():
            initialCircuits = set([x for cl,x in self.circuitsList])
##            if Cpp:
##                if Piping:
##                    self.computeCppInOutPipingChordlessCircuits(Odd=True,Debug=Debug)
##                else:
##                    self.computeCppChordlessCircuits(Odd=True,Debug=Debug)
##            elif Threading:
##                self.computeChordlessCircuitsMP(Odd=True,Comments=Debug,\
##                                                Threading=Threading,nbrOfCPUs=nbrOfCPUs)
##            else:
##                self.computeChordlessCircuits(Odd=True,Comments=Debug)
##           
            #print(self.circuitsList)
            self.addCircuits(Comments=Comments)
            if Cpp:
                if Piping:
                    self.computeCppInOutPipingChordlessCircuits(Odd=True,Debug=Debug)
                else:
                    self.computeCppChordlessCircuits(Odd=True,Debug=Debug)
            elif Threading:
                self.computeChordlessCircuitsMP(Odd=True,Comments=Debug,\
                                                Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            else:
                self.computeChordlessCircuits(Odd=True,Comments=Debug)
            currentCircuits = set([x for cl,x in self.circuitsList])
            if Comments:
                print('initialCircuits, currentCircuits', initialCircuits, currentCircuits)
            newCircuits = currentCircuits - initialCircuits

    def addCircuits(self,Comments=False):
        """
        Augmenting self with self.circuits.
        """
        import time
        from digraphsTools import flatten
        
        #from copy import deepcopy
        order0 = self.order
        newBreakings = 0
        if not(isinstance(self.actions,dict)):
            actions = {}
            for x in self.actions:
                actions[x] = {'name':x}
        else:
            actions = self.actions

        #ListActions = [frozenset([x]) for x in actions]
        circuitsList = self.circuitsList
        if Comments:
            print('list of circuits: ', circuitsList)
        valuationdomain = self.valuationdomain
        gamma = self.gamma
        relation = self.relation
        Med = valuationdomain['med']
        currentCircuits = list(circuitsList)
        for (cycleList,cycle) in circuitsList:
            degP,degN,minLink = self.circuitCredibilities(cycleList,Debug=Comments)
            if Comments:
                print(cycleList,cycle,degP,degN,minLink)
            #if degP+degN > Med:
            
            if (degP + degN) > valuationdomain['precision']:
#           if (degP + degN) >= valuationdomain['med']:   # adds potentially more circuits 
                if Comments:
                    print('Adding cycle:', cycle, ' with Pdegree=',degP,' and Ndegree=',degN )
                cn = '_'
                dcycle = set()
                acycle = set()
                for x in cycleList:
                    if isinstance(x,frozenset):
                        cn += actions[x]['name'] + '_'
                    else:
                        cn += str(x) + '_'
                    dcycle = dcycle | gamma[x][0]
                    dcycle = dcycle | set([x])
                    acycle = acycle | gamma[x][1]
                    acycle = acycle | set([x])
                gamma[cycle]=(dcycle,acycle)
                for x in actions:
                    if x in cycle:
                        dx0 = gamma[x][0] | set([cycle])
                        dx1 = gamma[x][1] | set([cycle])
                        gamma[x] = (dx0,dx1)
                        relxcn = relation[x]
                        #relxcn[cycle] = valuationdomain['max']
                        relxcn[cycle] = degP + degN
                        relation[x] = relxcn
                    else:
                        relxy = valuationdomain['min']
                        for y in cycle:
                            relxy = max(relxy,relation[x][y])
                            relxcn = relation[x]
                            relxcn[cycle] = relxy
                            relation[x] = relxcn
                relcycle = {}
                for x in actions:
                    if x in cycle:
                        #relcycle[x] = valuationdomain['max']
                        relcycle[x] = degP
                    else:
                        relxy = valuationdomain['min']
                        for y in cycle:
                            relxy = max(relxy,relation[y][x])
                        relcycle[x] = relxy
                relcycle[cycle] = valuationdomain['min']
                relation[cycle] = relcycle
                name = 'chordless odd %d-circuit' % (len(cycle))
                actions[cycle] = {'name': cn, 'comment': name}
                if Comments:
                    print(actions[cycle])
            else:
                if Comments:
                    print('Breaking:',cycleList,degP,degN)
                actionsSubset = [x for x in flatten(cycle)]
                if Comments:
                    self.showRelationTable(actionsSubset=actionsSubset)
                x = minLink[0]
                y = minLink[1]
                if Comments:
                    print('Minimal link put to doubt: ', x,y)
                relation[x][y] = Med
                relation[y][x] = Med
                currentCircuits.remove((cycleList,cycle))
                newBreakings += 1

        self.actions = actions
        self.order = len(actions)
        self.relation = relation
        self.circuitsList = currentCircuits
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        new = self.order - order0
        if Comments:
            if new == 0:
                print('  No circuits added !')
            else:
                print('  ',new,' circuit(s) added!')
        self.newBreakings = newBreakings
        self.breakings += newBreakings
        if Comments:
            if newBreakings == 0:
                print('  No further circuit brakings !')
            else:
                print('  ',newBreakings,' new circuit(s) were broken')

    def showCircuits(self,credibility=None,Debug=False):
        """
        show methods for chordless odd circuits in CocaGraph
        """
        print('*---- Chordless circuits ----*')
        for (circList,circSet) in self.circuitsList:
            if credibility == 'maximal':
                degM = self.circuitMaxCredibility(circList,Debug=Debug)
                print(circList, ', maximal credibility :', degM)
            elif credibility == 'minimal':
                degm = self.circuitMinCredibility(circList,Debug=Debug)
                print(circList, ', minimal credibility :', degm)
            elif credibility == 'average':
                degm = self.circuitMinCredibility(circList,Debug=Debug)
                print(circList, ', average credibility :', degm)
            else:
                degP,degN,minLink = self.circuitCredibilities(circList,Debug=Debug)
                print(circList, ', marginal credibility :', degP+degN)
                x = minLink[0]
                y = minLink[1]
                print('minimal link: ', minLink, self.relation[x][y],self.relation[y][x]) 
            
        print('Coca graph of order %d with %d odd chordless circuits.' % (len(self.actions), len(self.circuitsList)))
        #print len(aself.circuitsList),' cirduits

    def showComponents(self):
        """Shows the list of connected components of the digraph instance."""
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            #component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1

#--------------------
class CocaDigraph(Digraph):
    """

    Old CocaDigraph class without circuit breakings; all circuits and circuits of circuits are added as hyper-nodes.

    .. warning::

        May sometimes give inconsistent results when an autranking digraph shows loads of chordless cuircuits.
        It is recommended in this case to use instead either the BrokenCocsDigraph class (preferred option)
        or the  BreakAddCocsDigraph class.
    
    Parameters:

        - digraph: Stored or memory resident digraph instance.
        - Cpp: using a C++/Agrum version of the Digraph.computeChordlessCircuits() method.
        - Piping: using OS pipes for data in- and output between Python and C++.

    Specialization of general Digraph class for instantiation
    of chordless odd circuits augmented digraphs.

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,Comments=False):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
##            g = RandomValuationDigraph()
##            self.name = str(g.name)
##            self.actions = g.actions
##            self.valuationdomain = g.valuationdomain
##            self.relation = g.relation
            print('!!! Error: no valid digraph argument provided')

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph,BipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.deepcopy(digraph.actions)
            self.valuationdomain = copy.deepcopy(digraph.valuationdomain)
            self.relation = copy.deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = digraph
            self.actions = argDict['actionset']
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.closureChordlessOddCircuits(Cpp=Cpp,Piping=Piping,Comments=Comments)

    def closureChordlessOddCircuits(self,Cpp=False,Piping=False,Comments=False):
        """
        Closure of chordless odd circuits extraction.
        """
        newCircuits = None
        self.circuitsList = []
        while newCircuits != set():
            initialCircuits = set([x for cl,x in self.circuitsList])
            if Cpp:
                if Piping:
                    self.computeCppInOutPipingChordlessCircuits(Odd=True,Debug=Comments)
                else:
                    self.computeCppChordlessCircuits(Odd=True,Debug=Comments)
            else:
                self.computeChordlessCircuits(Odd=True,Comments=Comments)
            self.addCircuits(Comments=Comments)
            currentCircuits = set([x for cl,x in self.circuitsList])
            if Comments:
                print('initialCircuits, currentCircuits', initialCircuits, currentCircuits)
            newCircuits = currentCircuits - initialCircuits

    def addCircuits(self,Comments=False):
        """
        Augmenting self with self.circuits.
        """
        import copy,time
        order0 = self.order
        if isinstance(self.actions,(list,set)):
            actions = {}
            for x in self.actions:
                actions[x] = {'name':x}
        else:
            actions = self.actions

        #ListActions = [frozenset([x]) for x in actions]
        circuitsList = self.circuitsList
        if Comments:
            print('list of circuits: ', circuitsList)
        valuationdomain = self.valuationdomain
        gamma = self.gamma
        relation = self.relation
        for (cycleList,cycle) in circuitsList:
            cn = '_'
            dcycle = set()
            acycle = set()
            for x in cycleList:
                if isinstance(x,frozenset):
                    cn += actions[x]['name'] + '_'
                else:
                    cn += str(x) + '_'
                dcycle = dcycle | gamma[x][0]
                dcycle = dcycle | set([x])
                acycle = acycle | gamma[x][1]
                acycle = acycle | set([x])
            gamma[cycle]=(dcycle,acycle)
            for x in actions:
                if x in cycle:
                    dx0 = gamma[x][0] | set([cycle])
                    dx1 = gamma[x][1] | set([cycle])
                    gamma[x] = (dx0,dx1)
                    relxcn = relation[x]
                    relxcn[cycle] = valuationdomain['max']
                    #relxcn[cycle] = degP
                    relation[x] = relxcn
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[x][y])
                        relxcn = relation[x]
                        relxcn[cycle] = relxy
                        relation[x] = relxcn
            relcycle = {}
            for x in actions:
                if x in cycle:
                    relcycle[x] = valuationdomain['max']
                    #relcycle[x] = degP
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[y][x])
                    relcycle[x] = relxy
            relcycle[cycle] = valuationdomain['min']
            relation[cycle] = relcycle
            name = 'chordless odd %d-circuit' % (len(cycle))
            actions[cycle] = {'name': cn, 'comment': name}
            if Comments:
                print(actions[cycle])
        #self.actions = list(actions)
        self.actions = actions
        self.order = len(actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        new = self.order - order0
        if Comments:
            if self.order == order0:
                print('  No circuits added !')
            else:
                print('  ',new,' circuit(s) added!')

    def showCircuits(self,credibility=None):
        """
        show methods for chordless odd circuits in CocaGraph
        """
        print('*---- Chordless circuits ----*')
        for (circList,circSet) in self.circuitsList:
            if credibility == 'maximal':
                degM = self.circuitMaxCredibility(circSet)
                print(circList, ', maximal credibility :', degM)
            elif credibility == 'minimal':
                degm = self.circuitMinCredibility(circSet)
                print(circList, ', minimal credibility :', degm)
            elif credibility == 'average':
                degm = self.circuitMinCredibility(circSet)
                print(circList, ', average credibility :', degm)
            else:
                degP,degN,minLink = self.circuitCredibilities(circSet)
                print(circList, ', marginal credibility :', degP+degN)
            
        print('Coca graph of order %d with %d odd chordles circuits.' % (len(self.actions), len(self.circuitsList)))
        #print len(aself.circuitsList),' cirduits

    def showComponents(self):
        """Shows the list of connected components of the digraph instance."""
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            #component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1

#---------------------
##class CocaDigraph(_CocaDigraph):
##    """
##    CocaDigraph class wrapper for testing purposes only
##    """

#------------------------------------------

class StrongComponentsCollapsedDigraph(Digraph):
    """
    Reduction of Digraph object to its strong components.
    """
    def __init__(self,digraph=None):
        from copy import copy,deepcopy
        from collections import OrderedDict
        if digraph == None:
           print('Error: you must provide a valid digraph to the constructor!')
        else:
           self.name = digraph.name + '_Scc'
           self.valuationdomain = deepcopy(digraph.valuationdomain)
           scc = digraph.strongComponents()
           actions = OrderedDict()
           for i,strongComponent in enumerate(scc):
               actionShortName = 'Scc_'+str(i+1)
               actionKey = strongComponent
               actionName = '_'
               for x in strongComponent:
                   actionName += str(x)+'_'
               actions[actionKey] = {'name': actionName,\
                                     'shortName': actionShortName,\
                                     'comment': 'collapsed strong component'}
           self.actions = actions
           relation = {}
           actionsList = [x for x in actions]
           actionsList.sort()
           for xsc in actionsList:
               relation[xsc] = {}
               for ysc in actionsList:
                   relation[xsc][ysc] = self.valuationdomain['min']
                   for x in xsc:
                       for y in ysc:
                           if x == y:
                               relation[xsc][ysc] = self.valuationdomain['med']
                           elif digraph.relation[x][y] > relation[xsc][ysc]:
                               relation[xsc][ysc] = digraph.relation[x][y]
           self.relation = relation
           self.order = len(self.actions)
           self.gamma = self.gammaSets()
           self.notGamma = self.notGammaSets()

    def showComponents(self):
        """Shows the list of connected components of the digraph instance."""
        print('short', '\t', 'content')
        for x in self.actions:
            print(self.actions[x]['shortName'], '\t', self.actions[x]['name'])
#-------------------------------------------------------


# ------------ XML encoded stored Digraph instances obsolete

class _XMLDigraph24(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XML formatted digraphs.
    """

    def __init__(self,fileName='testsaveXML'):
        from xml.sax import make_parser
        xmlDigraph = _XMLDigraphHandler()
        saxParser = make_parser()
        saxParser.setContentHandler(xmlDigraph)
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        saxParser.parse(fo)
        self.name = xmlDigraph.name
        self.category = xmlDigraph.category
        self.subcategory = xmlDigraph.subcategory
        self.actions = xmlDigraph.actions
        self.valuationdomain = xmlDigraph.valuationdomain
        Min = xmlDigraph.valuationdomain['min']
        Max = xmlDigraph.valuationdomain['max']
        Med = Min + ((Max - Min)/2.0)
        self.valuationdomain['med'] = Med
        self.relation = xmlDigraph.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):

        if self.category == 'outranking':
            Digraph.showAll(self)
            self.showPreKernels()
            self.showGoodChoices()
            self.showBadChoices()

        else:
            Digraph.showAll(self)

class _XMLDigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XML formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xml).
    """

    def __init__(self,fileName='testsaveXML'):
        from xml.etree import ElementTree
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        digraph = ElementTree.parse(fo).getroot()
        self.category = digraph.attrib['category']
        self.subcategory = digraph.attrib['subcategory']
        self.name = digraph.find('header').find('name').text
        self.author = digraph.find('header').find('author').text
        self.reference = digraph.find('header').find('reference').text
        Min = Decimal(digraph.find('valuationdomain').find('min').text)
        Max = Decimal(digraph.find('valuationdomain').find('max').text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        actions = [action.text for action in digraph.find('nodes').findall('node')]
        self.actions = actions
        relation = {}
        for x in actions:
            relation[x] = {}
        for arc in digraph.find('relation').findall('arc'):
            relation[arc.find('i').text][arc.find('t').text] = Decimal(arc.find('v').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class _XMLDigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XML formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xml).
    """

    def __init__(self,fileName='testsaveXML'):
        from xml.etree import ElementTree
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        digraph = ElementTree.parse(fo).getroot()
        self.category = digraph.attrib['category']
        self.subcategory = digraph.attrib['subcategory']
        self.name = digraph.find('header').find('name').text
        self.author = digraph.find('header').find('author').text
        self.reference = digraph.find('header').find('reference').text
        Min = Decimal(digraph.find('valuationdomain').find('min').text)
        Max = Decimal(digraph.find('valuationdomain').find('max').text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        actions = [action.text for action in digraph.find('nodes').findall('node')]
        self.actions = actions
        relation = {}
        for x in actions:
            relation[x] = {}
        for arc in digraph.find('relation').findall('arc'):
            relation[arc.find('i').text][arc.find('t').text] = Decimal(arc.find('v').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class CSVDigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored csv formatted digraphs. Using the inbuilt module csv.

    Param:
        fileName (without the extension .csv).
    """

    def __init__(self,fileName='temp',valuationMin=-1,valuationMax=1):
        from csv import reader

        try:
            fileNameExt = fileName + '.csv'
            fi = open(fileNameExt,'r')
            csvReader = reader(fi)
            csvText = [x for x in csvReader]
        except:
            print("Error: File %s.csv not found !!" % (fileName))
        
        self.name = fileName
        self.order = len(csvText)-1
        self.reference = 'CSV Digraph input method.'
        Min = Decimal(valuationMin)
        Max = Decimal(valuationMax)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        self.actions = [csvText[0][i] for i in range(1,self.order+1)]
    
        relation = {}
        for i in range(1,self.order+1):
            relation[csvText[i][0]] = {}
            for j in range(1,self.order+1):
                relation[csvText[i][0]][csvText[0][j]] = Decimal(csvText[i][j])
        
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):
        try:
            if self.category == 'outranking':
                Digraph.showAll(self)
                self.showPreKernels()
                self.showGoodChoices()
                self.showBadChoices()
            else:
                Digraph.showAll(self)
        except:
            Digraph.showAll(self)

class _XMCDADigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XMCDA formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xmcda). 
    """

    def __init__(self,fileName='temp'):
        from xml.etree import ElementTree
        try:
            fileNameExt = fileName + '.xmcda'
            fo = open(fileNameExt,'r')
        except:
            try:
                fileNameExt = fileName + '.xml'
                fo = open(fileNameExt,'r')
            except:
                print("Error: file %s{.xml|.xmcda}  not found" % (fileName))
        XMCDA = ElementTree.parse(fo).getroot()
        description = {}
        for elem in [x for x in XMCDA.find('caseReference').getchildren()]:
            description[elem.tag] = elem.text
        self.description = description
        try:
            self.name = description['name']
        except:
            self.name ='temp'
        try:
            self.author = description['author']
        except:
            self.author = 'digraphs module (RB)'
        try:
            self.reference = description['comment']
        except:
            self.reference = 'XMCDA 1.0 Digraph input method.'        
        Min = Decimal(XMCDA.find('relationOnAlternatives').find('valuationDomain').find('minimum').getchildren().pop().text)
        Max = Decimal(XMCDA.find('relationOnAlternatives').find('valuationDomain').find('maximum').getchildren().pop().text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        actions = {}
        for alternative in XMCDA.find('alternatives').findall('alternative'):
            id = alternative.attrib['id']
            actions[id] = {}
            for elem in [x for x in alternative.find('description').getchildren()]:
                actions[id][elem.tag] = elem.text    
        self.actions = actions
        relation = {}
        try:
            if XMCDA.find('relationOnAlternatives').find('description').find('type').text == 'outrankingDigraph':
                self.category = 'outranking'
            else:
                self.category = 'general'
        except:
            pass
        for x in actions:
            relation[x] = {}
        for arc in XMCDA.find('relationOnAlternatives').find('arcs').findall('arc'):
            try:
                relation[arc.find('from').find('alternativeID').text][arc.find('to').find('alternativeID').text] = Decimal(arc.find('value').find('real').text)
            except:
                relation[arc.find('from').find('alternativeID').text][arc.find('to').find('alternativeID').text] = Decimal(arc.find('value').find('integer').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        
    def showAll(self):
        try:
            if self.category == 'outranking':
                Digraph.showAll(self)
                self.showPreKernels()
                self.showGoodChoices()
                self.showBadChoices()
            else:
                Digraph.showAll(self)
        except:
            Digraph.showAll(self)

class XMCDA2Digraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XMCDA-2.0 formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xmcda).
    """

    def __init__(self,fileName='temp'):
        from xml.etree import ElementTree

        fileNameExt = fileName + '.xml'
        try:
            fo = open(fileNameExt,'r')
        except:
            fileNameExt = fileName + '.xmcda'
            try:
                fo = open(fileNameExt,'r')
            except:
                fileNameExt = fileName + '.xmcda2'
                try:
                    fo = open(fileNameExt,'r')
                except:
                    print("Error: file %s  not found" % (fileNameExt))

        print("file %s is being read:" % (fileNameExt))
        XMCDA = ElementTree.parse(fo).getroot()
        try:
            self.name = XMCDA.attrib['name']
        except:
            self.name ='temp'

        description = {}
        for elem in [x for x in XMCDA.find('projectReference').getchildren()]:
            description[elem.tag] = elem.text
        self.description = description
        try:
            self.author = description['author']
        except:
            self.author = 'digraphs module (RB)'
        try:
            self.reference = description['comment']
        except:
            self.reference = 'XMCDA 1.0 Digraph input method.'

        Min = Decimal(XMCDA.find('alternativesComparisons').find('valuation').find('quantitative').find('minimum').getchildren().pop().text)
        Max = Decimal(XMCDA.find('alternativesComparisons').find('valuation').find('quantitative').find('maximum').getchildren().pop().text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain


        actions = {}
        for alternative in XMCDA.find('alternatives').findall('alternative'):
            id = alternative.attrib['id']
            actions[id] = {}
            actions[id]['name'] = alternative.attrib['name']
            for elem in [x for x in alternative.find('description').getchildren()]:
                actions[id][elem.tag] = elem.text
        self.actions = actions


        relation = {}
        try:
            if XMCDA.find('alternativesComparisons').attribute['mcdaConcept'] == 'outrankingDigraph':
                self.category = 'outranking'
            else:
                self.category = 'general'
        except:
            pass
        for x in actions:
            relation[x] = {}
        for pair in XMCDA.find('alternativesComparisons').find('pairs').findall('pair'):
            try:
                relation[pair.find('initial').find('alternativeID').text][pair.find('terminal').find('alternativeID').text] = Decimal(pair.find('value').find('real').text)
            except:
                relation[pair.find('initial').find('alternativeID').text][pair.find('terminal').find('alternativeID').text] = Decimal(pair.find('value').find('integer').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):
        try:
            if self.category == 'outranking':
                Digraph.showAll(self)
                self.showPreKernels()
                self.showGoodChoices()
                self.showBadChoices()
            else:
                Digraph.showAll(self)
        except:
            Digraph.showAll(self)

###  replace the old outrankingDigraphs
#from outrankingDigraphs import *
from randomDigraphs import *

#############################################

#----------test Digraph class ----------------
if __name__ == "__main__":
    import sys,array
    from digraphsTools import *
    from outrankingDigraphs import OutrankingDigraph,\
    RandomOutrankingDigraph, BipolarOutrankingDigraph
    from votingProfiles import CondorcetDigraph
    from randomPerfTabs import *


    print('*****************************************************')
    print('* Python digraphs module                            *')
    print('* $Revision: 2500+ $                                *')
    print('* Copyright (C) 2006-20018 Raymond Bisdorff         *')
    print('* The module comes with ABSOLUTELY NO WARRANTY      *')
    print('* to the extent permitted by the applicable law.    *')
    print('* This is free software, and you are welcome to     *')
    print('* redistribute it if it remains free software.      *')
    print('*****************************************************')

    narg = len(sys.argv)

    noTest = True

    if narg == 1:
        noTest = False

    elif narg == 2:
        if sys.argv[1] == '-r':
            g = RandomValuationDigraph()
        elif sys.argv[1] == '-rt':
            t = RandomPerformanceTableau()
            g = BipolarOutrankingDigraph(t)
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '-?':
            print('usage: digraphs.py [[-t|rt|v|av] <filename> | -r [n]] | -rt [[n] [m]]')
            print('  <filename> of valid python digraph (without .py extension)')
            print('  option = -t means valid performance tableau input.')
            print('  option = -rt means  performance tableau input.')
            print('  option = -v means valid voting profile input.')
            print('  option = -av means valid approval voting profile input.')
            print('  option = -r n : means a random digraph of order n (default n=10).')
            print('  option = -rt n m : means an outranking digraph from a random')
            print('                     performance tableau input with n actions and m criteria')
            print('                     (default n = 10, m = 7).')
            sys.exit(1)
        else:
            file = sys.argv[1]
            g = Digraph(file)
    elif narg == 3:
        if sys.argv[1] == '-r':
            order = int(sys.argv[2])
            g = RandomValuationDigraph(order)
        elif sys.argv[1] == '-rt':
            actions = int(sys.argv[2])
            t = RandomPerformanceTableau(numberOfActions=actions)
            g = BipolarOutrankingDigraph(t)
        elif sys.argv[1] == '-t':
            file = sys.argv[2]
            g = BipolarOutrankingDigraph(file)
        elif sys.argv[1] == '-v':
            file = sys.argv[2]
            g = CondorcetDigraph(file)
        elif sys.argv[1] == '-av':
            file = sys.argv[2]
            g = CondorcetDigraph(file,approvalVoting=True)
    elif narg == 4:
        if sys.argv[1] == '-rt':
            nActions = int(sys.argv[2])
            mCriteria = int(sys.argv[3])
            t = RandomPerformanceTableau(numberOfActions=nActions,numberOfCriteria=mCriteria)
            g = BipolarOutrankingDigraph(t)
    else:
        print('usage: digraphs.py [[-t|rt|v|av] <filename> | -r [n]] | -rt [[n] [m]]')
        print('  <filename> of valid python digraph (without .py extension)')
        print('  option = -t means valid performance tableau input.')
        print('  option = -rt means  performance tableau input.')
        print('  option = -v means valid voting profile input.')
        print('  option = -av means valid approval voting profile input.')
        print('  option = -r n : means a random digraph of order n (default n=10).')
        print('  option = -rt n m : means an outranking digraph from a random')
        print('                     performance tableau input with n actions and m criteria')
        print('                     (default n = 10, m = 7).')
        sys.exit(1)
    if noTest:
        print('*------ Results -------"')
        g.showRelationTable()
        g.showAll()
        g.showStatistics()
                    

    else:
        print('*-------- Testing classes and methods -------')

        from time import time
        from digraphsTools import *
        ##dg = RedhefferDigraph(order=113)
        #g = RandomTournament(order=10,seed=1)
        g = RandomValuationDigraph(order=20)
        #print(g)
        #g = CirculantDigraph(IndeterminateInnerPart=True)
        g.computeMaxHoleSize(Comments=True)
        
##        from outrankingDigraphs import BipolarOutrankingDigraph
##        from randomPerfTabs import Random3ObjectivesPerformanceTableau
####        from linearOrders import CopelandOrder
##        t1 = Random3ObjectivesPerformanceTableau(numberOfActions=7,numberOfCriteria=7,seed=101)
##        g = BipolarOutrankingDigraph(t1,Normalized=True)
##        g.showRelationTable()
##        print(g.computeDeterminateness())
##        print(g.computeDeterminateness(InPercents=True))
##        g.recodeValuation(0,1)
##        print(g.computeDeterminateness())
##        print(g.computeDeterminateness(InPercents=True))
##      
##        g.showHTMLBestChoiceRecommendation(ChoiceVector=False)
##        g.showPreKernels()
##        g.showRelationTable()
##        g.showHTMLBestChoiceRecommendation(ChoiceVector=False)
##        gcd = ~(-g)
##        cocb = BrokenCocsDigraph(gcd,Comments=True)
##        print(cocb.brokenLinks)
##        gcd.computeRubisChoice()
##        gcd.showGoodChoices()
##        g = RandomValuationDigraph(order=10,seed=3)
##        g.showHTMLPerformanceTableau(ndigits=0)
##        g.showHTMLRelationTable(IntegerValues=True)
##        g.recodeValuation()
##        g.showHTMLRelationTable(IntegerValues=True)
##        g.showHTMLPerformanceTableau(ndigits=0)
        
##        h3 = BrokenCocsDigraph(digraph=g,Comments=False)
##        h3.save('resbreakco2')
##        h3.showAll()

##        cop = CopelandOrder(g)
##        #g.showHTMLRelationMap(rankingRule='rankedPairs')
##        gcd = CoDualDigraph(g)
##        #gcd.showHTMLRelationMap(cop.copelandOrder)
##        g.showRubisBestChoiceRecommendation()
##        t1.computeQuantileOrder(3,10)
##        #g.showHTMLRelationMap(Colored=False)
##        #g.exportGraphViz()
##        from outrankingDigraphs import BipolarOutrankingDigraph
##        from randomPerfTabs import RandomCBPerformanceTableau
##        MP = False
##        with open('resGR.csv','w') as fo:
##            #fo.write('"card","tnewMP","tnew","told"\n')
##            for s in range(2,3):
##                print('Simulation: ',s)
##                t1 = Random3ObjectivesPerformanceTableau(numberOfActions=100,seed=s)
##                g = BipolarOutrankingDigraph(t1,Normalized=True)
##                #g = RandomDigraph(order=250,seed=s)
##                #g = RandomTournament(order=25,seed=s)
##                #g = GridDigraph(8,8,hasMedianSplitOrientation=True)
##                t0 = time()
##                print(len(g.computeChordlessCircuitsMP(Odd=False,
##                                                       Comments=False,
##                                                       Threading=MP)))
##                tnewMP = (time()-t0)
##                print(tnewMP)     
##                #g.showChordlessCircuits()
##                t0 = time()
##                print(len(g._computeChordlessCircuits(Odd=False,
##                                                       Comments=False)))
##                tnew = (time()-t0)
##                print(tnew)     
##                new = len(g.circuitsList)
##                t0 = time()
##                print(len(g.computeChordlessCircuits(Odd=False,Comments=False)))
##                told = (time()-t0)
##                print(told)
##                #g.showChordlessCircuits()
##                #g.showRelationTable(actionsSubset=['a05', 'a13', 'a17', 'a01', 'a08'])
##                old = len(g.circuitsList)
##                if new != old:
##                    print(s,new,old)
##                    break
##                #fo.write('%d,%.5f,%.5f,%.5f\n' %(new,tnewMP,tnew,told))

            
        #print(g.circuits)
        #from csv import reader
        #g = RandomValuationDigraph()
        #g.showAll()
##        MP=False
##        from outrankingDigraphs import BipolarOutrankingDigraph
##        from randomPerfTabs import RandomCBPerformanceTableau
##        t1 = RandomCBPerformanceTableau(numberOfActions=10,seed=1)
####        t1.saveXMCDA2('testP2')
####        t1.showCriteria()
##        t2 = RandomCBPerformanceTableau(numberOfActions=10,seed=2)
####        t1.saveXMCDA2('testP2')
####        t1.showCriteria()
##        #t = XMCDA2PerformanceTableau('testP')
##        g1 = BipolarOutrankingDigraph(t1,Normalized=True,Threading=MP)
##        g2 = BipolarOutrankingDigraph(t2,Normalized=True,Threading=MP)
##        print(g1.computeOrdinalCorrelationMP(g2,Comments=True,nbrOfCPUs=4,Threading=MP))        
##        gcd = ~(-g)
##        gcd.computeChordlessCircuits(Odd=True,Comments=True)
##        gcd.showPreKernels()
##        g.computeRubisChoice(Comments=True)
##        g.showCriteria()
##        print(gcd.dompreKernels)
##        print(gcd.abspreKernels)
##        for ker in gcd.dompreKernels:
##            print(ker, gcd.computeGoodChoiceVector(ker,Comments=False))
##        for ker in gcd.abspreKernels:
##            print(ker, gcd.computeGoodChoiceVector(ker,Comments=False))
       

        print('*------------------*')
        print('If you see this line all tests were passed successfully :-)')
        print('Enjoy !')

    print('*************************************')
    print('* R.B. July 2018                    *')
    print('* $Revision: 2500+ $                *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: digraphs.py,v $
#
#############################
