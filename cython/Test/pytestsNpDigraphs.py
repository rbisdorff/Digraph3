from cRandPerfTabs import *
from cnpBipolarDigraphs import * 

def testNpDigraphs():
    print('===> test npBipolarOutrankingDigraph class')
    na = 20
    nc = 13
    pt = cRandom3ObjectivesPerformanceTableau(numberOfActions = na,
                                   numberOfCriteria = nc,
                                   seed = 1)
    g = npBipolarOutrankingDigraph(pt)
    print(g)
    g.showPreKernels()
    (-(~g)).showPreKernels()
    g.computePreKernels()
    print(g.dompreKernels)
    print(g.abspreKernels)
    g.showChordlessCircuits()
    from outrankingDigraphs import BipolarOutrankingDigraph
    pt1 = pt.convert2Standard()
    g1 = BipolarOutrankingDigraph(pt1)
    print(g1)
    g1.showPreKernels()
    (-(~g1)).showPreKernels()
    g1.showChordlessCircuits()
