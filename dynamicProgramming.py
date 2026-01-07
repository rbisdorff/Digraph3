#!/Usr/bin/env python3
#########################
"""
Python3 implementation of a solver for **dynamic programming** problems.

Copyright (C) 2024-2025 Raymond Bisdorff

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

__version__ = "$Revision: Python 3.13.13 $"

from digraphs import Digraph
class DynamicProgrammingDigraph(Digraph):
    """
    Implementation of the *Bellman*, *Dijkstra*, or *Viterbi* min-sum algorithm for
    solving the canonical dynamic programming problem
    (see *Numerical Recipes, the Art of Scientific Computing* 3rd Ed. (2007),
    W.H. Press, S.A. Teukolsky, W.T: Vetterling and B.P. Flannery, Cambridge Unviersity Press,
    ISBN 978-0-521-88068-8, pp 555-562).

    We provide the lowest cost, respectively highest benefit, path from a single *source* node
    to a single *sink* node via an integer number *nstages* of
    execution stages characterized by finite subsets of execution states.

    Each forward arc from a state *x* in stage *i* to a state *y* in stage *i+1* is
    labelled with a decimal value stored, like the digraph relation,
    in a double dictionary *self.costs* attribute.
    
    """

    def __init__(self,fileName=None,Debug=False):
        from decimal import Decimal
        from copy import deepcopy
        if fileName is None:
            print('Error: the name of a stored DPdigraph file is required')
        else:
            fileNameExt = fileName+'.py'
            argDict = {}
            fi = open(fileNameExt,'r')
            fileText = fi.read()
            fi.close()
            exec(compile(fileText, fileNameExt, 'exec'),argDict)
            self.name = fileName
            self.actions = argDict['actions']
            self.order = len(self.actions)
            self.valuationdomain = argDict['valuationdomain']
            self.relation = argDict['relation']
            self.size = self.computeSize()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
            self.source = argDict['source']
            self.sink = argDict['sink']
            self.stages = self.computeStages(Debug=Debug)
            self.costsRange = argDict['costsRange']
            self.preferenceDirection = argDict['preferenceDirection']
            self.costs = argDict['costs']
            self.optimalPath = self.computeDynamicProgrammingSolution(Debug=Debug)

    def save(self,fileName='tempDPdigraph',decDigits=2):
        """
        Persistent storage of a dynamic programming problem
        in the format of a python source code file. The stored file may be reloaded with the
        :py:class:`~dynamicProgramming.DynamicProgrammingDigraph` class.

        *self.stages*, *self.optimalPath* and self.bestSum* attributes are automatically
        added by the class constructor.

        """
        print('*--- Saving DP digraph in file: <' + fileName + '.py> ---*')
        actions = self.actions
        relation = self.relation
        costs = self.costs
        costsRange = self.costsRange
        prefDir = self.preferenceDirection
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved dynamic programming problem\n')
        fo.write('from decimal import Decimal\n')
        # write actions
        fo.write('from collections import OrderedDict\n')
        fo.write('actions = OrderedDict([\n')
        for x in actions:
            fo.write('(\'' + str(x) + '\',\n')
            try:
                fo.write(str(actions[x])+'),\n')
            except:
                fo.write('{\'name\': \'%s\'}),\n' % str(x))
        fo.write('])\n')
        fo.write('source = \'%s\'\n' % self.source)
        fo.write('sink = \'%s\'\n' % self.sink)       
        # write relation
        IntegerValuation = self.valuationdomain['hasIntegerValuation']
        if not IntegerValuation:
            fo.write('valuationdomain = {\'hasIntegerValuation\': False, \'min\': Decimal("'+str(Min)+'"),\'med\': Decimal("'+str(Med)+'"),\'max\': Decimal("'+str(Max)+'")}\n')
        else:
            fo.write('valuationdomain = {\'hasIntegerValuation\': True, \'min\': Decimal("'+str(Min)+'"),\'med\': Decimal("'+str(Med)+'"),\'max\': Decimal("'+str(Max)+'")}\n')
        fo.write('relation = {\n')
        for x in actions:
            fo.write('\'' + str(x) + '\': {\n')
            for y in actions:
                if not IntegerValuation:
                    valueString = '\': Decimal(\'%%.%df\'),\n' % (decDigits)
                    fo.write('\'' + str(y) + (valueString % relation[x][y]))
                    #fo.write('\'' + str(y) + '\': Decimal("' + str(relation[x][y]) + '"),\n')
                else:
                    fo.write('\'' + str(y) + '\':' + str(relation[x][y]) + ',\n')
            fo.write('},\n')
        fo.write( '}\n')
        # write costs
        valueString = 'Decimal(\'%%.%df\')' % (decDigits)
        fo.write('costsRange = (' + (valueString % costsRange[0]) \
                               + ',' + (valueString % costsRange[1]) + ')\n' )
        fo.write('preferenceDirection = \'%s\'\n' % prefDir)
        fo.write('costs = {\n')
        for x in actions:
            fo.write('\'' + str(x) + '\': {\n')
            for y in actions:
                if not IntegerValuation:
                    valueString = '\': Decimal(\'%%.%df\'),\n' % (decDigits)
                    fo.write('\'' + str(y) + (valueString % costs[x][y]))
                else:
                    fo.write('\'' + str(y) + '\':' + str(costs[x][y]) + ',\n')
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()
    
            
    def computeStages(self,Debug=False):
        """
        Renders the decomposition of a
        :py:class:`~dynamicProgramming.DynamicProgrammingDigraph` object into a list
        of successive stages --subsets of states-- by taking the progessive union of the *gama* sets,
        starting from a single *self.source* node and ending in a single *self.sink* node.
        """
        stages = []
        source = self.source
        sink = self.sink
        stages.append([source])
        spl = self.computeShortestPathLengths()
        nstages = spl[source][sink]
        for i in range(1,nstages+1):
            if Debug:
                print('stage: ',i)
            neighbours = set()
            for x in stages[i-1]:
                nbx = self.gamma[x][0]
                if Debug:
                    print(x,nbx)
                neighbours |= nbx
            nbList = list(neighbours)
            nbList.sort()
            stages.append(nbList)
            if Debug:
                print(stages)
        if len(stages[0]) != 1  and len(stages[-1]) != 1:
            print('Error: the given digraph is not a valid dynamic programming diagram')
        else:
            return stages

    def computeDynamicProgrammingSolution(self,Debug=False):
        """
        The *Bellmann*, *Dijkstra*, or *Viterbi* dynamic programming algorithms a.o.,
        all proceed with a recursive forward-computing of best paths
        from stage *i-1* to stage *i*.

        In a second step, the overall best path is determined by
        backwards-selecting in each stage the best predecessor state.

        The resulting optimal path is stored in the *self.optimalPath* attribute
        and its global sum of costs (*prefernceDirection* == 'min'),
        respectively benefits (*prefernceDirection* == 'max', *negative* costs)
        is stored in the *self.bestSum* attribute.
        """
        from decimal import Decimal
        sink = self.sink
        source = self.source
        stages = self.stages
        costsRange = self.costsRange
        prefDir = self.preferenceDirection
        nstate = []
        nstages = len(stages)
        Med = self.valuationdomain['med']
        # forward computing best paths until satge *i*
        for i in range(nstages):
            #print(i,stages[i])
            nstate.append(len(stages[i]))
        Big = nstages * costsRange[1]
        best = {}
        best[0] = {}
        best[0][0] = Decimal('0')
        for i in range(1,nstages):
            best[i] = {}
            for k in range(nstate[i]):
                xk = stages[i][k]
                b = Big
                for j in range(nstate[i-1]):
                    yj = stages[i-1][j]
                    if self.relation[yj][xk] > Med:
                        if prefDir == 'min':
                            a = best[i-1][j] + self.costs[yj][xk]
                        else:
                            a = best[i-1][j] - self.costs[yj][xk]
                        if a < b:
                            b = a
                best[i][k] = b
        if Debug:
            self.best = best
        self.bestSum = abs(best[nstages-1][0])
        # Determine by backward inspec tion the best path from the sink to the source
        answer = [0 for i in range(nstages)]
        if Debug:
            print(answer)
        for i in range(nstages-2,0,-1):
            if Debug:
                print('>>>', i)
            k = answer[i+1]
            b = best[i+1][k]
            if Debug:
                print(i,b)
            for j in range(nstate[i]):
                xk = stages[i+1][k]
                yj = stages[i][j]
                if Debug:
                    print(j,xk,yj)
                if self.relation[yj][xk] > self.valuationdomain['med']:
                    if prefDir == 'min':
                        temp = best[i][j] + self.costs[yj][xk]
                    else:
                        temp = best[i][j] - self.costs[yj][xk]
                    if Debug:
                        print('b,best,temp',b,best[i][j],temp) 
                    if b == temp:
                        if Debug:
                            print('b,temp',b,temp) 
                        answer[i] = j
                        break
        if Debug:
            print(answer)
        optimalPath = []
        for i in range(len(answer)):
            if Debug:
                print(stages[i][answer[i]])
            optimalPath.append(stages[i][answer[i]])
        return optimalPath

    def exportGraphViz(self,fileName=None,direction='best',
                       WithBestPathDecoration=True,
                       ArrowHeads=True,
                       Comments=True,graphType='png',
                       graphSize='7,7',bgcolor='cornsilk',
                       fontSize=10,Debug=False):
        """
        Using the exportGraphViz() version of the TransitiveDigraph class
        """
        self.closeTransitive(InSite=True)
        from transitiveDigraphs import TransitiveDigraph
        TransitiveDigraph.exportGraphViz(self,
                        fileName=fileName,direction=direction,
                       WithBestPathDecoration=WithBestPathDecoration,
                       ArrowHeads=ArrowHeads,
                       Comments=Comments,graphType=graphType,
                       graphSize=graphSize,bgcolor=bgcolor,
                       fontSize=fontSize,Debug=Debug)
        self.closeTransitive(Reverse=True,InSite=True)

from dynamicProgramming import DynamicProgrammingDigraph
class RandomDynamicProgrammingDigraph(DynamicProgrammingDigraph):
    """
    Generator for creating random dynamic programming digraphs.

        - *preferenceDirection* = 'min' (default) | 'max'

        - *maxStages* = maximal number of stages

        - *costsRange(a,b)* : integer limits (*a* < *b*) for the random generation of arc labels

    
    Example Python session:

    
    >>> from dynamicProgramming import RandomDynamicProgrammingDigraph
    >>> dg = RandomDynamicProgrammingDigraph(
    ...                            order=12,
    ...                            maxStages=4,
    ...                            costsRange=(5,10),
    ...                            preferenceDirection='min',
    ...                            seed=2)
    >>> dg
     *------- Digraph instance description ------*
      Instance class      : RandomDynamicProgrammingDigraph
      Instance name       : randomDPdigraph
      Digraph Order       : 12
      Digraph Size        : 28
      Valuation domain    : [-1.00;1.00]
      Determinateness (%) : 80.30
      Attributes          : ['name', 'order', 'actions', 'valuationdomain',
                            'relation', 'gamma', 'notGamma',
                            'costsRange', 'preferenceDirection',
                            'costs', 'source', 'sink', 'shortestPathLengths',
                            'stages', 'nstages',
                            'bestSum', 'optimalPath']
    >>> print(dg.optimalPath)
     ['a01', 'a09', 'a02', 'a05', 'a12']
    >>> print(dg.bestSum)
     25.0
    >>> dg.exportGraphViz('testDP',WithBestPathDecoration=True)
     *---- exporting a dot file for GraphViz tools ---------*
     Exporting to testDP.dot
     dot -Grankdir=TB -Tpng testDP.dot -o testDP.png

    *Figure*: The path that minimizes the sum of the costs labels

    .. image:: testDP.png
       :width: 400 px
       :align: center
       :alt: The dynamic programming solution
  
    """
    def __init__(self,order=12,maxStages=4,costsRange=(5,10),
                 preferenceDirection='min',
                 seed=None,Debug=False):
        from randomDigraphs import RandomDigraph
        from decimal import Decimal
        from collections import OrderedDict
        from copy import deepcopy
        
        import random
        random.seed(seed)

        g = RandomDigraph(order=order,seed=seed)
        actionsList = [x for x in g.actions]
        source = actionsList[0]
        sink = actionsList[-1]
        Max = g.valuationdomain['max']
        Med = g.valuationdomain['med']
        Min = g.valuationdomain['min']
        
        if Debug:
            print(actionsList,source,sink)
        actionsStage = {source: 0, sink: maxStages}
        for i in range(1,order-1):
            x = actionsList[i]
            actionsStage[x] = random.randint(1,maxStages-1)
        if Debug:
            print(actionsStage)

        for i in range(order):
            x = actionsList[i]
            xst = actionsStage[x]
            for j in range(order):
                y = actionsList[j]
                yst = actionsStage[y]
                if x == y:
                    g.relation[x][y] = Med
                if xst - yst == -1:
                    g.relation[x][y] = Max
                elif xst - yst == 1:
                    g.relation[x][y] = Min
                else:
                    g.relation[x][y] = Med
        if Debug:
            g.showRelationTable()

        costs = {}
        for i in range(order):
            x = actionsList[i]
            costs[x] = {}
            for j in range(order):
                y = actionsList[j]
                if g.relation[x][y] > Med:
                    costs[x][y] = random.randint(costsRange[0],costsRange[1])
                else:
                    costs[x][y] = Decimal('0')
##                if x == y:
##                    costs[x][y] = Decimal('0')
##                else:
##                    costs[x][y] = random.randint(costsRange[0],costsRange[1]) \
##                              * g.relation[x][y]
        if Debug:
            print(costs)

        self.name = 'randomDPdigraph'
        self.order = order
        self.actions = deepcopy(g.actions)
        self.valuationdomain = {'min':Min,'med':Med,'max':Max,
                                'hasIntegerValuation': False}
        self.relation = deepcopy(g.relation)
        self.source = source
        self.sink = sink
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.stages = self.computeStages(Debug=Debug)
        self.nstages = len(self.stages)
        self.costs = costs
        self.costsRange = costsRange
        self.preferenceDirection = preferenceDirection
        self.optimalPath = self.computeDynamicProgrammingSolution(Debug=Debug)    
        #self.closeTransitive(Reverse = False,InSite=True)
##        self.gamma = self.gammaSets()
##        self.notGamma = self.notGammaSets()

# --------------------

###############################
if __name__ == '__main__':
    print("""
    ****************************************************
    * Digraph3 dynamicProgramming module               *
    * Revision: Python3.10                             *
    * Copyright (C) 2023 Raymond Bisdorff              *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    
    ######  scratch pad for testing the module components
    dg = RandomDynamicProgrammingDigraph(order=12,
                                         maxStages=4,
                                         costsRange=(5,10),
                                         preferenceDirection='min',
                                         seed=2)
    print(dg.optimalPath)
    print(dg.bestSum)
    print(dg.preferenceDirection)
    dg.exportGraphViz('testDP',WithBestPathDecoration=True)
    dg.save()

    dg1 = DynamicProgrammingDigraph('tempDPdigraph')
    print(dg1.optimalPath)
    print(dg1.bestSum)
    print(dg1.preferenceDirection)
  
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
#####################################


