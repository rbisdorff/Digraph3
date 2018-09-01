#!/usr/bin/env python3
"""
Python3+ implementation of random number generators
Copyright (C) 2014-2018  Raymond Bisdorff

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

__version__ = "Branch: 3.6 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

class DiscreteRandomVariable():
    """
    Discrete random variable generator

    Parameters:
        | discreteLaw := dictionary with integer values
        |                as keys and probabilities as float values,
        | seed := integer for fixing the sequence generation.

    Example usage:
        >>> from randomNumbers import DiscreteRandomVariable
        >>> discreteLaw = {0:0.0478,
                           1:0.3349,
                           2:0.2392,
                           3:0.1435,
                           4:0.0957,
                           5:0.0670,
                           6:0.0478,
                           7:0.0096,
                           8:0.0096,
                           9:0.0048,}
        ## initialze the random generator
        >>> rdv = DiscreteRandomVariable(discreteLaw,seed=1)
        ## sample discrete random variable and
        ## count frequencies of obtained values
        >>> sampleSize = 1000
        >>> frequencies = {}
        >>> for i in range(sampleSize):
                x = rdv.random() 
                try:
                    frequencies[x] += 1
                except:
                    frequencies[x] = 1
        ## print results
        >>> results = [x for x in frequencies]
        >>> results.sort()
        >>> counts= 0.0
        >>> for x in results:
                counts += frequencies[x]
                print  ('%s, %d, %.3f, %.3f' % (x, frequencies[x],
                          float(frequencies[x])/float(sampleSize),
                          discreteLaw[x]))
        >>> print ('# of valid samples = %d' % counts)
    """
    
    def __init__(self, discreteLaw = None, seed = None, Debug=False):
        """
        constructor for discrete random variables with
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed != None:
            self._random.seed(self.seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print ('No seed is used')
            
        if discreteLaw != None:
            self.discreteLaw = discreteLaw
            self.F = self._cumulative()
        else:
            print('!!! Error: A discrete law is required here!')
        

    def _cumulative(self):
        """
        renders the cumulative probability distribution F(x)
        of self.discreteLaw
        """
        quantile = [x for x in self.discreteLaw]
        quantile.sort()
        F = []
        percentile = 0.0
        for i in range(len(quantile)):
            percentile += self.discreteLaw[quantile[i]]
            F.append((quantile[i],percentile))
        return F
    

    def random(self):
        """
        generating discrete random values from a discrete random variable.
        """
        frequencies = {}
    
        u = self._random.random()

        for i in range(len(self.F)):
            if u < self.F[i][1]:
                return self.F[i][0]

        return self.F[-1][0]
        
######################################

class ExtendedTriangularRandomVariable():
    """
    Extended triangular random variable generator

    Parameters:
        - mode := most frequently observed value
        - probRepart := probability mass distributed until the mode
        - seed := integer for fixing the sequence generation.

    .. image:: extTrDistribution.png
        :alt: Extended triangular distribution
        :width: 500 px
        :align: center

    """
    
    def __init__(self, lowLimit=0.0, highLimit = 1.0,
                 mode=None, probRepart=0.5, seed=None, Debug=False):
        """
        constructor for extended triangular random variables with
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed != None:
            self._random.seed(seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print('Default seed is used')
        self.m = lowLimit
        self.M = highLimit
            
        if mode == None:
            self.xm = (highLimit-lowLimit)/2.0
        else:
            if mode >= lowLimit and mode <= highLimit: 
                self.xm = mode
            else:
                print('!!! Error: mode out of value range !!')
        if probRepart == None:
            self.r = 0.5
        else:
            if probRepart >= 0.0 and probRepart <= 1.0:
                self.r = probRepart
            else:
                print('!!! Error: probility repartition out of value range !!')
            
        
    def random(self):
        """
        generating an extended triangular random number.
        """
        
        from math import sqrt
        u = self._random.random()

        if u < self.r:
            randeval = self.m + sqrt(u/self.r)*(self.xm-self.m)                   
        else:
            randeval = self.M - sqrt((1-u)/(1-self.r))*(self.M-self.xm)

        return randeval

#-------------------
                  
class CauchyRandomVariable():
    """
    Cauchy random variable generator.

    Parameters:
        - position := median (default=0.0) of the Cauchy distribution
        - scale := typical spread (default=1.0) with respect to median 
        - seed := integer (default=None) for fixing the sequence generation.
    
    Cauchy quantile (inverse cdf) function:
        Q(x|position,scale) = position + scale*tan[pi(x-1/2)]

    .. image:: cauchyDistribution.png
        :alt: Cauchy Distribution
        :width: 500 px
        :align: center


    """
    
    def __init__(self, position=0.0, scale = 1.0,
                 seed=None, Debug=False):
        """
        constructor for Cauchy random variables.
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed != None:
            self._random.seed(seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print('Default seed is used')
        self.position = position
        self.scale = scale            
        
    def random(self):
        """
        generating a Cauchy random number.
        """
        
        from math import pi,tan

        prob = self._random.random()

        randeval = self.position + self.scale*( tan( pi*(prob - 0.5) ) )                  

        return randeval
            
#----------
class QuasiRandomKorobovPointSet():
    """
    Constructor for rendering a Korobov point set of dimension *n* which is *fully projection regular* in the $s$-dimensional real-valued [0,1)^s hypercube. The constructor uses a MLCG generator with potentially a full period. The point set is stored in a self.sequence attribute and saved in a CSV formatted file.

    *Source*: Chr. Lemieux, Monte Carlo and quasi Monte Carlo Sampling Springer 2009 Fig. 5.12 p. 176.

    *Parameters*:

        * *n* : (default=997) number of Korobov points and modulus of the underlying MLCG
        * *s* : (default=3) dimension of the hypercube
        * *Randomized* : (default=False) the sequence is randomly shifted (mod 1) to avoid cycling when *s* > *n*
        * *a* : (default=383) MLCG coefficient (0 < *a* < *n*), primitive with *n*. The choice of *a* and *n* is crucial for getting an MLCG with full period and hence a fully projection-regular sequence. A second good pair is given with *n* = 1021 (prime) and *a* = 76.
        * *fileName*: (default='korobov') name -without the csv suffix- of the stored result. 

    Sample Python session:

        >>> from randomNumbers import QuasiRandomKorobovPointSet
        >>> kor = QuasiRandomKorobovPointSet(Debug=True)
        0 [0.0, 0.0, 0.0]
        1 [0.13536725313948247, 0.23158619430934912, 0.8941657924971758]
        2 [0.36595043842175035, 0.7415995294344084, 0.7035940773517395]
        3 [0.8759637735468097, 0.5510278142889722, 0.714627176649633]
        4 [0.6853920584013734, 0.5620609135868657, 0.9403042077429129]
        5 [0.6964251576992669, 0.7877379446801456, 0.3746071164690914]

    The resulting Korobov sequence may be inspected in an R session::

        > x = read.csv('korobov.csv')
        > x[1:5,]
        >    x1       x2       x3
        1 0.000000 0.000000 0.000000
        2 0.135367 0.231586 0.894166
        3 0.365950 0.741600 0.703594
        4 0.875964 0.551028 0.714627
        5 0.685392 0.562061 0.940304
        > library('lattice')
        > cloud(x$x3 ~ x$x1 + x$x2)
        > plot(x$x1,x$x2,pch='°')
        > plot(x$x1,x$x3,pch="°")

    .. image:: korobov3D.png
        :alt: Checking projection regularity
        :width: 500 px
        :align: center

    .. image:: korobovProjection12.png
        :alt: Checking projection regularity
        :width: 400 px
        :align: center

    .. image:: korobovProjection13.png
        :alt: Checking projection regularity
        :width: 400 px
        :align: center

    """
    
    def __init__(self,n=997, s=3, a=383, Randomized=False, seed=None,fileName='korobov',Debug=False):
        # storing parameters
        self.n = n
        self.s = s
        self.a = a
        self.Randomized = Randomized
        self.seed = seed
        self.fileName = fileName
        self.Debug = Debug
        # float casting
        nf = float(n)
        # randomization
        if Randomized:
            import random
            random.seed(seed)
            v = [random.random() for j in range(s)]
        # storing the simulated point set
        sequence = [] 
        fileName += '.csv'
        with open(fileName,'w') as fo:
            # csv header row
            wstr = ''
            for j in range(s-1):
                wstr += '"x%d",' % (j+1)
            wstr += '"x%d"\n' % (s)
            fo.write(wstr)
            # start point set at origin
            u = [0.0 for j in range(s)]
            sequence.append((tuple(u)))
            if Debug:
                print(0,u)
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[j-1]
            fo.write(wstr)
            # first s-dimensional point with a full period MLCG
            x = 1.0
            u[0] = x/nf
            for j in range(1,s):
                x = (divmod(a*x,n))[1]
                u[j] = x/nf
            if Randomized:
                for j in range(s):
                    z = u[j] + v[j]
                    u[j] = z - int(z)
            sequence.append((tuple(u)))
            if Debug:
                print(1,u)
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
            # all the following points
            for i in range(2,n):
                #shuffle(u)
                for j in range(s-1):
                    u[j] = u[j+1] # << 1
                x = (divmod(a*x,n))[1]
                u[s-1] = x/nf
                if Randomized:
                    for j in range(s):
                        z = u[j] + v[j]
                        u[j] = z - int(z)
                sequence.append((tuple(u)))
                if Debug:
                    print(i,u)
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        self.sequence = sequence

    def testFct(self,seq=None,buggyRegionLimits=(0.45,0.55)):
        """
        Tiny buggy hypercube for testing a quasi random Korobov 3D sequence.
        """
        s = self.s
        buggyHypercube = dict()
        for j in range(s):
            buggyHypercube[j] = buggyRegionLimits
        Bugs = 0
        if seq == None:
            seq = self.sequence
        for x in seq:
            for j in range(s):
                if (x[j] >= buggyHypercube[j][0] and x[j] <= buggyHypercube[j][1]):
                    BuggyPoint = True
                else:
                    BuggyPoint = False
                    break
            if BuggyPoint:
                print('Bug:', x, buggyHypercube)
                Bugs += 1
        if Bugs > 0:
            return '%d bug(s) detected !!!' % Bugs
        else:
            return 'No bugs detected'

#-------
class QuasiRandomFareyPointSet():
    """
    Constructor for rendering Farey series of dimension *s* and max denominateor *n* which is *fully projection regular* in the $s$-dimensional real-valued [0,1)^s hypercube. The lattice constructor uses a randomly shuffled Farey series for the point construction. The resulting point set is stored in a self.sequence attribute and saved in a CSV formatted file.

    *Parameters*:

        *n* : (default=20) maximal denominator of the Farey series
        *s* : (default=3) dimension of the hypercube
        *seed* : for regenrating the same Farey point set 
        * *Randomized* : (default=False) the points are randomly shifted (mod 1) to avoid cycling when *s* > *n*.
        * *fileName*: (default='farey') name -without the csv suffix- of the stored result. 

    Sample Python session:

        >>> from randomNumbers import QuasiRandomFareyPointSet
        >>> qrfs = QuasiRandomFareyPointSet(n=20,s=5,seed=100,
                                            fileName='testFarey')
        >>> print(qrfs.fareySeries[:10])
        [0.0, 0.05, 0.0526, 0.0555, 0.0588, 0.0625, 0.0666, 0.0714, 
         0.0769, 0.083333]
        >>> print(qrfs.pointSet[:10])
        [(0.8461, 0.0588, 0.0526, 0.1053, 0.6923), 
         (0.0588, 0.0526, 0.1053, 0.6923, 0.3636), 
         (0.0526, 0.1053, 0.6923, 0.3636, 0.0625), 
         (0.1053, 0.6923, 0.3636, 0.0625, 0.8500), 
         (0.6923, 0.3636, 0.0625, 0.8500, 0.7692),
         ...]
     
    The resulting point set may be inspected in an R session::

        > x = read.csv('testFarey.csv')
        > x[1:5,]
        >    x1       x2       x3       x4       x5
        1 0.846154 0.058824 0.052632 0.105263 0.692308
        2 0.058824 0.052632 0.105263 0.692308 0.363636
        3 0.052632 0.105263 0.692308 0.363636 0.062500
        4 0.105263 0.692308 0.363636 0.062500 0.850000
        5 0.692308 0.363636 0.062500 0.850000 0.769231
       > library('lattice')
        > cloud(x$x5 ~ x$x1 + x$x4)
        > plot(x$x3,x$x4) 

    .. image:: farey3D.png
        :alt: Checking projection regularity
        :width: 500 px
        :align: center

    .. image:: fareyx1x4.png
        :alt: Checking projection regularity
        :width: 400 px
        :align: center

    """
    
    def __init__(self,n=20, s=3, Randomized=False, seed=None,fileName='farey',Debug=False):
        # imports
        import random
        from arithmetics import computeFareySeries
        # fixing random seed
        random.seed(seed)
        # storing parameters
        self.n = n
        self.s = s
        self.Randomized = Randomized
        self.seed = seed
        self.fileName = fileName
        self.Debug = Debug
        # randomization
        if Randomized:
            v = [random.random() for j in range(s)]
        # generate Farey series
        fs = computeFareySeries(n=n,AsFloats=True)
        self.fareySeries = list(fs)
        nf = len(fs)
        self.seriesLength= nf
        random.shuffle(fs)
        # storing the simulated point set
        if fileName != None:
            fileName += '.csv'
            fo =  open(fileName,'w') 
            # csv header row
            wstr = ''
            for j in range(s-1):
                wstr += '"x%d",' % (j+1)
            wstr += '"x%d"\n' % (s)
            fo.write(wstr)
        # start point set at origin
        u = [0.0 for j in range(s)]
        pointSet = [tuple(u)] 
        ptfs = 0
        if fileName != None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # first s-dimensional point 
        u[s-1] = fs[ptfs]
        ptfs += 1
        if Randomized:
            for j in range(s):
                z = u[j] + v[j]
                u[j] = z - int(z)
        pointSet.append((tuple(u)))
        if Debug:
            print(1,u)
        if fileName != None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # all the following points
        for i in range(ptfs,nf):
            for j in range(s-1):
                u[j] = u[j+1] # << 1
            u[s-1] = fs[i]
            if Randomized:
                for j in range(s):
                    z = u[j] + v[j]
                    u[j] = z - int(z)
            pointSet.append((tuple(u)))
            if Debug:
                print(i,u)
            if fileName != None:
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        fo.close()
        self.pointSet = pointSet

    def testFct(self,ptSet=None,buggyRegionLimits=(0.45,0.55)):
        """
        Tiny buggy hypercube for testing a quasi random Farey point set.
        """
        s = self.s
        buggyHypercube = dict()
        for j in range(s):
            buggyHypercube[j] = buggyRegionLimits
        Bugs = 0
        if ptSet == None:
            ptSet = self.pointSet
        for x in ptSet:
            for j in range(s):
                if (x[j] >= buggyHypercube[j][0] and x[j] <= buggyHypercube[j][1]):
                    BuggyPoint = True
                else:
                    BuggyPoint = False
                    break
            if BuggyPoint:
                print('Bug:', x, buggyHypercube)
                Bugs += 1
        if Bugs > 0:
            return '%d bug(s) detected !!!' % Bugs
        else:
            return 'No bugs detected'

        
#----------testing the code ----------------
if __name__ == "__main__":    
# #------------  Discrete number generator
#     ## initialize the discrete random variable 
#     discreteLaw = {0:0.0478,
#                    1:0.3349,
#                    2:0.2392,
#                    3:0.1435,
#                    4:0.0957,
#                    5:0.0670,
#                    6:0.0478,
#                    7:0.0096,
#                    8:0.0096,
#                    9:0.0048,}

#     ## initialze the random generator
#     rdv = DiscreteRandomVariable(discreteLaw,seed=1)
    
#     ## sample discrete random variable and count frequencies of obtained values
#     sampleSize = 1000
#     frequencies = {}
#     for i in range(sampleSize):
#         x = rdv.random() 
#         try:
#             frequencies[x] += 1
#         except:
#             frequencies[x] = 1
            
#     ## print results
#     results = [x for x in frequencies]
#     results.sort()
#     counts= 0.0
#     for x in results:
#         counts += frequencies[x]
#         print  ('%s, %d, %.3f, %.3f' % (x, frequencies[x],
#                                        float(frequencies[x])/float(sampleSize),
#                                        discreteLaw[x]))
#     print ('# of valid samples = %d' % counts)

# #-------------- Extended triangular number generator
#     from math import floor
#     rdv1 = ExtendedTriangularRandomVariable(seed=1)
#     rdv2 = ExtendedTriangularRandomVariable(lowLimit=1,
#                                             highLimit=2,
#                                             mode=1.25,
#                                             probRepart=0.5,
#                                             seed=1)

#     ## sample extTriangular random variable and count frequencies of obtained values
#     Nsim = 10**4
#     modulus = 128
#     frequencies = {}
#     freqKeys = [x for x in range(modulus*2)]
    
#     for k in freqKeys:
#         frequencies[k] = {1:0,2:0}

#     fo = open('testTr.csv','w')
#     fo.write('"x1","x2"\n')

#     for i in range(Nsim):
#         x1 = rdv1.random()
#         r1 = int(floor(x1*modulus))
#         x2 = rdv2.random()
#         fo.write('%.4f,%4f\n'%(x1,x2))
#         r2 = int(floor(x2*modulus))
#         frequencies[r1][1] += 1
#         frequencies[r2][2] += 1

#     fo.close()     
#     ## print results
#     print(frequencies)
#     results= [x for x in frequencies]
#     results.sort()
    
#     for x in results:
#         print('%s \t %d \t %.3f \t %d\t %.3f' % (x, frequencies[x][1],
#                                        float(frequencies[x][1])/float(Nsim),
#                                                  frequencies[x][2],
#                                        float(frequencies[x][2])/float(Nsim))
#               )
#     print('# of simulations = %d' % Nsim)

# #-------------- Cauchy number generator
#     rdv3 = CauchyRandomVariable(seed=1)
#     rdv4 = CauchyRandomVariable(position=10.0,scale=5.0)
                
#     ## sample Cauchy random variable and count frequencies of obtained values
#     Nsim = 10**4
#     modulus = 128
#     fo = open('testCauchy.csv','w')
#     fo.write('"x1","x2"\n')

#     for i in range(Nsim):
#         x1 = rdv3.random()
#         x2 = rdv4.random()
#         fo.write('%.4f,%4f\n'%(x1,x2))

#     fo.close()     
#     print('# of Cauchy simulations = %d' % Nsim)

#-------------- testing quasi random Korobov sampling against Mersenne twister sampling
    # kor = QuasiRandomKorobovPointSet(n=997,s=5,a=383,Randomized=True,seed=3,Debug=False)
    # print(kor.sequence[:10])
    # print('Korobov quasi random sampling')
    # print(kor.testFct(seq=kor.sequence,buggyRegionLimits=(0.45,0.55)))
    # randSeq = []
    # seed = 3
    # import random
    # random.seed(seed)
    # for i in range(997):
    #     point = []
    #     for j in range(kor.s):
    #         point.append(random.random())
    #     randSeq.append(point)
    # print('Mersenne Twister random sampling')
    # print(kor.testFct(seq=randSeq,buggyRegionLimits=(0.45,0.55)))
    qrfs = QuasiRandomFareyPointSet(n=25,s=4)
    print(qrfs.fareySeries)
    print(qrfs.pointSet)
    print(len(qrfs.pointSet))
            

