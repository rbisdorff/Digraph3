#######################
# R. Bisdorff 
# sortingDigraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsSortingDigraph.py
# # Current $Revision$
########################

from digraphs import *
from time import time

############# test sortingDigraphs ####################
from sortingDigraphs import *
from transitiveDigraphs import *

def testDefaultSortingDigraph():
    print('*---- testing default instantiation of the SortingDigraph Class ---*')
    s = SortingDigraph(isRobust=False)
    s.showCriteriaCategoryLimits()
    s.showActionsSortingResult()
    actions = list(s.getActionsKeys())
    sorting = s.computeSortingCharacteristics(Comments=True)
    actions.sort()
    for x in actions:
        for c in s.orderedCategoryKeys():
            if sorting[x][c]['categoryMembership'] >= s.valuationdomain['med']:
                print('%s in %s = %.2f' % (x,c,sorting[x][c]['categoryMembership']))
    sorts = s._computePessimisticSorting(Comments=False)
    for c in s.orderedCategoryKeys():
        print(c, sorts[c])

def testSortingDigraphComputeWeakOrder():
    print('*---- testing computeWeakOrder() of the SortingDigraph Class ---*')
    t = Random3ObjectivesPerformanceTableau(numberOfActions=25,
                                    numberOfCriteria=13,
                                    weightDistribution='equiobjectives',
                                    missingDataProbability=0.05,
                                    seed=1)
    nt = NormalizedPerformanceTableau(t)
    so = SortingDigraph(t,scaleSteps=7,Debug=True)
    print(so.categories)
    so.saveCategories('testCategories')
    so.showSorting(Reverse=False)
    print('optimistic')
    so.showWeakOrder(Descending=True,strategy='optimistic')
    print('pessimistic')
    so.showWeakOrder(strategy='pessimistic')
    print('average')
    so.showWeakOrder()
    so1 = SortingDigraph(nt,'testCategories')
    print(so.computeWeakOrder())
    so1.showWeakOrder()
    print(so1.computeWeakOrder())
    so.exportGraphViz('testWO')
    
    
def testRobustSortingDigraphClass():
    print('*---- testing SortingDigraph class instantiation ---*')
    t = RandomPerformanceTableau(numberOfCriteria=5)
    s = SortingDigraph(t)
    srb = SortingDigraph(t,isRobust=True)
    s.showCriteriaCategoryLimits()
    sorts = s._computePessimisticSorting(Comments=True)
    for c in s.orderedCategoryKeys():
        print(c, sorts[c])
    sorting = s.computeSortingCharacteristics(Comments=True)
    robustSorting = srb.computeSortingCharacteristics(Comments=True)
    actions = list(s.getActionsKeys())
    actions.sort()
    for x in actions:
        for c in s.orderedCategoryKeys():
            if sorting[x][c]['categoryMembership'] >= s.valuationdomain['med']:
                print('%s in %s = %.2f (%d)' % (x,c,sorting[x][c]['categoryMembership'],robustSorting[x][c]['categoryMembership']))

def testShowSortingMethod():
    print('*---- testing showSorting method ----*')
    t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=5)
    s = SortingDigraph(t,scaleSteps=5)
    html = s.showSorting(isReturningHTML=True)
    html += s.showSorting(Reverse=False,isReturningHTML=True)
    s.saveProfilesXMCDA2()
    fo = open('test.html','w')
    fo.write(html)
    fo.close()

def testSaveProfilesXMCDA2():
    print('*---- testing saveProfilesXMCDA2  method ----*')
    t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=5)
    s = SortingDigraph(t,scaleSteps=5)
    s.showSorting()
    s.saveProfilesXMCDA2()

def testIConstructorLowerOpenCategories():
    print('*-------- Testing lowerOpen Categories -------')
    s = SortingDigraph(scaleSteps=5)
    s.criteriaCategoryLimits['LowerClosed']= False
    s.relation = s._constructRelation(s.criteria,s.evaluation,terminal=s.actionsOrig,initial=s.profileLimits,hasNoVeto=False, hasBipolarVeto=True)
    s.sorting = s.computeSortingCharacteristics()
    s.showSorting(Reverse=True)
    s.showCriteriaCategoryLimits()

def testLowerOpenClosedCategories():
    print('*-------- Testing lowerClosedOpen Categories -------')
    t = RandomCBPerformanceTableau()
    t.save('test')
    s = SortingDigraph(t,LowerClosed=True)
    s.showSorting(Reverse=True)
    s1 = SortingDigraph('test',LowerClosed=False)
    s1.showSorting(Reverse=True)

def testQuantilesSortingDigraph():
    print('*-------- Testing QuantilesSortingDigraph class 1 -------')
    t = RandomCBPerformanceTableau(numberOfActions=20)
    t.saveXMCDA2('test')
    s0 = QuantilesSortingDigraph(t,limitingQuantiles="deciles",
                                LowerClosed=True,
                                outrankingType='bipolar',
                                Debug=False)
    print(s0.categories)
    s0.showSorting(Reverse=True)
    s0.showSorting(Reverse=False)
    sortingRelation = s0.computeSortingRelation()
    s0.showRelationTable(actionsSubset=s0.actionsOrig,relation=sortingRelation)
    s0.showOrderedRelationTable()
    s0.showWeakOrder(Descending=True)
    s0.exportGraphViz(graphType="png")

def testActionsSortingResult():
    print('*-------- Testing QuantilesSortingDigraph class 2 -------')
    t = RandomCBPerformanceTableau(numberOfActions=15,
                                   numberOfCriteria=13,
                                   weightDistribution='equiobjectives')
    s0 = QuantilesSortingDigraph(t,limitingQuantiles=[0,0.333,0.667,1],
                                LowerClosed=False,
                                Debug=False)
    s0.showSorting(Reverse=True)
    for x in s0.actions:
        s0.showActionCategories(x,Debug=False)
    s0.showActionsSortingResult()
    s0.exportGraphViz('tests0',graphType="pdf")
    s1 = QuantilesSortingDigraph(t,limitingQuantiles=20,
                                LowerClosed=True,
                                Debug=False)
    s1.showSorting(Reverse=False)
    s1.showActionsSortingResult()
    s1.exportGraphViz('tests1',graphType="pdf")
    
def testNormedQuantilesRatingDigraph():
    print('*-------- Testing NormedQuantilesRatingDigraph class -------')
    from randomPerfTabs import RandomCBPerformanceTableau
    from randomPerfTabs import RandomPerformanceGenerator
    import random
    seed = random.randint(1,100)
    #seed = 15
    print('=== >> seed = ',seed)
    nbrActions=1000
    nbrCrit = 13
    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,NegativeWeights=True,
                                    numberOfCriteria=nbrCrit,seed=seed)
    tp.convertWeights2Positive()
    pq = PerformanceQuantiles(tp,'deciles',LowerClosed=False,Debug=False)
    tpg = RandomPerformanceGenerator(tp,instanceCounter=0,seed=seed*2)
    newActions = tpg.randomActions(10)
    pq.updateQuantiles(newActions,historySize=100)
    nrq = NormedQuantilesRatingDigraph(pq,newActions,
                                       WithSorting=True,
                                       Debug=False)
    nrq.showQuantilesRating()
    nrq.exportRatingGraphViz(graphType='pdf')
    nrq.showSorting()
    nrq.showActionsSortingResult()
    nrq.showQuantilesSorting()
    newActions = tpg.randomPerformanceTableau(1000)
    pq.updateQuantiles(newActions,historySize=0)
    newActions = tpg.randomActions(10)
    pq.updateQuantiles(newActions,historySize=None,Debug=False)
    nrq = NormedQuantilesRatingDigraph(pq,newActions,quantiles='heptiles',
                                       WithSorting=True,
                                       Debug=False)
    nrq.showQuantilesRating()
    nrq.exportRatingGraphViz(graphType='pdf')
    nrq.showSorting()
    nrq.showActionsSortingResult()
    nrq.showQuantilesSorting()
    print(pq.computeQuantileProfile(0.5))
    pq.save(fileName='testPerfQuant')
    pq1 = PerformanceQuantiles('testPerfQuant')
    nrq1 = NormedQuantilesRatingDigraph(pq1,newActions,
                                       WithSorting=False,
                                       Debug=False)
    nrq1.showQuantilesRating()



