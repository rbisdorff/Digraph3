#!/usr/bin/env python3
# Python3+ implementation of random digraphs
# Based on Digraphs3 ressources
# Copyright (C) 2015  Raymond Bisdorff
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
from decimal import Decimal

#---------- Random Digraph classes -----------------

class RandomDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary crisp (irreflexive) random crisp digraphs.
    
    *Parameters*:
        * order (default = 10);
        * arc_probability (in [0.,1.], default=0.5)
        * If Bipolar=True, valuation domain = {-1,1} otherwise = {0,1}
        * Is seed != None, the random generator is seeded 

     """

    def __init__(self,order=9,arcProbability=0.5,
                 hasIntegerValuation=True, Bipolar=False,
                 seed=None):

        arcProbability = Decimal(str(arcProbability))
        if arcProbability > Decimal("1.0"):
            print('Error: arc probability too high !!')
        elif arcProbability < Decimal("0.0"):
            print('Error: arc probability too low !!')
        else:
            import copy
            from random import random,seed
            from digraphs import EmptyDigraph
##            g = RandomValuationDigraph(order=order,ndigits=0,hasIntegerValuation=hasIntegerValuation)
##            cutLevel = 1 - arcProbability
##            print(g.relation)
##            gp = PolarisedDigraph(digraph=g,level=cutLevel,KeepValues=False,AlphaCut=True)
##            gp.showRelationTable()
            if seed != None:
                seed(seed)
            if Bipolar:
                domain = (-1.0,1.0)
            else:
                domain = (0.0,1.0)
            g = EmptyDigraph(order=order, valuationdomain=domain)
            self.actions = copy.deepcopy(g.actions)
            self.valuationdomain = copy.deepcopy(g.valuationdomain)
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


class RandomValuationDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary uniformly valuated random digraphs.

    *Parameters*:
        * order > 0, number of arcs;
        * ndigits > 0, number of digits if hasIntegerValuation = True;
          Otherwise, decimal precision.
        * Normalized = True (r in [-1,1], r in [0,1] if False/default);
        * hasIntegerValuation = False (default)
        * If seed != none, the random generator is seeded


    Example python3 session:
        >>> from digraphs import RandomValuationDigraph
        >>> dg = RandomValuationDigraph(order=5,Normalized=True)
        >>> dg.showAll()
        *----- show detail -------------*
        Digraph          : randomValuationDigraph
        *---- Actions ----*
        ['1', '2', '3', '4', '5']
        *---- Characteristic valuation domain ----*
        {'max': Decimal('1.0'), 'min': Decimal('-1.0'),
         'med': Decimal('0.0'), 'hasIntegerValuation': False}
        * ---- Relation Table -----
          S   |  '1'    '2'    '3'    '4'     '5'     
         -----|-----------------------------------
          '1' |  0.00   0.28   0.46  -0.66   0.90    
          '2' | -0.08   0.00  -0.46  -0.42   0.52    
          '3' |  0.84  -0.10   0.00  -0.54   0.58    
          '4' |  0.90   0.88   0.90   0.00  -0.38    
          '5' | -0.50   0.64   0.42  -0.94   0.00    
        *--- Connected Components ---*
        1: ['1', '2', '3', '4', '5']
        Neighborhoods:
          Gamma     :
        '4': in => set(), out => {'1', '2', '3'}
        '5': in => {'1', '2', '3'}, out => {'2', '3'}
        '1': in => {'4', '3'}, out => {'5', '2', '3'}
        '2': in => {'4', '5', '1'}, out => {'5'}
        '3': in => {'4', '5', '1'}, out => {'5', '1'}
          Not Gamma :
        '4': in => {'5', '1', '2', '3'}, out => {'5'}
        '5': in => {'4'}, out => {'4', '1'}
        '1': in => {'5', '2'}, out => {'4'}
        '2': in => {'3'}, out => {'4', '1', '3'}
        '3': in => {'2'}, out => {'4', '2'}

        >>> dg.exportGraphViz()

    .. image:: randomValuationDigraph.png

    """

    def __init__(self,order=9, ndigits=2,
                 Normalized=False,
                 hasIntegerValuation=False,
                 seed = None):
        import random
        self.name = 'randomValuationDigraph'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        if hasIntegerValuation:
            precision = pow(10,ndigits) - 1
        else:
            precision = pow(10,ndigits)
        if hasIntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            if Normalized:
                 self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            else:
                self.valuationdomain = {'min':Decimal('0'), 'med':Decimal('0.5'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        if seed != None:
            random.seed(seed)
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

class RandomWeakTournament(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary bipolar-valued weak tournaments

    *Parameters*:
        * order = n > 0
        * weaknessDegree in [0.0,1.0]: proportion of indeterminate links (default = 0.25)
        * If hasIntegerValuation = True,
          valuation domain = [-pow(10,ndigits); + pow(10,ndigits)]
          else valuation domain = [-1.0,1.0]
        * If seed != None, the random number generator is seeded

    """

    def __init__(self,order=10,ndigits=2,
                 hasIntegerValuation=False,
                 weaknessDegree=0.25,
                 seed=None,
                 Comments=False):
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
        if seed != None:
            random.seed(seed)
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


class RandomTournament(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary weak tournaments

    *Parameter*:
       * order = n > 0
       * If valuationDomain = None, valuation is normalized (in [-1.0,1.0])
       * If is Crips = True, valuation is polarized to min and max values

    """

    def __init__(self,order=10,ndigits=2,
                 isCrisp=True,
                 valuationDomain=None,
                 seed=None):
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
        if seed != None:
            random.seed(seed)
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


class RandomFixedSizeDigraph(Digraph):
    """
    Generates a random crisp digraph with a fixed size, by instantiating a fixed numbers of arcs
    from random choices in the set of potential oriented pairs of nodes numbered from 1 to order. 
    """
    def __init__(self,order=7,size=14,seed=None):
        import random,copy
        random.seed(seed)
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

class RandomFixedDegreeSequenceDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary random crisp graphs (symmetric digraphs) with a fixed sequence of degrees.

    *Parameters*:
        order=n and degreeSequence=[degree_1, ... ,degree_n]>

    .. warning::

        The implementation is not guaranteeing a uniform choice among all potential valid graph instances.

    """
    def __init__(self,order=7,degreeSequence=[3,3,2,2,1,1,0],seed=None):
        import random,copy
        random.seed(seed)
        # check feasability
        degree = max(degreeSequence)
        if degree >= order:
            print('!!! Graph not feasable (1) !!!')
            print('Maximum degree > order !!!')
            self=None
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

class _RandomTree(Digraph):
    """
    Random generator for trees, using random Pruefer codes

    Parameter:
        numerOfNodes

    """
    def __init__(self,numberOfNodes=5, ndigits=0, hasIntegerValuation=True, seed=None):
        import random
        random.seed(seed)
        from decimal import Decimal
        self.name = 'randomTree'
        self.order = numberOfNodes
        # generate actions dictionary
        actions = {}
        nodes = [str(x+1) for x in range(numberOfNodes)]
        for x in nodes:
            actions[x] = {'name': 'node %s' % x}
        self.actions = actions
        print(actions)
        # set valuation domain
        precision = pow(10,ndigits)
        if hasIntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        # init empty relation dictionary
        relation = {}
        nodeKeys = [x for x in actions]
        print(nodeKeys)
        for x in nodeKeys:
            relation[x] = {}
            for y in nodeKeys:
                relation[x][y] = self.valuationdomain['min']
        # generate a random pruefer code
        nodes = [x for x in range(len(nodeKeys))]
        pruefer = []
        for i in range(len(nodeKeys)-2):
            pruefer.append(random.choice(nodes))
        print(pruefer)
        # contruct the corresponding relation (a tree)
        pairs = self._prufer_to_tree(pruefer)
        for (i,j) in pairs:
            relation[str(i+1)][str(j+1)] = self.valuationdomain['max']
            relation[str(j+1)][str(i+1)] = self.valuationdomain['max']
        self.relation = relation
        # generate neighboring sets
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _prufer_to_tree(self,a):
        tree = []
        T = list(range(0, len(a)+2))
        print(T)
        # the degree of each node is how many times it appears
        # in the sequence
        deg = [1]*len(T)
        print(deg)
        for i in a: deg[i] += 1

        # for each node label i in a, find the first node j with degree 1 and add
        # the edge (j, i) to the tree
        for i in a:
            for j in T:
                if deg[j] == 1:
                    tree.append((i,j))
                    # decrement the degrees of i and j
                    deg[i] -= 1
                    deg[j] -= 1
                    break

        last = [x for x in T if deg[x] == 1]
        tree.append((last[0],last[1]))

        return tree


class RandomRegularDigraph(Digraph):
    """
    Parameters:
        order and degree.

    Specialization of Digraph class for random regular symmetric instances.

    """
    def __init__(self,order=7,degree=2, seed=None):
        import random,copy
        random.seed(seed)
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

#############################################

#----------test Random Digraph classes ----------------
if __name__ == "__main__":

    print('****************************************************')
    print('* Python randomDigraphs module                     *')
    print('* Copyright (C) 2015 University of Luxembourg      *')
    print('* The module comes with ABSOLUTELY NO WARRANTY     *')
    print('* to the extent permitted by the applicable law.   *')
    print('* This is free software, and you are welcome to    *')
    print('* redistribute it if it remains free software.     *')
    print('****************************************************')


    print('*-------- Testing classes and methods -------')

##    rg1 = RandomDigraph(order=5,seed=1)
##    rg2 = RandomDigraph(Bipolar=True,order=5,seed=1)
##    rg1.showRelationTable()
##    rg2.showRelationTable()
    
    dg = RandomValuationDigraph(Normalized=True,
                                #hasIntegerValuation=True,
                                ndigits=2,
                                seed=1)
    dg.showRelationTable()

    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. July 2012                    *')
    print('* $Revision: 1.697 $                *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: randomDigraphs.py,v $
#############################
