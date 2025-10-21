from mpOutrankingDigraphs import *
def testMPBipolarOutrankingDigraph():
    print('*------- Testing MPBipolarOutrankingDigraph class ----*')
    if __name__ == '__main__':
        import sys
        from randomPerfTabs import Random3ObjectivesPerformanceTableau
        pt = Random3ObjectivesPerformanceTableau(
                                  numberOfActions=1000,seed=2,
            commonScale=(0.0,1000.0))
        from time import time
        t0 = time()
        bg = MPBipolarOutrankingDigraph(argPerfTab=pt,Normalized=True,
                                        startMethod='spawn',
                                        nbrCores=None,Comments=True)
        print(bg)
        print('Run time: %.4f' % (time() - t0) )
        # concurrent.futures multiple interpreters Python3.14+
        t0 = time()
        bg = MPBipolarOutrankingDigraph(argPerfTab=pt,Normalized=True,
                                    startMethod='forkserver',
                                    MultipleInterpreters=True,
                                    nbrCores=None,Comments=True)
        print(bg)
        print('Run time: %.4f' % (time() - t0) )
