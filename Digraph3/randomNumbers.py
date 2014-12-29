#!/usr/bin/env python3
# Python3+ implementation of random number generators
# Copyright (C) 2014  Raymond Bisdorff
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#######################

__version__ = "Branch: 3.4 $"
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
                print('!!! Error: mode out of value range !!')
            
        
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
        :width: 400 px
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
            

#----------testing the code ----------------
if __name__ == "__main__":    
#------------  Discrete number generator
    ## initialize the discrete random variable 
    discreteLaw = {0:0.0478,
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
    rdv = DiscreteRandomVariable(discreteLaw,seed=1)
    
    ## sample discrete random variable and count frequencies of obtained values
    sampleSize = 1000
    frequencies = {}
    for i in range(sampleSize):
        x = rdv.random() 
        try:
            frequencies[x] += 1
        except:
            frequencies[x] = 1
            
    ## print results
    results = [x for x in frequencies]
    results.sort()
    counts= 0.0
    for x in results:
        counts += frequencies[x]
        print  ('%s, %d, %.3f, %.3f' % (x, frequencies[x],
                                       float(frequencies[x])/float(sampleSize),
                                       discreteLaw[x]))
    print ('# of valid samples = %d' % counts)

#-------------- Extended triangular number generator
    from math import floor
    rdv1 = ExtendedTriangularRandomVariable(seed=1)
    rdv2 = ExtendedTriangularRandomVariable(lowLimit=1,
                                            highLimit=2,
                                            mode=1.25,
                                            probRepart=0.5,
                                            seed=1)

    ## sample extTriangular random variable and count frequencies of obtained values
    Nsim = 10**4
    modulus = 128
    frequencies = {}
    freqKeys = [x for x in range(modulus*2)]
    
    for k in freqKeys:
        frequencies[k] = {1:0,2:0}

    fo = open('testTr.csv','w')
    fo.write('"x1","x2"\n')

    for i in range(Nsim):
        x1 = rdv1.random()
        r1 = int(floor(x1*modulus))
        x2 = rdv2.random()
        fo.write('%.4f,%4f\n'%(x1,x2))
        r2 = int(floor(x2*modulus))
        frequencies[r1][1] += 1
        frequencies[r2][2] += 1

    fo.close()     
    ## print results
    print(frequencies)
    results= [x for x in frequencies]
    results.sort()
    
    for x in results:
        print('%s \t %d \t %.3f \t %d\t %.3f' % (x, frequencies[x][1],
                                       float(frequencies[x][1])/float(Nsim),
                                                 frequencies[x][2],
                                       float(frequencies[x][2])/float(Nsim))
              )
    print('# of simulations = %d' % Nsim)

#-------------- Cauchy number generator
    rdv3 = CauchyRandomVariable(seed=1)
    rdv4 = CauchyRandomVariable(position=10.0,scale=5.0)
                
    ## sample Cauchy random variable and count frequencies of obtained values
    Nsim = 10**4
    modulus = 128
    fo = open('testCauchy.csv','w')
    fo.write('"x1","x2"\n')

    for i in range(Nsim):
        x1 = rdv3.random()
        x2 = rdv4.random()
        fo.write('%.4f,%4f\n'%(x1,x2))

    fo.close()     
    print('# of Cauchy simulations = %d' % Nsim)


