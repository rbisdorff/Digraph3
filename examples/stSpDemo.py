###############################
# Digraph3 tutorials
# R. Bisdorff (c) 2020
# # Url: https://www.spiegel.de/thema/studentenspiegel/
# Ref: Der Spiegel 48/2004 p.181
###################################

from outrankingDigraphs import *
t = PerformanceTableau('studentenSpiegel04')
print(t)
t.computeMissingDataProportion(Comments=True)
disciplines = [t for t in t.criteria]
t.showHTMLPerformanceHeatmap(\
                  criteriaList=disciplines,ndigits=1,rankingRule=None)
t.showHTMLCriteria()

###########
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9)
pq.showHTMLLimitingQuantiles(Transposed=True,Sorted=False)

###########
from sortingDigraphs import *
nqr = NormedQuantilesRatingDigraph(pq,t,rankingRule='Copeland')
print(nqr)
nqr.showHTMLRatingHeatmap(rankingRule='Copeland',Correlations=True,ndigits=1)
nqr.showQuantilesRating()
nqr.exportRatingGraphViz('ratingResult',graphSize='12,12')

#############
nqr1 = NormedQuantilesRatingDigraph(pq,t,rankingRule='NetFlows')
from transitiveDigraphs import *
rankings = [nqr.actionsRanking,
            nqr1.actionsRanking]
rf = RankingsFusion(nqr1,rankings)
rf.exportGraphViz(fileName='fusionResult',WithRatingDecoration=True,graphType='png',graphSize='30,30')
# For decorating the 9-tiles lower limits the fusionResult.dat file
# may be edited by hand like in the ratingResult.dot
# fileshape = "box", fillcolor=lightcoral, style=filled,

###################
g = BipolarOutrankingDigraph(t)
print(g)
g.computeTransitivityDegree(Comments=True)
g.computeSymmetryDegree(Comments=True)
g.computeChordlessCircuits()
g.showChordlessCircuits()

############
qs = QuantilesSortingDigraph(t,9,LowerClosed=True)
qs.showHTMLQuantileOrdering(strategy='average')
qs.exportGraphViz(graphSize='12,12')


