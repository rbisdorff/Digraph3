#!/Usr/bin/env python3
##############################
"""
Python3+ implementation of Digraph3 tools

The module provides various generic methods and tools for handling digraphs.

Copyright (C) 2016-2025 Raymond Bisdorff

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
###################################

__version__ = "$Revision: Python 3.13.2"

#--------- Decimal precision --------------
from decimal import Decimal

#--------- X11 Color list ------------
# https://www.graphviz.org/doc/info/colors.html
_colorPalette0 = [
    'none',
    'black',
    'red',
    'cyan',
    'green',
    'brown',
    'blue',
    'gold',
    'orange',
    'grey',
    'green2',
]    
_colorPalette1 = [
    'none',
    '#EA2027',
      '#006266',
      '#1B1464',
      '#5758BB',
      '#6F1E51',
      '#EE5A24',
      '#009432',
      '#0652DD',
      '#9980FA',
      '#833471',
      '#F79F1F',
      '#A3CB38',
       '#1289A7',
       '#D980FA',
       '#B53471',
       '#FFC312',
       '#C4E538',
       '#12CBC4',
       '#FDA7DF',
       '#ED4C67',
       ]

_colorPalette2 = [
    'black',
      'blue',
      'coral',
      'gold',
      'gray',
      'black',
      'pink',
      'green',
      'orange',
      'skyblue',
      'wheat',
      'salmon']    

colorPalettes = {1: _colorPalette1, 2: _colorPalette2, 3: _colorPalette0}

#---------- general methods -----------------

# splitting list indexes
# def oldqtilingIndexList(indexList,q,Debug=True):
#     """
#     split an index list into q of equal length or, when there is a rest in len(indexList)//q, into q-1 parts of equal length plus a last shorter part.
    
#     """
#     n = len(indexList)
#     if Debug:
#         print(n, indexList, q)

#     nq = n//q
#     if nq * q < n:
#         q -= 1
#         nq = n // q
#         Rest = True
#         if Debug:
#             print('with Rest', n//q, nq*q, n - nq*(q))
#     else:
#         Rest = False
#         if Debug:
#             print('Without Rest', q, nq*q, n - nq*q  )
#     splitIndex = []
#     if Rest == True:
#         for j in range(q):
#             if Debug:
#                 print( nq, j*nq, (j+1)*nq )
#             splitIndex.append( (j*nq, (j+1)*nq) )
#         if Debug:
#             print("Rest", n - ((q)*nq), (q)*nq, n )
#         splitIndex.append( ((q)*nq, n) )
#     else:
#         for j in range(q):
#             if Debug:
#                 print( nq, j*nq, (j+1)*nq )
#             splitIndex.append( (j*nq, (j+1)*nq) )

#     return splitIndex
    
def qtilingIndexList(indexList,q,Debug=False,Comments=False):
    """
    split an index list into q parts of equal length n.
    When there is a rest r < q, the r first parts are put to a length of n+1.

    The method is used for distributing balanced sublists to q multiprocessing threads.

    Usage example::
    
        >>> from digraphsTools import qtilingIndexList
        >>> indexList = [i for i in range(10)]
        >>> indexlist
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> qtilingIndexList(indexList,4,Comments=True)
         cardinalities: [3, 3, 2, 2]
         [(0, 3), (3, 6), (6, 8), (8, 10)]
    
    """
    n = len(indexList)
    if Debug:
        Comments = True
        print(indexList, n, q)

    nq = n//(q)
    if nq * (q) < n:
        r = n - nq*(q)
        Rest = True
        if Debug:
            print('with Rest', nq, nq*(q), r)
    else:
        r = 0
        Rest = False
        if Debug:
            print('Without Rest', q, nq*q, r  )
            
    card = [nq for i in range(q)]
    for j in range(r):
        card[j] += 1
    if Comments:
        print('cardinalities:', card)

    splitIndex = []
    toi = 0
    fromi = 0
    for j in range(q):
        toi += card[j]
        splitIndex.append( (fromi, toi) )
        fromi = toi
    if Debug:
        print('splitIndex:', splitIndex)
    return splitIndex

# sorting list of scored tuples
def scoredTuplesSort(tuples,reverse=False,InSite=True):
    """ 
    Sorting a list of scored tuples only on the scores with *key=itemgetter(0)*:

    >>> L = [(1, 'c'), (2, 'd'), (1, 'a'), (2, 'b'), (3, 'e')]
    >>> scoredTuplesSort(L)
    >>> L
    [(1, 'c'), (1, 'a'), (2, 'd'), (2, 'b'), (3, 'e')]

    When *InSite==False*, returns the sorted tuples list.
    """
    from operator import itemgetter
    from copy import deepcopy
    if InSite:
        tuples.sort(reverse=reverse,key=itemgetter(0))
    else:
        newTuples = deepcopy(tuples)
        newTuples.sort(reverse=reverse,key=itemgetter(0))
        return newTuples
        
# Degfault quantile function from R
def quantile(x,p):
    """
    R type=7 (default) quantile function.

    *x* is a vector of statistical observations of length *n*.

    *p* is an upper-closed cumulative probabilitiy.

    Renders the quantile *q(p)*,
    i.e. the observation such that the probability to be lower or equal is *p*.
    """
    import math
    n = len(x)
    j0 = math.floor((n-1) * p)
    jf = (n-1)*p - j0
    j1 = math.ceil((n-1) * p)
    qp = x[j0] + jf*(x[j1]-x[j0])
    return qp

# from High Performance Python M Gorelick & I Ozswald
# O'Reilly 2014 p.27
from functools import wraps
from time import time
def timefn(fn):
    """
    A decorator for automate run time measurements
    from "High Performance Python" by  M Gorelick & I Ozswald
    O'Reilly 2014 p.27
    """
    @wraps(fn)
    def measure_time(*args,**kwargs):
        t1 = time()
        result = fn(*args,**kwargs)
        t2 = time()
        print("@timefn:" + fn.__name__ + " took " + str(t2-t1) + " sec.")
        return result
    return measure_time

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

# generate all permutations from a weak linear order, i.e. a list of lists
# recursive use of all_perms() on each equivalence class 
def all_partial_perms(px):
    """
    Yields all permutations obtained from a list of lists.

    Usage example:
    
    >>> listOfLists = [[1,2],[3],[4,5]]
    >>> [perm for perm in all_partial_perms(listOfLists)]
     [[1, 2, 3, 4, 5], [1, 2, 3, 5, 4],
      [2, 1, 3, 4, 5], [2, 1, 3, 5, 4]]

    """
    n = len(px)
    if n == 0:
        yield []
    elif n == 1:
        for perm in all_perms(px[0]):
            yield perm
    else:
        for perm in all_perms(px[0]):
            for partperm in all_partial_perms(px[1:]):
                yield perm + partperm
                
#symmetric average fusion operator
def symmetricAverage(Med,L,weights=None,Debug=False):
    """
    [Weighted] symmetric average data fusion for bipolar outranking characteristics
    computation: Med is the valuation domain median and L is a list of
    r-valued statement characteristics.

    With only **positive** or only **negative** [and median] characteristic values,
    the *symmetricAverage* operator  renders the [weighted] average of the characteristics values.
    
    The mixture of **both positive and negative** characteristic values results in
    an **indeterminate** value.

    Likewise to a mean, the *symmetric* operator is not associative.
    We therefore first assemble separately all positive, negative and null values 
    and operate *ofusion* on the three assembled values.
    
    """
    terms = list(L)
    nt = len(terms)
    termsPlus = Decimal('0')
    np = 0
    termsMinus = Decimal('0')
    nm = 0
##    termsNuls = []
    if weights is None:
        weights = [1 for i in range(nt)]
    sumWeights = 0
    for i in range(nt):
        sumWeights += weights[i]
        if terms[i] > Med:
            termsPlus += terms[i]*Decimal(str(weights[i]))
            np += weights[i]
        elif terms[i] < Med:
            termsMinus += terms[i]*Decimal(str(weights[i]))
            nm += weights[i]
##        else:
##            termsNuls.append(terms[i])
##    if Debug:
##        print('terms', terms)
##        print('termsPlus',termsPlus)
##        print('termsMinus', termsMinus)
##        print('termsNuls', termsNuls)
    if np > 0 and nm == 0:
        return termsPlus/Decimal(str(sumWeights))
    elif nm > 0 and np == 0:
        return termsMinus/Decimal(str(sumWeights))
    else:
        return Med

#epistemic or symmetric disjunction operator
def omax(Med,L, Debug=False):
    """
    Epistemic **disjunction** for bipolar outranking characteristics
    computation: Med is the valuation domain median and L is a list of
    r-valued statement characteristics.

    With **positive** arguments, omax operates a **max**,
    with **negative** arguments, a **min**.

    The mixture of **both positive and negative** arguments results in
    an **indeterminate** value.

    Likewise to a mean, the *omax* operator is not associative.
    We therefore first assemble all positive and negative terms
    and operate omax on the two assembled arguments.
    
    """
    terms = list(L)
    termsPlus = []
    termsMinus = []
    for i in range(len(terms)):
        if terms[i] > Med:
            termsPlus.append(terms[i])
        elif terms[i] < Med:
            termsMinus.append(terms[i])
##    if Debug:
##        print('terms', terms)
##        print('termsPlus',termsPlus)
##        print('termsMinus', termsMinus)
    np = len(termsPlus)
    nm = len(termsMinus)
    if np > 0 and nm == 0:
        return max(termsPlus)
    elif nm > 0 and np == 0:
        return min(termsMinus)
    else:
        return Med

# epistemic or symmetric conjunction operator
def omin(Med,L, Debug=False):
    """
    Epistemic **conjunction** of a list L of bipolar outranking characteristics.
    Med is the given valuation domain median.

    With **positive or zero** arguments, omin operates a **min**,
    with **negative or zero** arguments, a **max**.

    The mixture of both **positive and negative** arguments results
    in an **indeterminate** value.

    Likewise to a mean, the *omin* operator is not associative.
    We therefore first assemble separately all positive and negative terms
    and operate *omin* on the two assembled arguments. 

    """
    terms = list(L)
    termsPlus = []
    termsMinus = []
    termsNull = []
    for i in range(len(terms)):
        if terms[i] > Med:
            termsPlus.append(terms[i])
        elif terms[i] < Med:
            termsMinus.append(terms[i])
        else:
            termsNull.append(terms[i])
##    if Debug:
##        print('terms', terms)
##        print('termsPlus',termsPlus)
##        print('termsMinus', termsMinus)
    np = len(termsPlus)
    nm = len(termsMinus)
    nn = len(termsNull)
    if np > 0:
        if nm > 0:
            return Med
        elif nn > 0:
            return Med
        else:
            return min(termsPlus)
    elif nm > 0:
        if nn > 0:
            return Med
        else:
            return max(termsMinus)
    else:
        return Med

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

# generate the Gray code of length n by middle reflection
# RB Feb 2017
def grayCode(n):
    # generate a gray code step
    def _grayReflection(G0):
        G = []
        for x in G0:
            gx = '0' + x
            G.append(gx)
        for x in reversed(G0):
            gx = '1' + x
            G.append(gx)
        return G
    # generate recursively the list of n codes
    G = ['']
    for i in range(n):
        G = _grayReflection(G)
    return G

#@timefn
def generateGrayCode(n):
    """
    Knuth ACP (4) 7.2.1.1. p.6
    Algorithm G
    """
    a = [0 for j in range(n)]
    ainf = 0
    n2 = 2**n 
    for i in range(n2):
        #print(i, a)
        a1 = a.copy()
        yield a1
        ainf = 1 - ainf
        if ainf == 1:
            j = 0
        else:
            for j in range(1,n):
                if a[j-1] == 1:
                    break
            #print(j)
        if j < n:
            a[j] = 1 - a[j]
        else:
            break

#@timefn
def generateLooplessGrayCode(n):
    """
    Knuth ACP (4) 7.2.1.1. p.7
    Algorithm L
    """
    a = [0 for j in range(n)]
    f = [j for j in range(n+1)]
    n2 = 2**n 
    for i in range(n2):
        a1 = a.copy()
        yield a1
        j = f[0]
        f[0] = 0
        if j == n:
            break
        else:
            f[j] = f[j+1]
            f[j+1] = j+1
        a[j] = 1 - a[j]

def generateBipolarGrayCode(n):
    """
    Bipolar version of generateGrayCode.
    X is a partially determined -1 vector.
    """
    a = [-1 for j in range(n)]
    ainf = -1
    n2 = 2**n 
    for i in range(n2):
        a1 = a.copy()
        yield a1
        ainf = -ainf
        if ainf == 1:
            j = 0
        else:
            for j in range(1,n):
                if a[j-1] == 1:
                    break
             #print(j)
        if j < n:
            a[j] = -a[j]
        else:
            break

# generate random samples of DNA sequences
def generateRandomSequence(length=10,alphabet=['A','C','G','T']):
    """
    A generator for random samples of sequences
    given a certain alphabet (DNA by default).
    """
    from random import sample
    na = len(alphabet)
    counts=[length for i in range(na)]
    seq = sample(alphabet,counts=counts,k=length)
    return seq

# compute DNA sequences alignment with the Needleman-Wunsch algorithm
def computeSequenceAlignment(seqA,seqB,match=-1,mispen=1,
                             gappen=1,skwpen=1,
                             Comments=True,Debug=False):
    """
    Numerical Recipes 3rd Ed., Press, Teukolsky, Vetterling, Flannery
    Cambridge Unievrsity Press
    Chap 10.13.2 Example DNA Sequence Alignment
    Digraph3 RB June 2023
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

    *match* : match bonus (negative integer)

    *mispen*, *gappen*, *skwpen* : mismatch, resp. gap,
    resp skew penalty (positive integer)

    Return {'aout': aout, 'bout':bout, 'summary': summary,
    'sumCosts': sumCosts}

    Example session:
    
    >>> from digraphsTools import generateRandomSequence,computeSequenceAlignment
    >>> seqA = generateRandomSequence(10,alphabet=['A','C','G','T'])
    >>> seqB = generateRandomSequence(10,alphabet=['A','C','G','T'])
    >>> alignement = computeSequenceAlignment(seqA,seqB)
     aout:    ['C', 'C', 'A', 'T', 'G', 'A', ' ', 'G', 'C', 'G', 'A']
     bout:    [' ', 'A', 'A', 'T', 'A', 'A', 'T', 'T', 'C', 'C', 'T']
     summary: [' ', '!', '=', '=', '!', '=', ' ', '!', '=', '!', '!']
     statistics: {'match': 4, 'mismatch': 5, 'gapA': 1, 'gapB': 1}
     sum of costs 3

    """
    na = len(seqA)
    nb = len(seqB)
    if Debug:
        Comments=True

    # initialise the cost alignment tableau
    cost = {}
    statistics = {'match': 0,'mismatch': 0, 'gapA': 0, 'gapB': 0}
    for i in range(na):
        cost[i] = {}
        for j in range(nb):
            cost[i][j] = 0
    # fill in first row and column
    for i in range(1,na):
        cost[i][0] = cost[i-1][0] + skwpen
    for j in range(1,nb):
        cost[0][j] = cost[0][j-1] + skwpen
    # fill the cost table
    for i in range(1,na):
        for j in range(1,nb):
            if j == nb:
                dn = cost[i-1][j] + skwpen
            else:
                dn = cost[i-1][j] + gappen
            if i == na:
                rt = cost[i][j-1] + skwpen
            else:
                rt = cost[i][j-1] + gappen
            if seqA[i-1] == seqB[j-1]:
                dg = cost[i-1][j-1] + match
            else:
                dg = cost[i-1][j-1] + mispen
            cost[i][j] = min([dn,rt,dg])
    if Debug:
        showCostTable(seqA,seqB,cost)
        
    # backtracking
    i = na-1
    j = nb-1
    aout = [seqA[i]]
    bout = [seqB[j]]
    if seqA[i] == seqB[j]:
        summary = ['=']
        statistics['match'] += 1
        
    else:
        summary = ['!']
        statistics['mismatch'] += 1
    while (i > 0) and (j > 0):
        if (i > 0) and (j == nb):
            dn = cost[i-1][j] + skwpen
        else:
            dn = cost[i-1][j] + gappen
        if (j > 1) and (i == na):
            rt = cost[i][j-1] + skwpen
        else:
            rt = cost[i][j-1] + gappen
        if seqA[i-1] == seqB[j-1]:
            dg = cost[i-1][j-1] + match
        else:
            dg = cost[i-1][j-1] + mispen
        if dg <= min(dn,rt):
            i -= 1
            j -= 1
            aout.append(seqA[i])
            bout.append(seqB[j])
            if seqA[i] == seqB[j]:
                summary.append('=')
                if Debug:
                    print('match',i,j,cost[i][j])
                statistics['match'] += 1

            else:
                summary.append('!')
                if Debug:
                    print('inequality',i,j,cost[i][j])
                statistics['mismatch'] += 1

            #print(aout,bout,summary)
        elif dn < rt:
            i -= 1
            aout.append(seqA[i])
            bout.append(' ')
            summary.append(' ')
            if Debug:
                print('gap in seqB',i,j,cost[i][j])
            statistics['gapB'] += 1

        else:
            j -= 1       
            aout.append(' ')
            bout.append(seqB[j])
            summary.append(' ')
            if Debug:
                print('gap in seqA',i,j,cost[i][j])
            statistics['gapA'] += 1
    while i > 0:
        aout.append(seqA[i])
        bout.append(' ')
        summary.append(' ')
        statistics['gapB'] += 1
        i -= 1
    while j > 0:
        aout.append(' ')
        bout.append(seqB[j])
        summary.append(' ')
        statistics['gapA'] += 1
        j -= 1
         
    aout.reverse()
    bout.reverse()
    summary.reverse()
    if Comments:
        print('aout:\t', aout)
        print('bout:\t', bout)
    sumCosts = 0
    for i in range(len(summary)):
        if summary[i] == '=':
            sumCosts += match
        elif summary[i] == '!':
            sumCosts += mispen
        else: # summary[i] == ' ':
            sumCosts += gappen
    if Comments:
        print('summary:', summary)
        print(statistics)
        print('sum of costs', sumCosts)

    return {'aout': aout, 'bout':bout,
            'summary': summary, 'sumCosts': sumCosts}

# KMP pattern matching algorithm

def kmpMatch(haystack,needle,Comments=True,Debug=False):
    """
    Knuth Morris Pratt string matching algorithm
    https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm

    Returns a list of potential starting indexes of needle ocurrencies in the haystack
    
    >>> from digraphsTools import kmpMatch
    >>> kmpMatch('0011001011','0101',Comments=True)
     haystack: 00110010110011001011
     needle: 0101
     needle starting index positions in haystack: [5, 15]
    """
    # constructing the KMP failure table
    def _failTable(pattern,Debug=False):
        np = len(pattern)
        #T = [0 for i in range(np)]
        T = []
        if Debug:
            print(np,T)
        pos = 1
        cnd = 0
        T.append(-1)
        while pos < np:
            if pattern[pos] == pattern[cnd]: 
                #T[pos] = T[cnd]
                T.append(T[cnd])
                if Debug:
                    print(1,pos,cnd,T)
            else:
                T.append(cnd)
                while cnd >= 0 and pattern[pos] != pattern[cnd]:
                    cnd = T[cnd]
                if Debug:
                    print(2,pos,cnd,T)    
            pos += 1
            cnd += 1
            if Debug:
                print(3,pos,cnd,T)
        T.append(cnd)
        if Debug:
            print('fail table:', T)
        return T

    if Debug:
        Comments=True
    if Comments:
        print('needle:',needle)
        print('haystack:', haystack)

    fT = _failTable(needle,Debug=Debug)
    if Debug:
        print('fail table:', fT)

    P = []
    j = 0 # position in haystack
    k = 0 # position in needle
    nP = 0
    nn = len(needle)
    nh = len(haystack)
             
    while j < nh:
        if Debug:
            print(j, k)

        if haystack[j] == needle[k]:
            j += 1
            k += 1
            if k == nn:
                P.append(j-k)
                nP += 1
                k = fT[k]
        else:
            k = fT[k]
            if k < 0:
                j += 1
                k += 1
    if Comments:
        print('needle starting index positions in haystack:',P)
    return P
      
# transforms a ranking into a list of singletons
def ranking2preorder(R):
    """
    Transforms a ranking (list from best to worst) into
    a preorder (a list of lists from worst to best)

    Usage:

    >>> ranking = [1,2,3,4]
    >>> ranking2preorder(ranking)
     [[4],[3],[2],[1]]
    
    """
    preorder = [[x] for x in reversed(R)]
    return preorder

# flattens a list of lists into a flat list
import itertools as IT
from collections import abc

def flatten(iterable, ltypes=abc.Iterable):
    """
    Flattens a list of lists into a flat list.

    Main usage:
    
    >>> listOfLists = [[1,2],[3],[4]]
    >>> [x for x in flatten(listOfLists)]
    [1, 2, 3, 4]
    
    """
    
    remainder = iter(iterable)
    while True:
        try:
            first = next(remainder)
            if isinstance(first, ltypes) and not isinstance(first, str):
                remainder = IT.chain(first, remainder)
            else:
                yield first
        except:
            break

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint of an object and all of its contents.

    Automatically finds the contents of the following containers and
    their subclasses:  tuple, list, deque, dict, set, frozenset, Digraph and BigDigraph.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    See http://code.activestate.com/recipes/577504/  

    """
    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    from digraphs import Digraph
    from perfTabs import PerformanceTableau
    from sparseOutrankingDigraphs import SparseOutrankingDigraph
    
    try:
        from reprlib import repr
    except ImportError:
        pass

    # built-in containers and their subclasses
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                    }

    # Digraph3 objects 
    object_handler = lambda d: chain.from_iterable(d.__dict__.items())    
    handlers = {SparseOutrankingDigraph: object_handler,
                Digraph: object_handler,
                PerformanceTableau : object_handler,
                }
    
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

    

###############################
if __name__ == '__main__':
    ######  scratch pad for testing the module components

    print("""
    ****************************************************
    * Digraph33 digraphsTools module                   *
    * Copyright (C) 2010-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    # indexList = range(100000)
    # q = 12
    # splitIndex = oldqtilingIndexList(indexList,q,Debug=True)
    # print(splitIndex)
    # for i in range(len(splitIndex)):
    #     print('group',i+1, splitIndex[i])
    #     #for j in range(splitIndex[i][0],splitIndex[i][1]):
    #     #    print(j)
    indexList = range(100000)
    q = 12
    splitIndex = qtilingIndexList(indexList,q,Comments=True)
    print(splitIndex)
    for i in range(len(splitIndex)):
        print('group',i+1, splitIndex[i])
        #for j in range(splitIndex[i][0],splitIndex[i][1]):
        #    print(j)


##    seqA = generateRandomSequence(10)
##    seqB = generateRandomSequence(10)
##    seqA = ['T','A','C','G','G','G','C','C','C','G','C','T','A','C']
##    seqB = ['T','A','G','C','C','C','T','A','T','C','G','G','T','C','A']
##    alignnment = computeSequenceAlignment(seqA,seqB)
##    from digraphsTools import kmpMatch
##    haystack = '00110010110011001011'
##    needle = '0101'
##    kmpMatch(haystack,needle,Comments=True)


##    plist = [[1,2,3],[4],[5,6]]
##    perms = []
##    for p in all_partial_perms(plist):
##        perms.append(p)
##    print(perms)
 
    # l = [(1,'a'),(2,'b'),(1,'c'),(2,'d'),(3,'e')]
    # print(l)
    # scoredTuplesSort(l)
    # print(l)
    # scoredTuplesSort(l,reverse=True)
    # print(l)
##    from randomDigraphs import *
##    g1 = RandomValuationDigraph(order=5,seed=1)
##    g2 = RandomValuationDigraph(order=5,seed=2)
##    g3 = RandomValuationDigraph(order=5,seed=3)
##    from digraphs import FusionLDigraph
##    #fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-average')
##    g1.showRelationTable()
##    g2.showRelationTable()
##    g3.showRelationTable()
##    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-max')
##    fga.showRelationTable()
##    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-min')
##    fga.showRelationTable()
##    fga = FusionLDigraph([g1,g2,g3],weights=None,operator='o-average')
##    fga.showRelationTable()
##    fga = FusionLDigraph([g1,g2,g3],weights=[1,2,3],operator='o-average')
##    fga.showRelationTable()

             
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
#####################################

