#!/Usr/bin/env python3
"""
Python3+ implementation of Digraph3 tools

Copyright (C) 2016-2020 Raymond Bisdorff

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
__version__ = "Branch: 3.7 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

#from digraphs import *
#from perfTabs import *
#from randomPerfTabs import *

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

    Likewise to a mean, the *omax* operator is not associative. We therefore first assemble all positive, negative and null terms
    and operate omax on the three assembled arguments.
    
    """
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
##    if Debug:
##        print('terms', terms)
##        print('termsPlus',termsPlus)
##        print('termsMinus', termsMinus)
##        print('termsNuls', termsNuls)
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

    With **positive** arguments, omin operates a **min**,
    with **negative** arguments, a **max**.

    The mixture of both **positive and negative** arguments results
    in an **indeterminate** value.

    Likewise to a mean, the *omin* operator is not associative.
    We therefore first assemble all positive, negative and null terms
    and operate *omin* on the three assembled arguments. 

    """
    terms = list(L)
    termsPlus = []
    termsMinus = []
    termsNuls = []
    for i in range(len(terms)):
        if terms[i] >= Med:
            termsPlus.append(terms[i])
        elif terms[i] <= Med:
            termsMinus.append(terms[i])
        else:
            termsNuls.append(terms[i])
##    if Debug:
##        print('terms', terms)
##        print('termsPlus',termsPlus)
##        print('termsMinus', termsMinus)
##        print('termsNuls', termsNuls)
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
     
        
# transforms a ranking (list from best to worst) into
# a preorder ( a list of list from worst to best)
def ranking2preorder(R):
    preorder = [[x] for x in reversed(R)]
#    for x in R:
#        preorder.append([x])
#    preorder.reverse()
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
    [1,2,3,4]
    
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

    print(grayCode(4))
##    #print(list(generateBipolarGrayCode(4)))
##    print(list(generateGrayCode(4)))
##    print(list(generateLooplessGrayCode(4)))
##
##    X = list(range(4))
##    n = len(X)
##    for g in generateGrayCode(n):
##        Xg = set()
##        for i in range(n):
##            if g[i] == 1:
##                Xg.add(X[i])
##        print(Xg)
##        
##    from outrankingDigraphs import *
##    t = RandomPerformanceTableau()
##    g = BipolarOutrankingDigraph(t)
##    print(total_size(g))
##
##    from sparseOutrankingDigraphs import *
##    pr = PreRankedOutrankingDigraph(t)
##    print(total_size(pr))

             

