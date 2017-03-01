#!/Usr/bin/env python3
# Python3+ implementation of Digraph3 tools
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

__version__ = "Branch: 3.5 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

#from digraphs import *
#from perfTabs import *
#from randomPerfTabs import *

#--------- Decimal precision --------------
from decimal import Decimal

#---------- general methods -----------------
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
# epistemic or symmetric disjunction operator
def omax(Med,L, Debug=False):
    """
    epistemic disjunction for bipolar outranking characteristics
    computation: Med is the valuation domain median and L is a list of
    r-valued statement characteristics. 
    """
    #Med = self.valuationdomain['med']
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
    epistemic conjunction of a list L of bipolar outranking characteristics.
    Med is the given valuation domain median.
    """
    #Med = self.valuationdomain['med']
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
import collections

def flatten(iterable, ltypes=collections.Iterable):
    """
    Flattens a list of lists into a flat list.

    Main usage:
    
    >>> listOfLists = [[1,2],[3],[4]]
    >>> [x for x in flatten(listOfLists)]
    [1,2,3,4]
    
    """
    
    remainder = iter(iterable)
    while True:
        first = next(remainder)
        if isinstance(first, ltypes) and not isinstance(first, str):
            remainder = IT.chain(first, remainder)
        else:
            yield first

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

### see arithmetics module
##class Arithmetics:
##    """
##
##    Tools gathered from the internet for doing arithmetics.
##
##    """
##    def primesbelow(N):
##        """
##
##        http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
##        Input N>=6, Returns a list of primes, 2 <= p < N
##
##        """
##        correction = N % 6 > 1
##        N = {0:N, 1:N-1, 2:N+4, 3:N+3, 4:N+2, 5:N+1}[N%6]
##        sieve = [True] * (N // 3)
##        sieve[0] = False
##        for i in range(int(N ** .5) // 3 + 1):
##            if sieve[i]:
##                k = (3 * i + 1) | 1
##                sieve[k*k // 3::2*k] = [False] * ((N//6 - (k*k)//6 - 1)//k + 1)
##                sieve[(k*k + 4*k - 2*k*(i%2)) // 3::2*k] = [False] * ((N // 6 - (k*k + 4*k - 2*k*(i%2))//6 - 1) // k + 1)
##        return [2, 3] + [(3 * i + 1) | 1 for i in range(1, N//3 - correction) if sieve[i]]
##
##    _smallprimeset = set(primesbelow(100000))
##    _smallprimesetSize = 100000
##    def isprime(n, precision=7):
##        """
##
##        http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time
##
##        """
##        if n == 1 or n % 2 == 0:
##            return False
##        elif n < 1:
##            raise ValueError("Out of bounds, first argument must be > 0")
##        elif n < Arithmetics._smallprimesetSize:
##            return n in Arithmetics._smallprimeset
##
##
##        d = n - 1
##        s = 0
##        while d % 2 == 0:
##            d //= 2
##            s += 1
##
##        for repeat in range(precision):
##            a = random.randrange(2, n - 2)
##            x = pow(a, d, n)
##
##            if x == 1 or x == n - 1: continue
##
##            for r in range(s - 1):
##                x = pow(x, 2, n)
##                if x == 1: return False
##                if x == n - 1: break
##            else: return False
##
##        return True
##
##    def pollard_brent(n):
##        """
##
##        https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/
##
##        """
##        if n % 2 == 0: return 2
##        if n % 3 == 0: return 3
##
##        y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
##        g, r, q = 1, 1, 1
##        while g == 1:
##            x = y
##            for i in range(r):
##                y = (pow(y, 2, n) + c) % n
##
##            k = 0
##            while k < r and g==1:
##                ys = y
##                for i in range(min(m, r-k)):
##                    y = (pow(y, 2, n) + c) % n
##                    q = q * abs(x-y) % n
##                g = gcd(q, n)
##                k += m
##            r *= 2
##        if g == n:
##            while True:
##                ys = (pow(ys, 2, n) + c) % n
##                g = gcd(abs(x - ys), n)
##                if g > 1:
##                    break
##
##        return g
##
##    _smallprimes = primesbelow(1000) # might seem low, but 1000*1000 = 1000000, so this will fully factor every composite < 1000000
##    def primefactors(n, sort=False):
##        factors = []
##
##        limit = int(n ** .5) + 1
##        for checker in Arithmetics._smallprimes:
##            if checker > limit: break
##            while n % checker == 0:
##                factors.append(checker)
##                n //= checker
##                limit = int(n ** .5) + 1
##                if checker > limit: break
##
##        if n < 2: return factors
##
##        while n > 1:
##            if Arithmetics.isprime(n):
##                factors.append(n)
##                break
##            factor = Arithmetics.pollard_brent(n) # trial division did not fully factor, switch to pollard-brent
##            factors.extend(primefactors(factor)) # recurse to factor the not necessarily prime factor returned by pollard-brent
##            n //= factor
##
##        if sort: factors.sort()
##
##        return factors
##
##    def factorization(n):
##        factors = {}
##        for p1 in Arithmetics.primefactors(n):
##            try:
##                factors[p1] += 1
##            except KeyError:
##                factors[p1] = 1
##        return factors
##
##    _totients = {}
##    def totient(n):
##        """
##        Implements the totient function rendering
##        Euler's number of coprime elements a in Zn.
##        """
##        if n == 0: return 1
##
##        try: return Arithmetics._totients[n]
##        except KeyError: pass
##
##        tot = 1
##        for p, exp in Arithmetics.factorization(n).items():
##            tot *= (p - 1)  *  p ** (exp - 1)
##
##        Arithmetics._totients[n] = tot
##        return tot
##
##    def gcd(a, b):
##        """
##        Renders the greatest common divisor of a and b.
##        """
##        if a == b: return a
##        while b > 0: a, b = b, a % b
##        return a
##
##    def lcm(a, b):
##        """
##        Renders the least common multiple of a and b.
##        """
##        return abs(a * b) // Arithmetics.gcd(a, b)
##
##    def bezout(a,b):
##        """
##        Renders d = gcd(a,b) and the
##        Bezout coefficient x, y such that
##        d = ax + by.
##        """
##        
##        x,y,u,v = 1,0,0,1
##        print(a,0,x,y)
##        print(a,b,u,v)
##        while b != 0:
##            r = a % b
##            q = (a - r)/b
##            x,y, u,v = u,v, x-(q*u),y-(q*v)
##            print(a,b,q,r,u,v)
##            a,b = b,r
##        return a,x,y
##
##    def solPartEqnDioph(a,b,c):
##        """
##        renders a particular integer solution of the Diophantian equation
##        ax + by = c.
##        """
##
##        d = Arithmetics.gcd(a,b)
##        if c % d != 0:
##            return None,None,None,None # pas de solution
##        
##        A,B,C = a/d, b/d, c/d
##
##        D,x,y = Arithmetics.bezout(A,B)
##
##        return C*x, C*y , A, B # solution particulière plus coefficients
##
##    def zn_squareroots(n,Comments=False):
##        """
##        Renders the quadratic residues of Zn as a dictionary.
##        """
##        sqrt = {}
##        units = Arithmetics.zn_units(n)
##        if Comments:
##            print(units)
##        for i in units:
##            sqi =  i*i % n
##            if Comments:
##                print(i,i*i,sqi)
##            try:
##                sqrt[sqi].append(i)
##            except:
##                sqrt[sqi] = [i]
##        return sqrt
##
##    def zn_units(n,Comments=False):
##        """
##        Renders the set of units of Zn.
##        """
##        units = set()
##        for i in range(1,n):
##            for j in range(1,n):
##                if (i * j) % n == 1:
##                    units.add(i)
##                    units.add(j)
##        if Comments:
##            print(units)
##        return units
    

###############################
if __name__ == '__main__':
    ######  scratch pad for testing the module components
   
    print(grayCode(4))
    #print(list(generateBipolarGrayCode(4)))
    print(list(generateGrayCode(4)))
    print(list(generateLooplessGrayCode(4)))
    
    from outrankingDigraphs import *
    t = RandomPerformanceTableau()
    g = BipolarOutrankingDigraph(t)
    print(total_size(g))

    from sparseOutrankingDigraphs import *
    pr = PreRankedOutrankingDigraph(t)
    print(total_size(pr))

##  see arithmetics module
##    a = 17
##    b = 1
##    m = 19
##    
##    print( ( "Congruence: %dx =  %d (mod %d)" % (a,b,m) ) )  # \equiv = \u2262
##
##    x,y,A,B = Arithmetics.solPartEqnDioph(a,m,b)
##
##    if x == None:
##        print("Pas de solution")
##    else:
##        print("Solution générale: x = %d + %dn" % (x,B))
##        h = Arithmetics.gcd(a,m)
##        y = m / h
##        print('m,h,y',m,h,y)
##        print("Il y a %d solution(s) particulière(s):" % (h))
##        for i in range(h):
##            print("x_%d = %d + %d*%d (mod %d) = %d" % (i+1,x,i,y,m,(x + (i*y))%m ))
             

