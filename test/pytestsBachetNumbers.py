#######################
# R. Bisdorff
# pytest functions for the bachetNumbers module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from bachetNumbers import *
    
def testBachetIntegerEncoding():
    print('==>> Testing Bachet encoding of integers')
    n1 = BachetVector(12)
    n2 = BachetInteger(13)
    n3 = n1 + n2
    n4 = n1 * n2
    print('%s (%d) + %s (%d) = %s (%d)' % (n1, int(n1), n2, int(n2), n3, int(n3) ))
    print('%s (%d) * %s (%d) = %s (%d)' % (n1, int(n1), n2, int(n2), n4, int(n4) ))

    print('length of %s = %d' % (n1, len(n1)))
    n5 = n1.reverse()
    n6 = -n2
    print('%s (%d) + %s (%d) = %s (%d)' % ( n5, int(n5), n6, int(n6),n5 + n6, int(n5+n6) ))
def testBachetAdditionTimings():
    print('==>> Testing Bachet addition runtimes')
    from random import shuffle
    from time import time

    bi = BachetInteger(0)
    t0 = time()
    for s in range(1000):
        bi = bi + BachetInteger(s)
    
    print('addbi');print(time() - t0)
    bv = BachetVector(0)
    t0 = time()
    for s in range(1000):
        bv = bv + BachetVector(s)
    print('addbv');print(time() - t0)
def testBachetMultiplying():
    print('==>> Testing Bachet vector Multiplications')
    b1 = BachetInteger(12)
    b2 = BachetInteger(24)
    res = b1*b2
    print(res,int(res))
    b1 = BachetVector(12)
    b2 = BachetVector(24)
    res = b1*b2
    print(res,int(res))
def testBachetDivmod():
    print('==>> Testing Bachet vector divmod')
    n = BachetVector(vector=[1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[1,-1,-1,1])
    q,r = n._vdivmod(d)
    print('1) %d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('1) %d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    n = BachetVector(vector=[-1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[1,-1,-1,1])
    q,r = n._vdivmod(d)
    print('2)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('2)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    n = BachetVector(vector=[1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[-1,-1,-1,1])
    q,r = n._vdivmod(d)
    print('3)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('3)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    
    


    
