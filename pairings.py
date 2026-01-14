#!/usr/bin/env python3
"""
Python3 implementation of solvers for fair inter- and intragroup pairing problems

Copyright (C) 2023-2025 Raymond Bisdorff

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
#######################

__version__ = "$Revision: Python 3.13.13"

#-------------
from graphs import BipartiteGraph
class InterGroupPairing(BipartiteGraph):
    """
    Abstract root class with private and public methods for intergroup pairing graphs
    """
    def __init__(self):
        print('Abstract root class with private and public methods for intergroup pairing graphs')

    def __repr__(self):
        """
        Default description for FairPairing instances.
        """
        reprString = '*------- InterGroupPairing instance description ------*\n'
        reprString += 'Instance class     : %s\n' % self.__class__.__name__
        reprString += 'Instance name      : %s\n' % self.name
        reprString += 'Group sizes        : %d\n' % len(self.vpA.voters)
        reprString += 'Graph Order        : %d\n' % self.order
        reprString += 'Graph size         : %d\n' % self.size

        try:
            reprString += 'Partners swappings : %d\n' % self.iterations
        except:
            pass            
        reprString += 'Attributes         : %s\n' % list(self.__dict__.keys())
        reprString += '----  Constructor run times (in sec.) ----\n'
        try:
            val = self.runTimes['totalTime']
            reprString += 'Total time         : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['dataInput']
            reprString += 'Data input         : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['storeData']
            reprString += 'Store data         : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['bipartiteGraph']
            reprString += 'Bipartite graph    : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['GroupCorrelations']
            reprString += 'Group correlations : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['Correlations']
            reprString += 'Average correlation: %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['enhancing']
            reprString += 'Enhancing fairness : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['copelandGraph']
            reprString += 'Copeland graph     : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['maximalMatching']
            reprString += 'Maximal matching   : %.5f\n' % val
        except:
            pass
        return reprString

    def computePermutation(self,matching):
        """
        Renders the matching's permutation of *A* and *B* indexes.
        
        .. note:: The prefix of group *A* voters must preceed the prefix of the group *B* voters in alphabetic order 
        """
        permutation = []
        pairs = []
        aKeys = [k for k in self.vpA.voters]
        bKeys = [k for k in self.vpB.voters]
        for m in matching:
            pair = list(m)
            sortedPair = []
            if pair[0] in bKeys:
                pairs.append([pair[1],pair[0]])
            else:
                pairs.append([pair[0],pair[1]])                
        pairs.sort()
        for pair in pairs:
            a = pair[1]
            ai = bKeys.index(a)
            permutation.append(ai+1)
        return permutation

    def computePermutationGraph(self,matching):
        """
        Renders the permutation graph of the matching
        """
        from graphs import PermutationGraph
        permutation = self.computePermutation(matching)
        pg = PermutationGraph(permutation)
        pg.name = 'matching-permutation'
        return pg
        
    def showPairing(self,matching=None):
        print('*------------------------------*')
        pairs = []
        aKeys = [k for k in self.vpA.voters]
        bKeys = [k for k in self.vpB.voters]
        if matching is None:
            matching = self.matching
        for m in matching:
            pair = list(m)
            sortedPair = []
            if pair[0] in aKeys:
                pairs.append([pair[0],pair[1]])
            else:
                pairs.append([pair[1],pair[0]])                
        pairs.sort()
        for pair in pairs:
            print(pair)

    def showCopelandRankingScores(self):
        """
        Print the individual Copeland ranking scores
        """
        print('*---- Copeland ranking scores ----*')
        aKeys = [x for x in self.vpA.voters]
        bKeys = [x for x in self.vpB.voters]
        print('group A',end=':\t')
        for bj in bKeys:
            print(bj,end='\t')
        print()
        for ai in aKeys:
            print('    ',ai,end=':\t')
            for bj in bKeys:
                print('%d'% (self.copelandScores[ai][bj]), end='\t')
            print()
        print('----')
        print('group B',end=':\t')
        for ai in aKeys:
            print(ai,end='\t')
        print()
        for bj in bKeys:
            print('    ',bj,end=':\t')
            for ai in aKeys:
                print('%d'% (self.copelandScores[bj][ai]), end='\t')
            print()

    def showMatchingFairness(self,matching=None,
                            WithGroupCorrelations=True,
                            WithIndividualCorrelations=True):
        #from decimal import Decimal
        from statistics import mean,stdev
        vpA = self.vpA
        vpB = self.vpB
        groupA = [a for a in vpA.voters]
        groupB = [b for b in vpB.voters]

        if matching is None:
            matching = self.matching
        self.showPairing(matching)

        print('-----')
        
        fitness = self.computeIndividualCorrelations(matching)
        groupAScores = fitness[4]
        groupBScores = fitness[5]

        if WithIndividualCorrelations:
            print('group A correlations:')
            for pers in groupAScores:
                print(' \'%s\': %+.3f' % (pers,groupAScores[pers]))
        if WithGroupCorrelations:
            corrs = [ groupAScores[pers] for pers in groupAScores]
            print('group A average correlation (a) : %.3f' % (mean(corrs)))
            print('group A standard deviation      : %.3f' % (stdev(corrs)))

        print('-----')    
        if WithIndividualCorrelations:
            print('group B correlations:')
            for pers in groupBScores:
                print(' \'%s\': %+.3f' % (pers,groupBScores[pers]))
        if WithGroupCorrelations:
            corrs = [ groupBScores[pers] for pers in groupBScores]
            print('group B average correlation (b) : %.3f' % (mean(corrs)))
            print('group B standard deviation      : %.3f' % (stdev(corrs)))
            
        print('-----')
        print('Average correlation    : %.3f' % fitness[1])
        print('Standard Deviation     : %.3f' % fitness[2])
        print('Unfairness |(a) - (b)| : %.3f' % fitness[6])
        

    def exportPairingGraphViz(self,fileName=None,
                              Comments=True,
                              graphType='png',graphSize='7,7',
                              matching=None,
                              edgeColor='blue',
                              bgcolor='cornsilk',
                              lineWidth=1):
        """
        Exports GraphViz dot file for bipartite graph drawing filtering.
        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        Akeys = [x for x in self.vpA.voters]
        Bkeys = [x for x in self.vpB.voters]
        vertexkeys = Akeys + Bkeys
        n = len(vertexkeys)
        if matching is None:
            matching = self.matching
        edges = matching
        #Med = self.valuationDomain['med']
        i = 0
        if fileName is None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        fo = open(dotName,'w')
        fo.write('graph G {\n')
        if bgcolor is not None:
            fo.write('graph [ bgcolor = %s, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' % (bgcolor) )
        else:
            fo.write('graph [ fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nDigraph3 (graphviz), R. Bisdorff, 2023", size="')
        fo.write(graphSize),fo.write('"];\n')
        fo.write('splines=false;\n')
        fo.write('node[shape=circle]\n')
        fo.write('edge[color=%s]\n' % edgeColor)

        fo.write('subgraph cluster_1r {\n')
        n = len(Akeys)
        for i in range(n):
            fo.write('  %s [label="%s",fillcolor=white]\n' % (Akeys[i],Akeys[i]) )
        for i in range(n-1):
            fo.write('  %s--' % Akeys[i])
        fo.write('  %s [style=invis]\n' % (Akeys[n-1]) )
        fo.write('  label = "group A"\n')
        fo.write('  color = white\n')
        fo.write('}\n')
        
        fo.write('subgraph cluster_1l {\n')
        n = len(Bkeys)
        for i in range(n):
            fo.write('  %s [label="%s",fillcolor=white]\n' % (Bkeys[i],Bkeys[i]) )
        for i in range(n-1):
            fo.write('  %s--' % Bkeys[i])
        fo.write(' %s [style=invis]\n' % Bkeys[n-1] )
        fo.write('  label = "group B"\n')
        fo.write('  color = white\n')
        
        fo.write('}\n')

        for m in matching:
            pair = list(m)
            pair.sort()
            fo.write('%s--%s [constraint=false]\n' % (pair[0],pair[1]))
        fo.write('}\n')

        fo.close()
        layout = "dot"
            
        commandString = '%s -T%s %s -o %s.%s' % (layout,graphType,dotName,name,graphType)
        if Comments:
            print(commandString)
        try:
            from os import system
            system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                print('On Ubuntu: ..$ sudo apt-get install graphviz')


    def computeGaleShapleyMatching(self,Reverse=False):
        """
        Documentation:
        https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
        Our implementation is inspired by
        https://johnlekberg.com/blog/2020-08-22-stable-matching.html

        When *Reverse==False*, group *A* is proposing.
        Otherwise, group *B* is proposing
        """
        if Reverse:
            vpA = self.vpB
            vpB = self.vpA
        else:
            vpA = self.vpA
            vpB = self.vpB
        def pref_to_rank(pref):
            # helper fct
            return { a: {b: idx for idx, b in enumerate(a_pref)}
                            for a, a_pref in pref.items()}
        from collections import deque
        A = [a for a in vpA.voters]
        B = [b for b in vpB.voters]
        A_pref = vpA.linearBallot
        B_pref = vpB.linearBallot
        
        B_rank = pref_to_rank(B_pref)
        # lvA candidates are the proposers
        ask_list = {a: deque(bs) for a, bs in A_pref.items()}
        pair = {}

        #
        remaining_A = set(A)
        while len(remaining_A) > 0:
            a = remaining_A.pop()
            b = ask_list[a].popleft()
            if b not in pair:
                pair[b] = a
            else:
                a0 = pair[b]
                b_prefer_a0 = B_rank[b][a0] < B_rank[b][a]
                if b_prefer_a0:
                    remaining_A.add(a)
                else:
                    remaining_A.add(a0)
                    pair[b] = a
        #
        return [frozenset([a, b]) for b, a in pair.items()]

    def isStableMatching(self,matching,Comments=True,Debug=False):
        """
        Test for the existance of matching instabilities.
        Our implementation is inspired by
        https://johnlekberg.com/blog/2020-08-22-stable-matching.html        
        """
        def pref_to_rank(pref):
            # helper fct
            return { a: {b: idx for idx, b in enumerate(a_pref)} \
                            for a, a_pref in pref.items()}
        from collections import namedtuple
        vpA = self.vpA
        vpB = self.vpB
        Pair = namedtuple("Pair", ["groupA", "groupB"])
        groupA = {a for a in vpA.voters}
        groupB = {b for b in vpB.voters}
        A_rank = pref_to_rank(vpA.linearBallot)
        B_rank = pref_to_rank(vpB.linearBallot)
        pairedMatching = []
        for pair in matching:
            pl = list(pair)
            pl.sort()
            pairedMatching.append(Pair(groupA=pl[0], groupB=pl[1]))
        if Debug:
            print(pairedMatching)
                                   
        match_A = {pair.groupA : pair for pair in pairedMatching}
        match_B = {pair.groupB : pair for pair in pairedMatching}
        #print(match_B)
        Unstable = False
        for a in groupA:
            for b in groupB:
                if a != match_B[b].groupA and b != match_A[a].groupB:
                    if A_rank[a][b] < A_rank[a][match_A[a].groupB]\
                        and B_rank[b][a] < B_rank[b][match_B[b].groupA]:
                            if Comments:
                                print('Unstable match: ',\
                                      a,match_A[a],b,match_B[b])
                                print(a,b,'<--', match_A[a].groupB)
                                print(A_rank[a][b],\
                                      A_rank[a][match_A[a].groupB])
                                print(b,a,'<--',match_B[b].groupA)
                                print(B_rank[b][a], \
                                      B_rank[b][match_B[b].groupA])
                            Unstable = True
        if Unstable:
            if Comments:
                self.showPairing(matching)
                print('   is unstable!')
            return False
        else:
            if Comments:
                self.showPairing(matching)
                print('   is stable!')
            return True

    def computeIndividualCorrelations(self,matching,Debug=False):
        """
        Individual correlations for groups A and B
        returns a tuple called fitness with following content
        fitness=(matching,avgCorr,stdCorr,avgCorr-stdCorr,
        groupAScores,groupBScores,
        abs(avgCorrA-avgCorrB))
        """
        # computing groupA's scores
        from digraphs import IndeterminateDigraph
        from decimal import Decimal
        from statistics import mean, stdev
        groupAScores = {}
        vpA = self.vpA
        vpB = self.vpB
        groupA = [a for a in vpA.voters]
        groupB = [b for b in vpB.voters]
        for m in groupA:
            edg = IndeterminateDigraph(order=len(vpA.candidates))
            edg.actions = groupB
            Min = edg.valuationdomain['min']
            Med = edg.valuationdomain['med']
            Max = edg.valuationdomain['max']

            mmatch = [x for x in matching if m in x]
            mmatch = [x for x in mmatch[0] if x != m]
            
            relation = {}
            for x in groupB:
                relation[x] = {}
                for y in groupB:
                    relation[x][y] = Med
            n = len(edg.actions)
            for i in range(n):
                x = groupB[i]
                for j in range(i+1,n):
                    y = groupB[j]
                    if x == mmatch[0]:
                        relation[x][y] = Max
                        relation[y][x] = Min
                    elif y == mmatch[0]:
                        relation[x][y] = Min
                        relation[y][x] = Max
                    else:
                        pass
            edg.relation = relation
            edg.gamma = edg.gammaSets()
            edg.notGamma = edg.notGammaSets()
            #corr = edg.computeRankingCorrelation(vpA.linearBallot[m])
            corr = edg.computeOrdinalCorrelation(vpA.ballot[m])
            groupAScores[m] = Decimal('%.3f' % corr['correlation'])
        
        # computing groupB's scores
        groupBScores = {}
        for w in groupB:
            edg.actions = groupA
            Min = edg.valuationdomain['min']
            Med = edg.valuationdomain['med']
            Max = edg.valuationdomain['max']

            wmmatch = [x for x in matching if w in x]
            wmmatch = [x for x in wmmatch[0] if x != w]                
            relation = {}
            for x in groupA:
                relation[x] = {}
                for y in groupA:
                    relation[x][y] = Med
            n = len(edg.actions)
            for i in range(n):
                x = groupA[i]
                for j in range(i+1,n):
                    y = groupA[j]
                    if x == wmmatch[0]:
                        relation[x][y] = Max
                        relation[y][x] = Min
                    elif y == wmmatch[0]:
                        relation[x][y] = Min
                        relation[y][x] = Max
                    else:
                        pass
            edg.relation = relation
            edg.gamma = edg.gammaSets()
            edg.notGamma = edg.notGammaSets()
            #corr = edg.computeRankingCorrelation(vpB.linearBallot[w])
            corr = edg.computeOrdinalCorrelation(vpB.ballot[w])
            groupBScores[w] = Decimal('%.3f' % corr['correlation'])   

        # computing matching fitness scores

        fitness = []
        aCorrelations = []
        for w in groupAScores:
            aCorrelations.append(groupAScores[w])
        ACorr = mean(aCorrelations)
        bCorrelations = []
        for m in groupBScores:
            bCorrelations.append(groupBScores[m])
        BCorr = mean(bCorrelations)
        fairness = abs(ACorr-BCorr)
        matchingCorrelations = aCorrelations + bCorrelations
        if Debug:
            print(matching)
            print(matchingCorrelations)
        avgCorr = mean(matchingCorrelations)
        stdCorr = stdev(matchingCorrelations)
        if Debug:
            print(avgCorr,stdCorr)
        fitness=(matching,avgCorr,stdCorr,avgCorr-stdCorr,
                 groupAScores,groupBScores,fairness)

        return fitness

    def enhanceMatchingLVFairness(self,matching,Reversed=False,
                                  maxIterations=10,
                                Comments=False,Debug=False):
        """
        Enhance fairness of given matching by using reciprocal linear voting profiles
        """
        vpA = self.vpA
        vpB = self.vpB
        fg = matching
        pairs = []
        aKeys = [k for k in self.vpA.voters]
        bKeys = [k for k in self.vpB.voters]
        for m in matching:
            pair = list(m)
            sortedPair = []
            if pair[0] in aKeys:
                pairs.append([pair[0],pair[1]])
            else:
                pairs.append([pair[1],pair[0]])                
        pairs.sort()
##        pairs = []
##        for p in fg:
##            pair = list(p)
##            pair.sort(reverse=Reversed)
##            pairs.append(pair)
##        pairs.sort()        
        if Comments:
            print(pairs)
        n = len(pairs)
        newPairs = pairs.copy()    
        t = 1
        Enhanced = True
        history = []
        maxIterations = maxIterations
        while Enhanced:            
            Enhanced = False
            if Comments:
                print('==>>> Iteration: ', t)
            if Debug:
                print(pairs)
            enhanceFitness = []
            for i in range(n):
                pair1 = pairs[i]
                for j in range(i+1,n):
                    if Debug:
                        print(i,j)                
                    pair2 = pairs[j]
                    if [pair1,pair2] not in history:
                        # exchange right hands
                        rankDifA1 = -(vpA.linearBallot[pair1[0]].index(pair2[1]) \
                                      -vpA.linearBallot[pair1[0]].index(pair1[1]))
                        rankDifA2 = -(vpA.linearBallot[pair2[0]].index(pair1[1]) \
                                      - vpA.linearBallot[pair2[0]].index(pair2[1]))
                        difGroupA = rankDifA1 + rankDifA2
                        rankDifB1 = -(vpB.linearBallot[pair1[1]].index(pair2[0]) \
                                      - vpB.linearBallot[pair1[1]].index(pair1[0]))
                        rankDifB2 = - (vpB.linearBallot[pair2[1]].index(pair1[0]) \
                                      - vpB.linearBallot[pair2[1]].index(pair2[0]))
                        difGroupB = rankDifB1 + rankDifB2
                        if difGroupA <= difGroupB:
                            # enhance group A correlations
                            enhanceFitness.append(((difGroupA + difGroupB),(difGroupB-difGroupA),(i,j)))
                        else:
                            # enhance group B correlations
                            enhanceFitness.append(((difGroupA + difGroupB),(difGroupA-difGroupB),(i,j)))
            if Debug:
                print(enhanceFitness)
            from operator import itemgetter
            enhanceFitness.sort(reverse=True,key=itemgetter(0,1))
            if Debug:
                print(enhanceFitness[0])
            i = enhanceFitness[0][2][0]
            j = enhanceFitness[0][2][1]
            if Comments:
                print(i,pairs[i])
                print(j,pairs[j])
            pair1 = pairs[i]
            pair2 = pairs[j]
            npair1 = [pair1[0],pair2[1]]
            npair2 = [pair2[0],pair1[1]]
            if [npair1,npair2] in history:
                print('!!!! Cycling :', [npair1,npair2])
                if Debug:
                    print(history)
                Enhanced = False
            elif (enhanceFitness[0][0] >= 0):
                # and (enhanceFitness[0][1] >= 0):
                if Comments:
                    print(pair1,npair1)
                    print(pair2,npair2)
                if Debug:
                    print(pair1[0],self.vpA.linearBallot[pair1[0]])
                    print(pair1[1],self.vpB.linearBallot[pair1[1]])
                    print(pair2[0],self.vpA.linearBallot[pair2[0]])
                    print(pair2[1],self.vpB.linearBallot[pair2[1]])
                    print(npair1,npair2)
                    print(newPairs)
                newPairs.pop(i)
                newPairs.insert(i,npair1)
                newPairs.pop(j)
                newPairs.insert(j, npair2)
                if Debug:
                    print(newPairs)
                history.append([npair1,npair2])
                Enhanced = True
                pairs = newPairs.copy()            
                t += 1
                if t > maxIterations:
                    print('!!!! Too many iterations (max=%d): %d\n' % (maxIterations,t))
                    print('You may adjust the *maxIterations* parameter')
                    Enhanced = False
        nfg = []
        for pair in newPairs:
            nfg.append(frozenset(pair))
        if Comments:
            print('Given matching')
            self.showMatchingFairness(fg)
            print('Fairness enhanced matching')
            self.showMatchingFairness(nfg)
            print('number of iterations:',t)

        return nfg,t,history

    def computeCopelandScore(self,vpA,a,b):
        """
        Replacement for the linear voting profiles information
        when searching for promising swapping candidates
        """
        from decimal import Decimal
        ba = vpA.ballot[a]
        score = Decimal('0')
        candidates = [b for b in vpA.candidates]
        k = len(candidates)
        for i in range(k):
            score += ba[b][candidates[i]] - ba[candidates[i]][b]
        return score

    def enhanceMatchingGeneralFairness(self,matching,
                                       maxIterations=10,
                                       Comments=False,Debug=False):
        """
        Enahance fairness of a given matching using any reciprocal voting profiles
        """
                
        vpA = self.vpA
        vpB = self.vpB
        fg = matching
        pairs = []
        aKeys = [k for k in self.vpA.voters]
        bKeys = [k for k in self.vpB.voters]
        for m in matching:
            pair = list(m)
            sortedPair = []
            if pair[0] in aKeys:
                pairs.append([pair[0],pair[1]])
            else:
                pairs.append([pair[1],pair[0]])                
        pairs.sort()
        if Comments:
            print(pairs)
        n = len(pairs)
        newPairs = pairs.copy()    
        t = 1
        Enhanced = True
        history = []
        maxIterations = maxIterations
        while Enhanced:            
            Enhanced = False
            if Comments:
                print('==>>> Iteration: ', t)
            if Debug:
                print(pairs)
            enhanceFitness = []
            for i in range(n):
                pair1 = pairs[i]
                for j in range(i+1,n):
                    if Debug:
                        print(i,j)                
                    pair2 = pairs[j]
                    if [pair1,pair2] not in history:
                        rankDifA1 = self.copelandScores[pair1[0]][pair2[1]] - \
                                    self.copelandScores[pair1[0]][pair1[1]]
                        rankDifA2 = self.copelandScores[pair2[0]][pair1[1]] - \
                                    self.copelandScores[pair2[0]][pair2[1]]
                        difGroupA = rankDifA1 + rankDifA2
                        rankDifB1 = self.copelandScores[pair1[1]][pair2[0]] - \
                                    self.copelandScores[pair1[1]][pair1[0]]
                        rankDifB2 = self.copelandScores[pair2[1]][pair1[0]] - \
                                    self.copelandScores[pair2[1]][pair2[0]]
                        difGroupB = rankDifB1 + rankDifB2
                        if difGroupA <= difGroupB:
                            # enhance group B correlations
                            enhanceFitness.append(((difGroupA + difGroupB),(difGroupB-difGroupA),(i,j)))
                        else:
                            # enhance group A correlations
                            enhanceFitness.append(((difGroupA + difGroupB),(difGroupA-difGroupB),(i,j)))
                    else:
                        if Debug:
                            print([pair1,pair2], ' in history !')                          
##            if Debug:
##                print(enhanceFitness)
            from operator import itemgetter
            enhanceFitness.sort(reverse=True,key=itemgetter(0))
            if Debug:
                print(enhanceFitness)
            ie = enhanceFitness[0][2][0]
            je = enhanceFitness[0][2][1]
            if Comments:
                print(ie,pairs[ie])
                print(je,pairs[je])
            pair1 = pairs[ie]
            pair2 = pairs[je]
            npair1 = [pair1[0],pair2[1]]
            npair2 = [pair2[0],pair1[1]]
            if [npair1,npair2] in history:
                if Debug:
                    print(history)
                    print('!!!! Cycling :', [npair1,npair2])
                Enhanced = False
##            elif (enhanceFitness[0][0] >= 0) \
##                    and (enhanceFitness[0][1] >= 0):
            elif (enhanceFitness[0][0] >= 0):
                if Comments:
                    print(pair1,npair1)
                    print(pair2,npair2)
                if Debug:
                    print(npair1,npair2)
                    print(newPairs)
                newPairs.pop(ie)
                newPairs.insert(ie,npair1)
                newPairs.pop(je)
                newPairs.insert(je, npair2)
                if Debug:
                    print(newPairs)
                history.append([npair1,npair2])
                Enhanced = True
                pairs = newPairs.copy()            
                t += 1
                if Debug:
                    nfgt = []
                    for pair in newPairs:
                        nfgt.append(frozenset(pair))
                    fitness = self.computeIndividualCorrelations(nfgt)
                    print( '%.3f, %.3f, %.3f' \
                           % (fitness[1],fitness[2],fitness[6]) )
                    
                if t > maxIterations:
                    print('!!!! Too many iterations (max=%d): %d\n' % (maxIterations,t))
                    print('You may adjust the *maxIterations* parameter')
                    Enhanced = False
        nfg = []
        for pair in newPairs:
            nfg.append(frozenset(pair))
        fitness = self.computeIndividualCorrelations(nfg)
        if Comments:
            print('Given matching')
            self.showMatchingFairness(fg)
            print('Fairness enhanced matching')
            self.showMatchingFairness(nfg)
            print('number of iterations:',t)
        return nfg,t,history,fitness

#------   specialized pairing classes -------

class FairnessEnhancedInterGroupMatching(InterGroupPairing):
    """
    The class enhances the fairness of a given matching.

    *Parameters*:

       * *vpA* : any VotingProfile instance
       * *vpB* : reciprocal VotingProfile instance
       * *initialMatching* : a given perfect matching
         if *None* a matching is being previously constructed
         elif 'bestCopeland' a best Copeland intergroup matching is used,
         elif 'Random' a shuffled version of the bi is matched to the ai,
       * The *seed* parameter is used for allowing to repete the same experiment
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """
    def __init__(self,vpA,vpB,
                 initialMatching=None,
                 #RandomInit=False,
                 seed=None,
                 maxIterations=None,
                 Comments=False,Debug=False):
        from time import time
        from decimal import Decimal
        from copy import deepcopy
        self.runTimes = {}
        t0 = time()
        if initialMatching == 'random':
            RandomInit = True
            import random
            random.seed(seed)
            self.seed = seed
        else:
            RandomInit = False
        # store input data
        self.vpA = vpA
        self.vpB = vpB
        self.verticesKeysA = [x for x in vpA.voters]
        self.verticesKeysB = [y for y in vpB.voters]
        self.name = 'fairness-enhanced-matching'
        k = len(vpA.voters)
        self.order = 2 * k
        if maxIterations is None:
            maxIterations = self.order
        self.maxIterations = maxIterations
        if Comments:
            print('Initial matching:', initialMatching)
        # precomputing Copeland ranking scores
        copelandScores = {}
        aKeys = [a for a in vpA.voters]
        bKeys = [b for b in vpB.voters]
        n = len(aKeys)
        for i in range(n):
            ai = aKeys[i]
            bi = bKeys[i]
            copelandScores[ai] = {}
            copelandScores[bi] = {}
            for j in range(n):
                aj = aKeys[j]
                bj = bKeys[j]
                copelandScores[ai][bj] = Decimal()
                copelandScores[bi][aj] = Decimal()
        for i in range(n):
            ai = aKeys[i]
            for j in range(n):
                bj = bKeys[j]   
                copelandScores[ai][bj] = self.computeCopelandScore(vpA,ai,bj)               
        for j in range(n):
            bj = bKeys[j]
            for i in range(n):
                ai = aKeys[i]   
                copelandScores[bj][ai] = self.computeCopelandScore(vpB,bj,ai)                
        self.copelandScores = copelandScores
        if Debug:
            self.showCopelandRankingScores()
 
        t1 = time()
        self.runTimes['dataInput'] = t1 - t0
        # test initialMatching
        t2 = time()
        if initialMatching == 'bestCopeland':
            if Debug:
                print(initialMatching)
            cop = BestCopelandInterGroupMatching(vpA,vpB)
            initialMatching = cop.matching
            if Comments or Debug:
                print('Best Copeland initial matching')
                print(cop.matching)
            fitness = self.computeIndividualCorrelations(initialMatching)
            if fitness[1] == Decimal('1.0'):
                if Comments or Debug:
                    print('Storing given initial maximal fair matching')
                self.initialMatching = initialMatching
                self.matching = initialMatching
                self.iterations = 0
                self.history = []
                self.maxCorr = fitness[1]
                self.stDev = fitness[2]
                self.groupAScores = fitness[4]
                self.groupBScores = fitness[5]
                self.runTimes['enhancing'] = time() - t2             
            else:
                em,it,history,fitnessG = self.enhanceMatchingGeneralFairness(
                                        initialMatching,
                                        maxIterations=maxIterations,
                                        Comments=Comments,
                                        Debug=Debug)
                if fitness[1] >= fitnessG[1] and fitness[2] <= fitnessG[2]:
                    if Comments or Debug:
                        print('Storing given initial maximal fair matching')
                    self.initialMatching = initialMatching
                    self.matching = initialMatching
                    self.iterations = 0
                    self.history = []
                    self.maxCorr = fitness[1]
                    self.stDev = fitness[2]
                    self.groupAScores = fitness[4]
                    self.groupBScores = fitness[5]
                    self.runTimes['enhancing'] = time() - t2
                else:
                    if Comments or Debug:
                        print('Storing maximal fairness enhanced given matching')
                    self.initialMatching = initialMatching
                    self.matching = fitnessG[0]
                    self.iterations = it
                    self.history = history
                    self.maxCorr = fitnessG[1]
                    self.stDev = fitnessG[2]
                    self.groupAScores = fitnessG[4]
                    self.groupBScores = fitnessG[5]
                    self.runTimes['enhancing'] = time() - t2
                
        # compute initial matching
        elif initialMatching is None or initialMatching == 'random':
            
            initialMatchingL = set()
            initialMatchingR = set()
            aKeys = [a for a in vpA.voters]
            bKeys = [b for b in vpB.voters]
            if initialMatching == 'random':
                random.shuffle(bKeys)
            n = len(aKeys)
            for i in range(n):
                initialMatchingL.add(frozenset([aKeys[i],bKeys[i]]))
                initialMatchingR.add(frozenset([aKeys[i],bKeys[-(i+1)]]))
            # enhance left matching
            if Comments or Debug:
                print('==>>> Left initial matching')
            fitnessL = self.computeIndividualCorrelations(initialMatchingL)
            if fitnessL[1] < Decimal('1.0'):
                emL,itL,historyL,fitnessL = self.enhanceMatchingGeneralFairness(
                                            initialMatchingL,
                                            maxIterations=maxIterations,
                                            Comments=Comments,
                                            Debug=Debug)
                if fitnessL[1] == Decimal('1.0'):
                    if Comments or Debug:
                        print('Storing left initial matching maximum result')
                    self.initialMatching = initialMatchingL
                    self.matching = fitnessL[0]
                    self.iterations = itL
                    self.history = historyL
                    self.maxCorr = fitnessL[1]
                    self.stDev = fitnessL[2]
                    self.groupAScores = fitnessL[4]
                    self.groupBScores = fitnessL[5]
                    self.runTimes['enhancing'] = time() - t2                    
                else:
                    if Comments or Debug:
                        print('==>>> Right initial matching')
                    emR,itR,historyR,fitnessR = self.enhanceMatchingGeneralFairness(
                                                    initialMatchingR,
                                                    maxIterations=maxIterations,
                                                    Comments=Comments,
                                                    Debug=Debug)     
                    t2 = time()
                    self.runTimes['enhancing'] = t2 - t1
                    # storing the results
                    
                    if fitnessL[1] >= fitnessR[1] and fitnessL[2] <= fitnessR[2] :
                        if Comments or Debug:
                            print('Storing left maximal fair matching')
                        self.initialMatching = initialMatchingL
                        self.matching = fitnessL[0]
                        self.iterations = itL
                        self.history = historyL
                        self.maxCorr = fitnessL[1]
                        self.stDev = fitnessL[2]
                        self.groupAScores = fitnessL[4]
                        self.groupBScores = fitnessL[5]
                        t3 = time()
                        self.runTimes['enhancing'] = time() - t2
                    else:
                        if Comments or Debug:
                            print('Storing given initial maximal fair matching')
                        self.initialMatching = initialMatchingR
                        self.matching = fitnessR[0]
                        self.iterations = itR
                        self.history = historyR
                        self.maxCorr = fitnessR[1]
                        self.stDev = fitnessR[2]
                        self.groupAScores = fitnessR[4]
                        self.groupBScores = fitnessR[5]
                        self.runTimes['enhancing'] = time() - t2
                                              
            else:  # left initial correlation = +1.000
                if Comments:
                    print('Storing left matching maximum result')
                self.initialMatching = initialMatchingL
                self.matching = fitnessL[0]
                self.iterations = itL
                self.history = historyL
                self.maxCorr = fitnessL[1]
                self.stDev = fitnessL[2]
                self.groupAScores = fitnessL[4]
                self.groupBScores = fitnessL[5]
                self.runTimes['enhancing'] = time() - t2
        else:
            t2 = time()
            if Debug:
                print(initialMatching)
            if Comments:
                print('Given initial matching')
                print(initialMatching)
            fitness = self.computeIndividualCorrelations(initialMatching)
            if fitness[1] == Decimal('1.0'):
                if Comments or Debug:
                    print('Storing given initial maximal fair matching')
                self.initialMatching = initialMatching
                self.matching = initialMatching
                self.iterations = 0
                self.history = []
                self.maxCorr = fitness[1]
                self.stDev = fitness[2]
                self.groupAScores = fitness[4]
                self.groupBScores = fitness[5]
                self.runTimes['enhancing'] = time() - t2             
            else:
                em,it,history,fitnessG = self.enhanceMatchingGeneralFairness(
                                        initialMatching,
                                        maxIterations=maxIterations,
                                        Comments=Comments,
                                        Debug=Debug)
                if fitness[1] >= fitnessG[1] and fitness[2] <= fitnessG[2]:
                    if Comments or Debug:
                        print('Storing given initial maximal fair matching')
                    self.initialMatching = initialMatching
                    self.matching = initialMatching
                    self.iterations = 0
                    self.history = []
                    self.maxCorr = fitness[1]
                    self.stDev = fitness[2]
                    self.groupAScores = fitness[4]
                    self.groupBScores = fitness[5]
                    self.runTimes['enhancing'] = time() - t2
                else:
                    if Comments or Debug:
                        print('Storing maximal fairness enhanced given matching')
                    self.initialMatching = initialMatching
                    self.matching = fitnessG[0]
                    self.iterations = it
                    self.history = history
                    self.maxCorr = fitnessG[1]
                    self.stDev = fitnessG[2]
                    self.groupAScores = fitnessG[4]
                    self.groupBScores = fitnessG[5]
                    self.runTimes['enhancing'] = time() - t2
            
            
        #storing the Graph data
        self.vertices = vpA.voters | vpB.voters
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        mt = []
        for m in self.matching:
            mt.append(frozenset(m))
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                if edgeKey in mt:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()
        
        self.runTimes['totalTime'] = time() - t0

#---------------      

class BestCopelandInterGroupMatching(InterGroupPairing):
    """
    The class computes the individual Copeland ranking scores and
    constructs a best determined perfect intergroup matching
    with a ranked pairs rule

    *Parameters*:

       * *vpA* : any VotingProfile instance
       * *vpB* : reciprocal VotingProfile instance
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """
    def __init__(self,vpA,vpB,Comments=False,Debug=False):
        
        from time import time
        from decimal import Decimal
        from copy import deepcopy
        self.runTimes = {}
        t0 = time()
        # store input data
        self.vpA = vpA
        self.vpB = vpB
        order = len(vpA.voters)
        self.order = 2 * order
        # precomputing Copeland ranking scores
        copelandScores = {}
        aKeys = [a for a in vpA.voters]
        self.verticesKeysA = aKeys
        bKeys = [b for b in vpB.voters]
        self.verticesKeysB = bKeys
        for i in range(order):
            ai = aKeys[i]
            bi = bKeys[i]
            copelandScores[ai] = {}
            copelandScores[bi] = {}
            for j in range(order):
                aj = aKeys[j]
                bj = bKeys[j]
                copelandScores[ai][bj] = Decimal()
                copelandScores[bi][aj] = Decimal()
        minScore = Decimal('0.0')
        for i in range(order):
            ai = aKeys[i]
            for j in range(order):
                bj = bKeys[j]   
                copelandScores[ai][bj] = self.computeCopelandScore(vpA,ai,bj)
                if copelandScores[ai][bj] < minScore:
                    minScore = copelandScores[ai][bj]
        for j in range(order):
            bj = bKeys[j]
            for i in range(order):
                ai = aKeys[i]   
                copelandScores[bj][ai] = self.computeCopelandScore(vpB,bj,ai)                
                if copelandScores[bj][ai] < minScore:
                    minScore = copelandScores[bj][ai]
        self.copelandScores = copelandScores
        if Debug:
            self.showCopelandRankingScores()
        t1 = time()
        self.runTimes['dataInput'] = t1 - t0

        #storing the Copeland graph data
        t2 = time()
        self.name = 'copelandMatching'
        self.vertices = vpA.voters | vpB.voters
        Min = Decimal('%d' % (4*minScore) )
        Med = Decimal('0')
        Max = Decimal('%d' % (4*abs(minScore)) )
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                edges[edgeKey] = Min
        for i in range(order):
            for j in range(order):
                edgeKey = frozenset([aKeys[i],bKeys[j]])
                edges[edgeKey] = (2*abs(minScore)) + self.copelandScores[aKeys[i]][bKeys[j]] \
                            + self.copelandScores[bKeys[j]][aKeys[i]]            
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()
        t3 = time()
        self.runTimes['copelandGraph'] = t3 - t2
        
        # computing the best determined maximal matching
        t4 = time()
        remainingAKeys = [a for a in self.vpA.voters]
        remainingBKeys = [b for b in self.vpB.voters]
        if Debug:
            print(remainingAKeys,remainingBKeys)
        pairs = []
        edges = self.edges
        na = len(remainingAKeys)
        for i in range(na):
            for j in range(na):
                edgeKey = frozenset({remainingAKeys[i],
                                     remainingBKeys[j]})
                pairs.append((edges[edgeKey],edgeKey))
        pairs.sort(reverse=True)
        if Debug:
            print(pairs)
        lmatching = []
        i = 0
        na  = len(pairs)
        while i < na:
            keys = list(pairs[i][1])
            if Debug:
                print(keys)
            if (keys[0] in remainingAKeys and keys[1] in remainingBKeys):
                remainingAKeys.remove(keys[0])
                remainingBKeys.remove(keys[1])
                lmatching.append(pairs[i][1])
                i += 1
                if Debug:
                    print(i,keys,remainingAKeys,remainingBKeys)
                    print(lmatching)
            elif (keys[1] in remainingAKeys and keys[0] in remainingBKeys):
                remainingAKeys.remove(keys[1])
                remainingBKeys.remove(keys[0])
                lmatching.append(pairs[i][1])
                i += 1
                if Debug:
                    print(i,keys,remainingAKeys,remainingBKeys)
                    print(lmatching)
            else:
                i += 1
                
        if Debug:
            print(len(lmatching),lmatching)

        
        self.matching = lmatching
        t5 = time()
        self.runTimes['maximalMatching'] = t5 - t4
        
        t7 = time()
        self.runTimes['totalTime'] = t7 - t0

#----------


class _InterGroupCopelandMatching(InterGroupPairing):
    """
    !!! Not a satisfactory determined perfect matching guaranteed !!!
    
    The class computes the individual Copeland ranking scored
    based maximal matching resulting from the best determined spanning forest
    of the bipartite Copeland scores graph.

    *Parameters*:

       * *vpA* : any VotingProfile instance
       * *vpB* : reciprocal VotingProfile instance
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """
    def __init__(self,vpA,vpB,Comments=False,Debug=False):
        
        from time import time
        from decimal import Decimal
        from copy import deepcopy
        self.runTimes = {}
        t0 = time()
        # store input data
        self.vpA = vpA
        self.vpB = vpB
        self.name = 'copelandMatching'
        order = len(vpA.voters)
        self.order = order
        # precomputing Copeland ranking scores
        copelandScores = {}
        aKeys = [a for a in vpA.voters]
        self.verticesKeysA = aKeys
        bKeys = [b for b in vpB.voters]
        self.verticesKeysB = bKeys
        for i in range(order):
            ai = aKeys[i]
            bi = bKeys[i]
            copelandScores[ai] = {}
            copelandScores[bi] = {}
            for j in range(order):
                aj = aKeys[j]
                bj = bKeys[j]
                copelandScores[ai][bj] = Decimal()
                copelandScores[bi][aj] = Decimal()
        minScore = 0.0
        for i in range(order):
            ai = aKeys[i]
            for j in range(order):
                bj = bKeys[j]   
                copelandScores[ai][bj] = self.computeCopelandScore(vpA,ai,bj)
                if copelandScores[ai][bj] < minScore:
                    minScore = copelandScores[ai][bj]
        for j in range(order):
            bj = bKeys[j]
            for i in range(order):
                ai = aKeys[i]   
                copelandScores[bj][ai] = self.computeCopelandScore(vpB,bj,ai)                
                if copelandScores[bj][ai] < minScore:
                    minScore = copelandScores[bj][ai]
        self.copelandScores = copelandScores
        if Debug:
            self.showCopelandRankingScores()
        t1 = time()
        self.runTimes['dataInput'] = t1 - t0

        #storing the Graph data
        t2 = time()
        self.vertices = vpA.voters | vpB.voters
        Min = Decimal('%d' % (4*minScore) )
        Med = Decimal('0')
        Max = Decimal('%d' % (4*abs(minScore)) )
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                edges[edgeKey] = Min
        for i in range(order):
            for j in range(order):
                edgeKey = frozenset([aKeys[i],bKeys[j]])
                edges[edgeKey] = (2*abs(minScore)) + self.copelandScores[aKeys[i]][bKeys[j]] \
                            + self.copelandScores[bKeys[j]][aKeys[i]]            
        self.edges = edges
        self.gamma = self.gammaSets()
        t3 = time()
        self.runTimes['copelandGraph'] = t3 - t2
        
        # computing the best determined maximal matching
        t4 = time()
        from graphs import BestDeterminedSpanningForest
        bsf = BestDeterminedSpanningForest(self)
        if Debug:
            bsf.exportGraphViz(WithSpanningTree=True,layout='circo')
            dbsf = bsf.graph2Digraph()
            dbsf.showRelationTable(ndigits=0)
        matching = []
        unPaired = []
        gamma = bsf.gamma
        sortedVerticesList = [(len(gamma[v]),v) for v in self.vertices]
        sortedVerticesList.sort()
        verticesList = [v[1] for v in sortedVerticesList]
        if Debug:
            print(verticesList)
                        
        while len(verticesList) > 0:
            sortedVerticesList = [(len(gamma[v]),v) for v in verticesList]
            sortedVerticesList.sort()
            verticesList = [v[1] for v in sortedVerticesList]
            for v1 in verticesList:
                if Debug:
                    print('==>>v1', v1, gamma[v1])
                if len(gamma[v1]) == 1:
                    v2 = gamma[v1].pop()
                    if [v1,v2] not in matching and [v2,v1] not in matching:
                        matching.append(frozenset({v1,v2}))
                        if Debug:
                            print(matching)
                        verticesList.remove(v1)
                        verticesList.remove(v2)
                        gamma[v2] = set()
                        if Debug:
                            print(v1,gamma[v1],v2,gamma[v2])
                    for v3 in verticesList:
                        if Debug:
                            print('v3',v3,gamma[v3])
                        if v1 in gamma[v3]:
                            gamma[v3].remove(v1)
                        if v2 in gamma[v3]:
                            gamma[v3].remove(v2)
                        if Debug:
                            print('v3',v3,gamma[v3])
                elif len(gamma[v1]) == 0:
                    verticesList.remove(v1)
                    unPaired.append(v1)
        if Comments:
            print(len(matching),matching)
            print('==>> unpaired:', unPaired)
        if len(matching) < order:
            remainingAKeys = [a for a in self.vpA.voters]
            remainingBKeys = [b for b in self.vpB.voters]
            for m in matching:
                lm = list(m)
                lm.sort()
                remainingAKeys.remove(lm[0])
                remainingBKeys.remove(lm[1])
            if Debug:
                print(remainingAKeys,remainingBKeys)
            pairs = []
            edges = self.edges
            na = len(remainingAKeys)
            for i in range(na):
                for j in range(na):
                    edgeKey = frozenset({remainingAKeys[i],
                                         remainingBKeys[j]})
                    pairs.append((edges[edgeKey],edgeKey))
            pairs.sort(reverse=True)
            if Debug:
                print(pairs)
            lmatching = [m for m in matching]
            i = 0
            na  = len(pairs)
            while i < na:
                keys = list(pairs[i][1])
                if Debug:
                    print(keys)
                #keys.sort()
                if (keys[0] in remainingAKeys and keys[1] in remainingBKeys):
                    remainingAKeys.remove(keys[0])
                    remainingBKeys.remove(keys[1])
                    lmatching.append(pairs[i][1])
                    #na -= 1
                    i += 1
                    if Debug:
                        print(i,keys,remainingAKeys,remainingBKeys)
                        print(lmatching)
                elif (keys[1] in remainingAKeys and keys[0] in remainingBKeys):
                    remainingAKeys.remove(keys[1])
                    remainingBKeys.remove(keys[0])
                    lmatching.append(pairs[i][1])
                    #na -= 1
                    i += 1
                    if Debug:
                        print(i,keys,remainingAKeys,remainingBKeys)
                        print(lmatching)
                else:
                    i += 1
                    
                        
            matching = lmatching
            if Debug:
                print(len(matching),matching)

        
        self.matching = matching
        t5 = time()
        self.runTimes['maximalMatching'] = t5 - t4
        
        t7 = time()
        self.runTimes['totalTime'] = t7 - t0

#----------

class FairestGaleShapleyMatching(InterGroupPairing):
    """
    The class computes both Gale-Shapley matchings -- group A proposes and group B proposes--
    and renders the fairest of both.

    *Parameters*:

       * *lvA* : LinearVotingProfile instance
       * *lvB* : reciprocal LinearVotingProfile
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """

    def __init__(self,lvA,lvB,Comments=False):

        from decimal import Decimal
        from copy import deepcopy
        from time import time
        t0 = time()
        self.runTimes = {}
        
        # store input data
        self.vpA = lvA
        self.vpB = lvB
        self.name = 'fairest-Gale-Shapley'
        k = len(lvA.voters)
        self.order = 2 * k
        self.verticesKeysA = [x for x in lvA.voters]
        self.verticesKeysB = [y for y in lvB.voters]
        self.runTimes['dataInput'] = time() - t0
        
        # compute Gale-Shapley matchings
        t1 = time()
        gs1 = self.computeGaleShapleyMatching()
        gs2 = self.computeGaleShapleyMatching(Reverse=True)
        self.runTimes['galeShapley'] = time() - t1
        
        # choose the fairest of both
        t2 = time()
        corr1 = self.computeIndividualCorrelations(gs1)
        corr2 = self.computeIndividualCorrelations(gs2)
        if corr1[1] > corr2[1]:
            gs = gs1
        elif corr1[1] == corr2[1] and corr1[2] < corr2[2]:
            gs = gs1
        else:
            gs = gs2
        if Comments:
            print('Fairest Gale-Shapley matching')
            print(gs)
            self.showMatchingFairness(gs,WithIndividualCorrelations=True)
        self.matching = gs
        self.runTimes['chooseFairest'] = time() - t2
        
        # store Graph data
        t3 = time()
        self.vertices = lvA.voters | lvB.voters
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        mt = []
        for m in self.matching:
            mt.append(frozenset(m))
        edges = {}
        for i in range(k):
            vi = verticesList[i]
            for j in range(i+1,k):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                if edgeKey in mt:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()
        self.runTimes['storeGraph'] = time() - t3
        self.runTimes['totalTime'] = time() - t0

class FairestInterGroupPairing(InterGroupPairing):
    """
    The class computes the fitness scores of the complete set of maximal matchings between
    two groups *A* and *B* of persons of equal number *k* and delivers, based on these fitness scores, a fairest pairing of the persons of both groups.

    *Parameters*:

       * *vpA* : any type of VotingProfile instance
       * *vpB* : reciprocal VotingProfile instance
       * *oderLimit* : preventing a potential CPU memory or time overflow
       * *StableMatchings* : False (default) / True limits to only stable matchings

    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """

    def __init__(self,vpA,vpB,orderLimit=6,
                 StableMatchings=False,
                 Comments=False,Debug=False):

        from copy import deepcopy
        from decimal import Decimal
        runTimes = {}
        from time import time
        # check size of problem
        groupA = [x for x in vpA.voters]
        k = len(groupA)
        if Debug:
            print('groupA',groupA) 
        if k > orderLimit:
            print('The size %d of the groups to pair is too high' % k)
            print('The order limit is %d' % orderLimit)
            print('Use the orderLimit parameter for larger orders')
            return
        t0 = time()
        groupB = [x for x in vpB.voters]
        if Debug:
            print('groupB',groupB)
        # from graphs import BipartiteGraph
        # verticesKeys = groupA + groupB
        # if Debug:
        #     print(verticesKeys)

        # storing input data 
        self.name = 'pairingProblem'
        self.order = 2 * k
        self.vpA = vpA
        self.vpB = vpB
        self.verticesKeysA = groupA
        self.verticesKeysB = groupB
        t1 = time()
        runTimes['inputData'] = t1 - t0
        if Comments:
            print(runTimes)
        # compute bipartite graph
        # g = CompleteGraph(verticesKeys=verticesKeys)
        # dg = g.graph2Digraph()
        # from digraphs import BipartitePartialDigraph
        # bpdg = BipartitePartialDigraph(dg,groupA,groupB,Partial=False)
        # bpg = bpdg.digraph2Graph()
        from graphs import CompleteBipartiteGraph
        bpg = CompleteBipartiteGraph(groupA,groupB)
        if Debug:
            print('bipartite graph',bpg)
        t2 = time()
        runTimes['bipartiteGraph'] = t2 - t1
        if Comments:
            print(runTimes)
        # compute maximal matchings
        from graphs import LineGraph
        lbpg = LineGraph(bpg)
        lbpg.computeMIS()
        maximalMatchings = lbpg.misset
        t3 = time()
        runTimes['maximalMatching'] = t3 - t2
        if Comments:
            print(runTimes)
        # computing matching correlations
        from statistics import mean, stdev
        from decimal import Decimal
        from digraphs import IndeterminateDigraph
        pairings = []
        groupAScores = {}
        groupBScores = {}

        for matching in maximalMatchings:
            
            # computing groupA's scores
            groupAScores = {}
            for m in groupA:
                edg = IndeterminateDigraph(order=len(vpA.candidates))
                edg.actions = groupB
                Min = edg.valuationdomain['min']
                Med = edg.valuationdomain['med']
                Max = edg.valuationdomain['max']

                mmatch = [x for x in matching if m in x]
                mmatch = [x for x in mmatch[0] if x != m]
                
                relation = {}
                for x in groupB:
                    relation[x] = {}
                    for y in groupB:
                        relation[x][y] = Med
                n = len(edg.actions)
                for i in range(n):
                    x = groupB[i]
                    for j in range(i+1,n):
                        y = groupB[j]
                        if x == mmatch[0]:
                            relation[x][y] = Max
                            relation[y][x] = Min
                        elif y == mmatch[0]:
                            relation[x][y] = Min
                            relation[y][x] = Max
                        else:
                            pass
                edg.relation = relation
                edg.gamma = edg.gammaSets()
                edg.notGamma = edg.notGammaSets()
                #corr = edg.computeRankingCorrelation(vpA.linearBallot[m])
                corr = edg.computeOrdinalCorrelation(vpA.ballot[m])
                groupAScores[m] = Decimal('%.3f' % corr['correlation'])
            
            # computing groupB's scores
            groupBScores = {}
            for w in groupB:
                edg.actions = groupA
                Min = edg.valuationdomain['min']
                Med = edg.valuationdomain['med']
                Max = edg.valuationdomain['max']

                wmmatch = [x for x in matching if w in x]
                wmmatch = [x for x in wmmatch[0] if x != w]                
                relation = {}
                for x in groupA:
                    relation[x] = {}
                    for y in groupA:
                        relation[x][y] = Med
                n = len(edg.actions)
                for i in range(n):
                    x = groupA[i]
                    for j in range(i+1,n):
                        y = groupA[j]
                        if x == wmmatch[0]:
                            relation[x][y] = Max
                            relation[y][x] = Min
                        elif y == wmmatch[0]:
                            relation[x][y] = Min
                            relation[y][x] = Max
                        else:
                            pass
                edg.relation = relation
                edg.gamma = edg.gammaSets()
                edg.notGamma = edg.notGammaSets()
                #corr = edg.computeRankingCorrelation(vpB.linearBallot[w])
                corr = edg.computeOrdinalCorrelation(vpB.ballot[w])
                groupBScores[w] = Decimal('%.3f' % corr['correlation'])
            t3a = time()
            runTimes['GroupCorrelations'] = t3a - t3
            # computing matching fitness scores

            aCorrelations = [groupAScores[w] for w in groupAScores]
##            for w in groupAScores:
##                aCorrelations.append(groupAScores[w])
            bCorrelations = [groupBScores[m] for m in groupBScores]
##            for m in groupBScores:
##                bCorrelations.append(groupBScores[m])
            ACorr = mean(aCorrelations)
            BCorr = mean(bCorrelations)
            fairness = abs(ACorr-BCorr)
            matchingCorrelations = aCorrelations + bCorrelations
            if Debug:
                print(matching)
                print(matchingCorrelations)
            avgCorr = mean(matchingCorrelations)
            stdCorr = stdev(matchingCorrelations)
            if Debug:
                print(avgCorr,stdCorr)
            pairings.append((matching,avgCorr,-stdCorr,avgCorr-stdCorr,
                             groupAScores,groupBScores,-fairness))

        # sorting the fitness scores
        from operator import itemgetter
        pairings.sort(reverse=True,key=itemgetter(1,6,2))
        #pairings.sort(reverse=True,key=itemgetter(6,1,3))
        t4 = time()
        runTimes['Correlations'] = t4 - t3a
        # index to stable pairings
        if StableMatchings:
            stableIndex = []
            n = len(pairings)
            for i in range(n):
                m = pairings[i]
                matching = m[0]
                if self.isStableMatching(matching,Comments=False):
                    stableIndex.append(i)
            self.stableIndex = stableIndex
            t5 = time()
            runTimes['StableIndex'] = t5 -t4
        # storing results
        self.bpg = bpg
        self.pairings = pairings
        self.matching = pairings[0][0]
        #storing the Graph data
        self.vertices = vpA.voters | vpB.voters
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        mt = []
        for m in self.matching:
            mt.append(frozenset(m))
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                if edgeKey in mt:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        self.edges = edges
        self.size = self.computeSize()
        self.gamma = self.gammaSets()


        t6 = time()
        runTimes['totalTime'] = t6 - t0
        self.runTimes = runTimes
        
        # showing the faires pairing
        if Comments:
            print('Fairest pairing solution')
            self.showPairing(pairings[0][0])
        
    #------------- class methods

    # def exportBipartiteGraphViz(self,fileName=None,rank=1):
    #     """
    #     Bipartite graph circular drawing with Fairness ranked (default= fairest) matching in colour.

    #     The *rank* parameter allows to select a lesser fair matching in the self.pairings list.

    #     """
    #     from graphs import BipartiteGraph
    #     BipartiteGraph.exportBipartiteGraphViz(self,fileName=('pairing%d' % rank),
    #                             matching=self.pairings[rank-1][0],
    #                             layout='circo')
       
    def showFairestPairing(self,rank=1,WithIndividualCorrelations=False):
        """
        Setting the *rank* parameter to a value > 1,
        gives access to lesser fitting pairings.

        The *WithIndividualCorrelations* flag shows the correlations with
        the individual pairing preferences. 
        """
        index = rank - 1
        print('*------------------------------*')
        if index == 0:
            print('Fairest pairing')
        elif index == 1:
            print('2nd-ranked pairing')
        elif index == 2:
            print('3rd-ranked pairing')
        else:
            print('%th-ranked pairing' % (index+1))
        fitness = self.pairings
        self.showMatchingFairness(fitness[index][0],
                WithIndividualCorrelations=WithIndividualCorrelations)

    def computeMatchingFairnessIndex(self,matching,Comments=False):
        """
        Renders the index position of the given matching in the
        fairness ranked self.pairings list.
        """
        # converting to the frozenset formst
        pairing = []
        for pair in matching:
            pairing.append(frozenset(pair))
        pairing = frozenset(pairing)
        n = len(self.pairings)
        for i in range(n):
            if pairing == self.pairings[i][0]:
                if Comments:
                    print('Fairness index of matching: ',i)
                break
        return i

from graphs import Graph
class IntraGroupPairing(Graph):
    """
    Abstract root class for IntraGroup pairing solutions
    """

    def __init__():
        print('Abstract root class for intragroup pairing graphs')


    def __repr__(self):
        """
        Default description for FairPairing instances.
        """
        reprString = '*------- IntraGroupPairing instance description ------*\n'
        reprString += 'Instance class    : %s\n' % self.__class__.__name__
        reprString += 'Instance name     : %s\n' % self.name
        reprString += 'Group size        : %d\n' % self.order
        try:
            reprString += 'Nbr of matchings  : %d\n' % self.nbrOfMatchings
        except:
            pass            
        try:
            reprString += 'Partners swapping : %d\n' % self.iterations
        except:
            pass            
        reprString += 'Attributes        : %s\n' % list(self.__dict__.keys())
        reprString += '----  Constructor run times (in sec.) ----\n'
        try:
            val = self.runTimes['totalTime']
            reprString += 'Total time           : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['dataInput']
            reprString += 'Data input           : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['maximalMatching']
            reprString += 'Maximal matchings    : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['matchingCorrelations']
            reprString += 'Pairing correlations : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['sortingFitness']
            reprString += 'Sorting Fitness      : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['storeResults']
            reprString += 'Storing results      : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['CopelandGraph']
            reprString += 'Copeland graph       : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['PairingsSize']
            reprString += 'Pairings size        : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['enhancing']
            reprString += 'Enhancing fairness   : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['leftEnhancing']
            reprString += 'Left enhancing       : %.5f\n' % val
        except:
            pass
        try:
            val = self.runTimes['rightEnhancing']
            reprString += 'Right enhancing      : %.5f\n' % val
        except:
            pass
        return reprString

    def showPairing(self,matching=None):
        """
        shows the intragroup pairing solution when *matching is None*
        """
        print('Matched pairs')
        pairs = []
        aKeys = self.persons
        if matching is None:
            matching = self.matching
        for m in matching:
            pair = list(m)
            pairs.append([pair[0],pair[1]])
        pairs.sort()
        n = len(pairs)
        for i in range(n):
            print("{'%s', '%s'}" % (pairs[i][0],pairs[i][1]))

    def showMatchingFairness(self,matching=None,
                            WithIndividualCorrelations=True):
        """
        Shows the intragroup faines of a given matching.
        When *matching is None* the fairest matching of the class is used
        """
        #from decimal import Decimal
        from statistics import mean,stdev
        vpA = self.vpA
        groupA = self.persons
        if matching is None:
            matching = self.matching
        self.showPairing(matching)

        correlation,stdDev,groupAScores = \
                self.computeIndividualCorrelations(matching)

        if WithIndividualCorrelations:
            print('----')
            print('Individual correlations:')
            for pers in groupAScores:
                print(' \'%s\': %+.3f' % (pers,groupAScores[pers])  )
        print('-----')
        print('Average correlation : %+.3f' % correlation)
        print('Standard deviation  :  %.3f' % stdDev)

    def exportPairingGraphViz(self,fileName=None,
                              Comments=True,
                              graphType='png',graphSize='7,7',
                              matching=None,
                              edgeColor='blue',
                              bgcolor='cornsilk',
                              lineWidth=2):
        """
        Exports GraphViz dot file for pairing graph drawing filtering.
        """
        import os
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')

        #Akeys = self.persons
        #Bkeys = self.persons
        vertexKeys = self.persons
        n = len(vertexKeys)
        k = n//2
##        aKeys = vertexKeys[:k]
##        bKeys = vertexKeys[k:]

        if matching is None:
            edges = self.edges
        else:
            mt = {}
            for m in matching:
                mt.append(frozenset(m))
            edges = {}
            for i in range(n):
                vi = vertexKeys[i]
                for j in range(i+1,n):
                    vj = vertexKeys[j]
                    edgeKey = frozenset({vi,vj})
                    if edgeKey in mt:
                        edges[edgeKey] = Max
                    else:
                        edges[edgeKey] = Min
                        
        Med = self.valuationDomain['med']
        aKeys = []
        bKeys = []
        pairs = []
        for edgeKey in edges:
            if edges[edgeKey] > Med:
                pair = list(edgeKey)
                pair.sort()
                pairs.append(pair)
                if edges[edgeKey] > Med:
                    aKeys.append(pair[0])
                    bKeys.append(pair[1])
                             
        i = 0
        if fileName is None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        fo = open(dotName,'w')
        fo.write('graph G {\n')
        if bgcolor is not None:
            fo.write('graph [ bgcolor = %s, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' % (bgcolor) )
        else:
            fo.write('graph [ fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nDigraph3 (graphviz), R. Bisdorff, 2023", size="')
        fo.write(graphSize),fo.write('"];\n')
        fo.write('splines=false;\n')
        fo.write('node[shape=circle]\n')
        fo.write('edge[color=%s]\n' % edgeColor)

        fo.write('subgraph cluster_1r {\n')
        for i in range(k):
            fo.write('  a%d [label="%s",fillcolor=white]\n' % (i+1,aKeys[i]) )
        for i in range(k-1):
            fo.write('  a%d--' % (i+1) )
        fo.write('  a%d [style=invis]\n' % k )
        fo.write('  label = "Paired"\n')
        fo.write('  color = white\n')
        fo.write('}\n')
        
        fo.write('subgraph cluster_1l {\n')
        for i in range(k):
            fo.write('  b%d [label="%s",fillcolor=white]\n' % (i+1,bKeys[i]) )
        for i in range(k-1):
            fo.write('  b%d--' % (i+1) )
        fo.write(' b%d [style=invis]\n' % k )
        fo.write('  label = "Persons"\n')
        fo.write('  color = white\n')
        fo.write('}\n')

        Med = self.valuationDomain['med']
        for pair in pairs:
            inda = aKeys.index(pair[0]) + 1
            indb = bKeys.index(pair[1]) + 1
            fo.write('a%d--b%d [constraint=false]\n' % (inda,indb))
        fo.write('}\n')

        fo.close()
        layout = "dot"
            
        commandString = '%s -T%s %s -o %s.%s' % (layout,graphType,dotName,name,graphType)
        if Comments:
            print(commandString)
        try:
            from os import system
            system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')
                print('On Ubuntu: ..$ sudo apt-get install graphviz')


    def computeIndividualCorrelations(self,matching=None,Debug=False):
        """
        Individual correlations for intragroup pairing solution
        returns a tuple called fitness with following content
        avgCorr,stdCorr, groupScores
        """
        # computing groupA's scores
        from digraphs import IndeterminateDigraph
        from decimal import Decimal
        from statistics import mean, stdev
        groupAScores = {}
        vpA = self.vpA
        groupA = self.persons
        if matching is None:
            matching = self.matching
        for m in groupA:
            groupB = groupA
            edg = IndeterminateDigraph(order=len(groupA))
            edg.actions = groupB
            Min = edg.valuationdomain['min']
            Med = edg.valuationdomain['med']
            Max = edg.valuationdomain['max']

            mmatch = [x for x in matching if m in x]
            mmatch = [x for x in mmatch[0] if x != m]
            
            relation = {}
            for x in groupB:
                relation[x] = {}
                for y in groupB:
                    relation[x][y] = Med
            n = len(groupB)
            for i in range(n):
                x = groupB[i]
                for j in range(i+1,n):
                    y = groupB[j]
                    if x == mmatch[0]:
                        relation[x][y] = Max
                        relation[y][x] = Min
                    elif y == mmatch[0]:
                        relation[x][y] = Min
                        relation[y][x] = Max
                    else:
                        pass
            edg.relation = relation
            edg.gamma = edg.gammaSets()
            edg.notGamma = edg.notGammaSets()
            if Debug:
                print(m)
                edg.showRelationTable()
            ballot = vpA.ballot[m]
            if Debug:
                edg.showRelationTable(relation=ballot)
            corr = edg.computeOrdinalCorrelation(ballot)
            groupAScores[m] = Decimal('%.3f' % corr['correlation'])
        scores = [groupAScores[m] for m in groupAScores]
        
        return mean(scores), stdev(scores), groupAScores
            
    def computeCopelandScore(self,a,b):
        """
        Computes fitness of swapping candidates
        """
        from decimal import Decimal
        vpA = self.vpA
        ba = self.vpA.ballot[a]
        #ba = ballot
        score = Decimal('0')
        candidates = [b for b in vpA.voters]
        n = len(candidates)
        for i in range(n):
            score += ba[b][candidates[i]] - ba[candidates[i]][b]
        return score

    def showCopelandScores(self):
        try:
            copelandScores = self.copelandScores
        except:
            copelandScores = self.computeCopelandScores()
        copEdges = {}
        for p1 in self.persons:
            for p2 in self.persons:
                if p1 != p2:
                    edgeKey = frozenset([p1,p2])
                    copEdges[edgeKey] = copelandScores[p1][p2]
        self.showEdgesCharacteristicValues(edges=copEdges,ndigits=0)

    def enhanceMatchingFairness(self,matching,
                                Comments=False,Debug=False):
        """
        Heuristic for fairness enhancing of given matching
        """
        from copy import copy
        from decimal import Decimal
        
        
        vpA = self.vpA
        persons = self.persons
        initialMatching = matching
        pairs = []
        aKeys = persons
        bKeys = persons
        matchesVisited = [initialMatching]
        corrA, stdDevA, groupAScores =\
                self.computeIndividualCorrelations(initialMatching)
        maxCorr = corrA

        for m in initialMatching:
            pair = list(m)
            pairs.append(pair)                
        pairs.sort()
        if Comments:
            print('*---- Initial matching ----*')
            print(pairs)
        n = len(pairs)
        newPairs = pairs.copy()    
        self.t += 1
        if maxCorr < Decimal('1.0'):
            Enhanced = True
        else:
            Enhanced = False
            if Debug:
                print('the given matching is fairest possible')
                print(newPairs,maxCorr)
            return pairs,maxCorr,matchesVisited
        #history = []    
        while Enhanced and self.t <= self.maxIterations:            
            Enhanced = False
            if Comments:
                print('Enhancing iteration : ', self.t)
            if Debug:
                print(pairs)
            enhanceFitness = []
            for i in range(n):
                pair1 = pairs[i]
                for j in range(i+1,n):
                    if Debug:
                        print(i,j)                
                    pair2 = pairs[j]
                    #if (pair1,pair2) not in history:
                        #history.append((pair1,pair2))
                    rankDifA1 = self.copelandScores[pair1[0]][pair2[1]] - \
                                self.copelandScores[pair1[0]][pair1[1]]
                    rankDifA2 = self.copelandScores[pair2[0]][pair1[1]] - \
                                self.copelandScores[pair2[0]][pair2[1]]
##                    if Debug:
##                        print('rankDifferences A')
##                        print([pair1,pair2])
##                        print(pair1[0],pair2[1],pair1[1],rankDifA1)
##                        print(pair2[0],pair1[1],pair2[1],rankDifA2)
                    difGroupA = rankDifA1 + rankDifA2
                    rankDifB1 = self.copelandScores[pair1[1]][pair2[0]] - \
                                self.copelandScores[pair1[1]][pair1[0]]
                    rankDifB2 = self.copelandScores[pair2[1]][pair1[0]] - \
                                self.copelandScores[pair2[1]][pair2[0]]
##                    if Debug:
##                        print('rankDifferences B')
##                        print([pair1,pair2])      
##                        print(rankDifB1)
##                        print(rankDifB2)
                    difGroupB = rankDifB1 + rankDifB2
                    enhanceFitness.append( ( (difGroupA + difGroupB), (i,j), False ) )
##                    if Debug:
##                        print('Twisted')
##                        print('avant',pair1,pair2)
                    tpair1 = copy(pair1)
                    tpair2 = copy(pair2)
                    sw = copy(tpair1[1])
                    tw = copy(tpair2[0])
                    tpair1[1] = tw
                    tpair2[0] = sw
                    if Debug:
                        print(tpair1,tpair2)
##                    if [pair1,pair2] not in history:
                    rankDifA1 = self.copelandScores[tpair1[0]][tpair2[0]] - \
                                self.copelandScores[tpair1[0]][tpair1[1]]
                    rankDifA2 = self.copelandScores[tpair2[0]][tpair1[0]] - \
                                self.copelandScores[tpair2[0]][tpair2[1]]
##                    if Debug:
##                        print('rankDifferences A')
##                        print([tpair1,tpair2])
##                        print(rankDifA1,tpair1[0],tpair2[0],tpair1[1])
##                        print(rankDifA2,tpair2[0],tpair1[0],tpair2[1])
                    difGroupA = rankDifA1 + rankDifA2
                    rankDifB1 = self.copelandScores[tpair2[1]][tpair1[1]] - \
                                self.copelandScores[tpair2[1]][tpair2[0]]
                    rankDifB2 = self.copelandScores[tpair1[1]][tpair2[1]] - \
                                self.copelandScores[tpair1[1]][tpair1[0]]
##                    if Debug:
##                        print('rankDifferences B')
##                        print([tpair1,tpair2])
##                        print(rankDifB1,)
##                        print(rankDifB2)
                    difGroupB = rankDifB1 + rankDifB2
                    enhanceFitness.append( ( -(difGroupA + difGroupB), (i,j), True ) )
##                    else:
##                        print((pair1,pair2), 'already in history')
            if Debug:
                print(self.t, enhanceFitness)
                #print(history)
            from operator import itemgetter
            enhanceFitness.sort(reverse=True,key=itemgetter(0))
            if Debug:
                print(enhanceFitness)
            ne = len(enhanceFitness)
            _nbrOfSwappingRetrials = self._nbrOfSwappingRetrials
            if _nbrOfSwappingRetrials >= ne:
                _nbrOfSwappingRetrials = ne
            
            sortPosition = 0
            ie = -1
            je = -1
            while enhanceFitness[sortPosition][0] >= Decimal('0') and\
                  ie not in enhanceFitness[sortPosition][1] and \
                  je not in enhanceFitness[sortPosition][1]:
##                             and    sortPosition < _nbrOfSwappingRetrials:
                newPairs = copy(pairs)
                if Debug:
                    print('sortPosition:', sortPosition)
                    print(pairs)
                ie = enhanceFitness[sortPosition][1][0]
                je = enhanceFitness[sortPosition][1][1]
                Twisted = enhanceFitness[sortPosition][2]
                if Debug:
                    print(ie,pairs[ie])
                    print(je,pairs[je])
                pair1 = pairs[ie]
                pair2 = pairs[je]
                if Twisted:
                    npair1 = [pair1[0],pair2[0]]
                    npair2 = [pair1[1],pair2[1]]
                else:
                    npair1 = [pair1[0],pair2[1]]
                    npair2 = [pair2[0],pair1[1]]
##                if Debug:
##                    print(Twisted,npair1,npair2)
##                    print(pair1,'-->>', npair1)
##                    print(pair2,'-->>', npair2)
##                    print(newPairs)
                newPairs.pop(ie)
                newPairs.insert(ie,npair1)
                newPairs.pop(je)
                newPairs.insert(je,npair2)
                if Debug:
                    print('-->>>', newPairs)
                corrA, stdDevA, groupAScores =\
                           self.computeIndividualCorrelations(newPairs)
##                if Debug:
##                    print('sortPosition:', sortPosition)
##                    print(newPairs,corrA,stdDevA)
                if corrA == Decimal('1.0'):
                    if Debug:
                        print('Current matching is fairest possible')
                        print(newPairs,corrA)
                    return newPairs,corrA,matchesVisited
                if newPairs in matchesVisited:
                    if Debug:
                        print('Cycling:', newPairs)
                    sortPosition += 1                
                elif corrA < maxCorr:
                    if Debug:
                        print('No more correlation climbing')
                        print('maxCorr: %.3f, corrA: %.3f' % (maxCorr,corrA))
                    enhanced = False
                    break
                elif corrA >= maxCorr:
                    if Debug:
                        print('Correlation climbing')
                        print('maxCorr: %.3f, corrA: %.3f' % (maxCorr,corrA))                        
                    maxCorr = corrA
                    pairs = newPairs.copy()
                    matchesVisited.append(pairs)
                    Enhanced = True
                    sortPosition += 1
                    if Debug:
                        self.showMatchingFairness(pairs)
                else:
                    Enhanced = False
                    break
            self.t += 1
##            if sortPosition < _nbrOfSwappingRetrials:
##                #history.append([npair1,npair2])
##                maxCorr = corrA
##                pairs = newPairs.copy()
##                matchesVisited.append(pairs)
##                Enhanced = True
##                t += 1
##                if Debug:
##                    self.showMatchingFairness(pairs)                    
            if self.t > self.maxIterations:
                print('!!!! Too many iterations (max=%d): %d\n' % (self.maxIterations,self.t))
                print('You may adjust the *maxIterations* parameter')
                Enhanced = False
##        nfg = []
##        for pair in newPairs:
##            nfg.append(frozenset(pair))
        if Debug:
            print('Given matching')
            self.showMatchingFairness(initialMatching)
            print('Fairness enhanced matching')
            self.showMatchingFairness(pairs,WithIndividualCorrelations=True)
            print('number of iterations:',self.t)
        return pairs,maxCorr,matchesVisited

#-----------------------

class FairnessEnhancedIntraGroupMatching(IntraGroupPairing):
    """
    Solver for computing fair IntraGroup pairings using a similar hill climbing heuristic as the
    one for the intergroup pairing problem. The enhancing is guided by Copeland ranking scores.

    *Parameters*:   
        * *intraVp* : a IntraGroup voting profile instance with *2k* voters where the *2k-1* candidates of
          each person are the other persons
        * *initialMatching* : None (default) | 'random' | 'bestCopeland' the matching from which
          the fairness enhancing algorithm is starting.
          If *None*, a right --[pi,pi+1] for i = 1..2k-1 step 3-- and a left --[pi,p-i] for i = 1..k-- initial matching will be used
          elif 'random' a random maximal matching will be used with given *seed*
          elif 'bestCopeland' the best Copeland matching will be used as initial matching

    See the :ref:`tutorial on computing fair intragroup pairings <Fair-IntraGroup-Pairings-label>`.
          
    """
    def __init__(self,intraVp=None,
                 maxIterations=None,
                 initialMatching=None,
                 _nbrOfSwappingRetrials=None,
                 #RandomInit=False,
                 seed=None,
                 Comments=True,Debug=False):
        from decimal import Decimal
        from time import time
        from copy import deepcopy
        runTimes = {}
        t0 = time()
        self.name = 'fairnessEnhanced'
        if intraVp is None:
            print('!!! Error: a voting profile of even order is required')
            return
        else:
            if intraVp.IntraGroup:
                persons = [x for x in intraVp.voters]
            else:
                print('!!! Error: the voting profile is not IntraGroup as required')
                return
            order = len(persons)
            if (order % 2) != 0:
                print('!!! Error: the group size %d is not even' % order)
                return
            self.persons = persons 
            self.order = order
            self.vpA = intraVp
            # precomputing Copeland ranking scores
            copelandScores = {}
            for i in range(order):
                pi = persons[i]
                copelandScores[pi] = {}
                for j in range(order):
                    pj = persons[j]
                    copelandScores[pi][pj] = Decimal()
            for i in range(order):
                pi = persons[i]
                for j in range(i+1,order):
                    pj = persons[j]   
                    copelandScores[pi][pj] = self.computeCopelandScore(pi,pj)
                    copelandScores[pj][pi] = self.computeCopelandScore(pj,pi)                
            self.copelandScores = copelandScores
            if Debug:
                print(copelandScores)
        if initialMatching == 'random':
            RandomInit = True
            import random
            if seed is None:
                seed = random.randint(1,99)
            random.seed(seed)
        else:
            RandomInit = False
        self.seed = seed
        if maxIterations is None:
            self.maxIterations = 2 * len(persons)
        else:
            self.maxIterations = maxIterations
        if _nbrOfSwappingRetrials is None:
            self._nbrOfSwappingRetrials = 1
        else:
            self._nbrOfSwappingRetrials = _nbrOfSwappingRetrials

        # set enhancing iterations counter t
        self.t = 0
            
        runTimes['dataInput'] = time() - t0

        te = time()
        if initialMatching is None or initialMatching == 'random':
            n = self.order
            if RandomInit:
                persons = [x for x in intraVp.voters]
                random.shuffle(persons)
            if Debug:
                print('Shauffled list of persons:',persons)
            # left hand initial matching    
            if Comments or Debug:
                print('===>>> Enhancing left initial matching')
            tleft = time()
            initialMatchingL = []
            for i in range(1,n,2):
                initialMatchingL.append( [persons[i-1],persons[i]] )
            if Comments or Debug:
                print('Initial left matching')
                print(initialMatchingL)
            corrInitialL, stdDevA, groupAScores =\
                self.computeIndividualCorrelations(initialMatchingL)
            if corrInitialL == Decimal('1'):
                if Comments or Debug:
                    print('left initial matching is fairest possible')
                self.matching = initialMatchingL
                self.maxCorr = corrInitialL
                self.iterations = 0
                self.matchesVisited = []
                runTimes['leftEnhancing'] = time() - tleft
                runTimes['rightEnhancing'] = 0
                runTimes['enhancing'] = time() - te
                #runTimes['totalTime'] = t3 - t0
                #self.runTimes = runTimes
            else:
                self.maxCorr = corrInitialL
                femL,maxCorrL,matchesVisitedL =\
                                    self.enhanceMatchingFairness(
                                            initialMatchingL,                                        
                                            Comments=Debug,
                                            Debug=Debug)
                if Comments:
                    print('Fairness enhanced left matching')
                    print(femL, ', correlation: %.3f' % maxCorrL)            
                if maxCorrL == Decimal('1'):
                    if Comments or Debug:
                        print('left enhanced matching is fairest possible')
                    self.matching = femL
                    self.maxCorr = maxCorrL
                    self.iterations = self.t
                    self.matchesVisited = matchesVisitedL
                    runTimes['leftEnhancing'] = time() - tleft
                    runTimes['rightEnhancing'] = 0
                    runTimes['enhancing'] = time() - te
                    #runTimes['totalTime'] = t3 - t0
                    #self.runTimes = runTimes
                else: 
                    # right hand initial matching
        
                    if Comments or Debug:
                        print('===>>> Enhancing right initial matching')
                    tright = time()
                    initialMatchingR = []
                    if RandomInit:
                        #persons = [x for x in intraVp.voters]
                        random.shuffle(persons)
                    for i in range(1,n,2):
                        initialMatchingR.append( [persons[i-1],persons[-i]] )
                    if Comments or Debug:
                        print('Initialright matching')
                        print(initialMatchingR)
                    
                    corrInitialR, stdDevA, groupAScores =\
                        self.computeIndividualCorrelations(initialMatchingR)
                    if corrInitialR == Decimal('1'):
                        if Comments or Debug:
                            print('right initial matching is fairest possible')
                        self.matching = initialMatchingR
                        self.maxCorr = corrInitialR
                        #self.iterations = self.t
                        #self.matchesVisited = []
                        runTimes['rightEnhancing'] = time() - tright
                        runTimes['enhancing'] = time() - te
                        #runTimes['totalTime'] = t3 - t0
                        #self.runTimes = runTimes
                        
                    else:
                        self.maxCorr = corrInitialR
                        femR,maxCorrR,matchesVisitedR =\
                                self.enhanceMatchingFairness(
                                                    initialMatchingR,
                                                    Comments=Debug,
                                                    Debug=Debug)
                        if Comments or Debug:
                            print('Fairness enhanced right matching')
                            print(femR, ', correlation: %.3f' % maxCorrR)            
                        if maxCorrR == Decimal('1'):
                            if Comments or Debug:
                                print('right enhanced matching is fairest possible')
                            self.matching = femR
                            self.maxCorr = maxCorrR
                            self.iterations = self.t
                            try:
                                self.matchesVisited |= matchesVisitedR
                            except:
                                self.matchesVisited = matchesVisitedR
                            runTimes['rightEnhancing'] = time() - tright
                            runTimes['enhancing'] = time() - te
                            #self.runTimes = runTimes

                        else:
                            # choosing the best initial matching
                            if maxCorrL >= maxCorrR:
                                if Debug:
                                    print('==>> Store left initial matching',maxCorrL)
                                    print(femL)
                                self.initialMatching = initialMatchingL
                                self.matching = femL
                                self.iterations = self.t
                                self.maxCorr = maxCorrL
                            else:
                                if Debug:
                                    print('==>> Store right initial matching',maxCorrR)
                                    print(femR)
                                self.initialMatching = initialMatchingR    
                                self.matching = femR
                                self.iterations = self.t
                                self.maxCorr = maxCorrR   
                            runTimes['rightEnhancing'] = time() - tright
                            runTimes['enhancing'] = time() -te

        else:  # given matching
            if initialMatching == 'bestCopeland':
                from pairings import BestCopelandIntraGroupMatching
                cop = BestCopelandIntraGroupMatching(self.vpA,Comments=False)
                initialMatching = cop.matching
                if Comments:
                    print('initial best Copeland matching')
            self.initialMatching = initialMatching
            if Debug:
                print('*---- Given Initial Matching ----*')
                print(persons,initialMatching)
            corrInitialCop, stdDevCop, groupScoresCop =\
                self.computeIndividualCorrelations(initialMatching)
            if corrInitialCop == Decimal('1'):
                if Comments or Debug:
                    print('Initial Copeland matching is fairest possible')
                self.matching = initialMatchingCop
                self.maxCorr = corrInitialCop
                self.iterations = 0
                self.matchesVisited = []
                runTimes['enhancing'] = time() - te
                runTimes['leftEnhancing'] = 0
                runTimes['rightEnhancing'] = 0

                #self.runTimes = runTimes
            else:
                self.t = 0
                self.maxCorr = corrInitialCop
                fecop,maxCorrecop,matchesVisitedecop =\
                                self.enhanceMatchingFairness(
                                        initialMatching,
                                        Comments=Comments,
                                        Debug=Debug)
                self.matching = fecop
                self.maxCorr = maxCorrecop
                self.iterations = self.t
                self.matchesVisited = matchesVisitedecop
                runTimes['leftEnhancing'] = 0
                runTimes['rightEnhancing'] = 0
                runTimes['enhancing'] = time() - te

##        t4 = time()
##        runTimes['totalTime'] = t4 -t0
##        self.runTimes = runTimes
        if Debug:
            print(self.initialMatching)
            print(self.matching)
            print(self.maxCorr)
            print(self.iterations)
            print(self.matchesVisited)
        # store graph data
        tg = time()
        self.vertices = deepcopy(intraVp.voters)
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        mt = []
        for m in self.matching:
            mt.append(frozenset(m))
        edges = {}
        for i in range(self.order):
            vi = verticesList[i]
            for j in range(i+1,self.order):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                if edgeKey in mt:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        
        self.edges = edges
        self.gamma = self.gammaSets()
        runTimes['storeGraph'] = time() - tg
        runTimes['totalTime'] = time() - t0
        self.runTimes = runTimes
        if Comments:
            print('===>>> Best fairness enhanced matching')
            self.showPairing()
            print('Average correlation: %+.3f' % self.maxCorr)
            print('Total run time: %.3f sec.' % self.runTimes['totalTime'] )
            
#------------
class FairestIntraGroupPairing(IntraGroupPairing):
    """
    The class computes average ordinal correlations for the complete set of maximal IntraGroup matchings
    of an een-sized set of persons and delivers, based on these correlations scores, 
    a fairest possible pairing of the persons

    *Parameters*:

       * *vpA* : any type of VotingProfile instance
       * *oderLimit* : preventing a potential CPU memory or time overflow

    See the :ref:`tutorial on computing fair intragroup pairings <Fair-IntraGroup-Pairings-label>`.
    """

    def __init__(self,vp,orderLimit=6,
                 Comments=False,Debug=False):
        from copy import deepcopy
        from decimal import Decimal
        from time import time
        
        runTimes = {}

        # check size of problem
        persons = [x for x in vp.voters]
        order = len(persons)
        if Debug:
            print('persons',persons) 
        if order > orderLimit:
            print('The size %d of the group to pair is too high' % order)
            print('The order limit is %d' % orderLimit)
            print('Use the orderLimit parameter for larger orders')
            return
        if order % 2 != 0:
            print('The size %d of the group is not even' % order)
            return
         
        # check IntraGroup voting profile version
        if not vp.IntraGroup:
            print('!!!Error: the voting profile is not an IntraGroup instance')
            return

        # data input
        t0 = time()
        #groupB = [x for x in vpA.voters]
        #if Debug:
        #    print('groupB',groupB)
        verticesKeys = [x for x in vp.voters]
##        self.candidates = vpA.voters
##        self.approvalBallot = {}
##        self.ballot = vpA.ballot
##        self.pairingPreferences = pairingPreferences
        self.name = 'IntraGroupPairing'
        self.persons = persons
        self.order = order
        self.vpA = vp
        runTimes['dataInput'] = time() - t0        
        if Comments:
            print('Run time for input data: %.4f sec.' % runTimes['dataInput'])

        # compute maximal matchings
        tmm = time()
        from graphs import CompleteGraph,LineGraph
        cg = CompleteGraph(verticesKeys=verticesKeys)
        lcg = LineGraph(cg)
        lcg.computeMIS()
        maximalMatchings = lcg.misset
        nbrOfMatchings = len(maximalMatchings)
        if Comments:
            print('Number of maximal matchings: %d' % nbrOfMatchings)
        self.nbrOfMatchings = nbrOfMatchings                    
        runTimes['maximalMatching'] = time() - tmm
        if Comments:
            print('Run time for computing the maximxal matchings: %.4f sec.' %\
                  runTimes['maximalMatching'])

        # computing matching correlations
        tmc = time()
        from statistics import mean, stdev
        from decimal import Decimal
        from digraphs import IndeterminateDigraph
        pairings = []
        groupScores = {}

        for matching in maximalMatchings:
            if Debug:
                print('matching:', matching)
            # computing groupA's scores
            groupScores = {}
            for m in persons:
                edg = IndeterminateDigraph(order=len(vp.candidates))
                edg.actions = [x for x in vp.voters]
                Min = edg.valuationdomain['min']
                Med = edg.valuationdomain['med']
                Max = edg.valuationdomain['max']

                mmatch = [x for x in matching if m in x]
                if Debug:
                    print(mmatch)
                mmatch = [x for x in mmatch[0] if x != m]
                if Debug:
                    print(mmatch)
                relation = {}
                for x in edg.actions:
                    relation[x] = {}
                    for y in edg.actions:
                        relation[x][y] = Med
                n = len(edg.actions)
                for i in range(n):
                    x = edg.actions[i]
                    for j in range(i+1,n):
                        y = edg.actions[j]
                        if x == mmatch[0]:
                            relation[x][y] = Max
                            relation[y][x] = Min
                        elif y == mmatch[0]:
                            relation[x][y] = Min
                            relation[y][x] = Max
                        else:
                            pass
                edg.relation = relation
                edg.gamma = edg.gammaSets()
                edg.notGamma = edg.notGammaSets()
                corr = edg.computeOrdinalCorrelation(vp.ballot[m])
                groupScores[m] = Decimal('%.3f' % corr['correlation'])
            
            # computing matching fitness scores
            correlations = [groupScores[w] for w in groupScores]
            avgCorr = mean(correlations)
            stdCorr = stdev(correlations)           
            if Debug:
                print(avgCorr,stdCorr)
            pairings.append((matching,avgCorr,stdCorr,
                             groupScores,-stdCorr))
        runTimes['matchingCorrelations'] = time() - tmc
        if Comments:
            print('Run time for individual correlations: %.4f sec.' %\
                  runTimes['matchingCorrelations'])

        # sorting the fitness scores
        ts = time()
        from operator import itemgetter
        pairings.sort(reverse=True,key=itemgetter(1,4))
        runTimes['sortingFitness'] = time() - ts
        if Comments:
                print('Run time for fitness ranking: %.4f sec.' %\
                      runTimes['sortingFitness'])
            
            
        #self.cg = cg
        tst = time()
        self.pairings = pairings
        self.matching = pairings[0][0]
        self.avgCorr = pairings[0][1]
        self.stdCorr = pairings[0][2]
        self.groupScores = pairings[0][3]
        self.runTimes = runTimes

        # storing the Graph data
        self.vertices = deepcopy(vp.voters)
        Min = Decimal('-1')
        Med = Decimal('0')
        Max = Decimal('1')
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        mt = []
        for m in self.matching:
            mt.append(frozenset(m))
        edges = {}
        for i in range(self.order):
            vi = verticesList[i]
            for j in range(i+1,self.order):
                vj = verticesList[j]
                edgeKey = frozenset({vi,vj})
                if edgeKey in mt:
                    edges[edgeKey] = Max
                else:
                    edges[edgeKey] = Min
        
        self.edges = edges
        self.gamma = self.gammaSets()
        runTimes['storeResults'] = time() - tst
        if Comments:
                print('Run time for storing results: %.4f sec.' %\
                      runTimes['storeResults'])


        ######
        runTimes['totalTime'] = time() - t0
        if Comments:
            print('Total run time: %.4f sec.' %\
                      runTimes['totalTime'])
        
        # showing the faires pairing
        if Comments:
            print('Fairest pairing solution')
            self.showPairing(pairings[0][0])
            print('Average correlation : %.3f' % self.avgCorr )
            print('Fairness (stdev)    : %.3f' % self.stdCorr )
        
    #------------- class methods

    def computeMatchingFairnessIndex(self,matching,Comments=False):
        """
        Renders the index position of the given matching in the
        fairness ranked self.pairings list.
        """
        # converting to the frozenset formst
        pairing = []
        for pair in matching:
            pairing.append(frozenset(pair))
        pairing = frozenset(pairing)
        n = len(self.pairings)
        for i in range(n):
            if pairing == self.pairings[i][0]:
                if Comments:
                    print('Fairness index of matching: ',i)
                break
        return i

#---------------      

class _IntraGroupCopelandMatching(IntraGroupPairing):
    """
    !!! Not a satisfactory determined perfect matching guaranteed !!!
    
    The class computes the individual Copeland ranking scores
    based maximal matching resulting from the best determined spanning forest
    of the bipartite Copeland scores graph.

    *Parameters*:

       * *vpA* : intragroup *VotingProfile* instance
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """
    def __init__(self,vpA,Comments=True,Debug=True):
        
        from time import time
        from decimal import Decimal
        from copy import deepcopy
        self.runTimes = {}
        t0 = time()
        # store input data
        self.vpA = vpA        
        self.name = 'copelandMatching'
        if vpA is None:
            print('!!! Error: a voting profile of even order is required')
            return
        else:
            if vpA.IntraGroup:
                persons = [x for x in vpA.voters]
            else:
                print('!!! Error: the voting profile is not IntraGroup as required')
                return
            order = len(persons)
            if (order % 2) != 0:
                print('!!! Error: the group size %d is not even' % order)
                return
            self.persons = persons 
            self.order = order
            self.vpA = vpA
            # precomputing Copeland ranking scores
            copelandScores = {}
            minScore = 0.0
            for i in range(order):
                pi = persons[i]
                copelandScores[pi] = {}
                for j in range(order):
                    pj = persons[j]
                    copelandScores[pi][pj] = Decimal()
            for i in range(order):
                pi = persons[i]
                for j in range(i+1,order):
                    pj = persons[j]   
                    copelandScores[pi][pj] = self.computeCopelandScore(pi,pj)
                    copelandScores[pj][pi] = self.computeCopelandScore(pj,pi)
                    score = copelandScores[pi][pj] + copelandScores[pj][pi]
                    if Debug:
                        print(score)
                    if score < minScore:
                        minScore = score
                        
            self.copelandScores = copelandScores
            if Debug:
                print(copelandScores)
                print('minScore:', minScore)
        t1 = time()
        self.runTimes['dataInput'] = t1 - t0

        #storing the Graph data
        t2 = time()
        self.vertices = vpA.voters
        Min = Decimal('%d' % (2*minScore) )
        Med = Decimal('0')
        Max = Decimal('%d' % (2*abs(minScore)) )
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset([vi,vj])
                edges[edgeKey] = abs(minScore) + copelandScores[vi][vj] \
                            + copelandScores[vj][vi]
         
##        for i in range(order):
##            for j in range(order):
##                edgeKey = frozenset([aKeys[i],bKeys[j]])
##                edges[edgeKey] = self.copelandScores[aKeys[i]][bKeys[j]] \
##                            + self.copelandScores[bKeys[j]][aKeys[i]]            
        self.edges = edges
        self.gamma = self.gammaSets()
        self.edges = edges
        if Debug:
            dself = self.graph2Digraph()
            dself.showRelationTable(ndigits=0)
        t3 = time()
        self.runTimes['copelandGraph'] = t3 - t2
        
        # computing the best determined maximal matching
        t4 = time()
        from graphs import BestDeterminedSpanningForest
        bsf = BestDeterminedSpanningForest(self)
        if Debug:
            bsf.exportGraphViz(WithSpanningTree=True,layout='circo')
            dbsf = bsf.graph2Digraph()
            dbsf.showRelationTable(ndigits=0)
        matching = []
        unPaired = []
        gamma = bsf.gamma
        sortedVerticesList = [(len(gamma[v]),v) for v in self.vertices]
        sortedVerticesList.sort()
        verticesList = [v[1] for v in sortedVerticesList]
        if Debug:
            print(verticesList)
                        
        while len(verticesList) > 0:
            sortedVerticesList = [(len(gamma[v]),v) for v in verticesList]
            sortedVerticesList.sort()
            verticesList = [v[1] for v in sortedVerticesList]
            for v1 in verticesList:
                if Debug:
                    print('==>>v1', v1, gamma[v1])
                if len(gamma[v1]) == 1:
                    v2 = gamma[v1].pop()
                    if [v1,v2] not in matching and [v2,v1] not in matching:
                        matching.append(frozenset({v1,v2}))
                        if Debug:
                            print(matching)
                        verticesList.remove(v1)
                        verticesList.remove(v2)
                        gamma[v2] = set()
                        if Debug:
                            print(v1,gamma[v1],v2,gamma[v2])
                    for v3 in verticesList:
                        if Debug:
                            print('v3',v3,gamma[v3])
                        if v1 in gamma[v3]:
                            gamma[v3].remove(v1)
                        if v2 in gamma[v3]:
                            gamma[v3].remove(v2)
                        if Debug:
                            print('v3',v3,gamma[v3])
                elif len(gamma[v1]) == 0:
                    verticesList.remove(v1)
                    unPaired.append(v1)
        if Comments:
            print(len(matching),matching)
            print('==>> unpaired:', unPaired)
        if len(matching) < order:
            #aKeys = [a for a in self.vpA.voters]
            #bKeys = [b for b in self.vpB.voters]
            remaining = [v for v in self.vertices]
            for m in matching:
                lm = list(m)
                lm.sort()
                remaining.remove(lm[0])
                remaining.remove(lm[1])
            if Debug:
                print(remaining)
            pairs = []
            edges = self.edges
            na = len(remaining)
            for i in range(na):
                for j in range(i+1,na):
                    edgeKey = frozenset({remaining[i],remaining[j]})
                    pairs.append((edges[edgeKey],edgeKey))
            pairs.sort(reverse=True)
            if Debug:
                print(pairs)
            lmatching = [m for m in matching]
            i = 0
            while na > 0:
                keys = list(pairs[i][1])
                if Debug:
                    print(keys)
                if keys[0] in remaining and keys[1] in remaining:
                    remaining.remove(keys[0])
                    remaining.remove(keys[1])
                    lmatching.append(pairs[i][1])
                    na -= 2
                    i += 1
                else:
                    i += 1
            matching = lmatching
            if Debug:
                print(len(matching),matching)

        
        self.matching = matching
        t5 = time()
        self.runTimes['maximalMatching'] = t5 - t4
        
        t7 = time()
        self.runTimes['totalTime'] = t7 - t0

#------------

class BestCopelandIntraGroupMatching(IntraGroupPairing):
    """
    The class computes the individual Copeland ranking scores and
    construct the best determined perfect matching with a ranked pairs rule
    from the reciprocal Copeland ranking scores graph 

    *Parameters*:

       * *vpA* : intragroup *VotingProfile* instance
       
    See the :ref:`tutorial on computing fair intergroup pairings <Fair-InterGroup-Pairings-label>`.
    """
    def __init__(self,vpA,Comments=False,Debug=False):
        
        from time import time
        from decimal import Decimal
        from copy import deepcopy
        self.runTimes = {}
        t0 = time()
        # store input data
        self.vpA = vpA        
        self.name = 'copelandMatching'
        if vpA is None:
            print('!!! Error: a voting profile of even order is required')
            return
        else:
            if vpA.IntraGroup:
                persons = [x for x in vpA.voters]
            else:
                print('!!! Error: the voting profile is not IntraGroup as required')
                return
        order = len(persons)
        if (order % 2) != 0:
            print('!!! Error: the group size %d is not even' % order)
            return
        self.persons = persons 
        self.order = order
        self.vpA = vpA
        # precomputing Copeland ranking scores
        copelandScores = {}
        minScore = 0.0
        for i in range(order):
            pi = persons[i]
            copelandScores[pi] = {}
            for j in range(order):
                pj = persons[j]
                copelandScores[pi][pj] = Decimal()
        for i in range(order):
            pi = persons[i]
            for j in range(i+1,order):
                pj = persons[j]   
                copelandScores[pi][pj] = self.computeCopelandScore(pi,pj)
                copelandScores[pj][pi] = self.computeCopelandScore(pj,pi)
                score = copelandScores[pi][pj] + copelandScores[pj][pi]
                if Debug:
                    print(score)
                if score < minScore:
                    minScore = score
                    
        self.copelandScores = copelandScores
        if Debug:
            print(copelandScores)
            print('minScore:', minScore)
        t1 = time()
        self.runTimes['dataInput'] = t1 - t0

        #storing the Graph data
        t2 = time()
        self.vertices = vpA.voters
        Min = Decimal('%d' % (2*minScore) )
        Med = Decimal('0')
        Max = Decimal('%d' % (2*abs(minScore)) )
        self.valuationDomain = {'min': Min,
                                'med': Med,
                                'max': Max}
        verticesList = [v for v in self.vertices]
        n = len(verticesList)
        edges = {}
        for i in range(n):
            vi = verticesList[i]
            for j in range(i+1,n):
                vj = verticesList[j]
                edgeKey = frozenset([vi,vj])
                edges[edgeKey] = abs(minScore) + copelandScores[vi][vj] \
                            + copelandScores[vj][vi]
        self.edges = edges
        self.gamma = self.gammaSets()
        if Debug:
            dself = self.graph2Digraph()
            dself.showRelationTable(ndigits=0)
        t3 = time()
        self.runTimes['CopelandGraph'] = t3 - t2
        
        # computing the best determined maximal matching
        t4 = time()
        remaining = [v for v in self.vertices]
        if Debug:
            print(remaining)
        pairs = []
        edges = self.edges
        na = len(remaining)
        for i in range(na):
            for j in range(i+1,na):
                edgeKey = frozenset({remaining[i],remaining[j]})
                pairs.append((edges[edgeKey],edgeKey))
        pairs.sort(reverse=True)
        if Debug:
            print(pairs)
        lmatching = []
        i = 0
        while na > 0:
            keys = list(pairs[i][1])
            if Debug:
                print(keys)
            if keys[0] in remaining and keys[1] in remaining:
                remaining.remove(keys[0])
                remaining.remove(keys[1])
                lmatching.append(pairs[i][1])
                na -= 2
                i += 1
            else:
                i += 1
        if Debug:
            print(len(lmatching),lmatching)

        
        self.matching = lmatching
        t5 = time()
        self.runTimes['maximalMatching'] = t5 - t4
        
        t7 = time()
        self.runTimes['totalTime'] = t7 - t0


#----------test pairings class ----------------
if __name__ == "__main__":
    #from transitiveDigraphs import *

    print('****************************************************')
    print('* Python pairings module                           *')
    print('* $Revision: Python3.13 $                          *')
    print('* Copyright (C) 2023-2025 Raymond Bisdorff         *')
    print('* The module comes with ABSOLUTELY NO WARRANTY     *')
    print('* to the extent permitted by the applicable law.   *')
    print('* This is free software, and you are welcome to    *')
    print('* redistribute it if remains free software.        *')
    print('****************************************************')

    print('*-------- Testing classes and methods -------')

    from time import time
    from votingProfiles import *
##            RandomLinearVotingProfile,\
##            RandomBipolarApprovalVotingProfile,RandomVotingProfile
    from random import randint
    seed1 = randint(0,99)
    seed2 = randint(100,199)
##    seed1 = 1
##    seed2 = 1616
    order = 10
    Comments = True
    Debug = False

    # intragroup experiments
    vpG = RandomLinearVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='p',
                                    IntraGroup=True,
                                    #candidatesIdPrefix='b',
##                                             approvalProbability=0.2,
##                                             disapprovalProbability=0.2,
                                             seed=seed1,Debug=False)
##    vpG.showBipolarApprovals()
##    t0 = time()
    fp = FairestIntraGroupPairing(vpG,Comments=True,Debug=False,orderLimit=order)
##    t1 =time()
##    #print('fp total run time: %.3f sec.' % (t1-t0))
##
##    cop = BestCopelandIntraGroupMatching(vpG,Comments=False,Debug=False)
##    ecop = FairnessEnhancedIntraGroupMatching(vpG,initialMatching='bestCopeland',
##                                              Comments=True,Debug=False)
##    fegm = FairnessEnhancedIntraGroupMatching(vpG,initialMatching=fp.pairings[0][0],
##                                              Comments=True,Debug=False)
    fem = FairnessEnhancedIntraGroupMatching(vpG,initialMatching='bestCopeland',
                                              Comments=True,Debug=False)
##    
##    print('==>> Copeland')
##    cop.showMatchingFairness(WithIndividualCorrelations=True)
##    print(cop.runTimes)
##    print('==>> Fairness enhanced')
##    fem.showMatchingFairness(WithIndividualCorrelations=True)
##    print(fem.runTimes)
##    print('==>> Copeland enhanced')
##    ecop.showMatchingFairness(WithIndividualCorrelations=True)
##    print(ecop.runTimes)
##    print('==>> Fairest')
##    fp.showMatchingFairness(WithIndividualCorrelations=True)
##    print(fp.runTimes)

    #intergroup experiments
##    lvA = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
##                                    numberOfCandidates=order,
##                                    votersIdPrefix='a',
##                                             #IntraGroup=True,
##                                    candidatesIdPrefix='b',
##                                             approvalProbability=0.3,
##                                             disapprovalProbability=0.3,
##                                             seed=seed1,Debug=False)
##    lvB = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
##                                    numberOfCandidates=order,
##                                    votersIdPrefix='b',
##                                    #IntraGroup=False,
##                                    candidatesIdPrefix='a',
##                                             approvalProbability=0.3,
##                                             disapprovalProbability=0.3,
##                                             seed=seed2,Debug=False)
####    lvA = RandomLinearVotingProfile(numberOfVoters=order,
##                                    numberOfCandidates=order,
##                                    votersIdPrefix='a',
##                                    candidatesIdPrefix='b',
##                                    PartialLinearBallots=False,
##                                    lengthProbability=0.3,
##                                    seed=seed1)
##    lvB = RandomLinearVotingProfile(numberOfVoters=order,
##                                    numberOfCandidates=order,
##                                    votersIdPrefix='b',
##                                    candidatesIdPrefix='a',
##                                    PartialLinearBallots=False,
##                                    lengthProbability=0.3,
##                                    seed=seed2)
##    t0 = time()
##    fp = FairestInterGroupPairing(lvA,lvB,Comments=True,Debug=False,orderLimit=order)
##    t1 =time()
##    print('fp total run time: %.3f sec.' % (t1-t0))
##
##    igcg = BestCopelandInterGroupMatching(lvA,lvB,Comments=True,Debug=True)
##    print('==>> Copeland')
##    igcg.showMatchingFairness(WithIndividualCorrelations=True)
##    print(igcg.runTimes)
####    print('==>> Fairest')
####    fp.showMatchingFairness(WithIndividualCorrelations=True)
##
##    print('==>> Fairness random enhanced')    
##    fem1 = FairnessEnhancedInterGroupMatching(lvA,lvB,
##                                #initialMatching=fp.pairings[10][0],
##                                initialMatching = 'random',
##                                seed=1,
##                                Comments=True,
##                                Debug=False)
##    fem1.showMatchingFairness(WithIndividualCorrelations=True)
##    
##    print(fem1.runTimes)
##
##    print('==>> Fairness enhanced')
##    fem2 = FairnessEnhancedInterGroupMatching(lvA,lvB,
##                                initialMatching = fem1.matching,
##                                seed=1,
##                                Comments=True,
##                                Debug=True)
##    fem2.showMatchingFairness(WithIndividualCorrelations=True)
##    print(fem2.runTimes)

##    print('==>> Fairest matching')
##
##    fp.showMatchingFairness(WithIndividualCorrelations=True)
##    print(fp.runTimes)

    print('seed1:',seed1, 'seed2:', seed2)

####    vpB.showBipolarApprovals()
##    order = 6
##    seed = 0.7525016431335723
##    seed = None
##    rigvp = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
##                                               votersIdPrefix='p',
##                                               seed=seed,
##                                               IntraGroup=True,Debug=False)
##    
##    
##    t2 = time()
##    fgm = FairnessEnhancedIntraGroupMatching(vpG,
##                                             seed=seed1,
##                                             initialMatching='random,
##                                             #maxIterations=20,
##                                             Comments=True,Debug=True)
##    t3 = time()
##    print('fgm total run time: %.3f sec.' % (t3-t2))
##    fgm.showMatchingFairness(WithIndividualCorrelations=True)
##    fp.showMatchingFairness(WithIndividualCorrelations=True)
    


##    lvA = BipolarApprovalVotingProfile('debug')
##    lvA.IntraGroup = True
##    lvA.seed = 1
##    k = 4
##    
##    if Comments:
##        lvA.showBipolarApprovals()
##    fp = FairestIntraGroupPairing(lvA,orderLimit=k,Comments=Comments)
##    if Comments:
##        fp.showMatchingFairness(fp.matching)
##    #matchingIndex = random.randint(10,20)
##    em = FairnessEnhancedIntraGroupMatching(lvA,
##                        initialMatching=None,
##                        maxIterations=2*k,
##                        Comments=Comments,Debug=False)
##    corropt, stdopt, groupOptScores = fp.computeIndividualCorrelations(fp.matching,Debug=True)
##    lvA.showBipolarApprovals()
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. January 2023-202             *')
    print('* Version: Python3.13               *')
    print('*************************************')

