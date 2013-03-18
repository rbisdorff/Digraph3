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
        if Empty:
            self.name = 'emptyInstance'
            self.vertices = dict()
            self.edges = dict()
            self.valuationDomain = {'min':-1, 'med': 0, 'max':1}
            self.gamma = dict()
        elif fileName==None:
            g = RandomGraph(order=numberOfVertices,\
                               edgeProbability=edgeProbability)
            self.name = g.name
            self.vertices = g.vertices
            self.order = len(self.vertices)
            self.edges = g.edges
            self.valuationDomain = g.valuationDomain
            self.gamma = self.gammaSets()
        else:
            fileNameExt = fileName+'.py'
            exec(compile(open(fileNameExt).read(), fileNameExt, 'exec'))
            self.name = fileName
            self.vertices = locals()['vertices']
            self.order = len(self.vertices)
            self.valuationDomain = locals()['valuationDomain']
            self.edges = locals()['edges']
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

    def save(self,fileName='tempGraph',option=None,Decimal=True):
        """
        Persistent storage of a Graph class instance in the form of a python source code file.
        """
        print('*--- Saving graph in file: <' + fileName + '.py> ---*')
        verticesKeys = [x for x in self.vertices]
        verticesKeys.sort()
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


    def exportGraphViz(self,fileName=None, noSilent=True,graphType='png',graphSize='7,7'):
        """
        Exports GraphViz dot file  for graph drawing filtering.

        Example:
           >>> g = Graph(numberOfVertices=5,edgeProbability=0.3)
           >>> g.exportGraphViz('randomGraph'))
        
        .. image:: ../../randomGraph.png
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
        self.gamma = self.gammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Grid graph    : ', self.name)
        print('n             : ', self.n)
        print('m             : ', self.m)
        print('order         : ', self.order)

class RandomTree(Graph):
    """
    random instance of a tree generated from a random Prüfer code
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

        self.gamma = self.gammaSets(Debug)
        if Debug:
            print('gamma = ', self.gamma)




# --------------testing the module ----
if __name__ == '__main__':

    ## # g = GridGraph(n=4,m=4)
    ## g = RandomGraph(order=7,edgeProbability=0.5)
    ## # comment out the next line and uncomment the previous for random instances
    ## # g = Graph('problem')
    ## # g.save()
    ## g = Graph('tempGraph')
    ## g.showShort()
    ## g.computeChordlessCycles(Comments=True,Debug=False)
    ## g.saveEdges(Agrum=True)

    ## # put Debug to <True> to get a detailed execution trace of the algorithm
    ## g.exportGraphViz('randGraph')
    ## dg = g.graph2Digraph()
    ## dg.showShort()
    ## dg.showRelationTable()
    ## dg.exportGraphViz('randdDigraph')
    ## dg.showStatistics()
    ## print "You may install graphviz and the digraphs module on your system"

    #g = RandomTree(order=30)
    ## print t.prueferCode
    ## t.exportGraphViz()
    g = Graph(numberOfVertices=5,edgeProbability=0.3)
    g.save()
    g.showShort()
    #g = Graph('tempGraph')
    print(g.depthFirstSearch(Debug=True))
    g.exportGraphViz('randomGraph')
    for x in g.vertices:
        print(x, g.vertices[x]['startDate'], g.vertices[x]['endDate'])
