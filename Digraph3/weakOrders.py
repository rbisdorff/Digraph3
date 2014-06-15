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

    def showRankingByChoosing(self,actionsList=None,rankingByChoosing=None):
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
            print('Decreasing Weak Ordering')
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
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=showRelation,\
                                Sorted=False,\
                                ReflexiveTerms=False)

    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),noSilent=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName, bestChoice=bestChoice,worstChoice=worstChoice,noSilent=noSilent,graphType=graphType,graphSize=graphSize)

    def exportGraphViz(self,fileName=None,direction='best',\
                       noSilent=True,graphType='png',\
                       graphSize='7,7',\
                       fontSize=10):
        """
        export GraphViz dot file for weak order (Hasse diagram) drawing filtering.
        """
        import os
        from copy import deepcopy

        def _safeName(t0):
            t = t0.split(sep="-")
            t1 = t[0]
            n = len(t)
            if n > 1:
                for i in range(1,n):
                    t1 += '%s%s' % ('_',t[i])
            return t1
                
        if direction == 'best':
            try:
                rankingByChoosing = self.rankingByBestChoosing['result']
            except:
                self.computeRankingByBestChoosing()
                rankingByChoosing = self.rankingByBestChoosing['result']
        else:
            try:
                rankingByChoosing = self.rankingByLastChoosing['result']
            except:
                self.computeRankingByLastChoosing()
                rankingByChoosing = self.rankingByLastChoosing['result']
        
        if noSilent:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        actionKeys = [x for x in self.actions]
        n = len(actionKeys)
        relation = self.relation
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if noSilent:
            print('Exporting to '+dotName)
##        if bestChoice != set():
##            rankBestString = '{rank=max; '
##        if worstChoice != set():
##            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nweakOrders module (graphviz)\\n R. Bisdorff, 2014", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            try:
                nodeName = self.actions[x]['shortName']
            except:
                nodeName = str(x)
            node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                   % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        # same ranks for Hasses equivalence classes
        k = len(rankingByChoosing)
        for i in range(k):
            sameRank = '{ rank = same; '
            ich = rankingByChoosing[i][1]
            for x in ich:
                sameRank += str(_safeName(x))+'; '
            sameRank += '}\n'
            print(i,sameRank)
            fo.write(sameRank)
        # save original relation
        originalRelation = deepcopy(self.relation)
        
        self.closeTransitive(Reverse=True)
        for i in range(k-1):
            ich = rankingByChoosing[i][1]
            for x in ich:
                for j in range(i+1,k):
                    jch = rankingByChoosing[j][1]
                    for y in jch:
                        #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                        if self.relation[x][y] > self.valuationdomain['med']:
                            arcColor = 'black'
                            edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(x),_safeName(y),1,arcColor)
                            fo.write(edge)
                        elif self.relation[y][x] > self.valuationdomain['med']:
                            arcColor = 'black'
                            edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(y),_safeName(x),1,arcColor)
                            fo.write(edge)
                                                  
        fo.write('}\n \n')
        fo.close()
        # restore original relation
        self.relation = deepcopy(originalRelation)
        
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')

##    def showWeakOrder(self,rankingByChoosing=None):
##        """
##        specialisation for RankingByChoosing Digraphs.
##        """
##        if rankingByChoosing == None:
##            try:
##                rankingByChoosing = self.rankingByChoosing
##            except:
##                rankingByChoosing = self.computeRankingByChoosing(CoDual=self.CoDual,CppAgrum=self.CppAgrum)
##
##        Digraph.showRankingByChoosing(self,rankingByChoosing)

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
      S   |   'a01'  'a02'  'a03'  'a04'  'a05'  'a06'  'a07'   
     -----|------------------------------------------------------------
    'a01' |   +0.00  -1.00  -1.00  -0.33  +0.00  +0.00  +0.00  
    'a02' |   +1.00  +0.00  -0.17  +0.33  +1.00  +0.33  +0.67  
    'a03' |   +1.00  +0.67  +0.00  +0.33  +0.67  +0.67  +0.67  
    'a04' |   +0.33  +0.17  -0.33  +0.00  +1.00  +0.67  +0.67  
    'a05' |   +0.00  -0.67  -0.67  -1.00  +0.00  -0.17  +0.33  
    'a06' |   +0.33  +0.00  -0.33  -0.67  +0.50  +0.00  +1.00  
    'a07' |   +0.33  +0.00  -0.33  -0.67  +0.50  +0.17  +0.00  
    >>> from weakOrders import RankingByChoosingDigraph
    >>> rbc = RankingByChoosingDigraph(g)
    >>> rbc.showWeakOrder()
    Ranking by Choosing and Rejecting
      1st ranked ['a03'] (0.47)
       2nd ranked ['a02', 'a04'] (0.58)
        3rd ranked ['a06'] (1.00)
        3rd last ranked ['a06'] (1.00)
       2nd last ranked ['a07'] (0.50)
      1st last ranked ['a01', 'a05'] (0.58)
    >>> rbc.exportGraphViz('weakOrdering')
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to converse-dual_rel_randomCBperftab.dot
    dot -Grankdir=BT -Tpng converse-dual_rel_randomCBperftab.dot 
       -o weakOrdering.png 
        
    .. image:: weakOrdering.png
        
    >>> rbc.showOrderedRelationTable(direction="decreasing")
    * ---- Relation Table -----
      S   |  'a03'  'a04'  'a02'  'a06'  'a07'  'a01'  'a05'	  
     -----|------------------------------------------------------------
    'a03' |   -      0.33   0.17   0.33   0.33   1.00   0.67	 
    'a04' |  -0.33    -     0.00   0.67   0.67   0.33   1.00	 
    'a02' |  -0.17   0.00    -     0.33   0.67   1.00   0.67	 
    'a06' |  -0.33  -0.67  -0.33    -     0.17   0.33   0.17	 
    'a07' |  -0.33  -0.67  -0.67  -0.17	   -     0.33   0.33	 
    'a01' |  -1.00  -0.33  -1.00  -0.33  -0.33    -     0.00	 
    'a05' |  -0.67  -1.00  -0.67  -0.17  -0.33   0.00    - 	 
    """
    def __init__(self,other,
                 fusionOperator = "o-max",
                 CoDual=False,
                 Debug=False,
                 CppAgrum=False,
                 Threading=True):
        
        from copy import deepcopy
        from pickle import dumps, loads, load

        self.CoDual=CoDual
        self.Debug=Debug
        self.CppAgrum = CppAgrum
        self.Threading = Threading
        
        if Threading:
            from multiprocessing import Process, Lock, active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID, name, direction, tempDirName, Codual, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.direction = direction
                    self.workingDirectory = tempDirName
                    self.Codual = Codual
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
                    if Debug:
                        print("Starting working in %s on %s" % (self.workingDirectory, self.name))
                    #threadLock.acquire()
                    fi = open('dumpDigraph.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    if self.direction == 'best':
                        fo = open('rbbc.py','wb')
                        rbbc = digraph.computeRankingByBestChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
                        fo.write(dumps(rbbc,-1))
                    elif self.direction == 'worst':
                        fo = open('rbwc.py','wb')
                        rbwc = digraph.computeRankingByLastChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
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
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                digraphFileName = tempDirName +'/dumpDigraph.py'
                if Debug:
                    print('temDirName, digraphFileName', tempDirName,digraphFileName)
                fo = open(digraphFileName,'wb')
                pd = dumps(digraph,-1)
                fo.write(pd)
                fo.close()
                threadBest = myThread(1,"ComputeBest","best",tempDirName,CoDual,Debug)
                threadWorst = myThread(2,"ComputeWorst","worst",tempDirName,CoDual,Debug)
                threadBest.start()
                threadWorst.start()
                while active_children() != []:
                    pass
                print('Exiting computing threads')
                rbbcFileName = tempDirName +'/rbbc.py'          
                fi = open(rbbcFileName,'rb')
                digraph.rankingByBestChoosing = loads(fi.read())
                fi.close()
                rbwcFileName = tempDirName + '/rbwc.py'
                fi = open(rbwcFileName,'rb')
                digraph.rankingByLastChoosing = loads(fi.read())
                fi.close()
            
            
        else:
            digraph.computeRankingByBestChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
            digraph.computeRankingByLastChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
            
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
        if Debug:
            self.computeRankingByChoosing()
            self.showRankingByChoosing()
        
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        Dummy for showWeakOrder method
        """
        if rankingByChoosing == None:
            self.showWeakOrder(rankingByChoosing=self.computeRankingByChoosing())
        else:
            self.showWeakOrder(rankingByChoosing=rankingByChoosing)

    def computeRankingByBestChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            WeakOrder.computeRankingByBestChoosing(self,CoDual=self.CoDual,CppAgrum=self.CppAgrum)

    def computeRankingByLastChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            WeakOrder.computeRankingByLastChoosing(self,CoDual=self.CoDual,CppAgrum=self.CppAgrum)
 
class RankingByBestChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization of abstract WeakOrder class for computing a ranking by best-choosing.
    """
    def __init__(self,digraph,Normalized=True,CoDual=False,Debug=False):
        from copy import deepcopy
        digraphName = 'ranking-by-best'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.order = len(self.actions)
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
        """
        Specialisation of showWeakOrder() for ranking-by-best-choosing results.
        """
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
        self.order = len(self.actions)
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
        """
        Specialisation of showWeakOrder() for ranking-by-last-choosing results.
        """
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
    def __init__(self,other,fusionOperator="o-max",\
                 imageType=None,\
                 plotFileName=None,\
                 Threading=True,\
                 Debug=False):
        from copy import deepcopy
        from linearOrders import PrincipalOrder
        from pickle import dumps, loads, load

        if Threading:
            from multiprocessing import Process, Lock, active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID, name, direction,\
                             tempDirName, imageType, plotFileName, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.direction = direction
                    self.workingDirectory = tempDirName
                    self.imageType = imageType
                    self.plotFileName = plotFileName
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
                    if Debug:
                        print("Starting working in %s on %s" % (self.workingDirectory,self.name) )
                    fi = open('dumpDigraph.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    if self.direction == 'col':
                        fo = open('priCol.py','wb')
                        pc = PrincipalOrder(digraph,\
                                            Colwise=True,\
                                            imageType=imageType,\
                                            plotFileName=plotFileName,\
                                            Debug=Debug)
                        fo.write(dumps(pc,-1))
                    elif self.direction == 'row':
                        fo = open('priRow.py','wb')
                        pl = PrincipalOrder(digraph,\
                                            Colwise=False,\
                                            imageType=imageType,\
                                            plotFileName=plotFileName,\
                                            Debug=Debug)
                        fo.write(dumps(pl,-1))
                    fo.close()

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

        if Threading and cpu_count()>2:
            print('Threading ...')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                digraphFileName = tempDirName +'/dumpDigraph.py'
                if Debug:
                    print('temDirName, digraphFileName', tempDirName,digraphFileName)
                fo = open(digraphFileName,'wb')
                pd = dumps(digraph,-1)
                fo.write(pd)
                fo.close()
                threadCol = myThread(1,"ComputeCol","col",\
                                     tempDirName,\
                                     imageType=imageType,\
                                     plotFileName=plotFileName,\
                                     Debug=Debug)
                threadRow = myThread(1,"ComputeRow","row",\
                                     tempDirName,\
                                     imageType=imageType,\
                                     plotFileName=plotFileName,\
                                     Debug=Debug)
                threadCol.start()
                threadRow.start()
                while active_children() != []:
                    pass
                print('Exiting both computing threads')
                priColFileName = tempDirName+'/priCol.py'
                fi = open(priColFileName,'rb')
                pc = loads(fi.read())
                fi.close()
                priRowFileName = tempDirName+'/priRow.py'
                fi = open(priRowFileName,'rb')
                pl = loads(fi.read())
                fi.close()
            
        else:
            pc = PrincipalOrder(digraph,Colwise=True,\
                                imageType=imageType,\
                                plotFileName=plotFileName,\
                                Debug=Debug)
            pl = PrincipalOrder(digraph,Colwise=False,\
                                imageType=imageType,\
                                plotFileName=plotFileName,\
                                Debug=Debug)
        if Debug:
            print('Row wise: ')
            print(pl.principalRowwiseScores)
            pl.computeOrder()
            print(self.actions)
            for x in pl.principalRowwiseScores:
                print(x)
        self.principalRowwiseScores = deepcopy(pl.principalRowwiseScores)
        for x in pl.principalRowwiseScores:
            self.actions[x[1]]['principalRowwiseScore'] = x[0]
        if Debug:
            print('Column wise: ')
            print(pc.principalColwiseScores)
            pc.computeOrder()
        self.principalColwiseScores = deepcopy(pc.principalColwiseScores)
        for x in pc.principalColwiseScores:
            self.actions[x[1]]['principalColwiseScore'] = x[0]
        pf = FusionDigraph(pl,pc,operator=fusionOperator)
        self.relation = deepcopy(pf.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        #self.computeRankingByChoosing()
        #self.rankingByBestChoosing = pl.computeRankingByBestChoosing()
        #self.rankingByLastChoosing = pc.computeRankingByLastChoosing()
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
                
    def showWeakOrder(self, ColwiseOrder=False):
        """
        Specialisation for PrincipalInOutDegreesOrderings.
        """
##        if rankingByChoosing == None:
##            try:
##                weakOrdering = self.rankingByChoosing
##            except:
##                weakOrdering = self.computeRankingByChoosing(CoDual=False,CppAgrum=False)
        
        if ColwiseOrder:
            lps = self.principalColwiseScores
        else:
            lps = self.principalRowwiseScores
        n = len(lps)
        n2 = n//2
        ordering = []
        
        for i in range(n2):
            x = lps[i]
            y = lps[n-i-1]
            ordering.append( ( (x[0],[x[1]]),(y[0],[y[1]]) ) )
        if 2*n2 < n:
            x = lps[n2]
            ordering.append( ( (x[0],[x[1]]),(x[0],[x[1]]) ) )

        weakOrdering = {'result':ordering}
        #print(weakOrdering)

        WeakOrder.showWeakOrder(self,weakOrdering)
            

    def exportGraphViz(self,fileName=None,direction='ColwiseOrder',\
                       Comments=True,graphType='png',\
                       graphSize='7,7',\
                       fontSize=10):
        """
        Specialisation for PincipalInOutDegrees class.

        direction = "Colwise" (best to worst, default) | "Rowwise" (worst to best)
        """
        if direction == "Colwise":
            direction = 'best'
        else:
            direction = 'worst'
        WeakOrder.exportGraphViz(self, fileName=fileName,\
                            direction=direction,\
                            noSilent=Comments,\
                            graphType=graphType,\
                            graphSize=graphSize,\
                            fontSize=fontSize)

from sortingDigraphs import SortingDigraph                        
class QsRbcWeakOrdering(WeakOrder,SortingDigraph):
    """
    Refinig a quantiles sorting result
    with a local ranking-by-choosing of the category contents.

    *Parameter*:
          * limitingQuantiles are set by default to len(actions)//2
    """
    def __init__(self,
                 argPerfTab=None,
                 limitingQuantiles=None,
                 LowerClosed=True,
                 PrefThresholds=True,
                 hasNoVeto=False,
                 minValuation=-1.0,
                 maxValuation=1.0,
                 outrankingType = "bipolar",
                 Threading=False,
                 Debug=False):
        
        from copy import deepcopy
        from sortingDigraphs import QuantilesSortingDigraph
        # import the performance tableau
        if argPerfTab == None:
            perfTab = RandomPerformanceTableau(numberOfActions=10,
                                               numberOfCriteria=13)
        else:
            perfTab = argPerfTab

        if limitingQuantiles == None:
            limitingQuantiles = len(perfTab.actions) // 2
            
        qs = QuantilesSortingDigraph(argPerfTab,
                     limitingQuantiles=limitingQuantiles,
                     LowerClosed=LowerClosed,
                     PrefThresholds=PrefThresholds,
                     hasNoVeto=hasNoVeto,
                     minValuation=minValuation,
                     maxValuation=maxValuation,
                     outrankingType = outrankingType,
                     Threading=False,
                     Debug=False)
        catContent = qs.computeCategoryContents()
        if Debug:
            qs.showSorting()

        qsRelation = deepcopy(qs.relation) 
        catRelation = {}
        catRbc = {}
        for c in qs.orderedCategoryKeys(Reverse=True):
            if Debug:
                print(c, len(catContent[c]))
            if len(catContent[c]) > 0:
                currActions = list(catContent[c])
                for x in currActions:
                    for y in currActions:
                        qs.relation[x][y] = qs.relationOrig[x][y]
                catCRbc = qs.computeRankingByChoosing(currActions)
                if Debug:
                    print(c,catCRbc)
                catRbc[c] = deepcopy(catCRbc['result'])
                currActions = list(catContent[c])
                catRelation[c] = qs.computeRankingByChoosingRelation(\
                    actionsSubset=currActions,\
                    rankingByChoosing=catCRbc['result'],\
                    Debug=False)
        qs.catRbc = deepcopy(catRbc)
        qs.relation = deepcopy(qsRelation)
    
##        for c in qs.orderedCategoryKeys():
##            for x in catContent[c]:
##                for y in catContent[c]:
##                    qs.relation[x][y] = catRelation[c][x][y]

        self.name = 'qsrbc-'+qs.name
        self.actions = deepcopy(qs.actions)
        self.order = len(self.actions)
        self.criteria = deepcopy(qs.criteria)
        self.evaluation = deepcopy(qs.evaluation)
        self.categories = deepcopy(qs.categories)
        self.criteriaCategoryLimits = deepcopy(qs.criteriaCategoryLimits)
        self.profiles = deepcopy(qs.profiles)
        self.valuationdomain = deepcopy(qs.valuationdomain)
        self.catRbc = deepcopy(qs.catRbc)
        self.relationOrig = deepcopy(qs.relationOrig)
        self.relation = deepcopy(qs.relation)
        self._constructRelation()
        self.catRbc = deepcopy(qs.catRbc)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()        

    def _constructRelation(self):
        """
        Instantiates the weak order by taking the codual of the preoder !
        """
        weakOrdering = self.computeWeakOrder()
        relation = self.computePreorderRelation(weakOrdering)
        actionsList = [x for x in self.actions]
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        for x in actionsList:
            for y in actionsList:
                self.relation[x][y] = Max - relation[y][x] + Min 

    def computeWeakOrder(self,DescendingOrder=True,Comments=False,Debug=False):
        """
        specialisation of the showWeakOrder method
        """
        if Debug:
            Comments=True
        preWeakOrdering = []
        for c in self.orderedCategoryKeys(Reverse=DescendingOrder):
            if c in self.catRbc:
                ordering = [ch for ch in self.catRbc[c]]
                if Debug:
                    print(c,qsrbc.categories[c]['name'], ordering)
                    print('best ranked')
                for i in range(len(ordering)):
                    if Debug:
                        print(ordering[i][0][1])
                    preWeakOrdering.append(ordering[i][0][1])
                if Debug:
                    print('worst ranked')
                for i in range(len(ordering)-1,-1,-1):
                    if Debug:
                        print(ordering[i][1][1])
                    preWeakOrdering.append(ordering[i][1][1])
        remainingActions = set([x for x in self.actions])
        weakOrdering = []
        for ch in preWeakOrdering:
            if Debug:
                print(weakOrdering,ch,remainingActions)
            eqcl = []
            for x in ch:
                if x in remainingActions:
                    eqcl.append(x)
            if eqcl != []:
                weakOrdering.append(eqcl)
                remainingActions = remainingActions - set(eqcl)
        if Comments:
            print(weakOrdering)
        return weakOrdering

    
    def showOrderedRelationTable(self,direction="decreasing",originalRelation=False):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """
        if direction == "decreasing":
            DescendingOrder = True
        else:
            DescendingOrder = False
        weakOrdering = self.computeWeakOrder(DescendingOrder=DescendingOrder)
        actionsList = []
        for ch in weakOrdering:
            ch.sort()
            for x in ch:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error: missing actions!')
        if originalRelation:
            showRelation = self.originalRelation
        else:
            showRelation = self.relation
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=showRelation,\
                                Sorted=False,\
                                ReflexiveTerms=False)
                       
class QsRbcWeakOrderingWithThreading(QsRbcWeakOrdering):
    """
    Refinig a quantiles sorting result
    with a multiprocessing of local ranking-by-choosing of the category contents.

    *Parameter*:
          * limitingQuantiles are set by default to len(actions)//2
    """
    def __init__(self,
                 argPerfTab=None,
                 limitingQuantiles=None,
                 LowerClosed=True,
                 PrefThresholds=True,
                 hasNoVeto=False,
                 minValuation=-1.0,
                 maxValuation=1.0,
                 outrankingType = "bipolar",
                 Threading=True,
                 Debug=False):
        
        from copy import deepcopy
        from sortingDigraphs import QuantilesSortingDigraph
        # import the performance tableau
        if argPerfTab == None:
            perfTab = RandomPerformanceTableau(numberOfActions=10,
                                               numberOfCriteria=13)
        else:
            perfTab = argPerfTab

        if limitingQuantiles == None:
            limitingQuantiles = len(perfTab.actions) // 2
            
        qs = QuantilesSortingDigraph(argPerfTab,
                     limitingQuantiles=limitingQuantiles,
                     LowerClosed=LowerClosed,
                     PrefThresholds=PrefThresholds,
                     hasNoVeto=hasNoVeto,
                     minValuation=minValuation,
                     maxValuation=maxValuation,
                     outrankingType = outrankingType,
                     Threading=False,
                     Debug=False)
        catContent = qs.computeCategoryContents()
        if Debug:
            qs.showSorting()
        qsRelation = deepcopy(qs.relation)
        from multiprocessing import cpu_count
        if Threading and cpu_count() > 4:
            from pickle import dumps, loads, load
            from multiprocessing import Process, Lock, active_children
            class myThread(Process):
                def __init__(self, categID,\
                             tempDirName,\
                             Debug):
                    Process.__init__(self)
                    self.categID = categID
                    self.workingDirectory = tempDirName
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
                    if Debug:
                        print("Starting working in %s on %s" % (self.workingDirectory, self.name))
                    fi = open('dumpQs.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    fiName = 'catContent-'+str(self.categID)+'.py'
                    fi = open(fiName,'rb')
                    catContent = loads(fi.read())
                    fi.close()
                    if Debug:
                        print(self.categID,catContent)
                    if len(catContent) > 0:
                        currActions = list(catContent)
                        for x in currActions:
                            for y in currActions:
                                digraph.relation[x][y] = digraph.relationOrig[x][y]
                        catCRbc = digraph.computeRankingByChoosing(currActions)
                        if Debug:
                            print(self.categID,catCRbc)
                        catRbc = deepcopy(catCRbc['result'])
                        currActions = list(catContent)
                        catRelation = digraph.computeRankingByChoosingRelation(\
                                        actionsSubset=currActions,\
                                        rankingByChoosing=catCRbc['result'],\
                                        Debug=False)
                        splitCatRelation = [catRbc,catRelation]
                    else:
                        splitCatRelation = [[],[]]
                    foName = 'splitCatRelation-'+str(self.categID)+'.py'
                    fo = open(foName,'wb')                                            
                    fo.write(dumps(splitCatRelation,-1))
                    fo.close()
            print('Threading ... !')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                qsFileName = tempDirName +'/dumpQs.py'
                if Debug:
                    print('temDirName, qsFileName', tempDirName,qsFileName)
                fo = open(qsFileName,'wb')
                qsDp = dumps(qs,-1)
                fo.write(qsDp)
                fo.close()
                nbrCores = cpu_count()-2
                print('Nbr of cpus = ',nbrCores)
                for c in qs.orderedCategoryKeys(Reverse=True):
                    print('Threading categ', c, len(catContent[c]))
                    if Debug:
                        print(catContent[c])
                    foName = tempDirName+'/catContent-'+str(c)+'.py'
                    fo = open(foName,'wb')
                    spa = dumps(catContent[c],-1)
                    fo.write(spa)
                    fo.close()
                    splitThread = myThread(c,tempDirName,
                                           Debug)
                    splitThread.start()
                while active_children() != []:
                    pass
                print('Exiting computing threads')
                catRelation = {}
                catRbc = {}
                for j in qs.orderedCategoryKeys(Reverse=True):
                    fiName = tempDirName+'/splitCatRelation-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitCatRelation = loads(fi.read())
                    fi.close()
                    if Debug:
                        print(j, 'catRbc',splitCatRelation[0])
                        print(j,'catRelation', splitCatRelation[1])
                    catRbc[j] = splitCatRelation[0]
                    catRelation[j] = splitCatRelation[1] 
        else:
            catRelation = {}
            catRbc = {}
            for c in qs.orderedCategoryKeys(Reverse=True):
                if Debug:
                    print(c, len(catContent[c]))
                if len(catContent[c]) > 0:
                    currActions = list(catContent[c])
                    for x in currActions:
                        for y in currActions:
                            qs.relation[x][y] = qs.relationOrig[x][y]
                    catCRbc = qs.computeRankingByChoosing(currActions)
                    if Debug:
                        print(c,catCRbc)
                    catRbc[c] = deepcopy(catCRbc['result'])
                    currActions = list(catContent[c])
                    catRelation[c] = qs.computeRankingByChoosingRelation(\
                        actionsSubset=currActions,\
                        rankingByChoosing=catCRbc['result'],\
                        Debug=False)

        qs.catRbc = deepcopy(catRbc)
        qs.relation = deepcopy(qsRelation)
    
##        for c in qs.orderedCategoryKeys():
##            for x in catContent[c]:
##                for y in catContent[c]:
##                    qs.relation[x][y] = catRelation[c][x][y]

        self.name = 'qsrbc-'+qs.name
        self.actions = deepcopy(qs.actions)
        self.order = len(self.actions)
        self.criteria = deepcopy(qs.criteria)
        self.evaluation = deepcopy(qs.evaluation)
        self.categories = deepcopy(qs.categories)
        self.criteriaCategoryLimits = deepcopy(qs.criteriaCategoryLimits)
        self.profiles = deepcopy(qs.profiles)
        self.valuationdomain = deepcopy(qs.valuationdomain)
        self.catRbc = deepcopy(qs.catRbc)
        self.relationOrig = deepcopy(qs.relationOrig)
        self.relation = deepcopy(qs.relation)
        self._constructRelation()
        self.catRbc = deepcopy(qs.catRbc)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()        


#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from digraphs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from weakOrders import *
    from time import time

    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                 numberOfActions=150)
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('test')
    g = BipolarOutrankingDigraph(t,Normalized=True)
    limitingQuantiles = len(t.actions) // 3
    #limitingQuantiles = 20
    #qs = QuantilesSortingDigraph(t,g.order)
##    t0 = time()
##    qsrbc = QsRbcWeakOrdering(t,limitingQuantiles,Debug=False)
##    print(time()-t0)
##    qsrbc.showSorting()
##    weakOrdering = qsrbc.computeWeakOrder(Comments=False,Debug=False)
##    print(weakOrdering)
    t0=time()
    qsrbcwt = QsRbcWeakOrderingWithThreading(t,limitingQuantiles,Debug=False)
    print(time()-t0)
    #qsrbcwt.showSorting()
    weakOrdering = qsrbcwt.computeWeakOrder(Comments=False,Debug=False)
    print(weakOrdering)
    
##    weakOrdering = qsrbc.computeWeakOrder(Comments=False,Debug=False)
##    print(weakOrdering)
##    #qsrbc.showOrderedRelationTable()
##    qsrbc.exportGraphViz()
##    rbc = RankingByChoosingDigraph(g,Threading=False)
##    rbc.exportGraphViz()
##    qscorr = g.computeOrdinalCorrelation(qs)
##    print('qs',qscorr['correlation'],\
##          qscorr['correlation']*qscorr['determination'])
##    qsrbccorr = g.computeOrdinalCorrelation(qsrbc)
##    print('qsrbc', qsrbccorr['correlation'],\
##          qsrbccorr['correlation']*qsrbccorr['determination'])
##    rbccorr = g.computeOrdinalCorrelation(rbc)
##    print('rbc',rbccorr['correlation'],\
##          rbccorr['correlation']*rbccorr['determination'])
##    crosscorr = qsrbc.computeOrdinalCorrelation(rbc)
##    print('qsrbc<->rbc',crosscorr['correlation'],\
##          crosscorr['correlation']*crosscorr['determination'])
##    crosscorr = qsrbc.computeOrdinalCorrelation(qs)
##    print('qsrbc<->qs',crosscorr['correlation'],\
##          crosscorr['correlation']*crosscorr['determination'])
##    
    #g = RandomBipolarOutrankingDigraph(Normalized=True,numberOfActions=11)
    #g = RandomValuationDigraph(order=11)
##    print('=== >>> best and last fusion (default)')
##    t0 = time()
##    rcg0 = weakOrders.RankingByChoosingDigraph(g,\
##                                                     fusionOperator="o-min",\
##                                                     Debug=False,\
##                                                     Threading=False)
##    print('execution time %s: ' % (str ( time()-t0 ) ) )
##    rcg0.showRankingByBestChoosing()
##    rcg0.exportGraphViz()
####    rcg0.showRelationTable()
##    t0 = time()
##    rcg1 = weakOrders.RankingByChoosingDigraph(g,\
##                                               fusionOperator="o-min",\
##                                                     Debug=False,\
##                                                     Threading=True)
##    print('execution time %s: ' % (str ( time()-t0 ) ) )
##    rcg1.showWeakOrder()
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
##    t0 = time()
##    rcf1 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
##                                          imageType=None,Debug=False,
##                                          Threading=False)
##    rcf1.showWeakOrder(ColwiseOrder=True)
##    print('execution time %s: ' % (str ( time()-t0 ) ) )
##    t0 = time()
##    rcf2 = PrincipalInOutDegreesOrdering(g,fusionOperator="o-min",
##                                           imageType=None,Debug=False,\
##                                           Threading=True)
##    rcf2.showWeakOrder()
##    print('execution time %s: ' % (str ( time()-t0 ) ) )
##    rcf2.exportGraphViz(fileName='testcw',direction="Colwise")
##    rcf2.exportGraphViz(fileName='testrw',direction="Colwise",graphType='pdf')
##    rcf2.showWeakOrder()
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
