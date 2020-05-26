from outrankingDigraphs import *
t = PerformanceTableau('studentenSpiegel04')
t.showHTMLPerformanceTableau(title='Student gradings: 1 (weak), 2 (fair), 3 (good)',ndigits=0)

# ranking
input('Ranking with heatmap')
t.showHTMLPerformanceHeatmap(Correlations=True,colorLevels=5,pageTitle='Ranking with heatmap of the assessments',ndigits=0)

# best choice
g = BipolarOutrankingDigraph(t,Normalized=True)
input('Best choice recommendation')
g.showHTMLBestChoiceRecommendation()

# relative quantiles sorting
from sortingDigraphs import *
qs = QuantilesSortingDigraph(t,'deciles')
input('deciles sorting')
qs.showHTMLQuantileOrdering(title='Deciles sorting of the universities',strategy='average')

# absolute quantiles rating
from performanceQuantiles import *
pq = PerformanceQuantiles(t,numberOfBins=7,LowerClosed=False)
nqs = NormedQuantilesRatingDigraph(pq,t)
input('7-tiled rating heatmap')
nqs.showHTMLRatingHeatmap(ndigits=0,colorLevels=5,Correlations=True,pageTitle='3-tiled rating of the universities')

