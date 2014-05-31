#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#  Python 3 graphs.py module
#  Copyright (C)  2011-2013 Raymond Bisdorff
#############################################

class Graph(object):
    """
    Graph class implementation with a vertices and an edges dictionary
    and a gamma function (dictionary) from vertices to subsets of vertices.

    Example python3 session:
       >>> from graphs import Graph
       >>> g = Graph(numberOfVertices=5,edgeProbability=0.5)
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
    def __init__(self, fileName=None, Empty=False, numberOfVertices=7, edgeProbability=0.5):
        """
        Constructor for Graph objects.
        """
        from decimal import Decimal
        from copy import deepcopy
        
        if Empty:
            self.name = 'emptyInstance'
            self.vertices = dict()
            self.order = len(self.vertices)
            self.edges = dict()
            self.size = len(self.edges)
            self.valuationDomain = {'min':-1, 'med': 0, 'max':1}
            self.gamma = dict()
        elif fileName==None:
            g = RandomGraph(order=numberOfVertices,\
                               edgeProbability=edgeProbability)
            self.name = deepcopy(g.name)
            self.vertices = deepcopy(g.vertices)
            self.order = len(self.vertices)
            self.edges = deepcopy(g.edges)
            self.size = len(self.edges)
            self.valuationDomain = deepcopy(g.valuationDomain)
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
            self.size = len(self.edges)
            self.gamma = self.gammaSets()

    def graph2Digraph(self):
        """
        Converts a Graph object into a Digraph object.
        """
        from copy import deepcopy
        from digraphs import EmptyDigraph
        dg = EmptyDigraph(order=self.order)
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

    def saveEdges(self,fileName='graphEdges',Agrum=False,Decimal=True):
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
                if Debug:
                    print('e', e)
                pair = set(e)
                e1 = pair.pop()
                e2 = pair.pop()
                gamma[e1].add(e2)
                gamma[e2].add(e1)
        return gamma

    def chordlessPaths(self,Pk,v0, Comments = False, Debug = False):
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
        e = frozenset([v0,vn])
        if len(e) > 1:
            # not a reflexive link
            if self.edges[e] > Med and len(Pk) > 2:
                # we close the chordless pre cycle here
                detectedChordlessCycle = True
                if Debug:
                    print('Pk, len(Pk)', Pk, len(Pk))
                if len(Pk) > 3:
                    # only cycles of length 4 and more are holes in fact
                    self.xCC.append(Pk)
                    Pk.append(v0)
                    if Comments:
                        print('Chordless cycle certificate -->>> ', Pk)
                return detectedChordlessCycle
        if detectedChordlessCycle == False:
            NBvn = set(self.gamma[vn]) - set(Pk[1:len(Pk)])
            # exterior neighborhood of vn

            if Debug:
                print('vn, NBvn, Pk, Pk[1:len(Pk)] = ', vn, NBvn, Pk, Pk[1:len(Pk)])
            while NBvn != set():
                # we try in turn all neighbours of vn
                v = NBvn.pop()
                vCP = set(Pk)
                vCP.add(v)
                vCP = frozenset(vCP)
                if Debug:
                    print('v,vCP  =', v,vCP)
                if vCP not in self.visitedChordlessPaths:
                    # test history of paths
                    P = list(Pk)
                    if Debug:
                        print('P,P[:-1] = ', P,P[:-1])
                    noChord = True
                    for x in P[:-1]:
                        if Debug:
                            print('x = ', x)
                        if x != v0:
                            # we avoid the initial vertex
                            # to stay with a chordless precycle
                            ex = frozenset([x,v])
                            if Debug:
                                print('x, v, ex = ',x,v,ex)
                            if self.edges[ex] > Med:
                                # there is a chord
                                noChord = False
                                break
                    if noChord:
                        P.append(v)
                        if Debug:
                            print('P,v0',P,v0)
                        if self.chordlessPaths(P,v0,Comments,Debug):
                            # we continue with the current chordless precycle
                            detectedChordlessCycle=True
            if Debug:
                print('No further chordless precycles from ',vn,' to ',v0)
        return detectedChordlessCycle

    def computeChordlessCycles(self,Comments=True, Debug=False):
        """
        Renders the set of all chordless cycles observed in a Graph
        intance.
        """
        verticesKeys = [x for x in self.vertices]
        self.visitedChordlessPaths = set()
        chordlessCycles = []
        for v in verticesKeys:
            P = [v]
            self.xCC = []
            if self.chordlessPaths(P,v,Comments=Comments,Debug=Debug):
                chordlessCycles += self.xCC
        self.chordlessCycles = chordlessCycles
        chordlessCyclesList = [ (x,frozenset(x)) for x in chordlessCycles]
        if Debug:
            print('Return list of chordless cycles as a tuple (path, set)')
            for cc in chordlessCyclesList:
                print(cc)
        return chordlessCyclesList


    def exportGraphViz(self,fileName=None,
                       noSilent=True,
                       graphType='png',
                       graphSize='7,7'):
        """
        Exports GraphViz dot file  for graph drawing filtering.

        Example:
           >>> g = Graph(numberOfVertices=5,edgeProbability=0.3)
           >>> g.exportGraphViz('randomGraph'))

        .. image:: randomGraph.png
        """
        import os
        if noSilent:
            print('*---- exporting a dot file dor GraphViz tools ---------*')
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
        if noSilent:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2011", size="')
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
            try:
                if self.vertices[vertexkeys[i]]['spin'] == 1:
                    node += ', style = "filled", color = %s' % spinColor
            except:
                pass
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
        if isinstance(self,(GridGraph,RandomTree)):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')

    def depthFirstSearch(self,Debug=False):
        """
        Depth first search through a graph
        """
        def visitVertex(self, x, Debug = False):
            """
            Visits all followers of vertex x.
            """
            self.vertices[x]['color'] = 1
            ## self.date += 1
            self.vertices[x]['startDate'] = self.date
            self.dfsx.append(x)
            if Debug:
                print(' dfs %s, date = %d' % (str(self.dfs),  self.vertices[x]['startDate']))
            nextVertices = [y for y in self.gamma[x]]
            if Debug:
                print('   next ', nextVertices)
            for y in nextVertices:
                if self.vertices[y]['color'] == 0:
                    self.date += 1
                    visitVertex(self,y, Debug = Debug)
                    if self.vertices[x]['color'] == 1:
                        self.dfsx.append(x)
            self.vertices[x]['color'] = 2
            self.vertices[x]['endDate'] = self.date
            self.date += 1

        def visitAllVertices(self, Debug=False):
            """
            Mark the starting date for all vertices
            and controls the progress of the search with vertices colors:
            White (0), Grey (1), Black (2)
            """
            self.dfs = []
            for x in self.vertices:
                self.vertices[x]['color'] = 0
            self.date = 0
            for x in self.vertices:
                self.dfsx = []
                if self.vertices[x]['color'] == 0:
                    if Debug:
                        print('==>> Starting from %s ' % x)
                    visitVertex(self, x, Debug = Debug)
                    self.dfs.append(self.dfsx)
                #self.vertices[x]['color'] = 2
                #self.vertices[x]['endDate'] = self.date


        # ---- main -----
        visitAllVertices(self, Debug=Debug)
        return self.dfs


class RandomGraph(Graph):
    """
    Random instances of the Graph class

    *Parameters*:
        * order (positive integer)
        * edgeProbability (in [0,1])
    """
    def __init__(self,order=5,edgeProbability=0.4):
        from random import random
        self.name = 'randomGraph'
        self.order = order
        vertices = dict()
        for i in range(order):
            vertexKey = 'v%s' % (str(i+1))
            vertices[vertexKey] = {'shortName':vertexKey, 'name': 'random vertex'}
        self.vertices = vertices
        self.valuationDomain = {'min':-1,'med':0,'max':1}
        edges = dict()
        for x in vertices:
            for y in vertices:
                if x != y:
                    edgeKey = frozenset([x,y])
                    if random() > 1.0 - edgeProbability:
                        edges[edgeKey] = 1
                    else:
                        edges[edgeKey] = -1
        self.edges = edges
        self.size = len(self.edges)
        self.gamma = self.gammaSets()


class GridGraph(Graph):
    """
    Specialization of the general Graph class for generating
    temporary Grid graphs of dimension n times m.

    *Parameters*:
        * n,m > 0
        * valuationDomain ={'min':m, 'max':M}

    Default instantiation (5 times 5 Grid Digraph):
       * n = 5,
       * m=5,
       * valuationDomain = {'min':-1.0,'max':1.0}.

    Example of 5x5 GridGraph instance:

    .. image:: grid-5-5.png
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
        Min = valuationMin
        Max = valuationMax
        Med = (Max + Min)//2
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
        self.size = len(edges)
        self.gamma = self.gammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Grid graph    : ', self.name)
        print('n             : ', self.n)
        print('m             : ', self.m)
        print('order         : ', self.order)
        print('size          : ', self.size)

class RandomTree(Graph):
    """
    Random instance of a tree generated from a random Prüfer code.

    .. image:: randomTree.png
    """
    def __init__(self,order=None, prueferCode = None, myseed = None, Debug=False):
        from random import choice, seed
        self.name='randomTree'
        if order == None:
            if prueferCode == None:
                order = 6
            else:
                order = len(prueferCode) + 2
        self.order = order
        if Debug:
            print(self.name, self.order)

        vertices = dict()
        for i in range(order):
            vertexKey = i
            vertices[vertexKey] = {'shortName':str(vertexKey), 'name': 'random vertex'}
        self.vertices = vertices
        if Debug:
            print('vertices = ', self.vertices)

        self.valuationDomain = {'min':-1,'med':0,'max':1}
        if Debug:
            print('valuationDomain = ', self.valuationDomain)

        edges = dict()
        for i in range(order):
            for j in range(i+1,order):
                edgeKey = frozenset([i,j])
                edges[edgeKey] = -1
        self.edges = edges
        if Debug:
            print('edges = ',self.edges)
        if prueferCode == None:
            prueferCode = []
            if myseed != None:
                seed(myseed)
            for k in range(order-2):
                prueferCode.append( choice( list(range(order)) ) )
        self.prueferCode = prueferCode
        if Debug:
            print('prueferCode = ', self.prueferCode)

        degree = []
        for x in list(self.vertices.keys()):
            degree.append(1)
        for i in range(order-2):
            degree[prueferCode[i]] += 1
        if Debug:
            print('degrees = ', degree)

        for i in range(order-2):
            for j in list(self.vertices.keys()):
                if degree[j] == 1:
                    edgeKey = frozenset([prueferCode[i],j])
                    self.edges[edgeKey] = self.valuationDomain['max']
                    degree[j] -= 1
                    degree[prueferCode[i]] -= 1
                    break
        lastEdgeKey = frozenset([i for i in range(order) if degree[i] > 0])
        self.edges[lastEdgeKey] = self.valuationDomain['max']
        if Debug:
            print('updated edges = ', self.edges)
        self.size = len(self.edges)
        self.gamma = self.gammaSets(Debug)
        if Debug:
            print('gamma = ', self.gamma)

class Q_Coloring(Graph):
    """
    Generate a q-coloring of a Graph instance via a Gibbs MCMC sampler in
    nSim simulation steps (default = len(graph.edges)).
    
        Example 3-coloring of a grid 6x6 :
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
    """ 

    def __init__(self,g,colors=['gold','lightcoral','lightblue'],
                 nSim=None,maxIter=20,
                 Comments=True,Debug=False):
        from copy import deepcopy
        self.name = '%s-qcoloring' % g.name
        self.vertices = deepcopy(g.vertices)
        self.order = len(self.vertices)
        self.colors = colors
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = len(self.edges)
        self.gamma = deepcopy(g.gamma)
##        for v in self.vertices:
##            self.vertices[v]['color'] = colors[0]
        if nSim == None:
            nSim = len(self.edges)*2
        self.nSim = nSim
        infeasibleEdges = set([e for e in self.edges])
        _iter = 0
        while infeasibleEdges != set() and _iter < maxIter:
            _iter += 1
            print(_iter)
            self.generateFeasibleConfiguration(Reset=True,Debug=Debug)
            infeasibleEdges = self.checkFeasibility(Comments=Comments)
    
    def showConfiguration(self):
        for v in self.vertices:
            print(v,self.vertices[v]['color'])
            
    def generateFeasibleConfiguration(self,Reset=True,nSim=None,Debug=False):
        from random import choice
        if Reset:
            for v in self.vertices:
                self.vertices[v]['color'] = self.colors[0]           
        if nSim == None:
            nSim = self.nSim
        print('Running a Gibbs Sampler for %d step !' % nSim)
        for s in range(nSim):
            verticesKeys = [v for v in self.vertices]
            v = choice(verticesKeys)
            neighborColors = [self.vertices[x]['color']\
                                  for x in self.gamma[v]]
            feasibleColors = list(set(self.colors) - set(neighborColors))
            try:
                self.vertices[v]['color'] = choice(feasibleColors)
            except:
                if Debug:
                    print(s,v,'Warning !! Not feasible coloring')
                self.vertices[v]['color'] = choice(self.colors)
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
                       noSilent=True,
                       graphType='png',
                       graphSize='7,7'):
        """
        Exports GraphViz dot file  for q-coloring drawing filtering.

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
            >>> qc = Q_Coloring(g,Nsim=1000)
            Running a Gibbs Sampler for 1000 step !
            >>> qc.checkFeasibility()
            The q-coloring with 3 colors is feasible !!
            >>> qc.exportGraphViz()
            *---- exporting a dot file for GraphViz tools ---------*
            Exporting to randomGraph-qcoloring.dot
            fdp -Tpng randomGraph-qcoloring.dot -o randomGraph-qcoloring.png

        .. image:: randomGraph-qcoloring.png
        """
        import os
        if noSilent:
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
        if noSilent:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2014", size="')
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
        if isinstance(self,(GridGraph,RandomTree)):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')


class IsingModel(Graph):
    """
    Specialisation of a Gibbs Sampler for the Ising model

    Example:
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

    """
    def __init__(self,g,beta=0,
                nSim=None,
                Debug=False):
        from copy import deepcopy
        self.name = '%s-ising' % g.name
        self.vertices = deepcopy(g.vertices)
        self.order = len(self.vertices)
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = len(self.edges)
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
                       noSilent=True,
                       graphType='png',
                       graphSize='7,7',
                       colors=['gold','lightblue']):
        """
        Exports GraphViz dot file  for Ising models drawing filtering.

        """
        import os
        if noSilent:
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
        if noSilent:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2014", size="')
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

                        edge0 = edge+'-- n'+str(j+1)+' [dir=both,style="setlinewidth(1)",color=black, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)
                    elif edges[frozenset([vertexkeys[i],vertexkeys[j]])] == Med:
                        edge0 = edge+'-- n'+str(j+1)+' [dir=both, color=grey, arrowhead=none, arrowtail=none] ;\n'
                        fo.write(edge0)

        fo.write('}\n')
        fo.close()
        if isinstance(self,(GridGraph,RandomTree)):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')

class MetropolisChain(Graph):
    """
    Specialisation of the graph class for implementing a generic
    Markov Chain sampler with a given probability distribution
    probs = {'v1': x, 'v2': y, ...}

    """
    def __init__(self,g,
                 probs = None):
        from copy import deepcopy
        from random import choice
        self.name = '%s-metro' % g.name
        self.vertices = deepcopy(g.vertices)
        self.order = len(self.vertices)
        if probs == None:
            for v in self.vertices:
                self.vertices[v]['prob'] = 1.0/self.order
        else:
            for v in self.vertices:
                self.vertices[v]['prob'] = probs[v]       
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = len(self.edges)
        self.gamma = deepcopy(g.gamma)

    def transition(self,si,Debug=False):
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
        sc = si
        for i in range(nSim):
            sc = self.transition(sc)
            try:
                frequency[sc] += 1.0
            except:
                frequency[sc] = 1.0
        for x in frequency:
            frequency[x] /= nSim
        return frequency    
        
class MISModel(Graph):
    """
    Specialisation of a Gibbs Sampler for the hard code model,
    that is a random MIS generator.

    Example:
        >>> g = GridGraph(n=15,m=15)
        >>> g.showShort()
        *----- show short --------------*
        Grid graph    :  grid-6-6
        n             :  6
        m             :  6
        order         :  36
        size
        >>> mis = MISModel(g,nSim=100000,Debug=False)
        Running a Gibbs Sampler for 100000 step !
        >>> mis.exportGraphViz(colors=['lightblue','lightcoral'])
        *---- exporting a dot file for GraphViz tools ---------*
        Exporting to grid-15-15-mis.dot
        fdp -Tpng grid-15-15-mis.dot -o grid-15-15-mis.png

    .. image:: grid-15-15-mis.png

    """
    def __init__(self,g,beta=0,
                nSim=None,
                 maxIter=20,
                Debug=False):
        from copy import deepcopy
        self.name = '%s-mis' % g.name
        self.vertices = deepcopy(g.vertices)
        self.order = len(self.vertices)
        self.valuationDomain = deepcopy(g.valuationDomain)
        self.edges = deepcopy(g.edges)
        self.size = len(self.edges)
        self.gamma = deepcopy(g.gamma)
        if nSim == None:
            nSim = len(self.edges)*10
        self.nSim = nSim
##        for v in self.vertices:
##            self.vertices[v]['mis'] = 0
        unCovered = set([x for x in self.vertices])
        _iter = 0
        while unCovered != set() and _iter < maxIter:
            _iter += 1
            print(_iter)
            self.generateMIS(Reset=True,nSim=nSim,Debug=Debug)
            mis,misCover,unCovered = self.checkMIS()

    def generateMIS(self,Reset=True,nSim=None,Debug=False):
        from random import choice
        from math import exp
        if nSim == None:
            nSim = self.nSim
        if Reset:
            for v in self.vertices:
                self.vertices[v]['mis'] = 0
        print('Running a Gibbs Sampler for %d step !' % nSim)
        for s in range(nSim):
            verticesKeys = [v for v in self.vertices]
            v = choice(verticesKeys)
            neighbors = [x for x in self.gamma[v]]
            Potential = True
            for x in neighbors:
                if self.vertices[x]['mis'] == 1:
                    Potential = False
                    break
            if Potential:
                self.vertices[v]['mis'] = 1
            else:
                self.vertices[v]['mis'] = -1
            if Debug:               
                print('s,v,neighbors,mis\n',\
                      s,v,neighbors,self.vertices[v]['mis'])
        self.mis,self.misCover,self.unCovered = self.checkMIS(Comments=Debug)

    def checkMIS(self,Comments=True):
        """
        Verify maximality of independent set.

        ..note::
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
                       noSilent=True,
                       graphType='png',
                       graphSize='7,7',
                       misColor='lightblue'):
        """
        Exports GraphViz dot file  for Ising models drawing filtering.

        """
        import os
        if noSilent:
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
        if noSilent:
            print('Exporting to '+dotName)
        ## if bestChoice != set():
        ##     rankBestString = '{rank=max; '
        ## if worstChoice != set():
        ##     rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('strict graph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nGraphs Python module (graphviz), R. Bisdorff, 2014", size="')
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
        if isinstance(self,(GridGraph,RandomTree)):
            commandString = 'neato -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        else:
            commandString = 'fdp -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')


# --------------testing the module ----
if __name__ == '__main__':
    from time import sleep
    g = Graph(numberOfVertices=30,edgeProbability=0.2)
    probs = {}
    n = g.order
    i = 0
    for x in g.vertices:
        probs[x] = (n - i)/(n*(n+1)/2)
        i += 1
    sumProbs = 0.0
    for x in probs:
        sumProbs += probs[x]
    met = MetropolisChain(g,probs)
    #met.showShort()
    states = [x for x in met.vertices]
    frequency = met.checkSampling(states[0],nSim=30000)
    for x in probs:
        print(x,probs[x],frequency[x])
##    # Q-Colorings
##    g = Graph(numberOfVertices=30,edgeProbability=0.1)
##    #g = GridGraph(n=6,m=6)
##    g.showShort()
##    qc = Q_Coloring(g,nSim=100000,colors=['gold','lightcyan','lightcoral'],Debug=False)
##    qc.checkFeasibility(Comments=True)
##    qc.exportGraphViz()
##    # Ising Models
##    g = GridGraph(n=5,m=5)
##    g.showShort()
##    im = IsingModel(g,beta=0.1,nSim=10000,Debug=False)
##    H = im.computeSpinEnergy()
##    print( 'Spin energy = %d/%d = %.3f' % (H,im.size,H/im.size) )
##    print(im.SpinEnergy)
##    im.exportGraphViz()
##    im.save()
##    # MIS Models
##    g = GridGraph(n=10,m=10)
##    #g = Graph(numberOfVertices=30,edgeProbability=0.1)
##    g.showShort()
##    im = MISModel(g,nSim=100,beta=0.1,Debug=False)
##    im.checkMIS(Comments=True)
##    print('MIS       = ',im.mis)
##    print('Covered   = ',im.misCover)
##    print('Uncovered = ',im.unCovered)
##    print('MIS size  = ',len(im.mis))
##    im.exportGraphViz(misColor='coral')
