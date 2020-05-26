from outrankingDigraphs import *
t = PerformanceTableau('zeitRanking2005')

input('Performance tableau')
t.showHTMLPerformanceHeatmap(colorLevels=5,\
                rankingRule=None,\
                pageTitle='Performance Tableau \'Zeit Ranking 2005\'')

from sortingDigraphs import *
qs = QuantilesSortingDigraph(t,limitingQuantiles=7,LowerClosed=False)
input('7-tiles sorting')
qs.showSorting()
input('7-tiles qunatile ordering')
qs.showQuantileOrdering(strategy='average')

input('Ranking with heatmap')
t.showHTMLPerformanceHeatmap(colorLevels=5,rankingRule='NetFlows',
    Correlations=True,pageTitle='Performance Tableau \'Zeit Ranking 2006\'')

# absolute quantiles rating
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9,LowerClosed=False)
nqs = NormedQuantilesRatingDigraph(pq,t)
input('9-tiled rating heatmap')
nqs.showHTMLRatingHeatmap(ndigits=0,colorLevels=5,Correlations=True,pageTitle='3-tiled rating of the universities')

# best choice from preranked digraph
from sparseOutrankingDigraphs import *
prg = PreRankedOutrankingDigraph(t,5)
input('5-tiles preranked relation map')
prg.showHTMLRelationMap()
input('Preranked Best choice recommendation')
prg.showBestChoiceRecommendation()
