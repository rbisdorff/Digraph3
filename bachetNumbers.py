#!/Usr/bin/env python3
"""
Python3+ implementation of bipolar-valued base 3 integers.

Two versions are provided:

    - the *BachetInteger* class (default) based on the int() values of the Bachet numbers 

    - the *BachetVector* class based on the balanced ternary vectors,

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

def toDecimal(self,/):
    """
    Return Decimal(int(self))
    """
    return Decimal(int(self))

class BachetVector(object):
    """
    Bipolar-valued {-1,0,+1} base 3 encoded integers due to Claude Gaspard Bachet de Méziriac (1621)
    
    https://en.wikipedia.org/wiki/Claude_Gaspar_Bachet_de_M%C3%A9ziriac

    The class implements all arithmetic operations and comparison operators from the int class via the Bachet vectors.
    
    >>> from bachetNumbers import BachetVector as BachetNumber
    >>> n1 = BachetNumber(12)
    >>> n1
     *------- Bachet number description ------*
     Instance class : BachetNumber
     String         : '+1+10'
     Vector         : [1, 1, 0]
     Length         : 3
     Value          : 12
     Attributes     : ['vector']  
    >>> n2 = BachetNumber(vector=[1,1,1])
    >>> n2
     *------- Bachet number description ------*
     Instance class : BachetNumber
     String         : '+1+1+1'
     Vector         : [1, 1, 1]
     Length         : 3
     Value          : 13
     Attributes     : ['vector']
    >>> n3 = n1 + n2
    >>> n3
     *------- Bachet number description ------*
     Instance class : BachetNumber
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
    def __repr__(self):
        """
        Default presentation method for Bchet number instances.
        """
        reprString = '*------- Bachet number description ------*\n'
        reprString += 'Instance class : %s\n' % self.__class__.__name__
        reprString += 'String         : \'%s\'\n' % str(self)
        reprString += 'Vector         : %s\n' % self.vector
        reprString += 'Length         : %d\n' % len(self)
        reprString += 'Value          : %d\n' % int(self)
        reprString += 'Attributes     : %s\n' % list(self.__dict__.keys())    
        return reprString
    
    def __init__(self,num_int=None,vector=None,length=1):
        """
        Tranforms a potentially signed integer into a Bachet number.
        Returns [0] when no arguments are given. 
        """
        if num_int is None:
            if vector is not None:
                ln = len(vector)
                num_int = round(self._computeValue(vector))
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
            self.vector = self._int2bachet(num_int)
            vl = len(self.vector)
            if vl < length:
                nz = length - vl
                vector = [0 for i in range(nz)]
                self.vector = vector + self.vector

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

    def _int2bachet(self,num_int):
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
            
    # ---- arithmetic operations
    
    def __neg__(self, /):
        """
        Defines an unary negating operator for Bachet encoded numbers.
        """
        from copy import deepcopy
        negVector = []
        for i in range(len(self.vector)):
            negVector.append(self.vector[i] * -1)
        ln = len(self.vector)
        neg = BachetVector(vector = negVector,length=ln)
        return neg
        
    def __abs__(self, /):
        """
        Defines the addition operator for Bachet encoded numbers
        """
        ln = len(self.vector)
        v1 = int(self)
        v2 = abs(v1)
        return BachetVector(v2,length=ln)        

    def __add__(self,other,Debug=False):
        """
        Defines the balanced ternary addition operator for Bachet encoded numbers.
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

    def __sub__(self,other, /):
        """
        Return self-other
        """
        new = self + (-other)
        return new

    def __divmod__(self,other, /):
        """
        Return BachetNumber(q),BachetNumber(r) where q,r = divmod(int(self),int(other))
        """
        ln = max(len(self),len(other))
        q,r = divmod(int(self),int(other))
        return BachetVector(q,length=ln),BachetVector(r,length=ln)

    def __floordiv__(self,other,/):
        ln = max(len(self),len(other))
        q = int(self)//int(other)
        return BachetVector(q,length=ln)
  
    def __mul__(self,other,/):
        """
        Defines the multiplication operator for Bachet encoded numbers.
        """
        ln = max(len(self),len(other))
        n1 = int(self)
        n2 = int(other)
        n3 = n1 * n2
        return BachetVector(n3,length=ln)

    def __int__(self, /):
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

    def __len__(self):
        """
        Return the length of the BachetNumber vector attribute
        """
        return len(self.vector)

    def reverse(self):
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

    def __mod__(self, other, /):
        """
        Return self%other
        """
        v1 = int(self)
        v2 = int(other)
        v3 = v1%v2
        return BachetVector(v3)

#------------- end of BachetNumber class ------------------
    
class BachetInteger(object):
    """
    Bipolar-valued {-1,0,+1} base 3 encoded integers due to Claude Gaspard Bachet de Méziriac (1621)
    
    https://en.wikipedia.org/wiki/Claude_Gaspar_Bachet_de_M%C3%A9ziriac

    The class implements by integer value all the arithmetic operations and comparison operators from the int class.
    
    >>> from bachetNumbers import BachetInteger as BachetNumber
    >>> n1 = BachetInteger(12)
    >>> n1
     *------- Bachet Integer description ------*
     Instance class : BachetNumber
     String         : '+1+10'
     Vector         : [1, 1, 0]
     Length         : 3
     Value          : 12
     Attributes     : ['vector']  
    >>> n2 = BachetNumber(vector=[1,1,1])
    >>> n2
     *------- Bachet Integer description ------*
     Instance class : BachetNumber
     String         : '+1+1+1'
     Vector         : [1, 1, 1]
     Length         : 3
     Value          : 13
     Attributes     : ['vector']
    >>> n3 = n1 + n2
    >>> n3
     *------- Bachet number description ------*
     Instance class : BachetNumber
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
    def __repr__(self):
        """
        Default presentation method for Bchet number instances.
        """
        reprString = '*------- Bachet number description ------*\n'
        reprString += 'Instance class : %s\n' % self.__class__.__name__
        reprString += 'String         : \'%s\'\n' % str(self)
        reprString += 'Vector         : %s\n' % self.vector
        reprString += 'Length         : %d\n' % len(self)
        reprString += 'Value          : %d\n' % int(self)
        reprString += 'Attributes     : %s\n' % list(self.__dict__.keys())    
        return reprString
    
    def __init__(self,num_int=None,vector=None,length=1):
        """
        Tranforms a potentially signed integer into a Bachet number.
        Returns [0] when no arguments are given. 
        """
        if num_int is None:
            if vector is not None:
                ln = len(vector)
                num_int = round(self._computeValue(vector))
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

    def _int2bachet(self,num_int):
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
            
    # ---- arithmetic operations
    
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
        
    def __abs__(self, /):
        """
        Defines the addition operator for Bachet encoded numbers
        """
        #ln = len(self.vector)
        v1 = int(self)
        v2 = abs(v1)
        return BachetInteger(v2)        

    def __add__(self,other):
        """
        Defines the balanced ternary addition operator for Bachet encoded numbers.
        """
        v1 = int(self)
        v2 = int(other)
        v3 = v1 + v2
        return BachetInteger(v3)
    def __radd__(self,other):
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
        v1 = int(v1)
        v2 = int(v2)
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

    def __divmod__(self,other, /):
        """
        Return BachetNumber(q),BachetNumber(r) where q,r = divmod(int(self),int(other))
        """
        #ln = max(len(self),len(other))
        q,r = divmod(int(self),int(other))
        return BachetInteger(q),BachetInteger(r)

    def __floordiv__(self,other,/):
        #ln = max(len(self),len(other))
        q = int(self)//int(other)
        return BachetInteger(q)
  
    def __mul__(self,other,/):
        """
        Defines the multiplication operator for Bachet encoded numbers.
        """
        #ln = max(len(self),len(other))
        n1 = int(self)
        n2 = int(other)
        n3 = n1 * n2
        return BachetInteger(n3)

    def __int__(self, /):
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
    def __len__(self):
        """
        Return the length of the BachetNumber vector attribute
        """
        return len(self.vector)

    def reverse(self):
        """
        Reverse the Bachet vector. ! Returns a modified BachetNumber object.
        """
        #from copy import deepcopy
        ln = len(self.vector)
        result = [0 for i in range(ln)]
        for i in range(ln):
            result[i] = self.vector[ln-i-1]
        rev = BachetInteger(vector=result,length=ln)
        return rev

    def __invert__(self, /):
        """
        Return ~self
        """
        return self.reverse()

    def __mod__(self, other, /):
        """
        Return self%other
        """
        v1 = int(self)
        v2 = int(other)
        v3 = v1%v2
        return BachetInteger(v3)
    
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
    print('*-----Computing with Bachet numbers----------*') 
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
  
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    ## timings
    from random import shuffle
    from time import time

    bi = BachetInteger(0)
    t0 = time()
    for s in range(1000):
        bi = bi + BachetInteger(s)
    
    print('addbi');print(time() - t0)
    bv = BachetNumber(0)
    t0 = time()
    for s in range(1000):
        bv = bv + BachetNumber(s)
    print('addbv');print(time() - t0)
    
    
#####################################
