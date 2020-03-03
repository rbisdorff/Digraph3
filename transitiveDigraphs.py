#!/usr/bin/env python3
"""
Digraph3 module for working with transitive digraphs. 
Copyright (C) 2006-2020  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "Branch: 3.3 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

from digraphsTools import *
from digraphs import *
from outrankingDigraphs import *
from transitiveDigraphs import *


class TransitiveDigraph(Digraph):
    """
    Abstract class for specialized methods addressing transitive digraphs.
    """
    def showWeakOrder(self,rankingByChoosing=None):
        """
        A dummy for the showTransitiveDigraph() method.
        """
        self.showTransitiveDigraph()
        
    def showTransitiveDigraph(self,rankingByChoosing=None):
        """
        A show method for self.rankinByChoosing result.
        """
        if rankingByChoosing == None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                #print('Error: You must first run self.computeRankingByChoosing(CoDual=False(default)|True) !')
                self.computeRankingByChoosing()
                rankingByChoosing = self.rankingByChoosing['result']
                #return
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
        Dummy name for showTransitiveDigraph() method
        """
        self.showTransitiveDigraph(rankingByChoosing=rankingByChoosing)
    
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

    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),Comments=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName, bestChoice=bestChoice,worstChoice=worstChoice,Comments=Comments,graphType=graphType,graphSize=graphSize)

    def exportGraphViz(self,digraphClass=None,fileName=None,relation=None,direction='best',\
                       Comments=True,graphType='png',\
                       graphSize='7,7',\
                       fontSize=10):
        """
        export GraphViz dot file for Hasse diagram drawing filtering.
        """
        import os
        from copy import copy as deepcopy
        from sortingDigraphs import NormedQuantilesRatingDigraph
            
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
        
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        actionKeys = [x for x in self.actions]
        n = len(actionKeys)
        if relation == None:
            relation = deepcopy(self.relation)
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
##        if bestChoice != set():
##            rankBestString = '{rank=max; '
##        if worstChoice != set():
##            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nTransitiveDigraphs module (graphviz)\\n R. Bisdorff, 2014", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            if digraphClass == NormedQuantilesRatingDigraph:
                #print(digraphClass)
                if x in self.profiles:
                    cat = self.profiles[x]['category']
                    if self.LowerClosed:
                        nodeName = self.categories[cat]['lowLimit'] + ' -'
                    else:
                        nodeName = '- ' +self.categories[cat]['highLimit']
                    node = '%s [shape = "box", fillcolor=lightcoral, style=filled, label = "%s", fontsize=%d];\n'\
                           % (str(x),nodeName,fontSize)           
                else:
                    try:
                        nodeName = self.actions[x]['shortName']
                    except:
                        nodeName = str(x)
                    node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                           % (str(_safeName(x)),_safeName(nodeName),fontSize)
                   
            else: # standard TransitiveDigraphs  
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
        originalRelation = deepcopy(relation)
        
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
        relation = deepcopy(originalRelation)
        
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

class RankingsFusion(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    digraphs resulting from the epistemic
    disjunctive or conjunctive fusion (omax|omin operator) of a list of rankings.

    *Parameter*:

         * fusionOperator = 'o-max' (default) | 'o-min' : Disjunctive, resp. conjuntive epistemic fusion.

    Example application:

    >>> from TransitiveDigraphs import PartialRanking
    >>> from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
    >>> t = RandomPerformanceTableau()
    >>> pr = PreRankedOutrankingDigraph(t,10,quantilesOrderingStrategy='average')
    >>> r1 = qr.boostedRanking
    >>> pro = PreRankedOutrankingDigraph(t,10,quantilesOrderingStrategy='optimistic')
    >>> r2 = pro.boostedRanking
    >>> prp = QuantilesRankingDigraph(t,10,quantilesOrderingStrategy='pessimistic')
    >>> r3 = prp.boostedRanking
    >>> wqr = PartialRanking(pr,[r1,r2,r3])
    >>> wqr.exportGraphViz('partialOrdering',graphType="pdf")
    
    """
    def __init__(self,other,rankings,fusionOperator='o-max',Debug=False):
        
        from digraphsTools import ranking2preorder, omax, omin
        from copy import deepcopy
        from decimal import Decimal
        if Debug:
            print(rankings)
        if len(rankings) < 1:
            print('Error: several rankings have to be provided!')
            return
        self.__dict__ = deepcopy(other.__dict__)
        self.name = other.name + '_wk'
        self.valuationdomain['min'] = Decimal('-1')
        self.valuationdomain['max'] = Decimal('1')
        self.valuationdomain['med'] = Decimal('0')
        Med = self.valuationdomain['med']
        relations = []
        for rel in rankings:
            if Debug:
                print(rel)
            relations.append(self.computePreorderRelation(ranking2preorder(rel)))
        if Debug:
            print(relations)

        relation = {}
        
        for x in self.actions:
            relation[x] = {}
            for y in self.actions:
                L = [relations[i][x][y] for i in range(len(relations))]
                if fusionOperator == 'o-max':
                    relation[x][y] = omax(Med,L)
                elif fusionOperator == 'o-min':
                    relation[x][y] = omin(Med,L)
                else:
                    print('Error: incorrect fusion operator %s' % fusionOperator)
                    return
                if Debug:
                    print(x,y,L,relation[x][y])
        if Debug:
            print(relation)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class KemenyOrdersFusion(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    transitive digraphs resulting from the epistemic
    disjunctive (default) or conjubctive fusion of
    all potential Kemeny linear orderings.

    *Parameter*:

         * fusionOperator = 'o-max' (default) | 'o-min' : Disjunctive, resp. conjuntive epistemic fusion.
    
    """
    def __init__(self,other,orderLimit=7,fusionOperator='o-max',
                 Debug=False):
        
        if other.order > orderLimit:
            print('Digraph order %d to high. The default limit (7) may be changed with the oderLimit argument.')
            return
                  
        from digraphsTools import ranking2preorder, omax, omin
        from copy import deepcopy
        from decimal import Decimal

        self.__dict__ = deepcopy(other.__dict__)
        self.name = other.name + '_wk'
        self.valuationdomain['min'] = Decimal('-1')
        self.valuationdomain['max'] = Decimal('1')
        self.valuationdomain['med'] = Decimal('0')
        Med = self.valuationdomain['med']
        #relation = copy(other.relation)
        if self.computeKemenyRanking(orderLimit=orderLimit,Debug=False) == None:
        # [0] = ordered actions list, [1] = maximal Kemeny index
            print('Intantiation error: unable to compute the Kemeny Order !!!')
            print('Digraph order %d is required to be lower than 8!' % n)
            return
        kemenyRankings = self.maximalRankings
        if Debug:
            print(kemenyRankings)
        relations = []
        for rel in kemenyRankings:
            #print(rel)
            relations.append(self.computePreorderRelation(ranking2preorder(rel)))
        if Debug:
            print(relations)
        relation = {}
        
        for x in self.actions:
            relation[x] = {}
            for y in self.actions:
                L = [relations[i][x][y] for i in range(len(relations))]
                if fusionOperator == 'o-max':
                    relation[x][y] = omax(Med,L)
                elif fusionOperator == 'o-min':
                    relation[x][y] = omin(Med,L)
                else:
                    print('Error: incorrect fusion operator %s' % fusionOperator)
                    return
                if Debug:
                    print(x,y,L,relation[x][y])
        if Debug:
            print(relation)
        self.relation = relation
        #print(self.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class KohlerArrowRaynaudFusion(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    ranking-by-choosing orderings resulting from the epistemic
    disjunctive (o-max) or conjunctive (o-min) fusion of a
    Kohler linear best ordering and an Arrow-Raynaud linear worst ordering. 
    """
    def __init__(self,outrankingDigraph,
                 fusionOperator='o-max',
                 Threading=True,
                 Debug=False):
        
        from digraphsTools import ranking2preorder, omax, omin
        from copy import copy as deepcopy
        from pickle import dumps, loads, load
        from linearOrders import KohlerOrder
        self.Debug=Debug
        self.Threading = Threading
        
        if Threading:
            from multiprocessing import Process, Lock, active_children, cpu_count
            class myThread(Process):
                def __init__(self, threadID, name, direction, tempDirName, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.direction = direction
                    self.workingDirectory = tempDirName
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
                        fo = open('ko.py','wb')
                        ko = KohlerOrder(digraph)
                        fo.write(dumps(ko.relation,-1))
                    elif self.direction == 'worst':
                        fo = open('ar.py','wb')
                        ar = KohlerOrder((~(-digraph)))
                        fo.write(dumps(ar.relation,-1))
                    fo.close()
                    #threadLock.release()
                    
        digraph=deepcopy(outrankingDigraph)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        self.actions = deepcopy(digraph.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
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
                threadBest = myThread(1,"ComputeBest","best",tempDirName,Debug)
                threadWorst = myThread(2,"ComputeWorst","worst",tempDirName,Debug)
                threadBest.start()
                threadWorst.start()
                while active_children() != []:
                    pass
                print('Exiting computing threads')
                koFileName = tempDirName +'/ko.py'          
                fi = open(koFileName,'rb')
                KohlerRelation = loads(fi.read())
                fi.close()
                arFileName = tempDirName + '/ar.py'
                fi = open(arFileName,'rb')
                ArrowRaynaudRelation = loads(fi.read())
                fi.close()
            
        else:
            ko = KohlerOrder(digraph)
            ar = KohlerOrder((~(-digraph)))
            KohlerRelation = deepcopy(ko.relation)
            ArrowRaynaudRelation = deepcopy(ar.relation)
            
        if Debug:
            print('Kohler = ', KohlerRelation)
            print('ArrowRaynaud = ', ArrowRaynaudRelation)
            
        relation = {}
        Med = self.valuationdomain['med']
        for x in self.actions:
            relation[x] = {}
            for y in self.actions:
                L = [KohlerRelation[x][y],ArrowRaynaudRelation[x][y]]
                if fusionOperator == "o-max":
                    relation[x][y] = omax(Med,L)
                elif fusionOperator == "o-min":
                    relation[x][y] = omin(Med,L)
                else:
                    print('Error: invalid epistemic fusion operator %s' % fusionOperator)
                    return
                if Debug:
                    print('!',x,y,KohlerRelation[x][y],
                          ArrowRaynaudRelation[x][y],relFusion[x][y])  
        self.relation=deepcopy(relation)        
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

#---------------------
class RankingByChoosingDigraph(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
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
    >>> from TransitiveDigraphs import RankingByChoosingDigraph
    >>> rbc = RankingByChoosingDigraph(g)
    >>> rbc.showTransitiveDigraph()
    Ranking by Choosing and Rejecting
      1st ranked ['a03'] (0.47)
       2nd ranked ['a02', 'a04'] (0.58)
        3rd ranked ['a06'] (1.00)
        3rd last ranked ['a06'] (1.00)
       2nd last ranked ['a07'] (0.50)
      1st last ranked ['a01', 'a05'] (0.58)
    >>> rbc.exportGraphViz('TransitiveDigraphing')
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to converse-dual_rel_randomCBperftab.dot
    dot -Grankdir=BT -Tpng converse-dual_rel_randomCBperftab.dot 
       -o TransitiveDigraphing.png 
        
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

        from digraphsTools import ranking2preorder, omax, omin        
        from copy import copy, deepcopy
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
        self.actions = copy(digraph.actions)
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
        Med = digraph.valuationdomain['med']
        for x in digraph.actions:
            relFusion[x] = {}
            fx = relFusion[x]
            bx = relBest[x]
            lx = relLast[x]
            for y in digraph.actions:
                L = [bx[y],lx[y]]
                if fusionOperator == "o-max":
                    fx[y] = omax(Med,L)
                elif fusionOperator == "o-min":
                    fx[y] = omin(Med,L)
                else:
                    print('Error: invalid epistemic fusion operator %s' % operator)
                    return
##                if Debug:
##                    print('!',x,y,relBest[x][y],relLast[x][y],relFusion[x][y])  
        self.relation=relFusion
        self.rankingByLastChoosing = copy(digraph.rankingByLastChoosing)
        self.rankingByBestChoosing = copy(digraph.rankingByBestChoosing)
        if Debug:
            self.computeRankingByChoosing()
            self.showRankingByChoosing()
        
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showTransitiveDigraph(self,rankingByChoosing=None):
        """
        Specialization of generic method.
        Without argument, a weak ordering is recomputed from the
        valued self relation.
        """
        if rankingByChoosing == None:
            TransitiveDigraph.showTransitiveDigraph(self,rankingByChoosing=self.computeRankingByChoosing())
        else:
            TransitiveDigraph.showTransitiveDigraph(self,rankingByChoosing=rankingByChoosing)



    def showRankingByChoosing(self,rankingByChoosing=None):
        """
        Dummy for showTransitiveDigraph method
        """
        if rankingByChoosing == None:
            TransitiveDigraph.showTransitiveDigraph(self,rankingByChoosing=self.computeRankingByChoosing())
        else:
            TransitiveDigraph.showTransitiveDigraph(self,rankingByChoosing=rankingByChoosing)

    def computeRankingByBestChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            TransitiveDigraph.computeRankingByBestChoosing(self,CoDual=self.CoDual,CppAgrum=self.CppAgrum)

    def computeRankingByLastChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            TransitiveDigraph.computeRankingByLastChoosing(self,CoDual=self.CoDual,CppAgrum=self.CppAgrum)

#--------------------
class RankingByBestChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization of abstract TransitiveDigraph class for computing a ranking by best-choosing.
    """
    def __init__(self,digraph,Normalized=True,CoDual=False,Debug=False):
        from copy import copy as deepcopy
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
        
    def showTransitiveDigraph(self):
        """
        Specialisation of showTransitiveDigraph() for ranking-by-best-choosing results.
        """
        self.showRankingByBestChoosing()


class RankingByLastChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization of abstract TransitiveDigraph class for computing a ranking by rejecting.
    """
    def __init__(self,digraph,Normalized=True,CoDual=False,Debug=False):
        from copy import copy as deepcopy
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
    
    def showTransitiveDigraph(self):
        """
        Specialisation of showTransitiveDigraph() for ranking-by-last-choosing results.
        """
        self.showRankingByLastChoosing()


class RankingByPrudentChoosingDigraph(RankingByChoosingDigraph):
    """
    Specialization for ranking-by-rejecting results with prudent single elimination of chordless circuits. By default, the cut level for circuits elimination is set to 20% of the valuation domain maximum (1.0).
    """
    def __init__(self,digraph,CoDual=False,Normalized=True,Odd=True,Limited=0.2,Comments=False,Debug=False,SplitCorrelation=True):
        from copy import copy, deepcopy
        from time import time
        if Comments:          
            t0 = time()
            print('------- Commenting ranking by prudent choosing ------')
        digraph_ = deepcopy(digraph)
        if Normalized:
            digraph_.recodeValuation(-1,1)
        digraphName = 'sorting-by-prudent-choosing'+digraph_.name
        self.name = digraphName
        self.actions = copy(digraph_.actions)
        self.order = len(self.actions)
        self.valuationdomain = copy(digraph_.valuationdomain)
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
            self.relation = copy(fus.relation)
            self.rankingByBestChoosing = s2.rankingByBestChoosing
            self.rankingByLastChoosing = s1.rankingByLastChoosing

        #self.rankingByChoosing = self.computeRankingByChoosing(CoDual=CoDual)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Comments:
            t1 = time()
            gdeter = digraph_.computeDeterminateness()
            self.showTransitiveDigraph()
            print('Circuits cutting level limit  : %.3f' % Limited)
            print('Circuits elimination cut level: %.3f' % self.cutLevel)
            print('Ordinal Correlation with given outranking')
            corr = digraph_.computeOrdinalCorrelation(self)
            print('Correlation     : %.3f' % corr['correlation'])
            print('Determinateness : %.3f (%.3f)' % (corr['determination'],gdeter))
            print('Execution time  : %.4f sec.' % (t1-t0))


class PrincipalInOutDegreesOrderingFusion(TransitiveDigraph):
    """
    Specialization of abstract TransitiveDigraph class for ranking by fusion
    of the principal orders of the variance-covariance of in- 
    (Colwise) and outdegrees (Rowwise).
    
    Example Python3 session with same outranking digraph g as shown in the RankingByChoosingDigraph example session (see below). 
    
    
    >>> from TransitiveDigraphs import PrincipalInOutDegreesOrderingFusion
    >>> pro = PrincipalInOutDegreesOrdering(g,imageType="png",\ 
                     plotFileName="proTransitiveDigraphing")
    >>> pro.showTransitiveDigraph()
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
        from copy import copy, deepcopy
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
            self.actions = digraph.actions
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
        self.principalRowwiseScores = copy(pl.principalRowwiseScores)
        for x in pl.principalRowwiseScores:
            self.actions[x[1]]['principalRowwiseScore'] = x[0]
        if Debug:
            print('Column wise: ')
            print(pc.principalColwiseScores)
            pc.computeOrder()
        self.principalColwiseScores = copy(pc.principalColwiseScores)
        for x in pc.principalColwiseScores:
            self.actions[x[1]]['principalColwiseScore'] = x[0]
        pf = FusionDigraph(pl,pc,operator=fusionOperator)
        self.relation = copy(pf.relation)
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

    def computeTransitiveDigraph(self, ColwiseOrder=False):
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

        TransitiveDigraphing = {'result':ordering}
        return TransitiveDigraphing
                
    def showTransitiveDigraph(self, ColwiseOrder=False):
        """
        Specialisation for PrincipalInOutDegreesOrderings.
        """
##        if rankingByChoosing == None:
##            try:
##                TransitiveDigraphing = self.rankingByChoosing
##            except:
##                TransitiveDigraphing = self.computeRankingByChoosing(CoDual=False,CppAgrum=False)
        
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

        TransitiveDigraphing = {'result':ordering}
        #print(TransitiveDigraphing)

        TransitiveDigraph.showTransitiveDigraph(self,TransitiveDigraphing)
            

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
        TransitiveDigraph.exportGraphViz(self, fileName=fileName,\
                            direction=direction,\
                            Comments=Comments,\
                            graphType=graphType,\
                            graphSize=graphSize,\
                            fontSize=fontSize)

##################

def _jobTaskRubis(categID):
    """
    Task definition for multiprocessing threaded local RubisChoice jobs in the QantilesRankingDigraph contructor.
    
    .. note::
          Parameter maxContent: maximum allowed local catContent for RankingByRubisChoice 
          is set to 30. Above this cardinality, the PrincipalInOutDegreesOrdering is used.
          
    """
    from tempfile import TemporaryDirectory
    from os import getcwd, chdir
    from pickle import dumps, loads, load
    from copy import copy as deepcopy
    from outrankingDigraphs import BipolarOutrankingDigraph
    #from linearOrders import RankedPairsOrder, KohlerOrder
    from TransitiveDigraphs import PrincipalInOutDegreesOrdering
    maxCatContent = 30
    Comments = False
    if Comments:
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
                if Comments:
                    print('==>>> Failed RBC: Principal ranking')
##              rp = RankedPairsOrder(digraph)
##              catRbc = rp.computeRankingByChoosing()
##                ko = KohlerOrder(digraph)
##                catCRbc = ko.computeRankingByChoosing()
                try:
                    pri = PrincipalInOutDegreesOrdering(digraph,Threading=False)
                    catCRbc = pri.computeTransitiveDigraph()
                except:
                    catCRbc = {'result': \
                               [((digraph.valuationdomain['max'],catContent),\
                                (digraph.valuationdomain['max'],catContent))]}
        else:
            if Comments:
                print('==>>> Exceeds %d: Principal ranking' % maxCatContent)
##            rp = RankedPairsOrder(digraph)
##            catCRbc = rp.computeRankingByChoosing()
##            ko = KohlerOrder(digraph)
##            catCRbc = ko.computeRankingByChoosing()
            try:
                pri = PrincipalInOutDegreesOrdering(digraph,Threading=False)
                catCRbc = pri.computeTransitiveDigraph()
            except:
                catCRbc = {'result': [((digraph.valuationdomain['max'],catContent),\
                                       (digraph.valuationdomain['max'],catContent))]}

##        catRbc = deepcopy(catCRbc['result'])
##        currActions = list(catContent)
##        catRelation = digraph.computeRankingByChoosingRelation(\
##                            actionsSubset=currActions,\
##                            rankingByChoosing=catRbc,\
##                            Debug=False)
        
        #print(catRbc,catRelation)
        splitCatRelation = [catCRbc['result']]
        chdir(cwd)
    foName = 'splitCatRelation-'+str(categID)+'.py'
    fo = open(foName,'wb')                                            
    fo.write(dumps(splitCatRelation,-1))
    fo.close()
    writestr = 'Finished category %d %d' % (categID,nc)
    return writestr
#####
def _jobTaskKohler(categID):
    """
    Task definition for multiprocessing threaded jobs in QsRbcRanking.
    
    .. Note::
    
          The indiviual quantile classes are linarly order with
          Kohler's ranking rule.
    """
    from pickle import dumps, loads, load
    from copy import copy as deepcopy
    from outrankingDigraphs import BipolarOutrankingDigraph
    from linearOrders import KohlerOrder
    from TransitiveDigraphs import PrincipalInOutDegreesOrdering
    Comments = False
    if Comments:
        print("Starting working on category %d" % (categID), end=" ")
    fiName = 'partialPerfTab-'+str(categID)+'.py'
    fi = open(fiName,'rb')
    pt = loads(fi.read())
    fi.close()
    digraph = BipolarOutrankingDigraph(pt,Normalized=True)
    nc = digraph.order
    if Comments:
        print(nc)
    ko = KohlerOrder(digraph)
    catCRbc = ko.computeRankingByChoosing()
##    catRelation = digraph.computeRankingByChoosingRelation(\
##                        rankingByChoosing=catCRbc['result'],\
##                        Debug=False)
    splitCatRelation = [catCRbc['result']]
    foName = 'splitCatRelation-'+str(categID)+'.py'
    fo = open(foName,'wb')                                            
    fo.write(dumps(splitCatRelation,-1))
    fo.close()
    writestr = 'Finished category %d %d' % (categID,nc)
    return writestr

#####
def _jobTaskKohlerFusion(categID):
    """
    Task definition for multiprocessing threaded jobs in Quantiles Ranking.
    
    .. Note::
    
          The indiviual quantile classes are linarly order with a
          fusion between Kohler's and Arrow-Raynaud's ranking rules.
          The latter corresponds to Kohler's rule applied to the codual
          outranking digraph.
          
    """
    from pickle import dumps, loads, load
    from copy import copy as deepcopy
    from outrankingDigraphs import BipolarOutrankingDigraph
    from linearOrders import KohlerOrder
    from TransitiveDigraphs import PrincipalInOutDegreesOrdering
    Comments = False
    if Comments:
        print("Starting working on category %d" % (categID), end=" ")
    fiName = 'partialPerfTab-'+str(categID)+'.py'
    fi = open(fiName,'rb')
    pt = loads(fi.read())
    fi.close()
    digraph = BipolarOutrankingDigraph(pt,Normalized=True)
    nc = digraph.order
    if Comments:
        print(nc)
    ko = KohlerOrder(digraph)
    kos = KohlerOrder((~(-digraph)))
    fk = FusionDigraph(ko,kos)
    catCRbc = KohlerOrder.computeRankingByChoosing(fk)
    #catRbc = deepcopy(catCRbc['result'])
##    catRelation = digraph.computeRankingByChoosingRelation(\
##                        rankingByChoosing=catCRbc['result'],\
##                        Debug=False)
    splitCatRelation = [catCRbc['result']]
    foName = 'splitCatRelation-'+str(categID)+'.py'
    fo = open(foName,'wb')                                            
    fo.write(dumps(splitCatRelation,-1))
    fo.close()
    writestr = 'Finished category %d %d' % (categID,nc)
    return writestr




#####

class WeakCopelandOrder(TransitiveDigraph):
    """
    instantiates the Weak Copeland Order from
    a given bipolar-valued Digraph instance

    If *SelfCoDual* == *True*, strict incomparabilities are coded
    as *indeterminate* situations. Only the asymmetric part of the preorder is
    instantiated. Otherwise, the classic definition of the weak order as complement of
    the preorder is instantiated.

    """
    def __init__(self,other,SelfCoDual=True,Debug=False):
        """
        constructor for generating a weak order
        from a given other digraph following
        the Copeland ordering rule
        """

        from copy import deepcopy
        from collections import OrderedDict
        from time import time

        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        otherRelation = other.relation
        n = len(other.actions)
        actions = deepcopy(other.actions)
        gamma = other.gamma
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        c = PolarisedDigraph(other)
        cRelation = c.relation
        copelandScores = []
        for x in actions:
##            gx = gamma[x]
            copelandScore = Decimal('0')
            for y in actions:
                copelandScore += cRelation[x][y] - cRelation[y][x]
##            copelandScore = len(gx[0]) - len(gx[1])
            actions[x]['score'] = copelandScore
            copelandScores.append((-copelandScore,x))
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        copelandScores.sort()
        
        self.copelandScores = copelandScores

        copelandRanking = [x[1] for x in copelandScores]
        self.copelandRanking = copelandRanking
        copelandOrder = list(reversed(copelandRanking))
        self.copelandOrder = copelandOrder
        runTimes['copeland'] = time() - tnf

        # init relation
        tr = time()
        for x in actions:
            selfRelation[x] = {}
            for y in actions:
                if SelfCoDual and x == y:
                    selfRelation[x][y] = Med
                else:
                    selfRelation[x][y] = Min
                sx = actions[x]['score']
                sy = actions[y]['score']
                if sx > sy:
                    selfRelation[x][y] = Max
                elif SelfCoDual and sx == sy:
                    selfRelation[x][y] = Med
                else:
                    selfRelation[x][y] = Min
        runTimes['relation'] = time() - tr      
        if Debug:
            print(selfRelation) 
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('Copeland scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.copelandScores:
                print('%s \t %.2f' %(x[1],-x[0]))
        else:
            for x in reversed(self.copelandScores):
                print('%s \t %.2f' %(x[1],-x[0]))

class WeakNetFlowsOrder(TransitiveDigraph):
    """
    Instantiates the Weak NetFlows Order from
    a given bipolar-valued Digraph instance.

    If *SelfCoDual* == *True*, strict incomparabilities are coded as
    *indeterminate* situations. Only the asymmetric part of the preorder is
    instantiated. Otherwise, the classic definition of the weak order as
    complement of the preorder is instantiated.
    
    """
    def __init__(self,other,SelfCoDual=True,Debug=False):
        """
        Constructor for generating a weak order
        from a given other digraph following
        the NetFlows ordering rule
        """

        #from copy import deepcopy
        from collections import OrderedDict
        from time import time

        #timings
        tt = time()
        runTimes = OrderedDict()
        # prepare local variables
        otherRelation = other.relation
        n = len(other.actions)
        actions = other.actions
        gamma = other.gamma
        selfRelation = {}
        Min = Decimal('-1.0')
        Med = Decimal('0.0')
        Max = Decimal('1.0')
        valuationdomain = {'min': Min,\
                           'med': Med,\
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute net flows
        tnf = time()
        netFlowScores = []
        for x in actions:
            netFlowScore = Decimal('0')
            for y in actions:
                netFlowScore += otherRelation[x][y] - otherRelation[y][x]
                if Debug:
                    print(x,y,otherRelation[x][y],otherRelation[y][x],netFlowScore)
            actions[x]['score'] = netFlowScore
            netFlowScores.append((netFlowScore,x))
        # reversed sorting with keeping the actions initial ordering
        # in case of ties
        netFlowScores.sort(reverse=True)
        
        self.netFlowScores = netFlowScores

        netFlowsRanking = [x[1] for x in netFlowScores]
        self.netFlowsRanking = netFlowsRanking
        netFlowsOrder = list(reversed(netFlowsRanking))
        self.netFlowsOrder = netFlowsOrder
        runTimes['netFlows'] = time() - tnf

        # init relation
        tr = time()
        for x in actions:
            selfRelation[x] = {}
            for y in actions:
                if SelfCoDual and x == y:
                    selfRelation[x][y] = Med
                else:
                    selfRelation[x][y] = Min
                sx = actions[x]['score']
                sy = actions[y]['score']
                if sx > sy:
                    selfRelation[x][y] = Max
                elif SelfCoDual and sx == sy:
                    selfRelation[x][y] = Med
                else:
                    selfRelation[x][y] = Min
        runTimes['relation'] = time() - tr      
        if Debug:
            print(selfRelation) 
        self.name = other.name + '_ranked'        
        self.actions = actions
        self.order = n
        self.valuationdomain = valuationdomain
        self.relation = selfRelation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['totalTime'] = time() - tt
        self.runTimes = runTimes

    def showScores(self,direction='descending'):
        print('NetFlows scores in %s order' % direction)
        print('action \t score')
        if direction == 'descending':
            for x in self.netFlowScores:
                print('%s \t %.2f' %(x[1],x[0]))
        else:
            for x in reversed(self.netFlowScores):
                print('%s \t %.2f' %(x[1],x[0]))

#########
# compatibility with obsolete weakOrders module
#######################

class PartialRanking(RankingsFusion):
    """
    dummy class for backward compatibility.
    """

class KemenyWeakOrder(KemenyOrdersFusion):
    """
    dummy class for backward compatibility.
    """

class PrincipalInOutDegreesOrdering(PrincipalInOutDegreesOrderingFusion):
    """
    dummy class for backward compatibility.
    """

class WeakOrder(TransitiveDigraph):
    """
    dummy class for backward compatibility.
    """

####################

#----------test outrankingDigraphs classes ----------------
if __name__ == "__main__":

    from digraphs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from transitiveDigraphs import *
    from linearOrders import *
    from votingProfiles import *
    from time import time

##    v = RandomLinearVotingProfile(numberOfVoters=99,\
##                                  numberOfCandidates=9,seed=201)
##    g = CondorcetDigraph(v)
    g = RandomBipolarOutrankingDigraph(Normalized=True)
    wc = WeakCopelandOrder(g,SelfCoDual=True,Debug=False)
    wc.showRelationTable()
    cop = CopelandOrder(g)
    cop.showRelationTable()
    wc.showScores()
    cop.showScores()
    g.showRelationTable()
    order = g.computeCopelandOrder()
    print(g.computeOrderCorrelation(order))
    print(g.computeOrdinalCorrelation(cop))
    print(g.computeOrdinalCorrelation(wc))
##    wnf = WeakNetFlowsOrder(g,SelfCoDual=False,Debug=False)
##    wnf.showRelationTable()
##    wnf.showScores()
##    g.showRelationTable()
##    print(wc.copelandOrder)
##    print(wnf.netFlowsOrder)
##    wc.showTransitiveDigraph()
##    wnf.showTransitiveDigraph()
##    print(g.computeOrdinalCorrelation(wc))
##    print(g.computeOrdinalCorrelation(wnf))

##    Threading=False
##    t = PerformanceTableau('auditor2_2')
##    t.showHTMLPerformanceHeatmap(Correlations=True,ndigits=0,Debug=False)
##    t = XMCDA2PerformanceTableau('uniSorting')
##    t = RandomCBPerformanceTableau(weightDistribution="equiobjectives",
##                                   numberOfActions=8,seed=105)
##    g = BipolarOutrankingDigraph(t)
##    g.exportGraphViz('testg')
##    wke = KemenyOrdersFusion(g,orderLimit=8)
##    print(wke.topologicalSort())
##    wke.exportGraphViz(fileName='testwke')
##    print(wke.relation)
##
##    from transitiveDigraphs import RankingsFusion
##    from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
##    t = RandomCBPerformanceTableau(numberOfActions=50,seed=10)
##    from outrankingDigraphs import *
##    g = BipolarOutrankingDigraph(t,Normalized=True)
##    from linearOrders import *
##    cop = CopelandOrder(g)
##    nf = NetFlowsOrder(g)
##    wr = RankingsFusion(g,[cop.copelandRanking,nf.netFlowsRanking])
##    print(wr.topologicalSort())
## 
    # pra = PreRankedOutrankingDigraph(t,5,quantilesOrderingStrategy='average')
    # r1 = pra.boostedRanking
    # pro = PreRankedOutrankingDigraph(t,5,quantilesOrderingStrategy='optimistic')
    # r2 = pro.boostedRanking
    # prp = PreRankedOutrankingDigraph(t,5,quantilesOrderingStrategy='pessimistic')
    # r3 = prp.boostedRanking
    # wqr = RankingsFusionDigraph(pra,[r1,r2,r3])
    # wqr.exportGraphViz(fileName='partialOrdering',graphType="pdf")
 
   
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. october 2014                 *')
    print('* $Revision:  $                  *')
    print('*************************************')
