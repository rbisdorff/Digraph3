#!/usr/bin/env python3
"""
Python3+ implementation of random digraphs
Based on Digraphs3 ressources
Copyright (C) 2015-2020  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "Branch: 3.3 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

from digraphsTools import *
from decimal import Decimal
from collections import OrderedDict

#---------- Random Digraph classes -----------------
from digraphs import *

class RandomDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    temporary crisp (irreflexive) random crisp digraphs.
    
    *Parameters*:
        * order (default = 10);
        * arcProbability (in [0.,1.], default=0.5)
        * IntegerValuation (default = True);
        * If Bipolar=True, valuation domain = {-1,1} otherwise = {0,1}
        * Is seed != None, the random generator is seeded 

     """

    def __init__(self,order=9,arcProbability=0.5,
                 IntegerValuation=True, Bipolar=True,
                 seed=None):

        arcProbability = Decimal(str(arcProbability))
        if arcProbability > Decimal("1.0"):
            print('Error: arc probability too high !!')
        elif arcProbability < Decimal("0.0"):
            print('Error: arc probability too low !!')
        else:
            import random
            random.seed(seed)
            from digraphs import EmptyDigraph
            if Bipolar:
                domain = (-1.0,1.0)
            else:
                domain = (0.0,1.0)
            nd = len(str(order))
            actions = OrderedDict()
            for i in range(order):
                actionKey = ('a%%0%dd' % nd) % (i+1)
                actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
            self.actions = actions
##            actionsList = [x for x in self.actions]
##            actionsList.sort()
            valuationdomain = dict()
            Min = Decimal(str(domain[0]))
            Max = Decimal(str(domain[1]))
            Med = Min + \
                (Max-Min)/Decimal('2.0')
            valuationdomain['min'] = Min
            valuationdomain['max'] = Max
            valuationdomain['med'] = Med
            valuationdomain['hasIntegerValuation'] = IntegerValuation
            self.valuationdomain = valuationdomain
            relation = {}
            for x in actions.keys():
                relation[x] = {}
                rx = relation[x]
                for y in actions.keys():
                    if x == y:
                        rx[y] = Min
                    else:
                        if random.random() <= arcProbability:
                            rx[y] = Max
                        else:
                            rx[y] = Min
            self.relation = relation
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
        * ndigits > 0, number of digits if IntegerValuation = True, 
          otherwise number of decimals;
        * Normalized = True (r in [-1,1], r in [0,1] if False/default);
        * IntegerValuation = False (default)
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
                 Normalized=True,
                 IntegerValuation=False,
                 seed = None):
        import random
        random.seed(seed)
        self.name = 'randomValuationDigraph'
        self.order = order
        nd = len(str(order))
        actions = OrderedDict()
        for i in range(order):
            actionKey = ('a%%0%dd' % nd) % (i+1)
            actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
        self.actions = actions
##        actionsList = [x for x in self.actions]
##        actionsList.sort()
        if IntegerValuation:
            precision = pow(10,ndigits) - 1
        else:
            precision = pow(10,ndigits)
        if IntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            if Normalized:
                 self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            else:
                self.valuationdomain = {'min':Decimal('0'), 'med':Decimal('0.5'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = IntegerValuation
        Med = self.valuationdomain['med']
        relation = {}
        for x in actions.keys():
            relation[x] = {}
            rx = relation[x]
            for y in actions.keys():
                if x == y:
                    rx[y] = Med
                else:
                    if IntegerValuation:
                        rx[y] = (2*random.randrange(start=0,stop=precision)) - precision
                    elif Normalized:
                        rx[y] = (Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits))) * Decimal('2.0')) - Decimal('1.0')
                    else:
                        rx[y] = Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits)))
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
        * If IntegerValuation = True,
          valuation domain = [-pow(10,ndigits); + pow(10,ndigits)]
          else valuation domain = [-1.0,1.0]
        * If seed != None, the random number generator is seeded

    """

    def __init__(self,order=10,ndigits=2,
                 IntegerValuation=False,
                 weaknessDegree=0.25,
                 seed=None,
                 Comments=False):
        import random
        random.seed(seed)
        from decimal import Decimal

        self.name = 'randomWeakTournament'
        self.order = order
        nd = len(str(order))
        actions = OrderedDict()
        for i in range(order):
            actionKey = ('a%%0%dd' % nd) % (i+1)
            actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
        self.actions = actions
##        actionlist = list(range(order+1))
##        actionlist.remove(0)
##        actions = []
##        for x in actionlist:
##            actions.append(str(x))
##        self.actions = actions
        Max = pow(10,ndigits)
        Min = - Max
        Med = 0
        precision = Max
        dPrecision = Decimal(str(precision))
        if IntegerValuation:
            self.valuationdomain = {'hasIntegerValuation':True, 'min':Decimal(str(Min)), 'med':Decimal('0'), 'max':Decimal(str(Max))}
        else:
            self.valuationdomain = {'hasIntegerValuation':False, 'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        relation = {}
        for x in actions.keys():
            relation[x] = {}
            rx = relation[x]
            for y in actions.keys():
                rx[y] = self.valuationdomain['med']

        actionsList = list(actions.keys())
        random.shuffle(actionsList)
        weaknessDegree = Decimal(str(weaknessDegree))
        forwardDegree = (Decimal('1.0') - weaknessDegree)/Decimal('2')

        #print actionsList
        n = len(actionsList)
        for i in range(n):
            rai = relation[actionsList[i]]
            for j in range(i,n):
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    rai[actionsList[j]] = Med
                else:
                    u = Decimal(str(random.randint(0,precision)))/dPrecision
                    u1 = Decimal(str(random.randint(0,precision)))
                    u2 = Decimal(str(random.randint(0,precision)))

                    if u < weaknessDegree: # i = j
                        if IntegerValuation:
                            randeval1 = u1
                            randeval2 = u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = u2/dPrecision

                    elif u < forwardDegree: # i > j
                        if IntegerValuation:
                            randeval1 = u1
                            randeval2 = Min + u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = (Min + u2)/dPrecision

                    else: # j > i
                        if IntegerValuation:
                            randeval1 = Min + u1
                            randeval2 = u2
                        else:
                            randeval1 = (Min + u1)/dPrecision
                            randeval2 = u2/dPrecision

                    if IntegerValuation:
                        rai[actionsList[j]] = Decimal(str(randeval1))
                        relation[actionsList[j]][actionsList[i]] = Decimal(str(randeval2))
                    else:
                        rai[actionsList[j]] = Decimal(str(round(randeval1,ndigits)))
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
                 Crisp=True,
                 valuationDomain=[-1,1],
                 seed=None):
        import random
        random.seed(seed)
        from decimal import Decimal

        self.name = 'randomTournament'
        self.order = order
        nd = len(str(order))
        actions = OrderedDict()
        for i in range(order):
            actionKey = ('a%%0%dd' % nd) % (i+1)
            actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
        self.actions = actions
##
##        actionlist = list(range(order+1))
##        actionlist.remove(0)
##        actions = []
##        for x in actionlist:
##            actions.append(str(x))
##        self.actions = actions
        if valuationDomain == None:
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        else:
            #print(valuationDomain)
            vdMax = Decimal(str(valuationDomain[0]))
            vdMin = Decimal(str(valuationDomain[1]))
            self.valuationdomain = {'min': vdMax, 'max': vdMin}
            self.valuationdomain['med'] = (vdMin + vdMax)/Decimal('2.0')
        valuationRange = self.valuationdomain['max'] - self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        relation = {}
        for x in actions:
            relation[x] = {}
            rx = relation[x]
            for y in actions:
                rx[y] = Decimal('0.0')
##        if seed != None:
##            random.seed(seed)
        precision = pow(10,ndigits)
        actionsList = list(actions.keys())
        #print actionsList
        n = len(actionsList)
        for i in range(n):
            rai = relation[actionsList[i]]
            for j in range(i,n):
                raj = relation[actionsList[j]]
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    rai[actionsList[j]] = Med
                else:
                    u = random.randint(0,precision)
                    if Crisp:
                        if u < Decimal(str(precision))/Decimal('2'):
                            rai[actionsList[j]] = Min
                            raj[actionsList[i]] = Max
                        else:
                            rai[actionsList[j]] = Max
                            raj[actionsList[i]] = Min
                    else:
                        randeval = Min + Decimal(str(u))/Decimal(str(precision))*valuationRange
                        valuation = Decimal(str(round(randeval,ndigits)))
                        rai[actionsList[j]] = valuation
                        raj[actionsList[i]] = Max - valuation + Min

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
            nd = len(str(order))
            actions = OrderedDict()
            for i in range(order):
                actionKey = ('a%%0%dd' % nd) % (i+1)
                actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            Min = self.valuationdomain['min']
            Max = self.valuationdomain['max']
            allarcs = []
            relation = {}
            for x in actions.keys():
                relation[x] = {}
                rx = relation[x] 
                for y in actions.keys():
                    rx[y] = Min
                    if x != y:
                        allarcs.append((x,y))
            for arc in random.sample(allarcs,size):
                relation[arc[0]][arc[1]] = Max
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
                nd = len(str(order))
                actions = OrderedDict()
                for i in range(order):
                    actionKey = ('a%%0%dd' % nd) % (i+1)
                    actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
                self.actions = actions
                self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
                Min = self.valuationdomain['min']
                Max = self.valuationdomain['max']
                relation = {}
                for x in actions.keys():
                    relation[x] = {}
                    rx = relation[x]
                    for y in actions.keys():
                        rx[y] = Min
                # create a random pairing
                feasable = 0
                s = 0
                while feasable == 0 and s < 100:
                    s += 1
                    edges = []
                    cells = []
                    degreeseq = {}
                    i = 0
                    for x in actions.keys():
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
                    for x in actions.keys():
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

#######################################

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
            nd = len(str(order))
            actions = OrderedDict()
            for i in range(order):
                actionKey = ('a%%0%dd' % nd) % (i+1)
                actions[actionKey] = {'shortName':actionKey, 'name': 'random decision action'}
            self.actions = actions
##            actionlist = list(range(order+1))
##            actionlist.remove(0)
##            actions = []
##            for x in actionlist:
##                actions.append(str(x))
##            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            # create a random pairing
            feasable = 0
            s = 0
            while feasable == 0 and s < 100:
                s += 1
                edges = []
                cells = []
                degreeseq = {}
                for x in actions.keys():
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
                for x in actions.keys():
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

###############################3

class RandomGridDigraph(GridDigraph):
    """
    Specialization of the general Digraph class for generating
    temporary randomly oriented Grid digraphs of dimension n time m
    (default 5x5).

    Parameters:
        * n,m > 0;
        * valuationdomain ={'min':-1 (default),'max': 1 (default)}.
    """

    def __init__(self,n=5,m=5,valuationdomain = {'min':-1.0,'max':1.0},
                 seed=None,Debug=False):
        import random
        random.seed(seed)
        self.name = 'randomGrid-'+str(n)+'-'+str(m)
        self.n = n
        self.m = m
        # constructing the grid
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
        if Debug:
            print(n,m,actions,gridNodes)
        # defining the valuation domain
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        # instantiate empty relation dictionary 
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        # instantiate random orientation
        for x in actions:
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

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    

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
    
##    dg = RandomValuationDigraph(Normalized=True,
##                                #IntegerValuation=True,
##                                ndigits=2,
##                                seed=1)
##    dg.showRelationTable()

    dg = RandomGridDigraph()
    dg.exportGraphViz()

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
