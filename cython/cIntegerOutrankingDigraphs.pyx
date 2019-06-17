#!/usr/bin/env python3
"""
c-Extension for the Digraph3 collection.
Module cIntegerOutrankingDigraphs.py is a c-compiled part of the
:py:mod:`outrankingDigraphs` module for handling random performance tableaux of Big Data type,
ie with integer action keys and float performance evaluations.  

Copyright (C) 2018  Raymond Bisdorff
"""
#######################
cimport cython
from cpython cimport array
import array

cdef extern from "detertest.h":
    int cMAX(float a, float b);
    int cMIN(float a, float b)

__version__ = "Revision: Py35"

from digraphs import *
#from xmlrpc.client import ServerProxy
from cIntegerOutrankingDigraphs import *
from cRandPerfTabs import *

#-------------------------------------------
        
#############  cython
cdef inline int absInt(int x):
    if x < 0:
        return -x
    else:
        return x

cdef inline float absFloat(float x):
    if x < 0.0:
        return -x
    else:
        return x
    
cdef inline int _localConcordance(float d, float ind, float wp, float p):
    """
    Parameters: d := diff observed, wp := weak preference threshold,
    ind := indiffrence threshold, p := prefrence threshold.
    Renders the concordance index per criteria (-1,0,1)

            .. notice::  all parameters are float None == -1.0 !

    """
    if p > -1.0:
        if   d <= -p:
            return -1
        elif ind > -1.0:
            if d >= -ind:
                return 1
            else:
                return 0
        elif wp > -1.0:
            if d > -wp:
                return 1
            else:
                return 0
        else:
            if d < 0.0:
                return -1
            else:
                return 1
    else:
        if ind > -1.0:
            if d >= -ind:
                return 1
            else:
                return -1
        elif wp > -1.0:
            if d > -wp:
                return 1
            else:
                return -1
        else:
            if d < 0.0:
                return -1
            else:
                return 1                


cdef inline int _localVeto(float d, float wv, float v):
    """
    Parameters:
        d := diff observed, v (wv)  :=  (weak) veto threshold.

    .. notice::  all parameters are float None == -1.0 !

    Renders the local veto state (-1,0,1).

    """
    if v > -1.0:
        if  d <= - v:
            return 1
        elif wv > -1.0:
            if d <= - wv:
                return 0
            else:
                return -1
        else:
            return -1        
    elif wv > -1.0:
        if d <= -wv:
            return 0
        else:
            return -1
    else:
        return -1

cdef inline int _localNegativeVeto(float d, float wv, float v):
    """
    Parameters:
        d := diff observed, v (wv)  :=  (weak) veto threshold.

    .. notice::  all parameters are float None == -1.0 !

    Renders the local negative veto state (-1,0,1).

    """
    if v > -1.0:
        if  d >= v:
            return 1
        elif wv > -1.0:
            if d >= wv:
                return 0
            else:
                return -1
        else:
            return -1        
    elif wv > -1.0:
        if d >= wv:
            return 0
        else:
            return -1
    else:
        return -1


#cdef inline int extend(array self, array other) except -1
from outrankingDigraphs import BipolarOutrankingDigraph
class IntegerBipolarOutrankingDigraph(BipolarOutrankingDigraph,PerformanceTableau):
    """
    Specialization of the abstract OutrankingDigraph root class for generating
    integer-valued bipolar outranking digraphs.

    Parameters:
        * argPerfTab: instance of PerformanceTableau class.
          If a file name string is given, the performance tableau will directly be loaded first.
        * coalition: subset of criteria to be used for contruction the outranking digraph.
        * hasNoVeto: veto desactivation flag (False by default).
        * hasBipolarVeto: bipolar versus electre veto activation (true by default).
        * Threading: False by default. Allows to profit from SMP machines via the Python multiprocessing module.
        * nbrCores: controls the maximal number of cores that will be used in the multiprocessing phases. If None is given, the os.cpu_count method is used in order to determine the number of availble cores on the SMP machine.

    Example Python session:
        >>> from cRandPerfTabs import *
        >>> tc = cRandomPerformanceTableau(numberOfActions=9,seed=100)
        >>> tc
        *------- PerformanceTableau instance description ------*
        Instance class   : cRandomPerformanceTableau
        Instance name    : cRandomperftab
        # Actions        : 9
        # Criteria       : 7
        Attributes       : ['name', 'actions', 'criteria', 'evaluation', 'weightPreorder']
        >>> from cIntegerOutrankingDigraphs import *
        >>> idg = IntegerBipolarOutrankingDigraph(tc)
        >>> idg
        *------- Object instance description ------*
        Instance class   : IntegerBipolarOutrankingDigraph
        Instance name    : rel_cRandomperftab
        # Actions        : 9
        # Criteria       : 7
        Size             : 57
        Determinateness  : 37.302
        Valuation domain : {'min': -7, 'med': 0, 'max': 7, 
                            'hasIntegerValuation': True}
        ----  Constructor run times (in sec.) ----
        Total time       : 0.00243
        Data input       : 0.00034
        Compute relation : 0.00202
        Gamma sets       : 0.00006
        #Threads         : 1
        >>> idg.showRelationTable()
        * ---- Relation Table -----
         R  |   '0' '1' '2' '3' '4' '5' '6' '7' '8'   
        ----|--------------------------------------
        '0' |   +0  +0  -1  -1  +2  +1  -3  +0  +1  
        '1' |   +3  +0  -7  -7  +1  +2  -1  +1  +1  
        '2' |   +3  +7  +0  +4  +3  +3  +4  +1  +3  
        '3' |   +2  +7  +4  +0  +1  +3  +5  +2  +0  
        '4' |   +5  +2  +2  +1  +0  +3  +1  +1  +3  
        '5' |   +1  +2  -1  -1  +1  +0  -1  +0  +3  
        '6' |   +3  +5  +5  +4  +3  +2  +0  +1  +3  
        '7' |   +5  +5  +3  +4  +3  +7  +1  +0  +5  
        '8' |   +1  +3  +2  +7  +0  +2  +2  +0  +0  
        >>> idg.showRubisBestChoiceRecommendation()
        ***********************
        Rubis best choice recommendation(s) (BCR)
         (in decreasing order of determinateness)   
        Credibility domain: [-7.00,7.00]
         === >> potential best choice(s)
        * choice              : [2, 3, 4, 6, 7, 8]
          +-irredundancy      : 0.00
          independence        : 0.00
          dominance           : 1.00
          absorbency          : -2.00
          covering (%)        : 50.00
          determinateness (%) : 55.56
          - most credible action(s) = { '7': 1.00, '6': 1.00, '4': 1.00, '2': 1.00, }
         === >> potential worst choice(s) 
        * choice              : [0, 1, 4, 5, 7, 8]
          +-irredundancy      : 0.00
          independence        : 0.00
          dominance           : -1.00
          absorbency          : 3.00
          covering (%)        : 0.00
          determinateness (%) : 54.76
          - most credible action(s) = { '8': 1.00, '5': 1.00, '0': 1.00, }
        Execution time: 0.005 seconds
        *****************************
        >>> ig.computeCopelandRanking()
        [2, 6, 7, 3, 4, 8, 1, 5, 0]
      
    """
    
    def __init__(self,argPerfTab=None,\
                 coalition=None,\
                 actionsSubset=None,\
                 bint hasNoVeto=False,\
                 bint hasBipolarVeto=True,\
                 bint CopyPerfTab=True,\
                 bint BigData=False,\
                 bint Threading=False,\
                 tempDir=None,\
                 bint WithConcordanceRelation=False,\
                 bint WithVetoCounts=False,\
                 nbrCores=None,\
                 Debug=False,Comments=False):
                 
        cdef int n, nt, totalWeight=0, Min, Max, Med
        cdef double tt, tcp, tg
        
        from copy import deepcopy
        from time import time

        # set initial time stamp
        tt = time()

        # ----  performance tableau data input 
        if argPerfTab == None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
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

        #  install method Data and parameters
        methodData = {}
        try:
            valuationType = perfTab.parameter['valuationType']
            variant = perfTab.parameter['variant']
        except:
            valuationType = 'bipolar'
            variant = 'standard'
        methodData['parameter'] = {'valuationType': valuationType, 'variant': variant}
        try:
            vetoType = perfTab.parameter['vetoType']
            methodData['parameter']['vetoType'] = vetoType
        except:
            vetoType = 'normal'
            methodData['parameter']['vetoType'] = vetoType
        if vetoType == 'bipolar':
            hasBipolarVeto = True
        self.methodData = methodData

        # insert performance Data
        if CopyPerfTab:
            self.evaluation = deepcopy(perfTab.evaluation)
        else:
            self.evaluation = perfTab.evaluation
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

        # ---------- construct outranking relation
        # initial time stamp
        tcp = time()
        
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        actionsKeys = list(dict.keys(actions))
        self.relation = self._constructRelationWithThreading(criteria,\
                                                evaluation,\
                                                initial=actionsKeys,\
                                                terminal=actionsKeys,\
                                                hasNoVeto=hasNoVeto,\
                                                hasBipolarVeto=hasBipolarVeto,\
                                                hasSymmetricThresholds=True,\
                                                Threading=Threading,\
                                                tempDir=tempDir,\
                                                ## WithConcordanceRelation=WithConcordanceRelation,\
                                                ## WithVetoCounts=WithVetoCounts,\
                                                nbrCores=nbrCores,\
                                                Debug=Debug,Comments=Comments)
        # finished relation computing time stamp
        self.runTimes['computeRelation'] = time() - tcp

        # ----  computing the gamma sets
        tg = time()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['gammaSets'] = time() - tg 

        # total constructor time
        self.runTimes['totalTime'] = time() - tt
        if Comments:
            print(self)

############

    def __repr__(self):
        """
        Default presentation method for BipolarOutrankingDigraph instance.
        """
        reprString = '*------- Object instance description ------*\n'
        reprString += 'Instance class   : %s\n' % self.__class__.__name__
        reprString += 'Instance name    : %s\n' % self.name
        reprString += '# Actions        : %d\n' % self.order
        reprString += '# Criteria       : %d\n' % len(self.criteria)
        reprString += 'Size             : %d\n' % self.computeSize()
        reprString += 'Determinateness  : %.3f\n' % self.computeDeterminateness()
        reprString += 'Valuation domain : %s\n' % str(self.valuationdomain)
        try:
            val1 = self.runTimes['totalTime']
            val2 = self.runTimes['dataInput']
            val3 = self.runTimes['computeRelation']
            val4 = self.runTimes['gammaSets']
            reprString += '----  Constructor run times (in sec.) ----\n'
            reprString += 'Total time       : %.5f\n' % val1
            reprString += 'Data input       : %.5f\n' % val2
            reprString += 'Compute relation : %.5f\n' % val3
            reprString += 'Gamma sets       : %.5f\n' % val4
            try:
                reprString += '# Threads        : %d\n' % self.nbrThreads
            except:
                self.nbrThreads = 1
                reprString += '# Threads        : %d\n' % self.nbrThreads
        except:
            pass
        reprString += 'Attributes       : %s\n' % list(self.__dict__.keys())     
        return reprString
        
    def computeCriterionRelation(self,c, a,b,hasSymmetricThresholds=True):
        """
        *Parameters*:
             * c, 
             * a,
             * b,
             * hasSymmetricThresholds=True.

        Compute the outranking characteristic for actions x and y
        on criterion c.

        """
        critc = self.criteria[c]
        if a == b:
            return 1
        else:

            if self.evaluation[c][a] != Decimal('-999') and self.evaluation[c][b] != Decimal('-999'):		
                try:
                    indx = critc['thresholds']['ind'][0]
                    indy = critc['thresholds']['ind'][1]
                    if hasSymmetricThresholds:
                        ind = indx +indy * cMAX(absFloat(self.evaluation[c][a]), absFloat(self.evaluation[c][b]))
                    else:
                        ind = indx +indy * absFloat(self.evaluation[c][a])
                except:
                    ind = -1.0
                try:
                    wpx = critc['thresholds']['weakPreference'][0]
                    wpy = critc['thresholds']['weakPreference'][1]
                    if hasSymmetricThresholds:
                        wp = wpx + wpy * cMAX(absFloat(self.evaluation[c][a]), absFlost(self.evaluation[c][b]))
                    else:
                        wp = wpx + wpy * absFloat(self.evaluation[c][a])
                except:
                    wp = -1.0
                try:
                    px = critc['thresholds']['pref'][0]
                    py = critc['thresholds']['pref'][1]
                    if hasSymmetricThresholds:
                        p = px + py * cMAX(absFloat(self.evaluation[c][a]), absFloat(self.evaluation[c][b]))
                    else:
                        p = px + py * absFloat(self.evaluation[c][a]) 
                except:
                    p = -1.0
                
                d = self.evaluation[c][a] - self.evaluation[c][b]

                return self._localConcordance(d,ind,wp,p)

            else:
                return 0

    def computeSize(self):
        """
        Renders the number of validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        #actions = [x for x in self.actions]
        actions = self.actions
        relation = self.relation
        size = 0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        size += 1
        return size

            
    def _constructRelationWithThreading(self,criteria,\
                           evaluation,\
                           initial=None,\
                           terminal=None,\
                           bint hasNoVeto=False,\
                           bint hasBipolarVeto=True,\
                           bint Debug=False,\
                           bint hasSymmetricThresholds=True,\
                           bint Threading=False,
                           tempDir=None,\
                           bint WithConcordanceRelation=False,\
                           bint WithVetoCounts=False,\
                           nbrCores=None,Comments=False):
        """
        Specialization of the corresponding BipolarOutrankingDigraph method
        """
        
        cdef int i, j, ni, nt, n, nit, nbrOfJobs
        cdef array.array actions2Split = array.array('i')
        
        from multiprocessing import cpu_count
        #from array import array
        
        ##
        
        if not Threading or cpu_count() < 2:
            # set threading parameter
            self.nbrThreads = 1

            # !! concordance relation and veto counts need a complex constructor
            ## if (not hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
            ##     constructRelation = self._constructRelation
            ## else:
            constructRelation = self._constructRelationSimple

            return constructRelation(criteria,\
                                    evaluation,\
                                    initial=initial,\
                                    terminal=terminal,\
                                    hasNoVeto=hasNoVeto,\
                                    hasBipolarVeto=hasBipolarVeto,\
                                    #WithConcordanceRelation=WithConcordanceRelation,\
                                    #WithVetoCounts=WithVetoCounts,\
                                    Debug=Debug,\
                                    hasSymmetricThresholds=hasSymmetricThresholds)
        ##
        else:  # parallel computation
            from copy import copy, deepcopy
            from io import BytesIO
            from pickle import Pickler, dumps, loads, load
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            #Debug=True
            class myThread(Process):
                def __init__(self, int threadID,digraph,\
                             InitialSplit, tempDirName,\
                             splitActions,\
                             bint hasNoVeto, bint hasBipolarVeto,\
                             bint hasSymmetricThresholds, bint Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.digraph = digraph
                    self.InitialSplit = InitialSplit
                    self.workingDirectory = tempDirName
                    self.splitActions = splitActions
                    self.hasNoVeto = hasNoVeto
                    self.hasBipolarVeto = hasBipolarVeto,
                    self.hasSymmetricThresholds = hasSymmetricThresholds,
                    self.Debug = Debug
                def run(self):
                    from io import BytesIO
                    from pickle import Pickler, dumps, loads
                    from os import chdir
                    from array import array

                    digraph = self.digraph
                    
                    chdir(self.workingDirectory)
##                    if Debug:
##                        print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadId)))
                    #fi = open('dumpSelf.py','rb')
                    #digraph = loads(fi.read())
                    #fi.close()
                    splitActions = self.splitActions
##                    fiName = 'splitActions-'+str(self.threadID)+'.py'
##                    fi = open(fiName,'rb')
##                    splitActions = loads(fi.read())
##                    fi.close()
                    # compute partiel relation
                    ## if (not hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
                    ##     constructRelation = IntegerBipolarOutrankingDigraph._constructRelation
                    ## else:
                    #constructRelation = IntegerBipolarOutrankingDigraph._constructRelationSimple
                    if self.InitialSplit:
                        initialIn = splitActions
                        terminalIn = None
                    else:
                        initialIn = None
                        terminalIn = splitActions
                        #splitRelation = BipolarOutrankingDigraph._constructRelation(
                    splitRelation = digraph._constructRelationSimple(
                                            digraph.criteria,\
                                            digraph.evaluation,
                                            initial=initialIn,
                                            terminal=terminalIn,
                                            hasNoVeto=self.hasNoVeto,
                                            hasBipolarVeto=self.hasBipolarVeto,
                                            #WithConcordanceRelation=False,
                                            #WithVetoCounts=False,
                                            Debug=False,
                                            hasSymmetricThresholds=self.hasSymmetricThresholds)
                    ## else:
                    ##     #splitRelation = BipolarOutrankingDigraph._constructRelation(
                    ##     splitRelation = constructRelation(
                    ##                         digraph,digraph.criteria,\
                    ##                         digraph.evaluation,
                    ##                         #initial=initial,
                    ##                         terminal=splitActions,
                    ##                         hasNoVeto=hasNoVeto,
                    ##                         hasBipolarVeto=hasBipolarVeto,
                    ##                         WithConcordanceRelation=False,
                    ##                         WithVetoCounts=False,
                    ##                         Debug=False,
                    ##                         hasSymmetricThresholds=hasSymmetricThresholds)
                    # store partial relation
                    foName = 'splitRelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitRelation,-1))
                    fo.close()
                # .......
             
            if Comments:
                print('Threading ...')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                from copy import copy, deepcopy

                #selfDp = copy(self)
                selfFileName = tempDirName +'/dumpSelf.py'
                if Debug:
                    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                fo.write(dumps(self,-1))
                fo.close()

                if nbrCores == None:
                    nbrCores = cpu_count()
                if Comments:
                    print('Nbr of cpus = ',nbrCores)
                # set number of threads
                self.nbrThreads = nbrCores

                ni = len(initial)
                nt = len(terminal)
                if ni < nt:
                    n = ni
                    actions2Split = array.array('i',list(initial))
                    InitialSplit = True
                else:
                    n = nt
                    actions2Split = array.array('i',list(terminal))
                    InitialSplit = False
##                if Debug:
##                    print('InitialSplit, actions2Split', InitialSplit, actions2Split)
            
                nit = n//nbrCores
                nbrOfJobs = nbrCores
                if nit*nbrCores < n:
                    nit += 1
                while nit*(nbrOfJobs-1) >= n:
                    nbrOfJobs -= 1
                if Comments:
                    print('nbr of actions to split',n)
                    print('nbr of jobs = ',nbrOfJobs)    
                    print('nbr of splitActions = ',nit)

                relation = {}
                for x in initial:
                    relation[x] = {}
                    for y in terminal:
                        relation[x][y] = self.valuationdomain['med']
                i = 0
                actionsRemain = set(actions2Split)
                splitActionsList = []
                for j in range(nbrOfJobs):
                    if Comments:
                        print('Thread = %d/%d' % (j+1,nbrOfJobs),end=" ")
                    splitActions=array.array('i',[])
                    for k in range(nit):
                        if j < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = array.array('i',actionsRemain)
                        i += 1
                    if Comments:
                        print('%d' % (len(splitActions)) )
##                    if Debug:
##                        print(splitActions)
                    actionsRemain = actionsRemain - set(splitActions)
##                    if Debug:
##                        print(actionsRemain)
                    splitActionsList.append(splitActions)
##                    foName = tempDirName+'/splitActions-'+str(j)+'.py'
##                    fo = open(foName,'wb')
##                    spa = dumps(splitActions,-1)
##                    fo.write(spa)
##                    fo.close()
                    splitThread = myThread(j,self,InitialSplit,
                                           tempDirName,splitActions,
                                           hasNoVeto,hasBipolarVeto,
                                           hasSymmetricThresholds,Debug)
                    splitThread.start()
                    splitThread.join()	
	
                    
##                while active_children() != []:
##                    pass

                if Comments:    
                    print('Exiting computing threads')
                for j in range(len(splitActionsList)):
                    #print('Post job-%d/%d processing' % (j+1,nbrOfJobs))
##                    if Debug:
##                        print('job',j)
##                    fiName = tempDirName+'/splitActions-'+str(j)+'.py'
##                    fi = open(fiName,'rb')
##                    splitActions = loads(fi.read())
##                    fi.close()
                    splitActions = splitActionsList[j]
##                    if Debug:
##                        print('splitActions',splitActions)
                    fiName = tempDirName+'/splitRelation-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitRelation = loads(fi.read())
##                    if Debug:
##                        print('splitRelation',splitRelation)
                    fi.close()

                    #relation update with splitRelation)                    
                
                    if InitialSplit:
                        #for x,y in product(splitActions,terminal):
                        for x in splitActions:
                            rx = relation[x]
                            sprx = splitRelation[x]
                            for y in terminal:
                                rx[y] = sprx[y]
                    else:
                        #for x,y in product(initial,splitActions):
                        for x in initial:
                            rx = relation[x]
                            sprx = splitRelation[x]
                            for y in splitActions:
                                rx[y] = sprx[y]   
                return relation

    def _constructRelationSimple(self,criteria,\
                           evaluation,\
                           initial=None,\
                           terminal=None,\
                           bint hasNoVeto=False,\
                           bint hasBipolarVeto=True,\
                           #bint WithConcordanceRelation=False,\
                           #bint WithVetoCounts=False,\
                           bint hasSymmetricThresholds=True,\
                           bint Debug=False):
        """
        Parameters:
            * PerfTab.criteria, PerfTab.evaluation,
            * inital nodes, terminal nodes, for restricted purposes 
            
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        """

        cdef int totalWeight, Max, Med, concordance=0, lc0
        
        ## default setting for digraphs
        if initial == None:
            initial = self.actions
        if terminal == None:
            terminal = self.actions
        
##        totalweight = Decimal('0.0')
##        for c in dict.keys(criteria):
##            totalweight = totalweight + criteria[c]['weight']
        totalWeight = sum(abs(crit['weight']) for crit in criteria.values())

        relation = {}
        #vetos = []
        #negativeVetos = []
        
        #nc = len(criteria)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        for a in initial:
            relation[a] = {}
            ra = relation[a]
            for b in terminal:
                if a == b:
                    ra[b] = Med
                else:
                    concordance = 0
                    veto = {}
                    abvetos=[]
                    negativeVeto = {}
                    abNegativeVetos=[]

                    for c,crit in criteria.items():
                        evalca = evaluation[c][a]
                        evalcb = evaluation[c][b]
                        #maxAB = max(absFloat(evalca),absFloat(evalcb))
                        
                        if evalca != Decimal('-999') and evalcb != Decimal('-999'):
                            maxAB = cMAX(absFloat(evalca),absFloat(evalcb))
                            try:
                                indx = crit['thresholds']['ind'][0]
                                indy = crit['thresholds']['ind'][1]
                                ind = indx +indy * maxAB
                            except KeyError:
                                ind = -1.0
                            try:
                                wpx = crit['thresholds']['weakPreference'][0]
                                wpy = crit['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * maxAB
                                else:
                                    wp = wpx + wpy * absFloat(evalca) 
                            except KeyError:
                                wp = -1.0
                            try:
                                px = crit['thresholds']['pref'][0]
                                py = crit['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = px + py * maxAB
                                else:
                                    p = px + py * absFloat(evalca) 
                            except KeyError:
                                p = -1
                            if crit['weight'] >= 0:
                                d = evalca - evalcb
                            else:
                                d = evalcb - evalca
                            lc0 = _localConcordance(d,ind,wp,p)
                            ## print 'c,a,b,d,ind,wp,p,lco = ',c,a,b,d, ind,wp,p,lc0
                            concordance = concordance + (lc0 * crit['weight'])
                            try:
                                wvx = crit['thresholds']['weakVeto'][0]
                                wvy = crit['thresholds']['weakVeto'][1]
                                if hasNoVeto:
                                    wv = -1.0
                                else:
                                    if hasSymmetricThresholds:
                                        wv = wvx + wvy * maxAB
                                    else:
                                        wv = wvx + wvy * absFloat(evalca)
                            except KeyError:
                                wv = -1.0
                            try:
                                vx = crit['thresholds']['veto'][0]
                                vy = crit['thresholds']['veto'][1]
                                v = vx + vy * maxAB
                            except KeyError:
                                v = -1.0
                            veto[c] = (_localVeto(d,wv,v),d,wv,v)
                            if veto[c][0] > -1:
                                abvetos.append((c,veto[c]))
                            
                            negativeVeto[c] = (_localNegativeVeto(d,wv,v),d,wv,v)
                            if negativeVeto[c][0] > -1:
                                abNegativeVetos.append((c,negativeVeto[c]))
                        else:
                            concordance = concordance + 0 * crit['weight']
                            veto[c] = (-1,None,None,None)
                            negativeVeto[c] = (-1,None,None,None)
                                
                    concordindex = concordance                
                    
                    ## init vetoes lists and indexes
                    abVetoes=[]
                    abNegativeVetoes=[]

                    #  contradictory vetoes
                    
                    for c in criteria.keys():
                        if veto[c][0] >= 0:
                            abVetoes.append((c,veto[c]))
                        if negativeVeto[c][0] >= 0:
                            abNegativeVetoes.append((c,negativeVeto[c]))
                                         
                    vetoes = [-veto[c][0]*totalWeight for c in veto\
                               if veto[c][0] > -1]
                    negativeVetoes = [negativeVeto[c][0]*totalWeight for c in negativeVeto\
                                      if negativeVeto[c][0] > -1]
                    omaxList = [concordindex] + vetoes + negativeVetoes
                    if hasNoVeto:
                        outrankindex = concordindex
                    else:
                        outrankindex = omax(Med,omaxList,Debug=Debug)
                    # if Debug:
                    #     print(a,b)
                    #     print('vetoes = ', vetoes)
                    #     print('negativeVetoes = ', negativeVetoes)
                    #     print('omaxList',omaxList)
                    #     print('outrankindex',outrankindex)
                                                                
                    #if abVetoes != []:
                    #    vetos.append(([a,b,concordindex],abVetoes))
                    #if abNegativeVetoes != []:
                    #    negativeVetos.append(([a,b,concordindex],abNegativeVetoes))
                    ra[b] = outrankindex

        # return outranking relation    

        return relation


    def computeOrdinalCorrelation(self, other, bint Debug=False):
        """
        *Parameters*:
            * other,
            * Debug=False.
        
        Renders the ordinal correlation K of an integer Digraph instance
        when compared with a given compatible (same actions set) other integer Digraph or
        Digraph instance.

        *Formulas*:

        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             The global outranking relation of BigDigraph instances is contructed on the fly
             from the ordered dictionary of the components.

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """
        cdef int x, y, sMax, oMax, selfMultiple=1, otherMultiple=1
        cdef int corr, determ, selfRelation, otherRelation
        cdef int corrSum=0, determSum=0
        cdef double correlation=0.0, determination=0.0
        
        sMax = self.valuationdomain['max']
        oMax = int(other.valuationdomain['max'])
        if Debug:
            print('self Max', sMax)
            print('other Max', oMax)
        if (oMax != sMax) :
            selfMultiple = oMax
            otherMultiple = sMax
        if Debug:
            print('self', selfMultiple)
            print('other', otherMultiple)
        
        for x in self.actions:
            for y in self.actions:
                if x != y:
                    selfRelation = self.relation[x][y] * selfMultiple
                    try:
                        otherRelation = other.relation[x][y] * otherMultiple
                    except:
                        otherRelation = int(other.relation(x,y)) * otherMultiple
                    if Debug:
                       print(x,y,'self', selfRelation)
                       print(x,y,'other', otherRelation)
                    corr = min( max(-selfRelation,otherRelation),\
                                 max(selfRelation,-otherRelation) )
                    corrSum += corr
                    determ = min( absInt(selfRelation),absInt(otherRelation) )
                    determSum += determ

        if determSum > 0:
            correlation = float(corrSum) / float(determSum)
            n2 = (self.order*self.order) - self.order
            determination = (float(determSum) / n2)
            determination /= (sMax * selfMultiple)
            
        return { 'correlation': correlation,\
                     'determination': determination }

    def computeOrderCorrelation(self, order, bint Debug=False):
        """
        *Parameters*:
            * order (ordered sequence from worst to best of action keys), 
            * bint Debug=False.

        wrapper for the self.computeRankingCorrelation method
        The given argOrder is previously reversed.
     
        """
        ranking = list(reversed(order))
        return(self.computeRankingCorrelation(ranking,Debug))

    def computeRankingCorrelation(self, ranking, bint Debug=False):
        """
        *Parameters*:
            * ranking (ordered sequence from best to worst of action keys),
            * Debug=False.

        Renders the ordinal correlation K of an integer digraph instance
        when compared with a given linear ranking of its actions
        
        K = sum_{x != y} [ min( max(-self.relation(x,y)),other.relation(x,y), max(self.relation(x,y),-other.relation(x,y)) ]

        K /= sum_{x!=y} [ min(abs(self.relation(x,y),abs(other.relation(x,y)) ]

        .. note::

             The global outranking relation of BigDigraph instances is contructed on the fly
             from the ordered dictionary of the components.

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(other.relation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """
        cdef int i, j, x, y, sMax, oMax, selfMultiple=1, otherMultiple=1
        cdef int corr, determ, selfRelation, otherRelation
        cdef double corrSum=0.0, determSum=0.0
        cdef double correlation=0.0, determination=0.0
        
        sMax = self.valuationdomain['max']
        # selfMultiple = 1
        otherMultiple = sMax
        n = len(ranking)
        for i in range(n-1):
            x = ranking[i]
            for j in range(i+1,n):
                y = ranking[j]
                selfRelation = self.relation[x][y]
                otherRelation = sMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += float(corr)
                determ = min( absInt(selfRelation),absInt(otherRelation) )
                determSum += float(determ)
                selfRelation = self.relation[y][x]
                otherRelation = -sMax
                corr = min( max(-selfRelation,otherRelation),\
                            max(selfRelation,-otherRelation) )
                corrSum += float(corr)
                determ = min( abs(selfRelation),abs(otherRelation) )
                determSum += float(determ)

        if determSum > 0.000001:
            correlation = corrSum / determSum
            n2 = (self.order*self.order) - self.order
            determination = determSum / float(n2)
            determination /= float(sMax * selfMultiple)
            
            return { 'correlation': correlation,\
                     'determination': determination }
        else:
            return { 'correlation': 0.0,\
                     'determination': 0.0 }


    def computeOrdinalCorrelationMP(self, other,
                                    bint Threading=True, int nbrOfCPUs=0,
                                    bint Comments=False, bint Debug=False):
        """
        *Parameters*:
            * other (digraph instance),
            * Threading=True,
            * nbrOfCPUs=True,
            * Comments=False,
            * Debug=False.

        Multi processing version of the digraphs.computeOrdinalCorrelation() method.
        
        .. note::
             The relation filtering and the MedinaCut option are not implemented in the MP version.
             
        """
        cdef int n, nit, nbrOfJobs
        cdef int x, y, sMax, oMax, selfMultiple=1, otherMultiple=1
        cdef int corr, determ, selfRelation, otherRelation
        cdef int corrSum=0, determSum=0
        cdef double correlation=0.0, determination=0.0

        from multiprocessing import cpu_count

        n = self.order
        actionsList = list(self.actions.keys())
        
        sMax = self.valuationdomain['max']
        oMax = other.valuationdomain['max']
        if Debug:
            print('self Max', sMax)
            print('other Max', oMax)
        if (oMax != sMax) :
            selfMultiple = oMax
            otherMultiple = sMax
        if Debug:
            print('self', selfMultiple)
            print('other', otherMultiple)
        
        
        if Threading and cpu_count() > 4:
            from pickle import Pickler,dumps, loads, load
            #from io import BytesIO
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID,TempDirName, int selfMultiple,
                                 int otherMultiple, bint Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    self.Debug = Debug
                    self.selfMultiple = selfMultiple
                    self.otherMultiple = otherMultiple
                def run(self):
                    cdef int x, y,selfRelation, otherRelation
                    cdef long corr, determ, n2
                    cdef long corrSum=0, determSum=0
                    cdef double correlation=0.0, determination=0.0

                    from pickle import dumps, loads
                    from os import chdir
                    from decimal import Decimal
                    chdir(self.workingDirectory)

                    #fi = open('dumpActions.py','rb')
                    #actionsList = loads(fi.read())
                    #fi.close()

                    fi = open('dumpRelation.py','rb')
                    selfRel = loads(fi.read())
                    fi.close()

                    fi = open('dumpOtherRelation.py','rb')
                    otherRel = loads(fi.read())
                    fi.close()

                    fiName = 'splitActions-'+str(self.threadID)+'.py'
                    fi = open(fiName,'rb')
                    splitActions = loads(fi.read())
                    fi.close()
                    #n = len(splitActions
                    #n2 = len(splitActions)**2 
                    correlation = Decimal('0')
                    determination = Decimal('0')
                    for x in splitActions:
                        grx = selfRel[x]
                        orx = otherRel[x]
                        for y in actionsList:
                            if x != y:
                                selfRelation = grx[y] * otherMultiple
                                otherRelation = orx[y] * selfMultiple
                                corr = min( max(-selfRelation,otherRelation),\
                                                max(selfRelation,-otherRelation) )
                                corrSum += corr
                                determSum += min( absInt(selfRelation),\
                                                      absInt(otherRelation) )
                    # if determSum > 0:
                    #     correlation = float(corrSum) / float(determSum)
                    #     n2 = (self.order*self.order) - self.order
                    #     determination = (float(determSum) / n2)
                    #     determination /= (sMax * selfMultiple)
                    
                    splitCorrelation = {'correlation': corrSum,
                                        'determination': determSum}
                    # write partial correlation relation 
                    foName = 'splitCorrelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitCorrelation,-1))
                    fo.close()

            # pre-threading operations
            if nbrOfCPUs == 0:
                nbrOfCPUs = cpu_count()
            if Debug:
                print('Nbr of cpus = ',nbrOfCPUs)
            if Comments:
                print('Starting correlation computation with %d threads ...' % nbrOfCPUs)
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                #selfFileName = tempDirName +'/dumpActions.py'
                #if Debug:
                #    print('temDirName, selfFileName', tempDirName,selfFileName)
                #fo = open(selfFileName,'wb')
                #pd = dumps(actionsList,-1)
                #fo.write(pd)
                #fo.close()

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
                pd = dumps(other.relation,-1)
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
                    splitThread = myThread(jb,tempDirName,\
                                    selfMultiple,otherMultiple,Debug)
                    splitThread.start()
                    splitThread.join()
                    
##                while active_children() != []:
##                    pass
                
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
                    if Debug:
                        print('splitCorrelation',splitCorrelation)
                    fi.close()
                    corrSum += splitCorrelation['correlation']
                    determSum += splitCorrelation['determination']          
                                            
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
            for x in self.actions.keys():
                grx = self.relation[x] 
                orx = other.relation[x]
                for y in self.actions.keys():
                    if x != y:
                        selfRelation = grx[y] * otherMultiple
                        otherRelation = orx[y] * selfMultiple
                        corr = min( max(-selfRelation,otherRelation),\
                                    max(selfRelation,-otherRelation) )
                        corrSum += corr
                        determSum += min( absInt(selfRelation),\
                                              absInt(otherRelation) )
            #denominator = float(selfMultiple*otherMultiple)
            #determination = float(determSum) / denominator

        if determSum > 0:
            correlation = float(corrSum) / float(determSum)
            n2 = (n*n) - n
            determination = (float(determSum) / n2)
            determination /= (sMax * selfMultiple)
            return {'correlation': correlation,\
                    'determination': determination}
        else:
            return {'correlation': 0.0,\
                    'determination': determination}

    
    def criterionCharacteristicFunction(self,c,a,b,hasSymmetricThresholds=True):
        """
        *Parameters*:
             * c, 
             * a,
             * b,
             * hasSymmetricThresholds=True.

        Renders the characteristic value of the comparison of a and b on criterion c.
        """
        cdef int Min, Max
        cdef float evalca, evalcb, maxAB,indx, indy, ind, wpx, wpy, wp, 
        
        evalca = self.evaluation[c][a]
        evalcb = self.evaluation[c][b]
        #maxAB = max(abs(evalca),abs(evalcb))
        crit = self.criteria[c]
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        if evalca != Decimal('-999') and evalcb != Decimal('-999'):
            maxAB = max(absFloat(evalca),absFloat(evalcb))
            try:
                indx = crit['thresholds']['ind'][0]
                indy = crit['thresholds']['ind'][1]
                if hasSymmetricThresholds:
                    ind = indx +indy * maxAB
                else:
                    ind = indx +indy * absFloat(evalca)
            except:
                ind = -1.0
            try:
                wpx = crit['thresholds']['weakPreference'][0]
                wpy = crit['thresholds']['weakPreference'][1]
                if hasSymmetricThresholds:
                    wp = wpx + wpy * maxAB
                else:
                    wp = wpx + wpy * abs(evalca)
            except:
                wp = -1.0
            try:
                px = crit['thresholds']['pref'][0]
                py = crit['thresholds']['pref'][1]
                if hasSymmetricThresholds:
                    p = px + py * maxAB
                else:
                    p = px + py * abs(evalca)
            except:
                p = -1.0
            if crit['weight'] > 0:
                d = evalca - evalcb
            else:
                d = evalcb - evalca
            return self._localConcordance(d,ind,wp,p)
        else:
            return 0

    def computeDeterminateness(self):
        """
        Computes the Kendalll distance in % of self
        with the all median valued (indeterminate) digraph.
        """
        cdef int x,y, Max, Med, order
        cdef long deterSum=0
        cdef float deter
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = self.relation
        #actions = self.actions
        order = self.order
        #deter = Decimal('0.0')
        for x,rx in relation.items():
            for y,rxy in rx.items():
                if x != y:
                    #print(relation[x][y], Med, relation[x][y] - Med)
                    deterSum += absInt(rxy - Med)
                    #print(deter)
        #deter = (deter /Decimal(str((order * (order-1))))) * (Max - Med)
        deter = float(deterSum) / float(order * (order-1))
        return (deter/float(Max-Med))*100.0

    def convertValuation2Decimal(self):
        from decimal import Decimal
        self.valuationdomain['min'] = Decimal('%.2f' % self.valuationdomain['min'])
        self.valuationdomain['med'] = Decimal('%.2f' % self.valuationdomain['med'])
        self.valuationdomain['max'] = Decimal('%.2f' % self.valuationdomain['max'])
        for x,rx in self.relation.items():
            for y,rxy in rx.items():
                rxy = Decimal('%.2f' % rxy)
        from outrankingDigraphs import BipolarOutrankingDigraph
        self.__class__ = BipolarOutrankingDigraph
        
    def showActions(self,Alphabetic=False):
        """
        *Parameter*:
            * Alphabetic=False.

        Presentation methods for decision actions or alternatives.

        """
        print('*----- show decision action --------------*')
        actions = self.actions
        if Alphabetic:
            actionsKeys = [x for x in self.actions.keys()]
            actionsKeys.sort()
            for x in actionsKeys:
                print('key: ',x)
                try:
                    print('  short name:',actions[x]['shortName'])
                except KeyError:
                    pass
                print('  name:      ',actions[x]['name'])
                try:
                    print('  comment:   ',actions[x]['comment'])
                except KeyError:
                    pass
                print()
        else:
            for x in self.actions:
                print('key: ',x)
                try:
                    print('  short name:',actions[x]['shortName'])
                except KeyError:
                    pass
                print('  name:      ',actions[x]['name'])
                try:
                    print('  comment:   ',actions[x]['comment'])
                except KeyError:
                    pass
                print()
                
############################
