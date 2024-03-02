#!/Usr/bin/env python3
#########################
"""
Root module of the Digraph3 resources for Python CUDA. Requires a CUDA enabled NVIDIA Graphic device and Python numpy and numba modules installed.

The double dictionanry relation[x][y] is replaced with a 2 dmensional numpy array valuation[i,j] with indexes i,j in range of self.order.

Copyright (C) 2006-2023  Raymond Bisdorff

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
#######################
from digraphs import Digraph 
import numpy as np

class CudaDigraph(Digraph):
    """
    Implementation of bipolar integer-valued digraphs taking advantage of an CUDA enabled NIVIDA GPU.
    Input parameter is a *Digraph* object. The *relation* dictionaray is replaced with an integer vaued *numpy array* called *valuation*
    """ 
    def __init__(self,digraph):
        from copy import deepcopy
        att = [a for a in digraph.__dict__]
        att.remove('name')
        att.remove('relation')
        for a in att:
            self.__dict__[a] = deepcopy(digraph.__dict__[a])
        self.name = 'cuda' + digraph.name
        self.order = len(self.actions)
        #relation = deepcopy(digraph.relation)
        valuation = np.zeros((self.order,self.order),dtype=int)
        actionsList = [x for x in self.actions]
        order = self.order
        for i in range(order):
            x = actionsList[i]
            for j in range(self.order):
                y = actionsList[j]
                valuation[i,j] = digraph.relation[x][y]
        self.valuation = valuation
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def __repr__(self):
        """
        Default presentation method for Digraph instances.
        """
        reprString = '*------- CudaDigraph instance description ------*\n'
        reprString += 'Instance class      : %s\n' % self.__class__.__name__
        reprString += 'Instance name       : %s\n' % self.name
        reprString += 'Digraph Order       : %d\n' % self.order
        reprString += 'Digraph Size        : %d\n' % self.computeSize()
        reprString += 'Valuation domain    : [%.2f;%.2f]\n'\
                      % (self.valuationdomain['min'],self.valuationdomain['max'])
        #reprString += 'Determinateness (%%) : %.2f\n' % self.computeDeterminateness(InPercents=True)
        reprString += 'Attributes          : %s\n' % list(self.__dict__.keys())
       
        return reprString

    def __neg__(self):
        """
        Make the negation operator -self available for Digraph instances. 

        Returns a DualDigraph instance of self.
        """
        new = DualCudaDigraph(self)
        new.__class__ = self.__class__
        return new

    def __invert__(self):
        """
        Make the inverting operator ~self available for Digraph instances. 

        Returns a ConverseDigraph instance of self.
        """
        new = ConverseCudaDigraph(self)
        new.__class__ = self.__class__
        return new

    def gammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the dominated, and set *ax* gathering
        the absorbed neighborhood.

        """
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        order = self.order
        valuation = self.valuation
        gamma = {}
        for i in range(order):
            x = actionsList[i]
            dx = set()
            ax = set()
            for j in range(order):
                y = actionsList[j]
                if x != y:
                    if valuation[i,j] > Med:
                        dx.add(y)
                    if valuation[j,i] > Med:
                        ax.add(y)
            gamma[x] = (dx,ax)
        return gamma

    def notGammaSets(self):
        """
        Renders the dictionary of neighborhoods {node: (dx,ax)}
        with set *dx* gathering the not dominated, and set *ax* gathering
        the not absorbed neighborhood.

        """
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        order = self.order
        valuation  = self.valuation
        notGamma = {}
        for i in range(order):
            x = actionsList[i]
            dx = set()
            ax = set()
            for j in range(order):
                y = actionsList[j]
                if x != y:
                    if valuation[i,j] < Med:
                        dx.add(y)
                    if valuation[j,i] < Med:
                        ax.add(y)
            notGamma[x] = (dx,ax)
        return notGamma

    def computeSize(self):
        """
        Renders the number of validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        order = self.order
        valuation = self.valuation
        size = 0
        for i in range(order):
            for j in range(i+1,order):
                if valuation[i,j] > Med:
                    size += 1
                if valuation[j,i] > Med:
                    size += 1
        return size

    def computeCoSize(self):
        """
        Renders the number of non validated non reflexive arcs
        """
        Med = self.valuationdomain['med']
        actionsList = [x for x in self.actions]
        valuation = self.valuation
        order = self.order
        coSize = 0
        for i in range(order):
            for j in range(i+1,order):
                if valuation[i,j] < Med:
                    coSize += 1
                if valuation[j,i] < Med:
                    coSize += 1
        return coSize

    def computeDeterminateness(self,InPercents=False):
        """
        Computes the Kendalll distance of self
        with the all median-valued indeterminate digraph of order n.
        """
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        valuation = self.valuation
        actionsList = [x for x in self.actions]
        order = self.order
        D = Decimal('0.0')
        for i in range(order):
            for j in range(i+1,order):
                D += abs(valuation[i,j] - Med)
                D += abs(valuation[j,i] -Med )
        if order > 1:
            determination = D / Decimal(str((order * (order-1))))
        else:
            determination = D
        if InPercents:
            return ( (determination / (Max-Med)) + Decimal('1.0')) / Decimal('2.0') * Decimal('100.0')
        else:
            return determination

#-----------------------
class DualCudaDigraph(CudaDigraph):
    """
    Instantiates the dual ( = negated valuation) CudaDigraph object from a
    deep copy of a given other CudaDigraph instance.

    The relation constructor returns the dual (negation) of
    self.valuation 
    
    .. note::

        In a bipolar valuation, the dual operator corresponds to a simple changing of signs.


    """
    def __init__(self,other,Cuda=False):
        from time import time
        if Cuda:
            import numpy as np
            from numba import cuda
            import math
            @cuda.jit
            def negate(a,b):
                tx,ty = cuda.grid(2)
                size = len(b)
                if tx < a.shape[0] and ty < a.shape[1]:
                    b[tx,ty] = -a[tx,ty]
                    
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'dual-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])
        if Cuda:
            t0 = time()
            ad = cuda.to_device(other.valuation)
            bd = cuda.to_device(np.zeros([self.order,self.order]))
            threadsperblock = (32, 32)
            blockspergrid_x = math.ceil(bd.shape[0] / threadsperblock[0])
            blockspergrid_y = math.ceil(bd.shape[1] / threadsperblock[1])
            blockspergrid = (blockspergrid_x, blockspergrid_y)
            negate[blockspergrid, threadsperblock](ad,bd)
            self.valuation = bd.copy_to_host()
            print('Cuda time:', time()-t0)
        else:
            t0 = time()
            self.valuation = -other.valuation
            print('Numpy time:',time()-t0)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class ConverseCudaDigraph(CudaDigraph):
    """
    Instantiates the converse ( = transposed valuation) CudaDigraph object from a
    deep copy of a given other CudaDigraph instance.

    The relation constructor returns the inverse (transposition) of
    self.valuation 
    
    .. note::

        In a bipolar valuation, the inverse operator corresponds to a transpose of the adjacency table.


    """
    def __init__(self,other,Cuda=False):
        from time import time
        
        if Cuda:
            import numpy as np
            from numba import cuda
            import math
            @cuda.jit
            def invert(a,b):
                tx,ty = cuda.grid(2)
                size = len(b)
                if tx < a.shape[0] and ty < a.shape[1]:
                    b[tx,ty] = a[ty,tx]
                    
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'converse-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])

        if Cuda:
            t0 = time()
            ad = cuda.to_device(other.valuation)
            bd = cuda.to_device(np.zeros([self.order,self.order]))
            threadsperblock = (32, 32)
            blockspergrid_x = math.ceil(bd.shape[0] / threadsperblock[0])
            blockspergrid_y = math.ceil(bd.shape[1] / threadsperblock[1])
            blockspergrid = (blockspergrid_x, blockspergrid_y)
            invert[blockspergrid, threadsperblock](ad,bd)
            self.valuation = bd.copy_to_host()
            print('Cuda time:', time()-t0)
        else:
            t0 = time()
            self.valuation = other.valuation.transpose()       
            print('Numpy time:', time()-t0)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

class CoDualCudaDigraph(CudaDigraph):
    """
    Instantiates the codual ( = negated and transposed valuation) CudaDigraph object from a
    deep copy of a given other CudaDigraph instance.

    The relation constructor returns the codual of
    self.valuation 

    """
    def __init__(self,other,Cuda=False):
        from time import time
        
        if Cuda:
            import numpy as np
            from numba import cuda
            import math
            @cuda.jit
            def codual(a,b):
                tx,ty = cuda.grid(2)
                size = len(b)
                if tx < a.shape[0] and ty < a.shape[1]:
                    b[tx,ty] = -a[ty,tx]
                    
        from copy import deepcopy
        self.__class__ = other.__class__
        self.name = 'codual-' + str(other.name)
        att = [a for a in other.__dict__]
        att.remove('name')
        att.remove('valuation')
        for a in att:
            self.__dict__[a] = deepcopy(other.__dict__[a])

        if Cuda:
            t0 = time()
            ad = cuda.to_device(other.valuation)
            bd = cuda.to_device(np.zeros([self.order,self.order]))
            threadsperblock = (32, 32)
            blockspergrid_x = math.ceil(bd.shape[0] / threadsperblock[0])
            blockspergrid_y = math.ceil(bd.shape[1] / threadsperblock[1])
            blockspergrid = (blockspergrid_x, blockspergrid_y)
            codual[blockspergrid, threadsperblock](ad,bd)
            self.valuation = bd.copy_to_host()
            print('Cuda time:', time()-t0)
        else:
            t0 = time()
            self.valuation = -other.valuation.transpose()       
            print('Numpy time:', time()-t0)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


#############################################
# scratch space for testing ongoing developments
#----------test Digraph class ----------------
if __name__ == "__main__":

    print('*****************************************************')
    print('* Python digraphs module                            *')
    print('* $Revision: Python3.11 $                           *')
    print('* Copyright (C) 2024  Raymond Bisdorff              *')
    print('* The module comes with ABSOLUTELY NO WARRANTY      *')
    print('* to the extent permitted by the applicable law.    *')
    print('* This is free software, and you are welcome to     *')
    print('* redistribute it if it remains free software.      *')
    print('*****************************************************')

    print('*-------- Testing classes and methods -------')
    from cudaDigraphs import *
    from cRandPerfTabs import *
    from time import time
    pt = cRandomPerformanceTableau(numberOfActions=3000,seed=10)
    from cIntegerOutrankingDigraphs import *
    ig = IntegerBipolarOutrankingDigraph(pt,Threading=True)
    print(ig)
    t0 = time()
    cdig = ~(-ig)
    print(cdig)
    print('CoDualDigraph time',time()-t0)
    cd = CudaDigraph(ig)
    #print(cd)
    #dg = DualCudaDigraph(cd,Cuda=False)
    #print(dg)
    #dg = DualCudaDigraph(cd,Cuda=True)
    #print(dg)
    #invd = ConverseCudaDigraph(cd,Cuda=False)
    #print(invd)
    #invd = ConverseCudaDigraph(cd,Cuda=True)
    #print(invd)
    cdd = CoDualCudaDigraph(cd,Cuda=False)
    print(cdd)
    cdd = CoDualCudaDigraph(cd,Cuda=True)
    print(cdd)
    
    #print(cd.computeCoSize())
    #cd.showNeighborhoods()
##    from digraphs import *
##    g = RandomValuationDigraph()
##    g.save('testgDigraph')

    
