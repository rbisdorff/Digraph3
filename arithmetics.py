#!/Usr/bin/env python3
"""
Python3+ implementation of arithmetics tools
Copyright (C) 2016-2020  Raymond Bisdorff
Tools gathered for doing arithmetics.
Mainly inspired from G.A. Jones & J.M. Jones
Elementary Number Theroy
Springer Verlag London 1998

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################
from arithmetics import *
from digraphs import Digraph
from decimal import Decimal
from collections import OrderedDict

__version__ = "Branch: 3.5 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

"""


"""
class QuadraticResiduesDigraph(Digraph):
    """
    The **Legendre** symbol *(a/p)* of any pair of non null integers *a* and *p* is:

         - **0** if *a* = 0 (mod p);
         - **1** if *a* is a quadratic residue in *Zp*, ie *a* in *Qp*;
         - **-1** if *a* is a non quadratic residue unit in *Zp*, ie *a* in *Up* - *Qp*.

    The Legendre symbol hence defines a bipolar valuation on pairs 
    of non null integers. The **reciprocity theorem** of the Legendre symbol 
    states that, for *p* being an odd prime, *(a/p)* = *(p/a)*,
    apart from those pairs *(a/p)*, where *a* = *p* = 3 (mod 4). In this case, *(a/p)* = -*(p/a)*.

    We may graphically illustrate the reciprocity theorem as follows::
    
       >>> from arithmetics import *
       >>> leg = QuadraticResiduesDigraph(primesBelow(20,Odd=True))
       >>> from digraphs import AsymmetricPartialDigraph
       >>> aleg = AsymmetricPartialDigraph(leg)
       >>> aleg.exportGraphViz('legendreAsym')

    .. image:: legendreAsym.png
       :alt: Quadratic residues digraph asymmetric part
       :width: 300 px
       :align: center

    """
    def __init__(self,integers=[3,5,7,11,13,17,19]):
        """
        By default we consider only primes, but the Legendre symbol
        works for any integer sequence not containing 0.

        """
        import sys,array,copy
        self.name = 'legendreDigraph'
        self.order = len(integers)
        actionsList = integers
        actions = OrderedDict()
        for x in actionsList:
            if x == 0:
                print('Only positive integers are allowed!')
                return
            actions[x] = {'name':str(x),'shortName':str(x)}
        self.actions = actions
        Max = Decimal('1')
        Min = Decimal('-1')
        Med = Decimal('0')
        self.valuationdomain = {'min':Min,'med':Med,'max':Max}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        for p in actions:
            Units = set(zn_units(p))
            Sqrts = set(zn_squareroots(p))
            for a in actions:
                q,r = divmod(a,p)
                if r == 0:
                    relation[p][a] = Med
                else:
                    if r in Sqrts:
                        relation[p][a] = Max
                    elif r in Units-Sqrts:
                        relation[p][a] = Min
        self.relation = relation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    
def primesBelow(N,Odd=False):
    """

    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    Input N>=6, Returns a list of primes, 2 <= p < N

    """
    correction = N % 6 > 1
    N = {0:N, 1:N-1, 2:N+4, 3:N+3, 4:N+2, 5:N+1}[N%6]
    sieve = [True] * (N // 3)
    sieve[0] = False
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k*k // 3::2*k] = [False] * ((N//6 - (k*k)//6 - 1)//k + 1)
            sieve[(k*k + 4*k - 2*k*(i%2)) // 3::2*k] = [False] * ((N // 6 - (k*k + 4*k - 2*k*(i%2))//6 - 1) // k + 1)
    primes = [2, 3] + [(3 * i + 1) | 1 for i in range(1, N//3 - correction) if sieve[i]]
    if Odd:
        primes.remove(2)
    return primes

_smallprimeset = set(primesBelow(100000))
_smallprimesetSize = 100000
def isprime(n, precision=7):
    """

    http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time

    """
    if n == 1 or n % 2 == 0:
        return False
    elif n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n < _smallprimesetSize:
        return n in _smallprimeset


    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for repeat in range(precision):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1: continue

        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == 1: return False
            if x == n - 1: break
        else: return False

    return True

def pollard_brent(n):
    """

    https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/

    """
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    import random
    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break

    return g

_smallprimes = primesBelow(1000) # might seem low, but 1000*1000 = 1000000, so this will fully factor every composite < 1000000
def primeFactors(n, sort=True):
    factors = []

    limit = int(n ** .5) + 1
    for checker in _smallprimes:
        if checker > limit: break
        while n % checker == 0:
            factors.append(checker)
            n //= checker
            limit = int(n ** .5) + 1
            if checker > limit: break

    if n < 2: return factors

    while n > 1:
        if isprime(n):
            factors.append(n)
            break
        factor = pollard_brent(n) # trial division did not fully factor, switch to pollard-brent
        factors.extend(primeFactors(factor)) # recurse to factor the not necessarily prime factor returned by pollard-brent
        n //= factor

    if sort: factors.sort()

    return factors

def factorization(n):
    factors = OrderedDict()
    for p1 in primeFactors(n):
        try:
            factors[p1] += 1
        except KeyError:
            factors[p1] = 1
    return factors

def moebius_mu(n):
    """
    Implements the Moebius mu function on N based on n's prime factorization:
    n = p1^e1 * ... * pk^ek with each ei >= 1 for i = 1, ..., k.  

    mu = 0 if ei > 1 for some i = 1, ... k else mu = (-1)^k.
    
    """
    if n < 1:
        print('n must be a positive integer!')
        return
    factors = factorization(n)
    k = len(factors)
    SquareFree = True
    for p in factors:
        if factors[p] > 1:
            SquareFree = False
            break
    if SquareFree:
        return pow(-1,k)
    else:
        return 0

def divisors(n,Sorted=True):
    """
    Renders the list of divisors of integer n.
    """
    if n == 0:
        return
    Dn = [n]
    for i in range(2,n):
        q,r = divmod(n,i)
        if r == 0:
            Dn.append(q)
    Dn.append(1)
    if Sorted:
        Dn.reverse()       
    return Dn

def divisorsFunction(k,n):
    """
    generic divisor function:

       - the number of divisors of *n* is divisorsFunction(0,n)
       - the sum of the divisors of *n* is divisorsFunction(1,n)
    """
    tot = 0
    for d in divisors(n):
        tot += pow(d,k)
    return tot

_totients = {}
def totient(n):
    """
    Implements the totient function rendering
    Euler's number of coprime elements a in Zn.
    """
    if n == 0: return 1

    try: return _totients[n]
    except KeyError: pass

    tot = 1
    for p, exp in factorization(n).items():
        tot *= (p - 1)  *  p ** (exp - 1)

    _totients[n] = tot
    return tot

def continuedFraction(p, q):
    """
    Renders the continued fraction [a_0,a_1,a_2,...,a_n]
    of the ratio of two integers p and q, q > 0 and where a0 = p//q.
    """
    if q < 0:
        return None
    res = [p//q]
    #print(p,q,res)
    while q > 0: 
        q0 = q
        p, q = q, p % q
        if q > 1:
            res.append(p//q)
        elif q == 1 :
            res.append(1)
        elif q0 == 1:
            res.append(1)
        #print(p,q0,q,res)
    return res

def evalContinuedFraction(cf):
    """
    Backwise recursive evaluation: ev_i-1 + 1/ev_i, for i = n,..,1
    of the continued fraction cf = [a_0,a_1,a_2,...,a_n] and 
    where a_0 corresponds to its integer part.
    """
    from decimal import Decimal
    n = len(cf) - 1
    res = Decimal(str(cf[n]))
    #print(n,res)
    for i in range(n-1,0,-1):
        res = Decimal(str(cf[i])) + Decimal('1')/res
        #print(i,res)
    res = Decimal(str(cf[0])) + Decimal('1')/res
    return res
        
def gcd(a, b):
    """
    Renders the greatest common divisor of a and b.
    """
    if a == b: return a
    while b > 0: a, b = b, a % b
    return a

def lcm(a, b):
    """
    Renders the least common multiple of a and b.
    """
    return abs(a * b) // gcd(a, b)

def bezout(a,b):
    """
    Renders d = gcd(a,b) and the
    Bezout coefficient x, y such that
    d = ax + by.
    """
    
    x,y,u,v = 1,0,0,1
    print(a,0,x,y)
    print(a,b,u,v)
    while b != 0:
        r = a % b
        q = (a - r)/b
        x,y, u,v = u,v, x-(q*u),y-(q*v)
        print(a,b,q,r,u,v)
        a,b = b,r
    return a,x,y

def solPartEqnDioph(a,b,c):
    """
    renders a particular integer solution of the Diophantian equation
    ax + by = c.
    """

    d = gcd(a,b)
    if c % d != 0:
        return None,None,None,None # pas de solution
    
    A,B,C = a/d, b/d, c/d

    D,x,y = bezout(A,B)

    return C*x, C*y , A, B # solution particulière plus coefficients

def zn_squareroots(n,Comments=False):
    """
    Renders the quadratic residues of Zn as a dictionary.
    """
    sqrt = {}
    units = zn_units(n)
    if Comments:
        print(units)
    for i in units:
        sqi =  i*i % n
        if Comments:
            print(i,i*i,sqi)
        try:
            sqrt[sqi].append(i)
        except:
            sqrt[sqi] = [i]
    return sqrt

def zn_units(n,Comments=False):
    """
    Renders the set of units of Zn.
    """
    units = set()
    for i in range(1,n):
        for j in range(1,n):
            if (i * j) % n == 1:
                units.add(i)
                units.add(j)
    if Comments:
        print(units)
    return units

def computePiDecimals(decimalWordLength=4,nbrOfWords=600,Comments=False):
    """
    Renders at least decimalWordLenght * nbrOfWords (default: 4x600=2400) decimals of :math:`\pi`.
    The Python transcription here recodes an original C code of unknown author (see [*]_).

    Uses the following infinite Euler series:
    
         :math:`\pi = 2 * \sum_{n=0}^{\infty} [ (n !) / (1 * 3  * 5 ... * (2n+1)) ].`
    
    The series gives a new :math:`\pi` decimal after adding in average 3.32 terms.

        >>> from arithmetics import computePiDecimals
        >>> from time import time
        >>> t0=time();piDecimals = computePiDecimals(decimalWordLength=3,nbrOfWords=100);t1= time()
        >>> print('pi = '+piDecimals[0]+'.'+piDecimals[1:])
        pi = 3.14159265358979323846264338327950288419716939937510582097494459
        2307816406286208998628034825342117067982148086513282306647093844609
        5505822317253594081284811174502841027019385211055596446229489549303
        8196442881097566593344612847564823378678316527120190914564856692346
        034861045432664821339360726024914127372458700660630
        >>> print('precision = '+str(len(piDecimals[1:]))+'decimals')
        precision = 314 decimals
        >>> print('%.4f' % (t1-t0)+' sec.')
        0.0338 sec.
    
    .. [*] *Source:* J.-P. Delahaye "*Le fascinant nombre* :math:`\pi`", Pour la science Belin 1997 p.95.
    """
    na =    decimalWordLength  # maximal string length of a number expressed in base a
    a = 10**na                             # base of the integer computations of the decimals
    prna = nbrOfWords * na        # total number of  decimals to compute in base a
    c = prna*3 + prna//2              # Euler's pi series requires about 3.5 steps for one more pi decimal
    e = 0                                       # gathers the next na pi-decimals in base a
    x = a//5
    h = [x for i in range(c+1)]   # vectrized accumulator for the Horner transform of Euler's pi series
                                                    # a/10 pi = a/5( 1 + 1/3(1 + 2/5(1 + 3/7(...))))
                                                    # ! h index runs from 1 to c; f[0] is ignored !
    piDecimals = ''
    while c > 0:
        g = 2*c
        d = 0
        b = c
        while b > 0:
            d += h[b]*a
            g -=1
            d,h[b] = divmod(d,g)  # d = d//g; h[b] = d % g
            g -= 1
            b -= 1
            if b != 0:
                d *= b
        c -= (na*3 + na//2)     # ng * 3.5 steps for each group of ng decimals expressed in base a
        e += d // a
        nd = ('%%0%dd' % na) % e
        if Comments:
            print(nd)
        piDecimals += nd
        e = d % a
    if Comments:
        print('pi = '+piDecimals[0]+'.')
        print(piDecimals[1:])
    return piDecimals

def sternBrocot(m=5,n=7,Debug=False):
    """
    Renders the Stern-Brocot representation of the rational m/n (m and n are positive integers).
    For instance, sternBrocot(5,7) = ['L','R','R','L'].

    *Source*: Graham, Knuth, Patashnik, Sec. 4.5 in Concrete Mathematics 2nd Ed., Addison-Wesley 1994, pp 115-123. 
    """
    sb = []
    while m != n:
        if m < n:
            sb.append('L')
            n -= m
        else:
            sb.append('R')
            m -= n
        if Debug:
            print(sb)
    return sb

def invSternBrocot(sb=['L','R','R','L'],Debug=False):
    """
    Computing the rational which corresponds to the Stern-Brocot string sb.

    *Source*: Graham, Knuth, Patashnik, Sec. 4.5 in Concrete Mathematics 2nd Ed., Addison-Wesley 1994, pp 115-123. 
    """
    def _matMult(S,X):
        R = [[S[0][0]*X[0][0]+S[0][1]*X[1][0],S[0][0]*X[0][1]+S[0][1]*X[1][1]],
             [S[1][0]*X[0][0]+S[1][1]*X[1][0],S[1][0]*X[0][1]+S[1][1]*X[1][1]]]
        return R
    L = [[1,1],
         [0,1]]
    R = [[1,0],
         [1,1]]
    S = [[1,0],
         [0,1]]
    while sb != []:
        if sb[0] == 'L':
            S = _matMult(S,L)
        else:
            S = _matMult(S,R)
        if Debug:
            print(S)
        sb = sb[1:len(sb)]
        if Debug:
            print(sb)
    m = S[1][0]+S[1][1]
    n = S[0][0]+S[0][1]
    return m,n

def computeFareySeries(n=7,AsFloats=False,Debug=False):
    """
    Renders the Farey series, ie the ordered list of positive rational fractions with positive denominator lower or equal to n. For *n* = 1, we obtain: [[0,1],[1,1]].

    *Parametrs*:

        *n*: strictly positive integer (default = 7).
        *AsFloats*: If True (defaut False), renders the list of approximate floats corresponding to the rational fractions. 

    *Source*: Graham, Knuth, Patashnik, Sec. 4.5 in Concrete Mathematics 2nd Ed., Addison-Wesley 1994, pp 115-123. 
    """
    f = [[0,1],[1,1]]
    if n < 1:
        print('Error: n >=1! n = %d' % n)
    elif n == 1:
        return f

    i = 1
    while i < n:
        i += 1
        if Debug:
            print(i)
        fcur=[]
        j = 0
        while j < len(f)-1:
            if Debug:
                print(j)
            fcur.append(f[j])
            num = f[j][1] + f[j+1][1]
            if Debug:
                print(num,i)
            if num == i:
                denom = f[j][0] + f[j+1][0]
                fcur.append([denom,num])
            #fcur.append(f[j+1])
            j += 1
            if Debug:
                print(fcur)
        fcur.append(f[j])
        f = list(fcur)
    if AsFloats:
        f = [float(x[0])/float(x[1]) for x in f]
    return f

###############################
if __name__ == '__main__':
    ######  scratch pad for testing the module components
##    from digraphs import *
##    print(factorization(2224))
##    print(gcd(2224,12345))
##    print(lcm(2224,12345))
##    print(totient(11))
##    print(zn_squareroots(60,Comments=True))
##
##    a = 17
##    b = 1
##    m = 19
##    
##    print( ( "Congruence: %dx =  %d (mod %d)" % (a,b,m) ) )  # \equiv = \u2262
##
##    x,y,A,B = solPartEqnDioph(a,m,b)
##
##    if x == None:
##        print("Pas de solution")
##    else:
##        print("Solution générale: x = %d + %dn" % (x,B))
##        h = gcd(a,m)
##        y = m / h
##        print('m,h,y',m,h,y)
##        print("Il y a %d solution(s) particulière(s):" % (h))
##        for i in range(h):
##            print("x_%d = %d + %d*%d (mod %d) = %d" % (i+1,x,i,y,m,(x + (i*y))%m ))
##            
##    l = QuadraticResiduesDigraph(primesBelow(20,Odd=True))
##    l = QuadraticResiduesDigraph(range(1,20))
##    l.showRelationTable(Sorted=False)
##    l.exportGraphViz('legendre')
##    al = AsymmetricPartialDigraph(l)
##    al.exportGraphViz('legendreAsym')
##    al.computeChordlessCircuits()
##    al.showChordlessCircuits()
##
##    for i in range(1,13):
##        print(i,moebius_mu(i))
##
##    f12 = Factorizations
##    D12 = divisors(12)
##    print(D12)
##    print(totient(234))
##    tot = 0
##    for d in divisors(234):
##        tot += moebius_mu(d)*234//d
##    print(tot)
##    tot = 0
##    for d in divisors(234):
##        tot += d * moebius_mu(234//d)
##    print(tot)
##    for i in range(1,100):
##        df = divisorsFunction(0,i)
##        print(df)
##        if df % 2 == 1:
##            print('-->',i)
##        print(divisorsFunction(1,i))
##        print(divisorsFunction(2,i))
        
    # from time import time
    # t0 = time()
    # piDecimals = computePiDecimals(decimalWordLength=5,nbrOfWords=1000)
    # print(time()-t0,end=' sec.\n')
    # print('pi = '+piDecimals[0]+'.')
    # print(piDecimals[1:])
    # print('precision = '+str(len(piDecimals[1:])),end=" decimals\n")
    
##    sb = sternBrocot(21,101)
##    print(sb)
##    (m,n) = invSternBrocot(sb)
##    print(m,n)
##    print(computeFareySeries(n=10,AsFloats=False,Debug=True))
##
    from math import sqrt
    p = 5
    q = 8
    print('p =',p,', q =',q)
    print('cf(p,q) = ', continuedFraction(p,q) )
    print('eval(cf(p,q)) = ', evalContinuedFraction(continuedFraction(p,q)) )
    cf = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    print('cf(sqrt(2))_%d = ' % (len(cf)-1), cf )
    print('eval(cf(sqrt(2))_%d) = ' % (len(cf)-1), evalContinuedFraction(cf) )
    print('sqrt(2)              = ', sqrt(2) )
