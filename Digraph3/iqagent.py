#!/usr/bin/env python
#-*- coding: utf-8 -*-
# MICS Computational Statistics
# RB November 2011
###########################################3

class IncrementalQuantileEstimator(object):
    """
    John M. Chambers et al. IQagent python implementation
    Monitoring Networked Applications with incremental Quantile estimation
    Statistical Science 2006 (4):463-475
    Transcription from C++/nr3 implementation
    """

    def __init__(self,nbuf=1000,Debug=False):
        """
        contructor: nbuf := buffersize (default = 1000)
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
                print '-->> enter quantile iq: ', iq
                print '        tnew, target ' ,tnew,target
            if tnew < target:
                # find a succession of abcissa-ordinate pairs (qnew,tnew) that
                # are the discontinuity of value or slope and break to perform
                # an interpolation as we cross each target
                while True:
                    if self.Debug:
                        try:
                            print 'iq, jq, nq, jd, nd, qile[jq], dbuf[jd]',\
                                  iq, jq, nq, jd, nd, qile[jq], dbuf[jd]
                        except:
                            print '\niq, jq, nq, jd, nd, qile[jq]',\
                                  iq, jq, nq, jd, nd, qile[jq]
                    if (jq < nq) and ( (jd >= nd) or (qile[jq] < dbuf[jd]) ):
                        # found slope discontinuity from old cdf
                        qnew = qile[jq]
                        tnew = jd + nt*pval[jq]
                        jq += 1
                        if self.Debug:
                            print 'slope: tnew, target', tnew, target
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
                            print 'value 1: tnew, target', tnew, target
                        if tnew >= target:
                            break
                        told = tnew
                        tnew += 1.0
                        qold = qnew
                        if self.Debug:
                            print 'value 2: tnew, target', tnew, target
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
        return estimated p-quantile (default = median)
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
        save the state of the IncrementalQuantileEstimator self instance
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
    
# ------- for testing purposes --------
if __name__ == "__main__":

    import random
    random.seed(1)
    
    iqAgent = IncrementalQuantileEstimator(nbuf=1000,Debug=True)

    for i in range(2000):
        iqAgent.add(random.gauss(20,20))

    print iqAgent.report(0.0)
    print iqAgent.report(0.25)
    print iqAgent.report(0.5)
    print iqAgent.report(0.75)
    print iqAgent.report(1.0)

    iqAgent.saveState('test.csv')
    iqAgent.loadState('test.csv')

    print iqAgent.report(0.0)
    print iqAgent.report(0.25)
    print iqAgent.report(0.5)
    print iqAgent.report(0.75)
    print iqAgent.report(1.0)

