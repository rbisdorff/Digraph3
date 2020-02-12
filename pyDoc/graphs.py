#!/usr/bin/env python3
"""
  Digraph3 graphs.py module
  Python3.3+ computing resources
  Copyright (C)  2011-2019 Raymond Bisdorff

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
#############################################
from decimal import Decimal

class Graph(object):
    """
    In the `graphs` module, the root :py:class:`graphs.Graph` class provides a generic graph model. A given object consists in:
    
       1. a vertices dictionary
       2. a characteristic valuation domain, {-1,0,+1} by default
       3. an edges dictionary, characterising each edge in the given valuation domain
       4. a gamma function dictionary, holding the neighborhood vertices of each vertex

    General structure::

       vertices = {'v1': {'name': ...,'shortName': ...},
                   'v2': {'name': ...,'shortName': ...},
                   'v3': {'name': ...,'shortName': ...},
                   ... }
       valuationDomain = {'min': -1, 'med': 0, 'max': 1}
       edges = {frozenset({'v1','v2'}): 1,
                frozenset({'v1','v3'}): 1,
                frozenset({'v2','v3'}): -1,
                  ...}
       ## links from each vertex to its neighbors
       gamma = {'v1': {'v2',v3'}, 'v2': {'v1'}, 'v3': {'v1'}, ... }
       
    Example python3 session:
       >>> from graphs import Graph
       >>> g = Graph(numberOfVertices=5,edgeProbability=0.5) # random instance
       >>> g.showShort()
       *----- show short --------------*
       *---- short description of the graph ----*
       Name             :  'random'
       Vertices         :  ['v1', 'v2', 'v3', 'v4', 'v5']
       Valuation domain :  {'med': 0, 'max': 1, 'min': -1}
       Gamma function   :
       v1 -> ['v4']
       v2 -> []
       v3 -> ['v4']
       v4 -> ['v1', 'v3']
       v5 -> []
       
    """
    def __repr__(self):
        """
        Default presentation method for Graph instances.
        """
        reprString = '*------- Graph instance description ------*\n'
        reprString += 'Instance class   : %s\n' % self.__class__.__name__
        reprString += 'Instance name    : %s\n' % self.name
        try:
            reprString += 'Seed             : %s\n' % str(self.seed)      
        except AttributeError:
            pass
        try:
            reprString += 'Edge Probability     : %s\n' % str(self.edgeProbability)      
        except AttributeError:
            pass
        reprString += 'Graph Order      : %d\n' % self.order
        try:
            reprString += 'Permutation      : %s\n' % str(self.permutation)
        except AttributeError:
            pass
        reprString += 'Graph Size       : %d\n' % self.computeSize()
        reprString += 'Valuation domain : [%.2f; %.2f]\n'\
                      % (self.valuationDomain['min'],self.valuationDomain['max'])
        reprString += 'Attributes       : %s\n' % list(self.__dict__.keys())
       
        return reprString

    def __init__(self, fileName=None, Empty=False, numberOfVertices=7, edgeProbability=0.5):
        """
        Constructor for Graph objects.
        """
        from decimal import Decimal
        
        if Empty:
            self.name = 'emptyInstance'
            self.vertices = dict()
            self.order = len(self.vertices)
            self.edges = dict()
            self.valuationDomain = {'min': Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
            self.gamma = dict()
            self.size = 0
        elif fileName==None:
            g = RandomGraph(order=numberOfVertices,\
                               edgeProbability=edgeProbability)
            self.name = g.name
            self.vertices = g.vertices
            self.order = len(self.vertices)
            self.edges = g.edges
            self.valuationDomain = g.valuationDomain
            self.size = self.computeSize()
            self.gamma = self.gammaSets()
        else:
            fileNameExt = fileName+'.py'
            argDict = {}
            exec(compile(open(fileNameExt).read(), fileNameExt, 'exec'),argDict)
            self.name = fileName
            self.vertices = argDict['vertices']
            self.order = len(self.vertices)
            self.valuationDomain = argDict['valuationDomain']
            self.edges = argDict['edges']
            self.size = self.computeSize()
            self.gamma = self.gammaSets()

    def __neg__(self):
        """
        Make the negation operator -self available for Graph instances.
        Returns a DualGraph instance of self.
        """
        new = DualGraph(self)
        new.__class__ = self.__class__
        return new

#-----------Dias/Castonguay/Longo/Jradi--------*
    def _degreeLabelling(self):
        """
        Inspired from Dias, Castonguay, Longo & Jradi,
        Algorithmica 2015, p 14
        """
        degree = {}
        color = {}
        for v in self.vertices:
            degree[v] = len(self.gamma[v])
            color[v] = 'white'
            
        labelling = {}
        for i in range(1,self.order+1):
            minDegree = self.order
            for x in self.vertices:
                if color[x] == 'white' and degree[x] < minDegree:
                    v = x
                    minDegree = degree[x]
            labelling[v] = i
            color[v] = 'black'
            #print(v,i,minDegree)
            for u in self.gamma[v]:
                if color[u] == 'white':
                    degree[u] -= 1

        self.labelling = labelling
        return labelling

    
    def _triplets(self,Comments=False):
        """
        p.15 Inspired from Dias, Castonguay, Longo & Jradi,
        Algorithmica 2015.
        """
    
        from itertools import product
        labelling = self.labelling
        tG = []
        cycles = set()
        for u in self.vertices:
            for x,y in product(self.gamma[u],repeat=2):
                if x != y:
##                    print(u,self.labelling[u],
##                          x,self.labelling[x],
##                          y,self.labelling[y])
                    if labelling[u] < labelling[x] and \
                       labelling[x] < labelling[y]:
##                    if u < x and x < y:
                        if self.edges[frozenset([x,y])] < self.valuationDomain['med']:
                            if Comments:
                                print('inital triple:',x,u,y)
                            tG.append((x,u,y))
                        else:
                            if Comments:
                                print('3-cycle:',x,u,y)
                            cycles.add((x,u,y))
        #self.tG = tG
        #self.cycles = cycles
        return tG,cycles

##    def _computeChordlessCyclesMP(self,Odd=False,\
##                                   Threading=False,nbrOfCPUs=None,\
##                                   Comments=False,Debug=False):
##        """ 
##        Multiprocessing version of computeChordlessCycles().
##        
##        Renders the set of all chordless odd cycless detected in an undirrected  graph.
##        Result (possible empty list) stored in <self.cyclesList>
##        holding a possibly empty list tuples with at position 0 the
##        list of adjacent actions of the circuit and at position 1
##        the set of actions in the stored circuit.
##        Inspired by Dias, Castonguay, Longo, Jradi, Algorithmica (2015).
##
##        Returns a possibly empty list of tuples (cycle,frozenset(cycle)).
##
##        If Odd == True, only cycless of odd length are retained in the result. 
##        """
##
##        tG,self.cyclesList = self._triplets(Comments=Comments)
##        if Comments:
##            print('There are %d starting triplets !' % len(tG) )
##        self.blocked = {}
##        if Threading:
##            self.Odd = Odd
##            self.Comments = Comments
##            from multiprocessing import Pool
##            from os import cpu_count
##            if nbrOfCPUs == None:
##                nbrOfCPUs= cpu_count()
##            with Pool(nbrOfCPUs) as proc:   
##                cycless = proc.map(self._computeChordlessPathsFromInitialTriplet,tG)
##                #print(circuits)
##            for i in range(len(tG)):
##                if Debug:
##                    print(i,cycles[i])
##                if cycles[i] != []:
##                    for c in cycles[i]:
##                        #print(circ)
##                        self.cyclesList.append(c)
##        else:
##            for p in tG:
##                u = p[1]
####                if Debug:
####                    print('===>>>',p,u)
##                gammaU = (self.gamma[u][1] | self.gamma[u][0])
##                for x in gammaU:
##                    #print(x)
##                    self.blocked[x] += 1
##                self.cyclesList.append(self._ccVisit(p,u,
##                                                  Odd=Odd,
##                                                  Comments=Comments))
##                for x in gammaU:
##                    if self.blocked[x] > 0:
##                        self.blocked[x] -= 1
##        if Debug:
##            print(self.cyclessList)
##        return self.cyclessList
##
##    def _computeChordlessPathsFromInitialTriplet(self,p,Debug=False):
##        if self.Comments:
##            print('===>> thread : ',p)
##        u = p[1]
##        blocked = {}
##        for x in self.actions:
##            blocked[x] = 0
##        circuits = []
##        gammaU = (self.gamma[u][1] | self.gamma[u][0])
##        for x in gammaU:
##            blocked[x] += 1
##        cycless,blocked = self._ccVisitMP(cycless,blocked,p,u,Odd=self.Odd,Comments=self.Comments)
##        for x in gammaU:
##            if blocked[x] > 0:
##                blocked[x] -= 1
##        if self.Comments:
##            print(p,cycless)
##        for x in self.actions:
##            if blocked[x] > 1:
##                blocked[x] = 0
##        if Debug:
##            print(p,'return',c<cless)
##        return cycless
##
##    def _ccVisitMP(self,cyless,blocked,p,u,
##                   Odd=False,Comments=False,Debug=False):
##        """ p.15 """
##        Med = self.valuationdomain['med']
##        ut = p[-1]
##        u1 = p[0]
##        inAsymGammaUt = self.gamma[ut][1] - self.gamma[ut][0]
##        gammaUt = self.gamma[ut][0] | self.gamma[ut][1]
##        if Debug:
##            print(p,self.gamma[ut][1],ut,self.gamma[ut][0])
##        for x in gammaUt:
##            blocked[x] += 1
##        for v in inAsymGammaUt:
##            if str(v) > str(u) and blocked[v] == 1:
##                p1 = p + tuple([v])
##                if Debug:
##                    print(p,p1)
##                if self.relation[u1][v] > Med and\
##                   self.relation[v][u1] <= Med:
##                    if Odd:
##                        if (len(p1) % 2) != 1:
##                            OddFlag=False
##                        else:
##                            OddFlag = True
##                    else:
##                        OddFlag = True
##                    if OddFlag:
##                        circ = list(reversed(p1))
##                        if Comments:
##                            print(p,'cycle certificate: ',circ)
##                        circuits.append((circ,frozenset(circ)))
##
##                elif self.relation[u1][v] <= Med and\
##                    self.relation[v][u1] <= Med :
##                    if Debug:
##                        print(p,'continue with ', p1)
##                    cycles,blocked = self._ccVisitMP(cycles,blocked,
##                                                    p1,u,Odd=Odd,
##                                                    Comments=Comments)
####                    circuits.append(circuits1)
##                    if Debug:
##                        print(p,cycles)
##        for x in (gammaUt):
##            if blocked[x] > 0:
##                blocked[x] -= 1
##
##        return cycles,blocked


    def computeChordlessCycles(self,Cycle3=False,Comments=False,Debug=False):
        """
        Renders the set of all chordless cycles observed in a Graph
        intance. Inspired from Dias, Castonguay, Longo & Jradi,
        Algorithmica 2015.

        .. note::

             By default, a chordless cycle must have at least length 4.If the Cycle3 flag is set to True,
             the cyclicly closed triplets will be inserted as 3-cycles in the result.
             
        """

        if Debug:
            Comments=True
        #self.visitedChordlessPathsNew = []
        self._degreeLabelling()
        triplets,cycles3 = self._triplets(Comments=Debug)
        if Comments:
            print('# of initial triplets:',len(triplets))
            print('# of 3-cycles        :',len(cycles3))
        if Cycle3:
            cycles = cycles3
        else:
            cycles = set()
            
        self.blocked = {}
        for u in self.vertices:
            self.blocked[u] = 0
        for p in triplets:
            if Comments:
                print(p,self.blocked)
            if Comments:
                print('===>>>', p)
            u = p[1]
            for x in self.gamma[u]:
                self.blocked[x] += 1
            cycles = self._ccVisit(p,cycles,u,Comments=Comments)
            for x in self.gamma[u]:
                if self.blocked[x] > 0:
                    self.blocked[x] -= 1
        return cycles

    def _ccVisit(self,p,cycles,u,Comments=False):
        """ p.15 """
        #labelling = self.labelling
        #self.visitedChordlessPathsNew.append(p)
        ut = p[-1]
        u1 = p[0]
##        if Comments:
##            print(p,u1,u,ut)
        for x in self.gamma[ut]:
            self.blocked[x] += 1

        for v in self.gamma[ut]:
            if self.labelling[v] > self.labelling[u] and self.blocked[v] == 1:
                p1 = p + tuple([v])
                if self.edges[frozenset([u1,v])] > self.valuationDomain['med']:
                    if Comments:
                        print('Cycle certificate: ', p1)
                    cycles.add(p1)
                else:
                    if Comments:
                        print('continue ...',p1)
                    cycles = self._ccVisit(p1,cycles,u,Comments=Comments)

        for x in self.gamma[ut]:
            if self.blocked[x] > 0:
                self.blocked[x] -= 1

        return cycles
        
            
#----------------------------------------

    def _chordlessPaths(self,Pk,v0,Cycle3=False,Comments=False,Debug=False):
        """
        recursice chordless precycle (len > 3) construction:
            Pk is the current pre chordless cycle
            v0 is the initial vertex of the precycle
            vn is the last vertex of the precycle
        """
        vn = Pk[-1]
        detectedChordlessCycle = False
        self.visitedChordlessPaths.add(frozenset(Pk))
        Med = self.valuationDomain['med']
        if Cycle3:
            minPreCycleLength = 2
        else: # only cycles of length 4 and more are holes in fact
            minPreCycleLength = 3
        #if len(e) > 1:
        if v0 != vn:
            # not a reflexive link
            e = frozenset([v0,vn])
            if self.edges[e] > Med and len(Pk) > 2:
                # we close the chordless pre cycle here
                detectedChordlessCycle = True
##                if Debug:
##                    print('Pk, len(Pk)', Pk, len(Pk))
                if len(Pk) > minPreCycleLength:
                    # only cycles of length 4 and more are holes in fact
                    self.xCC.append(Pk)
                    Pk.append(v0)
                    if Comments:
                        print('Chordless cycle certificate -->>> ', Pk)
                return detectedChordlessCycle
        if detectedChordlessCycle == False:
            NBvn = set(self.gamma[vn]) - set(Pk[1:len(Pk)])
            # exterior neighborhood of vn

##            if Debug:
##                print('vn, NBvn, Pk, Pk[1:len(Pk)] = ', vn, NBvn, Pk, Pk[1:len(Pk)])
            #while NBvn != set():
            for v in NBvn:
                # we try in turn all neighbours of vn
                #v = NBvn.pop()
                vCP = set(Pk)
                vCP.add(v)
                vCP = frozenset(vCP)
##                if Debug:
##                    print('v,vCP  =', v,vCP)
                if vCP not in self.visitedChordlessPaths:
                    # test history of paths
                    P = list(Pk)
##                    if Debug:
##                        print('P,P[:-1] = ', P,P[:-1])
                    noChord = True
                    for x in P[:-1]:
##                        if Debug:
##                            print('x = ', x)
                        if x != v0:
                            # we avoid the initial vertex
                            # to stay with a chordless precycle
                            ex = frozenset([x,v])
##                            if Debug:
##                                print('x, v, ex = ',x,v,ex)
                            if self.edges[ex] > Med:
                                # there is a chord
                                noChord = False
                                break
                    if noChord:
                        P.append(v)
##                        if Debug:
##                            print('P,v0',P,v0)
                        if self._chordlessPaths(P,v0,Cycle3=Cycle3,Comments=Comments,Debug=Debug):
                            # we continue with the current chordless precycle
                            detectedChordlessCycle=True
##            if Debug:
##                print('No further chordless precycles from ',vn,' to ',v0)
        return detectedChordlessCycle

    def _MISgen(self,S,I):
        """
        generator of maximal independent choices (voir Byskov 2004):
            * S ::= remaining nodes;
            * I ::= current independent choice

        .. note::

            - Initialize self.misset = set() before using !    
            - Inititalize S with a set of vertex keys, and I with an empty set.
            - See self.showMIS() for usage instructions.
            
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
            Sv = S - (self.gamma[v])
            Iv = I | set([v])
            for choice in self._MISgen(Sv,Iv):
                yield choice
            for choice in self._MISgen(S,I):
                yield choice

    def _saveEdges(self,fileName='graphEdges',Agrum=False,Decimal=True):
        """
        Saving graph instances as list of edges, ie node node on each line
        for enumChordlessCycles C++/agrum progam.
        """
        print('*--- Saving graph edges in file: <' + fileName + '.text> ---*')
        verticesKeys = [x for x in self.vertices]
        verticesKeys.sort()
        Med = self.valuationDomain['med']
        fileNameExt = str(fileName)+str('.text')
        fo = open(fileNameExt, 'w')
        for i in range( len(verticesKeys) ):
            for j in range(i+1, len(verticesKeys)):
                if self.edges[frozenset([verticesKeys[i],verticesKeys[j]])] > Med:
                    if Agrum:
                        fo.write('%d %d\n' % ( i+1, j+1 )  )
                    else:
                        fo.write('%s %s\n' % ( str(verticesKeys[i]),str(verticesKeys[j]) )  )
        fo.close()

    def _singletons(self):
        """
        List of singletons in frozenset format with neighborhood
        and not neighbourhood sets.
        """
        s = []
        vertices = set([x for x in self.vertices])
        for x in vertices:
            indep = vertices - (self.gamma[x])
            s = s + [(frozenset([x]),self.gamma[x],indep)]
        return s

    def _computeChordlessCycles(self,Cycle3=False,Comments=True,Debug=False):
        """
        Renders the set of all chordless cycles observed in a Graph
        intance. Obsolete home brewed version.
        """
        verticesKeys = [x for x in self.vertices]
        self.visitedChordlessPaths = set()
        chordlessCycles = []
        for v in verticesKeys:
            P = [v]
            self.xCC = []
            if self._chordlessPaths(P,v,Cycle3=Cycle3,Comments=Comments,Debug=Debug):
                chordlessCycles += self.xCC
        self.chordlessCycles = chordlessCycles
        chordlessCyclesList = [ (x,frozenset(x)) for x in chordlessCycles]
        if Debug:
            print('Return list of chordless cycles as a tuple (path, set)')
            for cc in chordlessCyclesList:
                print(cc)
        return chordlessCyclesList

    def computeCliques(self,Comments=False):
        """
        Computes all cliques, ie maximal complete subgraphs in self:

        .. Note::

            - Computes the maximal independent vertex sets in the dual of self.
            - Result is stored in self.cliques.

        """
        import time,copy
        if Comments:
            print('*---  Maximal Cliques ---*')
        t0 = time.time()
        dualSelf = -self
        dualSelf.misset = set()
        vertices = set([x for x in self.vertices])
        self.cliques = [m[0] for m in dualSelf.generateIndependent(dualSelf._singletons()) if m[0] == m[2]]
        t1 = time.time()
        n = len(vertices)
        v = [0 for i in range(n+1)] 
        cliqueList = [(len(clique),clique) for clique in self.cliques]
        cliqueList.sort()
        for clq in cliqueList:  # clq = (len(clique),clique)
            clique = list(clq[1])
            clique.sort()
            print(clique)
            v[clq[0]] += 1
            cliqueNumber = clq[0]
        self.cliqueNumber= cliqueNumber
        if Comments:  
            print('number of solutions: ', len(self.cliques))
            print('cardinality distribution')
            print('card.: ', list(range(n+1)))
            print('freq.: ', v)
            print('clique Number: ', cliqueNumber)
            print('execution time: %.5f sec.' % (t1-t0))
            print('Results in self.cliques')

    def computeComponents(self):
        """
        Computes the connected components of a graph instance.
        Returns a partition of the vertices as a list
        """
        components = []
        dfs = self.depthFirstSearch()
        for tree in dfs:
            components.append(set(tree))
        return components
    
    def computeDegreeDistribution(self,Comments=False):
        """
        Renders the distribution of vertex degrees.
        """
        degreeDistribution = [0 for i in range(self.order)]
        for v in self.vertices:
            dv = len(self.gamma[v])
            degreeDistribution[dv] += 1
        if Comments:
            print('degrees      : ', list(range(self.order)))
            print('distribution : ', degreeDistribution)
        return degreeDistribution

    def computeDiameter(self, Oriented = False):
        """
        Renders the diameter (maximal neighbourhood depth) of the digraph instance.

        .. Note::

            The diameter of a disconnected graph is considered to be *infinite*
            (results in a value -1) !
            
        """
        order = self.order
        nbDepths = self.computeNeighbourhoodDepthDistribution()
        nbDepths.reverse()
        if nbDepths[0] != 0:
            diameter = -1
        else:
            diameter = 0
            for i in range(len(nbDepths)):
                if nbDepths[i+1] != 0:
                    diameter = order - (i+1)
                    break
        return diameter                       

    def computeGirth(self,girthType="any",Comments=False):
        """
        Renders the *girth* of self, i.e. the length of the shortest chordless cycle in the graph.

        *Parameter*:
            * *girthType* = "any" (default) | "odd" | "even"

        """
        cycles = self.computeChordlessCycles()
        if Comments:
            print(cycles)
        girth = self.order + 1
        for c in cycles:
            nc = len(c)
            if Comments:
                print(nc,c)
            if girthType == "odd":
                if nc % 2 == 1 and nc < girth:
                    girth = nc
            elif girthType == "even":
                if nc % 2 == 0 and nc < girth:
                    girth = nc
            else:
                if nc < girth:
                    girth = nc
        if girth == self.order + 1:
            if Comments:
                if girthType == "any":
                    print('the graph %s has no cycles' % (self.name))
                else:
                    print('the graph %s has no %s cycles' % (self.name,girthType))
                return
        if girthType == "odd":
            self.oddGirth = girth
            if Comments:
                print('odd girth = %d' % girth)
        elif girthType == "even":
            self.evenGirth = girth
            if Comments:
                print('even girth = %d' % girth)
        else:
            self.girth = girth
            if Comments:
                print('girth = %d' % girth)
        return girth
                
    def computeMaximumMatching(self,Comments=False):
        """
        Renders a maximum matching in *self* by computing
        a maximum MIS of the line graph of *self*.
        """
        from graphs import LineGraph
        ls = LineGraph(self)
        ls.computeMIS()
        matchings = [(len(mis),mis) for mis in ls.misset]
        ms = sorted(matchings,reverse=True)
        if Comments:
            for mis in ms:
                print(mis)
        return ms[0][1] # skipping the length argument

    def computeMIS(self,Comments=False):
        """
        Prints all maximal independent vertex sets:

        .. Note::
        
            - Result is stored in self.misset !

        """
        import time
        if Comments:
            print('*---  Maximal Independent Sets ---*')
        t0 = time.time()
        self.misset = set()
        vertices = set([x for x in self.vertices])
        self.misset = [m[0] for m in self.generateIndependent(self._singletons()) if m[0] == m[2]]
        t1 = time.time()
        n = len(vertices)
        v = [0 for i in range(n+1)] 
        misList = [(len(mis),mis) for mis in self.misset]
        misList.sort()
        #print(misList)
        for m in misList: # m = (len(mis),mis))
            mis = list(m[1])
            mis.sort()
            print(mis)
            v[m[0]] += 1
            stabilityNumber = m[0]
        self.stabilityNumber = stabilityNumber
        if Comments:
            print('number of solutions: ', len(misList))
            print('cardinality distribution')
            print('card.: ', list(range(n+1)))
            print('freq.: ', v)
            print('stability number : ', stabilityNumber)
            print('execution time: %.5f sec.' % (t1-t0))
            print('Results in self.misset')

    def computeNeighbourhoodDepth(self,vertex,Debug=False):
        """
        Renders the distribtion of neighbourhood depths.
        """
        import copy
        order = self.order
        vertices = set([x for x in self.vertices])
        if Debug:
            print('-->',vertex)
        nbx = 0
        neighbx = set([vertex])
        restVertices = vertices - neighbx
        while restVertices != set() and nbx < order:
            if Debug:
                print('nbx,restVertices', nbx,restVertices)
            nbx += 1
            iterneighbx = copy.copy(neighbx)
            for y in iterneighbx:
                neighbx = neighbx | self.gamma[y]
                if Debug:
                    print('y,self.gamma[y],neighbx', y,self.gamma[y],neighbx)
            restVertices = vertices - neighbx
        if Debug:
            print('nbx,restVertices',nbx,restVertices)
        if restVertices != set():
            return order
        else:
            return nbx

    def computeNeighbourhoodDepthDistribution(self,Comments=False,Debug=False):
        """
        Renders the distribtion of neighbourhood depths.
        """
        import copy
        vertices = set([x for x in self.vertices])
        order = self.order
        vecNeighbourhoodDepth = [0 for i in range(order+1)] 
        for x in vertices:
            if Debug:
                print('-->',x)
            nbx = 0
            neighbx = set([x])
            restVertices = vertices - neighbx
            while restVertices != set() and nbx < order:
                if Debug:
                    print('nbx,restVertices', nbx,restVertices)
                nbx += 1
                iterneighbx = copy.copy(neighbx)
                for y in iterneighbx:
                    neighbx = neighbx | self.gamma[y]
                    if Debug:
                        print('y,self.gamma[y],neighbx', y,self.gamma[y],neighbx)
                restVertices = vertices - neighbx
            if Debug:
                print('nbx,restVertices',nbx,restVertices)
            if restVertices != set():
                vecNeighbourhoodDepth[order] += 1
            else:
                vecNeighbourhoodDepth[nbx] += 1
        if Comments:
            depths = list(range(self.order))
            depths.append('inf.')
            print('nbh depths   : ', depths)
            print('distribution : ', vecNeighbourhoodDepth)

        return vecNeighbourhoodDepth

    def computeOrientedDigraph(self,PartiallyDetermined=False):
        """
        Renders a digraph where each edge of the permutation graph *self*
        is converted into an arc oriented in increasing order of the adjacent vertices' numbers.
        If self is a PermutationGraph instance, the orientation will be transitive.

        The parameter *PartiallyDetermined*: {True|False by default], converts if *True* all absent
        edges of the graph into indeterminate symmetric relations in the resulting digraph.
     
        >>> g = RandomGraph(order=6,seed=101)
        >>> dg = g.computeOrientedDigraph()
        >>> dg
        *------- Digraph instance description ------*
        Instance class   : Digraph
        Instance name    : oriented_randomGraph
        Digraph Order      : 6
        Digraph Size       : 5
        Valuation domain : [-1.00; 1.00]
        Determinateness  : 100.000
        Attributes       : ['name','order','actions','valuationdomain',
                            'relation', 'gamma', 'notGamma',
                            'size', 'transitivityDegree']
        >>> dg.tansitivityDegree
        Decimal('0.7142857142857142857142857143')
        
        """
        from digraphs import Digraph, EmptyDigraph
        from copy import deepcopy
        
        g = EmptyDigraph(order=self.order)
        g.__class__ = Digraph
        g.name = 'oriented_'+self.name
        g.actions = deepcopy(self.vertices)
        g.valuationdomain = deepcopy(self.valuationDomain)
        Max = g.valuationdomain['max']
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        relation = {}
        actionKeysList = [a for a in g.actions]
        for x in actionKeysList:
            relation[x] = {}
            for y in actionKeysList:
                relation[x][y] = Med
        n = len(actionKeysList)
        for i in range(n):
            x = actionKeysList[i]
            relation[x][x] = Med
            for j in range(i+1,n):
                y = actionKeysList[j]
                if self.edges[frozenset([x,y])] > Med:
                        relation[x][y] = Max
                        relation[y][x] = Min
                elif self.edges[frozenset([x,y])] < Med:
                    relation[x][y] = Min
                    relation[y][x] = Min
                else:
                    relation[x][y] = Med
                    relation[y][x] = Med
                        
        if PartiallyDetermined:
            for i in range(n):
                x = actionKeysList[i]
                for j in range(i+1,n):
                    y = actionKeysList[j]
                    if relation[x][y] < Med and relation[y][x] < Med:
                        relation[x][y] = Med
                        relation[y][x] = Med
                        
        g.relation = relation
        g.size = g.computeSize()
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        g.transitivityDegree = g.computeTransitivityDegree()
        return g

    def computeTransitivelyOrientedDigraph(self,PartiallyDetermined=False,Debug=False):
        """
        Renders a digraph where each edge of the permutation graph *self*
        is converted into an arc oriented in increasing order of the ranks of implication classes
        detected with the :py:func:`digraphs.Digraph.isComparabilityGraph` test and stored in self.edgeOrientations.

        The parameter *PartiallyDetermined*: {True|False (by default), converts if *True* all absent
        edges of the graph into indeterminate symmetric relations in the resulting digraph.
        Verifies if the graph instance is a comparability graph.
        
        *Source*: M. Ch. Golumbic (2004) Algorithmic Graph Thery and Perfect Graphs,
        Annals of Discrete Mathematics 57, Elsevier, p. 129-132.
     
        >>> g = RandomGraph(order=6,edgeProbability=0.5,seed=100)
        >>> og = g.computeTransitivelyOrientedDigraph()
        >>> if og != None:
        ...     print(og)
        ...     print('Transitivity degree: %.3f' % og.transitivityDegree)
        *------- Digraph instance description ------*
        Instance class   : TransitiveDigraph
        Instance name    : trans_oriented_randomGraph
        Digraph Order      : 6
        Digraph Size       : 7
        Valuation domain : [-1.00 - 1.00]
        Determinateness  : 46.667
        Attributes       : ['name', 'order', 'actions', 'valuationdomain', 'relation',
                           'gamma', 'notGamma', 'size', 'transitivityDegree']
        Transitivity degree: 1.000
        >>> gd = -g
        >>> ogd = gd.computeTransitivelyOrientedDigraph()
        >>> if ogd != None:
        ...     print(odg)
        ...     print('Dual transitivity degree: %.3f' % ogd.transitivityDegree)
        *------- Digraph instance description ------*
        Instance class   : TransitiveOrder
        Instance name    : trans_oriented_dual_randomGraph
        Digraph Order      : 6
        Digraph Size       : 8
        Valuation domain : [-1.00 - 1.00]
        Determinateness  : 53.333
        Attributes       : ['name', 'order', 'actions', 'valuationdomain', 'relation',
                            'gamma', 'notGamma', 'size', 'transitivityDegree']
        Dual transitivity degree: 1.000
        """
        from digraphs import EmptyDigraph
        from transitiveDigraphs import TransitiveDigraph
        from copy import deepcopy

        if not self.isComparabilityGraph():
            print('The graph %s does not admit a transitive orientation.' % self.name)
        else:
            if Debug:
                for arc in self.edgeOrientations:
                    print(arc, self.edgeOrientations[arc])
            g = EmptyDigraph(order=self.order)
            g.__class__ = TransitiveDigraph
            g.name = 'trans_oriented_'+self.name
            g.actions = deepcopy(self.vertices)
            g.valuationdomain = deepcopy(self.valuationDomain)
            Max = g.valuationdomain['max']
            Min = g.valuationdomain['min']
            Med = g.valuationdomain['med']
            relation = {}
            actionKeysList = [a for a in g.actions]
            for x in actionKeysList:
                relation[x] = {}
                for y in actionKeysList:
                    relation[x][y] = Med
            n = len(actionKeysList)
            for i in range(n):
                x = actionKeysList[i]
                relation[x][x] = Med
                for j in range(n):
                    y = actionKeysList[j]
                    if self.edgeOrientations[x,y] > 0:
                            relation[x][y] = Max
                    elif self.edgeOrientations[x,y] < 0:
                        relation[x][y] = Min
                    else:
                        relation[x][y] = Med            
            if PartiallyDetermined:
                for i in range(n):
                    x = actionKeysList[i]
                    for j in range(i+1,n):
                        y = actionKeysList[j]
                        if relation[x][y] < Med and relation[y][x] < Med:
                            relation[x][y] = Med
                            relation[y][x] = Med
            g.relation = relation
            g.closeTransitive()
            g.size = g.computeSize()
            g.gamma = g.gammaSets()
            g.notGamma = g.notGammaSets()
            g.transitivityDegree = g.computeTransitivityDegree()
            return g


    def computePermutation(self,seq1=None,seq2=None,Comments=True):
        """
        Tests whether the graph instance *self* is a permutation graph
        and renders, in case the test is positive,
        the corresponding permutation.
        """
        from digraphs import FusionDigraph
        if seq1 == None or seq2 == None:
            og = self.computeTransitivelyOrientedDigraph(PartiallyDetermined=True)
            odt = og.computeTransitivityDegree()
            if odt < Decimal('1'):
                if Comments:
                    print('Transitivity degree %.3f < 1' % odt)
                    print('The graph instance is not a permutation graph')
                return
            gd = -self
            ogd = gd.computeTransitivelyOrientedDigraph(PartiallyDetermined=True)
            ogdt = ogd.computeTransitivityDegree()
            if ogdt < Decimal('1'):
                if Comments:
                    print('Dual transitivity degree %.3f < 1' % ogdt)
                    print('The graph instance is not a permutation graph')
                return
            
            f1 = FusionDigraph(og,ogd,'o-max')
            f2 = FusionDigraph((-og),ogd,'o-max')
            seq1 = f1.computeCopelandRanking()
            if Comments:
                print(seq1)
            seq2 = f2.computeCopelandRanking()
            if Comments:
                print(seq2)
        permutation = [0 for j in range(self.order)]
        for j in range(self.order):
            permutation[seq2.index(seq1[j])] = j+1
        return permutation

    def computeSize(self):
        """
        Renders the number of positively characterised edges of this graph instance
        (result is stored in self.size).
        """
        size = 0
        Med = self.valuationDomain['med']
        for edge in self.edges:
            if self.edges[edge] > Med:
                size += 1
        self.size = size
        return size

    def breadthFirstSearch(self,s,alphabeticOrder=True,Warnings=True,Debug=False):
        """
        Breadth first search through a graph in lexicographical order
        of the vertex keys.

        Renders a list of vertice keys in
        increasing distance from the origin *s*. Ties in the distances
        are resolved by alphabetic ordering of the vertice keys.

        A warning is issued when the graph is not connected and the resulting
        search does not cover the whole set of graph vertices. 

        Source: Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* 2d Ed., MIT Press 2001.
        """
        vertices = self.vertices
        components = self.computeComponents()
        if Debug:
            print(components)
        for comp in components:
            if s in comp:
                verticesKeys = [x for x in comp]
                if alphabeticOrder:
                    verticesKeys.sort()
                nv = len(vertices)
                verticesKeys.remove(s)
                color = {}
                bfsDepth = {}
                parent = {}
                for x in verticesKeys:
                    color[x] = 0
                    bfsDepth[x] = nv
                    parent[x] = None
                color[s] = 1
                bfsDepth[s] = 0
                parent[s] = None
                if Debug:
                    print(color,bfsDepth,parent)
                F = [s]
                while F != []:
                    u = F.pop()
                    F.append(u)
                    for v in self.gamma[u]:
                        if color[v] == 0:
                            color[v] = 1
                            bfsDepth[v] = bfsDepth[u] + 1
                            parent[v] = u
                            F.append(v)
                        if Debug:
                            print('u,v,F',u,v,F)
                    F.remove(u)
                    color[u] = 2
                if Debug:
                    print(color,bfsDepth,parent)
                bfs = [(bfsDepth[v],v) for v in comp]
                bfs.sort()
                self.bfs = [x[1] for x in bfs]
                self.bfsDepth = bfsDepth
                return self.bfs
            else:
                if Warnings:
                    print('Warning: graph %s is not connected!' % self.name)
                    print('Not with %s connected vertices: %s' % (s,str(comp)) )
                                
    def depthFirstSearch(self,Debug=False):
        """
        Depth first search through a graph in lexicographical order
        of the vertex keys.
        """
        def _visitVertex(self, x, Debug = False):
            """
            Visits all followers of vertex x.
            """
            self.vertices[x]['color'] = 1
            ## self.date += 1
            self.vertices[x]['startDate'] = self.date
            self._dfsx.append(x)
            if Debug:
                print(' dfs %s, date = %d' % (str(self.dfs),  self.vertices[x]['startDate']))
            nextVertices = [y for y in self.gamma[x]]
            nextVertices.sort()
            if Debug:
                print('   next ', nextVertices)
            for y in nextVertices:
                if self.vertices[y]['color'] == 0:
                    self.date += 1
                    _visitVertex(self,y, Debug = Debug)
                    if self.vertices[x]['color'] == 1:
                        self._dfsx.append(x)
            self.vertices[x]['color'] = 2
            self.vertices[x]['endDate'] = self.date
            self.date += 1

        def _visitAllVertices(self, Debug=False):
            """
            Mark the starting date for all vertices
            and controls the progress of the search with vertices colors:
            White (0), Grey (1), Black (2)

            Stores the depth first search path in the *self.dfs* attribute
            and returns it.
            """
            self.dfs = []
            for x in self.vertices:
                self.vertices[x]['color'] = 0
            self.date = 0
            verticesList = [x for x in self.vertices]
            verticesList.sort()
            for x in verticesList:
                self._dfsx = []
                if self.vertices[x]['color'] == 0:
                    if Debug:
                        print('==>> Starting from %s ' % x)
                    _visitVertex(self, x, Debug = Debug)
                    self.dfs.append(self._dfsx)
                #self.vertices[x]['color'] = 2
                #self.vertices[x]['endDate'] = self.date


        # ---- main -----
        _visitAllVertices(self, Debug=Debug)
        return self.dfs

    def exportGraphViz(self,fileName=None,verticesSubset=None,
                       Comments=True,
                       graphType='png',graphSize='7,7',
                       WithSpanningTree=False,
                       WithVertexColoring=False,
                       matching=None,
                       layout=None,
                       arcColor='black',
                       lineWidth=1):
        """
        Exports GraphViz dot file  for graph drawing filtering.

        Example:
           >>> g = Graph(numberOfVertices=5,edgeProbability=0.3)
           >>> g.exportGraphViz('randomGraph'))

        .. image:: randomGraph.png
           :alt: Random graph
           :width: 300 px
           :align: center
        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        if verticesSubset == None:
            vertexkeys = [x for x in self.vertices]
        else:
            vertexkeys = [x for x in verticesSubset]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            if WithVertexColoring:
                node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
                node += ', style = "filled", color = %s' \
                 % self.vertices[vertexkeys[i]]['color']
            else:
                node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            try:
                if self.vertices[vertexkeys[i]]['spin'] == 1:
                    node += ', style = "filled", color = %s' % spinColor
            except:
                pass
            node += '];\n'                
            fo.write(node)
        if WithSpanningTree:
            try:
                dfs = self.dfs
            except:
                print('no spanning tree yet computed. Run self.randomDepthFirstSearch() !')
            edgesColored = set()
            print(dfs)
            for tree in dfs:
                for i in range((len(tree)-1)):
                    #print(i,tree[i],tree[i+1])
                    edgesColored.add(frozenset([tree[i],tree[i+1]]))
            #print('Spanning tree: ', edgesColored)
                    
        if matching != None:
            withMatching = True
            edgesColored = set()
            for edge in matching:
                edgesColored.add(edge)
            print('Matching: ', edgesColored)
        else:
            withMatching = False
        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    edge = 'n'+str(i+1)
                    if edges[frozenset( [vertexkeys[i], vertexkeys[j]])] > Med:
                        if WithSpanningTree and \
                        frozenset( [vertexkeys[i], vertexkeys[j]]) in edgesColored:
                               arrowFormat = \
        ' [dir=both,style="setlinewidth(3)",color=red, arrowhead=none, arrowtail=none] ;\n'                                          
                        elif withMatching and \
                        frozenset( [vertexkeys[i], vertexkeys[j]]) in edgesColored:
                               arrowFormat = \
        ' [dir=both,style="setlinewidth(3)",color=red, arrowhead=none, arrowtail=none] ;\n'                                          
                        else:
                            arrowFormat = \
        ' [dir=both,style="setlinewidth(%d)",color=%s, arrowhead=none, arrowtail=none] ;\n' % (lineWidth,arcColor)
                        edge0 = edge+'-- n'+str(j+1)+arrowFormat
                        fo.write(edge0)
                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
                        edge0 = edge+'-- n'+str(j+1)+\
            ' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        # choose layout model 
        if isinstance(self,(GridGraph,TriangulatedGrid,RandomTree)):
            if layout == None:
                layout = 'neato'
        elif isinstance(self,(CycleGraph)):
            if layout == None:
                layout = 'circo'
        else:
            if layout == None:
                layout = 'fdp'
            
        commandString = layout+' -T'+graphType+' '+dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                print('On Ubuntu: ..$ sudo apt-get install graphviz')

    def exportEdgeOrientationsGraphViz(self,fileName=None,verticesSubset=None,
                       Comments=True,
                       graphType='png',graphSize='7,7',
                       layout=None,
                       arcColor='black',
                       lineWidth=1,
                        palette=1,
                        Debug=False):
        """
        Exports GraphViz dot file for oriented graph drawing filtering.

        Example:
           >>> from graphs import *
           >>> g = RandomGraph(order=6,seed=100)
           >>> if g.isComparavbilityGraph():
           ...     g.exportEdgeOrientationGraphViz('orientedGraph')

        .. image:: orientedGraph.png
           :alt: Random graph
           :width: 300 px
           :align: center
        """
        import os
        if Debug:
            Comments=True
        try:
            edgeOrientations = self.edgeOrientations
        except AttributeError:
            if not self.isComparabilityGraph():
                print('The graph %s is not transitively orientable' % self.name)
            return

        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        if verticesSubset == None:
            vertexkeys = [x for x in self.vertices]
        else:
            vertexkeys = [x for x in verticesSubset]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            node += '];\n'                
            fo.write(node)

        # reminder include a color palette in digraphsToold
        from digraphsTools import colorPalettes
##        colors0 = ['black',
##                  'blue',
##                  'coral',
##                  'gold',
##                  'gray',
##                  'black',
##                  'pink',
##                  'green',
##                  'orange',
##                  'skyblue',
##                  'wheat',
##                  'salmon']    
##        colors1 = ['#EA2027',
##                  '#006266',
##                  '#1B1464',
##                  '#5758BB',
##                  '#6F1E51',
##                  '#EE5A24',
##                  '#009432',
##                  '#0652DD',
##                  '#9980FA',
##                  '#833471',
##                  '#F79F1F',
##                  '#A3CB38',
##                   '#1289A7',
##                   '#D980FA',
##                   '#B53471',
##                   '#FFC312',
##                   '#C4E538',
##                   '#12CBC4',
##                   '#FDA7DF',
##                   '#ED4C67',
##                   ]
        colors = colorPalettes[palette]
        edgeColors = {}
        for edge in self.edges:
            if edges[edge] > Med:
                arc = tuple(sorted([v for v in edge]))
                edgeColors[arc] = colors[abs(edgeOrientations[arc])]
        if Debug:
            print(self.edgeOrientations)
            print(edgeColors)    

        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    edge = 'n'+str(i+1)
                    edgeKey = frozenset([vertexkeys[i], vertexkeys[j]])
                    if edges[edgeKey] > Med:
                        arc = tuple(sorted([v for v in edgeKey]))
                        arcColor = edgeColors[arc]
                        if Debug:
                            print(arcColor,lineWidth)
                        if edgeOrientations[arc] > 0:
                            arrowFormat = \
        ' [dir=forward,style="setlinewidth(%d)",color="%s", arrowhead=normal, arrowtail=none] ;\n' %\
                     (lineWidth,arcColor)
                        elif edgeOrientations[arc] < 0:
                            arrowFormat = \
        ' [dir=back,style="setlinewidth(%d)",color="%s", arrowhead=none, arrowtail=normal] ;\n' %\
                     (lineWidth,arcColor)
                        edge0 = edge+'-- n'+str(j+1)+arrowFormat
                        fo.write(edge0)                    
##                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
##                        edge0 = edge+'-- n'+str(j+1)+\
##            ' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
##                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        # choose layout model 
        if layout == None:
            layout = 'fdp'
            
        commandString = layout+' -T'+graphType+' '+dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                print('On Ubuntu: ..$ sudo apt-get install graphviz')


    def exportPermutationGraphViz(self,fileName=None,
                       permutation=None,
                       Comments=True,
                       WithEdgeColoring=True,
                       hspace=100,
                       vspace=70,
                       graphType='png',graphSize='7,7',
                       arcColor='black',
                       lineWidth=1):
        """
        Exports GraphViz dot file for permutation drawing filtering.

        Horizontal (default=100) and vertical (default=75) spaces betwen the vertices'
        positions may be explicitely given in *hspace* and *vspace* parameters.

        .. note::
            If no *permutation* is provided, it is supposed to exist a self.permutation attribute.
            
        """
        import os
                # inversions drawing
        if permutation == None:
            try:
                permutation = self.permutation
            except AttributeError:
                print('No permutation available !!')
                return
        colors = {'gold':'gold',
                  'lightblue':'blue',
                  'lightcoral':'coral',
                  'lightyellow':'yellow',
                  'orange':'orange',
                  'gray':'black',
                  'lightpink':'pink',
                  'seagreen1':'green',
                  'skyblue':'skyblue',
                  'wheat1':'wheat',
                  'lightsalmon':'salmon'}
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        vertexkeys = [x for x in self.vertices]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = 'perm_'+self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        fo = open(dotName,'w')
        fo.write('strict digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        # horizontally positioned initial nodes at line 100
        # horinzontal space = 75
        vspace = 100
        hspace = 60
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            try:
                if self.vertices[vertexkeys[i]]['spin'] == 1:
                    node += ', style = "filled", color = %s, ' % spinColor
            except:
                pass
            node += 'pos="%d,%d"];\n' % (i*hspace,vspace)                
            fo.write(node)
        # horizontally positionned terminal nodes at line 0
        for i in range(n):
            k = permutation[i]-1
            try:
                nodeName = str(self.vertices[vertexkeys[k]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[k]]['name']
                except:
                    nodeName = str(vertexkeys[k])
            node = 'n'+str(n+k+1)+' [shape = "circle", label = "' +nodeName+'"'
            try:
                if self.vertices[vertexkeys[k]]['spin'] == 1:
                    node += ', style = "filled", color = %s, ' % spinColor
            except:
                pass
            node += 'pos="%d,%d"];\n' % (i*hspace,0)                
            fo.write(node)
        for i in range(n):
            edge = 'n'+str(i+1)
            if WithEdgeColoring:
                try:
                    colorKey = self.vertices[vertexkeys[i]]['color']
                except KeyError:
                    self.computeMinimalVertexColoring()
                    colorKey = self.vertices[vertexkeys[i]]['color']
                arrowFormat = \
                        edge0 = edge+'-> n'+str(n+i+1) +\
                ' [dir=both, color=%s, style="setlinewidth(2)",\
                              arrowhead=none, arrowtail=none] ;\n'\
                    % colors[colorKey]
##                except KeyError:
##                    arrowFormat = \
##                       edge0 = edge+'-> n'+str(n+i+1) +\
##                ' [dir=both, color=black, arrowhead=none, arrowtail=none] ;\n'
            else:
                arrowFormat = \
                        edge0 = edge+'-> n'+str(n+i+1) +\
                ' [dir=both, color=black, arrowhead=none, arrowtail=none] ;\n'    
            fo.write(edge0)
        fo.write('}\n')
        fo.close()
        # choose layout model 
        layout = 'neato'
        commandString = layout+' -n -T'+graphType+' '+dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                print('On Ubuntu: ..$ sudo apt-get install graphviz')

    def gammaSets(self,Debug=False):
        """
        renders the gamma function as dictionary
        """
        vkeys = [x for x in self.vertices]
        if Debug:
            print('vkeys', vkeys)
        edges = self.edges
        gamma = dict()
        for v in vkeys:
            gamma[v] = set()
        for e in edges:
            if edges[e] > 0:
##                if Debug:
##                    print('e', e)
                pair = set(e)
                e1 = pair.pop()
                e2 = pair.pop()
                gamma[e1].add(e2)
                gamma[e2].add(e1)
        return gamma

    def generateIndependent(self,U):
        """
        Generator for all independent vertices sets
        with neighborhoods of a graph instance:

        .. note::
        
               * Initiate with U = self._singletons().
               * Yields [independent set, covered set, all vertices - covered set)].
               * If independent set == (all vertices - covered set), the given independent set is maximal !

        """
        if U == []:
            vertices = set([x for x in self.vertices])
            yield [frozenset(),set(),vertices]
        else:
            x = list(U.pop())
            for S in self.generateIndependent(U):
                yield S
                if x[0] <=  S[2]:
                    Sxgam = S[1] | x[1]
                    Sxindep = S[2] &  x[2]
                    Sxchoice = S[0] | x[0]
                    Sx = [Sxchoice,Sxgam,Sxindep]
                    yield Sx


                 
    def graph2Digraph(self):
        """
        Converts a Graph object into a symmetric Digraph object.
        """
        from copy import deepcopy
        from digraphs import Digraph, EmptyDigraph
        dg = EmptyDigraph(order=self.order)
        dg.__class__ = Digraph
        dg.name = deepcopy(self.name)
        dg.actions = deepcopy(self.vertices)
        dg.order = len(dg.actions)
        dg.valuationdomain = deepcopy(self.valuationDomain)
        dg.convertValuationToDecimal()
        dg.relations = {}
        actionsKeys = [x for x in dg.actions]
        for x in actionsKeys:
            dg.relation[x] = {}
            for y in actionsKeys:
                if x == y:
                    dg.relation[x][y] = dg.valuationdomain['med']
                else:
                    edgeKey = frozenset([x,y])
                    dg.relation[x][y] = self.edges[edgeKey]
        dg.convertRelationToDecimal()
        dg.gamma = dg.gammaSets()
        dg.notGamma = dg.notGammaSets()
        return dg

    def isComparabilityGraph(self,Debug=False):
        """
        Verifies if the graph instance is a comparability graph.
        If yes, a tranditive orientation of the edges is stored 
        in self.edgeOrientations. 
        
        *Source*: M. Ch. Golumbic (2004) Algorithmic Graph Thery and Perfect Graphs,
        Annals of Discrete Mathematics 57, Elsevier, p. 129-132.
        """
        global orientation,IsComparabilityGraph,k
        def _explore(arc):
            global orientation,IsComparabilityGraph,k
            i = arc[0]
            j = arc[1]
            if Debug:
                print('arc', arc, orientation, self.gamma[i], self.gamma[j])

            for m in self.gamma[i]:
                if Debug:
                    print(i,j,m,self.gamma[j],orientation[(j,m)])
                if (m not in self.gamma[j]) or (abs(orientation[(j,m)]) < k): 
                    if orientation[(i,m)] == 999:
                        orientation[(i,m)] = k
                        orientation[(m,i)] = -k
                        _explore((i,m))
                    elif orientation[(i,m)] == -k:
                        orientation[(i,m)] = k
                        IsComparabilityGraph = False
                        if Debug:
                            print('is comp?',IsComparabilityGraph)
                        #return
                        _explore((i,m))
                    
            for m in self.gamma[j]:
                if Debug:
                    print(i,j,m,self.gamma[i],orientation[(i,m)])
                if (m not in self.gamma[i]) or (abs(orientation[(i,m)]) < k):
                    if orientation[(m,j)] == 999:
                        orientation[(m,j)] = k
                        orientation[(j,m)] = -k
                        _explore((m,j))
                    elif orientation[(m,j)] == -k:
                        orientation[(m,j)] = k
                        IsComparabilityGraph = False
                        if Debug:
                            print('is comp ?',IsComparabilityGraph)
                        #return
                        _explore((m,j))
                      
            if Debug:
                print(arc,orientation,IsComparabilityGraph)

        # initializing
        IsComparabilityGraph = True
        k = 0
        orientation = {}
        n = len(self.vertices)
        verticesList = list(self.vertices.keys())
        for i in range(n):
            vi = verticesList[i]
            orientation[(vi,vi)] = 0
            for j in range(i+1,n):
                vi = verticesList[i]
                vj = verticesList[j]
                edgeKey = frozenset([vi,vj])
                if self.edges[edgeKey] > Decimal('0'):
                    orientation[(vi,vj)] = 999
                    orientation[(vj,vi)] = 999
                else:
                    orientation[(vi,vj)] = 0
                    orientation[(vj,vi)] = 0
        #exploring all positive edges
        for edge in self.edges:
            arc = tuple(edge)
            if self.edges[edge] > Decimal('0'):  
                if orientation[arc] == 999:
                    k += 1
                    orientation[arc] = k
                    orientation[tuple(reversed(arc))] = -k
                    _explore(arc)
            if Debug:
                print('===>>>',edge,'=',self.edges[edge],orientation)
                
        # storing the edge decomposition
        self.IsComparabilityGraph = IsComparabilityGraph
        if IsComparabilityGraph:
            self.edgeOrientations = orientation

        return IsComparabilityGraph

    def isConnected(self):
        """
        Cheks if self is a connected graph instance.
        """
        dfs = self.depthFirstSearch()
        if len(dfs) == 1:
            return True
        else:
            return False

    def isIntervalGraph(self,Comments=False):
        """
        Checks whether the graph self is triangulated and
        its dual is a comparability graph.

        *Source*: M. Ch. Golumbic (2004) Algorithmic Graph Thery and Perfect Graphs,
        Annals of Discrete Mathematics 57, Elsevier, p. 16.

        """
        if self.isTriangulated():
            if Comments:
                print('Graph \'%s\' is triangulated.' % self.name)
            ds = -self
            if ds.isComparabilityGraph():
                if Comments:
                    print('Graph \'%s\' is transitively orientable.' % ds.name)
                    print('=> Graph \'%s\' is an interval graph.' % self.name)
                return True
            else:
                if Comments:
                    print('Graph \'%s\' is not transitively orientable.' % ds.name)
                return False        
        else:
            if Comments:
                print('Graph \%s\' is not triangulated' % self.name)
            return False

    def isPermutationGraph(self,Comments=False):
        """
        Checks whether the graph self and
        its dual are comparability graphs.

        *Source*: M. Ch. Golumbic (2004) Algorithmic Graph Thery and Perfect Graphs,
        Annals of Discrete Mathematics 57, Elsevier, p. 16.

        """
        if self.isComparabilityGraph():
            if Comments:
                print('Graph \'%s\' is transitively orientable.' % self.name)
            ds = -self
            if ds.isComparabilityGraph():
                if Comments:
                    print('Graph \'%s\' is transitively orientable.' % ds.name)
                    print('=> Graph \'%s\' is a permutation graph.' % self.name)
                return True
            else:
                if Comments:
                    print('Graph \'%s\' is not transitively orientable.' % ds.name)
                return False        
        else:
            if Comments:
                print('Graph \%s\' is not transitively orientable' % self.name)
            return False
         
    def isTree(self):
        """
        Checks if self is a tree by verifing the required number of
        edges: order-1; and the existence of leaves.
        """
        n = self.order
        m = self.size
        if n == 1:
            return True
        elif m != n-1:
            return False
        else:
            nbrOfLeaves = 0
            for x in self.vertices:
                degreex = len(self.gamma[x])
                if degreex == 0: # isolated vertex
                    return False 
                elif degreex == 1:
                    nbrOfLeaves += 1
            if nbrOfLeaves < 2: # a cycle graph
                return False
            else:
                return True

    def isTriangulated(self):
        """
        Checks if a graph contains no chordless cycle of
        length greater or equal to 4.
        """
        if self.computeChordlessCycles() == set():
            return True
        else:
            return False

    def isSplitGraph(self,Comments=False):
        """
        Checks whether the graph ' *self* ' and its dual ' *-self* ' are
        triangulated graphs
        """
        if self.isTriangulated():
            if Comments:
                print('Graph \'%s\' is triangulated.' % self.name)
            ds = -self
            if ds.isTriangulated():
                if Comments:
                    print('Graph \'%s\' is triangulated.' % ds.name)
                    print('=> Graph \'%s\' is a split graph.' % self.name)
                return True
            else:
                if Comments:
                    print('Graph \'%s\' is not is not triangulated.' % ds.name)
                return False        
        else:
            if Comments:
                print('Graph \%s\' is not triangulated' % self.name)
            return False

    def isPerfectGraph(self,Comments=False,Debug=False):
        """
        A graph *g* is perfect when neither *g*, nor *-g*, contain any chordless
        cycle of odd length.
        """
        cycles = self.computeChordlessCycles(Comments=Debug)
        for c in cycles:
            if (len(c) % 2) != 0:
                if Comments:
                    print('Graph %s contains an odd chordless circuit!' % self.name)
                    print(c)
                return False
        cycles = (-self).computeChordlessCycles(Comments=Debug)
        for c in cycles:
            if (len(c) % 2) != 0:
                if Comments:
                    print('The dual of graph %s contains an odd chordless circuit!' % self.name)
                    print(c)
                return False
        if Comments:
            print('Graph %s is perfect !' % self.name)
       
        return True
    
                  
    def randomDepthFirstSearch(self,seed=None,Debug=False):
        """
        Depth first search through a graph in random order of the vertex keys.

        .. Note::

            The resulting spanning tree (or forest) is by far not uniformly selected
            among all possible trees. Spanning stars will indeed be much less
            probably selected then streight walks !
            
        """
        import random
        random.seed(seed)
        
        def visitVertex(self,x,Debug=False):
            """
            Visits all followers of vertex x.
            """
            self.vertices[x]['color'] = 1
            ## self.date += 1
            self.vertices[x]['startDate'] = self.date
            self._dfsx.append(x)
            if Debug:
                print(' dfs %s, date = %d' % (str(self.dfs),  self.vertices[x]['startDate']))
            nextVertices = [y for y in self.gamma[x]]
            nextVertices.sort()
            if Debug:
                print('   next ', nextVertices)
            while nextVertices != []:
                y = random.choice(nextVertices)
                if self.vertices[y]['color'] == 0:
                    self.date += 1
                    visitVertex(self,y,Debug=Debug)
                    if self.vertices[x]['color'] == 1:
                        self._dfsx.append(x)
                nextVertices.remove(y)
            self.vertices[x]['color'] = 2
            self.vertices[x]['endDate'] = self.date
            self.date += 1

        def visitAllVertices(self,Debug=False):
            """
            Mark the starting date for all vertices
            and controls the progress of the search with vertices colors:
            White (0), Grey (1), Black (2)
            """
            self.dfs = []
            for x in self.vertices:
                self.vertices[x]['color'] = 0
            self.date = 0
            verticesList = [x for x in self.vertices]
            verticesList.sort()
            while verticesList != []:
                x = random.choice(verticesList)
                self._dfsx = []
                if self.vertices[x]['color'] == 0:
                    if Debug:
                        print('==>> Starting from %s ' % x)
                    visitVertex(self,x,Debug=Debug)
                    self.dfs.append(self._dfsx)
                verticesList.remove(x)


        # ---- main -----
        visitAllVertices(self,Debug=Debug)
        return self.dfs

    def recodeValuation(self,newMin=-1,newMax=1,Debug=False):
        """
        Recodes the characteristic valuation domain according
        to the parameters given.

        .. note::

            Default values gives a normalized valuation domain

        """
        from copy import deepcopy
        oldMax = self.valuationDomain['max']
        oldMin = self.valuationDomain['min']
        oldMed = self.valuationDomain['med']

        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)

        newMin = Decimal(str(newMin))
        newMax = Decimal(str(newMax))
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))

        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)

        verticesList = [x for x in self.vertices]
        oldEdges = self.edges
        newEdges = {}
        for i in range(self.order):
            x = verticesList[i]
            for j in range(i+1,self.order):
                y = verticesList[j]
                edge = frozenset([x,y])
                if oldEdges[edge] == oldMax:
                    newEdges[edge] = newMax
                elif oldEdges[edge] == oldMin:
                    newEdges[edge] = newMin
                elif oldEdges[edge] == oldMed:
                    newEdges[edge] = newMed
                else:
                    newEdges[edge] = newMin + ((oldEdges[edge] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(edge,oldEdges[edge],newEdges[edge])
        # install new values in self
        self.valuationDomain['max'] = newMax
        self.valuationDomain['min'] = newMin
        self.valuationDomain['med'] = newMed
        self.valuationDomain['hasIntegerValuation'] = False
        self.edges = deepcopy(newEdges)

    def save(self,fileName='tempGraph',Debug=False):
        """
        Persistent storage of a Graph class instance in the form of a python source code file.
        """
        print('*--- Saving graph in file: <' + fileName + '.py> ---*')
        verticesKeys = [x for x in self.vertices]
        verticesKeys.sort()
        #order = len(self.vertices)
        edges = self.edges
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Graph instance saved in Python format\n')
        fo.write('from decimal import Decimal\n')
        fo.write('vertices = {\n')
        for x in verticesKeys:
            fo.write('\'%s\': %s,\n' % (x,self.vertices[x]))
        fo.write('}\n')
        fo.write('valuationDomain = {\'min\':'+ str(Min)+',\'med\':'+str(Med)+',\'max\':'+str(Max)+'}\n')
        fo.write('edges = {\n')
        for i in range(self.order):
            for j in range(i+1,self.order):
                fo.write('frozenset([\'%s\',\'%s\']) : %d, \n' % (verticesKeys[i],verticesKeys[j],edges[frozenset([verticesKeys[i],verticesKeys[j]])]))
        fo.write( '}\n')
        fo.close()

    def setEdgeValue(self,edge,value,Comments=False):
        """
        Wrapper for updating the charactreistic valuation of a Graph instance.
        The egde parameter consists in a pair of vertices;
        edge = ('v1','v2') for instance.
        The new value must be in the limits of the valuation domain.
        """
        from decimal import Decimal
        # check vertices' existance
        verticesIds = [x for x in self.vertices]
        if (edge[0] not in verticesIds) or (edge[1] not in verticesIds):
            #self.showShort()
            print('!!! Error: edge %s not found !!!' % str(edge))
            return         
        # check new edge value
        Min = self.valuationDomain['min']
        Max = self.valuationDomain['max']
        newValue = Decimal(str(value))
        if newValue > Max or value < Min:
            print('!!! Error: edge value %s out of range !!!' % str(value))
            print(self.valuationDomain)
            return
        # set new value
        self.edges[frozenset(edge)] = Decimal(str(value))
        self.gamma = self.gammaSets()
        if Comments:
            print('edge %s put to value %s.' % (edge,str(value)))

    def showCliques(self):
        self.computeCliques(Comments=True)

    def showMIS(self):
        self.computeMIS(Comments=True)

    def showMore(self):
        """
        Generic show method for Graph instances.
        """
        print('*---- Properties of the graph ----*')
        print('Name             : \'%s\'' % (self.name) )
        vKeys = [x for x in self.vertices]
        vKeys.sort()
        print('Vertices         : ', vKeys)
        print('Order            : ', self.order)
        self.showMIS()
        self.showCliques()

    def showShort(self):
        """
        Generic show method for Graph instances.
        """
        print('*---- short description of the graph ----*')
        print('Name             : \'%s\'' % (self.name) )
        vKeys = [x for x in self.vertices]
        vKeys.sort()
        print('Vertices         : ', vKeys)
        print('Valuation domain : ', self.valuationDomain)
        print('Gamma function   : ')
        for v in vKeys:
            print('%s -> %s' % (v, list(self.gamma[v])))
        self.computeDegreeDistribution(Comments=True)
        self.computeNeighbourhoodDepthDistribution(Comments=True)

#----------------

class EmptyGraph(Graph):
    """
    Intantiates graph of given order without any positively valued edge.

    *Parameter*:
        * order (positive integer)

    """
    def __init__(self,order=5,seed=None):
        self.name = 'emptyGraph'
        self.order = order
        nd = len(str(order))
        vertices = dict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Min = self.valuationDomain['min']
        edges = dict()
        verticesList = [v for v in vertices]
        verticesList.sort()
        for x in verticesList:
            for y in verticesList:
                if x != y:
                    edgeKey = frozenset([x,y])
                    edges[edgeKey] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class CompleteGraph(Graph):
    """
    Instances of complete graphs bipolarly valuated in {-1,0,+1}.
    Each vertex x is positively linked to
    all the other vertices (edges[{x,y}] = +1)

    *Parameter*:
        * order (positive integer)

    """
    def __init__(self,order=5,seed=None):
        self.name = 'completeGraph'
        self.order = order
        nd = len(str(order))
        vertices = dict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Max = self.valuationDomain['max']
        edges = dict()
        verticesList = [v for v in vertices]
        verticesList.sort()
        for x in verticesList:
            for y in verticesList:
                if x != y:
                    edgeKey = frozenset([x,y])
                    edges[edgeKey] = Max
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class DualGraph(Graph):
    """
    Instantiates the dual Graph object of a given other Graph instance.

    The relation constructor returns the dual of self.relation with formula:
        relationOut[a][b] = Max - self.relation[a][b] + Min
        where Max (resp. Min) equals valuation maximum (resp. minimum).


    """
    def __init__(self,other):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'dual_' + str(other.name)
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:  # the dual of a PermutationGraph reverses the permutation
            permutation = list(other.permutation)
            permutation.reverse()
            self.permutation = permutation
        except AttributeError:
            pass        
        self.valuationDomain = deepcopy(other.valuationDomain)
        Max = self.valuationDomain['max']
        Min = self.valuationDomain['min']
        self.vertices = deepcopy(other.vertices)
        self.order = len(self.vertices)
        self.edges = {}
        for e in other.edges:
            self.edges[e] = Max - other.edges[e] + Min
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class CycleGraph(Graph):
    """
    Instances of cycle graph characterized in [-1,1].

    *Parameter*:
        * order (positive integer)

    Example of 7-cycle graph instance:

    .. image:: 7cycle.png
       :alt: 7-cycle instance
       :width: 300 px
       :align: center


    """
    def __init__(self,order=5,seed=None,Debug=False):
        from collections import OrderedDict
        self.name = 'cycleGraph'
        self.order = order
        nd = len(str(order))
        vertices = OrderedDict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'id':i+1, 'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        verticesList = [key for key in vertices]
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Min = self.valuationDomain['min']
        Max = self.valuationDomain['max']
        edges = OrderedDict()
        #verticesList = [v for v in vertices]
        #verticesList.sort()
        for x in vertices:
            for y in vertices:
                if x != y:
                    edgeKey = frozenset([x,y])
                    edges[edgeKey] = Min
        for i in range(order-1):
            edgeKey = frozenset(verticesList[i:i+2])
            edges[edgeKey] = Max
            if Debug:
                print(edgeKey)
        x = verticesList[-1]
        y = verticesList[0]
        edgeKey = frozenset([x,y])
        edges[edgeKey] = Max
        if Debug:
            print(edgeKey)
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class IntervalIntersectionsGraph(Graph):
    """
    Inveral graph constructed from a list of *n*
    intervals, ie pairs (a,b) of integer numbers where a < b.
    """
    def __init__(self,intervals,Debug=False):
        from collections import OrderedDict
        self.name = 'lineIntersections'
        self.intervals = intervals
        if Debug:
            print(intervals)
        order = len(intervals)
        self.order = order
        nd = len(str(order))
        vertices = OrderedDict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Min = self.valuationDomain['min']
        Max = self.valuationDomain['max']
        edges = OrderedDict()
        verticesList = [v for v in vertices]
        #verticesList.sort()
        for i in range(order):
            x = verticesList[i]
            a = intervals[i][0]
            b = intervals[i][1]
            for j in range(i+1,order):
                y = verticesList[j]
                c = intervals[j][0]
                d = intervals[j][1]
                edgeKey = frozenset([x,y])
                if c <= a and d >= a: 
                    edges[edgeKey] = Max
                    if Debug:
                        print(a,b,c,d,'=>',1)
                elif d >= b and c <= b:
                    edges[edgeKey] = Max
                    if Debug:
                        print(a,b,c,d,'=>',2)
                elif c <= a and d >= a:
                    edges[edgeKey] = Max
                    if Debug:
                        print(a,b,c,d,'=>',3)
                elif c >= a and d <= b:
                    edges[edgeKey] = Max
                    if Debug:
                        print(a,b,c,d,'=>',4)
                else:
                    edges[edgeKey] = Min
                    if Debug:
                        print(a,b,c,d,'=>',5)
                 
                if Debug:
                    print('a,b,c,d,edgeKey,edges[edgeKey]')
                    print(edgeKey,edges[edgeKey])
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class RandomIntervalIntersectionsGraph(IntervalIntersectionsGraph):
    """ Random generator for IntervalIntersectionsGraph intances."""
    def __init__(self,order=5,seed=None,m=0,M=10,Debug=False):
        import random
        random.seed(seed)
        self.seed = seed
        self.name = 'randIntervalIntersections'
        self.order = order
        intervals = []
        for i in range(order):
            a = random.randint(m,M)
            b = random.randint(m,M)
            if a < b:
                intervals.append((a,b))
            else:
                intervals.append((b,a))
        if Debug:
            print(intervals)
        self.intervals = intervals
        lis = IntervalIntersectionsGraph(intervals)
        self.vertices = lis.vertices
        self.valuationDomain = lis.valuationDomain
        self.edges = lis.edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()
        
class RandomGraph(Graph):
    """
    Random instances of the Graph class

    *Parameters*:
        * order (positive integer)
        * edgeProbability (in [0,1])
    """
    def __init__(self,order=5,edgeProbability=0.4,seed=None):
        from collections import OrderedDict
        import random
        random.seed(seed)
        self.seed = seed
        self.edgeProbability = edgeProbability
        self.name = 'randomGraph'
        self.order = order
        nd = len(str(order))
        vertices = OrderedDict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Min = self.valuationDomain['min']
        Max = self.valuationDomain['max']
        edges = OrderedDict()
        verticesList = [v for v in vertices]
        #verticesList.sort()
        for i in range(order):
            x = verticesList[i]
            for j in range(i+1,order):
                y = verticesList[j]
                edgeKey = frozenset([x,y])
                if random.random() > 1.0 - edgeProbability:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class RandomValuationGraph(Graph):
    """
    Specialization of the genuine Graph class for generating temporary
    randomly valuated graphs in the range [-1.0;1.0].
    
    *Parameter*:
        * order (positive integer)
        * ndigits (decimal precision) 

    """
    def __init__(self,order=5,ndigits=2,seed=None):
        import random
        random.seed(seed)
        self.name = 'randomGraph'
        self.order = order
        nd = len(str(order))
        vertices = dict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'id':i+1,'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        Min = float(self.valuationDomain['min'])
        Max = float(self.valuationDomain['max'])
        edges = dict()
        verticesList = [v for v in vertices]
        verticesList.sort()
        for i in range(order):
            x = verticesList[i]
            for j in range(i+1,order):
                y = verticesList[j]
                edgeKey = frozenset([x,y])
                weightString = ('%%.%df' % ndigits) %  random.uniform(Min,Max)
                edges[edgeKey] = Decimal(weightString)
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class RandomRegularGraph(Graph):
    """
    Specialization of the general Graph class for generating
    temporary random regular graphs of fixed degrees.
    """
    def __init__(self,order=7,degree=2,seed=None):
        from randomDigraphs import RandomRegularDigraph
        rdg = RandomRegularDigraph(order=order,
                                   degree=degree,
                                   seed=seed)
        rg = rdg.digraph2Graph()
        self.vertices = rg.vertices
        self.valuationDomain = rg.valuationDomain
        self.edges = rg.edges
        self.name = 'randomRegularGraph'
        self.order = len(self.vertices)
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

class RandomFixedSizeGraph(Graph):
    """
    Generates a random graph with a fixed size (number of edges), by instantiating a fixed numbers of arcs
    from random choices in the set of potential pairs of vertices numbered from 1 to order. 
    """
    def __init__(self,order=7,size=14,seed=None,Debug=False):
        import random
        random.seed(seed)
        # check feasability
        r = ((order * order) - order)//2
        if size > r :
            print('Graph not feasable: size exceeds number of potential edges = %d !!' % r)
            return
        print(order,size,r)
        self.name = 'randomFixedSize'
        self.order = order
        nd = len(str(order))
        vertices = dict()
        for i in range(order):
            vertexKey = ('v%%0%dd' % nd) % (i+1)
            vertices[vertexKey] = {'id':i+1,'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        if Debug:
            print(self.vertices)
        self.valuationDomain = {'min':Decimal('-1'),'med':Decimal('0'),'max':Decimal('1')}
        edges = dict()
        Min = self.valuationDomain['min']
        verticesList = [v for v in vertices]
        verticesList.sort()
        for x in verticesList:
            for y in verticesList:
                if x != y:
                    edgeKey = frozenset([x,y])
                    edges[edgeKey] = Min
        if Debug:
            print(edges)
        edgesKeys = [key for key in edges]
        edgesKeys.sort()
        if Debug:
            print(edgesKeys)
        Max = self.valuationDomain['max']
        for i in range(size):
                edgeKey = random.choice(edgesKeys)
                edges[edgeKey] = Max
                edgesKeys.remove(edgeKey)
                if Debug:
                    print(i,edgeKey,edgesKeys)
        self.edges = edges
        self.size = size
        self.gamma = self.gammaSets()

class RandomFixedDegreeSequenceGraph(Graph):
    """
    Specialization of the general Graph class for generating
    temporary random graphs with a fixed sequence of degrees.

    .. warning::

        The implementation is not guaranteeing a uniform choice
        among all potential valid graph instances.

    """
    def __init__(self,order=7,degreeSequence=[3,3,2,2,1,1,0],seed=None):
        from randomDigraphs import RandomFixedDegreeSequenceDigraph
        rdg = RandomFixedDegreeSequenceDigraph(order=order,
                                               degreeSequence=degreeSequence,
                                               seed=seed)
        rg = rdg.digraph2Graph()
        self.vertices = rg.vertices
        self.order = order
        self.valuationDomain = rg.valuationDomain
        self.edges = rg.edges
        self.size = self.computeSize()
        self.name = 'randomFixedDegreeSequenceGraph'
        self.gamma = self.gammaSets()

class GridGraph(Graph):
    """
    Specialization of the general Graph class for generating
    temporary Grid graphs of dimension n times m.

    *Parameters*:
        * n,m > 0
        * valuationDomain ={'min':-1, 'med':0, 'max':+1}

    Default instantiation (5 times 5 Grid Digraph):
       * n = 5,
       * m=5,
       * valuationDomain = {'min':-1.0,'max':1.0}.

    Example of 5x5 GridGraph instance:

    .. image:: grid-5-5.png
       :alt: 5x5 grid instance
       :width: 300 px
       :align: center
    """

    def __init__(self,n=5,m=5,valuationMin=-1,valuationMax=1):

        self.name = 'grid-'+str(n)+'-'+str(m)
        self.n = n
        self.m = m
        na = list(range(n+1))
        na.remove(0)
        ma = list(range(m+1))
        ma.remove(0)
        vertices = {}
        gridNodes={}
        for x in na:
            for y in ma:
                vertex = str(x)+'-'+str(y)
                gridNodes[vertex]=(x,y)
                vertices[vertex] = {'name': 'gridnode', 'shortName': vertex}
        order = len(vertices)
        self.order = order
        self.vertices = vertices
        self.gridNodes = gridNodes
        Min = Decimal(str(valuationMin))
        Max = Decimal(str(valuationMax))
        Med = Decimal(str((Max + Min)/Decimal('2')))
        self.valuationDomain = {'min':Min,'med':Med,'max':Max}
        edges = {} # instantiate edges
        verticesKeys = [x for x in vertices]
        for x in verticesKeys:
            for y in verticesKeys:
                if x != y:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            edges[frozenset([x,y])] = Max
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            edges[frozenset([x,y])] = Max
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    else:
                        edges[frozenset([x,y])] = Min


        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Grid graph    : ', self.name)
        print('n             : ', self.n)
        print('m             : ', self.m)
        print('order         : ', self.order)
        print('size          : ', self.size)

#--------------------------
class SnakeGraph(GridGraph):
    """
    Snake graphs S(p/q) are made up of all the integer grid squares between
    the lower and upper Christofel paths of the rational number p/q, 
    where p and q are two coprime integers such that
    0 <= p <= q, i.e. p/q gives an irreducible ratio between 0 and 1.
    
    *Reference*: M. Aigner,
    Markov's Theorem and 100 Years of the Uniqueness Conjecture, Springer, 2013, p. 141-149

    S(4/7) snake graph instance::
    
        >>> from graphs import SnakeGraph
        >>> s4_7 = SnakeGraph(p=4,q=7)
        >>> s4_7.showShort()
        *---- short description of the snake graph ----*
        Name             : 'snakeGraph'
        Rational p/q     : 4/7
        Christoffel words:
        Upper word       :  BBABABA
        Lower word       :  ABABABB
        >>> s4_7.exportGraphViz('4_7_snake',lineWidth=3,arcColor='red')

    .. image:: 4_7_snake.png
       :alt: 4/7 snake graph instance
       :width: 300 px
       :align: center

    """
    
    def __init__(self,p,q):
        from math import floor, ceil
        self.name = '%d_%d_snakeGraph' % (p,q)
        # vertices
        self.n = q
        self.m = p
        vertices = {}
        gridNodes={}
        for x in range(q+1):
            for y in range(p+1):
                vertex = str(x)+'-'+str(y)
                gridNodes[vertex]=(x,y)
                vertices[vertex] = {'name': 'gridnode', 'shortName': vertex}
        order = len(vertices)
        self.order = order
        self.vertices = vertices
        self.gridNodes = gridNodes
        # valuation domain
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        # edges
        edges = {} # instantiate edges
        verticesKeys = [x for x in vertices]
        for x in verticesKeys:
            for y in verticesKeys:
                if x != y:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            edges[frozenset([x,y])] = Med
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            edges[frozenset([x,y])] = Med
                        else:
                            edges[frozenset([x,y])] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            edges[frozenset([x,y])] = Med
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            edges[frozenset([x,y])] = Med
                        else:
                            edges[frozenset([x,y])] = Min
                    else:
                        edges[frozenset([x,y])] = Min
        self.edges = edges
        # snake lower Christoffel path
        k = [0 for i in range(q+1)]
        for i in range(q+1):
            k[i] = floor((p/q)*i)
        print(k)
        for i in range(q):
            if k[i] == k[i+1]:
                x = '%d-%d' % (i,k[i])
                y = '%d-%d' % (i+1,k[i+1])
                self.setEdgeValue((x,y),Max)
            else:
                x = '%d-%d' % (i,k[i])
                y = '%d-%d' % (i+1,k[i])
                self.setEdgeValue((x,y),Max)
                x = '%d-%d' % (i+1,k[i])
                y = '%d-%d' % (i+1,k[i+1])
                self.setEdgeValue((x,y),Max)
        # snake upper  Christoffel path
        K = [0 for i in range(q+1)]
        for i in range(q+1):
            K[i] = ceil((p/q)*i)
        print(K)
        for i in range(q):
            if K[i] == K[i+1]:
                x = '%d-%d' % (i,K[i])
                y = '%d-%d' % (i+1,K[i])
                print(x,y)
                self.setEdgeValue((x,y),Max)
            else:
                x = '%d-%d' % (i,K[i])
                y = '%d-%d' % (i,K[i+1])
                print(x,y)
                self.setEdgeValue((x,y),Max)
                x = '%d-%d' % (i,K[i+1])
                y = '%d-%d' % (i+1,K[i+1])
                print(x,y)
                self.setEdgeValue((x,y),Max)                
                    
        # storing graph instance
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

        # ChristoffelWord
        lcw = ''
        ucw = ''
        for i in range(1,q+1):
            if k[i]-k[i-1] == 0:
                lcw += 'A'
            else:
                lcw += 'B'
            if K[i]-K[i-1] == 0:
                ucw += 'A'
            else:
                ucw += 'B'
        self.cw = (lcw,ucw)

    def showShort(self,WithVertices=False):
        """
        Show method for SnakeGraph instances.
        """
        print('*---- short description of the snake graph ----*')
        print('Name             : \'%s\'' % (self.name) )
        print('Rational p/q     : %d/%d' % (self.m,self.n))
        print('Christoffel words:')
        print('Upper word       : ',self.cw[1])
        print('Lower word       : ',self.cw[0])
        if WithVertices:
            vKeys = [x for x in self.vertices]
            vKeys.sort()
            print('Vertices         : ', vKeys)
            print('Valuation domain : ', self.valuationDomain)
            print('Gamma function   : ')
            for v in vKeys:
                if self.gamma[v] != set():
                    print('%s -> %s' % (v, list(self.gamma[v])))

    def __repr__(self):
        """
        Show method for SnakeGraph instances.
        """
        reprString = Graph.__repr__(self)
        reprString += '*---- Snake graph specific data ----*\n'
        #reprString += 'Name             : \'%s\'\n' % (self.name)
        reprString += 'Rational p/q     : %d/%d\n' % (self.m,self.n)
        reprString += 'Christoffel words:\n'
        reprString += 'Upper word       : %s\n' % self.cw[1]
        reprString += 'Lower word       : %s\n' % self.cw[0]
        return reprString
        
#---------------------
class TriangulatedGrid(Graph):
    """
    Specialization of the general Graph class for generating
    temporary triangulated grids of dimension n times m.

    *Parameters*:
        * n,m > 0
        * valuationDomain = {'min':m, 'max':M}

    Example of 5x5 triangulated grid instance:

    .. image:: triangular-5-5.png
       :alt: triangulated 5x5 grid
       :width: 300 px
       :align: center
    """

    def __init__(self,n=5,m=5,valuationMin=-1,valuationMax=1):

        self.name = 'triangulated-'+str(n)+'-'+str(m)
        self.n = n
        self.m = m
        na = list(range(n+1))
        na.remove(0)
        ma = list(range(m+1))
        ma.remove(0)
        vertices = {}
        gridNodes={}
        for x in na:
            for y in ma:
                vertex = str(x)+'-'+str(y)
                gridNodes[vertex]=(x,y)
                vertices[vertex] = {'name': 'gridnode', 'shortName': vertex}
        order = len(vertices)
        self.order = order
        self.vertices = vertices
        self.gridNodes = gridNodes
        Min = Decimal(str(valuationMin))
        Max = Decimal(str(valuationMax))
        Med = Decimal((Max + Min)/Decimal('2'))
        self.valuationDomain = {'min':Min,'med':Med,'max':Max}
        edges = {} # instantiate edges
        verticesKeys = [x for x in vertices]
        for x in verticesKeys:
            for y in verticesKeys:
                if x != y:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            edges[frozenset([x,y])] = Max
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            edges[frozenset([x,y])] = Max
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]-1:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    elif gridNodes[x][0] == gridNodes[y][0]+1:
                        if gridNodes[x][1] == gridNodes[y][1]+1:
                            edges[frozenset([x,y])] = Max
                        else:
                            edges[frozenset([x,y])] = Min
                    else:
                        edges[frozenset([x,y])] = Min


        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

    def showShort(self):
        print('*----- show summary --------------*')
        print('Triangular graph : ', self.name)
        print('n x m            : ', self.n, 'x', self.m)
        print('order            : ', self.order)
        print('size             : ', self.size)

class RandomTree(Graph):
    """
    Instance of a tree generated from a random (or a given) Prüfer code.

    .. image:: randomTree.png
       :alt: radomTree instance
       :width: 300 px
       :align: center
   
    """

    def __repr__(self):
        """
        Show method for RandomTree instances.
        """
        try:
            code = self.prueferCode
            reprString = Graph.__repr__(self)
            reprString += '*---- RandomTree specific data ----*\n'
            reprString += 'Prüfer code  : %s\n' % code
        except AttributeError:
            reprString = Graph.__repr__(self)
        return reprString

    def __init__(self,order=None, vertices= None,
                 prueferCode = None, seed = None, Debug=False):
        import random
        random.seed(seed)
        self.name='randomTree'
        if order == None:
            if prueferCode == None:
                order = 6
            else:
                order = len(prueferCode) + 2
        self.order = order
        if Debug:
            print(self.name, self.order)
        if vertices == None:
            vertices = dict()
            for i in range(order):
                vertexKey = 'v%d' % (i+1)
                vertices[vertexKey] = {'shortName':str(vertexKey), 'name': 'random vertex'}
        self.vertices = vertices
        if Debug:
            print('vertices = ', self.vertices)

        self.valuationDomain = {'min':Decimal('-1'),
                                'med':Decimal('0'),
                                'max':Decimal('1')}
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        if Debug:
            print('valuationDomain = ', self.valuationDomain)


        verticesList = [x for x in self.vertices.keys()]
        verticesList.sort()
        if Debug:
            print(verticesList)
        edges = dict()
        for i in range(order):
            for j in range(i+1,order):
                edgeKey = frozenset([verticesList[i],verticesList[j]])
                edges[edgeKey] = Min
        self.edges = edges
        if Debug:
            print('edges = ',self.edges)
        if prueferCode == None:
            prueferCode = []
            for k in range(order-2):
                prueferCode.append( random.choice(verticesList) )
        self.prueferCode = prueferCode
        if Debug:
            print('prueferCode = ', self.prueferCode)

        degree = {}
        for x in verticesList:
            degree[x] = 1
        for i in range(order-2):
            degree[prueferCode[i]] += 1
        if Debug:
            print('degrees = ', degree)

        for i in range(order-2):
            for j in range(order):
                if degree[verticesList[j]] == 1:
                    edgeKey = frozenset([prueferCode[i],verticesList[j]])
                    self.edges[edgeKey] = Max
                    degree[verticesList[j]] -= 1
                    degree[prueferCode[i]] -= 1
                    break
        lastEdgeKey = frozenset([verticesList[i] for i in range(order) if degree[verticesList[i]] > 0])
        self.edges[lastEdgeKey] = Max
        if Debug:
            print('updated edges = ', self.edges)
        self.size = self.computeSize()
        self.gamma = self.gammaSets(Debug)
        if Debug:
            print('gamma = ', self.gamma)

    def tree2Pruefer(self,vertices=None,Debug=False):
        """
        Renders the Pruefer code of a given tree.
        """
        if vertices == None:
            vertices = self.vertices
        verticesList = [x for x in vertices]
        verticesList.sort()
        if Debug:
            print('verticesList = ',verticesList)
        np = len(verticesList)-2
        Med = self.valuationDomain['med']
        edges = [e for e in self.edges if self.edges[e] > Med]
        degree = dict()
        for v in verticesList:
            degree[v] = len(self.gamma[v])
        if Debug:
            print('degrees = ', degree)
        prueferCode = []
        for i in range(np):
            leaves = [v for v in verticesList if degree[v] == 1]
            leaves.sort()
            leavesEdges = [e for e in edges if leaves[0] in e]
            for v in leavesEdges[0]:
                if degree[v] > 1:
                    prueferCode.append(v)
                degree[v] -= 1
            edges.remove(leavesEdges[0])
        return prueferCode

class RandomSpanningForest(RandomTree):
    """
    Random instance of a spanning forest (one or more trees)
    generated from a random depth first search graph g traversal.

    .. image:: spanningForest.png
       :alt: randomSpanningForest instance
       :width: 300 px
       :align: center
    """
    def __init__(self,g,seed=None,Debug=False):
        from copy import deepcopy
        import random
        random.seed(seed)
        self.name= g.name+'_randomSpanningTree'
        if Debug:
            print(self.name)
        self.vertices = deepcopy(g.vertices)
        order = len(self.vertices)
        self.order = order
        self.valuationDomain = deepcopy(g.valuationDomain)
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        if Debug:
            print('valuationDomain = ', self.valuationDomain)

        verticesList = [x for x in self.vertices]
        verticesList.sort()
        edges = dict()
        for i in range(order):
            for j in range(i+1,order):
                edgeKey = frozenset([verticesList[i],verticesList[j]])
                if g.edges[edgeKey] > Med:
                    edges[edgeKey] = Med
                else:
                    edges[edgeKey] = g.edges[edgeKey]
        self.edges = deepcopy(edges)
        if Debug:
            print('edges = ',self.edges)

        self.dfs = g.randomDepthFirstSearch(seed=seed,Debug=Debug)
        if Debug:
            print('dfs = ', self.dfs)
        components = []
        for tree in self.dfs:
            component = set()
            n = len(tree)
            for i in range(n-1):
                component.add(tree[i])
                component.add(tree[i+1])
                edgeKey = frozenset([tree[i],tree[i+1]])
                self.edges[edgeKey] = Max
            if Debug:
                print('tree = ',tree)
                print('component = ',component)
            components.append(component)
        if Debug:
            print('updated edges = ', self.edges)
   
        self.size = self.computeSize()
        self.gamma = self.gammaSets(Debug)
        if Debug:
            print('gamma = ', self.gamma)

        prueferCodes = []
        for tree in self.dfs:
            component = set(tree)
            if len(component) > 2:
                prueferCodes.append({'component': component,
                                 'code': self.tree2Pruefer(vertices=component)
                                 })
            else:
                prueferCodes.append({'component': component, 'code': []})
                
        self.prueferCodes = prueferCodes

    def computeAverageTreeDetermination(self,dfs=None):
        """
        Renders the mean average determinations of the spanning trees.
        """
        from decimal import Decimal
        if dfs == None:
            dfs = self.dfs
        maxWeights = []
        n = len(dfs)
        for i in range(n):
            dfsx = dfs[i]
            maxWeight = Decimal('0')
            k = len(dfsx)
            if k > 1:
                for j in range(k-1):
                    edgeKey = frozenset([dfsx[j],dfsx[j+1]])
                    maxWeight += self.edges[edgeKey]
                maxWeights.append( maxWeight / Decimal(str(k-1)) )
            else:
                maxWeights.append(self.valuationDomain['max'])
        self.averageTreeDetermination = maxWeights 
        return  
        
class RandomSpanningTree(RandomTree):
    """
    Uniform random instance of a spanning tree
    generated with Wilson's algorithm from a connected Graph g instance.

    .. Note::

         Wilson's algorithm only works for connecte graphs.

    .. image:: randomSpanningTree.png
       :alt: randomSpanningTree instance
       :width: 300 px
       :align: center
    """
    
    
    def __init__(self,g,seed=None,Debug=False):
        from copy import copy as copy
        if not g.isConnected():
            print('Error !: Wilson\'s algorithm requires a connected graph!')
            return
        import random
        random.seed(seed)
        self.name= g.name+'_randomSpanningTree'
        if Debug:
            print(self.name)
        self.vertices = copy(g.vertices)
        order = len(self.vertices)
        self.order = order
        self.valuationDomain = copy(g.valuationDomain)
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        if Debug:
            print('valuationDomain = ', self.valuationDomain)
        
        verticesList = [x for x in self.vertices]
        random.shuffle(verticesList)
        if Debug:
            print(verticesList)
        spannedVertices = set()
        spanningTree = []
        randomWalk = [verticesList[0]]
        i = 0
        while randomWalk[i] != verticesList[-1]:
            nextVertex = random.choice(list(g.gamma[randomWalk[i]]))
            randomWalk.append(nextVertex)
            i += 1
        if Debug:
            print('random walk: ',randomWalk)
        spanningBranch = self._reduceCycles(randomWalk,Debug=Debug)
        spanningTree.append(spanningBranch)
        spannedVertices = spannedVertices | set(spanningBranch)
        remainingVertices = set(verticesList) - set(spanningBranch)
        if Debug:
            print('spanningBranch = ', spanningBranch)
            print('spannedVertices = ', spannedVertices)
            print('remainingVertices = ',remainingVertices)
            print('spanningTree = ', spanningTree)
        while remainingVertices != set():
            remainingVerticesList = list(remainingVertices)
            random.shuffle(remainingVerticesList)
            randomWalk = [random.choice(remainingVerticesList)]
            i = 0
            while randomWalk[i] not in spannedVertices:
                nextVertex = random.choice(list(g.gamma[randomWalk[i]]))
                randomWalk.append(nextVertex)
                i += 1
            if Debug:
                print('randomWalk = ',randomWalk)
            spanningBranch = self._reduceCycles(randomWalk,Debug=Debug)
            spannedVertices = spannedVertices | set(spanningBranch)
            remainingVertices = set(remainingVerticesList) - set(spanningBranch)
            spanningTree.append(spanningBranch)            
            if Debug:
                print('spanningBranch = ', spanningBranch)
                print('spannedVertices = ', spannedVertices)
                print('remainingVertices = ',remainingVertices)
                print('spanningTree = ', spanningTree)
                
        self.edges = copy(g.edges)
        for edgeKey in self.edges:
            if self.edges[edgeKey] > Med:
                self.edges[edgeKey] = Med
        for branch in spanningTree:
            for i in range(len(branch)-1):
                edgeKey = frozenset([branch[i],branch[i+1]])
                self.edges[edgeKey] = g.edges[edgeKey]
        if Debug:
            print('edges = ', self.edges)

        self.size = self.computeSize()
        self.gamma = self.gammaSets()
        self.dfs = self.depthFirstSearch()
        self.prueferCode = self.tree2Pruefer()
        
    def _reduceCycles(self,randomWalk,Debug=False):
        if Debug:
            print('randomWalk', randomWalk)
        reducedWalk = [randomWalk[0]]
        n = len(randomWalk)
        t = 0
        while t < n-1 and t < 100:
            k = t+1
            for j in range(t+1,n):
                if randomWalk[t] == randomWalk[j]:
                    k = j+1
                    if Debug:
                        print(t, k, j, n, randomWalk[t:k])
            reducedWalk.append(randomWalk[k])
            if Debug:
                print('reducedWalk', reducedWalk)
            t = k
        return reducedWalk
                      
#----------
class BestDeterminedSpanningForest(RandomSpanningForest):
    """
    Constructing the most determined spanning tree (or forest if not connected)
    using Kruskal's greedy algorithm on the dual valuation.

    Example Python session:
       >>> from graphs import *
       >>> g = RandomValuationGraph(seed=2)
       >>> g.showShort()
       *---- short description of the graph ----*
       Name             : 'randomGraph'
       Vertices         :  ['v1', 'v2', 'v3', 'v4', 'v5']
       Valuation domain :  {'med': Decimal('0'), 'min': Decimal('-1'), 'max': Decimal('1')}
       Gamma function   : 
       v1 -> ['v2', 'v3']
       v2 -> ['v4', 'v1', 'v5', 'v3']
       v3 -> ['v1', 'v5', 'v2']
       v4 -> ['v5', 'v2']
       v5 -> ['v4', 'v2', 'v3']
       >>> mt = BestDeterminedSpanningForest(g)
       >>> mt.exportGraphViz('spanningTree',WithSpanningTree=True)
       *---- exporting a dot file for GraphViz tools ---------*
       Exporting to spanningTree.dot
       [['v4', 'v2', 'v1', 'v3', 'v1', 'v2', 'v5', 'v2', 'v4']]
       neato -Tpng spanningTree.dot -o spanningTree.png

    .. image:: spanningTree.png
       :alt: Colored bes determined panning tree
       :width: 300 px
       :align: center

    """
    def __repr__(self):
        """
        Show method for best determined spanning forests instances.
        """
        reprString = Graph.__repr__(self)
        reprString += '*---- best determined spanning tree specific data ----*\n'
        reprString += 'Depth first search path(s) : %s\n' % str(self.dfs)
        reprString += 'Average determination(s)   : %s\n' %\
                      str(self.averageTreeDetermination)
       
        return reprString
    
    def __init__(self,g,seed=None,Debug=False):
        from copy import deepcopy
        import random
        random.seed(seed)
        self.name= g.name+'_randomSpanningForest'
        if Debug:
            print(self.name)
        self.vertices = deepcopy(g.vertices)
        verticesList = [x for x in self.vertices]
        verticesList.sort()
        order = len(self.vertices)
        self.order = order
        self.valuationDomain = deepcopy(g.valuationDomain)
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        if Debug:
            print('valuationDomain = ', self.valuationDomain)
        edges = dict()
        for i in range(order):
            for j in range(i+1,order):
                edgeKey = frozenset([verticesList[i],verticesList[j]])
                if g.edges[edgeKey] > Med:
                    edges[edgeKey] = Med
                else:
                    edges[edgeKey] = g.edges[edgeKey]
        forest = []
        weightedEdgesList = [(g.edges[e],e) \
                for e in g.edges if g.edges[e] > Med ]
        weightedEdgesList.sort(reverse=True)
        if Debug:
            print(weightedEdgesList)
        for e in weightedEdgesList:
            if Debug:
                print('===>>> ', e)
            edgeKeys = set([v for v in e[1]])
            Included = False
            connectedSubtrees = []
            for tree in forest:
                if Debug:
                    print(tree)
                test = tree[1] & edgeKeys
                if len(test) == 2: # already connected
                    Included = True
                    if Debug:
                        print('already included')
                    break
                elif len(test) == 1: # extending
                    connectedSubtrees.append(tree)
                    if Debug:
                        print('extending',tree)
            if not Included:
                edges[e[1]] = e[0]
                if Debug:
                    print(e[1],edges[e[1]])             
                    print('connecting subtrees',connectedSubtrees)
                if connectedSubtrees == []:
                    forest.append([set([e[1]]),edgeKeys])
                    if Debug:
                        print('Add new subtree')
                elif len(connectedSubtrees) == 1:
                    connectedSubtrees[0][0].add(e[1])
                    connectedSubtrees[0][1] = connectedSubtrees[0][1] | edgeKeys
                    if Debug:
                        print('Extending an existing subtree')
                else:
                    connectedSubtrees[0][0].add(e[1])
                    connectedSubtrees[0][0] =\
                            connectedSubtrees[0][0] | connectedSubtrees[1][0]
                    connectedSubtrees[0][1] =\
                connectedSubtrees[0][1] | connectedSubtrees[1][1] | edgeKeys
                    forest.remove(connectedSubtrees[1])
                    if Debug:
                        print('connected two subtrees')
                        print(forest)
                    
        self.edges = deepcopy(edges)
        if Debug:
            print('edges = ',self.edges)
        self.size = self.computeSize()
        self.gamma = self.gammaSets(Debug)
        if Debug:
            print('gamma = ', self.gamma)
        self.dfs = self.depthFirstSearch()
        self.computeAverageTreeDetermination()

class Q_Coloring(Graph):
    """
    Generate a q-coloring of a Graph instance via a Gibbs MCMC sampler in
    nSim simulation steps (default = len(graph.edges)).
    
        Example 3-coloring of a grid 6x6 :
           >>> from graphs import *
           >>> g = GridGraph(n=6,m=6)
           >>> g.showShort()
           >>> g.exportGraphViz()
           *----- show short --------------*
           Grid graph    :  grid-6-6
           n             :  6
           m             :  6
           order         :  36
           >>> qc = Q_Coloring(g,colors=['gold','lightblue','lightcoral'])
           Running a Gibbs Sampler for 630 step !
           >>> qc.checkFeasibility()
           The q-coloring with 3 colors is feasible !!
           >>> qc.exportGraphViz()
           *---- exporting a dot file for GraphViz tools ---------*
           Exporting to grid-6-6-qcoloring.dot
           fdp -Tpng grid-6-6-qcoloring.dot -o grid-6-6-qcoloring.png
           
        .. image:: grid-6-6-qcoloring.png
           :alt: 3 coloring of a 6x6 grid
           :width: 300 px
           :align: center
    """ 

    def __init__(self,g,colors=['gold','lightcoral','lightblue'],
                 nSim=None,maxIter=20,seed=None,
                 Comments=True,Debug=False):
        from copy import deepcopy
        self.gClass = g.__class__
        self.name = '%s-qcoloring' % g.name
        if isinstance(g.vertices,dict):
            self.vertices = deepcopy(g.vertices)
        else:
            self.vertices = dict()
            for v in g.vertices:
                self.vertices[v] = {'name':v,'shortName':v}
        self.order = len(self.vertices)
        self.colors = deepcopy(colors)
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = len(self.edges)
        self.gamma = deepcopy(g.gamma)
##        print(self.colors[0])
##        for v in self.vertices:
##            self.vertices[v]['color'] = colors[0]
        if nSim == None:
            nSim = len(self.edges)*2
        self.nSim = nSim
        infeasibleEdges = set([e for e in self.edges])
        _iter = 0
        while infeasibleEdges != set() and _iter < maxIter:
            _iter += 1
            print('Iteration:', _iter)
            self.generateFeasibleConfiguration(seed=seed,Reset=True,Debug=Debug)
            infeasibleEdges = self.checkFeasibility(Comments=Comments)
    
    def showConfiguration(self):
        for v in self.vertices:
            print(v,self.vertices[v]['color'])
            
    def generateFeasibleConfiguration(self,Reset=True,nSim=None,seed=None,Debug=False):
        import random
        random.seed(seed)
        if Reset:
            for v in self.vertices:
                self.vertices[v]['color'] = self.colors[0]           
        if nSim == None:
            nSim = self.nSim
        print('Running a Gibbs Sampler for %d step !' % nSim)
        for s in range(nSim):
            verticesKeys = [v for v in self.vertices]
            v = random.choice(verticesKeys)
            neighborColors = [self.vertices[x]['color']\
                                  for x in self.gamma[v]]
            feasibleColors = list(set(self.colors) - set(neighborColors))
            try:
                self.vertices[v]['color'] = random.choice(feasibleColors)
            except:
                if Debug:
                    print(s,v,'Warning !! Not feasible coloring')
                self.vertices[v]['color'] = random.choice(self.colors)
            if Debug:
                print(s, v,  self.vertices[v]['color'])

    def checkFeasibility(self,Comments=True,Debug=False):
        infeasibleEdges = set()
        for e in self.edges:
            if self.edges[e] > self.valuationDomain['med']:
                neighborColors = set([self.vertices[x]['color'] for x in e])
                if len(neighborColors) < 2:
                    if Debug:
                        print('Infeasible Confirguration !! See edge %s' % e)
                    infeasibleEdges.add(e)
                else:
                    if Debug:
                        print(e,neighborColors)
        if Comments:
            if infeasibleEdges == set():
                print('The q-coloring with %d colors is feasible !!'\
                      % len(self.colors))
            else:
                print('The q-coloring with %d colors is apparently not feasible !!'\
                      % len(self.colors))
                print('Either augment nSim=%d or add one more color'\
                      % self.nSim)
        return infeasibleEdges              

    def exportGraphViz(self,fileName=None,
                       Comments=True,
                       graphType='png',
                       graphSize='7,7',
                       layout=None):
        """
        Exports GraphViz dot file  for q-coloring drawing filtering.

        The graph drawing layout is depending on the graph type, but can be forced to either
        'fdp', 'circo' or 'neato' with the layout parameter.

        Example:
            >>> g = Graph(numberOfVertices=10,edgeProbability=0.4)
            >>> g.showShort()
            *---- short description of the graph ----*
            Name : 'randomGraph'
            Vertices :  ['v1','v10','v2','v3','v4','v5','v6','v7','v8','v9']
            Valuation domain :  {'max': 1, 'min': -1, 'med': 0}
            Gamma function   : 
            v1 -> ['v7', 'v2', 'v3', 'v5']
            v10 -> ['v4']
            v2 -> ['v1', 'v7', 'v8']
            v3 -> ['v1', 'v7', 'v9']
            v4 -> ['v5', 'v10']
            v5 -> ['v6', 'v7', 'v1', 'v8', 'v4']
            v6 -> ['v5', 'v8']
            v7 -> ['v1', 'v5', 'v8', 'v2', 'v3']
            v8 -> ['v6', 'v7', 'v2', 'v5']
            v9 -> ['v3']
            >>> qc = Q_Coloring(g,nSim=1000)
            Running a Gibbs Sampler for 1000 step !
            >>> qc.checkFeasibility()
            The q-coloring with 3 colors is feasible !!
            >>> qc.exportGraphViz()
            *---- exporting a dot file for GraphViz tools ---------*
            Exporting to randomGraph-qcoloring.dot
            fdp -Tpng randomGraph-qcoloring.dot -o randomGraph-qcoloring.png

        .. image:: randomGraph-qcoloring.png
            :alt: 3-coloring of a random graph
            :width: 300 px
            :align: center
        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        vertexkeys = [x for x in self.vertices]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            node += ', style = "filled", color = %s' \
                    % self.vertices[vertexkeys[i]]['color']
            node += '];\n'                
            fo.write(node)
        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    edge = 'n'+str(i+1)
                    if edges[frozenset( [vertexkeys[i], vertexkeys[j]])] > Med:

                        edge0 = edge+'-- n'+str(j+1)+' [dir=both,style="setlinewidth(1)",color=black, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)
                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
                        edge0 = edge+'-- n'+str(j+1)+' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        if layout == None:
            if self.gClass in (GridGraph,RandomTree):
                commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            elif self.gClass == CycleGraph:
                commandString = 'circo -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            else:
                commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = layout+' -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')


class IsingModel(Graph):
    """
    Specialisation of a Gibbs Sampler for the Ising model

    Example:
        >>> from graphs import GridGraph, IsingModel
        >>> g = GridGraph(n=15,m=15)
        >>> g.showShort()
        *----- show short --------------*
        Grid graph    :  grid-6-6
        n             :  6
        m             :  6
        order         :  36
        >>> im = IsingModel(g,beta=0.3,nSim=100000,Debug=False)
        Running a Gibbs Sampler for 100000 step !
        >>> im.exportGraphViz(colors=['lightblue','lightcoral'])
        *---- exporting a dot file for GraphViz tools ---------*
        Exporting to grid-15-15-ising.dot
        fdp -Tpng grid-15-15-ising.dot -o grid-15-15-ising.png

    .. image:: grid-15-15-ising.png
       :alt: ising configuration of a 15x15 grid with beta=0.3 
       :width: 300 px
       :align: center
    """
    def __init__(self,g,beta=0,
                nSim=None,
                Debug=False):
        from copy import deepcopy
        self.gClass = g.__class__
        self.name = '%s-ising' % g.name
        if isinstance(g.vertices,dict):
            self.vertices = deepcopy(g.vertices)
        else:
            self.vertices = dict()
            for v in g.vertices:
                self.vertices[v] = {'name':v,'shortName':v}
        self.order = len(self.vertices)
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = g.size
        self.gamma = deepcopy(g.gamma)
        for v in self.vertices:
            self.vertices[v]['spin'] = 0
        if nSim == None:
            nSim = len(self.edges)
        self.nSim = nSim
        self.generateSpinConfiguration(beta=beta,Debug=Debug)
        self.SpinEnergy = self.computeSpinEnergy()/self.size

    def generateSpinConfiguration(self,beta=0,nSim=None,Debug=False):
        from random import choice, random
        from math import exp
        if nSim == None:
            nSim = self.nSim
        print('Running a Gibbs Sampler for %d step !' % nSim)
        for s in range(nSim):
            verticesKeys = [v for v in self.vertices]
            v = choice(verticesKeys)
            plusNeighbors = [x for x in self.gamma[v] if self.vertices[x]['spin'] == 1]
            nPlus = len(plusNeighbors)
            minusNeighbors = [x for x in self.gamma[v] if self.vertices[x]['spin'] == -1]
            nMinus = len(minusNeighbors)
            numerator = exp(2*beta*(nPlus-nMinus))
            threshold = numerator/(numerator+1)
            U = random()
            if U < threshold:
                self.vertices[v]['spin'] = 1
            else:
                self.vertices[v]['spin'] = -1
            if Debug:
                print('Spin energy: %d' % (self.computeSpinEnergy()) )
                print('s,v,nPlus,nMinus,numerator,threshold,U,spin\n',\
                      s,v,nPlus,nMinus,numerator,threshold,U,self.vertices[v]['spin'])

    def computeSpinEnergy(self):
        """
        Spin energy H(c) of a spin configuration is
        H(c) = -sum_{{x,y} in self.edges}[spin_c(x)*spin_c(y)]
        """
        Hc = 0
        for e in self.edges:
            pair = list(e)
            x = pair[0]
            y = pair[1]
            Hc -= self.vertices[x]['spin'] * self.vertices[y]['spin']
        return Hc        
    
    def exportGraphViz(self,fileName=None,
                       Comments=True,
                       graphType='png',
                       graphSize='7,7',
                       edgeColor='black',
                       colors=['gold','lightblue']):
        """
        Exports GraphViz dot file  for Ising models drawing filtering.

        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        vertexkeys = [x for x in self.vertices]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            if self.vertices[vertexkeys[i]]['spin'] == 1:
                color=colors[0]
            elif self.vertices[vertexkeys[i]]['spin'] == -1:
                color=colors[1]
            else:
                color=None
            if color != None:
                node += ', style = "filled", color = %s' % color
            node += '];\n'                
            fo.write(node)
        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    edge = 'n'+str(i+1)
                    if edges[frozenset( [vertexkeys[i], vertexkeys[j]])] > Med:

                        edge0 = edge+'-- n'+str(j+1)+\
                                ' [dir=both,style="setlinewidth(1)",color='+edgeColor+\
                                ' arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)
                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
                        edge0 = edge+'-- n'+str(j+1)+' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        if self.gClass in (GridGraph,TriangulatedGrid,RandomTree):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        elif self.gClass == CycleGraph:
            commandString = 'circo -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

class MetropolisChain(Graph):
    """
    Specialisation of the graph class for implementing a generic
    Metropolis Markov Chain Monte Carlo sampler with a given probability distribution
    probs = {'v1': x, 'v2': y, ...}

    Usage example:
        >>> from graphs import *
        >>> g = Graph(numberOfVertices=5,edgeProbability=0.5)
        >>> g.showShort()
        *---- short description of the graph ----*
        Name             : 'randomGraph'
        Vertices         :  ['v1', 'v2', 'v3', 'v4', 'v5']
        Valuation domain :  {'max': 1, 'med': 0, 'min': -1}
        Gamma function   : 
        v1 -> ['v2', 'v3', 'v4']
        v2 -> ['v1', 'v4']
        v3 -> ['v5', 'v1']
        v4 -> ['v2', 'v5', 'v1']
        v5 -> ['v3', 'v4']        
        >>> probs = {}
        >>> n = g.order
        >>> i = 0
        >>> verticesList = [x for x in g.vertices]
        >>> verticesList.sort()
        >>> for v in verticesList:
        ...     probs[v] = (n - i)/(n*(n+1)/2)
        ...     i += 1
        >>> met = MetropolisChain(g,probs)
        >>> frequency = met.checkSampling(verticesList[0],nSim=30000)
        >>> for v in verticesList:
        ...     print(v,probs[v],frequency[v])
        v1 0.3333 0.3343
        v2 0.2666 0.2680
        v3 0.2    0.2030 
        v4 0.1333 0.1311
        v5 0.0666 0.0635
        >>> met.showTransitionMatrix()
        * ---- Transition Matrix -----
          Pij  | 'v1'    'v2'    'v3'    'v4'    'v5'	  
          -----|-------------------------------------
          'v1' |  0.23	 0.33	 0.30	 0.13	 0.00	 
          'v2' |  0.42   0.42 	 0.00	 0.17	 0.00	 
          'v3' |  0.50	 0.00	 0.33 	 0.00	 0.17	 
          'v4' |  0.33	 0.33	 0.00	 0.08 	 0.25	 
          'v5' |  0.00	 0.00	 0.50	 0.50	 0.00 	 
    """
    def __init__(self,g,
                 probs = None):
        from copy import deepcopy
        from random import choice
        self.name = '%s-metro' % g.name
        if isinstance(g.vertices,dict):
            self.vertices = deepcopy(g.vertices)
        else:
            self.vertices = dict()
            for v in g.vertices:
                self.vertices[v] = {'name':v,'shortName':v}
        self.order = len(self.vertices)
        if probs == None:
            for v in self.vertices:
                self.vertices[v]['prob'] = 1.0/self.order
        else:
            for v in self.vertices:
                self.vertices[v]['prob'] = probs[v]       
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = g.size
        self.gamma = deepcopy(g.gamma)
        self.transition = self.computeTransitionMatrix()

    def computeTransitionMatrix(self):
        from decimal import Decimal
        transition = {}
        for si in self.vertices:
            transition[si] = {}
            di = len(self.gamma[si])
            pi = self.vertices[si]['prob']
            for sj in self.vertices:
                if si != sj:
                    if sj in self.gamma[si]:
                        dj = len(self.gamma[sj])
                        pj = self.vertices[sj]['prob']
                        transition[si][sj] =\
                                    Decimal( str( min(1.0,(pj*di)/(pi*dj))/di ) )
                    else:
                        transition[si][sj] = Decimal('0')
                else:
                    sp = 0.0
                    for sx in self.gamma[si]:
                        dx = len(self.gamma[sx])
                        px = self.vertices[sx]['prob']
                        sp += min(1.0,(px*di)/(pi*dx))/di
                    transition[si][sj] = Decimal(str(1.0 - sp))
        return transition
                  
    def MCMCtransition(self,si,Debug=False):
        from random import random,choice
        neighborsSi = [x for x in self.gamma[si]]
        di = len(self.gamma[si])
        if di == 0:
            return si
        pi = self.vertices[si]['prob']
        sj = choice(neighborsSi)
        dj = len(self.gamma[sj])
        pj = self.vertices[sj]['prob']
        U = random()
        threshold = min(1.0,(pj*di)/(pi*dj))
        if Debug:
            print(si,di,pi,sj,dj,pj,U,threshold)
        if U < threshold:
            return sj
        else:
            return si

    def checkSampling(self,si,nSim):
        frequency = {}
        for v in self.vertices:
            frequency[v] = 0.0
        sc = si
        for i in range(nSim):
            sc = self.MCMCtransition(sc)
            frequency[sc] += 1.0
        for x in frequency:
            frequency[x] /= nSim
        return frequency

    def saveCSVTransition(self,fileName='transition',Debug=False):
        """Persistent storage of the transition matrix in the form of
            a csv file. """
        import csv
        from decimal import Decimal
        
        if Debug:
            print('*--- Saving transition matrix P_ij into file: %s.csv> ---*' %\
                  (fileName))
        fileNameExt = str(fileName)+str('.csv')
        fo = open(fileNameExt, 'w')
        csvfo = csv.writer(fo,quoting=csv.QUOTE_NONNUMERIC)
        verticesList = [x for x in self.vertices]
        verticesList.sort()
        headerText = ["P_ij"] + verticesList
        if Debug:
            print(headerText)
        csvfo.writerow(headerText)
        relation = self.transition
        for x in verticesList:
            rowText = [x]
            for y in verticesList:
                rowText.append( Decimal('%.5f' % float(relation[x][y])) )
            if Debug:
                print(rowText)
            csvfo.writerow(rowText)
        fo.close()

    def showTransitionMatrix(self,Sorted=True,\
                          IntegerValues=False,\
                          vertices=None,\
                          relation=None,\
                          ndigits=2,\
                          ReflexiveTerms=True):
        """
        Prints on stdout the transition probabilities in
        vertices X vertices table format.
        """
        if vertices == None:
            vertices = self.vertices
        if relation == None:
            try:
                relation = self.transition
            except:
                relation = self.computeTransitionMatrix()
        print('* ---- Transition Matrix -----\n', end=' ')
        print(' S   | ', end=' ')
        verticesList = []
        for x in vertices:
            if isinstance(x,frozenset):
                try:
                    verticesList += [(vertices[x]['shortName'],x)]
                except:
                    verticesList += [(verticess[x]['name'],x)]
            else:
                verticesList += [(str(x),x)]
        if Sorted:
            verticesList.sort()
        print(verticesList)
        verticesList.sort()
        for x in verticesList:
            print("'"+x[0]+"'\t ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in verticesList:
            print("'"+x[0]+"' | ", end=' ')
            for y in verticesList:
                if x != y:
                    formatString = '%%2.%df\t' % ndigits
                    print(formatString % (relation[x[1]][y[1]]), end=' ')
                else:
                    if ReflexiveTerms:
                        formatString = '%%2.%df\t' % ndigits
                        print(formatString % (relation[x[1]][y[1]]), end=' ')
                    else:  
                        formatString = ' - \t'
                        print(formatString, end=' ')                    
            print()
        print('\n')
        
class MISModel(Graph):
    """
    Specialisation of a Gibbs Sampler for the hard code model,
    that is a random MIS generator.

    Example:
        >>> from graphs import MISModel
        >>> from digraphs import CirculantDigraph        
        >>> dg = CirculantDigraph(order=15)
        >>> g = dg.digraph2Graph()
        >>> g.showShort()
        *---- short description of the graph ----*
        Name             : 'c15'
        Vertices         :  ['1', '10', '11', '12', '13', '14',
                             '15', '2', '3', '4', '5', '6', '7',
                             '8', '9']
        Valuation domain :  {'med': 0, 'min': -1, 'max': 1}
        Gamma function   : 
        1 -> ['2', '15']
        10 -> ['11', '9']
        11 -> ['10', '12']
        12 -> ['13', '11']
        13 -> ['12', '14']
        14 -> ['15', '13']
        15 -> ['1', '14']
        2 -> ['1', '3']
        3 -> ['2', '4']
        4 -> ['3', '5']
        5 -> ['6', '4']
        6 -> ['7', '5']
        7 -> ['6', '8']
        8 -> ['7', '9']
        9 -> ['10', '8']
        >>> mis = MISModel(g)
        Running a Gibbs Sampler for 1050 step !
        >>> mis.checkMIS()
        {'2','4','7','9','11','13','15'}  is maximal !
        >>> mis.exportGraphViz()
        *---- exporting a dot file for GraphViz tools ---------*
        Exporting to c15-mis.dot
        fdp -Tpng c15-mis.dot -o c15-mis.png

    .. image:: c15-mis.png
       :alt: 15-cycle with colored MIS
       :width: 300 px
       :align: center
       
    """
    def __init__(self,g,
                 nSim=None,
                 maxIter=20,
                 seed=None,
                 Debug=False):
        from copy import deepcopy
        self.gClass = deepcopy(g.__class__)
        self.name = '%s-mis' % g.name
        if isinstance(g.vertices,dict):
            self.vertices = deepcopy(g.vertices)
        else:
            self.vertices = dict()
            for v in g.vertices:
                self.vertices[v] = {'name':v,'shortName':v}
        self.order = len(self.vertices)
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = g.size
        self.gamma = deepcopy(g.gamma)
        if nSim == None:
            nSim = len(self.edges)*10
        self.nSim = nSim
        unCovered = set([x for x in self.vertices])
        _iter = 0
        while unCovered != set() and _iter < maxIter:
            _iter += 1
            print('Iteration: ', _iter)
            self.generateMIS(Reset=True,
                             nSim=nSim,seed=seed,Debug=Debug)
            mis,misCover,unCovered = self.checkMIS()

    def generateMIS(self,Reset=True,nSim=None,seed=None,Comments=True,Debug=False):
        import random
        random.seed(seed)
        from math import exp
        if nSim == None:
            nSim = self.nSim
        verticesKeys = [v for v in self.vertices]
        if Reset:
            for v in verticesKeys:
                self.vertices[v]['mis'] = 0
        if Comments:
            print('Running a Gibbs Sampler for %d step !' % nSim)
        for s in range(nSim):
            v = random.choice(verticesKeys)
            Potential = True
            for x in self.gamma[v]:
                if self.vertices[x]['mis'] == 1:
                    Potential = False
                    break
            if Potential:
                self.vertices[v]['mis'] = 1
            else:
                self.vertices[v]['mis'] = -1
            if Debug:               
                print('s,v,neighbors,mis\n',\
                      s,v,self.gamma[v],self.vertices[v]['mis'])
        self.mis,self.misCover,self.unCovered = self.checkMIS(Comments=Debug)

    def checkMIS(self,Comments=True):
        """
        Verify maximality of independent set.

        .. note::
             Returns three sets: an independent choice,
             the covered vertices, and the remaining uncovered vertices.
             When the last set is empty, the independent choice is maximal.
        """
        cover = set()
        mis = set()
        for x in self.vertices:
            if self.vertices[x]['mis'] == 1:
                cover = cover | self.gamma[x]
                mis.add(x)
        misCover = mis | cover
        unCovered = set(self.vertices.keys()) - misCover
        if Comments:
            if unCovered == set():
                print(mis,' is maximal !')
            else:
                print(mis,' is not maximal, uncovered = ',unCovered)
        return mis,misCover,unCovered
    
    def exportGraphViz(self,fileName=None,
                       Comments=True,
                       graphType='png',
                       graphSize='7,7',
                       misColor='lightblue'):
        """
        Exports GraphViz dot file  for MIS models drawing filtering.

        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        vertexkeys = [x for x in self.vertices]
        n = len(vertexkeys)
        edges = self.edges
        Med = self.valuationDomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2019", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = str(self.vertices[vertexkeys[i]]['shortName'])
            except:
                try:
                    nodeName = self.vertices[vertexkeys[i]]['name']
                except:
                    nodeName = str(vertexkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            if self.vertices[vertexkeys[i]]['mis'] == 1:
                color=misColor
            else:
                color=None
            if color != None:
                node += ', style = "filled", color = %s' % color
            node += '];\n'                
            fo.write(node)
        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    edge = 'n'+str(i+1)
                    if edges[frozenset( [vertexkeys[i], vertexkeys[j]])] > Med:

                        edge0 = edge+'-- n'+str(j+1)+' [dir=both,style="setlinewidth(1)",color=black, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)
                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
                        edge0 = edge+'-- n'+str(j+1)+' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        if self.gClass in (GridGraph,RandomTree):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        elif self.gClass == CycleGraph:           
            commandString = 'circo -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                
##########################

class LineGraph(Graph):
    """
    Line graphs represent the **adjacencies between edges** of a graph instance.

    Iterated line graph constructions are usually expanding, except for chordless cycles,
    where the same cycle is repeated. And, for non-closed paths (interupted cycles), where iterated line graphs
    progressively reduce one by one the number of vertices and edges and become eventually an empty graph. 

    >>> g = CycleGraph(order=5)
    >>> g
    *------- Graph instance description ------*
    Instance class   : CycleGraph
    Instance name    : cycleGraph
    Graph Order      : 5
    Graph Size       : 5
    Valuation domain : [-1.00; 1.00]
    Attributes       : ['name', 'order', 'vertices', 'valuationDomain',
                        'edges', 'size', 'gamma']
    g.showShort()
    *---- short description of the graph ----*
    Name             : 'cycleGraph'
    Vertices         :  ['v1', 'v2', 'v3', 'v4', 'v5']
    Valuation domain :  {'min': Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
    Gamma function   : 
    v1 -> ['v2', 'v5']
    v2 -> ['v1', 'v3']
    v3 -> ['v2', 'v4']
    v4 -> ['v3', 'v5']
    v5 -> ['v4', 'v1']
    degrees      :  [0, 1, 2, 3, 4]
    distribution :  [0, 0, 5, 0, 0]
    nbh depths   :  [0, 1, 2, 3, 4, 'inf.']
    distribution :  [0, 0, 5, 0, 0, 0]
    # the line graph of the 5-cycle graph
    >>> lg = LineGraph(g)
    >>> lg
    *------- Graph instance description ------*
    Instance class   : LineGraph
    Instance name    : line-cycleGraph
    Graph Order      : 5
    Graph Size       : 5
    Valuation domain : [-1.00; 1.00]
    Attributes       : ['name', 'graph', 'valuationDomain', 'vertices',
                        'order', 'edges', 'size', 'gamma']
    >>> lg.showShort()
    *---- short description of the graph ----*
    Name             : 'line-cycleGraph'
    Vertices         :  [frozenset({'v2', 'v1'}), frozenset({'v1', 'v5'}), frozenset({'v2', 'v3'}),
                         frozenset({'v4', 'v3'}), frozenset({'v4', 'v5'})]
    Valuation domain :  {'min': Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
    Gamma function   : 
    frozenset({'v2', 'v1'}) -> [frozenset({'v2', 'v3'}), frozenset({'v1', 'v5'})]
    frozenset({'v1', 'v5'}) -> [frozenset({'v2', 'v1'}), frozenset({'v4', 'v5'})]
    frozenset({'v2', 'v3'}) -> [frozenset({'v2', 'v1'}), frozenset({'v4', 'v3'})]
    frozenset({'v4', 'v3'}) -> [frozenset({'v2', 'v3'}), frozenset({'v4', 'v5'})]
    frozenset({'v4', 'v5'}) -> [frozenset({'v4', 'v3'}), frozenset({'v1', 'v5'})]
    degrees      :  [0, 1, 2, 3, 4]
    distribution :  [0, 0, 5, 0, 0]
    nbh depths   :  [0, 1, 2, 3, 4, 'inf.']
    distribution :  [0, 0, 5, 0, 0, 0]

    MISs in line graphs provide maximal matchings - maximal sets of independent edges - in the original graph.

    >>> c8 = CycleGraph(order=8)
    >>> lc8 = LineGraph(c8)
    >>> lc8.showMIS()
    *---  Maximal Independent Sets ---*
    [frozenset({'v3', 'v4'}), frozenset({'v5', 'v6'}), frozenset({'v1', 'v8'})]
    [frozenset({'v2', 'v3'}), frozenset({'v5', 'v6'}), frozenset({'v1', 'v8'})]
    [frozenset({'v8', 'v7'}), frozenset({'v2', 'v3'}), frozenset({'v5', 'v6'})]
    [frozenset({'v8', 'v7'}), frozenset({'v2', 'v3'}), frozenset({'v4', 'v5'})]
    [frozenset({'v7', 'v6'}), frozenset({'v3', 'v4'}), frozenset({'v1', 'v8'})]
    [frozenset({'v2', 'v1'}), frozenset({'v8', 'v7'}), frozenset({'v4', 'v5'})]
    [frozenset({'v2', 'v1'}), frozenset({'v7', 'v6'}), frozenset({'v4', 'v5'})]
    [frozenset({'v2', 'v1'}), frozenset({'v7', 'v6'}), frozenset({'v3', 'v4'})]
    [frozenset({'v7', 'v6'}), frozenset({'v2', 'v3'}), frozenset({'v1', 'v8'}), frozenset({'v4', 'v5'})]
    [frozenset({'v2', 'v1'}), frozenset({'v8', 'v7'}), frozenset({'v3', 'v4'}), frozenset({'v5', 'v6'})]
    number of solutions:  10
    cardinality distribution
    card.:  [0, 1, 2, 3, 4, 5, 6, 7, 8]
    freq.:  [0, 0, 0, 8, 2, 0, 0, 0, 0]
    execution time: 0.00029 sec.

    The two last MISs of cardinality 4 (see Lines 14-15 above) give
    **isomorphic perfect maximum matchings** of the 8-cycle graph.
    Every vertex of the cycle is adjacent to a matching edge.
    Odd cyle graphs do not admid any perfect matching.

    >>> maxMatching = c8.computeMaximumMatching()
    >>> c8.exportGraphViz(fileName='maxMatchingcycleGraph',
                          matching=maxMatching)
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to maxMatchingcyleGraph.dot
    Matching:  {frozenset({'v1', 'v2'}), frozenset({'v5', 'v6'}),
                frozenset({'v3', 'v4'}), frozenset({'v7', 'v8'}) }
    circo -Tpng maxMatchingcyleGraph.dot -o maxMatchingcyleGraph.png

    .. image:: maxMatchingcycleGraph.png
        :alt: maximum matching colored c8
        :width: 300 px
        :align: center 
    """
    def __init__(self, graph):
        from copy import deepcopy
        from collections import OrderedDict
        from graphs import CycleGraph
        from digraphsTools import omin

        if graph.__class__ == CycleGraph:
            self.__class__ = CycleGraph
        self.name = 'line-' + graph.name
        self.graph = deepcopy(graph)
        self.valuationDomain = deepcopy(graph.valuationDomain)
        Max = self.valuationDomain['max']
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']      
        vertices = OrderedDict()
        for edge in graph.edges:
            if graph.edges[edge] > Med:
                vertices[edge] = {'name': str(list(edge))}
        self.vertices = vertices
        self.order = len(vertices)
        edges = OrderedDict()
        for v1 in vertices:
            for v2 in vertices:
                if v1 != v2:
                    intv = v1 & v2
                    unv = v1 | v2
                    if len(intv) > 0:
                        edges[frozenset([frozenset(v1),frozenset(v2)])] = min(graph.edges[v1],graph.edges[v2])
                    else:
                        edges[frozenset([frozenset(v1),frozenset(v2)])] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

####################

class PermutationGraph(Graph):
    """
    Martin Ch. Gulombic, Agorithmic Graph Theory and Perfect Graphs 2nd Ed.,
    Annals of Discrete Mathematics 57, Elsevier, Chapter 7, pp 157-170.

    >>> from graphs import PermutationGraph
    >>> g = PermutationGraph()
    >>> g
    *------- Graph instance description ------*
    Instance class   : PermutationGraph
    Instance name    : permutationGraph
    Graph Order      : 6
    Permutation      : [4, 3, 6, 1, 5, 2]
    Graph Size       : 9
    Valuation domain : [-1.00; 1.00]
    Attributes       : ['name', 'vertices', 'order', 'permutation',
                        'valuationDomain', 'edges', 'size', 'gamma']
    >>> g.exportGraphViz()
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to permutationGraph.dot
    fdp -Tpng permutationGraph.dot -o permutationGraph.png

    .. image:: permutationGraph.png
        :alt: Default permutation graph
        :width: 300 px
        :align: center 
 
    """
    def __init__(self,permutation=[4,3,6,1,5,2],Debug=False):
        from collections import OrderedDict
        self.name = 'permutationGraph'
        vertices = OrderedDict()
        order = len(permutation)
        for i in range(1,order+1):
            vertices[str(i)] = {'name': str(i)}
        self.vertices = vertices
        self.order = len(vertices)
        self.permutation = permutation
        self.valuationDomain = {'min': Decimal('-1'),
                                'med': Decimal('0'),
                                'max': Decimal('1')}
        Min = self.valuationDomain['min']
        Max = self.valuationDomain['max']
        
        edges = OrderedDict()
        for i in range(1,order+1):
            for j in range(i+1,order+1):
                invi = permutation.index(i) + 1
                invj = permutation.index(j) + 1
                if Debug:
                    print('i,invi, j, invj',i,invi, j, invj)
                    print((i - j)*(invi - invj))
                if (i - j)*(invi - invj) < 0:
                    edges[frozenset([str(i),str(j)])] = Max
                else:
                    edges[frozenset([str(i),str(j)])] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()

    def transitiveOrientation(self):
        """
        Renders a digraph where each edge of the permutation graph *self*
        is converted into an arc oriented in increasing order of the adjacent vertices' numbers.
        This orientation is always transitive and delivers a weak ordering of the vertices.
    
        >>> dg = g.transitiveOrientation()
        >>> dg
        *------- Digraph instance description ------*
        Instance class   : TransitiveDigraph
        Instance name    : oriented_permutationGraph
        Digraph Order      : 6
        Digraph Size       : 9
        Valuation domain : [-1.00; 1.00]
        Determinateness  : 100.000
        Attributes       : ['name', 'order', 'actions', 'valuationdomain',
                            'relation', 'gamma', 'notGamma', 'size']
        >>> dg.exportGraphViz()
        *---- exporting a dot file for GraphViz tools ---------*
        Exporting to oriented_permutationGraph.dot
        0 { rank = same; 1; 2; }
        1 { rank = same; 5; 3; }
        2 { rank = same; 4; 6; }
        dot -Grankdir=TB -Tpng oriented_permutationGraph.dot -o oriented_permutationGraph.png

        .. image:: oriented_permutationGraph.png
            :alt: Transitive orientation of a permutation graph
            :width: 200 px
            :align: center 

        """
        from digraphs import EmptyDigraph
        from transitiveDigraphs import TransitiveDigraph
        from copy import deepcopy
        
        g = EmptyDigraph(order=self.order)
        g.__class__ = TransitiveDigraph
        g.name = 'oriented_'+self.name
        g.actions = deepcopy(self.vertices)
        g.valuationdomain = deepcopy(self.valuationDomain)
        Max = g.valuationdomain['max']
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        relation = {}
        for x in g.actions:
            relation[x] = {}
            for y in g.actions:
                if x == y:
                    relation[x][y] = Med
                else:
                    if self.edges[frozenset([x,y])] > Med:
                        if int(x) < int(y):
                            relation[x][y] = Max
                        else:
                            relation[x][y] = Min
                    else:
                        relation[x][y] = Min
        g.relation = relation
        g.size = g.computeSize()
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        return g

    def computeMinimalVertexColoring(self,colors=None,Comments=False,Debug=False):
        """
        Computes a vertex coloring by using a minimal number of color queues for sorting the
        given permutation. Sets by the way the chromatic number of the graph.
        """
        permutation = self.permutation
        vertexKeys = [x for x in self.vertices]
        n = len(permutation)
        if colors == None:
            colors = ['gold','lightblue','lightcoral','lightyellow','orange','gray',\
                  'lightpink','seagreen1','skyblue','wheat1','lightsalmon','wheat']
        nc = len(colors)
        Q = [[0,[0]] for x in range(nc)]
        for i in range(n):
            for j in range(nc):
                try:
                    jQpt = Q[j][0]
                except IndexError:
                    print('!!! Error: The number of available colors %d is not sufficient !!!' % nc)
                    print(colors)
                    return
                if permutation[i] > Q[j][1][jQpt]:
                    Q[j][1].append(permutation[i])
                    Q[j][0] += 1
                    break
        if Debug:
            print(Q)
        vertexColor = [0 for i in range(n)]
        chromNumber = 0
        for j in range(nc):
            nj = len(Q[j][1])
            if nj > 1:
                chromNumber += 1
                for i in range(1,nj):
                    k = Q[j][1][i] - 1
                    vertexColor[k] = colors[j]
        self.chromaticNumber = chromNumber
        if Debug:
            print(vertexColor)
            print(chromNumber)
        for i in range(n):
            self.vertices[vertexKeys[i]]['color'] = vertexColor[i]
            if Comments:
                print('vertex %s: %s' % (vertexKeys[i],vertexColor[i]))
    
class RandomPermutationGraph(PermutationGraph):
    """
    A generator for random permutation graphs.
    """
    def __init__(self,order=6,seed=None):
        import random
        random.seed(seed)
        permutation = list(range(1,order+1))
        random.shuffle(permutation)
        g = PermutationGraph(permutation=permutation)
        att = [a for a in g.__dict__]
        for a in att:
            self.__dict__[a] = g.__dict__[a]
        self.name = 'randomPermGraph'
        
# --------------testing the module ----
if __name__ == '__main__':

    #g = PermutationGraph(permutation=[4,3,6,1,5,2])
    #g = CycleGraph(order=6)
    #g = Graph('test')
##    g = RandomGraph(seed=100)
##    print(g)
##    g.exportGraphViz()
##    #g.exportPermutationGraphViz()
##    #g.computeMinimalVertexColoring(Comments=True,Debug=True)
##    #g.exportGraphViz(WithVertexColoring=True)
##
##    #b = BestDeterminedSpanningForest(g)
##    #print(b)
##    if g.isComparabilityGraph(Debug=True):
##        print('Comparability Graph ? = True',g.edgeOrientations)
##        dg = g.computeTransitivelyOrientedDigraph()
##        if dg != None:
##            print(dg)
##            print(dg.computeTransitivityDegree())
##            dg.exportGraphViz()
##    else:
##        print('Comparability Graph ? = False')
##    print(g.isTriangulated())
##    print((-g).isComparabilityGraph())
##    g.isIntervalGraph(Comments=True)
##
##    intervals = [(1,5),(2,3),(3,5),(7,8),(3,5),(1,9)]
##    i = LineIntersectionsGraph(intervals)
##    print(i)
##    print(i.intervals)
##    print(i.isTriangulated())
##    print((-i).isTriangulated())

##    ri = RandomGraph(order=8,seed=4335)
##    print(ri)
##    #print(ri.intervals)
##    #print(ri.isIntervalGraph(Comments=True))
##    #print(ri.isTriangulated())
##    #print((-ri).isTriangulated())
##    ri.exportGraphViz()
##    #ri.isSplitGraph(Comments=True)
##    #ri.isPermutationGraph(Comments=True)
##    #print(ri.computePermutation())
##    if ri.isComparabilityGraph():
##        ri.exportEdgeOrientationsGraphViz('testColors1')
##    rid = -ri
##    if rid.isComparabilityGraph():
##        rid.exportEdgeOrientationsGraphViz('testColors2',palette=2)

    g = RandomGraph(order=9,edgeProbability=0.5)
    g.save('testPerfectGraph')
    g.name = 'testPerfectGraph'
    g.exportGraphViz()
    #print(g.breadthFirstSearch('v1',Debug=False))
    print(g.isPerfectGraph(Comments=True))
    g.computeGirth(girthType="odd",Comments=True)
    g.computeGirth(girthType="even",Comments=True)
    g.computeGirth(Comments=True)
    
##    rg = RandomPermutationGraph(order=6,seed=None)
##    print(rg)
##    dg = g.transitiveOrientation()
##    print(dg)
##    dg.exportGraphViz()
##    rgd = -rg
##    print(rgd)
##    
##    g = RandomGraph(order=8,seed=4335)
##    og = g.computeOrientedDigraph(PartiallyDetermined=True)
##    print('Transitivity degree: %.3f' % og.transitivityDegree)
##    gd = -g
##    ogd = gd.computeOrientedDigraph(PartiallyDetermined=True)
##    print('Dual transitivity degree: %.3f' % ogd.transitivityDegree)
##    print(g.computePermutation(Debug=False))
##    from digraphs import FusionDigraph
##    from linearOrders import LinearOrder
##    f1gd = FusionDigraph(og,ogd,'o-max')
##    s1 = LinearOrder.computeOrder(f1gd)
##    f2gd = FusionDigraph((-og),ogd,'o-max')
##    s2 = LinearOrder.computeOrder(f2gd)
##    print(s1)
##    print(s2)
##    permutation= Graph.computePermutation(g)
##    print(permutation)
##    gtest = PermutationGraph(permutation=permutation)
##    print(gtest)
##    print(g)
##    gtest.exportPermutationGraphViz()
##    

    #g = CycleGraph(order=12)
##    g = RandomGraph(order=7)
##    print(g)
##    g.showShort()
##    lg = LineGraph(g)
##    print(lg)
##    lg.showShort()
##    llg = LineGraph(lg)
##    print(llg)
##    llg.showShort()
##    lg.showMIS()
##    maxMatching = g.computeMaximumMatching(Comments=False)
##    g.exportGraphViz(matching=maxMatching)
    
        # from graphs import SnakeGraph
        # S = SnakeGraph(p=3,q=7)
        # S.showShort()
        # S.exportGraphViz('4_7_snake',lineWidth=3,arcColor="red")

##    from time import time
##    #g = GridGraph(4,4)
##    g = RandomGraph(order=30,seed=10)
##    #g.exportGraphViz()
##    #print(g._degreeLabelling())
##    #print(g._triplets(Comments=True))
##    t0 = time();print(len(g._computeChordlessCycles(Cycle3=True,Comments=False)));print(time()-t0)
##    t0 = time();print(len(g.computeChordlessCycles(Cycle3=True,Comments=False)));print(time()-t0)
    
    
    #g.save('test')
    #g = Graph('test')
##    ust = RandomSpanningTree(g,seed=200,Debug=False)
##    ust.showShort()
##    ust.showMore()
##    ust.dfs = ust.randomDepthFirstSearch()
##    ust.exportGraphViz(WithSpanningTree=True)
##    print(ust.prueferCode)
    
