###############################
# Digraph3 tutorials
# R. Bisdorff (c) 2020
# # Url: https://www.spiegel.de/thema/studentenspiegel/
# Ref: Der Spiegel 48/2004 p.181
###################################

from outrankingDigraphs import *
t = PerformanceTableau('the_cs_2016')
print(t)
t.showCriteria()

##### show actions
for x in t.actions:
    print('%s:\t%s (%s)' % (x,t.actions[x]['name'],t.actions[x]['comment']) )

###### show objectives
print('THE ranking objectives')
for obj in t.objectives:
    print('%s: %s (%.1f%%),\n\t%s' %\
           (obj,
            t.objectives[obj]['name'],
            t.objectives[obj]['weight'],
            t.objectives[obj]['comment'])
            )

###### show criteria
print('THE performance criteria')
for g in t.criteria:
    print('%s: %s,\t%s (%.1f%%)' %\
           (g,t.criteria[g]['name'],t.criteria[g]['comment'],
            t.criteria[g]['weight']) )

##### compute THE ranking by average score
theScores = []
for x in t.actions:
    xScore = Decimal('0')
    for g in t.criteria:
        xScore += t.evaluation[g][x] * (t.criteria[g]['weight']/Decimal('100'))
    theScores.append((xScore,x))
theScores.sort(reverse=True)
theRanking = [it[1] for it in theScores]

##### show performance evaluations and overall average score
print('##  Univ \tgtch  gres  gcit  gint  gind  average')
print('-----------------------------------------------------')
crit = [g for g in t.criteria]
i = 1
for it in theScores:
    x = it[1]
    xScore = it[0]
    print('%2d: %s' % (i,x), end=' \t')
    for g in crit:
        print('%.1f ' % (t.evaluation[g][x]),end=' ')
    print(' %.1f' % xScore)
    i += 1
    
### the robust outranking digraph
rdg = RobustOutrankingDigraph(t)
print(rdg)
rdg.computeIncomparabilityDegree(Comments=True)
rdg.computeTransitivityDegree(Comments=True)
rdg.computeSymmetryDegree(Comments=True)
rdg.computeChordlessCircuits()
rdg.showChordlessCircuits()
rdg.showRelationTable(actionsSubset= ['albt','unlu','ariz','hels'],\
                          Sorted=False)

### the NetFlows ranking
nfRanking = rdg.computeNetFlowsRanking()
print(' NetFlows ranking       gtch  gres  gcit  gint  gind   THE ranking')
for i in range(75):
    x = nfRanking[i]
    nfxScore = rdg.netFlowsRankingDict[x]['netFlow']
    thexScore,thex = theScores[i]
    print('%2d: %s (%.2f) ' % (i+1,x,nfxScore), end=' \t')
    for g in crit:
        print('%.1f ' % (t.evaluation[g][x]),end=' ')
    print(' %s (%.2f)' % (thex,thexScore) )

### computing NetFloes scores
xethz = Decimal('0')
x = 'ethz'
for y in rdg.actions:
    if x != y:
        xethz += (rdg.relation[x][y] - rdg.relation[y][x])
print(x, xethz)

### NetFlows ranking quality assessments
rdg.showPairwiseOutrankings('ethz','calt')

rdg.showHTMLRelationMap(rankingRule='NetFlows',\
                  tableTitle='Robust Outranking Map')

corrnf = rdg.computeRankingCorrelation(nfRanking)
rdg.showCorrelation(corrnf)

rdg.showRankingConsensusQuality(nfRanking)

### criteria correlation PCA
rdg.showCriteriaCorrelationTable()
rdg.export3DplotOfCriteriaCorrelation(graphType='png')

### THE ranking quality assessments
theRanking = [item[1] for item in theScores]
corrthe = rdg.computeRankingCorrelation(theRanking)
rdg.showCorrelation(corrthe)
rdg.showHTMLPerformanceHeatmap(WithActionNames=True,\
                                   outrankingModel='this',\
				   rankingRule='NetFlows',\
				   ndigits=1,\
				   Correlations=True,\
                               fromIndex=0,toIndex=25)
