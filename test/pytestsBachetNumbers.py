#######################
# R. Bisdorff
# pytest functions for the arithmetics module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from bachetNumbers import *
    
def testBachetIntegerEncoding():
    print('==>> Testing Bachet encoding of integers')
    n1 = BachetNumber(12)
    n2 = BachetNumber(13)
    n3 = n1 + n2
    n4 = n1 * n2
    print('%s (%d) + %s (%d) = %s (%d)' % (n1, int(n1), n2, int(n2), n3, int(n3) ))
    print('%s (%d) * %s (%d) = %s (%d)' % (n1, int(n1), n2, int(n2), n4, int(n4) ))

    print('length of %s = %d' % (n1, len(n1)))
    n5 = n1.reverse()
    n6 = -n2
    print('%s (%d) + %s (%d) = %s (%d)' % ( n5, int(n5), n6, int(n6),n5 + n6, int(n5+n6) ))
    
    


    
