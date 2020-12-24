#from perfTabs import *
from outrankingDigraphs import *
t = PerformanceTableau('studentenSpiegel04')
t.showHTMLCriteria()
from linearOrders import *
thlm = PartialPerformanceTableau(t,objectivesSubset=['HLM'])
ghlm = BipolarOutrankingDigraph(thlm)
coph = CopelandRanking(ghlm)
##thlm.showHTMLPerformanceTableau(\
##    title='Faculty Humanities, Law & Management',ndigits=0,\
##    isSorted=False,actionsSubset=coph)
##thlm.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=3,rankingRule='Copeland',
##        pageTitle='Faculty Humanities, Law & Management',
##        ndigits=0)
##
tstm = PartialPerformanceTableau(t,objectivesSubset=['STM'])
gstm = BipolarOutrankingDigraph(tstm)
cops = CopelandRanking(gstm)
fs = FusionDigraph(coph,cops)
##tstm.showHTMLPerformanceTableau(\
##    title='Faculty Sciences, Technology & Medecine',ndigits=0,\
##    isSorted=False,actionsSubset=cops)
##tstm.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=3,
##            rankingRule='Copeland',
##            pageTitle='Faculty Sciences, Technology & Medecine',
##            ndigits=0)
g = BipolarOutrankingDigraph(t)
print(g)
g.computeTransitivityDegree(Comments=True)
g.computeSymmetryDegree(Comments=True)
g.computeChordlessCircuits()
g.showChordlessCircuits()
ranking = g.computeNetFlowsRanking()
g.showHTMLRelationTable(actionsList=ranking)

from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9)
pq.showLimitingQuantiles()

from sortingDigraphs import *
nqr = NormedQuantilesRatingDigraph(pq,t)
nqr.showQuantilesRating()
nqr.exportRatingGraphViz('ratingResult',graphSize='12,12')
