#!/Usr/bin/env python3
"""
Python3+ implementation of arithmetics tools

Copyright (C) 2016-2024 Raymond Bisdorff

Tools gathered for doing arithmetics.
Mainly inspired from G.A. Jones & J.M. Jones,
Elementary Number Theroy,
Springer Verlag London 1998.

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: Python 3.10 $"

from arithmetics import *
from digraphs import Digraph
from decimal import Decimal
from collections import OrderedDict

#---------------
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
       >>> primesBelow20 = primesBelow(20,Odd=True)
        [3,5,7,11,13,17,19]
       >>> leg = QuadraticResiduesDigraph(primesBelow20)
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

# ------ Bachet bipolar {-1,0,1} base 3 encoded integers ---------------
# Discrete Mathematics lectures 2008
# (c) 2025 RB 

class Bachet(object):
    """
    Bipolar-valued base {-1,0,1} encoded Bachet integers
    
    https://en.wikipedia.org/wiki/Claude_Gaspar_Bachet_de_M%C3%A9ziriac
    
    >>> from arithmetics import Bachet
    >>> n1 = Bachet(12)
    >>> n2 = Bachet(13)
    >>> n3 = n1 + n2
    >>> print('%s (%d) + %s (%d) = %s (%d)' % (n1, n1.value(), n2, n2.value(), n3, n3.value() ))
     110 (12) + 111 (13) = 10-11 (25)
    >>> print('length of %s = %d' % (n1, len(n1)))
     length of 110 = 3
    >>> n1.reverse()
    >>> -n2
    >>> print('%s (%d) + %s (%d) = %s (%d)' % ( n1, n1.value(), n2, n2.value(),n1 + n2, (n1+n2).value() ))
     011 (4) + -1-1-1 (-13) = -100 (-9)

    """
    def __repr__(self):
        """
        Default presentation method for Bchet number instances.
        """
        reprString = '*------- Bachet number description ------*\n'
        reprString += 'Instance class : %s\n' % self.__class__.__name__
        reprString += 'String         : %s\n' % str(self)
        reprString += 'Vector         : %s\n' % self.vector
        reprString += 'Length         : %d\n' % len(self)
        reprString += 'Value          : %d\n' % self.value()
        reprString += 'Attributes     : %s\n' % list(self.__dict__.keys())    
        return reprString
    
    def __init__(self,num_int):
        """
        Tranforms a potentially signed integer into a Bachet number
        """
        self.vector = self._int2bachet(num_int)

    def __str__(self):
        """
        Defines the printable string version of a Bachet number
        """
        bachet_string = ''
        for i in range(len(self.vector)):
            bachet_string += str(self.vector[i])
        return bachet_string
       
    def __neg__(self):
        """
        Defines the negation operator for Bachet encoded numbers
        """
        from copy import copy
        neg = copy(self)
        for i in range(len(self.vector)):
            neg.vector[i] = self.vector[i] * -1
        return neg
        
    def __add__(self,other):
        """
        Defines the addition operator for Bachet encoded numbers
        """
        n1 = self.value()
        n2 = other.value()
        n3 = n1 + n2
        return Bachet(n3)

    def __mul__(self,other):
        """
        Defines the addition operator for Bachet encoded numbers
        """
        n1 = self.value()
        n2 = other.value()
        n3 = n1 * n2
        return Bachet(n3)
        
    def _base10to3(self,num):
        """
        Change a base 10 number to a base 3 number.
        """
        new_num_string = ''
        current = num
        while current != 0:
            remainder = current%3
            remainder_string = str(remainder)
            new_num_string = remainder_string + new_num_string
            current = current//3
        return new_num_string

    def _base3toBachet(self,num_string):
        """
        Converts a base 3 encoded integer into a
        bipolar {-1,0,1} encoded one.

        """
        new_vector=[0 for x in range(len(num_string))]
        reste = 0
        for i in range(len(num_string)-1,-1,-1):
            num = eval(num_string[i])+reste
            if num == 2:
                new_vector[i] = -1
                reste = 1
            elif num == 3:
                new_vector[i] = 0
                reste = 1
            else:
                new_vector[i] = num
                reste = 0
        
        if reste == 1:
            new_vector = [1] + new_vector
            
        return new_vector

    def _int2bachet(self,num_int):
        """
        Converts a signed integer into a Bachet encoded number
        """
        if num_int < 0:
            unsigned_num_int = abs(num_int)
        else:
            unsigned_num_int = num_int
        base3_unsigned_num_int = self._base10to3(unsigned_num_int)
        bachet_unsigned_num_int = self._base3toBachet(base3_unsigned_num_int)
        if num_int > 0:
            return bachet_unsigned_num_int
        elif num_int == 0:
            return '0',[0]
        else:
            bachet_vector = bachet_unsigned_num_int
            for i in range(len(bachet_unsigned_num_int)):
                bachet_vector[i] = bachet_unsigned_num_int[i]*-1
            return bachet_vector
       
    def value(self):
        """
        Renders the integer corresponding to the Bachet number
        """
        result_int = 0
        for i in range(len(self.vector)):
            result_int += 3**i*self.vector[len(self.vector)-i-1]
        return result_int

    def __len__(self):
        """
        Returns the length of the Bachet encoding
        """
        return len(self.vector)

    def reverse(self):
        """
        Reverses the Bachet code
        """
        from copy import copy
        rev = copy(self)
        result = [0 for i in range(len(self.vector))]
        for i in range(len(self.vector)):
            result[i] = self.vector[len(self.vector)-i-1]
        rev.vector = result
        return rev

#------------- end of Bachet class ------------------
    
def primesBelow(N,Odd=False):
    """

    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    Input N>=6, Returns a list of primes, 2 <= p < N

    >>> import arithmetics as ar
    >>> ar.primesBelow(30,Odd=True)
     [3, 5, 7, 11, 13, 17, 19, 23, 29]

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

def _pollard_brent(n):
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
    """
    >>> import arithmetics as ar
    >>> ar.primeFactors(12345)
    [3, 5, 823]

    """
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
        factor = _pollard_brent(n) # trial division did not fully factor, switch to pollard-brent
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

    >>> import arithmetics as ar
    >>> ar.factorization(15)
     OrderedDict({3: 1, 5: 1})
    >>> ar.moebius_mu(15)
     1
    >>> ar.factorization(12345)
     OrderedDict({3: 1, 5: 1, 823: 1})
    >>> ar.moebius_mu(12345)
     -1
    >>> ar.factorization(12321)
     OrderedDict({3: 2, 37: 2})
    >>> ar.moebius_mu(12321)
     0

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

    >>> import arithmetics as ar
    >>> ar.divisors(12)
     [1, 2, 3, 4, 6, 12]
     
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

    >>> import arithmetics as ar
    >>> ar.totient(12)
     4

    """
    if n == 0: return 1

    try: return _totients[n]
    except KeyError: pass

    tot = 1
    for p, exp in factorization(n).items():
        tot *= (p - 1)  *  p ** (exp - 1)

    _totients[n] = tot
    return tot
        
def simpleContinuedFraction(p, q, Comments=False):
    """
    Renders the continued fraction [a_0,a_1,a_2,...,a_n]
    of the ratio of two positive integers p > 0 and q > 0 by
    following Euclide's division algorithm.

    >>> import arithmetics as ar
    >>> ar.simpleContinuedFraction(12,7,Comments=True)
     12//7 = 1R5
     7//5 = 1R2
     5//2 = 2R1
     2//1 = 2R0
     [1, 1, 2, 2]
    
    """
    if p < 0 or q < 0:
        Print('Error: p and q arguments must be positive integers!') 
        return None
    if type(p) != int or type(q) != int:
        Print('Error: p and q arguments must be positive integers!')
        return None
    
    res = [p//q]
    if Comments:
        print('%d//%d = %dR%d' % (p,q,(p//q),(p%q)) )
    while q > 0: 
        p, q = q, p % q
        if q > 1:
            res.append(p//q)
        elif q == 1 :
            res.append(p)
        if Comments:
            if q > 0:    
                print('%d//%d = %dR%d' % (p,q,(p//q),(p%q)) )
    return res

def simpleConvergents(cf, AsFloats=False):
    """
    Renders the convergents *pi* and *qi* for *i* = 0 to *n* in list format
    for a given simple continued fraction of two positive integer *a* and *b*.
    - If AsFloats==True, the float value *fi = pi/qi* are also provided.
    - The return delivers a tuple (p,q) or (p,q,f).
    - p[-1] and q[-1] deliver the initial numerator *a* and denominator *b*.
    - f[-1] delivers the float value of the rational fraction *a/b*.

    >>> import arithmetics as ar
    >>> cf = ar.simpleContinuedFraction(12,7)
    >>> cf
     [1, 1, 2, 2]
    >>> p,q,f = ar.simpleConvergents(cf, AsFloats=True)
    >>> p
     [1, 2, 5, 12]
    >>> q
     [1, 1, 3, 7]
    >>> f
     [1.0, 2.0, 1.6666666666666667, 1.7142857142857142]

    """
    n = len(cf)
    a = cf
    p = [a[0],(a[1]*a[0] + 1)]
    q = [1,a[1]]
    for i in range(2,n):
        p.append(a[i]*p[i-1] + p[i-2])
        q.append(a[i]*q[i-1] + q[i-2])
    f = []
    if AsFloats:
        for i in range(n):
            f.append(p[i]/q[i])
        return (p,q,f)
    else:
        return (p,q)

def decimalEvalContinuedFraction(cf):
    """
    Backwise recursive evaluation: ev_i-1 + 1/ev_i, for i = n,..,1
    of the continued fraction cf = [a_0,a_1,a_2,...,a_n] and 
    where a_0 corresponds to its integer part.

    >>> import arithmetics as ar
    >>> ar.decimalEvalContinuedFraction([1, 1, 2, 1, 1])  # 12/7
     Decimal('1.714285714285714285714285714')
    >>> 12/7
     1.7142857142857142

    """
    from decimal import Decimal
    n = len(cf) - 1
    res = Decimal(str(cf[n]))
    for i in range(n-1,0,-1):
        res = Decimal(str(cf[i])) + Decimal('1')/res
    res = Decimal(str(cf[0])) + Decimal('1')/res
    return res

def cf2Rational(cf, AsDecimal=False, Debug=False):
    """
    Converts the finite continued Fraction *cf* back to
    its corresponding rational number expression.
    Returns a/b or (a/b, Decimal(a/b)) if AsDecimal is True.

    >>> import arithmetics as ar
    >>> ar.simpleContinuedFraction(75,8)
     [9, 2, 1, 1, 1]
    >>> ar.cf2Rational([9,2,1,1,1], AsDecimal=True)
     ('75/8', Decimal('9.375')
    >>> eval('75/8')
     9.375

    """
    from decimal import Decimal
    p,q = simpleConvergents(cf)
    a = p[-1]
    b = q[-1]
    res = '%d/%d' % (a, b)
    if AsDecimal:
        resd = Decimal(str(a))/Decimal(str(b))
        return res,resd
    else:
        return res

def continuedFraction(x, terms=20, AsFloats=False, rel_tol=1e-9, abs_tol=0.0):
    """

    Source: https://leancrew.com/all-this/2023/08/continued-fractions-in-python/
    See also: https://en.wikipedia.org/wiki/Continued_fraction
    
    Returns a tuple with the continued fraction (in list format)
    and the convergents (in Fraction format) of the argument.

    >>> import arithmetics as ar
    >>> from math import sqrt, pi
    >>> ar.continuedFraction(sqrt(2))
     ([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [Fraction(1, 1),
     Fraction(3, 2), Fraction(7, 5), Fraction(17, 12), Fraction(41, 29),
     Fraction(99, 70), Fraction(239, 169), Fraction(577, 408),
     Fraction(1393, 985), Fraction(3363, 2378), Fraction(8119, 5741),
     Fraction(19601, 13860), Fraction(47321, 33461)])
    >>> ar.continuedFraction(sqrt(2),AsFloats=True)
     ([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
     [1.0, 1.5, 1.4, 1.4166666666666667, 1.4137931034482758,
      1.4142857142857144, 1.4142011834319526, 1.4142156862745099,
      1.4142131979695431, 1.4142136248948696, 1.4142135516460548,
      1.4142135642135643, 1.4142135620573204])
    >>> ar.continuedFraction(pi,rel_tol=1e-15,AsFloats=True)
     ([3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14],
    [3.0, 3.142857142857143, 3.141509433962264, 3.1415929203539825,
     3.1415926530119025, 3.141592653921421, 3.1415926534674368,
     3.1415926536189365, 3.141592653581078, 3.141592653591404,
     3.141592653589389, 3.1415926535898153, 3.1415926535897927])
    >>> pi
     3.141592653589793

    """

    from fractions import Fraction
    from math import isclose
    
    # Initialize, using Khinchin's notation
    a = []       # continued fraction terms
    p = [0, 1]   # convergent numerator terms (-2 and -1 indices)
    q = [1, 0]   # convergent denominator terms (-2 and -1 indices)
    s = []       # convergent terms
    remainder = x
  
    # Collect the continued fraction and convergent terms
    for i in range(terms):
        # Compute the next terms
        whole, frac = divmod(remainder, 1)
        an = int(whole)
        pn = an*p[-1] + p[-2]
        qn = an*q[-1] + q[-2]
        sn = Fraction(pn, qn)
   
        # Add terms to lists
        a.append(an)
        p.append(pn)
        q.append(qn)
        s.append(Fraction(sn))
  
        # Convergence check
        if isclose(x, float(sn), rel_tol=rel_tol, abs_tol=abs_tol):
            break

        # Get ready for next iteration
        remainder = 1/frac
  
    # Return the tuple of the continued fraction and the convergents
    if AsFloats:
        s = [float(x) for x in s]
    return(a, s) 

def gcd(a, b):
    """
    Renders the greatest common divisor of two positive integers a and b. 

    >>> import arithmetics as ar
    >>> ar.gcd(120,16)
     8

    """
    if a < 0 or b < 0:
        print('Error: both parameters a and b must be positive integers')
        return None
    a = int(a)
    b = int(b)
    if a == b: return a
    while b > 0: a, b = b, a % b
    return a
    
def lcm(a, b):
    """
    Renders the least common multiple of a and b.

    >>> import arithmetics as ar
    >>> ar.lcm(120,16)
     240

    """
    return abs(a * b) // gcd(a, b)

def bezout(a,b,Comments=False,Debug=False):
    """
    Renders the tuple *(d,x,y)* wher *d = gcd(a,b)* and *x* and *y* are the
    Bezout coefficients such that *d = ax + by*.

    Both arguments *a* and *b* must be positive integers.

    >>> import arithmetics as ar
    >>> ar.bezout(120,16,Comments=True)
     d = 8, x = 1, y = -7
     8 = 120*1 + 16*(-7)
     (8, 1, -7)
    """
    
    x,y,u,v = 1,0,0,1
    if a < 0 or b  < 0:
        print('Error: a and b must be positive integers !')
        return None,None,None
    arga = int(a)
    argb = int(b)
    if Debug:
        print(a,0,x,y)
        print(a,b,u,v)
    while b != 0:
        r = a % b
        q = (a - r)//b
        x,y, u,v = u,v, x-(q*u),y-(q*v)
        if Debug:
            print(a,b,q,r,u,v)
        a,b = b,r
    if Comments:
        print('d = %d, x = %d, y = %d' % (a,x,y))
        if x < 0:
            print('%d = %d*(%d) + %d*%d' % (a,arga,x,argb,y))
        elif y < 0:
            print('%d = %d*%d + %d*(%d)' % (a,arga,x,argb,y))
        else:
            print('%d = %d*%d + %d*%d' % (a,arga,x,argb,y))
    return a,x,y

def solPartEqnDioph(a,b,c,Comments=False):
    """
    renders a particular integer solution of the Diophantian equation
    ax + by = c. The method returns the tuple
    (C*x, B*y, A, B) where d = gcd(a,b), C=c//d, A = a//d, and B=b//d. 

    >>> import arithmetics as ar
    >>> ar.solPartEqnDioph(3,4,5,Comments=True)
     d = 1, a = 3, x = -5, b = 4, y = 5
     (3)*(-5) + (4)*(5) = 5
     (-5, 5, 3, 4)

    """

    d = gcd(a,b)
    if c % d != 0:
        return None,None,None,None # pas de solution
    
    A,B,C = a//d, b//d, c//d

    D,x,y = bezout(A,B)

    if Comments:
        print('C*x = %d, C*y = %d, A = %d, B = %d' % (C*x,C*y,A,B))
        print('(%d)*(%d) + (%d)*(%d) = %d' % (a, C*x, b, C*y, d)) 

    return C*x, C*y, A, B  # solution particulière plus coefficients

def zn_units(n,Comments=False):
    """
    Renders the set of units of Zn.
    
    >>> import arithmetics as ar
    >>> ar.zn_units(12)
     {1, 11, 5, 7}
     
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

def zn_squareroots(n,Comments=False):
    """
    Renders the quadratic residues of Zn as a dictionary.

    >>> import arithmetics as ar
    >>> ar.zn_squareroots(13,Comments=False)
     {1: [1, 12], 4: [2, 11],
      9: [3, 10], 3: [4, 9],
      12: [5, 8], 10: [6, 7]}
    
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

def computePiDecimals(decimalWordLength=4,nbrOfWords=600,Comments=False):
    """
    Renders at least *decimalWordLenght* x *nbrOfWords* (default: 4x600=2400)
    decimals of :math:`\\pi`.

    The Python transcription here recodes an original C code of unknown author (see [*]_).

    Uses the following infinite *Euler* series:
    
         :math:`\\pi = 2 * \\sum_{n=0}^{\\infty} [ (n !) / (1 * 3  * 5 ... * (2n+1)) ].`
    
    The series gives a new :math:`\\pi` decimal after adding in average 3.32 terms.

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
    
    .. [*] *Source:* J.-P. Delahaye "*Le fascinant nombre* :math:`\\pi`", Pour la science Belin 1997 p.95.
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

    >>> import arithmetics as ar
    >>> ar.computeFareySeries(4)
     [[0, 1], [1, 4], [1, 3], [1, 2], [2, 3], [3, 4], [1, 1]]
    >>> ar.computeFareySeries(4,AsFloats=True)
    [0.0, 0.25, 0.3333333333333333, 0.5, 0.6666666666666666, 0.75, 1.0]

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

def solvingQuadraticEquation(a,b,c,Comments=False):
    """
    Renders both roots x,y of ax2 + bx + c = 0 where
    x = (-b + sqrt(b^2 -4ac))/2a and
    y = (-b - sqrt(b^2 -4ac))/2a

    >>> import arithmetics as ar
    >>> ar.solvingQuadraticEquation(1,-2,-1,Comments=True)
     D = (b^2 -4*a*c) = 8.000000
     D > 0 => two real roots
     (2.414213562373095, -0.41421356237309515)
    >>> ar.solvingQuadraticEquation(1,2,1,Comments=True)
     D = (b^2 -4*a*c) = 0.000000
     D == 0 => one real root
     (-1.0, -1.0)
    >>> ar.solvingQuadraticEquation(-1,6,-10,Comments=True)
     D = (b^2 -4*a*c) = -4.000000
     D < 0 => two complex roots
     ((3-1j), (3+1j))

    """
    from math import sqrt
    D = (b*b -4*a*c)
    if Comments:
        print('D = (b^2 -4*a*c) = %f' % D )
        
    if D > 0:
        if Comments:
            print('D > 0 => two real roots')
        x = (-b + sqrt(D))/(2*a)
        y = (-b - sqrt(D))/(2*a)
    elif D == 0:
        if Comments:
            print('D == 0 => one real root')
        x = -b / (2*a)
        y = -b / (2*a)
    else:
        if Comments:
            print('D < 0 => two complex roots')       
        z = sqrt(-D)
        x = (complex(-b,z))/(2*a)
        y = (complex(-b,-z))/(2*a)
    return x,y
    
###############################
if __name__ == '__main__':
    print("""
    ****************************************************
    * Digraph3 arithmetics module                      *
    * Revision: Python3.9                              *
    * Copyright (C) 2010-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    
    ######  scratch pad for testing the module components
##    from math import sqrt
##    p = 5
##    q = 8
##    print('p =',p,', q =',q)
##    print('cf(p,q) = ', simpleContinuedFraction(p,q) )
##    print('eval(cf(p,q)) = ', decimalEvalContinuedFraction(simpleContinuedFraction(p,q)) )
##    cf = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
##    print('cf(sqrt(2))_%d = ' % (len(cf)-1), cf )
##    print('eval(cf(sqrt(2))_%d) = ' % (len(cf)-1), decimalEvalContinuedFraction(cf) )
##    print('sqrt(2)              = ', sqrt(2) )
##
    print('*-----Computing with Bachet numbers----------*') 
    n1 = Bachet(12)
    n2 = Bachet(13)
    n3 = n1 + n2
    n4 = n1 * n2
    print('%s (%d) + %s (%d) = %s (%d)' % (n1, n1.value(), n2, n2.value(), n3, n3.value() ))
    print('%s (%d) * %s (%d) = %s (%d)' % (n1, n1.value(), n2, n2.value(), n4, n4.value() ))

    n5 = n1.reverse()
    n6 = -n2
    print('%s (%d) + %s (%d) = %s (%d)' % ( n5, n5.value(), n6, n6.value(),n5 + n6, (n5+n6).value() ))

    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
#####################################
