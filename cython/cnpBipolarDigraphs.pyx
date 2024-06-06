#cython: language_level=3
import numpy as np
from numpy import array
from cRandPerfTabs import cRandomPerformanceTableau
#from outrankingDigraphs import BipolarOutrankingDigraph
import itertools
import cython
from time import time

class npDigraph(object):
    """
    Abstract root class for digraphs
    with a numpy integer *valuation* attribute instead of the traditional
    double decimal *relation* dictionary.
    """
    def __neg__(self):
        """
        Make the negation operator -self available for cDigraph instances. 

        Returns a DualDigraph instance of self.
        """
        new = DualnpDigraph(self)
        new.__class__ = self.__class__
        return new

    def __invert__(self):
        """
        Make the inverting operator ~self available for cDigraph instances. 

        Returns a ConverseDigraph instance of self.
        """
        new = ConversenpDigraph(self)
        new.__class__ = self.__class__
        return new

    def computeSize(self):
        """
        Renders the number of validated non reflexive arcs
        """
        cdef int n, size, i, j, Med
        n = len(self.actions)
        Med = self.valuationdomain['med']
        valuation = self.valuation
        size = 0
        for i in range(n):
            for j in range(i+1,n):
                if valuation[i][j] > Med:
                    size += 1
                if valuation[j][i] > Med:
                    size += 1
        return size

    def computeCoSize(self):
        """
        Renders the number of not validated non reflexive arcs
        """
        cdef int n, size, i, j, Med
        n = len(self.actions)
        Med = self.valuationdomain['med']
        valuation = self.valuation
        size = 0
        for i in range(n):
            for j in range(i+1,n):
                if valuation[i][j] < Med:
                    size += 1
                if valuation[j][i] < Med:
                    size += 1
        return size
    
    def computeDeterminateness(self,InPercents=True):
        """
        Computes the average absolute epistemic determination
        of the presence and the absence of all pairwise outranking situations. 
        """
        cdef int order, Max, Med, i, j, sumValuations
        cdef float deter
        Max = self.valuationdomain['max']
        actionsList = [x for x in self.actions]
        n = self.order
        valuation = self.valuation
        deter = 0.0
        sumValuations = 0
        for i in range(n):
            for j in range(i+1,n):
                sumValuations += abs(valuation[i][j])
                sumValuations += abs(valuation[j][i])
        deter = sumValuations / (n * (n-1))
        if InPercents:
            return ( (( deter / Max ) + 1) / 2 )  * 100.0
        else:
            return ( (deter / Max) + 1 ) / 2
        
    def gammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the dominated, and set *ax* gathering
        the absorbed neighborhood.

        """
        #from numpy import array
        cdef int Med, i, j, n
        cdef list actionsList
        Med = 0
        actionsList = [x for x in self.actions]
        n = self.order
        valuation = array( (n,n), dtype=int)
        valuation = self.valuation
        cdef dict gamma = {}
        cdef set dx, ax 
        for i in range(n):
            x = actionsList[i]
            dx = set()
            ax = set()
            for j in range(n):
                if i != j:
                    y = actionsList[j]
                    if valuation[i][j] > Med:
                            dx.add(y)
                    if valuation[j][i] > Med:
                            ax.add(y)
            gamma[x] = (dx,ax)
        return gamma

    def notGammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the **not** dominated, and set *ax* gathering
        the **not** absorbed neighborhood.

        """
        #from numpy import array
        cdef int Med, i, j, n
        cdef list actionsList
        Med = 0
        actionsList = [x for x in self.actions]
        n = self.order
        valuation = array( (n,n), dtype=int)
        valuation = self.valuation
        cdef dict notGamma = {}
        cdef set dx, ax 
        for i in range(n):
            x = actionsList[i]
            dx = set()
            ax = set()
            for j in range(n):
                if i != j:
                    y = actionsList[j]
                    if valuation[i][j] < Med:
                            dx.add(y)
                    if valuation[j][i] < Med:
                            ax.add(y)
            notGamma[x] = (dx,ax)
        return notGamma

    def singletons(self):
        """
        Renders the list of singletons with neighborhoods
        [(singx1, +nx1, -nx1, not(+nx1 or -nx1)),.... ]
        where +nx1 = dominated, -nx1 = absorbed neighborhood

        """
        cdef list s = []
        cdef set indep
        cdef list actionsList
        cdef int x, n, i
        actionsList = [x for x in self.actions]
        n = self.order
        cdef dict gamma
        gamma = self.gamma
        for i in range(n):
            x = actionsList[i]
            indep = set(actionsList) - (gamma[x][0] | gamma[x][1])
            s += [(frozenset([x]),gamma[x][0],gamma[x][1],indep)]
        return s

    def independentChoices(self,list U):
        """
        Generator for all independent choices with neighborhoods of a bipolar valued digraph:

        .. note::
        
               * Initiate with U = self.singletons().
               * Yields [(independent choice, domnb, absnb, indnb)].

        """
        cdef list S, Sx, x, actionsList
        cdef set Sxgamdom, Sxgamabs, Sxindep
        cdef frozenset Sxchoice
        actionsList = [i for i in self.actions]
        n = self.order
        if U == []:
            yield [(frozenset(),set(),set(),set(actionsList))]
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

    def computePreKernels(self):
        """
        computing dominant and absorbent preKernels:
            Result in self.dompreKernels and self.abspreKernels
        """
        cdef set actions, restactions
        cdef int n
        actions = set(self.actions)
        n = len(actions)
        cdef set dompreKernels, abspreKernels
        abspreKernels = set()
        dompreKernels = set()
        cdef list choice
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                abspreKernels.add(choice[0][0])
        self.dompreKernels = dompreKernels
        self.abspreKernels = abspreKernels

    def addRelation(self):
        """
        adding the traditional *relation* attribute to the *self*
        digraph object.

        """
        cdef list actionsList
        cdef int n, x, y
        actionsList = [ x for x in self.actions]
        n = len(actionsList)
        valuation = self.valuation
        cdef dict relation = {}
        for i in range(n):
            x = actionsList[i]
            relation[x] = {}
            for j in range(n):
                y = actionsList[j]
                relation[x][y] = valuation[i][j]
        self.relation = relation
        
        
#--------------------

class DualnpDigraph(npDigraph):
    """
    Instantiates the dual ( = negated valuation) cDigraph object from a
    deep copy of a given other cDigraph instance.

    The relation constructor returns the dual (negation) of
    self.valuation 
    
    .. note::

        In a bipolar valuation, the dual operator corresponds to a simple changing of signs.


    """
    def __init__(self,other):
        from copy import deepcopy
        from time import time
        t0 = time()
        self.__class__ = other.__class__
        self.name = 'dual-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        valuation = deepcopy(other.valuation)
        self.valuation = -valuation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['dualTransform'] = time() - t0

class ConversenpDigraph(npDigraph):
    """
    Instantiates the converse ( = transposed valuation) CudaDigraph object from a
    deep copy of a given other CudaDigraph instance.

    The relation constructor returns the inverse (transposition) of
    self.valuation 
    
    .. note::

        In a bipolar valuation, the inverse operator corresponds to a transpose of the adjacency table.


    """
    def __init__(self,other):
        from copy import deepcopy
        from time import time
        t0 = time()
        self.__class__ = other.__class__
        self.name = 'converse-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        valuation = deepcopy(other.valuation)
        self.valuation = valuation.transpose()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['converseTransform'] = time() -t0

class CoDualnpDigraph(npDigraph):
    """
    Instantiates the codual ( = negated and transposed valuation) CudaDigraph object from a
    deep copy of a given other CudaDigraph instance.

    The relation constructor returns the codual of
    self.valuation 

    """
    def __init__(self,other):
        from copy import deepcopy
        from time import time
        t0 = time()
        self.__class__ = other.__class__
        self.name = 'codual-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        valuation = deepcopy(other.valuation)
        self.valuation = -valuation.transpose()       
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['codualTransform'] = time() - t0

class omaxFusionnpDigraph(npDigraph):
    """
    Instantiates the epistemic disjunctive fusion *o-max* of 
    two given Digraph instances called dg1 and dg2.

    Parameter:

        * *dg1* and *dg2* are two npDigraph objects

    """

    def __init__(self,dg1,dg2,Cuda=False):
        import numpy as np
        from copy import deepcopy
        import math
        self.name = 'fusion-'+dg1.name+'-'+dg2.name
        self.actions = deepcopy(dg1.actions)
        actionsList = [ x for x in self.actions]
        order = len(actionsList)
        self.order = order
        self.valuationdomain = deepcopy(dg1.valuationdomain)
        #actionsList = list(self.actions)
        #max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        valuation1 = dg1.valuation
        valuation2 = dg2.valuation
        fusionValuation = np.zeros([order,order])
        for i in range(order):
            for j in range(order):
                if valuation1[i,j] >= 0 and valuation2[i,j] >= 0:
                    fusionValuation[i,j] =\
                    max(valuation1[i,j],valuation2[i,j])
                elif valuation1[i,j] <= 0 and valuation2[i,j] <= 0:
                    fusionValuation[i,j] =\
                    min(valuation1[i,j],valuation2[i,j])
                else:
                    fusionValuation[i,j] = 0
        self.valuation = fusionValuation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

#------------------

from cRandPerfTabs import cPerformanceTableau
class npBipolarOutrankingDigraph(npDigraph,cPerformanceTableau):
    """
    Cythonized BipolarOutrankingDigraph class with numpy
    integer arrays implemented characteristic valuation.

    Usage:

    >>> from cRandPerfTabs import *
    >>> na = 500
    >>> nc = 7
    >>> pt = cRandomCBPerformanceTableau(numberOfActions = na,
    ...                           numberOfCriteria = nc,
    ...                           seed = 1)
    >>> from cnpBipolarDigraphs import npBipolarOutrankingDigraph
    >>> g = cnpBipolarOutrankingDigraph(pt,Comments=True)
    *------- Object instance description ------*
    Instance class      : npBipolarOutrankingDigraph
    Instance name       : rel_randomCBperftab
    Actions             : 500
    Criteria            : 7
    Size                : 133181
    Valuation domain    : {'min': -24, 'med': 0, 'max': 24,
                           'hasIntegerValuation': True}
    Determinateness (%) : 66.72
    Attributes          : ['name', 'actions', 'objectives', 'criteria',
                           'totalWeight', 'valuationdomain', 'NA',
                           'evaluation', 'order', 'runTimes',
                           'majorityMargins', 'vetoes', 'counterVetoes',
                           'valuation', 'gamma', 'notGamma']
    ----  Constructor run times (in sec.) ----
    Total time        : 2.36183
    Data input        : 0.00503
    Majority margins  : 1.92353
    CPD polarisation  : 0.23210
    Gamma sets        : 0.20117

    """

    def __repr__(self):
        """
        Default presentation method for BipolarOutrankingDigraph instance.
        """
        reprString = '*------- Object instance description ------*\n'
        reprString += 'Instance class      : %s\n' % self.__class__.__name__
        reprString += 'Instance name       : %s\n' % self.name
        reprString += 'Actions             : %d\n' % self.order
        reprString += 'Criteria            : %d\n' % len(self.criteria)
        reprString += 'Size                : %d\n' % self.computeSize()
        reprString += 'Valuation domain    : %s\n' % str(self.valuationdomain)
        reprString += 'Determinateness (%%) : %.2f\n' % self.computeDeterminateness(InPercents=True)
        reprString += 'Attributes          : %s\n' % list(self.__dict__.keys())
        val1 = self.runTimes['totalTime']
        val2 = self.runTimes['dataInput']
        val3a = self.runTimes['computeMargins']
        val3b = self.runTimes['computeValuation']
        val4 = self.runTimes['gammaSets']
        reprString += '----  Constructor run times (in sec.) ----\n'
        reprString += 'Total time        : %.5f\n' % val1
        reprString += 'Data input        : %.5f\n' % val2
        reprString += 'Compute margins   : %.5f\n' % val3a
        reprString += 'Compute valuation : %.5f\n' % val3b        
        reprString += 'Gamma sets        : %.5f\n' % val4
        try:
            val5 = self.runTimes['dualTransform']
            reprString += 'Dual Transform   : %.5f\n' % val5
        except:
            pass
        try:
            val6 = self.runTimes['converseTransform']
            reprString += 'Converse Transform: %.5f\n' % val6
        except:
            pass
        try:
            val7 = self.runTimes['codualTransform']
            reprString += 'Codual Transform  : %.5f\n' % val7
        except:
            pass
        return reprString

    def __init__(self,argPerfTab=None,\
                 coalition=None,\
                 actionsSubset=None,\
                 #bint hasNoVeto=False,\
                 #bint hasBipolarVeto=True,\
                 bint CopyPerfTab=True,\
                 bint BigData=True,\
                 #bint Threading=False,\
                 #startMethod=None,\
                 #tempDir=None,\
                 #bint WithConcordanceRelation=False,\
                 #bint WithVetoCounts=False,\
                 #nbrCores=None,\
                 Debug=False,Comments=False):
                 
        cdef int n, nt, totalWeight=0, Min, Max, Med
        cdef double tt, tcp, tg
        
        from copy import deepcopy
        from time import time
        from collections import OrderedDict

        # set initial time stamp
        tt = time()

        # ----  performance tableau data input 
        if argPerfTab == None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = cPerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab
        # transfering the performance tableau data to self
        self.name = 'rel_' + perfTab.name
        # actions
        if actionsSubset == None:
            if isinstance(perfTab.actions,list):
                actions = {}
                for x in perfTab.actions:
                    actions[x] = {'name': str(x)}
                self.actions = actions
            else:
                if CopyPerfTab:
                    self.actions = deepcopy(perfTab.actions)
                else:
                    self.actions = perfTab.actions
        else:
            actions = {}
            for x in actionsSubset:
                actions[x] = {'name': str(x)}
            self.actions = actions

        # objectives and criteria
        try:
            if CopyPerfTab:
                self.objectives = deepcopy(perfTab.objectives)
            else:
                self.objectives = perfTab.objectives
        except:
            pass
        criteria = OrderedDict()
        if coalition == None:
            coalition = perfTab.criteria.keys()
        for g in coalition:
            if CopyPerfTab:
                criteria[g] = deepcopy(perfTab.criteria[g])
            else:
                criteria[g] = perfTab.criteria[g]
        self.criteria = criteria
        #self.convertWeightsToIntegers()
           
        # valuation domain
        for g in self.criteria:
            self.criteria[g]['weight'] = int(self.criteria[g]['weight'])
            totalWeight += abs(self.criteria[g]['weight'])
        self.totalWeight = totalWeight
        
        Min =   -totalWeight
        Med =   0
        Max =   totalWeight
        self.valuationdomain = {'min': Min,
                                'med': Med,
                                'max': Max,
                                'hasIntegerValuation': True}
        
        # insert missing data symbol
        if CopyPerfTab:
            self.NA = deepcopy(perfTab.NA)
        else:
            self.NA = perfTab.NA
            
        # insert performance Data
        if CopyPerfTab:
            self.evaluation = deepcopy(perfTab.evaluation)
            self.NA = deepcopy(perfTab.NA)
        else:
            self.evaluation = perfTab.evaluation
            self.NA = perfTab.NA
        if not BigData:
            #self.convertEvaluationFloatToDecimal()
            try:
                if CopyPerfTab:
                    self.description = deepcopy(perfTab.description)
                else:
                    self.description = perfTab.description
            except:
                pass
        # init general digraph Data
        self.order = len(self.actions)
        
        # finished data input time stamp
        self.runTimes = {'dataInput': time()-tt }

        # ---------- construct outranking valuation

        # initial time stamp
        tcp = time()
        self._computeMajorityMargins()
        self.runTimes['computeMargins'] = time() - tcp

        tcp = time()
        self._computeValuation()
        self.runTimes['computeValuation'] = time() - tcp
        
        # computing cover and co relations
        tg = time()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['gammaSets'] = time() - tg
        

        # total constructor time
        self.runTimes['totalTime'] = time() - tt
        if Comments:
            print(self)

    def _computeMajorityMargins(self):
        # initial time stamp
        tcp = time()
        
        #actions = self.actions
        evaluation = self.evaluation
        criteria = self.criteria

        NA = self.NA
        cdef list actionsList
        actionsList = [x for x in self.actions]
        #n = np.int64
        n = len(actionsList)

        cdef dict perfs = {}
        cdef int sumWeights = 0
        #sumWeights = 0
        cdef int i
        #i = np.int64
        for c in criteria:   
            sumWeights += criteria[c]['weight']
            perfs[c] = np.zeros((n,4),dtype=float)
            for i in range(n):
                a = actionsList[i]
                if evaluation[c][a] != NA:
                    perfs[c][i][0] = evaluation[c][a]
                    try:
                        perfs[c][i][1] = criteria[c]['thresholds']['ind'][0] \
                            + (perfs[c][i][0] * criteria[c]['thresholds']['ind'][1])
                    except:
                        perfs[c][i][1] = 1 / (2 * criteria[c]['scale'][1])
                    try:
                        perfs[c][i][2] = criteria[c]['thresholds']['pref'][0] \
                            + (perfs[c][i][0] * criteria[c]['thresholds']['pref'][1])
                    except:
                        perfs[c][i][2] = 1 / (criteria[c]['scale'][1])
                    try:
                        perfs[c][i][3] = criteria[c]['thresholds']['veto'][0] \
                            + (perfs[c][i][0] * criteria[c]['thresholds']['pref'][1])
                    except:
                        perfs[c][i][3] = 2 * criteria[c]['scale'][1]
        cdef dict votes = {}
        #votes = {}
        vetoes = np.zeros((n,n),dtype=int)
        counterVetoes = np.zeros((n,n),dtype=int)
        majorityMargins = np.zeros((n,n),dtype=int)
        cdef int j
        cdef float indi, prefi, vetoi
        #j = np.int64
        for c in criteria:
            votes[c] = np.zeros((n,n),dtype=int)
            cWeight = criteria[c]['weight']
            for i in range(n):
                a = actionsList[i]
                for j in range(i,n):
                    b = actionsList[j]
                    #print(c,a,evaluation[c][a],b,evaluation[c][b])
                    if evaluation[c][a] != NA and evaluation[c][b] != NA:
                        diffij = perfs[c][i][0] - perfs[c][j][0]
                        indij = max(perfs[c][i][1],perfs[c][j][1])
                        prefij = max(perfs[c][i][2],perfs[c][j][2])
                        vetoij = max(perfs[c][i][3],perfs[c][j][3])                      
                        if diffij <= -prefij:
                            votes[c][i][j] = -cWeight
                        elif diffij >= -indij:
                            votes[c][i][j] = +cWeight
                        if diffij <= -vetoij:
                            vetoes[i][j] += 1
                        elif diffij >= vetoij:
                            counterVetoes[i][j] += 1
                        diffji = perfs[c][j][0] - perfs[c][i][0]
                        if diffji <= -prefij:
                            votes[c][j][i] = -cWeight
                        elif diffji >= -indij:
                            votes[c][j][i] = +cWeight
                        if diffji <= -vetoij:
                            vetoes[j][i] += 1
                        elif diffji >= vetoij:
                            counterVetoes[j][i] += 1
                    else:
                        votes[c][i][j] = 0
                        votes[c][j][i] = 0
            majorityMargins += votes[c]
        self.majorityMargins = majorityMargins
        self.vetoes = vetoes
        self.counterVetoes = counterVetoes

    def _computeValuation(self):
        majorityMargins = self.majorityMargins
        vetoes = self.vetoes
        counterVetoes = self.counterVetoes
        sumWeights = self.totalWeight    
        cdef int n
        n = self.order
        valuation = np.zeros((n,n),dtype=int)
        for pair in itertools.product(range(n), repeat=2):
            i = pair[0]
            j = pair[1]
            if vetoes[i][j] > 0 and counterVetoes[i][j] > 0:
                valuation[i][j] = 0
            elif majorityMargins[i][j] > 0:
                if vetoes[i][j] > 0:
                    valuation[i][j] = 0
                elif counterVetoes[i][j] > 0:
                    valuation[i][j] = sumWeights
                else:
                    valuation[i][j] = majorityMargins[i][j]
            elif majorityMargins[i][j] < 0:
                if vetoes[i][j] > 0:
                    valuation[i][j] = -sumWeights
                elif counterVetoes[i][j] > 0:
                    valuation[i][j] = 0
                else:
                    valuation[i][j] = majorityMargins[i][j]
            elif majorityMargins[i][j] == 0:
                if vetoes[i][j] > 0:
                    valuation[i][j] = -sumWeights
                elif counterVetoes[i][j] > 0:
                    valuation[i][j] = sumWeights
                else:
                    valuation[i][j] = majorityMargins[i][j]
        self.valuation = valuation
        
        
#-----------------
