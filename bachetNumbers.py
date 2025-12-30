#!/Usr/bin/env python3
"""
Python3+ implementation of bipolar-valued base 3 integers due to
Claude Gaspard Bachet de Méziriac (1621)

Two versions are provided:

    - the *BachetVector* class based on the balanced ternary vectors 

    - the *BachetInteger* class based on the int() values of the Bachet numbers,
      faster with large integer numbers 


:ref:`See applications of bipolar-valued base 3 encoded Bachet numbers <Bachet-Tutorial-label>`

Copyright (C) 2025 Raymond Bisdorff

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the
Free Software Foundation, Inc., 51 Franklin Street,
Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "$Revision: Python 3.12.8 $"

# ------ Bachet bipolar {-1,0,1} base 3 encoded integers ---------------
# Discrete Mathematics lectures 2008
# (c) 2025 RB

from bachetNumbers import *
from decimal import Decimal

class BachetNumber(object):
    """
    Abstract base class for Bipolar-valued {-1,0,+1} base 3 encoded integers 

    """
    def __repr__(self):
        """
        Default presentation method for Bachet number instances.
        """
        reprString = '*------- Bachet number description ------*\n'
        reprString += 'Instance class : %s\n' % self.__class__.__name__
        reprString += 'String         : \'%s\'\n' % str(self)
        reprString += 'Vector         : %s\n' % self.vector
        reprString += 'Length         : %d\n' % len(self)
        reprString += 'Value          : %d\n' % int(self)
        reprString += 'Attributes     : %s\n' % list(self.__dict__.keys())    
        return reprString

    def _base10to3(self,num,/):
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

    def _base3toBachet(self,num_string,/):
        """
        Converts a base 3 encoded integer into a bipolar {-1,0,+1} encoded one.

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

    def _int2bachet(self,num_int,/):
        """
        Converts a signed integer into a Bachet encoded number.
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
            return [0]
        else:
            bachet_vector = bachet_unsigned_num_int
            for i in range(len(bachet_unsigned_num_int)):
                bachet_vector[i] = bachet_unsigned_num_int[i]*-1
            return bachet_vector

    def toDecimal(self,/):
        """
        Return Decimal(int(self))
        """
        from decimal import Decimal
        return Decimal(int(self))
        
    def __str__(self, /):
        """
        Defines the printable string version of a Bachet number.
        """
        bachet_string = ''
        for i in range(len(self.vector)):
            if self.vector[i] != 0:
                bachet_string += '%+d' % (self.vector[i])
            else:
                bachet_string += '%d' % (self.vector[i])
        return bachet_string

    def __neg__(self, /):
        """
        Defines an unary negating operator for Bachet encoded numbers.
        """
        from copy import deepcopy
        negVector = []
        ln = len(self.vector)
        for i in range(ln):
            negVector.append(self.vector[i] * -1)
        neg = BachetInteger(vector = negVector,length=ln)
        return neg

    def sign(self,/,Debug=True):
        """
        Return the first non-zero position (-1 or +1) in self.vector
        Returns 0 if int(self) = 0
        """
        ln = len(self)
        i = 0
        vector = self.vector
        while vector[i] != 0 and i >= ln:
            i += 1
        if i < ln:
            return vector[i]
        else:
            return 0

    def __sub__(self,other, /):
        """
        Return self-other
        """
        new = self + (-other)
        return new

    def __rsub__(self,other, /):
        """
        Return self-other
        """
        new = (-other) + self
        return new

    def __floordiv__(self,other,/):
        """
        Return self//other
        """
        q,r = divmod(self,other)
        return q
    
    def __mod__(self,other,/):
        """
        Return self%other
        """
        q,r = divmod(self,other)
        return r

    def _refreshInt(self,/):
        """
        Recompute self.integerValue
        """
        self.integerValue = self._computeValue()
        return self.integerValue

    def __int__(self,/):
        """
        Return self.integerValue
        """
        try:
            return self.integerValue
        except:
            self.integerValue = self._computeValue()
            return self.integerValue

    def _computeValue(self,vector=None):
        """
        Computes the integer value corresponding to the
        polarised, respectively valued, Bachet vector.
        """
        if vector is None:
            vector = self.vector
        value = 0
        nv = len(vector)
        base3Power = 1   # 3**0
        for i in range(nv):
            value += base3Power*vector[nv-i-1]
            base3Power *= 3 # 3**i
        return value

    def __float__(self,/):
        """
        Return float(self)
        """
        return float(int(self))   

    def __len__(self,/):
        """
        Return the length of the BachetNumber vector attribute
        """
        return len(self.vector)

    def reverse(self, /):
        """
        Reverse the Bachet vector. ! Returns a modified BachetNumber object.
        """
        #from copy import deepcopy
        ln = len(self.vector)
        result = [0 for i in range(ln)]
        for i in range(ln):
            result[i] = self.vector[ln-i-1]
        rev = BachetVector(vector=result,length=ln)
        return rev

    def __invert__(self, /):
        """
        Return ~self
        """
        return self.reverse()
    def __abs__(self, /):
        """
        Defines the abs() operator for Bachet encoded numbers
        """
        ln = len(self.vector)
        if int(self) < 0:
            return -self
        else:
            return self

#-----   end of abstract Bachet number's base class    

class BachetVector(BachetNumber):
    """
    The class implements all arithmetic operations and comparison operators from the int class via the Bachet vectors.
    
    >>> from bachetNumbers import BachetVector
    >>> n1 = BachetVector(12)
    >>> n1
     *------- Bachet number description ------*
     Instance class : BachetVector
     String         : '+1+10'
     Vector         : [1, 1, 0]
     Length         : 3
     Value          : 12
     Attributes     : ['vector']  
    >>> n2 = BachetVector(vector=[1,1,1])
    >>> n2
     *------- Bachet number description ------*
     Instance class : BachetVector
     String         : '+1+1+1'
     Vector         : [1, 1, 1]
     Length         : 3
     Value          : 13
     Attributes     : ['vector']
    >>> n3 = n1 + n2
    >>> n3
     *------- Bachet number description ------*
     Instance class : BachetVector
     String         : '+10-1+1'
     Vector         : [1, 0, -1, 1]
     Length         : 4
     Value          : 25
     Attributes     : ['vector']
    >>> print('%s (%d) + %s (%d) = %s (%d)'
    ...        % (n1, int(n1), n2, int(n2), n3, int(n3) ))
     '+1+10' (12) + '+1+1+1' (13) = 10-11 (25)
    >>> print('length of %s = %d' % (n1, len(n1)))
     length of '+1+10' = 3
    >>> n4 = n1.reverse() # n4 = ~n1
    >>> n5 = -n2
    >>> n6 = n4 + n5   # n6 = n4 + (-n2) = n4 - n2
    >>> print('%s (%d) + %s (%d) = %s (%d)'
    ...       % ( n4, int(n4), n5, int(n5),n6, int(n6) ) )
     '0+1+1' (4) + '-1-1-1' (-13) = '-100' (-9)

    """
    
    def __init__(self,/,num_int=None,vector=None,length=1):
        """
        Tranforms a potentially signed integer into a Bachet number.
        Returns [0] when no arguments are given. 
        """
        
        if num_int is None:
            if vector is not None:
                value = self._computeValue(vector)
                num_int = int(value)
                self.integerValue = num_int
                if num_int != value:
                    self.decimalValue = value
                    self.decimalVector = vector
                ln = len(vector)
                b = BachetVector(num_int,length=ln)
                vl = len(b.vector)
                if vl >= length:
                    self.vector = b.vector
                else:
                    nz = length - vl
                    zvector = [0 for i in range(nz)]
                    self.vector = zvector + b.vector
            else:
                self.vector=[0 for i in range(length)]
        else:
            self.integerValue = num_int
            self.vector = self._int2bachet(num_int)
            vl = len(self.vector)
            if vl < length:
                nz = length - vl
                vector = [0 for i in range(nz)]
                self.vector = vector + self.vector

            
    # ---- vector-wise arithmetic operators
            
    def __add__(self,other,/,Debug=False):
        """
        Defines the balanced ternary addition operator
        for Bachet encoded numbers.
        """
        from copy import deepcopy
        srv = self.reverse()
        orv = other.reverse()
        n1 = len(self)
        n2 = len(other)
        if n1 >= n2:
            vector = [0 for i in range(n1)]
        else:
            vector = [0 for i in range(n2)]
        n = max(n1,n2)
        reste = 0
        for i in range(n):
            try:
                psi = srv.vector[i]
            except:
                psi = 0
            try:
                poi = orv.vector[i]
            except:
                poi = 0
            pi = psi + poi + reste
            if Debug:
                print('i,psi,poi,reste,pi', i,psi,poi,reste,pi)
            if pi == 2:
                vector[i] = -1
                reste = 1
            elif pi == 3:
                vector[i] = 0
                reste = 1
            elif pi == -2:
                vector[i] = 1
                reste = -1
            elif pi == -3:
                vector[i] = 0
                reste = -1
            else:
                vector[i] = pi
                reste = 0
            if Debug:
                print("reste",reste)
        if reste != 0:
            if Debug:
                print('add',reste)
            vector = vector + [reste]
        if Debug:
            print(vector)
        new = ~(BachetVector(vector=vector,length=n))
        return new

    def __eq__(self,other, /):
        """
        Return the self==other value
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [o for i in range(abs(nz))]
            #for i in range(abs(nz)):
            #    vector = vector + [1]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            #for i in range(nz):
            #    vector += [1]
            v2 = vector + v2
        return v1==v2

    def __ge__(self,other, /):
        """
        Return self>=other
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [0 for i in range(abs(nz))]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            v2 = vector + v2
        return v1 >= v2

    def __gt__(self,other, /):
        """
        Return self>other
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [0 for i in range(abs(nz))]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            v2 = vector + v2
        return v1>v2

    def __le__(self,other, /):
        """
        Return self<=other
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [0 for i in range(abs(nz))]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            v2 = vector + v2
        return v1<=v2

    def __lt__(self,other, /):
        """
        Return self>other
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [0 for i in range(abs(nz))]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            v2 = vector + v2
        return v1<v2
    
    def __ne__(self,other, /):
        """
        Return self!=other
        """
        v1 = list(self.vector)
        v2 = list(other.vector)
        nz = len(v1) - len(v2)
        if nz < 0:
            vector = [0 for i in range(abs(nz))]
            v1 = vector + v1
        elif nz > 0:
            vector = [0 for i in range(nz)]
            v2 = vector + v2
        return v1!=v2
            
    def _vdivmod(self,other,Debug=False,/):
        """
        Return q,r = divmod(self,other) computed Bachet vector-wise

        The quotient q search starts from 0 and is recursively incremented
        by base 3 powers until a fix-point remainder r value is attained. 
        
        """
        if int(other) == 0:
            print('Error: Dividend must not be zero')
            return None,None
        n = abs(BachetVector(vector=self.vector))
        q = abs(BachetVector(vector=[1]))
        aOther = abs(other)
        ri = n - (q*aOther)
        rj = BachetVector()
        j = 0
        if Debug:
            print(j,int(n),int(q),int(q*aOther),int(ri))
        while ri > rj:
            ri = n - (q * aOther)
            ivector = [1]
            i = 0
            while (q * aOther) <= n:
                ivector.append(0)
                q = q + BachetVector(vector=ivector)
                i += 1
            q = q - BachetVector(vector=ivector)
            j += 1          
            rj = n - (q * aOther)
            if Debug:
                print(j,int(n),int(q),int(aOther),int(q*aOther),int(rj))
        while (q * aOther) <= n:
            if Debug:
                print('*', end='')
            q = q + BachetVector(vector=[1])
        if Debug:
            print()        
        if int(self) >= 0 and int(other) >= 0:
            q = q - BachetVector(vector=[1])
            r = n - q * aOther
            return q,r
        elif int(self) < 0 and int(other) < 0:
            q = q - BachetVector(vector=[1])
            r = n - q*aOther
            return q,-r
        elif int(self) < 0 and int(other) > 0:
            r = n - (q * aOther)
            return -q,-r
        elif int(self) > 0 and int(other) < 0:
            r = n - (q * aOther)
            return -q,r
        
    def __divmod__(self,other, /):
        """
        Return BachetNumber(q),BachetNumber(r) where q,r = divmod(int(self),int(other))
        """
        q,r = self._vdivmod(other)
        return q,r
  
    def __mul__(self,other,Debug=False):
        """
        Return self*other computed vectorwise
        KNUTH D. Seminumerical Algorithmas Vol2 3Ed.
        Addison-Wesley 1998 ISBN 0-201-89684-2 p.2008
        """
        n = len(other)
        otherReverse = ~other
        res = BachetInteger()
        for i in range(n):
            ivector = self.vector + [0 for j in range(i)]
            if Debug:
                print(i,ivector,otherReverse.vector[i])
            if otherReverse.vector[i] == -1:
                res = res - BachetInteger(vector=ivector)
            elif otherReverse.vector[i] == 1:
                res = res + BachetInteger(vector=ivector)
            if Debug:
                print(res)
        return res
        

#------------- end of BachetVector class ------------------
    
class BachetInteger(BachetNumber):
    """
    The class implements by integer value all the arithmetic operations
    and comparison operators from the int class.
    This class is faster then the BachetVector class with very large integers. 
    
    >>> from bachetNumbers import BachetInteger
    >>> n1 = BachetInteger(12)
    >>> n1
     *------- Bachet Integer description ------*
     Instance class : BachetInteger
     String         : '+1+10'
     Vector         : [1, 1, 0]
     Length         : 3
     Value          : 12
     Attributes     : ['vector']  
    >>> n2 = BachetInteger(vector=[1,1,1])
    >>> n2
     *------- Bachet Integer description ------*
     Instance class : BachetInteger
     String         : '+1+1+1'
     Vector         : [1, 1, 1]
     Length         : 3
     Value          : 13
     Attributes     : ['vector']
    >>> n3 = n1 + n2
    >>> n3
     *------- Bachet number description ------*
     Instance class : BachetInteger
     String         : '+10-1+1'
     Vector         : [1, 0, -1, 1]
     Length         : 4
     Value          : 25
     Attributes     : ['vector']
    >>> print('%s (%d) + %s (%d) = %s (%d)'
    ...        % (n1, int(n1), n2, int(n2), n3, int(n3) ))
     '+1+10' (12) + '+1+1+1' (13) = 10-11 (25)
    >>> print('length of %s = %d' % (n1, len(n1)))
     length of '+1+10' = 3
    >>> n4 = n1.reverse() # n4 = ~n1
    >>> n5 = -n2
    >>> n6 = n4 + n5   # n6 = n4 + (-n2) = n4 - n2
    >>> print('%s (%d) + %s (%d) = %s (%d)'
    ...       % ( n4, int(n4), n5, int(n5),n6, int(n6) ) )
     '0+1+1' (4) + '-1-1-1' (-13) = '-100' (-9)

    """
    
    def __init__(self,/,num_int=None,vector=None,length=1):
        """
        Tranforms a potentially signed integer into a Bachet number.
        Returns [0] when no arguments are given. 
        """
        if num_int is None:
            if vector is not None:
                value = self._computeValue(vector)
                num_int = int(value)
                self.integerValue = num_int
                if num_int != value:
                    self.decimalValue = value
                    self.decimalVector = vector
                ln = len(vector)
                b = BachetInteger(num_int,length=ln)
                vl = len(b.vector)
                if vl >= length:
                    self.vector = b.vector
                else:
                    nz = length - vl
                    zvector = [0 for i in range(nz)]
                    self.vector = zvector + b.vector
            else:
                self.vector=[0 for i in range(length)]
        else:
            self.vector = self._int2bachet(num_int)
            vl = len(self.vector)
            if vl < length:
                nz = length - vl
                vector = [0 for i in range(nz)]
                self.vector = vector + self.vector
            
    # ---- arithmetic operations based on int() transforms
            
    def __abs__(self, /):
        """
        Defines the addition operator for Bachet encoded numbers
        """
        #ln = len(self.vector)
        v1 = int(self)
        v2 = abs(v1)
        return BachetInteger(v2)        

    def __add__(self,other,/):
        """
        Defines the balanced ternary addition operator for Bachet encoded numbers.
        """
        v1 = int(self)
        v2 = int(other)
        v3 = v1 + v2
        return BachetInteger(v3)

    def __radd__(self,other,/):
        """
        Defines the balanced ternary addition operator for Bachet encoded numbers.
        """
        v1 = int(other)
        v2 = int(self)
        v3 = v1 + v2
        return BachetInteger(v3)

    def __eq__(self,other, /):
        """
        Return the self==other value
        """
        v1 = int(self)
        v2 = int(other)
        return v1==v2

    def __ge__(self,other, /):
        """
        Return self>=other
        """
        v1 = int(self)
        v2 = int(other)
        return v1 >= v2

    def __gt__(self,other, /):
        """
        Return self>other
        """
        v1 = int(self)
        v2 = int(other)
        return v1>v2

    def __le__(self,other, /):
        """
        Return self<=other
        """
        v1 = int(self)
        v2 = int(other)
        return v1<=v2

    def __lt__(self,other, /):
        """
        Return self>other
        """
        v1 = int(self)
        v2 = int(other)
        return v1<v2
    
    def __ne__(self,other, /):
        """
        Return self!=other
        """
        v1 = int(self)
        v2 = int(other)
        return v1!=v2

    def __mul__(self,other,/):
        """
        Defines the multiplication operator via int() transforms
        """
        #ln = max(len(self),len(other))
        n1 = int(self)
        n2 = int(other)
        n3 = n1 * n2
        return BachetInteger(n3)
    
###############################
if __name__ == '__main__':
    print("""
    ****************************************************
    * Digraph3 bachetNumbers module                    *
    * Revision: Python3.12.8                            *
    * Copyright (C) 2025      Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    ######  scratch pad for testing the module components
    from bachetNumbers import BachetVector as BachetNumber
    print('*-----Computing with BachetInteger numbers----------*') 
    n1 = BachetNumber(12)
    n2 = BachetNumber(154)
    n3 = n1 + n2
    n4 = n1 * n2
    print('\'%s\' (%d) + \'%s\' (%d) = \'%s\' (%d)' % (n1, int(n1), n2, int(n2), n3, int(n3) ))
    print('\'%s\' (%d) * \'%s\' (%d) = \'%s\' (%d)' % (n1, int(n1), n2, int(n2), n4, int(n4) ))

    n5 = n1.reverse()
    n6 = -n1
    print('\'%s\' (%d) + \'%s\' (%d) = \'%s\' (%d)' % ( n5, int(n5), n6, int(n6),
                                                       (n5 + n6), int(n5+n6) ))
    from bachetNumbers import BachetVector as BachetNumber
    print('*-----Computing with BachetVector numbers----------*') 
    n1 = BachetNumber(12)
    n2 = BachetNumber(154)
    n3 = n1 + n2
    n4 = n1 * n2
    print('\'%s\' (%d) + \'%s\' (%d) = \'%s\' (%d)' % (n1, int(n1), n2, int(n2), n3, int(n3) ))
    print('\'%s\' (%d) * \'%s\' (%d) = \'%s\' (%d)' % (n1, int(n1), n2, int(n2), n4, int(n4) ))

    n5 = n1.reverse()
    n6 = -n1
    print('\'%s\' (%d) + \'%s\' (%d) = \'%s\' (%d)' % ( n5, int(n5), n6, int(n6),
                                                       (n5 + n6), int(n5+n6) ))

    ## timings
    print('Timings: int(Bachet), Bachet.vector and inbuilt integers')
    from random import shuffle
    from time import time

    bi = BachetInteger(0)
    t0 = time()
    for s in range(10000,20000):
        bi = bi + BachetInteger(s)
    print('addbi: ',bi,', ',int(bi));print(time() - t0)
    bv = BachetVector(0)
    t0 = time()
    for s in range(10000,20000):
        bv = bv + BachetVector(s)
    print('addbv: ',bv,', ',int(bv));print(time() - t0)
    i = 0
    t0 = time()
    for s in range(10000,20000):
        i += s
    print('addint: ',i);print(time() - t0)

    ## vectormul
    b1 = BachetVector(12)
    b2 = BachetVector(24)
    res = b1*b2
    print(res,int(res))
    b1 = BachetInteger(12)
    b2 = BachetInteger(24)
    res = b1*b2
    print(res,int(res))

    ## vectordivide
    n = BachetVector(vector=[1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[1,-1,-1,1])
    q,r = divmod(n,d)
    print('1) %d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('1) %d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    n = BachetVector(vector=[-1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[1,-1,-1,1])
    q,r = divmod(n,d)
    print('2)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('2)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    n = BachetVector(vector=[1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[-1,-1,-1,1])
    q,r = divmod(n,d)
    print('3)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('3)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    n = BachetVector(vector=[-1,1,1,1,1,1,1,1])
    d = BachetVector(vector=[-1,-1,-1,1])
    q,r = divmod(n,d)
    print('4)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) ) 
    q,r = divmod(int(n),int(d))
    print('4)%d / %d = %d rest %d' % (int(n), int(d), int(q), int(r)) )

    ## miscellaneous opertions
    print('n = \'%s\' = %d' % (str(n), int(n)) )
    print('abs(%d) = %d' % ( int(n), int(abs(n)) ) )
    print('sign of %d = %d' % ( int(n),n.sign() ) )
    print('sign of %d = %d' % ( int(-n),(-n).sign() ) )
    print('sign of %d = %d' % ( int(BachetVector()), BachetVector().sign() ) )
    print('abs(%d) = %d' % ( int(BachetVector()), BachetVector().sign() ) )
    
    #############
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    
    
#####################################
