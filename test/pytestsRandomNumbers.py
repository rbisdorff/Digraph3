#######################
# R. Bisdorff
# randomNumbers.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsRandomNumbers.py
# # Current $Revision:  $
########################
from randomNumbers import *

def testIqAgent():
    print('==>> Testing the iqagent')
    import random
    random.seed(1)
    iqAgent = IncrementalQuantilesEstimator(nbuf=100,Debug=True)
    for i in range(200):
        iqAgent.add(random.gauss(20,20))
    print(iqAgent.report(0.0))
    print(iqAgent.report(0.25))
    print(iqAgent.report(0.5))
    print(iqAgent.report(0.75))
    print(iqAgent.report(1.0))
    iqAgent.saveState('test.csv')
    iqAgent.loadState('test.csv')
    print(iqAgent.report(0.0))
    print(iqAgent.report(0.25))
    print(iqAgent.report(0.5))
    print(iqAgent.report(0.75))
    print(iqAgent.report(1.0))

def testIqAgentHistoryWeight():
    print('==>> Testing add listDatum with historyWeight')
    from randomNumbers import IncrementalQuantilesEstimator
    import random
    random.seed(1)
    iqAgent = IncrementalQuantilesEstimator(nbuf=100)
    # feeding the iqAgent with standard Gaussian random numbers 
    for i in range(1000):
        iqAgent.add(random.gauss(mu=0,sigma=1))
    # reporting the estimated Gaussian quartiles
    print(iqAgent.report(0.0))
    #    -2.961214270519158
    print(iqAgent.report(0.25))
    #    -0.6832621550224423
    print(iqAgent.report(0.50))
    #    -0.014392849958746522
    print(iqAgent.report(0.75))
    #    0.7029655732010196
    print(iqAgent.report(1.00))
    #    2.737259509189501
    random.seed(1)
    #iqAgent = IncrementalQuantilesEstimator(nbuf=100)
    # feeding the iqAgent with standard Gaussian random numbers
    listDatum = []
    for i in range(1000):
        listDatum.append(random.gauss(mu=0,sigma=1))
    iqAgent.addList(listDatum,historyWeight=0.0)
    # reporting the estimated Gaussian quartiles
    print(iqAgent.report(0.0))
    #    -2.961214270519158
    print(iqAgent.report(0.25))
    #    -0.6832621550224423
    print(iqAgent.report(0.50))
    #    -0.014392849958746522
    print(iqAgent.report(0.75))
    #    0.7029655732010196
    print(iqAgent.report(1.00))
    #    2.737259509189501
    listDatum = []
    for i in range(1000):
        listDatum.append(random.gauss(mu=0,sigma=1))
    iqAgent.addList(listDatum,historyWeight=0.5)
    # reporting the estimated Gaussian quartiles
    print(iqAgent.report(0.0))
    #    -2.961214270519158
    print(iqAgent.report(0.25))
    #    -0.6832621550224423
    print(iqAgent.report(0.50))
    #    -0.014392849958746522
    print(iqAgent.report(0.75))
    #    0.7029655732010196
    print(iqAgent.report(1.00))
    #    2.737259509189501


def testDiscreteRandomVariable():
    print('==>> Testing discrete random number generator')
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

def testExtendedTriangularRandomVariable():
    print('==>> Testing extended triangular number generator')
    from math import floor
    rdv1 = ExtendedTriangularRandomVariable(seed=1)
    rdv2 = ExtendedTriangularRandomVariable(lowLimit=1,
                                            highLimit=2,
                                            mode=1.25,
                                            probRepart=0.5,
                                            seed=1)

    ## sample discrete random variable and count frequencies of obtained values
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

def testCauchyRandomVariable():
    print('==>> Testing Cauchy number generator')
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

def testUniformityOfQuasiRandomPointSet():
    print('==>> Testing the uniformity of a quasi random point set')
    print('Quasi random Korobov sampling')
    seed=101
    d=3
    kor = QuasiRandomKorobovPointSet(n=997,s=d,a=383,Randomized=True,seed=seed,Debug=False)
    print(kor.__dict__.keys())
    print(kor.pointSet[:10])
    print(kor.pointSetCardinality)
    print(kor.testFct(seq=kor.pointSet,buggyRegionLimits=(0.45,0.55)))

    print('Mersenne Twister random sampling')
    randSeq = []
    import random
    random.seed(seed)
    for i in range(997):
        point = []
        for j in range(d):
            point.append(random.random())
        randSeq.append(point)
    print(kor.testFct(seq=randSeq,buggyRegionLimits=(0.45,0.55)))

    print('Quasi random Farey sampling')
    qrfs = QuasiRandomFareyPointSet(n=55,s=d,Randomized=True,seed=seed)
    print(qrfs.__dict__.keys())
    print(qrfs.fareySeries[:10])
    print(qrfs.shuffledFareySeries[:10])
    print(qrfs.seriesLength)
    print(qrfs.pointSet[:5])
    print(qrfs.pointSetCardinality)
    print(qrfs.testFct(seq=qrfs.pointSet,buggyRegionLimits=(0.45,0.55)))

    print('Quasi random uniform sampling')
    qrus = QuasiRandomUniformPointSet(n=997,s=d,Randomized=True,seed=seed)
    print(qrus.__dict__.keys())
    print(qrus.uniformSeries[:10])
    print(qrus.shuffledUniformSeries[:10])
    print(qrus.seriesLength)
    print(qrus.pointSet[:5])
    print(qrus.pointSetCardinality)
    print(qrus.testFct(seq=qrfs.pointSet,buggyRegionLimits=(0.45,0.55)))
    kor.testUniformityDiscrepancy(k=3,fileName='korobovTest')
    qrfs.testUniformityDiscrepancy(k=3,fileName='fareyTest')
    qrus.testUniformityDiscrepancy(k=3,fileName='uniformTest')
    qrfs.testUniformityDiscrepancy(k=3,pointSet=randSeq,fileName='randTest')
    
