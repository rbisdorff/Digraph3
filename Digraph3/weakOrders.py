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
                    from sys import setrecursionlimit
                    setrecursionlimit(2**20)
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
            from sys import setrecursionlimit
            setrecursionlimit(2**20)
            digraph.computeRankingByBestChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
            digraph.computeRankingByLastChoosing(CppAgrum=CppAgrum,CoDual=CoDual,Debug=Debug)
            setrecursionlimit(1000)
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

    def computeWeakOrder(self, ColwiseOrder=False):
        """
        Specialisation for PrincipalInOutDegreesOrderings.
        """        
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
        return weakOrdering
                
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

##################

def _jobTask(categID):
    """
    Task definition for multiprocessing threaded jobs in QsRbcRanking.
    
    .. note::
    
          Parameter maxContent: maximum allowed local catContent for rbc
          is set to 50. Above this cardinality,
          Tideman's ranked pairs heuristics is used.
    """
    from tempfile import TemporaryDirectory
    from os import getcwd, chdir
    from pickle import dumps, loads, load
    from copy import deepcopy
    from outrankingDigraphs import BipolarOutrankingDigraph
    #from linearOrders import RankedPairsOrder, KohlerOrder
    from weakOrders import PrincipalInOutDegreesOrdering
    maxCatContent = 40
    print("Starting working on category %d" % (categID), end=" ")
    fiName = 'partialPerfTab-'+str(categID)+'.py'
    fi = open(fiName,'rb')
    pt = loads(fi.read())
    fi.close()
    with TemporaryDirectory() as TempDirName:
        cwd = getcwd()
        chdir(TempDirName)
        digraph = BipolarOutrankingDigraph(pt,Normalized=True)
        Max = digraph.valuationdomain['max']
        Med = digraph.valuationdomain['med']
        catContent = [x for x in digraph.actions]
        nc = len(catContent)
        print(nc,maxCatContent)
        #print(catContent)
        if nc <= maxCatContent:
            currActions = list(catContent)
            try:
                catCRbc = digraph.computeRankingByChoosing(CoDual=True)
            except:
                print('==>>> Failed RBC: Principal ranking')
##              rp = RankedPairsOrder(digraph)
##              catRbc = rp.computeRankingByChoosing()
##                ko = KohlerOrder(digraph)
##                catCRbc = ko.computeRankingByChoosing()
                try:
                    pri = PrincipalInOutDegreesOrdering(digraph,Threading=False)
                    catCRbc = pri.computeWeakOrder()
                except:
                    catCRbc = {'result': \
                               [((digraph.valuationdomain['max'],catContent),\
                                (digraph.valuationdomain['max'],catContent))]}
        else:
            print('==>>> Exceeds %d: Principal ranking' % maxCatContent)
##            rp = RankedPairsOrder(digraph)
##            catCRbc = rp.computeRankingByChoosing()
##            ko = KohlerOrder(digraph)
##            catCRbc = ko.computeRankingByChoosing()
            try:
                pri = PrincipalInOutDegreesOrdering(digraph,Threading=False)
                catCRbc = pri.computeWeakOrder()
            except:
                catCRbc = {'result': [((digraph.valuationdomain['max'],catContent),\
                                       (digraph.valuationdomain['max'],catContent))]}

        catRbc = deepcopy(catCRbc['result'])
        currActions = list(catContent)
        catRelation = digraph.computeRankingByChoosingRelation(\
                            actionsSubset=currActions,\
                            rankingByChoosing=catRbc,\
                            Debug=False)
        
        #print(catRbc,catRelation)
        splitCatRelation = [catRbc,catRelation]
        chdir(cwd)
    foName = 'splitCatRelation-'+str(categID)+'.py'
    fo = open(foName,'wb')                                            
    fo.write(dumps(splitCatRelation,-1))
    fo.close()
    writestr = 'Finished category %d %d' % (categID,nc)
    return writestr
#####

from sortingDigraphs import QuantilesSortingDigraph                                              
class QsRbcWeakOrdering(WeakOrder,QuantilesSortingDigraph):
    """
    Refinig a quantiles sorting result
    with a ranking-by-choosing of the local quantile equivalence classes
    of less than 40 items.

    For larger quantile equivalence classes,
    the principal ordering along the covariance
    of the in- and outdegrees credibilities is used.

    *Main parameters*:
          * limitingQuantiles are set by default to len(actions)//2
            for outranking digraph orders below 200.
            For higher orders, centiles are used by default.
          * Threading is on (True) by default for CPUs with more than 2 cores.

    .. note::

          The weak ordering is instantiated as weak strict order,
          its dual being a weakly complete preorder!
          
    .. warning::
    
          For larger orders a consistent size of several
          Giga bytes cpu memory is required!
          
    """

    def __init__(self,
                 argPerfTab=None,
                 limitingQuantiles=None,
                 LowerClosed=True,
                 PrefThresholds=False,
                 hasNoVeto=False,
                 minValuation=-1.0,
                 maxValuation=1.0,
                 outrankingType = "bipolar",
                 Threading=True,
                 cores=None,
                 Comments=True,
                 Debug=False):
        
        from copy import deepcopy
        from sortingDigraphs import QuantilesSortingDigraph
        from multiprocessing import Pool, cpu_count
        from time import time

        # import the performance tableau
        if argPerfTab == None:
            perfTab = RandomPerformanceTableau(numberOfActions=10,
                                               numberOfCriteria=13)
        else:
            perfTab = argPerfTab

        na = len(perfTab.actions)

        if limitingQuantiles == None:
            if na < 200:
                limitingQuantiles = na // 2
            else:
                limitingQuantiles = 100
        if Comments:        
            print('Computing the %d-quantiles sorting digraph ...' % (limitingQuantiles))
        t0 = time()
        if Threading and cpu_count() > 2:    
            qs = QuantilesSortingDigraph(perfTab,
                         limitingQuantiles=limitingQuantiles,
                         LowerClosed=LowerClosed,
                         PrefThresholds=PrefThresholds,
                         hasNoVeto=hasNoVeto,
                         minValuation=minValuation,
                         maxValuation=maxValuation,
                         outrankingType = outrankingType,
                         Threading=True,
                         CompleteOutranking = False)                
        else:
            qs = QuantilesSortingDigraph(perfTab,
                         limitingQuantiles=limitingQuantiles,
                         LowerClosed=LowerClosed,
                         PrefThresholds=PrefThresholds,
                         hasNoVeto=hasNoVeto,
                         minValuation=minValuation,
                         maxValuation=maxValuation,
                         outrankingType = outrankingType,
                         CompleteOutranking = True)
        self.tqs = time() - t0
        if Comments:
            print('execution time: %.4f' % (self.tqs))
        
        Max = qs.valuationdomain['max']
        Med = qs.valuationdomain['med']
        catContent = {}
##        weakOrdering = qs.computeWeakOrder()
##        nwo = len(weakOrdering)
##        for i in range(nwo):
##            catContent[i+1] = weakOrdering[i]
##            if Debug:
##                print(i+1,weakOrdering[i])        
        weakOrdering = QsRbcWeakOrdering.computeWeakOrder(qs)
        nwo = len(weakOrdering)
        for i in range(nwo):
            catContent[i+1] = weakOrdering[i]
            if Debug:
                print(i+1,weakOrdering[i])        

        qsRelation = deepcopy(qs.relation)

        catRelation = {}
        catRbc = {}
        if Threading and cpu_count() > 2:
            from pickle import dumps, loads, load
            if cores == None:
                cores = 8
            Nproc = cpu_count()
            if Nproc > cores:
                Nproc = cores
            from tempfile import TemporaryDirectory
            from os import getcwd, chdir
            with TemporaryDirectory() as tempDirName:
                cwd = getcwd()
                chdir(tempDirName)
                filledCategKeys = []
                print('Preparing the thread data ...')
                t0 = time()
                for c in range(1,nwo+1):
                    nc = len(catContent[c])
                    print('%d/%d %d' %(c,nwo,nc))
                    if nc > 1:
                        filledCategKeys.append(int(c))
                        pt = PartialPerformanceTableau(perfTab,actionsSubset=catContent[c])                     
                        foName = 'partialPerfTab-'+str(c)+'.py'
                        fo = open(foName,'wb')
                        ptDp = dumps(pt,-1)
                        fo.write(ptDp)
                        fo.close()
                t1 = time()
                if Comments:
                    print(filledCategKeys)
                    print('%d of %d' % (len(filledCategKeys),nwo))
                    print('Execution time: %.4f sec.' % (t1-t0))
                
                print('Threading ... !')
                t0 = time()
                with Pool(processes=Nproc) as pool:
                    for res in pool.imap_unordered(_jobTask,filledCategKeys):
                        print(res)
                self.trbc = time() - t0
                print('Finished all threads in %.4f sec.' % (self.trbc) )
                for c in range(1,nwo+1):                    
                    nc = len(catContent[c])
                    if nc > 1:
                        fiName = 'splitCatRelation-'+str(c)+'.py'
                        fi = open(fiName,'rb')
                        splitCatRelation = loads(fi.read())
                        fi.close()
                        if Debug:
                            print(c,'catRbc',splitCatRelation[0])
                            print(c,'catRelation',splitCatRelation[1])
                        catRbc[c] = splitCatRelation[0]
                        catRelation[c] = splitCatRelation[1]
                    elif nc == 1:
                        if Debug:
                            print('singleton category %d : %d' % (c,nc))
                            print(catContent[c])
                        catRbc[c] = [((Max,catContent[c]),(Max,catContent[c]))]
                        for x in catContent[c]:
                            catRelation[c] = {str(x): {str(x): Med}}
                        if Debug:
                            print(c,'catRbc',catRbc[c])
                            print(c,'catRelation',catRelation[c])               
                chdir(cwd)                
        else:
            ## without threading
            if Comments:
                print('Without threading ...')
            for c in range(1,nwo+1):
                if Debug:
                    print(c, len(catContent[c]))
                if len(catContent[c]) > 0:
                    currActions = list(catContent[c])
                    for x in currActions:
                        for y in currActions:
                            qs.relation[x][y] = qs.relationOrig[x][y]
                    catCRbc = qs.computeRankingByChoosing(currActions,CoDual=True)
                    if Debug:
                        print(c,catCRbc)
                    catRbc[c] = deepcopy(catCRbc['result'])
                    currActions = list(catContent[c])
                    catRelation[c] = qs.computeRankingByChoosingRelation(\
                        actionsSubset=currActions,\
                        rankingByChoosing=catCRbc['result'],\
                        Debug=False)

        self.name = 'qsrbc-'+qs.name
        self.actions = deepcopy(qs.actions)
        self.order = len(self.actions)
        self.criteria = deepcopy(qs.criteria)
        self.evaluation = deepcopy(qs.evaluation)
        self.categories = deepcopy(qs.categories)
        self.limitingQuantiles = deepcopy(qs.limitingQuantiles)
        self.criteriaCategoryLimits = deepcopy(qs.criteriaCategoryLimits)
        self.profiles = deepcopy(qs.profiles)
        self.valuationdomain = deepcopy(qs.valuationdomain)
        self.catRbc = deepcopy(catRbc)
        try:
            self.relationOrig = deepcopy(qs.relationOrig)
        except:
            pass
        self.relation = deepcopy(qsRelation)
        self._constructRelation(Debug=Debug)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructRelation(self,Debug=False):
        """
        Instantiates the weak order by taking the codual of the
        preoder obtained from the actions categories intervals !
        """
        preOrdering = self.computeWeakOrder(Debug=Debug)
        relation = self.computePreorderRelation(preOrdering)
        actionsList = [x for x in self.actions]
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        for x in actionsList:
            for y in actionsList:
                #self.relation[x][y] = relation[x][y]
                self.relation[x][y] = Max - relation[y][x] + Min 

    def computeWeakOrder(self,Descending=True,Comments=False,Debug=False):
        """
        specialisation of the showWeakOrder method
        """
        if Comments:
            Debug=True
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            try:
                actionsCategories[(int(highCateg),int(lowCateg))].append(a)
            except:
                actionsCategories[(int(highCateg),int(lowCateg))] = [a]
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)
        weakOrdering = []
        for item in actionsCategIntervals:
            #print(item)
            if Debug:
                if self.criteriaCategoryLimits['LowerClosed']:
                    print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                            self.categories[str(item[0][9])]['highLimit'],\
                                            str(item[1])) )
                else:
                    print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                            self.categories[str(item[0][0])]['highLimit'],\
                                            str(item[1])) )
            weakOrdering.append(item[1])
        return weakOrdering

    def computeQsRbcRanking(self,Descending=True,
                            Comments=False,
                            Debug=False):
        """                                                                     
        Render the ranking result of QsRbcWeakOrdering constructor                              
        """
        if Debug:
            Comments=True
        rbcResult = [(i,self.catRbc[i]) for i in self.catRbc]
        rbcResult.sort()
        ranking = []
        remainingActions = set([x for x in self.actions])
        for it in rbcResult:
            ordering = it[1]
            n = len(ordering)
            if Debug:
                print(ordering,n)
            for i in range(n):
                ranking.append(ordering[i][0][1])
                remainingActions = remainingActions - set(ordering[i][0][1])
            for i in range(n-1,-1,-1):
                restOrdering = set(ordering[i][1][1]) & remainingActions
                if restOrdering != set():
                    ranking.append(list(restOrdering))
                    remainingActions = remainingActions - restOrdering
        rankcopy = list(ranking)
        for i in range(len(rankcopy)-1):
            if rankcopy[i] == rankcopy[i+1]:
                if Debug:
                    print('double',rankcopy[i])
                ranking.remove(rankcopy[i])
        if not Descending:
            ranking.reverse()
        if Comments:
            print(rankcopy)
            print(ranking)
        return ranking
            
    
    def showOrderedRelationTable(self,direction="decreasing",originalRelation=False):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """
        if direction == "decreasing":
            Descending = True
        else:
            Descending = False
        weakOrdering = self.computeQsRbcRanking(Descending=Descending)
        actionsList = []
        for ch in weakOrdering:
            ch.sort()
            for x in ch:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error: missing or double actions!')
        if originalRelation:
            showRelation = self.originalRelation
        else:
            showRelation = self.relation
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=showRelation,\
                                Sorted=False,\
                                ReflexiveTerms=False)

    def showActionCategories(self,action,Debug=False,Comments=True):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        sorting = self.computeSortingCharacteristics(action=action,Comments=Debug)
        keys = []
        for c in self.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                keys.append(c)
                if Debug:
                    print(action, c, sorting[action][c])
        n = len(keys)
        credibility = min(lowLimit,notHighLimit)
        if n == 0:
            return None
        elif n == 1:
            if Comments:
                print('%s in %s - %s with credibility: %.2f = min(%.2f,%.2f)' % (action,\
                                     self.categories[keys[0]]['lowLimit'],\
                                     self.categories[keys[0]]['highLimit'],\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[0],\
                    credibility
        else:
            if Comments:
                print('%s in %s - %s with credibility: %.2f = min(%.2f,%.2f)' % (action,\
                                     self.categories[keys[0]]['lowLimit'],\
                                     self.categories[keys[-1]]['highLimit'],\
                                     credibility,lowLimit,notHighLimit) )
            return action,\
                    keys[0],\
                    keys[-1],\
                    credibility            

    def showActionsSortingResult(self,actionSubset=None):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        if actionSubset == None:
            actions = [x for x in self.actions]
        else:
            actions = [x for x in actionSubset]
        actions.sort()
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showActionCategories(x)

    def showQsRbcRanking(self,Descending=True):
        """
        show the ranking-by-sorting refinement of the quantiles sorting result
        """
        print(self.computeQsRbcRanking(Descending=Descending,
                                       Comments=False))

#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from digraphs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from weakOrders import *
    from time import time

    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
                                numberOfActions=93)
    t.saveXMCDA2('test')
    #t = XMCDA2PerformanceTableau('uniSorting')
##    g = BipolarOutrankingDigraph(t,Normalized=True)
    limitingQuantiles = len(t.actions) // 2
    #limitingQuantiles = 100
    #qs = QuantilesSortingDigraph(t,g.order)
    t0 = time()
    qsrbc = QsRbcWeakOrdering(t,7,LowerClosed=False,Threading=True,Debug=True)
    t1 = time()-t0
    qsrbc.showSorting()
    qsrbc.showActionsSortingResult()
    qsrbc.computeWeakOrder(Comments=True)
##    qsrbc.computeQsRbcRanking(Debug=False)
##    qsrbc.exportGraphViz(graphType="pdf")
##    #qsrbc.showOrderedRelationTable()
##    t0=time()
##    qsrbcwt = QsRbcWeakOrdering(t,limitingQuantiles,
##                                             cores=8,
##                                             Threading=False,
##                                             Debug=False)
##    t2 = time()-t0
##    qsrbcwt.showSorting()
##    qsrbc.showQsRbcRanking(Descending=True)
##    qsrbcwt.showQsRbcRanking(Descending=True)
##    print('qsrbc',t1,'qsrbcwt',t2)
##    corr = g.computeOrdinalCorrelation(qsrbc)
##    print('qsrbc',corr['correlation'],\
##          corr['correlation']*corr['determination'])
##    corr = g.computeOrdinalCorrelation(qsrbcwt)
##    print('qsrbcwt', corr['correlation'],\
##          corr['correlation']*corr['determination'])
    
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. october 2014                 *')
    print('* $Revision:  $                  *')
    print('*************************************')
