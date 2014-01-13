#!/usr/bin/env python3
# Python3+ implementation of digraphs
# Based on Python 2 $Revision: 1.697 $
# Copyright (C) 2006-2014  Raymond Bisdorff
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
from perfTabs import *
from outrankingDigraphs import *
from weakOrders import *

class WeakOrder(Digraph):
    """
    Abstract class for weak orderings' specialized methods.
    """
    
    def showWeakOrder(self,rankingByChoosing=None):
        """
        A show method for self.rankinByChoosing result.
        """
        if rankingByChoosing == None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                print('Error: You must first run self.computeRankingByChoosing(CoDual=True(default)|False) !')
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
            print(' %s%s%s ranked %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
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
            print(' %s%s%s last ranked %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))        

    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        Dummy name for showWeakOrder() method
        """
        self.showWeakOrder(rankingByChoosing=rankingByChoosing)
    
    def showOrderedRelationTable(self,direction="decreasing",originalRelation=False):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """ 

        actionsList = []
        
        if direction == "decreasing":
            print('Decrasing Weak Ordering')
            self.showRankingByBestChoosing()
            try:
                ordering = self.rankingByBestChoosing
            except:
                ordering = self.computeRankingByBestChoosing(Debug=False)
        elif direction == "increasing":
            print('Increasing Weak Ordering')
            self.showRankingByLastChoosing()
            try:
                ordering = self.rankingByLastChoosing
            except:
                ordering = self.computeRankingByLastChoosing()
        else:
            print('Direction error !: %s is not a correct instruction (decreasing=default or increasing)' % direction)

        for eq in ordering['result']:
            #print(eq[1])
            eq = eq[1]
            eq.sort()
            for x in eq:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error !: missing action(s) %s in ordered table.')

        if originalRelation:
            showRelation = self.originalRelation
        else:
            showRelation = self.relation
            
        self.showRelationTable(actionsSubset=actionsList,\
                                relation=showRelation,\
                                Sorted=False,\
                                ReflexiveTerms=False)        

class RankingByChoosingDigraph(WeakOrder):
    """
    Specialization of the abstract WeakOrder class for 
    ranking-by-Rubis-choosing orderings.
    
    Example python3 session:
    
    >>> from outrankingDigraphs import *
    >>> t = RandomCBPerformanceTableau(numberOfActions=7,\ 
                numberOfCriteria=5,\ 
                weightDistribution='equiobjectives')
    >>> g = BipolarOutrankingDigraph(t,Normalized=True)
    >>> g.showRelationTable()
    * ---- Relation Table -----
      S   | 'a01'  'a02'  'a03'  'a04'  'a05'  'a06'  'a07'   
    ------|-------------------------------------------------
    'a01' | +0.00  +0.00  +0.67  +0.00  -0.67  -0.33  -0.17  
    'a02' | +0.00  +0.00  +1.00  +0.17  +0.00  -0.50  +0.33  
    'a03' | -0.33  -1.00  +0.00  -1.00  -0.67  -1.00  -0.33  
    'a04' | +0.00  +0.17  +1.00  +0.00  +0.00  -0.50  +0.00  
    'a05' | +0.67  +0.00  +1.00  +0.00  +0.00  -0.33  +1.00  
    'a06' | +0.67  +1.00  +1.00  +1.00  +0.33  +0.00  +0.33  
    'a07' | +0.67  +0.00  +1.00  +0.00  -0.17  -0.33  +0.00 
    >>> (~(-g)).exportGraphViz('weakOrdering')
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to converse-dual_rel_randomCBperftab.dot
    dot -Grankdir=BT -Tpng converse-dual_rel_randomCBperftab.dot 
       -o weakOrdering.png 
        
    .. image:: weakOrdering.png
        
    >>> from weakOrders import RankingByChoosingDigraph
    >>> rbc = RankingByChoosingDigraph(g)
    >>> rbc.showWeakOrder()
    Ranking by Choosing and Rejecting
    1st ranked ['a06'] (0.50)
        2nd ranked ['a02', 'a04', 'a05'] (0.14)
        2nd last ranked ['a01', 'a04', 'a07'] (0.14)
    1st last ranked ['a03'] (0.72)
    >>> rbc.showOrderedRelationTable(direction="decreasing")
    * ---- Relation Table -----
      S   | 'a06'  'a02'  'a05'  'a04'	'a01'  'a07'  'a03'	  
    ------|-------------------------------------------------
    'a06' |   -    +1.00  +0.33	 +1.00	+0.67  +0.33  +1.00	 
    'a02' | -0.50    -    +0.00  +0.00  +0.00  +0.33  +1.00	 
    'a05' | -0.33  +0.00    -    +0.00  +0.67  +1.00  +1.00	 
    'a04' | -0.50  +0.00  +0.00	   -    +0.00  +0.00  +1.00	 
    'a01' | -0.33  +0.00  -0.67	 +0.00	  -    +0.00  +0.67	 
    'a07' | -0.33  +0.00  -0.17	 +0.00	+0.00    -    +1.00	 
    'a03' | -1.00  -1.00  -0.67	 -1.00	-0.33  -0.33  +0.00	 
    """
    def __init__(self,other,
                 fusionOperator = "o-min",
                 CoDual=False,
                 Debug=False,
                 Threading=False):
        
        from copy import deepcopy
        from pickle import dumps, loads, load

        if Threading:
            from multiprocessing import Process, Lock, active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID, name, direction, Codual, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.direction = direction
                    self.Codual = Codual
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    if Debug:
                        print("Starting " + self.name)
                    #threadLock.acquire()
                    fi = open('dumpDigraph.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    if self.direction == 'best':
                        fo = open('rbbc.py','wb')
                        rbbc = digraph.computeRankingByBestChoosing(CoDual=CoDual,Debug=Debug)
                        fo.write(dumps(rbbc,-1))
                    elif self.direction == 'worst':
                        fo = open('rbwc.py','wb')
                        rbwc = digraph.computeRankingByLastChoosing(CoDual=CoDual,Debug=Debug)
                        fo.write(dumps(rbwc,-1))
                    fo.close()
                    #threadLock.release()
                    
        digraph=deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        self.actions = deepcopy(digraph.actions)
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        self.originalRelation = digraph.relation

        if Threading and cpu_count()>2:
            print('Threading ...')
            fo = open('dumpDigraph.py','wb')
            pd = dumps(digraph,-1)
            fo.write(pd)
            fo.close()
            #threadLock = Lock()
            #threads = []

            threadBest = myThread(1,"ComputeBest","best",CoDual,Debug)
            threadWorst = myThread(2,"ComputeWorst","worst",CoDual,Debug)
            threadBest.start()
            #threads.append(threadBest)
            threadWorst.start()
            #threads.append(threadWorst)

            #for th in threads:
            #    th.join()
            #if Debug:
            while active_children() != []:
                pass
            print('Exiting both computing threads')
            fi = open('rbbc.py','rb')
            digraph.rankingByBestChoosing = loads(fi.read())
            fi.close()
            fi = open('rbwc.py','rb')
            digraph.rankingByLastChoosing = loads(fi.read())
            fi.close()
            
        else:
            digraph.computeRankingByBestChoosing(CoDual=CoDual,Debug=Debug)
            digraph.computeRankingByLastChoosing(CoDual=CoDual,Debug=Debug)
            
        relBest = digraph.computeRankingByBestChoosingRelation()
        if Debug:
                digraph.showRankingByBestChoosing()
        relLast = digraph.computeRankingByLastChoosingRelation()
        if Debug:
            digraph.showRankingByLastChoosing()
        relFusion = {}
        for x in digraph.actions:
            relFusion[x] = {}
            for y in digraph.actions:
                if fusionOperator == "o-max":
                    relFusion[x][y] = digraph.omax((relBest[x][y],relLast[x][y]))
                elif fusionOperator == "o-min":
                    relFusion[x][y] = digraph.omin((relBest[x][y],relLast[x][y]))
                else:
                    print('Error: invalid epistemic fusion operator %s' % operator)
                if Debug:
                    print('!',x,y,relBest[x][y],relLast[x][y],relFusion[x][y])  
        self.relation=relFusion
        self.rankingByLastChoosing = deepcopy(digraph.rankingByLastChoosing)
        self.rankingByBestChoosing = deepcopy(digraph.rankingByBestChoosing)
        self.computeRankingByChoosing()
        if Debug:
            self.showRankingByChoosing()
        
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showWeakOrder(self,rankingByChoosing=None):
        """
        specialisation for RankingByChoosing Digraphs.
        """
        if rankingByChoosing == None:
            try:
                rankingByChoosing = self.rankingByChoosing
            except:
                rankingByChoosing = self.computeRankingByChoosing()

        WeakOrder.showWeakOrder(self,rankingByChoosing)

    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        Dummy for showWeakOrder method
        """
        self.showWeakOrder(rankingByChoosing=rankingByChoosing)

    def computeRankingByBestChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            WeakOrder.computeRankingByBestChoosing(self)

    def computeRankingByLastChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            WeakOrder.computeRankingByLastChoosing(self)
 
class RankingByBestChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization of abstrct WeakOrder class for computing a ranking by best-choosing.
    """
    def __init__(self,digraph,Normalized=True,CoDual=False,Debug=False):
        from copy import deepcopy
        digraphName = 'ranking-by-best'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        digraph.computeRankingByBestChoosing(CoDual=CoDual,Debug=False)
        self.relation = digraph.computeRankingByBestChoosingRelation()
        if Normalized:
            self.recodeValuation(-1,1)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.rankingByBestChoosing = digraph.rankingByBestChoosing
        
    def showWeakOrder(self):
        self.showRankingByBestChoosing()


class RankingByLastChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization of abstract WeakOrder class for computing a ranking by rejecting.
    """
    def __init__(self,digraph,Normalized=True,CoDual=False,Debug=False):
        from copy import deepcopy
        digraphName = 'ranking-by-last'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        digraph.computeRankingByLastChoosing(CoDual=CoDual,Debug=False)
        self.relation = digraph.computeRankingByLastChoosingRelation()
        if Normalized:
            self.recodeValuation(-1,1)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.rankingByLastChoosing = digraph.rankingByLastChoosing
    
    def showWeakOrder(self):
        self.showRankingByLastChoosing()


class RankingByPrudentChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization for ranking-by-rejecting results with prudent single elimination of chordless circuits. By default, the cut level for circuits elimination is set to 20% of the valuation domain maximum (1.0).
    """
    def __init__(self,digraph,CoDual=False,Normalized=True,Odd=True,Limited=0.2,Comments=False,Debug=False,SplitCorrelation=True):
        from copy import deepcopy
        from time import time
        if Comments:          
            t0 = time()
            print('------- Commenting ranking by prudent choosing ------')
        digraph_ = deepcopy(digraph)
        if Normalized:
            digraph_.recodeValuation(-1,1)
        digraphName = 'sorting-by-prudent-choosing'+digraph_.name
        self.name = digraphName
        self.actions = deepcopy(digraph_.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(digraph_.valuationdomain)
        s1 = RankingByLastChoosingDigraph(digraph_,CoDual=CoDual,Debug=False)
        s2 = RankingByBestChoosingDigraph(digraph_,CoDual=CoDual,Debug=False)
        fus = FusionDigraph(s1,s2)
        cutLevel = min(digraph_.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments),Decimal(Limited))
        self.cutLevel = cutLevel
        if cutLevel > self.valuationdomain['med']:
            if cutLevel < self.valuationdomain['max']:
                gp = PolarisedDigraph(digraph_,level=cutLevel,StrictCut=True)
            else:
                gp = PolarisedDigraph(digraph_,level=cutLevel,StrictCut=False)
            s1p = RankingByLastChoosingDigraph(gp,CoDual=CoDual,Debug=False)
            s2p = RankingByBestChoosingDigraph(gp,CoDual=CoDual,Debug=False)
            fusp = FusionDigraph(s1p,s2p)
            corrgp = digraph_.computeOrdinalCorrelation(fusp)
            corrg = digraph_.computeOrdinalCorrelation(fus)
            if Comments:
                print('Correlation with cutting    : %.3f x %.3f = %.3f' % (corrgp['correlation'],corrgp['determination'],corrgp['correlation']*corrgp['determination']))
                print('Correlation without cutting : %.3f x %.3f = %.3f' % (corrg['correlation'],corrg['determination'],corrg['correlation']*corrg['determination']))
            if SplitCorrelation:
                if corrgp['correlation'] > corrg['correlation']:           
                    self.relation = deepcopy(fusp.relation)
                    self.rankingByBestChoosing = sp2.rankingByBestChoosing
                    self.rankingByLastChoosing = sp1.rankingByLastChoosing
                else:
                    self.relation = deepcopy(fus.relation)
                    self.rankingByBestChoosing = s2.rankingByBestChoosing
                    self.rankingByLastChoosing = s1.rankingByLastChoosing
            else:
                if (corrgp['correlation']*corrgp['determination']) > (corrg['correlation']*corrg['determination']):
                    self.relation = deepcopy(fusp.relation)
                    self.rankingByBestChoosing = sp2.rankingByBestChoosing
                    self.rankingByLastChoosing = sp1.rankingByLastChoosing
                else:
                    self.relation = deepcopy(fus.relation)                
                    self.rankingByBestChoosing = s2.rankingByBestChoosing
                    self.rankingByLastChoosing = s1.rankingByLastChoosing
        else:
            self.relation = deepcopy(fus.relation)
            self.rankingByBestChoosing = s2.rankingByBestChoosing
            self.rankingByLastChoosing = s1.rankingByLastChoosing

        #self.rankingByChoosing = self.computeRankingByChoosing(CoDual=CoDual)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Comments:
            t1 = time()
            gdeter = digraph_.computeDeterminateness()
            self.showWeakOrder()
            print('Circuits cutting level limit  : %.3f' % Limited)
            print('Circuits elimination cut level: %.3f' % self.cutLevel)
            print('Ordinal Correlation with given outranking')
            corr = digraph_.computeOrdinalCorrelation(self)
            print('Correlation     : %.3f' % corr['correlation'])
            print('Determinateness : %.3f (%.3f)' % (corr['determination'],gdeter))
            print('Execution time  : %.4f sec.' % (t1-t0))


class PrincipalInOutDegreesOrdering(WeakOrder):
    """
    Specialization of abstract WeakOrder class for ranking by fusion
    of the principal orders of the variance-covariance of in- 
    (Colwise) and outdegrees (Rowwise).
    
    Example Python3 session with same outranking digraph g as shown in the RankingByChoosingDigraph example session (see below). 
    
    
    >>> from weakOrders import PrincipalInOutDegreesOrdering
    >>> pro = PrincipalInOutDegreesOrdering(g,imageType="png",\ 
                     plotFileName="proWeakOrdering")
    >>> pro.showWeakOrder()
    Ranking by Choosing and Rejecting
     1st ranked ['a06'] (1.00)
       2nd ranked ['a05'] (1.00)
         3rd ranked ['a02'] (1.00)
           4th ranked ['a04'] (1.00)
           4th last ranked ['a04'] (1.00)
         3rd last ranked ['a07'] (1.00)
       2nd last ranked ['a01'] (1.00)
     1st last ranked ['a03'] (1.00)
    >>> pro.showPrincipalScores(ColwiseOrder=True)
    List of principal scores
    Column wise covariance ordered
    action 	 colwise 	 rowwise
    a06 	 15.52934 	 13.74739
    a05 	 7.71195 	 4.95199
    a02 	 3.40812 	 0.70554
    a04 	 2.76502 	 0.15189
    a07 	 0.66875 	 -1.77637
    a01 	 -3.19392 	 -5.36733
    a03 	 -18.51409 	 -21.09102

    .. image:: proWeakOrdering_Colwise.png
    
    """
    def __init__(self,other,fusionOperator="o-min",imageType=None,plotFileName=None,Debug=False):
        from copy import deepcopy
        from linearOrders import PrincipalOrder
        digraph = deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        if isinstance(digraph.actions,list):
            self.actions = {}
            for x in digraph.actions:
                self.actions[x] = {}
                self.actions[x]['name'] = x
        else:
            self.actions = deepcopy(digraph.actions)
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        pl = PrincipalOrder(digraph,Colwise=False,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        if Debug:
            print('Row wise: ')
            print(pl.principalRowwiseScores)
            pl.computeOrder()
        self.principalRowwiseScores = pl.principalRowwiseScores
        for x in pl.principalRowwiseScores:
            self.actions[x[1]]['principalRowwiseScore'] = x[0]
        pc = PrincipalOrder(digraph,Colwise=True,imageType=imageType,
                            plotFileName=plotFileName,Debug=Debug)
        if Debug:
            print('Column wise: ')
            print(pc.principalColwiseScores)
            pc.computeOrder()
        self.principalColwiseScores = pc.principalColwiseScores
        for x in pc.principalColwiseScores:
            self.actions[x[1]]['principalColwiseScore'] = x[0]
        pf = FusionDigraph(pl,pc,operator=fusionOperator)
        self.relation = deepcopy(pf.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.computeRankingByChoosing()
        if Debug:
            print(self.computeOrdinalCorrelation(digraph))

    def showPrincipalScores(self, ColwiseOrder=False, RowwiseOrder=False):
        """
        showing the principal in- (Colwise) and out-degrees (Rowwise) scores.
        """
        print('List of principal scores')
        if not ColwiseOrder and not RowwiseOrder:
            print('action \t colwise \t rowwise')
            for x in self.actions:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
        elif ColwiseOrder:
            print('Column wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalColwiseScores:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
        else:
            print('Row wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalRowwiseScores:
                print('%s \t %.5f \t %.5f' %(x,
                                             self.actions[x]['principalColwiseScore'],
                                             self.actions[x]['principalRowwiseScore']))
                

#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from digraphs import *
    from outrankingDigraphs import *
    import weakOrders
    from time import time

    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                 numberOfActions=25)
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    #g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=11)
    #g = RandomValuationDigraph(order=11)
    print('=== >>> best and last fusion (default)')
    t0 = time()
    rcg0 = weakOrders.RankingByChoosingDigraph(g,\
                                                     fusionOperator="o-min",\
                                                     Debug=False,\
                                                     Threading=False)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcg0.showWeakOrder()
##    rcg0.showRelationTable()
    t0 = time()
    rcg1 = weakOrders.RankingByChoosingDigraph(g,\
                                                     fusionOperator="o-min",\
                                                     Debug=False,\
                                                     Threading=True)
    print('execution time %s: ' % (str ( time()-t0 ) ) )
    rcg1.showWeakOrder()
##    rcg1.showRelationTable()
##    print(rcg0.computeOrdinalCorrelation(g))
##    rcg0.showOrderedRelationTable(direction="decreasing")
##    rcg0.showOrderedRelationTable(direction="increasing")
##    print(g.computeChordlessCircuits())
##    
#    rcg0 = RankingByChoosingDigraph(g,fusionOperator="o-max",Debug=False)
#    rcg0.showWeakOrder()
#    print(rcg0.computeOrdinalCorrelation(g))
#    rcg0.showOrderedRelationTable()
##    rcg.showRankingByChoosing()
##    rcg1 = RankingByChoosingDigraph(rcg,CoDual=True)
##    rcg1.showRankingByChoosing()
##    print(rcg1.computeOrdinalCorrelation(rcg))
##    print('=== >>> best') 
##    rcg1 = RankingByChoosingDigraph(g,Best=True,Last=False,Debug=False)
##    rcg1.showWeakOrder()
##    print(rcg1.computeOrdinalCorrelation(g))
##    print('=== >>> last')
##    rcg2 = RankingByChoosingDigraph(g,Best=False,Last=True,Debug=False)
##    rcg2.showWeakOrder()
##    print(rcg2.computeOrdinalCorrelation(g))
##    print('=== >>> bipolar best and last')
##    rcg3 = RankingByChoosingDigraph(g,Best=False,Last=False,Debug=False)
##    rcg3.showWeakOrder()
##    print(rcg3.computeOrdinalCorrelation(g))
##    print('=== >>> principal weak order')
#    rcf1 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
#                                        imageType=None,Debug=False)
#    rcf1.showWeakOrder()
#    print(rcf1.computeOrdinalCorrelation(g))
#    rcf2 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-max",
#                                        imageType=None,Debug=False)
#    rcf2.showWeakOrder()
#    print(rcf2.computeOrdinalCorrelation(g))
#    #rcf.showPrincipalScores()
#    rcf1.showPrincipalScores(ColwiseOrder=True)
#    rcf1.showPrincipalScores(RowwiseOrder=True)
#    rp = RankingByPrudentChoosingDigraph(g,CoDual=True,Comments=True,Limited=0.2)
#    rp.showOrderedRelationTable(direction="increasing")
#    rp.showOrderedRelationTable()
