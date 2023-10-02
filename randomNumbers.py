#!/usr/bin/env python3
"""
Python3+ implementation of random number generators
Copyright (C) 2014-2023  Raymond Bisdorff

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

__version__ = "$Revision: Python 3.10"

class IncrementalQuantilesEstimator(object):
    """
    *References*: 
       - John M. Chambers (et al.), Monitoring Networked Applications 
    with incremental Quantile estimation, *Statistical Science* 2006 (4):463-475
       - William H. Press, Saul A. Teukolsky, William T. Vetterling, and Brian P. Flannery, *Numerical Recipes : The Art of Scientific Computing,Third Edition* (NR3), Cambridge University Press, Cambridge UK 2007.

    Python reimplementation (RB) from the C++/NR3 source code.
 
    See Computational Statistics Course : http://hdl.handle.net/10993/37870
    Lecture 5.

    Example usage:

        >>> from randomNumbers import IncrementalQuantilesEstimator
        >>> import random
        >>> random.seed(1)
        >>> iqAgent = IncrementalQuantilesEstimator(nbuf=100)
        >>> # feeding the iqAgent with standard Gaussian random numbers 
        >>> for i in range(1000):
        ...     iqAgent.add(random.gauss(mu=0,sigma=1))
        >>> # reporting the estimated Gaussian quartiles
        >>> print(iqAgent.report(0.0))
        -2.961214270519158
        >>> print(iqAgent.report(0.25))
        -0.6832621550224423
        >>> print(iqAgent.report(0.50))
        -0.014392849958746522
        >>> print(iqAgent.report(0.75))
        0.7029655732010196
        >>> print(iqAgent.report(1.00))
        2.737259509189501
        >>> # saving the iqAgent's state
        >>> iqAgent.saveState('test.csv')
  
    """

    def __init__(self,nbuf=1000,Debug=False):
        """
        *nbuf* := buffersize in bytes (default = 1000B)
        250 quantiles containing all percentiles from 0.10 to 0.90
        and heavy tails.
        
        """
        from sys import float_info
        self.Debug=Debug
        self.nbrupd = 0
        self.nq = 251
        self.qile = [0.0 for x in range(self.nq)]
        pval = [0.0 for x in range(self.nq)]
        for j in range(85,166):
            pval[j] = (j-75.0)/100.0
        for j in range(84,-1,-1):
            pval[j] = 0.87191909*pval[j+1]
            pval[250-j] = 1.0-pval[j]
        self.pval = pval
        
        self.nt = 0
        
        self.nbuf = nbuf
        self.dbuf = []
        
        self.q0 = float_info[0] # max float
        self.qm = float_info[3] # min float
        if Debug:
            self.saveState('initState.csv')

    def reset(self):
        """
        Reset the content of the estimator to the initial state.
        """
        self.nbrupd = 0
        self.qile = [0.0 for x in range(self.nq)]
        self.nt = 0
        self.dbuf = []

    def add(self,datum):
        """
        Assimilate a new value from the stream
        """
        x = datum
        self.dbuf.append(x)
        if x < self.q0:
            self.q0 = x
        if x > self.qm:
            self.qm = x
        if len(self.dbuf) == self.nbuf:
            self._update()

    def addList(self,listDatum,historyWeight=None):
        """
        Assimilate a list of new values.

        Parameter:

        *historyWeight* takes decimal values in [0.0;1.0[ and  
        indicates a requested proportional weight of the history 
        wrt to the length of listDatum. 

        Is ignored when None (default).
        
        """
        if historyWeight is not None:
            if (historyWeight < 0.0) or (historyWeight >= 1.0):
                print('Error: historyWeight %.f must be in [0.0;1.0[' \
                      % historyWeight)
                return
            m = len(listDatum)
            if m > 0:
                self.nt = round(historyWeight/(1.0 - historyWeight)*m)
        if len(self.dbuf) > 0:
            self._update() # clearing the income buffer
        for datum in listDatum:
            self.add(datum)

    def _update(self):
        """
        Batch update. For internal use only.
        Called a.o. by self.add(), self.report() and
        self.saveState() methods
        """
        jd = 0
        jq = 1
        told = 0.0
        tnew = 0.0
        nq = self.nq
        nt = self.nt
        q0 = self.q0
        qm = self.qm
        dbuf = self.dbuf
        dbuf.sort()
        nd = len(dbuf)
        pval = self.pval
        qile = self.qile
        newqile = [0.0 for i in range(self.nq)]

        # set lowest and highest to min and max values seen so far
        qold = q0
        qnew = q0
        qile[0] = q0
        newqile[0] = q0
        qile[nq-1] = qm
        newqile[nq-1] = qm
        # and set compatible p-values
        pval[0] = min(0.5/(nt+nd),0.5*pval[1])
        pval[nq-1] = max(1.0-0.5/(nt+nd),0.5*(1.0+pval[nq-2]))

        for iq in range(1,nq-1):
            # main loop over target p-values for interpolation
            target = (nt+nd)*pval[iq]
            if self.Debug:
                print('-->> enter quantile iq: ', iq)
                print('        tnew, target ' ,tnew,target)
            if tnew < target:
                # find a succession of abcissa-ordinate pairs (qnew,tnew) that
                # are the discontinuity of value or slope and break to perform
                # an interpolation as we cross each target
                while True:
                    if self.Debug:
                        try:
                            print('iq, jq, nq, jd, nd, qile[jq], dbuf[jd]',\
                                  iq, jq, nq, jd, nd, qile[jq], dbuf[jd])
                        except:
                            print('\niq, jq, nq, jd, nd, qile[jq]',\
                                  iq, jq, nq, jd, nd, qile[jq])
                    if (jq < nq) and ( (jd >= nd) or (qile[jq] < dbuf[jd]) ):
                        # found slope discontinuity from old cdf
                        qnew = qile[jq]
                        tnew = jd + nt*pval[jq]
                        jq += 1
                        if self.Debug:
                            print('slope: tnew, target', tnew, target)
                        if tnew >= target:
                            break
                    else:
                        # found value discontinuity from batch cdf
                        qnew = dbuf[jd]
                        tnew = told
                        
                        if qile[jq] > qile[jq-1]:
                            tnew += nt*(pval[jq]-pval[jq-1])\
                                    * (qnew-qold)/(qile[jq]-qile[jq-1])
                        jd += 1
                        if self.Debug:
                            print('value 1: tnew, target', tnew, target)
                        if tnew >= target:
                            break
                        told = tnew
                        tnew += 1.0
                        qold = qnew
                        if self.Debug:
                            print('value 2: tnew, target', tnew, target)
                        if tnew >= target:
                            break

                    told = tnew
                    qold = qnew
            # break to here and perform the new interpolation
            if tnew == told:
                newqile[iq] = 0.5* (qold+qnew)
            else:
                newqile[iq] = qold + (qnew - qold)*(target-told)/(tnew-told)
            told = tnew
            qold = qnew

        
        self.q0 = q0
        self.qm = qm
        self.pval = pval
        self.qile = newqile
        self.nt += nd
        self.dbuf = []

        if self.Debug:
            self.nbrupd += 1
            fileName = 'saveState-%d.csv' % self.nbrupd
            self.saveState(fileName)
        
    def report(self, p = 0.5):
        """
        Return estimated *p*-quantile (default = median)
        for the data seen so far 
        """
        nq = self.nq
        pval = self.pval
        qile = self.qile
        if len(self.dbuf) > 0:
            self._update()
        jl = 0
        jh = nq-1
        while (jh - jl) > 1:
            j = (jh + jl) >> 1
            if p > pval[j]:
                jl = j
            else:
                jh = j
        j = jl
        
        try:
            q = qile[j] + (qile[j+1]-qile[j])*(p-pval[j])/(pval[j+1]-pval[j])
        except:
            q = qile[j]
            
        return max(qile[0],min(qile[nq-1],q))

    def cdf(self,x=0):
        """
        return proportion of data lower or equal to value x
        """
        nq = self.nq
        pval = self.pval
        qile = self.qile
        if len(self.dbuf) > 0:
            self._update
        jl = 0
        jh = nq-1
        while (jh - jl) > 1:
            j = (jh + jl) >> 1
            if x > qile[j]:
                jl = j
            else:
                jh = j
        j = jl
        if (qile[j+1] - qile[j]) > 0:
            p = pval[j] + (pval[j+1]-pval[j])*(x - qile[j])/(qile[j+1]-qile[j])
        else:
            p = pval[j]
        return max(pval[0], min(pval[nq-1],p))

        
    def saveState(self,fileName='state.csv'):
        """
        Save the state of the IncrementalQuantileEstimator self instance
        """
        if len(self.dbuf) > 0:
            self._update()
        fo = open(fileName,'w')
        fo.write('"p-value","quantile"\n')
        for iq in range(self.nq):
            fo.write('%.7f, %.5f\n' % (self.pval[iq],self.qile[iq]))
        fo.close()

    def loadState(self,FileName='state.csv'):
        """
        Load a previously saved state of the estimator
        """
        from csv import DictReader
        fo = open(FileName,'r')
        csvDict = DictReader(fo)
        for i,row in enumerate(csvDict):
            self.pval[i] = float(row['p-value'])
            self.qile[i] = float(row['quantile'])
        fo.close()


class DiscreteRandomVariable():
    """
    Discrete random variable generator

    Parameters:
        | discreteLaw := dictionary with discrete variable states
        |                as keys and corresponding probabilities
        |                as float values,
        | seed := integer for fixing the sequence generation.

    Example usage:
        >>> from randomNumbers import DiscreteRandomVariable
        >>> discreteLaw = {0:0.0478,
        ...                1:0.3349,
        ...                2:0.2392,
        ...                3:0.1435,
        ...                4:0.0957,
        ...                5:0.0670,
        ...                6:0.0478,
        ...                7:0.0096,
        ...                8:0.0096,
        ...                9:0.0048,}
        >>> ## initialze the random generator
        >>> rdv = DiscreteRandomVariable(discreteLaw,seed=1)
        >>> ## sample discrete random variable and
        >>> ## count frequencies of obtained values
        >>> sampleSize = 1000
        >>> frequencies = {}
        >>> for i in range(sampleSize):
        ...     x = rdv.random() 
        ...     try:
        ...         frequencies[x] += 1
        ...     except:
        ...         frequencies[x] = 1
        >>> ## print results
        >>> results = [x for x in frequencies]
        >>> results.sort()
        >>> counts= 0.0
        >>> for x in results:
        ...     counts += frequencies[x]
        ...     print('%s, %d, %.3f, %.3f'\
                      % (x, frequencies[x],\
                      float(frequencies[x])/float(sampleSize),\
                      discreteLaw[x]))
        0, 53, 0.053, 0.048
        1, 308, 0.308, 0.335
        2, 243, 0.243, 0.239
        3, 143, 0.143, 0.143
        4, 107, 0.107, 0.096
        5, 74, 0.074, 0.067
        6, 45, 0.045, 0.048
        7, 12, 0.012, 0.010
        8, 12, 0.012, 0.010
        9, 3, 0.003, 0.005
        >>> print ('# of valid samples = %d' % counts)
        # of valid samples = 1000
    """
    
    def __init__(self, discreteLaw = None, seed = None, Debug=False):
        """
        Constructor for discrete random variables with
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed is not None:
            self._random.seed(self.seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print ('No seed is used')
            
        if discreteLaw is not None:
            self.discreteLaw = discreteLaw
            self.F = self._cumulative()
        else:
            print('!!! Error: A discrete law is required here!')
        

    def _cumulative(self):
        """
        Renders the cumulative probability distribution F(x)
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
        Generates discrete random values from a discrete random variable.
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
        - seed := number for fixing the sequence generation.

    .. image:: extTrDistribution.png
        :alt: Extended triangular distribution
        :width: 500 px
        :align: center

    """
    
    def __init__(self, lowLimit=0.0, highLimit = 1.0,
                 mode=None, probRepart=0.5, seed=None, Debug=False):
        """
        Constructor for extended triangular random variables
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed is not None:
            self._random.seed(seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print('Default seed is used')
        self.m = lowLimit
        self.M = highLimit
            
        if mode is None:
            amplitude = highLimit-lowLimit
            self.xm = highLimit - (amplitude/2.0)
        else:
            if mode >= lowLimit and mode <= highLimit: 
                self.xm = mode
            else:
                print('!!! Error: mode out of value range !!')
        if probRepart is None:
            self.r = 0.5
        else:
            if probRepart >= 0.0 and probRepart <= 1.0:
                self.r = probRepart
            else:
                print('!!! Error: probility repartition out of value range !!')
            
        
    def random(self):
        """
        Generates an extended triangular random number.
        """
        
        from math import sqrt
        u = self._random.random()

        if u < self.r:
            randeval = self.m + sqrt(u/self.r)*(self.xm-self.m)                   
        else:
            randeval = self.M - sqrt((1-u)/(1-self.r))*(self.M-self.xm)

        return randeval

#-------------------
                  
class BinomialRandomVariable():
    """
    Binomial random variable generator

    Parameters:
        - size := integer number > 0 of trials
        - prob := float success probability 
        - seed := number for fixing the sequence generation.
    
    """
    
    def __init__(self, size=10, prob = 0.5,
                 seed=None, Debug=False):
        """
        constructor for binomial random variables.
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed is not None:
            self._random.seed(seed)
            if Debug:
                print('seed %d is used' % (seed))
        else:
            if Debug:
                print('Default seed is used')
        self.size = size
        self.prob = prob            
        
    def random(self):
        """
        Generates a binomial random number by
        repeating *self.size* Bernouilli trials.
        """
        successCount = 0
        size = self.size
        prob = self.prob
        for i in range(size):
            if self._random.random() < prob:
                successCount += 1                  
        return successCount

#-------------------
                  
class CauchyRandomVariable():
    """
    Cauchy random variable generator.

    Parameters:
        - position := median (default=0.0) of the Cauchy distribution
        - scale := typical spread (default=1.0) with respect to median 
        - seed := number (default=None) for fixing the sequence generation.
    
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
        Constructor for Cauchy random variables.
        """
        import random
        self._random = random
        self.seed = seed
        if self.seed is not None:
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
        Generates a Cauchy random number.
        """
        
        from math import pi,tan

        prob = self._random.random()

        randeval = self.position + self.scale*( tan( pi*(prob - 0.5) ) )                  

        return randeval

#---------
class QuasiRandomPointSet():
    """
    Abstract class for generic quasi random point set methods and tools.
    """
    def testFct(self,seq=None,buggyRegionLimits=(0.45,0.55)):
        """
        Tiny buggy hypercube for testing a quasi random Korobov 3D sequence.
        """
        s = self.s
        buggyHypercube = dict()
        for j in range(s):
            buggyHypercube[j] = buggyRegionLimits
        Bugs = 0
        if seq is None:
            seq = self.pointSet
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

    def countHits(self,regionLimits,pointSet=None):
        """
        Counts *hits* of a quasi random point set in given regionLimits.
        """
        s = self.s
        hits = 0
        if pointSet is None:
            pointSet = self.pointSet
        for x in pointSet:
            for j in range(s):
                if (x[j] >= regionLimits[j][0] and x[j] <= regionLimits[j][1]):
                    HitPoint = True
                else:
                    HitPoint = False
                    break
            if HitPoint:
                #print('Hit:', x, regionLimits)
                hits += 1
        return hits
    
    def testUniformityDiscrepancy(self,k=4,pointSet=None,fileName='testUniformity',Debug=True):
        """
        Counts the number of point in each partial hypercube [(x-1)/k,x/k]^d
        where x integer ands 0 < x <= k.
        """
        from itertools import product
        s = self.s
        ctrlLists = []
        kf = float(k)
        for i in range(s):
            ctrlLists.append([((x-1)/kf,x/kf) for x in range(1,k+1)])
            #if Debug:
            #    print(ctrlLists)
        with open(fileName+'.csv','w') as fo:
            fo.write('"x\n"')
            for region in product(*ctrlLists):
                #print(region)
                hits = self.countHits(region,pointSet)
                fo.write('%d\n' % hits)            
        r = k**s
        if pointSet is not None:
            cardPtSet = len(pointSet)
        else:
            cardPtSet = self.pointSetCardinality
        thProb = float(cardPtSet)/r
        print('Theoretical distribution: %d / %d = %.3f'\
              % (cardPtSet,r,thProb) )
        
            
    
#----------
class QuasiRandomKorobovPointSet(QuasiRandomPointSet):
    """
    Constructor for rendering a Korobov point set of dimension *n* which is *fully projection regular* in the $s$-dimensional real-valued [0,1)^s hypercube. The constructor uses a MLCG generator with potentially a full period. The point set is stored in a self.sequence attribute and saved in a CSV formatted file.

    *Source*: Chr. Lemieux, Monte Carlo and quasi Monte Carlo Sampling Springer 2009 Fig. 5.12 p. 176.

    *Parameters*:

        * *n* : (default=997) number of Korobov points and modulus of the underlying MLCG
        * *s* : (default=3) dimension of the hypercube
        * *Randomized* : (default=False) the sequence is randomly shifted (mod 1) to avoid cycling when *s* > *n*
        * *a* : (default=383) MLCG coefficient (0 < *a* < *n*), primitive with *n*. The choice of *a* and *n* is crucial for getting an MLCG with full period and hence a fully projection-regular sequence. A second good pair is given with *n* = 1021 (prime) and *a* = 76.
        * *fileName*: (default='korobov') name -without the csv suffix- of the stored result. 
        * *seed* := number (default=None) for fixing the sequence generation.

    Sample Python session:

        >>> from randomNumbers import QuasiRandomKorobovPointSet
        >>> kor = QuasiRandomKorobovPointSet(Debug=True)
        0 [0.0, 0.0, 0.0]
        1 [0.13536725313948247, 0.23158619430934912, 0.8941657924971758]
        2 [0.36595043842175035, 0.7415995294344084, 0.7035940773517395]
        3 [0.8759637735468097, 0.5510278142889722, 0.714627176649633]
        4 [0.6853920584013734, 0.5620609135868657, 0.9403042077429129]
        5 [0.6964251576992669, 0.7877379446801456, 0.3746071164690914]

    The resulting Korobov sequence may be inspected in an **R** session::

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
    
    def __init__(self,n=997, s=3, a=383, Randomized=False, seed=None,\
                 fileName='korobov',Debug=False):
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
        self.pointSet = sequence
        self.pointSetCardinality = len(sequence)


#-------
class QuasiRandomFareyPointSet(QuasiRandomPointSet):
    """
    Constructor for rendering a Farey point set of dimension *s* and max denominateor *n* which is *fully projection regular* in the $s$-dimensional real-valued [0,1]^s hypercube. The lattice constructor uses a randomly shuffled Farey series for the point construction. The resulting point set is stored in a self.pointSet attribute and saved by default in a CSV formatted file.

    *Parameters*:

        * *n* : (default=20) maximal denominator of the Farey series
        * *s* : (default=3) dimension of the hypercube
        * *seed* : (default = None) number for regenerating a fixed Farey point set 
        * *Randomized* : (default=True) On each dimension, the points are randomly shifted (mod 1) to avoid constant projections for equal dimension index distances.
        * *fileName*: (default='farey') name -without the csv suffix- of the stored result file. 

    Sample Python session:

        >>> from randomNumbers import QuasiRandomFareyPointSet
        >>> qrfs = QuasiRandomFareyPointSet(n=20,s=5,Randomized=True,
        ...                                 fileName='testFarey')
        >>> print(qrfs.__dict__.keys())
        dict_keys(['n', 's', 'Randomized', 'seed', 'fileName', 'Debug', 
                   'fareySeries', 'seriesLength', 'shuffledFareySeries', 
                   'pointSet', 'pointSetCardinality'])
        >>> print(qrfs.fareySeries)
        [0.0, 0.04, 0.04166, 0.0435, 0.04545, 0.0476, 0.05, 0.05263, 
         0.0555, 0.058823529411764705, ...] 
        >>> print(qrfs.seriesLength)
        201
        >>> print(qrfs.pointSet)
        [(0.0, 0.0, 0.0, 0.0, 0.0), (0.5116, 0.4660, 0.6493, 0.41757, 0.3663),
         (0.9776, 0.1153, 0.0669, 0.7839, 0.5926), (0.6269, 0.5329, 0.4332, 0.0102, 0.6126),
         (0.0445, 0.8992, 0.6595, 0.0302, 0.6704), ...]
        >>> print(qrfs.pointSetCardinality)
        207
     
    The resulting point set may be inspected in an R session::

        > x = read.csv('testFarey.csv')
        > x[1:5,]
          x1       x2       x3       x4       x5
        1   0.000000 0.000000 0.000000 0.000000 0.000000
        2   0.511597 0.466016 0.649321 0.417573 0.366316
        3   0.977613 0.115336 0.066893 0.783889 0.592632
        4   0.626933 0.532909 0.433209 0.010205 0.612632
        5   0.044506 0.899225 0.659525 0.030205 0.670410
       > library('lattice')
        > cloud(x$x5 ~ x$x1 + x$x3)
        > plot(x$x1,x$x3) 

    .. image:: farey3D.png
        :alt: Checking hypercube filling
        :width: 500 px
        :align: center

    .. image:: fareyx1x3.png
        :alt: Checking projection regularity
        :width: 400 px
        :align: center

    """
    
    def __init__(self,n=20,s=3,seed=None,Randomized=True,
                 fileName='farey',Debug=False):
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
        if s > nf:
            print('Error: s = %d larger than Farey series length = %d !!' % (s,nf))
            print('Choose a higher denominator than the actual n = %d !!' % n)
            return
        self.seriesLength = nf
        random.shuffle(fs)
        if fs[0] < self.fareySeries[1]:   # if first term is zero 
            fs[0],fs[1] = fs[1],fs[0]     # swap first and second !!!
        if fs[nf-1] > self.fareySeries[nf-2]:   # if last term is one  
            fs[nf-1],fs[nf-2] = fs[nf-2],fs[nf-1]     # swap last and second last!!!
        self.shuffledFareySeries = list(fs)
        # storing the simulated point set
        if fileName is not None:
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
        if fileName is not None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # first s-dimensional point
        u[s-1] = fs[0]
        if Randomized:
            for j in range(s):
                z = u[j] + v[j]
                u[j] = z - int(z)
        pointSet.append((tuple(u)))
        if Debug:
            print(1,u)
        if fileName is not None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # all the following points
        for i in range(1,nf):
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
            if fileName is not None:
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        # close with adding s ones
        if Randomized:
            u = [self.fareySeries[nf-1] for j in range(s)]
            pointSet.append((tuple(u)))
            if fileName is not None:
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        else:
            for jj in range(s):
                for j in range(s-1):
                    u[j] = u[j+1] # << 1
                u[s-1] = self.fareySeries[nf-1]
                pointSet.append((tuple(u)))
                if fileName is not None:
                    wstr = ''
                    for j in range(s-1):
                        wstr += '"%f",' % (u[j])
                    wstr += '"%f"\n' % (u[s-1])
                    fo.write(wstr)
        # close file and store point set
        fo.close()
        self.pointSet = pointSet
        self.pointSetCardinality = 1 + nf + s 

#-------
class QuasiRandomUniformPointSet(QuasiRandomPointSet):
    """
    Constructor for rendering a quai random point set of dimension *s* and
    max denominateor *n* which is *fully projection regular* in the *s*-dimensional
    real-valued [0,1]^s hypercube. The lattice constructor uses a randomly shuffled
    *uniform* series for the point construction. The resulting point set is stored
    in a *self.pointSet* attribute and saved by default in a CSV formatted file.

    *Parameters*:

        * *n* : (default=100) denominator of the uniform series x/n with 0 <= x <= n,
        * *s* : (default=3) dimension of the hypercube,
        * *seed* : number (default = None) for regenerating the same Farey point set ,
        * *Randomized* : (default=True) On each dimension, the points are randomly
           shifted (mod 1) to avoid constant projections for equal dimension index distances,
        * *fileName*: (default='uniform') name -without the csv suffix- of the stored result file. 

    """
    
    def __init__(self,n=100,s=3,seed=None,Randomized=True,fileName='uniform',Debug=False):
        # imports
        import random
        # fixing random seed
        random.seed(seed)
        # storing parameters
        self.n = n
        nf = float(n)
        self.s = s
        self.Randomized = Randomized
        self.seed = seed
        self.fileName = fileName
        self.Debug = Debug
        # randomization
        if Randomized:
            v = [random.random() for j in range(s)]
        # generate uniform series
        us = [x/nf for x in range(n+1)]
        self.uniformSeries = list(us)
        nu = len(us)
        if s > nu:
            print('Error: s = %d larger than uniform series length = %d !!' % (s,nf))
            print('Choose a higher denominator than the actual n = %d !!' % n)
            return
        self.seriesLength = nu
        random.shuffle(us)
        if us[0] < self.uniformSeries[1]:   # if first term is zero 
            us[0],us[1] = us[1],us[0]     # swap first and second !!!
        if us[nu-1] > self.uniformSeries[nu-2]:   # if last term is one  
            us[nu-1],us[nu-2] = us[nu-2],us[nu-1]     # swap last and second last!!!
        self.shuffledUniformSeries = list(us)
        # storing the simulated point set
        if fileName is not None:
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
        if fileName is not None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # first s-dimensional point
        u[s-1] = us[0]
        if Randomized:
            for j in range(s):
                z = u[j] + v[j]
                u[j] = z - int(z)
        pointSet.append((tuple(u)))
        if Debug:
            print(1,u)
        if fileName is not None:
            wstr = ''
            for j in range(s-1):
                wstr += '"%f",' % u[j]
            wstr += '"%f"\n' % u[s-1]
            fo.write(wstr)
        # all the following points
        for i in range(1,nu):
            for j in range(s-1):
                u[j] = u[j+1] # << 1
            u[s-1] = us[i]
            if Randomized:
                for j in range(s):
                    z = u[j] + v[j]
                    u[j] = z - int(z)
            pointSet.append((tuple(u)))
            if Debug:
                print(i,u)
            if fileName is not None:
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        # close with adding s ones
        if Randomized:
            u = [self.uniformSeries[nu-1] for j in range(s)]
            pointSet.append((tuple(u)))
            if fileName is not None:
                wstr = ''
                for j in range(s-1):
                    wstr += '"%f",' % (u[j])
                wstr += '"%f"\n' % (u[s-1])
                fo.write(wstr)
        else:
            for jj in range(s):
                for j in range(s-1):
                    u[j] = u[j+1] # << 1
                u[s-1] = self.uniformSeries[nu-1]
                pointSet.append((tuple(u)))
                if fileName is not None:
                    wstr = ''
                    for j in range(s-1):
                        wstr += '"%f",' % (u[j])
                    wstr += '"%f"\n' % (u[s-1])
                    fo.write(wstr)
        # close file and store point set
        fo.close()
        self.pointSet = pointSet
        self.pointSetCardinality = 1 + nu + s 

# --------------------------
class MontyHallGameSimulator(object):
    """
    Generalized Monty Hall game simulator:
    https://en.wikipedia.org/wiki/Monty_Hall_problem

    Suppose you're on a game show, and you're given the choice of *n* doors:
    Behind one door is a car; behind the others, goats.
    You pick a door, say No. 1, and the host, who knows what's behind the doors,
    to give you some clues, opens *k* other doors which have a goat.
    He then says to you, "Do you want to pick another closed door?"
    Is it to your advantage to switch your choice?

    ! The number *n* of doors must be at least equal to 3.
   
    ! The number *k* of clues cannot exceed the number of doors minus two,
    namely the initially chosen and the last closed door where the car could be behind.


    With *n* doors and *k* clues, the success probabilities become:
    *1/n* when not switched, and *(n-1)/n(n-1-k)* when switched.
    When the number of clues *k* = 0, both success probabilities remain the same,
    namely *1/n* = *(n-1)/n(n-1)*. Evidently there is no reason to switch the
    initial choice in this case. However, when 0 < *k* < *(n-1)*,
    then the complement probability of *1/n*, i.e. *(n-1)/n* gets
    divided by the number *(n-1-k) > 0* of still closed doors.
    With positive clues, it is hence the more interesting to switch
    the initial choice the more clues one is given.
    With a maximum of *k = n-2* clues, the success probability,
    when switching, becomes: *(n-1)/n*.  

        >>> from randomNumbers import MontyHallGameSimulator
        >>> m = MontyHallGameSimulator(numberOfDoors=6,
        ...                            numberOfClues=4)
        >>> m.simulate(numberOfTrials=1000,seed=1)
         *******************************
         Monty Hall game successes count
         Number of doors: 6
         Number of clues: 4
         Sampling size  : 1000
         Random seed    : 1
         ----------------------------------
         Switched    : 838 (0.8380); Theoretical probability: 0.8333
         Not switched: 162 (0.1620); Theoretical probability: 0.1667

    """
    def __init__(self,numberOfDoors=3,numberOfClues=1):
        if numberOfDoors < 3:
            print('Error: the number *n* of doors must be at least three !!!')
            return
        self.numberOfDoors = numberOfDoors
        if numberOfClues > numberOfDoors-2:
            print('Error: the number *k* of clues  cannot exceed *(n-2)* !!!')
            return
        self.numberOfClues = numberOfClues

    def simulate(self,numberOfTrials=10,seed=None,Comments=True):
        import random
        from copy import copy
        random.seed(seed)
        numberOfDoors = self.numberOfDoors
        numberOfClues = self.numberOfClues
        successes = {'notSwitched': 0, 'switched': 0}
        nd = numberOfDoors-1
        doors = ['goat' for i in range(nd)]
        doors.append('car')
        sampling = numberOfTrials
        for s in range(sampling):
            random.shuffle(doors)
            choice1a = random.randint(0,nd)
            i = 0
            h = 0
            clues=[]
            while h < numberOfClues:
                if i != choice1a and doors[i] != 'car' :
                    clues.append(i)
                    h += 1
                    i += 1
                else:
                    i += 1
            choice1b = random.randint(0,nd)
            while choice1b == choice1a or choice1b in clues: 
                choice1b = random.randint(0,nd)
            if doors[choice1a] == 'car':
                successes['notSwitched'] += 1
            elif doors[choice1b] == 'car':
                successes['switched'] += 1
        if Comments:
            print('*******************************')
            print('Monty Hall game successes count')
            print('Number of doors: %d' % numberOfDoors)
            print('Number of clues: %d' % numberOfClues)
            print('Sampling size  : %d' % sampling)
            print('Random seed    : %d' % seed)
            print('----------------------------------')
            print('Switched    : %d (%.4f); Theoretical probability: %.4f' %\
                  ( successes['switched'],
                  ( successes['switched']/sampling),
                  ( (numberOfDoors-1) /\
                    (numberOfDoors*(numberOfDoors-1-numberOfClues)) )
                  )
                 )
            print('Not switched: %d (%.4f); Theoretical probability: %.4f' %\
                  ( successes['notSwitched'],
                    (successes['notSwitched']/sampling),
                    (1/numberOfDoors)
                  )
                 )
            
        return successes

#----------testing the code ----------------
if __name__ == "__main__":

    print("""
    ****************************************************
    * Digraph3 randomNumbers module                    *
    * Copyright (C) 2010-2021 Raymond Bisdorff         *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    m = MontyHallGameSimulator(numberOfDoors=6,numberOfClues=0)
    m.simulate(100000,1)
    m = MontyHallGameSimulator(numberOfDoors=6,numberOfClues=4)
    m.simulate(numberOfTrials=1000,seed=1)
    
##    brg = BinomialRandomVariable()
##    print(brg.random())

##    from randomNumbers import IncrementalQuantilesEstimator
##    import random
##    random.seed(1)
##    iqAgent = IncrementalQuantilesEstimator(nbuf=100)
##    # feeding the iqAgent with standard Gaussian random numbers 
##    for i in range(1000):
##        iqAgent.add(random.gauss(mu=0,sigma=1))
##    # reporting the estimated Gaussian quartiles
##    print(iqAgent.report(0.0))
##    #    -2.961214270519158
##    print(iqAgent.report(0.25))
##    #    -0.6832621550224423
##    print(iqAgent.report(0.50))
##    #    -0.014392849958746522
##    print(iqAgent.report(0.75))
##    #    0.7029655732010196
##    print(iqAgent.report(1.00))
##    #    2.737259509189501
##    random.seed(1)
##    #iqAgent = IncrementalQuantilesEstimator(nbuf=100)
##    # feeding the iqAgent with standard Gaussian random numbers
##    listDatum = []
##    for i in range(1000):
##        listDatum.append(random.gauss(mu=0,sigma=1))
##    iqAgent.addList(listDatum,historyWeight=0.0)
##    # reporting the estimated Gaussian quartiles
##    print(iqAgent.report(0.0))
##    #    -2.961214270519158
##    print(iqAgent.report(0.25))
##    #    -0.6832621550224423
##    print(iqAgent.report(0.50))
##    #    -0.014392849958746522
##    print(iqAgent.report(0.75))
##    #    0.7029655732010196
##    print(iqAgent.report(1.00))
##    #    2.737259509189501
##    listDatum = []
##    for i in range(1000):
##        listDatum.append(random.gauss(mu=0,sigma=1))
##    iqAgent.addList(listDatum,historyWeight=0.5)
##    # reporting the estimated Gaussian quartiles
##    print(iqAgent.report(0.0))
##    #    -2.961214270519158
##    print(iqAgent.report(0.25))
##    #    -0.6832621550224423
##    print(iqAgent.report(0.50))
##    #    -0.014392849958746522
##    print(iqAgent.report(0.75))
##    #    0.7029655732010196
##    print(iqAgent.report(1.00))
##    #    2.737259509189501
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
#####################################
