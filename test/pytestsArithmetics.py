#######################
# R. Bisdorff
# pytest functions for the arithmetics module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from arithmetics import *
from digraphs import *

def testArithemtics():
    print('==>> Testing arithemtics')    
    print(factorization(2224))
    print(gcd(2224,12345))
    print(lcm(2224,12345))
    print(totient(11))
    print(zn_squareroots(60,Comments=True))

    a = 17
    b = 1
    m = 19
    
    print( ( "Congruence: %dx =  %d (mod %d)" % (a,b,m) ) )  # \equiv = \u2262

    x,y,A,B = solPartEqnDioph(a,m,b)

    if x == None:
        print("Pas de solution")
    else:
        print("Solution générale: x = %d + %dn" % (x,B))
        h = gcd(a,m)
        y = m / h
        print('m,h,y',m,h,y)
        print("Il y a %d solution(s) particulière(s):" % (h))
        for i in range(h):
            print("x_%d = %d + %d*%d (mod %d) = %d" % (i+1,x,i,y,m,(x + (i*y))%m ))
            
    l = QuadraticResiduesDigraph(primesBelow(20,Odd=True))
    #l = QuadraticResiduesDigraph(range(1,20))
    l.showRelationTable(Sorted=False)
    l.exportGraphViz('legendre')
    al = AsymmetricPartialDigraph(l)
    al.exportGraphViz('legendreAsym')
    al.computeChordlessCircuits()
    al.showChordlessCircuits()

    for i in range(1,13):
        print(i,moebius_mu(i))

def testComputePiDecimals():
    print('==>> Testing computePiDecimals')
    from time import time
    t0 = time()
    piDecimals = computePiDecimals(decimalWordLength=5,nbrOfWords=1000)
    print(time()-t0,end=' sec.\n')
    print('pi = '+piDecimals[0]+'.')
    print(piDecimals[1:])
    print('precision = '+str(len(piDecimals[1:])),end=" decimals\n")

def testSternBrocot():
    print('==>> Testing the Stern-Brocot encoding of rationals')
    sb = sternBrocot(21,101,Debug=True)
    print(sb)
    (m,n) = invSternBrocot(sb,Debug=True)
    print(m,n)

def testContinuedFraction():
    from math import sqrt
    p = 5
    q = 8
    print('p =',p,', q =',q)
    print('cf(p,q) = ', simpleContinuedFraction(p,q) )
    print('eval(cf(p,q)) = ', decimalEvalContinuedFraction(simpleContinuedFraction(p,q)) )
    cf = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    print('cf(sqrt(2))_%d = ' % (len(cf)-1), cf )
    print('eval(cf(sqrt(2))_%d) = ' % (len(cf)-1), decimalEvalContinuedFraction(cf) )
    print('sqrt(2)              = ', sqrt(2) )
    
    


    
