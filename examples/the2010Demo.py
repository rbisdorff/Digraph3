from outrankingDigraphs import *
t = PerformanceTableau('theRanking2010')

input('Performance tableau')
t.showHTMLPerformanceHeatmap(colorLevels=5,\
                rankingRule=None,\
                pageTitle='Performance Tableau \'theRanking10\'')
# best choice
g = BipolarOutrankingDigraph(t)
input('Best choice recommendation')
g.showHTMLBestChoiceRecommendation()

from sortingDigraphs import *
qs = QuantilesSortingDigraph(t,limitingQuantiles=17,LowerClosed=False)
input('17-tiles sorting')
qs.showSorting()
input('17-tiles qunatile ordering')
qs.showQuantileOrdering(strategy='average')

input('Ranking with heatmap')
t.showHTMLPerformanceHeatmap(colorLevels=5,rankingRule='NetFlows',
    Correlations=True,pageTitle='Performance Tableau \'theRanking10\'')

# absolute quantiles rating
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=9,LowerClosed=False)
nqs = NormedQuantilesRatingDigraph(pq,t)
input('9-tiled rating heatmap')
nqs.showHTMLRatingHeatmap(ndigits=0,colorLevels=5,Correlations=True,pageTitle='3-tiled rating of the universities')
