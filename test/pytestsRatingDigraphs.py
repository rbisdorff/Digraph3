#######################
# R. Bisdorff
# pytest functions for the ratingDigraphs module
# ..$python3 -m pip install pytest  # installing the pytest package
########################


def testRelativeQuantilesRatingDigraph():
    print('*-------- Testing Relative Quantiles RatingDigraph class -------')
    from ratingDigraphs import RatingByRelativeQuantilesDigraph
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    from time import time
    t = Random3ObjectivesPerformanceTableau(numberOfActions=50,seed=100)
    rqr = RatingByRelativeQuantilesDigraph(t,quantiles="deciles",
                                LowerClosed=False,CopyPerfTab=False,
                                           rankingRule='Copeland',
                                Debug=False)
    print(rqr)
    rqr.showRatingByQuantilesSorting()
    rqr.showRatingByQuantilesRanking()
    rqr.showAllQuantiles()
    rqr.showCriteriaQuantileLimits(ByCriterion=True)
    rqr.showHTMLPerformanceHeatmap()
    rqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    rqr.showSorting()
    rqr.showHTMLSorting()
    rqr.showSortingCharacteristics()
    rqr.exportRatingBySortingGraphViz('sortRel')
    rqr.exportRatingByRankingGraphViz('rankRel')

def testConfidentRelativeQuantilesRatingDigraph():
    print('*-------- Testing Relative Quantiles confident RatingDigraph  -------')
    from ratingDigraphs import RatingByRelativeQuantilesDigraph
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    from time import time
    t = Random3ObjectivesPerformanceTableau(numberOfActions=50,seed=100)
    rqr = RatingByRelativeQuantilesDigraph(t,quantiles="deciles",
                                LowerClosed=False,CopyPerfTab=False,
                                           rankingRule='Copeland',
                                outrankingModel='confident',
                                Debug=False)
    print(rqr)
    rqr.showRatingByQuantilesSorting()
    rqr.showRatingByQuantilesRanking()
    rqr.showAllQuantiles()
    rqr.showCriteriaQuantileLimits(ByCriterion=True)
    rqr.showHTMLPerformanceHeatmap()
    rqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    rqr.showSorting()
    rqr.showHTMLSorting()
    rqr.showSortingCharacteristics()
    rqr.exportRatingBySortingGraphViz('sortConfRel')
    rqr.exportRatingByRankingGraphViz('rankConfRel')

def testRobustRelativeQuantilesRatingDigraph():
    print('*-------- Testing Relative Quantiles Robust RatingDigraph -------')
    from ratingDigraphs import RatingByRelativeQuantilesDigraph
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    from time import time
    t = Random3ObjectivesPerformanceTableau(numberOfActions=50,seed=100)
    rqr = RatingByRelativeQuantilesDigraph(t,quantiles="deciles",
                                LowerClosed=False,CopyPerfTab=False,
                                           rankingRule='Copeland',
                                outrankingModel='robust',
                                Debug=False)
    print(rqr)
    rqr.showRatingByQuantilesSorting()
    rqr.showRatingByQuantilesRanking()
    rqr.showAllQuantiles()
    rqr.showCriteriaQuantileLimits(ByCriterion=True)
    rqr.showHTMLPerformanceHeatmap()
    rqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    rqr.showSorting()
    rqr.showHTMLSorting()
    rqr.showSortingCharacteristics()
    rqr.exportRatingBySortingGraphViz('sortRobRel')
    rqr.exportRatingByRankingGraphViz('rankRobfRel')


def testAbsoluteQuantilesRatingDigraph():
    print('*-------- Testing Learned Quantiles RatingDigraph class -------')
    # generating random historical performance records and quantiles
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    hpt = Random3ObjectivesPerformanceTableau(numberOfActions=1000,seed=2)
    from performanceQuantiles import PerformanceQuantiles
    pq = PerformanceQuantiles(hpt,numberOfBins=10,LowerClosed=True,Debug=False)
    # generating new incoming performance records of the same kind
    from randomPerfTabs import RandomPerformanceGenerator
    tpg = RandomPerformanceGenerator(hpt,instanceCounter=0,seed=3)
    newRecords = tpg.randomActions(20)
    # updating the historical performance quantiles
    pq.updateQuantiles(newRecords,historySize=None)
    # rating the new set of performance records after
    from ratingDigraphs import RatingByLearnedQuantilesDigraph
    lqr = RatingByLearnedQuantilesDigraph(pq,newRecords,
                                          outrankingModel='standard',
                                          rankingRule='NetFlows',
                                          quantiles=7,Debug=False)
    lqr.showRatingByQuantilesSorting(strategy='average')
    lqr.showRatingByQuantilesRanking()    
    lqr.showAllQuantiles()
    lqr.showCriteriaQuantileLimits(ByCriterion=True)
    lqr.showHTMLPerformanceHeatmap()
    lqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    lqr.showSorting()
    lqr.showHTMLSorting()
    lqr.showSortingCharacteristics()

    lqr.exportRatingBySortingGraphViz('sortAbs')
    lqr.exportRatingByRankingGraphViz('rankAbs')

def testConfidentAbsoluteQuantilesRatingDigraph():
    print('*-------- Testing Learned Quantiles Confident RatingDigraph -------')
    # generating random historical performance records and quantiles
    from randomPerfTabs import RandomPerformanceTableau
    hpt = RandomPerformanceTableau(numberOfActions=1000,seed=2)
    from performanceQuantiles import PerformanceQuantiles
    pq = PerformanceQuantiles(hpt,numberOfBins=20,LowerClosed=True,Debug=False)
    # generating new incoming performance records of the same kind
    from randomPerfTabs import RandomPerformanceGenerator
    tpg = RandomPerformanceGenerator(hpt,instanceCounter=0,seed=3)
    newRecords = tpg.randomActions(10)
    # updating the historical performance quantiles
    pq.updateQuantiles(newRecords,historySize=None)
    # rating the new set of performance records after
    from ratingDigraphs import RatingByLearnedQuantilesDigraph
    lqr = RatingByLearnedQuantilesDigraph(pq,newRecords,
                                          outrankingModel='confident',
                                          rankingRule='RankedPairs',
                                          quantiles=7,Debug=False)
    lqr.showRatingByQuantilesSorting(strategy='average')
    lqr.showRatingByQuantilesRanking()    
    lqr.showAllQuantiles()
    lqr.showCriteriaQuantileLimits(ByCriterion=True)
    lqr.showHTMLPerformanceHeatmap()
    lqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    lqr.showSorting()
    lqr.showHTMLSorting()
    lqr.showSortingCharacteristics()

    lqr.exportRatingBySortingGraphViz('sortConfAbs')
    lqr.exportRatingByRankingGraphViz('rankConfAbs')

def testRobustAbsoluteQuantilesConfidentRatingDigraph():
    print('*-------- Testing Learned Quantiles RatingDigraph class -------')
    # generating random historical performance records and quantiles
    from randomPerfTabs import RandomPerformanceTableau
    hpt = RandomPerformanceTableau(numberOfActions=1000,seed=1)
    from performanceQuantiles import PerformanceQuantiles
    pq = PerformanceQuantiles(hpt,numberOfBins=20,LowerClosed=True,Debug=False)
    # generating new incoming performance records of the same kind
    from randomPerfTabs import RandomPerformanceGenerator
    tpg = RandomPerformanceGenerator(hpt,instanceCounter=0,seed=1)
    newRecords = tpg.randomActions(10)
    # updating the historical performance quantiles
    pq.updateQuantiles(newRecords,historySize=None)
    # rating the new set of performance records after
    from ratingDigraphs import RatingByLearnedQuantilesDigraph
    lqr = RatingByLearnedQuantilesDigraph(pq,newRecords,
                                          outrankingModel='robust',
                                          rankingRule='RankedPairs',
                                          quantiles=7,Debug=False)
    lqr.showRatingByQuantilesSorting(strategy='average')
    lqr.showRatingByQuantilesRanking()    
    lqr.showAllQuantiles()
    lqr.showCriteriaQuantileLimits(ByCriterion=True)
    lqr.showHTMLPerformanceHeatmap()
    lqr.showHTMLRatingHeatmap(WithActionNames=True,colorLevels=5,Correlations=True)
    lqr.showSorting()
    lqr.showHTMLSorting()
    lqr.showSortingCharacteristics()

    lqr.exportRatingBySortingGraphViz('sortRobAbs')
    lqr.exportRatingByRankingGraphViz('rankRobAbs')
   

    

    
 
