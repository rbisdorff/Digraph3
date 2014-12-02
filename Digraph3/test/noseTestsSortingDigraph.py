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
from weakOrders import *

def testDefaultSortingDigraph():
    print('*---- testing default instantiation of the SortingDigraph Class ---*')
    s = SortingDigraph(isRobust=False)
    s.showCriteriaCategoryLimits()
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
    s1 = SortingDigraph(t,LowerClosed=False)
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
    
