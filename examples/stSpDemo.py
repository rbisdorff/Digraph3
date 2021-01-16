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
#t.showHTMLPerformanceHeatmap(\
#                  criteriaList=disciplines,ndigits=1,rankingRule=None)
#t.showHTMLCriteria()

###########
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9)
#pq.showHTMLLimitingQuantiles(Transposed=True,Sorted=False)

###########
from sortingDigraphs import *
nqr = LearnedQuantilesRatingDigraph(pq,t,rankingRule='Copeland')
print(nqr)
nqr.showHTMLRatingHeatmap(rankingRule='Copeland',Correlations=True,ndigits=1)
nqr.showQuantilesRating()
nqr.exportRatingByRankingGraphViz('ratingResult',graphSize='12,12')

#############
nqr1 = NormedQuantilesRatingDigraph(pq,t,rankingRule='NetFlows')
from transitiveDigraphs import *
rankings = [nqr.actionsRanking,
            nqr1.actionsRanking]
print(rankings)
rf = RankingsFusion(nqr1,rankings)
rf.exportGraphViz(fileName='fusionResult',WithRatingDecoration=True,graphType='png',graphSize='30,30')

###################
nqr.showActionsSortingResult()
nqr.showHTMLQuantilesSorting()
nqr.exportRatingBySortingGraphViz('nineTilingDrawing',graphSize='12,12')




