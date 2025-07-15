#!/usr/bin/env python3
"""
Digraph3 module for working with transitive digraphs. 
Copyright (C) 2006-2025  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: Python 3.13.2"

from digraphsTools import *
from digraphs import *
from outrankingDigraphs import *
from transitiveDigraphs import *
#from multiprocessing import Process, active_children, cpu_count
import multiprocessing as mp
mpctx = mp.get_context('spawn')
Process = mpctx.Process
active_children = mpctx.active_children
cpu_count = mpctx.cpu_count


class TransitiveDigraph(Digraph):
    """
    Abstract class for specialized methods addressing transitive digraphs.
    """
    def __init__(self):
        print('abstract root class')

   
            
        
##        for comp in components.values():
##            #comp = self.components[cki]
##            pg = comp['subGraph']
##            if rankingRule == 'Copeland':
##                opg = CopelandOrder(pg)
##                ranking += opg.copelandRanking
##            elif rankingRule == 'NetFlows':
##                opg = NetFlowsOrder(pg)
##                ranking += opg.netFlowsRanking
##            elif rankingRule == 'Kohler':
##                opg = KohlerOrder(pg)
##                ranking += opg.kohlerRanking
##        return ranking

    def computeBoostedOrdering(self,orderingRule='Copeland'):
        """
        Renders an ordred list of decision actions ranked in
        increasing preference direction following the orderingRule
        on each component.
        """
        ranking = self.computeBoostedRanking(rankingRule=orderingRule)
        ranking.reverse()
        return ranking
    
        
    def showPartialOrder(self,rankingByChoosing=None,WithCoverCredibility=False):
        """
        A dummy for the showTransitiveDigraph() method.
        """
        self.showTransitiveDigraph(WithCoverCredibility=WithCoverCredibility)

    def showPartialRanking(self,rankingByChoosing=None,WithCoverCredibility=False):
        """
        A dummy for the showTransitiveDigraph() method.
        """
        self.showTransitiveDigraph(WithCoverCredibility=WithCoverCredibility)
        
    def showTransitiveDigraph(self,rankingByChoosing=None,WithCoverCredibility=False):
        """
        A show method for self.rankinByChoosing result.
        """
        if rankingByChoosing is None:
            try:
                rankingByChoosing = self.rankingByChoosing['result']
            except:
                #print('Error: You must first run self.computeRankingByChoosing(CoDual=False(default)|True) !')
                self.computeRankingByChoosing()
                rankingByChoosing = self.rankingByChoosing['result']
##            else:
##                try:
##                    rankingByChoosing = self.rankingByLastChoosing['result']
##                except:
##                    #print('Error: You must first run self.computeRankingByChoosing(CoDual=False(default)|True) !')
##                    self.computeRankingByLastChoosing()
##                    rankingByChoosing = self.rankingByLastChoosing['result']
        else:
            rankingByChoosing = rankingByChoosing['result']
        print('Ranking by recursively first and last choosing')
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
            if WithCoverCredibility:
                print(' %s%s%s ranked %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
            else:
                print(' %s%s%s ranked %s' % (space,i+1,nstr,ch) )
                
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
            if WithCoverCredibility:
                print(' %s%s%s last ranked %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))
            else:
                print(' %s%s%s last ranked %s' % (space,n-i,nstr,ch) )
                

    def showRankingByChoosing(self,actionsList=None,rankingByChoosing=None,WithCoverCredibility=False):
        """
        Dummy name for showTransitiveDigraph() method
        """
        self.showTransitiveDigraph(rankingByChoosing=rankingByChoosing,
                                   WithCoverCredibility=WithCoverCredibility)
    
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
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,
                                relation=showRelation,
                                Sorted=False,
                                ReflexiveTerms=False)

    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),Comments=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName,
                               bestChoice=bestChoice,
                               worstChoice=worstChoice,
                               Comments=Comments,
                               graphType=graphType,
                               graphSize=graphSize)

#     def exportTopologicalGraphViz(self,fileName=None,
#                                   relation=None,direction='best',
#                                   Comments=True,graphType='png',
#                                   graphSize='7,7',
#                                   fontSize=10,Debug=True):
#         """
#         export GraphViz dot file for Hasse diagram drawing filtering.
#         """
#         import os
#         from copy import copy as deepcopy
            
#         def _safeName(t0):
#             t = t0.split(sep="-")
#             t1 = t[0]
#             n = len(t)
#             if n > 1:
#                 for i in range(1,n):
#                     t1 += '%s%s' % ('_',t[i])
#             return t1
#         # working on a deepcopy of self
#         digraph = deepcopy(self)
#         digraph.computeTopologicalRanking()
#         if not digraph.Acyclic:
#             print('Error: not a transitive digraph !!!')
#             return
#         topologicalRanking = digraph.computeTopologicalRanking()
#         if Debug:
#             print(topologicalRanking)
# ##        if direction == 'best':
# ##            try:
# ##                rankingByChoosing = digraph.rankingByBestChoosing['result']
# ##            except:
# ##                digraph.computeRankingByBestChoosing()
# ##                rankingByChoosing = digraph.rankingByBestChoosing['result']
# ##        else:
# ##            try:
# ##                rankingByChoosing = digraph.rankingByLastChoosing['result']
# ##            except:
# ##                digraph.computeRankingByLastChoosing()
# ##                rankingByChoosing = digraph.rankingByLastChoosing['result']
# ##        if Debug:
# ##            print(rankingByChoosing)
        
#         if Comments:
#             print('*---- exporting a dot file for GraphViz tools ---------*')
#         actionKeys = [x for x in digraph.actions]
#         n = len(actionKeys)
#         if relation is None:
#             relation = deepcopy(digraph.relation)
#         Med = digraph.valuationdomain['med']
#         i = 0
#         if fileName is None:
#             name = digraph.name
#         else:
#             name = fileName
#         dotName = name+'.dot'
#         if Comments:
#             print('Exporting to '+dotName)
# ##        if bestChoice != set():
# ##            rankBestString = '{rank=max; '
# ##        if worstChoice != set():
# ##            rankWorstString = '{rank=min; '
#         fo = open(dotName,'w')
#         fo.write('digraph G {\n')
#         fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
#         fo.write('\\nDigraph3 (graphviz)\\n R. Bisdorff, 2020", size="')
#         fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
#         # nodes
#         for x in actionKeys:  
#             try:
#                 nodeName = digraph.actions[x]['shortName']
#             except:
#                 nodeName = str(x)
#             node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
#                    % (str(_safeName(x)),_safeName(nodeName),fontSize)
#             fo.write(node)
#         # same ranks for Hasses equivalence classes
#         k = len(topologicalRanking)
#         i = 1
#         for ich in topologicalRanking:
#             sameRank = 'subGraph { rank = %d ; ' % i
#             for x in topologicalRanking[ich]:
#                 sameRank += str(_safeName(x))+'; '
#             sameRank += '}\n'
#             print(i,sameRank)
#             fo.write(sameRank)
#             i += 1
# ##        k = len(rankingByChoosing)
# ##        for i in range(k):
# ##            sameRank = '{ rank = same; '
# ##            ich = rankingByChoosing[i][1]
# ##            for x in ich:
# ##                sameRank += str(_safeName(x))+'; '
# ##            sameRank += '}\n'
# ##            print(i,sameRank)
# ##            fo.write(sameRank)

#         # save original relation
#         #originalRelation = deepcopy(relation)
#         #digraph.closeTransitive(Reverse=False)
#         relation = digraph.closeTransitive(Reverse=True,InSite=False)
#         k = len(topologicalRanking)
#         for i in range(1,k+1):
#             ich = topologicalRanking[i]
#             for x in ich:
#                 for j in range(i+1,k+1):
#                     jch = topologicalRanking[j]
#                     for y in jch:
#                         if relation[x][y] > digraph.valuationdomain['med']:
#                             arcColor = 'black'
#                             edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
#                                 (_safeName(x),_safeName(y),1,arcColor)
#                             fo.write(edge)                                                  
#         fo.write('}\n \n')
#         fo.close()
        
#         commandString = 'dot -Grankdir=TB -T'+graphType+' ' + \
#                            dotName+' -o '+name+'.'+graphType
#             #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
#         if Comments:
#             print(commandString)
#         try:
#             os.system(commandString)
#         except:
#             if Comments:
#                 print('graphViz tools not avalaible! Please check installation.')

    def exportGraphViz(self,fileName=None,direction='best',
                       WithBestPathDecoration=False,
                       WithRatingDecoration=False,
                       ArrowHeads=False,
                       Comments=True,graphType='png',
                       graphSize='7,7',bgcolor='cornsilk',
                       fontSize=10,Debug=False):
        """
        export GraphViz dot file for Hasse diagram drawing filtering.
        """
        import os
        from copy import copy as deepcopy
            
        def _safeName(t0):
            t = t0.split(sep="-")
            t1 = t[0]
            n = len(t)
            if n > 1:
                for i in range(1,n):
                    t1 += '%s%s' % ('_',t[i])
            return t1
        # working on a deepcopy of self
        digraph = deepcopy(self)
        if direction == 'best':
            try:
                rankingByChoosing = digraph.rankingByBestChoosing['result']
            except:
                digraph.computeRankingByBestChoosing()
                rankingByChoosing = digraph.rankingByBestChoosing['result']
        else:
            try:
                rankingByChoosing = digraph.rankingByLastChoosing['result']
            except:
                digraph.computeRankingByLastChoosing()
                rankingByChoosing = digraph.rankingByLastChoosing['result']
        if Debug:
            print(rankingByChoosing)
        
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        actionKeys = [x for x in digraph.actions]
        n = len(actionKeys)
        #if relation is None:
        #    relation = deepcopy(digraph.relation)
        Med = digraph.valuationdomain['med']
        i = 0
        if fileName is None:
            name = digraph.name
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
        if bgcolor is None:
            fo.write('graph [ ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')

        else:
            fo.write('graph [ bgcolor = %s, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' % bgcolor)
        fo.write('\\nDigraph3 (graphviz)\\n R. Bisdorff, 2020", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            if WithRatingDecoration:
                if x in digraph.profiles:
                    cat = digraph.profiles[x]['category']
                    if digraph.LowerClosed:
                        nodeName = digraph.categories[cat]['lowLimit'] + ' -'
                    else:
                        nodeName = '- ' +digraph.categories[cat]['highLimit']
                    node = '%s [shape = "box", fillcolor=lightcoral, style=filled, label = "%s", fontsize=%d];\n'\
                       % (str(x),nodeName,fontSize)           
                else:
                    try:
                        nodeName = digraph.actions[x]['shortName']
                    except:
                        nodeName = str(x)
                    node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                       % (str(_safeName(x)),_safeName(nodeName),fontSize)       
            elif WithBestPathDecoration:
                try:
                    nodeName = digraph.actions[x]['shortName']
                except:
                    nodeName = str(x)                    
                if x in digraph.optimalPath:
                    node = '%s [shape = "circle", fillcolor=lightcoral, style=filled, label = "%s", fontsize=%d];\n'\
                       % (str(_safeName(x)),_safeName(nodeName),fontSize)           
                else:
                    node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                       % (str(_safeName(x)),_safeName(nodeName),fontSize)       
            else:
                try:
                    nodeName = digraph.actions[x]['shortName']
                except:
                    nodeName = str(x)
                node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                       % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        # same ranks for Hasses equivalence classes
        k = len(rankingByChoosing)
        for i in range(k):
            sameRank = 'subgraph { rank=same; '
            ich = rankingByChoosing[i][1]
            for x in ich:
                sameRank += str(_safeName(x))+'; '
            sameRank += '}\n'
            print(i,sameRank)
            fo.write(sameRank)

        # open transitive links and write the positive arcs
        relation = digraph.closeTransitive(Reverse=True,InSite=False)
        for i in range(k-1):
            ich = rankingByChoosing[i][1]
            for x in ich:
                for j in range(i+1,k):
                    jch = rankingByChoosing[j][1]
                    for y in jch:
                        #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                        if WithBestPathDecoration:
                            if x in digraph.optimalPath and y in digraph.optimalPath:
                                arcColor = 'blue'
                                lineWidth = 2
                                if relation[x][y] > digraph.valuationdomain['med']:
                                    #arcColor = 'black'
                                    edge = '%s-> %s [label="%.0f",style="setlinewidth(%d)",color=%s] ;\n' %\
                                        (_safeName(x),_safeName(y),digraph.costs[x][y],lineWidth,arcColor)
                                    fo.write(edge)
                                elif relation[y][x] > digraph.valuationdomain['med']:
                                    #arcColor = 'black'
                                    edge = '%s-> %s [label="%.0f",style="setlinewidth(%d)",color=%s] ;\n' %\
                                        (_safeName(y),_safeName(x),digraph.costs[y][x],lineWidth,arcColor)
                                    fo.write(edge)
                            else:
                                arcColor= 'grey'
                                lineWidth = 1
                                if relation[x][y] > digraph.valuationdomain['med']:
                                    #arcColor = 'black'
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                        (_safeName(x),_safeName(y),lineWidth,arcColor)
                                    fo.write(edge)
                                elif relation[y][x] > digraph.valuationdomain['med']:
                                    #arcColor = 'black'
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                        (_safeName(y),_safeName(x),lineWidth,arcColor)
                                    fo.write(edge)

                        else:
                            if relation[x][y] > digraph.valuationdomain['med']:
                                arcColor = 'black'
                                if ArrowHeads:
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                    (_safeName(x),_safeName(y),1,arcColor)
                                else:
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s,arrowhead=none] ;\n' %\
                                    (_safeName(x),_safeName(y),1,arcColor)                                    
                                fo.write(edge)
                            elif relation[y][x] > digraph.valuationdomain['med']:
                                arcColor = 'black'
                                if ArrowHeads:
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                    (_safeName(y),_safeName(x),1,arcColor)
                                else:
                                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s,arrowhead=none] ;\n' %\
                                    (_safeName(y),_safeName(x),1,arcColor)
                                    
                                fo.write(edge)
                                                  
        fo.write('}\n \n')
        fo.close()
        # restore original relation
        #relation = deepcopy(originalRelation)
        
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+\
                        ' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')


class RankingsFusionDigraph(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    digraphs resulting from the epistemic
    disjunctive or conjunctive fusion (omax|omin operator) of a list of rankings.

    *Parameters*:
    
        * other = either a Digraph or a PerformanceTableau object;
        * fusionOperator = 'o-max' (default) | 'o-min' : Disjunctive, resp. conjuntive epistemic fusion.

    Example application:

    >>> from transitiveDigraphs import RankingsFusionDigraph
    >>> from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
    >>> t = RandomPerformanceTableau(seed=1)
    >>> pr = PreRankedOutrankingDigraph(t,10,quantilesOrderingStrategy='average')
    >>> r1 = pr.boostedRanking
    >>> pro = PreRankedOutrankingDigraph(t,10,quantilesOrderingStrategy='optimistic')
    >>> r2 = pro.boostedRanking
    >>> prp = PreRankedOutrankingDigraph(t,10,quantilesOrderingStrategy='pessimistic')
    >>> r3 = prp.boostedRanking
    >>> wqr = RankingsFusionDigraph(pr,[r1,r2,r3])
    >>> wqr.boostedRanking
    ['a07', 'a10', 'a06', 'a11', 'a02', 'a08', 'a04', 'a03', 'a01', 'a09', 'a12', 'a13', 'a05']

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
        self.order = len(self.actions)
        self.name = other.name + '_wk'
        self.rankings = rankings
        self.fusionOperator = fusionOperator
        self.valuationdomain = {}
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

class RankingsFusion(RankingsFusionDigraph):
    """
    Obsolete dummy for the RankingsFusionDigraph class
    """

class KemenyOrdersFusion(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    transitive digraphs resulting from the epistemic
    disjunctive (default) or conjunctive fusion of
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
        if self.computeKemenyRanking(orderLimit=orderLimit,Debug=False) is None:
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

# myThread for KohlerArrawRaynaudFusion
##        if Threading:
##            from multiprocessing import Process, Lock, active_children, cpu_count
class _myKARThread(Process):
    def __init__(self, threadID, name, direction, tempDirName, Debug):
        Process.__init__(self)
        self.threadID = threadID
        self.name = name
        self.direction = direction
        self.workingDirectory = tempDirName
        self.Debug = Debug
    def run(self):
        from linearOrders import KohlerOrder
        from pickle import dumps, loads
        from os import chdir
        chdir(self.workingDirectory)
        from sys import setrecursionlimit
        setrecursionlimit(2**20)
        if self.Debug:
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
                threadBest = _myKARThread(1,"ComputeBest","best",tempDirName,Debug)
                threadWorst = _myKARThread(2,"ComputeWorst","worst",tempDirName,Debug)
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
# my Thread for the RankingByChoosing class
class _myRBCThread(Process):
    def __init__(self, threadID, name, direction, tempDirName, CoDual, Debug):
        Process.__init__(self)
        self.threadID = threadID
        self.name = name
        self.direction = direction
        self.workingDirectory = tempDirName
        self.CoDual = CoDual
        self.Debug = Debug
    def run(self):
        from pickle import dumps, loads
        from os import chdir
        chdir(self.workingDirectory)
        from sys import setrecursionlimit
        setrecursionlimit(2**20)
        Debug = self.Debug
        CoDual = self.CoDual
        if Debug:
            print("Starting working in %s on %s" % (self.workingDirectory, self.name))
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

class RankingByChoosingDigraph(TransitiveDigraph):
    """
    Specialization of the abstract TransitiveDigraph class for 
    ranking-by-Rubis-choosing orderings.
    
    Example python3 session:
    
    >>> from outrankingDigraphs import *
    >>> t = RandomCBPerformanceTableau(numberOfActions=7,
    ...            numberOfCriteria=5,
    ...            weightDistribution='equiobjectives')
    >>> g = BipolarOutrankingDigraph(t,Normalized=True)
    >>> g.showRelationTable()
    * ---- Relation Table -----
       r   |  'a1'   'a2'   'a3'   'a4'   'a5'   'a6'   'a7'   
    -----|------------------------------------------------------------
    'a1' |    +1.00  +1.00  +0.67  +0.33  +0.33  -0.17  +0.00  
    'a2' |   -1.00   +1.00  +0.00  +0.00  +1.00  +0.00  +0.50  
    'a3' |   -0.33  +0.00   +1.00  +0.17  +0.17  -0.17  +0.00  
    'a4' |   +0.00  +0.00  +0.50   +1.00  +0.17  -0.33  -0.50  
    'a5' |   -0.33  -1.00  +0.00  -0.17   +1.00  +0.17  +0.00  
    'a6' |   +0.17  +0.00  +0.42  +0.33  -0.17   +1.00  +0.00  
    'a7' |   +0.00  +0.42  +0.00  +0.50  +0.00  +0.00   +1.00  
    Valuation domain: [-1.000; 1.000]
    >>> from transitiveDigraphs import RankingByChoosingDigraph
    >>> rbc = RankingByChoosingDigraph(g)
    Threading ...
    Exiting computing threads
    >>> rbc.showTransitiveDigraph()
    Ranking by Choosing and Rejecting
     1st ranked ['a3', 'a5', 'a6']
       2nd ranked ['a4']
       2nd last ranked ['a7'])
     1st last ranked ['a1', 'a2'])
    >>> rbc.showOrderedRelationTable(direction="decreasing")
    Decreasing Weak Ordering
    Ranking by recursively best-choosing
     1st Best Choice ['a3', 'a6'] (0.07)
       2nd Best Choice ['a5'] (0.08)
         3rd Best Choice ['a1', 'a4'] (0.17)
           4th Best Choice ['a7'] (-0.67)
             5th Best Choice ['a2'] (1.00)
    * ---- Relation Table -----
      S   |  'a3'	  'a6'	  'a5'	  'a1'	  'a4'	  'a7'	  'a2'	  
    ------|-------------------------------------------
     'a3' |   - 	 0.00	 0.00	 0.67	 0.33	 0.00	 1.00	 
     'a6' |  0.00	  - 	 0.00	 0.00	 0.00	 0.00	 0.17	 
     'a5' |  0.00	 0.00	  - 	 0.33	 0.25	 0.17	 0.17	 
     'a1' |  -0.67	 0.00	 -0.33	  - 	 0.00	 0.00	 0.00	 
     'a4' |  0.00	 0.00	 0.00	 0.00	  - 	 0.33	 0.33	 
     'a7' |  0.00	 0.00	 0.00	 0.00	 0.00	  - 	 0.67	 
     'a2' |  -1.00	 -0.17	 -0.17	 0.00	 -0.33	 -0.67	  - 	 
    Valuation domain: [-1.00;1.00]

    """

    def __repr__(self):
        """
        Presentation method for RankingByChoosing Digraph instance.
        """
        String =  '*-----  Object instance description -----------*\n'
        String += 'Instance class      : %s\n' % self.__class__.__name__
        String += 'Instance name       : %s\n' % self.name
        String += 'Actions             : %d\n' % len(self.actions)
        String += 'Valuation domain    : [%.2f-%.2f]\n' %\
                  (self.valuationdomain['min'],self.valuationdomain['max'])
        String += 'Size                : %d\n' % self.computeSize()
        String += 'Attributes: %s\n' % list(self.__dict__.keys())
        String += 'Determinateness (%%) : %.1f\n' %\
                  self.computeDeterminateness(InPercents=True)
        String += '*------  Constructor run times (in sec.) ------*\n'
        try:
            String += 'Threads             : %d\n' % self.nbrThreads
        except:
            pass
        String += 'Total time          : %.5f\n' % self.runTimes['totalTime']
        String += 'Data input          : %.5f\n' % self.runTimes['dataInput']
        String += 'Ranking-by-choosing : %.5f\n' % self.runTimes['bestLast']
        String += 'Compute fusion      : %.5f\n' % self.runTimes['fusing']
        String += 'Store results       : %.5f\n' % self.runTimes['storing']
        return String 

                    
    
    def __init__(self,other,
                 fusionOperator = "o-max",
                 CoDual=False,
                 Debug=False,
                 #CppAgrum=False,
                 Threading=True):

        from digraphsTools import ranking2preorder, omax, omin        
        from copy import copy, deepcopy
        from pickle import dumps, loads, load
        from time import time

        self.CoDual=CoDual
        self.Debug=Debug
        #self.CppAgrum = CppAgrum
        self.Threading = Threading

        runTimes = {}
        t0 = time()
        #if Threading:
        digraph=deepcopy(other)
        digraph.recodeValuation(-1.0,1.0)
        self.name = digraph.name
        #self.__class__ = digraph.__class__
        self.actions = copy(digraph.actions)
        self.order = len(self.actions)
        self.valuationdomain = digraph.valuationdomain
        self.originalRelation = digraph.relation
        runTimes['dataInput'] = time() - t0

        # compute ranking by best and by last choosing
        t1 = time()
        if Threading and cpu_count()>2:
            print('Threading ...')
            self.nbrThreads = 2
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as tempDirName:
                digraphFileName = tempDirName +'/dumpDigraph.py'
                if Debug:
                    print('temDirName, digraphFileName', tempDirName,digraphFileName)
                fo = open(digraphFileName,'wb')
                pd = dumps(digraph,-1)
                fo.write(pd)
                fo.close()
                threadBest = _myRBCThread(1,"ComputeBest","best",tempDirName,CoDual,Debug)
                threadWorst = _myRBCThread(2,"ComputeWorst","worst",tempDirName,CoDual,Debug)
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
            self.nbrThreads = 1
            from sys import setrecursionlimit
            setrecursionlimit(2**20)
            digraph.computeRankingByBestChoosing(CoDual=CoDual,Debug=Debug)
            digraph.computeRankingByLastChoosing(CoDual=CoDual,Debug=Debug)
            setrecursionlimit(1000)
        runTimes['bestLast'] = time() - t1

        # compute ranking fusion
        t2 = time()
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
        runTimes['fusing'] = time() - t2
        # storing results
        t3 = time()
        self.relation=relFusion
        self.rankingByLastChoosing = copy(digraph.rankingByLastChoosing)
        self.rankingByBestChoosing = copy(digraph.rankingByBestChoosing)
        if Debug:
            self.computeRankingByChoosing()
            self.showRankingByChoosing()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        runTimes['storing'] = time() -t3
        runTimes['totalTime'] = time() - t0
        self.runTimes = runTimes

    def showTransitiveDigraph(self,rankingByChoosing=None,rankingStrategy='optimistic',WithCoverCredibility=False):
        """
        Specialization of generic method.
        Without argument, a weak ordering is recomputed from the
        valued self relation.
        """
        if rankingByChoosing is None:
            if rankingStrategy == 'optimistic':  
                TransitiveDigraph.showTransitiveDigraph(self,
                    rankingByChoosing=self.computeRankingByBestChoosing())
            else:
                TransitiveDigraph.showTransitiveDigraph(self,
                    rankingByChoosing=self.computeRankingByLastChoosing())
        else:
            TransitiveDigraph.showTransitiveDigraph(self,rankingByChoosing=rankingByChoosing)



    def showRankingByChoosing(self,rankingByChoosing=None,rankingStrategy='optimistic',WithCoverCredibility=False):
        """
        Dummy for showTransitiveDigraph method
        """
        self.showTransitiveDigraph(rankingByChoosing=rankingByChoosing,
                                   rankingStrategy=rankingStrategy,
                                   WithCoverCredibility=WithCoverCredibility)

    def computeRankingByBestChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            TransitiveDigraph.computeRankingByBestChoosing(self,CoDual=self.CoDual)

    def computeRankingByLastChoosing(self,Forced=False):
        """
        Dummy for blocking recomputing without forcing. 
        """
        if Forced:
            TransitiveDigraph.computeRankingByLastChoosing(self,CoDual=self.CoDual)

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
        
    def showTransitiveDigraph(self,WithCoverCredibility=False):
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
    
    def showTransitiveDigraph(self,WithCoverCredibility=False):
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

# multiprocessing thread for the principal fusion class
#from multiprocessing import Process, Lock, active_children, cpu_count
class _myPRIODThread(Process):
    def __init__(self, threadID, name, direction,
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
        from linearOrders import PrincipalOrder
        chdir(self.workingDirectory)
        if self.Debug:
            print("Starting working in %s on %s" % (self.workingDirectory,self.name) )
        fi = open('dumpDigraph.py','rb')
        digraph = loads(fi.read())
        fi.close()
        if self.direction == 'col':
            fo = open('priCol.py','wb')
            pc = PrincipalOrder(digraph,
                                Colwise=True,
                                imageType=self.imageType,
                                plotFileName=self.plotFileName,
                                Debug=self.Debug)
            fo.write(dumps(pc,-1))
        elif self.direction == 'row':
            fo = open('priRow.py','wb')
            pl = PrincipalOrder(digraph,
                                Colwise=False,
                                imageType=self.imageType,
                                plotFileName=self.plotFileName,
                                Debug=self.Debug)
            fo.write(dumps(pl,-1))
        fo.close()

class PrincipalInOutDegreesOrderingFusion(TransitiveDigraph):
    """
    Specialization of abstract TransitiveDigraph class for ranking by fusion
    of the principal orders of the variance-covariance of in- 
    (Colwise) and outdegrees (Rowwise).
    
    Example Python3 session with same outranking digraph g as shown in the RankingByChoosingDigraph example session (see below). 
    
    
    >>> from transitiveDigraphs import *
    >>> from votingProfiles import *
    >>> v = RandomLinearVotingProfile(numberOfVoters=99,
    ...                               numberOfCandidates=9,seed=201)
    >>> g = CondorcetDigraph(v)
    >>> pro = PrincipalInOutDegreesOrdering(g,imageType="png", 
    ...                 plotFileName="proTransitiveDigraphing")
        Threading ...
        Exiting both computing threads
    >>> pro.showTransitiveDigraph()
    Ranking by Choosing and Rejecting
     1st ranked ['c9']
       2nd ranked ['c8']
         3rd ranked ['c4']
           4th ranked ['c5']
             5th ranked ['c2']
             5th last ranked ['c2'])
           4th last ranked ['c3'])
         3rd last ranked ['c6'])
       2nd last ranked ['c7'])
     1st last ranked ['c1'])
    >>> pro.showPrincipalScores(ColwiseOrder=True)
    List of principal scores
    Column wise covariance ordered
    action 	 colwise 	 rowwise
    c9 	 0.23974 	 0.23974
    c8 	 0.15961 	 0.15961
    c4 	 0.14299 	 0.14299
    c5 	 0.04205 	 0.04205
    c2 	 -0.04186 	 -0.04186
    c3 	 -0.04552 	 -0.04552
    c6 	 -0.11143 	 -0.11143
    c7 	 -0.16567 	 -0.16567
    c1 	 -0.21991 	 -0.21991
    
    """
    def __init__(self,other,fusionOperator="o-max",
                 imageType=None,
                 plotFileName=None,
                 Threading=True,
                 Debug=False):
        from copy import copy, deepcopy
        from linearOrders import PrincipalOrder
        from pickle import dumps, loads, load

        #if Threading:

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
                threadCol = _myPRIODThread(1,"ComputeCol","col",
                                     tempDirName,
                                     imageType=imageType,
                                     plotFileName=plotFileName,
                                     Debug=Debug)
                threadRow = _myPRIODThread(1,"ComputeRow","row",
                                     tempDirName,
                                     imageType=imageType,
                                     plotFileName=plotFileName,
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
            pc = PrincipalOrder(digraph,Colwise=True,
                                imageType=imageType,
                                plotFileName=plotFileName,
                                Debug=Debug)
            pl = PrincipalOrder(digraph,Colwise=False,
                                imageType=imageType,
                                plotFileName=plotFileName,
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
                print('%s \t %.5f \t %.5f' %\
                      (x,self.actions[x]['principalColwiseScore'],
                       self.actions[x]['principalRowwiseScore']))
        elif ColwiseOrder:
            print('Column wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalColwiseScores:
                print('%s \t %.5f \t %.5f' %\
                      (x,self.actions[x]['principalColwiseScore'],
                       self.actions[x]['principalRowwiseScore']))
        else:
            print('Row wise covariance ordered')
            print('action \t colwise \t rowwise')
            for (y,x) in self.principalRowwiseScores:
                print('%s \t %.5f \t %.5f' %\
                      (x,self.actions[x]['principalColwiseScore'],
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
                
    def showTransitiveDigraph(self, ColwiseOrder=False,WithCoverCredibility=False):
        """
        Specialisation for PrincipalInOutDegreesOrderings.
        """
##        if rankingByChoosing is None:
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
            

    def exportGraphViz(self,fileName=None,direction='ColwiseOrder',
                       Comments=True,graphType='png',
                       graphSize='7,7',
                       fontSize=10):
        """
        Specialisation for PincipalInOutDegrees class.

        direction = "Colwise" (best to worst, default) | "Rowwise" (worst to best)
        """
        if direction == "Colwise":
            direction = 'best'
        else:
            direction = 'worst'
        TransitiveDigraph.exportGraphViz(self, fileName=fileName,
                            direction=direction,
                            Comments=Comments,
                            graphType=graphType,
                            graphSize=graphSize,
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
    with TemporaryDirectory() as tempDirName:
        cwd = getcwd()
        chdir(tempDirName)
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
                               [((digraph.valuationdomain['max'],catContent),
                                (digraph.valuationdomain['max'],catContent))]}
        else:
            if Comments:
                print('==>>> Exceeds %d: Principal ranking' % maxCatContent)
            try:
                pri = PrincipalInOutDegreesOrdering(digraph,Threading=False)
                catCRbc = pri.computeTransitiveDigraph()
            except:
                catCRbc = {'result': [((digraph.valuationdomain['max'],catContent),
                                       (digraph.valuationdomain['max'],catContent))]}

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
    instantiated. Otherwise, the classic definition of the weak order
    as complement of the preorder is instantiated.

    Note: *WithFairestRanking=True*, requires *other* to be
    a valid outranking digraph.
    """
    
    def __init__(self,other,WithFairestRanking=False,SelfCoDual=True,Debug=False):
        """
        constructor for generating a weak order
        from a given other digraph following
        the Copeland ordering rule.
        """

        from copy import deepcopy
        from collections import OrderedDict
        from time import time
        from operator import itemgetter
        from digraphsTools import all_partial_perms

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
        valuationdomain = {'min': Min,
                           'med': Med,
                           'max': Max}
        runTimes['prepareLocals'] = time()-tt
        
        # compute Copeland scores
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
            copelandScores.append((copelandScore,x))
        # sorting with keeping the actions initial ordering
        # in case of ties
        copelandScores.sort(key=itemgetter(0))
        copelandOrder = [x[1] for x in copelandScores]
        self.copelandOrder = copelandOrder       
        copelandScores.sort(key=itemgetter(0),reverse=True)
        copelandRanking = [x[1] for x in copelandScores]
        self.copelandRanking = copelandRanking
        self.copelandScores = copelandScores
        # computing the Copeland preorder
        pl = OrderedDict()
        for score in copelandScores:
            try:
                pl[score[0]].append(score[1])
            except:
                pl[score[0]] = [score[1]]
        plist = []
        for eq in pl:
            plist.append(pl[eq])
        self.copelandPreRanking = plist
        # computing the Copeland permutations
        # and fairest Copeland Ranking
        # Requires *other* to be an outranking digraph instance
        if WithFairestRanking:
            perms = []
            fairestPerms = []
            for p in all_partial_perms(plist):
                perms.append(p)
                corr = other.computeRankingCorrelation(p)
                try:
                    pRes = other.computeRankingConsensusQuality(p)
                except:
                    print('Error: WithFairestRanking is only available for outranking instances!')
                    return
                fairestPerms.append([float(pRes[1])-pRes[2],pRes[1],
                                     pRes[2],corr['correlation'],p])
            fairestPerms.sort(key=itemgetter(0),reverse=True)
            self.copelandPermutations = fairestPerms
            self.fairestCopelandRanking = fairestPerms[0][4]
        # mearsuring run time
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
        from operator import itemgetter
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
        valuationdomain = {'min': Min,
                           'med': Med,
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
        netFlowScores.sort(reverse=True,key=itemgetter(0))
        
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


class PartialBachetRanking(TransitiveDigraph):
    """
    Uses ba default the :py:class:`linearOrders.PolarisedBachetRanking` class for generating a number
    of best correlated Bachet rankings.

    The :py:class:`transitiveDigraphs.RankingsFusionDigraph` uses
    these *Bachet* rankings for contructing a partial *Bachet* ranking result.

    - *g* is a valid BipolarOutrankingDigraph instance.
    - *randomized = integer* (default = 100) gives the number of random permutations
      used for generating different Bachet ranking results.
    - *maxNbrOfRanking = integer* (defaut = 5) is the number of best correlated
      rankings that are used for constructing the *RankingsFusionDigraph* instance.
    - *Polarised = {True (default) | False}*, When Polarised = False, the
      :py:class:`linearOrders.ValuedBachetRanking` class is used.

    >>> from randomPerfTabs import RandomCBPerformanceTableau
    >>> t = RandomCBPerformanceTableau(numberOfActions=20,
    ...                 numberOfCriteria=13,seed=100)
    >>> from outrankingDigraphs import BipolarOutrankingDigraph
    >>> g = BipolarOutrankingDigraph(t)
    >>> from transitiveDigraphs import PartialBachetRanking
    >>> pbr = PartialBachetRanking(g,randomized=100,seed=100,
    ...                       maxNbrOfRankings=10)
    >>> pbr.showTransitiveDigraph(WithCoverCredibility=True)
     Ranking by Choosing and Rejecting
      1st ranked ['a04'] (1.00)
        2nd ranked ['a02', 'a05', 'a06', 'a11', 'a18', 'a20'] (0.70)
          3rd ranked ['a09', 'a14', 'a16'] (0.33)
          3rd last ranked ['a09', 'a10', 'a14']) (0.33)
        2nd last ranked ['a01', 'a03', 'a12', 'a13', 'a15']) (0.60)
      1st last ranked ['a07', 'a08', 'a17', 'a19']) (0.80)
    >>> vpbr = PartialBachetRanking(g,Polarised=False,randomized=100,
    ...                      seed=100,maxNbrOfRankings=10)
    >>> vpbr.showTransitiveDigraph(WithCoverCredibility=True)
     Ranking by Choosing and Rejecting
      1st ranked ['a04'] (1.00)
        2nd ranked ['a02', 'a05', 'a06', 'a18'] (0.77)
          3rd ranked ['a09', 'a11', 'a16', 'a20'] (0.55)
            4th ranked ['a14'] (1.00)
            4th last ranked ['a14'] (1.00)
          3rd last ranked ['a01', 'a12', 'a13', 'a15'] (0.55)
        2nd last ranked ['a03', 'a07', 'a08', 'a10', 'a17'] (0.69)
      1st last ranked ['a19'] (1.00)

    The cover credibities shown above represent in fact the mean outranking, respectively outranked, characteristic value of the complement of the nth choice or rejection. 
    """
    
    def __init__(self,g,randomized=100,maxNbrOfRankings=5,
                 seed=None,Polarised=True,
                 Comments=False,Debug=False):
        from time import time
        if Polarised:
            from linearOrders import PolarisedBachetRanking as BachetRanking
        else:
            from linearOrders import ValuedBachetRanking as BachetRanking
        from copy import deepcopy
        tt = time()
        statistics = {}
        actions = [x for x in g.actions]
        import random
        random.seed(seed)
        j = 0
        for i in range(randomized):
            random.shuffle(actions)
            ba = BachetRanking(g,actionsList=actions,BestQualified=False)
            corrKey = '%.4f' % ba.correlation
            try:
                statistics[corrKey]['freq'] += 1
                j += 1
                if Debug:
                    print(corrKey,j)
            except:
                j = 1
                if Debug:
                    print(corrKey,j)
                statistics[corrKey] = {'freq': j,
                                       'permutation': actions,
                                       'ranking': ba.bachetRanking}

        if Debug:
            print(statistics)
        resStat = [(float(x),statistics[x]) for x in statistics]
        resStat = list(sorted(resStat,reverse=True))
        print(len(resStat))
        bachetRankings = []
        if len(resStat) < maxNbrOfRankings:
            maxNbrOfRankings = len(resStat)
        for i in range(maxNbrOfRankings):
            bachetRankings.append((resStat[i][0],resStat[i][1]['ranking']))
        rankings = [bachetRankings[i][1] for i in range(maxNbrOfRankings)]
        if Debug:
            print(bachetRankings)
        ba1 = RankingsFusionDigraph(g,rankings)
        #ba1.resStat = resStat
        ba1.bachetRankings = bachetRankings
        #ba1.rankings = rankings
        atts = [att for att in ba1.__dict__]
        try:
            atts.remove('vetos')
            atts.remove('negativeVetos')
            atts.remove('methodData')
            atts.remove('concordanceRelation')
            atts.remove('largePerformanceDifferencesCount')
        except:
            pass
        atts.remove('fusionOperator')
        for att in atts:
            self.__dict__[att] = deepcopy(ba1.__dict__[att])
        if Debug:
            ba1.showRankingByChoosing()
        # store attributes
        self.randomized = randomized
        self.seed = seed
        self.maxNbrOfRankings = maxNbrOfRankings
        self.Polarised = Polarised
        self.partialBachetCorrelation = g.computeOrdinalCorrelation(ba1)
        try:
            self.runTimes['totalTime'] = time() - tt
        except:
            pass
        if Comments:
            self.showTransitiveDigraph(WithCoverCredibility=False)

##    def computeBoostedRanking(self):
##        """
##        Renders an ordred list of decision actions ranked in
##        decreasing preference direction following the rankingRule
##        on each component.
##        """
##        ranking = []
##        components = self.computeRankingByChoosing()
##        for i in range(len(components['result'])):
##            ranking += components['result'][i][0][1]
##        ordering = []
##        components = self.computeRankingByChoosing()
##        for i in range(len(components['result'])):
##            ordering += components['result'][i][1][1]
##        boostedRanking = ranking
##        for x in reversed(ordering):
##            if x not in ranking:
##                boostedRanking.append(x)
##        return boostedRanking
##
##    def computeBoostedOrdering(self):
##        """
##        Renders an ordred list of decision actions ranked in
##        decreasing preference direction following the rankingRule
##        on each component.
##        """
##        ranking = []
##        components = self.rankingByChoosing
##        for i in range(len(components['result'])):
##            ranking += components['result'][i][0][1]
##        ordering = []
##        components = self.rankingByChoosing
##        for i in range(len(components['result'])):
##            ordering += components['result'][i][1][1]
##        boostedOrdering = ordering
##        for x in reversed(ranking):
##            if x not in ordering:
##                boostedOrdering.append(x)
##        return boostedOrdering

    def computePartialOutrankingConsensusQuality(self,Sorted=True,
                                                 Comments=False):
        """
        Renders or shows the consensus data of apartial Bachet ranking
        """
        from outrankingDigraphs import OutrankingDigraph
        self.__class__ = OutrankingDigraph
        try:
            cons = self.computePartialOutrankingConsensusQuality(Comments=Comments,
                                ValuedCorrelation = not self.Polarised,
                                Sorted=Sorted)
        except:
            print('Error: the partial ranking is not of OutrankingDigraph type !!!')
            cons = None
        self.__class__ = PartialBachetRanking
        return cons

    def exportGraphViz(self,fileName=None,ArrowHeads=False,
                       Comments=True,graphType='png',
                       graphSize='7,7',bgcolor='cornsilk',
                       fontSize=10,Debug=False):
        """
        export GraphViz dot file for Hasse diagram drawing filtering.
        """
        import os
        from copy import copy as deepcopy
            
        def _safeName(t0):
            t = t0.split(sep="-")
            t1 = t[0]
            n = len(t)
            if n > 1:
                for i in range(1,n):
                    t1 += '%s%s' % ('_',t[i])
            return t1
        # working on a deepcopy of self
        digraph = deepcopy(self)
        digraph.computeRankingByChoosing()
        if Debug:
            print(digraph.rankingByChoosing)
        rbcp = digraph.rankingByChoosing['result']
        rankingByChoosing = []
        k = len(rbcp)
        for i in range(k):
            rankingByChoosing.append(rbcp[i][0])
        for i in range(k):
            rankingByChoosing.append(rbcp[k-i-1][1])
        k1 = len(rankingByChoosing)
        for i in range(1,k1):
            if Debug:
                print('==>>',i,rankingByChoosing[i-1],rankingByChoosing[i])
            ci = []
            for x in rankingByChoosing[i][1]:
                if x not in rankingByChoosing[i-1][1]:
                    ci.append(x)
            if Debug:
                print('==>>',i,rankingByChoosing[i-1],rankingByChoosing[i],ci)                
            rankingByChoosing[i] = (rankingByChoosing[1][0],ci)
        if Debug:
            print('rbcp: ', rbcp)
            print('rankingByChoosing:',rankingByChoosing)
        
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        actionKeys = [x for x in digraph.actions]
        n = len(actionKeys)
        Med = digraph.valuationdomain['med']
        i = 0
        if fileName is None:
            name = digraph.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        if bgcolor is None:
            fo.write('graph [ ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        else:
            fo.write('graph [ bgcolor = %s, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' % bgcolor)
        fo.write('\\nDigraph3 (graphviz)\\n R. Bisdorff, 2020", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            try:
                nodeName = digraph.actions[x]['shortName']
            except:
                nodeName = str(x)
            node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                   % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        # same ranks for Hasses equivalence classes
        k = len(rankingByChoosing)
        for i in range(k):
            sameRank = 'subGraph { rank = same; '
            #sameRank = '{ rank = i; '
            ich = rankingByChoosing[i][1]
            for x in ich:
                sameRank += str(_safeName(x))+'; '
            sameRank += '}\n'
            print(i,sameRank)
            fo.write(sameRank)

        # open transitive links and write the positive arcs
        relation = digraph.closeTransitive(Reverse=True,InSite=False)
        for i in range(k-1):
            ich = rankingByChoosing[i][1]
            for x in ich:
                for j in range(i+1,k):
                    jch = rankingByChoosing[j][1]
                    for y in jch:
                        #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                        if relation[x][y] > digraph.valuationdomain['med']:
                            arcColor = 'black'
                            if ArrowHeads:
                                edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                    (_safeName(x),_safeName(y),1,arcColor)
                            else:
                                edge = '%s-> %s [style="setlinewidth(%d)",color=%s,arrowhead=none] ;\n' %\
                                    (_safeName(x),_safeName(y),1,arcColor)                                
                            fo.write(edge)
                        elif relation[y][x] > digraph.valuationdomain['med']:
                            arcColor = 'black'
                            if ArrowHeads:
                                edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                                    (_safeName(y),_safeName(x),1,arcColor)
                            else:
                                edge = '%s-> %s [style="setlinewidth(%d)",color=%s,arrowhead=none] ;\n' %\
                                    (_safeName(y),_safeName(x),1,arcColor)
                                
                            fo.write(edge)
                                                  
        fo.write('}\n \n')
        fo.close()
        # restore original relation
        #relation = deepcopy(originalRelation)
        
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+\
                        ' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
         
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

    print("""
    ****************************************************
    * Digraph3 transitiveDigraphs module               *
    * depends on BipolarOutrankingDigraph and          *
    * $Revision$ Python3.9                             *
    * Copyright (C) 2010-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    pt = RandomCBPerformanceTableau(numberOfActions=9,numberOfCriteria=13,seed=100)
    g = BipolarOutrankingDigraph(pt)
    pbr = PartialBachetRanking(g,randomized=200,seed=1,Polarised=True,Comments=False,Debug=True)
    print(pbr)
    pbr.showTransitiveDigraph()
    pbr.exportGraphViz('wbg')
    TransitiveDigraph.exportGraphViz(pbr,'test')

    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

