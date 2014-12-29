#######################
# R. Bisdorff
# randomNumbers.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsRandomNumbers.py
# # Current $Revision:  $
########################
from randomNumbers import *

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

