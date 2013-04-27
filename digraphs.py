#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python3+ implementation of digraphs
# Based on Python 2 $Revision: 1.697 $
# Copyright (C) 2006-2013  Raymond Bisdorff
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

#--------- Decimal precision --------------
from decimal import Decimal

#---------- general methods -----------------
# generate all permutations from a string or a list
# From Michael Davies's recipe:
# http://snippets.dzone.com/posts/show/753
def all_perms(str):
    if len(str) <=1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]

# generate all subsets of a given set E
# Discrete Mathematics BINFO 1 course Lesson 2-sets
# RB October 2009 (recursive version)
def powerset(S):
    """
    Power set generator iterator.

    Parameter S may be any object that is accepted as input by the set class constructor.

    """
    E = set(S)
    if len(E) == 0:
        yield set()
    else:
        e = E.pop()
        for X in powerset(E):
            yield set([e]) | X
            yield X

#----------XML handling class -----------------
try:
    from xml.sax import *
except:
    print('XML extension will not work with this Python version!')

class _XMLDigraphHandler(ContentHandler):
    """
    A private handler to deal with digraphs stored in XML format.
    """

    inName = 0
    digraphName = ''
    inAction = 0
    actionName = ''
    actions = []
    iAction = ''
    tAction = ''
    inMin = 0
    minText = ''
    inMax = 0
    maxText = ''
    inValue = 0
    valueText = ''
    valuationdomain = {}
    relation = {}


    def startElement(self,nodeName,attrs):
        if nodeName == 'digraph':
            self.category = attrs.get("category", "")
            self.subcategory = attrs.get("subcategory", "")

        if nodeName == 'name':
            self.inName = 1

        if nodeName == 'nodes':
            self.actions = []

        if nodeName == 'node':
            self.actionName = ''
            self.inAction = 1

        if nodeName == 'min':
            self.inMin = 1

        if nodeName == 'max':
            self.inMax = 1

        if nodeName == 'relation':
            self.relation = {}
            for x in self.actions:
                self.relation[x] = {}

        if nodeName == 'i':
            self.actionName = ''
            self.inAction = 1

        if nodeName == 't':
            self.actionName = ''
            self.inAction = 1

        if nodeName == 'v':
            self.valueText = ''
            self.inValue = 1


    def endElement(self,nodeName):

        if nodeName == 'name':
            self.inName = 0
            self.name = str(self.digraphName)

        if nodeName == 'node':
            self.actions.append(str(self.actionName))
            self.inAction = 0

        if nodeName == 'min':
            self.inMin = 0
            self.valuationdomain['min'] = eval(self.minText)

        if nodeName == 'max':
            self.inMax = 0
            self.valuationdomain['max'] = eval(self.maxText)

        if nodeName == 'i':
            self.inAction = 0
            self.iAction = str(self.actionName)

        if nodeName == 't':
            self.inAction = 0
            self.tAction = str(self.actionName)

        if nodeName == 'v':
            self.inValue = 0

        if nodeName == 'arc':
            self.relation[self.iAction][self.tAction] = eval(self.valueText)

    def characters(self, ch):
        if self.inName:
            self.digraphName += ch
        if self.inAction:
            self.actionName += ch
        if self.inMin:
            self.minText += ch
        if self.inMax:
            self.maxText += ch
        if self.inValue:
            self.valueText += ch


#----------Digraph classes -----------------

class Digraph(object):
    """
    General class of digraphs, R.B. March 2006:

    Python data file format:
       * actionset = ['1','2','3','4','5']
       * valuationdomain = { 'min':0, 'med':1, 'max': 2}
       * relation = { '1': { '1':0, '2': 2, ...}, ...}

    Example python (>= 2.4 required) session::
       >>> from digraphs import Digraph
       >>> g = Digraph('tempdigraph')
       >>> g.showShort()
       *----- show short --------------*
       Digraph          : tempdigraph
       Actions          : ['1', '2', '3']
       Valuation domain : {'med': Decimal("0.5"), 'max': Decimal("1.0"), 'min': Decimal("0")}
       *--- Connected Components ---*
       1: ['1', '2', '3']

    """
    def __init__(self,file=None,order=7):
        import digraphs,sys,copy
        if file == None:
            g = digraphs.RandomValuationDigraph(order=order)
            self.name = g.name
            self.actions = copy.deepcopy(g.actions)
            self.order = len(self.actions)
            self.valuationdomain = copy.deepcopy(g.valuationdomain)
            self.convertValuationToDecimal()
            self.relation = copy.deepcopy(g.relation)
            self.convertRelationToDecimal()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        else:
            fileName = file+'.py'
            exec(compile(open(fileName).read(), fileName, 'exec'))
            self.name = file
            self.actions = locals()['actionset']
            self.order = len(self.actions)
            self.valuationdomain = locals()['valuationdomain']
            self.convertValuationToDecimal()
            self.relation = locals()['relation']
            self.convertRelationToDecimal()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        try:
            self.reflections = locals()['reflections']
            self.rotations = locals()['rotations']
        except:
            pass

    def __neg__(self):
        """
        Make the negation operator -self available for Digraph instances. Returns a DualDigraph instance of self.
        """
        new = DualDigraph(self)
        new.__class__ = self.__class__
        return new

    def __invert__(self):
        """
        Make the inverting operator ~self available for Digraph instances. Returns a ConverseDigraph instance of self.
        """
        new = ConverseDigraph(self)
        new.__class__ = self.__class__
        return new

    def digraph2Graph(self,valuationDomain={'min':-1,'med':0,'max':1},Debug=False,conjunctiveConversion=True):
        """
        Convert a Digraph instance to a Graph instance.
        """
        from graphs import Graph
        from copy import deepcopy
        g = Graph()
        g.name = deepcopy(self.name)
        g.vertices = deepcopy(self.actions)
        g.valuationDomain = valuationDomain
        gMin = valuationDomain['min']
        gMed = valuationDomain['med']
        gMax = valuationDomain['max']
        order = len(g.vertices)
        g.edges = {}
        verticesKeys = [x for x in g.vertices]
        dgMed = self.valuationdomain['med']
        for i in range(order):
            for j in range(i+1,order):
                x = verticesKeys[i]
                y = verticesKeys[j]
                vertex = frozenset([x,y])
                if conjunctiveConversion:
                    edgeValue = min(self.relation[x][y],self.relation[y][x])
                else:
                    edgeValue = max(self.relation[x][y],self.relation[y][x])
                if edgeValue > dgMed:
                    g.edges[vertex] = gMax
                elif edgeValue < dgMed:
                    g.edges[vertex] = gMin
                else:
                    g.edges[vertex] = gMed
                if Debug:
                    print('x,y,self.relation[x][y],self.relation[y][x],vertex,g.edges[vertex]', x,y,self.relation[x][y],self.relation[y][x],vertex,g.edges[vertex])
        g.gamma = g.gammaSets()
        return g


    def computeRelationalStructure(self,Debug=False):
        """
        Renders the counted decomposition of the valued relations into
        the following type of links:
        gt '>', eq '=', lt '<', incomp '<>',
        leq '<=', geq '>=', indeterm '?'
        """
        counts = {'>':0,'=':0,'<':0,'<>':0,'<=':0,'>=':0,'?':0}
        actions = [x for x in self.actions]
        n = len(actions)
        relation = self.relation
        for x in actions:
            for y in actions:
                if Debug:
                    print(x,y, relation[x][y],relation[y][x], end=' ')
                if x != y:
                    if relation[x][y] > self.valuationdomain['med']:
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['='] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['>'] += 1
                        else:
                            counts['>='] += 1
                    elif relation[x][y] < self.valuationdomain['med']:
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['<'] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['<>'] += 1
                        else:
                            counts['<='] += 1
                    else:  # relation[y][x] == self.valuationdomain['med']
                        if relation[y][x] > self.valuationdomain['med']:
                            counts['<='] += 1
                        elif relation[y][x] < self.valuationdomain['med']:
                            counts['>='] += 1
                        else:
                            counts['?'] += 1
                if Debug:
                    print(counts)
        nd = Decimal(str(n))
        if nd != Decimal('0'):
            counts['<'] = Decimal(str(counts['<']))/(nd*(nd-1))
            counts['<='] = Decimal(str(counts['<=']))/(nd*(nd-1))
            counts['>'] = Decimal(str(counts['>']))/(nd*(nd-1))
            counts['>='] = Decimal(str(counts['>=']))/(nd*(nd-1))
            counts['<>'] = Decimal(str(counts['<>']))/(nd*(nd-1))
            counts['='] = Decimal(str(counts['=']))/(nd*(nd-1))
            counts['?'] = Decimal(str(counts['?']))/(nd*(nd-1))
        return counts


    def computeRankingByChoosing(self,Debug=False,CoDual=False):
        """
        Computes a weak preordring of the self.actions by iterating
        jointly best and worst choice elagations.

        Stores in self.rankingByChoosing['result'] a list of ((P+,bestChoice),(P-,worstChoice)) pairs
        where P+ (resp. P-) gives the best (resp. worst) choice complement outranking
        (resp. outranked) average valuation via the computePairwiseClusterComparison
        method.

        If self.rankingByChoosing['CoDual'] is True, the ranking by chossing was computed on the codual of self.
        """
        from copy import deepcopy
        currG = deepcopy(self)
        remainingActions = [x for x in self.actions]
        rankingByChoosing = []
        bestChoice = (None,None)
        worstChoice = (None,None)
        i = 0
        while len(remainingActions) > 2 and (bestChoice[1] != [] or worstChoice[1] != []):
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = deepcopy(currG)
            currGcd.computeRubisChoice(Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))
            #bestChoiceCandidates.sort(reverse=True)
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: str(choice[1]) ) # lexigr choices
            bestChoiceCandidates = sorted(bestChoiceCandidates, key=lambda choice: -choice[0]) # sort by outranking power
            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                #print 'Error: no best choice in currGcd!'
                #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)

            #currGcd.computeBadChoices(Comments=Debug)
            worstChoiceCandidates = []
            j = 0
            for ch in currGcd.badChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranked = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('worst', j, ch[5], k1, k1Outranked)
                    worstChoiceCandidates.append( ( min(-k1Outranked['P+'],k1Outranked['P-']), k1 ) )
                else:
                    worstChoiceCandidates.append((self.valuationdomain['max'],k1))
            worstChoiceCandidates.sort(reverse=True)
            try:
                worstChoice = worstChoiceCandidates[0]
            except:
                #print 'Error: no worst choice in currGcd'
                #currGcd.save('currGcd_errorWorst')
                worstChoice=(self.valuationdomain['med'],[])
            if Debug:
                print('worstChoice', i, worstChoice, worstChoiceCandidates)

            if (bestChoice[1] != [] or worstChoice[1] != []):
                rankingByChoosing.append((bestChoice,worstChoice))

            if len(bestChoice[1]) > 0:
                for x in bestChoice[1]:
                    remainingActions.remove(x)
            if len(worstChoice[1]) > 0:
                for x in worstChoice[1]:
                    try:
                        remainingActions.remove(x)
                    except:
                        pass
            #print i, bestChoice, worstChoice, remainingActions, rankingByChoosing
        if (bestChoice[1] == [] and worstChoice[1] == []):
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(bestChoice,worstChoice)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByChoosing.append((bestChoice,worstChoice))
            if Debug:
                print(rankingByChoosing)
        elif len(remainingActions) == 2:
            i += 1
            currG.actions = remainingActions
            if CoDual:
                currGcd = CoDualDigraph(currG)
            else:
                currGcd = deepcopy(currG)
            currGcd.computeRubisChoice(Comments=Debug)
            #currGcd.computeGoodChoices(Comments=Debug)
            bestChoiceCandidates = []
            j = 0
            for ch in currGcd.goodChoices:
                k1 = currGcd.flatChoice(ch[5])
                if Debug:
                    print(ch[5],k1)
                ck1 = list(set(currG.actions)-set(k1))
                if len(ck1) > 0:
                    j += 1
                    k1Outranking = currG.computePairwiseClusterComparison(k1,ck1)
                    if Debug:
                        print('good', j, ch[5], k1, k1Outranking)
                    #bestChoiceCandidates.append((k1Outranking['P+'],k1))
                    bestChoiceCandidates.append( ( min(k1Outranking['P+'],-k1Outranking['P-']), k1 ) )
                else:
                    bestChoiceCandidates.append((self.valuationdomain['max'],k1))
            bestChoiceCandidates.sort(reverse=True)
            try:
                bestChoice = bestChoiceCandidates[0]
            except:
                #print 'Error: no best choice in currGcd!'
                #currGcd.save('currGcd_errorBest')
                bestChoice = (self.valuationdomain['med'],[])
            if Debug:
                print('bestChoice', i, bestChoice, bestChoiceCandidates)
            ## ### unique worst choice left
            k1 = list(set(currG.actions)-set(bestChoice[1]))
            if Debug:
                print('singleton worst choice left',k1)
            if len(k1) > 0:
                ck1 = list(set(currG.actions)-set(k1))
                k1Outranked = currG.computePairwiseClusterComparison(k1,ck1)
                worstChoice = ( min(-k1Outranked['P+'],k1Outranked['P-']), k1 )
            else:
                worstChoice = (self.valuationdomain['max'],bestChoice[1])
            if Debug:
                print('worstChoice', i, worstChoice)
            rankingByChoosing.append((bestChoice,worstChoice))

        elif len(remainingActions) == 1:
            #### only a singleton choice or a failure quadruple left to rank
            if Debug:
                print(bestChoice,worstChoice)
            bestChoice = (self.valuationdomain['max'],remainingActions)
            worstChoice = (self.valuationdomain['max'],remainingActions)
            rankingByChoosing.append((bestChoice,worstChoice))
            if Debug:
                print(rankingByChoosing)
        self.rankingByChoosing = {'CoDual': CoDual, 'result': rankingByChoosing}
        return {'CoDual': CoDual, 'result': rankingByChoosing}

    def iterateRankingByChoosing(self,Odd=False,CoDual=False,Comments=True,Debug=False):
        """
        Renders a ranking by choosing result when progressively eliminating
        all chordless (odd only) circuits with rising valuation cut levels.
        """
        from copy import deepcopy
        from time import time
        if Debug:
            Comments=True
        gcd = deepcopy(self)

        qualmaj0 = gcd.valuationdomain['min']
        if Comments:
            print('Ranking by choosing and rejecting after progressive cut elimination of chordless (odd = %s) circuits' % (str(Odd)) )
            print('Initial determinateness of the outranking relation: %.3f' % self.computeDeterminateness())
            i = 0
        qualmaj = gcd.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments)
        self.rankingByChoosing = None
        while qualmaj > qualmaj0:
            if Comments:
                i += 1
                print('--> Iteration %d' % (i))
                t0 = time()
            if qualmaj < gcd.valuationdomain['max']:
                pg = PolarisedDigraph(gcd,qualmaj,StrictCut=True)
            else:
                pg = PolarisedDigraph(gcd,qualmaj,StrictCut=False)
            if Comments:
                print('Polarised determinateness = %.3f' % pg.computeDeterminateness())
            if qualmaj > gcd.valuationdomain['med']:
                self.rankingByChoosing = pg.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
                self.rankingByChoosing['PolarizationLevel'] = qualmaj
            elif i==1:
                self.rankingByChoosing = pg.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
                self.rankingByChoosing['PolarizationLevel'] = qualmaj
            if Comments:
                self.showRankingByChoosing()
                print('Execution time:', time()-t0, 'sec.')
                ## pgRankingByChoosingRelation = self.computeRankingByChoosingRelation()
                ## corr = self.computeOrdinalCorrelation(pgRankingByChoosingRelation)
                ## print 'Ordinal (Kendall) correlation with outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination'])
                ## corr = self.computeOrdinalCorrelation(pgRankingByChoosingRelation,MedianCut=True,Debug=Debug)
                ## print 'Ordinal (Kendall) correlation with median cut outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination'])
            qualmaj0 = qualmaj
            qualmaj = pg.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
        
        return self.rankingByChoosing

    def computePrudentBestChoiceRecommendation(self,CoDual=False,Comments=False,Debug=False):
        """
        Renders the best choice recommendation after eliminating
        all odd chordless circuits with a minimal cut of the valuation.
        """
        from copy import deepcopy
        self.rankingByChoosing = self.iterateRankingByChoosing(CoDual=CoDual,Comments=Comments,Debug=Debug)
        if Comments:
            self.showRankingByChoosing()
        try:
            self.rankingByChoosing['result'][0][0][1].sort()
            return self.rankingByChoosing['result'][0][0][1]
        except:
            print("Error: no ranking by choosing result !!")
            return None

    def computePreorderRelation(self,preorder,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        a given preordering (list of lists) result.
        """

        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        actions = list(self.actions.keys())
        currentActions = set(actions)
        preorderRelation = {}
        for x in actions:
            preorderRelation[x] = {}
            for y in actions:
                preorderRelation[x][y] = Med

        for eqcl in preorder:
            currRest = currentActions - set(eqcl)
            if Debug:
                print(currentActions, eqcl, currRest)
            for x in eqcl:
                for y in eqcl:
                    if x != y:
                        preorderRelation[x][y] = Max
                        preorderRelation[y][x] = Max

            for x in eqcl:
                for y in currRest:
                    preorderRelation[x][y] = Max
                    preorderRelation[y][x] = Min
            currentActions = currentActions - set(eqcl)
        return preorderRelation

    def computeRankingByChoosingRelation(self,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        the self.rankingByChoosing result.
        """
        try:
            rankingByChoosing = self.rankingByChoosing['result']
        except:
            print('Error: first run computeRankingByChoosing(CoDual=T/F) !')
            return None

        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        actions = [x for x in self.actions]
        currActions = set(actions)
        rankingRelation = {}
        for x in actions:
            rankingRelation[x] = {}
            for y in actions:
                rankingRelation[x][y] = Med
        n = len(rankingByChoosing)
        for i in range(n):
            ibch = set(rankingByChoosing[i][0][1])
            iwch = set(rankingByChoosing[i][1][1])
            ribch = set(currActions) - ibch
            for x in ibch:
                for y in ibch:
                    if x != y:
                        rankingRelation[x][y] = self.omax([rankingRelation[x][y],Max])
                        rankingRelation[y][x] = self.omax([rankingRelation[x][y],Max])
                for y in ribch:
                    rankingRelation[x][y] = self.omax([rankingRelation[x][y],Max])
                    rankingRelation[y][x] = self.omax([rankingRelation[y][x],Min])
            riwch = set(currActions) - iwch
            for y in iwch:
                for x in iwch:
                    if x != y:
                        rankingRelation[x][y] = self.omax([rankingRelation[x][y],Max])
                        rankingRelation[y][x] = self.omax([rankingRelation[y][x],Max])
                for x in riwch:
                    rankingRelation[x][y] = self.omax([rankingRelation[x][y],Max])
                    rankingRelation[y][x] = self.omax([rankingRelation[y][x],Min])
            currActions = currActions - (ibch | iwch)
        return rankingRelation

    def showRankingByChoosing(self):
        """
        A show method for self.rankinByChoosing result.

        .. warning::

             The self.computeRankingByChoosing(CoDual=False/True) method instantiating the self.rankingByChoosing slot is pre-required !
        """
        try:
            rankingByChoosing = self.rankingByChoosing['result']
        except:
            print('Error: You must first run self.computeRankingByChoosing(CoDual=True(default)|False) !')
            #rankingByChoosing = self.computeRankingByChoosing(Debug,CoDual)
            return
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
            print(' %s%s%s Best Choice %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
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
            print(' %s%s%s Worst Choice %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))
        if self.rankingByChoosing['CoDual']:
            corr1 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation())
            print('Ordinal bipolar correlation with codual (strict) outranking relation: %.3f (%.1f%%)' % (corr1['correlation'],corr1['determination']*Decimal('100')))
            corr2 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation(),MedianCut=True)
            print('Ordinal bipolar correlation with codual (strict) median cut outranking relation: %.3f (%.1f%%)' % (corr2['correlation'],corr2['determination']*Decimal('100')))

        else:
            corr1 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation())
            print('Ordinal bipolar correlation with outranking relation: %.3f (%.1f%%)'% (corr1['correlation'],corr1['determination']*Decimal('100')))
            corr2 = self.computeBipolarCorrelation(self.computeRankingByChoosingRelation(),MedianCut=True)
            print('Ordinal bipolar correlation with median cut outranking relation: %.3f (%.1f%%)'% (corr2['correlation'],corr2['determination']*Decimal('100')))

    def computeValuationStatistics(self,Sampling=False,Comments=False):
        """
        Renders the mean and variance of the valuation
        of the non reflexive pairs.
        """
        from math import sqrt
        mean = Decimal('0.0')
        squares = Decimal('0.0')
        actions = [x for x in self.actions]
        n = len(actions)
        n2 = n * (n-1)
        n2d = Decimal(str(n2))
        relation = self.relation
        for x in actions:
            for y in actions:
                if x != y:
                    mean += relation[x][y]
                    squares += relation[x][y]*relation[x][y]
        mean = mean / n2d
        if Sampling:
            var = ( squares / (n2d-Decimal('1')) ) - (mean * mean)
        else:
            var = squares / n2d - (mean * mean)
        stdDev = sqrt(var)
        if Comments:
            print('mean: %.5f, std. dev.: %.5f' % (mean,stdDev))
        return mean,stdDev


    def computeBipolarCorrelation(self, other, MedianCut=False, Debug=False):
        """
        Renders the bipolar correlation K of a
        self.relation when compared
        with a given compatible (same actions set)) digraph or
        a [-1,1] valued compatible relation (same actions set).

        If MedianCut=True, the correlation is computed on the median polarized relations.

        K = sum_{x != y} [ min( max(-self.relation[x][y]),other.relation[x][y]), max(self.relation[x][y],-other.relation[x][y]) ]

        K /= sum_{x!=y} [ min(abs(self.relation[x][y]),abs(other.relation[x][y])) ]

        .. warning::

             Renders a tuple with at position 0 the actual bipolar correlation index
             and in position 1 the minimal determination level D of self and
             the other relation.

             D = sum_{x != y} min(abs(self.relation[x][y]),abs(other.relation[x][y])) / n(n-1)

             where n is the number of actions considered.

             The correlation index with a completely indeterminate relation
             is by convention 0.0 at determination level 0.0 .

        """
        from copy import deepcopy
        g = deepcopy(self)
        g.recodeValuation(-1,1)
        actions = [x for x in g.actions]
        if MedianCut:
            g = PolarisedDigraph(g,level=Decimal('0.0'),KeepValues=False,StrictCut=True)

        if not isinstance(other,(dict)):
            if Debug:
                print('inputting a Digraph instance')
            otherg = deepcopy(other)
            otherg.recodeValuation(-1,1)
            if MedianCut:
                otherg = PolarisedDigraph(otherg,level=Decimal('0.0'),KeepValues=False,StrictCut=True)
            otherRelation = otherg.relation
        else:
            otherRelation = other
            Med = g.valuationdomain['med']
            if MedianCut:
                for x in g.actions:
                    for y in g.actions:
                        if x == y:
                            otherRelation[x][y] = Decimal('0.0')
                        else:
                            if otherRelation[x][y] > Med:
                                otherRelation[x][y] = Decimal('1.0')
                            elif otherRelation[x][y] < Med:
                                otherRelation[x][y] = Decimal('-1.0')
                            else:
                                otherRelation[x][y] = Decimal('0.0')

        correlation = Decimal('0.0')
        determination = Decimal('0.0')

        n = len(actions)
        n2 = (n*(n-1))
        for x in actions:
            for y in actions:
                if x != y:
                    ###### Bipolar approach
                    corr = min( max(-g.relation[x][y],otherRelation[x][y]), max(g.relation[x][y],-otherRelation[x][y]) )
                    correlation += corr
                    determination += min( abs(g.relation[x][y]),abs(otherRelation[x][y]) )
                    #determination += abs(corr)
                    if Debug:
                        print(x,y,g.relation[x][y],otherRelation[x][y],correlation,determination)
        if determination > Decimal('0.0'):
            correlation /= determination
            return { 'MedianCut':MedianCut, 'correlation': correlation, 'determination': determination / Decimal(str(n2)) }
        else:
            return {'MedianCut':MedianCut, 'correlation': Decimal('0.0'), 'determination': determination}


    def computeOrdinalCorrelation(self, other, MedianCut=False, Debug=False):
        """
        obsolete: dummy replacement for Digraph.computeBipolarCorrelation method
        """
        return self.computeBipolarCorrelation(other= other,MedianCut=MedianCut,Debug=Debug)
    ##     """
    ##     Renders the ordinal (Kendall) correlation K of a
    ##     self.relation when compared
    ##     with a given compatible (same actions set)) digraph or
    ##     a [-1,1] valued compatible relation (same actions set).

    ##     If MedianCut=True, the correlation is computed on the median polarized relations.

    ##     K = sum_{x != y} =

    ##         +min(abs(self.relation[x][y]),abs(other.relation[x][y])) if abs(\omin(self.relation[x][y],other.relation[x][y])) > 0.0;

    ##         -min(abs(self.relation[x][y]),abs(other.relation[x][y])) otherwise.

    ##     K = K / sum_{x!=y} min(abs(self.relation[x][y]),abs(other.relation[x][y]))

    ##     .. warning::

    ##          Renders a tuple with at position 0 the actual correlation index
    ##          and in position 1 the minimal determination level D of self and
    ##          the other relation.

    ##          D = sum_{x != y} min(abs(self.relation[x][y]),abs(other.relation[x][y])) / n(n-1)

    ##          where n is the number of actions considered.

    ##          The correlation index with a completely undeterminate relation
    ##          is by convention 0.0 at determination level 0.0 .

    ##     """
    ##     from copy import deepcopy
    ##     g = deepcopy(self)
    ##     g.recodeValuation(-1,1)
    ##     if MedianCut:
    ##         g = PolarisedDigraph(g,0.0,KeepValues=False,StrictCut=True)

    ##     if isinstance(other,(Digraph,OutrankingDigraph)):
    ##         if Debug:
    ##             print 'inputting a Digraph instance'
    ##         otherg = deepcopy(other)
    ##         if MedianCut:
    ##             otherg = PolarisedDigraph(otherg,level=0.0,KeepValues=False,StrictCut=True)
    ##         otherg.recodeValuation(-1,1)
    ##         otherRelation = otherg.relation
    ##     else:
    ##         otherRelation = other
    ##         Med = g.valuationdomain['med']
    ##         if MedianCut:
    ##             for x in g.actions:
    ##                 for y in g.actions:
    ##                     if x == y:
    ##                         otherRelation[x][y] = Med
    ##                     else:
    ##                         if otherRelation[x][y] > Med:
    ##                             otherRelation[x][y] = Decimal('1.0')
    ##                         elif otherRelation[x][y] < Med:
    ##                             otherRelation[x][y] = Decimal('-1.0')
    ##                         else:
    ##                             otherRelation[x][y] = Med
    ##     correlation = Decimal('0.0')
    ##     determination = Decimal('0.0')
    ##     actions = [x for x in g.actions]
    ##     n = len(actions)
    ##     n2 = 2*(n * (n-1))
    ##     for x in actions:
    ##         for y in actions:
    ##             if x != y:
    ##                 corr = abs(g.omin([g.relation[x][y],
    ##                                           otherRelation[x][y]]))
    ##                 if corr > Decimal('0'):
    ##                     correlation += (abs(g.relation[x][y]) + abs(otherRelation[x][y]))
    ##                 else:
    ##                     correlation -= (abs(g.relation[x][y]) + abs(otherRelation[x][y]))
    ##                 determination += (abs(g.relation[x][y]) + abs(otherRelation[x][y]))
    ##                 if Debug:
    ##                     print x,y,g.relation[x][y],otherRelation[x][y],correlation,determination
    ##     if determination > Decimal('0.0'):
    ##         correlation /= determination
    ##         return {'MedianCut':MedianCut, 'correlation': correlation, 'determination': determination / Decimal(str(n2))}
    ##     else:
    ##         return {'MedianCut':MedianCut, 'correlation': Decimal('0.0'), 'determination': determination}

    def computeKemenyIndex(self, otherRelation):
        """
        renders the Kemeny index of the self.relation
        compared with a given crisp valued relation of a compatible
        other digraph (same nodes or actions).
        """
        KemenyIndex = 0.0
        actions = [x for x in self.actions]
        for x in actions:
            for y in actions:
                if x != y:
                    if otherRelation[x][y] > Decimal('0'):
                        KemenyIndex += float(self.relation[x][y])
                    elif otherRelation[x][y] < Decimal('0'):
                        KemenyIndex -= float(self.relation[x][y])
        return KemenyIndex

    def flatChoice(self,ch,Debug=False):
        """
        Converts set or list ch recursively to a flat list of items.
        """
        result = []
        for x in ch:
            if Debug:
                print(x)
            if isinstance(x,frozenset):
                for y in self.flatChoice(x,Debug):
                    result.append(y)
            else:
                result.append(x)
        if Debug:
            print(result)
        return result

    def convertValuationToDecimal(self):
        """
        Convert the float valuation limits to Decimals.
        """
        self.valuationdomain['min'] = Decimal(str(self.valuationdomain['min']))
        self.valuationdomain['med'] = Decimal(str(self.valuationdomain['med']))
        self.valuationdomain['max'] = Decimal(str(self.valuationdomain['max']))

    def convertRelationToDecimal(self):
        """
        Convert the float valued self.relation in a decimal valued one.
        """
        actions = [x for x in self.actions]
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Decimal(str(self.relation[x][y]))
        return relation

    def bipolarKCorrelation(self, digraph,Debug=False):
        """
        Renders the bipolar Kendall correlation between two bipolar valued
        digraphs computed from the average valuation of the
        XORDigraph(self,digraph) instance.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other) Digraph method

        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        actions = [x for x in self.actions]
        n = len(actions)
        xor.recodeValuation(-1.0,1.0)

        kDistance = Decimal("0.0")
        for x in actions:
            for y in actions:
                if x != y:
                    kDistance += xor.relation[x][y]
        kDistance = Decimal(str(kDistance)) / Decimal(str((n * (n-1))))
        # the negation of the kDistance, i.e. -kDistance gives
        # the bipolar extended Kendall tau correlation
        return -kDistance

    def crispKDistance(self, digraph,Debug=False):
        """
        Renders the crisp Kendall distance between two bipolar valued
        digraphs.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other, MedianCut=True) Digraph method
        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        actions = [x for x in self.actions]
        n = len(actions)

        k2Distance = xor.size()
        k2Distance = Decimal(str(k2Distance)) / Decimal(str((n * (n-1))))

        return k2Distance

    def bipolarKDistance(self, digraph,Debug=False):
        """
        Renders the bipolar crisp Kendall distance between two bipolar valued
        digraphs.

        .. warning::

             Obsolete! Is replaced by the self.computeBipolarCorrelation(other, MedianCut=True) Digraph method

        """
        xor = XORDigraph(self,digraph,Debug)
        if Debug:
            xor.showRelationTable()
        actions = [x for x in self.actions]
        n = len(actions)

        k2Distance = xor.coSize() - xor.size()
        k2Distance = Decimal(str(k2Distance)) / Decimal(str((n * (n-1))))

        return k2Distance

    def weakCondorcetWinners(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] >= self.valuationdomain['med']
        for all y != x.
        """
        actions = [x for x in self.actions]
        Med = self.valuationdomain['med']
        wCW = []
        for x in actions:
            Winner = True
            for y in [z for z in self.actions if z != x]:
                if self.relation[x][y] < Med:
                    Winner = False
                    break
            if Winner:
                wCW.append(x)
        wCW.sort()
        return wCW

    def condorcetWinners(self):
        """
        Renders the set of decision actions x such that
        self.relation[x][y] > self.valuationdomain['med']
        for all y != x.
        """
        actions = [x for x in self.actions]
        Med = self.valuationdomain['med']
        CW = []
        for x in actions:
            Winner = True
            for y in [z for z in self.actions if z != x]:
                if self.relation[x][y] <= Med:
                    Winner = False
                    break
            if Winner:
                CW.append(x)
        CW.sort()
        return CW

    def forcedBestSingleChoice(self):
        """
        Renders the set of most determined outranking singletons in self.
        """
        import copy
        actions = set(self.actions)
        relation = self.relation
        valuationList = []
        for x in actions:
            for y in actions:
                if relation[x][y] not in valuationList:
                    valuationList.append(relation[x][y])
        valuationList.sort()
        print('Credibility levels:', valuationList)
        bestSingleChoices = copy.deepcopy(actions)
        i=0
        while bestSingleChoices != set():
            current = copy.deepcopy(bestSingleChoices)
            i += 1
            print('i_bestSingleChoices:', i,  bestSingleChoices)
            print('level', valuationList[i])
            for x in current:
                #print 'x', x
                notBest = False
                for y in actions:
                    #print 'y', y, relation[x][y]
                    if x != y and relation[x][y] < valuationList[i]:
                        notBest = True
                if notBest:
                    bestSingleChoices.remove(x)

        print('final bestSingleChoice:', current)
        print('leveal of credibility:',  valuationList[i-1])
        return (valuationList[i-1], current)

    def computeMoreOrLessUnrelatedPairs(self):
        """
        Renders a list of more or less unrelated pairs.
        """
        actions = set(self.actions)
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        moreOrLessUnrelatedPairs = []
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] < Med and relation[x][y] > Min:
                        if relation[y][x] < Med and relation[y][x] > Min:
                            if ((y,x),(relation[y][x],relation[x][y])) not in moreOrLessUnrelatedPairs:
                                moreOrLessUnrelatedPairs.append(((x,y),(relation[x][y],relation[y][x])))
        return moreOrLessUnrelatedPairs

    def computeUnrelatedPairs(self):
        """
        Renders a list of more or less unrelated pairs.
        """
        actions = set(self.actions)
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        unrelatedPairs = []
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] < Med:
                        if relation[y][x] < Med:
                            if ((y,x),(relation[y][x],relation[x][y])) not in unrelatedPairs:
                                unrelatedPairs.append(((x,y),(relation[x][y],relation[y][x])))
        return unrelatedPairs

    def closeSymmetric(self):
        """
        Produces the symmetric closure of self.relation.
        """
        actions = set(self.actions)
        relation = self.relation.copy()
        for x in actions:
            for y in actions:
                relation[x][y] = max(relation[x][y],relation[y][x])
        self.relation = relation.copy()
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeTransitivityDegree(self):
        """
        Renders the transitivity degree of a digraph.
        """
        import copy
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        relationOrig = copy.deepcopy(self.relation)
        self.closeTransitive()
        relation = self.relation
        n0 = Decimal('0')
        n1 = Decimal('0')
        for x in actionsList:
            for y in actionsList:
                if relationOrig[x][y] > Med:
                    n0 += 1
                if relation[x][y] > Med:
                    n1 += 1
        self.relation = copy.deepcopy(relationOrig)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if n1 > Decimal('0'):
            return n0/n1
        else:
            return Decimal('0')

    def computeSizeTransitiveClosure(self):
        """
        Renders the size of the transitive closure of a digraph.
        """
        import copy
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        relationOrig = copy.deepcopy(self.relation)
        self.closeTransitive()
        relation = self.relation
        n1 = 0
        for x in actionsList:
            for y in actionsList:
                if relation[x][y] > Med:
                    n1 += 1
        self.relation = copy.deepcopy(relationOrig)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        return n1


    def closeTransitive(self,Irreflexive=True):
        """
        Produces the transitive closure of self.relation.
        """
        import copy
        actions = set(self.actions)
        relation = copy.deepcopy(self.relation)
        for x in actions:
            for y in actions:
                for z in actions:
                    relation[y][z] = max(relation[y][z],min(relation[y][x],relation[x][z]))
        if Irreflexive:
            for x in actions:
                relation[x][x] = self.valuationdomain['min']
        self.relation = copy.deepcopy(relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def isCyclic(self, Debug=True):
        """
        checks the cyclicity of self.relation by checking
        for a reflexive loop in its transitive closure
        !! self.relation is supposed to be irreflexive !!
        """
        import copy
        Med = self.valuationdomain['med']
        if Debug:
            print(Med)
        actions = set(self.actions)
        relation = copy.deepcopy(self.relation)

        isCyclic = False
        for x in actions:
            for y in actions:
                for z in actions:
                    relation[y][z] = max(relation[y][z],min(relation[y][x],relation[x][z]))

        if Debug:
            for x in actions:
                print('x, relation[x][x]', x, relation[x][x])
        for x in actions:
            if relation[x][x] > Med:
                isCyclic = True
                break

        return isCyclic


    def automorphismGenerators(self):
        """
        Add automorphism group generators to digraph.
        """
        import os
        Name = self.name
        self.savedre(Name)
        aindex = self.aindex
        arevindex = {}
        for i in aindex:
            arevindex[str(aindex[i])] = i
        print(arevindex)
        File0 = Name+'.dre'
        File1 = Name+'.auto'
        print('# automorphisms extraction from dre file #')
        print('# Using input file: ' + File0)
        String2 = "echo '<"+File0+' -m p >'+File1+" x' | dreadnaut"
        print(String2)
        os.system(String2)
        try:
            f1 = open(File1,'r')
            noError = True
        except:
            print('The input file: ', File1,' could not be found!')
            print("Be sure that nauty's dreadnaut programm is available!")
            noError = False
        if noError:
            permutations = {}
            t = f1.readline()
            nl = 0
            while t[:1] != '':
                nl += 1
                if t[:1] == ' ':
                    ts = f1.readline()
                    while ts[:2] == '  ':
                        suite = 1
                        t = t + ts
                        ts = f1.readline()
                    permutation = t.split()
                    print('# permutation = '+ str(nl)+str(permutation))
                    permutations[str(nl)] = {}
                    for i in range(len(permutation)):
                        permutations[str(nl)][str(arevindex[str(i+1)])] = str(arevindex[str(permutation[i])])
                    t = ts
                else:
                    #print '# ', t
                    grpsize = ''
                    for i in range(len(t)):
                        #print t[i],
                        if t[i] == '=':
                            #print 'ok'
                            #grpsize = ''
                            for j in range(i+1,len(t)):
                                if t[j] != ';':
                                    #print t[j]
                                    grpsize += t[j]
                                else:
                                    break
                            break
                    #print eval(grpsize)
                    #t = f1.readline
                    break
            f1.close()
            self.reflections = {}
            self.permutations = permutations
            self.automorphismGroupSize = eval(grpsize)

    def showAutomorphismGenerators(self):
        """
        Renders the generators of the automorphism group.
        """
        print('*---- Automorphism group generators ----')
        try:
            reflections = self.reflections
            permutations = self.permutations
            noError = True
        except:
            print('No permutations or reflections defined yet !!')
            noError = False
        if noError:
            print('Permutations')
            for g in permutations:
                print(self.permutations[g])
            print('Reflections')
            for g in reflections:
                print(self.reflexions[g])
        else:
            print('Run self.automorphismGenerators()')

    def showOrbits(self,InChoices,withListing=True):
        """
        Prints the orbits of Choices along the automorphisms of
        the digraph self.
        """
        try:
            reflections = self.reflections
            permutations = self.permutations
            noError = True
        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')
            noError=False
        if noError:
            Choices = InChoices.copy()
            print('*--- Isomorphic reduction of choices')
            Iso = set()
            v = [0 for i in range(1,self.automorphismGroupSize + 1)]
            print('Number of choices:', len(Choices))
            while Choices != set():
                sCur = Choices.pop()
                print()
                print('current representative: ',sCur)
                print('length   : ', len(sCur))
                IsosCur = set([sCur])
                Isos = set()
                while IsosCur != Isos:
                    Isos = IsosCur.copy()
                    IsosRes = IsosCur.copy()
                    for s in IsosCur:
                        for g in reflections:
                            cur = s
                            for a in reflections[g]:
                                if (a[0] in cur) and a[1] not in cur:
                                    cur = cur - set([a[0]])
                                    cur = cur | set([a[1]])
                                else:
                                    if a[1] in cur and a[0] not in cur:
                                        cur = cur - set([a[1]])
                                        cur = cur | set([a[0]])
                            IsosRes.add(cur)
                    IsosCur = IsosRes.copy()
                    for s in IsosCur:
                        for g in permutations:
                            cur = frozenset()
                            for x in s:
                                cur = cur | set([permutations[g][str(x)]])
                            IsosRes = IsosRes | set([cur])
                    IsosCur = IsosRes.copy()
                Iso.add(sCur)
                niso = len(Isos)
                print('number of isomorph choices', niso)
                v[(self.automorphismGroupSize//niso)-1] += 1
                if withListing:
                    print('isormorph choices')
                    for ch in Isos:
                        print(list(ch))
                print('Number of choices before : ', len(Choices) + 1)
                Choices = Choices - Isos
                print('Number of choices after  : ', len(Choices))
            print()
            print('*---- Global result ----')
            print('Number of choices: ', len(InChoices))
            print('Number of orbits : ', len(Iso))
            print('Labelled representatives:')
            for ch in Iso:
                print(list(ch))
            print()
            print('                     Symmetry vector')
            print('stabilizer size  : ', list(range(1,self.automorphismGroupSize + 1)))
            print('frequency        : ', v)
            self.orbits = Iso

    def showOrbitsFromFile(self,InFile,withListing=True):
        """
        Prints the orbits of Choices along the automorphisms of
        the digraph self by reading in the 0-1 misset file format.
        """
        try:
            reflections = self.reflections
            permutations = self.permutations
            f1 = open(InFile,'r')
            noError = True
        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')
            noError = False

        if noError:
            actions = [x for x in self.actions]
            print('*--- Isomorphic reduction of choices')
            Iso = set()
            misset = set()
            v = [0 for i in range(1,self.order + 1)]
            while 1:
                line = f1.readline()
                if not line: break
                sCur = set()
                for i in range(len(line)):
                    if line[i] == '1':
                        sCur.add(actions[i])
                if sCur not in misset:
                    print('current representative: ',sCur)
                    print('length   : ', len(sCur))
                    IsosCur = set([frozenset(sCur)])
                    Isos = set()
                    while IsosCur != Isos:
                        Isos = IsosCur.copy()
                        IsosRes = IsosCur.copy()
                        for s in IsosCur:
                            for g in reflections:
                                cur = s
                                for a in reflections[g]:
                                    if (a[0] in cur) and a[1] not in cur:
                                        cur = cur - set([a[0]])
                                        cur = cur | set([a[1]])
                                    else:
                                        if a[1] in cur and a[0] not in cur:
                                            cur = cur - set([a[1]])
                                            cur = cur | set([a[0]])
                                IsosRes.add(cur)
                        IsosCur = IsosRes.copy()
                        for s in IsosCur:
                            for g in permutations:
                                cur = frozenset()
                                for x in s:
                                    cur = cur | set([permutations[g][x]])
                                IsosRes = IsosRes | set([cur])
                        IsosCur = IsosRes.copy()
                    Iso = Iso | set([frozenset(sCur)])
                    niso = len(Isos)
                    print('number of isomorph choices', niso)
                    v[((2*self.order)//niso)-1] += 1
                    if withListing:
                        print('isormorph choices')
                        for ch in Isos:
                            print(list(ch))
                    print('Number of choices before : ', len(misset) + 1)
                    misset = misset | Isos
                    print('Number of choices after  : ', len(misset))
            print()
            print('*---- Global result ----')
            print('Labelled representatives:')
            for ch in Iso:
                print(list(ch))
            print()
            print('Number of choices: ', len(misset))
            print('Number of orbits : ', len(Iso))
            print('symmetry vector  : ', list(range(1,self.order + 1)))
            print('frequency        : ', v)
            self.orbits = Iso

    def readPerrinMisset(self,file):
        """
        read method for 0-1-char-coded MISs from perrinMIS.c curd.dat file.
        """
        try:
            f1 = open(file,'r')
            noError = True
        except:
            noError = False
            print('The input file: ', file,' could not be found ?')

        if noError:
            actions = [x for x in self.actions]
            nl = 0
            misset = set()
            while 1:
                line = f1.readline()
                if not line: break
                nl += 1
                mis = set()
                for i in range(len(line)):
                    if ord(line[i]) == 1:
                        mis.add(actions[i])
                #print mis
                misset = misset | set([frozenset(mis)])
            #print 'Reading ' + str(nl) + ' MISs.'
            self.misset = misset

    def readPerrinMissetOpt(self,file):
        """
        read method for 0-1-char-coded MISs from perrinMIS.c curd.dat file.
        """
        try:
            f1 = open(file,'r')
            noError = True
        except:
            noError = False
            print('The input file: ', file,' could not be found ?')

        if noError:
            actions = [x for x in self.actions]
            nl = 0
            misset = set()
            for line in f1.readlines():
                if not line: break
                nl += 1
                mis = set()
                for i in range(len(line)):
                    if line[i] == '1':
                        mis.add(actions[i])
                #print mis
                misset = misset | set([frozenset(mis)])
            #print 'Reading ' + str(nl) + ' MISs.'
            self.misset = misset


    def computeOrbit(self,choice,withListing=False):
        """
        renders the set of isomorph copies of a choice following
        the automorphism of the digraph self
        """
        try:
            reflections = self.reflections
            permutations = self.permutations
            if withListing:
                print('*- ----------------"')
                print('Compute orbit of choice: ',choice)
                print('follwoing  automorphisms of digraph: ', self.name)
                print('Automorphism group size: ', self.automorphismGroupSize)
                print('Generators:')
                print('Reflections: ', reflections)
                print('Permutations: ', permutations)
            IsosCur = set([choice])
            Isos = set()
            while IsosCur != Isos:
                Isos = IsosCur.copy()
                IsosRes = IsosCur.copy()
                for s in IsosCur:
                    for g in reflections:
                        cur = s
                        for a in reflections[g]:
                            if (a[0] in cur) and a[1] not in cur:
                                cur = cur - set([a[0]])
                                cur = cur | set([a[1]])
                            else:
                                if a[1] in cur and a[0] not in cur:
                                    cur = cur - set([a[1]])
                                    cur = cur | set([a[0]])
                        IsosRes.add(cur)
                IsosCur = IsosRes.copy()
                for s in IsosCur:
                    for g in permutations:
                        cur = frozenset()
                        for x in s:
                            cur = cur | set([permutations[g][x]])
                        IsosRes = IsosRes | set([cur])
                IsosCur = IsosRes.copy()
            if withListing:
                print('Orbit size: ', len(Isos))
                print('List of isormorph choices')
                for ch in Isos:
                    print(list(ch))
            return Isos

        except:
            print('No permutations or reflections defined yet !!')
            print('Run self.automorphismGenerators()')

    def showActions(self):
        """
        presentation methods for digraphs actions
        """
        print('*----- show digraphs actions --------------*')
        actionsList = [x for x in self.actions]
        actionsList.sort()
        for x in actionsList:
            print('key: ',x)
            try:
                print('  short name:',self.actions[x]['shortName'])
            except:
                pass
            print('  name:      ',self.actions[x]['name'])
            print('  comment:   ',self.actions[x]['comment'])
            print()

    def showShort(self):
        """
        concise presentation method for genuine digraphs.
        """
        print('*----- show short --------------*')
        print('Digraph          :', self.name)
        print('Actions          :', self.actions)
        print('Valuation domain :', self.valuationdomain)
        self.showComponents()

    def showAll(self):
        print('*----- show detail -------------*')
        print('Digraph          :', self.name)
        print('*---- Actions ----*')
        #actionsList = [x for x in self.actions]
        actionsList = []
        for x in self.actions:
            if isinstance(x,frozenset):
                actionsList += [self.actions[x]['name']]
            else:
                actionsList += [str(x)]
        actionsList.sort()
        print(actionsList)
        print('*---- Characteristic valuation domain ----*')
        print(self.valuationdomain)
        self.showRelationTable()
        self.showComponents()
        gamma = self.gammaSets()
        notGamma = self.notGammaSets()
        print('Neighborhoods:')
        print('  Gamma     :')
        for x in gamma:
            print('\'%s\': in => %s, out => %s' % (x,gamma[x][1],gamma[x][0]))
        print('  Not Gamma :')
        for x in notGamma:
            print('\'%s\': in => %s, out => %s' % (x,notGamma[x][1],notGamma[x][0]))

    def showRelation(self):
        """
        prints the relation valuation in ##.## format.
        """
        print('* ---- Relation -----', end=' ')
        actionsList = []
        for x in self.actions:
            if isinstance(x,frozenset):
                actionsList += [(self.actions[x]['name'],x)]
            else:
                actionsList += [(x,x)]
        #actionsList = [x for x in self.actions]
        actionsList.sort()
        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = False
        for x in actionsList:
            print()
            for y in actionsList:
                if hasIntegerValuation:
                    print('('+str(x[0])+', '+str(y[0])+') = '+' % .2f ' % (self.relation[x[1]][y[1]]))
                else:
                    print('('+str(x[0])+', '+str(y[0])+') = '+' %d ' % (self.relation[x[1]][y[1]]))

        print()

    def showRelationTable(self,IntegerValues=False,actionsSubset= None,relation=None,ndigits=2):
        """
        prints the relation valuation in actions X actions table format.
        """
        if actionsSubset == None:
            actions = self.actions
        else:
            actions = actionsSubset
        if relation == None:
            relation = self.relation
        print('* ---- Relation Table -----\n', end=' ')
        print(' S   | ', end=' ')
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(str(x),x)]
        actionsList.sort()
        #print actionsList
        #actionsList.sort()

        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = IntegerValues

        for x in actionsList:
            print("'"+x[0]+"'\t ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in actionsList:
            print("'"+x[0]+"' | ", end=' ')
            for y in actionsList:
                if hasIntegerValuation:
                    print('%d\t' % (relation[x[1]][y[1]]), end=' ')
                else:
                    formatString = '%%2.%df\t' % ndigits
                    print(formatString % (relation[x[1]][y[1]]), end=' ')
            print()
        print('\n')
        print('Valuation domain: ', self.valuationdomain)

    def htmlRelationTable(self,tableTitle='Relation Table',relationName=' R ',hasIntegerValues=False,actionsSubset= None,isColored=False):
        """
        renders the relation valuation in actions X actions html table format.
        """
        Med = self.valuationdomain['med']
        if actionsSubset == None:
            actions = self.actions
        else:
            actions = actionsSubset
        s = ''
        s += '<h1>%s</h1>' % tableTitle
        s += '<table border="1">'
        if isColored:
            s += '<tr bgcolor="#9acd32"><th>%s</th>' % relationName
        else:
            s += '<tr><th>%s</th>' % relationName
        #actions = [x for x in actions]
        actionsList = []
        for x in actions:
            if isinstance(x,frozenset):
                try:
                    actionsList += [(actions[x]['shortName'],x)]
                except:
                    actionsList += [(actions[x]['name'],x)]
            else:
                actionsList += [(str(x),str(x))]
        actionsList.sort()
        #print actionsList
        #actionsList.sort()

        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = hasIntegerValues

        for x in actionsList:
            if isColored:
                s += '<th bgcolor="#FFF79B">%s</th>' % (x[0])
            else:
                s += '<th>%s</th>' % (x[0])
        s += '</tr>'
        for x in actionsList:
            s += '<tr>'
            if isColored:
                s += '<th bgcolor="#FFF79B">%s</th>' % (x[0])
            else:
                s += '<th>%s</th>' % (x[0])
            for y in actionsList:
                if hasIntegerValuation:
                    if isColored:
                        if self.relation[x[1]][y[1]] > Med:
                            s += '<td bgcolor="#ddffdd" align="right">%d</td>' % (self.relation[x[1]][y[1]])
                        elif self.relation[x[1]][y[1]] < Med:
                            s += '<td bgcolor="#ffddff"  align="right">%d</td>' % (self.relation[x[1]][y[1]])
                        else:
                            s += '<td bgcolor="#dddddd" align="right" >%d</td>' % (self.relation[x[1]][y[1]])
                    else:
                        s += '<td>%d</td>' % (self.relation[x[1]][y[1]])
                else:
                    if isColored:
                        if self.relation[x[1]][y[1]] > Med:
                            s += '<td bgcolor="#ddffdd" align="right">%2.2f</td>' % (self.relation[x[1]][y[1]])
                        elif self.relation[x[1]][y[1]] < Med:
                            s += '<td  bgcolor="#ffddff" align="right">%2.2f</td>' % (self.relation[x[1]][y[1]])
                        else:
                            s += '<td  bgcolor="#dddddd" align="right">%2.2f</td>' % (self.relation[x[1]][y[1]])
                    else:
                        s += '<td>%2.2f</td>' % (self.relation[x[1]][y[1]])
            s += '</tr>'
        s += '</table>'
        return s

    def showdre(self):
        """
        Shows relation in nauty format.
        """
        print('*----- show dre -------------*')
        actions = [x for x in self.actions]
        aindex = {}
        i = 1
        print('Actions index:')
        for x in actions:
            print(i,': ', str(x))
            aindex[x] = i
            i += 1
        Med = self.valuationdomain['med']
        relation = self.relation
        n = len(actions)
        print('n='+str(n)+' $=1 d g')
        for x in actions:
            res = str(aindex[x]) + ': '
            for y in actions:
                if relation[x][y] > Med:
                    res = res + str(aindex[y]) + ' '
            res = res + ';'
            print(res)

    def exportGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),noSilent=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file  for graph drawing filtering.
        """
        import os
        if noSilent:
            print('*---- exporting a dot file dor GraphViz tools ---------*')
        actionkeys = [x for x in self.actions]
        n = len(actionkeys)
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
        if bestChoice != set():
            rankBestString = '{rank=max; '
        if worstChoice != set():
            rankWorstString = '{rank=min; '
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\nRubis Python Server (graphviz), R. Bisdorff, 2008", size="')
        fo.write(graphSize),fo.write('"];\n')
        for i in range(n):
            try:
                nodeName = self.actions[actionkeys[i]]['shortName']
            except:
                try:
                    nodeName = self.actions[actionskeys[i]]['name']
                except:
                    nodeName = str(actionkeys[i])
            node = 'n'+str(i+1)+' [shape = "circle", label = "' +nodeName+'"'
            if actionkeys[i] in bestChoice:
                node += ', style = "filled", color = gold];\n'
                rankBestString += 'n'+str(i+1)+' '
            elif actionkeys[i] in worstChoice:
                node += ', style = "filled", color = lightblue];\n'
                rankWorstString += 'n'+str(i+1)+' '
            else:
                node += '];\n'
            fo.write(node)
        if bestChoice != set():
            rankBestString += '}\n'
        if worstChoice != set():
            rankWorstString += '}\n'
##         for i in range(n):
##             edge = 'n'+str(i+1)
##             for j in range(n):
##                 if i != j and relation[actions[i]][actions[j]] > Med:
##                     edge0 = edge+'-> n'+str(j+1)+';\n'
##                     fo.write(edge0)
##                     j += 1
##             i += 1
        for i in range(n):
            for j in range(i+1, n):
                edge = 'n'+str(i+1)
                if relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] > Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both,style="setlinewidth(2)",color=black, arrowhead=normal, arrowtail=normal] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] == Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowhead=normal, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] > Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=black, arrowtail=normal, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] == Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=both, color=grey, arrowhead=empty, arrowtail=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] > Med and relation[actionkeys[j]][actionkeys[i]] <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=black] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] == Med and relation[actionkeys[j]][actionkeys[i]] <  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=forward, color=grey, arrowhead=empty] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] < Med and relation[actionkeys[j]][actionkeys[i]] >  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=back, color=black] ;\n'
                    fo.write(edge0)
                elif relation[actionkeys[i]][actionkeys[j]] < Med and relation[actionkeys[j]][actionkeys[i]] ==  Med:
                    edge0 = edge+'-> n'+str(j+1)+' [dir=back, color=grey, arrowtail=empty] ;\n'
                    fo.write(edge0)

        if bestChoice != set():
            fo.write(rankBestString)
        if worstChoice != set():
            fo.write(rankWorstString)
        fo.write('}\n')
        fo.close()
        if type(self) == CirculantDigraph:
            commandString = 'circo -T'+graphType+' '+dotName+' -o '+name+'.' + graphType
        elif type(self) == RandomTree:
            commandString = 'neato -T'+graphType+' '+dotName+' -o '+name+'.' + graphType
        else:
            commandString = 'dot -Grankdir=BT -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType

        if noSilent:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if noSilent:
                print('graphViz tools not avalaible! Please check installation.')


    def savedre(self,name='temp'):
        """
        save digraph in nauty format.
        """
        print('*----- saving digraph in nauty dre format  -------------*')
        actions = [x for x in self.actions]
        Name = name+'.dre'
        aindex = {}
        i = 1
        print('Actions index:')
        for x in actions:
            print(i,': ', str(x))
            aindex[x] = i
            i += 1
        Med = self.valuationdomain['med']
        relation = self.relation
        n = len(actions)
        fo = open(Name,'w')
        fo.write('n='+str(n)+' $=1 d g\n')
        for x in actions:
            res = str(aindex[x]) + ': '
            for y in actions:
                if relation[x][y] > Med:
                    res = res + str(aindex[y]) + ' '
            res = res + ';\n'
            fo.write(res)
        fo.close()
        self.aindex = aindex.copy()

    def saveXML(self,name='temp',category='general',subcategory='general',author='digraphs Module (RB)',reference='saved from Python'):
        """
        save digraph in XML format.
        """
        print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = name+'.xml'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="digraphs.xsl"?>\n')
        fo.write('<!DOCTYPE digraph SYSTEM "digraphs.dtd">\n')
        fo.write('<digraph ')
        fo.write('category="' + category+'" subcategory="'+subcategory+'">\n')
        fo.write('<header>\n')
        fo.write('<name>')
        fo.write(nameExt)
        fo.write('</name>\n')
        fo.write('<author>')
        fo.write(author)
        fo.write('</author>\n')
        fo.write('<reference>')
        fo.write(reference)
        fo.write('</reference>\n')
        fo.write('</header>')
        actions = self.actions
        fo.write('<nodes>\n')
        for x in actions:
            fo.write('<node>')
            fo.write(str(x))
            fo.write('</node>\n')
        fo.write('</nodes>\n')
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        fo.write('<valuationdomain>\n')
        fo.write('<min>')
        fo.write(str(Min))
        fo.write('</min>\n')
        fo.write('<max>')
        fo.write(str(Max))
        fo.write('</max>\n')
        fo.write('</valuationdomain>\n')
        fo.write('<relation>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<arc>\n')
                fo.write('<i>')
                fo.write(str(x))
                fo.write('</i>\n')
                fo.write('<t>')
                fo.write(str(y))
                fo.write('</t>\n')
                fo.write('<v>')
                fo.write(str(relation[x][y]))
                fo.write('</v>\n')
                fo.write('</arc>\n')
        fo.write('</relation>\n')
        fo.write('</digraph>\n')
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMCDA(self,fileName='temp',relationName='R',category='random',subcategory='valued',author='digraphs Module (RB)',reference='saved from Python',valuationType='standard',servingD3=False):
        """
        save digraph in XMCDA format.
        """
        print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = fileName+'.xmcda'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcdaDefault.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2008/UMCDA-ML-1.0 umcda-ml-1.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2008/UMCDA-ML-1.0">\n'))
        # write description
        fo.write('<caseReference>\n')
        fo.write('<title>Valued Digraph in XMCDA format</title>\n')
        fo.write('<id>%s</id>\n' % (fileName) )
        fo.write('<name>%s</name>\n' % (self.name) )
        fo.write('<type>root</type>\n')
        fo.write('<user>%s</user>\n' % (author) )
        fo.write('<version>%s</version>\n' % (reference) )
        fo.write('</caseReference>\n')
        # write nodes
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives>\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('List of Alternatives'))
        fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('<comment>Potential decision actions.</comment>\n')
        fo.write('</description>\n')
        for i in range(na):
            fo.write('<alternative id="%s">\n' % (actionsList[i]))
            fo.write('<description>\n')
            fo.write('<name>')
            try:
                fo.write(str(actions[actionsList[i]]['name']))
            except:
                fo.write('nameless')
            fo.write('</name>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                fo.write('No comment')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<alternativeType>potential</alternativeType>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        # write valued binary Relation
        fo.write('<relationOnAlternatives>\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Valued Binary Relation'))
        fo.write('<name>%s</name>\n' % (relationName) )
        fo.write('<type>%s</type>\n' % ('valuedBinaryRelation'))
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        fo.write('<valuationDomain>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valuation Domain'))
        fo.write('</description>\n')
        fo.write('<valuationType>%s</valuationType>\n' % (valuationType) )
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        fo.write('<minimum><real>%2.2f</real></minimum>\n' % (Min))
        fo.write('<maximum><real>%2.2f</real></maximum>\n' % (Max))
        fo.write('</valuationDomain>\n')
        fo.write('<arcs>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valued Adjacency Table'))
        try:
            category = self.category
            subcategory = self.subcategory
        except:
            pass
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<arc>\n')
                fo.write('<from><alternativeID>')
                fo.write(str(x))
                fo.write('</alternativeID></from>\n')
                fo.write('<to><alternativeID>')
                fo.write(str(y))
                fo.write('</alternativeID></to>\n')
                fo.write('<value><real>%2.2f' % (relation[x][y]) )
                fo.write('</real></value>\n')
                fo.write('</arc>\n')
        fo.write('</arcs>\n')
        fo.write('</relationOnAlternatives>\n')
        fo.write('</xmcda:XMCDA>\n')
        fo.close()
        print('File: ' + nameExt + ' saved !')

    def saveXMCDA2(self,fileName='temp',relationName='R',relationType='binary',category='random',subcategory='valued',author='digraphs Module (RB)',reference='saved from Python',valuationType='standard',digits=2,servingD3=False):
        """
        save digraph in XMCDA format.
        """
        print('*----- saving digraph in XML format  -------------*')
        actions = [x for x in self.actions]
        nameExt = fileName+'.xmcda2'
        fo = open(nameExt,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if servingD3:
            fo.write('<!-- ?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"? -->\n')
        else:
            fo.write('<?xml-stylesheet type="text/xsl" href="xmcdaXSL.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/UMCDA-2.0.0 file:../XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">\n'))
        # write description
        fo.write('<projectReference id="%s" name="%s">\n' % (fileName,self.name))
        fo.write('<title>Stored Digraph in XMCDA-2.0 format</title>\n')
        #fo.write('<id>%s</id>\n' % (fileName) )
        #fo.write('<name>%s</name>\n' % (self.name) )
        #fo.write('<type>root</type>\n')
        fo.write('<user>%s</user>\n' % (author) )
        fo.write('<version>%s</version>\n' % (reference) )
        fo.write('</projectReference>\n')
        # write nodes
        actionsList = [x for x in self.actions]
        actionsList.sort()
        na = len(actionsList)
        actions = self.actions
        fo.write('<alternatives mcdaConcept="Digraph nodes">\n')
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Nodes of the digraph'))
        #fo.write('<type>%s</type>\n' % ('alternatives'))
        fo.write('<comment>Set of nodes of the digraph.</comment>\n')
        fo.write('</description>\n')
        for i in range(na):
            try:
                alternativeName = str(actions[actionsList[i]]['name'])
            except:
                alternativeName = 'nameless'

            fo.write('<alternative id="%s" name="%s">\n' % (actionsList[i],alternativeName))
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(actions[actionsList[i]]['comment']))
            except:
                fo.write('No comment')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<type>real</type>\n')
            fo.write('<active>true</active>\n')
            fo.write('<reference>false</reference>\n')
            fo.write('</alternative>\n')
        fo.write('</alternatives>\n')
        # write valued binary Relation
        fo.write('<alternativesComparisons id="1" name="%s">\n' % (relationName))
        fo.write('<description>\n')
        fo.write('<title>%s</title>\n' % ('Randomly Valued Binary Relation'))
        #fo.write('<name>%s</name>\n' % (relationName) )
        #fo.write('<type>%s</type>\n' % ('valuedBinaryRelation'))
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        fo.write('<valuation name="valuationDomain">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valuation Domain'))
        fo.write('</description>\n')
        fo.write('<quantitative>')
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        if valuationType == 'integer':
            fo.write('<minimum><integer>%d</integer></minimum>\n' % (Min))
            fo.write('<maximum><integer>%d</integer></maximum>\n' % (Max))
        else:
            formatString = '%%2.%df' % (digits)
            fo.write('<minimum><real>')
            fo.write(formatString % (Min))
            fo.write('</real></minimum>\n')
            fo.write('<maximum><real>')
            fo.write(formatString % (Max))
            fo.write('</real></maximum>\n')
        fo.write('</quantitative>\n')
        fo.write('</valuation>\n')
        fo.write('<comparisonType>%s</comparisonType>\n' % (relationName))
        fo.write('<pairs>\n')
        fo.write('<description>\n')
        fo.write('<subTitle>%s</subTitle>\n' % ('Valued Adjacency Table'))
        try:
            category = self.category
            subcategory = self.subcategory
        except:
            pass
        fo.write('<comment>%s %s Digraph</comment>\n' % (category,subcategory) )
        fo.write('</description>\n')
        relation = self.relation
        for x in actions:
            for y in actions:
                fo.write('<pair>\n')
                fo.write('<initial><alternativeID>')
                fo.write(str(x))
                fo.write('</alternativeID></initial>\n')
                fo.write('<terminal><alternativeID>')
                fo.write(str(y))
                fo.write('</alternativeID></terminal>\n')
                if valuationType == 'bipolar':
                    formatString = '%%+2.%df' % (digits)
                else:
                    formatString = '%%2.%df' % (digits)
                fo.write('<value><real>')
                fo.write(formatString % (relation[x][y]) )
                fo.write('</real></value>\n')
                fo.write('</pair>\n')
        fo.write('</pairs>\n')
        fo.write('</alternativesComparisons>\n')
        fo.write('</xmcda:XMCDA>\n')
        fo.close()
        print('File: ' + nameExt + ' saved !')


    def computeDensities(self,choice):
        """
        parameter: choice in self
        renders the four densitiy parameters:
        arc density, double arc density, single arc density, absence arc density.
        """
        actions = set(choice)
        relation = self.relation
        Med = self.valuationdomain['med']
        order = float(len(actions))
        d = 0.0
        dd = 0.0
        sd = 0.0
        ad = 0.0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        d += 1.0
                    if relation[x][y] > Med and relation[y][x] > Med:
                        dd += 1.0
                    if relation[x][y] > Med and relation[y][x] <= Med:
                        sd += 1.0
                    if relation[x][y] <= Med and relation[y][x] <= Med:
                        ad += 1.0
        d = d / (order*(order-1))
        dd / (order*(order-1))
        sd = (2*sd) / (order*(order-1))
        ad = ad / (order*(order-1))
        return d,dd,sd,ad

    def computeCutLevelDensities(self,choice,level):
        """
        parameter: choice in self, robustness level
        renders three robust densitiy parameters:
        robust double arc density,
        robust single arc density,
        robust absence arc densitiy.
        """
        actions = set(choice)
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        negLevel = Max - level + Min
        order = float(len(actions))
        rdd = 0.0
        rsd = 0.0
        rad = 0.0
        if level < Med or level >= Max:
            print('Error: robustness level too low or too high !!!')
        else:
            for x in actions:
                for y in actions:
                    if x != y:
                        if relation[x][y] > level and relation[y][x] > level:
                            rdd += 1.0
                        if relation[x][y] > level:
                            if relation[y][x] < negLevel:
                                rsd += 1.0
                        if relation[x][y] < negLevel and relation[y][x] < negLevel:
                            rad += 1.0
            rdd = rdd / (order*(order-1))
            rsd = (2*rsd) / (order*(order-1))
            rad = rad / (order*(order-1))
        density = {}
        density['double'] = rdd
        density['single'] = rsd
        density['absence'] = rad
        return density

    def computeAllDensities(self,choice=None):
        """
        parameter: choice in self
        renders six densitiy parameters:
        arc density, double arc density,
        single arc density, strict single arc density,
        absence arc density, strict absence arc densitiy.
        """
        if choice != None:
            actions = set(choice)
        else:
            actions = self.actions
        relation = self.relation
        Med = self.valuationdomain['med']
        order = float(len(actions))
        d = 0.0
        dd = 0.0
        sd = 0.0
        ssd = 0.0
        ad = 0.0
        asd = 0.0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        d += 1.0
                    if relation[x][y] > Med and relation[y][x] > Med:
                        dd += 1.0
                    if relation[x][y] > Med:
                        if relation[y][x] < Med:
                            ssd += 1.0
                            sd += 1.0
                        elif relation[y][x] == Med:
                            sd += 1.0
                    if relation[x][y] <= Med and relation[y][x] <= Med:
                        ad += 1.0
                    if relation[x][y] < Med and relation[y][x] < Med:
                        asd += 1.0
        d = d / float(order*(order-1))
        dd = dd / float(order*(order-1))
        sd = (2*sd) / float(order*(order-1))
        ssd = (2*ssd) / float(order*(order-1))
        ad = ad / float(order*(order-1))
        asd = asd / float(order*(order-1))
        density = {}
        density['arc'] = d
        density['double'] = dd
        density['single'] = sd
        density['strictSingle'] = ssd
        density['absence'] = ad
        density['strictAbsence'] = asd
        return density

    def computeValuationLevels(self,choice=None, Debug=False):
        """
        renders the symmetric closure of the
        apparent valuations levels of self
        in an increasingly ordered list.
        If parameter choice is given, the
        computation is limited to the actions
        of the choice.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']

        if choice == None:
            actions = [x for x in self.actions]
        else:
            actions = [x for x in choice]

        relation = self.relation

        levels = set([Max,Min])
        for x in actions:
            for y in actions:
                levels.add(relation[x][y])
                levels.add(Max - relation[x][y] + Min)
        ## if Debug:
        ##     print levels
        levelsList = list(levels)
        levelsList.sort()
        if Debug:
            print('levelsList', levelsList)
        return levelsList

    def computePrudentBetaLevel(self, Debug=False):
        """
        computes alpha, ie the lowest valuation level, for which the
        bipolarly polarised digraph doesn't contain a chordless circuit.
        """
        Med = self.valuationdomain['med']
        valuationLevels= self.computeValuationLevels(Debug=Debug)
        if Debug:
            print('number of levels; %d' % len(valuationLevels))
        valuationLevels.reverse()
        for i in range(len([x for x in valuationLevels if x > Med])):
            level = valuationLevels[i+1]
            if Debug:
                print('checking level: ', level)
            gp = PolarisedDigraph(self,level=level)
            if len(gp.computeChordlessCircuits()) > 0:
                if Debug:
                    gp.showChordlessCircuits()
                    print('prudent order level = %s (med = %.2f)' % (str(valuationLevels[i-1]),Med))
                self.prudentBetaLevel = valuationLevels[i]
                return self.prudentBetaLevel

        self.prudentBetaLevel = Med
        if Debug:
            ## self.computeChordlessCircuits()
            ## self.showChordlessCircuits()
            print('prudent order level = %s = med' % str(Med))
        return Med

    def computeValuationPercentiles(self,choice, percentages, withValues=False):
        """
        Parameters: choice and list of percentages.
        renders a series of quantiles of the characteristics valuation of
        the arcs in the digraph.
        """
        relation = self.relation
        vx = []
        for x in choice:
            for y in choice:
                if x != y:
                    vx.append(relation[x][y])
        vx.sort()
        if withValues:
            print('values ', vx)
        nv = len(vx)
        percentile = {}
        for q in percentages:
            kq = q*nv//100
            r = (nv*q)% 100
            if q == 0:
                percentile[q] = vx[0]
            elif q == 100:
                percentile[q] = vx[nv-1]
            else:
                percentile[q] = vx[kq-1] + (Decimal(str(r))/Decimal('100.0')) * (vx[kq]-vx[kq-1])
        return percentile

    def computeValuationPercentages(self,choice,percentiles,withValues=False):
        """
        Parameters: choice and list of percentages.
        renders a series of quantiles of the characteristics valuation of
        the arcs in the digraph.
        """
        relation = self.relation
        vx = []
        for x in choice:
            for y in choice:
                if x != y:
                    vx.append(relation[x][y])
        vx.sort()
        nv = len(vx)
        if withValues:
            print('values ', vx)
        np = len(percentiles)
        rv = [0.0 for i in range(np)]
        for val in vx:
            for i in range(np):
                if percentiles[i] > val:
                    rv[i] += 1.0
        percentages = {}
        for i in range(np):
            percentages[percentiles[i]] = rv[i]/float(nv)
        return percentages

    def computeAverageValuation(self):
        """
        Computes the bipolar average correlation between
        self and the crisp complete digraph of same order
        of the irreflexive and determined arcs of the digraph
        """
        Med = self.valuationdomain['med']
        averageValuation = Decimal('0.0')
        determined = Decimal('0.0')
        actions = [x for x in self.actions]
        nbDeterm = 0
        for x in actions:
            for y in actions:
                if x != y:
                    if self.relation[x][y] != Med:
                        nbDeterm += 1
                        averageValuation += self.relation[x][y]
                        determined += abs(self.relation[x][y])
        return averageValuation / determined

    def computeDeterminateness(self):
        """
        Computes the Kendalll distance of self
        with the all median valued (indeterminate) digraph.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        relation = self.relation
        order = self.order
        deter = Decimal('0.0')
        for x in actionsList:
            for y in actionsList:
                if x != y:
                    #print relation[x][y], Med, relation[x][y] - Med
                    deter += abs(relation[x][y] - Med)
        deter /= order * (order-1) * (Max - Med)
        return deter

    def showStatistics(self):
        """
        Computes digraph statistics like order, size and arc-density.
        """
        #import array
        print('*----- general statistics -------------*')
        nbrcomp = len(self.components())
        nbrstrcomp = len(self.strongComponents())
        actions = [x for x in self.actions]
        relation = self.relation
        order = len(actions)
        size,undeterm,arcDensity = self.sizeSubGraph(actions)
        self.size = size
        self.undeterm = undeterm
        density = self.computeAllDensities(actions)
        self.arcDensity = density['arc']
        outDegrees = self.outDegreesDistribution()
        inDegrees = self.inDegreesDistribution()
        symDegrees = self.symDegreesDistribution()
        nbDepths = self.neighbourhoodDepthDistribution()
        nb = len(nbDepths)
        meanLength = 0.0
        for i in range(nb):
            meanLength += i * nbDepths[i]
        if nbDepths[nb-1] != 0:
            meanLength = 'infinity'
        else:
            meanLength = float(meanLength/order)

        self.meanNeighbourhoodDepth = meanLength

        self.digraphDiameter = self.diameter()

        self.agglomerationCoefficient,self.meanAgglomerationCoefficient = self.agglomerationDistribution()
        # Outranking determinateness
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        deter = Decimal('0.0')
        for x in actions:
            for y in actions:
                if x != y:
                    #print relation[x][y], Med, relation[x][y] - Med
                    deter += abs(relation[x][y] - Med)
        deter /= order * (order-1) * (Max - Med)
        #  output results
        print('for digraph              : <' + str(self.name) + '.py>')
        print('order                    : ', self.order, 'nodes')
        print('size                     : ', self.size, 'arcs')
        print('# undetermined           : ', self.undeterm, 'arcs')
        print('determinateness          : %.2f' % (deter))
        print("arc density              : %.2f" % (density['arc']))
        print("double arc density       : %.2f" % (density['double']))
        print("single arc density       : %.2f" % (density['single']))
        print("absence density          : %.2f" % (density['absence']))
        print("strict single arc density: %.2f" % (density['strictSingle']))
        print("strict absence density   : %.2f" % (density['strictAbsence']))
        print('# components             : ', nbrcomp)
        print('# strong components      : ', nbrstrcomp)
        print('transitivity degree      : %.2f' % (self.computeTransitivityDegree()))

        print('                         : ', list(range(len(outDegrees))))
        print('outdegrees distribution  : ', list(outDegrees))
        print('indegrees distribution   : ', list(inDegrees))
        print('mean outdegree           : %.2f' % (self.computeMeanOutDegree()))
        print('mean indegree            : %.2f' % (self.computeMeanInDegree()))
        print('                         : ', list(range(len(symDegrees))))
        print('symmetric degrees dist.  : ', list(symDegrees))
        print('mean symmetric degree    : %.2f' % (self.computeMeanSymDegree()))

        outgini = self.computeConcentrationIndex(list(range(len(outDegrees))),list(outDegrees))
        ingini = self.computeConcentrationIndex(list(range(len(inDegrees))),list(inDegrees))
        symgini = self.computeConcentrationIndex(list(range(len(symDegrees))),list(symDegrees))
        print('outdegrees concentration index   : %.4f' % (outgini))
        print('indegrees concentration index    : %.4f' % (ingini))
        print('symdegrees concentration index   : %.4f' % (symgini))
        listindex = list(range(order))
        listindex.append('inf')
        print('                                 : ', listindex)
        print('neighbourhood depths distribution: ', list(nbDepths))
        if meanLength != 'infinity':
            print("mean neighbourhood depth         : %.2f " % (meanLength))
        else:
            print('mean neighbourhood length        : ', meanLength)
        print('digraph diameter                 : ', self.digraphDiameter)
        print('agglomeration distribution       : ')
        for i in range(order):
            print(actions[i], end=' ')
            print(": %.2f" % (self.agglomerationCoefficient[i]))
        print("agglomeration coefficient        : %.2f" % (self.meanAgglomerationCoefficient))

    def meanLength(self,Oriented=False):
        """
        Renders the (by default non-oriented) mean neighbourhoor depth of self.
        !!! self.order must be set previously !!!
        """
        nbDepths = self.neighbourhoodDepthDistribution(Oriented)
        nb = len(nbDepths)
        meanLength = 0.0
        for i in range(nb):
            meanLength += i * nbDepths[i]
        if nbDepths[nb-1] != 0:
            meanLength = 'infinity'
        else:
            meanLength = meanLength/float(self.order)
        return meanLength

    def meanDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        inDegrees = self.inDegreesDistribution()
        degrees = []
        nd = len(outDegrees)
        meanDegree = 0.0
        for i in range(nd):
            degrees.append(outDegrees[i]+inDegrees[i])
            meanDegree += i * (max(outDegrees[i],inDegrees[i]))
        if self.size == 0:
            meanDegree = 0
        else:
            meanDegree = meanDegree/float(2 * self.order)
        return meanDegree

    def computeMeanOutDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        nd = len(outDegrees)
        meanOutDegree = 0.0
        for i in range(nd):
            meanOutDegree += i * outDegrees[i]
        if self.size == 0:
            meanOutDegree = 0
        else:
            meanOutDegree = meanOutDegree/float(self.order)
        return meanOutDegree

    def computeMeanInDegree(self):
        """
        Renders the mean indegree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        inDegrees = self.inDegreesDistribution()
        nd = len(inDegrees)
        meanInDegree = 0.0
        for i in range(nd):
            meanInDegree += i * inDegrees[i]
        if self.size == 0:
            meanInDegree = 0
        else:
            meanInDegree = meanInDegree/self.order
        return meanInDegree

    def computeMedianOutDegree(self):
        """
        Renders the median outdegree of self.
        !!! self.size must be set previously !!!
        """
        order = len(self.actions)
        outDegrees = self.outDegreesDistribution()
        nd = len(outDegrees)
        outDegreesList = []
        for d in range(nd):
            for x in range(outDegrees[d]):
                outDegreesList.append(d)
        outDegreesList.sort()
        #print 'outdegrees sorted', outDegreesList
        ndl = len(outDegreesList)
        if ndl % 2 == 0:
            medpos = ndl//2
            medianOutDegree = outDegreesList[medpos]
        else:
            medpos0 = ndl//2
            medpos1 = (ndl + 1)//2
            medianOutDegree =  (outDegreesList[medpos0] + outDegreesList[medpos1])/2
        return medianOutDegree

    def computeMedianSymDegree(self):
        """
        Renders the median symmetric degree of self.
        !!! self.size must be set previously !!!
        """
        symDegrees = self.symDegreesDistribution()
        nd = len(symDegrees)
        symDegreesList = []
        for d in range(nd):
            for x in range(symDegrees[d]):
                symDegreesList.append(d)
        nd = len(symDegrees)
        symDegreesList.sort()
        ndl = len(symDegreesList)
        if ndl % 2 == 0:
            medpos = ndl//2
            medianSymDegree = symDegreesList[medpos]
        else:
            medpos0 = ndl/2
            medpos1 = (ndl + 1)//2
            medianSymDegree =  (symDegreesList[medpos0] + symDegreesList[medpos1])/2
        return medianSymDegree

    def computeMeanSymDegree(self):
        """
        Renders the mean degree of self.
        !!! self.size must be set previously !!!
        """
        order = float(len(self.actions))
        symDegrees = self.symDegreesDistribution()
        nd = len(symDegrees)
        meanSymDegree = 0.0
        for i in range(nd):
            meanSymDegree += i * symDegrees[i]
        if self.size == 0:
            meanSymDegree = 0.0
        else:
            meanSymDegree = meanSymDegree/self.order
        return meanSymDegree

    def diameter(self, Oriented = False):
        """
        Renders the (by default non-oriented) diameter of the digraph instance
        """
        order = len(self.actions)
        nbDepths = self.neighbourhoodDepthDistribution(Oriented)
        nbDepths.reverse()
        if nbDepths[0] != 0:
            diameter = 'infinity'
        else:
            diameter = 0
            for i in range(len(nbDepths)):
                if nbDepths[i+1] != 0:
                    diameter = order - (i+1)
                    break
        return diameter

    def graphDetermination(self):
        """
        Output: average arc determination
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        determ = Decimal("0.0")
        actions = [x for x in self.actions]
        for x in actions:
            for y in actions:
                if x != y:
                    if self.relation[x][y] > Med:
                        determ += self.relation[x][y]
                    else:
                        determ += Max - self.relation[x][y] + Min
        n = self.order * (self.order - 1)
        averageDeterm = determ / Decimal(str(n))
        return  averageDeterm

    def size(self):
        """
        Renders the number of validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        size = 0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] > Med:
                        size += 1
        return size

    def coSize(self):
        """
        Renders the number of non validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        coSize = 0
        for x in actions:
            for y in actions:
                if x != y:
                    if relation[x][y] < Med:
                        coSize += 1
        return coSize

    def sizeSubGraph(self,choice):
        """
        Output: (size, undeterm,arcDensity).
        Renders the arc density of the induced subgraph.
        """
        Med = self.valuationdomain['med']
        relation = self.relation
        order = float(len(choice))
        size = 0
        undeterm = 0
        for x in choice:
            for y in choice:
                if x != y:
                    if relation[x][y] > Med:
                        size += 1
                    if relation[x][y] == Med:
                        undeterm += 1
        if len(choice) < 2:
            arcDensity = 0.0
        else:
            arcDensity = (size * 100.0)/ (order * (order - 1 ))
        return size, undeterm, arcDensity

    def agglomerationDistribution(self):
        """
        Output: aggloCoeffDistribution, meanCoeff
        Renders the distribution of agglomeration coefficients.
        """
        import array
        actions = [x for x in self.actions]
        order = len(actions)
        aggloCoeff = array.array('f', [0] * order)
        meanCoeff = 0.0
        for i in range(order):
            neighborhood = self.gamma[actions[i]][0] | self.gamma[actions[i]][1]
            size, undeterm, aggloCoeff[i] = self.sizeSubGraph(neighborhood)
            meanCoeff += aggloCoeff[i]
        if order == 0:
            meanCoeff = 0.0
        else:
            meanCoeff /= order
        return aggloCoeff, meanCoeff

    def outDegreesDistribution(self):
        """
        Renders the distribution of outdegrees.
        """
        import array
        order = len(self.actions)
        outDegrees = array.array('i', [0] * (order+1))
        for x in self.actions:
            nx = len(self.gamma[x][0])
            outDegrees[nx] += 1
        return outDegrees

    def computeConcentrationIndexTrapez(self,X,N):
        """
        Renders the Gini concentration index of the X serie.
        N contains the partial frequencies.
        Based on the triangles summation formula.
        """
        n = len(X)
        #dg = self.outDegreesDistribution()
        X = list(range(10))
        N = [0,0,0,0,0,0,0,0,0,0,]
        print('Xi ', X, N)
        Q = [0.0 for i in range(n)]
        F = [0.0 for i in range(n)]
        Qsum = 0.0
        for i in range(n):
            Qsum += X[i] * N[i]
        print('Qsum ',Qsum)
        F[0] = float(X[0])/float(n)
        Q[0] = 0.0
        for i in range(1,n,1):
            qi = (X[i] * N[i])/Qsum
            Q[i] += Q[i-1] + qi
            print('Q[i] i ', i, Q[i])
            fi = float(N[i])/n
            F[i] += F[i-1] + fi
            print('i, F[i]', i, F)
        f0 = float(N[0])/float(n)
        gini = 1.0 - (f0*Q[0])
        print('o gini ', gini)
        for i in range(1,n):
            fi = (float(N[i])/float(n))
            gini -= fi * (Q[i-1] + Q[i])
            print('i gini', i, gini)
        return gini

    def computeConcentrationIndex(self,X,N):
        """
        Renders the Gini concentration index of the X serie.
        N contains the partial frequencies.
        Based on the triangle summation formula.
        """
        Qsum = 0.0
        n = 0.0
        r = len(X)
        for i in range(r):
            n += N[i]
            Qsum += X[i] * N[i]
        if Qsum != 0.0:
            Q = [0.0 for i in range(r)]
            F = [0.0 for i in range(r)]
            F[0] = N[0]/n
            Q[0] = (X[0] * N[0])/Qsum
            for i in range(1,r,1):
                qi = (X[i] * N[i])/Qsum
                Q[i] += Q[i-1] + qi
                fi = N[i]/n
                F[i] += F[i-1] + fi
            gini = 0.0
            for i in range(r-1):
                gini += (F[i]*Q[i+1]) - (Q[i]*F[i+1])
        else:
            gini = -1
        return gini

    def inDegreesDistribution(self):
        """
        Renders the distribution of indegrees.
        """
        import array
        order = len(self.actions)
        inDegrees = array.array('i', [0] * (order+1))
        for x in self.actions:
            nx = len(self.gamma[x][1])
            inDegrees[nx] += 1
        return inDegrees

    def symDegreesDistribution(self):
        """
        Renders the distribution of symmetric degrees.
        """
        import array
        order = len(self.actions)
        symDegrees = array.array('i', [0] * ((2*order)+1))
        for x in self.actions:
            nx = len(self.gamma[x][0])+len(self.gamma[x][1])
            symDegrees[nx] += 1
        return symDegrees

    def neighbourhoodDepthDistribution(self, Oriented=False):
        """
        Renders the distribtion of neighbourhood depths.
        """
        import array,copy
        actions = set(self.actions)
        order = len(actions)
        nv = order + 1
        vecNeighbourhoodDepth = array.array('i', [0] * nv)
        for x in actions:
            nbx = 0
            neighbx = set([x])
            restactions = actions - neighbx
            while restactions != set() and nbx < order:
                nbx += 1
                iterneighbx = copy.copy(neighbx)
                for y in iterneighbx:
                    if Oriented:
                        neighbx = neighbx | self.gamma[y][0]
                    else:
                        neighbx = neighbx | self.gamma[y][0] | self.gamma[y][1]
                restactions = actions - neighbx
            if restactions != set():
                vecNeighbourhoodDepth[order] += 1
            else:
                vecNeighbourhoodDepth[nbx] += 1
        return vecNeighbourhoodDepth


    def neighbourhoodCollection(self, Oriented = False, Potential = False):
        """
        Renders the neighbourhood.
        """
        import array,copy
        actions = set(self.actions)
        order = len(actions)
        if Potential:
            weakGamma = self.weakGammaSets()
        neighbourhoods = {}
        for x in actions:
            nbx = 0
            neighbx = set([x])
            restactions = actions - neighbx
            while restactions != set() and nbx < order:
                nbx += 1
                iterneighbx = copy.copy(neighbx)
                for y in iterneighbx:
                    if Potential:
                        if Oriented:
                            neighbx = neighbx | weakGamma[y][0]
                        else:
                            neighbx = neighbx | weakGamma[y][0] | weakGamma[y][1]
                    else:
                        if Oriented:
                            neighbx = neighbx | self.gamma[y][0]
                        else:
                            neighbx = neighbx | self.gamma[y][0] | self.gamma[y][1]
                    restactions = actions - neighbx
            #print 'neighbx', neighbx
            neighbourhoods[x]= neighbx
        return neighbourhoods

    def strongComponents(self, setPotential = False):
        """
        renders the set of strong components of self.
        """
        neighbourhoods = self.neighbourhoodCollection(Oriented = True, Potential = setPotential)
        strongComponents = set()
        for x in self.actions:
            componentx = set([x])
            for y in neighbourhoods[x]:
                if x in neighbourhoods[y]:
                    componentx = componentx | set([y])
            strongComponents = strongComponents | set([frozenset(componentx)])
        return strongComponents

    def showMIS(self,withListing=True):
        """
        Prints all maximal independent choices
           Result in self.misset.
        """
        import time
        print('*---  Maximal independent choices ---*')
        t0 = time.time()
        self.misset = set()
        actions = set(self.actions)
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.MISgen(actions,frozenset()):
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.misset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.misset')

    def showMinDom(self,withListing=True):
        """
        Prints all minimal dominant choices:
           Result in self.domset.
        """
        import time
        print('*--- Computing minimal dominant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        cover = {}
        for x in actions:
            cover[x]=self.gamma[x][1] | set([x])
        dom1 = (frozenset(list(actions)),cover)
        #print dom1
        self.minset = set()
        self.minhistory = set()
        for choice in self.minimalChoices(dom1):
            pass
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.minset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.minset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('iteration history: ', len(self.minhistory))
        self.domset = self.minset.copy()
        print('Results in self.domset')

    def showMinAbs(self,withListing=True):
        """
        Prints minimal absorbent choices:
           Result in self.absset.
        """
        import time
        print('*--- Computing minimal absorbent choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        cover = {}
        for x in actions:
            cover[x]=self.gamma[x][0] | set([x])
        abs1 = (frozenset(list(actions)),cover)
        print(abs1)
        self.minset = set()
        self.minhistory = set()
        for choice in self.minimalChoices(abs1):
            pass
        n = len(actions)
        v = [0 for i in range(n+1)]
        for choice in self.minset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        t1 = time.time()
        print('number of solutions: ', len(self.minset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('iteration history: ', len(self.minhistory))
        self.absset = self.minset.copy()
        print('Results in self.absset')

    def showMaxDomIrred(self,withListing=True):
        """Computing maximal +irredundant choices:
           Result in self.domirset."""
        import time
        print('*--- Computing maximal +irredundant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        self.domirset = set()
        for choice in self.plusirredundant(actions):
            add = 1
            mirsetit = self.domirset.copy()
            for mir in mirsetit:
                if mir < choice:
                    self.domirset.remove(mir)
                else:
                    if choice <= mir:
                        add = 0
                        break
            if add == 1:
                self.domirset.add(frozenset(choice))
        t1 = time.time()
        n = len(self.actions)
        v = [0 for i in range(n+1)]
        for choice in self.domirset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        print('number of solutions: ', len(self.domirset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.domirset')

    def showMaxAbsIrred(self,withListing=True):
        """Computing maximal -irredundant choices:
           Result in self.absirset."""
        import time
        print('*--- Computing maximal -irredundant choices ---*')
        t0 = time.time()
        actions = set(self.actions)
        self.absirset = set()
        for choice in self.absirredundant(actions):
            add = 1
            mirsetit = self.absirset.copy()
            for mir in mirsetit:
                if mir < choice:
                    self.absirset.remove(mir)
                else:
                    if choice <= mir:
                        add = 0
                        break
            if add == 1:
                self.absirset.add(frozenset(choice))
        t1 = time.time()
        n = len(self.actions)
        v = [0 for i in range(n+1)]
        for choice in self.absirset:
            v[len(choice)] += 1
            if withListing:
                print(list(choice))
        print('number of solutions: ', len(self.absirset))
        print('cardinality distribution')
        print('card.: ', list(range(n+1)))
        print('freq.: ', v)
        print('execution time: %.5f sec.' % (t1-t0))
        print('Results in self.absirset')


    def showPreKernels(self,withListing=True):
        """
        Printing dominant and absorbent preKernels
        Result in self.dompreKernels and self.abspreKernels
        """
        import time
        print('*--- Computing preKernels ---*')
        actions = set(self.actions)
        n = len(actions)
        self.dompreKernels = set()
        self.abspreKernels = set()
        t0 = time.time()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                self.dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                self.abspreKernels.add(choice[0][0])
        t1 = time.time()
        if withListing:
            print('Dominant preKernels :')
            for choice in self.dompreKernels:
                print(list(choice))
                print('   independence : ', self.intstab(choice))
                print('   dominance    : ', self.domin(choice))
                print('   absorbency   : ', self.absorb(choice))
                print('   covering     :  %.3f' % self.averageCoveringIndex(choice, direction='out'))
            print('Absorbent preKernels :')
            for choice in self.abspreKernels:
                print(list(choice))
                print('   independence : ', self.intstab(choice))
                print('   dominance    : ', self.domin(choice))
                print('   absorbency   : ', self.absorb(choice))
                print('   covering     :  %.3f' % self.averageCoveringIndex(choice, direction='in'))
        print('*----- statistics -----')
        print('graph name: ', self.name)
        print('number of solutions')
        print(' dominant kernels : ', len(self.dompreKernels))
        print(' absorbent kernels: ', len(self.abspreKernels))
        print('cardinality frequency distributions')
        print('cardinality     : ', list(range(n+1)))
        v = [0 for i in range(n+1)]
        for ch in self.dompreKernels:
            v[len(ch)] += 1
        print('dominant kernel : ',v)
        v = [0 for i in range(n+1)]
        for ch in self.abspreKernels:
            v[len(ch)] += 1
        print('absorbent kernel: ',v)
        print('Execution time  : %.5f sec.' % (t1-t0))
        print('Results in sets: dompreKernels and abspreKernels.')

    def computePreKernels(self):
        """
        computing dominant and absorbent preKernels
        Result in self.dompreKernels and self.abspreKernels
        """
        actions = set(self.actions)
        n = len(actions)
        dompreKernels = set()
        abspreKernels = set()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                abspreKernels.add(choice[0][0])
        self.dompreKernels = dompreKernels
        self.abspreKernels = abspreKernels


    def generateDomPreKernels(self):
        """
        Generate all dominant prekernels from independent
        choices generator.
        """
        actions = set(self.actions)
        for item in self.independentChoices(self.singletons()):
            choice = item[0][0]
            gammaDomChoice = item[0][1]
            restactions = actions - choice
            if restactions <= gammaDomChoice:
                yield choice

    def generateAbsPreKernels(self):
        """
        Generate all absorbent prekernels from independent
        choices generator.
        """
        actions = set(self.actions)
        for item in self.independentChoices(self.singletons()):
            choice = item[0][0]
            gammaAbsChoice = item[0][2]
            restactions = actions - choice
            if restactions <= gammaAbsChoice:
                yield choice

    def components(self):
        """Renders the list of connected components."""
        A = {}
        for x in self.actions:
            A[x] = 0
        ncomp = 1
        ConComp = []
        for x in A:
            Comp = set()
            if A[x] == 0:
                A[x] = ncomp
                Comp = Comp | set([x])
                Comp = Comp | self.collectcomps(x, A, ncomp)
            if len(Comp) > 0:
                ncomp = ncomp + 1
                ConComp = ConComp + [Comp]
        return ConComp

    def showComponents(self):
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1

    def collectcomps(self, x, A, ncomp):
        """Recursive subroutine of the components method."""
        Comp = set()
        Nx = self.gamma[x][0] | self.gamma[x][1]
        for y in Nx:
            if A[y] == 0:
                A[y] = ncomp
                Comp.add(y)
                Comp = Comp | self.collectcomps(y, A, ncomp)
        return Comp

    def outDegrees(self):
        """
        renders the median cut outdegrees
        """
        outDegrees ={}
        for x in self.actions:
            outDegrees[x] = len(self.gamma[x][0])
        return outDegrees

    def inDegrees(self):
        """
        renders the median cut indegrees
        """
        inDegrees ={}
        for x in self.actions:
            inDegrees[x] = len(self.gamma[x][1])
        return inDegrees

    def bestRanks(self):
        """
        renders best possible ranks from indegrees account
        """
        bestRanks = {}
        inDegrees = self.inDegrees()
        for x in self.actions:
            bestRanks[x] = inDegrees[x] + 1
        return bestRanks

    def worstRanks(self):
        """
        renders worst possible ranks from outdegrees account
        """
        worstRanks = {}
        outDegrees = self.outDegrees()
        for x in self.actions:
            worstRanks[x] = self.order - outDegrees[x]
        return worstRanks


    def gammaSets(self):
        """ Renders the dictionary of neighborhoods {node: (dx,ax)}"""
        gamma = {}
        for x in self.actions:
            dx = self.dneighbors(x)
            ax = self.aneighbors(x)
            gamma[x] = (dx,ax)
        return gamma

    def weakGammaSets(self):
        """ Renders the dictionary of neighborhoods {node: (dx,ax)}"""
        weakGamma = {}
        for x in self.actions:
            dx = self.weakDneighbors(x)
            ax = self.weakAneighbors(x)
            weakGamma[x] = (dx,ax)
        return weakGamma

    ## def quasiGammaSets(self,Epsilon=None):
    ##     """ Renders the dictionary of neighborhoods {node: (dx,ax)}"""
    ##     if Epsilon == None:
    ##         Threshold = 0.1*(self.valuationdomain['max']-self.valuationdomain['min'])
    ##     quasiGamma = {}
    ##     for x in self.actions:
    ##         dx = self.quasiDneighbors(x)
    ##         ax = self.quasiAneighbors(x)
    ##         quasiGamma[x] = (dx,ax)
    ##     return quasiGamma/home/bisi/Desktop/CBCVS/Digraph/digraphs.py

    def notGammaSets(self):
        """ Renders the dictionary of not neighborhoods {node: (dx,ax)} """
        notGamma = {}
        for x in self.actions:
            dx = self.notdneighbors(x)
            ax = self.notaneighbors(x)
            notGamma[x] = (dx,ax)
        return notGamma

    def weakDneighbors(self,node):
        """ Renders the set of dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[node][a] >= Med:
                nb.add(a)
        return nb

    def dneighbors(self,node):
        """ Renders the set of dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[node][a] > Med:
                nb.add(a)
        return nb

    def notdneighbors(self,node):
        """ Renders the set of not dominated out-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if a != node:
                if self.relation[node][a] < Med:
                    nb.add(a)
        return nb

    def aneighbors(self,node):
        """ Renders the set of absorbed in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[a][node] > Med:
                nb.add(a)
        return nb

    def weakAneighbors(self,node):
        """ Renders the set of absorbed in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if self.relation[a][node] >= Med:
                nb.add(a)
        return nb

    def notaneighbors(self,node):
        """ Renders the set of absorbed not in-neighbors of a node."""
        Med = self.valuationdomain['med']
        nb = set()
        for a in self.actions:
            if a != node:
                if self.relation[a][node] < Med:
                    nb.add(a)
        return nb

    def singletons(self):
        """list of singletons and neighborhoods
           [(singx1, +nx1, -nx1, not(+nx1 or -nx1)),.... ]"""
        s = []
        for x in self.actions:
            indep = set(self.actions) - (self.gamma[x][0] | self.gamma[x][1])
            s = s + [(frozenset([x]),self.gamma[x][0],self.gamma[x][1],indep)]
        return s


    def MISgen(self,S,I):
        """
        generator of maximal independent choices
        S ::= remaining nodes; I ::= current independent choice
        inititalize: self.MISgen(self.actionscopy(),set())
        (voir Byskov 2004)
        """
        if S == set():
            add = 1
            self.missetit = self.misset.copy()
            for mis in self.missetit:
                if mis < I:
                    self.misset.remove(mis)
                else:
                    if I <= mis:
                        add = 0
                        break
            if add == 1:
                self.misset = self.misset | frozenset([I])
                yield I
        else:
            v = S.pop()
            Sv = S - (self.gamma[v][0] | self.gamma[v][1])
            Iv = I | set([v])
            for choice in self.MISgen(Sv,Iv):
                yield choice
            for choice in self.MISgen(S,I):
                yield choice

    def independentChoices(self,U):
        """
         Generator for all independent choices with neighborhoods
         of a bipolar valued digraph.
         Initiate with U = self.singletons().
         Yields [(independent choice, domnb, absnb, indnb)].
        """
        if U == []:
            yield [(frozenset(),set(),set(),set(self.actions))]
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

    def coveringIndex(self,choice,direction="out"):
        """
        Renders the covering index of a given choice in a set of objects,
        ie the minimum number of choice members that cover each
        non selected object.
        """
        from decimal import Decimal
        actions = set([x for x in self.actions])
        nonSelected = actions - choice
        n = len(choice)
        index = n
        for x in nonSelected:
            if direction == 'out':
                index = min( index, len(self.gamma[x][1] & choice) )
            else:
                index = min( index, len(self.gamma[x][0] & choice) )
        if n > 0:
            return Decimal(str(index))/Decimal(str(n))
        else:
            return Decimal("0.0")

    def averageCoveringIndex(self,choice,direction="out"):
        """
        Renders the average covering index of a given choice in a set of objects,
        ie the average number of choice members that cover each
        non selected object.
        """
        from decimal import Decimal
        choice = set(choice)
        actions = set([x for x in self.actions])
        nonSelected = actions - choice
        n = len(choice)
        m = len(nonSelected)
        index = 0
        for x in nonSelected:
            if direction == 'out':
                index += len(self.gamma[x][1] & choice)
            else:
                index += len(self.gamma[x][0] & choice)
        if n > 0 and m > 0:
            return ( Decimal(str(index))/Decimal(str(m)) ) / Decimal(str(n))
        elif n > 0:
            return Decimal("1.0")
        else:
            return Decimal("0.0")

    def zoomValuation(self,zoomFactor=1.0):
        """
        Zooms in or out, depending on the value of the zoomFactor provided,
        the bipolar valuation of a digraph.
        """

        zoomFactor = Decimal(str(zoomFactor))

        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']

        newMin = oldMin * zoomFactor
        newMax = oldMax * zoomFactor
        newMed = oldMed * zoomFactor

        actions = self.actions
        oldRelation = self.relation
        newRelation = {}
        for x in actions:
            newRelation[x] = {}
            for y in actions:
                newRelation[x][y] = oldRelation[x][y] * zoomFactor

        # install new values in self
        self.valuationdomain['max'] = newMax
        self.valuationdomain['min'] = newMin
        self.valuationdomain['med'] = newMed

        self.relation = newRelation.copy()


    def recodeValuation(self,newMin=-10.0,newMax=10.0,Debug=False):
        """
        Recodes the characteristic valuation domain according
        to the parameters given.
        """
        from copy import deepcopy
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']

        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)

        newMin = Decimal(str(newMin))
        newMax = Decimal(str(newMax))
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))

        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)

        actions = self.actions
        oldrelation = self.relation
        newrelation = {}
        for x in actions:
            newrelation[x] = {}
            for y in actions:
                if oldrelation[x][y] == oldMax:
                    newrelation[x][y] = newMax
                elif oldrelation[x][y] == oldMin:
                    newrelation[x][y] = newMin
                elif oldrelation[x][y] == oldMed:
                    newrelation[x][y] = newMed
                else:
                    newrelation[x][y] = newMin + ((self.relation[x][y] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(x,y,self.relation[x][y],newrelation[x][y])
        # install new values in self
        self.valuationdomain['max'] = newMax
        self.valuationdomain['min'] = newMin
        self.valuationdomain['med'] = newMed
        self.valuationdomain['hasIntegerValuation'] = False

        self.relation = deepcopy(newrelation)

    def dominantChoices(self,S):
        """
        Generates all minimal dominant choices of a bipolar valued digraph.
           Initiate with S = self.actions,copy().
        """
        Med = self.valuationdomain['med']
        add = 1
        domsetit = self.domset.copy()
        for dom in domsetit:
            if S < dom:
                self.domset.remove(dom)
            else:
                if S >= dom:
                    add = 0
                    break
        if add == 1:
            self.domset = self.domset | set([frozenset(S)])
            yield S
            for x in S:
                S1 = S - set([x])
                if self.domin(S1) > Med:
                    for choice in self.dominantChoices(S1):
                        yield choice

    def minimalChoices(self,S):
        """
        Generates all dominant or absorbent choices of a bipolar
        valued digraph.

        Initiate with:
           S = (actions, dict of dominant or absorbent closed neighborhoods), see showMinDom and showMinAbs methods.
        """
        if S[0] not in self.minhistory:
            self.minhistory = self.minhistory | set([frozenset(S[0])])
            add = True
            minsetit = self.minset.copy()
            for minch in minsetit:
                if S[0] < minch:
                    self.minset.remove(minch)
                else:
                    if S[0] >= minch:
                        add = False
                        break
            if add:
                self.minset = self.minset | set([frozenset(S[0])])
                yield S
            for x in S[0]:
                Sxchoice = S[0] - set([x])
                Sx = (Sxchoice,{})
                covering = True
                for cover in S[1]:
                    coverx = S[1][cover] - set([x])
                    if coverx == set():
                        covering = False
                        break
                    Sx[1][cover] = coverx
                if covering:
                    for choice in self.minimalChoices(Sx):
                        yield choice

    def absorbentChoices(self,S):
        """
        Generates all minimal absorbent choices of a bipolar valued digraph.
        """
        Med = self.valuationdomain['med']
        add = 1
        abssetit = self.absset.copy()
        for absch in abssetit:
            if S < absch:
                self.absset.remove(absch)
            else:
                if S >= absch:
                    add = 0
                    break
        if add == 1:
            self.absset = self.absset | set([frozenset(S)])
            yield S
            for x in S:
                S1 = S - set([x])
                if self.absorb(S1) > Med:
                    for choice in self.absorbentChoices(S1):
                        yield choice

    def kChoices(self,A,k):
        """
        Renders all choices of length k from set A
        """
        import copy
        if k == 0:
            yield set()
        else:
            while len(A) > 0:
                x = A.pop()
                Ax = copy.copy(A)
                k1 = k - 1
                for ch in self.kChoices(Ax,k1):
                    yield ch | set([x])


    def powerset(self,U):
        """
        Generates all subsets of a set.
        """
        if U == set():
            yield set()
        else:
            U1 = set(U)
            x = U1.pop()
            for S in self.powerset(U1):
                yield S
                yield S | set([x])

    def plusirredundant(self,U):
        """
        Generates all +irredundant choices of a digraph.
        """
        Med = self.valuationdomain['med']
        if U == set():
            yield set()
        else:
            x = U.pop()
            for S in self.plusirredundant(U):
                yield S
                Sx = S | set([x])
                if self.domirred(Sx) > Med:
                    yield Sx

    def absirredundant(self,U):
        """
        Generates all -irredundant choices of a digraph.
        """
        Med = self.valuationdomain['med']
        if U == set():
            yield set()
        else:
            x = U.pop()
            for S in self.absirredundant(U):
                yield S
                S1 = S | set([x])
                if self.absirred(S1) > Med:
                    Sx = S | set([x])
                    yield Sx

    def intstab(self,choice):
        """
        Computes the independence degree of a choice.
        """
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        relation = self.relation
        deg = Min
        for a in choice:
            for b in choice:
                x = relation[a][b]
                if x > deg and a != b:
                    deg = x
        res = Max - deg + Min
        return res



    def domin(self,choice):
        """
        Renders the dominance degree of a choice.
        """
        deg = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        restactions = set(self.actions) - choice
        for a in restactions:
            dega = Min
            for b in choice:
                x = self.relation[b][a]
                if x > dega:
                    dega = x
            if dega < deg:
                deg = dega
        return deg

    def absorb(self,choice):
        """
        Renders the absorbency degree of a choice.
        """
        deg = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        restactions = set(self.actions) - choice
        for a in restactions:
            dega = Min
            for b in choice:
                x = self.relation[a][b]
                if x > dega:
                    dega = x
            if dega < deg:
                deg = dega
        return deg

    def domirred(self,choice):
        """
        Renders the crips +irredundance degree of a choice.
        """
        Med = self.valuationdomain['med']
        irred = 1
        if len(choice) > 1:
            for x in choice:
                if self.domirredx(choice,x) < Med:
                    irred = 0
                    break
        if irred == 1:
            return self.valuationdomain['max']
        else:
            return self.valuationdomain['min']

    def domirredval(self,choice,relation):
        """
        Renders the valued +irredundance degree of a choice.
        """
        #import array
        actions = self.actions
        n = len(actions)
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        Max = Decimal(str(self.valuationdomain['max']))
        for x in actions:
            relation[x][x] = Max
        result = Max
        for x in choice:
            nbclx = self.readabsvector(x,relation)
            nbclchoice = [Min for i in actions]
            restchoice = set(choice)
            restchoice.remove(x)
            for y in restchoice:
                nbcly = self.readabsvector(y,relation)
                nbclchoice = [max(nbclchoice[i],nbcly[i]) for i in range(n)]
            resultx = max([min(nbclx[i],self.contra(nbclchoice)[i]) for i in range(n)])
            result = min(result, resultx)
        return result

    def domirredx(self,choice,x):
        """
        Renders the crips +irredundance degree of node x in a choice.
        """
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        nx = self.gamma[x][0] | set([x])
        chx = choice - set([x])
        ny = set()
        for y in chx:
            ny = ny | self.gamma[y][0] | set([y])
        nxpriv = nx - ny
        if nxpriv == set():
            return Min
        else:
            return Max

    def absirredval(self,choice,relation):
        """
        Renders the valued -irredundance degree of a choice.
        """
        #import array
        actions = self.actions
        n = len(actions)
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        for x in actions:
            relation[x][x] = Max
        result = Max
        for x in choice:
            nbclx = self.readdomvector(x,relation)
            nbclchoice = [Decimal(str(Min)) for i in actions]
            restchoice = set(choice)
            restchoice.remove(x)
            for y in restchoice:
                nbcly = self.readdomvector(y,relation)
                nbclchoice = [max(nbclchoice[i],nbcly[i]) for i in range(n)]
            resultx = max([min(nbclx[i],self.contra(nbclchoice)[i]) for i in range(n)])
            result = min(result, resultx)
        return result

    def absirred(self,choice):
        """
        Renders the crips -irredundance degree of a choice.
        """
        Med = self.valuationdomain['med']
        irred = 1
        if len(choice) > 1:
            for x in choice:
                if self.absirredx(choice,x) < Med:
                    irred = 0
                    break
        if irred == 1:
            return self.valuationdomain['max']
        else:
            return self.valuationdomain['min']

    def absirredx(self,choice,x):
        """Computes the crips -irredundance degree of node x in a choice."""
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        nx = self.gamma[x][1] | set([x])
        chx = choice - set([x])
        ny = set()
        for y in chx:
            ny = ny | self.gamma[y][1] | set([y])
        nxpriv = nx - ny
        if nxpriv == set():
            return Min
        else:
            return Max

    def save(self,fileName='tempdigraph',option=None,Decimal=True):
        """Persistent storage of a Digraph class instance in the form of
            a python source code file"""
        print('*--- Saving digraph in file: <' + fileName + '.py> ---*')
        actions = self.actions
        relation = self.relation
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# automatically generated random irreflexive digraph\n')
        fo.write('actionset = [\n')
        for x in actions:
            fo.write('\'' + str(x) + '\',\n')
        fo.write(']\n')
        try:
            hasIntegerValuation = self.valuationdomain['hasIntegerValuation']
        except KeyError:
            hasIntegerValuation = not Decimal
        if not hasIntegerValuation:
            fo.write('valuationdomain = {\'hasIntegerValuation\': False, \'min\': Decimal("'+str(Min)+'"),\'med\': Decimal("'+str(Med)+'"),\'max\': Decimal("'+str(Max)+'")}\n')
        else:
            fo.write('valuationdomain = {\'hasIntegerValuation\': True, \'min\': '+str(Min)+',\'med\': '+str(Med)+',\'max\': '+str(Max)+'}\n')

        fo.write('relation = {\n')
        for x in actions:
            fo.write('\'' + str(x) + '\': {\n')
            for y in actions:
                if not hasIntegerValuation:
                    fo.write('\'' + str(y) + '\': Decimal("' + str(relation[x][y]) + '"),\n')
                else:
                    fo.write('\'' + str(y) + '\':' + str(relation[x][y]) + ',\n')
            fo.write('},\n')
        fo.write( '}\n')
        if option == 'withAutomorphismGenerators':
            fo.write('reflections = {\n')
            for ga in self.reflections:
                fo.write('\' '+str(ga)+'\':'+str(self.reflections[ga])+',\n')
            fo.write('}\n')
            fo.write('permutations = {\n')
            for ga in self.permutations:
                fo.write("\'"+str(ga)+"\': {\n")
                for p in self.permutations[ga]:
                    fo.write('\''+str(p)+'\': \''+str(self.permutations[ga][p])+'\',\n')
                fo.write('},\n')
            fo.write('}\n')
        fo.close()

    def chordlessPaths(self,Pk,n2,Odd=False,Comments=False,Debug=False):
        """
        New procedure from Agrum study April 2009
        recursive chordless path extraction strating from path
        Pk = [n2, ...., n1] and ending in node n2.
        Optimized with marking of visited chordless P1s.
        """
        if Comments:
            Debug = True
        n1 = Pk[-1]
        self.visitedArcs.add((n1,n2))
        self.visitedArcs.add((n2,n1))
        med = self.valuationdomain['med']
        if self.relation[n1][n2] > med and self.relation[n2][n1] <= med:
            detectedChordlessPath = True
            #self.visitedArcs.add((n1,n2))
            #OddFlag = True
            if Debug:
                print('len(Pk)', Pk, len(Pk), len(Pk) % 2)

            if Odd:
                if (len(Pk) % 2) != 1:
                    OddFlag = False
                else:
                    OddFlag = True
            else:
                OddFlag = True

            if Debug:
                print('OddFlag: ', OddFlag)
            if OddFlag:
                #Pk.append(n2)
                self.xCC.append(Pk)
                if Debug:
                    print('Chordless circuit certificate -->>> ', Pk)
        else:
            detectedChordlessPath = False
            NBn1 = set(self.gamma[n1][0]-self.gamma[n1][1])
            while NBn1 != set():
                n = NBn1.pop()
                if (n1,n) not in self.visitedArcs and (n,n1) not in self.visitedArcs:
                    P = list(Pk)
                    noChord = True
                    for x in P[:-1]:
                        ## if x == n1:
                        ##     if self.relation[n][x] > med:
                        ##         noChord = False
                        ## elif x == n2:
                        if x == n2:
                            if self.relation[x][n] > med:
                                noChord = False
                                break
                        else:
                            if self.relation[x][n] > med or self.relation[n][x] > med:
                                noChord = False
                                break
                    if noChord:
                        P.append(n)
                        if Debug:
                            print('P,n2',P,n2)
                        if self.chordlessPaths(P,n2,Odd,Comments,Debug):
                            detectedChordlessPath = True
            #self.visitedArcs.add((n1,n2))
            if Debug:
                print('No further chordless path from ',n1,' to ', n2)
        return detectedChordlessPath

    def detectChordlessPath(self,Pk,n2,Comments=False,Debug=False):
        """
        New procedure from Agrum study April 2009
        recursive chordless path extraction strating from path
        Pk = [n2, ...., n1] and ending in node n2.
        Optimized with marking of visited chordless P1s.
        """
        if Comments:
            Debug = True
        n1 = Pk[-1]
        self.visitedArcs.add((n1,n2))
        self.visitedArcs.add((n2,n1))
        med = self.valuationdomain['med']

        if self.relation[n1][n2] > med and self.relation[n2][n1] <= med:
            Detected = True
            if Debug:
                print('Chordless circuit certificate -->>> ', Pk)
        else:
            Detected = False
            NBn1 = set(self.gamma[n1][0]-self.gamma[n1][1])
            while NBn1 != set():
                n = NBn1.pop()
                if (n1,n) not in self.visitedArcs and (n,n1) not in self.visitedArcs:
                    P = list(Pk)
                    noChord = True
                    for x in P[:-1]:
                        if x == n2:
                            if self.relation[x][n] > med:
                                noChord = False
                                break
                        else:
                            if self.relation[x][n] > med or self.relation[n][x] > med:
                                noChord = False
                                break
                    if noChord:
                        P.append(n)
                        if Debug:
                            print('P,n2',P,n2)
                        Detected = self.detectChordlessPath(P,n2,Comments,Debug)
                if Detected:
                        break
        return Detected

    def detectCppChordlessCircuits(self,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits detection
        exchange arguments with external temporary files.
        Returns a boolean value
        """
        import os
        from tempfile import mkstemp
        fd, tempFileName = mkstemp()
        fo = os.fdopen(fd,'w')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        fo.write('%d %d\n' % (i+1,j+1))
        fo.close()

        resultFile = tempFileName+'.py'
        if os.path.exists('/usr/local/bin/detectChordlessCircuits'):
            os.system('/usr/local/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/opt/local/bin/detectChordlessCircuits'):
            os.system('/opt/local/bin/detectChordlessCircuits ' + tempFileName + ' ' + resultFile)
        else:
            print('Error: detectChordlessCircuits binary could not be found !!!')
        exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'))
        circuits = locals()['circuitsList']
        if circuits == []:
            Detected = False
        else:
            Detected = True
        if Debug:
            print(resultFile)
            print(locals()['circuitsList'])
            if Detected:
                print('A chordless circuit has been detected !')
            else:
                print('No chordless circuit has been detected !')
            print('certificate: ', circuits)

        return Detected

    def computeCppInOutPipingChordlessCircuits(self,Odd=False,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits enumeration
        exchange arguments with external temporary files
        """
        import os
        from subprocess import Popen,PIPE

        if os.path.exists('/usr/local/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/usr/local/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        elif os.path.exists('/opt/local/bin/enumChordlessCircuitsInOutPiping'):
            p = Popen(args=['/opt/local/bin/enumChordlessCircuitsInOutPiping'],stdin=PIPE,stdout=PIPE)
        else:
            print('Error: executable enumChordlessCircuitsInOutPiping not found !!!')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        inputString = ''
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        inputString += '%d %d \n' % (i+1,j+1)
        circuits = eval(p.communicate(input=inputString.encode('utf-8'))[0])
        if Debug:
            print(circuits)
        result = []
        for x in circuits:
            # !! a circuit has a length n + 1 !!
            if Odd:
                r = len(x) % 2
                ## if Debug:
                ##     print x, r
                if r != 1:
                    oddCircuit = []
                    for ino in x[:-1]:
                        oddCircuit.append(actions[ino-1])
                    result.append( ( oddCircuit, frozenset(oddCircuit) ) )
            else:
                allCircuit = []
                for ino in x[:-1]:
                    allCircuit.append(actions[ino-1])
                result.append( ( allCircuit, frozenset(allCircuit) ) )
        self.circuitsList = result
        return result

    def computeCppChordlessCircuits(self,Odd=False,Debug=False):
        """
        python wrapper for the C++/Agrum based chordless circuits enumeration
        exchange arguments with external temporary files
        """
        import os
        from tempfile import mkstemp
        fd, tempFileName = mkstemp()
        fo = os.fdopen(fd,'w+b')
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        inputString = ''
        for i,x in enumerate(actions):
            for j,y in enumerate(actions):
                if i != j:
                    if relation[x][y] > Med:
                        inputString += '%d %d \n' % (i+1,j+1)
        fo.write(inputString.encode('utf-8'))
        fo.close()
        ## if Debug:
        ##     print 'see file: ', tempFileName
        resultFile = tempFileName+'.py'
        if os.path.exists('/usr/local/bin/enumChordlessCircuits'):
            os.system('/usr/local/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        elif os.path.exists('/opt/local/bin/enumChordlessCircuits'):
            os.system('/opt/local/bin/enumChordlessCircuits ' + tempFileName + ' ' + resultFile)
        else:
            print('Error: enumChordlessCircuits binary not found !!!')
        exec(compile(open(str(resultFile)).read(), str(resultFile), 'exec'))
        circuits = locals()['circuitsList']
        if Debug:
            print(resultFile)
            print(locals()['circuitsList'])
        result = []
        for x in circuits:
            # !! a circuit has a length n + 1 !!
            if Odd:
                r = len(x) % 2
                ## if Debug:
                ##     print x, r
                if r != 1:
                    oddCircuit = []
                    for ino in x[:-1]:
                        oddCircuit.append(actions[ino-1])
                    result.append( ( oddCircuit, frozenset(oddCircuit) ) )
            else:
                allCircuit = []
                for ino in x[:-1]:
                    allCircuit.append(actions[ino-1])
                result.append( ( allCircuit, frozenset(allCircuit) ) )
        self.circuitsList = result
        return result

    def computeChordlessCircuits(self,Odd=False,Comments=False,Debug=False):
        """
        Renders the set of all chordless odd circuits detected in a digraph.
        Result (possible empty list) stored in <self.circuitsList>
        holding a possibly empty list tuples with at position 0 the
        list of adjacent actions of the circuit and at position 1
        the set of actions in the stored circuit.
        """
        #import copy
        if Comments:
            if Odd:
                print('*--- chordless odd circuits ---*')
            else:
                print('*--- chordless circuits ---*')

        actionsList = list(self.actions)
        self.visitedArcs = set()
        chordlessCircuits = []

        for x in actionsList:
            P = [x]
            if Comments:
                print('Starting from ', x)
            self.xCC = []
            if self.chordlessPaths(P,x,Odd,Comments,Debug):
                chordlessCircuits += self.xCC
        self.chordlessCircuits = chordlessCircuits
        if Comments:
            print('result:', len(self.chordlessCircuits), 'circuit(s)')
            print(self.chordlessCircuits)

        circuitsList = []
        for x in self.chordlessCircuits:
            circuitsList.append( (x,frozenset(x)) )
        self.circuitsList = circuitsList
        return circuitsList

    def detectChordlessCircuits(self,Comments=False,Debug=False):
        """
        Detects a chordless circuit in a digraph.
        Returns a Boolean
        """
        if Comments:
            print('* ---- detecting a chordless circuit, the case given. ----*')

        actionsList = list(self.actions)
        self.visitedArcs = set()
        Detected = False

        for x in actionsList:
            P = [x]
            if Comments:
                print('Starting from ', x)
            self.xCC = []
            if self.detectChordlessPath(P,x,Comments,Debug):
                Detected = True
                break
        if Comments:
            if Detected:
                print('A chordless circuit has been detected !')
            else:
                print('No chordless circuit has been detected !')

        return Detected


    def showCircuits(self):
        """
        show methods for chordless circuits in CocaGraph
        """
        print('*---- Chordless circuits ----*')
        try:
            for (circList,circSet) in self.circuitsList:
                deg = self.circuitMinCredibility(circSet)
                print(circList, ', credibility :', deg)
            print('%d circuits.' % (len(self.circuitsList)))
        except:
            print('No circuits computed. Run computeChordlessCircuits()!')


    def showChordlessCircuits(self):
        """
        show methods for chordless circuits in CocaGraph
        """
        print('*---- Chordless circuits ----*')
        try:
            for (circList,circSet) in self.circuitsList:
                deg = self.circuitMinCredibility(circSet)
                print(circList, ', credibility :', deg)
            print('%d circuits.' % (len(self.circuitsList)))
        except:
            print('No circuits computed. Run computeChordlessCircuits()!')

    def minimalValuationLevelForCircuitsElimination(self,Odd=True,Debug=False,Comments=False):
        """
        renders the minimal valuation level <lambda> that eliminates all
        self.circuitsList stored odd chordless circuits from self.

        .. warning::

            The <lambda> level polarised may still contain newly appearing chordless odd circuits !

        """
        # try:
        #     circuitslist = self.circuitslist
        # except:
        self.computeChordlessCircuits(Odd=Odd,Comments=Debug)
        circuitsList = self.circuitsList
        Med = self.valuationdomain['med']
        qualmaj = Med
        oddCircuitsList = [cc for cc in circuitsList if (len(cc[0])%2 == 1)]
        if Comments:
            print('Number of chordless circuits: ', len(circuitsList))
            print(circuitsList)
            print('Number of chordless odd circuits: ', len(oddCircuitsList))
            print(oddCircuitsList)
        for cc in circuitsList:
            circuit = cc[0]
            if Debug:
                print(circuit)
            ccqualmaj = self.circuitMinCredibility(circuit)
            ## n = len(circuit)
            ## for i in range(n-1):
            ##     x = cc[0][i]
            ##     y = cc[0][i+1]
            ##     if Debug:
            ##         print x, y, self.relation[x][y],y,x,self.relation[y][x]
            ##     if self.relation[x][y] > Med:
            ##         if self.relation[x][y] < ccqualmaj:
            ##             ccqualmaj = self.relation[x][y]
            ## else:
            ##     if self.relation[y][x] < Med:
            ##         if abs(self.relation[y][x]) < ccqualmaj:
            ##             ccqualmaj = abs(self.relation[y][x])
            if Debug:
                print('==>>', circuit, ccqualmaj)
            qualmaj = max(qualmaj,ccqualmaj)
        if Debug or Comments:
            # if Odd:
            #     print('Number of chordless odd circuits: ', len(oddCircuitsList))
            # else:
            #     print('Number of chordless circuits: ', len(circuitsList))
            print('Minimal cutting level for eliminating them: %.3f' % qualmaj)
        return qualmaj

    ## def minimalValuationLevelForCircuitsEliminationOld(self,Debug=False):
    ##     """
    ##     renders the minimal valuation level <lambda> that eliminates all
    ##     self.circuitsList stored odd chordless circuits from self.

    ##     .. warning::

    ##         The <lambda> level polarised may still contain newly appearing chordless odd circuits !

    ##     """
    ##     try:
    ##         circuitslist = self.circuitslist
    ##     except:
    ##         self.computeChordlessCircuits(Odd=True,Comments=Debug)
    ##         circuitsList = self.circuitsList
    ##     Max = self.valuationdomain['max']
    ##     Med = self.valuationdomain['med']
    ##     qualmaj = Med
    ##     for cc in circuitsList:
    ##         ccqualmaj = Max
    ##         if Debug:
    ##             print cc
    ##         circuit = cc[0]
    ##         circuit.append(cc[0][0])
    ##         if Debug:
    ##             print circuit
    ##         n = len(circuit)
    ##         for i in range(n-1):
    ##             x = cc[0][i]
    ##             y = cc[0][i+1]
    ##             if Debug:
    ##                 print x, y, self.relation[x][y],y,x,self.relation[y][x]
    ##             if self.relation[x][y] > Med:
    ##                 if self.relation[x][y] < ccqualmaj:
    ##                     ccqualmaj = self.relation[x][y]
    ##         else:
    ##             if self.relation[y][x] < Med:
    ##                 if abs(self.relation[y][x]) < ccqualmaj:
    ##                     ccqualmaj = abs(self.relation[y][x])
    ##         if Debug:
    ##             print '==>>', circuit, ccqualmaj
    ##         if ccqualmaj > qualmaj:
    ##             qualmaj = ccqualmaj
    ##     if Debug:
    ##         print qualmaj
    ##     return qualmaj

    def circuitMinCredibility(self,circuit):
        """
        Renders the minimal linking credibility of a COC.
        """
        actions = self.actions
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = self.relation
        deg = Max
        n = len(circuit)
        for i in range(n):
            x = circuit[i]
            for j in range(i+1,n):
                y =  circuit[j]
                if j == i+1:
                    deg = min(deg,max(relation[x][y],-relation[y][x]))
        x = circuit[-1]
        y = circuit[0]
        deg = min(deg,max(relation[x][y],-relation[y][x]))
        return deg

    ## def circuitMinCredibilityOld(self,circuit):
    ##     """
    ##     Renders the minimal linking credibility of a COC.
    ##     """
    ##     actions = self.actions
    ##     Max = self.valuationdomain['max']
    ##     Med = self.valuationdomain['med']
    ##     relation = self.relation
    ##     deg = Max
    ##     for x in circuit:
    ##         for y in circuit:
    ##             if relation[x][y] > Med:
    ##                 deg = min(deg,relation[x][y])
    ##     return deg

    def circuitAverageCredibility(self,circuit):
        """
        Renders the average linking credibility of a COC.
        """
        actions = self.actions
        n = len(actions)
        narcs = n * (n-1)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relation = self.relation
        deg = Decimal('0.0')
        for x in circuit:
            for y in circuit:
                if x != y:
                    deg += relation[x][y]
        deg = deg / Decimal(str(narcs))
        return deg

    def contra(self, v):
        """
        Parameter: choice.
        Renders the negation of a choice v characteristic's vector.
        """
        Max = Decimal(str(self.valuationdomain['max']))
        Min = Decimal(str(self.valuationdomain['min']))
        #print v
        nv = [Max - v[x] + Min for x in range(len(v))]
        return nv

    def sharpvec(self, v, w):
        """
        Paramaters: choice characteristic vectors.
        Renders the sharpest of two characteristic vectors v and w.
        """
        sv = [self.sharp(v[x],w[x]) for x in range(len(v))]
        return sv

    def sharp(self, x, y):
        """
        Paramaters: choice characteristic values.
        Renders the sharpest of two characteristic values x and y.
        """
        med = Decimal(str(self.valuationdomain['med']))
        if x >= med and y >= med:
            return max(x,y)
        elif x <= med and y <= med:
            return min(x,y)
        else:
            return med

    def inner_prod(self, v1, v2):
        """
        Parameters: two choice characteristic vectors
        Renders the inner product of two characteristic vetors.
        """
        res = Decimal(str(self.valuationdomain['min']))
        for i in range(len(v1)):
            res = max(res, min(v1[i],v2[i]))
        return res

    def matmult2(self, m, v):
        """
        Parameters: digraph relation and choice characteristic vector
        matrix multiply vector by inner production
        """
        return [self.inner_prod(r, v) for r in m]

    def readdomvector(self, x,relation):
        """
        Parameter: action x
        dominant out vector.
        """
        #import array
        actions = self.actions
        vec = [relation[y][x] for y in actions]
        return vec

    def readabsvector(self, x,relation):
        """
        Parameter: action x
        absorbent in vector.
        """
        #import array
        actions = self.actions
        vec = [relation[x][y] for y in actions]
        return vec

    # -----  graph restrictions methods

    def domkernelrestrict(self, choice):
        """
        Parameter: prekernel
        Renders dominant prekernel restricted relation.
        """
        actions = self.actions
        relation = self.relation
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        relation_k = {}
        for x in actions:
            relation_k[x] = {}
            for y in actions:
                relation_k[x][y] = {}
                if x == y:
                    relation_k[x][y] = Min
                elif x in choice and y in choice:
                    relation_k[x][y] = relation[x][y]
                elif x in choice and relation[x][y] > Med:
                    relation_k[x][y] = relation[x][y]
                elif y in choice and relation[x][y] < Med:
                    relation_k[x][y] = relation[x][y]
                else:
                    relation_k[x][y] = Med
        return relation_k

    def abskernelrestrict(self, choice):
        """
        Parameter: prekernel
        Renders absorbent prekernel restricted relation.
        """
        actions = self.actions
        relation = self.relation
        Min = Decimal(str(self.valuationdomain['min']))
        Med = Decimal(str(self.valuationdomain['med']))
        relation_k = {}
        for x in actions:
            relation_k[x] = {}
            for y in actions:
                relation_k[x][y] = {}
                if x == y:
                    relation_k[x][y] = Min
                elif x in choice and y in choice:
                    relation_k[x][y] = relation[x][y]
                elif x in choice and relation[x][y] < Med:
                    relation_k[x][y] = relation[x][y]
                elif y in choice and relation[x][y] > Med:
                    relation_k[x][y] = relation[x][y]
                else:
                    relation_k[x][y] = Med
        return relation_k


    def showRubyChoice(self,Comments=False):
        """
        dummy for showRubisChoice()
        older versions compatibility
        """
        self.showRubisBestChoiceRecommendation(Comments=Comments)

    def showRubisBestChoiceRecommendation(self,Comments=False,Debug=False):
        """
        Renders the RuBis best choice recommendation.
        """
        import copy,time
        if Debug:
            Comments = True
        print('***********************')
        print('RuBis BCR')
        if Comments:
            print('All comments !!!')
        t0 = time.time()
        n0 = self.order
        _selfwcoc = CocaDigraph(self,Comments=Comments)
        n1 = _selfwcoc.order
        nc = n1 - n0
        if nc > 0:
            self.actions_orig = copy.deepcopy(self.actions)
            self.relation_orig = copy.deepcopy(self.relation)
            self.actions = copy.deepcopy(_selfwcoc.actions)
            self.order = len(self.actions)
            self.relation = copy.deepcopy(_selfwcoc.relation)
        print('List of pseudo-independent choices')
        print(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Debug:
            self.showRelationTable()
        #self.showPreKernels()
        actions = set([x for x in self.actions])
        self.dompreKernels = set()
        self.abspreKernels = set()
        #t0 = time.time()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                self.dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                self.abspreKernels.add(choice[0][0])
        self.computeGoodChoices(Comments=Comments)
        self.computeBadChoices(Comments=Comments)
        t1 = time.time()
        print('* --- Rubis best choice recommendation(s) ---*')
        print('  (in decreasing order of determinateness)   ')
        print('Credibility domain: ', self.valuationdomain)
        Med = self.valuationdomain['med']
        bestChoice = set()
        worstChoice = set()
        for gch in self.goodChoices:
            if gch[0] <= Med:
                goodChoice = True
                for bch in self.badChoices:
                    if gch[5] == bch[5]:
                        #if gch[0] == bch[0]:
                        if gch[3] == gch[4]:
                            if Comments:
                                print('null choice ')
                                self.showChoiceVector(gch)
                                self.showChoiceVector(bch)
                            goodChoice = False
                        elif gch[4] > gch[3]:
                            if Comments:
                                print('outranked choice ')
                                self.showChoiceVector(gch)
                                self.showChoiceVector(bch)
                            goodChoice = False
                        else:
                            goodChoice = True
                if goodChoice:
                    print(' === >> potential BCR ')
                    self.showChoiceVector(gch)
                    if bestChoice == set():
                        bestChoice = gch[5]
            else:
                if Comments:
                    print('non robust best choice ')
                    self.showChoiceVector(gch)
        for bch in self.badChoices:
            if bch[0] <= Med:
                badChoice = True
                nullChoice = False
                for gch in self.goodChoices:
                    if bch[5] == gch[5]:
                        #if gch[0] == bch[0]:
                        if bch[3] == bch[4]:
                            if Comments:
                                print('null choice ')
                                self.showChoiceVector(gch)
                                self.showChoiceVector(bch)
                            badChoice = False
                            nullChoice = True
                        elif bch[3] > bch[4]:
                            if Comments:
                                print('outranking choice ')
                                self.showChoiceVector(gch)
                                self.showChoiceVector(bch)
                            badChoice = False
                        else:
                            badChoice = True
                if badChoice:
                    print(' === >> potential worst choice ')
                    self.showChoiceVector(bch)
                    if worstChoice == set():
                        worstChoice = bch[5]
                elif nullChoice:
                    print(' === >> ambiguous choice ')
                    self.showChoiceVector(bch)
                    if worstChoice == set():
                        worstChoice = bch[5]

            else:
                if Comments:
                    print('non robust worst choice ')
                    self.showChoiceVector(bch)
        print()
        print('Execution time: %.3f seconds' % (t1-t0))
        print('*****************************')
        self.bestChoice = bestChoice
        self.worstChoice = worstChoice
        if nc > 0:
            self.actions = copy.deepcopy(self.actions_orig)
            self.relation = copy.deepcopy(self.relation_orig)
            self.order = len(self.actions)
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
        ## try:
        ##     self.worstChoice = self.badChoices[0][5]
        ## except:
        ##     self.worstChoice = set()

    def computeRubyChoice(self,Comments=False):
        """
        dummy for computeRubisChoice()
        old versions compatibility.
        """
        self.computeRubisChoice(Comments=Comments)

    def computeRubisChoice(self,Comments=False):
        """
        Renders self.strictGoodChoices, self.nullChoices
        self.strictBadChoices, self.nonRobustChoices.
        """
        import copy,time
        if Comments:
            print('*--- computing the COCA digraph --*')

        n0 = self.order
        t0 = time.time()
        _selfwcoc = CocaDigraph(self,Comments=Comments)
        t1 = time.time()
        n1 = _selfwcoc.order
        nc = n1 - n0
        if Comments:
            print('Execution time: %.3f seconds' % (t1-t0))
            _selfwcoc.showPreKernels()
        try:
            actions_orig = copy.deepcopy(self.actions_orig)
        except:
            actions_orig = copy.deepcopy(self.actions)
        self.actions_orig = actions_orig
        self.relation_orig = copy.deepcopy(self.relation)

        self.actions = copy.deepcopy(_selfwcoc.actions)
        self.order = len(self.actions)
        self.relation = copy.deepcopy(_selfwcoc.relation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        actions = set([x for x in self.actions])
        self.dompreKernels = set()
        self.abspreKernels = set()
        for choice in self.independentChoices(self.singletons()):
            restactions = actions - choice[0][0]
            if restactions <= choice[0][1]:
                self.dompreKernels.add(choice[0][0])
            if restactions <= choice[0][2]:
                self.abspreKernels.add(choice[0][0])
        self.computeGoodChoices(Comments=Comments)
        self.computeBadChoices(Comments=Comments)
        self.strictGoodChoices = set()
        self.nullChoices = set()
        self.strictBadChoices = set()
        self.nonRobustChoices = set()
        for gch in self.goodChoices:
            if gch[0] <= 0:
                goodChoice = True
                for bch in self.badChoices:
                    if gch[5] == bch[5]:
                        if gch[3] == gch[4]:
                            goodChoice = False
                            self.nullChoices.add(frozenset(gch[5]))
                        elif gch[4] > gch[3]:
                            goodChoice = False
                            self.strictBadChoices.add(frozenset(bch[5]))
                        else:
                            goodChoice = True
                if goodChoice:
                    self.strictGoodChoices.add(frozenset(gch[5]))
            else:
                self.nonRobustChoices.add(frozenset(gch[5]))
        if Comments:
            self.showGoodChoices()
            self.showBadChoices()
        ## if nc > 0:
        ##     self.actions = copy.deepcopy(self.actions_orig)
        ##     self.relation = copy.deepcopy(self.relation_orig)
        ##     self.order = len(self.actions)
        ##     self.gamma = self.gammaSets()
        ##     self.notGamma = self.notGammaSets()



    def computeGoodChoices(self,Comments=False):
        """
        | Characteristic values for potentially good choices.
        | [(0)-determ,(1)degirred,(2)degi,(3)degd,(4)dega,(5)str(choice),(6)domvec]
        """
        import copy
        from operator import itemgetter
        temp = copy.deepcopy(self)
        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        relation = temp.relation
        domChoicesSort = []
        if 'dompreKernels' not in dir(temp):
            if Comments:
                temp.showPreKernels()
            else:
                temp.computePreKernels()
        for ker in temp.dompreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.domirredval(ker,relation)
            degmd = min(degi,degd)
            cover = temp.averageCoveringIndex(ker)
            relation_k = temp.domkernelrestrict(choice)
            n = len(actions)
            #vec1_a = array.array('f', [Max] * n)
            vec1_a = [Max for i in range(n)]
            #vec0_a = array.array('f', [Min] * n)
            vec0_a = [Min for i in range(n)]
            mat = [temp.readdomvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            if Comments:
                print('initial veclowa',veclowa)
                print('initial vechigha', vechigha)
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                if Comments:
                    print(it, 'th veclowa  :',veclowa)
                    print(it, 'th vechigha :',vechigha)
                it += 1
            if Comments:
                print('final veclowa  :', veclowa)
                print('final vechigha :', vechigha)
                print('#iterations    :', it)
            domvec = temp.sharpvec(veclowa,vechigha)
            determ = temp.determinateness(domvec)
            domChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),domvec,cover])
        domChoicesSort.sort()
        ## domChoicesSort.sort(reverse=True, key=itemgetter(7))
        ## for ch in domChoicesSort:
        ##     ch[5] = eval(ch[5])
        ## self.goodChoices = domChoicesSort
        ## return domChoicesSort
        goodChoicesDic = {}
        for ch in domChoicesSort:
            ch[5] = eval(ch[5])
            goodChoicesDic[frozenset(ch[5])] = {'determ':-ch[0],
                                    'degirred':ch[1],
                                    'degi':ch[2],
                                    'degd':ch[3],
                                    'dega':ch[4],
                                    'cover':ch[7],
                                    'bpv':ch[6]}

        self.goodChoices = domChoicesSort
        return goodChoicesDic

    def computeGoodPirlotChoices(self,Comments=False):
        """
        Characteristic values for potentially good choices
        using the Pirlot fixpoint algorithm.
        """
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        actions = self.actions
        n = len(actions)
        relation = self.relation
        domChoicesSort = []
        if 'dompreKernels' not in dir(self):
            self.computePreKernels()
        for ker in self.dompreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = self.intstab(ker)
            dega = self.absorb(ker)
            degd = self.domin(ker)
            degirred = self.domirredval(ker,relation)
            degmd = min(degi,degd)
            #vecmed = array.array('f', [Med] * n)
            #vecsol0 = array.array('f', [Min] * n)
            vecmed = [Med for i in range(n)]
            vecsol0 = [Min for i in range(n)]
            for x in range(n):
                if actions[x] in choice:
                    vecsol0[x] = Max
            if Comments:
                print('initial solution', vecsol0)
            mat0 = [self.readdomvector(x,relation) for x in actions]
            mat = self.irreflex(mat0)
            vecsol = vecsol0
            vecsolfin = vecmed
            it = 0
            while it < 2*n*n:
                vecsolfin = self.matmult2(mat,vecsol)
                if Comments:
                    print(it, 'th vecsol  :',vecsol)
                veccur = self.contra(vecsolfin)
                if vecsol == veccur : break
                vecsol = veccur
                it += 1
            if Comments:
                print('Final Solution=', vecsol)
            determ = self.determinateness(vecsol)
            domChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),vecsol])
        domChoicesSort.sort()
        for ch in domChoicesSort:
            ch[5] = eval(ch[5])
        self.goodChoices = domChoicesSort


    def computeBadPirlotChoices(self,Comments=False):
        """
        Characteristic values for potentially bad choices
        using the Pirlot's fixpoint algorithm.
        """
        import array
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        actions = self.actions
        n = len(actions)
        relation = self.relation
        absChoicesSort = []
        if 'abspreKernels' not in dir(self):
            self.computePreKernels()
        for ker in self.abspreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = self.intstab(ker)
            dega = self.absorb(ker)
            degd = self.domin(ker)
            degirred = self.absirredval(ker,relation)
            degmd = min(degi,degd)
            #vecmed = array.array('f', [Med] * n)
            #vecsol0 = array.array('f', [Min] * n)
            vecmed = [Med for i in range(n)]
            vecsol0 = [Min for i in range(n)]
            for x in range(n):
                if actions[x] in choice:
                    vecsol0[x] = Max
            if Comments:
                print('initial solution', vecsol0)
            mat0 = [self.readabsvector(x,relation) for x in actions]
            mat = self.irreflex(mat0)
            vecsol = vecsol0
            vecsolfin = vecmed
            it = 0
            while it < 2*n*n:
                vecsolfin = self.matmult2(mat,vecsol)
                if Comments:
                    print(it, 'th vesol :',vecsol)
                veccur = self.contra(vecsolfin)
                if vecsol == veccur : break
                vecsol = veccur
                it += 1
            if Comments:
                print('Final Solution=', vecsol)
            determ = self.determinateness(vecsol)
            absChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),vecsol])
        absChoicesSort.sort()
        for ch in absChoicesSort:
            ch[5] = eval(ch[5])
        self.badChoices = absChoicesSort

    def determinateness(self,vec,inPercent = True):
        """
        Renders the determinateness of a bipolar characteristic vector
        """
        Min = Decimal(str(self.valuationdomain['min']))
        Max = Decimal(str(self.valuationdomain['max']))
        Med = Decimal(str(self.valuationdomain['med']))
        result = Decimal('0.0')
        n = len(vec)
        for i in range(n):
            result += abs(vec[i]-Med)
            #print result
        result /= n*(Max-Med)
        #print result
        if inPercent:
            return (result + Decimal('1.0'))/Decimal('2.0')
        else:
            return result*(Max-Med)


    def computeBadChoices(self,Comments=False):
        """
        | Characteristic values for potentially bad choices.
        | [(0)-determ,(1)degirred,(2)degi,(3)degd,(4)dega,(5)str(choice),(6)absvec]
        """
        import copy
        from operator import itemgetter

        temp = copy.deepcopy(self)

        Max = Decimal(str(temp.valuationdomain['max']))
        Min = Decimal(str(temp.valuationdomain['min']))
        Med = Decimal(str(temp.valuationdomain['med']))
        actions = [x for x in temp.actions]
        relation = temp.relation
        absChoicesSort = []
        if 'abspreKernels' not in dir(temp):
            temp.computePreKernels()
        for ker in temp.abspreKernels:
            if Comments:
                print('--> kernel:', ker)
            choice = [y for y in ker]
            #choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.absirredval(ker,relation)
            cover = temp.averageCoveringIndex(ker,direction="in")
            relation_k = temp.abskernelrestrict(choice)
            n = len(actions)
            #vec1_a = array.array('f', [Max] * n)
            #vec0_a = array.array('f', [Min] * n)
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readabsvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            if Comments:
                print('initial veclowa',veclowa)
                print('initial vechigha', vechigha)
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                if Comments:
                    print(it, 'th veclowa  :',veclowa)
                    print(it, 'th vechigha :',vechigha)
                it += 1
            if Comments:
                print('final veclowa',veclowa)
                print('final vechigha', vechigha)
            absvec = temp.sharpvec(veclowa,vechigha)
            determ = temp.determinateness(absvec)
            absChoicesSort.append([-determ,degirred,degi,degd,dega,str(choice),absvec,cover])
        absChoicesSort.sort()
        ## absChoicesSort.sort(reverse=True, key=itemgetter(7))
        ## for ch in absChoicesSort:
        ##     ch[5] = eval(ch[5])
        ## self.badChoices = absChoicesSort
        badChoicesDic = {}
        for ch in absChoicesSort:
            ch[5] = eval(ch[5])
            badChoicesDic[frozenset(ch[5])] = {'determ':-ch[0],
                                    'degirred':ch[1],
                                    'degi':ch[2],
                                    'degd':ch[3],
                                    'dega':ch[4],
                                    'cover':ch[7],
                                    'bpv':ch[6]}
        self.badChoices = absChoicesSort
        return badChoicesDic

    def showChoiceVector(self,ch):
        """
        show procedure for annotated bipolar choices
        """
        actions = [x for x in self.actions]
        determ = -ch[0]
        degirred = ch[1]
        degi = ch[2]
        degd = ch[3]
        dega = ch[4]
        choice = ch[5]
        vec = ch[6]
        print('* choice              : ' + str(choice))
        print('  +-irredundancy      : %.2f' % (degirred))
        print('  independence        : %.2f' % (degi))
        print('  dominance           : %.2f' % (degd))
        print('  absorbency          : %.2f' % (dega))
        print('  covering (%)' + '        : %.2f' % ( self.averageCoveringIndex(choice) * Decimal('100') ))
        print("  determinateness (%)", end=' ')
        print(': %.2f' % (determ))
        print('  - characteristic vector = [', end=' ')
        for i in range(len(actions)):
            print('\'%s\': %.2f,' %  (str(actions[i]),vec[i]), end=' ')
        print(']')
        print()

    def showGoodChoices(self,Recompute=True):
        """
        Characteristic values for potentially good choices.
        """
        import array,copy
        temp = copy.deepcopy(self)

        Max = temp.valuationdomain['max']
        Min = temp.valuationdomain['min']
        Med = temp.valuationdomain['med']
        actions = [x for x in temp.actions]
        n = len(actions)
        relation = temp.relation
        print('*** Potentially good choices ***')
        print('    valuationdomain', temp.valuationdomain)
        domChoicesSort = []
        if 'dompreKernels' not in dir(temp) or Recompute:
            temp.computePreKernels()
        for ker in temp.dompreKernels:
            choice = [str(y) for y in ker]
            choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.domirredval(ker,relation)
            degmd = min(degi,degd)
            domChoicesSort.append([-degmd,degirred,degi,degd,dega,str(choice)])
        print('domChoicesSort', domChoicesSort)
        for ch in domChoicesSort:
            choice = ch[5]
            degirred = ch[1]
            degi = ch[2]
            degd = ch[3]
            dega = ch[4]
            print('* choice           : ' + str(choice))
            print('  +irredundance    : %.2f' % (degirred))
            print('  independence     : %.2f' % (degi))
            print('  dominance        : %.2f' % (degd))
            print('  absorbency       : %.2f' % (dega))
            relation_k = temp.domkernelrestrict(eval(choice))
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readdomvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                it += 1
            print('  + characteristic vector = [', end=' ')
            bestvec = temp.sharpvec(veclowa,vechigha)
            for i in range(len(actions)):
                print('\'' + str(actions[i]) + '\': ',bestvec[i], ' ', end=' ')
            print(']')
            print()

    def irreflex(self,mat):
        """
        puts diagonal entries of mat to valuationdomain['min']
        """
        Min = self.valuationdomain['min']
        n = len(mat[0])
        for i in range(n):
            mat[i][i] = Min
        return mat

    def showBadChoices(self,Recompute=True):
        """
        Characteristic values for potentially bad choices.
        """
        import copy
        temp = copy.deepcopy(self)

        Max = temp.valuationdomain['max']
        Min = temp.valuationdomain['min']
        Med = temp.valuationdomain['med']
        actions = [x for x in temp.actions]
        #actions.sort()
        relation = temp.relation
        print('*** Potentially bad choices ***')
        print('    valuationdomain', temp.valuationdomain)
        absChoicesSort = []
        if 'abspreKernels' not in dir(temp) or Recompute:
            temp.computePreKernels()
        for ker in temp.abspreKernels:
            choice = [str(y) for y in ker]
            choice.sort()
            degi = temp.intstab(ker)
            dega = temp.absorb(ker)
            degd = temp.domin(ker)
            degirred = temp.absirredval(ker,relation)
            degmd = min(degi,dega)
            absChoicesSort.append((-degmd,degirred,degi,degd,dega,str(choice)))
        print('absChoicesSort', absChoicesSort)
        absChoicesSort.sort()
        for ch in absChoicesSort:
            choice = ch[5]
            degirred = ch[1]
            degi = ch[2]
            degd = ch[3]
            dega = ch[4]
            print('* choice           : ' + str(choice))
            print('  -irredundance    : %.2f' % (degirred))
            print('  independence     : %.2f' % (degi))
            print('  dominance        : %.2f' % (degd))
            print('  absorbency       : %.2f' % (dega))
            relation_k = temp.abskernelrestrict(eval(choice))
            n = len(actions)
            vec1_a = [Max for i in range(n)]
            vec0_a = [Min for i in range(n)]
            mat = [temp.readabsvector(x,relation_k) for x in actions]
            veclowa = vec0_a
            vechigha = vec1_a
            it = 1
            while veclowa != vechigha and it < 2*n*n:
                veclowb = temp.matmult2(mat,veclowa)
                vechighb = temp.matmult2(mat,vechigha)
                veclow = temp.contra(vechighb)
                vechigh = temp.contra(veclowb)
                if veclow == veclowa and vechigh == vechigha : break
                veclowa = veclow
                vechigha = vechigh
                it += 1
            print('  - characteristic vector = [', end=' ')
            bestvec = temp.sharpvec(veclowa,vechigha)
            for i in range(len(actions)):
                print('\'' + str(actions[i]) + '\': ',bestvec[i], ' ', end=' ')
            print(']')
            print()

    def showMIS_AH(self,withListing=True):
        """
        Prints all MIS using the Hertz method.
        Result saved in self.hertzmisset.
        """
        import sys,random,copy,time
        relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        gamma = self.gammaSets()
        notGamma = self.notGammaSets()
        t0 = time.time()
        # MIS extraction
        print('*---- MIS extraction ----')
        t0 = time.time()
        # initialize MIS extraction
        hertzmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | gamma[i][0]
        if withListing:
            print('===>>> Inital solution : ', list(S))
        hertzmisset = hertzmisset | set([frozenset(S)])
        # initialize all variables
        R = V - S
        ns = len(S)
        n = self.order
        i = 0
        P  = [set() for x in range(n)]
        M  = [set() for x in range(n)]
        NR = [set() for x in range(n)]
        Q  = [set() for x in range(n)]
        v  = [0     for x in range(n)]
        NON_R = set()
        OUI_R = set()
        NON_S = set()
        OUI_S = set()
        hist = 0
        # core of the algorithm
        while i >= 0:
            hist += 1
            # Part 1
            for k in [x for x in NON_R if gamma[x][0] & (OUI_R | OUI_S) == set() and len(gamma[x][0] - NON_R - NON_S) == 1]:
                sr = gamma[k][0]-NON_R-NON_S
                if sr != set():
                    if sr < R:
                        P[i] = P[i] | sr
                        OUI_R = OUI_R | sr
                        r = sr.pop()
                        NR[i] = NR[i] | (gamma[r][0] & (R-NON_R))
                        NON_R = NON_R | (gamma[r][0] & R)
                        M[i] = M[i] | (gamma[r][0] & (S-NON_S))
                        NON_S = NON_S | (gamma[r][0] & S)
                        test = True
                        for vr in (R - OUI_R):
                            if gamma[vr][0] & ((S - NON_S) | OUI_R) == set():
                                test = False
                                break
                        if test == True:
                            hertzmisset = hertzmisset | set([frozenset((S - NON_S) | OUI_R)])
                    else:
                        Q[i] = Q[i] | sr
                        OUI_S = OUI_S | sr
                        r = sr.pop()
                        NR[i] = NR[i] | (gamma[r][0] & (R-NON_R))
                        NON_R = NON_R | (gamma[r][0] & R)

           # Part 2
            if (NON_R | OUI_R) != R:
                i +=1
                setPart2v = R - NON_R - OUI_R
                v[i] = setPart2v.pop()
                P[i] = set([v[i]])
                OUI_R = OUI_R | P[i]
                M[i] = gamma[v[i]][0] & (S - NON_S)
                NON_S = NON_S | M[i]
                NR[i] = gamma[v[i]][0] & (R - NON_R)
                NON_R = NON_R | NR[i]
                test = True
                for vr in (R - OUI_R):
                    if gamma[vr][0] & ((S - NON_S) | OUI_R) == set():
                        test = False
                        break
                if test == True:
                    hertzmisset = hertzmisset | set([frozenset((S - NON_S) | OUI_R)])
            else:
                i -= 1
                NR[i] = NR[i] | set([v[i+1]])
                NON_R = (NON_R - NR[i+1]) | set([v[i+1]])
                NON_S = NON_S - M[i+1]
                OUI_R = OUI_R - P[i+1]
                OUI_S = OUI_S - Q[i+1]
                Q[i+1] = set()

        # end of algorithm
        t1 = time.time()
        if withListing:
            print('*---- results ----*')
        v = [0 for i in range(n+1)]
        mislen = set()
        for ch in hertzmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
            mislen = mislen | set([len(ch)])
        print('*---- statistics ----*')
        print('mis lengths      : ', list(range(self.order+1)))
        print('frequency        : ', v)
        mislenlist = list(mislen)
        mislenlist.sort()
        print('mis lengths      : ', mislenlist)
        print('mis solutions    : ', len(hertzmisset))
        print('execution time   : %.5f sec.' % (t1 - t0))
        print('iteration history: ', hist)
        print('result in self.hertzmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. version 7(6)-25-Apr-06       *')
        print('*-----------------------------------*')
        # store global results
        self.mislen = mislenlist
        self.hertzmisset = hertzmisset
        # restore original relation and neigborhooods
        self.relation = relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showMIS_RB(self,withListing=True):
        """
        Prints all MIS using the Bisdorff method.
        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        t0 = time.time()
        # initialize MIS extraction
        newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        newmisset = newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                newmisset = newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        i = 0
        for mis in initmisset:
            print(list(mis[1]), mis[0])
            i +=1

        # MIS extraction
        print('*---- MIS extraction ----')
        mislen = set()   # list of MIS length observed
        S = initmisset[i-1][1]  # start with largest init MIS
        print('===>>> Initial solution : ', list(S))
        ns = len(S)

        print('--> iteration 0 ')
        mislen = mislen | set([ns])

        upmis = set()  # independent choices as MIS candidates
        R = V - S
        for r in R:   # add a node from outside S
            Sr = (S - self.gamma[r][0]) | set([r]) # Sr independent
            upmis = upmis | set([frozenset(Sr)])

        iter = 0
        uphistory = set()
        while upmis != set():
            iter += 1  # next iteration init
            print('--> up iteration: ', iter)
            upmisiter = copy.copy(upmis)
            print('potential choices: ', len(upmisiter))
            uphistory = uphistory | upmis
            upmis = set()
            # up movement
            for Sch in upmisiter:

                gammaSch = set()
                for x in Sch:
                    gammaSch = gammaSch | self.gamma[x][0]

                while (Sch | gammaSch) != V:
                    i = random.choice(list(V-Sch-gammaSch))
                    Sch = Sch | set([i])
                    gammaSch = gammaSch | self.gamma[i][0]

                if Sch not in newmisset:
                    mislen = mislen | set([len(Sch)])
                    newmisset = newmisset | set([frozenset(Sch)])

                    Rch = V - Sch
                    for r in Rch:   # add a node from outside S
                        Srch = (Sch - self.gamma[r][0]) | set([r]) # Sr independent
                        if Srch not in uphistory:
                            upmis = upmis | set([frozenset(Srch)])

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        mislenlist = list(mislen)
        mislenlist.sort()
        print('mis lengths   : ', mislenlist)
        print('mis solutions : ', len(newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('up-history    : ', len(uphistory))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. version Ronda  April 2006    *')
        print('*-----------------------------------*')
        # store global results
        self.mislen = mislenlist
        self.newmisset = newmisset
        # restore original relation and neigborhooods
        self.relation = relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def showMIS_UD(self,withListing=True):
        """
        Prints all MIS using the Hertz-Bisdorff method.
        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        sys.setrecursionlimit(15000)
        self.relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.showAll()
        t0 = time.time()
        # initilaize MIS extraction
        self.newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        V = set(self.actions)
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        self.newmisset = self.newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                self.newmisset = self.newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        for mis in initmisset:
            print(list(mis[1]), mis[0])
        print('*---- same mises with up and down potentials ----')
        self.upmis = set()    # independent choices as MIS candidates
        self.downmis = set()  # covering choices as MIS candidates
        self.mislen = set()   # list of MIS length observed
        for mis in initmisset:
            S = mis[1]
            print('===>>> Inital solution : ', list(S))
            print('--> compute MIS of same size ', len(S))
            s = 0
            ns = mis[0]
            self.mislen = self.mislen | set([ns])
            V = set(self.actions)
            self.computeupdown1(s,S)  # compute all MIS of length ns
            iter = 0
            while self.upmis != set() or self.downmis != set():
                iter += 1  # next iteration init
                print('\n--> up iteration: ', iter)
                self.upmisiter = self.upmis.copy()
                self.upmis = set()
                self.downmisiter = self.downmis.copy()
                self.downmis = set()
                V = set(self.actions)
                # up movement
                for Sup in self.upmisiter:
                    Sch = Sup[0]
                    gammaSch = Sup[1]
                    while (Sch | gammaSch) != V:
                        i = random.choice(list(V-Sch-gammaSch))
                        Sch = Sch | set([i])
                        gammaSch = gammaSch | self.gamma[i][0]
                    if Sch not in self.newmisset:
                        self.mislen = self.mislen | set([len(Sch)])
                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                        s = 0
                        self.computeupdown1(s,Sch)
                # down movement
                print('\n*    <<< down potentials in', iter)
                for Sch in self.downmisiter:
                    for v in Sch:
                        if self.gamma[v][0] & Sch != set():
                            Sch = Sch - set([v])
                            gammaSch = set()
                            for x in Sch:
                                gammaSch = gammaSch | self.gamma[x][0]
                            if gammaSch & Sch == set():
                                if Sch | gammaSch == V:
                                    if Sch not in self.newmisset:
                                        self.mislen = self.mislen | set([len(Sch)])
                                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                                        self.computeupdown1(s,Sch)
                            else:
                                if Sch | gammaSch == V:
                                    self.downmis = self.downmis | set([frozenset(Sch)])

            print('solutions: ', len(self.newmisset))

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in self.newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        print('mis lengths   : ', list(self.mislen))
        print('mis solutions : ', len(self.newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. April 2006                   *')
        print('*-----------------------------------*')
        # restore original relation and neigborhooods
        self.relation = self.relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeupdown1(self, s, S):
        """
        Help method for show_MIS_HB2 method.
        fills self.newmisset, self.upmis, self.downmis.
        """
        Min = self.valuationdomain['min']
        V = set(self.actions)
        R = V - S
        print(s, end=' ') # recursion depth: traces the discovery of MISs
        s += 1
        for v in S: # choose a leaving node
            Sv = S - set([v])
            gammaSv = set() # recompute neighborhood
            for sv in Sv:
                gammaSv = gammaSv | self.gamma[sv][0]
            for r in R:   # add a node from outside S
                Svr = Sv | set([r])
                gammaSvr = gammaSv | self.gamma[r][0]
                if gammaSvr & Svr == set(): # if independent
                    if gammaSvr | Svr == V: # and if covering
                        if Svr not in self.newmisset:
                            #print 'MIS ', Svr
                            self.newmisset = self.newmisset | set([frozenset(Svr)])
                            self.computeupdown1(s,Svr)
                    else:                   # indep. and not covering
                        #print 'up ->',Svr
                        self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])
                elif Svr | gammaSvr == V:   # covering but not independent
                    #print 'down->',Svr
                    self.downmis = self.downmis | set([frozenset(Svr)])


    def showMIS_HB2(self,withListing=True):
        """
        Prints all MIS using the Hertz-Bisdorff method.
        Result saved in self.newmisset.
        """
        import sys,random,copy,time
        sys.setrecursionlimit(15000)
        self.relationBackup = copy.copy(self.relation)
        relation = {}
        V = set(self.actions)
        for x in V:
            relation[x] = {}
            for y in V:
                relation[x][y] = max(self.relation[x][y],self.relation[y][x])
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.showAll()
        t0 = time.time()
        # initilaize MIS extraction
        self.newmisset = set()  # global MIS collector set to empty
        # compute inital MIS
        initmisset = [] # initial MISs collector
        n = len(V)
        S = set() # initial MIS
        gammaS = set() # initial MIS neighborhood
        V = set(self.actions)
        while (S | gammaS) != V:
            i = random.choice(list(V-S-gammaS))
            S.add(i)
            gammaS = gammaS | self.gamma[i][0]
        self.newmisset = self.newmisset | set([frozenset(S)])
        initmisset.append((len(S),frozenset(S)))
        R = V - S # remaining unused nodes
        # find disjoint further inital MISs
        while R != set():
            S = set() # current MIS candidate
            gammaS = set() # current MIS neighborhood
            Cr = R # current remaining unused nodes
            while Cr != set() and S | gammaS != V: # independence condition
                i = Cr.pop()
                S.add(i)
                gammaS = gammaS | self.gamma[i][0]
                Cr = R - S - gammaS
            if S | gammaS == V: # cover condition
                self.newmisset = self.newmisset | set([frozenset(S)])
                initmisset.append((len(S),frozenset(S)))
            R = R - S # further remaining unused nodes
        print('\ninital MISs ')
        # sorting MIS by increasing length
        initmisset.sort()
        for mis in initmisset:
            print(list(mis[1]), mis[0])
        print('*---- same mises with up and down potentials ----')
        self.upmis = set()    # independent choices as MIS candidates
        self.uphistory = set()
        self.downmis = set()  # covering choices as MIS candidates
        self.downhistory = set()
        self.mislen = set()   # list of MIS length observed
        for mis in initmisset:
            S = mis[1]
            print('===>>> Inital solution : ', list(S))
            print('--> compute MIS of same size ', len(S))
            s = 0
            ns = mis[0]
            self.mislen = self.mislen | set([ns])
            V = set(self.actions)
            self.computeupdown2(s,S)  # starting from S compute all MIS of same length
            iter = 0
            while self.upmis != set() or self.downmis != set():
                iter += 1  # next iteration init
                self.upmisiter = self.upmis.copy()
                self.uphistory = self.uphistory | self.upmis
                self.upmis = set()
                self.downmisiter = self.downmis.copy()
                self.downhistory = self.downhistory | self.downmis
                self.downmis = set()
                V = set(self.actions)
                # up movement
                print('\n  >>> up iteration: ', iter)
                for Sup in self.upmisiter:
                    Sch = Sup[0]
                    gammaSch = Sup[1]
                    while (Sch | gammaSch) != V:
                        i = random.choice(list(V-Sch-gammaSch))
                        Sch = Sch | set([i])
                        gammaSch = gammaSch | self.gamma[i][0]
                    if Sch not in self.newmisset:
                        self.mislen = self.mislen | set([len(Sch)])
                        self.newmisset = self.newmisset | set([frozenset(Sch)])
                        s = 0
                        self.computeupdown2(s,Sch)
                # down movement
                print('\n*    <<< down potentials in', iter)
                for Sch in self.downmisiter:
                    for v in Sch:
                        if self.gamma[v][0] & Sch != set():
                            Sch = Sch - set([v])
                            gammaSch = set()
                            for x in Sch:
                                gammaSch = gammaSch | self.gamma[x][0]
                            if gammaSch & Sch == set():
                                if Sch | gammaSch == V and Sch not in self.newmisset:
                                    self.mislen = self.mislen | set([len(Sch)])
                                    self.newmisset = self.newmisset | set([frozenset(Sch)])
                                    s = 0
                                    self.computeupdown2(s,Sch)
                                #elif Sch not in self.uphistory:
                                    #print 'up ->',Sch
                                    #self.upmis = self.upmis | set([(frozenset(Sch),frozenset(gammaSch))])

                            else:
                                if Sch | gammaSch == V and Sch not in self.downhistory:
                                    self.downmis = self.downmis | set([frozenset(Sch)])

            print('solutions: ', len(self.newmisset))

        t1 = time.time()
        print('*---- results ----*')
        v = [0 for i in range(n+1)]
        for ch in self.newmisset:
            v[len(ch)] += 1
            if withListing:
                print(list(ch))
        print('*---- statistics ----*')
        print('mis lengths   : ', list(range(self.order+1)))
        print('frequency     : ', v)
        print('mis lengths   : ', list(self.mislen))
        print('mis solutions : ', len(self.newmisset))
        print('execution time: %.5f sec.' % (t1 - t0))
        print('result in self.newmisset')
        print('*-----------------------------------*')
        print("* Python implementation of Hertz's  *")
        print('* algorithm for generating all MIS  *')
        print('* R.B. April 2006                   *')
        print('*-----------------------------------*')
        # restore original relation and neigborhooods
        self.relation = self.relationBackup
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeupdown2irred(self, s, S):
        """
        Help method for show_MIS_HB1 method.
        fills self.newmisset, self.upmis, self.downmis.
        """
        #import copy
        newmis = set([frozenset(S)])
        V = set(self.actions)
        s = 0
        while newmis != set():
            self.newmisset = self.newmisset | newmis
            S = newmis.pop()
            R = V - S
            print(s, end=' ') # recursion depth: traces the discovery of MISs
            s += 1
            #Siter = copy.copy(S)
            for v in S: # choose a leaving node
                Sv = S - set([v])
                gammaSv = set() # recompute Sv neighborhood
                for sv in Sv:
                    gammaSv = gammaSv | self.gamma[sv][0]
                privgammav = (self.gamma[v][0] | set([v])) - (gammaSv | Sv)
                for r in R:   # add a node from outside S
                    if privgammav <= self.gamma[r][0]:  # covering
                        Svr = Sv | set([r])
                        if self.gamma[r][0] & Sv == set():  # independent
                            if Svr not in self.newmisset:
                                print('new MIS ', Svr)
                                newmis = newmis | set([frozenset(Svr)])
                        else:
                            if Svr not in self.downhistory:
                                print('down->',Svr)
                                self.downmis = self.downmis | set([frozenset(Svr)])
                    else:
                        if self.gamma[r][0] & Sv == set():  # independent
                            Svr = Sv | set([r])
                            if Svr not in self.uphistory:
                                print('up ->',Svr)
                                gammaSvr = gammaSv | self.gamma[r][0]
                                self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])

    def computeupdown2(self, s, S):
        """
        Help method for show_MIS_HB1 method.
        fills self.newmisset, self.upmis, self.downmis.
        """
        #import copy
        newmis = set([frozenset(S)])
        V = set(self.actions)
        s = 0
        while newmis != set():
            self.newmisset = self.newmisset | newmis
            S = newmis.pop()
            R = V - S
            print(s, end=' ') # recursion depth: traces the discovery of MISs
            s += 1
            #Siter = copy.copy(S)
            for v in S: # choose a leaving node
                Sv = S - set([v])
                gammaSv = set() # recompute neighborhood
                for sv in Sv:
                    gammaSv = gammaSv | self.gamma[sv][0]
                #privgammav = (self.gamma[v][0] | set([v])) - gammaSv
                for r in R:   # add a node from outside S
                    Svr = Sv | set([r])
                    gammaSvr = gammaSv | self.gamma[r][0]
                    if gammaSvr & Svr == set(): # if independent
                        if gammaSvr | Svr == V: # and if covering
                            if Svr not in self.newmisset:
                                #print 'new MIS ', Svr
                                newmis = newmis | set([frozenset(Svr)])
                        else:                   # indep. and not covering
                            if Svr not in self.uphistory:
                                #print 'up ->',Svr
                                self.upmis = self.upmis | set([(frozenset(Svr),frozenset(gammaSvr))])
                    elif Svr | gammaSvr == V:   # covering but not independent
                        if Svr not in self.downhistory:
                            #print 'down->',Svr
                            self.downmis = self.downmis | set([frozenset(Svr)])


    def computeODistance(self,op2,comments=False):
        """
        renders the squared normalized distance of
        two digraph valuations.
        Parameters: op2 digraphs of same order as self.
        The digraphs must be of same order.
        """
        import math,copy

        op1 = copy.deepcopy(self)

        Debug = False

        if comments:
            print('* --- compute O Distance of two digraphs ---- *')
        ODistance = 0.0
        actionsList1 = [x for x in op1.actions]
        actionsList2 = [x for x in op2.actions]
        if len(actionsList1) != len(actionsList2):
            ODistance = None
            if comments:
                print('actionsList1', actionsList1)
                print('actionsList2', actionsList2)
                print('Error: Actions sets are not comaptible ?')
                print('       ODistance = None !!!')
        else:
            Minop1 = op1.valuationdomain['min']
            Maxop1 = op1.valuationdomain['max']
            Minop2 = op2.valuationdomain['min']
            Maxop2 = op2.valuationdomain['max']
            op1.recodeValuation(-1.0,1.0)
            op2.recodeValuation(-1.0,1.0)
            n = len(actionsList1)
            for i in range(n):
                for j in range(i+1,n):
                    ODistance += math.pow(op1.relation[actionsList1[i]][actionsList1[j]] - op2.relation[actionsList2[i]][actionsList2[j]],2)
                    if Debug:
                        print('==>>', end=' ')
                        print(actionsList1[i],actionsList1[j], 'op1 =', end=' ')
                        print(op1.relation[actionsList1[i]][actionsList1[j]])
                        print(actionsList2[i],actionsList2[j], 'op2 =', end=' ')
                        print(op2.relation[actionsList2[i]][actionsList2[j]])
                        print('ODistance +=', math.pow(op1.relation[actionsList1[i]][actionsList1[j]] - op2.relation[actionsList2[i]][actionsList2[j]],2))
            if comments:
                print('ODistance between',op1.name, ' and')
                print(op2.name, '=', ODistance)
            op1.recodeValuation(Minop1,Maxop1)
            op2.recodeValuation(Minop1,Maxop2)


        return ODistance

    def computeSingletonRanking(self,Comments = False, Debug = False):
        """
        Renders the sorted bipolar net determinatation of outrankingness
        minus outrankedness credibilities of all singleton choices.
        res = ((netdet,singleton,dom,absorb)+)
        """
        import copy

        valuationdomain = copy.deepcopy(self.valuationdomain)

        self.recodeValuation(0.0,100.0)


        sigs = [x[0] for x in self.singletons()]

        res = []
        for i in range(len(sigs)):
            if Debug:
                print(sigs[i], self.domin(sigs[i]) - self.absorb(sigs[i]))
            res.append((self.domin(sigs[i]) - self.absorb(sigs[i]),sigs[i],self.domin(sigs[i]),self.absorb(sigs[i])))

        res.sort(reverse=True)


        if Comments:
            for x in res:
                print("{%s} : %.3f " % ( [y for y in x[1]][0], (float(x[0]) + 100.0)/2.0 ))

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

    def omax(self,L, Debug=False):
        """
        epistemic disjunction for bipolar outranking characteristics
        computation
        """
        Med = self.valuationdomain['med']
        terms = list(L)
        termsPlus = []
        termsMinus = []
        termsNuls = []
        for i in range(len(terms)):
            if terms[i] > Med:
                termsPlus.append(terms[i])
            elif terms[i] < Med:
                termsMinus.append(terms[i])
            else:
                termsNuls.append(terms[i])
        if Debug:
            print('terms', terms)
            print('termsPlus',termsPlus)
            print('termsMinus', termsMinus)
            print('termsNuls', termsNuls)
        np = len(termsPlus)
        nm = len(termsMinus)
        if np > 0 and nm == 0:
            return max(termsPlus)
        elif nm > 0 and np == 0:
            return min(termsMinus)
        else:
            return Med

    def omin(self,L, Debug=False):
        """
        epistemic conjunction for bipolar outranking characteristics
        computation
        """
        Med = self.valuationdomain['med']
        terms = list(L)
        termsPlus = []
        termsMinus = []
        termsNuls = []
        for i in range(len(terms)):
            if terms[i] > Med:
                termsPlus.append(terms[i])
            elif terms[i] < Med:
                termsMinus.append(terms[i])
            else:
                termsNuls.append(terms[i])
        if Debug:
            print('terms', terms)
            print('termsPlus',termsPlus)
            print('termsMinus', termsMinus)
            print('termsNuls', termsNuls)
        np = len(termsPlus)
        nm = len(termsMinus)
        if np > 0:
            if nm > 0:
                return Med
            else:
                return min(termsPlus)
        else:
            if nm > 0:
                return max(termsMinus)
            else:
                return Med

    def computeKohlerRanking(self,Debug=False):
        """
        renders a ranking of the actions following Kohler's rule.
        """
        Max = self.valuationdomain['max']
        actionsList = [x for x in self.actions]
        relation = self.relation
        rank = {}
        k = 1
        while actionsList != []:
            maximin = []
            for x in actionsList:
                xmin = Max
                for y in actionsList:
                    if x != y:
                        if relation[x][y] < xmin:
                            xmin = relation[x][y]
                if Debug:
                    print('x, xmin', x, xmin)
                maximin.append((xmin,x))
            maximin.sort()
            if Debug:
                print(maximin, maximin[-1][1])
            rank[maximin[-1][1]] = {'rank':k,'majorityMargin':maximin[-1][0]}
            actionsList.remove(maximin[-1][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)
        return rank

    def computeArrowRaynaudRanking(self,Debug=False):
        """
        renders a ranking of the actions following Arrow&Raynaud's rule.
        """
        Min = self.valuationdomain['min']
        actionsList = [x for x in self.actions]
        n = len(actionsList)
        relation = self.relation
        rank = {}
        k = 1
        while actionsList != []:
            minimax = []
            for x in actionsList:
                xmax = Min
                for y in actionsList:
                    if x != y:
                        if relation[x][y] > xmax:
                            xmax = relation[x][y]
                if Debug:
                    print('x, xmax', x, xmax)
                minimax.append((xmax,x))
            minimax.sort()
            if Debug:
                print(minimax, minimax[0][1])
            rank[minimax[0][1]] = {'rank':n-k+1,'majorityMargin':minimax[0][0]}
            actionsList.remove(minimax[0][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)
        return rank

    def computeRankedPairsOrder(self,Cpp=False,Debug=False):
        """
        renders a ranking of the actions obtained from the
        ranked pairs rule.
        """
        relation = self.relation
        actions = [x for x in self.actions]
        actions.sort()

        n = len(actions)

        listPairs = []
        for x in actions:
            for y in [z for z in actions if z != x]:
                listPairs.append((-relation[x][y],(x,y),x,y))
        listPairs.sort(reverse=False)

        g = IndeterminateDigraph(order=n)
        g.actions = self.actions
        g.valuationdomain = {'min':Decimal('-1'), 'med': Decimal('0'), 'max': Decimal('1')}
        Min = g.valuationdomain['min']
        Max = g.valuationdomain['max']
        Med = g.valuationdomain['med']
        g.relation = {}
        for x in g.actions:
            g.relation[x] = {}
            for y in g.actions:
                g.relation[x][y] = Min

        rankedPairs = [x[1] for x in listPairs]
        for pair in rankedPairs:
            if Debug:
                print('next pair: ', pair)
            x = pair[0]
            y = pair[1]
            if g.relation[x][y] == Min and g.relation[y][x] == Min:
                g.relation[x][y] = Max
                g.gamma = g.gammaSets()
                g.notGamma = g.notGammaSets()
                if Cpp:
                    circ = g.computeCppChordlessCircuits()
                else:
                    circ = g.computeChordlessCircuits()
                if len(circ) != 0:
                    if Debug:
                        print(circ)
                    g.relation[x][y] = Min
                else:
                    if Debug:
                        print('added: (%s,%s) characteristic: %.2f' % (x,y, self.relation[x][y]))

        g.gamma = g.gammaSets()

        outdegrees = []
        for x in g.actions:
            outdegrees.append((len(g.gamma[x][0]),x))
        outdegrees.sort(reverse=True)

        rankedPairsOrder = []
        for x in outdegrees:
            rankedPairsOrder.append(x[1])
        if Debug:
            print('Ranked Pairs Order = ', rankedPairsOrder)
        return rankedPairsOrder


    def computeKemenyOrder(self,isProbabilistic=False, orderLimit=7, seed=None, sampleSize=1000, Debug=False):
        """
        renders a ranking of the actions with minimal Kemeny index.
        Return a tuple: kemenyOrder, kemenyIndex
        """
        from random import seed, shuffle
        from digraphs import all_perms


        Min = self.valuationdomain['min']
        relation = self.relation
        actions = [x for x in self.actions]
        n = len(actions)

        ## Monte Carlo computation of a Kemeny order
        if isProbabilistic:
            if seed != None:
                seed = seed
            a = list(actions)
            kemenyIndex = Decimal(str(n)) * Decimal(str(n)) *Min
            kemenyOrder = list(a)
            sampleSize = sampleSize

            for s in range(sampleSize):
                shuffle(a)
                kcurr = Decimal('0.0')
                for i in range(n):
                    for j in range(i+1,n):
                        kcurr += relation[a[i]][a[j]] - relation[a[j]][a[i]]

                if kcurr > kemenyIndex:
                    kemenyIndex = kcurr
                    kemenyOrder = list(a)
                    if Debug:
                        print(s, kemenyIndex)
            if Debug:
                print('Probabilistic Kemeny Order = ', kemenyOrder)
                print('Probabilistic Kemeny Index = ', kemenyIndex)
                print('with samplesize :            ', sampleSize)


        ## Exact computation of a Kemeny order
        ## respecting a maximum of marginal majority margins
        else:
            if n > orderLimit:
                return None
            kemenyIndex = Decimal(str(n)) * Decimal(str(n)) * Min
            kemenyOrder = list(actions)
            s = 1
            for a in all_perms(kemenyOrder):
                kcurr = Decimal('0.0')
                s += 1
                for i in range(n):
                    for j in range(i+1,n):
                        kcurr += relation[a[i]][a[j]] - relation[a[j]][a[i]]
                if Debug:
                    print(s, a, kcurr)
                if kcurr >= kemenyIndex:
                    kemenyIndex = kcurr
                    kemenyOrder = list(a)
                    if Debug:
                        print(s, kemenyOrder, kemenyIndex)
            if Debug:
                print('Exact Kemeny Order = ', kemenyOrder)
                print('Exact Kemeny Index = ', kemenyIndex)
                print('# of permutations  = ', s)

        return kemenyOrder, kemenyIndex


    def computeSlaterOrder(self,isProbabilistic=False, seed=None, sampleSize=1000, Debug=False):
        """
        renders a ranking of the actions with minimal Slater index.
        Return a tuple: slaterOrder, slaterIndex
        """
        from random import seed, shuffle
        try:
            from math import copysign
            CopySign = True
        except:
            CopySign = False
        from digraphs import all_perms


        Min = self.valuationdomain['min']
        relationOrig = self.relation
        minOrig = self.valuationdomain['min']
        maxOrig = self.valuationdomain['max']
        self.recodeValuation(-1,1)
        relation = self.relation
        actions = [x for x in self.actions]
        n = len(actions)

        ## Monte Carlo computation of a Slater order
        if isProbabilistic:
            if seed != None:
                seed = seed
            a = list(actions)
            slaterIndex = -(n*n)
            slaterOrder = list(a)
            sampleSize = sampleSize

            for s in range(sampleSize):
                shuffle(a)
                kcurr = 0
                for i in range(n):
                    for j in range(i+1,n):
                        if CopySign:
                            kcurr += copysign(1,relation[a[i]][a[j]]) - copysign(1,relation[a[j]][a[i]])
                        else:
                            if relation[a[i]][a[j]] > 0:
                                kcurr += 1
                            elif relation[a[i]][a[j]] < 0:
                                kcurr -= 1
                            if relation[a[j]][a[i]] > 0:
                                kcurr -= 1
                            elif relation[a[j]][a[i]] < 0:
                                kcurr += 1

                if kcurr > slaterIndex:
                    slaterIndex = kcurr
                    slaterOrder = list(a)
                    if Debug:
                        print(s, slaterIndex)
            if Debug:
                print('Probabilistic Slater Order = ', slaterOrder)
                print('Probabilistic Slater Index = ', slaterIndex)
                print('with samplesize :            ', sampleSize)


## Exact computation of a Slater order
## respecting a maximum of marginal majority margins
        else:

            slaterIndex = -(n*n)
            slaterOrder = list(actions)
            s = 0
            for a in all_perms(slaterOrder):
                kcurr = 0
                s += 1
                for i in range(n):
                    for j in range(i+1,n):
                        if CopySign:
                            kcurr += copysign(1,relation[a[i]][a[j]]) - copysign(1,relation[a[j]][a[i]])
                        else:
                            if relation[a[i]][a[j]] > 0:
                                kcurr += 1
                            elif relation[a[i]][a[j]] < 0:
                                kcurr -= 1
                            if relation[a[j]][a[i]] > 0:
                                kcurr -= 1
                            elif relation[a[j]][a[i]] < 0:
                                kcurr += 1
                        #kcurr += copysign(1,relation[a[i]][a[j]]) - copysign(1,relation[a[j]][a[i]])
                if Debug:
                    print(s, a, kcurr)
                if kcurr >= slaterIndex:
                    slaterIndex = kcurr
                    slaterOrder = list(a)
                    if Debug:
                        print(s, slaterOrder, slaterIndex)
            if Debug:
                print('Exact Slater Order = ', slaterOrder)
                print('Exact Slater Index = ', slaterIndex)
                print('# of permutations  = ', s)

        self.recodeValuation(minOrig,maxOrig)
        return slaterOrder, slaterIndex

    def computePairwiseClusterComparison(self, K1, K2, Debug=False):
        """
        compute the pairwise cluster comparison credibility vector
        from bipolar-valued digraph g. with K1 and K2 disjoint
        lists of action keys from g actions disctionary.
        Returns the dictionary
        {'I': Decimal(),'P+':Decimal(),'P-':Decimal(),'R' :Decimal()}
        where one and only one item is strictly positive.
        """
        from decimal import Decimal
        n = Decimal(str(len(K1)*len(K2)))
        if Debug:
            print('K1 = ', K1, ', K2 = ', K2, ', n = ', n)

        rK1SK2 = Decimal('0')
        rK2SK1 = Decimal('0')
        for x in K1:
            for y in K2:
                rK1SK2 += self.relation[x][y]
                rK2SK1 += self.relation[y][x]

        if Debug:
            print('r(K1 >= K2) = ', rK1SK2/n, ' r(K2 >= K1) = ', rK2SK1/n)

        rK1IK2 = min(rK1SK2,rK2SK1)/n
        rK1PK2 = min(rK1SK2,-rK2SK1)/n
        rK2PK1 = min(-rK1SK2,rK2SK1)/n
        rK1RK2 = min(-rK1SK2,-rK2SK1)/n

        if Debug:
            print('r(K1 = K2) = %.2f' % rK1IK2)
            print('r(K1 > K2) = %.2f' % rK1PK2)
            print('r(K1 < K2) = %.2f' % rK2PK1)
            print('r(K1 ? K2) = %.2f' % rK1RK2)

        return {'I': rK1IK2, 'P+': rK1PK2, 'P-' :rK2PK1, 'R' :  rK1RK2 }



# ------ CoDual construction

class CoDualDigraph(Digraph):
    """
    Instantiates the associated codual version from
    a given Digraph called other.

    Instantiates as other.__class__ !

    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'codual-'+other.name
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = deepcopy(other.evaluation)
        except AttributeError:
            pass
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(other.valuationdomain)
        actionsList = list(self.actions)
        max = self.valuationdomain['max']
        min = self.valuationdomain['min']
        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                relation[x][y] = max - other.relation[y][x] + min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# ------ Converse construction

class ConverseDigraph(Digraph):
    """
    Instantiates the associated converse orreciprocal version from
    a given Digraph called other.

    Instantiates as other.__class__ !

    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'converse-'+other.name
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = deepcopy(other.evaluation)
        except AttributeError:
            pass
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(other.valuationdomain)
        actionsList = list(self.actions)
        max = self.valuationdomain['max']
        min = self.valuationdomain['min']
        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                relation[x][y] = other.relation[y][x]
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# ------ Ranking By Choosing Digraph
class RankingByChoosingDigraph(Digraph):
    """
    Instantiates the digraph resulting from the
    ranking by choosing method applied to a Digraph object.
    """
    def __init__(self,otherIn,CoDual=False,MedianCut=False,Debug=False,Iterate=False):
        from copy import deepcopy
        other = deepcopy(otherIn)
        self.name = 'rbc-'+other.name
        self.actions = other.actions
        self.order = len(self.actions)

        other.recodeValuation(-1,1)
        self.valuationdomain = other.valuationdomain

        self.originalRelation = other.relation

        if Iterate:
            self.rankingByChoosing = other.iterateRankingByChoosing(CoDual=CoDual,Comments=False,Debug=Debug)
        else:
            self.rankingByChoosing = other.computeRankingByChoosing(CoDual=CoDual,Debug=Debug)
        if Debug:
            print(self.rankingByChoosing)


        self.relation = self.computeRankingByChoosingRelation(Debug=Debug)

        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showRankingByChoosing(self,Debug=False):
        """
        A show method for self.rankinByChoosing
        """
        if Debug:
            print(self.rankingByChoosing)
        rankingByChoosing = self.rankingByChoosing['result']
        print('Ranking by Choosing Result')
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
            ch = list(ibch)
            ch.sort()
            print(' %s%s%s Best Choice %s (%.2f)' % (space,i+1,nstr,ch,rankingByChoosing[i][0][0]))
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
            ch = list(iwch)
            ch.sort()
            if len(iach) > 0 and i > 0:
                space = space[:-2]
                print('  %s Ambiguous Choice %s' % (space,list(iach)))
            print(' %s%s%s Worst Choice %s (%.2f)' % (space,n-i,nstr,ch,rankingByChoosing[n-i-1][1][0]))
        if Debug:
            self.showRelationTable(self.originalRelation)
        if self.rankingByChoosing['CoDual']:
            corr = self.computeOrdinalCorrelation(self.originalRelation,Debug=Debug)
            print('Ordinal Correlation with codual (strict) outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination']))
            corr = self.computeOrdinalCorrelation(self.originalRelation,MedianCut=True,Debug=Debug)
            print('Ordinal Correlation with codual (strict) median cut outranking relation: %.3f (%.3f)' % (corr['correlation'],corr['determination']))

        else:
            corr = self.computeOrdinalCorrelation(self.originalRelation,Debug=Debug)
            print('Ordinal Correlation with outranking relation: %.3f (%.3f)'% (corr['correlation'],corr['determination']))
            corr = self.computeOrdinalCorrelation(self.originalRelation,MedianCut=True,Debug=Debug)
            print('Ordinal Correlation with median cut outranking relation: %.3f (%.3f)'% (corr['correlation'],corr['determination']))


# ------ Preorder construction

class Preorder(Digraph):
    """
    Instantiates the associated preorder from
    a given Digraph called other.

    Instantiates as other.__class__ !

    Copies the case given the description, the criteria
    and the evaluation dictionary into self.
    """

    def __init__(self,other,direction="best"):
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'preorder-'+other.name
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = deepcopy(other.evaluation)
        except AttributeError:
            pass
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.valuationdomain = deepcopy(other.valuationdomain)
        actionsList = [x for x in self.actions]
        Max = self.valuationdomain['max']
        Min = self.valuationdomain['min']
        relation = {}
        for x in actionsList:
            relation[x] = {}
            for y in actionsList:
                relation[x][y] = None

        if direction == 'best':
            rank = other.bestRanks()
        else:
            rank = other.worstRanks()
        for i in range(len(actionsList)):
            x = actionsList[i]
            for j in range(i, len(actionsList)):
                y = actionsList[j]
                if rank[x] < rank[y]:
                    relation[x][y] = Max
                    relation[y][x] = Min
                elif rank[x] > rank[y]:
                    relation[x][y] = Min
                    relation[y][x] = Max
                else:
                    relation[x][y] = Max
                    relation[y][x] = Max

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

# ------- XOR construction

class XORDigraph(Digraph):
    """
    Instantiates the XOR digraph of two bipolar
    digraphs d1 and d2 of same order.
    """

    def __init__(self,d1,d2,Debug = False):
        import copy
        self.name = 'XORDigraph'
        if d1.order != d2.order:
            if Debug:
                print("XORDigraph init ERROR:\n the input digraphs are not of the same order !")
            return None
        self.order = d1.order
        self.actions = copy.deepcopy(d1.actions)

        actions = [x for x in self.actions]
        Mind1 = d1.valuationdomain['min']
        Maxd1 = d1.valuationdomain['max']
        Mind2 = d2.valuationdomain['min']
        Maxd2 = d2.valuationdomain['max']
        d1.recodeValuation(-1.0,1.0)
        d2.recodeValuation(-1.0,1.0)
        xorRelation = {}
        for x in actions:
            xorRelation[x] = {}
            for y in actions:
                xorRelation[x][y] = max( min(d1.relation[x][y],-d2.relation[x][y]), min(d2.relation[x][y],-d1.relation[x][y]) )
                if Debug:
                    print(x,y,d1.relation[x][y],d2.relation[x][y],xorRelation[x][y])

        self.relation = xorRelation
        self.valuationdomain = {'min': Decimal("-1.0"),
                                'med': Decimal("0.0"),
                                'max': Decimal("1.0")}
        d1.recodeValuation(Mind1,Maxd1)
        d2.recodeValuation(Mind2,Maxd2)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class EquivalenceDigraph(Digraph):
    """
    Instantiates the logical equivalence digraph of two bipolar
    digraphs d1 and d2 of same order. Returns None if d1 and d2 are of different order
    """

    def __init__(self,d1,d2,Debug = False):
        from copy import deepcopy
        self.name = 'EquivDigraph'
        if d1.order != d2.order:
            print("EquivDigraph init ERROR:\n the input digraphs are not of the same order !")
            return None

        self.order = d1.order
        self.actions = deepcopy(d1.actions)
        actions = [x for x in self.actions]

        Mind1 = d1.valuationdomain['min']
        Maxd1 = d1.valuationdomain['max']
        Mind2 = d2.valuationdomain['min']
        Maxd2 = d2.valuationdomain['max']
        d1.recodeValuation(-1.0,1.0)
        d2.recodeValuation(-1.0,1.0)

        equivRelation = {}
        for x in actions:
            equivRelation[x] = {}
            for y in actions:
                equivRelation[x][y] = min( max(-d1.relation[x][y],d2.relation[x][y]), max(-d2.relation[x][y],d1.relation[x][y]) )
                if Debug:
                    print(x,y,d1.relation[x][y],d2.relation[x][y],equivRelation[x][y])

        self.relation = equivRelation
        self.valuationdomain = {'min': Decimal("-1.0"),
                                'med': Decimal("0.0"),
                                'max': Decimal("1.0")}

        d1.recodeValuation(Mind1,Maxd1)
        d2.recodeValuation(Mind2,Maxd2)

        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def computeCorrelation(self):
        """
        Renders the global bipolar correlation index resulting from the pairwise
        equivalence valuations.
        """
        corr = Decimal('0')
        dterm = Decimal('0')
        actions = [x for x in self.actions]
        relation = self.relation
        for x in actions:
            for y in actions:
                if x != y:
                    corr += relation[x][y]
                    dterm += abs(relation[x][y])
        return corr / dterm


# ------- Specialisations of the Digraph class -----------

class RandomDigraph(Digraph):
    """
    Parameters:
        order = n > 0; 0.0 <= arc_probability <= 1.0

    Specialization of the general Digraph class for generating
    temporary irreflexive random crisp digraphs
    """

    def __init__(self,order=10,arcProbability=0.5,hasIntegerValuation=False):
        """
        Constructor for RandomDigraph intances.

        Parameters:
           order, arcProbability, hasIntegerValuation.

        """
        arcProbability = Decimal(str(arcProbability))
        if arcProbability > Decimal("1.0"):
            print('Error: arc probability too high !!')
        elif arcProbability < Decimal("0.0"):
            print('Error: arc probability too low !!')
        else:
            import copy
            g = RandomValuationDigraph(order=order,hasIntegerValuation=hasIntegerValuation)
            cutLevel = 1 - arcProbability
            gp = PolarisedDigraph(digraph=g,level=cutLevel,AlphaCut=True)
            self.actions = copy.deepcopy(g.actions)
            self.valuationdomain = copy.deepcopy(gp.valuationdomain)
            self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
            self.relation = copy.deepcopy(gp.relation)
            self.order = g.order
            self.name = 'randomDigraph'
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()


class RandomValuationDigraph(Digraph):
    """
    Parameters:
        order = n > 0 (default 9); ndigits (default=2)

    Specialization of the general Digraph class for generating
    temporary irreflexive random graphs

    """

    def __init__(self,order=9, ndigits=2,Normalized=False,hasIntegerValuation=False):
        import random
        self.name = 'randomValuationDigraph'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        precision = pow(10,ndigits)
        if hasIntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            if Normalized:
                 self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            else:
                self.valuationdomain = {'min':Decimal('0'), 'med':Decimal('0.5'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        random.seed()
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                if x == y:
                    if hasIntegerValuation:
                        relation[x][y] = 0
                    elif Normalized:
                        relation[x][y] = Decimal('0.0')
                    else:
                        relation[x][y] = Decimal('0.5')
                else:
                    if hasIntegerValuation:
                        relation[x][y] = (2*random.randrange(start=0,stop=precision)) - precision
                    elif Normalized:
                        relation[x][y] = (Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits))) * Decimal('2.0')) - Decimal('1.0')
                    else:
                        relation[x][y] = Decimal(str(round(float(random.randrange(start=0,stop=precision))/precision,ndigits)))
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class RandomWeakTournament(Digraph):
    """
    Parameter:
        order = n > 0

    Specialization of the general Digraph class for generating
    temporary bipolar-valued weak tournaments

    """

    def __init__(self,order=10,ndigits=2,hasIntegerValuation=False,weaknessDegree=0.25,Comments=False):
        import random
        from decimal import Decimal

        self.name = 'randomWeakTournament'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        random.seed()
        Max = pow(10,ndigits)
        Min = - Max
        Med = 0
        precision = Max
        dPrecision = Decimal(str(precision))
        if hasIntegerValuation:
            self.valuationdomain = {'hasIntegerValuation':True, 'min':Decimal(str(Min)), 'med':Decimal('0'), 'max':Decimal(str(Max))}
        else:
            self.valuationdomain = {'hasIntegerValuation':False, 'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = self.valuationdomain['med']

        actionsList = [x for x in actions]
        random.shuffle(actionsList)
        weaknessDegree = Decimal(str(weaknessDegree))
        forwardDegree = (Decimal('1.0') - weaknessDegree)/Decimal('2')

        #print actionsList
        n = len(actionsList)
        for i in range(n):
            for j in range(i,n):
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    relation[actionsList[i]][actionsList[j]] = self.valuationdomain['med']
                else:
                    u = Decimal(str(random.randint(0,precision)))/dPrecision
                    u1 = Decimal(str(random.randint(0,precision)))
                    u2 = Decimal(str(random.randint(0,precision)))

                    if u < weaknessDegree: # i = j
                        if hasIntegerValuation:
                            randeval1 = u1
                            randeval2 = u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = u2/dPrecision

                    elif u < forwardDegree: # i > j
                        if hasIntegerValuation:
                            randeval1 = u1
                            randeval2 = Min + u2
                        else:
                            randeval1 = u1/dPrecision
                            randeval2 = (Min + u2)/dPrecision

                    else: # j > i
                        if hasIntegerValuation:
                            randeval1 = Min + u1
                            randeval2 = u2
                        else:
                            randeval1 = (Min + u1)/dPrecision
                            randeval2 = u2/dPrecision

                    if hasIntegerValuation:
                        relation[actionsList[i]][actionsList[j]] = Decimal(str(randeval1))
                        relation[actionsList[j]][actionsList[i]] = Decimal(str(randeval2))
                    else:
                        relation[actionsList[i]][actionsList[j]] = Decimal(str(round(randeval1,ndigits)))
                        relation[actionsList[j]][actionsList[i]] = Decimal(str(round(randeval2,ndigits)))


        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

        if Comments:
             print(self.order*(self.order-1), self.computeRelationalStructure())




## class RandomWeakTournamentOld(Digraph):
##     """
##     Obsolete version !

##     Parameter:
##         order = n > 0

##     Specialization of the general Digraph class for generating
##     temporary bipolar-valued weak tournaments

##     """

##     def __init__(self,order=10,ndigits=2,valuationDomain=None,Comments=False):
##         import random
##         from decimal import Decimal

##         self.name = 'randomWeakTournament'
##         self.order = order
##         actionlist = range(order+1)
##         actionlist.remove(0)
##         actions = []
##         for x in actionlist:
##             actions.append(str(x))
##         self.actions = actions
##         if valuationDomain == None:
##             self.valuationdomain = {'min':Decimal('-1'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
##         else:
##             self.valuationdomain = valuationDomain
##         valuationRange = self.valuationdomain['max'] - self.valuationdomain['min']
##         relation = {}
##         for x in actions:
##             relation[x] = {}
##             for y in actions:
##                 relation[x][y] = self.valuationdomain['med']
##         random.seed()
##         precision = pow(10,ndigits)
##         actionsList = [x for x in actions]
##         #print actionsList
##         n = len(actionsList)
##         for i in range(n):
##             for j in range(i,n):
##                 #print i,j
##                 if i == j:
##                     #print actionsList[i],actionsList[j]
##                     relation[actionsList[i]][actionsList[j]] = self.valuationdomain['med']
##                 else:
##                     u = random.randint(0,precision)
##                     #print 'uij', u
##                     randeval = self.valuationdomain['min'] + Decimal(str(u))/Decimal(str(precision))*valuationRange
##                     if u < precision/2:
##                         relation[actionsList[i]][actionsList[j]] = Decimal(str(round(randeval,ndigits)))
##                         u = random.randint(0,precision)
##                         #print 'uji<', u
##                         randeval = self.valuationdomain['med'] + (Decimal(str(u))*valuationRange)/(Decimal(str(precision))*Decimal('2.0'))
##                         relation[actionsList[j]][actionsList[i]] = Decimal(str(round(randeval,ndigits)))
##                     else:
##                         relation[actionsList[i]][actionsList[j]] = Decimal(str(round(randeval,ndigits)))
##                         u = random.randint(0,precision)
##                         #print 'uji>', u
##                         randeval = self.valuationdomain['min'] + (Decimal(str(u))*valuationRange)/Decimal(str(precision))
##                         relation[actionsList[j]][actionsList[i]] = Decimal(str(round(randeval,ndigits)))
##                 #print i, j, relation[actionsList[i]][actionsList[j]], relation[actionsList[j]][actionsList[i]]


##         self.relation = relation
##         self.gamma = self.gammaSets()
##         self.notGamma = self.notGammaSets()
##         if Comments:
##            print self.order*(self.order-1), self.computeRelationalStructure()


class RandomTournament(Digraph):
    """
    Parameter:
       order = n > 0

    Specialization of the general Digraph class for generating
    temporary weak tournaments

    """

    def __init__(self,order=10,ndigits=2,isCrisp=True,valuationDomain=None):
        import random
        from decimal import Decimal

        self.name = 'randomTournament'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        if valuationDomain == None:
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        else:
            self.valuationdomain = valuationDomain
        valuationRange = self.valuationdomain['max'] - self.valuationdomain['min']
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Decimal('0.0')
        random.seed()
        precision = pow(10,ndigits)
        actionsList = [x for x in actions]
        #print actionsList
        n = len(actionsList)
        for i in range(n):
            for j in range(i,n):
                #print i,j
                if i == j:
                    #print actionsList[i],actionsList[j]
                    relation[actionsList[i]][actionsList[j]] = self.valuationdomain['med']
                else:
                    u = random.randint(0,precision)
                    if isCrisp:
                        if u < Decimal(str(precision))/Decimal('2'):
                            relation[actionsList[i]][actionsList[j]] = self.valuationdomain['min']
                            relation[actionsList[j]][actionsList[i]] = self.valuationdomain['max']
                        else:
                            relation[actionsList[i]][actionsList[j]] = self.valuationdomain['max']
                            relation[actionsList[j]][actionsList[i]] = self.valuationdomain['min']
                    else:
                        randeval = self.valuationdomain['min'] + Decimal(str(u))/Decimal(str(precision))*valuationRange
                        valuation = Decimal(str(round(randeval,ndigits)))
                        relation[actionsList[i]][actionsList[j]] = valuation
                        relation[actionsList[j]][actionsList[i]] = self.valuationdomain['max'] - valuation + self.valuationdomain['min']

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class RandomFixedSizeDigraph(Digraph):
    """
    Parameters:
        order and size

    Specialization of Digraph class for random fixed size instances.

    """
    def __init__(self,order=7,size=14):
        import random,copy
        # check feasability
        r = (order * order) - order
        if size > r :
            print('Graph not feasable (1) !!')
        else:
            self.name = 'randomFixedSize'
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = []
            for x in actionlist:
                actions.append(str(x))
            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            Min = self.valuationdomain['min']
            Max = self.valuationdomain['max']
            random.seed()
            allarcs = []
            relation = {}
            for x in actions:
                relation[x] = {}
                for y in actions:
                    relation[x][y] = Min
                    if x != y:
                        allarcs.append((x,y))
            for i in range(size):
                arc = random.choice(allarcs)
                relation[arc[0]][arc[1]] = Max
                allarcs.remove(arc)
            self.relation = relation.copy()
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()

class RandomFixedDegreeSequenceDigraph(Digraph):
    """
    Parameters:
        order=n and degreeSequence=[degree_1, ... ,degree_n]>

    Specialization of Digraph class for random symmetric instances
    with fixed degree sequence.

    """
    def __init__(self,order=7,degreeSequence=[3,3,2,2,1,1,0]):
        import random,copy
        # check feasability
        degree = max(degreeSequence)
        if degree >= order:
            print('!!! Graph not feasable (1) !!!')
            print('Maximum degree > order !!!')
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
                actionlist = list(range(order+1))
                actionlist.remove(0)
                actions = []
                for x in actionlist:
                    actions.append(str(x))
                self.actions = actions
                self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
                Min = self.valuationdomain['min']
                Max = self.valuationdomain['max']
                relation = {}
                for x in actions:
                    relation[x] = {}
                    for y in actions:
                        relation[x][y] = Min
                random.seed()
                # create a random pairing
                feasable = 0
                s = 0
                while feasable == 0 and s < 100:
                    s += 1
                    edges = []
                    cells = []
                    degreeseq = {}
                    i = 0
                    for x in actions:
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
                    for x in actions:
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

class RandomTree(Digraph):
    """
    Random generator for trees, using random Pruefer codes

    Parameter:
        numerOfNodes

    """
    def __init__(self,numberOfNodes=5, ndigits=2, hasIntegerValuation=True):
        from random import choice
        from decimal import Decimal
        self.name = 'randomTree'
        self.order = numberOfNodes
        actions = {}
        nodes = [str(x+1) for x in range(numberOfNodes)]
        for x in nodes:
            actions[x] = {'name': 'node %s' % x}
        self.actions = actions
        print(actions)
        precision = pow(10,ndigits)
        if hasIntegerValuation:
            self.valuationdomain = {'min':-precision, 'med':0, 'max':precision}
        else:
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
        self.valuationdomain['hasIntegerValuation'] = hasIntegerValuation
        # init relation dictionary
        relation = {}
        nodeKeys = [x for x in actions]
        print(nodeKeys)
        for x in nodeKeys:
            relation[x] = {}
            for y in nodeKeys:
                relation[x][y] = self.valuationdomain['min']
        nodes = [x for x in range(len(nodeKeys))]
        pruefer = []
        for i in range(len(nodeKeys)-2):
            pruefer.append(choice(nodes))
        print(pruefer)
        pairs = self.prufer_to_tree(pruefer)
        for (i,j) in pairs:
            relation[str(i+1)][str(j+1)] = Decimal('1.0')
            relation[str(j+1)][str(i+1)] = Decimal('1.0')
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def prufer_to_tree(self,a):
        tree = []
        T = list(range(0, len(a)+2))
        print(T)
        # the degree of each node is how many times it appears
        # in the sequence
        deg = [1]*len(T)
        print(deg)
        for i in a: deg[i] += 1

        # for each node label i in a, find the first node j with degree 1 and add
        # the edge (j, i) to the tree
        for i in a:
            for j in T:
                if deg[j] == 1:
                    tree.append((i,j))
                    # decrement the degrees of i and j
                    deg[i] -= 1
                    deg[j] -= 1
                    break

        last = [x for x in T if deg[x] == 1]
        tree.append((last[0],last[1]))

        return tree


class RandomRegularDigraph(Digraph):
    """
    Parameters:
        order and degree.

    Specialization of Digraph class for random regular symmetric instances.

    """
    def __init__(self,order=7,degree=2):
        import random,copy
        # check feasability
        r = (order * degree) % 2
        if degree >= order or r == 1:
            print('Graph not feasable (1) !!')
        else:
            self.name = 'randomRegular'
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = []
            for x in actionlist:
                actions.append(str(x))
            self.actions = actions
            self.valuationdomain = {'min':Decimal('-1.0'), 'med':Decimal('0.0'), 'max':Decimal('1.0')}
            random.seed()
            # create a random pairing
            feasable = 0
            s = 0
            while feasable == 0 and s < 100:
                s += 1
                edges = []
                cells = []
                degreeseq = {}
                for x in actions:
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
                for x in actions:
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

class EmptyDigraph(Digraph):
    """
    Parameters:
        order > 0 (default=5); valuationdomain =(Min,Max).

    Specialization of the general Digraph class for generating
    temporary empty graphs of given order in {-1,0,1}.

    """
    def __init__(self,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        self.name = 'empty'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        Min = Decimal(str((valuationdomain[0])))
        Max = Decimal(str((valuationdomain[1])))
        Med = (Max + Min)/2
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class IndeterminateDigraph(Digraph):
    """
    Parameters: order > 0; valuationdomain =(Min,Max).
    Specialization of the general Digraph class for generating
    temporary empty graphs of order 5 in {-1,0,1}.
    """
    def __init__(self,other=None,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        self.name = 'indeterminate'
        if other == None:
            self.order = order
            actionlist = list(range(order+1))
            actionlist.remove(0)
            actions = []
            for x in actionlist:
                actions.append(str(x))

            Min = Decimal(str(valuationdomain[0]))
            Max = Decimal(str(valuationdomain[1]))
            Med = (Max + Min)/Decimal('2')
            self.valuationdomain = {'min':Min,'med':Med,'max':Max}

        else:
            self.__class__ = other.__class__
            self.order = other.order
            actions = other.actions
            self.valuationdomain = other.valuationdomain
            Med = self.valuationdomain['med']

        self.actions = actions

        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class CirculantDigraph(Digraph):
    """
    Parameters:
        | order > 0;
        | valuationdomain ={'min':m, 'max':M};
        | circulant connections = list of positive
               and/or negative circular shifts of value 1 to n.

    Specialization of the general Digraph class for generating
    temporary circulant digraphs

    Default instantiation C_7:
        | order = 7,
        | valuationdomain = {'min':-1.0,'max':1.0},
        | circulants = [-1,1].

    """
    def __init__(self,order=7,valuationdomain = {'min':Decimal('-1.0'),'max':Decimal('1.0')},circulants = [-1,1]):
        import sys,array,copy
        self.name = 'c'+str(order)
        self.order = order
        self.circulants = circulants
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        arcs = [] # circulant arcs
        for x in actionlist:
            for y in circulants:
                r = (x + y) % order
                if r == 0:
                    arcs.append((str(x), str(order)))
                else:
                    arcs.append((str(x), str(r)))
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if x == y:
                    relation[x][y] = Min
                elif (x,y) in arcs:
                    relation[x][y] = Max
                else:
                    relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Circulant graph : ', self.name)
        print('Order           : ', self.order)
        print('Circulants      : ', self.circulants)

class KneserDigraph(Digraph):
    """
    Parameters:
        | n > 0; n > j > 0;
        | valuationdomain ={'min':m, 'max':M}.

    Specialization of the general Digraph class for generating
    temporary Kneser digraphs

    Default instantiation as Petersen graph:
        n = 5, j = 2, valuationdomain = {'min':-1.0,'max':1.0}.

    """

    def __init__(self,n=5,j=2,valuationdomain = {'min':-1.0,'max':1.0}):
        import sys,array,copy
        self.name = 'kneser-'+str(n)+'-'+str(j)
        self.n = n
        self.j = j
        na = list(range(n+1))
        na.remove(0)
        ob = set()
        for x in na:
            ob.add(str(x))
        obActions = []
        for x in self.kChoices(ob,j):
            obActions.append(frozenset(x))
        order = len(obActions)
        self.order = order
        actions = []
        for i in range(order):
            actions.append(str(i+1))
        self.actions = actions
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        aindex = {}
        for i in range(order):
            aindex[actions[i]]=obActions[i]
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if aindex[x] & aindex[y] == set():
                    relation[x][y] = Max
                else:
                    relation[x][y] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Kneser graph    : ', self.name)
        print('n               : ', self.n)
        print('j               : ', self.j)
        print('order           : ', self.order)


class GridDigraph(Digraph):
    """
    Parameters:
        n,m > 0; valuationdomain ={'min':m, 'max':M}.

    Specialization of the general Digraph class for generating
    temporary Grid digraphs of dimension n times m.

    Default instantiation (5 times 5 Grid Digraph):
        n = 5, m=5, valuationdomain = {'min':-1.0,'max':1.0}.

    Randomly orientable with hasRandomOrientation=True (default=False).

    """

    def __init__(self,n=5,m=5,valuationdomain = {'min':-1.0,'max':1.0},hasRandomOrientation=False,hasMedianSplitOrientation=False):
        import sys,array,copy
        self.name = 'grid-'+str(n)+'-'+str(m)
        self.n = n
        self.m = m
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
        Min = Decimal(str(valuationdomain['min']))
        Max = Decimal(str(valuationdomain['max']))
        Med = (Max + Min)/Decimal('2')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {} # instantiate relation
        for x in actions:
            relation[x] = {}
            for y in actions:
                if gridNodes[x][1] == gridNodes[y][1]:
                    if gridNodes[x][0] == gridNodes[y][0]-1 :
                        relation[x][y] = Max
                    elif gridNodes[x][0] == gridNodes[y][0]+1:
                        relation[x][y] = Max
                    else:
                        relation[x][y] = Min
                elif gridNodes[x][0] == gridNodes[y][0]:
                    if gridNodes[x][1] == gridNodes[y][1]-1:
                        relation[x][y] = Max
                    elif gridNodes[x][1] == gridNodes[y][1]+1:
                        relation[x][y] = Max
                    else:
                        relation[x][y] = Min
                else:
                    relation[x][y] = Min

        if hasRandomOrientation:
            import random
            random.seed()
            for x in actions:
                relation[x] = {}
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

        elif hasMedianSplitOrientation:
            for x in actions:
                relation[x] = {}
                for y in actions:
                    if gridNodes[x][1] == gridNodes[y][1]:
                        if gridNodes[x][0] == gridNodes[y][0]-1 :
                            if gridNodes[y][1] <= gridNodes[x][0]:
                                relation[x][y] = Max
                                relation[y][x] = Min
                            else:
                                relation[x][y] = Min
                                relation[y][x] = Max
                        elif gridNodes[x][0] == gridNodes[y][0]+1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        else:
                            relation[x][y] = Min

                    elif gridNodes[x][0] == gridNodes[y][0]:
                        if gridNodes[x][1] == gridNodes[y][1]-1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        elif gridNodes[x][1] == gridNodes[y][1]+1:
                            if gridNodes[y][1] >= gridNodes[x][0]:
                                relation[x][y] = Min
                                relation[y][x] = Max
                            else:
                                relation[x][y] = Max
                                relation[y][x] = Min
                        else:
                            relation[x][y] = Min
                    else:
                        relation[x][y] = Min

        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showShort(self):
        print('*----- show short --------------*')
        print('Grid graph    : ', self.name)
        print('n             : ', self.n)
        print('m             : ', self.m)
        print('order         : ', self.order)


class CompleteDigraph(Digraph):
    """
    Parameters:
        order > 0; valuationdomain=(Min,Max).

    Specialization of the general Digraph class for generating
    temporary complete graphs of order 5 in {-1,0,1} by default.

    """
    def __init__(self,order=5,valuationdomain = (-1.0,1.0)):
        import sys,array,copy
        self.name = 'complete'
        self.order = order
        actionlist = list(range(order+1))
        actionlist.remove(0)
        actions = []
        for x in actionlist:
            actions.append(str(x))
        self.actions = actions
        Max = Decimal(str((valuationdomain[1])))
        Min = Decimal(str((valuationdomain[0])))
        Med = (Max + Min)/2
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                if x == y:
                    relation[x][y] = Min
                else:
                    relation[x][y] = Max
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


class PolarisedDigraph(Digraph):
    """
    ... parameters::

        digraph + beta cut level between Med and Max.

        KeepValues=True/False,

        AlphaCut=False/True,

        StrictCut=False/True

    """
    def __init__(self,digraph=None,level=None,KeepValues=True,AlphaCut=False,StrictCut=False):
        if digraph == None:
            digraph = RandomValuationDigraph()
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        if level == None:
            level = Max - (Max - Med)*Decimal('0.5')
        self.name = 'cut_' + str(level)+ '_' + str(digraph.name)
        self.actions = digraph.actions
        if AlphaCut:
            self.relation = self.constructAlphaCutRelation(digraph.relation,
                                                           level=level,
                                                           StrictCut=StrictCut)
        else:
            self.relation = self.constructBetaCutRelation(digraph.relation,
                                                          level=level,
                                                          KeepValues=KeepValues,
                                                          StrictCut=StrictCut)

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructBetaCutRelation(self,relationin, level, KeepValues=True,AlphaCut=False,StrictCut=False):
        """
        Parameters: relation and cut level.
        Flags: KeepValues (True), AlphaCut(False, unilateral cut), StrictCut (False)
        Renders the polarised relation.

        """
        Debug = False
        if Debug:
            print('Level, KeepValues,AlphaCut', level, KeepValues,AlphaCut)
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        level = Decimal(str(level))
        compLevel = Max - level + Min
        if level < Med:
            print('Cut Level :', level, 'too low !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        elif level > Max:
            print('Cut Level :', level, 'too high !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        else:
            relationout = {}
            for a in actions:
                relationout[a] = {}
                for b in actions:
                    if StrictCut:
                        if relationin[a][b] > level:
                            if KeepValues:
                                relationout[a][b] = relationin[a][b]
                            else:
                                relationout[a][b] = Max
                        elif relationin[a][b] < compLevel:
                            if KeepValues:
                                relationout[a][b] = relationin[a][b]
                            else:
                                relationout[a][b] = Min
                        else:
                            relationout[a][b] = Med
                    else:
                        if relationin[a][b] >= level:
                            if KeepValues:
                                relationout[a][b] = relationin[a][b]
                            else:
                                relationout[a][b] = Max
                        elif relationin[a][b] <= compLevel:
                            if KeepValues:
                                relationout[a][b] = relationin[a][b]
                            else:
                                relationout[a][b] = Min
                        else:
                            relationout[a][b] = Med
        return relationout

    def constructAlphaCutRelation(self,relationin, level, KeepValues=True,AlphaCut=False,StrictCut=False):
        """
        Parameters: relation and cut level.
        Renders the polarised relation.
        """
        Debug = False
        if Debug:
            print('Level, KeepValues,AlphaCut', level, KeepValues,AlphaCut)
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        level = Decimal(str(level))
        relationout = {}
        for a in actions:
            relationout[a] = {}
            for b in actions:
                if StrictCut:
                    if relationin[a][b] > level:
                        relationout[a][b] = Max
                    else:
                        relationout[a][b] = Min
                else:
                    if relationin[a][b] >= level:
                        relationout[a][b] = Max
                    else:
                        relationout[a][b] = Min
        return relationout


class MedianExtendedDigraph(Digraph):
    """
    Parameters:
        digraph + beta cut level between Med and Max.

    Specialisation of Outranking relation.

    """
    def __init__(self,digraph=None,Level=None):
        if digraph == None:
            digraph = RandomValuationDigraph()
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        if Level == None:
            Level = Max - (Max - Med)*0.5
        self.name = 'cut_' + str(Level)+ '_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self.constructRelation(digraph.relation, Level)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationin, Level):
        """
        Parameters: relation and cut level.
        Renders the polarised relation.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        CompLevel = Max - Level + Min
        if Level < Med:
            print('Cut Level :', Level, 'too low !!!')
            print(self.valuationdomain)
            print('Original relation not changed !!!')
            return relationin
        else:
            relationout = {}
            for a in actions:
                relationout[a] = {}
                for b in actions:
                    if relationin[a][b] <= Level and relationin[a][b] >= CompLevel:
                        relationout[a][b] = Med
                    else:
                        relationout[a][b] = relationin[a][b]
        return relationout

class DualDigraph(Digraph):
    """
    Instantiates the dual Digraph object of a given other Digraph instance

    """
    def __init__(self,other):
        from copy import deepcopy
        self.name = 'dual_' + str(other.name)
        try:
            self.description = deepcopy(other.description)
        except AttributeError:
            pass
        try:
            self.criteria = deepcopy(other.criteria)
        except AttributeError:
            pass
        try:
            self.evaluation = deepcopy(other.evaluation)
        except AttributeError:
            pass
        self.valuationdomain = deepcopy(other.valuationdomain)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.actions = deepcopy(other.actions)
        self.order = len(self.actions)
        self.relation = self.constructRelation(other.relation)
        self.__class__ = other.__class__
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationIn):
        """
        Renders the dual relation with formula:
        relationOut[a][b] = Max - relationIn[a][b] + Min
        where Max (resp. Min) equals valuation maximum (resp. minimum).
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                relationOut[a][b] = Max - relationIn[a][b] + Min
        return relationOut

class PreferenceDigraph(Digraph):
    """
    Initiates the valued difference S(a,b) - S(b,a) of a Digraph instance.
    """
    def __init__(self,digraph):
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.name = 'dual_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self.constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationIn):
        """
        Parameters: relation
        Renders the polarised relation.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                relationOut[a][b] = (relationIn[a][b] - relationIn[b][a])/Decimal('2.0')
        return relationOut

class AsymmetricPartialDigraph(Digraph):
    """
    Renders the asymmetric part of a Digraph instance
    """
    def __init__(self,digraph):
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.name = 'asymmetric_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self.constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationIn):
        """
        Parameters: relation and cut level.
        Renders the polarised relation.
        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                if a != b:
                    if relationIn[a][b] >= Med and relationIn[b][a] <= Med:
                        relationOut[a][b] = relationIn[a][b]
                    elif relationIn[a][b] <= Med and relationIn[b][a] >= Med:
                        relationOut[a][b] = relationIn[a][b]
                    else:
                        relationOut[a][b] = Med
                    ## relationOut[a][b] = min(relationIn[a][b],Max-relationIn[b][a]+Min)
                else:
                    relationOut[a][b] = Med
        return relationOut

class AsymmetricDigraph(Digraph):
    """
    Renders the asymmetric of a Digraph instance
    """
    def __init__(self,digraph):
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.name = 'asymmetric_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self.constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationIn):
        """
        Parameters:
            relation and cut level.

        Renders the polarised relation.

        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                relationOut[a][b] = min( relationIn[a][b], (Max-relationIn[b][a]+Min) )
                ## if a != b:
                ##     if relationIn[a][b] >= Med and relationIn[b][a] <= Med:
                ##         relationOut[a][b] = relationIn[a][b]
                ##     elif relationIn[a][b] <= Med and relationIn[b][a] >= Med:
                ##         relationOut[a][b] = relationIn[a][b]
                ##     else:
                ##         relationOut[a][b] = Med
                ##     ## relationOut[a][b] = min(relationIn[a][b],Max-relationIn[b][a]+Min)
                ## else:
                ##     relationOut[a][b] = Med
        return relationOut

class SymmetricPartialDigraph(Digraph):
    """
    Renders the symmetric part of a Digraph instance
    """
    def __init__(self,digraph):
        self.valuationdomain = digraph.valuationdomain
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        self.name = 'symmetric_' + str(digraph.name)
        self.actions = digraph.actions
        self.relation = self.constructRelation(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def constructRelation(self,relationIn):
        """
        Parameters:
            relation and cut level.

        Renders the polarised relation.

        """
        actions = self.actions
        Min = self.valuationdomain['min']
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        relationOut = {}
        for a in actions:
            relationOut[a] = {}
            for b in actions:
                if a != b:
                    if relationIn[a][b] >= Med and relationIn[b][a] >= Med:
                        relationOut[a][b] = relationIn[a][b]
                    elif relationIn[a][b] <= Med and relationIn[b][a] <= Med:
                        relationOut[a][b] = relationIn[a][b]
                    else:
                        relationOut[a][b] = Med
                    ## relationOut[a][b] = min(relationIn[a][b],relationIn[b][a])
                else:
                    relationOut[a][b] = Min
        return relationOut

class kChoicesDigraph(Digraph):
    """
    Parameters:
        | digraph := Stored or memory resident digraph instance
        | k := cardinality of the choices

    Specialization of general Digraph class for instantiation
    of chordless odd circuits augmented digraphs.
    """
    def __init__(self,digraph=None,k=3):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
        if digraph == None:
            digraph = RandomValuationDigraph()
            self.name = str(digraph.name)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph)):
            self.name = str(digraph.name)

        self.valuationdomain = digraph.valuationdomain.copy()
        dactions = [x for x in digraph.actions]
        drelation = copy.deepcopy(digraph.relation)
        actions = {}
        for kChoice in Digraph.kChoices(digraph,dactions,k):
            cn = '_'
            for x in kChoice:
                cn += str(x) + '_'
            commentString = '%d-choice candidate' % (k)
            actions[frozenset(kChoice)] = {'name': cn, 'comment': commentString}
        self.actions = actions
        self.order = len(self.actions)
        self.relation = self.computeRelation(drelation)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def computeRelation(self,relation):
        """
        computing the relation on kChoices
        """
        Min = self.valuationdomain['min']
        kChoices = self.actions
        krelation = {}
        for xch in kChoices:
            krelation[xch] = {}
            for ych in kChoices:
                krelation[xch][ych] = Min
                for x in (xch-ych):
                    for y in (ych-xch):
                        krelation[xch][ych] = max(krelation[xch][ych],relation[x][y])
        return krelation

#########

class WeakCocaDigraph(Digraph):
    """
    Parameters:
        Stored or memory resident digraph instance.

    Specialization of general Digraph class for instantiation
    of weak chordless odd circuits augmented digraphs.

    """
    def __init__(self,digraph=None,comment=None):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph

        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'weakcocosilent =', silent
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = copy.copy(g.actions)
            self.valuationdomain = copy.copy(g.valuationdomain)
            self.relation = copy.deepcopy(g.relation)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.copy(digraph.actions)
            self.valuationdomain = copy.copy(digraph.valuationdomain)
            self.relation = copy.deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            exec(compile(open(fileName).read(), fileName, 'exec'))
            self.name = digraph
            self.actions = locals()['actionset']
            self.valuationdomain = locals()['valuationdomain']
            self.relation = locals()['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.weakCircuits = set()
        self.closureWeakChordlessOddCircuits(comment=silent)

    def closureWeakChordlessOddCircuits(self,comment=None):
        """
        Closure of cdordless odd circuits extraction.
        """
        newCircuits = None
        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'closuresilent=', silent
        while newCircuits != set():
            coc = set(self.weakCircuits)
            self.weakChordlessOddCircuits(comment=silent)
            self.addWeakCircuits(comment=silent)
            newCircuits = self.weakCircuits - coc

    def addWeakCircuits(self,comment=None):
        """
        Augmenting self with self.weakCircuits.
        """
        import copy,time
        if comment == None:
            silent = True
        else:
            silent = not(comment)
        #print 'addweaksilent = ', silent
        order0 = self.order
        actions = set(self.actions)
        weakCircuits = self.weakCircuits
        valuationdomain = self.valuationdomain
        weakGamma = self.weakGamma
        relation = self.relation
        for cycle in weakCircuits:
            cn = '_'
            dcycle = set()
            acycle = set()
            for x in cycle:
                cn = cn + str(x) + '_'
                dcycle = dcycle | weakGamma[x][0]
                dcycle = dcycle | set([x])
                acycle = acycle | weakGamma[x][1]
                acycle = acycle | set([x])
            weakGamma[cn]=(dcycle,acycle)
            for x in actions:
                if x in cycle:
                    dx0 = weakGamma[x][0] | set([cn])
                    dx1 = weakGamma[x][1] | set([cn])
                    weakGamma[x] = (dx0,dx1)
                    relxcn = relation[x]
                    relxcn[cn] = valuationdomain['max']
                    relation[x] = relxcn
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[x][y])
                        relxcn = relation[x]
                        relxcn[cn] = relxy
                        relation[x] = relxcn
            relcycle = {}
            for x in actions:
                if x in cycle:
                    relcycle[x] = valuationdomain['max']
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[y][x])
                    relcycle[x] = relxy
            relcycle[cn] = valuationdomain['min']
            relation[cn] = relcycle
            actions = actions | set([cn])
        self.actions = list(actions)
        self.order = len(actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        new = self.order - order0
        if not silent:
            if self.order == order0:
                print('  No weak circuits added !')
            else:
                print('  ',new,' weak circuit(s) added!')

    def showCircuits(self):
        """
        show methods for chordless odd circuits in CocaGraph
        """
        print('*---- Chordless odd circuits ----*')
        for circ in self.weakCircuits:
            deg = self.circuitMinCredibility(circ)
            print(list(circ), ', credibility :', deg)

#--------------------
class CoceDigraph(Digraph):
    """
    Parameters:
        Stored or memory resident digraph instance.

    Specialization of general Digraph class for instantiation
    of chordless odd circuits eliminated digraphs.

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,Comments=False,Debug=False):
        import random,sys,array
        from copy import deepcopy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph

        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = deepcopy(g.actions)
            self.valuationdomain = deepcopy(g.valuationdomain)
            self.relation = deepcopy(g.relation)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph,BipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = deepcopy(digraph.actions)
            self.valuationdomain = deepcopy(digraph.valuationdomain)
            self.relation = deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            exec(compile(open(fileName).read(), fileName, 'exec'))
            self.name = digraph
            self.actions = locals()['actionset']
            self.valuationdomain = locals()['valuationdomain']
            self.relation = locals()['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        level,pg = self.iterateCocElimination(Comments=Comments, Debug=Debug)
        if pg != None:
            self.name = '%s_pol_%.2f' % (self.name,level)
            self.relation = deepcopy(pg.relation)
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()
            self.weakGamma = self.weakGammaSets()


    def iterateCocElimination(self,Comments=True,Debug=False):
        """
        Eliminates all chordless odd circuits with rising valuation cut levels.
        Renders a tuple (level,polarisedDigraph) where level is the
        necessary bipolar cut level for eliminating all chordless odd circuits,
        and polarisedDigraph is the resulting digraph instance.
        Renders (None,None) if no chordless odd circuit is detected.
        """
        from copy import deepcopy
        from time import time
        if Debug:
            Comments=True
        gcd = deepcopy(self)

        qualmaj0 = gcd.valuationdomain['med']
        if Comments:
            print('Chorless odd circuits elimination')
            i = 0
        qualmaj = gcd.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
        while qualmaj > qualmaj0:
            if Comments:
                i += 1
                print('--> Iteration %d' % (i))
                t0 = time()
            if qualmaj < gcd.valuationdomain['max']:
                pg = PolarisedDigraph(gcd,qualmaj,
                                      StrictCut=True,
                                      KeepValues=True)
            else:
                pg = PolarisedDigraph(gcd,qualmaj,
                                      StrictCut=False,
                                      KeepValues=True)
            qualmaj0 = qualmaj
            qualmaj = pg.minimalValuationLevelForCircuitsElimination(Debug=Debug,Comments=Comments)
        if i == 0:
            return (None,None)
        else:
            return (qualmaj0,pg)


#--------------------
class CocaDigraph(Digraph):
    """
    Parameters:
        Stored or memory resident digraph instance.

    Specialization of general Digraph class for instantiation
    of chordless odd circuits augmented digraphs.

    """
    def __init__(self,digraph=None,Cpp=False,Piping=False,Comments=False):
        import random,sys,array,copy
        from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
        ## if comment == None:
        ##     silent = True
        ## else:
        ##     silent = not(comment)
        if digraph == None:
            g = RandomValuationDigraph()
            self.name = str(g.name)
            self.actions = copy.copy(g.actions)
            self.valuationdomain = copy.copy(g.valuationdomain)
            self.relation = copy.deepcopy(g.relation)

        elif isinstance(digraph,(Digraph,OutrankingDigraph,RandomOutrankingDigraph,BipolarOutrankingDigraph)):
            self.name = str(digraph.name)
            self.actions = copy.copy(digraph.actions)
            self.valuationdomain = copy.copy(digraph.valuationdomain)
            self.relation = copy.deepcopy(digraph.relation)
        else:
            fileName = digraph + 'py'
            exec(compile(open(fileName).read(), fileName, 'exec'))
            self.name = digraph
            self.actions = locals()['actionset']
            self.valuationdomain = locals()['valuationdomain']
            self.relation = locals()['relation']

        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        self.closureChordlessOddCircuits(Cpp=Cpp,Piping=Piping,Comments=Comments)

    def closureChordlessOddCircuits(self,Cpp=False,Piping=False,Comments=False):
        """
        Closure of chordless odd circuits extraction.
        """
        newCircuits = None
        self.circuitsList = []
        while newCircuits != set():
            initialCircuits = set([x for cl,x in self.circuitsList])
            if Cpp:
                if Piping:
                    self.computeCppInOutPipingChordlessCircuits(Odd=True,Debug=Comments)
                else:
                    self.computeCppChordlessCircuits(Odd=True,Debug=Comments)
            else:
                self.computeChordlessCircuits(Odd=True,Comments=Comments)
            self.addCircuits(Comments=Comments)
            currentCircuits = set([x for cl,x in self.circuitsList])
            if Comments:
                print('initialCircuits, currentCircuits', initialCircuits, currentCircuits)
            newCircuits = currentCircuits - initialCircuits

    def addCircuits(self,Comments=False):
        """
        Augmenting self with self.circuits.
        """
        import copy,time
        order0 = self.order
        if not(isinstance(self.actions,dict)):
            actions = {}
            for x in self.actions:
                actions[x] = {'name':x}
        else:
            actions = self.actions

        #ListActions = [frozenset([x]) for x in actions]
        circuitsList = self.circuitsList
        if Comments:
            print('list of circuits: ', circuitsList)
        valuationdomain = self.valuationdomain
        gamma = self.gamma
        relation = self.relation
        for (cycleList,cycle) in circuitsList:
            cn = '_'
            dcycle = set()
            acycle = set()
            for x in cycleList:
                if isinstance(x,frozenset):
                    cn += actions[x]['name'] + '_'
                else:
                    cn += str(x) + '_'
                dcycle = dcycle | gamma[x][0]
                dcycle = dcycle | set([x])
                acycle = acycle | gamma[x][1]
                acycle = acycle | set([x])
            gamma[cycle]=(dcycle,acycle)
            for x in actions:
                if x in cycle:
                    dx0 = gamma[x][0] | set([cycle])
                    dx1 = gamma[x][1] | set([cycle])
                    gamma[x] = (dx0,dx1)
                    relxcn = relation[x]
                    relxcn[cycle] = valuationdomain['max']
                    relation[x] = relxcn
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[x][y])
                        relxcn = relation[x]
                        relxcn[cycle] = relxy
                        relation[x] = relxcn
            relcycle = {}
            for x in actions:
                if x in cycle:
                    relcycle[x] = valuationdomain['max']
                else:
                    relxy = valuationdomain['min']
                    for y in cycle:
                        relxy = max(relxy,relation[y][x])
                    relcycle[x] = relxy
            relcycle[cycle] = valuationdomain['min']
            relation[cycle] = relcycle
            name = 'chordless odd %d-circuit' % (len(cycle))
            actions[cycle] = {'name': cn, 'comment': name}
            if Comments:
                print(actions[cycle])
        #self.actions = list(actions)
        self.actions = actions
        self.order = len(actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.weakGamma = self.weakGammaSets()
        new = self.order - order0
        if Comments:
            if self.order == order0:
                print('  No circuits added !')
            else:
                print('  ',new,' circuit(s) added!')

    def showCircuits(self):
        """
        show methods for chordless odd circuits in CocaGraph
        """
        print('*---- Chordless circuits ----*')
        for (circList,circSet) in self.circuitsList:
            deg = self.circuitMinCredibility(circSet)
            print(circList, ', credibility :', deg)
        print('Coca graph of order %d with %d odd chordles circuits.' % (len(self.actions), len(self.circuitsList)))
        #print len(aself.circuitsList),' cirduits

    def showComponents(self):
        print('*--- Connected Components ---*')
        k=1
        for Comp in self.components():
            component = list(Comp)
            #component.sort()
            print(str(k) + ': ' + str(component))
            xk = k + 1

#------------------------------------------

class StrongComponentsCollapsedDigraph(Digraph):
    """
    Reduction of Digraph object to its strong components.
    """
    def __init__(self,digraph=None):

        if digraph == None:
           print('Error: you must provide a valid digraph to the constructor!')
        else:
           self.name = digraph.name + '_Scc'
           self.valuationdomain = digraph.valuationdomain
           scc = digraph.strongComponents()
           actions = {}
           for i,strongComponent in enumerate(scc):
               actionShortName = 'Scc_'+str(i+1)
               actionKey = strongComponent
               actionName = '_'
               for x in strongComponent:
                   actionName += str(x)+'_'
               actions[actionKey] = {'name': actionName,\
                                     'shortName': actionShortName,\
                                     'comment': 'collapsed strong component'}
           self.actions = actions
           relation = {}
           actionsList = [x for x in actions]
           actionsList.sort()
           for xsc in actionsList:
               relation[xsc] = {}
               for ysc in actionsList:
                   relation[xsc][ysc] = self.valuationdomain['min']
                   for x in xsc:
                       for y in ysc:
                           if x == y:
                               relation[xsc][ysc] = self.valuationdomain['med']
                           elif digraph.relation[x][y] > relation[xsc][ysc]:
                               relation[xsc][ysc] = digraph.relation[x][y]
           self.relation = relation
           self.order = len(self.actions)
           self.gamma = self.gammaSets()
           self.notGamma = self.notGammaSets()

    def showComponents(self):
        print('short', '\t', 'content')
        for x in self.actions:
            print(self.actions[x]['shortName'], '\t', self.actions[x]['name'])
#-------------------------------------------------------


# ------------ XML encoded stored Digraph instances

class XMLDigraph24(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XML formatted digraphs.
    """

    def __init__(self,fileName='testsaveXML'):
        from xml.sax import make_parser
        xmlDigraph = _XMLDigraphHandler()
        saxParser = make_parser()
        saxParser.setContentHandler(xmlDigraph)
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        saxParser.parse(fo)
        self.name = xmlDigraph.name
        self.category = xmlDigraph.category
        self.subcategory = xmlDigraph.subcategory
        self.actions = xmlDigraph.actions
        self.valuationdomain = xmlDigraph.valuationdomain
        Min = xmlDigraph.valuationdomain['min']
        Max = xmlDigraph.valuationdomain['max']
        Med = Min + ((Max - Min)/2.0)
        self.valuationdomain['med'] = Med
        self.relation = xmlDigraph.relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):

        if self.category == 'outranking':
            Digraph.showAll(self)
            self.showPreKernels()
            self.showGoodChoices()
            self.showBadChoices()

        else:
            Digraph.showAll(self)

class XMLDigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XML formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xml).
    """

    def __init__(self,fileName='testsaveXML'):
        from xml.etree import ElementTree
        fileNameExt = fileName + '.xml'
        fo = open(fileNameExt,'r')
        digraph = ElementTree.parse(fo).getroot()
        self.category = digraph.attrib['category']
        self.subcategory = digraph.attrib['subcategory']
        self.name = digraph.find('header').find('name').text
        self.author = digraph.find('header').find('author').text
        self.reference = digraph.find('header').find('reference').text
        Min = Decimal(digraph.find('valuationdomain').find('min').text)
        Max = Decimal(digraph.find('valuationdomain').find('max').text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        actions = [action.text for action in digraph.find('nodes').findall('node')]
        self.actions = actions
        relation = {}
        for x in actions:
            relation[x] = {}
        for arc in digraph.find('relation').findall('arc'):
            relation[arc.find('i').text][arc.find('t').text] = Decimal(arc.find('v').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class XMCDADigraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XMCDA formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xmcda).
    """

    def __init__(self,fileName='temp'):
        from xml.etree import ElementTree
        try:
            fileNameExt = fileName + '.xmcda'
            fo = open(fileNameExt,'r')
        except:
            try:
                fileNameExt = fileName + '.xml'
                fo = open(fileNameExt,'r')
            except:
                print("Error: file %s{.xml|.xmcda}  not found" % (fileName))
        XMCDA = ElementTree.parse(fo).getroot()
        description = {}
        for elem in [x for x in XMCDA.find('caseReference').getchildren()]:
            description[elem.tag] = elem.text
        self.description = description
        try:
            self.name = description['name']
        except:
            self.name ='temp'
        try:
            self.author = description['author']
        except:
            self.author = 'digraphs module (RB)'
        try:
            self.reference = description['comment']
        except:
            self.reference = 'XMCDA 1.0 Digraph input method.'
        Min = Decimal(XMCDA.find('relationOnAlternatives').find('valuationDomain').find('minimum').getchildren().pop().text)
        Max = Decimal(XMCDA.find('relationOnAlternatives').find('valuationDomain').find('maximum').getchildren().pop().text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain
        actions = {}
        for alternative in XMCDA.find('alternatives').findall('alternative'):
            id = alternative.attrib['id']
            actions[id] = {}
            for elem in [x for x in alternative.find('description').getchildren()]:
                actions[id][elem.tag] = elem.text
        self.actions = actions
        relation = {}
        try:
            if XMCDA.find('relationOnAlternatives').find('description').find('type').text == 'outrankingDigraph':
                self.category = 'outranking'
            else:
                self.category = 'general'
        except:
            pass
        for x in actions:
            relation[x] = {}
        for arc in XMCDA.find('relationOnAlternatives').find('arcs').findall('arc'):
            try:
                relation[arc.find('from').find('alternativeID').text][arc.find('to').find('alternativeID').text] = Decimal(arc.find('value').find('real').text)
            except:
                relation[arc.find('from').find('alternativeID').text][arc.find('to').find('alternativeID').text] = Decimal(arc.find('value').find('integer').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):
        try:
            if self.category == 'outranking':
                Digraph.showAll(self)
                self.showPreKernels()
                self.showGoodChoices()
                self.showBadChoices()
            else:
                Digraph.showAll(self)
        except:
            Digraph.showAll(self)

class XMCDA2Digraph(Digraph):
    """
    Specialization of the general Digraph class for reading
    stored XMCDA-2.0 formatted digraphs. Using the inbuilt module
    xml.etree (for Python 2.5+).

    Param:
        fileName (without the extension .xmcda).
    """

    def __init__(self,fileName='temp'):
        from xml.etree import ElementTree

        fileNameExt = fileName + '.xml'
        try:
            fo = open(fileNameExt,'r')
        except:
            fileNameExt = fileName + '.xmcda'
            try:
                fo = open(fileNameExt,'r')
            except:
                fileNameExt = fileName + '.xmcda2'
                try:
                    fo = open(fileNameExt,'r')
                except:
                    print("Error: file %s  not found" % (fileNameExt))

        print("file %s is being read:" % (fileNameExt))
        XMCDA = ElementTree.parse(fo).getroot()
        try:
            self.name = XMCDA.attrib['name']
        except:
            self.name ='temp'

        description = {}
        for elem in [x for x in XMCDA.find('projectReference').getchildren()]:
            description[elem.tag] = elem.text
        self.description = description
        try:
            self.author = description['author']
        except:
            self.author = 'digraphs module (RB)'
        try:
            self.reference = description['comment']
        except:
            self.reference = 'XMCDA 1.0 Digraph input method.'

        Min = Decimal(XMCDA.find('alternativesComparisons').find('valuation').find('quantitative').find('minimum').getchildren().pop().text)
        Max = Decimal(XMCDA.find('alternativesComparisons').find('valuation').find('quantitative').find('maximum').getchildren().pop().text)
        Med = Min + ((Max - Min)/Decimal('2.0'))
        valuationdomain = {}
        valuationdomain['min'] = Min
        valuationdomain['med'] = Med
        valuationdomain['max'] = Max
        self.valuationdomain = valuationdomain


        actions = {}
        for alternative in XMCDA.find('alternatives').findall('alternative'):
            id = alternative.attrib['id']
            actions[id] = {}
            actions[id]['name'] = alternative.attrib['name']
            for elem in [x for x in alternative.find('description').getchildren()]:
                actions[id][elem.tag] = elem.text
        self.actions = actions


        relation = {}
        try:
            if XMCDA.find('alternativesComparisons').attribute['mcdaConcept'] == 'outrankingDigraph':
                self.category = 'outranking'
            else:
                self.category = 'general'
        except:
            pass
        for x in actions:
            relation[x] = {}
        for pair in XMCDA.find('alternativesComparisons').find('pairs').findall('pair'):
            try:
                relation[pair.find('initial').find('alternativeID').text][pair.find('terminal').find('alternativeID').text] = Decimal(pair.find('value').find('real').text)
            except:
                relation[pair.find('initial').find('alternativeID').text][pair.find('terminal').find('alternativeID').text] = Decimal(pair.find('value').find('integer').text)
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showAll(self):
        try:
            if self.category == 'outranking':
                Digraph.showAll(self)
                self.showPreKernels()
                self.showGoodChoices()
                self.showBadChoices()
            else:
                Digraph.showAll(self)
        except:
            Digraph.showAll(self)

###  replace the old outrankingDigraphs
#from outrankingDigraphs import *

#############################################

#----------test Digraph class ----------------
if __name__ == "__main__":
    import sys,array
    from outrankingDigraphs import OutrankingDigraph, RandomOutrankingDigraph, BipolarOutrankingDigraph
    from votingDigraphs import CondorcetDigraph


    print('****************************************************')
    print('* Python digraphs module                           *')
    print('* $Revision: 1.697 $                               *')
    print('* Copyright (C) 2006-2007 University of Luxembourg *')
    print('* The module comes with ABSOLUTELY NO WARRANTY     *')
    print('* to the extent permitted by the applicable law.   *')
    print('* This is free software, and you are welcome to    *')
    print('* redistribute it if it remains free software.     *')
    print('****************************************************')

    narg = len(sys.argv)

    noTest = True

    if narg == 1:
        noTest = False

    elif narg == 2:
        if sys.argv[1] == '-r':
            g = RandomValuationDigraph()
        elif sys.argv[1] == '-rt':
            t = RandomPerformanceTableau()
            g = BipolarOutrankingDigraph(t)
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '-?':
            print('usage: digraphs.py [[-t|rt|v|av] <filename> | -r [n]] | -rt [[n] [m]]')
            print('  <filename> of valid python digraph (without .py extension)')
            print('  option = -t means valid performance tableau input.')
            print('  option = -rt means  performance tableau input.')
            print('  option = -v means valid voting profile input.')
            print('  option = -av means valid approval voting profile input.')
            print('  option = -r n : means a random digraph of order n (default n=10).')
            print('  option = -rt n m : means an outranking digraph from a random')
            print('                     performance tableau input with n actions and m criteria')
            print('                     (default n = 10, m = 7).')
            sys.exit(1)
        else:
            file = sys.argv[1]
            g = Digraph(file)
    elif narg == 3:
        if sys.argv[1] == '-r':
            order = int(sys.argv[2])
            g = RandomValuationDigraph(order)
        elif sys.argv[1] == '-rt':
            actions = int(sys.argv[2])
            t = RandomPerformanceTableau(numberOfActions=actions)
            g = BipolarOutrankingDigraph(t)
        elif sys.argv[1] == '-t':
            file = sys.argv[2]
            g = BipolarOutrankingDigraph(file)
        elif sys.argv[1] == '-v':
            file = sys.argv[2]
            g = CondorcetDigraph(file)
        elif sys.argv[1] == '-av':
            file = sys.argv[2]
            g = CondorcetDigraph(file,approvalVoting=True)
    elif narg == 4:
        if sys.argv[1] == '-rt':
            nActions = int(sys.argv[2])
            mCriteria = int(sys.argv[3])
            t = RandomPerformanceTableau(numberOfActions=nActions,numberOfCriteria=mCriteria)
            g = BipolarOutrankingDigraph(t)
    else:
        print('usage: digraphs.py [[-t|rt|v|av] <filename> | -r [n]] | -rt [[n] [m]]')
        print('  <filename> of valid python digraph (without .py extension)')
        print('  option = -t means valid performance tableau input.')
        print('  option = -rt means  performance tableau input.')
        print('  option = -v means valid voting profile input.')
        print('  option = -av means valid approval voting profile input.')
        print('  option = -r n : means a random digraph of order n (default n=10).')
        print('  option = -rt n m : means an outranking digraph from a random')
        print('                     performance tableau input with n actions and m criteria')
        print('                     (default n = 10, m = 7).')
        sys.exit(1)
    if noTest:
        print('*------ Results -------"')
        g.showRelationTable()
        g.showAll()
        g.showStatistics()

    else:
        print('*-------- Testing classes and methods -------')
        from time import time
        from operator import itemgetter
        t = RandomCBPerformanceTableau(numberOfActions=15)
        t.save('test')
        t = PerformanceTableau('test')
        g = BipolarOutrankingDigraph(t)
        g.iterateRankingByChoosing(Odd=False,Debug=True,CoDual=True)
        ## g = RandomValuationDigraph()
        ## print(g.computePrudentBestChoiceRecommendation(CoDual=False,Comments=True))


        ## coceg = CoceDigraph(g,Comments=True)
        ## #coceg.showStatistics()
        ## coceg.computeChordlessCircuits()

        ## g.showRubisBestChoiceRecommendation(Comments=True)
        # cog = CocaDigraph(g,Comments=True)
        # gcd = CoDualDigraph(cog)
        # gcd.computeGoodChoices()
        # gcd.computeBadChoices()
        # gcd.goodChoices.sort(key=itemgetter(7),reverse=True)
        # gcd.badChoices.sort(key=itemgetter(7),reverse=True)
        # print('==>> good choices')
        # for ch in gcd.goodChoices:
        #     print(ch[5])
        #     print(gcd.averageCoveringIndex(ch[5],direction="out"))
        #     print(gcd.averageCoveringIndex(ch[5],direction='in'))
        # print('==>> bad choices')
        # for ch in gcd.badChoices:
        #     print(ch[5])
        #     print(gcd.averageCoveringIndex(ch[5],direction="in"))
        #     print(gcd.averageCoveringIndex(ch[5],direction='out'))

        # cog = CoceDigraph(g,Comments=True)
        # gcd = CoDualDigraph(cog)
        # gcd.computeGoodChoices()
        # gcd.computeBadChoices()
        # gcd.goodChoices.sort(key=itemgetter(7),reverse=True)
        # gcd.badChoices.sort(key=itemgetter(7),reverse=True)
        # print('==>> good choices')
        # for ch in gcd.goodChoices:
        #     print(ch[5])
        #     print(gcd.averageCoveringIndex(ch[5],direction="out"))
        #     print(gcd.averageCoveringIndex(ch[5],direction='in'))
        # print('==>> bad choices')
        # for ch in gcd.badChoices:
        #     print(ch[5])
        #     print(gcd.averageCoveringIndex(ch[5],direction="in"))
        #     print(gcd.averageCoveringIndex(ch[5],direction='out'))
        ## #coceg.showRubisBestChoiceRecommendation()

        ## equivg = EquivalenceDigraph(g,coceg)

        ## print equivg.computeDeterminateness()
        ## print equivg.graphDetermination()
        ## print g.computeBipolarCorrelation(equivg)
        ## print g.computeOrdinalCorrelation(equivg)

        ## print coceg.computeDeterminateness()
        ## print coceg.graphDetermination()
        ## print g.computeBipolarCorrelation(coceg)
        ## print g.computeOrdinalCorrelation(coceg)

        ## t1 = RandomWeakTournament(order=30,ndigits=3)
        ## print t1.computeRelationalStructure()
        ## #t.showRelationTable(ndigits=3)
        ## t2 = RandomWeakTournament(order=30,weaknessDegree=0.5)
        ## print t2.computeRelationalStructure()
        ## #t.showRelationTable()
        ## t3 = RandomWeakTournament(order=30,ndigits=1,hasIntegerValuation=True)
        ## #t3.showRelationTable()
        ## print t3.computeRelationalStructure()
        ## #t.showRelationTable()=
        ## print t1.computeAverageValuation()
        ## print t2.computeAverageValuation()
        ## print t3.computeAverageValuation()
        ## print 1,2,t1.computeBipolarCorrelation(t2)
        ## print 1,3,t1.computeBipolarCorrelation(t3)
        ## print 2,3,t2.computeBipolarCorrelation(t3)
        ## tcd1 = CoDualDigraph(t1)
        ## tcd2 = CoDualDigraph(t2)
        ## tcd3 = CoDualDigraph(t3)
        ## print tcd1.computeRelationalStructure()
        ## print tcd2.computeRelationalStructure()
        ## print tcd3.computeRelationalStructure()
        ## print 1,2,tcd1.computeBipolarCorrelation(tcd2)
        ## print 1,3,tcd1.computeBipolarCorrelation(tcd3)
        ## print 2,3,tcd2.computeBipolarCorrelation(tcd3)

        ## e12 = EquivalenceDigraph(t1,t2)
        ## print e12.computeCorrelation()
        ## print e12.computeDeterminateness()
        ## e13 = EquivalenceDigraph(t1,t3)
        ## print e13.computeCorrelation()
        ## print e13.computeDeterminateness()
        ## e23 = EquivalenceDigraph(t2,t3)
        ## print e23.computeCorrelation()
        ## print e23.computeDeterminateness()

        ## g1 = RandomBipolarOutrankingDigraph()
        ## p1 = PolarisedDigraph(g1,level=g1.valuationdomain['med'],StrictCut=True,KeepValues=False)
        ## g2 = RandomBipolarOutrankingDigraph()
        ## p2 = PolarisedDigraph(g2,level=g2.valuationdomain['med'],StrictCut=True,KeepValues=False)
        ## e12 = EquivalenceDigraph(p1,p2)

        ## e12.showRelationTable()
        ## #e12.exportGraphViz()
        ## corr = e12.computeCorrelation()
        ## dterm = e12.computeDeterminateness()
        ## print dterm, corr, corr*dterm

        ## #g1 = RandomValuationDigraph(Normalized=True,hasIntegerValuation=True)
        ## g1 = RandomOutrankingDigraph()
        ## g1.showRelationTable()
        ## #g1.computeValuationStatistics(Comments=True)
        ## dg1 = -g1
        ## dg1.showRelationTable()
        ## cg1 = ~g1
        ## cg1.showRelationTable()
        ## cdg1 = -(~g1)
        ## cdg1.showRelationTable()
        ## cd = CoDualDigraph(g1)
        ## cd.showRelationTable()

        ## g1 = RandomValuationDigraph()
        ## g2 = RandomValuationDigraph()
        ## g3 = RandomValuationDigraph()
        ## c12 = g1.computeBipolarCorrelation(g2)
        ## c13 = g1.computeBipolarCorrelation(g3)
        ## c23 = g2.computeBipolarCorrelation(g3)
        ## d12 = (-c12['correlation'] + Decimal('1'))/Decimal('2')
        ## d13 = (-c13['correlation'] + Decimal('1'))/Decimal('2')
        ## d23 = (-c23['correlation'] + Decimal('1'))/Decimal('2')
        ## print d12,d23,d13


        print('*------------------*')
        print('If you see this line all tests were passed successfully :-)')
        print('Enjoy !')

    print('*************************************')
    print('* R.B. July 2012                    *')
    print('* $Revision: 1.697 $                *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: digraphs.py,v $
#
# Revision 1.696  2013/01/01 14:10:53  bisi
# added computePrudentBestChoiceRecommendation() method to the Digraph class
#
# Revision 1.694  2012/12/24 15:18:21  bisi
# compatibility patch for old (-2008) python performance tableaux
#
# Revision 1.693  2012/09/11 05:12:14  bisi
# debugging rankingByChoosing for failure quadruple
#
# Revision 1.691  2012/09/06 18:28:44  bisi
# Added unary __neg__ (-) and __invert__ (~) operators to the Digraph class methods.
#
# Revision 1.689  2012/08/12 06:30:21  bisi
# Added valuation statistics for digraphs
#
# Revision 1.688  2012/08/11 05:56:39  bisi
# added iqagent.py module
#
# Revision 1.687  2012/08/04 06:27:35  bisi
# Refactored RandomWeakTournament class constructor.
#
# Revision 1.686  2012/07/31 09:25:18  bisi
# Added a constructor ConverseDigraph() for the reciprocal of a digraph
#
# Revision 1.685  2012/07/20 07:06:37  bisi
# minor
#
# Revision 1.684  2012/07/20 06:50:33  bisi
# Added computeCorrelation() to the EquivalenceDigraph class.
#
#############################
