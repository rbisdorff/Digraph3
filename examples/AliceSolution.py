from outrankingDigraphs import *
#t = XMCDA2PerformanceTableau('Alice')
t = PerformanceTableau('AliceChoice')
t.showActions()
t.showHTMLCriteria()
g = BipolarOutrankingDigraph(t,Normalized=True)
g.showConsiderablePerformancesPolarisation()
print(g.computeCondorcetWinners())
print(g.computeWeakCondorcetWinners())
print(g.computeChordlessCircuits())
g.showBestChoiceRecommendation()
(~(-g)).exportGraphViz(fileName='test',bestChoice=['ID-FH-K'],worstChoice=['TD-FH-M', 'TD-UD', 'TD-UHB', 'TD-USB'])

