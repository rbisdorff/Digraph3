#!/usr/bin/env python3
"""
Python3 implementation of outranking digraphs.
Copyright (C) 2006-2023  Raymond Bisdorff

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

__version__ = "Revision: Py3.10"

from digraphsTools import *
from digraphs import *
from xmlrpc.client import ServerProxy
from outrankingDigraphs import *
from copy import copy, deepcopy
from io import BytesIO
from pickle import Pickler, dumps, loads, load
#from multiprocessing import Process, Lock,\
#                        active_children, cpu_count
import multiprocessing as mp
# mpctx = mp.get_context('spawn')
# Process = mpctx.Process
# active_children = mpctx.active_children
# cpu_count = mpctx.cpu_count

#-------------------------------------------
        
class OutrankingDigraph(Digraph,PerformanceTableau):
    """
    Abstract root class for **outranking digraphs** inheritating methods both from the generic :py:class:`digraphs.Digraph`
    and from the generic :py:class:`perfTabs.PerformanceTableau` root classes.
    As such, our genuine outranking digraph model is a hybrid object appearing on the one side as digraph with a
    nodes set (the decision alternatives) and a binary relation (outranking situations) and, on the other side, as
    a performance tableau with a set of decision alternatives, performance criteria and a table of performance measurements.

    Provides common methods to all specialized models of outranking digraphs, the standard outranking digraph model being provided
    by the :py:class:`outrankingDigraphs.BipolarOutrankingDigraph` class. 

    A given object of this class consists at least in:

    1. a potential set of decision **actions** : an (ordered) dictionary describing the potential decision actions or alternatives with 'name' and 'comment' attributes,
    2. a coherent family of **criteria**: an (ordered) dictionary of criteria functions used for measuring the performance of each potential decision action with respect to the preference dimension captured by each criterion,
    3. the **evaluations**: a dictionary of performance evaluations for each decision action or alternative on each criterion function. 
    4. the digraph **valuationdomain**, a dictionary with three entries: the *minimum* (-100, means certainly no link), the *median* (0, means missing information) and the *maximum* characteristic value (+100, means certainly a link),
    5. the **outranking relation** : a double dictionary defined on the Cartesian product of the set of decision alternatives capturing the credibility of the pairwise *outranking situation* computed on the basis of the performance differences observed between couples of decision alternatives on the given family if criteria functions.   


    .. warning::

        Cannot be called directly ! No __init__(self,...) method defined.
        
    """

    def computeMarginalObjectiveCorrelation(self,args,Threading=False,
                                    nbrOfCPUs=None,Debug=False,
                                    Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the marginal criterion relation and a 
        given normalized outranking relation.

        args = (objective,relation)
        """
        objective = args[0]
        relation = args[1]
        gc = BipolarOutrankingDigraph(self,Normalized=True,
                                          #coalition=[criterion],
                                          objectivesSubset=[objective],
                                          CopyPerfTab=True,
                                          Threading=Threading,
                                          nbrCores=nbrOfCPUs,
                                          Comments=Comments)
        corr = gc.computeOrdinalCorrelationMP(relation,
                                              Threading=Threading,
                                              nbrOfCPUs=nbrOfCPUs)
        if Debug:
            print(corr)
        return corr

    def computeMarginalCorrelation(self,args,Threading=False,
                                    nbrOfCPUs=None,Debug=False,
                                    Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the marginal criterion relation and a 
        given normalized outranking relation.

        args = (criterion,relation)
        """
        criterion = args[0]
        relation = args[1]
        gc = BipolarOutrankingDigraph(self,Normalized=True,
                                          coalition=[criterion],
                                          CopyPerfTab=True,
                                          Threading=Threading,
                                          nbrCores=nbrOfCPUs,
                                          Comments=Comments)
        corr = gc.computeOrdinalCorrelationMP(relation,
                                              Threading=Threading,
                                              nbrOfCPUs=nbrOfCPUs)
        if Debug:
            print(corr)
        return corr

    def showOutrankingConsensusQuality(self,Sorted=True,ValuedCorrelation=True,
                                          Threading=False,nbrCores=None,
                                          Comments=True):
        """ Show method for the computeOutrankingConsensusQuality() method."""
        self.computeOutrankingConsensusQuality(self,Sorted=Dorted,
                                               ValuedCorrelation=ValuedCorrelation,
                                          Threading=Threading,nbrCores=nbrCores,
                                          Comments=Comments)
        
    def computeOutrankingConsensusQuality(self,Sorted=True,ValuedCorrelation=True,
                                          Threading=False,nbrCores=None,
                                          Comments=False):
        """
        Renders the marginal criteria correlations with the corresponding global outranking relation with summary.
        """
        from math import sqrt
        # self is an OutrankingDigraph object
        criteria = self.criteria
        marginalCorrelations=\
            self.computeMarginalVersusGlobalOutrankingCorrelations(
                Sorted=Sorted,
                ValuedCorrelation=ValuedCorrelation,
                Threading=Threading,nbrCores=nbrCores,
                Comments=False)
        ncrit = Decimal(str(len(marginalCorrelations)))
        meanMarginalCorrelation = Decimal('0.0')
        varMarginalCorrelation = Decimal('0.0')
        sumWeights = Decimal('0.0')
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            sumWeights += abs(criteria[cg[1]]['weight'])
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            meanMarginalCorrelation += cg[0]*cgw
        for cg in marginalCorrelations:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg[1]]['weight'])/sumWeights
            varMarginalCorrelation += ((cg[0]-meanMarginalCorrelation)**2)*cgw
            #varMarginalCorrelation += (cg[0]**2)*cgw
        # #meanMarginalCriteriaCorrelation /= ncrit
        # #varMarginalCriteriaCorrelation /= ncrit
        # #varMarginalCorrelation -= meanMarginalCorrelation*meanMarginalCriteriaCorrelation
        sdMarginalCorrelation = sqrt(varMarginalCorrelation) 
        # # showing the results
        if Comments:
            print('Consensus quality of global outranking:')
            if ValuedCorrelation:
                print('criterion (weight): valued correlation')
                print('--------------------------------------')
            else:
                print('criterion (weight): correlation')
                print('-------------------------------')
            for cg in marginalCorrelations:
                print('%s (%.3f): %+.3f' % (
                    cg[1],abs(criteria[cg[1]]['weight'])/sumWeights,cg[0]) )
            print('Summary:')
            print('Weighted mean marginal correlation (a): %+.3f' %\
                  meanMarginalCorrelation)
            print('Standard deviation (b)                : %+.3f' %\
                  sdMarginalCorrelation)
            print('Ranking fairness (a)-(b)              : %+.3f' %\
                  (float(meanMarginalCorrelation) - sdMarginalCorrelation) )
        return (marginalCorrelations,
                meanMarginalCorrelation,
                sdMarginalCorrelation)

#-----------------

    def showMarginalObjectivesVersusGlobalRankingCorrelations(self,ranking,
                        Sorted=True,ValuedCorrelation=False,
                        Threading=False,nbrCores=None):
        """
        Corresponding compute method with Comments = True flag.
        """
        self.computeMarginalObjectivesVersusGlobalRankingCorrelations(
                    ranking,Sorted=Sorted,ValuedCorrelation=ValuedCorrelation,
                    Threading=Threading,nbrCores=nbrCores,Comments=True)
        
    def computeMarginalObjectivesVersusGlobalRankingCorrelations(self,ranking,
                                                           Sorted=True,ValuedCorrelation=False,
                                                          Threading=False,nbrCores=None,
                                                                 startMethod=None,
                                                          Comments=False):
        """
        Method for computing correlations between each individual objective's outranking relation and the given global ranking relation.
        
        Returns a list of tuples (correlation,objectiveKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of available cores.

        *Usage example*:

        >>> from outrankingDigraphs import *
        >>> t = Random3ObjectivesPerformanceTableau(
                                   numberOfActions=21,
                                   numberOfCriteria=17,
                                   vetoProbability=0.2,
                                   seed=12)
        >>> g = BipolarOutrankingDigraph(t)
        >>> ranking = g.computeNetFlowsRanking()
        >>> g.computeMarginalObjectivesVersusGlobalRankingCorrelations(
                          ranking,Threading=False,Comments=True)
         Marginal objective ordinal correlation with given ranking
         -------------------------------------------------
         Given ranking: ['p04', 'p09', 'p01', 'p08', 'p16', 'p03', 
                         'p13', 'p20', 'p15', 'p10', 'p18', 'p19', 
                         'p06', 'p02', 'p07', 'p11', 'p05', 'p12', 
                         'p14', 'p21', 'p17']
         Objective (weight): correlation
         Soc (135.00): 	 +0.473
         Eco (135.00): 	 +0.457
         Env (135.00): 	 +0.326

        """
        try:
            objectives = [obj for obj in self.objectives]
        except:
            print('No objectives deined in this performance tableau!')
            return
        from copy import deepcopy
        from operator import itemgetter
        preorder = ranking2preorder(ranking)
        preorderRelation = self.computePreorderRelation(preorder)
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            origValuationdomain = deepcopy(self.valuationdomain)
            self.recodeValuation(-1,1)
            Normalizing = True
        else:
            Normalizing = False
        if Threading:
            #from multiprocessing import Pool
            #from os import cpu_count
            import multiprocessing as mp
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            Pool = mpctx.Pool
            cpu_count = mpctx.cpu_count

            if nbrCores is None:
                nbrCores= cpu_count()
                
            argsList = [(x,preorderRelation) for x in self.objectives]
            with Pool(nbrCores) as proc:   
                correlations = proc.map(self.computeMarginalObjectiveCorrelation,argsList)
            if ValuedCorrelation:
                objectivesCorrelation = [(correlations[i]['correlation']*correlations[i]['determination'],argsList[i][0]) for i in range(len(argsList))]
            else:
                objectivesCorrelation = [(correlations[i]['correlation'],argsList[i][0]) for i in range(len(argsList))]
        else:
            objectives = [c for c in self.objectives]
            objectivesCorrelation = []
            for c in objectives:
                corr = self.computeMarginalObjectiveCorrelation((c,preorderRelation),Threading=False)
                if ValuedCorrelation:
                    objectivesCorrelation.append((corr['correlation']*corr['determination'],c))            
                else:
                    objectivesCorrelation.append((corr['correlation'],c))            
        if Sorted:
            objectivesCorrelation.sort(reverse=True,key=itemgetter(0))
        if Normalizing:
            self.recodeValuation(origValuationdomain['min'],origValuationdomain['max'])
        if Comments:
            if objectivesCorrelation != []:
                if ValuedCorrelation:
                    print("Marginal objective valued correlation with given ranking")
                else:
                    print("Marginal objective ordinal correlation with given ranking")
                print('-------------------------------------------------')
                print('Given ranking:',ranking)
                print('Objective (weight): correlation')
                for item in objectivesCorrelation:
                    if ValuedCorrelation:
                        print('%s (%.2f): \t %+.3f' % (
                            item[2],self.objectives[item[2]]['weight'],
                            (item[0]*item[1])) )
                    else:
                        print('%s (%.2f): \t %+.3f' % (
                            item[1],self.objectives[item[1]]['weight'],
                            item[0]) )
            else:
                print('No objectives defined !')

        return objectivesCorrelation   

    def showMarginalVersusGlobalOutrankingCorrelation(self,Sorted=True,ValuedCorrelation=False,
                                                      Threading=False,
                                                      nbrOfCPUs=None,Comments=True):
        """
        Show method for computeCriterionCorrelation results.
        """
        from copy import deepcopy
        from operator import itemgetter
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            origValuationdomain = deepcopy(self.valuationdomain)
            self.recodeValuation(-1,1)
            Normalizing = True
        else:
            Normalizing = False
        criteriaList = [x for x in self.criteria]
        criteriaCorrelation = []
        totCorrelation = Decimal('0.0')
        for c in criteriaList:
            corr = self.computeCriterionCorrelation(c,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            if ValuedCorrelation:
                totCorrelation += corr['correlation']*corr['determination']
                criteriaCorrelation.append(((corr['correlation']*corr['determination']),c))
            else:
                totCorrelation += corr['correlation']
                criteriaCorrelation.append((corr['correlation'],c))                
        if Sorted:
            criteriaCorrelation.sort(reverse=True,key=itemgetter(0))
        if Comments:
            if ValuedCorrelation:
                print('Marginal versus global outranking valued correlation')
            else:
                print('Marginal versus global outranking correlation')
            print('criterion | weight\t correlation')
            print('----------|---------------------------')
            for x in criteriaCorrelation:
                c = x[1]
                print('%9s |  %.2f \t %.3f' % (
                    c,self.criteria[c]['weight'],x[0]))
            print('Sum(Correlations) : %.3f' % (totCorrelation))
            print('Determinateness   : %.3f' % (corr['determination']))
        if Normalizing:
            self.recodeValuation(origValuationdomain['min'],
                                 origValuationdomain['max'])
        return criteriaCorrelation

#---------------
    def computeMarginalVersusGlobalRankingCorrelations(self,
                    ranking,
                    Sorted=True,ValuedCorrelation=False,
                    Threading=False,nbrCores=None,
                    startMethod=None,
                    Comments=False):
        """
        Method for computing correlations between each individual criterion relation with the corresponding global ranking relation.
        
        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number ofavailable cores.
        """
        from copy import deepcopy
        from operator import itemgetter
        preorder = ranking2preorder(ranking)
        preorderRelation = self.computePreorderRelation(preorder)
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            origValuationdomain = deepcopy(self.valuationdomain)
            self.recodeValuation(-1,1)
            Normalizing = True
        else:
            Normalizing = False
        if Threading:
            #from multiprocessing import Pool
            #from os import cpu_count
            import multiprocessing as mp
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            Pool = mpctx.Pool
            cpu_count = mpctx.cpu_count

            if nbrCores is None:
                nbrCores= cpu_count()
                
            argsList = [(x,preorderRelation) for x in self.criteria]
            with Pool(nbrCores) as proc:   
                correlations = proc.map(self.computeMarginalCorrelation,argsList)
            if ValuedCorrelation:
                criteriaCorrelation = [(correlations[i]['correlation']*correlations[i]['determination'],argsList[i][0]) for i in range(len(argsList))]
            else:
                criteriaCorrelation = [(correlations[i]['correlation'],argsList[i][0]) for i in range(len(argsList))]
        else:
            #criteriaList = [x for x in self.criteria]
            criteria = self.criteria
            criteriaCorrelation = []
            for c in dict.keys(criteria):
                corr = self.computeMarginalCorrelation((c,preorderRelation),Threading=False)
                if ValuedCorrelation:
                    criteriaCorrelation.append((corr['correlation']*corr['determination'],c))            
                else:
                    criteriaCorrelation.append((corr['correlation'],c))            
        if Sorted:
            criteriaCorrelation.sort(reverse=True,key=itemgetter(0))
        if Normalizing:
            self.recodeValuation(origValuationdomain['min'],origValuationdomain['max'])
        return criteriaCorrelation   

    def computeCriterionCorrelation(self,criterion,Threading=False,
                                    nbrOfCPUs=None,Debug=False,
                                    Comments=False):
        """
        Renders the ordinal correlation coefficient between
        the global outranking and the marginal criterion relation.

        Uses the digraphs.computeOrdinalCorrelationMP().

        .. note::

             Renders a dictionary with the key 'correlation' containing the actual bipolar correlation index and the key 'determination' containing the minimal determination level D of the self outranking and the marginal criterion relation.

             D = sum_{x != y} min(abs(self.relation(x,y)),abs(marginalCriterionRelation(x,y)) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .
        """
        gc = BipolarOutrankingDigraph(self,Normalized=True,coalition=[criterion],CopyPerfTab=True,
                                      Threading=Threading,nbrCores=nbrOfCPUs,
                                      Comments=Comments)
        corr = self.computeOrdinalCorrelationMP(gc,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
        if Debug:
            print(corr)
        return corr

    def computeMarginalVersusGlobalOutrankingCorrelations(self,Sorted=True,ValuedCorrelation=False,
                                                          Threading=False,nbrCores=None,
                                                          startMethod=None,
                                                          Comments=False):
        """
        Method for computing correlations between each individual criterion relation with the corresponding
        global outranking relation.
        
        Returns a list of tuples (correlation,criterionKey) sorted by default in decreasing order of the correlation.

        If Threading is True, a multiprocessing Pool class is used with a parallel equivalent of the built-in map function.

        If nbrCores is not set, the os.cpu_count() function is used to determine the number of
        available cores.
        """
        from copy import deepcopy
        from operator import itemgetter
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            origValuationdomain = deepcopy(self.valuationdomain)
            self.recodeValuation(-1,1)
            Normalizing = True
        else:
            Normalizing = False
        if Threading:
            #from multiprocessing import Pool
            #from os import cpu_count
            import multiprocessing as mp
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            Pool = mpctx.Pool
            cpu_count = mpctx.cpu_count

            if nbrCores is None:
                nbrCores= cpu_count()
            criteriaList = [x for x in self.criteria]
            with Pool(nbrCores) as proc:   
                correlations = proc.map(self.computeCriterionCorrelation,criteriaList)
            if ValuedCorrelation:
                criteriaCorrelation = [
                    (correlations[i]['correlation']\
                      * correlations[i]['determination'],
                     criteriaList[i]) for i in range(len(criteriaList))]
            else:
                criteriaCorrelation = [
                    (correlations[i]['correlation'],
                     criteriaList[i]) for i in range(len(criteriaList))]
        else:
            #criteriaList = [x for x in self.criteria]
            criteria = self.criteria
            criteriaCorrelation = []
            for c in dict.keys(criteria):
                corr = self.computeCriterionCorrelation(c,Threading=False)
                if ValuedCorrelation:
                    criteriaCorrelation.append(
                        ( (corr['correlation']*corr['determination']) ,c) )
                else:
                    criteriaCorrelation.append((corr['correlation'],c))
        if Sorted:
            criteriaCorrelation.sort(reverse=True,key=itemgetter(0))
        if Normalizing:
            self.recodeValuation(origValuationdomain['min'],
                                 origValuationdomain['max'])
        return criteriaCorrelation   

    def showMarginalVersusGlobalOutrankingCorrelation(self,
                        Sorted=True,ValuedCorrelation=False,
                        Threading=False,
                        nbrOfCPUs=None,Comments=True):
        """
        Show method for computeCriterionCorrelation results.
        """
        from copy import deepcopy
        from operator import itemgetter
        if self.valuationdomain['min'] != Decimal('-1') or\
           self.valuationdomain['max'] != Decimal('1'):
            origValuationdomain = deepcopy(self.valuationdomain)
            self.recodeValuation(-1,1)
            Normalizing = True
        else:
            Normalizing = False
        criteriaList = [x for x in self.criteria]
        criteriaCorrelation = []
        totCorrelation = Decimal('0.0')
        for c in criteriaList:
            corr = self.computeCriterionCorrelation(c,Threading=Threading,nbrOfCPUs=nbrOfCPUs)
            if ValuedCorrelation:
                totCorrelation += corr['correlation']*corr['determination']
                criteriaCorrelation.append(((corr['correlation']*corr['determination']),c))
            else:
                totCorrelation += corr['correlation']
                criteriaCorrelation.append((corr['correlation'],c))                
        if Sorted:
            criteriaCorrelation.sort(reverse=True,key=itemgetter(0))
        if Comments:
            if ValuedCorrelation:
                print('Marginal versus global outranking valued correlation')
            else:
                print('Marginal versus global outranking correlation')
            print('criterion | weight\t correlation')
            print('----------|---------------------------')
            for x in criteriaCorrelation:
                c = x[1]
                print('%9s |  %.2f \t %.3f' % (
                    c,self.criteria[c]['weight'],x[0]) )
            print('Sum(Correlations) : %.3f' % (totCorrelation) )
            print('Determinateness   : %.3f' % (corr['determination']) )
        if Normalizing:
            self.recodeValuation(
                origValuationdomain['min'],origValuationdomain['max'])
        return criteriaCorrelation

    def computeQuantileSortRelation(self,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        the self quantile sorting result.
        """
        quantileSorting = self.computeQuantileSort()
        if Debug:
            print(quantileSorting)
        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        actions = list(self.actions.keys())
        n = len(actions)
        rankingRelation = {}
        for x in actions:
            rankingRelation[x] = {}
            rrx = rankingRelation[x]
            for y in actions:
                rrx[y] = Med
        for i in range(n):
            x = quantileSorting[i][1]
            for j in range(i+1,n):
                y = quantileSorting[j][1]
                if Debug:
                    print(x, y, quantileSorting[i][0], quantileSorting[j][0])
                if quantileSorting[i][0] > quantileSorting[j][0]:
                    rankingRelation[x][y] = Max
                    rankingRelation[y][x] = Min
                elif quantileSorting[i][0] < quantileSorting[j][0]:
                    rankingRelation[x][y] = Min
                    rankingRelation[y][x] = Max
                else:
                    rankingRelation[x][y] = Max
                    rankingRelation[y][x] = Max
                if Debug:
                    print(rankingRelation[x][y],rankingRelation[y][x])
        return rankingRelation        

    def showCriterionRelationTable(self,criterion, actionsSubset= None):
        """
        prints the relation valuation in actions X actions table format.
        """
        if actionsSubset is None:
            actions = self.actions
        else:
            actions = actionsSubset
        print('* ---- Criterion %s Relation Table -----\n' % (
                                          criterion), end=' ')
        print(' S   | ', end=' ')
        #actions = [x for x in actions]
        actionsList = [x for x in actions]

        actionsList.sort()
        
        for x in actionsList:
            print("'"+x+"', ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in actionsList:
            print("'"+x+"' | ", end=' ')
            for y in actionsList:
                #print '%2.2f ' % (self.relation[x[1]][y[1]]),
                print('%2.2f ' % (
                    self.computeCriterionRelation(criterion,x,y)), end=' ')
            print()
        print('\n')

    def computeAMPLData(self,OldValuation=False):
        """
        renders the ampl data list
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        for x in actionsList:
            for y in actionsList:
                print(str(x)+str(y), end=' ')
                for c in self.criteria:
                    value = self.computeCriterionRelation(c,x,y)
                    if OldValuation:                        
                        value = (value + Decimal("1.0"))/Decimal("2.0")
                    else:
                        value = self.computeCriterionRelation(c,x,y)
                    print('%.1f' % (value), end=' ')
                print()         

    def computeCriterionRelation(self,c,a,b):
        """
        compute the outranking characteristic for actions x and y
        on criterion c.
        """
        criteria = self.criteria
        evaluation = self.evaluation
        try:
            NA = self.NA
        except:
            NA = Decimal('-999')
        if a == b:
            return Decimal("1.0")
        else:

            if self.evaluation[c][a] != NA and self.evaluation[c][b] != NA:		
                try:
                    indx = self.criteria[c]['thresholds']['ind'][0]
                    indy = self.criteria[c]['thresholds']['ind'][1]
                    ind = indx +indy * self.evaluation[c][a]
                except:
                    ind = None
                try:
                    wpx = self.criteria[c]['thresholds']['weakPreference'][0]
                    wpy = self.criteria[c]['thresholds']['weakPreference'][1]
                    wp = wpx + wpy * self.evaluation[c][a]
                except:
                    wp = None
                try:
                    px = self.criteria[c]['thresholds']['pref'][0]
                    py = self.criteria[c]['thresholds']['pref'][1]
                    p = px + py * self.evaluation[c][a]
                except:
                    p = None
                if self.criteria[c]['weight'] > Decimal('0.0'):
                    d = self.evaluation[c][a] - self.evaluation[c][b]
                else:
                    d = self.evaluation[c][b] - self.evaluation[c][a]
                if ind is None:
                    return self._localConcordance(d,wp,p)
                else:
                    return self._localConcordance(d,ind,p)
            else:
                return Decimal("0.5")


    def computeSingletonRanking(self,Comments = False, Debug = False):
        """
        Renders the sorted bipolar net determinatation of outrankingness
        minus outrankedness credibilities of all singleton choices.

        res = ((netdet,singleton,dom,absorb)+)

        """
        import copy
        from operator import itemgetter
        valuationdomain = copy.deepcopy(self.valuationdomain)
        
        self.recodeValuation(0.0,100.0)
        

        sigs = [x[0] for x in self.singletons()]

        res = []
        for i in range(len(sigs)):
            if Debug:
                print(sigs[i], self.domin(sigs[i]) - self.absorb(sigs[i]))
            res.append((self.domin(sigs[i]) - self.absorb(sigs[i]),sigs[i],self.domin(sigs[i]),self.absorb(sigs[i])))

        res.sort(reverse=True,key=itemgetter(0))

    
        if Comments:
            for x in res:
                print("{%s} : %.3f " % (
                    [y for y in x[1]][0], (float(x[0]) + 100.0)/2.0 ))

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
    

    def defaultDiscriminationThresholds(self, quantile = {'ind':10,'pref':20,'weakVeto':60,'veto':80}, Debug = False, comments = False):
        """
        updates the discrimination thresholds with the percentiles
        from the performance differences.

        Parameters:
            quantile = {'ind': 10, 'pref': 20, 'weakVeto': 60, 'veto: 80}.
        
        """
        self.computeDefaultDiscriminationThresholds(quantile,Debug,comments)
        self.relation = self._constructRelation(self.criteria,self.evaluation)

    def computeWeightsConcentrationIndex(self):
        """
        Renders the Gini concentration index of the weight distribution

        Based on the triangle summation formula.

        """
        import copy
        weightSum = Decimal('0.0')
        p= len(self.criteria)
        #p = Decimal(str(len(self.criteria)))
        criteriaList = list(copy.deepcopy(self.criteria))
        criteria = []
        for i in range(p):
            criteria.append((self.criteria[criteriaList[i]]['weight'],criteriaList[i]))
        criteria.sort()
        for i in range(p):
            weightSum += abs(self.criteria[criteriaList[i]]['weight'])
        if weightSum != Decimal('0.0'):
            Q = [Decimal('0.0') for i in range(p)]
            F = [Decimal('0.0') for i in range(p)]
            F[0] = Decimal('1.0')/Decimal(str(p))
            i = 1
            Q[0] = self.criteria[criteria[0][1]]['weight']/weightSum           
            for i in range(1,p):
                qi = self.criteria[criteria[i][1]]['weight']/weightSum
                Q[i] += Q[i-1] + qi
                fi = Decimal('1.0')/Decimal(str(p))
                F[i] += F[i-1] + fi
                i += 1
            gini = Decimal('0.0')
            for i in range(p-1):
                gini += (F[i]*Q[i+1]) - (Q[i]*F[i+1])
        else:
            gini = Decimal('-1')
        return gini

    def _constructRelation(self,criteria,evaluation,hasNoVeto=False):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        actions = self.actions
        NA = self.NA
        Min = Decimal(str(self.valuationdomain['min']))
        Max = Decimal(str(self.valuationdomain['max']))
        totalweight = Decimal('0.0')
        for c in criteria:
            totalweight = totalweight + abs(criteria[c]['weight'])
        vetos = []
        relation = {}
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a == b:
                    relation[a][b] = Min
                else:
                    nc = len(criteria)
                    counter = Decimal('0.0')
                    veto = Decimal('0')
                    abvetos = []
                    for c in criteria:
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                ax = criteria[c]['thresholds']['ind'][0]
                                ay = criteria[c]['thresholds']['ind'][1]
                                ind = ax + ay * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            except:
                                ind = None
                            try:
                                ax = criteria[c]['thresholds']['weakPreference'][0]
                                ay = criteria[c]['thresholds']['weakPreference'][1]
                                wp = ax + ay * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            except:
                                wp = None
                            try:
                                bx = criteria[c]['thresholds']['pref'][0]
                                by = criteria[c]['thresholds']['pref'][1]
                                p = bx + by * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            except:
                                p = None
                            try:
                                vx = criteria[c]['thresholds']['veto'][0]
                                vy = criteria[c]['thresholds']['veto'][1]
                                v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            except:
                                v = None
                            if criteria[c]['weight'] > Decimal('0.0'):
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]
                            lc0 = self._localConcordance(d,ind,wp,p)
                            counter = counter + (lc0 * abs(criteria[c]['weight']))
                            testveto = self._localVeto(d,v)
                            if criteria[c]['weight'] > Decimal('0'):
                                veto = veto + testveto
                                if testveto == Decimal('1'):
                                    abvetos.append((c,v,d))
                        else:
                            counter = counter + Decimal('0.5') * abs(criteria[c]['weight'])
                    concordindex = ((counter / totalweight) * (Max-Min)) + Min
                    discordindex = Min
                    if veto == Decimal('0'):
                        relation[a][b] = concordindex
                    else:
                        relation[a][b] = discordindex
                        vetos.append(([a,b,concordindex],abvetos))
        for a in actions:
            relation[a][a] = Min
        self.vetos = vetos
        return relation

    def computePairwiseOddsMatrix(self):
            """
            renders a double dictionary with odds:
            (positive chaacteristics, negative characteristics)
            per actions pair.
            """
            actionsList = [x for x in self.actions]
            n = len(actionsList)
            criteriaList = [x for x in self.criteria]
            oddsMatrix = {}
            for a in actionsList:
                oddsMatrix[a] = {}
                for b in actionsList:
                    if a == b:
                        oddsMatrix[a][b] = (Decimal('0.0'),Decimal('0.0'))
                    else:               
                        plusOdds = Decimal('0.0')
                        minusOdds = Decimal('0.0')
                        for c in criteriaList:
                            cab = self.criterionCharacteristicFunction(c,a,b)
                            if cab > Decimal('0'):
                                plusOdds += cab
                            else:
                                minusOdds += -cab
                            #print(c,plusodds,minusodds)
                        oddsMatrix[a][b] = (plusOdds,minusOdds)
            return oddsMatrix

    def computePairwiseCompleteComparison(self,a,b,c):
        """
        renders pairwise complete comparison parameters for actions a and b
        on criterion c.
        """
        Debug = False
        
        evaluation = self.evaluation
        NA = self.NA
        criteria = self.criteria
        actionsList = [x for x in self.actions]

        # initialize Degenne vector
        pairwiseComparison = {'v':0, 'wv':0, 'lt':0, 'leq':0, 'eq':0, 'geq':0, 'gt':0, 'gwvt':0, 'gvt':0}

        # main loop
        if evaluation[c][a] != NA or evaluation[c][b] != NA:
            # compute discrimination thresholds
            try:
                indx = criteria[c]['thresholds']['ind'][0]
                indy = criteria[c]['thresholds']['ind'][1]
                ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
            except:
                ind = Decimal('0')
            try:
                wpx = criteria[c]['thresholds']['weakPreference'][0]
                wpy = criteria[c]['thresholds']['weakPreference'][1]
                wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))                           
            except:
                wp = None

            try:
                px = criteria[c]['thresholds']['pref'][0]
                py = criteria[c]['thresholds']['pref'][1]
                p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
            except:
                p = None
            try:
                wvx = criteria[c]['thresholds']['weakVeto'][0]
                wvy = criteria[c]['thresholds']['weakVeto'][1]
                wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
            except:
                wv = Decimal(str(criteria[c]['scale'][1])) + Decimal('1')
            try:
                vx = criteria[c]['thresholds']['veto'][0]
                vy = criteria[c]['thresholds']['veto'][1]
                v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
            except:
                v = Decimal(str(criteria[c]['scale'][1])) + Decimal('1')
                
            # compute performance difference
            if criteria[c]['weight'] > Decimal('0.0'):
                d = evaluation[c][a] - evaluation[c][b]
            else:
                d = evaluation[c][b] - evaluation[c][a]
            # compute characteristic
            
            if d > Decimal('0'):  # positive difference
                if d >= v:
                    pairwiseComparison['gvt'] = 1
                elif d >= wv:
                    pairwiseComparison['gwvt'] = 1 
                elif p is not None:
                    if d >= p:
                        pairwiseComparison['gt'] = 1
                    elif wp is not None:
                        if d >= wp:
                            pairwiseComparison['geq'] = 1
                        else:
                            pairwiseComparison['eq'] = 1
                    else:
                        if d > ind:
                            pairwiseComparison['geq'] = 1
                        else:
                            pairwiseComparison['eq'] = 1
                else:
                    pairwiseComparison['geq'] = 1
                    
            elif d == Decimal('0'): # zero difference
                pairwiseComparison['eq'] = 1

            else:   # negative difference

                if d <= -v:
                    pairwiseComparison['v'] = 1
                elif d <= -wv:
                    pairwiseComparison['wv'] = 1 
                elif p is not None:
                    if d <= -p:
                        pairwiseComparison['lt'] = 1
                    elif wp is not None:
                        if d <= -wp:
                            pairwiseComparison['leq'] = 1
                        else:
                            pairwiseComparison['eq'] = 1
                    else:
                        if d < -ind:
                            pairwiseComparison['leq'] = 1
                        else:
                            pairwiseComparison['eq'] = 1
                else:
                    pairwiseComparison['leq'] = 1
        else:
            # missing evaluation(s)
            d = None
            pairwiseComparison = None
        if Debug:
            print('>>> c,a,b,d', c,a,b,d)
            print('ind,wp,p,wv,v', ind,wp,p,wv,v)
            print('pairwiseComparison', pairwiseComparison)
            
        return pairwiseComparison

    def computeActionsComparisonCorrelations(self):
        """
        renders the comparison correlations between the actions
        """
        from decimal import Decimal
        
        criteriaList = [x for x in self.criteria]
        actionsList = [x for x in self.actions]
        #nPairs = Decimal(str(len(criteriaList)*((len(criteriaList)-1))))

        actionsCorrelationIndex = {}

        for a in actionsList:
        #for gi in criteriaList:
            actionsCorrelationIndex[a] = {}
            #for gj in criteriaList:
            for b in actionsList:
                actionsCorrelationIndex[a][b] = Decimal('0.0')
                nPairs = Decimal('0.0')
                #for a in actionsList:
                for gi in criteriaList:                
                    #for b in actionsList:
                    for gj in criteriaList:
                        if gi != gj:                                                    
                            nPairs += Decimal('1.0')
                            compi = self.computePairwiseCompleteComparison(a,b,gi)
                            compj = self.computePairwiseCompleteComparison(a,b,gj)
                            if compi is not None and compj is not None:
                                if compi == compj:
                                    actionsCorrelationIndex[a][b] += Decimal('1.0')
                                elif (compi['gvt']==1 or compi['gwvt']==1 or compi['gt']==1) and (compj['gvt']==1 or compj['gwvt']==1 or compj['gt']==1):
                                    actionsCorrelationIndex[a][b] += Decimal('0.5')
                                elif (compi['v']==1 or compi['wv']==1 or compi['lt']==1) and (compj['v']==1 or compj['wv']==1 or compj['lt']==1):
                                    actionsCorrelationIndex[a][b] += Decimal('0.5')
                            else:
                                actionsCorrelationIndex[a][b] += Decimal('0.5')
                #print nPairs,criteriaCorrelationIndex[gi][gj]
                actionsCorrelationIndex[a][b] = (Decimal('2.0') * actionsCorrelationIndex[a][b] - nPairs) / nPairs
        return actionsCorrelationIndex

    def computeCriteriaCorrelations(self,ValuedCorrelation=False):
        """
        renders the relation equivalence or correlation between the criteria
        """
        from digraphs import EquivalenceDigraph
        criteriaList = [x for x in self.criteria]
        actionsList = [x for x in self.actions]
        nPairs = self.order*(self.order-1)
        #nPairs = self.order*(self.order)
        tau = {}
        d = {}
        
        for gi in criteriaList:
            tau[gi] = {}
            d[gi] = {}
            Pgi = BipolarOutrankingDigraph(self,coalition=[gi])
            for gj in criteriaList:
                M = Decimal('0.0')
                D = Decimal('0.0')
                Pgj = BipolarOutrankingDigraph(self,coalition=[gj])
                EQ = EquivalenceDigraph(Pgi,Pgj)
                #nPairs = 0.0
                for x in actionsList:
                    for y in actionsList:
                        #if x != y:
                        M += EQ.relation[x][y]
                        D += abs(EQ.relation[x][y])
                if ValuedCorrelation:
                    tau[gi][gj] = M / nPairs
                elif D != Decimal('0.0'):
                    tau[gi][gj] = M / D
                else:
                    tau[gi][gj] = Decimal('0.0')
                d[gi][gj] = D / nPairs                            
                
        return tau, d

    def computeCriteriaComparisonCorrelations(self):
        """
        renders the comparison correlations between the criteria
        """
        criteriaList = [x for x in self.criteria]
        actionsList = [x for x in self.actions]
        nPairs = Decimal(str(len(actionsList)*((len(actionsList)-1))))

        criteriaCorrelationIndex = {}

        for gi in criteriaList:
            criteriaCorrelationIndex[gi] = {}
            for gj in criteriaList:
                criteriaCorrelationIndex[gi][gj] = Decimal('0.0')
                #nPairs = 0.0
                for a in actionsList:
                    for b in actionsList:
                        if a != b:
                            #nPairs += 1.0
                            compi = self.computePairwiseCompleteComparison(a,b,gi)
                            compj = self.computePairwiseCompleteComparison(a,b,gj)
                            if compi is not None and compj is not None:
                                if compi == compj:
                                    criteriaCorrelationIndex[gi][gj] += Decimal('1.0')
                                elif (compi['gvt']==1 or compi['gwvt']==1 or compi['gt']==1) and (compj['gvt']==1 or compj['gwvt']==1 or compj['gt']==1):
                                    criteriaCorrelationIndex[gi][gj] += Decimal('0.5')
                                elif (compi['v']==1 or compi['wv']==1 or compi['lt']==1) and (compj['v']==1 or compj['wv']==1 or compj['lt']==1):
                                    criteriaCorrelationIndex[gi][gj] += Decimal('0.5')                                
                            else:
                                criteriaCorrelationIndex[gi][gj] += Decimal('0.5')
                #print nPairs,criteriaCorrelationIndex[gi][gj]
                criteriaCorrelationIndex[gi][gj] = (Decimal('2.0') * criteriaCorrelationIndex[gi][gj] - nPairs) / nPairs
        return criteriaCorrelationIndex


    def showCriteriaCorrelationTable(self,ValuedCorrelation=False,isReturningHTML=False,ndigits=3):
        """
        prints the ordinal correlation index tau between criteria in table format.
        """
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        n = len(self.actions)
        nPairs = n*n
        corr,deter = self.computeCriteriaCorrelations(ValuedCorrelation=ValuedCorrelation)
        html = ''
        # title
        if isReturningHTML:
            if ValuedCorrelation:
                html += '<h1>Criteria valued ordinal correlation index</h1>'
            else:
                html += '<h1>Criteria ordinal correlation index</h1>'
        else:
            if ValuedCorrelation:
                print('Criteria valued ordinal correlation index')
            else:
                print('Criteria ordinal correlation index')
        # header row
        if isReturningHTML:
            html += '<table border=1><tr bgcolor="#9acd32"><th>&tau;</th>'
        else:
            print('     |', end=' ')
        for x in criteriaList:
            if isReturningHTML:
                html += '<th bgcolor="#FFEEAA">%s</th>' % (x)
            else:
                print('%5s  ' % (x), end=' ')
        if isReturningHTML:
            html += '</tr>'
        else:
            print()
            hline = '-----|'
            for i in range(len(criteriaList)+1):
                hline += '-------'
            print(hline)
        # table body
        for i in range(len(criteriaList)):
            if isReturningHTML:
                html += '<tr><th bgcolor="#FFEEAA">%s</th>' % (criteriaList[i])
            else:
                print('%4s |' %(criteriaList[i]), end=' ')
            for j in range(len(criteriaList)):
                if i <= j:
                    gi = criteriaList[i]
                    gj = criteriaList[j]
                    index = corr[gi][gj]
                    if isReturningHTML:
                        if index >= 0:
                            html += '<td bgcolor="#ddffdd">%+2.2f</td>' %\
                                (index)
                        else:
                            html += '<td bgcolor="#ffddff">%+2.2f</td>' %\
                                (index)
                            
                    else:
                        print(('%%+2.%df ' % ndigits)  % (index), end=' ')
                else:
                    if isReturningHTML:
                        html += '<td>&nbsp;</td>'
                    else:
                        index = '       '
                        print(index, end=' ')
            if isReturningHTML:
                html += '</tr>'
            else:
                print()
        if isReturningHTML:
            html += '</table>'
        # render the result
        return html
                
    def computeActionsCorrelationDigraph(self):
        """
        renders the pairwise actions comparison digraph
        """
        from digraphs import Digraph
        from copy import deepcopy
        corr = self.computeActionsComparisonCorrelations()
        n = self.order
        g = EmptyDigraph(order=n)
        g.__class__ = Digraph
        g.name = 'actCorrGraph'
        g.valuationdomain = {'min':Decimal('-1.0'),'med':Decimal('0.0'),'max':Decimal('1.0')}
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        Max = g.valuationdomain['max']
        g.actions = deepcopy(self.actions)
        g.relation = self.computeActionsComparisonCorrelations()
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        return g

    def computeCriteriaCorrelationDigraph(self,ValuedCorrelation=True,WithMedian=False):
        """
        renders the ordinal criteria correlation digraph.
        """
        from digraphs import Digraph
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        corr,d = self.computeCriteriaCorrelations(ValuedCorrelation=ValuedCorrelation)
        n = len(criteriaList)
        g = EmptyDigraph(order=n)
        g.__class__ = Digraph
        if ValuedCorrelation:
            g.name = 'valCorrGraph'
        else:
            gname = 'corrGraph'
        g.valuationdomain = {'min':Decimal('-1.0'),'med':Decimal('0.0'),'max':Decimal('1.0')}
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        Max = g.valuationdomain['max']
        if WithMedian:
            criteriaList.append('m')
        relation = {}
        for i in range(n):
            relation[criteriaList[i]] = {}
            for j in range(n):
                relation[criteriaList[i]][criteriaList[j]] = corr[criteriaList[i]][criteriaList[j]]
        if WithMedian:
            margCorr = self.computeOutrankingConsensusQuality(ValuedCorrelation=ValuedCorrelation)
            #print(margCorr)
            relation['m'] = {}
            relation['m']['m'] = self.computeDeterminateness()
            for item in margCorr[0]:
                relation[item[1]]['m'] = item[0]
                relation['m'][item[1]] = item[0]
        g.actions = criteriaList
        g.relation = relation
        #g.gamma = g.gammaSets()
        #g.notGamma = g.notGammaSets()
        return g
        
    def showCriteriaHierarchy(self):
        """
        shows the Rubis clustering of the ordinal criteria correlation table
        """
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        corr,d = self.computeCriteriaCorrelations()
        n = len(criteriaList)
        g = RandomValuationDigraph(order=n)
        g.name = 'corrGraph'
        g.valuationdomain = {'min':Decimal('-1.0'),'med':Decimal('0.0'),'max':Decimal('1.0')}
        Min = g.valuationdomain['min']
        Med = g.valuationdomain['med']
        Max = g.valuationdomain['max']
        g.actions = criteriaList
        relation = {}
        for i in range(n):
            relation[criteriaList[i]] = {}
            for j in range(n):
                relation[criteriaList[i]][criteriaList[j]] = -corr[criteriaList[i]][criteriaList[j]]
        g.relation = relation
        g.gamma = g.gammaSets()
        g.notGamma = g.notGammaSets()
        g.computePreKernels()
        actions = set(g.actions)
        criteriaHierarchy = []
        for ker in g.dompreKernels:
            cluster = [y for y in ker]
            cluster.sort()
            degintstab = g.intstab(ker)
            degextstab = g.domin(ker)
            cred = min(degintstab,degextstab)
            criteriaHierarchy.append((-cred,degintstab,degextstab,cluster))
        criteriaHierarchy.sort()
        print('*------ criteria clustering hierarchy ------*')
        clustered = set()
        hierarchy = []
        for ch in criteriaHierarchy:
            hierarchy = hierarchy + [ch[3]]
            clustered |= set(ch[3])
            rest = actions - clustered
            print('Cluster: %s\n   Credibility level: %2.2f%%; Exterior stability: %2.2f%%; Interior stability: %2.2f%%' % (str(ch[3]),
                (-ch[0]+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0'),
                (ch[2]+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0'),
                (ch[1]+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0')))
            print('   Hierarchy: ', hierarchy)
            print()

    def saveActionsCorrelationTable(self,fileName='tempcorr.prn',delimiter=' ',Bipolar=True,Silent=False,Centered=False):
        """
        Delimited save of correlation table
        """
        import math
        actionsList = [x for x in self.actions]
        actionsList.sort()
        n = len(actionsList)
        nd = Decimal(str(n))
        corr = self.computeActionsComparisonCorrelations()
        if not Bipolar:
            for i in range(n):
                for j in range(n):
                    corr[actionsList[i]][actionsList[j]] = Decimal('1.0') - (corr[actionsList[i]][actionsList[j]] + Decimal('1.0'))/Decimal('2.0')
        if Centered:
            centcorr = [Decimal('0.0') for x in range(n)]
            for i in range(n):
                for j in range(n):
                    centcorr[i] += corr[actionsList[i]][actionsList[j]]/nd
            #print centcorr
            for i in range(n):
                for j in range(n):
                    corr[actionsList[i]][actionsList[j]] = (corr[actionsList[i]][actionsList[j]]-centcorr[i])/Decimal.sqrt(nd)
                #print i, corr[actionsList[i]]
        fo = open(fileName,'w')
        for i in range(n):
            for j in range(n-1):
##                 if Bipolar:
                value = corr[actionsList[i]][actionsList[j]]
##                 else:
##                     value = 1.0 - (corr[actionsList[i]][actionsList[j]] + 1.0)/2.0
                fo.write('%2.2f %s' % (value,delimiter)),
##             if Bipolar:
            value = corr[actionsList[i]][actionsList[n-1]]
##             else:
##                 value = 1.0 - (corr[actionsList[i]][actionsList[len(actionsList)-1]] + 1.0)/2.0
            fo.write('%2.2f\n' % (value))
        fo.close()
        if not Silent:
            print('Actions Correlation saved on file %s' % (fileName))
        
        
    def saveCriteriaCorrelationTable(self,fileName='tempcorr.prn',delimiter=' ',
                                     ValuedCorrelation=False,Bipolar=True,
                                     Silent=False,Centered=False):
        """
        Delimited save of correlation table
        """
        import math
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        #print(criteriaList)
        n = len(criteriaList)
        nd = Decimal(str(n))
        corr,d = self.computeCriteriaCorrelations(ValuedCorrelation=ValuedCorrelation)
        #print(corr)
        if not Bipolar:
            for i in range(n):
                for j in range(n):
                    corr[criteriaList[i]][criteriaList[j]] = Decimal('1.0') - (corr[criteriaList[i]][criteriaList[j]] + Decimal('1.0'))/Decimal('2.0')
        if Centered:
            centcorr = [Decimal('0.0') for x in range(n)]
            for i in range(n):
                for j in range(n):
                    centcorr[i] += corr[criteriaList[i]][criteriaList[j]]/nd
            #print centcorr
            for i in range(n):
                for j in range(n):
                    corr[criteriaList[i]][criteriaList[j]] = (corr[criteriaList[i]][criteriaList[j]]-centcorr[i])/Decimal.sqrt(nd)
                #print i, corr[criteriaList[i]]
        fo = open(fileName,'w')
        for i in range(n):
            for j in range(n-1):
##                 if Bipolar:
                value = corr[criteriaList[i]][criteriaList[j]]
##                 else:
##                     value = 1.0 - (corr[criteriaList[i]][criteriaList[j]] + 1.0)/2.0
                fo.write('%2.2f %s' % (value,delimiter)),
##             if Bipolar:
            value = corr[criteriaList[i]][criteriaList[n-1]]
##             else:
##                 value = 1.0 - (corr[criteriaList[i]][criteriaList[len(criteriaList)-1]] + 1.0)/2.0
            fo.write('%2.2f\n' % (value))
        fo.close()
        if not Silent:
            print('Criteria Correlation saved on file %s' % (fileName))

    def export3DplotOfCriteriaCorrelation(self,plotFileName="critCorr",
                                          tempDir='.',
                                          graphType=None,
                                          pictureFormat='pdf',
                                          bgcolor='cornsilk',
                                          ValuedCorrelation=False,
                                          WithMedian=False,
                                          Comments=False):
        """
        Using R for producing a plot (pdf format by default) of the principal components of
        the criteria ordinal correlation table.

        *Parameters*:

            * *plotFileName* := name of the created R plot image,
            * *pictureFormat* := 'png' (default) | 'pdf' | 'jpeg' | 'xfig',
            * *graphType* := deprecated
            * *bgcolor* := 'cornsilk' by default | None,
            * *ValuedCorrelation* := False (tau by default) | True (r(<=>) otherwise,
            * *WithMedian* includes the marginal correlation with the global outranking relation
            * *tempDir* := '.' : default current working directory.
        
        """
        cg = CriteriaCorrelationDigraph(self,ValuedCorrelation=ValuedCorrelation,WithMedian=WithMedian)
        if graphType is not None:
            pictureFormat = graphType
        cg.exportPrincipalImage(plotFileName=plotFileName,
                                tempDir=tempDir,
                                pictureFormat=pictureFormat,
                                bgcolor=bgcolor,
                                Comments=Comments)

    def _export3DplotOfCriteriaCorrelation(self,plotFileName="correlation",
                                          ValuedCorrelation=False,Type="pdf",
                                          graphType='pdf',bgcolor='cornsilk',
                                          Comments=False,bipolarFlag=False,
                                          _dist=True,_centeredFlag=False,
                                          tempDir=None):
        """
        Obsolete and deprecated
        use Calmat and R for producing a plot of the principal components of
        the criteria ordinal correlation table.

        *Parameters*;

            * *plotFileName* := name of the created R plot image.
            * deprecated ! *Type*,
            * *graphType* := format of graphics file: pdf, png, jpeg, xfig, 
            * *bgcolor* := 'cornsilk' by default | None
            * *ValuedCorrelation* := False (tau by default) | True (r(<=>) otherwise
            * *tempDir* : if None the tempfile.gettempdir() is used to get the platform independent temporary directory.
            * *bipolarFlag*: obsolete
            * *_dist*: internal Calmat flag
            * *_centeredFlag* : internal Calmat flag
            
        """
        import time
        from tempfile import TemporaryDirectory, gettempdir
        import os
        currentDir = os.getcwd()
        #print(currentDir)
        plotFileName = '%s/%s' % (currentDir,plotFileName)
        Type = graphType
        if Comments:
            print('3DplotFileName: %s' % plotFileName)
        if tempDir is None:
            tempDir = gettempdir()
        with TemporaryDirectory(dir=tempDir) as tempDirName:
            if Comments:
                print('*----  export 3dplot of type %s -----' % (Type))
            os.chdir(tempDirName)
            criteriaList = [x for x in self.criteria]
            criteriaList.sort()
            n = len(criteriaList)
            fo = open('criteriaLabels.prn','w')
            for key in criteriaList:
                fo.write('%s ' % (key))
            fo.close()
            self.saveCriteriaCorrelationTable(fileName='tempcorr.prn',Silent=True,
                                              ValuedCorrelation=ValuedCorrelation,
                                              Bipolar=bipolarFlag,Centered=_centeredFlag)
            # create Calmat script and calmat execution (the prn extension is standard)
            try:
                if Comments:
                    if _dist:
                        cmd = 'env defdist.sh tempcorr '+str(n)+' '+str(n)
                    else:
                        cmd = 'env defdista.sh tempcorr '+str(n)+' '+str(n) 
                else:
                    if _dist:
                        cmd = 'env defdist.sh tempcorr '+str(n)+' '+str(n)+' > /dev/null'
                    else:
                        cmd = 'env defdista.sh tempcorr '+str(n)+' '+str(n)+' > /dev/null'
                os.system(cmd)
                if Comments:
                    os.system('env calmat tempcorr.prg')
                else:
                    os.system('env calmat tempcorr.prg > /dev/null')
            except:
                print('Error: You need to install calmat !!!')
                return
            # create R 3d scatter plot script
            if Type == "interactive":
                fo = open('scatter.r','w')
                fo.write('# 3d scatter plot RB April 2008\n')
                fo.write('test.mat <- matrix(scan("compolg.prn"),ncol=%d,byrow=T)\n' % (n))
    ##             fo.write('choose<-c(%d,%d,%d)\n' % (1,2,3))
                fo.write('choose<-c(%d,%d,%d)\n' % (n,n-1,n-2))
                fo.write('test.labels <- scan("criteriaLabels.prn",what="character")\n') 
                fo.write('valprop <- matrix(scan("val_prlg.prn"),ncol=2,byrow=T)\n') 
                fo.write('require(rgl)\n')
                fo.write('open3d()\n')
                fo.write('points3d(test.mat[,choose])\n')
                fo.write('text3d(test.mat[,choose],text=test.labels,col="red3")\n')
                fo.write('axes3d(edges=c("x","y","z"),pos=c(0,0,0),labels=F,ticks=F)\n')
                fo.write('axes3d(edges=c("x","y","z"))\n')
                fo.write('title3d(main="Criteria Ordinal Correlation",xlab=valprop[choose,2][1],ylab=valprop[choose,2][2],zlab=valprop[choose,2][3],col="blue",line=4)\n')
                fo.write('rgl.viewpoint(1,1/4,interactive=T)\n')
                fo.write('rgl.snapshot("%s.png")\n' % (plotFileName+'.png') )
                fo.close()
            else:
                fo = open('scatter.r','w')
                fo.write('# scatter plot RB April 2008\n')
                fo.write('test.mat <- matrix(scan("compolg.prn"),ncol=%d,byrow=T)\n' % (n))
                fo.write('lim1 <- max(test.mat)\n')
                fo.write('lim2 <- min(test.mat)\n')
                if _centeredFlag:
                    fo.write('choose12<-c(%d,%d)\n' % (1,2))
                    fo.write('choose23<-c(%d,%d)\n' % (2,3))
                    fo.write('choose13<-c(%d,%d)\n' % (1,3))
                    fo.write('choose21<-c(%d,%d)\n' % (2,1))
                else:
                    fo.write('choose12<-c(%d,%d)\n' % (n,n-1))
                    fo.write('choose23<-c(%d,%d)\n' % (n-1,n-2))
                    fo.write('choose13<-c(%d,%d)\n' % (n,n-2))
                    fo.write('choose21<-c(%d,%d)\n' % (n-1,n))
                fo.write('test.labels <- scan("criteriaLabels.prn",what="character")\n') 
                fo.write('valprop <- matrix(scan("val_prlg.prn"),ncol=2,byrow=T)\n')
                if Type == "png":
                    fo.write('png("%s.png",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
                elif Type == "jpeg":
                    fo.write('jpeg("%s.jpg",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
                elif Type == "xfig":
                    fo.write('xfig("%s.fig",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
                elif Type == "pdf":
                    if bgcolor is not None:
                        fo.write('pdf("%s.pdf",width=6,height=6,bg="%s",title="PCA of Criteria Correlation Index")\n' % (plotFileName,bgcolor) )
                    else:
                        fo.write('pdf("%s.pdf",width=6,height=6,title="PCA of Criteria Correlation Index")\n' % (plotFileName) )
                         
                else:
                    print('Error: Plotting device %s not defined !' % (Type))
                    return     
                fo.write('par(mfrow=c(2,2))\n')
                fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
                fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
                fo.write('title(sub=paste("total inertia:",(valprop[choose12,2][1]+valprop[choose12,2][2])*100,"%"),main="factors 1 and 2",col="blue")\n')
                fo.write('text(test.mat[,choose12],labels=test.labels,col="red3",cex=1.0)\n')
    ##             fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
                fo.write('plot(test.mat[,choose12],xlab=paste("axis 2:",valprop[choose23,2][1]*100,"%"),ylab=paste("axis 3:",valprop[choose23,2][2]*100,"%"),type="n",asp=1)\n')
                fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
                fo.write('title(sub=paste("total inertia:",(valprop[choose23,2][1]+valprop[choose23,2][2])*100,"%"),main="factors 2 and 3",col="blue")\n')
                fo.write('text(test.mat[,choose23],labels=test.labels,col="red3",cex=1.0)\n')
    ##             fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
                fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose13,2][1]*100,"%"),ylab=paste("axis 3:",valprop[choose13,2][2]*100,"%"),type="n",asp=1)\n')
                fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
                fo.write('title(sub=paste("total inertia:",(valprop[choose13,2][1]+valprop[choose13,2][2])*100,"%"),main="factors 1 and 3",col="blue")\n')
                fo.write('text(test.mat[,choose13],labels=test.labels,col="red3",cex=1.0)\n')
                if _centeredFlag:
                    fo.write('barplot(valprop[1:nrow(valprop)-1,2]*100,names.arg=c(1:%d),main="Axis inertia (in %%)",col="orangered")\n' % (n-1))
                else:
                    fo.write('barplot(valprop[nrow(valprop):2,2]*100,names.arg=c(1:%d),main="Axis inertia (in %%)",col="orangered")\n' % (n-1))     
                fo.write('dev.off()\n')           
                fo.close()
                
            try:
                ## if Comments:
                ##     os.system('/usr/bin/R -q --vanilla --verbose < scatter.r 2>&1')
                ## else:
                ##     os.system('/usr/bin/R -q --vanilla < scatter.r > /dev/null 2> /dev/null')
                if Comments:
                    os.system('env R -q --vanilla --verbose < scatter.r 2>&1')
                else:
                    os.system('env R -q --vanilla < scatter.r > /dev/null 2> /dev/null')
                time.sleep(3)     
                if Comments:
                    print('See %s.%s ! ' % (plotFileName,Type))
            except:
                print('Error: You need to install R !!!')

        # reset current working dir !!!
        os.chdir(currentDir)

    def export3DplotOfActionsCorrelation(self,plotFileName="actCorr",
                                          graphType=None,
                                          pictureFormat='pdf',
                                          bgcolor='cornsilk', Comments=False):
        """
        Using R for producing a plot -pdf format by default- of the principal components of
        the actions ordinal correlation table. 

        See export3DplotCriteriaCorrelation()
        """
        from copy import deepcopy
        relationOrig = deepcopy(self.relation)
        self.relation = self.computeActionsComparisonCorrelations()
        self.exportPrincipalImage(plotFileName=plotFileName,
                                  pictureFormat=pictureFormat,
                                  bgcolor=bgcolor,
                                  Comments=Comments)
        self.relation = relationOrig
        
    def _export3DplotOfActionsCorrelation(self,plotFileName="actionsCorrelati",
                                         Type="pdf",graphType='pdf',
                                         pictureFormat=None,bgcolor='cornsilk',
                                         Comments=False,bipolarFlag=False,
                                         _dist=True,_centeredFlag=False):
        """
        use Calmat and R for producing a png plot of the principal components of
        the the actions ordinal correlation table. 

        See export3DplotCriteriaCorrelation()
        """
        import time
        #from tempfile import TemporaryDirectory
        #with TemporaryDirectory(dir=tempDir) as tempDirName:
        if pictureFormat is not None:
            Type = pictureFormat
        else:
            Type = graphType
        if Comments:
            print('*----  export 3dplot of type %s -----' % (graphType))
        import os
        actionsList = [x for x in self.actions]
        actionsList.sort()
        n = len(actionsList)
        fo = open('actionsLabels.prn','w')
        for key in actionsList:
            fo.write('%s ' % (key))
        fo.close()
        self.saveActionsCorrelationTable(
            fileName='tempcorr.prn',Silent=True,
            Bipolar=bipolarFlag,Centered=_centeredFlag)
        # create Calmat script and calmat execution
        # (the prn extension is standard)
        try:
            if Comments:
                if _dist:
                    cmd = 'env defdist.sh tempcorr '+str(n)+' '+str(n)
                else:
                    cmd = 'env defdista.sh tempcorr '+str(n)+' '+str(n) 
            else:
                if _dist:
                    cmd = 'env defdist.sh tempcorr '+str(n)+' '+str(n)+' > /dev/null'
                else:
                    cmd = 'env defdista.sh tempcorr '+str(n)+' '+str(n)+' > /dev/null'
            os.system(cmd)
            if Comments:
                os.system('env calmat tempcorr.prg')
            else:
                os.system('env calmat tempcorr.prg > /dev/null')
        except:
            print('Error: You need to install calmat !!!')
            return
        # create R 3d scatter plot script
        if Type == "interactive":
            fo = open('scatter.r','w')
            fo.write('# 3d scatter plot RB April 2008\n')
            fo.write('test.mat <- matrix(scan("compolg.prn"),ncol=%d,byrow=T)\n' % (n))
##             fo.write('choose<-c(%d,%d,%d)\n' % (1,2,3))
            fo.write('choose<-c(%d,%d,%d)\n' % (n,n-1,n-2))
            fo.write('test.labels <- scan("actionsLabels.prn",what="character")\n') 
            fo.write('valprop <- matrix(scan("val_prlg.prn"),ncol=2,byrow=T)\n') 
            fo.write('require(rgl)\n')
            fo.write('open3d()\n')
            fo.write('points3d(test.mat[,choose])\n')
            fo.write('text3d(test.mat[,choose],text=test.labels,col="red3")\n')
            fo.write('axes3d(edges=c("x","y","z"),pos=c(0,0,0),labels=F,ticks=F)\n')
            fo.write('axes3d(edges=c("x","y","z"))\n')
            fo.write('title3d(main="Actions Ordinal Correlation",xlab=valprop[choose,2][1],ylab=valprop[choose,2][2],zlab=valprop[choose,2][3],col="blue",line=4)\n')
            fo.write('rgl.viewpoint(1,1/4,interactive=T)\n')
            fo.write('rgl.snapshot("%s.png")\n' % (plotFileName+'.png') )
            fo.close()
        else:
            fo = open('scatter.r','w')
            fo.write('# scatter plot RB April 2008\n')
            fo.write('test.mat <- matrix(scan("compolg.prn"),ncol=%d,byrow=T)\n' % (n))
            fo.write('lim1 <- max(test.mat)\n')
            fo.write('lim2 <- min(test.mat)\n')
            if _centeredFlag:
                fo.write('choose12<-c(%d,%d)\n' % (1,2))
                fo.write('choose23<-c(%d,%d)\n' % (2,3))
                fo.write('choose13<-c(%d,%d)\n' % (1,3))
                fo.write('choose21<-c(%d,%d)\n' % (2,1))
            else:
                fo.write('choose12<-c(%d,%d)\n' % (n,n-1))
                fo.write('choose23<-c(%d,%d)\n' % (n-1,n-2))
                fo.write('choose13<-c(%d,%d)\n' % (n,n-2))
                fo.write('choose21<-c(%d,%d)\n' % (n-1,n))
            fo.write('test.labels <- scan("actionsLabels.prn",what="character")\n') 
            fo.write('valprop <- matrix(scan("val_prlg.prn"),ncol=2,byrow=T)\n')
            if Type == "png":
                fo.write('png("%s.png",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
            elif Type == "jpeg":
                fo.write('jpeg("%s.jpg",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
            elif Type == "xfig":
                fo.write('xfig("%s.fig",width=480,height=480,bg="cornsilk")\n' % (plotFileName) )
            elif Type == "pdf":
                if bgcolor is not None:
                    fo.write('pdf("%s.pdf",width=6,height=6,bg="%s",title="PCA of Actions Correlation Index")\n' % (plotFileName,bgcolor) )
                else:
                    fo.write('pdf("%s.pdf",width=6,height=6,title="PCA of Actions Correlation Index")\n' % (plotFileName) )                    
            else:
                print('Error: Plotting device %s not defined !' % (Type))
                return     
            fo.write('par(mfrow=c(2,2))\n')
            fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
            fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
            fo.write('title(sub=paste("total inertia:",(valprop[choose12,2][1]+valprop[choose12,2][2])*100,"%"),main="factors 1 and 2",col="blue")\n')
            fo.write('text(test.mat[,choose12],labels=test.labels,col="red3",cex=1.0)\n')
##             fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
            fo.write('plot(test.mat[,choose12],xlab=paste("axis 2:",valprop[choose23,2][1]*100,"%"),ylab=paste("axis 3:",valprop[choose23,2][2]*100,"%"),type="n",asp=1)\n')
            fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
            fo.write('title(sub=paste("total inertia:",(valprop[choose23,2][1]+valprop[choose23,2][2])*100,"%"),main="factors 2 and 3",col="blue")\n')
            fo.write('text(test.mat[,choose23],labels=test.labels,col="red3",cex=1.0)\n')
##             fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose12,2][1]*100,"%"),ylab=paste("axis 2:",valprop[choose12,2][2]*100,"%"),type="n",asp=1)\n')
            fo.write('plot(test.mat[,choose12],xlab=paste("axis 1:",valprop[choose13,2][1]*100,"%"),ylab=paste("axis 3:",valprop[choose13,2][2]*100,"%"),type="n",asp=1)\n')
            fo.write('abline(h=0,v=0,col="grey",lty="dotted")\n')            
            fo.write('title(sub=paste("total inertia:",(valprop[choose13,2][1]+valprop[choose13,2][2])*100,"%"),main="factors 1 and 3",col="blue")\n')
            fo.write('text(test.mat[,choose13],labels=test.labels,col="red3",cex=1.0)\n')
            if _centeredFlag:
                fo.write('barplot(valprop[1:nrow(valprop)-1,2]*100,names.arg=c(1:%d),main="Axis inertia (in %%)",col="orangered")\n' % (n-1))
            else:
                fo.write('barplot(valprop[nrow(valprop):2,2]*100,names.arg=c(1:%d),main="Axis inertia (in %%)",col="orangered")\n' % (n-1))     
            fo.write('dev.off()\n')           
            fo.close()
            
        try:
            ## if Comments:
            ##     os.system('/usr/bin/R -q --vanilla --verbose < scatter.r 2>&1')
            ## else:
            ##     os.system('/usr/bin/R -q --vanilla < scatter.r > /dev/null 2> /dev/null')
            if Comments:
                os.system('env R -q --vanilla --verbose < scatter.r 2>&1')
            else:
                os.system('env R -q --vanilla < scatter.r > /dev/null 2> /dev/null')
            time.sleep(3)     
            if Comments:
                print('See %s.%s ! ' % (plotFileName,Type))
        except:
            print('Error: You need to install R !!!')
            
    def computePairwiseComparisons(self,hasSymmetricThresholds=True):
        """
        renders pairwise comparison parameters for all pairs of actions
        """
        evaluation = self.evaluation
        NA = self.NA
        criteria = self.criteria
        actionsList = [x for x in self.actions]
        
        pairwiseComparisons = {}
        for x in actionsList:
            pairwiseComparisons[x] = {}
            for y in actionsList:
                pairwiseComparisons[x][y] = {'lt':0, 'leq':0, 'eq':0, 'geq':0, 'gt':0}
        for a in actionsList:
            for b in actionsList:
                for c in criteria:
                    if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                        try:
                            indx = criteria[c]['thresholds']['ind'][0]
                            indy = criteria[c]['thresholds']['ind'][1]
                            if hasSymmetricThresholds:
                                ind = indx + indy *\
                                    max(abs(evaluation[c][a]),
                                        abs(evaluation[c][b]))
                            else:
                                ind = indx + indy * abs(evaluation[c][a])
                        except:
                            ind = Decimal('0')
                        try:
                            wpx = criteria[c]['thresholds']['weakPreference'][0]
                            wpy = criteria[c]['thresholds']['weakPreference'][1]
                            if hasSymmetricThresholds:
                                wp = wpx + wpy *\
                                    max(abs(evaluation[c][a]),
                                        abs(evaluation[c][b]))
                            else:
                                wp = wpx + wpy * abs(evaluation[c][a])                           
                        except:
                            wp = ind + Decimal("0.00000000000001")
                        try:
                            px = criteria[c]['thresholds']['pref'][0]
                            py = criteria[c]['thresholds']['pref'][1]
                            if hasSymmetricThresholds:
                                p = px + py * max(abs(evaluation[c][a]),
                                                  abs(evaluation[c][b]))
                            else:
                                p = px + py * abs(evaluation[c][a])
                        except:
                            p = wp
                        if criteria[c]['weight'] > Decimal('0.0'):
                            d = evaluation[c][a] - evaluation[c][b]
                        else:
                            d = evaluation[c][b] - evaluation[c][a]
                        if evaluation[c][a] - p >= evaluation[c][b]:
                            pairwiseComparisons[a][b]['gt'] += abs(criteria[c]['weight'])
                        elif evaluation[c][a] - wp >= evaluation[c][b]:
                            pairwiseComparisons[a][b]['geq'] += abs(criteria[c]['weight'])
                        elif evaluation[c][a] + ind >= evaluation[c][b]:
                            pairwiseComparisons[a][b]['eq'] += abs(criteria[c]['weight'])
                        elif evaluation[c][a] + p > evaluation[c][b]:
                            pairwiseComparisons[a][b]['leq'] += abs(criteria[c]['weight'])
                        elif evaluation[c][a] + p <= evaluation[c][b]:
                            pairwiseComparisons[a][b]['lt'] += abs(criteria[c]['weight'])
                        else:
                            print("Error: a,b,c,d,ind,wp,p",a,b,c,d,ind,wp,p)
                        
        return pairwiseComparisons

    def showPairwiseComparisonsDistributions(self):
        """
        Renders the lt,leq, eq, geq, gt distributions for all pairs
        """
        a = [x for x in self.actions]
        a.sort()
        pc = self.computePairwiseComparisons()
        print(' distribution of pairwise comparisons')
        print(' a  b | "<" "<=" "==" ">=" ">" | "S"')
        print('-----------------------------')
        for i in range(len(a)):
            for j in range(i+1,len(a)):
                print(' %s  %s | %.2f %.2f %.2f %.2f %.2f | %.2f' % (
                    a[i],a[j],pc[a[i]][a[j]]['lt'],
                    pc[a[i]][a[j]]['leq'],pc[a[i]][a[j]]['eq'],
                    pc[a[i]][a[j]]['geq'],pc[a[i]][a[j]]['gt'],
                    self.relation[a[i]][a[j]]))
                print(' %s  %s | %.2f %.2f %.2f %.2f %.2f | %.2f' % (
                    a[j],a[i],pc[a[j]][a[i]]['lt'],
                    pc[a[j]][a[i]]['leq'],pc[a[j]][a[i]]['eq'],
                    pc[a[j]][a[i]]['geq'],pc[a[j]][a[i]]['gt'],
                    self.relation[a[j]][a[i]]))

    def showOldPairwiseComparison(self,a,b,
                               Debug=False,isReturningHTML=False,
                               hasSymmetricThresholds=True):
        """
        Obsolete: Renders the pairwise comprison parameters on all criteria
        with weak preference and weak veto thresholds.
        """
        evaluation = self.evaluation
        NA = self.NA
        criteria = self.criteria
        if Debug:
            print('a,b =', a, b)
        if a != b:
            if isReturningHTML:
                html  = '<h1>Pairwise Comparison</h1>'
                html += '<h2>Comparing actions : (%s,%s)</h2>' % (a,b)
                html += '<table style="background-color:White" border="1">'
                html += '<tr bgcolor="#9acd32">'
                html += '<th>crit.</th><th>wght.</th> <th>g(x)</th> <th>g(y)</th> <th>diff</th> <th>ind</th> <th>wp</th> <th>p</th> <th>concord</th> <th>wv</th> <th>v</th> <th>polarisation</th>'
                html += '</tr>'
            else:
                print('*------------  pairwise comparison ----*')
                print('Comparing actions : (%s, %s)' % (a,b))
                print('crit. wght.  g(x)  g(y)    diff  \t| ind     wp      p    concord \t|  wv   v   weak veto veto')
                print('-------------------------------  \t ----------------------------- \t ----------------')                
            concordance = 0
            sumWeights = 0
            criteriaList = [x for x in criteria]
            criteriaList.sort()
            for c in criteriaList:
                sumWeights += abs(criteria[c]['weight'])
                if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                    try:
                        indx = criteria[c]['thresholds']['ind'][0]
                        indy = criteria[c]['thresholds']['ind'][1]
                        if hasSymmetricThresholds:
                            ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            ind = indx +indy * abs(evaluation[c][a])
                    except:
                        ind = None
                    try:
                        wpx = criteria[c]['thresholds']['weakPreference'][0]
                        wpy = criteria[c]['thresholds']['weakPreference'][1]
                        if hasSymmetricThresholds:
                            wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            wp = wpx + wpy * abs(evaluation[c][a])
                    except:
                        wp = None
                    try:
                        px = criteria[c]['thresholds']['pref'][0]
                        py = criteria[c]['thresholds']['pref'][1]
                        if hasSymmetricThresholds:
                            p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            p = px + py * abs(evaluation[c][a])
                    except:
                        p = None
                    if self.criteria[c]['weight'] > Decimal('0.0'):
                        d = evaluation[c][a] - evaluation[c][b]
                    else:
                        d = evaluation[c][b] - evaluation[c][a]
                    lc0 = self._localConcordance(d,ind,wp,p)
                    if ind is not None:
                        ind = round(ind,2)
                    if wp is not None:
                        wp = round(wp,2)
                    if p is not None:
                        p = round(p,2)
                    if isReturningHTML:
                        html += '<tr>'
                        html += '<td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td> <td>%2.2f</td> <td>%2.2f</td> <td>%+2.2f</td> <td>%s</td>  <td>%s</td>  <td>%s</td>   <td>%+.2f</td>' % (c,criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*abs(criteria[c]['weight']))
                    else:
                         print(c, '  %.2f  %2.2f  %2.2f  %+2.2f \t| %s  %s  %s   %+.2f \t|' % (criteria[c]['weight'],evaluation[c][a],evaluation[c][b],d, str(ind),str(wp),str(p),lc0*abs(criteria[c]['weight'])), end=' ')
                    concordance = concordance + (lc0 * abs(criteria[c]['weight']))
                    try:
                        wvx = criteria[c]['thresholds']['weakVeto'][0]
                        wvy = criteria[c]['thresholds']['weakVeto'][1]
                        if hasSymmetricThresholds:
                            wv = wvx + wvy * max(abs(evaluation[c][a]),
                                                 abs(evaluation[c][b]))
                        else:
                            wv = wvx + wvy * abs(evaluation[c][a])
                    except:
                        wv = None
                    try:
                        vx = criteria[c]['thresholds']['veto'][0]
                        vy = criteria[c]['thresholds']['veto'][1]
                        if hasSymmetricThresholds:
                            v = vx + vy * max(abs(evaluation[c][a]),
                                              abs(evaluation[c][b]))
                        else:
                            v = vx + vy * abs(evaluation[c][a])
                    except:
                        v = None
                    veto = self._localVeto(d,wv,v)
                    try:
                        negativeVeto = self._localNegativeVeto(d,wv,v)
                        hasBipolarVeto = True
                    except:
                        hasBipolarVeto = False
                    if hasBipolarVeto:
                        if v is not None:
                            if d >= v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, negativeVeto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ddffdd">%+2.2f</td>' % (v, negativeVeto)
                            elif d <= -v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, -veto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                            else:
                                if not isReturningHTML:                                
                                    print()
                                else:
                                    html += '</tr>'
                        elif wv is not None:
                            if d >= wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, negativeVeto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ddffdd">%+2.2f</td>' % (wv, negativeVeto)
                            elif d <= -wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, -veto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if not isReturningHTML:
                                    print()
                                else:
                                    html += '</tr>'
                        else:
                            if not isReturningHTML:
                                print()
                            else:
                                html += '</tr>'
                    else:
                        ## unipolar case  Electre III for instance
                        if veto > Decimal("-1.0"):
                            if wv is not None:
                                if v is not None:
                                    if not isReturningHTML:
                                        print(' %2.2f %2.2f %+2.2f' % (wv, v, veto))
                                    else:
                                        html += '<td>%2.2f</td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, v, veto)
                                else:
                                    if not isReturningHTML:
                                        print(' %2.2f       %+2.2f' % (wv, -veto))
                                    else:
                                        html += '<td>%2.2f</td> <td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if v is not None:
                                    if not isReturningHTML:
                                        print('       %2.2f %+2.2f' % (v, veto))
                                    else:
                                        html += '<td></td> <td>%2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                                else:
                                    if not isReturningHTML:
                                        print()
                                    else:
                                        html += '</tr>'
                        
                else:
                    if evaluation[c][a] == NA:
                        eval_c_a = 'NA'
                    else:
                        eval_c_a = '%2.2f' % evaluation[c][a]
                    if evaluation[c][b] == NA:
                        eval_c_b = 'NA'
                    else:
                        eval_c_b = '%2.2f' % evaluation[c][b]
                    
                    if not isReturningHTML:
                        print(c,'    %s %s' % (eval_c_a,eval_c_b))
                    else:
                        html += '<tr><td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td><td>%s</td><td>%s</td><td></td><td></td><td></td><td></td><td>%.2f</td></tr>' %\
                                (c, criteria[c]['weight'],eval_c_a,eval_c_b, self.valuationdomain['med']*criteria[c]['weight'])
            if not isReturningHTML:
                print('             ----------------------------------------')
                print(' Valuation in range: %+.2f to %+.2f; global concordance: %+.2f' % (-sumWeights,sumWeights,concordance))
            else:
                html += '</tr></table>'
                html += '<b>Valuation in range: %+.2f to %+.2f; global concordance: %+.2f </b>' % (-sumWeights,sumWeights,concordance)
        if isReturningHTML:
            return html

    def showPairwiseComparison(self,a,b,
                               Debug=False,isReturningHTML=False,
                               hasSymmetricThresholds=True):
        """
        Renders the pairwise comprison parameters on all criteria
        in html format
        """
        evaluation = self.evaluation
        NA = self.NA
        criteria = self.criteria
        if Debug:
            print('a,b =', a, b)
        if a != b:
            if isReturningHTML:
                html  = '<h1>Pairwise Comparison</h1>'
                html += '<h2>Comparing actions : (%s,%s)</h2>' % (a,b)
                html += '<table style="background-color:White" border="1">'
                html += '<tr bgcolor="#9acd32">'
                html += '<th>crit.</th><th>wght.</th> <th>g(x)</th> <th>g(y)</th> <th>diff</th> <th>ind</th> <th>pref</th> <th>concord</th> <th>v</th> <th>polarisation</th>'
                html += '</tr>'
            else:
                print('*------------  pairwise comparison ----*')
                print('Comparing actions : (%s, %s)' % (a,b))
                print('crit. wght.  g(x)  g(y)    diff  \t| ind   pref    r() \t|   v  veto')
                print('-------------------------------  \t ----------------------------- \t ----------------')                
            concordance = 0
            sumWeights = 0
            criteriaList = [x for x in criteria]
            criteriaList.sort()
            for c in criteriaList:
                sumWeights += abs(criteria[c]['weight'])
                if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                    try:
                        indx = criteria[c]['thresholds']['ind'][0]
                        indy = criteria[c]['thresholds']['ind'][1]
                        if hasSymmetricThresholds:
                            ind = indx +indy * max(abs(evaluation[c][a]),
                                                   abs(evaluation[c][b]))
                        else:
                            ind = indx +indy * abs(evaluation[c][a])
                    except:
                        ind = None
                    wp = None
                    try:
                        px = criteria[c]['thresholds']['pref'][0]
                        py = criteria[c]['thresholds']['pref'][1]
                        if hasSymmetricThresholds:
                            p = px + py * max(abs(evaluation[c][a]),
                                              abs(evaluation[c][b]))
                        else:
                            p = px + py * abs(evaluation[c][a])
                    except:
                        p = None
                    if self.criteria[c]['weight'] > Decimal('0.0'):
                        d = evaluation[c][a] - evaluation[c][b]
                    else:
                        d = evaluation[c][b] - evaluation[c][a]
                    lc0 = self._localConcordance(d,ind,wp,p)
                    if ind is not None:
                        ind = round(ind,2)
                    if wp is not None:
                        wp = round(wp,2)
                    if p is not None:
                        p = round(p,2)
                    if isReturningHTML:
                        html += '<tr>'
                        html += '<td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td> <td>%2.2f</td> <td>%+2.2f</td> <td>%s</td>  <td>%s</td>  <td>%s</td>   <td>%+.2f</td>' %\
                                (c,criteria[c]['weight'],evaluation[c][a],
                                 evaluation[c][b],d, str(ind),str(p),
                                 lc0*abs(criteria[c]['weight']))
                    else:
                         print(c, '  %.2f  %2.2f  %2.2f  %+2.2f \t| %s  %s   %+.2f \t|' %\
                               (criteria[c]['weight'],evaluation[c][a],
                                evaluation[c][b],d, str(ind),str(p),
                                lc0*abs(criteria[c]['weight'])), end=' ')
                    concordance = concordance + (lc0 * abs(criteria[c]['weight']))
                    wv = None
                    try:
                        vx = criteria[c]['thresholds']['veto'][0]
                        vy = criteria[c]['thresholds']['veto'][1]
                        if hasSymmetricThresholds:
                            v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                        else:
                            v = vx + vy * abs(evaluation[c][a])
                    except:
                        v = None
                    veto = self._localVeto(d,wv,v)
                    try:
                        negativeVeto = self._localNegativeVeto(d,wv,v)
                        hasBipolarVeto = True
                    except:
                        hasBipolarVeto = False
                    if hasBipolarVeto:
                        if v is not None:
                            if d >= v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, negativeVeto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ddffdd">%+2.2f</td>' % (v, negativeVeto)
                            elif d <= -v:
                                if not isReturningHTML:
                                    print('     %2.2f       %+2.2f' % (v, -veto))
                                else:
                                    html += '<td></td> <td> %2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                            else:
                                if not isReturningHTML:                                
                                    print()
                                else:
                                    html += '</tr>'
                        elif wv is not None:
                            if d >= wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, negativeVeto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ddffdd">%+2.2f</td>' % (wv, negativeVeto)
                            elif d <= -wv:
                                if not isReturningHTML:
                                    print('%2.2f      %+2.2f' % (wv, -veto))
                                else:
                                    html += '<td>%2.2f</td><td></td> <td bgcolor="#ffddff">%+2.2f</td>' % (wv, -veto)
                            else:
                                if not isReturningHTML:
                                    print()
                                else:
                                    html += '</tr>'
                        else:
                            if not isReturningHTML:
                                print()
                            else:
                                html += '</tr>'
                    else:
                        ## unipolar case  Electre III for instance
                        if veto > Decimal("-1.0"):
                            if v is not None:
                                if not isReturningHTML:
                                    print('       %2.2f %+2.2f' % (v, veto))
                                else:
                                    html += '<td></td> <td>%2.2f</td> <td bgcolor="#ffddff">%+2.2f</td>' % (v, -veto)
                            else:
                                if not isReturningHTML:
                                    print()
                                else:
                                    html += '</tr>'
                        
                else:
                    if evaluation[c][a] == NA:
                        eval_c_a = 'NA'
                    else:
                        eval_c_a = '%2.2f' % evaluation[c][a]
                    if evaluation[c][b] == NA:
                        eval_c_b = 'NA'
                    else:
                        eval_c_b = '%2.2f' % evaluation[c][b]
                    
                    if not isReturningHTML:
                        print(c,'    %s %s' % (eval_c_a,eval_c_b))
                    else:
                        html += '<tr><td bgcolor="#FFEEAA" align="center">%s</td> <td>%.2f</td><td>%s</td><td>%s</td><td></td><td></td><td></td><td></td><td>%.2f</td></tr>' %\
                                (c, criteria[c]['weight'],eval_c_a,eval_c_b,
                                 self.valuationdomain['med']*criteria[c]['weight'])
            if not isReturningHTML:
                print('             ----------------------------------------')
                print(' Valuation in range: %+.2f to %+.2f; global concordance: %+.2f' %\
                      (-sumWeights,sumWeights,concordance))
            else:
                html += '</tr></table>'
                html += '<b>Valuation in range: %+.2f to %+.2f; global concordance: %+.2f </b>' %\
                    (-sumWeights,sumWeights,concordance)
        if isReturningHTML:
            return html

    def showHTMLPairwiseComparison(self,a,b,htmlFileName=None):
        """
        Exporting the pairwise comparison table of actions a and b in the default system browser. A specific file name may be provided.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        # if fileName is None:
        #     fileName = 'pairwiseComparison_%s_%s.html' % (a,b)
        fo = open(fileName,'w')
        fo.write(self.showPairwiseComparison(a,b,isReturningHTML=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)

    def showPairwiseOutrankings(self,a,b,
                               Debug=False,isReturningHTML=False,
                               hasSymmetricThresholds=True):
        """
        Renders the pairwise outrankings table for actions *a* and *b*.
        """
        self.showPairwiseComparison(a,b,\
                               Debug=Debug,isReturningHTML=isReturningHTML,\
                               hasSymmetricThresholds=hasSymmetricThresholds)
        self.showPairwiseComparison(b,a,\
                               Debug=Debug,isReturningHTML=isReturningHTML,\
                               hasSymmetricThresholds=hasSymmetricThresholds)

    def showHTMLPairwiseOutrankings(self,a,b,htmlFileName=None):
        """
        Exporting the pairwise outrankings table of actions a and b
        in the default system browser. A specific file name may be provided.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self.showPairwiseComparison(a,b,isReturningHTML=True))
        fo.write(self.showPairwiseComparison(b,a,isReturningHTML=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)

    def showShort(self):
        """
        specialize the general showShort method with the criteria.
        """
        Digraph.showShort(self)
        self.showCriteria()
        self.showPerformanceTableau()

    def showAll(self):
        """
        specialize the general showAll method with criteria
        and performance tableau output
        """
        print('*----- show detail -------------*')
        print('Digraph          :', self.name)
        print('*---- Actions ----*')
        print(self.actions)
        self.showCriteria()
        self.showPerformanceTableau()
        print('*---- Valuation domain ----*')
        print(self.valuationdomain)
        self.showRelationTable()
        self.showComponents()
        self.showPreKernels()


    def showRelationTable(self,IntegerValues=False,
                          actionsSubset= None,
                          rankingRule=None,
                          Sorted=False,
                          hasLPDDenotation=False,
                          OddsDenotation=False,
                          StabilityDenotation=False,
                          hasLatexFormat=False,
                          hasIntegerValuation=False,
                          relation=None,
                          ReflexiveTerms=True,
                          fromIndex=None,
                          toIndex=None):
        """
        Prints the relation valuation in actions X actions table format.
        Copeland and NetFlows ranking rule may be applied.
        """
        if hasLPDDenotation:
            try:
                largePerformanceDifferencesCount = self.largePerformanceDifferencesCount
            except:
                hasLPDDenotation = False
        if OddsDenotation:
            try:
                oddsMatrix = self.computePairwiseOddsMatrix()
            except:
                OddsDenotation = False
        if StabilityDenotation:
            try:
                stability = self.stability
            except AttributeError:
                robustg = RobustOutrankingDigraph(self)
                stability = robustg.stability
            #except:
            #    hasStabilityDenotation = False
            
##        if actionsSubset is None:
##            actions = self.actions
##        else:
##            actions = actionsSubset
        if actionsSubset is None:
            if rankingRule is None:
                actions = self.actions
            else:
                if rankingRule == 'Copeland':
                    computeRanking = self.computeCopelandRanking
                elif rankingRule == 'NetFlows':
                    computeRanking = self.computeNetFlowsRanking
                actions = computeRanking()
                Sorted = False
        else:
            actions = actionsSubset

        if relation is None:
            if hasLPDDenotation:
                relation = self.relation
            else:
                relation = self.relation
            
        print('* ---- Relation Table -----\n', end=' ')
        if OddsDenotation:
            print('r/(pro:con)| ', end=' ')
        elif StabilityDenotation:
            print('r/(stab)| ', end=' ')
        elif hasLPDDenotation:
            print('r/(lh)| ', end=' ')
        else:
            print('  r   | ', end=' ')
        actions = [x for x in actions]
        if fromIndex is None:
            fromIndex = 0
        if toIndex is None:
            toIndex = len(actions)
        actionsList = []
        for x in actions[fromIndex:toIndex]:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
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
            print("'"+x[0]+"'  ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in actionsList:
            if hasLatexFormat:
                print("$"+x[0]+"$ & ", end=' ')
            else:
                print("'"+x[0]+"' |  ", end=' ')
            for y in actionsList:
                if x == y:
                    if not ReflexiveTerms:
                        if hasLPDDenotation:
                            print('   -   ', end=' ')
                        elif hasLatexFormat:
                            print('$\\;-\\;$ &', end=' ')
                        else:
                            print('  -  ', end=' ')
                    else:
                        Max = self.valuationdomain['max']
                        if hasLPDDenotation:
                            print(' %+.2f ' % Max, end=' ')
                        elif hasLatexFormat:
                            print('$%.2f$ &' % Max, end=' ')
                        else:
                            print(' %+.2f ' % Max, end=' ')
                else:    
                    if hasIntegerValuation:
                        if hasLPDDenotation:
                            print('%+d ' % (relation[x[1]][y[1]]), end=' ')
                        elif hasLatexFormat:
                            print('$%+d$ &' % (relation[x[1]][y[1]]), end=' ')
                        else:
                            print('%+d ' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        if hasLPDDenotation:
                            print('%+2.2f ' % (relation[x[1]][y[1]]), end=' ')
                        elif hasLatexFormat:
                            print('$%+2.2f$ & ' % (relation[x[1]][y[1]]), end=' ')       
                        else:
                            print('%+2.2f ' % (relation[x[1]][y[1]]), end=' ')
                
            if hasLatexFormat:
                print(' \\cr')
            else:
                print()
            if hasLPDDenotation:
                print("       | ", end=' ')
                for y in actionsList:
                    print('(%+d,%+d)' % (largePerformanceDifferencesCount[x[1]][y[1]]['positive'],
                                         largePerformanceDifferencesCount[x[1]][y[1]]['negative']),
                          end=' ')
                print()
            elif OddsDenotation:
                print("       | ", end=' ')
                for y in actionsList:
                    print('(%.0f:%.0f)' % (oddsMatrix[x[1]][y[1]][0],oddsMatrix[x[1]][y[1]][1]), end='  ')
                print()
            elif StabilityDenotation:
                print("     | ", end=' ')
                for y in actionsList:
                    if x == y and StabilityDenotation:
                        print(' (+4) ', end=' ')
                    else:
                        print(' (%+d) ' % stability[x[1]][y[1]], end=' ')
                print('')
        print('Valuation domain: [%.3f; %.3f]' %\
                  (self.valuationdomain['min'],self.valuationdomain['max']) )
        if rankingRule is not None:
            print('RankingRule = %s' % rankingRule)
        
        if StabilityDenotation:
            print('Stability denotation semantics:')
            print(' +4|-4 : unanimous outranking | outranked situation;')
            print(' +3|-3 : validated outranking | outranked situation')
            print('         in each coalition of equisignificant criteria;')
            print(' +2|-2 : outranking | outranked situation validated')
            print('         with all potential significance weights that are')
            print('         compatible with the given significance preorder;')
            print(' +1|-1 : validated outranking | outranked situation with')
            print('         the given significance weights;')
            print('   0   : indeterminate relational situation.')
            print()
            
    def showPerformanceTableau(self,actionsSubset=None):
        """
        Print the performance Tableau.
        """
        evaluation = self.evaluation
        NA = self.NA
        print('*----  performance tableau -----*')
        criteriaList = list(self.criteria)
        criteriaList.sort()
        if actionsSubset is None:
            actionsList = list(self.actions)
            #actionsList.sort()
        else:
            actionsList = list(actionsSubset)
        print('criteria | ', end=' ')
        for x in actionsList:
            print('\''+str(x)+'\'  ', end=' ')
        print('\n---------|-----------------------------------------')
        for g in criteriaList:
            print('   \''+str(g)+'\'  |', end=' ')
            for x in actionsList:
                if evaluation[g][x] != NA:
                    print('% .1f, ' % (evaluation[g][x]), end=' ')
                else:
                    print(' NA, ', end=' ')
            print()      

    def computeVetosShort(self):
        """
        renders the number of vetoes and real vetoes in an OutrankingDigraph.
        """
        Med = self.valuationdomain['med']
        nv = len(self.vetos)
        realveto = 0
        for i in range(nv):
            if self.vetos[i][0][2] > Med:
                realveto += 1
        return nv,realveto

    def computeVetoesStatistics(self,level=None):
        """
        renders the cut level vetos in dictionary format:
        vetos = {'all': n0, 'strong: n1, 'weak':n2}.
        """
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        if level is None:
            level = Med
        else:
            level = Decimal(str(level))
        negLevel = Max - level + Min
        nv = len(self.vetos)
        weakVeto = 0
        strongVeto = 0
        for i in range(nv):
            if self.vetos[i][0][2] > level:
                strongVeto += 1
            elif self.vetos[i][0][2] > negLevel:
                weakVeto += 1
        vetos = {}
        vetos['all'] = nv
        vetos['strong'] = strongVeto
        vetos['weak'] = weakVeto
        return vetos

    def showConsiderablePerformancesPolarisation(self):
        """
        prints all considerable performance polarisations.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        vet = self.vetos
        negVet = self.negativeVetos
        vp =  [(x[0][0],x[0][1]) for x in vet]
        nvp = [(x[0][0],x[0][1]) for x in negVet]
        #print(vp)
        #print(nvp)
        nv = len(vp)
        nnv = len(nvp)
        i = 0
        j = 0
        while i < nv or j < nnv:
            if i < nv and j < nnv:
                if vp[i] == nvp[j]:
                    print('*----- Consirable contradictory performance difference! ------*')
                    print('r(%s >= %s) = %.2f' %\
                        (vet[i][0][0],vet[i][0][1],vet[i][0][2]) )
                    for lpd in vet[i][1]:
                        print('criterion: ' + str(lpd[0]))
                        print('Considerable negative performance difference : %.2f' % lpd[1][1] )
                        print('Veto discrimination threshold       : %.2f' % -lpd[1][3] )
                    for lpd in negVet[j][1]:
                        print('criteria: ' + str(lpd[0]))
                        print('Considerable positive performance difference : %.2f' % lpd[1][1] )
                        print('Counter-veto threshold              : %.2f' % lpd[1][3] )            
                    print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                          (vet[i][0][0],vet[i][0][1],vet[i][0][2],Med) )                    
                    i += 1; j +=1
                elif vp[i] < nvp[j]:
                    print('*------ Considerable negative performance difference -----"')
                    print('r(%s >= %s) = %.2f' %\
                            (vet[i][0][0],vet[i][0][1],vet[i][0][2]) )
                    for lpd in vet[i][1]:
                        print('criterion: ' + str(lpd[0]))
                        print('Considerable negative performance difference : %.2f' % lpd[1][1] )
                        print('Veto discrimination threshold       : %.2f' % -lpd[1][3] )
                    if vet[i][0][2] > Med:
                        print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                          (vet[i][0][0],vet[i][0][1],vet[i][0][2],Med) )
                    else:
                        print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                          (vet[i][0][0],vet[i][0][1],vet[i][0][2],Min) )
                    i += 1
                else:
                    print('*------ Considerable positive performance difference -----"')
                    print('r(%s >= %s) = %.2f' %\
                            (negVet[j][0][0],negVet[j][0][1],negVet[i][0][2]) )
                    for lpd in negVet[j][1]:
                        print('criteria: ' + str(lpd[0]))
                        print('Considerable positive performance difference : %.2f' % lpd[1][1] )
                        print('Counter-veto threshold              : %.2f' % lpd[1][3] )            
                    if negVet[j][0][2] < Med:
                        print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                          (negVet[j][0][0],negVet[j][0][1],negVet[j][0][2],Med) )
                    else:
                        print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                          (negVet[j][0][0],negVet[j][0][1],negVet[j][0][2],Max) )
                    j += 1
            else:
                break
        while i < nv:
            print('*------ Considerable negative performance difference -----"')
            print('r(%s >= %s) = %.2f' %\
                    (vet[i][0][0],vet[i][0][1],vet[i][0][2]) )
            for lpd in vet[i][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable negative performance difference : %.2f' % lpd[1][1] )
                print('Veto discrimination threshold       : %.2f' % -lpd[1][3] )
            if vet[i][0][2] > Med:
                print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                  (vet[i][0][0],vet[i][0][1],vet[i][0][2],Med) )
            else:
                print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                  (vet[i][0][0],vet[i][0][1],vet[i][0][2],Min) )
            i +=1
        while j < nnv:
            print('*------ Considerable positive performance difference -----"')
            print('r(%s >= %s) = %.2f' %\
                    (negVet[j][0][0],negVet[j][0][1],negVet[j][0][2]) )
            for lpd in negVet[j][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable positive performance difference : %.2f' % lpd[1][1] )
                print('Counter-veto threshold              : %.2f' % lpd[1][3] )            
            if negVet[j][0][2] < Med:
                print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                  (negVet[j][0][0],negVet[j][0][1],negVet[j][0][2],Med) )
            else:
                print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                  (negVet[j][0][0],negVet[j][0][1],negVet[j][0][2],Max) )
            j += 1

    def showPolarisations(self,cutLevel=None,realVetosOnly = False):       
        """
        prints all negative and positive polarised situations observed in the OutrankingDigraph instance.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        try:
            lpdCount = self.largePerformanceDifferencesCount
        except:
            print('No large performance differences count has been stored')
            return
        try:
            vetos = self.vetos
        except:
            vetos = []
        print('*----  Negative polarisations ----*')
        #nv, realveto = self.computeVetosShort()
        #vetos.sort()
        nv = len(vetos)
        print('number of negative polarisations : %d ' % (nv))
        for i in range(nv):
            print('%d: r(%s >= %s) = %.2f' %\
                (i+1,vetos[i][0][0],vetos[i][0][1],vetos[i][0][2]) )
            for lpd in vetos[i][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable performance difference : %.2f' % lpd[1][1] )
                print('Veto discrimination threshold       : %.2f' % -lpd[1][3] )
            if lpdCount[vetos[i][0][0]][vetos[i][0][1]]['positive'] == 0:
                if vetos[i][0][2] > Med:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Med) )
                else:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Min) )
            else:
                print('Consirable contradictory performance differences!')
                print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Med) )
        #print('number of real vetos: %d' % (realveto))
        #return nv,realveto
        try:
            negativeVetos = self.negativeVetos
        except:
            negativeVetos = []
        print('\n*----  Positive polarisations ----*')
        #vetos.sort()
        cv = len(negativeVetos)
        print('number of positive polarisations: %d ' % (cv))
        for i in range(cv):
            print('%d: r(%s >= %s) = %.2f' %\
                      (i+1,negativeVetos[i][0][0],
                       negativeVetos[i][0][1],negativeVetos[i][0][2]) )
            for lpd in negativeVetos[i][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable performance difference : %.2f' % lpd[1][1] )
                print('Counter-veto threshold              : %.2f' % lpd[1][3] )            
            if lpdCount[negativeVetos[i][0][0]][negativeVetos[i][0][1]]['negative'] == 0:
                if negativeVetos[i][0][2] < Med:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (negativeVetos[i][0][0],
                       negativeVetos[i][0][1],negativeVetos[i][0][2],Med) )
                else:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                      (negativeVetos[i][0][0],
                       negativeVetos[i][0][1],negativeVetos[i][0][2],Max) )
            else:
                print('Consirable contradictory performance differences!')
                print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (negativeVetos[i][0][0],
                       negativeVetos[i][0][1],negativeVetos[i][0][2],Med) )

    def showVetos(self,cutLevel=None,realVetosOnly = False):
        """
        prints all veto and counter-veto situations observed in the OutrankingDigraph instance.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        lpdCount = self.largePerformanceDifferencesCount
        print('*----  Veto situations ---')
        #nv, realveto = self.computeVetosShort()
        vetos = self.vetos
        #vetos.sort()
        nv = len(vetos)
        print('number of veto situations : %d ' % (nv))
        for i in range(nv):
            print('%d: r(%s >= %s) = %.2f' %\
                (i+1,vetos[i][0][0],vetos[i][0][1],vetos[i][0][2]) )
            for lpd in vetos[i][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable performance difference : %.2f' % lpd[1][1] )
                print('Veto discrimination threshold       : %.2f' % -lpd[1][3] )
            if lpdCount[vetos[i][0][0]][vetos[i][0][1]]['positive'] == 0:
                if vetos[i][0][2] > Med:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Med) )
                else:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Min) )
            else:
                print('Consirable contradictory performance differences!')
                print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (vetos[i][0][0],vetos[i][0][1],vetos[i][0][2],Med) )
        #print('number of real vetos: %d' % (realveto))
        #return nv,realveto
        print('\n*----  Counter-veto situations ---')
        negativeVetos = self.negativeVetos
        #vetos.sort()
        cv = len(negativeVetos)
        print('number of counter-veto situations : %d ' % (nv))
        for i in range(cv):
            print('%d: r(%s >= %s) = %.2f' %\
                      (i+1,negativeVetos[i][0][0],\
                       negativeVetos[i][0][1],negativeVetos[i][0][2]) )
            for lpd in negativeVetos[i][1]:
                print('criterion: ' + str(lpd[0]))
                print('Considerable performance difference : %.2f' % lpd[1][1] )
                print('Counter-veto threshold              : %.2f' % lpd[1][3] )            
            if lpdCount[negativeVetos[i][0][0]][negativeVetos[i][0][1]]['negative'] == 0:
                if negativeVetos[i][0][2] < Med:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (negativeVetos[i][0][0],\
                       negativeVetos[i][0][1],negativeVetos[i][0][2],Med) )
                else:
                    print('Polarisation: r(%s >= %s) = %.2f ==> %+.2f' %\
                      (negativeVetos[i][0][0],\
                        negativeVetos[i][0][1],negativeVetos[i][0][2],Max) )
            else:
                print('Consirable contradictory performance differences!')
                print('Polarisation: r(%s >= %s) = %.2f ==> %.2f' %\
                      (negativeVetos[i][0][0],\
                       negativeVetos[i][0][1],negativeVetos[i][0][2],Med) )
               

    def saveXMCDA2RubisChoiceRecommendation(self,fileName='temp',
                                            category='Rubis',subcategory='Choice Recommendation',
                                            author='digraphs Module (RB)',reference='saved from Python',
                                            comment=True,servingD3=False,relationName='Stilde',
                                            graphValuationType='bipolar',variant='standard',
                                            instanceID='void',stringNA='NA',_OldCoca=True,
                                            Debug=False):
        """
        save complete Rubis problem and result in XMCDA 2.0 format with unicode encoding.

        *Warning*: obsolete now!
        """
        import codecs,copy

        # save a copy of self
        selfOrig = copy.deepcopy(self)
        if Debug:
            print('Debug sel orig:', self.__dict__.keys())

        # the next command augments self with chordless circuits,
        # the case given ! _OldCoca is True by default for compatibility reasons
        # with the old Rubis web services in D3 and D4 for instance !
        self.computeRubyChoice(_OldCoca=_OldCoca)
        if Debug:
            print('Debug after computeRubyChoice:', self.__dict__.keys())

        if isinstance(self,RobustOutrankingDigraph):
            category = 'Robust Rubis'

        if comment:
            print('*----- saving digraph in XMCDA 2.0 format  -------------*')        
        nameExt = fileName+'.xmcda2'
        #nameExt = fileName+'.xml'
        fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if category=='Rubis':
            if not servingD3:
                fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2RubisChoice.xsl"?>\n')
            else:
                fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2RubisChoice.xsl"? -->\n')
        elif category=='Robust Rubis':
            if not servingD3:
                fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2RubisRobustChoice.xsl"?>\n')
            else:
                fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2RubisRobustChoice.xsl"? -->\n')
        else:
            if not servingD3:
                fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n')
            else:
                fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n')     
        fo.write('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n xsi:schemaLocation="http://www.decision-deck.org/2009/XMCDA-2.0.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.0.0.xsd"\n xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0" instanceID="%s">\n' % str(instanceID) )

        # write description
        try:
            projectName = self.description['name']
        except:
            projectName = self.name
        try:
            projectID = self.description['id']
        except:
            projectID = fileName
            
        fo.write('<projectReference id="%s" name="%s">\n' % (str(projectID),str(projectName)))
        # titles
        if category == 'Rubis':
            title = 'Rubis Best Choice Recommendation'
        elif category == 'Robust Rubis':
            title = 'Condorcet Robustness of a Rubis Best Choice Recommendation'
        fo.write('<%s>%s</%s>\n' % ('title', str(title),'title') )
        try:
            fo.write('<%s>%s</%s>\n' % ('subTitle', str(self.description['title']),'subTitle') )
        except:
            pass
        try:
            fo.write('<%s>%s</%s>\n' % ('subSubTitle', str(self.description['subTitle']),'subSubTitle') )
        except:
            pass
        # rest of case description including the bibliography
        try:
            for entry in self.description:
                if entry == 'bibliography':
                    fo.write('<bibliography>\n')
                    for bibEntry in [x for x in self.description[entry]]:
                        if bibEntry == 'description':
                            fo.write('<description><subSubTitle>%s</subSubTitle></description>\n' %\
                                     (str(self.description['bibliography']['description']['subSubTitle'])) )
                        else:
                            fo.write('<bibEntry>%s</bibEntry>\n' %\
                                     (str(self.description['bibliography'][bibEntry])) )
                    fo.write('</bibliography>\n')
                elif entry != 'title' and entry != 'subTitle' and entry != 'subSubTitle' and entry != 'name' and entry != 'id' and entry != 'type':
                    fo.write('<%s>%s</%s>\n' % (entry, str(self.description[entry]),entry) )
        except:
            fo.write('<author>%s</author>\n' % (str(author)) )
            fo.write('<version>%s</version>\n' % (str(reference)) )
        fo.write('</projectReference>\n')

        # write methodParameters
        if category == 'Robust Rubis':
            fo.write('<methodParameters id="%s" name="%s">\n' % ('Robust Rubis','Robustness analysis of Rubis best choice method'))
            fo.write('<description>\n')
            fo.write('<subTitle>Method data</subTitle>\n')
            fo.write('<comment>Results of Condorcet robustness analysis in XMCDA format.</comment>\n')
        else:
            fo.write('<methodParameters id="%s" name="%s">\n' % ('Rubis','Rubis best choice method') )
            fo.write('<description>\n')
            fo.write('<subTitle>Method data</subTitle>\n')
            fo.write('<comment>Rubis best choice recommendation in XMCDA format.</comment>\n')        
        fo.write('<version>%s</version>\n' % ('1.0'))
        fo.write('</description>\n')
        fo.write('<parameters>\n')
        try:
            variant = self.methodData['parameter']['variant']
            fo.write('<parameter name="%s">\n' % ('variant'))
            fo.write('<value>\n')
            fo.write('<label>%s</label>\n' % (variant) )
            fo.write('</value>\n')
            fo.write('</parameter>\n')
        except:
            pass
        try:
            valuationType = self.methodData['parameter']['valuationType']
            fo.write('<parameter name="%s">\n' % ('valuationType') )
            fo.write('<value>\n')
            fo.write('<label>%s</label>\n' % (valuationType) )
            fo.write('</value>\n')
            fo.write('</parameter>\n')
        except:
            pass   
        try:
            vetoType = self.methodData['parameter']['vetoType']
            fo.write('<parameter name="%s">\n' % ('vetoType') )
            fo.write('<value>\n')
            fo.write('<label>%s</label>\n' % (vetoType) )
            fo.write('</value>\n')
            fo.write('</parameter>\n')
        except:
            pass   
        fo.write('</parameters>\n')
        fo.write('</methodParameters>\n')

        # write potential actions 
        origActionsList = [x for x in self.actions_orig]
        origActionsList.sort()            
        fo.write('<alternatives mcdaConcept="alternatives">\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('List of Alternatives'))
        fo.write('<subTitle>Potential decision actions.</subTitle>\n')
        #fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('</description>\n')                  
        for x in origActionsList:
            try:
                alternativeName=self.actions_orig[x]['name']
            except:
                alternativeName=x
            
            fo.write('<alternative id="%s" name="%s">\n' % (str(x),str(alternativeName)) )
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(self.actions_orig[x]['comment'])) 
            except:
                fo.write('potential decision actions')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<type>real</type>\n')
            fo.write('<active>true</active>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        
        # coca actions if any
        cocaActionsList = [x for x in self.actions if isinstance(x,frozenset)]
        if Debug:
            print('Debug: cocaActionsList',cocaActionsList) 
        if cocaActionsList != []:
            cocaActionsList.sort()
            fo.write('<alternatives mcdaConcept="%s">\n' % ('cocaActions'))
            fo.write('<description>\n')
            fo.write('<subTitle>%s</subTitle>\n' % ('Coca digraph actions'))
            #fo.write('<type>%s</type>\n' % ('cocaActions'))
            fo.write('<comment>Chordless odd circuits added to the original outranking digraph.</comment>\n')
            fo.write('</description>\n')                  
            for x in cocaActionsList:
                fo.write('<alternative id="%s" name="%s">\n' %\
                         (str(self.actions[x]['name']),str(self.actions[x]['name'])) )
                fo.write('<description>\n')
                fo.write('<comment>%s</comment>\n' % (str(self.actions[x]['comment'])) )
                fo.write('</description>\n')
                fo.write('<type>fictive</type>\n')
                fo.write('</alternative>\n')
            fo.write('</alternatives>\n')

        # save objectives if there are any
        try:
            objectivesList = [x for x in self.objectives]
            objectivesList.sort()
            objectives = self.objectives
            fo.write('<objectives mcdaConcept="objectives">\n')
            fo.write('<description>\n')
            fo.write('<subTitle>Set of decision objectives</subTitle>\n')
            fo.write('</description>\n')
            for obj in objectivesList:
                try:
                    objectiveName = str(objectives[obj]['name'])
                except:
                    objectiveName = str(obj)
                fo.write('<objective id="%s" name="%s" mcdaConcept="%s">\n' % (str(obj),objectiveName,'objective' ) )
                fo.write('<description>\n')                
                try:
                    fo.write('<comment>%s</comment>\n' % (str(objective[obj]['comment'])) )
                except:
                    fo.write('<comment>%s</comment>\n' % ('No comment') )
                fo.write('<version>%s</version>\n' % ('Rubis') )
                fo.write('</description>\n')
                fo.write('<active>true</active>\n')
                fo.write('<weight><value><real>%.2f</real></value></weight>\n' %\
                                                        (objectives[obj]['weight']) )
                try:
                    objCriteria = [x for x in self.criteria if self.criteria[x]['objective'] == obj]
                    fo.write('<objectiveCriteria>%s</objectiveCriteria>\n' %\
                             (str(objCriteria)) )
                except:
                    pass
                fo.write('</objective>\n')
            fo.write('</objectives>\n')
        except:
            pass
        
        # save criteria
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        criteria = self.criteria
        fo.write('<criteria mcdaConcept="%s">\n' % ('criteria'))
        fo.write('<description>\n')
        fo.write('<title>Rubis family of criteria.</title>\n')
        #fo.write('<type>%s</type>\n' % ('criteria'))
        fo.write('</description>\n')       
        for g in criteriaList:
            critg = criteria[g]
            try:
                criterionName = str(critg['name'])
            except:
                criterionName = 'nameless'
            
            fo.write('<criterion id="%s" name="%s" mcdaConcept="%s">\n' %\
                     (g,criterionName,'criterion') )
            fo.write('<description>\n')
            try:
                fo.write('<comment>%s</comment>\n' % (str(critg['comment'])) )
            except:
                fo.write('<comment>%s</comment>\n' % ('no comment') )
            fo.write('<version>%s</version>\n' % ('performance') )
            fo.write('</description>\n')
            fo.write('<active>true</active>\n')
            try:
                fo.write('<criterionObjective>%s</criterionObjective>\n' %\
                         critg['objective'])
            except:
                pass
            try:
                if critg['IntegerWeights']:
                    fo.write('<criterionValue><value><integer>%d</integer></value></criterionValue>\n' %\
                             (critg['weight']) )
                else:
                    fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' %\
                             (critg['weight']) )
            except:
                fo.write('<criterionValue><value><real>%.2f</real></value></criterionValue>\n' %\
                         (critg['weight']) )
 
            #fo.write('<criterionFunction category="%s" subCategory="%s" >\n' % ('Rubis','performance'))
            fo.write('<scale>\n')
            fo.write('<quantitative>\n')
            try:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' %\
                         (critg['preferenceDirection']) )
                if critg['preferenceDirection'] == 'min':
                    #pdir = -1
                    pdir = 1
                else:
                    pdir = 1
            except:
                fo.write('<preferenceDirection>%s</preferenceDirection>\n' % ('max') )
                pdir = 1
            fo.write('<minimum><real>%.2f</real></minimum>\n' % (critg['scale'][0]) )
            fo.write('<maximum><real>%.2f</real></maximum>\n' % (critg['scale'][1]) )

            fo.write('</quantitative>\n')
            fo.write('</scale>\n')
            fo.write('<thresholds>\n')
            try:
                if critg['thresholds']['ind'] is not None:
                    fo.write('<threshold id="%s">\n' % ('ind'))
                    if critg['thresholds']['ind'][1] != Decimal('0.0'):
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' %\
                                 (pdir*critg['thresholds']['ind'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' %\
                                 (critg['thresholds']['ind'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' % (critg['thresholds']['ind'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
                
            except:
                pass
            try:
                if critg['thresholds']['weakPreference'] is not None:
                    fo.write('<threshold id="%s">\n' % ('weakPreference'))
                    if critg['thresholds']['weakPreference'][1] != Decimal('0.0'):
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' %\
                                 (pdir*critg['thresholds']['weakPreference'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' %\
                                 (critg['thresholds']['weakPreference'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' %\
                                 (critg['thresholds']['weakPreference'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if critg['thresholds']['pref'] is not None:
                    fo.write('<threshold id="%s">\n' % ('pref'))
                    if critg['thresholds']['pref'][1] != Decimal('0.0'):
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' %\
                                 (pdir*critg['thresholds']['pref'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' %\
                                 (critg['thresholds']['pref'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' %\
                                 (critg['thresholds']['pref'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if critg['thresholds']['weakVeto'] is not None:
                    fo.write('<threshold id="%s">\n' % ('weakVeto'))
                    if critg['thresholds']['weakVeto'][1] != Decimal('0.0'):
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' %\
                                 (pdir*critg['thresholds']['weakVeto'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' %\
                                 (critg['thresholds']['weakVeto'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' %\
                                 (critg['thresholds']['weakVeto'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            try:
                if critg['thresholds']['veto'] is not None:
                    fo.write('<threshold id="%s">\n' % ('veto'))
                    if critg['thresholds']['veto'][1] != Decimal('0.0'):
                        fo.write('<linear>\n')
                        fo.write('<slope><real>%.2f</real></slope>\n' %\
                                 (pdir*critg['thresholds']['veto'][1]) )
                        fo.write('<intercept><real>%.2f</real></intercept>\n' %\
                                 (critg['thresholds']['veto'][0]) )
                        fo.write('</linear>\n')
                    else:
                        fo.write('<constant>\n')
                        fo.write('<real>%.2f</real>\n' %\
                                 (critg['thresholds']['veto'][0]) )
                        fo.write('</constant>\n')                       
                    fo.write('</threshold>\n')
            except:
                pass
            fo.write('</thresholds>\n')
            #fo.write('</criterionFunction>\n')
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')
        
        # save performance table
        evaluation = self.evaluation
        NA = self.NA
        fo.write('<performanceTable mcdaConcept="%s">\n' %('performanceTable') )
        fo.write('<description>\n')
        fo.write('<title>Rubis Performance Table</title>\n')            
        fo.write('</description>\n')
        for i in range(len(origActionsList)):
            fo.write('<alternativePerformances>\n')
            fo.write('<alternativeID>'+str(origActionsList[i])+'</alternativeID>\n')
            for g in criteriaList:
                fo.write('<performance>\n')
                fo.write('<criterionID>')       
                fo.write(g)
                fo.write('</criterionID>\n')
                val = evaluation[g][origActionsList[i]]
                if val == NA:
                    fo.write('<value><NA>')
                    fo.write('%s' % stringNA )
                    fo.write('</NA></value>\n')
                else:
                    try:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            if self.criteria[g]['weight'] > Decimal('0'):
                                pdir = Decimal('-1')
                            else:
                                pdir = Decimal('1')
                        else:
                            pdir = Decimal('1')
                    except:
                        pdir = Decimal('1')

                    fo.write('<value><real>')
                    fo.write('%.2f' % (pdir*evaluation[g][origActionsList[i]]) )
                    fo.write('</real></value>\n')
                fo.write('</performance>\n')
            fo.write('</alternativePerformances>\n')
        fo.write('</performanceTable>\n')        

        # criteria ordinal correlation analysis
        if category != 'Robust Rubis':
            corr,d = selfOrig.computeCriteriaCorrelations()
            criteriaList = [x for x in self.criteria]
            cn = len(criteriaList)
            criteriaList.sort()
            criteria = self.criteria
            fo.write('<criteriaComparisons mcdaConcept="%s">\n' % ('correlationTable'))
            fo.write('<description>\n')
            fo.write('<title>%s</title>\n' % ('Ordinal Criteria Correlation Index'))
            fo.write('<comment>%s</comment>\n' %\
                     ('Generalisation of Kendall&apos;s &#964; to nested homogeneous semiorders.') )
            fo.write('</description>\n')
            fo.write('<comparisonType>%s</comparisonType>' % ('correlation'))
            fo.write('<pairs>\n')
            for ci in range(cn):
                for cj in range(cn):
                    fo.write('<pair>\n')        
                    fo.write('<initial><criterionID>')
                    fo.write(str(criteriaList[ci]))
                    fo.write('</criterionID></initial>\n')                       
                    fo.write('<terminal><criterionID>')
                    fo.write(str(criteriaList[cj]))
                    fo.write('</criterionID></terminal>\n')                                             
                    fo.write('<value><real>%2.2f' %\
                             (corr[criteriaList[ci]][criteriaList[cj]]) )
                    fo.write('</real></value>\n')                       
                    fo.write('</pair>\n')               
            fo.write('</pairs>\n')
            fo.write('</criteriaComparisons>\n')
        
        # outranking digraph
        if category != 'Robust Rubis':
            fo.write('<alternativesComparisons name="%s" mcdaConcept="%s">\n' %\
                     (relationName,'outrankingDigraph'))
            fo.write('<description>\n')
            fo.write('<title>%s</title>\n' % ('Bipolar-valued Outranking Relation'))
            #fo.write('<name>%s</name>\n' % (relationName) )
            #fo.write('<type>%s</type>\n' % ('outrankingDigraph'))
            fo.write('<comment>%s %s Relation</comment>\n' % (category,subcategory) )
        else:
            fo.write('<alternativesComparisons name="%s" mcdaConcept="%s">\n' %\
                     (relationName,'CondorcetRobustness') )
            fo.write('<description>\n')
            fo.write('<title>%s</title>\n' % ('Valued Outranking Relation'))
            #fo.write('<name>%s</name>\n' % (relationName) )
            #fo.write('<type>%s</type>\n' % ('outrankingDigraph'))
            fo.write('<comment>%s</comment>\n' % ('with Condorcet Robustness denotation') )
            
        fo.write('</description>\n')                  
        fo.write('<valuation>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valuation Domain'))
        if category != 'Robust Rubis':
            fo.write('<comment>%s</comment>\n' % ('Significance degrees') )
        else:
            fo.write('<comment>%s</comment>\n' % ('Condorcet robustness degrees') )
        fo.write('</description>\n')
        fo.write('<valuationType>%s</valuationType>\n' % (graphValuationType) )
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        fo.write('<quantitative>')
        if category == 'Robust Rubis':        
            fo.write('<minimum><real>%d</real></minimum>' % (Min))
            fo.write('<maximum><real>%d</real></maximum>' % (Max))
        else:
            fo.write('<minimum><real>%2.2f</real></minimum>' % (Min))
            fo.write('<maximum><real>%2.2f</real></maximum>' % (Max))
        fo.write('</quantitative>\n')
        fo.write('</valuation>\n')
        fo.write('<pairs>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valued Adjacency Table'))
        try:
            category = self.category
            subcategory = self.subcategory
        except:
            pass
        if category == 'Robust Rubis':
            fo.write('<comment>Pairwise outranking significance degrees in the range: %d to %d with Condorcet robustness degrees shown in brackets. </comment>\n' %\
                     (self.cardinalValuationdomain['min'],self.cardinalValuationdomain['max']) )
        else:
            fo.write('<comment>Pairwise outranking significance degrees in the range: %2.2f to %2.2f</comment>\n' % (Min,Max) )
            
            
        fo.write('</description>\n')                  
        relation = self.relation
        if category == 'Robust Rubis':
            cardinalRelation = self.cardinalRelation
        for x in origActionsList:
            for y in origActionsList:
                fo.write('<pair>\n')        
                fo.write('<initial><alternativeID>')
                fo.write(str(x))
                fo.write('</alternativeID></initial>\n')                       
                fo.write('<terminal><alternativeID>')
                fo.write(str(y))
                fo.write('</alternativeID></terminal>\n')
                try:
                    if self.methodData['parameter']['valuationType'] == 'integer':
                        fo.write('<value><integer>%d</integer></value>' % (relation[x][y]) )
                    elif category == 'Robust Rubis':
                        fo.write('<values>\n')
                        if x != y:
                            fo.write('<value name="outranking"><integer>%d</integer></value>\n' %\
                                     (cardinalRelation[x][y]) )
                            fo.write('<value name="robustness"><integer>%d</integer></value>\n' %\
                                     (relation[x][y]) )
                        else:
                            fo.write('<value name="outranking"><integer>%d</integer></value>\n' % (100) )
                            fo.write('<value name="robustness"><integer>%d</integer></value>\n' % (3) )                            
                        fo.write('</values>\n')
                    else:
                        fo.write('<value><real>%2.2f</real></value>' % (relation[x][y]) )
                except:
                    if category == 'Robust Rubis':
                        fo.write('<values>\n')
                        fo.write('<value name="outranking"><real>%2.2f</real></value>\n' % (cardinalRelation[x][y]) )
                        if x == y:
                            fo.write('<value name="outranking"><real>%2.2f</real></value>\n' % (100) )
                            fo.write('<value name="robustness"><integer>%d</integer></value>\n' % (3) )
                        else:
                            fo.write('<value name="outranking"><real>%2.2f</real></value>\n' %\
                                     (cardinalRelation[x][y]) )
                            fo.write('<value name="robustness"><integer>%d</integer></value>\n' %\
                                     (int(relation[x][y])) )
                        fo.write('</values>\n') 
                    else:
                        fo.write('<value><real>%2.2f' % (relation[x][y]) )
                        fo.write('</real></value>\n')                       
                fo.write('</pair>\n')
        fo.write('</pairs>\n')
        fo.write('</alternativesComparisons>\n')     

        # vetos if any
        try:
            vetos = self.vetos
            if vetos != []:
                Med = self.valuationdomain['med']
                fo.write('<alternativesComparisons mcdaConcept="Vetoes">\n')
                fo.write('<description>\n')
                fo.write('<title>%s</title>\n' % ('Vetoes'))
                fo.write('</description>\n')                  
                fo.write('<pairs>\n')
                fo.write('<description>\n')
                fo.write('<subTitle>%s</subTitle>\n' % ('Effective and potential veto situations'))
                fo.write('</description>\n')                  
                for veto in vetos:
                    arc = veto[0]
                    fo.write('<pair>\n')
                    fo.write('<description>\n')
                    fo.write('<comment>concordance degree:%.2f</comment>\n' % (arc[2]) )
                    fo.write('</description>\n')
                    fo.write('<initial><alternativeID>')
                    fo.write(str(arc[0]))
                    fo.write('</alternativeID></initial>\n')                       
                    fo.write('<terminal><alternativeID>')
                    fo.write(str(arc[1]))
                    fo.write('</alternativeID></terminal>\n')                                             
                    situations = veto[1]
                    for v in situations:
                        fo.write('<values id="%s">\n' % ( str(v[0]) ) )
                        fo.write('<description>\n')
                        fo.write('<comment>')
                        if arc[2] > Med:
                            if v[1][0] > Decimal('0'):
                                fo.write('effective veto')
                            else:
                                fo.write('effective weak veto')
                        elif arc[2] == Med:
                            if v[1][0] > Decimal('0'):
                                fo.write('effective veto')
                            else:
                                fo.write('potential weak veto')
                        else:
                            if v[1][0] > Decimal('0'):
                                fo.write('potential veto')
                            else:
                                fo.write('potential weak veto')                   
                        fo.write('</comment>\n')
                        fo.write('</description>\n')
                        fo.write('<value name="%s">\n' % ('performanceDifference'))
                        fo.write('<real>%.2f</real>' % (v[1][1]))
                        fo.write('</value>\n')
                        fo.write('<value name="%s">\n' % ('vetoCharacteristic'))
                        fo.write('<real>%.2f</real>' % (v[1][0]))
                        fo.write('</value>\n')
                        fo.write('</values>\n')
                    fo.write('</pair>\n')
                fo.write('</pairs>\n')
                fo.write('</alternativesComparisons>\n') 
        except:
            pass
   
        # good choices
        
        amplitude = (Max - Min) / Decimal('100.0')
        fo.write('<alternativesSets mcdaConcept="%s">\n' % ('goodChoices'))
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Rubis Choice Recommendation'))
        if category == 'Robust Rubis':
            fo.write('<comment>In decreasing order of determinateness.</comment>\n')
        else:
            fo.write('<comment>In decreasing order of determinateness. All values expressed in %. </comment>\n')
        fo.write('</description>\n')
        nb = Decimal('0')
        maxDet = Decimal('0.0')
        for ch in self.goodChoices:
            maxDet = max(maxDet,ch[0])
        for ch in self.goodChoices:
            #if ch[3] > -ch[4]:
            nb += 1
            fo.write('<alternativesSet id="good_%d" mcdaConcept="%s">\n' % (nb,'goodChoice') )
            fo.write('<description>\n')
            if category == 'Robust Rubis':
                determ = (ch[0]*Decimal('6')) - Decimal('3')
                if determ > Decimal('1'):
                    fo.write('<comment>Robust good choice</comment>\n')
                else:
                    fo.write('<comment>Potential good choice</comment>\n')
            else:
                if maxDet == ch[0]:
                    fo.write('<comment>Best choice</comment>\n')
                else:
                    fo.write('<comment>Potential good choice</comment>\n')                    
            fo.write('</description>\n')
            for x in ch[5]:
                fo.write('<element>\n')
                fo.write('<alternativeID>')
                if isinstance(x,frozenset):
                    #print(self.actions[x])
                    fo.write(str(self.actions[x]['name']))
                else:
                    fo.write(str(x))
                fo.write('</alternativeID>\n')
                fo.write('</element>\n')
            if category == 'Robust Rubis':
                fo.write('<values>\n')
                independent = ch[2]
                fo.write('<value name="choiceSet independence"><integer>%d</integer></value>\n' %(independent) )
                outranking = ch[3]
                fo.write('<value name="outranking"><integer>%d</integer></value>\n' %(outranking) )
                outranked = ch[4]
                fo.write('<value name="outranked"><integer>%d</integer></value>\n' % (outranked) )
                determ = (ch[0]*Decimal('6'))-Decimal('3')
                fo.write('<value name="determinateness"><real>%2.2f</real></value>\n' % (determ)  )
                fo.write('</values>\n')
            else:
                fo.write('<values>\n')
                independent = (ch[2] - Min) / amplitude
                fo.write('<value name="choiceSet independence"><real>%2.2f</real></value>\n' %(independent) )
                outranking = (ch[3] - Min) / amplitude
                fo.write('<value name="outranking"><real>%2.2f</real></value>\n' %(outranking) )
                outranked = (ch[4] - Min) / amplitude
                fo.write('<value name="outranked"><real>%2.2f</real></value>\n' %(outranked) )
                determ = ch[0]*Decimal('100.0')
                fo.write('<value name="determinateness"><real>%2.2f</real></value>\n' %(determ) )
                fo.write('</values>\n')                    
            fo.write('</alternativesSet>\n')             
        fo.write('</alternativesSets>\n')

        # bad choices if any

        if self.badChoices != []:
            #amplitude = float(Max - Min)/float(100.0)
            fo.write('<alternativesSets mcdaConcept="badChoices">\n')
            fo.write('<description>\n')
            fo.write('<subTitle>%s</subTitle>\n' % ('Potentially Bad Choices'))
            if category != 'Robust Rubis':
                fo.write('<comment>All values expressed in %.</comment>\n')
            fo.write('</description>\n')
            nb = 0
            for ch in self.badChoices:
                #if -ch[3] > ch[4]: 
                nb += 1
                fo.write('<alternativesSet id="bad_%d" mcdaConcept="badChoice">\n' % (nb) )
                fo.write('<description>\n')
                if category == 'Robust Rubis':
                    determ = (ch[0]*Decimal('6'))-Decimal('3')
                    if determ > Decimal('1'):
                        fo.write('<comment>Robust bad choice</comment>\n')
                    else:
                        fo.write('<comment>Potential bad choice</comment>\n')
                else:
                    if ch[4] > ch[3]:
                        fo.write('<comment>Bad choice</comment>\n')
                    else:
                        fo.write('<comment>Ambiguous choice</comment>\n')
                fo.write('</description>\n')
                for x in ch[5]:
                    fo.write('<element>\n')
                    fo.write('<alternativeID>')
                    if isinstance(x,frozenset):
                        fo.write(str(self.actions[x]['name']))
                    else:
                        fo.write(str(x))
                    fo.write('</alternativeID>\n')
                    fo.write('</element>\n')
                if category == 'Robust Rubis':
                    fo.write('<values>\n')
                    independent = ch[2]
                    fo.write('<value name="choiceSet independence"><integer>%d</integer></value>\n' %\
                             (independent) )
                    outranking = ch[3]
                    fo.write('<value name="outranking"><integer>%d</integer></value>\n' %\
                             (outranking) )
                    outranked = ch[4]
                    fo.write('<value name="outranked"><integer>%d</integer></value>\n' %(outranked) )
                    determ = (ch[0]*Decimal('6')) - Decimal('3')
                    fo.write('<value name="determinateness"><real>%2.2f</real></value>\n' %(determ) )
                    fo.write('</values>\n')
                else:
                    fo.write('<values>\n')
                    independent = (ch[2] - Min)/amplitude
                    fo.write('<value name="choiceSet independence"><real>%2.2f</real></value>\n' %\
                             (independent) )
                    outranking = (ch[3] - Min)/amplitude
                    fo.write('<value name="outranking"><real>%2.2f</real></value>\n' %(outranking) )
                    outranked = (ch[4] - Min)/amplitude
                    fo.write('<value name="outranked"><real>%2.2f</real></value>\n' %(outranked) )
                    determ = ch[0]*Decimal('100.0')
                    fo.write('<value name="determinateness"><real>%2.2f</real></value>\n' %(determ) )
                    fo.write('</values>\n')                    
                fo.write('</alternativesSet>\n')             
            fo.write('</alternativesSets>\n')

        # end of XMCDA 2.0 file
        fo.write('</xmcda:XMCDA>\n')
        
        fo.close()
        
        if comment:
            print('File: ' + nameExt + ' saved !')

        # restore self to its original content
        self.__dict__ = selfOrig.__dict__
        

class _Electre3OutrankingDigraph(OutrankingDigraph):
    """
    Specialization of the standard OutrankingDigraph class for generating classical Electre III outranking digraphs (with vetoes and no counter-vetoes).

    Parameters:
        | performanceTableau (fileName of valid py code)
        | optional, coalition (sublist of criteria)


    """
    def __init__(self,argPerfTab=None,coalition=None,hasNoVeto=False):
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        self.name = 'rel_' + perfTab.name
        self.actions = copy.deepcopy(perfTab.actions)
        Min =   Decimal('0')
        Med =   Decimal('50')
        Max =   Decimal('100')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        if coalition is None:
            criteria = copy.deepcopy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
        self.relation = self._constructRelation(criteria,perfTab.evaluation,hasNoVeto=hasNoVeto)
        self.criteria = criteria
        self.evaluation = copy.deepcopy(perfTab.evaluation)
        try:
            self.description = copy.deepcopy(perfTab.description)
        except:
            pass
        methodData = {}
        try:
            valuationType = perfTab.parameter['valuationType']
            variant = perfTab.parameter['variant']
        except:
            valuationType = 'normalized'
            variant = 'electre3'
        methodData['parameter'] = {'valuationType':valuationType,'variant':variant}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        

    def showVetos(self,cutLevel=None,realVetosOnly = False,Comments=True):
        """
        prints all veto situations observed in the OutrankingDigraph instance.
        """
        if Comments:
            print('*----  Veto situations ---')
        nv, realveto = self.computeVetosShort()
        vetos = self.vetos
        vetos.sort()
        if realVetosOnly:
            if Comments:
                print(self.valuationdomain)
            cutveto = 0
            if cutLevel is None:
                cutLevel = self.valuationdomain['med']
            else:
                cutLevel = Decimal(str(cutLevel))
            if cutLevel > self.valuationdomain['max']:
                if Comments:
                    print("Error! min = %.3f, max = %.3f" %\
                          (self.valuationdomain['min'],self.valuationdomain['max']))
                return None
            if Comments:
                print('Real vetos at cut level: %.3f' % (cutLevel))
            for i in range(nv):
                if self.vetos[i][0][2] > cutLevel:
                    if Comments:
                        print('self.vetos[i][0][2]=',self.vetos[i][0][2])
                        print(str(i)+': relation: '+str(vetos[i][0])+', criteria: ' + str(vetos[i][1]))
                    cutveto += 1
            return nv,realveto,cutveto
        else:
            if Comments:
                print('number of potential vetos: %d ' % (nv))
            for i in range(nv):
                if Comments:
                    print(str(i)+': relation: '+str(vetos[i][0])+', criteria: ' + str(vetos[i][1]))
            if Comments:
                print('number of real vetos: %d' % (realveto))
            return nv,realveto

    def computeVetos(self,cutLevel=None,realVetosOnly = False):
        """
        prints all veto situations observed in the OutrankingDigraph instance.
        """

        nv, realveto = self.computeVetosShort()
        vetos = self.vetos
        vetos.sort()
        if realVetosOnly:
            cutveto = 0
            if cutLevel is None:
                cutLevel = self.valuationdomain['med']
            else:
                cutLevel = Decimal(str(cutLevel))
            if cutLevel > self.valuationdomain['max']:
                return None
            for i in range(nv):
                if self.vetos[i][0][2] > cutLevel:
                    cutveto += 1
            return nv,realveto,cutveto
        else:
            return nv,realveto


    def _constructRelation(self,criteria,evaluation,hasNoVeto=False):
        """
        Parameters: PerfTab.criteria, PerfTab.evaluation.
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        actions = self.actions
        NA = self.NA
        totalweight = Decimal('0.0')
        for c in criteria:
            totalweight = totalweight + abs(criteria[c]['weight'])
        relation = {}
        vetos = []
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a == b:
                    relation[a][b] = Decimal('0.0')
                else:
                    nc = len(criteria)
                    counter = Decimal('0.0')
                    veto = {}
                    for c in criteria:
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                ax = criteria[c]['thresholds']['ind'][0]
                                ay = criteria[c]['thresholds']['ind'][1]
                                h = ax + ay * abs(evaluation[c][a])
                            except:
                                h = None
                            try:
                                ax = criteria[c]['thresholds']['weakPreference'][0]
                                ay = criteria[c]['thresholds']['weakPreference'][1]
                                h = ax + ay * abs(evaluation[c][a])
                            except:
                                if h is None:
                                    h = Decimal('0.0')
                            try:    
                                bx = criteria[c]['thresholds']['pref'][0]
                                by = criteria[c]['thresholds']['pref'][1]
                                p = bx + by * abs(evaluation[c][a])
                            except:
                                p = None
                            try:   
                                vx = criteria[c]['thresholds']['veto'][0]
                                vy = criteria[c]['thresholds']['veto'][1]
                                if hasNoVeto:
                                    v = None
                                else:
                                    v = vx + vy * abs(evaluation[c][a])
                            except:
                                v = None
                            if criteria[c]['weight'] > Decimal('0.0'):
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]
                            lc0 = self._localConcordance(d,h,h,p)
                            counter = counter + (lc0 * abs(criteria[c]['weight']))
                            veto[c] = (self._localVeto(d,p,v),d,v)
                        else:
                            counter = counter + Decimal('0.5') * criteria[c]['weight']
                            veto[c] = (Decimal('0.0'),None,None)     
                    concordindex = counter/totalweight                    
                    discordindex = Decimal('1.0')
                    abvetos=[]
                    for c in criteria:
                        if veto[c][0] > concordindex:
                            discordindex = discordindex * (Decimal('1.0') - veto[c][0])/(Decimal('1.0') - concordindex)
                            abvetos.append((c,veto[c]))
                    if abvetos != []:
                        vetos.append(([a,b,concordindex*Decimal('100.0'),discordindex*Decimal('100.0')],abvetos))    
                    outrankindex = concordindex * discordindex         
                    relation[a][b] = outrankindex*Decimal('100.0')
        self.vetos = vetos
        return relation

    def computeCriterionRelation(self,c,a,b,hasSymmetricThresholds=False):
        """
        compute the outranking characteristic for actions x and y
        on criterion c.
        """
        criteria = self.criteria
        evaluation = self.evaluation
        NA = self.NA
        if a == b:
            return Decimal("1.0")
        else:

            if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                try:
                    indx = criteria[c]['thresholds']['ind'][0]
                    indy = criteria[c]['thresholds']['ind'][1]
                    if hasSymmetricThresholds:
                        ind = indx + indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                    else:
                        ind = indx + indy * abs(evaluation[c][a])
                except:
                    ind = Decimal("0.0")
                try:
                    wpx = criteria[c]['thresholds']['weakPreference'][0]
                    wpy = criteria[c]['thresholds']['weakPreference'][1]
                    if hasSymmetricThresholds:
                        wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                    else:
                        wp = wpx + wpy * abs(evaluation[c][a])
                    ind = wp
                except:
                    wp = None
                try:
                    px = criteria[c]['thresholds']['pref'][0]
                    py = criteria[c]['thresholds']['pref'][1]
                    if hasSymmetricThresholds:
                        p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                    else:
                        p = px + py * abs(evaluation[c][a]) 
                except:
                    p = None
                if criteria[c]['weight'] > Decimal('0.0'):
                    d = evaluation[c][a] - evaluation[c][b]
                else:
                    d = evaluation[c][b] - evaluation[c][a]
                return self._localConcordance(d,ind,wp,p)

            else:
                return Decimal("0.5")


    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters: d := diff observed, ind := indifference threshold,
        wp := weak prefrence threshold,  p := prefrence threshold, 
        Renders the concordance index per criteria.
        """
        Debug = False
        if Debug:
            print('d,ind,wp,p', d,ind,wp,p)
        if p is not None:
            if   d < -p:
                return Decimal('0')
            elif ind is not None:
                if d < -ind:
                    return (p + d)/(p - ind)
                else:
                    return Decimal('1')
            else:
                return Decimal('1')
        else:
            if ind is not None:
                if d < -ind:
                    return Decimal('0')
                else:
                    return Decimal('1')
            else:
                if d < Decimal('0'):
                    return Decimal('0')
                else:
                    return Decimal('1')
                
            

    def _localVeto(self, d, p, v):
        """
        Parameters:
            d := diff observed, v := veto threshold.

        Renders the local veto state
        """
        if v is not None:
            if p is not None:
                if  d > -p:
                    return Decimal('0.0')
                elif d < -v:
                    return Decimal('1.0')
                else:
                    return (Decimal('-1'))*(d+p)/(v+p)
            else:
                if d < -v:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
        else:
            return Decimal('0.0')

# multiprocessing thread for BipolarOutrankingDigraph class
class _myBODGThread(Process):
    def __init__(self, target,args):
        Process.__init__(self)
        self.threadID = target
        self.digraph = args[0]
        self.InitialSplit = args[1]
        self.workingDirectory = args[2]
        self.splitActions = args[3]
        self.hasNoVeto = args[4]
        self.hasBipolarVeto = args[5]
        self.hasSymmetricThresholds = args[6]
        self.Debug = args[7]
    def run(self):
        from io import BytesIO
        from pickle import Pickler, dumps, loads
        from os import chdir
        chdir(self.workingDirectory)
        Debug = self.Debug
        if Debug:
            print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadId)))
##                    fi = open('dumpSelf.py','rb')
##                    digraph = loads(fi.read())
##                    fi.close()
        digraph = self.digraph
        splitActions = self.splitActions
##                    fiName = 'splitActions-'+str(self.threadID)+'.py'
##                    fi = open(fiName,'rb')
##                    splitActions = loads(fi.read())
##                    fi.close()
        # compute partiel relation
        #if (not self.hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
        #    constructRelation = BipolarOutrankingDigraph._constructRelation
        #else:
        constructRelation = BipolarOutrankingDigraph._constructRelationSimple
        if self.InitialSplit:
            #splitRelation = BipolarOutrankingDigraph._constructRelation(
            splitRelation = constructRelation(
                                digraph,digraph.criteria,\
                                digraph.evaluation,
                                initial=splitActions,
                                #terminal=terminal,
                                hasNoVeto=self.hasNoVeto,
                                hasBipolarVeto=self.hasBipolarVeto,
                                WithConcordanceRelation=False,
                                WithVetoCounts=False,
                                Debug=False,
                                hasSymmetricThresholds=self.hasSymmetricThresholds)
        else:
            #splitRelation = BipolarOutrankingDigraph._constructRelation(
            splitRelation = constructRelation(
                                digraph,digraph.criteria,\
                                digraph.evaluation,
                                #initial=initial,
                                terminal=splitActions,
                                hasNoVeto=self.hasNoVeto,
                                hasBipolarVeto=self.hasBipolarVeto,
                                WithConcordanceRelation=False,
                                WithVetoCounts=False,
                                Debug=False,
                                hasSymmetricThresholds=self.hasSymmetricThresholds)
        # store partial relation
        foName = 'splitRelation-'+str(self.threadID)+'.py'
        fo = open(foName,'wb')
        fo.write(dumps(splitRelation,-1))
        fo.close()
    # .......


class BipolarOutrankingDigraph(OutrankingDigraph):
    """
    Specialization of the abstract OutrankingDigraph root class for generating
    bipolarly-valued outranking digraphs.

    Parameters:
        * argPerfTab: instance of PerformanceTableau class.
          If a file name string is given, the performance tableau will directly be loaded first.
        * coalition: subset of criteria to be used for contructing the outranking digraph.
        * hasNoVeto: veto desactivation flag (False by default).
        * hasBipolarVeto: bipolar versus electre veto activation (true by default).
        * Normalized: the valuation domain is set by default to [-100,+100] (bipolar percents).
          If True, the valuation domain is recoded to [-1.0,+1.0].
        * WithConcordanceRelation: True by default when not threading.
          The self.concordanceRelation contains the significance majority margin of the "at least as good relation as"
          without the large performance difference polarization.
        * WithVetoCounts: True by default when not threading. All vetos and countervetos
          are stored in self.vetos and self.negativeVetos slots,
          as well the counts of large performance differences in self.largePerformanceDifferencesCount slot.
        * Threading: False by default. Allows to profit from SMP machines via the Python multiprocessing module.
        * startMethod: 'spawn' (default), 'forkserver' or 'fork' (not safe against dead locks)
        * nbrCores: controls the maximal number of cores that will be used in the multiprocessing phases.
          If None is given, the os.cpu_count method is used in order to determine the number of available CPU cores on the SMP machine.

   .. warning:: The multiprocessing :py:class:`~outrankingDigraphs.BipolarOutrankingDigraph` constructor uses
        by default the 'spawn' start-mathod for threading.
        When not using the 'fork' start method in a python script file,
        the main entry code must hence be protected with the __name__=='__main__' test
        in order to avoid a recursive re-execution of the whole script.
        (see the documentation of the :py:mod:`multiprocessing` module.

        If Threading is *True*, *WithConcordanceRelation* and *WithVetoCounts* flags
        are automatically set both to False.
    
    """
    def __repr__(self):
        """
        Default presentation method for BipolarOutrankingDigraph instance.
        """
        reprString = '*------- Object instance description ------*\n'
        reprString += 'Instance class       : %s\n' % self.__class__.__name__
        reprString += 'Instance name        : %s\n' % self.name
        reprString += 'Actions              : %d\n' % self.order
        reprString += 'Criteria             : %d\n' % len(self.criteria)
        reprString += 'Size                 : %d\n' % self.computeSize()
        try:
            oppDeg = self.computeOppositeness(InPercents=True)
            reprString += 'Oppositeness (%%)    : %.2f\n' % (oppDeg['oppositeness'])
        except:
            pass
        try:
            if self.distribution == 'beta':
                reprString += 'Uncertainty model  : %s(a=%.1f,b=%.1f)\n' %\
                    (self.distribution,self.betaParameter,self.betaParameter)
            else:
                reprString += 'Uncertainty model    : %s(a=%s,b=%s)\n' %\
                             (self.distribution,'0','2w') 
            reprString += 'Likelihood domain    : [-1.0;+1.0]\n'
            reprString += 'Confidence level     : %.2f (%.1f%%)\n' %\
                         (self.bipolarConfidenceLevel,\
                         (self.bipolarConfidenceLevel+1.0)/2.0*100.0)
            reprString += 'Confident majority   : %.2f (%.1f%%)\n' %\
                (self.confidenceCutLevel,\
                (self.confidenceCutLevel+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0'))
        except:
            pass
        reprString += 'Determinateness (%%)  : %.2f\n' %\
                      self.computeDeterminateness(InPercents=True)
        reprString += 'Valuation domain     : [%.2f;%.2f]\n' \
            % (self.valuationdomain['min'],self.valuationdomain['max'])
        #reprString += 'Valuation domain : %s\n' % str(self.valuationdomain)
        reprString += 'Attributes           : %s\n' % list(self.__dict__.keys())
        val1 = self.runTimes['totalTime']
        val2 = self.runTimes['dataInput']
        val3 = self.runTimes['computeRelation']
        val4 = self.runTimes['gammaSets']
        reprString += '----  Constructor run times (in sec.) ----\n'
        try:
            if self.nbrThreads > 1:
                reprString += 'Threads          : %d\n' % self.nbrThreads
                reprString += 'Start method     : %s\n' % self.startMethod
        except:
            pass
        reprString += 'Total time       : %.5f\n' % val1
        reprString += 'Data input       : %.5f\n' % val2
        reprString += 'Compute relation : %.5f\n' % val3
        reprString += 'Gamma sets       : %.5f\n' % val4
        return reprString
    
    def __init__(self,argPerfTab=None,
                 objectivesSubset=None,
                 criteriaSubset=None,
                 coalition=None,
                 actionsSubset=None,
                 hasNoVeto=False,
                 hasBipolarVeto=True,
                 Normalized=True,
                 ndigits=4,
                 CopyPerfTab=True,
                 BigData=False,
                 Threading=False,
                 startMethod=None,
                 tempDir=None,
                 WithConcordanceRelation=True,
                 WithVetoCounts=True,
                 nbrCores=None,
                 Debug=False,Comments=False):
        from copy import deepcopy
        from time import time
        #from digraphsTools import omax, omin

        # set initial time stamp
        tt = time()

        # ----  performance tableau data input 
        if argPerfTab is None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab

        # set Threading parameters
        if Threading:
            WithConcordanceRelation = False
            WithVetoCounts = False

            
        # transfering the performance tableau data to self
        self.name = 'rel_' + perfTab.name
        # actions
        if actionsSubset is None:
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
           
        # valuation domain
        self.ndigits=ndigits
        if Normalized:
            Min =   Decimal('-1.0')
            Med =   Decimal('0.0')
            Max =   Decimal('1.0')
        else:
            Min =   Decimal('-100.0')
            Med =   Decimal('0.0')
            Max =   Decimal('100.0')
        self.valuationdomain = {'min':Min,
                                'med':Med,
                                'max':Max,
                                'hasIntegerValuation':False}
        try:
            self.valuationdomain['precision'] = \
                           perfTab.valuationPrecision
        except:
            self.valuationdomain['precision'] = \
                           Decimal('1')/Decimal(str(ndigits))
            
        # objectives
        if objectivesSubset is None:
            try:
                if CopyPerfTab:
                    self.objectives = deepcopy(perfTab.objectives)
                else:
                    self.objectives = perfTab.objectives
            except:
                pass
        else:
            objectives = OrderedDict()
            for obj in objectivesSubset:
                if CopyPerfTab:
                    objectives[obj] = deepcopy(perfTab.objectives[obj])
                else:
                    objectives[obj] = perfTab.objectives[obj]
            self.objectives = objectives
                
        # criteria coalition
        if criteriaSubset is None and objectivesSubset is None and coalition is None:
            if CopyPerfTab:
                self.criteria = deepcopy(perfTab.criteria)
            else:
                self.criteria = perfTab.criteria
        else:
            criteria = OrderedDict()
            if criteriaSubset is None:
                if objectivesSubset is None and coalition is None:
                    if criteriaSubset is None:
                        coalition = list(perfTab.criteria.keys())
                    else:
                        coalition = criteriaSubset

                elif objectivesSubset is not None and coalition is None:
                    coalition = []
                    for obj in objectivesSubset:
                        objCrit = self.objectives[obj]['criteria']
                        coalition += objCrit
                elif objectivesSubset is not None and coalition is not None:
                    print('Error: Objectives Subset and coalition given')
                    return
                else:
                    for g in coalition:
                        if CopyPerfTab:
                            criteria[g] = deepcopy(perfTab.criteria[g])
                        else:
                            criteria[g] = perfTab.criteria[g]
            else:
                for g in criteriaSubset:
                    if CopyPerfTab:
                        criteria[g] = deepcopy(perfTab.criteria[g])
                    else:
                        criteria[g] = perfTab.criteria[g]
            self.criteria = criteria
        # convert criteria weights to Decimal format    
        criteria = OrderedDict()
        if objectivesSubset is None:
            if coalition is None:
                if criteriaSubset is None:
                    coalition = list(perfTab.criteria.keys())
                else:
                    coalition = criteriaSubset
        else:
            coalition = []
            for obj in objectives:
                objCrit = self.objectives[obj]['criteria']
                coalition += objCrit

        for g in coalition:
            if CopyPerfTab:
                criteria[g] = deepcopy(perfTab.criteria[g])
            else:
                criteria[g] = perfTab.criteria[g]
                    
        self.criteria = criteria
        self.convertWeight2Decimal()

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
            self.NA = deepcopy(perfTab.NA)
        else:
            self.evaluation = perfTab.evaluation
            self.NA = perfTab.NA
        if not BigData:
            self.convertEvaluation2Decimal()
        try:
            if CopyPerfTab:
                self.description = deepcopy(perfTab.description)
            elif not BigData:
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
                                                startMethod=startMethod,\
                                                tempDir=tempDir,\
                                                WithConcordanceRelation=WithConcordanceRelation,\
                                                WithVetoCounts=WithVetoCounts,\
                                                nbrCores=nbrCores,\
                                                Debug=Debug,Comments=Comments)

        # rounding up to ndigits
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        self.recodeValuation(Min,Max,ndigits)
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
        
    def computeCriterionRelation(self,c,a,b,hasSymmetricThresholds=True):
        """
        Compute the outranking characteristic for actions x and y
        on criterion c.
        """
        criteria = self.criteria
        evaluation = self.evaluation
        NA = self.NA
        if a == b:
            return Decimal("1.0")
        else:

            if self.evaluation[c][a] != NA and self.evaluation[c][b] != NA:		
                try:
                    indx = criteria[c]['thresholds']['ind'][0]
                    indy = criteria[c]['thresholds']['ind'][1]
                    if hasSymmetricThresholds:
                        ind = indx +indy * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        ind = indx +indy * abs(evaluation[c][a])
                except:
                    ind = None
                try:
                    wpx = criteria[c]['thresholds']['weakPreference'][0]
                    wpy = criteria[c]['thresholds']['weakPreference'][1]
                    if hasSymmetricThresholds:
                        wp = wpx + wpy * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        wp = wpx + wpy * abs(evaluation[c][a])
                except:
                    wp = None
                try:
                    px = criteria[c]['thresholds']['pref'][0]
                    py = criteria[c]['thresholds']['pref'][1]
                    if hasSymmetricThresholds:
                        p = px + py * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        p = px + py * abs(evaluation[c][a]) 
                except:
                    p = None
                if self.criteria[c]['weight'] > Decimal("0.0"):
                    d = evaluation[c][a] - evaluation[c][b]
                else:
                    d = evaluation[c][b] - evaluation[c][a]

                return self._localConcordance(d,ind,wp,p)

            else:
                return Decimal("0.0")
            
    def _constructRelationWithThreading(self,criteria,
                           evaluation,
                           initial=None,
                           terminal=None,
                           hasNoVeto=False,
                           hasBipolarVeto=True,
                           Debug=False,
                           hasSymmetricThresholds=True,
                           Threading=False,
                            startMethod=None,
                           tempDir=None,
                           WithConcordanceRelation=True,
                           WithVetoCounts=True,
                           nbrCores=None,Comments=False):
        """
        Specialization of the corresponding BipolarOutrankingDigraph method
        """
        from multiprocessing import cpu_count
        
        ##
        
        if not Threading or cpu_count() < 2:
            # set threading parameter
            if Comments:
                print('Computing without threading ...')
            self.nbrThreads = 1

            # !! concordance relation and veto counts need a complex constructor
            if (not hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
                constructRelation = self._constructRelation
            else:
                constructRelation = self._constructRelationSimple

            return constructRelation(criteria,\
                                    evaluation,\
                                    initial=initial,\
                                    terminal=terminal,\
                                    hasNoVeto=hasNoVeto,\
                                    hasBipolarVeto=hasBipolarVeto,\
                                    WithConcordanceRelation=WithConcordanceRelation,\
                                    WithVetoCounts=WithVetoCounts,\
                                    Debug=Debug,\
                                    hasSymmetricThresholds=hasSymmetricThresholds)
        ##
        else:  # parallel computation
            from copy import copy, deepcopy
            from io import BytesIO
            from pickle import Pickler, dumps, loads, load
            # setting default start method
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            Process = mpctx.Process
            active_children = mpctx.active_children
            cpu_count = mpctx.cpu_count
            self.startMethod = mpctx.get_start_method()
 
            if Comments:
                print('Threading ...')
                print(startMethod)
            from tempfile import TemporaryDirectory
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                from copy import copy, deepcopy

##                #selfDp = copy(self)
##                selfFileName = tempDirName +'/dumpSelf.py'
##                if Debug:
##                    print('temDirName, selfFileName', tempDirName,selfFileName)
##                fo = open(selfFileName,'wb')
##                fo.write(dumps(self,-1))
##                fo.close()

                if nbrCores is None:
                    nbrCores = cpu_count()
                if Comments:
                    print('Nbr of cpus = ',nbrCores)
                # set number of threads
                self.nbrThreads = nbrCores

                ni = len(initial)
                nt = len(terminal)
                if ni < nt:
                    n = ni
                    actions2Split = list(initial)
                    InitialSplit = True
                else:
                    n = nt
                    actions2Split = list(terminal)
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
                    splitActions=[]
                    for k in range(nit):
                        if j < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = list(actionsRemain)
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
                    splitThread = _myBODGThread(target=j,
                                            args=(self,
                                                  InitialSplit,
                                                  tempDirName,splitActions,
                                                  hasNoVeto,hasBipolarVeto,
                                                  hasSymmetricThresholds,Debug))
                    splitThread.start()
                    
                while active_children() != []:
                    pass

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

    def _constructRelationSimple(self,criteria,
                           evaluation,
                           initial=None,
                           terminal=None,
                           hasNoVeto=False,
                           hasBipolarVeto=True,
                           WithConcordanceRelation=False,
                           WithVetoCounts=False,
                           hasSymmetricThresholds=True,
                           Debug=False):
        """
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        Parameters:
            * PerfTab.criteria, PerfTab.evaluation,
            * inital nodes, terminal nodes, for restricted purposes 
            
        """
        ## default setting for digraphs
        if initial is None:
            initial = self.actions
        if terminal is None:
            terminal = self.actions
        
##        totalweight = Decimal('0.0')
##        for c in dict.keys(criteria):
##            totalweight = totalweight + criteria[c]['weight']
        totalweight = sum(abs(crit['weight']) for crit in criteria.values())

        relation = {}
        vetos = []
        negativeVetos = []
        
        #nc = len(criteria)
        NA = self.NA
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        for a in initial:
            relation[a] = {}
            ra = relation[a]
            for b in terminal:
                if a == b:
                    ra[b] = Med
                else:
                    concordance = Decimal('0.0')
                    veto = {}
                    abvetos=[]
                    negativeVeto = {}
                    abNegativeVetos=[]

                    for c,crit in criteria.items():
                        evalca = evaluation[c][a]
                        evalcb = evaluation[c][b]
                        maxAB = max(abs(evalca),abs(evalcb))
                        
                        if evalca != NA and evalcb != NA:		
                            try:
                                indx = crit['thresholds']['ind'][0]
                                indy = crit['thresholds']['ind'][1]
                                ind = indx +indy * maxAB
                            except KeyError:
                                ind = None
                            try:
                                wpx = crit['thresholds']['weakPreference'][0]
                                wpy = crit['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * maxAB
                                else:
                                    wp = wpx + wpy * abs(evalca) 
                            except KeyError:
                                wp = None
                            try:
                                px = crit['thresholds']['pref'][0]
                                py = crit['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = px + py * maxAB
                                else:
                                    p = px + py * abs(evalca) 
                            except KeyError:
                                p = None
                            if crit['weight'] > Decimal('0.0'):
                                d = evalca - evalcb
                            else:
                                d = evalcb - evalca
                            lc0 = self._localConcordance(d,ind,wp,p)
                            ## print 'c,a,b,d,ind,wp,p,lco = ',c,a,b,d, ind,wp,p,lc0
                            concordance = concordance + (lc0 * abs(crit['weight']))
                            try:
                                wvx = crit['thresholds']['weakVeto'][0]
                                wvy = crit['thresholds']['weakVeto'][1]
                                if hasNoVeto:
                                    wv = None
                                else:
                                    if hasSymmetricThresholds:
                                        wv = wvx + wvy * maxAB
                                    else:
                                        wv = wvx + wvy * abs(evalca)
                            except KeyError:
                                wv = None
                            try:
                                vx = crit['thresholds']['veto'][0]
                                vy = crit['thresholds']['veto'][1]
                                v = vx + vy * maxAB
                            except KeyError:
                                v = None
                            veto[c] = (self._localVeto(d,wv,v),d,wv,v)
                            if veto[c][0] > Decimal('-1.0'):
                                abvetos.append((c,veto[c]))
                            
                            negativeVeto[c] = (self._localNegativeVeto(d,wv,v),d,wv,v)
                            if negativeVeto[c][0] > Decimal('-1.0'):
                                abNegativeVetos.append((c,negativeVeto[c]))
                        else:
                            concordance = concordance + Decimal('0.0') * crit['weight']
                            veto[c] = (Decimal('-1.0'),None,None,None)
                            negativeVeto[c] = (Decimal('-1.0'),None,None,None)
                                
                    concordindex = concordance / totalweight                 
                    
                    ## init vetoes lists and indexes
                    abVetoes=[]
                    abNegativeVetoes=[]

                    #  contradictory vetoes
                    
                    for c in criteria.keys():
                        if veto[c][0] >= Decimal('0'):
                            abVetoes.append((c,veto[c]))
                        if negativeVeto[c][0] >= Decimal('0'):
                            abNegativeVetoes.append((c,negativeVeto[c]))
                    if not hasNoVeto:                     
                        vetoes = [-veto[c][0] for c in veto if veto[c][0] > Decimal('-1')]
                        negativeVetoes = [negativeVeto[c][0] for c in negativeVeto\
                                          if negativeVeto[c][0] > Decimal('-1')]
                    else:
                        vetoes = []
                        negativeVetoes = []
                    
##                    if Debug:
##                        print('vetoes = ', vetoes)
##                        print('negativeVetoes = ', negativeVetoes)
                    omaxList = [concordindex] + vetoes + negativeVetoes
                    outrankindex = omax(Med,omaxList,Debug=Debug)
                                                                 
                    if abVetoes != []:
                        vetos.append(([a,b,concordindex*Max],abVetoes))
                    if abNegativeVetoes != []:
                        negativeVetos.append(([a,b,concordindex*Max],abNegativeVetoes))
                    ra[b] = outrankindex*Max

        # return outranking relation    

        return relation


    def _constructRelation(self,criteria,
                           evaluation,
                           initial=None,
                           terminal=None,
                           hasNoVeto=False,
                           hasBipolarVeto=True,
                           WithConcordanceRelation=True,
                           WithVetoCounts=True,
                           Debug=False,
                           hasSymmetricThresholds=True):
        """
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        Parameters:
            * PerfTab.criteria, PerfTab.evaluation,
            * inital nodes, terminal nodes, for restricted purposes 

        Flags:
            * hasNoVeto = True inhibits taking into account large performances differences
            * hasBipolarVeto = False allows to revert (if False) to standard Electre veto handling
            
        """
        from digraphsTools import omax,omin
        ## default setting for digraphs
        if initial is None:
            initial = self.actions
        if terminal is None:
            terminal = self.actions
        
##        totalweight = Decimal('0.0')
##        for c in dict.keys(criteria):
##            totalweight = totalweight + criteria[c]['weight']
        totalweight = sum(abs(criteria[c]['weight']) for c in criteria)

        relation = {}
        concordanceRelation = {}
        vetos = []

        if hasBipolarVeto:
            negativeVetos = []

        largePerformanceDifferencesCount = {}        
        for a in initial:
            largePerformanceDifferencesCount[a] = {}
            lpda = largePerformanceDifferencesCount[a]
            for b in terminal:
                lpda[b] = {'positive':0,'negative':0}

        
        #nc = len(criteria)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        NA = self.NA
        for a in initial:
            relation[a] = {}
            ra = relation[a]
            concordanceRelation[a] = {}
            crda = concordanceRelation[a]
            for b in terminal:
                if a == b:
                    ra[b] = Med
                    crda[b] = Decimal('0.0')
                else:
                    
                    concordance = Decimal('0.0')

                    veto = {}
                    abvetos=[]

                    if hasBipolarVeto:
                        negativeVeto = {}
                        abNegativeVetos=[]

                    for c,crit in criteria.items():
                        evalca = evaluation[c][a]
                        evalcb = evaluation[c][b]
                        maxAB = max(abs(evalca),abs(evalcb))
                        if evalca != NA and evalcb != NA:		
                            try:
                                indx = crit['thresholds']['ind'][0]
                                indy = crit['thresholds']['ind'][1]
                                ind = indx +indy * maxAB
                            except KeyError:
                                ind = None
                            try:
                                wpx = crit['thresholds']['weakPreference'][0]
                                wpy = crit['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * maxAB
                                else:
                                    wp = wpx + wpy * abs(evalca) 
                            except KeyError:
                                wp = None
                            try:
                                px = crit['thresholds']['pref'][0]
                                py = crit['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = px + py * maxAB
                                else:
                                    p = px + py * abs(evalca) 
                            except KeyError:
                                p = None
                            if crit['weight'] > Decimal('0.0'):
                                d = evalca - evalcb
                            else:
                                d = evalcb - evalca
                            lc0 = self._localConcordance(d,ind,wp,p)
                            ## print 'c,a,b,d,ind,wp,p,lco = ',c,a,b,d, ind,wp,p,lc0
                            concordance = concordance + (lc0 * abs(crit['weight']))
                            try:
                                wvx = crit['thresholds']['weakVeto'][0]
                                wvy = crit['thresholds']['weakVeto'][1]
                                if hasNoVeto:
                                    wv = None
                                else:
                                    if hasSymmetricThresholds:
                                        wv = wvx + wvy * maxAB
                                    else:
                                        wv = wvx + wvy * abs(evalca)
                            except KeyError:
                                wv = None
                            try:
                                vx = crit['thresholds']['veto'][0]
                                vy = crit['thresholds']['veto'][1]
                                if hasNoVeto:
                                    v = None
                                else:
                                    if hasSymmetricThresholds:
                                        v = vx + vy * maxAB
                                    else:
                                        v = vx + vy * abs(evalca)
                            except KeyError:
                                v = None
                            veto[c] = (self._localVeto(d,wv,v),d,wv,v)
                            if veto[c][0] > Decimal('-1.0'):
                                abvetos.append((c,veto[c]))
                                largePerformanceDifferencesCount[a][b]['negative'] -= 1
                            ## if d < -wv:
                            ##     print 'd,wv,v,veto[c]',d,wv,v,veto[c]
                            if hasBipolarVeto:
                                negativeVeto[c] = (self._localNegativeVeto(d,wv,v),d,wv,v)
                                if negativeVeto[c][0] > Decimal('-1.0'):
                                    abNegativeVetos.append((c,negativeVeto[c]))
                                    largePerformanceDifferencesCount[a][b]['positive'] += 1
                                ## if d > wv:
                                ##     print 'd,wv,v,negativeVeto[c]',d,wv,v,negativeVeto[c] 
                        else:
                            concordance = concordance + Decimal('0.0') * crit['weight']
                            veto[c] = (Decimal('-1.0'),None,None,None)
                            if hasBipolarVeto:
                                negativeVeto[c] = (Decimal('-1.0'),None,None,None)
                                
                    if totalweight != Decimal('0.0'):
                        concordindex = concordance / totalweight
                    else:
                        concordindex = concordance
                    crda[b] = concordindex
                    
                    ## init vetoes lists and indexes
                    abVetoes=[]
                    abNegativeVetoes=[]

                    #  contradictory vetoes
                    
                    for c in criteria.keys():
                        if veto[c][0] >= Decimal('0'):
                            abVetoes.append((c,veto[c]))
                        if hasBipolarVeto:
                            if negativeVeto[c][0] >= Decimal('0'):
                                abNegativeVetoes.append((c,negativeVeto[c]))
                                         
                    if hasBipolarVeto:
                        vetoes = [-veto[c][0] for c in veto if veto[c][0] > Decimal('-1')]
                        negativeVetoes = [negativeVeto[c][0] for c in negativeVeto if negativeVeto[c][0] > Decimal('-1')]
                        if Debug:
                            print('vetoes = ', vetoes)
                            print('negativeVetoes = ', negativeVetoes)
                        omaxList = [concordindex] + vetoes + negativeVetoes
                        outrankindex = omax(Med,omaxList,Debug=Debug)
                        if Debug:
                            print('a b outrankindex = ', a,b, outrankindex)
                    else:
                        # hasBipolarVeto == False
                        vetoIndex = Decimal('-1.0')
                        for c in criteria:
                            vetoIndex = max(vetoIndex,veto[c][0])
                        outrankindex = min(concordindex,-vetoIndex)
                                                                 
                    if abVetoes != []:
                        vetos.append(([a,b,concordindex*Max],abVetoes))
                    if hasBipolarVeto:
                        if abNegativeVetoes != []:
                            negativeVetos.append(([a,b,concordindex*Max],abNegativeVetoes))
                    ra[b] = outrankindex*Max

        # storing concordance relation and vetoes
        if WithConcordanceRelation:
            self.concordanceRelation = concordanceRelation
        if WithVetoCounts:
            self.vetos = vetos
            if hasBipolarVeto:
                self.negativeVetos = negativeVetos
                self.largePerformanceDifferencesCount = largePerformanceDifferencesCount

        # return outranking relation    

        return relation


    
    def criterionCharacteristicFunction(self,c,a,b,hasSymmetricThresholds=True):
        """
        Renders the characteristic value of the comparison of a and b on criterion c.
        """
        evalca = self.evaluation[c][a]
        evalcb = self.evaluation[c][b]
        maxAB = max(abs(evalca),abs(evalcb))
        crit = self.criteria[c]
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        NA = self.NA
        if evalca != NA and evalcb != NA:		
            try:
                indx = crit['thresholds']['ind'][0]
                indy = crit['thresholds']['ind'][1]
                if hasSymmetricThresholds:
                    ind = indx +indy * maxAB
                else:
                    ind = indx +indy * abs(evalca)
            except:
                ind = None
            try:
                wpx = crit['thresholds']['weakPreference'][0]
                wpy = crit['thresholds']['weakPreference'][1]
                if hasSymmetricThresholds:
                    wp = wpx + wpy * maxAB
                else:
                    wp = wpx + wpy * abs(evalca)
            except:
                wp = None
            try:
                px = crit['thresholds']['pref'][0]
                py = crit['thresholds']['pref'][1]
                if hasSymmetricThresholds:
                    p = px + py * maxAB
                else:
                    p = px + py * abs(evalca)
            except:
                p = None
            if crit['weight'] > Decimal('0.0'):
                d = evalca - evalcb
            else:
                d = evalcb - evalca
            return self._localConcordance(d,ind,wp,p)
        else:
            return Decimal('0.0')

    def computeSingleCriteriaNetflows(self):
        """
        renders the Promethee single criteria netflows matrix M
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        n = len(actionsList)
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        matrixM = {}
        for a in actionsList:
            matrixM[a] = {}
            for c in criteriaList:
                netflow= Decimal('0.0')
                for b in actionsList:
                    if a != b:
                        cab = self.criterionCharacteristicFunction(c,a,b)
                        cba = self.criterionCharacteristicFunction(c,b,a)
                        netflow += cab - cba
                netflow = float(netflow)/float(n-1)
                matrixM[a][c] = netflow
        return matrixM
    
    def saveSingleCriterionNetflows(self,fileName='tempnetflows.prn',delimiter=' ',Comments=True):
        """
        Delimited save of single criteria netflows matrix
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        M = self.computeSingleCriteriaNetflows()
        fo = open(fileName,'w')
        for a in actionsList:
            for c in criteriaList:
                fo.write('%2.2f ' % (M[a][c]))
            fo.write('\n')
        fo.close()
        if Comments:
            print('Single Criteria Netflows saved on file %s' % (fileName))
        
    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters: d := diff observed, wp := weak preference threshold,
        ind := indiffrence threshold, p := prefrence threshold.
        Renders the concordance index per criteria (-1,0,1)
        """
        if p is not None:
            if   d <= -p:
                return Decimal('-1.0')
            elif ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                if d < Decimal('0.0'):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')
        else:
            if ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            else:
                if d < Decimal("0.0"):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')                
            

    def _localVeto(self, d, wv, v):
        """
        Parameters:
            d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local veto state (-1,0,1).

        """
        if v is not None:
            if  d <= - v:
                return Decimal('1.0')
            elif wv is not None:
                if d <= - wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d <= -wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')

    def _localNegativeVeto(self, d, wv, v):
        """
        Parameters:
            d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local negative veto state (-1,0,1).

        """
        if v is not None:
            if  d >= v:
                return Decimal('1.0')
            elif wv is not None:
                if d >= wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d >= wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')

class _BipolarOutrankingDigraph(OutrankingDigraph):
    """
    Specialization of the abstract OutrankingDigraph root class for generating
    bipolarly-valued outranking digraphs.

    Parameters:
        * argPerfTab: instance of PerformanceTableau class.
          If a file name string is given, the performance tableau will directly be loaded first.
        * coalition: subset of criteria to be used for contruction the outranking digraph.
        * hasNoVeto: veto desactivation flag (False by default).
        * hasBipolarVeto: bipolar versus electre veto activation (true by default).
        * Normalized: the valuation domain is set by default to [-100,+100] (bipolar percents).
          If True, the valuation domain is recoded to [-1.0,+1.0].
        * WithConcordanceRelation: True by default when not threading.
          The self.concordanceRelation contains the significance majority margin of the "at least as good relation as"
          without the large performance difference polarization.
        * WithVetoCounts: True by default when not threading. All vetos and countervetos
          are stored in self.vetos and self.negativeVetos slots,
          as well the counts of large performance differences in self.largePerformanceDifferencesCount slot.
        * Threading: False by default. Allows to profit from SMP machines via the Python multiprocessing module.
        * nbrCores: controls the maximal number of cores that will be used in the multiprocessing phases.
          If None is given, the os.cpu_count method is used in order to determine the number of availble cores on the SMP machine.

    .. warning::

        If Threading is True, WithConcordanceRelation and WithVetoCounts flags are automatically set both to False.
        Removing this limitation is on the todo list and will be done soon.
       
    """
    def __init__(self,argPerfTab=None,
                 coalition=None,
                 hasNoVeto=False,
                 hasBipolarVeto=True,
                 Normalized=False,
                 CopyPerfTab=True,
                 Threading=False,
                 WithConcordanceRelation=True,
                 WithVetoCounts=True,
                 nbrCores=None,
                 Debug=False,Comments=False):
        from copy import deepcopy 
        if argPerfTab is None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab

        # set Threading parameters
        if Threading:
            WithConcordanceRelation = False
            WithVetoCounts = False
            
        #self.performanceTableau = perfTab

        self.name = 'rel_' + perfTab.name

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
        if Normalized:
            Min =   Decimal('-1.0')
            Med =   Decimal('0.0')
            Max =   Decimal('1.0')
        else:
            Min =   Decimal('-100.0')
            Med =   Decimal('0.0')
            Max =   Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}

        if coalition is None:
            try:
                if CopyPerfTab:
                    self.objectives = deepcopy(perfTab.objectives)
                else:
                    self.objectives = perfTab.objectives
            except:
                pass
            if CopyPerfTab:
                self.criteria = deepcopy(perfTab.criteria)
            else:
                self.criteria = perfTab.criteria
            
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
            self.criteria = criteria
        self.convertWeight2Decimal()
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
        self.convertEvaluation2Decimal()
        try:
            if CopyPerfTab:
                self.description = deepcopy(perfTab.description)
            else:
                self.description = perfTab.description
        except:
            pass
        # init general digraph Data
        self.order = len(self.actions)
        
        # construct outranking relation
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
                                                WithConcordanceRelation=WithConcordanceRelation,\
                                                WithVetoCounts=WithVetoCounts,\
                                                nbrCores=nbrCores,\
                                                Debug=Debug,Comments=Comments)

##        if Normalized:
##            self.recodeValuation(-1.0,1.0)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeCriterionRelation(self,c,a,b,hasSymmetricThresholds=True):
        """
        Compute the outranking characteristic for actions x and y
        on criterion c.
        """
        criterion = self.criteria[c]
        evaluation = self.evaluation
        NA = self.NA
        if a == b:
            return Decimal("1.0")
        else:

            if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                try:
                    indx = criterion['thresholds']['ind'][0]
                    indy = criterion['thresholds']['ind'][1]
                    if hasSymmetricThresholds:
                        ind = indx +indy * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        ind = indx +indy * abs(evaluation[c][a])
                except:
                    ind = None
                try:
                    wpx = criterion['thresholds']['weakPreference'][0]
                    wpy = criterion['thresholds']['weakPreference'][1]
                    if hasSymmetricThresholds:
                        wp = wpx + wpy * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        wp = wpx + wpy * abs(evaluation[c][a])
                except:
                    wp = None
                try:
                    px = self.criteria[c]['thresholds']['pref'][0]
                    py = self.criteria[c]['thresholds']['pref'][1]
                    if hasSymmetricThresholds:
                        p = px + py * max(abs(evaluation[c][a]), abs(evaluation[c][b]))
                    else:
                        p = px + py * abs(evaluation[c][a]) 
                except:
                    p = None
                if self.criteriion['weight'] > Decimal('0.0'):
                    d = evaluation[c][a] - evaluation[c][b]
                else:
                    d = evaluation[c][b] - evaluation[c][a]
                return self._localConcordance(d,ind,wp,p)

            else:
                return Decimal("0.0")
            
    def _constructRelationWithThreading(self,criteria,
                           evaluation,
                           initial=None,
                           terminal=None,
                           hasNoVeto=False,
                           hasBipolarVeto=True,
                           Debug=False,
                           hasSymmetricThresholds=True,
                           Threading=False,
                           WithConcordanceRelation=True,
                           WithVetoCounts=True,
                           nbrCores=None,Comments=False):
        """
        Specialization of the corresponding BipolarOutrankingDigraph method
        """
        from multiprocessing import cpu_count
        
        ##
        if not Threading or cpu_count() < 6:
            return self._constructRelation(criteria,\
                                    evaluation,\
                                    initial=initial,\
                                    terminal=terminal,\
                                    hasNoVeto=hasNoVeto,\
                                    hasBipolarVeto=hasBipolarVeto,\
                                    WithConcordanceRelation=WithConcordanceRelation,\
                                    WithVetoCounts=WithVetoCounts,\
                                    Debug=Debug,\
                                    hasSymmetricThresholds=hasSymmetricThresholds)
        ##
        else:  # parallel computation
            from copy import copy, deepcopy
            from io import BytesIO
            from pickle import Pickler, dumps, loads, load
            #from multiprocessing import Process, Lock,\
            #                            active_children, cpu_count
            import multiprocessing as mp
            if startMethod is None:
                startMethod = 'spawn'
            mpctx = mp.get_context(startMethod)
            Process = mpctx.Process
            active_children = mpctx.active_children
            cpu_count = mpctx.cpu_count

            #Debug=True
            class myThread(Process):
                def __init__(self, threadID,
                             InitialSplit, tempDirName,
                             hasNoVeto, hasBipolarVeto,
                             hasSymmetricThresholds, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.InitialSplit = InitialSplit
                    self.workingDirectory = tempDirName
                    self.hasNoVeto = hasNoVeto
                    self.hasBipolarVeto = hasBipolarVeto,
                    hasSymmetricThresholds = hasSymmetricThresholds,
                    self.Debug = Debug
                def run(self):
                    from io import BytesIO
                    from pickle import Pickler, dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
                    if Debug:
                        print("Starting working in %s on thread %s" %\
                              (self.workingDirectory, str(self.threadId)))
                    fi = open('dumpSelf.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    fiName = 'splitActions-'+str(self.threadID)+'.py'
                    fi = open(fiName,'rb')
                    splitActions = loads(fi.read())
                    fi.close()
                    foName = 'splitRelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    if self.InitialSplit:
                        splitRelation = BipolarOutrankingDigraph._constructRelation(
                                            digraph,digraph.criteria,
                                            digraph.evaluation,
                                            initial=splitActions,
                                            hasNoVeto=hasNoVeto,
                                            hasBipolarVeto=hasBipolarVeto,
                                            WithConcordanceRelation=False,
                                            WithVetoCounts=False,
                                            Debug=False,
                                            hasSymmetricThresholds=hasSymmetricThresholds)
                    else:
                        splitRelation = BipolarOutrankingDigraph._constructRelation(digraph,digraph.criteria,\
                                            digraph.evaluation,
                                            terminal=splitActions,
                                            hasNoVeto=hasNoVeto,
                                            hasBipolarVeto=hasBipolarVeto,
                                            WithConcordanceRelation=False,
                                            WithVetoCounts=False,
                                            Debug=False,
                                            hasSymmetricThresholds=hasSymmetricThresholds)
                    buff = BytesIO()
                    pickler = Pickler(buff, -1)
                    pickler.fast = 1
                    pickler.dump(splitRelation)
                    buff.flush()
                    fo.write(buff.getvalue())
                    fo.close()
                # .......
             
            if Comments:
                print('Threading ...')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                from copy import copy, deepcopy
                #selfDp = copy(self)
                selfFileName = tempDirName +'/dumpSelf.py'
                if Debug:
                    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                pd = dumps(self,-1)
                fo.write(pd)
##                buff = BytesIO()
##                pickler = Pickler(buff, -1)
##                pickler.fast = 1
##                pickler.dump(self)
##                buff.flush()
##                fo.write(buff.getvalue())
                fo.close()

                if nbrCores is None:
                    nbrCores = cpu_count()-1
                if Comments:
                    print('Nbr of cpus = ',nbrCores)

                ni = len(initial)
                nt = len(terminal)
                if ni < nt:
                    n = ni
                    actions2Split = list(initial)
                    InitialSplit = True
                else:
                    n = nt
                    actions2Split = list(terminal)
                    InitialSplit = False
                if Debug:
                    print('InitialSplit, actions2Split', InitialSplit, actions2Split)
            
                nit = n//nbrCores
                nbrOfJobs = nbrCores
                if nit*nbrCores < n:
                    nit += 1
                while nit*(nbrOfJobs-1) >= n:
                    nbrOfJobs -= 1
                if Debug:
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
                for j in range(nbrOfJobs):
                    if Comments:
                        print('Thread = %d/%d' % (j+1,nbrOfJobs),end=" ")
                    splitActions=[]
                    for k in range(nit):
                        if j < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = list(actionsRemain)
                        i += 1
                    if Comments:
                        print(len(splitActions))
                    if Debug:
                        print(splitActions)
                    actionsRemain = actionsRemain - set(splitActions)
                    if Debug:
                        print(actionsRemain)
                    foName = tempDirName+'/splitActions-'+str(j)+'.py'
                    fo = open(foName,'wb')
                    spa = dumps(splitActions,-1)
                    fo.write(spa)
##                    buff = BytesIO()
##                    pickler = Pickler(buff, -1)
##                    pickler.fast = 1
##                    pickler.dump(splitActions)
##                    buff.flush()
##                    fo.write(buff.getvalue())
                    fo.close()

                    fo.close()
                    splitThread = myThread(j,InitialSplit,
                                           tempDirName,hasNoVeto,hasBipolarVeto,
                                           hasSymmetricThresholds,Debug)
                    splitThread.start()
                    
                while active_children() != []:
                    pass

                if Comments:    
                    print('Exiting computing threads')
                for j in range(nbrOfJobs):
                    #print('Post job-%d/%d processing' % (j+1,nbrOfJobs))
                    if Debug:
                        print('job',j)
                    fiName = tempDirName+'/splitActions-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitActions = loads(fi.read())
                    if Debug:
                        print('splitActions',splitActions)
                    fi.close()
                    fiName = tempDirName+'/splitRelation-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitRelation = loads(fi.read())
                    if Debug:
                        print('splitRelation',splitRelation)
                    fi.close()

                    #relation.update(splitRelation)
                    from itertools import product
                    if InitialSplit:
                        for x,y in product(splitActions,terminal):
                        #for x in splitActions:
                        #    for y in terminal:
                            relation[x][y] = splitRelation[x][y]
                    else:
                        for x,y in product(initial,splitActions):
                        #for x in initial:
                        #    for y in splitActions:
                            relation[x][y] = splitRelation[x][y]   
                return relation

    def _constructRelation(self,criteria,
                           evaluation,
                           initial=None,
                           terminal=None,
                           hasNoVeto=False,
                           hasBipolarVeto=True,
                           WithConcordanceRelation=True,
                           WithVetoCounts=True,
                           Debug=False,
                           hasSymmetricThresholds=True):
        """
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        Parameters:
            * PerfTab.criteria, PerfTab.evaluation,
            * inital nodes, terminal nodes, for restricted purposes 

        Flags:
            * hasNoVeto = True inhibits taking into account large performances differences
            * hasBipolarVeto = False allows to revert (if False) to standard Electre veto handling
            
        """
        ## default setting for digraphs
        if initial is None:
            initial = self.actions
        if terminal is None:
            terminal = self.actions
        
##        totalweight = Decimal('0.0')
##        for c in dict.keys(criteria):
##            totalweight = totalweight + criteria[c]['weight']
        totalweight = sum([abs(criteria[c]['weight']) for c in criteria])
        relation = {}
        concordanceRelation = {}
        vetos = []

        if hasBipolarVeto:
            negativeVetos = []
    
        largePerformanceDifferencesCount = {}        
        for a in initial:
            largePerformanceDifferencesCount[a] = {}
            for b in terminal:
                largePerformanceDifferencesCount[a][b] = {'positive':0,'negative':0}

        Max = self.valuationdomain['max']                                             
        Med = self.valuationdomain['med']
        NA = self.NA
        for a in initial:
            relation[a] = {}
            concordanceRelation[a] = {}
            for b in terminal:
                if a == b:
                    relation[a][b] = Med
                    concordanceRelation[a][b] = Decimal('0.0')
                else:
                    nc = len(criteria)
                    concordance = Decimal('0.0')

                    veto = {}
                    abvetos=[]

                    if hasBipolarVeto:
                        negativeVeto = {}
                        abNegativeVetos=[]

                    for c in criteria:
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                indx = criteria[c]['thresholds']['ind'][0]
                                indy = criteria[c]['thresholds']['ind'][1]
                                ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            except:
                                ind = None
                            try:
                                wpx = criteria[c]['thresholds']['weakPreference'][0]
                                wpy = criteria[c]['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wp = wpx + wpy * abs(evaluation[c][a]) 
                            except:
                                wp = None
                            try:
                                px = criteria[c]['thresholds']['pref'][0]
                                py = criteria[c]['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    p = px + py * abs(evaluation[c][a]) 
                            except:
                                p = None
                            if criteria[g]['weight'] > Decimal('0'):
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]
                            lc0 = self._localConcordance(d,ind,wp,p)
                            ## print 'c,a,b,d,ind,wp,p,lco = ',c,a,b,d, ind,wp,p,lc0
                            concordance += (lc0 * criteria[c]['weight'])
                            try:
                                wvx = criteria[c]['thresholds']['weakVeto'][0]
                                wvy = criteria[c]['thresholds']['weakVeto'][1]
                                if hasNoVeto:
                                    wv = None
                                else:
                                    if hasSymmetricThresholds:
                                        wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                    else:
                                        wv = wvx + wvy * abs(evaluation[c][a])
                            except:
                                wv = None
                            try:
                                vx = criteria[c]['thresholds']['veto'][0]
                                vy = criteria[c]['thresholds']['veto'][1]
                                if hasNoVeto:
                                    v = None
                                else:
                                    if hasSymmetricThresholds:
                                        v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                    else:
                                        v = vx + vy * abs(evaluation[c][a])
                            except:
                                v = None
                            veto[c] = (self._localVeto(d,wv,v),d,wv,v)
                            if veto[c][0] > Decimal('-1.0'):
                                abvetos.append((c,veto[c]))
                                largePerformanceDifferencesCount[a][b]['negative'] -= 1
                            ## if d < -wv:
                            ##     print 'd,wv,v,veto[c]',d,wv,v,veto[c]
                            if hasBipolarVeto:
                                negativeVeto[c] = (self._localNegativeVeto(d,wv,v),d,wv,v)
                                if negativeVeto[c][0] > Decimal('-1.0'):
                                    abNegativeVetos.append((c,negativeVeto[c]))
                                    largePerformanceDifferencesCount[a][b]['positive'] += 1
                                ## if d > wv:
                                ##     print 'd,wv,v,negativeVeto[c]',d,wv,v,negativeVeto[c] 
                        else:
                            concordance += Decimal('0.0') * criteria[c]['weight']
                            veto[c] = (Decimal('-1.0'),None,None,None)
                            if hasBipolarVeto:
                                negativeVeto[c] = (Decimal('-1.0'),None,None,None)
                                
                    concordindex = concordance / totalweight                 
                    concordanceRelation[a][b] = concordindex
                    
                    ## init vetoes lists and indexes
                    abVetoes=[]
                    abNegativeVetoes=[]

                    #  contradictory vetoes
                    
                    for c in criteria:
                        if veto[c][0] >= Decimal('0'):
                            abVetoes.append((c,veto[c]))
                        if hasBipolarVeto:
                            if negativeVeto[c][0] >= Decimal('0'):
                                abNegativeVetoes.append((c,negativeVeto[c]))
                                         
                    if hasBipolarVeto:
                        vetoes = [-veto[c][0] for c in veto if veto[c][0] > Decimal('-1')]
                        negativeVetoes = [negativeVeto[c][0] for c in negativeVeto if negativeVeto[c][0] > Decimal('-1')]
                        if Debug:
                            print('vetoes = ', vetoes)
                            print('negativeVetoes = ', negativeVetoes)
                        omaxList = [concordindex] + vetoes + negativeVetoes
                        outrankindex = omax(Med,omaxList,Debug=Debug)
                        if Debug:
                            print('a b outrankindex = ', a,b, outrankindex)
                    else:
                        # hasBipolarVeto == False
                        vetoIndex = Decimal('-1.0')
                        for c in criteria:
                            vetoIndex = max(vetoIndex,veto[c][0])
                        outrankindex = min(concordindex,-vetoIndex)

                    if abVetoes != []:
                        vetos.append(([a,b,concordindex*Max],abVetoes))
                    if hasBipolarVeto:
                        if abNegativeVetoes != []:
                            negativeVetos.append(([a,b,concordindex*Max],abNegativeVetoes))
                    relation[a][b] = outrankindex*Max

        # storing concordance relation and vetoes
        if WithConcordanceRelation:
            self.concordanceRelation = concordanceRelation
        if WithVetoCounts:
            self.vetos = vetos
            if hasBipolarVeto:
                self.negativeVetos = negativeVetos
                self.largePerformanceDifferencesCount = largePerformanceDifferencesCount

        # return outranking relation    

        return relation


    
    def criterionCharacteristicFunction(self,c,a,b,hasSymmetricThresholds=True):
        """
        Renders the characteristic value of the comparison of a and b on criterion c.
        """
        evaluation = self.evaluation
        NA = self.NA
        criterion = self.criteria[c]
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
            try:
                indx = criterion['thresholds']['ind'][0]
                indy = criterion['thresholds']['ind'][1]
                if hasSymmetricThresholds:
                    ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    ind = indx +indy * abs(evaluation[c][a])
            except:
                ind = None
            try:
                wpx = criterion['thresholds']['weakPreference'][0]
                wpy = criterion['thresholds']['weakPreference'][1]
                if hasSymmetricThresholds:
                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    wp = wpx + wpy * abs(evaluation[c][a])
            except:
                wp = None
            try:
                px = criterion['thresholds']['pref'][0]
                py = criterion['thresholds']['pref'][1]
                if hasSymmetricThresholds:
                    p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    p = px + py * abs(evaluation[c][a])
            except:
                p = None
            if criterion['weight'] > Decimal('0'):
                d = evaluation[c][a] - evaluation[c][b]
            else:
                d = evaluation[c][b] - evaluation[c][a]
            return self._localConcordance(d,ind,wp,p)
        else:
            return Decimal('0.0')

    def computeSingleCriteriaNetflows(self):
        """
        renders the Promethee single criteria netflows matrix M
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        n = len(actionsList)
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        matrixM = {}
        for a in actionsList:
            matrixM[a] = {}
            for c in criteriaList:
                netflow= Decimal('0.0')
                for b in actionsList:
                    if a != b:
                        cab = self.criterionCharacteristicFunction(c,a,b)
                        cba = self.criterionCharacteristicFunction(c,b,a)
                        netflow += cab - cba
                netflow = float(netflow)/float(n-1)
                matrixM[a][c] = netflow
        return matrixM
    
    def saveSingleCriterionNetflows(self,fileName='tempnetflows.prn',delimiter=' ',Comments=True):
        """
        Delimited save of single criteria netflows matrix
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        M = self.computeSingleCriteriaNetflows()
        fo = open(fileName,'w')
        for a in actionsList:
            for c in criteriaList:
                fo.write('%2.2f ' % (M[a][c]))
            fo.write('\n')
        fo.close()
        if Comments:
            print('Single Criteria Netflows saved on file %s' % (fileName))
        
    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters: d := diff observed, wp := weak preference threshold,
        ind := indiffrence threshold, p := prefrence threshold.
        Renders the concordance index per criteria (-1,0,1)
        """
        if p is not None:
            if   d <= -p:
                return Decimal('-1.0')
            elif ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                if d < Decimal('0.0'):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')
        else:
            if ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            else:
                if d < Decimal("0.0"):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')                
            

    def _localVeto(self, d, wv, v):
        """
        Parameters:
            d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local veto state (-1,0,1).

        """
        if v is not None:
            if  d <= - v:
                return Decimal('1.0')
            elif wv is not None:
                if d <= - wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d <= -wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')

    def _localNegativeVeto(self, d, wv, v):
        """
        Parameters:
            d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local negative veto state (-1,0,1).

        """
        if v is not None:
            if  d >= v:
                return Decimal('1.0')
            elif wv is not None:
                if d >= wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d >= wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')


class _BipolarPreferenceDigraph(BipolarOutrankingDigraph,PerformanceTableau):
    """
    Parameters:
        | performanceTableau (fileName of valid py code)
        | optional, coalition (sublist of criteria)

    Specialization of the standard BipolarOutrankingDigraph class for generating
    new bipolar ordinal-valued outranking digraphs.

    """
    def __init__(self,argPerfTab=None,coalition=None):
        import copy
        if argPerfTab is None:
            perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab
        self.performanceTableau = perfTab
        self.name = 'rel_' + perfTab.name
        self.actions = copy.copy(perfTab.actions)
        Min =   Decimal('-2.0')
        Med =   Decimal('0.0')
        Max =   Decimal('2.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        if coalition is None:
            criteria = copy.copy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = copy.copy(perfTab.criteria[g])
        self.criteria = criteria
        self.convertWeight2Decimal()
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
        # construct outranking relation
        self.relation = self._constructRelation(criteria,perfTab.evaluation,hasNoVeto=hasNoVeto,hasBipolarVeto=hasBipolarVeto)

        # insert performance Data
        self.evaluation = copy.copy(perfTab.evaluation)
        self.convertEvaluation2Decimal()
        try:
            self.description = copy.copy(perfTab.description)
        except:
            pass
        # init general digraph Data
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def _constructRelation(self,criteria,evaluation,hasNoVeto=False,hasBipolarVeto=False,hasSymmetricThresholds=True):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        """
        actions = self.actions
        NA = self.NA
        totalweight = Decimal('0.0')
        for c in criteria:
            totalweight = totalweight + abs(criteria[c]['weight'])
        relation = {}
        vetos = []
        if hasBipolarVeto:
            negativeVetos = []
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a == b:
                    relation[a][b] = Decimal('0.0')
                else:
                    nc = len(criteria)
                    concordance = Decimal('0.0')
                    veto = {}
                    if hasBipolarVeto:
                        negativeVeto = {}
                    for c in criteria:
                        criterion = criteria[c]
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                indx = criterion['thresholds']['ind'][0]
                                indy = criterion['thresholds']['ind'][1]
                                if hasSymmetricThresholds:
                                    ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    ind = indx +indy * abs(evaluation[c][a])
                            except:
                                ind = None
                            try:
                                wpx = criterion['thresholds']['weakPreference'][0]
                                wpy = criterion['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wp = wpx + wpy * abs(evaluation[c][a])
                            except:
                                wp = None
                            try:
                                px = criterion['thresholds']['pref'][0]
                                py = criterion['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    p = px + py * abs(evaluation[c][a])
                                    
                            except:
                                p = None
                            if criterion['weight'] > Decimal('0'):
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]
                            lc0 = self._localConcordance(d,ind,wp,p)
                            ## print 'c,a,b,d,ind,wp,p,lco = ',c,a,b,d, ind,wp,p,lc0
                            concordance = concordance + (lc0 * criterion['weight'])
                            try:
                                wvx = criterion['thresholds']['weakVeto'][0]
                                wvy = criterion['thresholds']['weakVeto'][1]
                                if hasNoVeto:
                                    wv = None
                                else:
                                    if hasSymmetricThresholds:
                                        wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                    else:
                                        wv = wvx + wvy * abs(evaluation[c][a])  
                            except:
                                wv = None
                            try:
                                vx = criterion['thresholds']['veto'][0]
                                vy = criterion['thresholds']['veto'][1]
                                if hasNoVeto:
                                    v = None
                                else:
                                    if hasSymmetricThresholds:
                                        v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                    else:
                                        v = vx + vy * abs(evaluation[c][a])
                            except:
                                v = None
                            veto[c] = (self._localVeto(d,wv,v),d,wv,v)
                            ## if d < -wv:
                            ##     print 'd,wv,v,veto[c]',d,wv,v,veto[c]
                            if hasBipolarVeto:
                                negativeVeto[c] = (self._localNegativeVeto(d,wv,v),d,wv,v)
                                ## if d > wv:
                                ##     print 'd,wv,v,negativeVeto[c]',d,wv,v,negativeVeto[c] 
                        else:
                            concordance = concordance + Decimal('0.0') * criterion['weight']
                            veto[c] = (Decimal('-1.0'),None,None,None)
                            if hasBipolarVeto:
                                negativeVeto[c] = (Decimal('-1.0'),None,None,None)
                    concordindex = concordance / totalweight                 

                    ## init vetoes lists and indexes
                    abvetos=[]
                    abNegativeVetos=[]
                    vetoIndex = Decimal('-1.0')
                    negativeVetoIndex = Decimal('-1.0')
                    ## compute bipolar vetoes indexes
                    for c in criteria:
                        vetoIndex = max(vetoIndex,veto[c][0])
                        if hasBipolarVeto:
                            negativeVetoIndex = max(negativeVetoIndex,negativeVeto[c][0])

                    #  contradictory vetoes
                    if hasBipolarVeto:
                        #  contradictory vetoes
                        if vetoIndex > Decimal('-1.0') and negativeVetoIndex > Decimal('-1.0'):
                            abvetos.append((c,veto[c]))
                            abNegativeVetos.append((c,negativeVeto[c]))
                            outrankindex = Decimal('0.0')
                        #  veto
                        elif vetoIndex > Decimal('-1.0'):
                            abvetos.append((c,veto[c]))
                            if concordindex > Decimal('0.0'):
                                outrankindex = Decimal('0.0')
                            else:
                                outrankindex = min(concordindex,-vetoIndex)
                        #  dictator
                        elif negativeVetoIndex > Decimal('-1.0'):
                            abNegativeVetos.append((c,negativeVeto[c]))
                            if concordindex < Decimal('0.0'):
                                outrankindex = Decimal('0.0')
                            else:
                                outrankindex = max(concordindex,negativeVetoIndex)
                        else:
                            # no vetoes or dictators
                            outrankindex = concordindex
                    else:
                        # hasBipolarVeto == False
                        outrankindex = min(concordindex,-vetoIndex)
                                                                 
                    if abvetos != []:
                        vetos.append(([a,b,concordindex*Decimal('100.0')],abvetos))
                    if hasBipolarVeto:
                        if abNegativeVetos != []:
                            negativeVetos.append(([a,b,concordindex*Decimal('100.0')],abNegativeVetos))
                    relation[a][b] = outrankindex*Decimal('100.0')
        self.vetos = vetos
        if hasBipolarVeto:
            self.negativeVetos = negativeVetos
        return relation

    def criterionCharacteristicFunction(self,c,a,b,hasSymmetricThresholds=True):
        """
        Renders the characteristic value of the comparison of a and b on criterion c.
        """
        evaluation = self.evaluation
        NA = self.NA
        criterion = self.criteria[c]
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
            try:
                indx = criterion['thresholds']['ind'][0]
                indy = criterion['thresholds']['ind'][1]
                if hasSymmetricThresholds:
                    ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    ind = indx +indy * abs(evaluation[c][a])
            except:
                ind = None
            try:
                wpx = criterion['thresholds']['weakPreference'][0]
                wpy = criterion['thresholds']['weakPreference'][1]
                if hasSymmetricThresholds:
                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    wp = wpx + wpy * abs(evaluation[c][a])
            except:
                wp = None
            try:
                px = criterion['thresholds']['pref'][0]
                py = criterion['thresholds']['pref'][1]
                if hasSymmetricThresholds:
                    p = px + py * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                else:
                    p = px + py * abs(evaluation[c][a])
            except:
                p = None
            if criterion['weight'] > Decimal('0'):
                d = evaluation[c][a] - evaluation[c][b]
            else:
                d = evaluation[c][b] - evaluation[c][a]
            return self._localConcordance(d,ind,wp,p)
        else:
            return Decimal('0.0')

    def computeSingleCriteriaNetflows(self):
        """
        renders the Promethee single criteria netflows matrix M
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        n = len(actionsList)
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        matrixM = {}
        for a in actionsList:
            matrixM[a] = {}
            for c in criteriaList:
                netflow= Decimal('0.0')
                for b in actionsList:
                    if a != b:
                        cab = self.criterionCharacteristicFunction(c,a,b)
                        cba = self.criterionCharacteristicFunction(c,b,a)
                        netflow += cab - cba
                netflow = float(netflow)/float(n-1)
                matrixM[a][c] = netflow
        return matrixM
    
    def saveSingleCriterionNetflows(self,fileName='tempnetflows.prn',delimiter=' ',Comments=True):
        """
        Delimited save of single criteria netflows matrix
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        M = self.computeSingleCriteriaNetflows()
        fo = open(fileName,'w')
        for a in actionsList:
            for c in criteriaList:
                fo.write('%2.2f ' % (M[a][c]))
            fo.write('\n')
        fo.close()
        if Comments:
            print('Single Criteria Netflows saved on file %s' % (fileName))
        
    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters: d := diff observed, wp := weak preference threshold,
        ind := indiffrence threshold, p := prefrence threshold.
        Renders the concordance index per criteria (-1,0,1)
        """
        if p is not None:
            if   d <= -p:
                return Decimal('-1.0')
            elif ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                if d < Decimal('0.0'):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')
        else:
            if ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            else:
                if d < Decimal("0.0"):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')                
            

    def _localVeto(self, d, wv, v):
        """
        Parameters: d := diff observed, v (wv)  :=  (weak) veto threshold.
        Renders the local veto state (-1,0,1).
        """
        if v is not None:
            if  d <= - v:
                return Decimal('1.0')
            elif wv is not None:
                if d <= - wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d <= -wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')

    def _localNegativeVeto(self, d, wv, v):
        """
        Parameters: d := diff observed, v (wv)  :=  (weak) veto threshold.
        Renders the local negative veto state (-1,0,1).
        """
        if v is not None:
            if  d >= v:
                return Decimal('1.0')
            elif wv is not None:
                if d >= wv:
                    return Decimal('0.0')
                else:
                    return Decimal('-1.0')
            else:
                return Decimal('-1.0')        
        elif wv is not None:
            if d >= wv:
                return Decimal('0.0')
            else:
                return Decimal('-1.0')
        else:
            return Decimal('-1.0')

class _MedianBipolarOutrankingDigraph(BipolarOutrankingDigraph,PerformanceTableau):
    """
    Parameters: performanceTableau (fileName of valid py code)
                optional: coalition (sublist of criteria)
                          percentile as rational (n,d)
                          for instance (50,100) or (1,2) renders Q2, (1,4) = Q1
                          (1,10) = D1, (3,4) = Q3
                     
    Specialization of the standard OutrankingDigraph class for generating
    a median bipolar outranking digraph.
    """
    def __init__(self,argPerfTab=None,coalition=None,percentile=(1,2),Debug=False):
        from  copy import deepcopy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        self.name = 'rel_' + perfTab.name
        if isinstance(argPerfTab.actions,list):
            actions = {}
            for x in argPerfTab.actions:
                actions[x] = {'name': str(x)}
            self.actions = actions
        else:
            self.actions = copy.copy(argPerfTab.actions)
        Min =   Decimal('-100.0')
        Med =   Decimal('0.0')
        Max =   Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        if coalition is None:
            criteria = deepcopy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
        self.relation = self._constructRelation(perfTab,percentile,Debug)
        self.criteria = criteria
        self.evaluation = deepcopy(perfTab.evaluation)
        try:
            self.description = deepcopy(perfTab.description)
        except:
            pass
        methodData = {}
        try:
            valuationType = perfTab.parameter['valuationType']
            variant = perfTab.parameter['variant']
        except:
            valuationType = 'normalized'
            variant = 'median'
        methodData['parameter'] = {'valuationType':valuationType,'variant':variant}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,t,percentile,Debug=False):
        """
        Parameters: PerfTab.criteria, quantile (0 - 100)
        Renders the quantile-outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        from copy import deepcopy
        
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        #criteriaKey = [x for x in t.criteria]
        criteriaRelation = {}
        criteriaWeight = {}
        criteriaVeto = {}
        for x in criteria.keys():
            gx = BipolarOutrankingDigraph(t,coalition=[x])
            
            if Debug:
                print('criterion : ', x, t.criteria[x]['weight'])
                gx.showRelationTable()
                print(gx.vetos)
            else:
                pass
                
            criteriaRelation[x] = deepcopy(gx.relation)
            criteriaWeight[x] = t.criteria[x]['weight']
            criteriaVeto[x] = deepcopy(gx.vetos)


        veto = {}
        for x in criteria.keys():
           for v in criteriaVeto[x]:
                if Debug:
                    print('===>>>> v :', v,v[0][1],v[0][2])
                else:
                    pass
                try:
                    veto[v[0][0]][v[0][1]] = min(veto[v[0][0]][v[0][1]],v[0][2])
                except:
                    try:
                        veto[v[0][0]][v[0][1]] = v[0][2]
                    except:
                        veto[v[0][0]] = {}                   
                        veto[v[0][0]][v[0][1]] = v[0][2]
                        
        if Debug:
            print('Vetoes ', veto)
        else:
            pass

        #actionsKey = [x for x in t.actions]
        relation = {}
        for x in actions.keys():
            relation[x] = {}
            for y in actions.keys():
                try:
                    if veto[x][y] == Decimal("-1.0"):
                        relation[x][y] = Min
                    
                except:
                    pass
                characteristics = []
                for c in criteria.keys():
                    for i in range(int(criteriaWeight[c])):
                        characteristics.append(criteriaRelation[c][x][y])
                characteristics.sort(reverse=False)
                n = len(characteristics)
                
                ## if n % 2 == 1:
                m = (n+1)*percentile[0]
                if m % percentile[1] == 0:
                    k = m // percentile[1]
                    quantile = characteristics[k-1]
                else:
                    k = (m//percentile[1])
                    quantile0 = characteristics[k-1]
                    quantile1 = characteristics[k]
                    if quantile1 <= Med:
                        quantile = quantile1
                    elif quantile0 >= Med:
                        quantile = quantile0
                    else:
                        quantile = Med
                if Debug:
                    print('x,y,n,k', x,y,n,k)
                    print(characteristics, end=' ')
                else:
                    pass

                try:
                    relation[x][y] = min(quantile,veto[x][y])
                except:
                    relation[x][y] = characteristics[k-1]
                #print relation[x][y]
                        
        return relation



class _BipolarIntegerOutrankingDigraph(BipolarOutrankingDigraph,PerformanceTableau):
    """
    Parameters:
        | performanceTableau (fileName of valid py code)
        | optional, coalition (sublist of criteria)

    Specialization of the standard OutrankingDigraph class for generating
    bipolar integer-valued outranking digraphs.

    """
    def __init__(self,argPerfTab=None,coalition=None,
                 hasBipolarVeto=True,
                 hasSymmetricThresholds=True):
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau(integerWeights=True)
            else:
                perfTab = PerformanceTableau(argPerfTab)
        self.name = 'rel_' + perfTab.name
        #self.performanceTableau = copy.deepcopy(perfTab)
        self.actions = copy.copy(perfTab.actions)
        if coalition is None:
            criteria = copy.copy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
        totalWeight = Decimal('0')
        for c in criteria:
            totalWeight += abs(Decimal(str(criteria[c]['weight'])))
        self.criteria = criteria
        try:
            self.description = copy.copy(perfTab.description)
        except:
            pass
        methodData = {}
        try:
            valuationType = perfTab.parameter['valuationType']
        except:
            valuationType = 'integer'
        try:
            variant = perfTab.parameter['variant']
        except:
            variant = 'standard'
        try:
            vetoType = perfTab.parameter['vetoType']
        except:
            vetoType = 'normal'
            
        methodData['parameter'] = {'valuationType':valuationType,\
                                   'variant':variant, 'vetoType':vetoType}
        self.methodData = methodData

        Min = -totalWeight
        Med = Decimal('0')
        Max = totalWeight
        self.valuationdomain = {'min':Min,'med':Med,'max':Max,
                                'hasIntegerValuation':True}
        
        evaluation = copy.copy(perfTab.evaluation)
        
        if vetoType == "bipolar":
            hasBipolarVeto = True    
        self.relation = self._constructRelation(criteria,evaluation,\
                                                hasBipolarVeto=hasBipolarVeto,\
                                                hasSymmetricThresholds=hasSymmetricThresholds)
        
        self.evaluation = evaluation
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,criteria,evaluation,hasBipolarVeto=False,hasSymmetricThresholds=True):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.

        """
        actions = self.actions
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        NA = self.NA
        relation = {}
        vetos = []
        if hasBipolarVeto:
            negativeVetos = []
        largePerformanceDifferencesCount = {}
        for a in actions:
            largePerformanceDifferencesCount[a] = {}
            for b in actions:
                largePerformanceDifferencesCount[a][b] = {'positive':0,'negative':0}
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a == b:
                    relation[a][b] = Decimal('0')
                else:
                    nc = len(criteria)
                    concordance = Decimal('0')
                    veto = {}
                    abvetos=[]
                    if hasBipolarVeto:
                        negativeVeto = {}
                        abNegativeVetos=[]
                    for c in criteria:
                        criterion = criteria[c]
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                indx = criterion['thresholds']['ind'][0]
                                indy = criterion['thresholds']['ind'][1]
                                if hasSymmetricThresholds:
                                    ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    ind = indx +indy * abs(evaluation[c][a])
                                wp = None
                            except:
                                ind = None
                            try:    
                                wpx = criterion['thresholds']['weakPreference'][0]
                                wpy = criterion['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wp = wpx + wpy * abs(evaluation[c][a])
                                ind = None
                            except:
                                wp = None
                            try:
                                prefx = criterion['thresholds']['pref'][0]
                                prefy = criterion['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = prefx + prefy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    p = prefx + prefy * abs(evaluation[c][a])
                            except:
                                p = None

                            if criteria[c]['weight'] > Decimal('0'):    
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]

                            lc0 = self._localConcordance(d,ind,wp,p)
                            #print 'a,b,c,w,d,ind,wp,p,localConcordance(d,ind,wp,p)',a,b,c,criteria[c]['weight'],d,ind,wp,p,lc0
                            concordance = concordance + (lc0 * criteria[c]['weight'])
                            try:
                                wvx = criterion['thresholds']['weakVeto'][0]
                                wvy = criterion['thresholds']['weakVeto'][1]
                                if hasSymmetricThresholds:
                                    wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wv = wvx + wvy * abs(evaluation[c][a])
                            except:
                                wv = None
                            try:
                                vx = criterion['thresholds']['veto'][0]
                                vy = criterion['thresholds']['veto'][1]
                                if hasSymmetricThresholds:
                                    v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    v = vx + vy * abs(evaluation[c][a])
                            except:
                                v = None
                            vetoindex = self._localVeto(d,wv,v)
                            veto[c] = (vetoindex,d,wv,v)
                            if veto[c][0] >  Min:
                                 abvetos.append((c,veto[c]))
                                 largePerformanceDifferencesCount[a][b]['negative'] -= 1
                                
                            if hasBipolarVeto:
                                negativeVetoindex = self._localNegativeVeto(d,wv,v)
                                negativeVeto[c] = (negativeVetoindex,d,wv,v)
                                if negativeVeto[c][0] > Min:
                                    abNegativeVetos.append((c,negativeVeto[c]))
                                    largePerformanceDifferencesCount[a][b]['positive'] += 1
                            #if d < -wv:
                            #    print 'd,wv,v,veto[c]',d,wv,v,veto[c] 
                        else:
                            veto[c] = (Min,None,None,None)
                            if hasBipolarVeto:
                                negativeVeto[c] = (Min,None,None,None)
                    #outrankindex = concordance
                    concordindex = concordance

                    ## init vetoes lists and indexes
                    #abvetos=[]
                    #abNegativeVetos=[]
                    vetoIndex = Min
                    negativeVetoIndex = Min
                    ## compute bipolar vetoes indexes
                    for c in criteria:
                        vetoIndex = max(vetoIndex,veto[c][0])
                        if hasBipolarVeto:
                            negativeVetoIndex = max(negativeVetoIndex,negativeVeto[c][0])
                    #  contradictory vetoes
                    if hasBipolarVeto:
                        #  contradictory vetoes
                        if vetoIndex > Min and negativeVetoIndex > Min:
                            #abvetos.append((c,veto[c]))
                            #abNegativeVetos.append((c,negativeVeto[c]))
                            outrankindex = Med
                        #  veto
                        elif vetoIndex > Min:
                            #abvetos.append((c,veto[c]))
                            if concordindex > Med:
                                outrankindex = Med
                            else:
                                outrankindex = min(concordindex,Max - vetoIndex + Min)
                        #  dictator
                        elif negativeVetoIndex > Min:
                            #abNegativeVetos.append((c,negativeVeto[c]))
                            if concordindex < Med:
                                outrankindex = Med
                            else:
                                outrankindex = max(concordindex,negativeVetoIndex)
                        else:
                            # no vetoes or dictators
                            outrankindex = concordindex
                    else:
                        # hasBipolarVeto == False
                        outrankindex = min(concordindex,Max - vetoIndex + Min)
                                                    
                    if abvetos != []:
                        vetos.append(([a,b,concordance],abvetos))
                    if hasBipolarVeto:
                        if abNegativeVetos != []:
                            negativeVetos.append(([a,b,concordance],abNegativeVetos))
                    relation[a][b] = outrankindex
                    #print 'relation[a][b]', a,b, relation[a][b]
        self.vetos = vetos
        if hasBipolarVeto:
            self.negativeVetos = negativeVetos
            self.largePerformanceDifferencesCount = largePerformanceDifferencesCount
        return relation

    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters:
            | d := diff observed, h := weak preference threshold,
            | p := prefrence threshold.

        Renders the concordance index per criteria (Min,Med,Max)

        """
        Max = 1
        Med = 0
        Min = -1

        if p is not None:
            if   d <= -p:
                return Min
            elif ind is not None:
                if d >= -ind:
                    return Max
                else:
                    return Med
            elif wp is not None:
                if d > -wp:
                    return Max
                else:
                    return Med
            else:
                if d < Decimal("0.0"):
                    return Min
                else:
                    return Max
        else:
            if ind is not None:
                if d >= -ind:
                    return Max
                else:
                    return Min
            elif wp is not None:
                if d > -wp:
                    return Max
                else:
                    return Min
            else:
                if d < Decimal("0.0"):
                    return Min
                else:
                    return Max                
            

    def _localVeto(self, d, wv, v):
        """
        Parameters:
            | d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local veto state (Min,Med,Max).

        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']

        if v is not None:
            if  d <= - v:
                return Max
            elif wv is not None:
                if d <= - wv:
                    return Med
                else:
                    return Min
            else:
                return Min        
        elif wv is not None:
            if d <= -wv:
                return Med
            else:
                return Min
        else:
            return Min

    def _localNegativeVeto(self, d, wv, v):
        """
        Parameters:
            | d := diff observed, v (wv)  :=  (weak) veto threshold.

        Renders the local negative veto state (Min,Med,Max).

        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']

        if v is not None:
            if  d >= v:
                return Max
            elif wv is not None:
                if d >= wv:
                    return Med
                else:
                    return Min
            else:
                return Min        
        elif wv is not None:
            if d >= wv:
                return Med
            else:
                return Min
        else:
            return Min



    def showRelation(self):
        """
        prints the relation valuation in ##.## format.
        """
        print('* ---- Relation -----', end=' ')
        for x in self.actions:
            print()
            for y in self.actions:
                print('('+str(x)+', '+str(y)+') = '+' %d ' % (self.relation[x][y]))
        print()


    def savePy2Gprolog(self,name='temp'):
        """
        save digraph in gprolog version
        """
        print('*----- saving digraph in gprolog format  -------------*')        
        Name = name+'.pl'
        fo = open(Name,'w')
        fo.write('/*------- data set ---------*\n')
        fo.write(' * digraph pl export        *\n')
        fo.write(' * RB May 2007              *\n')
        fo.write(' * ---------------------....*/\n')
        fo.write('% data set: ')
        fo.write(Name)
        fo.write('\n')

        actions = list(self.actions)
        fo.write('actions(')
        fo.write(str(actions))
        fo.write(').\n')

        criteria = self.criteria
        listCriteriaNames = []
        for g in criteria:
            listCriteriaNames.append(g)
            criteriaScale = criteria[g]['scale'][1]
            try:
                weakPreferenceThreshold = criteria[g]['thresholds']['ind'][0]
            except:
                weakPreferenceThreshold = criteria[g]['thresholds']['weakPreference'][0]
            preferenceThreshold = criteria[g]['thresholds']['pref'][0]
            vetoThreshold = criteria[g]['thresholds']['veto'][0]
            weakVetoThreshold = criteria[g]['thresholds']['weakVeto'][0]

        fo.write('criteria(')
        fo.write(str(listCriteriaNames))
        fo.write(').\n')

        fo.write('criteriaScale(')
        fo.write(str(criteriaScale))
        fo.write(').\n')
        # changing valuation from a bipolar to a positive one #
        Med = self.valuationdomain['max']
        Min = self.valuationdomain['min'] + Med
        Max = self.valuationdomain['max'] + Med
        fo.write('valuationDomain([')
        fo.write(str(Min)+', '+str(Med)+', '+str(Max))       
        fo.write(']).\n')

        fo.write('sumWeights(')
        fo.write(str(Max))
        fo.write(').\n')
        
        fo.write('weakPreferenceThreshold(')
        fo.write(str(weakPreferenceThreshold))
        fo.write(').\n')

        fo.write('preferenceThreshold(')
        fo.write(str(preferenceThreshold))
        fo.write(').\n')

        fo.write('weakVetoThreshold(')
        fo.write(str(weakVetoThreshold))
        fo.write(').\n')

        fo.write('vetoThreshold(')
        fo.write(str(vetoThreshold))
        fo.write(').\n')

        relation = self.relation
        for x in actions:
            resx = 'relation('+str(x)+','
            for y in actions:
                if x == y:
                    value = Min
                else:
                    value = relation[x][y] + Med
                resxy = resx + str(y)+','+str(value)+').\n'
                fo.write(resxy)
        fo.close()


class _RandomElectre3OutrankingDigraph(_Electre3OutrankingDigraph):
    """
    Parameters:
        | n := nbr of actions, p := number criteria, scale := [Min,Max],
        | thresholds := [h,q,v]

    Specialization of the OutrankingDigraph class for generating temporary
    Digraphs from random performance tableaux.

    """
    def __init__(self,numberOfActions=7, numberOfCriteria=7, weightDistribution='random', weightScale = [1,10], commonScale=[0.0,100.0], commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0)], commonMode=['uniform',None,None]):
        import random,time
        self.name = 'rel_randomperftab'
        # generate random performance tableau
        tb = RandomS3PerformanceTableau(numberOfActions=numberOfActions,numberOfCriteria=numberOfCriteria, weightDistribution=weightDistribution, weightScale=weightScale, commonScale=commonScale,commonThresholds = commonThresholds, commonMode=commonMode)
        self.actions = tb.actions
        self.criteria = tb.criteria
        self.evaluation = tb.evaluation
        # instantiate default valuation domain
        Min = Decimal('0.0')
        Med = Decimal('50.0')
        Max = Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        # generate relation
        self.relation = self._constructRelation(tb.criteria,tb.evaluation)
        
        # standard Digraph parameters initialization
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()



class RandomBipolarOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Specialization of the BipolarOutrankingDigraph class for generating temporary Digraphs from RandomPerformanceTableau instances.

    *Parameters*:
       See :py:class:`randomPerfTabs.RandomPerformanceTableau` class.

    """
    def __init__(self,numberOfActions=7,
                 numberOfCriteria=7,
                 weightDistribution='random',
                 weightScale = [1,10],
                 commonScale=[0.0,100.0],
                 commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(80.0,0.0)],
                 commonMode=('uniform',None,None),
                 hasBipolarVeto=True,
                 Normalized=True,
                 seed=None):
        # generate random performance tableau
        from copy import deepcopy
        tb = RandomPerformanceTableau(numberOfActions=numberOfActions,\
                                      numberOfCriteria=numberOfCriteria,\
                                      weightDistribution=weightDistribution,\
                                      weightScale=weightScale,\
                                      commonScale=commonScale,\
                                      commonThresholds = commonThresholds,\
                                      commonMode=commonMode,\
                                      seed=seed)
        g = BipolarOutrankingDigraph(tb,Normalized=Normalized,\
                                     hasBipolarVeto=hasBipolarVeto)
        self.__dict__ = deepcopy(g.__dict__)
        # self.name = deepcopy(g.name)
        # self.actions = deepcopy(g.actions)
        # self.criteria = deepcopy(g.criteria)
        # self.evaluation = deepcopy(g.evaluation)
        # self.relation = deepcopy(g.relation)
        # self.valuationdomain = deepcopy(g.valuationdomain)
        # self.NA = deepcopy(g.NA)
        # self.order = len(self.actions)
        # self.gamma = self.gammaSets()
        # self.notGamma = self.notGammaSets()

class RandomOutrankingDigraph(RandomBipolarOutrankingDigraph):
    """
    Dummy for obsolete RandomOutrankingDigraph Class
    """
        
class PolarisedOutrankingDigraph(PolarisedDigraph,OutrankingDigraph):
    """
    Specilised :py:class:`digraphs.PolarisedDigraph` instance for Outranking Digraphs.

    .. warning::

        If called with argument *digraph=None*, a RandomBipolarOutrankingDigraph instance is generated first.
        
    """
    def __init__(self,digraph=None,level=None,KeepValues=True,AlphaCut=False,StrictCut=False):
        import copy
        if digraph is None:
            digraph = RandomBipolarOutrankingDigraph()
        PolarisedDigraph.__init__(self,digraph=digraph,
                                  level=level,KeepValues=KeepValues,
                                  AlphaCut=AlphaCut,StrictCut=StrictCut)
        self.criteria = copy.copy(digraph.criteria)
        self.evaluation = copy.copy(digraph.evaluation)
        self.NA = copy.copy(digraph.NA)
        #self.vetos = self.computeVetos(digraph,level)
        try:
            self.vetos = copy.copy(digraph.vetos)
        except:
            pass


class EquiSignificanceMajorityOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the general OutrankingDigraph class for 
    temporary outranking digraphs with equisignificant criteria.
    """
    def __init__(self,argPerfTab=None,coalition=None,hasNoVeto=False):
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        #self.performanceTableau = perfTab
        self.name = 'eqsignmajrel_' + perfTab.name
        self.actions = copy.copy(perfTab.actions)
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('+1')
        self.valuationdomain = {'hasIntegerValuation':True, 'min':Min,'med':Med,'max':Max}
        #self.weightPreorder = perfTab.computeWeightPreorder()
        if coalition is None:
            criteria = copy.copy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = copy.copy(perfTab.criteria[g])
        #self.relation = self._constructRelation(criteria,perfTab.evaluation, self.weightPreorder)
        self.criteria = criteria
        self.convertWeight2Decimal()
        self.evaluation = copy.copy(perfTab.evaluation)
        self.convertEvaluation2Decimal()
        self.relation = self._constructRelation(perfTab,hasNoVeto=hasNoVeto)
        methodData = {}
        methodData['parameter'] = {'valuationType':'integer','variant':'bipolar'}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def _constructRelation(self,perfTab,hasNoVeto=False):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        Debug = False
        
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        
        weightPreorder = self.computeWeightPreorder()
        k = len(weightPreorder)

        actionsList = [x for x in self.actions]
        characteristicVector = {}
        for x in actionsList:
            characteristicVector[x] = {}
            for y in actionsList:
                characteristicVector[x][y] = []
        if Debug:
            print(characteristicVector)
        coalitionsRelation = {}
        for i in range(k):
            _g = BipolarOutrankingDigraph(perfTab,coalition=weightPreorder[i],hasNoVeto=hasNoVeto)
            _g.recodeValuation(-1,1)
            coalitionsRelation[i] = _g.relation

        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                isPosStable = True
                isNegStable = True
                for i in range(k):
                    if coalitionsRelation[i][x][y] <= Med:
                        isPosStable = False
                    if coalitionsRelation[i][x][y] >= Med:
                        isNegStable = False
                if isPosStable:
                    relation[x][y] = Max
                elif isNegStable:
                    relation[x][y] = Min
                else:
                    relation[x][y] = Med
                if Debug:
                    print(x,y,relation[x][y])

        return relation
                
# ------------        
class _OutrankingOddsDigraph(OutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the general OutrankingDigraph class for 
    temporary outranking digraphs with odds valuation,
    i.e. ratio of the number of positive over the number
    of negative marginal outranking situations. 
    """
    def __init__(self,argPerfTab=None):
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        #self.performanceTableau = perfTab
        self.name = 'eqsignmajrel_' + perfTab.name
        self.actions = copy.copy(perfTab.actions)
        Min = Decimal('0')
        Med = Decimal('1')
        Max = Decimal('Infinity')
        self.valuationdomain = {'hasIntegerValuation':False, 'min':Min,'med':Med,'max':Max}
        #self.weightPreorder = perfTab.computeWeightPreorder()
        criteria = copy.copy(perfTab.criteria)
       #self.relation = self._constructRelation(criteria,perfTab.evaluation, self.weightPreorder)
        self.criteria = criteria
        self.convertWeight2Decimal()
        self.NA = perfTab.NA
        self.evaluation = copy.copy(perfTab.evaluation)
        self.convertEvaluation2Decimal()
        self.relation = self._constructRelation()
        methodData = {}
        methodData['parameter'] = {'valuationType':'exponential','variant':'standard'}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,hasSymmetricThresholds=True):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the outranking ods relation from the data
        of a given performance tableau instantiation PerfTab.

        """
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        valuationdomain = self.valuationdomain
        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        NA = self.NA
        relation = {}
        vetos = []
        negativeVetos = []
        largePerformanceDifferencesCount = {}
        for a in actions:
            largePerformanceDifferencesCount[a] = {}
            for b in actions:
                largePerformanceDifferencesCount[a][b] = {'positive':0,'negative':0}
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a == b:
                    relation[a][b] = valuationdomain['med']
                else:
                    nc = len(criteria)
                    concordance = Decimal('0')
                    discordance = Decimal('0')
                    veto = {}
                    abvetos=[]
                    negativeVeto = {}
                    abNegativeVetos=[]
                    for c in criteria:
                        criterion = criteria[c]
                        if evaluation[c][a] != NA and evaluation[c][b] != NA:		
                            try:
                                indx = criterion['thresholds']['ind'][0]
                                indy = criterion['thresholds']['ind'][1]
                                if hasSymmetricThresholds:
                                    ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    ind = indx +indy * abs(evaluation[c][a])
                                wp = None
                            except:
                                ind = None
                            try:    
                                wpx = criterion['thresholds']['weakPreference'][0]
                                wpy = criterion['thresholds']['weakPreference'][1]
                                if hasSymmetricThresholds:
                                    wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wp = wpx + wpy * abs(evaluation[c][a])
                                ind = None
                            except:
                                wp = None
                            try:
                                prefx = criterion['thresholds']['pref'][0]
                                prefy = criterion['thresholds']['pref'][1]
                                if hasSymmetricThresholds:
                                    p = prefx + prefy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    p = prefx + prefy * abs(evaluation[c][a])
                            except:
                                p = None

                            if criteria[c]['weight'] > Decimal('0'):    
                                d = evaluation[c][a] - evaluation[c][b]
                            else:
                                d = evaluation[c][b] - evaluation[c][a]

                            lc0 = self._localConcordance(d,ind,wp,p)
                            #print 'a,b,c,w,d,ind,wp,p,localConcordance(d,ind,wp,p)',a,b,c,criteria[c]['weight'],d,ind,wp,p,lc0
                            if lc0 > Med:
                                concordance = concordance + (lc0 * criteria[c]['weight'])
                            elif lc0 < Med:
                                discordance = discordance - (lc0 * criteria[c]['weight'])
                            try:
                                wvx = criterion['thresholds']['weakVeto'][0]
                                wvy = criterion['thresholds']['weakVeto'][1]
                                if hasSymmetricThresholds:
                                    wv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    wv = wvx + wvy * abs(evaluation[c][a])
                            except:
                                wv = None
                            try:
                                vx = criterion['thresholds']['veto'][0]
                                vy = criterion['thresholds']['veto'][1]
                                if hasSymmetricThresholds:
                                    v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    v = vx + vy * abs(evaluation[c][a])
                            except:
                                v = None
                            vetoindex = self._localVeto(d,wv,v)
                            veto[c] = (vetoindex,d,wv,v)
                            if veto[c][0] > Med:
                                 abvetos.append((c,veto[c]))
                                 largePerformanceDifferencesCount[a][b]['negative'] -= 1
                                
                            negativeVetoindex = self._localNegativeVeto(d,wv,v)
                            negativeVeto[c] = (negativeVetoindex,d,wv,v)
                            if negativeVeto[c][0] > Med:
                                abNegativeVetos.append((c,negativeVeto[c]))
                                largePerformanceDifferencesCount[a][b]['positive'] += 1
                            #if d < -wv:
                            #    print 'd,wv,v,veto[c]',d,wv,v,veto[c] 
                        else:
                            veto[c] = (Min,None,None,None)
                            negativeVeto[c] = (Min,None,None,None)
                    #outrankindex = oddsindex
                    oddsindex = concordance / discordance

                    ## init vetoes lists and indexes
                    #abvetos=[]
                    #abNegativeVetos=[]
                    vetoIndex = Med
                    negativeVetoIndex = Med
                    ## compute bipolar vetoes indexes
                    for c in criteria:
                        vetoIndex = max(vetoIndex,veto[c][0])
                        negativeVetoIndex = max(negativeVetoIndex,negativeVeto[c][0])
                    #  contradictory vetoes
                    if vetoIndex > Med and negativeVetoIndex > Med:
                        #abvetos.append((c,veto[c]))
                        #abNegativeVetos.append((c,negativeVeto[c]))
                        outrankindex = valuationdomain['med']
                    #  veto
                    elif vetoIndex > Med:
                        #abvetos.append((c,veto[c]))
                        if oddsindex > valuationdomain['med']:
                            outrankindex = valuationdomain['med']
                        else:
                            if vetoIndex < Med:
                                outrankindex = valuationdomain['min']
                            else:
                                outrankindex = oddsindex
                    #  dictator
                    elif negativeVetoIndex > Med:
                        #abNegativeVetos.append((c,negativeVeto[c]))
                        if oddsindex < Med:
                            outrankindex = valuationdomain['med']
                        else:
                            if negativeVetoIndex < Med:
                                outrankindex = valuationdomain['max']
                            else:
                                outrankindex = oddsindex
                    if abvetos != []:
                        vetos.append(([a,b,oddsindex],abvetos))
                    if abNegativeVetos != []:
                        negativeVetos.append(([a,b,oddsindex],abNegativeVetos))
                    else:
                        outrankindex = oddsindex
                    relation[a][b] = outrankindex
                    #print 'relation[a][b]', a,b, relation[a][b]
        self.vetos = vetos
        self.negativeVetos = negativeVetos
        self.largePerformanceDifferencesCount = largePerformanceDifferencesCount
        return relation

             
# ------------

class OrdinalOutrankingDigraph(OutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the general OutrankingDigraph class for 
    temporary ordinal outranking digraphs
    """
    def __init__(self,argPerfTab=None,coalition=None,hasNoVeto=False):
        """Generic constructor for many outranking digraph models."""
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        self.performanceTableau = perfTab
        self.name = 'rel_' + perfTab.name
        self.actions = copy.deepcopy(perfTab.actions)
        Min = Decimal('0.0')
        Med = Decimal('50.0')
        Max = Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        #self.weightPreorder = perfTab.computeWeightPreorder()
        if coalition is None:
            criteria = copy.deepcopy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
        self.criteria = criteria
        self.convertWeight2Decimal()
        self.evaluation = copy.deepcopy(perfTab.evaluation)
        self.NA = copy.deepcopy(perfTab.NA)
        self.convertEvaluation2Decimal()
        self.relation = self._constructRelation(criteria,perfTab.evaluation,hasNoVeto=hasNoVeto)
        methodData = {}
        methodData['parameter'] = {'valuationType':'decimal','variant':'none'}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    

    def _constructRelation(self,criteria,evaluation,hasSymmetricThresholds=True,hasNoVeto=False):
        """
        Parameters:
            PerfTab.criteria, PerfTab.evaluation.

        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        Debug = False
        
        weightPreorder = self.computeWeightPreorder()
        if Debug:
            print('weightPreorder=', weightPreorder)
        #  constructing the bipolar semiotical references lsr
        lsr = []
        for c in criteria:
            ci = c + '+'
            cj = c + '-'
            lsr.append(ci)
            lsr.append(cj)
        # constructing the bipolar ordering of lsr
        losr = []
        k = 1
        for w in weightPreorder:
            lowp = []
            lown = []
            for i in w:
                wp = i + '+'
                wn = i + '-'
                lowp.append(wp)
                lown.append(wn)
            losr.append((k,lowp))
            losr.append((-k,lown))
            k = k + 1
        losr.sort()
        if Debug:
            print('lsr', lsr)            
            print('losr', losr)
        actions = [x for x in self.actions]
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        NA = self.NA
        # computing weight distributions
        relation = {}
        for a in actions:
            relation[a] = {}
            for b in actions:
                # positive distribution ----------------------
                veto = Decimal('0')
                v = {}	
                for i in lsr:
                    v[i] = Decimal('0.0')
                for c in criteria:
                    criterion = criteria[c]
                    if evaluation[c][a] != NA and evaluation[c][b] != NA:
                        try:
                            indx = criterion['thresholds']['ind'][0]
                            indy = criterion['thresholds']['ind'][1]
                            if hasSymmetricThresholds:
                                ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                ind = indx +indy * abs(evaluation[c][a])
                            wp = None
                        except:
                            ind = None
                        try:    
                            wpx = criterion['thresholds']['weakPreference'][0]
                            wpy = criterion['thresholds']['weakPreference'][1]
                            if hasSymmetricThresholds:
                                wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                wp = wpx + wpy * abs(evaluation[c][a])
                            ind = None
                        except:
                            wp = None
                        try:
                            prefx = criterion['thresholds']['pref'][0]
                            prefy = criterion['thresholds']['pref'][1]
                            if hasSymmetricThresholds:
                                p = prefx + prefy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                p = prefx + prefy * abs(evaluation[c][a])
                        except:
                            p = None
                                                    
                        try:
                            wvx = criterion['thresholds']['weakVeto'][0]
                            wvy = criterion['thresholds']['weakVeto'][1]
                            if hasSymmetricThresholds:
                                wvv = wvx + wvy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                wvv = wvx + wvy * abs(evaluation[c][a])
                        except:
                            wvv = None
                        if hasNoVeto:
                            wvv = None
                        try:
                            vx = criterion['thresholds']['veto'][0]
                            vy = criterion['thresholds']['veto'][1]
                            if hasSymmetricThresholds:
                                vv = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                vv = vx + vy * abs(evaluation[c][a])
                        except:
                            vv = None
                        if hasNoVeto:
                            vv = None
                            
                        if criterion['weight'] < Decimal('0'):
                            d = evaluation[c][b] - evaluation[c][a]
                        else:
                            d = evaluation[c][a] - evaluation[c][b]

                        veto = veto + self._localVeto(d,wvv,vv)
                        counter = self._localConcordance(d,ind,wp,p)
                        if Debug:
                            print('--> c,a,b,evaluation[c][a],evaluation[c][b], d', c,a,b,evaluation[c][a],evaluation[c][b], d)
                            print('ind, wp, p, counter, veto', ind, wp, p, counter, veto)
                        
                        v[c + '+'] = v[c + '+'] + counter
                        v[c + '-'] = v[c + '-'] + (Decimal('1.0') - counter)
                    else:
                        v[c + '+'] = v[c + '+'] + Decimal('0.5')
                        v[c + '-'] = v[c + '-'] + Decimal('0.5')
                da = []
                for w in losr:
                    d = Decimal('0')
                    for i in w[1]:
                        d = d + v[i] 
                    da.append((w, d))
                nc = len(losr)
                dcd = [da[0]]
                k = 1
                while k < nc:
                    dcv = dcd[k-1][1]+da[k][1]
                    dcd.append((da[k][0],dcv))
                    k = k + 1
                if Debug:
                    print('dcd', dcd)
                # negative distribution	 ------------------------
                vn = {}
                for i in lsr:
                    vn[i] = Decimal('0.0')
                for c in criteria:
                    criterion = criteria[c]
                    if evaluation[c][a] != NA and evaluation[c][b] != NA:
                        try:
                            indx = criterion['thresholds']['ind'][0]
                            indy = criterion['thresholds']['ind'][1]
                            if hasSymmetricThresholds:
                                ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                ind = indx +indy * abs(evaluation[c][a])
                            wp = None
                        except:
                            ind = None
                        try:    
                            wpx = criterion['thresholds']['weakPreference'][0]
                            wpy = criterion['thresholds']['weakPreference'][1]
                            if hasSymmetricThresholds:
                                wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                wp = wpx + wpy * abs(evaluation[c][a])
                            ind = None
                        except:
                            wp = None

                        try:
                            prefx = criterion['thresholds']['pref'][0]
                            prefy = criterion['thresholds']['pref'][1]
                            if hasSymmetricThresholds:
                                p = prefx + prefy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                p = prefx + prefy * abs(evaluation[c][a])
                        except:
                            p = None
                        
                        if criterion['weight'] < Decimal('0'):
                            d = evaluation[c][b] - evaluation[c][a]
                        else:
                            d = evaluation[c][a] - evaluation[c][b]
                            
                        counter = self._localConcordance(d,ind,wp,p)
                            
                        vn[c + '+'] = vn[c + '+'] - counter + Decimal('1.0')
                        vn[c + '-'] = vn[c + '-'] + counter
                    else:
                        vn[c + '+'] = vn[c + '+'] + Decimal('0.5')
                        vn[c + '-'] = vn[c + '-'] + Decimal('0.5')
                dan = []
                for w in losr:
                    d = Decimal('0')
                    for i in w[1]:
                        d = d + vn[i]
                    dan.append((w, d))
                nc = len(losr)
                dcg = [dan[0]]
                k = 1
                while k < nc:
                    dcv = dcg[k-1][1]+dan[k][1]
                    dcg.append((dan[k][0],dcv))
                    k = k + 1
                if Debug:
                    print('dcg' , dcg)
                #  first order stochastic dominance
                i = 0
                j = 0
                while i < nc:
                    if dcd[i][1] > dcg[i][1]:
                        break
                    elif dcd[i][1] < dcg[i][1]:
                        j += 1
                    i += 1
                if i >=  nc:
                    if j > 0 and veto == Decimal('0'):
                        relation[a][b] = Max
                    elif veto == Decimal('0'):
                        relation[a][b] = Med
                    else:
                        relation[a][b] = Min
                        
                else:
                    i = 0
                    j = 0
                    while i < nc:
                        if dcd[i][1] < dcg[i][1]:
                            break
                        elif dcd[i][1] > dcg[i][1]:
                            j += 1
                        i += 1
                    if i >= nc:
                        if j > 0 or veto == Decimal('1'):
                            relation[a][b] = Min
                        elif veto < Decimal('1'):
                            relation[a][b] = Med
                    else:
                        if veto > Decimal('0'):
                            relation[a][b] = Min
                        else:
                            relation[a][b] = Med
        for a in actions:
            relation[a][a] = Min
        return relation

    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters:
            | d := diff observed, h := indifference threshold,
            | p := prefrence threshold.

        Renders the concordance index per criterion.
        """
        Debug = False
        if Debug:
            print('ordinal concordance locla concordance')
            print('d,ind,wp,p', d,ind,wp,p)
        if p is not None:
            if   d <= -p:
                return Decimal('0.0')
            elif ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.5')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.5')
            else:
                if d > Decimal("0.0"):
                    return Decimal('1.0')
                else:
                    return Decimal('0.5')
        else:
            if ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                if d < Decimal("0.0"):
                    return Decimal('0.0')
                else:
                    return Decimal('1.0')

    def _localVeto(self, d, wv,v):
        """
        Parameters: d := diff observed, v := veto threshold.
        Renders the local veto state
        """

        if v is not None:
            if  d <= - v:
                return Decimal('1.0')
            elif wv is not None:
                if d <= - wv:
                    return Decimal('0.5')
                else:
                    return Decimal('0.0')
            else:
                return Decimal('0.0')        
        elif wv is not None:
            if d <= -wv:
                return Decimal('0.5')
            else:
                return Decimal('0.0')
        else:
            return Decimal('0.0')


class UnanimousOutrankingDigraph(OutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the general OutrankingDigraph class for 
    temporary unanimous outranking digraphs
    """
    def __init__(self,argPerfTab=None,coalition=None,hasNoVeto=False):
        """Generic constructor for many outranking digraph models."""
        import copy
        if isinstance(argPerfTab, (PerformanceTableau,RandomPerformanceTableau)):
            perfTab = argPerfTab
        else:
            if argPerfTab is None:
                perfTab = RandomPerformanceTableau()
            else:
                perfTab = PerformanceTableau(argPerfTab)
        self.performanceTableau = perfTab
        self.name = 'rel_' + perfTab.name
        self.actions = copy.deepcopy(perfTab.actions)
        Min = Decimal('0.0')
        Med = Decimal('50.0')
        Max = Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        #self.weightPreorder = perfTab.computeWeightPreorder()
        if coalition is None:
            criteria = copy.deepcopy(perfTab.criteria)
        else:
            criteria = {}
            for g in coalition:
                criteria[g] = perfTab.criteria[g]
        self.criteria = criteria
        self.convertWeight2Decimal()
        self.evaluation = copy.deepcopy(perfTab.evaluation)
        self.NA = copy.deepcopy(perfTab.NA)
        self.convertEvaluation2Decimal()
        self.relation = self._constructRelation(criteria,perfTab.evaluation,hasNoVeto=hasNoVeto)
        methodData = {}
        methodData['parameter'] = {'valuationType':'decimal','variant':'none'}
        self.methodData = methodData
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,criteria,evaluation,hasSymmetricThresholds=True,hasNoVeto=True):
        """
        Parameters: PerfTab.criteria, PerfTab.evaluation.
        Renders the biploar valued outranking relation from the data
        of a given performance tableau instantiation PerfTab.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        NA = self.NA
        relation = {}
        for a in actions:
            relation[a] = {}
            for b in actions:
                nc = len(criteria)
                nvc = nc
                counter = 0
                veto = 0
                for c in criteria:
                    criterion = criteria[c]
                    if evaluation[c][a] != NA and evaluation[c][b] != NA:
                        #d = evaluation[c][a] - evaluation[c][b]
                        try:
                            indx = criterion['thresholds']['ind'][0]
                            indy = criterion['thresholds']['ind'][1]
                            if hasSymmetricThresholds:
                                ind = indx +indy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                ind = indx +indy * abs(evaluation[c][a])
                            wp = None
                        except:
                            ind = None
                        try:    
                            wpx = criterion['thresholds']['weakPreference'][0]
                            wpy = criterion['thresholds']['weakPreference'][1]
                            if hasSymmetricThresholds:
                                wp = wpx + wpy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                wp = wpx + wpy * abs(evaluation[c][a])
                            ind = None
                        except:
                            wp = None
                        try:
                            prefx = criterion['thresholds']['pref'][0]
                            prefy = criterion['thresholds']['pref'][1]
                            if hasSymmetricThresholds:
                                p = prefx + prefy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                            else:
                                p = prefx + prefy * abs(evaluation[c][a])
                        except:
                            p = None
                            
                        if criterion['weight'] < Decimal('0'):    
                            d = evaluation[c][b] - evaluation[c][a]
                        else:
                            d = evaluation[c][a] - evaluation[c][b]
                            
                        lc0 = self._localConcordance(d,ind,wp,p)
                            
                        counter += lc0
                        if not hasNoVeto:
                            try:
                                vx = criterion['thresholds']['veto'][0]
                                vy = criterion['thresholds']['veto'][1]
                                if hasSymmetricThresholds:
                                    v = vx + vy * max(abs(evaluation[c][a]),abs(evaluation[c][b]))
                                else:
                                    v = vx + vy * abs(evaluation[c][a])
                                veto = veto + self._localVeto(d, v)
                            except:
                                veto = veto + Decimal("0")
                    else:
                        nvc = nvc - 1
                        # under the universality condition nvc not to be used.
                if not hasNoVeto:
                    if veto == Decimal("0"):
                        if counter ==  nc:
                            relation[a][b] = Max
                        elif counter == -nc:
                            relation[a][b] = Min
                        else:
                            relation[a][b] = Med
                    else:
                        relation[a][b] = Min
                else:
                    if counter ==  nc:
                        relation[a][b] = Max
                    elif counter == -nc:
                        relation[a][b] = Min
                    else:
                        relation[a][b] = Med
                    
        for a in actions:
            relation[a][a] = Min
        return relation

    def _localConcordance(self,d,ind,wp,p):
        """
        Parameters: d := diff observed, h := indifference threshold,
        p := prefrence threshold.
        Renders the concordance index per criterion.
        """
        Debug = False
        if Debug:
            print('ordinal concordance locla concordance')
            print('d,ind,wp,p', d,ind,wp,p)
        if p is not None:
            if   d <= -p:
                return Decimal('-1.0')
            elif ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                if d > Decimal("-1.0"):
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
        else:
            if ind is not None:
                if d >= -ind:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            elif wp is not None:
                if d > -wp:
                    return Decimal('1.0')
                else:
                    return Decimal('-1.0')
            else:
                if d < Decimal("0.0"):
                    return Decimal('-1.0')
                else:
                    return Decimal('1.0')

            

    def _localVeto(self, d, v):
        """
        Parameters: d := diff observed, v := veto threshold.
        Renders the local veto state
        """

        if  d > -v:
            return Decimal("0")
        else:
            return Decimal("1")

class RobustOutrankingDigraph(BipolarOutrankingDigraph):
    """
    *Parameters*:
        performanceTableau (fileName or valid py code)

    Specialization of the general OutrankingDigraph class for 
    new robustness analysis distinguishing between three nested stability levels:
    
        * +4 (resp. -4) : unanimous outranking (resp. outranked;
        * +3 (resp. -3) : majority outranking (resp. outranked) situation
          in all coalitions of equi-ignificant citeria;
        * +2 (resp. -2) : validated outranking (resp. outranked) situation
          with all potential weights compatible with the criteria significance preorder;
        * +1 (resp. -1) : validated outranking (resp. outranked) situation with
          the given criteria significances;
        * 0 : indeterminate preferential situation-

    *Sematics*:
    
        * alternative *x* robustly outranks alternative *y* when the
          outranking situation is qualified greater or equal to level +2
          and there is no considerable counter-performance
          observed on a discordant criteria;
        * alternative *x* robustly does not outrank alternative *y* when the
          outranking situation is qualified lower or equal to level -2
          and there is no considerable performance
          observed on a discordant criteria.

    *Usage example*:

    >>> from outrankingDigraphs import *
    >>> t = RandomPerformanceTableau(numberOfActions=7,weightDistribution='random',seed=100)
    >>> t.showPerformanceTableau()
     *----  performance tableau -----*
     Criteria |  'g1'    'g2'    'g3'    'g4'    'g5'    'g6'    'g7'   
     Actions  |    4       6       2       7       4       4       2    
     ---------|-------------------------------------------------------
       'a1'   | 44.51   43.90   19.10   16.22   14.81   45.49   41.66  
       'a2'   |   NA    38.75   27.73   21.53   79.70   22.03   12.82  
       'a3'   | 58.00   35.84   41.46   51.16   67.48   33.83   21.92  
       'a4'   | 24.22   29.12   22.41     NA    13.97   31.83   75.74  
       'a5'   | 29.10   34.79   21.52   39.35     NA    69.98   15.45  
       'a6'   | 96.58   62.22   56.90   32.06   80.16   48.80    6.05  
       'a7'   | 82.29   44.23   46.37   47.67   69.62   82.88    9.96  
    >>> t.showWeightPreorder()
     *------- weights preordering --------*
     ['g3', 'g7'] (2) <
     ['g1', 'g5', 'g6'] (4) <
     ['g2'] (6) <
     ['g4'] (7)
    >>> g = RobustOutrankingDigraph(t)
    >>> g
     *------- Object instance description ------*
     Instance class      : RobustOutrankingDigraph
     Instance name       : robust_randomperftab
     Actions             : 7
     Criteria            : 7
     Size                : 19
     Determinateness (%) : 67.53
     Valuation domain    : [-1.00;1.00]
     Attributes          : ['name', 'methodData', 'actions',
                            'order', 'criteria', 'evaluation',
                            'vetos', 'valuationdomain', 'relation',
                            'concordanceRelation',
                            'largePerformanceDifferencesCount',
                            'ordinalRelation', 'equisignificantRelation',
                            'unanimousRelation', 'stability',
                            'gamma', 'notGamma']
    >>> g.showRelationTable(StabilityDenotation=True)
     * ---- Relation Table -----
     r/(stab) |  'a1'   'a2'   'a3'   'a4'   'a5'   'a6'   'a7'   
     ---------|------------------------------------------------------------
       'a1'   |    +1.00  -0.03  -0.17  +0.55  +0.00  -0.72  -0.45  
              |   (+4)   (-2)   (-2)   (+2)   (+1)   (-2)   (-2)  
       'a2'   |   +0.03   +1.00  -0.17  +0.21  -0.10  -0.45  -0.45  
              |   (+2)   (+4)   (-2)   (+2)   (-2)   (-2)   (-2)  
       'a3'   |   +0.17  +0.38   +1.00  +0.62  +0.59  +0.00  +0.00  
              |   (+2)   (+2)   (+4)   (+2)   (+2)   (-1)   (-1)  
       'a4'   |   -0.21  -0.21  -0.34   +1.00  -0.21  -0.62  -0.62  
              |   (-2)   (-2)   (-2)   (+4)   (-2)   (-2)   (-2)  
       'a5'   |   +0.03  +0.38  -0.17  +0.48   +1.00  +0.03  -0.72  
              |   (+2)   (+2)   (-2)   (+2)   (+4)   (+2)   (-2)  
       'a6'   |   +0.86  +0.72  +0.00  +0.62  -0.03   +1.00  +0.00  
              |   (+2)   (+2)   (+1)   (+2)   (-2)   (+4)   (+1)  
       'a7'   |   +0.86  +0.52  +0.62  +0.62  +0.72  +0.00   +1.00  
              |   (+2)   (+2)   (+2)   (+2)   (+2)   (-1)   (+4)  
    
    """
    def __init__(self, filePerfTab = None,Debug=False,hasNoVeto=True):
        
        import copy
        
        if filePerfTab is None:
            filePerfTab = 'randomPerf'
            t = RandomPerformanceTableau()
            t.save(filePerfTab)
            self.name='newrobust_randomPerf'
        else:
            self.name = 'robust_' + filePerfTab.name
        cardinal = BipolarOutrankingDigraph(filePerfTab,Normalized=True,WithConcordanceRelation=True,WithVetoCounts=True)
        ordinal  = OrdinalOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        ordinal.recodeValuation(-1,1)
        equisignificant = EquiSignificanceMajorityOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        equisignificant.recodeValuation(-1,1)
        unanimous = UnanimousOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        unanimous.recodeValuation(-1,1)
        
        if Debug:
            print('unanimous')
            print(unanimous.valuationdomain)
            unanimous.showRelationTable(hasIntegerValuation=True)
            print('equisignificant')
            print(equisignificant.valuationdomain)
            equisignificant.showRelationTable()
            print('ordinal')
            print(ordinal.valuationdomain)
            ordinal.showRelationTable()
            print('cardinal')
            print(cardinal.valuationdomain)
            cardinal.showRelationTable(hasLPDDenotation=True)
            
        try:
            self.description = copy.copy(cardinal.description)
        except:
            pass
        try:
            self.methodData = copy.copy(cardinal.methodData)
        except:
            pass
        self.actions = copy.copy(cardinal.actions)
        self.order = len(self.actions)
        try:
            self.objectives = copy.copy(cardinal.objectives)
        except:
            pass
        self.criteria = copy.copy(cardinal.criteria)
        self.evaluation = copy.copy(cardinal.evaluation)
        self.NA = copy.copy(cardinal.NA)
        self.vetos = copy.copy(cardinal.vetos)
        self.valuationdomain = copy.copy(cardinal.valuationdomain)
        self.relation = copy.copy(cardinal.relation)
        self.concordanceRelation = copy.copy(cardinal.concordanceRelation)
        self.largePerformanceDifferencesCount = copy.copy(cardinal.largePerformanceDifferencesCount)
        self.ordinalRelation = copy.copy(ordinal.relation)
        self.equisignificantRelation = copy.copy(equisignificant.relation)
        self.unanimousRelation = copy.copy(unanimous.relation)
        self.stability = self._constructRelation()
        if Debug:
            self.showRelationTable(hasStabilityDenotation=True)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self):
        """
        Help method for constructing robust outranking relation.
        """
        Debug = False
        unanimousRelation = self.unanimousRelation
        equisignificantRelation = self.equisignificantRelation
        ordinalRelation = self.ordinalRelation
        concordanceRelation = self.concordanceRelation
        
        if Debug:
            print(self.valuationdomain)
            
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        One = Decimal("1")
        MinusOne = Decimal("-1")
        actions = [x for x in self.actions]
        stability = {}
        relation = {}
        for a in actions:
            stability[a] = {}
            relation[a] = {}
            for b in actions:
                if a != b:
                    if unanimousRelation[a][b] == One:
                        stability[a][b] = 4
                        relation[a][b] = self.relation[a][b]
                    elif unanimousRelation[a][b] == MinusOne:
                        stability[a][b] = -4
                        relation[a][b] = self.relation[a][b]
                    elif equisignificantRelation[a][b] == One:
                        stability[a][b] = 3
                        relation[a][b] = self.relation[a][b]
                    elif equisignificantRelation[a][b] == MinusOne:
                        stability[a][b] = -3
                        relation[a][b] = self.relation[a][b]                        
                    elif ordinalRelation[a][b] == One:
                        stability[a][b] = 2
                        relation[a][b] = self.relation[a][b]
                    elif ordinalRelation[a][b] == MinusOne:
                        stability[a][b] = -2
                        relation[a][b] = self.relation[a][b]
                    elif concordanceRelation[a][b] > Med:
                        stability[a][b] = 1
                        relation[a][b] = Med
                    elif concordanceRelation[a][b] < Med:
                        stability[a][b] = -1
                        relation[a][b] = Med
                    else:
                        stability[a][b] = 0
                        relation[a][b] = Med
                else:
                    stability[a][b] = 0
                    relation[a][b] = Med
        self.relation = relation
        return stability

    def showRelationTable(self,IntegerValues=False,
                          actionsSubset= None,
                          rankingRule=None,
                          Sorted=True,
                          hasLPDDenotation=False,
                          StabilityDenotation=True,
                          hasLatexFormat=False,
                          hasIntegerValuation=False,
                          relation=None,
                          ReflexiveTerms=True):
        """
        prints the relation valuation in actions X actions table format by default with
        the stability denotation in brackets:

        +4 | -4 : unanimous outranking | outranked situation;

        +3 | -3 : validated outranking | outranked situation in each coalition
        of equisignificant criteria;

        +2 | -2 : outranking | outranked situation validated with all potential significance weights
        that are compatible with the given significance preorder;

        +1 | -1 : validated outranking | outranked situation with the given significance weights;

        0 : indeterminate relational situation.

        """
        OutrankingDigraph.showRelationTable(self,
                          IntegerValues=IntegerValues,
                          actionsSubset= actionsSubset,
                          rankingRule=rankingRule,
                          Sorted=Sorted,
                          hasLPDDenotation=hasLPDDenotation,
                          StabilityDenotation=StabilityDenotation,
                          hasLatexFormat=hasLatexFormat,
                          hasIntegerValuation=hasIntegerValuation,
                          relation=relation,
                          ReflexiveTerms=ReflexiveTerms)

class OldRobustOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the general OutrankingDigraph class for 
    robustness analysis distinguishing 3 levels of stability.
    """
    def __init__(self, filePerfTab = None,Debug=False,hasNoVeto=True):
        
        import copy
        
        if filePerfTab is None:
            filePerfTab = 'randomPerf'
            t = RandomPerformanceTableau()
            t.save(filePerfTab)
            self.name='robust_randomPerf'
        else:
            self.name = 'robust_' + filePerfTab.name
        cardinal = BipolarOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        ordinal  = OrdinalOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        unanimous = UnanimousOutrankingDigraph(filePerfTab,hasNoVeto=hasNoVeto)
        
        if Debug:
            print('unanimous')
            print(unanimous.valuationdomain)
            unanimous.showRelationTable()
            print('ordinal')
            print(ordinal.valuationdomain)
            ordinal.showRelationTable()
            print('cardinal')
            print(cardinal.valuationdomain)
            cardinal.showRelationTable()
            
        try:
            self.description = copy.deepcopy(cardinal.description)
        except:
            pass
        try:
            self.methodData = copy.deepcopy(cardinal.methodData)
        except:
            pass
        self.actions = copy.copy(cardinal.actions)
        self.order = len(self.actions)
        self.criteria = copy.copy(cardinal.criteria)
        self.evaluation = copy.copy(cardinal.evaluation)
        self.NA = copy.copy(cardinal.NA)
        self.vetos = copy.copy(cardinal.vetos)
        self.valuationdomain = {'min':Decimal("-3"), 'med':Decimal("0"), 'max':Decimal("3")}
        self.cardinalRelation = copy.copy(cardinal.relation)
        self.cardinalValuationdomain =  copy.copy(cardinal.valuationdomain)
        self.relation = self._constructRelation(unanimous, ordinal, cardinal,hasNoVeto=hasNoVeto)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self, unanimous, ordinal, cardinal,hasNoVeto=True):
        """
        Parameters: normal -, ordinal -, and unanimous outranking relation.
        Help method for constructing robust outranking relation.
        """
        Debug = False

        if Debug:
            print(self.valuationdomain)
            
        uMin = unanimous.valuationdomain['min']
        uMed = unanimous.valuationdomain['med']
        uMax = unanimous.valuationdomain['max']
        
        oMin = ordinal.valuationdomain['min']
        oMed = ordinal.valuationdomain['med']
        oMax = ordinal.valuationdomain['max']
        
        cMin = cardinal.valuationdomain['min']
        cMed = cardinal.valuationdomain['med']
        cMax = cardinal.valuationdomain['max']
        
        rMin = self.valuationdomain['min']
        rMed = self.valuationdomain['med']
        rMax = self.valuationdomain['max'] 
      
        actions = [x for x in self.actions]
        relation = {}
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a != b:
                    if unanimous.relation[a][b] == uMax:
                        relation[a][b] = rMax
                    elif unanimous.relation[a][b] == uMin:
                        relation[a][b] = rMin
                    elif ordinal.relation[a][b] == oMax:
                        relation[a][b] = Decimal('2.0')
                    elif ordinal.relation[a][b] == oMin:
                        relation[a][b] = Decimal('-2.0')
                    elif cardinal.relation[a][b] > cMed:
                        relation[a][b] = Decimal('1.0')
                    elif cardinal.relation[a][b] < cMed:
                        relation[a][b] = Decimal('-1.0')
                    else:
                        relation[a][b] = rMed
                else:
                    relation[a][b] = rMed
                    
        return relation

    def showRelationTable(self):
        """ specialisation for integer values """

        Digraph.showRelationTable(self,IntegerValues=True)


    def saveAMPLDataFile(self,name='temp',Unique=False,Comments=True):
        """
        save the ampl reverse data for cplex
        """
        actionsList = [x for x in self.actions]
        actionsList.sort()
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        nc = len(criteriaList)
        
        relation = self.relation
        fileName = 'amplReverse'+name+'.dat'
        fo = open(fileName,'w')
        fo.write('data;\n\n')
        fo.write('set CRITERIA := ')
        for i in range(nc):
            fo.write(str(criteriaList[i])+' ')
        fo.write(';\n\n')
        
        fo.write('set ALLPAIRS := \n')
        for x in actionsList:
            for y in actionsList:
                if x != y:
                    fo.write(str(x)+str(y)+' ')
            fo.write('\n')
        fo.write(';\n\n')

        if Unique:
            pairwiseComparison = {}
            for x in actionsList:
                for y in actionsList:
                    if x != y:
                        xy = str(x)+str(y)
                        lineString = ''
                        for i in range(nc):
                            value = self.computeCriterionRelation(criteriaList[i],x,y)
                            value = (value + Decimal("1.0"))/Decimal("2.0")
                            lineString += '%.1f ' % (value)
                        pairwiseComparison[xy] = lineString
            self.pairwiseComparison = pairwiseComparison
        
        p2 = []
        pm2 = []
        p1 = []
        pm1 = []
        p0 = []

        if Unique:
            setP2 = set()
            setPm2 = set()
            setP1 = set()
            setPm1 = set()
            setP0 = set()
            count2 = 0
            countm2 = 0
            count1 = 0
            countm1 = 0
            count0 = 0
            countSave2 = 0
            countSavem2 = 0
            countSave1 = 0
            countSavem1 = 0
            countSave0 = 0
            for x in actionsList:
                for y in actionsList:
                    if x != y:
                        xy = str(x)+str(y)
                        if relation[x][y] == Decimal("2.0"):
                            count2 += 1
                            if pairwiseComparison[xy] not in setP2:
                                countSave2 += 1
                                p2.append(str(x)+str(y))
                                setP2.add(pairwiseComparison[xy])
                        elif relation[x][y] == Decimal("-2.0"):
                            countm2 += 1
                            if pairwiseComparison[xy] not in setPm2:
                                countSavem2 += 1
                                pm2.append(str(x)+str(y))
                                setPm2.add(pairwiseComparison[xy])
                        elif relation[x][y] == Decimal("1.0"):
                            count1 += 1
                            if pairwiseComparison[xy] not in setP1:
                                countSave1 += 1
                                p1.append(str(x)+str(y))
                                setP1.add(pairwiseComparison[xy])
                        elif relation[x][y] == Decimal("-1.0"):
                            countm1 += 1
                            if pairwiseComparison[xy] not in setPm1:
                                countSavem1 += 1
                                pm1.append(str(x)+str(y))
                                setPm1.add(pairwiseComparison[xy])
                        elif relation[x][y] == Decimal("0.0"):
                            count0 += 1
                            if pairwiseComparison[xy] not in setP0:
                                countSave0 += 1
                                p0.append(str(x)+str(y))
                                setP0.add(pairwiseComparison[xy])
            if Comments:
                print('counts: 2  \t-2 \t1  \t-1 \t0')
                print('        %d \t%d \t%d \t%d \t%d\n' % (count2,countm2,count1,countm1,count0))
                print('        %d \t%d \t%d \t%d \t%d\n' % (countSave2,countSavem2,countSave1,countSavem1,countSave0))
                print(' -----------------------------------------------------------')
                print('        %d \t%d \t%d \t%d \t%d\n' % (count2-countSave2,countm2-countSavem2,count1-countSave1,countm1-countSavem1,count0-countSave0))
                totalcount = count2+ countm2+count1+ countm1+count0
                totalcountSave = countSave2+countSavem2+countSave1+countSavem1+countSave0
                print('totals: counts: %d, countsUnique: \t%d, reduction: %d\n' %(totalcount,totalcountSave,totalcount-totalcountSave))
        else:
            for x in actionsList:
                for y in actionsList:
                    if x != y:
                        xy = str(x)+str(y)
                        if relation[x][y] == Decimal("2.0"):
                            p2.append(str(x)+str(y))
                        elif relation[x][y] == Decimal("-2.0"):
                            pm2.append(str(x)+str(y))
                        elif relation[x][y] == Decimal("1.0"):
                            p1.append(str(x)+str(y))
                        elif relation[x][y] == Decimal("-1.0"):
                            pm1.append(str(x)+str(y))
                        elif relation[x][y] == Decimal("0.0"):
                            p0.append(str(x)+str(y))

                            
        fo.write('set PAIRS2 :=\n')
        i = 0
        for x in p2:
            i += 1
            if i < 7:
                fo.write(x+' ')
            else:
                fo.write('\n'+x+' ')
                i = 0
        fo.write(';\n\n')

        fo.write('set PAIRSm2 :=\n')
        i = 0
        for x in pm2:
            i += 1
            if i < 7:
                fo.write(x+' ')
            else:
                fo.write('\n'+x+' ')
                i = 0
        fo.write(';\n\n')

        fo.write('set PAIRS1 :=\n')
        for x in p1:
            fo.write(x+' ')
        fo.write(';\n\n')
        fo.write('set PAIRSm1 :=\n')
        for x in pm1:
            fo.write(x+' ')
        fo.write(';\n\n')

        fo.write('set PAIRS0 :=\n')
        for x in p0:
            fo.write(x+' ')
        fo.write(';\n\n')

        fo.write('param S : ')
        for i in range(nc):
            fo.write(str(criteriaList[i])+' ')
        fo.write(':= \n')
        if Unique:
            Sset = set()
            for x in actionsList:
                for y in actionsList:
                    if x != y:
                        xy = str(x)+str(y)
                        if pairwiseComparison[xy] not in Sset:
                            fo.write(xy+' '+pairwiseComparison[xy]+'\n')
                            Sset.add(pairwiseComparison[xy])
            fo.write(';\n')
        else:    
            for x in actionsList:
                for y in actionsList:
                    if x != y:
                        fo.write(str(x)+str(y)+' ')
                        for i in range(nc):
                            value = self.computeCriterionRelation(criteriaList[i],x,y)
                            value = (value + Decimal("1.0"))/Decimal("2.0")
                            fo.write('%.1f ' % (value))
                        fo.write('\n')
            fo.write(';\n')
        fo.close()

        

    def saveXMLRubisOutrankingDigraph(self,name='temp',category='Rubis outranking robustness digraph',subcategory='Choice recommendation',author='digraphs Module (RB)',reference='saved from Python',comment=True,servingD3=True):
        """
        save complete robust Rubis problem and result in XML format with unicode encoding.
        """
        import codecs
        self.computeRubyChoice()

        if comment:
            print('*----- saving outranking robustness digraph in XML format  -------------*')        
        nameExt = name+'.xml'
        fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<!DOCTYPE rubisOutrankingDigraph SYSTEM "http://localhost/rubisServer/Schemas/rubisOutrankingDigraph-1.0/rubisOutrankingDigraph.dtd">\n')
        if not servingD3:
            fo.write('<?xml-stylesheet type="text/xsl" href="rubisOutrankingDigraph.xsl"?>\n')
        else:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="robustRubisOutrankingDigraph.xsl"? -->\n')
        fo.write('<rubisOutrankingDigraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="rubisOutrankingDigraph.xsd"')
        fo.write(' category="' + str(category)+'" subcategory="'+str(subcategory)+'">\n')

        fo.write('<header>\n')
        fo.write('<comment>header declaration </comment>\n')
        fo.write('<name>')
        fo.write(str(nameExt))
        fo.write('</name>\n')       
        fo.write('<author>')
        fo.write(str(author))
        fo.write('</author>\n')
        fo.write('<reference>')
        fo.write(str(reference))
        fo.write('</reference>\n')
        fo.write('</header>')

        actionsOrigList = [x for x in self.actions_orig]
        actionsOrigList.sort()
        fo.write('<actions>\n')
        fo.write('<comment>Potential decision actions </comment>\n')
        for x in actionsOrigList:
            fo.write('<action id="'+str(x)+'">\n')
            fo.write('<name>')
            try:
                fo.write(str(self.actions_orig[x]['name']))
            except:
                pass
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(self.actions_orig[x]['comment'])) 
            except:
                pass
            fo.write('</comment>\n')
            fo.write('</action>\n')
        fo.write('</actions>\n')

        fo.write('<criteria>\n')
        fo.write('<comment>List of performance criteria </comment>\n')
        criteriaList = [g for g in self.criteria]
        criteriaList.sort()
        for g in criteriaList:
            fo.write('<criterion id="'+str(g)+'" category="performance">\n')
            fo.write('<name>')
            try:
                fo.write(str(self.criteria[g]['name']))
            except:
                pass
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(self.criteria[g]['comment'])) 
            except:
                pass
            fo.write('</comment>\n')
            fo.write('<scale>')
            fo.write('<min>')
            fo.write('%.2f' % (self.criteria[g]['scale'][0]))
            fo.write('</min>')
            fo.write('<max>')
            fo.write('%.2f' % (self.criteria[g]['scale'][1]))
            fo.write('</max>')
            fo.write('</scale>\n')
            fo.write('<thresholds>\n')
            try:
                th1,th2 = self.criteria[g]['thresholds']['ind']
                fo.write('<indifference>'),fo.write('(%.2f,%.2f)' % (th1,th2) ), fo.write('</indifference>\n')
            except:
                try:
                    th1,th2 = self.criteria[g]['thresholds']['weakPreference']
                    fo.write('<weakPreference>'),fo.write('(%.2f,%.2f)' % (th1,th2) ),fo.write('</weakPreference>\n')
                except:
                    pass
            fo.write('<preference>')
            fo.write('(%.2f,%.2f)' % (self.criteria[g]['thresholds']['pref'][0],self.criteria[g]['thresholds']['pref'][1]))   
            fo.write('</preference>\n')
            try:
                th1,th2 = self.criteria[g]['thresholds']['weakVeto']
                fo.write('<weakVeto>'),fo.write('(%.2f,%.2f)' % (th1,th2) ),fo.write('</weakVeto>\n')
            except:
                pass
            try:
                th1,th2 = self.criteria[g]['thresholds']['veto']
                fo.write('<veto>'),fo.write('(%.2f,%.2f)' % (th1,th2) ),fo.write('</veto>\n')
            except:
                pass
             
            fo.write('</thresholds>')
            fo.write('<weight>')
##             fo.write(str(self.criteria[g]['weight']))
            fo.write('%.2f' % (self.criteria[g]['weight']))
            fo.write('</weight>')       
            fo.write('</criterion>\n')
        fo.write('</criteria>\n')

        evaluation = self.evaluation
        fo.write('<evaluations>\n')
        fo.write('<comment>performance table </comment>\n')
        for g in criteriaList:
            fo.write('<evaluation>\n')
            fo.write('<criterionID>'+str(g)+'</criterionID>\n')
            for x in actionsOrigList:
                fo.write('<performance>\n')
                fo.write('<actionID>')       
                fo.write(str(x))
                fo.write('</actionID>\n')                    
                fo.write('<value>')
##                 fo.write(str(evaluation[g][x]))
                fo.write('%.2f' % (evaluation[g][x]))
                fo.write('</value>\n')
                fo.write('</performance>\n')
            fo.write('</evaluation>\n')        
        fo.write('</evaluations>\n')        
  
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        fo.write('<valuationDomain category="bipolar" subcategory="robustness">\n')               
        fo.write('<comment>valuation domain declaration </comment>')
        fo.write('<min>')
        fo.write('%1d' % (int(Min)))
        fo.write('</min>\n')
        fo.write('<med>')
        fo.write('%1d' % (int(Med)))
        fo.write('</med>\n')
        fo.write('<max>')
        fo.write('%1d' % (int(Max)))
        fo.write('</max>\n')
        fo.write('</valuationDomain>\n')

        fo.write('<relation>\n')
        relation = self.relation_orig
        fo.write('<comment>valued outranking relation declaration. </comment>')
        for x in actionsOrigList:
            for y in actionsOrigList:
                fo.write('<arc>\n')        
                fo.write('<initialActionID>')
                fo.write(str(x))
                fo.write('</initialActionID>\n')                       
                fo.write('<terminalActionID>')
                fo.write(str(y))
                fo.write('</terminalActionID>\n')                                             
                fo.write('<value>')
##                 fo.write(str(relation[x][y]))
                fo.write('%1d' % (int(relation[x][y])))
                fo.write('</value>\n')                       
                fo.write('</arc>\n')        
        fo.write('</relation>\n')

        fo.write('<vetos>\n')
        fo.write('<comment>Effective and potential weto situations.</comment>\n')
        try:
            vetos = self.vetos
            for veto in vetos:
                fo.write('<veto>\n')
                arc = veto[0]
                fo.write('<arc>\n')
                fo.write('<initialActionID>')
                fo.write(str(arc[0]))
                fo.write('</initialActionID>\n')                       
                fo.write('<terminalActionID>')
                fo.write(str(arc[1]))
                fo.write('</terminalActionID>\n')                                             
                fo.write('<concordanceDegree>')
                fo.write('%.2f' % (arc[2]))
                fo.write('</concordanceDegree>\n')                                    
                fo.write('</arc>\n')
                situations = veto[1]
                fo.write('<vetoSituations>\n')
                for v in situations:
                    fo.write('<vetoSituation>\n')
                    fo.write('<criterionID>')
                    fo.write(str(v[0]))
                    fo.write('</criterionID>\n')
                    fo.write('<performanceDifference>')
                    fo.write('%.2f' % (v[1][1]))
                    fo.write('</performanceDifference>\n')
                    fo.write('<vetoCharacteristic>')
                    fo.write('%.2f' % (v[1][0]))
                    fo.write('</vetoCharacteristic>\n')
                    fo.write('<comment>')
                    if arc[2] > Med:
                        if v[1][0] > 0:
                            fo.write('effective veto')
                        else:
                            fo.write('effective weak veto')
                    elif arc[2] == Med:
                        if v[1][0] > 0:
                            fo.write('effective veto')
                        else:
                            fo.write('potential weak veto')
                    else:
                        if v[1][0] > 0:
                            fo.write('potential veto')
                        else:
                            fo.write('potential weak veto')                   
                    fo.write('</comment>\n')
                    fo.write('</vetoSituation>\n')

                fo.write('</vetoSituations>\n')
                fo.write('</veto>\n')
        except:
            pass
        fo.write('</vetos>\n')
        
        fo.write('<choiceRecommendation category="Rubis">\n')
        fo.write('<comment>List of good and bad choices following the Rubis methodology.</comment>\n')

        cocaActionsList = [x for x in self.actions if isinstance(x,frozenset)]
        if cocaActionsList != []:
            cocaActionsList.sort()
            fo.write('<cocaActions>')
            fo.write("<comment>weak COCA digraph actions' declaration </comment>\n")
            for x in cocaActionsList:
                fo.write('<cocaAction id="'+str(self.actions[x]['name'])+'">\n')
                fo.write('<name>')
                fo.write('chordless odd circuit')
                fo.write('</name>\n')
                fo.write('<comment>')
                fo.write('Rubis construction')
                fo.write('</comment>\n')
                fo.write('</cocaAction>\n')     
            fo.write('</cocaActions>\n')
        amplitude = float(Max - Min)/float(100.0)
        fo.write('<goodChoices>\n')
        for ch in self.goodChoices:
##             fo.write('<choiceSet independence="'+str(ch[2])+'" outranking="'+str(ch[3])+'" outranked="'+str(ch[4])+'" determinateness="'+str(-ch[0])+'" >')
            if ch[3] > ch[4]:
                #independent = float(ch[2])/amplitude
                #outranking = float(ch[3])/amplitude
                #outranked = float(ch[4])/amplitude
                independent = ch[2]
                outranking = ch[3]
                outranked = ch[4]
                #determ = -ch[0]*100.0
                determ = -(ch[0]*6) - 3
                fo.write('<choiceSet independence="%1d" outranking="%1d" outranked="%1d" determinateness="%1.2f" >\n' % (int(independent),int(outranking),int(outranked),determ))
                fo.write('<choiceActions>\n')
                for x in ch[5]:
                    fo.write('<actionID>')
                    fo.write(str(x))
                    fo.write('</actionID>\n')
                fo.write('</choiceActions>\n')              
                fo.write('</choiceSet>\n')
        fo.write('</goodChoices>\n')

        fo.write('<badChoices>\n')
        for ch in self.badChoices:
##             fo.write('<choiceSet independence="'+str(ch[2])+'" outranking="'+str(ch[3])+'" outranked="'+str(ch[4])+'" determinateness="'+str(-ch[0])+'" >')
            if ch[4] >= ch[3]:
                #independent = float(ch[2])/float(amplitude)
                #outranking = float(ch[3])/float(amplitude)
                #outranked = float(ch[4])/float(amplitude)
                independent = ch[2]
                outranking = ch[3]
                outranked = ch[4]
                #determ = -ch[0]*100.0
                determ = -(ch[0]*6) - 3
                fo.write('<choiceSet independence="%1d" outranking="%1d" outranked="%1d" determinateness="%1.2f" >\n' % (int(independent),int(outranking),int(outranked),determ))
                fo.write('<choiceActions>\n')
                for x in ch[5]:
                    fo.write('<actionID>')
                    fo.write(str(x))
                    fo.write('</actionID>\n')
                fo.write('</choiceActions>\n')              
                fo.write('</choiceSet>\n')
        fo.write('</badChoices>\n')
        
        fo.write('</choiceRecommendation>\n')

        fo.write('</rubisOutrankingDigraph>\n')
        
        fo.close()
        if comment:
            print('File: ' + nameExt + ' saved !')

    
            
class DissimilarityOutrankingDigraph(OutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the OutrankingDigraph class for generating
    temporary dissimilarity random graphs
    """
    def __init__(self,argPerfTab=None,Debug=False):
        if argPerfTab is None:
            print('Performance tableau required !')
            perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab
        import sys,copy
##        if filePerfTab is None:
##            t = RandomPerformanceTableau()
##            filePerfTab = 'randomPerf'
##            t.save(filePerfTab)
##        perfTab = PerformanceTableau(filePerfTab)
        self.name = 'rel_'+perfTab.name
        self.actions = copy.copy(perfTab.actions)
        self.criteria = copy.copy(perfTab.criteria)
        self.evaluation = copy.copy(perfTab.evaluation)
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        weightPreorder = perfTab.computeWeightPreorder()
        self.NA = copy.copy(perfTab.NA)
        self.relation = self._constructRelation(Debug=Debug)
        # for g in perfTab.actions:
        #     actions.append(g)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,Debug=False):
        """
        Renders the valued dissimilarity relation between criteria.
        """
        actions = self.actions
        if Debug:
            print(actions)
        criteria = self.criteria
        if Debug:
            print(criteria)
        evaluation = self.evaluation
        if Debug:
            print(evaluation)
        NA = self.NA        
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = {}
        for ga in criteria:
            criteriona = criteria[ga]
            relation[ga] = {}
            for gb in criteria:
                criterionb = criteria[gb]
                if ga != gb:
                    na = len(actions)
                    counter = Decimal('0')
                    for x in actions:
                        if evaluation[ga][x] != NA and evaluation[gb][x] != NA:
                            d = abs(evaluation[ga][x] - evaluation[gb][x])
                            hgax = criteriona['thresholds']['ind'][0]
                            hgay = criteriona['thresholds']['ind'][1]
                            hga = hgax + hgay * evaluation[ga][x]
                            hgbx = criterionb['thresholds']['ind'][0]
                            hgby = criterionb['thresholds']['ind'][1]
                            hgb = hgbx + hgby * evaluation[gb][x]
                            qgax = criteriona['thresholds']['pref'][0]
                            qgay = criteriona['thresholds']['pref'][1]
                            qga = qgax + qgay * evaluation[ga][x]
                            qgbx = criterionb['thresholds']['pref'][0]
                            qgby = criterionb['thresholds']['pref'][1]
                            qgb = qgbx + qgby * evaluation[gb][x]
                            h = max(hga,hgb)
                            q = max(qga,qgb)
                            counter = counter + self._localDissimilarity(d, h, q)
                        else:
                            counter = counter + Decimal('0.5')
                    relation[ga][gb] = Decimal(str((round((counter/na*(Max-Min)))))) + Min
                else:
                    relation[ga][ga] = Min
        return relation
                

    def _localDissimilarity(self, d, h, q):
        """
        Renders local dissimilarity between two criterial evaluations
        """
        dn = q - h
        if d <= h:
            return Decimal('0.0')
        elif dn == Decimal('0'):
            return Decimal('1.0')
        elif d <= q:
            return (d-h)/(q-h)
        else:
            return Decimal('1.0')
            
    def showAll(self):
        """
        specialize the general showAll method for the dissimilarity case
        """
        print('*----- show detail -------------*')
        print('Digraph          :', self.name)
        print('Criteria         :', self.actions)
        print('Valuation domain :', self.valuationdomain)
        print('*----  evaluated actions per criteria -----*')
        print(self.criteria)
        print('*----  evaluation tableau -----*')
        for g in self.actions:
            print(g, ': ', self.evaluation[g])
        print('*----  dissimilarity between criteria -----*')       
        print(self.relation)
        self.showComponents()
        print('*----  neighbourhoods -----*')       
        print('Gamma        :', self.gamma)
        print('Not Gamma    :', self.notGamma)

class MultiCriteriaDissimilarityDigraph(OutrankingDigraph):
    """
    Parameters:
        performanceTableau (fileName of valid py code)

    Specialization of the OutrankingDigraph class for generating
    temporary multiple criteria based dissimilarity graphs.
    """
    def __init__(self,perfTab=None,filePerfTab=None):
        import sys,copy
        if perfTab is None:
            if filePerfTab is None:
                perftab = RandomPerformanceTableau()
                filePerfTab = 'randomPerf'
                t.save(filePerfTab)
            else:
                perfTab = PerformanceTableau(filePerfTab)
        self.name = 'rel_'+perfTab.name
        self.actions = copy.copy(perfTab.actions)
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        weightPreorder = perfTab.computeWeightPreorder()
        self.criteria = copy.copy(perfTab.criteria)
        self.evaluation = copy.copy(perfTab.evaluation)
        self.NA = copy.copy(perfTab.NA)
        self.relation = self._constructRelation()
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self):
        """
        Renders the valued dissimilarity relation between criteria.
        """
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        NA = self.NA
        maxWeight = Decimal('0.0')
        for g in criteria:
            maxWeight += abs(criteria[g]['weight'])
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = {}
        for a in actions:
            relation[a] = {}
            for b in actions:
                if a != b:
                    nc = len(criteria)
                    counter = Decimal('0.0')
                    for g in criteria:
                        criterion = criteria[g]
                        if evaluation[g][a] != NA and evaluation[g][b] != NA:
                            if criterion['weight'] > Decimal('0'):
                                d = abs(evaluation[g][a] - evaluation[g][b])
                            else:
                                d = abs(evaluation[g][b] - evaluation[g][a])
                            try:
                                hx = criterion['thresholds']['ind'][0]
                                hy = criterion['thresholds']['ind'][1]
                                h = hx + hy * evaluation[g][a]
                            except:
                                h = None
                            try:
                                wpx = criterion['thresholds']['weakPref'][0]
                                wpy = criterion['thresholds']['weakPref'][1]
                                wp = wpx + wpy * evaluation[g][a]
                            except:
                                wp = None
                            try:
                                px = criterion['thresholds']['pref'][0]
                                py = criterion['thresholds']['pref'][1]
                                p = px + py * evaluation[g][a]
                            except:
                                p = None
                            index = self._localDissimilarity(d,h,wp,p)
##                             print d,h,wp,p
##                             print counter, index, criteria[g]['weight']
                            counter += index * criterion['weight']
                        else:
                            counter += Decimal('0.0')
##                    relation[a][b] = counter/maxWeight*(Max-Min) + Min
                    relation[a][b] = counter/maxWeight
                else:
                    relation[a][b] = Med
        return relation
                

    def _localDissimilarity(self, d, h, wp, p):
        """
        Renders local dissimilarity between two criterial evaluations
        """
        if h is not None:
            if d <= h:
                return Decimal('-1.0')
            elif p is not None:
                if d < p:
                    return Decimal('0.0')
                else:
                    return Decimal('1.0')
            elif d > h:
                return Decimal('1.0')
            else:
                print('Error: should never come here !!!')
        elif wp is not None:
            if d < wp:
                return Decimal('-1.0')
            elif p is not None:
                if d < p:
                    return Decimal('1.0')
                else:
                    return Decimal('0.0')
            else:
                return Decimal('1.0')
        elif p is not None:
            if d < p:
                return Decimal('-1.0')
            else:
                return Decimal('1.0')
        else:
            if d > Decimal('0.0'):
                return Decimal('1.0')
            else:
                return Decimal('-1.0')


            
class ConfidentBipolarOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Confident bipolar outranking digraph based on multiple criteria of
    uncertain significance.
    
    The digraph's bipolar valuation represents the bipolar outranking relation
    based on a sufficient likelihood of the at least as good as relation
    that is outranking without veto and counterveto.

    By default, each criterion i' significance weight is supposed to
    be a triangular random variable of mode w_i in the range 0 to 2*w_i.

    *Parameters*:

        * argPerfTab: PerformanceTableau instance or the name (without extension) of a stored one. If None, a random instance is generated.
        * distribution: {triangular|uniform|beta}, probability distribution used for generating random weights
        * betaParameter: a = b (default = 2)
        * confidence: required likelihood (in %) of the outranking relation
        * other standard parameters from the BipolarOutrankingDigraph class (see documentation).

    """
    def __init__(self,argPerfTab=None,
                 distribution = 'triangular',
                 betaParameter = 2,
                 confidence = 90.0,
                 coalition=None,
                 hasNoVeto=False,
                 hasBipolarVeto=True,
                 Normalized=True,
                 #Threading=False,
                 #nbrOfCPUs=1,
                 Debug=False,):
        # getting module ressources and setting the random seed
        from copy import copy, deepcopy
        # getting performance tableau
        if argPerfTab is None:
            perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = copy(argPerfTab)
        # initializing the bipolar outranking digraph
        bodg = BipolarOutrankingDigraph(argPerfTab=perfTab,coalition=coalition,\
                                     hasNoVeto=hasNoVeto,\
                                     hasBipolarVeto=hasBipolarVeto,\
                                     Normalized=Normalized,\
                                     #Threading=Threading,\
                                     #nbrCores=nbrOfCPUs,\
                                        )
        self.name = bodg.name + '_CLT'
        self.bipolarConfidenceLevel = (confidence/100.0)*2.0 -1.0 
        self.distribution = distribution
        self.betaParameter = betaParameter
        self.actions = copy(bodg.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(bodg.valuationdomain)
        self.criteria = copy(bodg.criteria)
        self.evaluation = copy(bodg.evaluation)
        self.NA = copy(bodg.NA)
        #if not Threading:
        self.concordanceRelation = copy(bodg.concordanceRelation)
        self.vetos = copy(bodg.vetos)
        self.negativeVetos = copy(bodg.negativeVetos)
        self.largePerformanceDifferencesCount =\
               copy(bodg.largePerformanceDifferencesCount)
        self.likelihoods = self.computeCLTLikelihoods(distribution=distribution,
                                                      betaParameter=betaParameter,
                                                      #Threading=Threading,
                                                      Debug=Debug)
        self.relation = self._computeConfidentRelation(
            bodg.relation,
            #likelihoodLevel=confidence,
            Debug=Debug)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _computeConfidentRelation(self,
                               outrankingRelation,
                               likelihoodLevel=None,
                               Debug=False):
        """
        Renders the relation cut at likelihood level.
        """
        
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']

        if likelihoodLevel is None:
            likelihoodLevel = self.bipolarConfidenceLevel

        if Debug:
            print('Likelihood level = %.2f%%' % ( (likelihoodLevel + 1.0)/2.0*100.0) )
        confidenceCutLevel = Med
        confidentRelation = {}
        actionsList = [x for x in self.actions]

        for x in actionsList:
            confidentRelation[x] = {}
            for y in actionsList:
                if abs(self.likelihoods[x][y]) >= likelihoodLevel:
                    confidentRelation[x][y] = outrankingRelation[x][y]
                else:
                    confidentRelation[x][y] = Med
                    level = abs(outrankingRelation[x][y])
                    if level < Max and level > confidenceCutLevel:
                        confidenceCutLevel = level
                if Debug:
                    print(x,y,outrankingRelation[x][y],self.likelihoods[x][y])
            self.confidenceCutLevel = confidenceCutLevel
        return confidentRelation
        
    def _recodeConcordanceValuation(self,oldRelation,sumWeights,Debug=False):
        """
        Recodes the characteristic valuation according
        to the parameters given.
        """
        if Debug:
            print(oldRelation,sumWeights)
        from copy import copy as deepcopy
        
##        oldMax = Decimal('1')
##        oldMin = Decimal('-1')
##        oldMed = Decimal('0')
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']
        oldAmplitude = oldMax - oldMin
        if Debug:
            print('old: ',oldMin, oldMed, oldMax, oldAmplitude)

        newMin = -sumWeights
        newMax = sumWeights
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))
        newAmplitude = newMax - newMin
        if Debug:
            print('new: ', newMin, newMed, newMax, newAmplitude)

        actions = [x for x in self.actions]
        newRelation = {}
        for x in actions:
            newRelation[x] = {}
            for y in actions:
                if oldRelation[x][y] == oldMax:
                    newRelation[x][y] = newMax
                elif oldRelation[x][y] == oldMin:
                    newRelation[x][y] = newMin
                elif oldRelation[x][y] == oldMed:
                    newRelation[x][y] = newMed
                else:
                    newRelation[x][y] = newMin +\
                        ((oldRelation[x][y] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(x,y,oldRelation[x][y],newRelation[x][y])

        return newRelation

    def _myGaussCDF(self,mean,sigma,x,Bipolar=True):
        """
        Bipolar error function of z = (x-mu)/sigma) divided by sqrt(2).
        If Bipolar = False,
        renders the Gauss cdf(z) = [erf( z ) + 1] / 2
        sqrt(2) = 1.4142135623731
        """
        from math import sqrt,erf
        try:
            z = (x - mean) / (sigma * 1.4142135623731)
        except ZeroDivisionError:
            z = 0.0        
        if Bipolar:
            return erf(z)
        else:
            return 0.5 + 0.5*erf(z)
    
    def computeCLTLikelihoods(self,distribution="triangular",
                              betaParameter=None,
                              #Threading=False,
                              #nbrOfCPUs=1,
                              Debug=False):
        """
        Renders the pairwise CLT likelihood of the at least as good as relation
        neglecting all considerable large performance differences polarisations.
        """
        from copy import copy as deepcopy
        from decimal import Decimal
        from math import sqrt
        from random import gauss
        actionsList = [x for x in self.actions]
        sumWeights = Decimal('0')
        criteriaList = [x for x in self.criteria]
        m = len(criteriaList)
        
        weightSquares = {}
        for g in criteriaList:
            gWeight = abs(self.criteria[g]['weight'])
##            if Debug:
##                print(g,gWeight)
            weightSquares[g] = gWeight*gWeight
            sumWeights += gWeight
##        if Debug:
##            print(sumWeights)
##            print(weightSquares)
##        if Threading:
##            g = BipolarOutrankingDigraph(self,hasNoVeto=True,
##                                         Threading=Threading,nbrCores=nbrOfCPUs)
##            concordanceRelation = g.relation
##        else:

        concordanceRelation = self._recodeConcordanceValuation(\
                                self.concordanceRelation,sumWeights,Debug=Debug)

        ccf = {}
        if distribution == 'uniform':
            varFactor = Decimal('1')/Decimal('3')
        elif distribution == 'triangular':
            varFactor = Decimal('1')/Decimal('6')
        elif distribution == 'beta':
            if betaParameter is not None:
                a = Decimal(str(betaParameter))
            else:
                a = self.betaParameter
            varFactor = Decimal('1')/(Decimal('2')*a + Decimal('1'))
        ## elif distribution == 'beta(4,4)':
        ##     varFactor = Decimal('1')/Decimal('9')
        for x in actionsList:
            ccf[x] = {}
            for y in actionsList:
                ccf[x][y] = {'std': Decimal('0.0')}
                for c in criteriaList:
                    ccf[x][y][c] = self.criterionCharacteristicFunction(c,x,y)
                    ccf[x][y]['std'] += abs(ccf[x][y][c])*weightSquares[c]
##                    if Debug:
##                        print(c,x,y,ccf[x][y][c])
                ccf[x][y]['std'] = sqrt(varFactor*ccf[x][y]['std'])
##                if Debug:
##                    print(x,y,ccf[x][y]['std'])
        lh = {}
        for x in actionsList:
            lh[x] = {}
            for y in actionsList:

                mean = float(concordanceRelation[x][y])
                std = float(ccf[x][y]['std'])
                lh[x][y] = -self._myGaussCDF(mean,std,0.0)
                if Debug:
                    print(x,y,lh[x][y])
        return lh

    def showRelationTable(self,IntegerValues=False,
                          actionsSubset= None,
                          Sorted=True,
                          LikelihoodDenotation=True,
                          hasLatexFormat=False,
                          hasIntegerValuation=False,
                          relation=None,
                          Debug=False):
        """
        prints the relation valuation in actions X actions table format.
        """
        if LikelihoodDenotation:
            try:
                likelihoods = self.likelihoods
            except:
                LikelihoodDenotation = False
        if Debug:
            print(LikelihoodDenotation)
        if actionsSubset is None:
            actions = self.actions
        else:
            actions = actionsSubset
            
        if relation is None:
            relation = self.relation
            
        print('* ---- Outranking Relation Table -----')
        if LikelihoodDenotation:
            print('r/(lh) | ', end=' ')
        else:
            print(' r()   | ', end=' ')
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(x,x)]
        if Sorted:
            actionsList.sort()

        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = IntegerValues
        
        for x in actionsList:
            print("'"+x[0]+"'\t", end=' ')
        print('\n-------|------------------------------------------------------------')
        for x in actionsList:
            if hasLatexFormat:
                print("$"+x[0]+"$ & ", end=' ')
            else:
                print(" '"+x[0]+"' |", end=' ')
            for y in actionsList:
                if hasIntegerValuation:
                    if hasLatexFormat:
                        print('$%+d$ &' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        print('%+d' % (relation[x[1]][y[1]]), end=' ')
                else:
                    if hasLatexFormat:
                        print('$%+.2f$ & ' % (relation[x[1]][y[1]]), end=' ')       
                    else:
                        print(' %+.2f ' % (relation[x[1]][y[1]]), end=' ')
                
            if hasLatexFormat:
                print(' \\cr')
            else:
                print()
            if LikelihoodDenotation:
                headString = "' "+x[0]+"' "
                formatStr = ' ' * len(headString)
                print(formatStr+'|', end=' ')
                for y in actionsList:
                    if x != y:
                        print('(%+.2f)' % (likelihoods[x[1]][y[1]]), end=' ')
                    else:
                        print(' ( - ) ', end=' ')
                print()

        print('Valuation domain   : [%+.3f; %+.3f] ' % (self.valuationdomain['min'],
                                                   self.valuationdomain['max']))
        if self.distribution == 'beta':
            print('Uncertainty model  : %s(a=%.1f,b=%.1f) ' % (self.distribution,
                                                         self.betaParameter,
                                                         self.betaParameter)
                                                         )
        else:
            print('Uncertainty model  : %s(a=%s,b=%s) ' % (self.distribution,'0','2w') )
          
        print('Likelihood domain  : [-1.0;+1.0] ')
        print('Confidence level   : %.2f (%.1f%%) ' % (self.bipolarConfidenceLevel,
                                                     (self.bipolarConfidenceLevel+1.0)/2.0*100.0))

        print('Confident majority : %.2f (%.1f%%) ' % (self.confidenceCutLevel,\
                            (self.confidenceCutLevel+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0')))
        deter = self.computeDeterminateness(InPercents=False)
        print('Determinateness    : %.2f (%.1f%%)' % (deter,\
                            (deter+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0')))
        print('\n')


#--------------------        
class StochasticBipolarOutrankingDigraph(BipolarOutrankingDigraph):
    """
    Stochastic bipolar outranking digraph based on multiple criteria of uncertain significance.
    
    The digraph's bipolar valuation represents the median of sampled outranking relations with a
    sufficient likelihood (default = 90%) to remain positive, repectively negative,
    over the possible criteria significance ranges.

    Each criterion i' significance weight is supposed to
    be a triangular random variables of mode w_i in the range 0 to 2*w_i.

    *Parameters*:

        * argPerfTab: PerformanceTableau instance or the name of a stored one.
          If None, a random instance is generated.
        * sampleSize: number of random weight vectors used for Monte Carlo simulation.
        * distribution: {triangular|extTriangular|uniform|beta(2,2)|beta(4,4)}, probability distribution used for generating random weights
        * spread: weight range = weight mode +- (weight mode * spread)
        * likelihood: 1.0 - frequency of valuations of opposite sign compared to the median valuation.
        * other standard parameters from the BipolarOutrankingDigraph class (see documentation).

    """
    def __init__(self,argPerfTab=None,
                 sampleSize = 50,
                 samplingSeed = None,
                 distribution = 'triangular',
                 spread = 1.0,
                 likelihood = 0.9,
                 coalition=None,
                 hasNoVeto=False,
                 hasBipolarVeto=True,
                 Normalized=False,
                 Debug=False,
                 SeeSampleCounter=False):
        # getting module ressources and setting the random seed
        from copy import copy, deepcopy
        if distribution == 'extTriangular':
            from randomNumbers import ExtendedTriangularRandomVariable
        else:
            from random import triangular, uniform, betavariate
            if samplingSeed is not None:
                from random import seed
                seed = samplingSeed   
        # getting performance tableau
        if argPerfTab is None:
            perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = deepcopy(argPerfTab)
        # initializing the bipolar outranking digraph
        bodg = BipolarOutrankingDigraph(argPerfTab=perfTab,coalition=coalition,\
                                     hasNoVeto = hasNoVeto,\
                                     hasBipolarVeto = hasBipolarVeto,\
                                     Normalized=Normalized)
        self.name = bodg.name + '_MC'
        self.sampleSize = sampleSize
        self.likelihood = likelihood
        self.actions = copy(bodg.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(bodg.valuationdomain)
        self.criteria = copy(bodg.criteria)
        self.evaluation = copy(bodg.evaluation)
        self.NA = copy(bodg.NA)
        self.relation = copy(bodg.relation)
        
        # normalize valuation to percentages
        self.recodeValuation(-100.0,100.0)
        Med = self.valuationdomain['med']
        
        # bin breaks per percent unit
        breaks = [(x,i) for i,x  in enumerate(range(-100,101))]
        
        # quantiles for cdf calls
        quantilesId = dict(breaks)
        if Debug:
            print(quantilesId)
            
        # initialize frequency and observation dictionaries
        frequency = {}
        valuationObservations = {}
        for x in self.actions:
            valuationObservations[x] = {}
            frequency[x] = {}
            for y in self.actions:
                valuationObservations[x][y] = []
                frequency[x][y] = [0 for i in range(len(breaks))]

        # initialize the weight modes
        weights = dict([(g,self.criteria[g]['weight']) for g in self.criteria])
        spread = Decimal(spread)
        if Debug:
            print(weights)
        for sample in range(sampleSize):
            if SeeSampleCounter:
                print(sample)
            if Debug:
                print('===>>> sample %d ' % (sample+1) )
            for g in self.criteria:
                lowerWeightLimit = float(weights[g]- (weights[g]*spread))
                upperWeightLimit = float(weights[g] + (weights[g]*spread))
                weightMode = float(weights[g])
                weightRange = upperWeightLimit - lowerWeightLimit
                if distribution == 'triangular':
                    rw = Decimal( '%.2f' % triangular(lowerWeightLimit,upperWeightLimit,weightMode) )
                elif distribution == 'uniform':
                    rw = Decimal( '%.2f' % uniform(lowerWeightLimit,upperWeightLimit) )
                elif distribution == 'beta(2,2)':
                    rw = Decimal( '%.2f' % (lowerWeightLimit+(betavariate(2,2)*weightRange)) )
                elif distribution == 'beta(4,4)':
                    rw = Decimal( '%.2f' % (lowerWeightLimit+(betavariate(4,4)*weightRange)) )
                elif distribution == 'extTriangular':
                    extTrRdv = ExtendedTriangularRandomVariable(lowLimit=float(weights[g])/2.0,
                                                                highLimit=float(weights[g])*2.0,
                                                                mode=weightMode,
                                                                seed=samplingSeed)
                    rw = Decimal( '%.2f' % ( extTrRdv.random() ) )
                else:
                    print('Error: wrong distribution %s. Available laws: triangular (default), uniform, beta(2,2), beta(12,12)' % distribution)        
                perfTab.criteria[g]['weight'] = rw
##                if Debug:
##                    print(self.criteria[g]['weight'],rw)
            srelation = self._constructRelation(perfTab.criteria,\
                                               perfTab.evaluation,\
                                               hasNoVeto = hasNoVeto,\
                                               hasBipolarVeto = hasBipolarVeto,\
                                               )
            for x in self.actions:
                for y in self.actions:
                    valuationObservations[x][y].append(srelation[x][y])
                    for i in range(len(breaks)):
                        if srelation[x][y] <= breaks[i][0]:
                            frequency[x][y][i] += 1
                            
        self.relationStatistics = {}
        for x in self.actions:
            self.relationStatistics[x] = {}
            for y in self.actions:
                self.relationStatistics[x][y] = {}              
                valuationObservations[x][y].sort()
##                if Debug and x == 'a04' and y == 'a05':
##                    print(x,y)
##                    print(valuationObservations[x][y])
                
##                q = sampleSize//2
##                if (sampleSize % 2) == 0:    
##                    median = (valuationObservations[x][y][q] + valuationObservations[x][y][q+1])/Decimal('2')
##                else:
##                    median = (valuationObservations[x][y][q])
##                print(median,self._computeQuantile(0.5,valuationObservations[x][y]))

                self.relationStatistics[x][y]['median'] = self._computeQuantile(0.5,valuationObservations[x][y])
                if Debug and x == 'a04' and y == 'a05':
                    print(frequency[x][y])
                    print(quantilesId)
                    print(frequency[x][y][quantilesId[0]])
                if self.relation[x][y] > Med:
                    self.relationStatistics[x][y]['likelihood'] = 1.0 - float(frequency[x][y][quantilesId[0]])/float(sampleSize)
                elif self.relation[x][y] <= Med:
                    self.relationStatistics[x][y]['likelihood'] = float(frequency[x][y][quantilesId[0]])/float(sampleSize)
                self._computeRelationStatistics(x,y,valuationObservations[x][y])
                if Debug:
                    print(self.relationStatistics[x][y])
                requiredLikelihood = likelihood
                if self.relationStatistics[x][y]['likelihood'] < requiredLikelihood:
                    self.relation[x][y] = self.valuationdomain['med']
                else:
                    self.relation[x][y] = Decimal('%.3f' % self.relationStatistics[x][y]['median'])
                
        #self.relationStatistics = deepcopy(relationStatistics)
        if Normalized:
            self.recodeValuation(-1,1)
        if Debug:
            self.valuationObservations = deepcopy(valuationObservations)
        # sampled valuations r(x,y) are observed in standard bipolar percentages, i.e. [-100,100]
        # the breaks are left closed integers and go from -100 to 100
        # the quantileId disctionary gives the
        self.frequency = frequency
        self.quantilesId = quantilesId
##        if Debug:
##            print(self.valuationObservations)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeCDF(self,x,y,rValue):
        """
        computes by interpolation the likelihood of a given rValue with respect to the sampled r(x,y) valuations.

        *Parameters*:

            * action key x
            * action key y
            * r(x,y)
            
        """
        from math import floor
        fval = (-100.0 + (float(rValue) - float(self.valuationdomain['min']))\
                /(float(self.valuationdomain['max'] - self.valuationdomain['min']))*200.0)
        val = int(floor(fval))
        #print(fval,val)
        if val < 100:
            #print(self.frequency[x][y][self.quantilesId[val]],self.frequency[x][y][self.quantilesId[val+1]])
            Fval = float(self.frequency[x][y][self.quantilesId[val]])/float(self.sampleSize)
            Fval1 = float(self.frequency[x][y][self.quantilesId[val+1]])/float(self.sampleSize)
            prob = Fval + ((fval - val)*(Fval1 - Fval))
        else:
            Fval = float(self.frequency[x][y][self.quantilesId[val]])/float(self.sampleSize)
            prob = Fval
        return prob
        
    def _computeQuantile(self,p,observations):
        """
        computes by interpolation the quantile of probability p of a list of sorted observations.
        """
        from math import floor,ceil
        n = len(observations)
        if p <= 0.0:
            quantile = observations[0]
        elif p >= 1.0:
            quantile = observations[-1]        
        else:
            q = (n)*p
            flq = floor(q)
            clq = ceil(q)
            quantile = float(observations[int(flq)])\
                   + (q-flq) * float(observations[int(clq)]- observations[int(flq)])
        return quantile

    def _computeRelationStatistics(self,x,y,observations):
        """
        Computes the pairwise relation statistics from the sampled observations.
        Results are stored in the self.relationStatistics[x][y] dictionary
        with keys = 'sd','Q0,'Q1,'Q3','Q4'.
        """
        from math import sqrt
        n = len(observations)
        fn = float(n)
        mean = 0.0
        meansq2 = 0.0 
        for v in observations:
            fv = float(v)
            mean += fv
            meansq2 += (fv * fv)
        mean /= fn
        self.relationStatistics[x][y]['mean'] = mean
        variance = (meansq2 / fn) - (mean*mean)
        self.relationStatistics[x][y]['sd'] = sqrt(variance)
        self.relationStatistics[x][y]['Q0'] = float(min(observations))
        self.relationStatistics[x][y]['Q1'] = self._computeQuantile(0.25,observations)
        self.relationStatistics[x][y]['Q3'] = self._computeQuantile(0.75,observations)
        self.relationStatistics[x][y]['Q4'] = float(max(observations))

    def showRelationTable(self,IntegerValues=False,
                          actionsSubset= None,
                          hasLPDDenotation=False,
                          hasLatexFormat=False,
                          hasIntegerValuation=False,
                          relation=None):
        """
        specialising BipolarOutrankingDigraph.showRelationTable() for stochstic instances.
        """
        print('Stochastic outranking digraph %s' % self.name)
        print('Sampling size: %d' % self.sampleSize)
        print('Likelihood of Condorcet digraph: %.2f' % self.likelihood)
        BipolarOutrankingDigraph.showRelationTable(self,IntegerValues=IntegerValues,
                          actionsSubset= actionsSubset,
                          hasLPDDenotation=hasLPDDenotation,
                          hasLatexFormat=hasLatexFormat,
                          hasIntegerValuation=hasIntegerValuation,
                          relation=relation)

    def computeCLTLikelihoods(self,distribution="triangular",Debug=False):
        """
        Renders the pairwise CLT likelihood of the at least as good as relation
        neglecting all considerable large performance differences polarisations.
        """
        from decimal import Decimal
        from math import sqrt
        from scipy import stats
        from scipy.stats import norm
        actionsList = [x for x in self.actions]
        sumWeights = Decimal('0')
        criteriaList = [x for x in self.criteria]
        m = len(criteriaList)
        weightSquares = {}
        for g in criteriaList:
            gWeight = abs(self.criteria[g]['weight'])
##            if Debug:
##                print(g,gWeight)
            weightSquares[g] = gWeight*gWeight
            sumWeights += gWeight
##        if Debug:
##            print(sumWeights)
##            print(weightSquares)
        g = BipolarOutrankingDigraph(self,hasNoVeto=True)
        g.recodeValuation(-sumWeights,sumWeights)
        if Debug:
            g.showRelationTable()
        ccf = {}
        if distribution == 'uniform':
            varFactor = Decimal('1')/Decimal('3')
        elif distribution == 'triangular':
            varFactor = Decimal('1')/Decimal('6')
        elif distribution == 'beta(2,2)':
            varFactor = Decimal('1')/Decimal('5')
        elif distribution == 'beta(4,4)':
            varFactor = Decimal('1')/Decimal('9')
        for x in actionsList:
            ccf[x] = {}
            for y in actionsList:
                ccf[x][y] = {'std': Decimal('0.0')}
                for c in criteriaList:
                    ccf[x][y][c] = g.criterionCharacteristicFunction(c,x,y)
                    ccf[x][y]['std'] += abs(ccf[x][y][c])*weightSquares[c]
##                    if Debug:
##                        print(c,x,y,ccf[x][y][c])
                ccf[x][y]['std'] = sqrt(varFactor*ccf[x][y]['std'])
##                if Debug:
##                    print(x,y,ccf[x][y]['std'])
        lh = {}
        for x in actionsList:
            lh[x] = {}
            for y in actionsList:
                n = norm(float(g.relation[x][y]),float(ccf[x][y]['std']))
                lh[x][y] = {}
                if g.relation[x][y] > g.valuationdomain['med']:
                    lh[x][y] = 1.0 - n.cdf(0.0)
                else:
                    lh[x][y] = n.cdf(0.0)
                if Debug:
                    print(x,y,lh[x][y])
        return lh


    def showRelationStatistics(self,argument='likelihoods',
                          actionsSubset= None,
                          hasLatexFormat=False,
                          Bipolar=False):
        """
        prints the relation statistics in actions X actions table format.
        """
        from math import copysign
##        if hasLPDDenotation:
##            try:
##                largePerformanceDifferencesCount = self.largePerformanceDifferencesCount
##                gnv = BipolarOutrankingDigraph(self.performanceTableau,hasNoVeto=True)
##                recodeValuation(self.valuationdomain['min'],self.valuationdomain['max'])
##            except:

        hasLPDDenotation = False
            
        if actionsSubset is None:
            actions = self.actions
        else:
            actions = actionsSubset
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                if argument == 'likelihoods':
                    if Bipolar:
                        relation[x][y] =\
        copysign( ((2.0 * self.relationStatistics[x][y]['likelihood']) - 1.0),
                   self.relation[x][y])
                    else:
                        relation[x][y] = self.relationStatistics[x][y]['likelihood']
                elif argument == 'medians':
                    relation[x][y] = self.relationStatistics[x][y]['median']
                elif argument == 'means':
                    relation[x][y] = self.relationStatistics[x][y]['mean']
                
            
        print('* ---- Relation statistics -----\n', end=' ')
        if argument == 'likelihoods':
            print(' 0 p-val | ', end=' ')
        elif argument == 'means':
            print(' mean  | ', end=' ')
        elif argument == 'medians':
            print('  med  | ', end=' ')
            
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(x,x)]
        actionsList.sort()

##        try:
##            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
##        except KeyError
        hasIntegerValuation = False
        
        for x in actionsList:
            print("'"+x[0]+"',  ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in actionsList:
            if hasLatexFormat:
                print("$"+x[0]+"$ & ", end=' ')
            else:
                print("'"+x[0]+"' |  ", end=' ')
            for y in actionsList:
                if hasIntegerValuation:
                    if hasLPDDenotation:
                        print('%+d ' % (relation[x[1]][y[1]]), end=' ')
                    elif hasLatexFormat:
                        print('$%+d$ &' % (relation[x[1]][y[1]]), end=' ')
                    else:
                        print('%+d ' % (relation[x[1]][y[1]]), end=' ')
                else:
                    if hasLPDDenotation:
                        print('%+2.2f ' % (relation[x[1]][y[1]]), end=' ')
                    elif hasLatexFormat:
                        print('$%+2.2f$ & ' % (relation[x[1]][y[1]]), end=' ')       
                    else:
                        print('%+2.2f ' % (relation[x[1]][y[1]]), end=' ')
                
            if hasLatexFormat:
                print(' \\cr')
            else:
                print()
            if hasLPDDenotation:
                print("'"+x[0]+"' | ", end=' ')
                for y in actionsList:
                    print('(%+d,%+d)' % (largePerformanceDifferencesCount[x[1]][y[1]]['positive'],\
                                          largePerformanceDifferencesCount[x[1]][y[1]]['negative']), end=' ')
                print()
            
                
        print('\n')
    

class CoalitionsOutrankingsFusionDigraph(BipolarOutrankingDigraph):
    """
    With a list of criteria coalitions, a fusion digraph is constructed form the fusion of the corresponding marginal coalitions restricted bipolar outranking digraphs.

    When *coalitionsList* is None, an 'o-average' fusion of the decision objectives restricted outranking digraphs is produced (see *UnOpposedBipolarOutrankingDigraph* class).
    """
    def __init__(self,argPerfTab,
                     coalitionsList=None,
                     actionsSubset=None,
                     CopyPerfTab=True,
                     Comments=False):
        from copy import deepcopy
        from time import time

        # set initial time stamp
        tt = time()
        
        # ----  performance tableau data input 
        if argPerfTab is None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab

        # transfering the performance tableau data to self
        self.name = 'objectivesFusion_' + perfTab.name
        # actions
        if actionsSubset is None:
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
     
        # valuation domain
        Min =   Decimal('-1.0')
        Med =   Decimal('0.0')
        Max =   Decimal('1.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        try:
            self.valuationdomain['precision'] = perfTab.valuationPrecision
        except:
            self.valuationdomain['precision'] = Decimal('0')
 
        # objectives and criteria
        try:
            if CopyPerfTab:
                self.objectives = deepcopy(perfTab.objectives)
                self.criteria = deepcopy(perfTab.criteria)
            else:
                self.objectives = perfTab.objectives
                self.criteria = perfTab.criteria
        except:
            pass

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
        try:
            if CopyPerfTab:
                self.description = deepcopy(perfTab.description)
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
        if coalitionsList is None:
            try:
                objectives = self.objectives
                coalitionsList = [objectives[obj]['criteria'] for obj in objectives]
                #print(coalitionsList)
            except:
                print('!!! Error: No coalitions given and performance tableau has no objectives')
                return
        marginalRelations = {}
        marginalDigraphs = []
        for coalition in coalitionsList:
            mg = BipolarOutrankingDigraph(perfTab,criteriaSubset=coalition)
            marginalRelations[tuple(coalition)] = deepcopy(mg.relation)
            marginalDigraphs.append(mg)
        weights = []
        for coalition in coalitionsList:
            sumMarginalWeights = Decimal('0')
            for g in coalition:
                sumMarginalWeights += self.criteria[g]['weight']
            weights.append(sumMarginalWeights)            
        #weights = [objectives[obj]['weight'] for obj in objectives]
        fg = FusionLDigraph(marginalDigraphs,'o-average',weights)
        self.relation = deepcopy(fg.relation)
        self.marginalRelationsRelations = marginalRelations

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


class UnOpposedBipolarOutrankingDigraph(CoalitionsOutrankingsFusionDigraph):
    """
    When operating an *o-average* fusion of the mariginal outranking digraphs restricted to the coalition of criteria supporting each decision objective, we obtain **unopposed** outranking situtations, namely *validated* by one or more decision objectives without being *invalidated* by any other decision objective. 

    These positive, as well as negative outranking characteristics, appear hence stable with respect to the importance of the decision objectives when proportional criteria significances are given. 

    Furthermore, polarising the outranking digraph with considerable performance differences is here restricted to each decision objective, which makes it easier to decide on veto discrimination thresholds.
   
    """

    def __init__(self,argPerfTab,actionsSubset=None,
                 CopyPerfTab=True,Comments=False):

                 
        from copy import deepcopy
        for att in argPerfTab.__dict__:
            self.__dict__[att] = argPerfTab.__dict__[att]
        try:
            coalitions = [self.objectives[obj]['criteria'] for obj in self.objectives]
            if Comments:
                print('coalitions:',coalitions)
        except:
            print('!! Error: the given performance tableau does not contain objectives.')
            return
        uoo = CoalitionsOutrankingsFusionDigraph(argPerfTab,\
                                            CopyPerfTab=False,\
                                            coalitionsList=coalitions,\
                                            actionsSubset=actionsSubset,\
                                            Comments=Comments)
        for att in uoo.__dict__:
            self.__dict__[att] = uoo.__dict__[att]
        self.name += '_unopposed_outrankings'
        if Comments:
            print(self)

    def computeOppositeness(self,InPercents=False):
        """
        Computes the degree in *[0.0, 1.0]* of oppositeness --**preferential disagreement**-- of the multiple decision objectives.
        
        Renders a dictionary with three entries:

        - *standardSize* : size of the corresponding
          standard bipolar-valued outranking digraph;
        - *unopposedSize* : size of the the corresponding
          unopposed bipolar-valued outranking digraph;
        - *oppositeness* : (1.0 - unopposedSize/standardSize);
          if *InPercents* has value True, the *oppositeness* is rendered in percents format.
    
        """
        from outrankingDigraphs import BipolarOutrankingDigraph
        du = self.computeSize()
        g = BipolarOutrankingDigraph(self)
        d = g.computeSize()
        if InPercents:
            op = (1.0 -(du/d))*100.0
        else:
            op = (1.0 -(du/d))
        return {'standardSize': d, 'unopposedSize': du, 'oppositeness': op}
        
        
class SymmetricAverageFusionOutrankingDigraph(BipolarOutrankingDigraph):
    """
    in development !
    """
    def __init__(self,argPerfTab,actionsSubset=None,coalition=None,
                 CopyPerfTab=True,Normalized=True,Comments=False):
        from copy import deepcopy
        from time import time

        # set initial time stamp
        tt = time()
        
        # ----  performance tableau data input 
        if argPerfTab is None:
            print('Performance tableau required !')
            #perfTab = RandomPerformanceTableau(commonThresholds = [(10.0,0.0),(20.0,0.0),(80.0,0.0),(101.0,0.0)])
        elif isinstance(argPerfTab,(str)):
            perfTab = PerformanceTableau(argPerfTab)
        else:
            perfTab = argPerfTab

        # transfering the performance tableau data to self
        self.name = 'symAvFusion_' + perfTab.name
        # actions
        if actionsSubset is None:
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
     
        # valuation domain
        if Normalized:
            Min =   Decimal('-1.0')
            Med =   Decimal('0.0')
            Max =   Decimal('1.0')
        else:
            Min =   Decimal('-100.0')
            Med =   Decimal('0.0')
            Max =   Decimal('100.0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        try:
            self.valuationdomain['precision'] = perfTab.valuationPrecision
        except:
            self.valuationdomain['precision'] = Decimal('0')
 
        # objectives and criteria
        try:
            if CopyPerfTab:
                self.objectives = deepcopy(perfTab.objectives)
            else:
                self.objectives = perfTab.objectives
        except:
            pass
        criteria = OrderedDict()
        if coalition is None:
            coalition = perfTab.criteria.keys()
        for g in coalition:
            if CopyPerfTab:
                criteria[g] = deepcopy(perfTab.criteria[g])
            else:
                criteria[g] = perfTab.criteria[g]
        self.criteria = criteria
        self.convertWeight2Decimal()

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
        try:
            if CopyPerfTab:
                self.description = deepcopy(perfTab.description)
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
        margG = []
        for g in criteria:
            gg = BipolarOutrankingDigraph(perfTab,coalition=[g],\
                                          CopyPerfTab=CopyPerfTab,\
                                          Normalized=True)
            margG.append(gg)
        weights = [criteria[g]['weight'] for g in criteria]
        fg = FusionLDigraph(margG,'o-average',weights)
        self.relation = deepcopy(fg.relation)
        
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


class _RubisRestServer(ServerProxy):
    """
    xmlrpc-cgi Proxy Server for accessing on-line
    a Rubis Rest Solver.
    Deprecated !
    """
    def __init__(self,host="https://leopold-loewenheim.uni.lu/cgi-bin/xmlrpc_cgi.py",Debug=False):
        """
        Rubis Rest Server connection.
        """
        import sys,xmlrpc.client,ssl
        self._server = xmlrpc.client.ServerProxy(host)
        
        if Debug:
            print("host=%s" % host)
            try:           
                response = self._server.hello()
                print (response['message'])
                print("available service ports")
                for m in self._server.system.listMethods():
                    if 'system' not in m:
                        print (m, self._server.system.methodHelp(m))

            except xmlrpc.client.Fault as faultobj:
                print ("Rubis Server error:", faultobj.faultCode)
                print (">>> %s <<<" % faultobj.faultString)
                return None

            except:
                print ("Client Error: '%s/%s'" % (sys.exc_info()[0],sys.exc_info()[1]))
                return None
            
    def ping(self,Debug=False):
        response = self._server.hello()
        print(response['message'])
        if Debug:
            print("available service ports")
            for m in self._server.system.listMethods():
                if 'system' not in m:
                    print (m, self._server.system.methodHelp(m))

    def submitProblem(self,perfTab,\
                      valuation='bipolar',\
                      hasVeto=True,\
                      argTitle='XMCDA 2.0 encoding',\
                      Debug=False):
        """
        Submit PerformanceTableau class instances.

        *Parameters*:

             * valuation: 'bipolar', 'robust', 'integer'
             * hasVeto: Switch on or off vetoes
             * argTitle: set specific application title

        """
        self.name = perfTab.name
        self.problemText = perfTab.saveXMCDA2(isStringIO=True,\
                                         valuationType=valuation,\
                                         servingD3=False,\
                                         comment='Rubis Rest Server generated',\
                                         hasVeto = hasVeto,
                                         title = argTitle)
        self.valuation = valuation
        arg = {'problemFile': self.problemText}
        if Debug:
            print(arg)
        answer = self._server.submitProblem(arg)
        self.ticket = answer['ticket'] 
        print(answer['message'])
        print('Server ticket: %s' % answer['ticket'])
        fileNameTicket = self.name+'Ticket.txt'
        fo = open(fileNameTicket,'w')
        fo.write(answer['ticket'])
        fo.close()

    def submitXMCDA2Problem(self,fileName,valuation=None,Debug=False):
        """
        Submit stored XMCDA 2.0 encoded performance tableau.

        .. warning::

            An <_.xml> file extension is assumed !
            
        """
        print("Calling submitXMCDA2Problem(%s)" % fileName)
        self.name = fileName
        fileNameExt = fileName + '.xml'
        fi = open(fileNameExt,'r')
        self.problemText = fi.read()
        fi.close()
        self.valuation = valuation
        arg = {'problemFile': self.problemText}
        if Debug:
            print(arg)
        answer = self._server.submitProblem(arg)
        self.ticket = answer['ticket'] 
        print(answer['message'])
        print(answer['ticket'])
        fileNameTicket = fileName+'Ticket.txt'
        fo = open(fileNameTicket,'w')
        fo.write(answer['ticket'])
        fo.close()

    def saveXMCDA2Solution(self,fileName=None,Debug=False):
        """
        Save the solution in XMCDA 2.0 encoding.
        """
        if fileName is None:
            fileNameExt = "Solution"+str(self.ticket)+".xml"
        else:
            fileNameExt = fileName+"Solution.xml"
        arg = {'ticket': self.ticket}
        answer = self._server.requestSolution(arg)
        try:
            self.solution = answer['solution']
            if Debug:
                print(self.solution)
            fo = open(fileNameExt,'w')
            fo.write(self.solution)
            fo.close()
            print("saving solution in file %s" %fileNameExt)
        except:
            print(answer['message'])

    def showHTMLSolution(self,ticket=None,valuation='bipolar'):
        """
        Show XMCDA 2.0 solution in a default browser window.
        The valuation parameter may set the correct style sheet.
        

        *Parameter*:
        
            * valuation: 'bipolar' or 'robust'.
              By default the valuation type is set
              automatically at problem submission.

        """
        import os,webbrowser
        newTab = 2 # open in a new tab if possible
        if ticket is not None:
            self.ticket = ticket
        if valuation is None:
            try:
                valuation = self.valuation
                if valuation is None:
                    valuation = 'bipolar'
            except:
                if valuation is None:
                    valuation = 'bipolar'
        arg = {'ticket': self.ticket, 'valuation': valuation}
        answer = self._server.requestSolutionHTML(arg)
        try:
            fileName = str(self.name)+str(self.ticket)+"Solution.html"
            fo = open(fileName,'w')
            fo.write(answer['html'])
            fo.close()
            url = "file://"+os.getcwd()+"/%s" % fileName
            webbrowser.open(url,new=newTab)
        except:
            print(answer['message'])

################################################################ 
#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    import copy
    from time import time, sleep
    from random import randint
    from outrankingDigraphs import BipolarOutrankingDigraph
    from transitiveDigraphs import RankingByChoosingDigraph
    print("""
    ****************************************************
    * Digraph3 outrankingDigraphs module               *
    * Copyright (C) 2011-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)
    
    print('*-------- Testing classes and methods -------')

    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    t = Random3ObjectivesPerformanceTableau(
                                    numberOfActions=500,\
                                    numberOfCriteria=7,\
                                    vetoProbability=0.2,\
                                    seed=1)
    g = BipolarOutrankingDigraph(t,Threading=True,
                                 startMethod=None,
                                 nbrCores=10,Comments=True)
    print(g)
    t0 = time()
    g.showHTMLPerformanceHeatmap(Correlations=True,Threading=False)
    print(time()-t0)
    #g.showPolarisations()
    #g.showObjectives()
    # ranking = g.computeNetFlowsRanking()
    # sizeOfDiagonal = 5
    # quasiRelation = {}
    # Med = g.valuationdomain['med']
    # for x in g.actions:
    #     quasiRelation[x] = {}
    #     xi = ranking.index(x)
    #     for y in g.actions:
    #         yj = ranking.index(y)
    #         #if abs(xi-yj) > sizeOfDiagonal:
    #         #    quasiRelation[x][y] = g.relation[x][y]
    #         if xi >= yj:
    #             quasiRelation[x][y] = min(Med, g.relation[x][y])
    #         else:
    #             quasiRelation[x][y] = max(Med, g.relation[x][y])
    # g.relation = quasiRelation
    # gcd = ~(-g)
    # gcd.showHTMLRelationHeatmap(actionsList=ranking,colorLevels=9)
  
#############################
############################
