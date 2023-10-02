from outrankingDigraphs import *
t = PerformanceTableau('graffiti03')
#t.showHTMLPerformanceTableau(title='Graffiti Star wars',ndigits=0)
t.showHTMLPerformanceHeatmap(WithActionNames=True,
                             pageTitle='Graffiti Star wars',
                             rankingRule=None,colorLevels=5,
                             ndigits=0)

# ranking
input('Ranking with heatmap')
t.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=5,
                             pageTitle='Ranking the movies',
                             rankingRule='NetFlows',
                             ndigits=0)

# best choice
g = BipolarOutrankingDigraph(t,Normalized=True)
input('Best choice recommendation')
g.showHTMLBestChoiceRecommendation()

# relative quantiles sorting
from sortingDigraphs import *
qs = QuantilesSortingDigraph(t,'deciles')
input('Deciles sorting')
qs.showHTMLQuantileOrdering(title='Deciles preordering of the movies')

# absolute quantiles rating
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=10,LowerClosed=True)
nqs = NormedQuantilesRatingDigraph(pq,t,rankingRule='Copeland')
input('Deciles Rating heatmap')
nqs.showHTMLRatingHeatmap(ndigits=0,colorLevels=5,Correlations=True,pageTitle='Deciles rating of the movies')

