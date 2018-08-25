#######################
# R. Bisdorff
# randomNumbers.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsRandomNumbers.py
# # Current $Revision:  $
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
     


    
