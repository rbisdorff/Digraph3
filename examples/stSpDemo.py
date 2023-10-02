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

###########
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9)
pq.showHTMLLimitingQuantiles(Transposed=True,Sorted=False)

###########
from sortingDigraphs import *
lqr = LearnedQuantilesRatingDigraph(pq,t,rankingRule='Copeland',Debug=False)
print(lqr)
lqr.showHTMLRatingHeatmap(rankingRule=None,Correlations=True,ndigits=1)
lqr.showQuantilesRating()
lqr.exportRatingByRankingGraphViz('ratingResult',graphSize='12,12')
######
lqr1 = LearnedQuantilesRatingDigraph(pq,t,rankingRule='NetFlows')
from transitiveDigraphs import RankingsFusionDigraph
rankings = [lqr.actionsRanking, lqr1.actionsRanking]
rf = RankingsFusionDigraph(lqr,rankings)
rf.exportGraphViz(fileName='fusionResult',\
                             WithRatingDecoration=True,\
                             graphSize='30,30')
###################
dg = BipolarOutrankingDigraph(t)
print(dg)
dg.computeTransitivityDegree(Comments=True)
dg.computeSymmetryDegree(Comments=True)
dg.computeChordlessCircuits()
dg.showChordlessCircuits()
##
##############
lqr.showActionsSortingResult()
lqr.showHTMLQuantilesSorting(strategy='average')
lqr.exportRatingBySortingGraphViz('nineTilingDrawing',graphSize='12,12')
